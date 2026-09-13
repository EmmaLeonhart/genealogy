#!/usr/bin/env python3
"""Guard: may this repo edit Wikidata yet?

**This repo's own date, and nothing else.** The shintowiki scripts use a different
lockdown period; this repo starts on 1 September. The two are not the same repo and
are not coordinated.

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

#: ⛔ **EDITING IS HELD, AND THE DATES DO NOT MATTER WHILE IT IS.** Ruled 2026-09-13:
#: *"disable any editing of Wikidata by this, uh, by the runner right now so that... because
#: because we aren't ready for it. And the queue structure was supposed to make that be the
#: case."*
#:
#: **The queue structure was already the rule and it was not honoured.** The Wikidata work sits
#: at the END of `queue.md` — the isolate path campaign is pinned last, and the standing
#: condition is that the Wikidata people get connected through the path search first. Batches
#: went out anyway, which is how `Q45383466` had a Tang-dynasty Chinese man's name replaced by a
#: katakana transliteration of its own romanisation. *"you had no business having any submissions
#: going through until everything was done."*
#:
#: So this is not a date and must not be written as one. A date arrives on its own; a hold is
#: lifted by a person. **Both gates consult it**, so neither the dispatched path nor the schedule
#: can send while it is set, and `--dry-run` is unaffected because a dry run sends nothing.
#:
#: **To lift it:** set `HELD = False` here and `EDITS_HELD: "no"` in
#: `.github/workflows/wikidata-edits.yml`. `tests/test_wikidata_start_date.py` fails if the two
#: disagree, the same way it does for the two dates.
HELD = True

#: Why, in one line, printed by every refusal so a run never just says "locked".
HELD_REASON = ("held by hand 2026-09-13 -- the Wikidata campaign runs AFTER the queue, and the "
               "isolate path connections come first")

#: The date this repo may begin editing Wikidata: no Wikidata edits until
#: 1 September 2026. It matches ``START_DATE`` in
#: ``.github/workflows/wikidata-edits.yml``; `tests/test_wikidata_start_date.py`
#: fails if the two ever disagree, which is the whole reason to write it twice.
START_DATE = "2026-09-01"

#: The date the daily batch starts running BY ITSELF: on the 15th, all of this runs
#: automatically. What starts is the daily Garborg batch, sent through the
#: bot-password API.
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
    """(allowed, detail). Anything unreadable is LOCKED — see the module docstring.

    The hand-set `HELD` flag is checked FIRST and no environment variable lifts it. The date
    overrides exist so a dry run can be exercised against a date that has not arrived; a hold is
    a stop order and an escape hatch through it would be the thing it is protecting against.
    """
    if HELD:
        return False, f"HELD - {HELD_REASON}"
    return _after(os.environ.get(_OVERRIDE, "").strip() or START_DATE,
                  today, "editing")


def automation_allowed(today: datetime.date | None = None) -> tuple[bool, str]:
    """(allowed, detail) for the SCHEDULED run, which starts later than the manual one.

    A caller must pass both gates: this one says the schedule may go live, and
    `editing_allowed` still says whether editing is permitted at all. `HELD` is checked here too
    rather than relying on that pairing: a future caller that forgets one of the two gates must
    not be the thing that lets a held run through.
    """
    if HELD:
        return False, f"HELD - {HELD_REASON}"
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
