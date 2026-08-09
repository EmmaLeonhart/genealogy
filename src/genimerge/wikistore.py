"""Read the local Wikidata dump, so that nothing has to ask Wikidata.

`CLAUDE.md` § *Never query Wikidata to check something* is the reason this
module exists. Every geni↔Wikidata answer in this repo currently runs through
:mod:`genimerge.wikidata`, the SPARQL/API client — `reconcile`, `crosscheck` and
`namelinks` import it directly and `coverage` sits on `reconcile` — so the
questions the 1.4M downloaded items were meant to make free were still only
reachable over the network. This is the offline half of that seam.

**Shards are the truth; this index is derived.** That is
:mod:`genimerge.wikidownload`'s rule and it applies unchanged here: the sqlite
file lives under ``out/`` (gitignored), is rebuilt by re-reading the shards, and
is never committed. A committed index would be a second copy of the truth that
can disagree with it.

**Why an index at all.** The store is 1,408 shards and 2.7 GB gzipped; a full
streaming pass is about six minutes. That is fine once and hopeless as the inner
loop of a join. Indexing QID → *shard* rather than QID → byte offset is the
cheap version that gzip actually supports: a shard is ~1000 items and a couple
of megabytes, so a random lookup decompresses one shard instead of the store.

**This does not emulate SPARQL, deliberately.** The ten ``client.sparql`` call
sites each ask one concrete question, and porting them means answering those
questions from the index one at a time. A general query engine pretending to be
an endpoint would be far more code and would invite exactly the "just quickly
check" habit the rule forbids.
"""

from __future__ import annotations

import gzip
import json
import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Iterator

__all__ = [
    "GENI_ID_PROPERTY",
    "IndexStats",
    "StoreReader",
    "build_index",
    "default_index_path",
    "write_p2600_map",
]

#: Geni.com profile ID. Documented in `CLAUDE.md` § *Wikidata properties*.
GENI_ID_PROPERTY = "P2600"

#: How many rows to accumulate before handing them to sqlite. Large enough that
#: the 1.4M-row build is not a million round trips, small enough to stay small
#: in memory — the whole point of this module is that the store never has to be
#: resident.
WRITE_BATCH = 20000


def default_index_path(out_dir: Path) -> Path:
    """Where the derived index lives — under ``out/``, never committed."""
    return Path(out_dir) / "wikidata" / "store-index.sqlite3"


@dataclass
class IndexStats:
    """What one build pass saw. Returned rather than logged so tests can assert."""

    shards: int = 0
    items: int = 0
    geni_pairs: int = 0
    items_with_geni: int = 0
    #: Items carrying more than one P2600. Queue item 1.D is about these; the
    #: count is surfaced here so building the index answers "are there any?"
    #: without a second pass.
    items_with_several_geni: int = 0


def _shard_number(path: Path) -> int:
    """``items-01408.jsonl.gz`` → 1408.

    The number is the shard's identity in the index, so it is parsed from the
    name rather than taken from enumeration order: a gap in the sequence must
    not silently shift every later shard's key.
    """
    return int(path.stem.split(".")[0].split("-")[-1])


def shards(store_dir: Path) -> list[Path]:
    return sorted(Path(store_dir).glob("items-*.jsonl.gz"))


def read_shard(path: Path) -> Iterator[dict]:
    """Every item in one shard, in file order."""
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def geni_ids_of(entity: dict) -> list[str]:
    """The Geni profile IDs an item claims, in statement order.

    Guards the same two shapes :func:`genimerge.wikidownload.relatives` does —
    a ``novalue``/``somevalue`` snak carries no ``datavalue``, and a datavalue
    that is not a string is malformed but occurs. Returns a list, never a single
    value: an item carrying two Geni IDs is a real case this repo wants found,
    not an anomaly to collapse.
    """
    found: list[str] = []
    for statement in (entity.get("claims") or {}).get(GENI_ID_PROPERTY) or []:
        snak = statement.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        value = (snak.get("datavalue") or {}).get("value")
        if isinstance(value, str) and value:
            found.append(value)
    return found


