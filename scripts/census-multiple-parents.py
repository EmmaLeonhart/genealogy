"""People with more than one father or more than one mother, on BOTH sides.

    python scripts/census-multiple-parents.py

**Emma, 2026-08-25:** *"Put into the queue an analysis on both corpuses of people with multiple
mothers or multiple fathers."*

**This is not tidiness. It tests an assumption the zipper join is built on.**
`scripts/zipper-join.py` compares "our father" against "their `P22`" as though each side had at
most one, and its teeth-consuming step is written for a value rather than a set. Where either side
holds two, the join is choosing between them with no rule saying how — and 44,725 correspondences
now rest on that.

**It read `0` on our side the first time it ran, and that was an artefact.**
`scripts/derive-family.py` held parents in a plain `dict[str, str]`, so a second father
silently overwrote the first and `derived-family.csv` could not express the case at all --
it showed one parent, chosen by family-iteration order, with nothing saying another
existed. Every one of the 44 scripts reading that file, the zipper join included, has been
seeing a single parent that may be the wrong one. Fixed the same day by adding `fathers`
and `mothers` columns; `father`/`mother` keep their single-value meaning so no consumer
breaks. **A census that reports zero is a claim about a parser until proven otherwise.**

**Ours can hold two for a reason `CLAUDE.md` records, and it is structural rather than an error.**
The merge unions `FAMC`/`CHIL` and never drops one, so a parent link Geni has since *deleted*
survives forever once any export carries it. `exports/excluded/` exists precisely because nothing
else can remove one — the Samaritan case, where Geni rewrote a family in place and merging old with
new gave Abram two fathers, one of them the other's father.

**Theirs can hold two for different reasons** — a disputed parentage carried as two statements, an
adoptive alongside a biological parent (`P22` with a qualifier), or two items for one person not
yet merged.

Three questions, three outputs:

* `reports/multi-parents-ours.tsv` — every person in `reports/derived-family.csv` whose `father`
  or `mother` cell holds more than one id, with the parents' names and years.
* `reports/multi-parents-theirs.tsv` — every item in `out/wikidata/relations.tsv` with more than
  one `P22` or `P25`.
* `reports/multi-parents-crossed.tsv` — **the ones that matter to the join**: a person we hold a
  correspondence for where either side is multi-valued. If our side has two fathers and theirs has
  one, the zipper picked, and this names who.

Offline. Reads the derived CSVs and the extracted relations; asks Wikidata nothing.
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
    """`reports/derived-family.csv` uses ` | `. Splitting without stripping silently
    yields tokens that match no index -- the bug that made the zipper blind to every
    multi-child family until 2026-08-25."""
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def main():
    fam, ours_multi = {}, []
    with open(R / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fam[row["geni_id"]] = row
    print(f"{len(fam):,} people in our tree")

    names, years = {}, {}
    with open(R / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            names[row["geni_id"]] = row["label_en"] or row["label_mul"]
    with open(R / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["birth_date_year"]:
                years[row["geni_id"]] = row["birth_date_year"]

    if "fathers" not in next(iter(fam.values())):
        sys.exit("derived-family.csv has no `fathers` column - re-run "
                 "scripts/derive-family.py. "
                 "Before 2026-08-25 the generator held parents in a plain dict, so a second "
                 "father silently overwrote the first and this census could only ever report 0.")
    for g, row in fam.items():
        for slot in ("fathers", "mothers"):
            vs = split(row[slot])
            if len(vs) > 1:
                ours_multi.append({
                    "geni_id": g, "name": names.get(g, ""), "slot": slot[:-1],
                    "n": len(vs), "parents": ";".join(vs),
                    "parent_names": " | ".join(names.get(v, "?") for v in vs),
                    "parent_years": " | ".join(years.get(v, "") for v in vs),
                })

    theirs, theirs_multi = {}, []
    lab = {}
    with open(ROOT / "out" / "wikidata" / "labels.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            lab[row["qid"]] = (row["en"] or row["mul"] or row["no"] or row["nb"]
                               or row["sv"] or row["da"])
    with open(ROOT / "out" / "wikidata" / "relations.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            theirs[row["qid"]] = row
            for prop, slot in (("p22", "father"), ("p25", "mother")):
                vs = [x for x in (row[prop] or "").split(";") if x]
                if len(vs) > 1:
                    theirs_multi.append({
                        "qid": row["qid"], "label": "", "slot": slot,
                        "n": len(vs), "parents": ";".join(vs),
                    })
    for r in theirs_multi:
        r["label"] = lab.get(r["qid"], "")
        r["parent_labels"] = " | ".join(lab.get(v, "?") for v in r["parents"].split(";"))
    print(f"{len(theirs):,} Wikidata items with relationships")

    # --- the crossing: correspondences where either side is multi-valued -------------
    held = {}
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0].startswith("Q") and row[1].strip().isdigit():
                held.setdefault(row[1].strip(), row[0])
    stated = len(held)
    zipper = {}
    with open(R / "zipper-pairs.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            zipper[row["geni_id"]] = row
            held.setdefault(row["geni_id"], row["qid"])
    print(f"{stated:,} stated + {len(zipper):,} zipper = {len(held):,} correspondences")

    crossed = []
    for g, q in held.items():
        mine, their = fam.get(g), theirs.get(q)
        if not mine or not their:
            continue
        for slot, prop in (("fathers", "p22"), ("mothers", "p25")):
            a = split(mine[slot])
            b = [x for x in (their[prop] or "").split(";") if x]
            if len(a) <= 1 and len(b) <= 1:
                continue
            z = zipper.get(g, {})
            crossed.append({
                "geni_id": g, "name": names.get(g, ""), "qid": q,
                "label": lab.get(q, ""), "slot": slot[:-1],
                "ours_n": len(a), "theirs_n": len(b),
                "ours": ";".join(a), "theirs": ";".join(b),
                "ours_names": " | ".join(names.get(v, "?") for v in a),
                "theirs_labels": " | ".join(lab.get(v, "?") for v in b),
                "pair_from": "wikidata-p2600" if g not in zipper else
                             f"zipper r{z.get('round','?')} {z.get('slot','')}/{z.get('method','')}",
            })

    for path, rows in ((R / "multi-parents-ours.tsv", ours_multi),
                       (R / "multi-parents-theirs.tsv", theirs_multi),
                       (R / "multi-parents-crossed.tsv", crossed)):
        with open(path, "w", encoding="utf-8", newline="") as f:
            if not rows:
                f.write("(none)\n")
                continue
            w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {path.relative_to(ROOT)}: {len(rows):,} rows")

    def by_slot(rows):
        return dict(collections.Counter(r["slot"] for r in rows))

    print(f"\nOURS   {len(ours_multi):,} people with a multi-valued parent slot "
          f"({100 * len({r['geni_id'] for r in ours_multi}) / len(fam):.2f}% of the tree) "
          f"{by_slot(ours_multi)}")
    print(f"THEIRS {len(theirs_multi):,} items {by_slot(theirs_multi)}")
    print(f"CROSSED {len(crossed):,} slots where the join had to choose {by_slot(crossed)}")
    if crossed:
        shape = collections.Counter((r["ours_n"], r["theirs_n"]) for r in crossed)
        print("\nshape (ours x theirs):")
        for (a, b), n in shape.most_common(8):
            print(f"   {a} x {b}   {n:>6,}")
        src = collections.Counter(r["pair_from"].split()[0] for r in crossed)
        print("\nwhere the correspondence came from:")
        for k, n in src.most_common():
            print(f"   {n:>6,}  {k}")


if __name__ == "__main__":
    main()
