"""Where the browser QuickStatements loop stands, read from the account's own contributions.

    python scripts/qs-loop-status.py [--batch-file reports/wikidata-garborg-day-manual.txt]

The loop (Emma, 2026-09-27): run the day batch in a browser QuickStatements tab; as soon as the
random individuals and the whole ring have been CREATED, start a lean rebuild
(`gh workflow run pipeline.yml -f batch_only=true -f force=true`), so the next ring begins to form
while the old tab finishes its tail; when the new batch lands, run it in a NEW tab. The browser is
driven by the Claude session (the Chrome tools), on a session cron; this only reports the state
it decides from. Read-only, one API request per call.

⛔ **A tab that is running a batch is never navigated or closed.** Closing the tab stops a
QuickStatements run done in the browser (it runs in the page), which is how a run was killed on
2026-09-27. New batches go in new tabs; old ones finish on their own.

Prints JSON: for each `#temporary_batch_…` in the last 500 edits, its creations and edits, first
and last edit time, and whether it is still moving; and, from the batch file's headers, how many
creations the random individuals plus the ring come to (the point to start the next rebuild).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACCOUNT = "日巫女"
UA = {"User-Agent": "genealogy-pipeline/1.0 (https://github.com/EmmaLeonhart/genealogy)"}
BATCH_TAG = re.compile(r"#temporary_batch_(\d+)")
HEADER = re.compile(r"^# ▶ (RANDOM INDIVIDUALS|THE RING): (?:all )?(\d+)")


def ring_target(text):
    """Creations up to the end of the ring section: the random individuals plus the ring."""
    return sum(int(m.group(2)) for m in map(HEADER.match, text.splitlines()) if m)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch-file", default=str(ROOT / "reports" / "wikidata-garborg-day-manual.txt"))
    ap.add_argument("--pages", type=int, default=4)
    args = ap.parse_args()
    p = {"action": "query", "list": "usercontribs", "ucuser": ACCOUNT, "uclimit": "500",
         "ucprop": "title|timestamp|comment", "format": "json"}
    # Up to `--pages` pages of 500 (default 4, one request each): a batch past 500 edits would
    # otherwise have its early creations fall out of view and the ring point come late.
    rows, cont = [], {}
    for _ in range(args.pages):
        url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({**p, **cont})
        data = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        rows += data["query"]["usercontribs"]
        if "continue" not in data:
            break
        cont = {"uccontinue": data["continue"]["uccontinue"], "continue": data["continue"]["continue"]}
    batches = {}
    for c in rows:
        m = BATCH_TAG.search(c.get("comment") or "")
        if not m:
            continue
        b = batches.setdefault(m.group(1), {"edits": 0, "creations": 0, "first": c["timestamp"],
                                            "last": c["timestamp"]})
        b["edits"] += 1
        b["creations"] += "wbeditentity-create" in (c.get("comment") or "")
        b["first"] = min(b["first"], c["timestamp"])
        b["last"] = max(b["last"], c["timestamp"])
    now = dt.datetime.now(dt.timezone.utc)
    for b in batches.values():
        last = dt.datetime.strptime(b["last"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        b["idle_minutes"] = round((now - last).total_seconds() / 60, 1)
    path = Path(args.batch_file)
    target = ring_target(path.read_text(encoding="utf-8")) if path.exists() else None
    print(json.dumps({"now": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "ring_target_creations": target,
                      "batches_in_recent_edits": batches}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
