"""Would any CREATE in the batch be refused for sharing a label with an existing item?

    python scripts/check-label-collisions.py [--batch reports/wikidata-garborg-day.txt]

**Emma's rule, `queue.md` § *Wikidata person descriptions*:**

> *"blank descriptions are not deduplicated, but descriptions are deduplicated… If there is an
> unlabelled individual with the description 'Son of Jack' and you try to add the label 'John'
> then it just straight up refuses it. This is by far the worst trap to accidentally fall into…
> But also, this will cause it so that if we're trying to create an individual, it throws an
> error."*

Wikidata enforces uniqueness on the **label + description pair** per language. Two items both
labelled `Ole Olsen` with no description are the same pair, so the second is refused — and a
refusal lands mid-batch, where `CLAUDE.md` says the damage is discoverable only by reading
QuickStatements' output line by line.

**This is a pre-flight check, not a fix.** It reports; it changes no batch and adds no
description, in any language, ever. `CLAUDE.md` § *An item is NEVER created with a description*
-- Emma, 2026-08-30: *"It's a hard rule that we never create items with descriptions."* A
collision is resolved by **holding the creation**, which is why this writes the Geni ids.

## What it asks, and why it has to be live

The offline store carries labels but not descriptions, so it cannot answer "does the colliding
item have one". `wbsearchentities` returns label and description together, which settles both
halves in one request per label. `CLAUDE.md` § *Querying Wikidata is ALLOWED* covers it; the
volume is one request per creation in a batch of ~20.

A collision is reported when an existing item has the **same label** and **no description**,
because that is the pair our creation would duplicate. An existing item with a description does
not collide with our undescribed one.
"""
from __future__ import annotations

import argparse
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

DELAY = 0.4


def creations(path):
    """`[(label, language, geni_id)]` for every CREATE block, `en` preferred.

    The Geni id comes from the block's own `P2600`, so a collision is reported against the
    PERSON and not only the label -- which is what lets the generator hold that creation.
    """
    out = []
    text = path.read_text(encoding="utf-8")
    for block in text.split("CREATE")[1:]:
        body = block.split("\nCREATE")[0]
        labels = dict(re.findall(r'^LAST\tL([a-z-]+)\t"([^"]+)"', body, re.M))
        label = labels.get("en") or labels.get("mul")
        geni = re.search(r'^LAST\tP2600\t"(\d+)"', body, re.M)
        if label:
            out.append((label, "en" if "en" in labels else "mul",
                        geni.group(1) if geni else ""))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--batch", default="reports/wikidata-garborg-day.txt")
    args = ap.parse_args()

    path = ROOT / args.batch
    wanted = creations(path)
    print(f"{len(wanted)} CREATE blocks in {args.batch}\n")

    ua = {"User-Agent": require_agent()}
    collisions, clear = [], 0
    for label, lang, geni in wanted:
        url = ("https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json"
               "&type=item&limit=20&language=en&uselang=en&search="
               + urllib.parse.quote(label))
        data = json.loads(_http_fetch(url, headers=ua))
        same = [r for r in data.get("search", [])
                if (r.get("label") or "").casefold() == label.casefold()]
        # Only an existing item with NO description shares our pair.
        undescribed = [r for r in same if not (r.get("description") or "").strip()]
        if undescribed:
            collisions.append((label, lang, geni, [r["id"] for r in undescribed],
                               [(r["id"], r.get("description", "")) for r in same
                                if (r.get("description") or "").strip()]))
        else:
            clear += 1
        time.sleep(DELAY)

    # **The generator reads this, so the hold is data rather than a hand-maintained list.**
    # `CLAUDE.md` § *An item is NEVER created with a description*: a collision is resolved by
    # holding the creation, and holding it needs the Geni id, not the label.
    # **CUMULATIVE, and it has to be.** `--compose` draws a fresh set of people each run, so
    # rewriting this file would release everybody held by the previous draw the moment a new
    # one appeared -- the batch would oscillate and never reach zero collisions. Measured:
    # 5 collisions, regenerate, 4 collisions, none of them the original five.
    out = ROOT / "reports" / "label-collisions.tsv"
    rows = {}
    if out.exists():
        for row in csv.DictReader(out.open(encoding="utf-8"), delimiter="\t"):
            rows[row["geni_id"]] = (row["label"], row["lang"], row["collides_with"])
    for label, lang, geni, ids, _described in collisions:
        rows[geni] = (label, lang, ";".join(ids))
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("geni_id\tlabel\tlang\tcollides_with\n")
        for geni, (label, lang, ids) in sorted(rows.items()):
            fh.write(f"{geni}\t{label}\t{lang}\t{ids}\n")
    print(f"wrote {out.relative_to(ROOT)} -- {len(rows)} held in total\n")

    print(f"{clear} creations have no colliding item")
    print(f"{len(collisions)} would duplicate an existing label+empty-description pair\n")
    for label, lang, geni, ids, described in collisions:
        print(f"   {label}  ({lang})  geni:{geni}")
        print(f"      collides with: {', '.join(ids)}")
        for qid, desc in described[:2]:
            print(f"      (also {qid}, which has a description: {desc[:60]})")
    if collisions:
        print("\nA collision does NOT mean the person is a duplicate -- it means the CREATE "
              "would be refused. It is resolved by HOLDING the creation, never by adding a "
              "description: Emma, 2026-08-30, \"It's a hard rule that we never create items "
              "with descriptions.\"")


if __name__ == "__main__":
    main()
