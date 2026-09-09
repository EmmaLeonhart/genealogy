"""Download whole Wikidata items and grow outward from them, resumably.

The job `todo.md` § 8a-revised describes: pull the ~515,000 Wikidata items that
carry a Geni profile ID (P2600), *complete*, then grow the set by walking family
links to items that have none. The result is a Wikidata-side tree accreted item
by item, to be held beside the Geni-side tree that arrives in bulk exports.

**Two queues, which is Emma's design and not an implementation detail.**

1. The **fetch queue** — "take from Wikidata". QIDs known to exist and not yet
   held. It starts as the whole P2600 seed set and is fed by the scan.
2. The **iteration queue** — items already held, waiting to be read for the
   relatives they name. Every relative not already held or queued joins the
   fetch queue; a fetched item joins the **end** of the iteration queue. That
   is the BFS: the frontier is whatever the last round discovered.

**The iteration queue is the shard sequence itself, plus a cursor**, rather than
a second list of QIDs. Items are appended in fetch order, so "the end of the
iteration queue" is "the end of the last shard" for free, and scanning is a
forward read of files already on disk — no random access into 500k items, and
nothing to keep in sync with what is stored.

**AN EMPTY FETCH QUEUE IS NOT CONVERGENCE.** The walk stops when one ``--scan-per-round``
slice discovers nothing *and* the queue is empty — it does **not** check that the cursor
reached the end of the store. At the default slice of 500 that is two thousand items, so a
run announces closure a few hundred shards in and prints ``0 QIDs still queued``. On
2026-08-31 that read as a closed frontier three separate times while the cursor sat at
shard 21 of 2,249; a walk with ``--scan-per-round 150000`` then found **89,832** unknown
relatives, and the pass after it another **87,693**. Discovery per item scanned went 4.0%
to 59%, because newly-fetched people are exactly the ones whose relatives are missing.
**Read the cursor, not the queue length**, and treat "discovered 0" over the opening shards
as meaningless — they are the original P2600 seed region and were expanded long ago.

**Shards are the truth; the index is derived.** Items are appended to gzipped
JSONL shards of a fixed size and those are what gets committed — many ordinary
files that push incrementally, deliberately not one big one that would need LFS.
The QID → status index and the cursor are SQLite, live in ``out/``, and are
rebuilt by re-reading the shards. A binary index committed alongside would be a
second copy of the truth that can disagree with it.

**Appending to a gzip file is legal and is what makes this incremental.** A
``.gz`` holding several concatenated members reads back as one stream, so each
batch becomes one member — durable the moment the request returns, with no shard
rewriting. Compression is per member, which is why a batch is written in one
call rather than an item at a time: 50 items in one member compress; 50 members
of one item do not.

**Nothing here commits or pushes.** The cadence — every 500-1000 items, never
per item — belongs to the caller, and keeping git out of this module is what
lets the tests run without one.

Network access is injected the same way :class:`genimerge.wikidata.WikidataClient`
injects it, so every path below is exercised offline.
"""

from __future__ import annotations

import gzip
import json
import sqlite3
import time
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Iterator, Sequence

from . import wikidata

__all__ = [
    "SHARD_ITEMS",
    "FETCH_BATCH",
    "RELATION_PROPERTIES",
    "ItemStore",
    "StateIndex",
    "WalkStats",
    "relatives",
    "fetch_step",
    "scan_step",
    "walk",
    "seed_qids",
]

#: Items per shard. 1000 keeps a shard in the low megabytes compressed — a size
#: git handles without complaint and a human can decompress and read. Nothing
#: depends on the value, so it can change between runs without invalidating what
#: is already stored.
SHARD_ITEMS = 1000

#: QIDs per ``wbgetentities`` request. The MediaWiki limit for anonymous callers
#: is 50, and it is why the live path is affordable at all: 515k items is ~10,300
#: requests at 50 apiece against 515,000 one at a time. Raising it does not make
#: the run faster, it makes the API reject the request.
FETCH_BATCH = 50

#: How long a heartbeat stays valid. Longer than any single round takes and
#: short enough that a killed run's lock is stale before a supervisor's next
#: tick — five minutes against a run that beats every couple of seconds.
LOCK_STALE_SECONDS = 300

#: The family links the walk follows: father, mother, spouse, child, sibling.
#: § 8a names the first four; P3373 is included because a sibling edge can be the
#: only thing joining two branches on an item whose parents are unrecorded, and
#: it is cheap — an edge to an item already held costs nothing but a set lookup.
#: Every one of these is in `CLAUDE.md`'s property table, which
#: `tests/test_wikidata_ids_documented.py` requires.
RELATION_PROPERTIES = ("P22", "P25", "P26", "P40", "P3373")


