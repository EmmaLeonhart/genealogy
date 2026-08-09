"""Parents Wikidata records that our tree does not have.

The three statuses are the whole point of the module, so each gets a test that
pins it against a tree and a store built to produce exactly that case.
"""

from __future__ import annotations

import pytest

from genimerge import wikiancestors, wikistore
from genimerge.model import Person, Tree

from test_wikistore import item, write_store


def person(geni_id: str, father: str | None = None, mother: str | None = None) -> Person:
    return Person(geni_id=geni_id, father_id=father, mother_id=mother)


def tree_of(*people: Person) -> Tree:
    return Tree(people={p.geni_id: p for p in people}, families={})


def parent_item(qid: str, father: str | None = None, mother: str | None = None, geni: list[str] | None = None) -> dict:
    entity = item(qid, geni)
    for prop, target in ((wikiancestors.FATHER, father), (wikiancestors.MOTHER, mother)):
        if target:
            entity["claims"].setdefault(prop, []).append(
                {"mainsnak": {"snaktype": "value", "datavalue": {"value": {"id": target}}}}
            )
    return entity


@pytest.fixture
def store(tmp_path):
    def build(items):
        directory = write_store(tmp_path / "items", {1: items})
        index = tmp_path / "index.sqlite3"
        wikistore.build_index(directory, index)
        return wikistore.StoreReader(directory, index)

    return build


def test_a_parent_with_a_geni_id_we_lack_is_an_export_target(store):
    reader = store(
        [
            parent_item("Q1", father="Q2", geni=["100"]),
            parent_item("Q2", geni=["200"]),  # the father, whom we do not hold
        ]
    )
    with reader:
        result = wikiancestors.find_missing_parents(
            tree_of(person("100")), reader, {"100": "Q1"}
        )
    assert result.counts[wikiancestors.EXPORTABLE] == 1
    (finding,) = result.by_status(wikiancestors.EXPORTABLE)
    assert (finding.parent_qid, finding.parent_geni_ids) == ("Q2", ("200",))
    assert finding.is_father


def test_a_parent_with_no_geni_id_is_an_entity_resolution_case(store):
    reader = store([parent_item("Q1", mother="Q3", geni=["100"]), parent_item("Q3")])
    with reader:
        result = wikiancestors.find_missing_parents(
            tree_of(person("100")), reader, {"100": "Q1"}
        )
    (finding,) = result.by_status(wikiancestors.UNLINKED)
    assert finding.parent_qid == "Q3"
    assert finding.parent_geni_ids == ()
    assert not finding.is_father


def test_a_parent_we_already_hold_is_counted_and_not_reported(store):
    # The normal case. Reporting it would bury the two that matter.
    reader = store([parent_item("Q1", father="Q2", geni=["100"]), parent_item("Q2", geni=["200"])])
    with reader:
        result = wikiancestors.find_missing_parents(
            tree_of(person("100"), person("200")), reader, {"100": "Q1"}
        )
    assert result.counts[wikiancestors.HELD] == 1
    assert result.findings == []


def test_our_own_blank_parent_slot_is_counted_separately(store):
    # "Wikidata knows more" vs "we know it by another route".
    reader = store([parent_item("Q1", father="Q2", geni=["100"]), parent_item("Q2", geni=["200"])])
    with reader:
        result = wikiancestors.find_missing_parents(
            tree_of(person("100", father="999")), reader, {"100": "Q1"}
        )
    assert result.counts["ours_present"] == 1
    assert result.counts["ours_blank"] == 0


def test_a_person_not_in_our_tree_is_never_looked_at(store):
    reader = store([parent_item("Q1", father="Q2", geni=["100"]), parent_item("Q2")])
    with reader:
        result = wikiancestors.find_missing_parents(tree_of(person("999")), reader, {"100": "Q1"})
    assert result.matched == 0
    assert result.findings == []


def test_an_item_the_store_never_downloaded_is_counted_not_an_error(store):
    # The P2600 map lists every statement on Wikidata; the download stopped
    # short of some of them. That is a count, not a failure.
    reader = store([parent_item("Q1", geni=["100"])])
    with reader:
        result = wikiancestors.find_missing_parents(
            tree_of(person("100"), person("200")), reader, {"100": "Q1", "200": "Q_absent"}
        )
    assert result.not_stored == 1


def test_a_novalue_parent_snak_is_not_a_parent():
    entity = {"claims": {wikiancestors.FATHER: [{"mainsnak": {"snaktype": "somevalue"}}]}}
    assert wikiancestors._parent_qids(entity) == []


