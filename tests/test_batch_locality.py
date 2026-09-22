"""The batch locality guard, exercised through pytest.

⛔ **THE CHECK ITSELF LIVES IN `scripts/check-batch-locality.py`** and this only drives it, so the
rule has ONE implementation. `pipeline.yml` runs that script directly because that workflow is
stdlib-only and installs no pytest -- the first version of the step failed with
`No module named pytest` on run 35329948498, having checked nothing.

`CLAUDE.md` § *A GUARD IN ONE EMITTER IS NOT A GUARD* is what this arrangement is for, and this
night is made of that mistake: the locality gate was written for the sender, then for
`derived_labels`, then for `lines`, and leaked each time because each was a path and not the
output.
"""
from __future__ import annotations

import importlib.util
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "check_batch_locality", REPO / "scripts" / "check-batch-locality.py")
check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check)


@pytest.mark.parametrize("rel", check.BATCHES)
def test_batch_touches_nothing_outside_the_universe(rel):
    path = REPO / rel
    if not path.exists():
        pytest.skip(f"{rel} not built")
    allowed = check.universe()
    if not allowed:
        pytest.skip("out/wikidata/edit-universe.json absent -- recompose to build it")
    # ⛔ **THREE VALUES, NOT TWO.** `NEVER_EDIT` was added to `offenders` on 2026-09-18 and the
    # script's own `main()` was updated with it; this driver was not, so every one of the three
    # parametrised cases died on `ValueError: too many values to unpack` -- the locality gate
    # checking NOTHING through pytest while reading as a real red. That is
    # `CLAUDE.md` § *A GUARD IN ONE EMITTER IS NOT A GUARD* landing in the test layer, on the
    # same night the docstring above was written about it happening in the emitters.
    non_local, on_kanji, never = check.offenders(path, allowed, check.kanji_items())
    assert not non_local, (
        f"{rel}: {len(non_local)} item(s) neither in the universe nor one step beyond it, "
        f"first at line {min(non_local.values())}: " + ", ".join(sorted(non_local)[:8])
        + " -- CLAUDE.md: ALL EDITS, NO EXCEPTIONS")
    assert not on_kanji, (
        f"{rel}: label edits on {len(on_kanji)} item(s) whose ja label is KANJI, which marks a "
        f"Sinosphere name and takes no label edit in any language: "
        + ", ".join(sorted(on_kanji)[:8]))
    assert not never, (
        f"{rel}: {len(never)} edit(s) on an item this pipeline may NEVER touch again, first at "
        f"line {min(never.values())}: " + ", ".join(sorted(never))
        + " -- scripts/wikidata_lockout.NEVER_EDIT")


def test_an_absent_universe_is_not_permission():
    """A missing universe file must never read as 'everything is allowed'."""
    assert check.universe() is None or check.universe(), "universe() must be None or non-empty"


# ---------------------------------------------------------------------------
# ⛔ NO CREATION SURVIVES THE GATE WITH NOTHING POINTING AT IT.
#
# Ruled 2026-09-21, from three live items Emma checked by hand:
# *"three isolated individuals were created. They become immediate entry points and fix the
# error that made them."*
#
#     Q141529844  Solveig Halfdansdatter                      off Q2521523
#     Q141529845  Ogmund Torbergsson Giske                    off Q12001101
#     Q141529847  Poppo von Berg-Schelklingen zu Roggenstein  off Q30301558
#
# `Special:WhatLinksHere` reports "No pages link to" for all three. Each was made by
# `build-ancestor-creations.py`, which emits a creation and EXACTLY ONE relationship -- the
# reciprocal `Q<child> P22|P25 LAST` that is the whole reason the person was picked. The
# locality filter dropped that line because the child sits outside the edit universe, and the
# CREATE above it was not dropped with it.
#
# `build-garborg-day.compose` has refused an unrelated creation since 2026-08-29, but it runs
# INSIDE the composer -- before the growth passes append and before anything is stripped. A
# guard that runs before the last thing to edit the file is not the last guard.
# ---------------------------------------------------------------------------

_qs_spec = importlib.util.spec_from_file_location(
    "qs_v1", pathlib.Path(__file__).resolve().parents[1] / "scripts" / "qs_v1.py")
qs_v1 = importlib.util.module_from_spec(_qs_spec)
_qs_spec.loader.exec_module(qs_v1)


