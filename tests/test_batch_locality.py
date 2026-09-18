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
    non_local, on_kanji = check.offenders(path, allowed, check.kanji_items())
    assert not non_local, (
        f"{rel}: {len(non_local)} item(s) neither in the universe nor one step beyond it, "
        f"first at line {min(non_local.values())}: " + ", ".join(sorted(non_local)[:8])
        + " -- CLAUDE.md: ALL EDITS, NO EXCEPTIONS")
    assert not on_kanji, (
        f"{rel}: label edits on {len(on_kanji)} item(s) whose ja label is KANJI, which marks a "
        f"Sinosphere name and takes no label edit in any language: "
        + ", ".join(sorted(on_kanji)[:8]))


def test_an_absent_universe_is_not_permission():
    """A missing universe file must never read as 'everything is allowed'."""
    assert check.universe() is None or check.universe(), "universe() must be None or non-empty"
