"""The rules that keep the edit-object emitters from damaging Wikidata.

Queue item 14d. Emma, 2026-08-16: *"Don't just test them before September 1st.
Put them at the end of the queue."*

Six scripts now write JSON edit objects meant to run against Wikidata, and none
had a test. That is the repo's normal pattern for `scripts/` — but a report being
wrong wastes a run, and an edit being wrong changes a live wiki. In one night
these emitters produced three near-misses, every one caught by reading output
rather than by a test:

* the name-item planner treated only `resolved` as "already exists" and would
  have created a **tenth `Maria`**, on top of the nine Wikidata already has;
* the Samaritan batch read only links Wikidata already stated, ignoring the QIDs
  Emma wrote onto the Geni profiles, and would have created **`Jonathan I`** and
  **`Baba Rabba`** twice;
* the source comparison called **69 people absent** and then **13 fathers in
  conflict**, both from name matching that was too strict and then too loose.

**What is pinned here is the shape of those failures, not the scripts' output.**
The numbers move every time the corpus grows; the rules do not.

Loaded by path — the scripts have hyphens in their names and are not importable.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
REPORTS = REPO / "reports"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_"), SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _edits(path: Path):
    if not path.exists():
        pytest.skip(f"{path.name} not generated yet")
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("edits", [])


# -- never create what already exists ----------------------------------
#
# The one failure mode `CLAUDE.md` calls out as damaging Wikidata rather than
# merely wasting a run.


def test_a_name_whose_label_is_ambiguous_is_never_created():
    """`Maria` matches nine Wikidata items. It must not become a tenth.

    The planner's first version treated only `resolved` as existing, so every
    name that matched *several* items came out as a creation.
    """
    planner = _load("build-name-item-batch")
    assert planner.MIN_BEARERS >= 1

    path = REPORTS / "name-item-plan.csv"
    if not path.exists():
        pytest.skip("name-item-plan.csv not generated yet")
    import csv
    csv.field_size_limit(10 ** 7)
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    ambiguous = [r for r in rows if r["action"].startswith("AMBIGUOUS")]
    assert ambiguous, "no ambiguous names at all - the guard may have been lost"

    # Per (token, usage), not per token. `Maria` is ambiguous as a GIVEN name
    # and legitimately created as a FAMILY name with 8 bearers - one item per
    # usage, `CLAUDE.md` § "Jackson Jackson Jackson". Comparing bare tokens
    # failed on exactly that and the test was wrong, not the emitter.
    created = {(e["labels"]["mul"], e.get("usage"))
               for e in _edits(REPORTS / "wikidata-name-items.json")
               if e.get("labels", {}).get("mul")}
    for row in ambiguous:
        assert (row["token"], row["usage"]) not in created, (
            f"{row['token']!r} is ambiguous as a {row['usage']} name on Wikidata "
            "and is also being created as one")


def test_a_name_item_that_exists_is_linked_not_created():
    import csv
    path = REPORTS / "name-item-plan.csv"
    if not path.exists():
        pytest.skip("name-item-plan.csv not generated yet")
    csv.field_size_limit(10 ** 7)
    for row in csv.DictReader(path.open(encoding="utf-8", newline="")):
        if row["existing_qid"]:
            assert row["action"] == "link", (
                f"{row['token']!r} already has {row['existing_qid']} and is "
                f"marked {row['action']!r}")


def test_the_samaritan_batch_creates_nobody_who_has_a_qid():
    """`Jonathan I` and `Baba Rabba` exist; the batch proposed creating them.

    The cause was reading only links Wikidata already stated and ignoring the
    QIDs Emma wrote onto the Geni profiles. Both sources are read now.
    """
    import csv
    pairs = REPORTS / "geni-wikidata-pairs.csv"
    batch = REPORTS / "wikidata-samaritan-priests.json"
    if not (pairs.exists() and batch.exists()):
        pytest.skip("inputs not generated yet")
    linked = {r["geni_id"] for r in csv.DictReader(pairs.open(encoding="utf-8", newline=""))
              if r.get("qid")}
    for edit in _edits(batch):
        gid = (edit.get("subject") or {}).get("geni_id")
        assert gid not in linked, (
            f"creating {edit.get('labels', {}).get('en')!r} ({gid}) which already "
            "has a Wikidata item via the QID on its Geni profile")


# -- never let an order.life QID reach a Wikidata value ------------------


def test_no_orderlife_qid_is_emitted_as_a_wikidata_value():
    """`Q153719` is order.life's *Female*, not a person, and would type-check.

    `reports/orderlife-properties.md` calls the local Q-space the worse of the
    two traps, because a `wikibase-item` value carries no marker saying which
    wiki it belongs to.
    """
    # Checked against statement and link VALUES only. `subject.orderlife_qid` is
    # provenance - it records which order.life item an edit came from and is
    # supposed to hold a local QID. A first version scanned the whole blob and
    # flagged that, which was the test being wrong rather than the emitter.
    forbidden = {"Q153718", "Q153719", "Q153800", "Q153801", "Q153802",
                 "Q153806", "Q153721"}
    for name in ("wikidata-orderlife-identifiers.json", "wikidata-orderlife.json"):
        for edit in _edits(REPORTS / name):
            values = [s.get("value") for s in edit.get("statements", [])]
            values += [l.get("value") for l in edit.get("links", [])]
            for value in values:
                assert value not in forbidden, (
                    f"{name}: order.life's {value} is a class item and appears "
                    f"as a Wikidata value in {edit.get('id')}")
            # And the subject of a creation must not BE a class item.
            subject = (edit.get("subject") or {}).get("orderlife_qid")
            if edit.get("type") == "create_individual":
                assert subject not in forbidden, (
                    f"{name}: creating order.life's class item {subject} "
                    f"({edit.get('labels', {}).get('en')!r}) as a person")


# -- citations -----------------------------------------------------------


def test_a_geni_sourced_statement_cites_the_profile_it_came_from():
    for edit in _edits(REPORTS / "wikidata-entity-resolution.json"):
        if edit.get("type") != "add_geni_id":
            continue
        refs = edit["statements"][0]["references"]
        props = {r["property"] for r in refs}
        assert "P854" in props and "P813" in props, (
            f"{edit['id']} states a Geni ID with no reference to the profile")


def test_nothing_cites_a_source_wikidata_does_not_have():
    """A reference to a source that does not exist makes the statement unusable.

    Emma, 2026-08-14: *"These JSONs aren't gonna fire because they're trying to
    cite an order.life citation that doesn't exist."* So a person with no Geni ID
    carries **no reference**, never a broken one.
    """
    for edit in _edits(REPORTS / "wikidata-orderlife.json"):
        gid = (edit.get("subject") or {}).get("geni_id")
        for statement in edit.get("statements", []):
            refs = statement.get("references") or []
            if not gid:
                assert not refs, (
                    f"{edit.get('id')} has no Geni ID but carries a reference")
            for ref in refs:
                assert ref.get("property") in {"P2600", "P854", "P813"}, (
                    f"{edit.get('id')} cites {ref.get('property')}, which is not "
                    "a source Wikidata holds")


# -- the succession normalisation ---------------------------------------


def test_the_succession_never_removes_what_it_does_not_replace():
    """`remove` is the riskiest verb in the repo: it deletes live statements.

    An entry may only drop the old `P155`/`P156` if the new office statement
    carries the same succession as a qualifier.
    """
    for edit in _edits(REPORTS / "wikidata-samaritan-succession.json"):
        if not edit.get("remove"):
            continue
        quals = {q["property"] for add in edit.get("add", [])
                 for q in add.get("qualifiers", [])}
        assert quals & {"P1365", "P1366"}, (
            f"{edit['id']} removes P155/P156 without stating the succession "
            "anywhere else")


def test_every_succession_entry_states_the_office():
    for edit in _edits(REPORTS / "wikidata-samaritan-succession.json"):
        if not edit.get("add"):
            continue
        assert any(a["property"] == "P39" and a["value"] == "Q678510"
                   for a in edit["add"]), (
            f"{edit['id']} adds something other than the office")


def test_no_structural_correspondence_gives_one_profile_two_items():
    """A Geni profile already linked to another item is a disagreement, not an edit.

    The walk's `MERGE` branch fires whenever our parent's QID is not among
    Wikidata's — including when our parent *has* a QID and it is a different one.
    Emitting `P2600` there would leave two items claiming one Geni profile, which
    is the reverse of the case `CLAUDE.md` blesses: two Geni profiles on one item
    is ordinary, one Geni profile on two items is a claim about identity.

    A second Geni ID on the *item* stays allowed, and the flag stays on it.
    """
    for edit in _edits(REPORTS / "wikidata-structural-correspondence.json"):
        gid = edit["subject"]["geni_id"]
        already = edit.get("geni_ids_already_on_item") or []
        assert gid not in already, (
            f"{edit['id']} adds a Geni ID the item already states")
        assert edit.get("adds_a_second_geni_id") == bool(already), (
            f"{edit['id']} mis-flags whether it adds a second Geni ID")
        assert edit["statements"][0]["property"] == "P2600", (
            f"{edit['id']} emits something other than the identifier; her order "
            "is the Geni ID first and everything derived from it after")


def test_a_person_with_genealogy_is_never_dropped_as_a_class():
    """`Q1` Aster and `Q5` Hesper are people, and were briefly dropped as classes.

    The class screen started as "every QID anything declares itself an instance
    of", which finds order.life's `Male`/`Female`/`Person` rows — and also caught
    Aster (child, spouse, sex, birth) and Hesper (mother, child, sex), because
    Wikidata happens to use `Q5` for *human*. A class is a thing pointed at as a
    class **and** carrying no genealogy of its own.
    """
    batch = _load("build-orderlife-batch")
    assert batch.GENEALOGICAL, "the genealogical-property guard has been removed"

    created = {(e.get("subject") or {}).get("orderlife_qid")
               for e in _edits(REPORTS / "wikidata-orderlife.json")}
    for qid, who in (("Q1", "Aster"), ("Q5", "Hesper")):
        assert qid in created, (
            f"order.life {qid} ({who}) has genealogy and must not be screened "
            "out as a class")
