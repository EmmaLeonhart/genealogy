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
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import wikidata_lockout  # noqa: E402

WORKFLOW = REPO / ".github" / "workflows" / "wikidata-edits.yml"


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


def test_editing_is_locked_the_day_before():
    start = datetime.date.fromisoformat(wikidata_lockout.START_DATE)
    allowed, why = wikidata_lockout.editing_allowed(
        start - datetime.timedelta(days=1))
    assert not allowed, why


def test_editing_is_allowed_on_the_day_itself():
    start = datetime.date.fromisoformat(wikidata_lockout.START_DATE)
    allowed, why = wikidata_lockout.editing_allowed(start)
    assert allowed, why


def test_an_unreadable_date_fails_closed(monkeypatch):
    """The half that matters: a broken gate is a shut gate, never an open one."""
    monkeypatch.setenv("WIKIDATA_START_DATE", "not-a-date")
    allowed, why = wikidata_lockout.editing_allowed(datetime.date(2099, 1, 1))
    assert not allowed
    assert "fail-closed" in why


def test_nothing_in_the_gate_reaches_the_network():
    """It used to fetch another repo's state file over HTTPS, and failed closed on
    every network error — so an outage read as a stop order. Emma, 2026-08-23:
    *"Shintowiki scripts and this one are not the same and not really
    coordinated."* The coupling was invented here, not observed."""
    source = (REPO / "scripts" / "wikidata_lockout.py").read_text(encoding="utf-8")
    body = "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith("#")
    )
    for banned in ("urllib", "http", "LOCKOUT_STATE_URL", "urlopen"):
        assert banned not in body.split('"""')[-1], (
            f"the start-date gate reaches for {banned!r}; it must be local only"
        )


# ---------------------------------------------------------------------------
# THE SECOND DATE. Emma, 2026-09-05: "I want to on the 15th start all of this
# stuff automatically" — the daily Garborg batch, through the bot-password API.
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


def test_the_automation_is_locked_the_day_before_and_open_on_the_day():
    start = datetime.date.fromisoformat(wikidata_lockout.AUTOMATION_START_DATE)
    before, why = wikidata_lockout.automation_allowed(
        start - datetime.timedelta(days=1))
    assert not before, why
    on, why = wikidata_lockout.automation_allowed(start)
    assert on, why


def test_the_automation_gate_also_fails_closed(monkeypatch):
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