def test_a_parent_snak_pointing_at_a_date_is_skipped():
    claim = {"mainsnak": {"snaktype": "value", "datavalue": {"value": "1850"}}}
    assert wikiancestors._parent_qids({"claims": {wikiancestors.FATHER: [claim]}}) == []


def test_both_parents_are_read(store):
    reader = store(
        [parent_item("Q1", father="Q2", mother="Q3", geni=["100"]), parent_item("Q2"), parent_item("Q3")]
    )
    with reader:
        result = wikiancestors.find_missing_parents(
            tree_of(person("100")), reader, {"100": "Q1"}
        )
    assert {f.relation for f in result.findings} == {wikiancestors.FATHER, wikiancestors.MOTHER}


def dated_item(qid: str, year: int | None, geni: list[str] | None = None) -> dict:
    entity = item(qid, geni)
    if year is not None:
        literal = f"{'+' if year > 0 else '-'}{abs(year):04d}-01-01T00:00:00Z"
        entity["claims"][wikiancestors.BIRTH] = [
            {"mainsnak": {"snaktype": "value", "datavalue": {"value": {"time": literal}}}}
        ]
    return entity


def test_a_parents_birth_year_is_read_from_the_stored_item(store):
    reader = store([parent_item("Q1", father="Q2", geni=["100"]), dated_item("Q2", 1834, ["200"])])
    with reader:
        result = wikiancestors.find_missing_parents(tree_of(person("100")), reader, {"100": "Q1"})
        years = wikiancestors.parent_birth_years(reader, result.findings)
    assert years == {"Q2": 1834}


def test_a_parent_with_no_birth_date_is_kept_as_none_not_dropped(store):
    # Dropping it would inflate every percentage computed below it.
    reader = store([parent_item("Q1", father="Q2", geni=["100"]), dated_item("Q2", None, ["200"])])
    with reader:
        result = wikiancestors.find_missing_parents(tree_of(person("100")), reader, {"100": "Q1"})
        years = wikiancestors.parent_birth_years(reader, result.findings)
    assert years == {"Q2": None}


def test_a_bce_birth_year_survives_the_round_trip(store):
    reader = store([parent_item("Q1", father="Q2", geni=["100"]), dated_item("Q2", -44, ["200"])])
    with reader:
        result = wikiancestors.find_missing_parents(tree_of(person("100")), reader, {"100": "Q1"})
        years = wikiancestors.parent_birth_years(reader, result.findings)
    assert years == {"Q2": -44}


@pytest.mark.parametrize(
    "year,label",
    [(-44, "BCE"), (1, "100s"), (100, "100s"), (101, "200s"), (1834, "1900s"), (None, "no date")],
)
def test_centuries_are_labelled_by_the_years_they_contain(year, label):
    assert wikiancestors._century(year) == label


def test_century_rows_are_oldest_first_with_undated_last():
    findings = [
        wikiancestors.Finding("1", "Q1", wikiancestors.FATHER, "Qa", wikiancestors.EXPORTABLE),
        wikiancestors.Finding("2", "Q2", wikiancestors.FATHER, "Qb", wikiancestors.EXPORTABLE),
        wikiancestors.Finding("3", "Q3", wikiancestors.FATHER, "Qc", wikiancestors.EXPORTABLE),
    ]
    years = {"Qa": 1834, "Qb": -100, "Qc": None}
    assert wikiancestors._century_rows(findings, years) == [("BCE", 1), ("1900s", 1), ("no date", 1)]


def test_the_century_section_appears_only_once_dates_are_read(store):
    reader = store([parent_item("Q1", father="Q2", geni=["100"]), dated_item("Q2", 1834, ["200"])])
    tree = tree_of(person("100"))
    with reader:
        result = wikiancestors.find_missing_parents(tree, reader, {"100": "Q1"})
        without = wikiancestors.render_markdown(result, tree)
        result.years = wikiancestors.parent_birth_years(reader, result.findings)
        with_dates = wikiancestors.render_markdown(result, tree)
    # Degrades to counts rather than failing when the second pass has not run.
    assert "Which centuries" not in without
    assert "Which centuries" in with_dates
    assert "**1 of 1** are born 1800 or later" in with_dates


def test_the_report_names_both_problems_separately(store):
    reader = store(
        [parent_item("Q1", father="Q2", mother="Q3", geni=["100"]), parent_item("Q2", geni=["200"]), parent_item("Q3")]
    )
    tree = tree_of(person("100"))
    with reader:
        result = wikiancestors.find_missing_parents(tree, reader, {"100": "Q1"})
    text = wikiancestors.render_markdown(result, tree)
    assert "Geni profiles one hop above us — 1" in text
    assert "Parents with no Geni link — 1" in text
    assert "Q2" in text
