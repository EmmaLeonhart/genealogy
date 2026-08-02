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


# --- the contradiction count and its denominator ---------------------------
#
# `considered` exists so the contradiction count in the report is reported
# against something. Every link the CLI passes is expansion-inferred, so it is
# also the only direct check this project has on inference quality.


def test_considered_counts_every_link_exactly_once(tmp_path):
    client = _client(tmp_path, {"Q2": "2", "Q3": "999"})
    batch = quickstatements.build_batch(
        client, tree(), {"1": "Q1", "2": "Q2", "3": "Q3"}, retrieved="2026-08-01"
    )

    # one with no ID, one already correct, one contradicting
    assert (len(batch.edits), len(batch.already_present), len(batch.conflicting)) == (1, 1, 1)
    assert batch.considered == 3


def test_considered_is_zero_for_an_empty_batch():
    assert quickstatements.Batch().considered == 0


def test_report_states_the_contradiction_count_against_its_denominator(tmp_path):
    client = _client(tmp_path, {"Q3": "999"})
    batch = quickstatements.build_batch(
        client, tree(), {"1": "Q1", "2": "Q2", "3": "Q3"}, retrieved="2026-08-01"
    )

    markdown = quickstatements.render_markdown(batch)

    assert "| expansion-inferred links examined | 3 |" in markdown
    assert "**1 of the 3 inferred links examined here are contradicted" in markdown


def test_report_carries_the_not_an_error_rate_caveat(tmp_path):
    """Asserted by identity, so rewording the caveat does not break this."""
    client = _client(tmp_path, {"Q3": "999"})
    batch = quickstatements.build_batch(
        client, tree(), {"3": "Q3"}, retrieved="2026-08-01"
    )

    markdown = quickstatements.render_markdown(batch)

    assert quickstatements.NOT_AN_ERROR_RATE in markdown


def test_the_not_an_error_rate_caveat_still_says_the_two_things_that_matter():
    """Identity alone would pass on an emptied constant, so pin its substance.

    Both ideas are load bearing. Without the first, a contradiction reads as a
    proven bad match; without the second, 3-of-36 reads as a measured accuracy
    figure rather than as what little the check can see.
    """
    caveat = quickstatements.NOT_AN_ERROR_RATE

    assert "duplicate Geni profiles for one person" in caveat
    assert "already carries a P2600, which almost none do" in caveat


def test_no_contradiction_section_when_nothing_contradicts(tmp_path):
    client = _client(tmp_path, {})
    batch = quickstatements.build_batch(client, tree(), {"1": "Q1"}, retrieved="2026-08-01")

    markdown = quickstatements.render_markdown(batch)

    assert "## Contradictions" not in markdown
    assert "error rate" not in markdown
    # the denominator is still reported, because 0-of-N is a result too
    assert "| expansion-inferred links examined | 1 |" in markdown
