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
#: **The condition for lifting it, ruled 2026-09-13:** *"between everything else in the queue and
#: running stuff on wikidata you must attempt all the wikidata isolates."* Every isolate in
#: `reports/unconnected-p2600.tsv` ATTEMPTED — tried, not necessarily connected, and stamped by
#: `scripts/attempt_ledger.py` so it is a fact in a file. `queue.md` § *Wikidata isolate
#: connection* is the gate and carries the three stages.
#:
#: **⛔ LIFTED 2026-09-14, AND THE CONDITION ABOVE IS SUPERSEDED.** Ruled that evening:
#:
#: > *"the condition has changed ... I made the decision that this is going to take a long time,
#: > the solution is that the agent is triggered to run this thing every single session, and all
#: > it does is it just runs this script and commits and pushes it, and the CI/CD is going to be
#: > able to deal with everything ... It should be wired in right now."*
#:
#: The old gate was *every isolate in `reports/unconnected-p2600.tsv` attempted first*. At the
#: path runner's measured rate that is **261,084 people still to request at roughly 900 an
#: hour** — months, not evenings. It was gating the wrong thing: the isolate sweep needs a real
#: logged-in browser and therefore an agent, while the edits need neither, so holding the edits
#: behind the sweep made the slow half the pacemaker for the fast one.
#:
#: **The division now:**
#:
#:     the agent, once a session   the browser-only work — run scripts/pathrun.js, commit, push
#:     CI/CD, continuously         compose, split, publish and SEND
#:
#: **To put the hold back:** `HELD = True` here and `EDITS_HELD: "yes"` in
#: `.github/workflows/wikidata-edits.yml`. Both, or the halves disagree and
#: `tests/test_wikidata_start_date.py` fails — which is the whole reason it is written twice.
HELD = False

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


#: ⛔ **THE CLAN LABELS DO NOT GO OUT BEFORE THIS DATE.** Ruled 2026-08-29: *"we block the clan
#: name application stuff for one month. In October, once the October gate passes, then the quick
#: statements generate with these clan names in them, but otherwise they do not, because I'm just
#: too sceptical of the clan names."*
#:
#: **It lives here because it was implemented in ONE emitter and a second one routed around it.**
#: `build-garborg-day.py` has had this gate working since the day it was ruled -- it prints
#: `CJK clan labels suppressed until 2026-10-01` on every run -- and it suppresses a hardcoded
#: list of **163 QIDs**. Then `reports/wikidata-cjk-mul-labels.json` was committed by hand on
#: 2026-09-10, `22b82b05`, and `wikidata-edit-run.py` reads it directly: **1,431 clan-seat
#: labels, none of the 163, gate not consulted.** § *A GUARD IN ONE EMITTER IS NOT A GUARD*.
#:
#: Emma, 2026-09-14, on being shown the 1,431 as though they were news: *"I'm pretty sure this is
#: a thing that was resolved like two weeks ago ... we came up with a solution, and you might have
#: just not implemented it."* Correct on both halves -- the solution was real and it was
#: implemented in one place.
#:
#: So the test is PROVENANCE, not a QID list. An edit that says it was derived from a clan seat
#: is a clan label whatever batch it arrives in and whoever wrote it, and a list of ids can only
#: ever cover the ids somebody remembered to add. `build-garborg-day.CLAN_BLOCK_GATE` reads this
#: date rather than keeping a second copy -- two copies of one date is the bug this module exists
#: for.
CLAN_BLOCK_GATE = datetime.date(2026, 10, 1)

#: What a clan-seat label says about itself in its `derived_from`. The batch's own wording is
#: `carries the clan seat 隆西狄道, which is Chinese`; matching the stable part of it.
_CLAN_SEAT_MARK = "clan seat"


def is_clan_seat_edit(edit) -> bool:
    """True when this edit object is a label derived from a Chinese clan seat (郡望)."""
    if not isinstance(edit, dict):
        return False
    return _CLAN_SEAT_MARK in str(edit.get("derived_from") or "")


def clan_labels_allowed(today: datetime.date | None = None) -> tuple[bool, str]:
    """Whether clan-seat labels may be emitted yet.

    Independent of `HELD` on purpose: this answers *is this KIND of edit ready*, while `HELD`
    answers *is editing open at all*. A caller needs both and they lift on different days.
    """
    today = today or datetime.date.today()
    if today >= CLAN_BLOCK_GATE:
        return True, f"clan labels allowed - {today} is on or after {CLAN_BLOCK_GATE}"
    return False, f"CJK clan labels suppressed until {CLAN_BLOCK_GATE} (ruled 2026-08-29)"


def drop_clan_labels(edits, today: datetime.date | None = None):
    """`(kept, dropped)` -- the clan-seat labels removed while the gate is shut."""
    allowed, _why = clan_labels_allowed(today)
    if allowed:
        return list(edits), []
    kept, dropped = [], []
    for e in edits:
        (dropped if is_clan_seat_edit(e) else kept).append(e)
    return kept, dropped


def main() -> int:
    # The detail string is ASCII, but a cp1252 console has crashed on this output
    # before; the wrapper stays.
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    allowed, detail = editing_allowed()
    print(("ALLOWED - " if allowed else "LOCKED - ") + detail)
    return 0 if allowed else 1


if __name__ == "__main__":
    raise SystemExit(main())
