"""`genimerge.editorder` — Emma's resolver, and the ways it must not be wrong.

Her design, 2026-08-23: *"it randomly selects an edit object, sees if its
requirements are present, if they are then it runs, if no then randomly select and
run another one."*

Two failure modes are worth more than the happy path:

* **Running an edit before its prerequisite.** On the 1,271 items whose only `NN`
  lives in `en`, applying the `en` edit before the `mul` one erases the marker. A
  resolver that gets this wrong is worse than no resolver, because it looks careful.
* **Treating "nothing runnable" as "finished".** That silently drops the tail. It
  raises `Blocked` instead, and the test below is what stops someone helpfully
  changing that to a `return`.

Randomness is checked by running many seeds and asserting the invariant holds in
every one — not by pinning one order, which would test the shuffle rather than the
constraint.
"""
from __future__ import annotations

import pytest

from genimerge.editorder import Blocked, run_when_ready, runnable_order


def edit(name, *requires):
    return {"id": name, "requires": list(requires)}


def positions(order):
    return {e["id"]: i for i, e in enumerate(order)}


def test_an_edit_never_precedes_something_it_requires():
    edits = [edit("c", "b"), edit("b", "a"), edit("a"), edit("d", "a")]
    for seed in range(50):
        at = positions(runnable_order(edits, seed=seed))
        assert at["a"] < at["b"] < at["c"]
        assert at["a"] < at["d"]


def test_every_edit_is_run_exactly_once():
    edits = [edit(n) for n in "abcdef"]
    for seed in range(20):
        order = runnable_order(edits, seed=seed)
        assert sorted(e["id"] for e in order) == list("abcdef")


def test_the_nn_case_the_module_exists_for():
    """`mul` carries the marker; `en` reuses the slot. Order is not optional."""
    edits = [
        {"id": "en_label:Q1", "requires": ["nn_preserve:Q1"]},
        {"id": "nn_preserve:Q1", "requires": []},
    ]
    for seed in range(30):
        at = positions(runnable_order(edits, seed=seed))
        assert at["nn_preserve:Q1"] < at["en_label:Q1"]


def test_a_dependency_nothing_carries_blocks_rather_than_being_ignored():
    """55,776 of these sat unnoticed because nothing checked. Not ignored here."""
    with pytest.raises(Blocked) as got:
        runnable_order([edit("a", "does-not-exist")])
    assert got.value.remaining[0]["id"] == "a"


def test_a_cycle_blocks_rather_than_looping_forever():
    with pytest.raises(Blocked):
        runnable_order([edit("a", "b"), edit("b", "a")])


def test_nothing_runnable_is_not_the_same_as_finished():
    """The tail must not be dropped silently — that is the whole point of Blocked."""
    edits = [edit("a"), edit("b", "ghost")]
    with pytest.raises(Blocked) as got:
        runnable_order(edits)
    ids = {e["id"] for e in got.value.remaining}
    assert "b" in ids, "the unorderable edit must be reported"


def test_already_applied_ids_unblock_a_resumed_batch():
    """A second run must not deadlock on work the first one genuinely did."""
    order = runnable_order([edit("b", "a")], satisfied={"a"})
    assert [e["id"] for e in order] == ["b"]


def test_an_empty_batch_is_not_an_error():
    assert runnable_order([]) == []


def test_run_when_ready_applies_in_the_resolved_order():
    seen = []
    edits = [edit("c", "b"), edit("a"), edit("b", "a")]
    out = run_when_ready(edits, lambda e: seen.append(e["id"]) or e["id"], seed=1)
    assert seen == ["a", "b", "c"]
    assert out == ["a", "b", "c"]


def test_run_when_ready_refuses_the_whole_batch_rather_than_half_applying_it():
    """Half-applied is worse than refused: it leaves the wiki mid-edit."""
    ran = []
    with pytest.raises(Blocked):
        run_when_ready([edit("a"), edit("b", "ghost")], ran.append)
    assert ran == [], "nothing may be sent when the batch cannot be ordered"


def test_the_order_actually_varies_across_seeds():
    """Randomised, per her design — so this is not a topological sort in disguise."""
    edits = [edit(n) for n in "abcdefgh"]
    orders = {tuple(e["id"] for e in runnable_order(edits, seed=s))
              for s in range(25)}
    assert len(orders) > 1, "the pick is supposed to be random"


# --- the runner actually uses it ------------------------------------------
#
# `scripts/wikidata-edit-run.py` took `edits[:limit]` in FILE order until
# 2026-08-24, so every `requires` in the repo was decorative. These pin that the
# wiring is present, because a resolver nothing calls protects nothing.

import subprocess
import sys as _sys
from pathlib import Path as _Path

REPO = _Path(__file__).resolve().parent.parent
RUNNER = REPO / "scripts" / "wikidata-edit-run.py"


def _run(*args):
    return subprocess.run([_sys.executable, str(RUNNER), *args],
                          capture_output=True, text=True, cwd=REPO)


def test_the_runner_orders_before_it_slices():
    """A dry run must say so, or the ordering is not in the path that matters."""
    batch = REPO / "reports" / "wikidata-samaritan-priests.json"
    if not batch.exists():
        import pytest
        pytest.skip("samaritan batch not generated")
    out = _run("--batch", "reports/wikidata-samaritan-priests.json",
               "--limit", "3", "--seed", "1")
    assert out.returncode == 0, out.stderr
    assert "ordered by requires" in out.stdout


def test_the_runner_refuses_a_batch_whose_prerequisites_are_elsewhere():
    """`wikidata-mul-labels.json` needs `wikidata-en-labels.json` 14,972 times.

    Refusing is right: running the `en` label edit before the `mul` one erases the
    `NN` marker on the 1,271 items whose only copy lives in `en`. The message has to
    name the providing file, or the refusal is not actionable.
    """
    batch = REPO / "reports" / "wikidata-mul-labels.json"
    if not batch.exists():
        import pytest
        pytest.skip("mul-labels batch not generated")
    out = _run("--batch", "reports/wikidata-mul-labels.json", "--limit", "3")
    assert out.returncode == 1, "a batch that cannot be ordered must not exit 0"
    assert "REFUSED" in out.stderr
    assert "wikidata-en-labels.json" in out.stderr, (
        "the refusal must name the batch that provides what is missing")
