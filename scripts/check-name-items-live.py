"""Which name tokens the plan would CREATE already have an item on Wikidata?

    python scripts/check-name-items-live.py [--usage family] [--limit N]

**Emma, 2026-08-29:** *"certain names, for example Tunheim, I've noticed that some of these
names got merged in with an existing item. I'm extremely confused how this happened, and it
seems to me to indicate maybe you're not actually checking the existence of the names correctly
in our data."*

She is right, and the cause is written in the resolver's own docstring.
`measure-name-resolution.py`: *"A name item counts only if some person in our own store already
points at it with `P735` or `P734` … A Geni name Wikidata has an item for, which nobody in our
store carries, is invisible here."* `Q36927172` *Tunheim* (family name) exists on Wikidata and
is even in our local store — but no stored person links to it, so it is absent from
`reports/name-items.csv`, so `reports/name-resolution.csv` reads `family,Tunheim,64,no item`,
so `reports/name-item-plan.csv` reads `create`. A second Tunheim.

**The existence check is scoped to names our own people already use, and it is being read as
"does Wikidata have this name".** Those are different questions and only the second one decides
whether creating an item makes a duplicate.

## Why this asks Wikidata rather than the store

The store has no `instance of` index — `out/wikidata/relations.tsv` carries `P22`/`P25`/`P40`/
`P26`/`P2600` and nothing else, and `reports/wikidata-labels.tsv` is id-to-label with no type.
So "is there a `Q101352` *family name* item labelled X" cannot be answered offline today.
`CLAUDE.md` § *Querying Wikidata is ALLOWED* permits the question; the rate rule shapes how.

One `wbsearchentities` per token — the API has no batch form for a label search — at
`DELAY` seconds apart, then the candidates' `P31` in `wbgetentities` batches of 50, which does
batch. Every response is written as it arrives so a killed run keeps its work and
`--resume` continues.

Writes `reports/name-item-existing.csv`: one row per token, the QIDs sharing its label, and
whether any of them is the right kind of name item.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from genimerge.wikidata import _http_fetch, require_agent  # noqa: E402

PLAN = ROOT / "reports" / "name-item-plan.csv"
OUT = ROOT / "reports" / "name-item-existing.csv"

#: The `P31` value that makes a candidate the same KIND of name item, per usage.
#: `CLAUDE.md` § *One name item per USAGE*: a token that is a surname and a given name gets
#: two items, so a `Q202444` given name sharing the label does NOT make a family-name
#: creation a duplicate.
KIND = {"family": {"Q101352"},
        "given": {"Q202444", "Q12308941", "Q11879590", "Q3409032"},
        "patronymic": {"Q110874"}}

DELAY = 0.4
FIELDS = ("token", "usage", "bearers", "script", "same_label_qids", "same_kind_qids", "verdict")


def search(token, ua):
    url = ("https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json"
           "&type=item&language=en&limit=20&search=" + urllib.parse.quote(token))
    d = json.loads(_http_fetch(url, headers=ua))
    return [x["id"] for x in d.get("search", [])
            if (x.get("label") or "").casefold() == token.casefold()]


def types_of(qids, ua):
    out = {}
    for i in range(0, len(qids), 50):
        url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json"
               "&props=claims&ids=" + "|".join(qids[i:i + 50]))
        d = json.loads(_http_fetch(url, headers=ua))
        for q, e in d.get("entities", {}).items():
            out[q] = {s["mainsnak"].get("datavalue", {}).get("value", {}).get("id")
                      for s in e.get("claims", {}).get("P31", [])}
        time.sleep(DELAY)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--usage", default="family", choices=sorted(KIND))
    ap.add_argument("--script", default="Latin")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", action="store_true",
                    help="skip tokens already in reports/name-item-existing.csv.")
    args = ap.parse_args()

    ua = {"User-Agent": require_agent()}
    rows = [r for r in csv.DictReader(PLAN.open(encoding="utf-8", newline=""))
            if r["action"] == "create" and r["usage"] == args.usage
            and r["script"] == args.script]
    done = set()
    if args.resume and OUT.exists():
        done = {r["token"] for r in csv.DictReader(OUT.open(encoding="utf-8", newline=""))}
    todo = [r for r in rows if r["token"] not in done]
    if args.limit:
        todo = todo[:args.limit]
    print(f"{len(rows):,} {args.script} {args.usage} tokens the plan would CREATE; "
          f"{len(done):,} already checked, {len(todo):,} to go")

    new = not OUT.exists() or not done
    with OUT.open("a" if done else "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        dupes = 0
        for n, r in enumerate(todo, 1):
            cands = search(r["token"], ua)
            time.sleep(DELAY)
            same_kind = []
            if cands:
                t = types_of(cands, ua)
                same_kind = [q for q in cands if t.get(q, set()) & KIND[args.usage]]
            dupes += bool(same_kind)
            w.writerow({"token": r["token"], "usage": r["usage"], "bearers": r["bearers"],
                        "script": r["script"], "same_label_qids": "|".join(cands),
                        "same_kind_qids": "|".join(same_kind),
                        "verdict": "ALREADY EXISTS" if same_kind else "create"})
            fh.flush()
            if n % 25 == 0:
                print(f"  {n:,}/{len(todo):,}  {dupes:,} already exist", flush=True)
    print(f"wrote {OUT.relative_to(ROOT)} -- {dupes:,} of {len(todo):,} already exist")


if __name__ == "__main__":
    main()
