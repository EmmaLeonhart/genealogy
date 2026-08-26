"""Every solo-child slot the zipper resolved, and why that cell is the worst in the join.

    python scripts/census-solo-children.py

**Emma, 2026-08-25:** *"solo child gives a bit of support but it's not gospel I'm gonna ask for a
queued up analysis on synoptic tree vs wikidata solo children situations like this."* And, before
any of it was measured: *"Solo child says nothing unless there's some reason to match them lol."*

She was right and it is now measured twice. `child`+`solo` is the worst cell in the join by the
one check with near-total coverage — **10.0%** of its pairs are refuted outright by `P21` *sex or
gender*, against **0.0%** for `father`+`solo` and `mother`+`solo`.

**What no previous pass could say is why**, and the reason matters because `solo` looks like the
strongest possible evidence: one unpaired person on each side, no ambiguity at all. The catch is
that uniqueness is worthless when the set has one element. A slot reads `1 × 1` for two very
different reasons:

* **genuinely an only child** — both sides record one child and mean it;
* **a truncated sibship** — one or both sides record one child because that is all anybody
  entered, or because an export ball hit its size bound mid-family.

The second is not a match. It is two arbitrary children of the same couple, and position cannot
tell them apart any better than it can tell two-against-two apart — which the zipper already
refuses.

## What this builds

One row per solo-child slot, per `CLAUDE.md` § *"Analyse this" means build a CSV*: every
instance, not a sample. Columns say what each side recorded, what each side *actually has*, and
whether the free checks agree.

The discriminator the join never uses is **sex**: `P21` against our `sex` column costs nothing,
needs no name, and refutes a pairing outright. It is already applied as a filter in
`scripts/zipper-join.py`; here it is used to measure what is left.

Writes `reports/solo-children.csv` and prints the analysis.
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
    # **The refuted proposals are included, and leaving them out was the first version's
    # mistake.** `scripts/zipper-join.py` already drops sex-refuted proposals, so
    # `zipper-pairs.tsv` holds only survivors -- measuring sex disagreement over it returns
    # 0.0% by construction, which describes the filter and not the join. `CLAUDE.md` records
    # this shape twice already: a date curve that tracked date coverage, and one that tracked
    # date softness. Third time.
    pairs = []
    for path, was_refuted in ((R / "zipper-pairs.tsv", False),
                              (R / "zipper-sex-refuted.tsv", True)):
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                if r["slot"] == "child" and r["method"] == "solo":
                    r["_refuted"] = was_refuted
                    pairs.append(r)
    kept = sum(1 for r in pairs if not r["_refuted"])
    print(f"{len(pairs):,} proposals through a solo CHILD slot: "
          f"{kept:,} kept, {len(pairs) - kept:,} already refused by sex")

    fam = {}
    with open(R / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fam[row["geni_id"]] = row
    theirs = {}
    with open(ROOT / "out" / "wikidata" / "relations.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            theirs[row["qid"]] = row
    our_sex, their_sex, our_year, their_year = {}, {}, {}, {}
    with open(R / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["sex"] in ("M", "F"):
                our_sex[row["geni_id"]] = row["sex"]
            if row["birth_date_year"]:
                try:
                    our_year[row["geni_id"]] = int(row["birth_date_year"])
                except ValueError:
                    pass
    with open(ROOT / "out" / "wikidata" / "sex.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["sex"] in ("M", "F"):
                their_sex[row["qid"]] = row["sex"]
    with open(ROOT / "out" / "wikidata" / "dates.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["birth_year"]:
                their_year[row["qid"]] = int(row["birth_year"])
    names = {}
    with open(R / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            names[row["geni_id"]] = row["label_en"] or row["label_mul"]

    # How many exports hold each person: a person seen once may sit on a ball's rim, where a
    # sibship is truncated by the size bound rather than by the family being small.
    presence = {}
    p = R / "density-presence.tsv"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                presence[row.get("geni_id", "")] = row.get("exports", "")

    rows, tally = [], collections.Counter()
    for r in pairs:
        g, q, parent = r["geni_id"], r["qid"], r["from_geni"]
        pr = fam.get(parent) or {}
        ours_kids = [x for x in split(pr.get("children")) if x in fam]
        their_parent = theirs.get(r["from_qid"]) or {}
        their_kids = [x for x in (their_parent.get("p40") or "").split(";") if x]

        sx = ""
        if r["_refuted"]:
            sx = "DISAGREE"
        elif our_sex.get(g) and their_sex.get(q):
            sx = "agree" if our_sex[g] == their_sex[q] else "DISAGREE"
        dt = ""
        if g in our_year and q in their_year:
            d = abs(our_year[g] - their_year[q])
            dt = "within 10y" if d <= 10 else f"{d}y apart"

        # The shape that matters: was the slot 1x1 because the family IS small, or because
        # only one child is recorded on a side that plainly has more?
        shape = ("both sides record ONE child" if len(ours_kids) <= 1 and len(their_kids) <= 1
                 else "our side records more" if len(ours_kids) > 1 and len(their_kids) <= 1
                 else "their side records more" if len(their_kids) > 1 and len(ours_kids) <= 1
                 else "BOTH sides record more")
        tally[shape] += 1
        rows.append({
            "geni_id": g, "our_name": names.get(g, ""), "qid": q,
            "parent_geni": parent, "parent_name": names.get(parent, ""),
            "our_siblings_recorded": len(ours_kids), "their_siblings_recorded": len(their_kids),
            "shape": shape, "sex": sx, "dates": dt, "round": r["round"],
            "our_exports": presence.get(g, ""),
            "sex_refused_it": "yes" if r["_refuted"] else "",
        })

    with open(R / "solo-children.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    print(f"\nWHY the slot was 1x1 -- the whole question:\n")
    for shape, n in tally.most_common():
        print(f"   {n:>6,}  {100 * n / len(rows):>5.1f}%  {shape}")

    print("\nsex disagreement by shape, over PROPOSALS not survivors:")
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        c = by[r["shape"]]
        if r["sex"]:
            c["checked"] += 1
            if r["sex"] == "DISAGREE":
                c["bad"] += 1
    for shape, c in sorted(by.items(), key=lambda kv: -kv[1]["checked"]):
        if c["checked"] < 20:
            continue
        print(f"   {c['bad']:>4,} of {c['checked']:>5,}  {100*c['bad']/c['checked']:>5.1f}%  "
              f"{shape}")

    print("\ndate disagreement by shape, where both sides carry a year:")
    byd = collections.defaultdict(collections.Counter)
    for r in rows:
        if r["dates"]:
            c = byd[r["shape"]]
            c["checked"] += 1
            if r["dates"] != "within 10y":
                c["bad"] += 1
    for shape, c in sorted(byd.items(), key=lambda kv: -kv[1]["checked"]):
        if c["checked"] < 20:
            continue
        print(f"   {c['bad']:>4,} of {c['checked']:>5,}  {100*c['bad']/c['checked']:>5.1f}%  "
              f"{shape}")
    print("\nwrote reports/solo-children.csv")


if __name__ == "__main__":
    main()
