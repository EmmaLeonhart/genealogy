"""The Wikidata start date is written in two places, so pin them together.

`scripts/wikidata_lockout.py` carries `START_DATE` and
`.github/workflows/wikidata-edits.yml` carries `START_DATE:`. Two copies of one
date is exactly the shape that produced the bug this module was rewritten to fix:
a freeze recorded in one place, read from another, and nobody noticing they had
come apart.

They are written twice on purpose — the workflow gates before it checks out the
repo, so it cannot import the module — which makes an automated check the only
thing keeping them equal.

**The gate fails closed**, and that half matters more than the date. An unreadable
date must report LOCKED: the cost of failing closed is a skipped run, the cost of
failing open is editing through a stop order.

Nothing here asserts *which* date it is beyond what the repo already declares, so
moving the date is a one-line change in two files and this test follows it.
"""

from __future__ import annotations

import datetime
import re
import sys

import pytest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import wikidata_lockout  # noqa: E402

WORKFLOW = REPO / ".github" / "workflows" / "wikidata-edits.yml"


@pytest.fixture
def dates_only(monkeypatch):
    """Lift `HELD` so the DATE mechanism can be tested while the hold is on.

    **This is the fix for four tests that were red on `main` every day from at least
    2026-09-10 to 2026-09-14**, and being red is the whole of what they did wrong: the gate was
    behaving exactly as designed. `editing_allowed` checks `HELD` first and returns
    `HELD - ...` for every input, so four tests written about the dates -- *allowed on the day
    itself*, *fail-closed on an unreadable date* -- were asserting things the hold makes
    unreachable, and they will go red again on the day the hold is next applied.

    **A permanently-red suite is not a small problem, it is the mechanism.** Eleven tests were
    failing and four of them were these; that is what teaches a reader that red means nothing,
    and underneath it `test_no_numeral_gets_a_name_item_in_any_notation` had been failing since
    the day it was written on `'--' would get a name item` -- a real guard, really broken, for a
    day and a half, minting junk name items the entire time.

    So the hold is now a PASSING state. The date logic stays under test while held, which is
    what makes it safe to lift; the hold itself is tested separately and without this fixture by
    `test_a_hold_refuses_regardless_of_the_dates`, which is the test that must never be
    bypassed. Nothing here can lift the hold in production: `HELD` is a module constant read at
    call time, and `monkeypatch` puts it back.
    """
    monkeypatch.setattr(wikidata_lockout, "HELD", False)


def workflow_start_date():
    text = WORKFLOW.read_text(encoding="utf-8")
    m = re.search(r'^\s*START_DATE:\s*"([0-9]{4}-[0-9]{2}-[0-9]{2})"\s*$',
                  text, re.M)
    assert m, "no START_DATE in wikidata-edits.yml"
    return m.group(1)


def test_the_two_copies_of_the_start_date_agree():
    assert wikidata_lockout.START_DATE == workflow_start_date()


def test_the_start_date_is_a_real_date():
    datetime.date.fromisoformat(wikidata_lockout.START_DATE)


def test_editing_is_locked_the_day_before(dates_only):
    start = datetime.date.fromisoformat(wikidata_lockout.START_DATE)
    allowed, why = wikidata_lockout.editing_allowed(
        start - datetime.timedelta(days=1))
    assert not allowed, why


def test_editing_is_allowed_on_the_day_itself(dates_only):
    start = datetime.date.fromisoformat(wikidata_lockout.START_DATE)
    allowed, why = wikidata_lockout.editing_allowed(start)
    assert allowed, why


def test_an_unreadable_date_fails_closed(dates_only, monkeypatch):
    """The half that matters: a broken gate is a shut gate, never an open one."""
    monkeypatch.setenv("WIKIDATA_START_DATE", "not-a-date")
    allowed, why = wikidata_lockout.editing_allowed(datetime.date(2099, 1, 1))
    assert not allowed
    assert "fail-closed" in why


def test_nothing_in_the_gate_reaches_the_network():
    """It used to fetch another repo's state file over HTTPS, and failed closed on
    every network error — so an outage read as a stop order. The shintowiki
    scripts and this repo are not the same and are not coordinated; that
    coupling was invented here, not observed."""
    source = (REPO / "scripts" / "wikidata_lockout.py").read_text(encoding="utf-8")
    body = "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith("#")
    )
    for banned in ("urllib", "http", "LOCKOUT_STATE_URL", "urlopen"):
        assert banned not in body.split('"""')[-1], (
            f"the start-date gate reaches for {banned!r}; it must be local only"
        )


