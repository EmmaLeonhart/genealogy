"""A qualifier must land on the statement the item already holds, never beside it.

⛔ Reported 2026-09-16: an item carried `P2600 6000000009968757483` **twice** -- once bare and
once qualified `subject named as "Heinrich VI von Plauen III"` -- both written by this pipeline.

The cause is `wbeditentity` semantics. A claim object with no `id` is a NEW statement, always;
the API has no notion that a statement with the same mainsnak is the same one. So the live claim
id has to be read off the item and set on the outgoing claim.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# `wikidata-edit-run.py` imports `qs_v1`, a sibling in scripts/, and the hyphen in its own name
# means it can only be loaded by path.
sys.path.insert(0, str(REPO / "scripts"))
_spec = importlib.util.spec_from_file_location(
    "edit_run", REPO / "scripts" / "wikidata-edit-run.py")
edit_run = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(edit_run)


def string_snak(prop, value):
    return {"snaktype": "value", "property": prop, "datatype": "string",
            "datavalue": {"type": "string", "value": value}}


def outgoing(value="6000000009968757483", named="Heinrich VI von Plauen III"):
    return {"claims": [{
        "type": "statement", "rank": "normal",
        "mainsnak": string_snak("P2600", value),
        "qualifiers": {"P1810": [string_snak("P1810", named)]},
    }]}


def live(value="6000000009968757483", qualifiers=None, refs=None):
    claim = {"id": "Q1$abc-123", "mainsnak": string_snak("P2600", value)}
    if qualifiers:
        claim["qualifiers"] = qualifiers
    if refs:
        claim["references"] = refs
    return {"P2600": [claim]}


def test_qualifier_attaches_to_the_existing_statement():
    data = outgoing()
    assert edit_run.merge_into_existing(data, live()) == ["Q1$abc-123"]
    claim = data["claims"][0]
    assert claim["id"] == "Q1$abc-123", "no id means wbeditentity makes a second statement"
    assert claim["qualifiers"]["P1810"][0]["datavalue"]["value"] == "Heinrich VI von Plauen III"


def test_a_different_value_is_left_as_a_new_statement():
    """A SECOND Geni id is not a duplicate -- `CLAUDE.md` says so explicitly."""
    data = outgoing()
    assert edit_run.merge_into_existing(data, live(value="4198641")) == []
    assert "id" not in data["claims"][0]


def test_an_existing_qualifier_is_not_replaced():
    """Passing `qualifiers` on a claim with an `id` REPLACES the set, which would delete a
    human's qualifier. § *The purpose is to ADD, not to correct*."""
    theirs = {"P585": [string_snak("P585", "somebody else's qualifier")]}
    data = outgoing()
    edit_run.merge_into_existing(data, live(qualifiers=theirs))
    merged = data["claims"][0]["qualifiers"]
    assert "P585" in merged, "the existing qualifier was dropped"
    assert "P1810" in merged, "ours was not added"


def test_the_same_qualifier_twice_is_not_doubled():
    mine = {"P1810": [string_snak("P1810", "Heinrich VI von Plauen III")]}
    data = outgoing()
    edit_run.merge_into_existing(data, live(qualifiers=mine))
    assert len(data["claims"][0]["qualifiers"]["P1810"]) == 1


def test_existing_references_survive():
    theirs = [{"snaks": {"P248": [string_snak("P248", "a source")]}}]
    data = outgoing()
    edit_run.merge_into_existing(data, live(refs=theirs))
    assert data["claims"][0]["references"] == theirs
