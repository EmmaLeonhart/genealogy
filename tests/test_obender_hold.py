"""The month-long hold on items `OBender12` has touched.

Emma's control, 2026-08-30, recorded in `reports/strategic-analysis-2026-08-30.md`
§ *Decisions*: *any item `OBender12` has touched is locked — our QuickStatements may not edit
it.* The hold is on the full contributions list rather than its overlap with the ledger, and it
expires on its own so that nothing has to remember to lift it.

What these pin is the part that is easy to get wrong under a rebuild: the hold is on the
**subject** of a statement and never on its value, and it lapses on the date.
"""
from __future__ import annotations

import datetime
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

spec = importlib.util.spec_from_file_location(
    "build_garborg_day", ROOT / "scripts" / "build-garborg-day.py")
bgd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bgd)


@pytest.fixture()
def touched(tmp_path, monkeypatch):
    """A stand-in contributions file, so the test does not depend on the real fetch."""
    p = tmp_path / "obender12-touched.tsv"
    p.write_text(
        "qid\tfirst_touched\tlast_touched\tedits\n"
        "Q141180409\t2026-08-29T10:00:00Z\t2026-08-30T09:00:00Z\t3\n"
        "Q633094\t2026-08-30T11:00:00Z\t2026-08-30T11:00:00Z\t1\n",
        encoding="utf-8")
    monkeypatch.setattr(bgd, "OBENDER_TOUCHED", p)
    return p


def test_the_hold_reads_the_contributions_file(touched):
    held = bgd.held_items(today=datetime.date(2026, 9, 1))
    assert held == {"Q141180409", "Q633094"}


def test_the_hold_expires_on_its_own(touched):
    """A hold that must be remembered to be lifted is a hold that never lifts.

    The premise of the whole control is that an editor's recognition decays; a permanent
    exclusion would outlive the thing it protects against.
    """
    assert bgd.held_items(today=bgd.OBENDER_HOLD_EXPIRES) == set()
    assert bgd.held_items(today=datetime.date(2026, 12, 25)) == set()


def test_a_missing_file_holds_nothing_rather_than_failing(tmp_path, monkeypatch):
    """A clean checkout has not run the fetch, and must still be able to build a batch."""
    monkeypatch.setattr(bgd, "OBENDER_TOUCHED", tmp_path / "absent.tsv")
    assert bgd.held_items(today=datetime.date(2026, 9, 1)) == set()


def test_the_hold_is_on_the_subject_and_never_on_the_value(touched):
    """`Q1 P22 Q2` is an edit to `Q1`. `Q2` is referenced, and appears on nobody's watchlist.

    Holding values too would drop most of the ring -- the items that editor merged are the
    well-connected ones -- and would reduce nothing that they actually see.
    """
    held = bgd.held_items(today=datetime.date(2026, 9, 1))
    subject_line = 'Q141180409\tP22\tQ99999'
    value_line = 'Q99999\tP22\tQ141180409'
    assert subject_line.split("\t")[0] in held
    assert value_line.split("\t")[0] not in held