# ---------------------------------------------------------------------------
# THE SECOND DATE: on the 15th all of this starts running automatically — the
# daily Garborg batch, through the bot-password API.
#
# It is written twice for exactly the reason the first one is: the workflow's
# `Decide what this run does` step compares dates in bash, before the module
# could be imported even if it wanted to. Two copies of a date is the shape that
# produced the bug this file exists for, so it gets the same pin.
# ---------------------------------------------------------------------------


def workflow_automation_start_date():
    text = WORKFLOW.read_text(encoding="utf-8")
    m = re.search(r'^\s*AUTOMATION_START_DATE:\s*"([0-9]{4}-[0-9]{2}-[0-9]{2})"\s*$',
                  text, re.M)
    assert m, "no AUTOMATION_START_DATE in wikidata-edits.yml"
    return m.group(1)


def test_the_two_copies_of_the_automation_date_agree():
    assert (wikidata_lockout.AUTOMATION_START_DATE
            == workflow_automation_start_date())


def test_the_automation_date_is_a_real_date():
    datetime.date.fromisoformat(wikidata_lockout.AUTOMATION_START_DATE)


def test_the_automation_starts_no_earlier_than_editing_does():
    """A schedule that went live before editing was allowed would be a gate that
    opens a door behind a locked one. Ordering them is cheaper than reasoning
    about which check fires first."""
    assert (datetime.date.fromisoformat(wikidata_lockout.AUTOMATION_START_DATE)
            >= datetime.date.fromisoformat(wikidata_lockout.START_DATE))


def test_the_automation_is_locked_the_day_before_and_open_on_the_day(dates_only):
    start = datetime.date.fromisoformat(wikidata_lockout.AUTOMATION_START_DATE)
    before, why = wikidata_lockout.automation_allowed(
        start - datetime.timedelta(days=1))
    assert not before, why
    on, why = wikidata_lockout.automation_allowed(start)
    assert on, why


def test_the_automation_gate_also_fails_closed(dates_only, monkeypatch):
    monkeypatch.setenv("WIKIDATA_AUTOMATION_START_DATE", "the-fifteenth")
    allowed, why = wikidata_lockout.automation_allowed(datetime.date(2099, 1, 1))
    assert not allowed
    assert "fail-closed" in why


def test_the_scheduled_run_sends_the_daily_batch_and_a_receipt():
    """The two things that make the schedule safe to leave alone.

    The batch must be the daily file rather than whatever a dispatch defaults to,
    and the receipt must be passed — without it a re-sent batch mints the same
    people again, which is the one failure of this design that cannot be undone
    by running it correctly next time.
    """
    text = WORKFLOW.read_text(encoding="utf-8")
    assert 'DAILY_BATCH: reports/wikidata-garborg-day.txt' in text
    assert "--receipt" in text
    assert 'echo "batch=$DAILY_BATCH"' in text


# --------------------------------------------------------------------------------------
# **THE HOLD, 2026-09-13.** *"disable any editing of Wikidata by this, uh, by the runner
# right now so that... because we aren't ready for it. And the queue structure was supposed
# to make that be the case."* Written in two places for the same reason the dates are: the
# workflow gates before it can check the repo out and cannot import the module.
# --------------------------------------------------------------------------------------

def test_the_hold_is_written_the_same_in_both_places():
    """`HELD` and `EDITS_HELD` say the same thing, or the next lift only lifts half of it."""
    import re
    text = (REPO / ".github" / "workflows" / "wikidata-edits.yml").read_text(encoding="utf-8")
    m = re.search(r'^\s*EDITS_HELD:\s*"(yes|no)"\s*$', text, re.M)
    assert m, "wikidata-edits.yml has no EDITS_HELD line"
    assert (m.group(1) == "yes") == wikidata_lockout.HELD, (
        "the workflow and scripts/wikidata_lockout.py disagree about the hold")


def test_a_hold_refuses_regardless_of_the_dates():
    """No environment override lifts a hold — that is what makes it a stop order."""
    if not wikidata_lockout.HELD:
        return
    allowed, why = wikidata_lockout.editing_allowed()
    assert not allowed and "HELD" in why
    allowed, why = wikidata_lockout.automation_allowed()
    assert not allowed and "HELD" in why
