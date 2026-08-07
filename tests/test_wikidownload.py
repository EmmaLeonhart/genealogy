"""Unit tests for the Wikidata full-item download.

Everything here runs offline: `WikidataClient` takes an injectable ``fetch``,
and these tests substitute one that serves items out of a dict. That is the
whole reason the seam exists — the alternative is a download loop whose resume,
redirect and missing-item paths are only ever exercised against the live
endpoint, which is exactly the behaviour `todo.md` § 8a was written against.

The properties pinned are the ones a resumed run depends on: an item is never
requested twice, a killed run appends to the shard it was filling rather than
starting a new one, and the index can be thrown away and rebuilt from the
shards.
"""

from __future__ import annotations

import gzip
import json
import urllib.error
import urllib.parse

import pytest

from genimerge import wikidata, wikidownload


def make_client(tmp_path, entities: dict, *, fail_on=(), record=None):
    """A client whose network is a dict of QID → entity JSON.

    ``retries``/``max_backoff`` are floored because the real backoff sleeps for
    real: six attempts doubling from two seconds is 126 seconds of a test run
    spent asleep, which is what the first version of this file did. The backoff
    itself is right and is tested where it belongs, in `test_wikidata.py`.
    """

    def fetch(url, data=None, headers=None):
        ids = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["ids"][0].split("|")
        if record is not None:
            record.append(list(ids))
        if any(qid in fail_on for qid in ids):
            raise urllib.error.HTTPError(url, 500, "boom", None, None)
        payload = {}
        for qid in ids:
            entity = entities.get(qid)
            payload[entity["id"] if entity else qid] = entity or {"id": qid, "missing": ""}
        return json.dumps({"entities": payload}).encode("utf-8")

    return wikidata.WikidataClient(
        cache_dir=tmp_path / "cache", fetch=fetch, delay=0.0, retries=1, max_backoff=0.0
    )


def person(qid: str, label: str = "x") -> dict:
    return {
        "id": qid,
        "type": "item",
        "labels": {"en": {"language": "en", "value": label}},
        "claims": {"P31": [{"mainsnak": {"datavalue": {"value": {"id": "Q5"}}}}]},
    }


def store_and_index(tmp_path, per_shard: int = wikidownload.SHARD_ITEMS):
    store = wikidownload.ItemStore(tmp_path / "items", per_shard=per_shard)
    index = wikidownload.StateIndex(tmp_path / "state.sqlite3")
    return store, index


# -- the store ---------------------------------------------------------


def test_a_batch_is_one_gzip_member_and_reads_back_whole(tmp_path):
    store = wikidownload.ItemStore(tmp_path / "items")
    store.write([person("Q1"), person("Q2")])
    store.write([person("Q3")])

    assert len(store.shards()) == 1
    assert [item["id"] for item in store.items()] == ["Q1", "Q2", "Q3"]


def test_shards_roll_at_the_configured_size(tmp_path):
    store = wikidownload.ItemStore(tmp_path / "items", per_shard=2)
    store.write([person("Q1"), person("Q2")])
    store.write([person("Q3")])

    assert [p.name for p in store.shards()] == ["items-00000.jsonl.gz", "items-00001.jsonl.gz"]
    assert [item["id"] for item in store.items()] == ["Q1", "Q2", "Q3"]


def test_a_batch_is_never_split_across_shards(tmp_path):
    # Four items into shards of three: the batch stays whole and the shard goes
    # one over rather than the member being broken for a round number.
    store = wikidownload.ItemStore(tmp_path / "items", per_shard=3)
    store.write([person(f"Q{n}") for n in range(4)])

    assert len(store.shards()) == 1
    assert sum(1 for _ in store.items()) == 4


def test_a_reopened_store_appends_to_the_partly_filled_shard(tmp_path):
    store = wikidownload.ItemStore(tmp_path / "items", per_shard=10)
    store.write([person("Q1")])

    reopened = wikidownload.ItemStore(tmp_path / "items", per_shard=10)
    reopened.write([person("Q2")])

    assert len(reopened.shards()) == 1, "a killed run must not strand a one-item shard"
    assert [item["id"] for item in reopened.items()] == ["Q1", "Q2"]


