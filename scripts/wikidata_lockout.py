#!/usr/bin/env python3
"""Guard: may this repo edit Wikidata yet?

**This repo's own date, and nothing else.** Emma, 2026-08-23: *"Shintowiki scripts
uses a different lockdown period lol. This repo starts at sept 1"*, and then:
*"Shintowiki scripts and this one are not the same and not really coordinated."*

So the coupling is gone. This module used to fetch a lockout state file belonging
to `shintowiki-scripts` over HTTPS, wired there by an earlier session on the
reasoning that this repo's 2026-09-01 start fell inside that repo's month-long
freeze. Two repos that are not coordinated must not gate each other: that setup
**failed closed**, so from 2026-09-01 it would have silently blocked editing this
repo is entitled to do, for a reason belonging to somewhere else — and it would
have looked exactly like a run with nothing to do.

What replaces it is the date this repo already declares. `wikidata-edits.yml`
carries ``START_DATE: "2026-09-01"``; this is the same date on the live path, so a
local run is covered too and neither can drift without the other failing.

**Still fails CLOSED.** An unparseable or missing date reports LOCKED. The cost of
failing closed is a skipped run; the cost of failing open is editing through a stop
order. No network is involved any more, so the failure modes that used to reach
here — no route, a 404, a truncated body — cannot.

    python scripts/wikidata_lockout.py     # exit 0 = allowed, 1 = locked
"""

from __future__ import annotations

import datetime
import io
import os
import sys

#: The date this repo may begin editing Wikidata. Emma, 2026-08-14: *"no wikidata
#: edits until September 1"*. It matches ``START_DATE`` in
#: ``.github/workflows/wikidata-edits.yml``; `tests/test_wikidata_start_date.py`
#: fails if the two ever disagree, which is the whole reason to write it twice.
START_DATE = "2026-09-01"

#: The date the daily batch starts running BY ITSELF. Emma, 2026-09-05: *"I want to
#: on the 15th start all of this stuff automatically"*, and asked what starts, "The
#: daily Garborg batch", sent through the bot-password API.
#:
#: It is a second date rather than a move of the first, because they gate different
#: things and both stay true. ``START_DATE`` is when this repo may edit Wikidata at
#: all, and it has been in force since 2026-09-01 — a hand-dispatched live run is
#: allowed today. This one is when the *schedule* stops being a dry run. Collapsing
#: them into one would either back-date the automation or re-lock the manual path.
#:
#: Mirrored as ``AUTOMATION_START_DATE:`` in ``.github/workflows/wikidata-edits.yml``
#: for the same reason as ``START_DATE``: the workflow gates before it checks the
#: repo out and cannot import this module. `tests/test_wikidata_start_date.py` fails
#: if the two disagree.
AUTOMATION_START_DATE = "2026-09-15"

#: Escape hatch for a dry run against a date that has not arrived. Never set in
#: CI: the workflow gates on its own ``START_DATE`` before this module is reached.
_OVERRIDE = "WIKIDATA_START_DATE"

#: The same escape hatch for the automation date. Same rule: never set in CI.
_AUTOMATION_OVERRIDE = "WIKIDATA_AUTOMATION_START_DATE"


def _after(raw: str, today: datetime.date | None, what: str) -> tuple[bool, str]:
    try:
        start = datetime.date.fromisoformat(raw)
    except ValueError:
        return False, f"LOCKED (fail-closed): unparseable start date {raw!r}"

    if today is None:
        today = datetime.datetime.now(datetime.timezone.utc).date()

    if today >= start:
        return True, f"{what} allowed - {today} is on or after {start}"
    return False, f"LOCKED until {start} - today is {today}"


def editing_allowed(today: datetime.date | None = None) -> tuple[bool, str]:
    """(allowed, detail). Anything unreadable is LOCKED — see the module docstring."""
    return _after(os.environ.get(_OVERRIDE, "").strip() or START_DATE,
                  today, "editing")


def automation_allowed(today: datetime.date | None = None) -> tuple[bool, str]:
    """(allowed, detail) for the SCHEDULED run, which starts later than the manual one.

    A caller must pass both gates: this one says the schedule may go live, and
    `editing_allowed` still says whether editing is permitted at all.
    """
    return _after(os.environ.get(_AUTOMATION_OVERRIDE, "").strip()
                  or AUTOMATION_START_DATE, today, "automation")


def main() -> int:
    # The detail string is ASCII, but a cp1252 console has crashed on this output
    # before; the wrapper stays.
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    allowed, detail = editing_allowed()
    print(("ALLOWED - " if allowed else "LOCKED - ") + detail)
    return 0 if allowed else 1


if __name__ == "__main__":
    raise SystemExit(main())
