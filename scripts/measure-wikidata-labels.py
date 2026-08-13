"""What languages do the stored Wikidata items actually have labels in?

Emma, 2026-08-12: *"I'm asking for Japanese language labels… I'm talking about
wiki data only."* And, on being given a figure over the 14,157 people who overlap
our tree: *"there are probably hundreds of thousands of people."*

Both corrections are right, and both were mine. This counts **labels on Wikidata
items**, over the **whole store** — 1,408,401 items — with no Geni input of any
kind. A GEDCOM name has no language (the corpus contains zero `LANG` subtags), so
nothing about Geni can answer a question about `ja` labels.

Reported three ways, because the denominators differ and quoting one alone
misleads: all stored items, the subset carrying a Geni ID, and the subset our own
tree actually holds.

Offline. Reads `wikidata/items/` only.

    py scripts/measure-wikidata-labels.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import wikistore  # noqa: E402

STORE = REPO_ROOT / "wikidata" / "items"
OURS = REPO_ROOT / "reports" / "derived-labels.csv"
OUT_MD = REPO_ROOT / "reports" / "wikidata-label-languages.md"
OUT_CSV = REPO_ROOT / "reports" / "wikidata-label-languages.csv"

csv.field_size_limit(10_000_000)


def main() -> int:
    ours: set[str] = set()
    if OURS.exists():
        with open(OURS, encoding="utf-8", newline="") as handle:
            ours = {r["qid"] for r in csv.DictReader(handle) if r["qid"]}
    print(f"{len(ours):,} items are people in our tree", flush=True)

    all_items = Counter()          # language -> items having a label in it
    geni_items = Counter()
    our_items = Counter()
    totals = Counter()
    label_counts = Counter()       # how many languages an item has

    shards = wikistore.shards(STORE)
    for n, shard in enumerate(shards, 1):
        for entity in wikistore.read_shard(shard):
            qid = entity.get("id") or ""
            labels = entity.get("labels") or {}
            claims = entity.get("claims") or {}
            has_geni = "P2600" in claims

            totals["items"] += 1
            if has_geni:
                totals["with a Geni ID"] += 1
            if qid in ours:
                totals["in our tree"] += 1
            label_counts[min(len(labels), 50)] += 1

            for code in labels:
                all_items[code] += 1
                if has_geni:
                    geni_items[code] += 1
                if qid in ours:
                    our_items[code] += 1
        if n % 200 == 0 or n == len(shards):
            print(f"  shard {n:,}/{len(shards):,}  {totals['items']:,} items", flush=True)

    languages = sorted(all_items, key=lambda c: -all_items[c])

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["language", "all_items", "items_with_geni_id", "items_in_our_tree"])
        for code in languages:
            writer.writerow([code, all_items[code], geni_items[code], our_items[code]])

    ti, tg, to = totals["items"], totals["with a Geni ID"], totals["in our tree"]
    L: list[str] = []
    add = L.append
    add("# Label languages on the stored Wikidata items")
    add("")
    add("Counted over **every stored item**, with no Geni input. A GEDCOM name carries")
    add("no language — the corpus has zero `LANG` subtags — so nothing about Geni can")
    add("answer a question about `ja` labels.")
    add("")
    add(f"| population | items |")
    add("| --- | ---: |")
    add(f"| all stored items | {ti:,} |")
    add(f"| …carrying a Geni ID (`P2600`) | {tg:,} |")
    add(f"| …people in our own tree | {to:,} |")
    add("")
    add("## The top languages")
    add("")
    add("| language | all items | share | with a Geni ID | share | in our tree | share |")
    add("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for code in languages[:30]:
        add(f"| `{code}` | {all_items[code]:,} | {100.0*all_items[code]/max(ti,1):.1f}% "
            f"| {geni_items[code]:,} | {100.0*geni_items[code]/max(tg,1):.1f}% "
            f"| {our_items[code]:,} | {100.0*our_items[code]/max(to,1):.1f}% |")
    add("")
    add("## English against Japanese")
    add("")
    add("| | all items | with a Geni ID | in our tree |")
    add("| --- | ---: | ---: | ---: |")
    for code in ("en", "ja", "zh", "ko", "mul"):
        add(f"| `{code}` | {all_items[code]:,} ({100.0*all_items[code]/max(ti,1):.1f}%) "
            f"| {geni_items[code]:,} ({100.0*geni_items[code]/max(tg,1):.1f}%) "
            f"| {our_items[code]:,} ({100.0*our_items[code]/max(to,1):.1f}%) |")
    add("")
    add(f"**Items with no label at all: {label_counts[0]:,}.**")
    add("")
    add(f"`reports/wikidata-label-languages.csv` has all {len(languages):,} languages.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print()
    print(f"  {'lang':<6} {'all items':>12} {'with Geni ID':>14} {'in our tree':>13}")
    for code in ("en", "ja", "zh", "ko", "mul"):
        print(f"  {code:<6} {all_items[code]:>12,} {geni_items[code]:>14,} {our_items[code]:>13,}")
    print(f"\n  totals: {ti:,} items, {tg:,} with a Geni ID, {to:,} in our tree")
    print(f"  {label_counts[0]:,} items have no label in any language")
    print(f"\nwrote {OUT_MD} and {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
