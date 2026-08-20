#!/usr/bin/env python3
"""Guard: is Wikidata editing currently allowed, or is a lockout in force?

Emma, 2026-08-18: "I want a gate to be set up that there will be no wikidata
editing for a month." This repo has its OWN Wikidata editor with its own
bot-password secrets (`scripts/wikidata-edit-run.py`, `wikidata-edits.yml`), and
its `START_DATE` of 2026-09-01 falls inside that month. A gate that covered only
the shintowiki bots would have left this path open.

**There is exactly one lockout state file for all of Emma's repos**, and it is
NOT in this one. Its location is held in the ``LOCKOUT_STATE_URL`` secret rather than
written here: Emma, 2026-08-18, *"no fucking github links in it either"* — an agent or a
source file that names her repositories tells a reader where to look, and that applies to
a URL in a constant as much as to a User-Agent.

That file is public, so this reads it over plain HTTPS with no credentials. It is
deliberately NOT copied here: the mechanism this replaced was a freeze date pasted
into two workflow files, and one of them missed a freeze. A local copy would be
the same mistake across two repos instead of two files. To lift or extend the
lockout, edit that ONE file.

**Fails CLOSED.** Any error — no network, a 404, unparseable JSON — reports LOCKED.
A lockout you cannot read is not an absent lockout, and the standing rule on the
Wikidata side is that being visible is worse than losing data. The cost of failing
closed is a skipped run; the cost of failing open is editing through a stop order.

    python scripts/wikidata_lockout.py     # exit 0 = allowed, 1 = locked
"""

from __future__ import annotations

from bot_identity import BOT_USER_AGENT

import datetime
import io
import os
import json
import sys
import urllib.request

#: From the ``LOCKOUT_STATE_URL`` secret. Empty when unset, and an empty URL is treated
#: as LOCKED below — the same fail-closed rule the whole module runs on, so a missing
#: secret stops editing rather than silently allowing it.
STATE_URL = os.environ.get("LOCKOUT_STATE_URL", "").strip()

TIMEOUT = 20


def editing_allowed(url: str = "") -> tuple[bool, str]:
    """(allowed, detail). Any failure is LOCKED — see the module docstring."""
    url = url or STATE_URL
    if not url:
        return (False, "LOCKOUT_STATE_URL is not set - locked, because this module "
                       "fails closed and an unconfigured gate is not an open one")
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": BOT_USER_AGENT}
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as fh:
            state = json.loads(fh.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001 — every failure mode lands here on purpose
        return False, f"LOCKED (fail-closed): could not read the lockout state — {e}"

    if not state.get("locked"):
        return True, "wikidata editing not locked"

    locked_until = state.get("locked_until")
    if not locked_until:
        return False, "LOCKED (no expiry date recorded)"
    try:
        until = datetime.date.fromisoformat(locked_until)
    except ValueError:
        return False, f"LOCKED (unparseable locked_until={locked_until!r})"

    today = datetime.datetime.now(datetime.timezone.utc).date()
    if today >= until:
        return True, f"wikidata lockout expired ({locked_until}) — editing resumed"
    return False, f"LOCKED until {locked_until} — {state.get('reason', '')}"


def main() -> int:
    # The reason string carries em-dashes; a cp1252 console must not crash on them.
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    allowed, detail = editing_allowed()
    print(("ALLOWED — " if allowed else "LOCKED — ") + detail)
    return 0 if allowed else 1


if __name__ == "__main__":
    raise SystemExit(main())
