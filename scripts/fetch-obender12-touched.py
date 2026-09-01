"""Every Wikidata item `OBender12` has touched, for the month-long hold.

    python scripts/fetch-obender12-touched.py

**Emma's control, 2026-08-30**, after the day in which one editor saw the same mistake from
this account repeatedly: *any item `OBender12` has touched is locked — our QuickStatements may
not edit it.* Her decision of 2026-08-30 is where the reasoning
sits, and the short form of it is that the live risk is not the errors but **an editor holding
a recent memory of the account**. Recognition decays, but more slowly than duplicates clear, so
the only variable worth controlling is how many more times that one person sees us.

**The full contributions list, not the overlap with our ledger.** Decision 1 of the analysis is
explicit about this: the 37-item intersection is what we would collide with *today*, and the
whole point of the hold is that tomorrow's batch is not today's. Holding only the overlap
re-derives the collision set on every run and reintroduces exactly the coupling the hold exists
to break.

**A RECENT window, not the whole account.** They have 785,050 edits since 2020, and holding
every item behind all of them would be an exclusion of hundreds of thousands of items -- which
is not what a *month-long* hold means, and would quietly gut the pipeline. The risk model says
what the window should be: the exposure is one person's **batch and recent memory**, and an
item they touched in 2021 is neither. So the default is the last 30 days, symmetric with how
long the hold runs.

**One request per 500 revisions, `ucnamespace=0` so only items come back.** `CLAUDE.md`
§ *Querying Wikidata is ALLOWED* governs: batch where the API offers batching, do not fan out.

Writes `reports/obender12-touched.tsv` — `qid`, `first_touched`, `last_touched`, `edits`.
`build-garborg-day.py` reads it through `held_items()` and refuses to emit any statement whose
subject is in it, until `OBENDER_HOLD_EXPIRES`.
"""
from __future__ import annotations

import argparse
import collections
import datetime
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from genimerge.wikidata import require_agent  # noqa: E402

API = "https://www.wikidata.org/w/api.php"
EDITOR = "OBender12"
OUT = ROOT / "reports" / "obender12-touched.tsv"

#: How far back one batch is plausibly live, and the length of the hold itself.
WINDOW_DAYS = 30


def fetch_contributions(agent, since):
    """Namespace-0 revisions by the editor back to `since`, newest first, 500 at a time.

    `ucend` is the OLDEST timestamp in a newest-first listing, so it is the floor of the window.
    """
    params = {
        "action": "query",
        "list": "usercontribs",
        "ucuser": EDITOR,
        "ucnamespace": "0",
        "uclimit": "500",
        "ucprop": "title|timestamp",
        "ucend": since,
        "format": "json",
        "formatversion": "2",
    }
    seen = 0
    while True:
        url = f"{API}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"User-Agent": agent})
        with urllib.request.urlopen(req, timeout=60) as fh:
            data = json.load(fh)
        batch = data.get("query", {}).get("usercontribs", [])
        for row in batch:
            yield row["title"], row["timestamp"]
        seen += len(batch)
        print(f"  {seen:,} revisions", flush=True)
        cont = data.get("continue")
        if not cont:
            return
        params.update(cont)
        time.sleep(1)  # polite, not throttled to


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=WINDOW_DAYS,
                    help="how far back to look (default: %(default)s)")
    args = ap.parse_args()

    agent = require_agent()
    since = (datetime.datetime.now(datetime.timezone.utc)
             - datetime.timedelta(days=args.days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"fetching {EDITOR}'s item edits back to {since} ...", flush=True)

    edits = collections.Counter()
    first, last = {}, {}
    for title, stamp in fetch_contributions(agent, since):
        if not title.startswith("Q"):
            continue
        edits[title] += 1
        # Revisions arrive newest first, so the first one seen is the latest.
        last.setdefault(title, stamp)
        first[title] = stamp

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        fh.write("qid\tfirst_touched\tlast_touched\tedits\n")
        for qid in sorted(edits, key=lambda q: int(q[1:])):
            fh.write(f"{qid}\t{first[qid]}\t{last[qid]}\t{edits[qid]}\n")

    print(f"\n{len(edits):,} distinct items, {sum(edits.values()):,} revisions")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
