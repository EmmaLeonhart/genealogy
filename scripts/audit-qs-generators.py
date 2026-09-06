"""Which QuickStatements batches in `reports/` are produced by anything, and by anything scheduled?

    python scripts/audit-qs-generators.py

**Emma, 2026-09-05**, on finding a per-day cap sitting on a script nothing ran: *"Uhh I'm just
confused why are these segregated in code?"* The answer was that it was not segregated by design
-- it was abandoned, which is `CLAUDE.md` § *Code that is WRITTEN but never CALLED is not done*.

This makes the question answerable rather than a thing to notice by accident. A `.qs` is
*produced* when some script under `scripts/` names it, and *scheduled* when that script is named
in a workflow. Neither test is clever, and both are the ones that matter: a generator nobody
calls is the failure, and a batch file nobody generates is either a record or a relic.

**It deletes nothing and decides nothing.** Whether an unscheduled generator should be folded
into the daily batch, given its own schedule, or removed is hers.
"""

from __future__ import annotations

import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    scripts = list((ROOT / "scripts").glob("*.py"))
    workflows = "\n".join(
        p.read_text(encoding="utf-8", errors="replace")
        for p in (ROOT / ".github" / "workflows").glob("*.yml"))
    scheduled = set(re.findall(r"scripts/([A-Za-z0-9_\-]+\.py)", workflows))

    counts = {"scheduled": 0, "unscheduled": 0, "orphan": 0}
    for qs in sorted((ROOT / "reports").glob("*.qs")):
        producers = [s.name for s in scripts
                     if qs.name in s.read_text(encoding="utf-8", errors="replace")]
        runs = [p for p in producers if p in scheduled]
        date = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", str(qs)],
            capture_output=True, text=True, cwd=ROOT).stdout.strip()
        if runs:
            state, counts["scheduled"] = "SCHEDULED: " + ", ".join(runs), counts["scheduled"] + 1
        elif producers:
            state = "generator exists, NOT scheduled: " + ", ".join(producers)
            counts["unscheduled"] += 1
        else:
            state, counts["orphan"] = "NO GENERATOR AT ALL", counts["orphan"] + 1
        print(f"  {qs.name:50s} {date:12s} {state}")

    print(f"\nscheduled {counts['scheduled']} | generator but unscheduled "
          f"{counts['unscheduled']} | no generator {counts['orphan']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
