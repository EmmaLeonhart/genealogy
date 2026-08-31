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

## RUN THIS ONCE. It is not a watcher, and it should not have been written as one

**Emma, 2026-08-31:** *"It is extremely stupid that you wrote it as something that actively
watches the editor's edits… I don't want this to be an ongoing thing! I want to watch their
edits once and then leave it."*

She is right. As written it re-crawls `editors_touching` over 200 ledger items and then every
editor's full contribution history on **every invocation**, re-deriving from scratch a fact that
only needed capturing once. That is hundreds of sequential requests, it takes tens of minutes,
and it is a standing surveillance of other people's edit histories that nobody asked for.

**What is already right, and why this is not being rebuilt now** (her call, same message: *"I
don't want you to over-engineer the thing by deciding to fucking stop the generation right now
and make it again"*): the output is a **static file**, and `build-garborg-day.read_suppressed`
only ever *reads* it. The generator never calls this script. So the pipeline is already
snapshot-shaped — the fix, when it happens, is to this script alone.

**Do not schedule it, do not put it in a cron, do not run it as part of the daily batch.**
"""
from __future__ import annotations

import csv
import json
import re
import sys
import time
import urllib.parse
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


def editors_touching(qids, ua, limit=200):
    """Editors other than ours who have recently changed a ledger item."""
    seen = set()
    for qid in list(qids)[:limit]:
        url = ("https://www.wikidata.org/w/api.php?action=query&format=json&prop=revisions"
               "&rvprop=user|comment|timestamp&rvlimit=20&titles=" + qid)
        try:
            data = json.loads(_http_fetch(url, headers=ua))
        except Exception:                                           # noqa: BLE001
            continue
        for page in data.get("query", {}).get("pages", {}).values():
            for rev in page.get("revisions", []):
                if rev.get("user") and rev["user"] != OURS:
                    seen.add(rev["user"])
        time.sleep(0.2)
    return seen


def removals_by(user, keep, ua):
    out, cont = [], None
    for _ in range(10):
        url = ("https://www.wikidata.org/w/api.php?action=query&format=json&list=usercontribs"
               "&ucuser=" + urllib.parse.quote(user) +
               "&uclimit=500&ucnamespace=0&ucprop=title|timestamp|comment")
        if cont:
            url += "&uccontinue=" + urllib.parse.quote(cont)
        data = json.loads(_http_fetch(url, headers=ua))
        for c in data.get("query", {}).get("usercontribs", []):
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
    return out


def main():
    ua = {"User-Agent": require_agent()}
    keep = ledger_qids()
    print(f"{len(keep)} ledger items")

    editors = editors_touching(keep, ua)
    print(f"{len(editors)} other editors have touched them: {', '.join(sorted(editors)) or 'none'}")

    rows = []
    for user in sorted(editors):
        found = removals_by(user, keep, ua)
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
