"""What does OUR tree say about the two Geni profiles one Wikidata item claims?

    python scripts/classify-multi-p2600-by-tree.py

`Q122925764` was settled on 2026-08-26 without opening a single page. The item is
**Станіслаў Томаш Сапега** — *Stanisław Tomasz Sapieha*, one man whose name is both given
names — and it carries `P2600` for two Geni profiles. Our own corpus gives those two profiles
**the same father**, so Geni holds two brothers where Wikidata holds one person. `CLAUDE.md` §
*A second Geni ID on one Wikidata item is NOT a conflict* calls that ordinary and correct:
*"it is impossible to merge these geni profiles, simple as that."*

**The check generalises, and it is free.** For every item carrying more than one Geni id, ask
what relationship our tree already records between the profiles. The answer means something
different in each case, and none of them needs a browser:

| our tree says | reading |
| --- | --- |
| **same parents** | two siblings. Wikidata has merged them, or Geni has split one person into two — either way our snapshot matches Geni and there is nothing to do. |
| **one is the other's parent** | a generation has been collapsed on one side. Worth Emma's eye: this is the shape that produced the Samaritan `exports/excluded/` case. |
| **spouses** | a couple merged into one item. Almost certainly a Wikidata error, and the loudest kind. |
| **no relationship recorded** | the two are unconnected in our tree, which is the Zerubbabel shape — duplicate profiles that cannot be merged on Geni. Ordinary. |
| **one or both absent from our corpus** | we cannot say anything, and saying so is the answer. |

**Nothing here is resolved and nothing is emitted.** `CLAUDE.md` is explicit that duplicate
merges are Emma's and that the question is only ever whether our snapshot matches Geni — never
whether Geni is right. This sorts the population so the residue that genuinely needs a page
opened is small and named.

Writes `reports/multi-p2600-tree-shapes.tsv`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "reports"


def split(cell):
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def main():
    # Every item Wikidata itself gives more than one Geni id. Only what Wikidata STATES --
    # an inferred second id would make this a question about our own inference instead.
    multi = collections.defaultdict(set)
    with open(ROOT / "out" / "wikidata" / "relations.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            ids = [g for g in (row.get("p2600") or "").split(";") if g]
            if len(ids) > 1:
                multi[row["qid"]] = set(ids)
    print(f"{len(multi):,} Wikidata items state more than one Geni id")

    fam = {}
    with open(R / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fam[row["geni_id"]] = row
    names = {}
    with open(R / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            names[row["geni_id"]] = row["label_en"] or row["label_mul"]
    wlab = {}
    with open(ROOT / "out" / "wikidata" / "labels.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["qid"] in multi:
                wlab[row["qid"]] = (row["en"] or row["mul"] or row["sv"] or row["no"]
                                    or row["nb"] or row["da"])

    rows, tally = [], collections.Counter()
    for qid, ids in sorted(multi.items()):
        held = [g for g in sorted(ids) if g in fam]
        if len(held) < 2:
            shape = ("neither profile is in our corpus" if not held
                     else "only one of the profiles is in our corpus")
            tally[shape] += 1
            rows.append({"qid": qid, "label": wlab.get(qid, ""), "geni_ids": ";".join(sorted(ids)),
                         "in_corpus": len(held), "shape": shape, "detail": ""})
            continue

        # Pairwise, so an item with three ids still says something useful.
        shapes, detail = set(), []
        for i, a in enumerate(held):
            for b in held[i + 1:]:
                ra, rb = fam[a], fam[b]
                pa = set(split(ra["fathers"]) + split(ra["mothers"]))
                pb = set(split(rb["fathers"]) + split(rb["mothers"]))
                if b in split(ra["fathers"]) + split(ra["mothers"]) or \
                   a in split(rb["fathers"]) + split(rb["mothers"]):
                    shapes.add("one is the other's PARENT")
                    detail.append(f"{names.get(a,a)} / {names.get(b,b)}: parent-child")
                elif b in split(ra["spouses"]) or a in split(rb["spouses"]):
                    shapes.add("they are SPOUSES")
                    detail.append(f"{names.get(a,a)} / {names.get(b,b)}: spouses")
                elif pa and pb and pa & pb:
                    shapes.add("SIBLINGS - they share a parent")
                    detail.append(f"{names.get(a,a)} / {names.get(b,b)}: share "
                                  f"{', '.join(names.get(x, x) for x in sorted(pa & pb))}")
                else:
                    shapes.add("no relationship recorded between them")
                    detail.append(f"{names.get(a,a)} / {names.get(b,b)}: unrelated in our tree")
        # A stronger shape outranks a weaker one when an item has several pairs.
        for s in ("they are SPOUSES", "one is the other's PARENT",
                  "SIBLINGS - they share a parent", "no relationship recorded between them"):
            if s in shapes:
                shape = s
                break
        tally[shape] += 1
        rows.append({"qid": qid, "label": wlab.get(qid, ""), "geni_ids": ";".join(sorted(ids)),
                     "in_corpus": len(held), "shape": shape, "detail": " | ".join(detail[:3])})

    with open(R / "multi-p2600-tree-shapes.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["shape"], r["qid"])))

    total = sum(tally.values())
    print(f"\n{total:,} items classified from our own tree, no page opened:\n")
    for shape, n in tally.most_common():
        print(f"   {n:>6,}  {100 * n / total:>5.1f}%  {shape}")
    print("\nthe ones that are loud - a couple merged into one item:")
    for r in rows:
        if r["shape"] == "they are SPOUSES":
            print(f"   {r['label'][:44]:<44} {r['qid']}  {r['detail'][:70]}")
    print("\nwrote reports/multi-p2600-tree-shapes.tsv")
    print("NOTHING IS RESOLVED. Duplicate merges are Emma's, and the only question "
          "CLAUDE.md allows is whether our snapshot matches Geni.")


if __name__ == "__main__":
    main()