def test_the_stored_bytes_are_the_response_verbatim(tmp_path):
    # Nothing reshapes an item on the way in. What a later phase wants out of
    # one is not yet known, and a lossily stored item has to be fetched again.
    store = wikidownload.ItemStore(tmp_path / "items")
    original = person("Q1", "Ærlig")
    store.write([original])

    with gzip.open(store.shards()[0], "rt", encoding="utf-8") as handle:
        assert json.loads(handle.read()) == original


# -- the index ---------------------------------------------------------


def test_held_covers_done_and_missing_but_not_error(tmp_path):
    index = wikidownload.StateIndex(tmp_path / "state.sqlite3")
    index.record("Q1", "done", shard="items-00000.jsonl.gz")
    index.record("Q2", "missing")
    index.record("Q3", "error", error="HTTPError: 500")
    index.commit()

    assert index.held() == {"Q1", "Q2"}
    assert index.counts() == {"done": 1, "missing": 1, "error": 1}


def test_attempts_accumulate_across_records(tmp_path):
    index = wikidownload.StateIndex(tmp_path / "state.sqlite3")
    index.record("Q1", "error", error="first")
    index.record("Q1", "error", error="second")
    index.commit()

    row = index._conn.execute("SELECT attempts, error FROM items WHERE qid='Q1'").fetchone()
    assert row == (2, "second"), "a retry budget needs the count, not just the last state"


def test_the_index_rebuilds_from_the_shards(tmp_path):
    store, index = store_and_index(tmp_path)
    store.write([person("Q1"), person("Q2")])
    index.record("Q1", "done")
    index.commit()
    index.close()

    fresh = wikidownload.StateIndex(tmp_path / "state2.sqlite3")
    assert fresh.rebuild(store) == 2
    assert fresh.held() == {"Q1", "Q2"}



# -- relatives ---------------------------------------------------------


def with_relatives(qid: str, **links) -> dict:
    item = person(qid)
    for prop, targets in links.items():
        item["claims"][prop] = [
            {"mainsnak": {"snaktype": "value", "datavalue": {"value": {"id": t}}}}
            for t in targets
        ]
    return item


def test_relatives_reads_every_family_property():
    item = with_relatives("Q1", P22=["Q2"], P25=["Q3"], P26=["Q4"], P40=["Q5", "Q6"], P3373=["Q7"])

    assert wikidownload.relatives(item) == ["Q2", "Q3", "Q4", "Q5", "Q6", "Q7"]


def test_relatives_ignores_claims_that_name_nobody():
    # `somevalue` — "has a father, unknown who" — carries no datavalue at all,
    # and a date sitting on a relation property is malformed but does occur.
    # Both are a KeyError in the obvious version of this function.
    item = person("Q1")
    item["claims"]["P22"] = [
        {"mainsnak": {"snaktype": "somevalue"}},
        {"mainsnak": {"snaktype": "value", "datavalue": {"value": "1830-01-01"}}},
        {"mainsnak": {"snaktype": "value", "datavalue": {"value": {"id": "Q2"}}}},
    ]

    assert wikidownload.relatives(item) == ["Q2"]


def test_relatives_of_an_item_with_no_claims_is_empty():
    assert wikidownload.relatives({"id": "Q1"}) == []


# -- the fetch queue ---------------------------------------------------


def test_the_queue_is_fifo_and_dedupes(tmp_path):
    index = wikidownload.StateIndex(tmp_path / "state.sqlite3")

    assert index.enqueue(["Q1", "Q2", "Q1"]) == 2
    assert index.enqueue(["Q2", "Q3"]) == 1
    assert index.take(10) == ["Q1", "Q2", "Q3"]


def test_enqueueing_a_held_item_does_not_demote_it(tmp_path):
    index = wikidownload.StateIndex(tmp_path / "state.sqlite3")
    index.record("Q1", "done", shard="items-00000.jsonl.gz")

    assert index.enqueue(["Q1"]) == 0
    assert index.status("Q1") == "done"
    assert index.take(10) == []


# -- fetching ----------------------------------------------------------


