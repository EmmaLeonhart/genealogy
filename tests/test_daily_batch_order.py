"""`build-daily-batch.py` — step 0's second half, and where in the run it sits.

`docs/daily-algorithm.md` § *Step 0* is two halves: read her Wikidata contributions into the
ledger, then **take those out and check what remains against the ideal state**. Only the first
half was wired into the orchestrator; `queue.md` carried the second as *"model-vs-reality.py is
the diff and is not yet wired into the daily command"*.

The two things worth pinning are the ones that would silently regress:

* **the diff runs before the three generators.** After them it is a post-mortem of the day
  rather than a check on it, and it would still print a plausible-looking table either way.
* **the summary keeps `missing` and `CONFLICT` and drops rows that are `extra` alone.**
  `extra` is Emma's hand-work and is never touched; the full table is 90-odd rows of it, which
  is how a summary stops being one.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def daily():
    spec = importlib.util.spec_from_file_location(
        "build_daily_batch", REPO / "scripts" / "build-daily-batch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


#: A real run's output, trimmed. The property table is the shape `model-vs-reality.py` prints.
DIFF_OUTPUT = """657 people in garborg-qids.tsv
using the cached snapshot, 0.0 hours old -- pass --refetch to renew.
657 items held

9,376 differences over 657 people

   9,198  extra
     127  missing
      51  CONFLICT

BY PROPERTY -- a CONFLICT repeated across people is ONE RULE that is wrong,
not N separate errors. That is the whole reason for this file:

   property    missing   extra  CONFLICT
   P734              3     223         4
   P1449            66       0         0
   P3373             0      22         0
   P27               0      13         0

wrote reports\\model-vs-reality.tsv
NOTHING IS EMITTED. A batch is a projection of the `missing` column and of nothing else.
"""


def test_the_summary_keeps_what_moves_and_drops_hand_work(daily):
    kept = daily.diff_summary(DIFF_OUTPUT)
    assert "127  missing" in kept
    assert "51  CONFLICT" in kept
    # Both of these are `extra` alone -- 22 siblings and 13 countries Emma added by hand.
    assert "P3373" not in kept
    assert "P27 " not in kept
    # Both of these move: one on every column, one on `missing` alone.
    assert "P734" in kept
    assert "P1449" in kept
    # The freshness line is the reason the flag exists and must survive the trim.
    assert "cached snapshot" in kept
    # The prose is not a summary.
    assert "NOTHING IS EMITTED" not in kept
    assert "N separate errors" not in kept


def test_a_stale_snapshot_reports_itself_rather_than_diffing_71_of_657(daily):
    """`ITEM NOT FETCHED` is how the diff says it is measuring the wrong population.

    On 2026-08-30 the cached snapshot held 71 items against a ledger of 657, so 587 rows read
    `ITEM NOT FETCHED` and the diff was over a ninth of the day. It is a count, so it survives
    the trim -- a summary that hid it would report 1,230 differences and mean nothing.
    """
    kept = daily.diff_summary("     587  ITEM NOT FETCHED\n     166  missing\n")
    assert "ITEM NOT FETCHED" in kept


def test_the_diff_runs_before_the_generators(daily, monkeypatch, capsys):
    calls = []

    def fake_run(script, args):
        calls.append(script)
        return ""

    monkeypatch.setattr(daily, "run", fake_run)
    monkeypatch.setattr(daily.sys, "argv", ["build-daily-batch.py"])
    daily.main()
    capsys.readouterr()

    assert "model-vs-reality.py" in calls, "step 0c never ran"
    assert calls.index("model-vs-reality.py") < calls.index("build-garborg-day.py"), (
        "the diff must run before the generators; after them it is a post-mortem")


def test_the_refetch_is_bound_to_the_ledger_refresh(daily, monkeypatch, capsys):
    """One flag, one network day. A refreshed ledger against a frozen snapshot is the
    mismatch that produced 587 `ITEM NOT FETCHED` rows in the first place."""
    seen = {}

    def fake_run(script, args):
        seen[script] = list(args)
        return ""

    monkeypatch.setattr(daily, "run", fake_run)
    monkeypatch.setattr(daily.sys, "argv", ["build-daily-batch.py", "--refresh-ledger"])
    daily.main()
    capsys.readouterr()
    assert seen["model-vs-reality.py"] == ["--refetch"]

    seen.clear()
    monkeypatch.setattr(daily.sys, "argv", ["build-daily-batch.py"])
    daily.main()
    capsys.readouterr()
    assert seen["model-vs-reality.py"] == []
