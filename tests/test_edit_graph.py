"""The ordering the JSON batches declare, and whether it holds together.

Every edit object carries `requires`, a list of the `id`s that must land first.
`CLAUDE.md` leans on that in the place it matters most: the `NN` label fix is **two**
edits per item, the `mul` one declared as a dependency of the `en` one, *"so the
marker is written before the slot holding it is reused"*. On the 1,271 items whose
only `NN` lives in `en`, the wrong order erases the marker.

**Nothing currently reads `requires`.** `scripts/wikidata-edit-run.py` does not
mention it; 284,125 edit objects declare an ordering that no executor enforces. That
is recorded in `queue.md` as work, not fixed here — a resolver is a design decision
about how the batches run, not a test.

**`genimerge.editorder` now reads `requires`** — Emma's design, a random pick from
whatever is ready. It orders all 284,146 objects in about a second with no violations.

Two of these tests failed when the file was written and **both markers are now off**:
55,776 dangling dependencies became 0 once three scripts stopped naming ids nothing
emits, and 33 duplicate ids became 0 once two id schemes gained the Geni id and one
emitter deduplicated a claim it reached twice. `reports/edit-graph.md` is the full
accounting; `scripts/audit-edit-graph.py` regenerates it.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
REPORTS = REPO / "reports"

KNOWN_TYPES = {
    "set_labels", "set_label", "create_individual", "add_relationship",
    "create_name_item", "add_geni_id", "normalise_office", "add_statement",
    # Added 2026-08-25 for `reports/wikidata-remove-wrong-p2600.json`. The only DESTRUCTIVE
    # type in the repo: it deletes a `P2600` *Geni.com profile ID* an item should never have
    # carried, as against the merged-away case, which is a rank change to deprecated and is
    # not this. `scripts/resolve-multi-geni-by-parents.py` explains what may and may not
    # produce one.
    "remove_statement",
}


@pytest.fixture(scope="module")
def edits():
    """(batch name, edit) for every edit object. ~1.7s, so no `slow` marker."""
    out = []
    for path in sorted(REPORTS.glob("wikidata-*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        items = data if isinstance(data, list) else data.get("edits", [])
        out.extend((path.name, e) for e in items if isinstance(e, dict))
    if not out:
        pytest.skip("no JSON edit batches generated yet")
    return out


def ids_of(edits):
    return {e.get("id") for _n, e in edits}


def test_every_edit_has_an_id_a_type_and_a_subject(edits):
    """Without these an edit cannot be addressed, dispatched, or attributed."""
    bad = [(n, e.get("id")) for n, e in edits
           if not e.get("id") or not e.get("type") or "subject" not in e]
    assert not bad, f"{len(bad)} malformed edit objects, e.g. {bad[:5]}"


def test_every_edit_type_is_one_the_repo_knows(edits):
    """A new type is fine — add it here, so it is a decision and not a surprise."""
    seen = Counter(e.get("type") for _n, e in edits)
    unknown = {t: n for t, n in seen.items() if t not in KNOWN_TYPES}
    assert not unknown, (
        f"edit types not in KNOWN_TYPES: {unknown}. Add them here once you have "
        f"decided what the executor should do with them.")


CREATIONS = {"create_individual", "create_name_item"}


def test_every_edit_that_is_not_a_creation_names_something_to_act_on(edits):
    """A creation has no identifier yet -- that is what it is for.

    A first cut demanded a `qid` or `geni_id` on every subject and failed on 41,706
    edits that were all correct, which is worth writing down because each is a
    deliberate design decision this repo already made:

    * `create_name_item` (13,320) -- a name is identified by its label and usage.
      There is nothing else to name it by until the item exists.
    * `create_individual` in `wikidata-orderlife.json` (19,228) -- order.life
      people, carried in `subject.orderlife_qid`. They are not from Geni.
    * `create_individual` in `wikidata-patronymic-fathers.json` (9,158) -- Emma's
      item, `CLAUDE.md`: *"add items for the hypothetical fathers that are implied
      to exist from the patronymics. These ones would be wiki data items that do not
      have geni items."* Having no Geni id is the point.

    What is left is the real rule: an edit that modifies an existing item must say
    which one.
    """
    bad = []
    for n, e in edits:
        if e.get("type") in CREATIONS:
            continue
        s = e.get("subject") or {}
        if not (s.get("qid") or s.get("geni_id")):
            bad.append((n, e.get("id"), e.get("type")))
    assert not bad, f"{len(bad)} non-creations with no subject, e.g. {bad[:5]}"


def test_the_dependency_graph_has_no_cycles(edits):
    """A before B before A can never be executed in any order."""
    known = ids_of(edits)
    graph = {e.get("id"): [r for r in (e.get("requires") or []) if r in known]
             for _n, e in edits}
    colour, cycles = {}, []

    def walk(node, stack):
        if colour.get(node) == 2:
            return
        if colour.get(node) == 1:
            cycles.append(stack[stack.index(node):] + [node])
            return
        colour[node] = 1
        for nxt in graph.get(node, ()):
            walk(nxt, stack + [nxt])
        colour[node] = 2

    import sys
    sys.setrecursionlimit(100000)
    for node in graph:
        if colour.get(node) is None:
            walk(node, [node])
    assert not cycles, f"{len(cycles)} cycles, e.g. {cycles[:2]}"


def test_no_two_edits_claim_the_same_id(edits):
    """Was strict `xfail` at 33 on 2026-08-23; now zero, and the two causes differed.

    **Twenty-one were two correct statements sharing one name.** One Wikidata item
    can carry two Geni ids -- the multi-valued `P2600` case -- so
    `structural_correspondence:<qid>` and `add_geni_id:<qid>` each named two
    different edits. The Geni id is now part of the id; nothing declared a
    `requires` on either prefix, so widening the key broke no dependency.

    **Twelve were one claim reached twice.** Two order.life people can map to a
    single Wikidata item, so `Q96124 P22 Q161419` arrived once via Danaus and once
    via Oceanus -- identical subject and statement, differing only in the provenance
    note. Wikidata gets one statement either way, so those are collapsed and both
    notes kept.
    """
    seen, dupes = set(), []
    for _n, e in edits:
        if e.get("id") in seen:
            dupes.append(e.get("id"))
        seen.add(e.get("id"))
    assert not dupes, f"{len(dupes)} duplicate ids, e.g. {dupes[:5]}"


def test_no_edit_requires_an_id_nothing_emits(edits):
    """Was strict `xfail` at 55,776 for about an hour on 2026-08-23; now zero.

    Three scripts named dependencies nothing emitted.
    `build-orderlife-batch.py` wrote `requires: person:<q>` while emitting its ids
    as `<kind>:<q>` -- one script disagreeing with itself 55,765 times; it now
    decides each person's kind up front and names the edit that will exist, and
    drops the entry entirely for a person who needs no edit, because depending on
    nothing is not a dependency. `build-samaritan-succession.py` and
    `build-abram-father-fix.py` required `entity_resolution:<q>` for nine QIDs that
    file covers **none** of -- the Geni ID for those priests is added by
    `samaritan_priest_link:<q>`.
    """
    known = ids_of(edits)
    dangling = [(n, e.get("id"), r) for n, e in edits
                for r in (e.get("requires") or []) if r not in known]
    assert not dangling, (
        f"{len(dangling)} unsatisfiable dependencies, e.g. {dangling[:3]}")
