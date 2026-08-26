"""The Bure roster from BOTH sides, and the residue each one misses.

    python scripts/build-bure-roster.py

**Emma, 2026-08-25**, asked for *"bure kinship people (all of them)"* as random-walk start points,
and would not choose between roster definitions when offered them — so both are built and the
residue is the deliverable. Her framing of why this is a different job:

> *"bure is a bunch of unlinked people with entity resolutions to geni, so it isn't dense it's a
> different kind of area though which needs its own algorithm... as so many people there have
> wikidata items already the types of quickstatements will be different and potentially more
> challenging."*

## The two definitions

**(a) Wikidata-side** — the existing `reports/bureatten.csv` roster, joined back to Geni through
`P2600` *Geni.com profile ID* and the roster's own `geni_ids` column.

**(b) Geni-side** — the connected Bure neighbourhood in **our corpus**, grown outward from the
people in (a) who are actually in our tree, and joined to Wikidata by `P2600`. This is the
definition that can find people Wikidata's own categories never grouped.

**The residue is the point.** Somebody in (b) and not (a) is a Bure relative Wikidata's roster
does not know about. Somebody in (a) and not (b) is a rostered person our corpus cannot reach —
which is a statement about our exports, not about them.

## The ratio that decides the batch shape

Before proposing any batch, count how many of the roster already carry each of `P22` *father*,
`P25` *mother*, `P26` *spouse* and `P40` *child*. **That ratio is what makes this a different
algorithm from the Garborg batches**: there almost every statement is part of a `CREATE`, and here
most subjects already exist, so the work is linking two QIDs that both exist. `LAST` never enters
it, and the one-hop-a-day pacing that exists to work around `LAST` does not apply.

**Bureätten the EXPORT campaign stays closed** — 7 resolved, 76 dropped, 0 exports ever run.
Nothing here searches for anybody or proposes an export.

Writes `reports/bure-roster.tsv` and `reports/bure-roster.md`. Offline.
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

#: How far to grow the Geni-side neighbourhood out from the rostered people we hold. Kinship
#: is not a radius, but a walk has to stop somewhere, and each hop is a parent, child or
#: spouse edge -- so 3 reaches cousins and grandparents without crossing into married-in
#: families' own ancestries.
GENI_HOPS = 3


def split(cell):
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def main():
    # ---- (a) the Wikidata-side roster ------------------------------------------------
    q2g, kind, title = collections.defaultdict(set), {}, {}
    with open(R / "bureatten.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            kind[row["qid"]] = row["kind"]
            title[row["qid"]] = row["sv_title"]
            for g in re.split(r"[;,| ]+", row["geni_ids"] or ""):
                if g.strip().isdigit():
                    q2g[row["qid"]].add(g.strip())
    roster = set(kind)
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0] in roster and row[1].strip().isdigit():
                q2g[row[0]].add(row[1].strip())
    p = R / "bureatten-resolved.tsv"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                if row["geni_id"].strip().isdigit():
                    q2g[row["qid"]].add(row["geni_id"].strip())

    owner = collections.defaultdict(set)
    for q, gs in q2g.items():
        for g in gs:
            owner[g].add(q)
    g2q = {g: next(iter(qs)) for g, qs in owner.items() if len(qs) == 1}
    side_a = set(g2q)
    print(f"(a) Wikidata-side: {len(roster):,} entries, "
          f"{sum(1 for k in kind.values() if k == 'person'):,} people, "
          f"{len(side_a):,} with an unambiguous Geni id")

    # ---- (b) the Geni-side neighbourhood ---------------------------------------------
    fam = {}
    with open(R / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fam[row["geni_id"]] = row
    seed = {g for g in side_a if g in fam}
    print(f"    of those, {len(seed):,} are in our corpus and {len(side_a) - len(seed):,} "
          f"are not")

    dist = {g: 0 for g in seed}
    frontier = list(seed)
    for hop in range(1, GENI_HOPS + 1):
        nxt = []
        for g in frontier:
            row = fam.get(g)
            if not row:
                continue
            for col in ("father", "mother", "children", "spouses"):
                for other in split(row[col]):
                    if other in fam and other not in dist:
                        dist[other] = hop
                        nxt.append(other)
        frontier = nxt
        if not frontier:
            break
    side_b = set(dist)
    print(f"(b) Geni-side: {len(side_b):,} people within {GENI_HOPS} hops of a rostered one")

    # ---- the correspondence for side (b) ---------------------------------------------
    held = dict(g2q)
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[1].strip() in side_b and row[0].startswith("Q"):
                held.setdefault(row[1].strip(), row[0])
    zp = R / "zipper-pairs.tsv"
    if zp.exists():
        with open(zp, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                if row["geni_id"] in side_b:
                    held.setdefault(row["geni_id"], row["qid"])

    # ---- what each side already carries ----------------------------------------------
    theirs = {}
    with open(ROOT / "out" / "wikidata" / "relations.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            theirs[row["qid"]] = row
    props = collections.Counter()
    qids = {held[g] for g in side_b if g in held}
    for q in qids:
        row = theirs.get(q)
        if not row:
            props["item has NO relationships at all"] += 1
            continue
        for prop, label in (("p22", "P22 father"), ("p25", "P25 mother"),
                            ("p26", "P26 spouse"), ("p40", "P40 child")):
            if row.get(prop):
                props[label] += 1
        if not any(row.get(p) for p in ("p22", "p25", "p26", "p40")):
            props["item has NO relationships at all"] += 1

    names = {}
    with open(R / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in side_b:
                names[row["geni_id"]] = row["label_en"] or row["label_mul"]

    rows = []
    for g in sorted(side_b, key=lambda x: (dist[x], names.get(x, ""))):
        rows.append({
            "geni_id": g, "name": names.get(g, ""), "hops_from_roster": dist[g],
            "qid": held.get(g, ""),
            "in_wikidata_roster": "yes" if g in side_a else "",
            "has_p22": "y" if (theirs.get(held.get(g, "")) or {}).get("p22") else "",
            "has_p25": "y" if (theirs.get(held.get(g, "")) or {}).get("p25") else "",
            "has_p26": "y" if (theirs.get(held.get(g, "")) or {}).get("p26") else "",
            "has_p40": "y" if (theirs.get(held.get(g, "")) or {}).get("p40") else "",
        })
    with open(R / "bure-roster.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    only_b = side_b - side_a
    only_a = side_a - side_b
    linked_b = sum(1 for g in side_b if g in held)

    with open(R / "bure-roster.md", "w", encoding="utf-8", newline="\n") as f:
        f.write("# The Bure roster, from both sides\n\n")
        f.write("Generated by `scripts/build-bure-roster.py`. Emma would not choose between the "
                "two definitions, so both are built and **the residue is the deliverable**.\n\n")
        f.write("| | count |\n| --- | ---: |\n")
        f.write(f"| (a) Wikidata-side roster with a Geni id | {len(side_a):,} |\n")
        f.write(f"| (b) Geni-side neighbourhood, {GENI_HOPS} hops | {len(side_b):,} |\n")
        f.write(f"| in both | {len(side_a & side_b):,} |\n")
        f.write(f"| **only Geni-side** — relatives Wikidata's roster misses | "
                f"**{len(only_b):,}** |\n")
        f.write(f"| **only Wikidata-side** — rostered but outside our corpus | "
                f"**{len(only_a):,}** |\n")
        f.write(f"| of (b), carrying a Wikidata item | {linked_b:,} |\n\n")
        f.write("## What the linked ones already have\n\n")
        f.write("This ratio is what makes Bure a different algorithm: the items exist, so the "
                "work is linking two QIDs rather than creating anybody, and `LAST` never "
                "enters it.\n\n")
        f.write(f"Of the **{len(qids):,}** distinct items in (b):\n\n")
        f.write("| property | items carrying it | share |\n| --- | ---: | ---: |\n")
        for label, n in props.most_common():
            f.write(f"| {label} | {n:,} | {100 * n / max(len(qids), 1):.0f}% |\n")
        f.write("\n**`reports/bure-roster.tsv`** has every person with their hop distance, QID "
                "and which of the four properties their item already carries.\n\n")
        f.write("**Bureätten the export campaign stays closed** — 7 resolved, 76 dropped, 0 "
                "exports. Nothing here searches for anybody or proposes an export.\n")

    print(f"\nin both: {len(side_a & side_b):,}")
    print(f"only Geni-side (Wikidata's roster misses them): {len(only_b):,}")
    print(f"only Wikidata-side (outside our corpus): {len(only_a):,}")
    print(f"\nof {len(qids):,} linked items in (b):")
    for label, n in props.most_common():
        print(f"   {n:>6,}  {100 * n / max(len(qids), 1):>3.0f}%  {label}")
    print("\nwrote reports/bure-roster.tsv, reports/bure-roster.md")


if __name__ == "__main__":
    main()
