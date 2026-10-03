"""Every NAME item already in the local Wikidata store, with its labels.

    python scripts/extract-name-items.py

**`Tunheim` was in the download the whole time and simply went unused, because nothing in the
store pointed at it.** `Q36927172` *Tunheim* sits in
`wikidata/items/items-01552.jsonl.gz` carrying `P31 Q101352` *family name*, and the resolver
never looked at it.

`measure-name-resolution.py` builds its universe from `reports/name-items.csv` — name items
**some person in our store already points at** with `P735`/`P734`. That is 132,569 items. This
scan asks the store the other question, *which items ARE name items*, and finds **823,907**.

The gap is what created a second Tunheim, and it is not a rare shape: joined against
`reports/name-item-plan.csv`, **5,212 of the 14,351 tokens the plan would create already have an
item of the right kind on our own disk** — `Thomas`, `Hans`, `Sarah`, `Henry`, `陳`, `藤原`.

**Kind matters and is not collapsed.** `CLAUDE.md` § *One name item per USAGE*: a token that is
both a surname and a given name gets two items, so a `Q202444` given name sharing a label does
not make a family-name creation a duplicate. The `kind` column keeps them apart.

**A label is folded on case only.** `CLAUDE.md`: `María`, `Mária` and `Marià` are three items on
purpose, and folding diacritics away manufactured ambiguity for 1,312 names.

Writes `out/wikidata/name-items-in-store.tsv` — `qid`, `kind`, `p31`, and every label the item
carries, `|`-separated. One pass over the 2,248 shards, no network, ~5 minutes.
"""
from __future__ import annotations

import glob
import gzip
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")

OUT = ROOT / "out" / "wikidata" / "name-items-in-store.tsv"
#: Every name item's `en` label and `en` description (whatever its `P31`: `Eriksson` is classed
#: as a patronymic surname and is still a "family name" by its description), which decide whether a surname may
#: link to one (Emma, 2026-10-03, `namemodel.family_item_fits`).
FAMILY_EN = ROOT / "out" / "wikidata" / "family-name-items-en.tsv.gz"

#: `P31` value -> the usage a person links to it with. Confirmed in `CLAUDE.md` § *Names*.
KIND = {"Q101352": "family",       # family name, linked with P734
        "Q202444": "given",        # given name, linked with P735
        "Q12308941": "given",      # male given name
        "Q11879590": "given",      # female given name
        "Q3409032": "given",       # unisex given name
        "Q110874": "patronymic"}   # patronymic, linked with P5056

#: A cheap prefilter so 2.2M items are not JSON-parsed. Every line that could possibly hold one
#: of the type QIDs is parsed; everything else is skipped on a substring test.
PROBE = tuple(f'"{q}"' for q in KIND)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    scanned = found = 0
    start = time.time()
    with OUT.open("w", encoding="utf-8", newline="") as out, \
            gzip.open(FAMILY_EN, "wt", encoding="utf-8", newline="\n") as fam:
        out.write("qid\tkind\tp31\tlabels\n")
        fam.write("qid\ten_label\ten_description\n")
        for path in sorted(glob.glob(str(ROOT / "wikidata" / "items" / "items-*.jsonl.gz"))):
            with gzip.open(path, "rt", encoding="utf-8") as fh:
                for line in fh:
                    scanned += 1
                    named = any(p in line for p in PROBE)
                    if not named and '"family name"' not in line:
                        continue
                    item = json.loads(line)
                    en = (item.get("labels", {}).get("en") or {}).get("value", "")
                    desc = (item.get("descriptions", {}).get("en") or {}).get("value", "")
                    p31 = [s["mainsnak"].get("datavalue", {}).get("value", {}).get("id")
                           for s in item.get("claims", {}).get("P31", [])]
                    kinds = sorted({KIND[q] for q in p31 if q in KIND})
                    # Every name item, and any item described "family name" whatever its `P31`
                    # (`Eriksson` `Q1354604` is classed a patronymic surname).
                    if kinds or desc == "family name":
                        fam.write(f"{item['id']}\t{en}\t{desc}\n")
                    if not kinds:
                        continue
                    labels = sorted({v["value"] for v in item.get("labels", {}).values()})
                    out.write(f"{item['id']}\t{'|'.join(kinds)}\t"
                              f"{'|'.join(q for q in p31 if q)}\t{'|'.join(labels)}\n")
                    found += 1
    print(f"{scanned:,} items scanned, {found:,} name items found in "
          f"{time.time() - start:.0f}s")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
