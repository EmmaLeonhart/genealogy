"""Resolve every QID in the Garborg ledger through Wikidata redirects.

    python scripts/resolve-merged-qids.py [--write]

**Emma, 2026-08-29:** *"a lot of the items were merged and this is a problem. since it
means a lot of relationship statements consistently use the wrong thing"*.

She is right that this is the failure mode. When two items are merged, the loser becomes
a **redirect** to the winner. Our ledger keeps whichever QID it recorded first, so every
`P22`/`P25`/`P26`/`P40`/`P3373` the daily batch emits against that row points at a
redirect rather than at the surviving item. QuickStatements will often follow it, but the
statement is then attributed to an item that is not the one we meant, and a later batch
comparing "does the item already hold this" against the *target* sees nothing and emits
it again.

`CLAUDE.md` already asked for this check, in her words: *"I do want to check all the IDs
to ensure that they haven't been merged or anything"*.

**One batched request per 50 ids, `action=wbgetentities&props=info`.** A redirected entity
comes back with a `redirects` block naming `from` and `to`. This is the same sanctioned
path the ledger refresh uses -- it is not an ad-hoc lookup about a person.
"""

from __future__ import annotations

import csv
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from bot_identity import agent as _bot_agent  # noqa: E402

API = "https://www.wikidata.org/w/api.php"
LEDGER = ROOT / "reports" / "garborg-qids.tsv"
CHUNK = 50


def fetch(ids, ua):
    params = {"action": "wbgetentities", "ids": "|".join(ids),
              "props": "info", "format": "json", "formatversion": "2"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                 headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main() -> int:
    ua = _bot_agent()
    if not ua:
        sys.exit("no contact address: set BOT_CONTACT or create .bot-contact")

    rows = list(csv.DictReader(LEDGER.open(encoding="utf-8"), delimiter="\t"))
    qids = sorted({r["qid"] for r in rows if r.get("qid", "").startswith("Q")})
    print(f"{len(rows)} ledger rows, {len(qids)} distinct QIDs")

    redirect, missing = {}, []
    for i in range(0, len(qids), CHUNK):
        chunk = qids[i:i + CHUNK]
        data = fetch(chunk, ua)
        for qid, ent in (data.get("entities") or {}).items():
            if ent.get("missing") is not None or "missing" in ent:
                missing.append(qid)
        # formatversion=2 reports redirects as a list of {from, to}
        for r in data.get("redirects") or []:
            redirect[r["from"]] = r["to"]
        # ...and older shapes hide the target in the entity itself
        for qid, ent in (data.get("entities") or {}).items():
            tgt = (ent.get("redirects") or {}).get("to")
            if tgt and tgt != qid:
                redirect[qid] = tgt
        time.sleep(0.3)

    print(f"\n{len(redirect)} of {len(qids)} QIDs are REDIRECTS (merged away)")
    print(f"{len(missing)} are missing/deleted\n")
    for src, dst in sorted(redirect.items()):
        who = [r for r in rows if r["qid"] == src]
        label = who[0].get("label", "") if who else ""
        print(f"   {src:12} -> {dst:12}  {label[:44]}")
    for q in missing:
        who = [r for r in rows if r["qid"] == q]
        print(f"   {q:12} -> MISSING      {(who[0].get('label','') if who else '')[:44]}")

    if "--write" in sys.argv and redirect:
        n = 0
        for r in rows:
            if r.get("qid") in redirect:
                r["note"] = ((r.get("note") or "") +
                             f" [merged {r['qid']} -> {redirect[r['qid']]} 2026-08-29]").strip()
                r["qid"] = redirect[r["qid"]]
                n += 1
        with LEDGER.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
            w.writeheader()
            w.writerows(rows)
        print(f"\nrewrote {LEDGER.relative_to(ROOT)}: {n} rows repointed at the merge target")
    elif redirect:
        print("\n(dry run -- pass --write to repoint the ledger)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
