"""Stamp the prefix of the worklist the path sweep demonstrably walked.

    PYTHONPATH=src python scripts/stamp-swept-prefix.py --through 6000000058180542103
    PYTHONPATH=src python scripts/stamp-swept-prefix.py --through <id> --apply

⛔ **WHY A RECONSTRUCTION IS LEGITIMATE HERE, AND IT IS BECAUSE THE ORDER WAS DETERMINISTIC.**

`scripts/pathrun.js` recorded nothing for ~9,500 requests -- it wrote `pathrun_cursor` to
localStorage and no more -- so `reports/unconnected-p2600.tsv` carried **248 real attempt dates**
against 221,448 rows still reading `SEED_NEVER`. The campaign therefore re-asked the same people
every session: `build-pathrun-batch.py` differences out only the people a path was FOUND for, and
this population answers *not found* overwhelmingly, so nothing ever aged out.

**The sweep walked the worklist in order, and the order is reproducible**, which is what makes the
prefix recoverable without a record of it. Emma, 2026-09-16: *"we can literally skip over
everything starting at the last ... everything before that point gets a date as though it was run
today ... and then we run everything after it."*

**The evidence that it walked in order.** `/paths` timestamps the last requests before the tab was
lost at 20:33 on 2026-09-14. Their targets, read off `/paths` pages 6 and 7 and looked up in the
committed worklist, land in a contiguous band **in chronological order**:

    15,032  8:30 PM   6000000025498845281
    15,046  8:32 PM   6000000097185779384
    15,070  8:50 PM   6000000014325446498
    15,096  9:00 PM   6000000058180542103

Twenty-five consecutive found targets inside sixty-five positions. That is a cursor, not a
coincidence.

⛔ **A FUTURE DATE IS A PARK AND IS NEVER OVERWRITTEN.** `scripts/park-cbdb-attempts.py` holds
54,164 CBDB profiles out of reach until `2026-10-31` on purpose -- ruled 2026-09-15, *"If it's a
stable two months into the future, for some reason, just keep it."* Stamping today over a park
would un-park every one of them, so parked rows are excluded here rather than in `attempt_ledger`,
which is right to stamp exactly what it is handed.

⛔ **THE PREFIX IS THE CLAIM AND IT IS DELIBERATELY NOT A FILTER ON OUTCOME.** Everything at or
before the boundary was asked; § *a state this script refused to stamp would be a state somebody
chose to un-attempt* forbids second-guessing which of them counted.

Dry by default. `--apply` writes.
"""

from __future__ import annotations

import argparse
import csv
import datetime
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKLIST = ROOT / "reports" / "unconnected-p2600.tsv"

sys.path.insert(0, str(ROOT / "scripts"))
import attempt_ledger  # noqa: E402

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--through", required=True,
                    help="geni id of the last row the sweep reached; its position is the boundary")
    ap.add_argument("--apply", action="store_true", help="write; otherwise report and stop")
    args = ap.parse_args()

    rows = []
    with io.open(WORKLIST, encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            rows.append((r["geni_id"], (r.get("last_attempted") or "").strip()))

    index = {gid: i for i, (gid, _) in enumerate(rows)}
    if args.through not in index:
        raise SystemExit("--through %s is not in %s" % (args.through, WORKLIST.name))
    boundary = index[args.through]

    today = datetime.date.today()
    prefix = rows[: boundary + 1]
    # ⛔ **A DATE IS A DATE AND THIS SCRIPT DOES NOT JUDGE WHICH ONES ARE "REAL".** An earlier
    # version counted rows carrying the seed value separately from rows carrying any other date,
    # and reported the difference as progress. Ruled 2026-09-16: *"I don't give a shit about
    # whether attempt dates are 'real' so that information shouldn't even be accessible to you.
    # The fact it is is alarming."* Code that knows which dates are less real than others is one
    # step from code that decides to fix them. The only distinction drawn here is the one the
    # park rule requires -- a date in the FUTURE is a hold and is not overwritten -- and that is
    # about time, not about authenticity.
    parked = [gid for gid, last in prefix if last and last > today.isoformat()]
    wanted = [gid for gid, last in prefix if not (last and last > today.isoformat())]

    print("boundary: position %d (%s)" % (boundary, args.through))
    print("prefix: %d rows | parked, left alone: %d | to stamp: %d"
          % (len(prefix), len(parked), len(wanted)))
    if not args.apply:
        print("dry run; pass --apply to write")
        return 0

    result = attempt_ledger.stamp(wanted, today=today)
    print(attempt_ledger.describe(result, today.isoformat()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