def _shard_name(index: int) -> str:
    return f"items-{index:05d}.jsonl.gz"


def relatives(entity: dict) -> list[str]:
    """The QIDs an item names as family, in property then statement order.

    Guards the two ways a claim carries no target: ``novalue``/``somevalue``
    snaks, which have no ``datavalue`` at all, and a datavalue that is not an
    entity id — a date or a string sitting on a relation property, which is
    malformed but does occur. Neither is an error worth stopping for; both would
    be a ``KeyError`` in the obvious version of this function.
    """
    found: list[str] = []
    claims = entity.get("claims") or {}
    for prop in RELATION_PROPERTIES:
        for statement in claims.get(prop) or []:
            snak = statement.get("mainsnak") or {}
            if snak.get("snaktype") != "value":
                continue
            value = (snak.get("datavalue") or {}).get("value")
            qid = value.get("id") if isinstance(value, dict) else None
            if isinstance(qid, str) and qid.startswith("Q"):
                found.append(qid)
    return found


@dataclass
class ItemStore:
    """Gzipped JSONL shards holding whole Wikidata items.

    One JSON object per line, exactly as ``wbgetentities`` returned it, with no
    reshaping: what a later phase wants out of an item is not yet known, and an
    item stored lossily has to be fetched again.
    """

    directory: Path
    per_shard: int = SHARD_ITEMS

    def __post_init__(self) -> None:
        self.directory = Path(self.directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._shard_index, self._shard_count = self._resume_point()

    # -- layout --------------------------------------------------------

    def shards(self) -> list[Path]:
        return sorted(self.directory.glob("items-*.jsonl.gz"))

    def _resume_point(self) -> tuple[int, int]:
        """Which shard to append to next, and how full it already is.

        Counting the last shard's lines means decompressing it, which is cheap
        for one shard and is the only way to land on a partly-filled one after a
        kill. Starting a fresh shard every run would leave a directory of stubs
        after a flaky day.

        It is also where a **truncated shard** is repaired. A batch is written
        as one gzip member; lose power partway through that write and the member
        ends mid-stream. Reading it then raises, and — worse — appending a fresh
        member after the break makes the new items unreachable too, because
        decompression never gets past it. So a shard that will not read is
        rewritten from the lines that do, before anything is appended. The items
        lost with the broken tail were never committed to the index as held, so
        the walk simply fetches them again.
        """
        existing = self.shards()
        if not existing:
            return 0, 0
        last = existing[-1]
        index = int(last.stem.split("-")[1].split(".")[0])
        try:
            return index, sum(1 for _ in _read_lines(last))
        except (EOFError, gzip.BadGzipFile, zlib.error, UnicodeDecodeError):
            return index, self.repair(last)

    def repair(self, shard: Path) -> int:
        """Rewrite a shard from the lines that still decompress. Returns how many.

        Writes beside the shard and renames, so an interrupted repair leaves the
        original in place rather than replacing it with a half-written file.
        """
        kept = list(_read_lines(shard, tolerant=True))
        temporary = shard.with_name(shard.name + ".repair")
        with gzip.open(temporary, "wt", encoding="utf-8", newline="\n") as handle:
            handle.writelines(kept)
        temporary.replace(shard)
        return len(kept)

    @property
    def current_shard(self) -> Path:
        return self.directory / _shard_name(self._shard_index)

    # -- writing -------------------------------------------------------

    def write(self, items: Sequence[dict]) -> Path:
        """Append items as one gzip member. Returns the shard written to.

        The whole batch lands in one shard even if that takes it past
        ``per_shard`` — splitting a batch across two members to honour a round
        number would cost the compression this design exists for, and a shard 4%
        over is not a problem.
        """
        if not items:
            return self.current_shard
        if self._shard_count >= self.per_shard:
            self._shard_index += 1
            self._shard_count = 0
        path = self.current_shard
        payload = "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in items)
        with gzip.open(path, "at", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
        self._shard_count += len(items)
        return path

    # -- reading -------------------------------------------------------

    def read(self, *, after: tuple[str, int] | None = None) -> Iterator[tuple[str, int, dict]]:
        """Walk the store forward, yielding ``(shard name, line, item)``.

        ``after`` resumes past a position already consumed — this is what makes
        the shard sequence usable as the iteration queue. Items appended while a
        walk is in progress are picked up by the next call, because the shard
        list is re-read each time.
        """
        start_shard, start_line = after or ("", -1)
        for shard in self.shards():
            if shard.name < start_shard:
                continue
            for number, line in enumerate(_read_lines(shard)):
                if shard.name == start_shard and number <= start_line:
                    continue
                if line.strip():
                    yield shard.name, number, json.loads(line)

    def items(self) -> Iterator[dict]:
        """Every item in the store, shard order then insertion order.

        A QID appearing twice is possible in principle — a resumed run whose
        index was lost mid-batch — so a reader needing one item per QID must say
        which wins. Here the *later* one does, matching the merge's
        later-sources-win rule.
        """
        for _, _, item in self.read():
            yield item


def _read_lines(path: Path, *, tolerant: bool = False) -> Iterator[str]:
    """Lines of a gzipped shard. ``tolerant`` stops at a truncated tail.

    Tolerance is off by default on purpose: a shard that will not read is
    something the caller should find out about, and silently returning a short
    file is how a store quietly loses items. :meth:`ItemStore.repair` is the one
    place that wants the salvage behaviour.
    """
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        iterator = iter(handle)
        while True:
            try:
                line = next(iterator)
            except StopIteration:
                return
            except (EOFError, gzip.BadGzipFile, zlib.error, UnicodeDecodeError):
                if tolerant:
                    return
                raise
            yield line


@dataclass
class StateIndex:
    """The fetch queue, the walk cursor, and QID → status.

    Derived from the shards and therefore disposable: :meth:`rebuild` restores it
    by re-reading them. It also carries what the shards cannot — attempt counts
    and the last error for a QID that failed — which is why a run that hits a bad
    patch does not retry it forever.
    """

    path: Path
    _conn: sqlite3.Connection = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.path = Path(self.path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path)
        self._conn.executescript(
            "CREATE TABLE IF NOT EXISTS items ("
            " qid TEXT PRIMARY KEY,"
            " status TEXT NOT NULL,"      # queued | done | missing | error
            " shard TEXT,"
            " seq INTEGER,"               # arrival order: the fetch queue is FIFO
            " attempts INTEGER NOT NULL DEFAULT 0,"
            " error TEXT);"
            "CREATE INDEX IF NOT EXISTS items_status ON items (status, seq);"
            "CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT);"
        )
        self._conn.commit()
        # Read once, then kept in memory. Arrival order only has to be
        # monotonic, and one process owns the index for the length of a run.
        self._seq = self._conn.execute("SELECT COALESCE(MAX(seq), 0) FROM items").fetchone()[0]

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "StateIndex":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    # -- queries -------------------------------------------------------

    def status(self, qid: str) -> str | None:
        row = self._conn.execute("SELECT status FROM items WHERE qid = ?", (qid,)).fetchone()
        return row[0] if row else None

    def counts(self) -> dict[str, int]:
        return dict(self._conn.execute("SELECT status, COUNT(*) FROM items GROUP BY status"))

    def held(self) -> set[str]:
        """QIDs needing no further request — stored, or known absent.

        ``error`` is deliberately excluded: an error is a request that may
        succeed next time, and the retry decision belongs to the caller reading
        ``attempts``.
        """
        rows = self._conn.execute("SELECT qid FROM items WHERE status IN ('done', 'missing')")
        return {row[0] for row in rows}

    def known(self) -> set[str]:
        """Every QID the index has seen, queued or settled.

        The scan checks against this rather than against :meth:`held`, or a
        relative already waiting in the fetch queue would be enqueued again by
        every item that names them — which for a well-connected family is most
        of them.
        """
        return {row[0] for row in self._conn.execute("SELECT qid FROM items")}

    def queue_length(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) FROM items WHERE status = 'queued'").fetchone()
        return row[0]

    # -- the fetch queue -----------------------------------------------

    def enqueue(self, qids: Iterable[str]) -> int:
        """Add QIDs to the back of the fetch queue. Returns how many were new.

        ``INSERT OR IGNORE`` on the primary key is the dedup: a QID already
        known — queued, held or errored — is left exactly as it is, so
        re-enqueueing a stored item cannot demote it back to pending.

        One ``executemany`` rather than a statement per QID, and the sequence
        number comes from a counter held in memory rather than a ``SELECT MAX``.
        The obvious version of both was fine on the ten-item tests and took
        longer than five minutes to seed the real 514,822.
        """
        rows = []
        for qid in qids:
            rows.append((qid, self._next_seq()))
        before = self._conn.total_changes
        self._conn.executemany(
            "INSERT OR IGNORE INTO items (qid, status, seq) VALUES (?, 'queued', ?)", rows
        )
        return self._conn.total_changes - before

    def _next_seq(self) -> int:
        self._seq += 1
        return self._seq

    def take(self, count: int) -> list[str]:
        """The next ``count`` QIDs to fetch, oldest first. Does not dequeue.

        They leave the queue when :func:`fetch_step` records their outcome —
        so a crash mid-batch loses nothing, and the same batch is simply
        attempted again.
        """
        rows = self._conn.execute(
            "SELECT qid FROM items WHERE status = 'queued' ORDER BY seq LIMIT ?", (count,)
        )
        return [row[0] for row in rows]

    # -- outcomes ------------------------------------------------------

    def requeue_errors(self, max_attempts: int = 5) -> int:
        """Put failed QIDs back on the queue. Returns how many moved.

        **Without this an outage loses items silently.** A batch that fails is
        marked ``error``, which takes it off the queue — and nothing ever put it
        back, so an internet drop partway through a four-hour run would leave
        those QIDs neither held nor queued and the run would finish "complete"
        with holes in it. Called at the start of every run, so resuming after a
        drop retries what the drop cost.

        ``max_attempts`` stops a QID that fails for its own reasons from being
        retried forever; the attempts already recorded are what it counts.
        """
        cursor = self._conn.execute(
            "UPDATE items SET status = 'queued' WHERE status = 'error' AND attempts < ?",
            (max_attempts,),
        )
        self._conn.commit()
        return cursor.rowcount

    def record(self, qid: str, status: str, *, shard: str = "", error: str = "") -> None:
        self._conn.execute(
            "INSERT INTO items (qid, status, shard, seq, attempts, error)"
            " VALUES (?, ?, ?, ?, 1, ?)"
            " ON CONFLICT(qid) DO UPDATE SET"
            "  status = excluded.status,"
            "  shard = excluded.shard,"
            "  attempts = items.attempts + 1,"
            "  error = excluded.error",
            (qid, status, shard, self._next_seq(), error),
        )

    def commit(self) -> None:
        self._conn.commit()

    # -- the single-run lock -------------------------------------------

    def claim(self, *, stale_after: float = LOCK_STALE_SECONDS, now: Callable[[], float] = time.time) -> bool:
        """Take the run lock, or return False because someone else holds it.

        **This exists because the run is meant to be restarted automatically.**
        Emma's machine interrupts the download constantly, so something has to
        notice and start it again — and the moment that is automatic, the way it
        fails is two copies running at once, both appending to the same shard.
        That corrupts the store rather than merely wasting requests.

        The lock is a heartbeat rather than a PID file: a run refreshes it every
        round, and a run that died leaves one that goes stale on its own. No
        cleanup step to forget, and nothing to check against a process table.

        The check and the write are not one atomic statement, so two processes
        starting in the same microsecond could both claim. Against a supervisor
        that ticks every few minutes that window is not worth a lock table.
        """
        row = self._conn.execute("SELECT v FROM meta WHERE k = 'heartbeat'").fetchone()
        if row:
            try:
                last = float(row[0])
            except (TypeError, ValueError):
                last = 0.0
            if now() - last < stale_after:
                return False
        self.beat(now=now)
        return True

    def beat(self, *, now: Callable[[], float] = time.time) -> None:
        """Refresh the run lock. Called every round, so a crash goes stale."""
        self._conn.execute(
            "INSERT INTO meta (k, v) VALUES ('heartbeat', ?)"
            " ON CONFLICT(k) DO UPDATE SET v = excluded.v",
            (repr(now()),),
        )
        self._conn.commit()

    def release(self) -> None:
        """Drop the lock on a clean exit, so the next run starts immediately."""
        self._conn.execute("DELETE FROM meta WHERE k = 'heartbeat'")
        self._conn.commit()

    # -- the walk cursor -----------------------------------------------

    def cursor(self) -> tuple[str, int] | None:
        row = self._conn.execute("SELECT v FROM meta WHERE k = 'cursor'").fetchone()
        if not row:
            return None
        shard, _, line = row[0].rpartition("|")
        return shard, int(line)

    def set_cursor(self, shard: str, line: int) -> None:
        self._conn.execute(
            "INSERT INTO meta (k, v) VALUES ('cursor', ?)"
            " ON CONFLICT(k) DO UPDATE SET v = excluded.v",
            (f"{shard}|{line}",),
        )

    # -- rebuilding ----------------------------------------------------

    def rebuild(self, store: ItemStore) -> int:
        """Re-derive held items from the shards. Returns how many were found.

        The fetch queue and the cursor are **reset**, not preserved: a queue
        rebuilt from a discarded index would claim the walk had already covered
        ground it has no record of. Re-scanning re-discovers the same relatives,
        which costs local reads and no requests.
        """
        self._conn.execute("DELETE FROM items WHERE status IN ('done', 'queued')")
        self._conn.execute("DELETE FROM meta WHERE k = 'cursor'")
        found = 0
        for shard, _, item in store.read():
            qid = item.get("id")
            if qid:
                self.record(qid, "done", shard=shard)
                found += 1
        self.commit()
        return found


@dataclass
class WalkStats:
    """What the pilot exists to measure, plus how the frontier is behaving."""

    requested: int = 0
    stored: int = 0
    missing: int = 0
    errors: int = 0
    batches: int = 0
    scanned: int = 0
    discovered: int = 0
    bytes_json: int = 0
    seconds: float = 0.0
    #: Set when the circuit breaker tripped, and the reason. Empty on a normal
    #: finish, so a caller can tell "the queue is empty" from "I gave up".
    stopped_early: str = ""

    @property
    def bytes_per_item(self) -> float:
        return self.bytes_json / self.stored if self.stored else 0.0

    @property
    def items_per_second(self) -> float:
        return self.stored / self.seconds if self.seconds else 0.0

    def projection(self, total: int) -> dict[str, float]:
        """Extrapolate to a run of ``total`` items.

        A straight multiplication of a small sample, and it should be read as
        one: a short run has not met the throttling a ten-hour run meets, so the
        hours figure is a floor rather than an estimate.
        """
        return {
            "items": total,
            "requests": total / FETCH_BATCH,
            "hours": (total / self.items_per_second / 3600) if self.items_per_second else 0.0,
            "gigabytes_json": total * self.bytes_per_item / 1e9,
        }


def _resolve(entities: dict) -> dict:
    """Key a ``wbgetentities`` response by the id that was *asked for*.

    Wikidata resolves redirects silently: ask for a QID that has been merged away
    and the item comes back under the target's id, with a ``redirects`` block
    naming where it came from. Keying on the response's own ids therefore loses
    the caller's QID, and the caller then treats it as missing and asks again
    next run.
    """
    resolved = dict(entities)
    for entity in entities.values():
        source = (entity.get("redirects") or {}).get("from")
        if source:
            resolved[source] = entity
    return resolved


def fetch_step(
    client: wikidata.WikidataClient,
    store: ItemStore,
    index: StateIndex,
    stats: WalkStats,
    *,
    batch_size: int = FETCH_BATCH,
) -> int:
    """Take one batch off the fetch queue, store it, record every outcome.

    Returns how many QIDs were attempted — zero means the queue is empty. Every
    QID in the batch is recorded whatever happens, which is what takes it off
    the queue; a batch that raises marks its QIDs ``error`` and the walk carries
    on rather than stopping on one bad response.
    """
    batch = index.take(batch_size)
    if not batch:
        return 0

    stats.batches += 1
    stats.requested += len(batch)
    try:
        entities = client.full_entities(batch)
    except Exception as error:  # noqa: BLE001 - the QIDs must be marked, whatever failed
        stats.errors += len(batch)
        for qid in batch:
            index.record(qid, "error", error=f"{type(error).__name__}: {error}")
        index.commit()
        return len(batch)

    resolved = _resolve(entities)
    keep: list[dict] = []
    for qid in batch:
        entity = resolved.get(qid)
        if entity is None or "missing" in entity:
            # A QID Wikidata no longer serves: deleted, or a P2600 statement
            # pointing at nothing. Settled so the next run does not ask again,
            # and counted separately because a lot of these would say something
            # about the seed list.
            stats.missing += 1
            index.record(qid, "missing")
            continue
        keep.append(entity)

    shard = store.write(keep)
    for entity in keep:
        stats.stored += 1
        stats.bytes_json += len(json.dumps(entity, ensure_ascii=False).encode("utf-8"))
        index.record(entity.get("id", ""), "done", shard=shard.name)
    # A redirected QID is settled too, under the id that was asked for. Without
    # this the next run re-requests it forever: the response came back under the
    # target's id, so nothing ever marks the source done.
    for qid in batch:
        entity = resolved.get(qid)
        if entity is not None and "missing" not in entity and entity.get("id") != qid:
            index.record(qid, "done", shard=shard.name)
    index.commit()
    return len(batch)


def scan_step(
    store: ItemStore,
    index: StateIndex,
    stats: WalkStats,
    *,
    items: int,
    known: set[str] | None = None,
) -> int:
    """Read forward from the cursor, enqueueing relatives not already known.

    Returns how many items were read — zero means the iteration queue has caught
    up with what is stored, which is the walk's real termination condition once
    the fetch queue is also empty.

    ``known`` is the caller's living set of every QID the index has seen, and
    :func:`walk` keeps one across the whole run for a reason: loading it from
    SQLite costs a half-million-row query, which is nothing once and is the
    dominant cost of the job if it happens every round. Passing ``None`` loads
    it, which is what a one-shot caller wants.
    """
    if known is None:
        known = index.known()
    read = 0
    position: tuple[str, int] | None = None

    for shard, line, item in store.read(after=index.cursor()):
        position = (shard, line)
        read += 1
        fresh = [q for q in relatives(item) if q not in known]
        if fresh:
            # Deduplicated against `known` *before* the insert as well as by it,
            # so one item naming the same person twice counts as one discovery.
            unique = list(dict.fromkeys(fresh))
            stats.discovered += index.enqueue(unique)
            known.update(unique)
        if read >= items:
            break

    if position is not None:
        index.set_cursor(*position)
        index.commit()
    stats.scanned += read
    return read


def walk(
    client: wikidata.WikidataClient,
    store: ItemStore,
    index: StateIndex,
    *,
    batch_size: int = FETCH_BATCH,
    scan_per_round: int = 500,
    limit: int | None = None,
    max_consecutive_failures: int = 5,
    progress: Callable[[WalkStats], None] | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> WalkStats:
    """Alternate scanning and fetching until both queues are empty.

    Scanning first, so a resumed run discovers what the last one stored before
    spending a request; and scanning more items per round than a batch fetches,
    because reading local JSON is free and the point is to keep the fetch queue
    supplied rather than to finish the scan.

    ``limit`` caps how many QIDs are *requested*, which is what makes a pilot a
    pilot. It bounds the network, not the scan — stopping the scan early would
    leave the queue short and understate the frontier the pilot is measuring.

    ``max_consecutive_failures`` is the circuit breaker. The internet going away
    makes every batch fail, and without a breaker the walk would sprint through
    the whole queue marking 10,000 batches ``error`` in the time the outage
    lasts. Stopping instead leaves the queue intact, and ``requeue_errors`` on
    the next run returns the few that did fail.
    """
    stats = WalkStats()
    started = clock()
    # Loaded once and maintained by the scan. See scan_step on why.
    known = index.known()
    consecutive_failures = 0

    while True:
        scan_step(store, index, stats, items=scan_per_round, known=known)
        if limit is not None and stats.requested >= limit:
            break
        room = batch_size if limit is None else min(batch_size, limit - stats.requested)
        failures_before = stats.errors
        attempted = fetch_step(client, store, index, stats, batch_size=room)
        index.beat()
        consecutive_failures = consecutive_failures + 1 if stats.errors > failures_before else 0
        stats.seconds = clock() - started
        if progress is not None:
            progress(stats)
        if consecutive_failures >= max_consecutive_failures:
            stats.stopped_early = (
                f"{consecutive_failures} batches failed in a row — stopping rather than "
                "burning the queue. Check the connection and re-run; nothing is lost."
            )
            break
        if attempted == 0:
            # Nothing left to fetch. One more scan settles whether the last
            # batch stored anything that names someone new; if it did not, the
            # walk has closed.
            before = stats.discovered
            scan_step(store, index, stats, items=scan_per_round, known=known)
            if stats.discovered == before and index.queue_length() == 0:
                break

    stats.seconds = clock() - started
    return stats


def seed_qids(path: Path) -> list[str]:
    """The seed set: every QID in ``out/wikidata/p2600-all.tsv``.

    That file is already on disk from `genimerge overlap`, which pulled all of
    P2600 in sixteen partitions — so the seed phase needs no SPARQL at all until
    the map is refreshed. Deduplicated because a QID carrying two Geni IDs
    appears on two lines, which is 44 of them at last count and is a real thing
    rather than a corrupt file.
    """
    seen: dict[str, None] = {}
    with Path(path).open(encoding="utf-8") as handle:
        for line in handle:
            qid = line.split("\t", 1)[0].strip()
            if qid.startswith("Q"):
                seen[qid] = None
    return list(seen)
