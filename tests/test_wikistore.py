"""The offline reader for the downloaded Wikidata store.

Built against fixtures for shape and against two real shards for reality, the
same split the rest of the suite uses. The real-store test copies a couple of
shards into a temp directory rather than indexing all 1,408: a full build is
minutes, and what needs proving against real bytes is that the parsing holds,
not that a loop repeats.
"""

from __future__ import annotations

import gzip
import json
import shutil
from pathlib import Path

import pytest

from genimerge import wikistore

REAL_STORE = Path(__file__).resolve().parents[1] / "wikidata" / "items"


def item(qid: str, geni: list[str] | None = None, **extra) -> dict:
    claims: dict[str, list[dict]] = {}
    for value in geni or []:
        claims.setdefault(wikistore.GENI_ID_PROPERTY, []).append(
            {"mainsnak": {"snaktype": "value", "datavalue": {"value": value, "type": "string"}}}
        )
    return {"id": qid, "claims": claims, **extra}


def write_store(directory: Path, shards: dict[int, list[dict]]) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    for number, items in shards.items():
        path = directory / f"items-{number:05d}.jsonl.gz"
        with gzip.open(path, "wt", encoding="utf-8") as handle:
            for entity in items:
                handle.write(json.dumps(entity) + "\n")
    return directory


@pytest.fixture
def reader(tmp_path):
    store = write_store(
        tmp_path / "items",
        {
            1: [item("Q1", ["100"]), item("Q2", ["200", "201"])],
            2: [item("Q3"), item("Q4", ["400"])],
        },
    )
    index = tmp_path / "index.sqlite3"
    wikistore.build_index(store, index)
    with wikistore.StoreReader(store, index) as opened:
        yield opened


def test_the_index_records_every_item_and_which_shard_holds_it(reader):
    assert reader.count("items") == 4
    assert reader.shard_of("Q1") == 1
    assert reader.shard_of("Q4") == 2
    assert reader.shard_of("Q999") is None


def test_entities_come_back_whole_and_in_the_shape_they_were_stored(reader):
    found = reader.entities(["Q1", "Q4"])
    assert set(found) == {"Q1", "Q4"}
    # Not reshaped: the caller is code that used to read `wbgetentities`.
    assert found["Q1"]["claims"][wikistore.GENI_ID_PROPERTY][0]["mainsnak"]["datavalue"]["value"] == "100"


def test_a_qid_that_is_not_stored_is_simply_absent(reader):
    # The API omits unknown ids rather than erroring, and callers rely on that.
    assert reader.entities(["Q1", "Q999"]) .keys() == {"Q1"}


def test_the_geni_map_keeps_pairs_rather_than_collapsing_them(reader):
    pairs = list(reader.geni_pairs())
    assert pairs == [("100", "Q1"), ("200", "Q2"), ("201", "Q2"), ("400", "Q4")]


def test_an_item_claiming_two_geni_ids_is_found(reader):
    assert reader.items_with_several_geni_ids() == [("Q2", ["200", "201"])]


def test_a_geni_id_claimed_by_two_items_is_found(tmp_path):
    store = write_store(tmp_path / "items", {1: [item("Q1", ["100"]), item("Q2", ["100"])]})
    index = tmp_path / "index.sqlite3"
    wikistore.build_index(store, index)
    with wikistore.StoreReader(store, index) as reader:
        assert reader.geni_ids_with_several_items() == [("100", ["Q1", "Q2"])]


def test_qids_for_geni_ids_answers_the_join(reader):
    assert reader.qids_for_geni_ids(["100", "400", "nope"]) == {"100": ["Q1"], "400": ["Q4"]}


def test_a_snak_with_no_value_is_not_a_geni_id():
    # `novalue`/`somevalue` snaks carry no datavalue at all. The obvious version
    # of this parse is a KeyError on real data.
    assert wikistore.geni_ids_of({"claims": {"P2600": [{"mainsnak": {"snaktype": "novalue"}}]}}) == []


def test_a_non_string_geni_value_is_skipped():
    claim = {"mainsnak": {"snaktype": "value", "datavalue": {"value": {"id": "Q5"}}}}
    assert wikistore.geni_ids_of({"claims": {"P2600": [claim]}}) == []


def test_an_item_with_no_claims_at_all_is_not_an_error():
    assert wikistore.geni_ids_of({"id": "Q1"}) == []


def test_the_shard_number_comes_from_the_name_not_from_enumeration(tmp_path):
    # A gap in the sequence must not shift every later shard's key.
    store = write_store(tmp_path / "items", {1: [item("Q1")], 7: [item("Q7")]})
    index = tmp_path / "index.sqlite3"
    wikistore.build_index(store, index)
    with wikistore.StoreReader(store, index) as reader:
        assert reader.shard_of("Q7") == 7
        assert reader.entities(["Q7"])["Q7"]["id"] == "Q7"


def test_building_twice_does_not_double_the_rows(tmp_path):
    store = write_store(tmp_path / "items", {1: [item("Q1", ["100"])]})
    index = tmp_path / "index.sqlite3"
    wikistore.build_index(store, index)
    stats = wikistore.build_index(store, index)
    assert stats.items == 1
    with wikistore.StoreReader(store, index) as reader:
        assert reader.count("items") == 1
        assert reader.count("geni") == 1


def test_the_map_file_is_one_row_per_pair(tmp_path, reader):
    path = tmp_path / "p2600-map.tsv"
    written = wikistore.write_p2600_map(reader, path)
    lines = path.read_text(encoding="utf-8").splitlines()
    assert written == 4
    assert lines[0] == "geni_id\tqid"
    assert lines[1:] == ["100\tQ1", "200\tQ2", "201\tQ2", "400\tQ4"]


def test_stats_count_the_doubles_while_building(tmp_path):
    store = write_store(tmp_path / "items", {1: [item("Q1", ["1"]), item("Q2", ["2", "3"])]})
    stats = wikistore.build_index(store, tmp_path / "index.sqlite3")
    assert (stats.items, stats.items_with_geni, stats.geni_pairs) == (2, 2, 3)
    assert stats.items_with_several_geni == 1


def test_a_missing_index_says_which_command_builds_it(tmp_path):
    with pytest.raises(FileNotFoundError, match="wikidata-index"):
        wikistore.StoreReader(tmp_path, tmp_path / "absent.sqlite3")


@pytest.mark.skipif(not REAL_STORE.exists(), reason="no downloaded store")
def test_two_real_shards_index_and_read_back(tmp_path):
    real = wikistore.shards(REAL_STORE)[:2]
    if not real:
        pytest.skip(f"no shards under {REAL_STORE}")
    store = tmp_path / "items"
    store.mkdir(parents=True)
    for path in real:
        shutil.copy(path, store / path.name)

    index = tmp_path / "index.sqlite3"
    stats = wikistore.build_index(store, index)
    assert stats.items > 0
    # The seed set is items selected *for* carrying P2600, so real shards from
    # the seed phase carry it densely. A floor, not an equality.
    assert stats.items_with_geni > 0

    with wikistore.StoreReader(store, index) as reader:
        sample = [qid for qid, _ in list(reader.geni_pairs())[:5]]
        by_geni = reader.qids_for_geni_ids(sample)
        assert by_geni
        qids = [q for qids in by_geni.values() for q in qids]
        found = reader.entities(qids)
        assert set(found) == set(qids)
        for entity in found.values():
            # Whole items, not a projection — the thing
            # test_wikidata_store_real.py guards for the store itself.
            assert "claims" in entity and "labels" in entity