def test_a_batch_is_fifty_and_leaves_the_queue_when_recorded(tmp_path):
    calls: list[list[str]] = []
    qids = [f"Q{n}" for n in range(1, 121)]
    client = make_client(tmp_path, {q: person(q) for q in qids}, record=calls)
    store, index = store_and_index(tmp_path)
    index.enqueue(qids)
    stats = wikidownload.WalkStats()

    while wikidownload.fetch_step(client, store, index, stats):
        pass

    assert [len(c) for c in calls] == [50, 50, 20]
    assert stats.stored == 120 and index.queue_length() == 0


def test_nothing_already_held_is_ever_requested(tmp_path):
    calls: list[list[str]] = []
    qids = ["Q1", "Q2", "Q3"]
    client = make_client(tmp_path, {q: person(q) for q in qids}, record=calls)
    store, index = store_and_index(tmp_path)
    index.record("Q2", "done")
    index.enqueue(qids)

    wikidownload.fetch_step(client, store, index, wikidownload.WalkStats())

    assert calls == [["Q1", "Q3"]], "the never-query-twice property is the whole design"


def test_a_missing_item_is_settled_rather_than_retried_forever(tmp_path):
    client = make_client(tmp_path, {"Q1": person("Q1")})
    store, index = store_and_index(tmp_path)
    index.enqueue(["Q1", "Q404"])
    stats = wikidownload.WalkStats()

    wikidownload.fetch_step(client, store, index, stats)

    assert stats.stored == 1 and stats.missing == 1
    assert index.status("Q404") == "missing"
    assert index.queue_length() == 0, "a deleted item must not be asked for on every run"


def test_a_redirect_settles_the_qid_that_was_asked_for(tmp_path):
    # Ask for Q1, get Q2 back with a redirects block. Both are the same item and
    # both must count as held, or Q1 is re-requested on every future run.
    target = person("Q2")
    target["redirects"] = {"from": "Q1", "to": "Q2"}
    client = make_client(tmp_path, {"Q1": target})
    store, index = store_and_index(tmp_path)
    index.enqueue(["Q1"])

    wikidownload.fetch_step(client, store, index, wikidownload.WalkStats())

    assert index.status("Q1") == "done" and index.status("Q2") == "done"
    assert [item["id"] for item in store.items()] == ["Q2"]


def test_a_failed_batch_marks_its_qids_and_the_walk_carries_on(tmp_path):
    qids = ["Q1", "Q2", "Q3", "Q4"]
    client = make_client(tmp_path, {q: person(q) for q in qids}, fail_on={"Q1"})
    store, index = store_and_index(tmp_path)
    index.enqueue(qids)
    stats = wikidownload.WalkStats()

    while wikidownload.fetch_step(client, store, index, stats, batch_size=2):
        pass

    assert stats.errors == 2 and stats.stored == 2
    assert index.status("Q1") == "error"
    assert index.queue_length() == 0
    assert [item["id"] for item in store.items()] == ["Q3", "Q4"]


# -- scanning ----------------------------------------------------------


def test_the_scan_queues_relatives_not_already_known(tmp_path):
    store, index = store_and_index(tmp_path)
    store.write([with_relatives("Q1", P22=["Q2"], P40=["Q3"])])
    index.record("Q1", "done")
    index.record("Q3", "done")
    stats = wikidownload.WalkStats()

    wikidownload.scan_step(store, index, stats, items=10)

    assert index.take(10) == ["Q2"], "Q3 is already held; only Q2 is new"
    assert stats.scanned == 1 and stats.discovered == 1


def test_the_scan_does_not_requeue_what_is_already_queued(tmp_path):
    # Two siblings both naming the same father. Without checking the queue as
    # well as the store, a well-connected family enqueues its parents once per
    # child, which over 500k items is most of the queue.
    store, index = store_and_index(tmp_path)
    store.write([with_relatives("Q1", P22=["Q9"]), with_relatives("Q2", P22=["Q9"])])
    stats = wikidownload.WalkStats()

    wikidownload.scan_step(store, index, stats, items=10)

    assert stats.discovered == 1 and index.take(10) == ["Q9"]


def test_the_cursor_makes_the_shards_the_iteration_queue(tmp_path):
    store, index = store_and_index(tmp_path)
    store.write([with_relatives("Q1", P22=["Q10"])])
    stats = wikidownload.WalkStats()
    wikidownload.scan_step(store, index, stats, items=10)

    # A later fetch appends to the end of the store; the next scan picks up
    # exactly there rather than re-reading what it has already walked.
    store.write([with_relatives("Q2", P22=["Q11"])])
    wikidownload.scan_step(store, index, stats, items=10)

    assert stats.scanned == 2, "an item scanned once must not be scanned again"
    assert index.take(10) == ["Q10", "Q11"]


