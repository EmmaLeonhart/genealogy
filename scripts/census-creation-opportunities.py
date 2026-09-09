"""Children of people we have already matched, who are not on Wikidata at all.

    python scripts/census-creation-opportunities.py

**Emma, 2026-08-25, on the lopsided slots -- 2,484 where we hold two unmatched children and
Wikidata holds one, 2,012 where we hold five and they hold one:** *"Uhhhh yeah no shit it's an
adding opportunity but we do need to figure out which person merges in if present lmfao lol like
zipping has a direction. If we have entity resolved one of the children and the other 4 are absent
from wikidata is not a problem at all lol."*

Both halves matter and they run in that order:

**Direction first.** A five-against-one slot is not five candidates for one item. It is one item
that belongs to one of our five, and four people Wikidata does not have. `scripts/zipper-join.py`
now does the placing -- solo, then dates, then names inside the slot -- so by the time this runs,
their one child either has a partner or is honestly still ambiguous.

**Then the leftovers are the opportunity, not a failure.** A child of ours with no correspondence,
whose parent *does* have one, is a person we can create **already attached to a parent that
exists** -- which is the whole shape `docs/wikidata-item-template.md` describes and the reason
`CLAUDE.md` puts the Geni id before everything else.

Ranked by **distance from Arne Garborg**, because `CLAUDE.md` is explicit that proximity beats
volume: *"A thousand people on the far side of the tree are worth less than fifty in her own
neighbourhood."* Distance is hop count over parent, child and spouse edges in our own tree.

**This writes a census, never an edit batch.** `CLAUDE.md`: a `.qs` produced uninvited *"presents
work as ready that nobody sanctioned"*.

Writes `reports/creation-opportunities.tsv`. Offline.
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

#: **Arne Garborg the writer**, `Q467497`. Note `reports/derived-labels.csv` gives this profile
#: the label `Arne Olaus Fjørtoft Garborg` -- which is the name `CLAUDE.md`'s own NN-label example
#: uses -- and carries `Q11959067` against it, while `reports/garborg-qids.tsv` puts `Q467497` on
#: his FATHER `6000000003492005116` `Aadne Eivindson Garborg`. One of those is wrong and it is not
#: this script's to settle; the hop count only needs the right person.
ARNE = "6000000005607426327"
MAX_HOPS = 12


def split(cell):
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def main():
    ours = {}
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ours[row["geni_id"]] = row
    names = {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            names[row["geni_id"]] = row["label_en"] or row["label_mul"]
    years = {}
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["birth_date_year"]:
                years[row["geni_id"]] = row["birth_date_year"]

    # Every correspondence we hold: what Wikidata states, plus the join.
    held = {}
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0].startswith("Q") and row[1].strip().isdigit():
                held.setdefault(row[1].strip(), row[0])
    stated = len(held)
    with open(ROOT / "reports" / "zipper-pairs.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            held.setdefault(row["geni_id"], row["qid"])
    print(f"{stated:,} stated + zipper -> {len(held):,} people we can already point at an item")

    # Hops from Arne over parent/child/spouse edges. Proximity beats volume.
    dist = {ARNE: 0}
    frontier = [ARNE]
    for hop in range(1, MAX_HOPS + 1):
        nxt = []
        for g in frontier:
            r = ours.get(g)
            if not r:
                continue
            for col in ("father", "mother", "children", "spouses"):
                for n in split(r.get(col)):
                    if n in ours and n not in dist:
                        dist[n] = hop
                        nxt.append(n)
        frontier = nxt
        if not frontier:
            break
    print(f"{len(dist):,} people within {MAX_HOPS} hops of Arne Garborg")

    rows = []
    for g, r in ours.items():
        if g not in held:
            continue                       # only anchored parents can host a creation
        for c in split(r.get("children")):
            if c not in ours or c in held:
                continue
            rows.append({
                "child_geni_id": c,
                "child_name": names.get(c, ""),
                "child_birth_year": years.get(c, ""),
                "parent_geni_id": g,
                "parent_name": names.get(g, ""),
                "parent_qid": held[g],
                "hops_from_arne": dist.get(c, ""),
            })
    # One row per child, keeping the parent that is nearest Arne.
    best = {}
    for row in rows:
        k = row["child_geni_id"]
        cur = best.get(k)
        rank = row["hops_from_arne"] if row["hops_from_arne"] != "" else 999
        if cur is None or rank < (cur["hops_from_arne"] if cur["hops_from_arne"] != "" else 999):
            best[k] = row
    rows = sorted(best.values(),
                  key=lambda r: (r["hops_from_arne"] if r["hops_from_arne"] != "" else 999,
                                 r["child_name"]))

    out = ROOT / "reports" / "creation-opportunities.tsv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"\n{len(rows):,} people absent from Wikidata whose PARENT already has an item")
    near = collections.Counter(r["hops_from_arne"] for r in rows)
    print("\nby hops from Arne Garborg:")
    for h in sorted(k for k in near if k != ""):
        print(f"   {h:>3} hops   {near[h]:>7,}")
    if near.get(""):
        print(f"   beyond {MAX_HOPS}   {near['']:>7,}")
    print(f"\nwrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
