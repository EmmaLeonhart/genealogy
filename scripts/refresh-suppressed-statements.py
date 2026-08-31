"""Statements another editor REMOVED, so the batch never puts them back.

    python scripts/refresh-suppressed-statements.py

**The failure this closes, 2026-08-30.** `OBender12` merged our duplicate name items and stripped
the `P734` links pointing at the losers. The next build re-emitted them — because the generator
emits a name statement when the item does not have one, and his deletion is exactly what "does
not have one" looks like.

**It is not statefulness. It is the absence of it.** Nothing recorded that a human had made a
decision about that statement, so every rebuild saw a fresh gap and filled it, more confidently
each time. Any *emit what is missing* pipeline will fight any editor who deletes, indefinitely.
Emma had to undo her own undos and then make cosmetic edits to cover the trail.

## How a removal is detected

Not from our own batches: a statement we emitted and she never ran is also absent, and
suppressing that would silently drop real work. The evidence has to be a **removal by somebody
else**, which is what `wbremoveclaims` in an edit comment records.

So this reads the contributions of editors *other than* the account, keeps the `wbremoveclaims`
edits on items in the ledger, and parses the property and value out of the comment — the form is
`/* wbremoveclaims-remove:1| */ [[Property:P734]]: [[Q141223707]]`.

**A removal by Emma herself is NOT suppressed.** She is the one running the batches; if she
removes something and the batch re-adds it, that is a conversation she is having with her own
pipeline, not an edit war with a stranger.

Writes `reports/suppressed-statements.tsv`: `qid`, `property`, `value`, `removed_by`, `when`.

## RUN THIS ONCE, over the LAST 30 DAYS of the named editor's contributions

**Emma, 2026-08-31:** *"you're supposed to run that on the last 30 days of his activity and then
have it as a static file. That's what I asked for."* And, on the first version: *"It is extremely
stupid that you wrote it as something that actively watches the editor's edits... I want to watch
their edits once and then leave it."*

**What was wrong, and it is why this never ran.** The first version spent its whole budget
*discovering* which editors to look at — 200 sequential revision fetches over ledger items — before
touching a single contribution list. That made it hundreds of requests and tens of minutes, and I
then quoted that cost back at her as a reason to skip it. The editor was never unknown: it is
`OBender12`, named in the failure this exists to close. Naming him directly turns the job into a
handful of `usercontribs` pages bounded by `ucend`.

**The bound is 30 days and it is a snapshot, not a window that slides.** Re-running would produce a
different file; that is the point of it being static. `build-garborg-day.read_suppressed` only ever
reads it, and the generator never calls this.

**Do not schedule it, do not put it in a cron, do not run it as part of the daily batch.**
"""
from __future__ import annotations

import csv
import json
import re
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from genimerge.wikidata import _http_fetch, require_agent  # noqa: E402

OUT = ROOT / "reports" / "suppressed-statements.tsv"
LEDGER = ROOT / "reports" / "garborg-qids.tsv"
OURS = "日巫女"

#: `/* wbremoveclaims-remove:1| */ [[Property:P734]]: [[Q141223707]]`
REMOVAL = re.compile(r"wbremoveclaims.*?\[\[Property:(P\d+)\]\]:\s*\[\[(Q\d+)\]\]")


def ledger_qids():
    with LEDGER.open(encoding="utf-8") as fh:
        return {r["qid"] for r in csv.DictReader(fh, delimiter="\t") if r.get("qid")}


#: **Named, not discovered.** Her instruction is *"the last 30 days of his activity"*, and `his`
#: is `OBender12` — the editor who merged our duplicate name items and stripped the `P734` links.
#: A second name goes here if one ever earns it; a crawl to find them does not.
EDITORS = ("OBender12",)

#: Her bound, in days.
WINDOW_DAYS = 30


def removals_by(user, keep, ua, since):
    """`wbremoveclaims` edits by `user` on ledger items, no older than `since`.

    `ucend` is the *oldest* timestamp the API will return, so the walk stops itself rather than
    paging through years of history to filter locally.
    """
    out, cont, pages = [], None, 0
    while pages < 20:
        url = ("https://www.wikidata.org/w/api.php?action=query&format=json&list=usercontribs"
               "&ucuser=" + urllib.parse.quote(user) +
               "&uclimit=500&ucnamespace=0&ucprop=title|timestamp|comment"
               "&ucend=" + urllib.parse.quote(since))
        if cont:
            url += "&uccontinue=" + urllib.parse.quote(cont)
        data = json.loads(_http_fetch(url, headers=ua))
        contribs = data.get("query", {}).get("usercontribs", [])
        pages += 1
        for c in contribs:
            if c["title"] not in keep:
                continue
            m = REMOVAL.search(c.get("comment", ""))
            if m:
                out.append({"qid": c["title"], "property": m.group(1), "value": m.group(2),
                            "removed_by": user, "when": c["timestamp"][:10]})
        cont = data.get("continue", {}).get("uccontinue")
        if not cont:
            break
        time.sleep(0.3)
    print(f"   {user}: {pages} contribution page(s) read")
    return out


def main():
    ua = {"User-Agent": require_agent()}
    keep = ledger_qids()
    since = (datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"{len(keep)} ledger items; {', '.join(EDITORS)} since {since[:10]} "
          f"({WINDOW_DAYS} days)")

    rows = []
    for user in EDITORS:
        found = removals_by(user, keep, ua, since)
        if found:
            print(f"   {user}: {len(found)} statement removals on ledger items")
        rows += found

    seen, unique = set(), []
    for r in rows:
        key = (r["qid"], r["property"], r["value"])
        if key not in seen:
            seen.add(key)
            unique.append(r)

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["qid", "property", "value", "removed_by", "when"],
                           delimiter="\t")
        w.writeheader()
        w.writerows(sorted(unique, key=lambda r: (r["qid"], r["property"])))
    print(f"\n{len(unique)} statements suppressed -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