def test_the_scan_stops_at_its_item_budget_and_resumes_there(tmp_path):
    store, index = store_and_index(tmp_path)
    store.write([with_relatives(f"Q{n}", P22=[f"Q{n}0"]) for n in range(1, 6)])
    stats = wikidownload.WalkStats()

    assert wikidownload.scan_step(store, index, stats, items=2) == 2
    assert index.take(10) == ["Q10", "Q20"]
    assert wikidownload.scan_step(store, index, stats, items=2) == 2
    assert index.take(10) == ["Q10", "Q20", "Q30", "Q40"]


def test_rebuilding_the_index_resets_the_cursor_and_the_queue(tmp_path):
    # The queue and the cursor describe a walk, and a walk cannot be recovered
    # from the shards. Re-scanning re-discovers the same relatives at no network
    # cost, so resetting is the safe direction.
    store, index = store_and_index(tmp_path)
    store.write([with_relatives("Q1", P22=["Q2"])])
    stats = wikidownload.WalkStats()
    wikidownload.scan_step(store, index, stats, items=10)
    assert index.take(10) == ["Q2"]

    index.rebuild(store)

    assert index.cursor() is None and index.take(10) == []
    assert index.held() == {"Q1"}


# -- the walk ----------------------------------------------------------


def test_the_walk_reaches_people_the_seed_set_never_named(tmp_path):
    # Q1 is the seed. Its father Q2 carries no Geni ID and so is in no seed
    # list; Q2's mother Q3 is a further hop out. Both must arrive. This is the
    # whole point of the expansion phase.
    entities = {
        "Q1": with_relatives("Q1", P22=["Q2"]),
        "Q2": with_relatives("Q2", P25=["Q3"]),
        "Q3": person("Q3"),
    }
    client = make_client(tmp_path, entities)
    store, index = store_and_index(tmp_path)
    index.enqueue(["Q1"])

    stats = wikidownload.walk(client, store, index, batch_size=10, scan_per_round=10)

    assert sorted(item["id"] for item in store.items()) == ["Q1", "Q2", "Q3"]
    assert stats.discovered == 2 and index.queue_length() == 0


def test_the_walk_terminates_on_a_cycle(tmp_path):
    # Spouses name each other, so the graph is full of two-cycles. Termination
    # comes from what is already known, not from the shape of the data.
    entities = {
        "Q1": with_relatives("Q1", P26=["Q2"]),
        "Q2": with_relatives("Q2", P26=["Q1"]),
    }
    client = make_client(tmp_path, entities)
    store, index = store_and_index(tmp_path)
    index.enqueue(["Q1"])

    stats = wikidownload.walk(client, store, index, batch_size=10, scan_per_round=10)

    assert stats.stored == 2 and stats.requested == 2


def test_a_resumed_walk_continues_where_the_last_one_stopped(tmp_path):
    qids = [f"Q{n}" for n in range(1, 11)]
    entities = {q: person(q) for q in qids}
    store, index = store_and_index(tmp_path)
    index.enqueue(qids)

    first = wikidownload.walk(
        make_client(tmp_path, entities), store, index, batch_size=2, limit=4
    )
    calls: list[list[str]] = []
    second = wikidownload.walk(
        make_client(tmp_path, entities, record=calls), store, index, batch_size=2
    )

    assert first.stored == 4 and second.stored == 6
    assert calls[0] == ["Q5", "Q6"]
    assert sorted(item["id"] for item in store.items()) == sorted(qids)


def test_limit_bounds_the_network_and_not_the_scan(tmp_path):
    qids = [f"Q{n}" for n in range(1, 21)]
    client = make_client(tmp_path, {q: person(q) for q in qids})
    store, index = store_and_index(tmp_path)
    index.enqueue(qids)

    stats = wikidownload.walk(client, store, index, batch_size=3, limit=5)

    assert stats.requested == 5, "a pilot must not overshoot its request budget"
    assert stats.scanned >= stats.stored


