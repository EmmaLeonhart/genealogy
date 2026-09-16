"""A qualifier must land on the statement the item already holds, never beside it.

⛔ Reported 2026-09-16: an item carried `P2600 6000000009968757483` **twice** -- once bare and
once qualified `subject named as "Heinrich VI von Plauen III"` -- both written by this pipeline.

The cause is `wbeditentity` semantics. A claim object with no `id` is a NEW statement, always;
the API has no notion that a statement with the same mainsnak is the same one.

⛔ **AND THE FIRST FIX WAS THE WRONG MECHANISM.** It set the live claim id on the outgoing claim
and sent the merged qualifier set. `wbeditentity` on a claim carrying an `id` REPLACES that set,
so every write depended on our reconstruction being complete and current, and a human qualifier
added between the read and the write would be silently deleted. Emma pointed at the logic that
already existed: *"there's logic in shintowiki-scripts that was intentionally added to implement
this that you didn't do"* -- `find_claim` then `wbsetqualifier`/`wbsetreference` by GUID, which
is additive by construction. These tests are on that mechanism.
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


def test_qualifier_goes_to_the_existing_statement_by_guid():
    """The claim leaves the payload entirely; the qualifier is attached to its GUID."""
    data = outgoing()
    plans = edit_run.plan_attachments(data, live())
    assert [p["guid"] for p in plans] == ["Q1$abc-123"]
    assert plans[0]["qualifiers"]["P1810"][0]["datavalue"]["value"] \
        == "Heinrich VI von Plauen III"
    assert "claims" not in data, "a claim left in the payload is written a second time"


def test_a_different_value_is_left_as_a_new_statement():
    """A SECOND Geni id is not a duplicate -- `CLAUDE.md` says so explicitly."""
    data = outgoing()
    assert edit_run.plan_attachments(data, live(value="4198641")) == []
    assert len(data["claims"]) == 1
    assert "id" not in data["claims"][0]


def test_someone_elses_qualifier_is_never_touched():
    """The set is never sent, so there is nothing that could replace it: only OUR qualifier
    is attached, and by a call that cannot remove anything."""
    theirs = {"P585": [string_snak("P585", "somebody else's qualifier")]}
    data = outgoing()
    plans = edit_run.plan_attachments(data, live(qualifiers=theirs))
    assert list(plans[0]["qualifiers"]) == ["P1810"], "their qualifier is not ours to resend"


def test_a_qualifier_already_present_is_not_sent_again():
    mine = {"P1810": [string_snak("P1810", "Heinrich VI von Plauen III")]}
    data = outgoing()
    assert edit_run.plan_attachments(data, live(qualifiers=mine)) == []
    assert "claims" not in data


def test_a_reference_already_present_is_not_sent_again():
    theirs = [{"snaks": {"P248": [string_snak("P248", "a source")]}}]
    data = {"claims": [{
        "type": "statement", "rank": "normal",
        "mainsnak": string_snak("P2600", "6000000009968757483"),
        "references": theirs,
    }]}
    assert edit_run.plan_attachments(data, live(refs=theirs)) == []


def test_a_new_reference_is_attached_and_the_old_one_left_alone():
    theirs = [{"snaks": {"P248": [string_snak("P248", "a source")]}}]
    ours = [{"snaks": {"P248": [string_snak("P248", "Geni")]}}]
    data = {"claims": [{
        "type": "statement", "rank": "normal",
        "mainsnak": string_snak("P2600", "6000000009968757483"),
        "references": ours,
    }]}
    plans = edit_run.plan_attachments(data, live(refs=theirs))
    assert plans[0]["references"] == ours


def test_already_present_is_a_success_not_a_failure():
    """Measured in shintowiki-scripts on 2026-09-12: 23 of 26 reported failures were this."""
    assert edit_run.is_already_present(
        "The statement has already a qualifier with hash 1a2b3c")
    assert edit_run.is_already_present(
        "The statement has already a reference with hash 1a2b3c")
    assert not edit_run.is_already_present("The save has failed.")
    assert not edit_run.is_already_present("")
