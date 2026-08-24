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

What these tests do is make sure the graph would be *usable* by such a resolver, and
two of them fail today. Both are marked strict `xfail`: the defect is real, the
number is measured, and when someone fixes it the suite goes red asking for the
marker to come off. `reports/edit-graph.md` is the full accounting,
`scripts/audit-edit-graph.py` regenerates it.
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


@pytest.mark.xfail(strict=True, reason=(
    "33 duplicate ids, measured 2026-08-23. `add_geni_id:Q694696` collides because "
    "the id scheme is keyed on the QID alone and that QID has two Geni profiles -- "
    "the multi-valued P2600 case, so both edits are correct and the NAMING is wrong. "
    "The other 32 are repeated add_relationship and structural_correspondence rows. "
    "See reports/edit-graph.md."))
def test_no_two_edits_claim_the_same_id(edits):
    seen, dupes = set(), []
    for _n, e in edits:
        if e.get("id") in seen:
            dupes.append(e.get("id"))
        seen.add(e.get("id"))
    assert not dupes, f"{len(dupes)} duplicate ids, e.g. {dupes[:5]}"


@pytest.mark.xfail(strict=True, reason=(
    "55,776 dependencies name an id no batch emits, measured 2026-08-23. "
    "build-orderlife-batch.py writes `requires: person:<q>` while emitting ids as "
    "`create_individual:<q>` / `add_geni_id:<q>` -- one script disagreeing with "
    "itself, 55,765 times. The other 11 are samaritan-succession and abram-father "
    "requiring `entity_resolution:<q>` for QIDs that file does not contain. "
    "See reports/edit-graph.md."))
def test_no_edit_requires_an_id_nothing_emits(edits):
    known = ids_of(edits)
    dangling = [(n, e.get("id"), r) for n, e in edits
                for r in (e.get("requires") or []) if r not in known]
    assert not dangling, (
        f"{len(dangling)} unsatisfiable dependencies, e.g. {dangling[:3]}")