def test_stats_measure_what_the_pilot_is_for(tmp_path):
    qids = [f"Q{n}" for n in range(1, 5)]
    client = make_client(tmp_path, {q: person(q) for q in qids})
    store, index = store_and_index(tmp_path)
    index.enqueue(qids)
    ticks = iter([0.0, 2.0, 2.0, 2.0, 2.0])

    stats = wikidownload.walk(client, store, index, batch_size=4, clock=lambda: next(ticks))

    assert stats.items_per_second == 2.0
    assert stats.bytes_per_item > 0
    projected = stats.projection(500_000)
    assert projected["requests"] == 500_000 / wikidownload.FETCH_BATCH
    assert projected["hours"] == pytest.approx(500_000 / 2.0 / 3600)

# -- the seed list -----------------------------------------------------


def test_seed_qids_reads_the_p2600_map_and_dedupes(tmp_path):
    # A QID carrying two Geni IDs is on two lines — 44 of them at last count,
    # and a real thing rather than a corrupt file.
    path = tmp_path / "p2600-all.tsv"
    path.write_text(
        "Q1\t6000000000000000001\nQ2\t6000000000000000002\nQ1\t6000000000000000003\n",
        encoding="utf-8",
    )

    assert wikidownload.seed_qids(path) == ["Q1", "Q2"]


def test_seed_qids_ignores_anything_that_is_not_a_qid(tmp_path):
    path = tmp_path / "seeds.tsv"
    path.write_text("qid\tgeni\nQ1\t1\n\nP31\t2\n", encoding="utf-8")

    assert wikidownload.seed_qids(path) == ["Q1"]


def test_full_entities_asks_for_every_property(tmp_path):
    # props is omitted on purpose: the point of the pass is that a later phase
    # never has to come back for a field nobody thought to request.
    seen: list[str] = []

    def fetch(url, data=None, headers=None):
        seen.append(url)
        return b'{"entities": {"Q1": {"id": "Q1"}}}'

    client = wikidata.WikidataClient(cache_dir=tmp_path, fetch=fetch, delay=0.0)
    assert client.full_entities(["Q1"]) == {"Q1": {"id": "Q1"}}

    query = urllib.parse.parse_qs(urllib.parse.urlparse(seen[0]).query)
    assert query["action"] == ["wbgetentities"] and "props" not in query


def test_full_entities_does_not_use_the_report_cache(tmp_path):
    # The cache is keyed on the exact batch, so caching full items would store a
    # second copy of everything under a key no resumed run could reconstruct.
    calls = []

    def fetch(url, data=None, headers=None):
        calls.append(url)
        return b'{"entities": {"Q1": {"id": "Q1"}}}'

    client = wikidata.WikidataClient(cache_dir=tmp_path / "cache", fetch=fetch, delay=0.0)
    client.full_entities(["Q1"])
    client.full_entities(["Q1"])

    assert len(calls) == 2
    assert not (tmp_path / "cache").exists()


# -- surviving a kill --------------------------------------------------


def truncate_last_member(shard, keep_fraction: float = 0.5) -> None:
    """Chop the tail off a shard, as losing power mid-write would."""
    raw = shard.read_bytes()
    shard.write_bytes(raw[: int(len(raw) * keep_fraction)])


def test_a_truncated_shard_keeps_the_batches_written_before_the_break(tmp_path):
    # Power loss partway through writing a batch ends that gzip member
    # mid-stream. Reading it then raises, and appending after the break would
    # make the new items unreachable too. A shard holds twenty batches, so the
    # earlier members are what there is to save — and they do survive.
    store = wikidownload.ItemStore(tmp_path / "items")
    for start in range(1, 51, 10):
        store.write([person(f"Q{n}", "a name long enough to compress") for n in range(start, start + 10)])
    shard = store.shards()[0]
    truncate_last_member(shard, keep_fraction=0.7)

    with pytest.raises((EOFError, OSError, UnicodeDecodeError)):
        list(wikidownload._read_lines(shard))

    reopened = wikidownload.ItemStore(tmp_path / "items")
    survivors = [item["id"] for item in reopened.items()]

    assert 0 < len(survivors) < 50, "the batches before the break must still read"


