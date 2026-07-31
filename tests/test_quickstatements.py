import json

from genimerge import gedcom, quickstatements
from genimerge.model import build_tree
from genimerge.wikidata import WikidataClient

TREE = """0 HEAD
0 @I1@ INDI
1 NAME Harald /Fairhair/
1 RFN geni:1
0 @I2@ INDI
1 NAME Gorm /the Old/
1 RFN geni:2
0 @I3@ INDI
1 NAME Someone /Else/
1 RFN geni:3
0 TRLR
"""


def tree():
    return build_tree(gedcom.parse(TREE).records)


def _client(tmp_path, existing):
    """`existing` maps qid -> the P2600 already on that item."""
    response = json.dumps(
        {
            "results": {
                "bindings": [
                    {
                        "item": {"value": f"http://www.wikidata.org/entity/{qid}"},
                        "geni": {"value": geni},
                    }
                    for qid, geni in existing.items()
                ]
            }
        }
    ).encode("utf-8")
    return WikidataClient(
        cache_dir=tmp_path / "c", fetch=lambda *a, **k: response, delay=0, max_backoff=0
    )


def test_an_item_with_no_geni_id_gets_a_statement(tmp_path):
    batch = quickstatements.build_batch(
        _client(tmp_path, {}), tree(), {"1": "Q1"}, retrieved="2026-07-30"
    )

    assert [(e.qid, e.geni_id) for e in batch.edits] == [("Q1", "1")]
    assert batch.already_present == [] and batch.conflicting == []


def test_an_item_that_already_says_the_same_thing_is_skipped(tmp_path):
    batch = quickstatements.build_batch(
        _client(tmp_path, {"Q1": "1"}), tree(), {"1": "Q1"}, retrieved="2026-07-30"
    )

    assert batch.edits == []
    assert [e.qid for e in batch.already_present] == ["Q1"]


def test_an_item_with_a_different_geni_id_is_reported_not_overwritten(tmp_path):
    # Either our match is wrong or the item points at a duplicate Geni profile.
    # Neither is safe to overwrite.
    batch = quickstatements.build_batch(
        _client(tmp_path, {"Q1": "999"}), tree(), {"1": "Q1"}, retrieved="2026-07-30"
    )

    assert batch.edits == []
    assert [(e.qid, e.geni_id, current) for e, current in batch.conflicting] == [
        ("Q1", "1", "999")
    ]


def test_a_contradiction_never_reaches_the_batch_file(tmp_path):
    batch = quickstatements.build_batch(
        _client(tmp_path, {"Q1": "999"}), tree(), {"1": "Q1"}, retrieved="2026-07-30"
    )

    assert quickstatements.render_quickstatements(batch) == ""
    assert "999" in quickstatements.render_markdown(batch)


def test_the_statement_line_is_valid_quickstatements_v1(tmp_path):
    batch = quickstatements.build_batch(
        _client(tmp_path, {}), tree(), {"1": "Q1"}, retrieved="2026-07-30"
    )
    line = quickstatements.render_quickstatements(batch).strip()
    fields = line.split("\t")

    assert fields[0] == "Q1"
    assert fields[1] == "P2600"
    assert fields[2] == '"1"'
    # A reference, so the edit can be checked rather than landing unattributed.
    assert fields[3] == "S854" and fields[4].startswith('"https://www.geni.com/')
    assert fields[5] == "S813" and fields[6] == "+2026-07-30T00:00:00Z/11"


def test_the_retrieved_date_is_passed_in_so_a_rerun_reproduces_the_file(tmp_path):
    first = quickstatements.render_quickstatements(
        quickstatements.build_batch(
            _client(tmp_path, {}), tree(), {"1": "Q1"}, retrieved="2026-01-01"
        )
    )
    second = quickstatements.render_quickstatements(
        quickstatements.build_batch(
            _client(tmp_path, {}), tree(), {"1": "Q1"}, retrieved="2026-01-01"
        )
    )

    assert first == second
    assert "2026-01-01" in first


def test_several_edits_come_out_in_a_stable_order(tmp_path):
    batch = quickstatements.build_batch(
        _client(tmp_path, {}), tree(), {"2": "Q2", "1": "Q1"}, retrieved="2026-07-30"
    )

    assert [e.qid for e in batch.edits] == ["Q1", "Q2"]


def test_the_readable_companion_names_the_person_and_links_both_sides(tmp_path):
    batch = quickstatements.build_batch(
        _client(tmp_path, {}), tree(), {"1": "Q1"}, retrieved="2026-07-30"
    )
    text = quickstatements.render_markdown(batch)

    assert "Harald Fairhair" in text
    assert "https://www.wikidata.org/wiki/Q1" in text
    assert "https://www.geni.com/people/x/1" in text
    assert "Nothing here has been sent to Wikidata" in text


def test_an_empty_batch_produces_an_empty_file_not_a_stray_newline(tmp_path):
    assert quickstatements.render_quickstatements(quickstatements.Batch()) == ""
