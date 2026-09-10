"""Stamp every id the EXTENSION recorded as attempted. Reads a dump, picks nothing.

    PYTHONPATH=src python scripts/stamp-attempts.py < attempted.json

⛔ **THE EXTENSION DECIDES WHO WAS ATTEMPTED, NOT THE AGENT.**

Ruled 2026-09-10: *"the extension should be scraping the page and adding and basically just
writing into the file automatically whether it has tried the page. It's not agentic."*

`attempt_ledger.py` already does the stamping and already documents why it is a script rather
than extension code -- **nothing downloads**, so the extension cannot write into the repo, and
every file the collector produces is written by a script instead. That constraint stands.

The part that was agentic was never the writing. It was the **choosing**. On 2026-09-10 fourteen
people whom Geni answered `429` for were stamped by typing their ids into a command line, which
means a person decided which attempts counted -- and the same person could have decided they did
not count, which is exactly the exception the ruling forbids:

> *"You aren't trying to do some sort of exception where you decide, oh, we didn't really do
> these people, and you don't list them as being attempted. They've been attempted."*

So the extension keeps an `attempted` list in its own storage, appending every id it runs on
whatever the outcome -- a hit, a miss, a rate-limit, an error. This reads that list and stamps
all of it. There is no id argument and there is deliberately no filter: a state this script
refused to stamp would be a state somebody chose to un-attempt.

`attempt_ledger.py` never mints a row (§ *IT NEVER ADDS A ROW*), so an id that is not in the
worklist -- already connected, or not a `P2600` holder -- is counted and ignored, exactly as it
is on the ordinary path.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_stdin() -> str:
    """UTF-8 explicitly. `sys.stdin.read()` decodes by locale on Windows, which is the mojibake
    bug `write-family-scrape.py` carries the same guard against."""
    buf = getattr(sys.stdin, "buffer", None)
    if buf is not None:
        return buf.read().decode("utf-8", errors="replace")
    return sys.stdin.read()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    raw = read_stdin().strip()
    if not raw:
        print("nothing on stdin: no attempts to stamp")
        return 0

    data = json.loads(raw)
    rows = data if isinstance(data, list) else data.get("attempted", [])

    # Order preserved, duplicates dropped: a person walked twice in one run is one attempt.
    ids, seen = [], set()
    for r in rows:
        gid = str(r.get("geni_id") if isinstance(r, dict) else r).strip()
        if gid and gid not in seen:
            seen.add(gid)
            ids.append(gid)

    if not ids:
        print("no geni ids in the dump")
        return 0

    by_state: dict[str, int] = {}
    for r in rows:
        if isinstance(r, dict):
            by_state[r.get("state") or "(none)"] = by_state.get(r.get("state") or "(none)", 0) + 1
    print("attempts from the extension: %d ids, states: %s"
          % (len(ids), ", ".join("%s=%d" % kv for kv in sorted(by_state.items()))))

    # Straight through to the existing ledger. Nothing is filtered on the way.
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "attempt_ledger.py"), *ids],
        cwd=str(ROOT),
    )
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