def _schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS items (
            qid   TEXT PRIMARY KEY,
            shard INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS geni (
            geni_id TEXT NOT NULL,
            qid     TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
    )


def build_index(
    store_dir: Path,
    index_path: Path,
    *,
    progress: Callable[[int, int, int], None] | None = None,
) -> IndexStats:
    """Read every shard once and write the QID → shard and Geni ID → QID tables.

    The pass is streaming and holds no items: at 1.4M whole entities, keeping
    them would be tens of gigabytes, which is the mistake
    `tests/test_wikidata_store_real.py` was fixed for on 2026-08-09.

    Rebuilt from scratch each time rather than updated in place. The store only
    ever grows by appending, so an incremental build is possible — but it would
    need to know which shards changed, and the whole pass costs minutes against
    a download that costs hours.
    """
    store_dir, index_path = Path(store_dir), Path(index_path)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    if index_path.exists():
        index_path.unlink()

    stats = IndexStats()
    files = shards(store_dir)
    stats.shards = len(files)

    conn = sqlite3.connect(index_path)
    try:
        # The index is derived and regenerable, so durability buys nothing and
        # costs a great deal over 1.4M inserts.
        conn.execute("PRAGMA journal_mode=OFF;")
        conn.execute("PRAGMA synchronous=OFF;")
        _schema(conn)

        item_rows: list[tuple[str, int]] = []
        geni_rows: list[tuple[str, str]] = []

        def flush() -> None:
            if item_rows:
                conn.executemany("INSERT OR REPLACE INTO items VALUES (?, ?);", item_rows)
                item_rows.clear()
            if geni_rows:
                conn.executemany("INSERT INTO geni VALUES (?, ?);", geni_rows)
                geni_rows.clear()

        for position, path in enumerate(files, start=1):
            number = _shard_number(path)
            for entity in read_shard(path):
                qid = entity.get("id")
                if not isinstance(qid, str) or not qid:
                    continue
                stats.items += 1
                item_rows.append((qid, number))
                ids = geni_ids_of(entity)
                if ids:
                    stats.items_with_geni += 1
                    stats.geni_pairs += len(ids)
                    if len(ids) > 1:
                        stats.items_with_several_geni += 1
                    geni_rows.extend((geni_id, qid) for geni_id in ids)
                if len(item_rows) >= WRITE_BATCH:
                    flush()
            if progress is not None:
                progress(position, len(files), stats.items)

        flush()
        # Indexes are created after the bulk load, which is markedly faster than
        # maintaining them per row.
        conn.executescript(
            """
            CREATE INDEX IF NOT EXISTS geni_by_id  ON geni (geni_id);
            CREATE INDEX IF NOT EXISTS geni_by_qid ON geni (qid);
            """
        )
        conn.executemany(
            "INSERT OR REPLACE INTO meta VALUES (?, ?);",
            [
                ("shards", str(stats.shards)),
                ("items", str(stats.items)),
                ("geni_pairs", str(stats.geni_pairs)),
                ("items_with_geni", str(stats.items_with_geni)),
                ("items_with_several_geni", str(stats.items_with_several_geni)),
            ],
        )
        conn.commit()
    finally:
        conn.close()
    return stats


@dataclass
class StoreReader:
    """Random access to stored items, one shard at a time.

    Holds the sqlite connection open; the shards themselves are read on demand
    and nothing is cached, because the callers below walk the store once each
    and a cache would only compete with them for memory.
    """

    store_dir: Path
    index_path: Path
    _conn: sqlite3.Connection = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.store_dir = Path(self.store_dir)
        self.index_path = Path(self.index_path)
        if not self.index_path.exists():
            raise FileNotFoundError(
                f"no store index at {self.index_path} — run `genimerge wikidata-index` first"
            )
        self._conn = sqlite3.connect(f"file:{self.index_path}?mode=ro", uri=True)

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "StoreReader":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    # -- counts --------------------------------------------------------

    def count(self, table: str = "items") -> int:
        if table not in {"items", "geni"}:
            raise ValueError(f"unknown table {table!r}")
        return int(self._conn.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0])

    def meta(self) -> dict[str, str]:
        return dict(self._conn.execute("SELECT key, value FROM meta;"))

    # -- the join key --------------------------------------------------

    def geni_pairs(self) -> Iterator[tuple[str, str]]:
        """Every (Geni ID, QID) pair, Geni ID order.

        A generator of pairs rather than a dict, for the reason
        :class:`genimerge.wikidata.Match` is a list: the mapping is not
        one-to-one in either direction, and collapsing it would hide the double
        claims that queue item 1.D is about.
        """
        yield from self._conn.execute("SELECT geni_id, qid FROM geni ORDER BY geni_id, qid;")

    def qids_for_geni_ids(self, geni_ids: Iterable[str]) -> dict[str, list[str]]:
        """Which stored items claim each of these Geni IDs."""
        found: dict[str, list[str]] = defaultdict(list)
        wanted = list({str(g) for g in geni_ids})
        for chunk in _chunks(wanted, 900):  # sqlite's default variable limit
            placeholders = ",".join("?" * len(chunk))
            rows = self._conn.execute(
                f"SELECT geni_id, qid FROM geni WHERE geni_id IN ({placeholders});", chunk
            )
            for geni_id, qid in rows:
                found[geni_id].append(qid)
        return dict(found)

    def geni_ids_with_several_items(self) -> list[tuple[str, list[str]]]:
        """Geni IDs claimed by more than one stored item."""
        rows = self._conn.execute(
            "SELECT geni_id, qid FROM geni WHERE geni_id IN ("
            "  SELECT geni_id FROM geni GROUP BY geni_id HAVING COUNT(DISTINCT qid) > 1"
            ") ORDER BY geni_id, qid;"
        )
        grouped: dict[str, list[str]] = defaultdict(list)
        for geni_id, qid in rows:
            grouped[geni_id].append(qid)
        return sorted(grouped.items())

    def items_with_several_geni_ids(self) -> list[tuple[str, list[str]]]:
        """Stored items claiming more than one Geni ID — queue item 1.D."""
        rows = self._conn.execute(
            "SELECT qid, geni_id FROM geni WHERE qid IN ("
            "  SELECT qid FROM geni GROUP BY qid HAVING COUNT(DISTINCT geni_id) > 1"
            ") ORDER BY qid, geni_id;"
        )
        grouped: dict[str, list[str]] = defaultdict(list)
        for qid, geni_id in rows:
            grouped[qid].append(geni_id)
        return sorted(grouped.items())

    # -- item access ---------------------------------------------------

    def shard_of(self, qid: str) -> int | None:
        row = self._conn.execute("SELECT shard FROM items WHERE qid = ?;", (qid,)).fetchone()
        return None if row is None else int(row[0])

    def entities(self, qids: Iterable[str]) -> dict[str, dict]:
        """Whole stored items by QID, in the shape ``wbgetentities`` returned.

        Requests are grouped by shard so each shard is decompressed at most
        once — asking for a thousand scattered QIDs one at a time would
        decompress a thousand shards. QIDs absent from the store are simply
        missing from the result, the same way the API omits them.
        """
        wanted = list({str(q) for q in qids})
        by_shard: dict[int, set[str]] = defaultdict(set)
        for chunk in _chunks(wanted, 900):
            placeholders = ",".join("?" * len(chunk))
            rows = self._conn.execute(
                f"SELECT qid, shard FROM items WHERE qid IN ({placeholders});", chunk
            )
            for qid, shard in rows:
                by_shard[int(shard)].add(qid)

        found: dict[str, dict] = {}
        for shard, qids_here in sorted(by_shard.items()):
            path = self.store_dir / f"items-{shard:05d}.jsonl.gz"
            if not path.exists():
                continue
            remaining = set(qids_here)
            for entity in read_shard(path):
                qid = entity.get("id")
                if qid in remaining:
                    found[qid] = entity
                    remaining.discard(qid)
                    if not remaining:
                        break
        return found


def _chunks(items: list[str], size: int) -> Iterator[list[str]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def write_p2600_map(reader: StoreReader, path: Path) -> int:
    """Write ``out/wikidata/p2600-map.tsv`` — the join key between the trees.

    One row per (Geni ID, QID) **pair**. Returns the row count.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("geni_id\tqid\n")
        for geni_id, qid in reader.geni_pairs():
            handle.write(f"{geni_id}\t{qid}\n")
            written += 1
    return written