def test_an_interrupted_batch_is_lost_whole_and_fetched_again(tmp_path):
    # One batch is one gzip member, so a write cut in half yields nothing from
    # that batch rather than half of it. That is the right outcome: the index is
    # committed after the shard, so none of those items were ever recorded as
    # held and the walk simply asks for them again.
    store, index = store_and_index(tmp_path)
    store.write([person(f"Q{n}", "a name long enough to compress") for n in range(1, 51)])
    truncate_last_member(store.shards()[0])

    reopened = wikidownload.ItemStore(tmp_path / "items")

    assert list(reopened.items()) == []
    assert index.held() == set(), "nothing was committed, so nothing is believed held"


def test_a_repaired_shard_can_be_appended_to_and_read_back(tmp_path):
    store = wikidownload.ItemStore(tmp_path / "items")
    store.write([person(f"Q{n}", "a name long enough to compress") for n in range(1, 51)])
    truncate_last_member(store.shards()[0])

    reopened = wikidownload.ItemStore(tmp_path / "items")
    before = len(list(reopened.items()))
    reopened.write([person("Q999")])

    ids = [item["id"] for item in wikidownload.ItemStore(tmp_path / "items").items()]
    assert len(ids) == before + 1
    assert ids[-1] == "Q999", "an append after a repair must be reachable"


def test_items_lost_to_a_truncated_tail_are_fetched_again(tmp_path):
    # The index is committed after the shard is written, so items lost with a
    # broken tail were never recorded as held. Rebuilding from the shards is
    # what re-opens them for fetching.
    store, index = store_and_index(tmp_path)
    store.write([person(f"Q{n}", "a name long enough to compress") for n in range(1, 51)])
    for n in range(1, 51):
        index.record(f"Q{n}", "done")
    index.commit()
    truncate_last_member(store.shards()[0])

    reopened = wikidownload.ItemStore(tmp_path / "items")
    kept = {item["id"] for item in reopened.items()}
    index.rebuild(reopened)

    assert index.held() == kept
    assert len(kept) < 50


# -- surviving an outage -----------------------------------------------


def test_failed_qids_go_back_on_the_queue_on_the_next_run(tmp_path):
    # Without this an outage loses items silently: `error` takes a QID off the
    # queue and nothing ever put it back, so a run after a drop would report
    # itself complete with holes in it.
    index = wikidownload.StateIndex(tmp_path / "state.sqlite3")
    index.record("Q1", "error", error="URLError: unreachable")
    index.record("Q2", "done")
    index.commit()

    assert index.requeue_errors() == 1
    assert index.take(10) == ["Q1"]
    assert index.status("Q2") == "done"


def test_a_qid_that_keeps_failing_is_eventually_left_alone(tmp_path):
    index = wikidownload.StateIndex(tmp_path / "state.sqlite3")
    for _ in range(5):
        index.record("Q1", "error", error="boom")
    index.commit()

    assert index.requeue_errors(max_attempts=5) == 0, "a bad QID must not retry forever"


def test_an_outage_trips_the_breaker_instead_of_burning_the_queue(tmp_path):
    qids = [f"Q{n}" for n in range(1, 101)]
    # `fail_on` everything: the internet is gone, every batch fails.
    client = make_client(tmp_path, {q: person(q) for q in qids}, fail_on=set(qids))
    store, index = store_and_index(tmp_path)
    index.enqueue(qids)

    stats = wikidownload.walk(
        client, store, index, batch_size=2, max_consecutive_failures=3
    )

    assert stats.stopped_early, "a walk that gives up must say so"
    assert stats.batches == 3, "it must not sprint through the whole queue"
    assert index.queue_length() == 94, "the untouched queue survives the outage"


def test_the_breaker_resets_on_a_batch_that_works(tmp_path):
    # One bad batch in the middle of a good run is not an outage.
    qids = [f"Q{n}" for n in range(1, 11)]
    entities = {q: person(q) for q in qids}
    client = make_client(tmp_path, entities, fail_on={"Q3"})
    store, index = store_and_index(tmp_path)
    index.enqueue(qids)

    stats = wikidownload.walk(
        client, store, index, batch_size=2, max_consecutive_failures=2
    )

    assert not stats.stopped_early
    assert stats.stored == 8 and stats.errors == 2