def _block(label, geni, reciprocal=None):
    out = ["CREATE",
           'LAST\tLen\t"%s"' % label,
           'LAST\tDen\t"Geni %s"' % geni,
           'LAST\tLmul\t"%s"' % label,
           'LAST\tP31\tQ5\tS2600\t"%s"' % geni,
           'LAST\tP2600\t"%s"' % geni,
           'LAST\tP21\tQ6581097\tS2600\t"%s"' % geni]
    if reciprocal:
        out.append('%s\tP22\tLAST\tS2600\t"%s"' % (reciprocal, geni))
    return out


def test_a_creation_whose_only_link_was_stripped_is_withdrawn():
    """The exact shape of the three. Strip the reciprocal, and the CREATE must go too."""
    lines = _block("Solveig Halfdansdatter", "6000000002106194792") + [""]
    kept, dropped = qs_v1.drop_orphaned_creations(lines)
    assert dropped == ["Solveig Halfdansdatter"]
    assert "CREATE" not in kept


def test_a_creation_that_kept_its_link_is_untouched():
    """The fourth pick of that same run, off Q141216494, which IS in the universe."""
    lines = _block("Jacob Knutson Skiftun", "6000000177945982827", "Q141216494") + [""]
    kept, dropped = qs_v1.drop_orphaned_creations(lines)
    assert dropped == []
    assert kept == lines


def test_the_last_creation_in_the_file_is_not_hidden_by_the_relationships_section():
    """⛔ "Until the next CREATE" is the wrong boundary, and it hid exactly one of the three.

    The batch ends with hundreds of `Q… P22 Q…` lines between items that already exist. Read as
    part of the final creation's block they make it look perfectly well connected -- and
    `Poppo von Berg-Schelklingen zu Roggenstein` IS the last creation in the file and IS one of
    the three isolates. The first version of the guard missed him and only him.
    """
    lines = (_block("Poppo von Berg-Schelklingen zu Roggenstein", "6000000002187828621")
             + ["", "# RELATIONSHIPS between items that already exist",
                'Q5916189\tP22\tQ5916162\tS2600\t"6000000021501491188"',
                'Q5916189\tP25\tQ4988935\tS2600\t"6000000021501491188"'])
    kept, dropped = qs_v1.drop_orphaned_creations(lines)
    assert dropped == ["Poppo von Berg-Schelklingen zu Roggenstein"]
    # The relationships section is not a creation and must survive untouched.
    assert 'Q5916189\tP22\tQ5916162\tS2600\t"6000000021501491188"' in kept


def test_a_name_item_is_not_an_isolate():
    """A name item carries no relationship and is not supposed to. Only `P31 Q5` is a person."""
    lines = ["CREATE",
             'LAST\tLen\t"Simonsdotter"',
             'LAST\tLmul\t"Simonsdotter"',
             'LAST\tDen\t"patronymic"',
             "LAST\tP31\tQ110874",
             ""]
    kept, dropped = qs_v1.drop_orphaned_creations(lines)
    assert dropped == []
    assert kept == lines


def test_the_picker_never_chooses_a_child_outside_the_universe():
    """⛔ The ROOT cause, and the docstring said it while the code tested something else.

    `eligible()` read *"The CHILD must be in the universe"* and tested `qid` -- that the child
    is on Wikidata at all, a far larger set than `out/wikidata/edit-universe.json`. Every pick
    outside that artifact loses its only relationship to the locality filter and becomes an
    isolate.
    """
    spec = importlib.util.spec_from_file_location(
        "ancestor_creations",
        pathlib.Path(__file__).resolve().parents[1] / "scripts" / "build-ancestor-creations.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    owner = mod.OWNER
    # owner -> in-universe child with a known parent, and an OUT-of-universe child with one.
    fam = {
        owner: ("Q141216494", "inside", "QIN", "outside", "QOUT"),
        "inside": ("QIN", "parent_of_inside", "", "", ""),
        "outside": ("QOUT", "parent_of_outside", "", "", ""),
    }
    mod._universe = lambda: {"Q141216494", "QIN"}
    picks = mod.eligible(fam)
    chosen_parents = {p for _g, _q, p, _r in picks}
    assert "parent_of_inside" in chosen_parents
    assert "parent_of_outside" not in chosen_parents, (
        "a child outside the edit universe loses its reciprocal to the locality filter, so the "
        "creation hung off it is an isolate the moment it is made")
