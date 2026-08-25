"""Prove two Geni profiles are one person because their RELATIVES are paired too.

    python scripts/corroborate-pairs-by-lineage.py

**Found 2026-08-25 while opening the multi-`P2600` targets by hand.** `Q13478526` pairs
*Vasilko II Bryachislavich of Vitebsk* with *Василий Брячиславич* — and both profiles record the
same daughter, who is herself another target: `Q13478538` pairs *Lyubava Vasilkovna of Vitebsk*
with *Любовь Васильевна*. Checking the cluster, **17 of the 52 unopened targets are one lineage**,
the Polotsk / Vitebsk / Smolensk Rurikids, imported into Geni twice — once romanised, once in
Cyrillic — with Wikidata joining them person by person.

## The test, and why it is not name matching

For a pair `(A, B)` on one Wikidata item, look at `A`'s father and `B`'s father in **our tree**.
If those two profiles are themselves both carried by a **single** Wikidata item, that is an
independent assertion that `A`'s father and `B`'s father are one man — and two people with the
same father, the same mother or the same child are the same person.

**No name is compared anywhere in this module.** The evidence is entirely `P2600` incidence:
Wikidata already claims each relative pair is one person, and this module only asks whether those
claims line up across a generation. That is the zipper join Emma described — *"we merge them based
off of whether something is the mother on both sides of an individual"* — applied to a pair whose
identity is in question rather than to a pair being proposed.

## What it can and cannot conclude

* **`CORROBORATED`** — at least one relative pair is co-carried. The two profiles are one person,
  and the wrong `P2600` is a removal candidate for `resolve-multi-geni-by-parents.py`.
* **`CONTRADICTED`** — a relative slot is filled on both sides and the two relatives are on
  **different** Wikidata items which are not the same item. That argues the pair is two people.
* **`NO EVIDENCE`** — the relatives are absent from our tree, or absent from Wikidata, or present
  but never co-carried. **Silence, not a verdict**: most pairs will land here and it means only
  that the lineage was not imported twice.

**It never emits an edit.** Output feeds the hand-judging queue in
`reports/multi-p2600-verdicts.tsv`, which is still only written after both Geni pages are opened.
The corroboration is strong enough to rank a pair, not to delete a statement unseen.

Writes `reports/multi-p2600-lineage.tsv`.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent


def main():
    # Which Wikidata items carry which Geni ids -- Wikidata's own statements only.
    carried = collections.defaultdict(set)      # geni id -> {qid}
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0].startswith("Q") and row[1].strip().isdigit():
                carried[row[1].strip()].add(row[0])
    print(f"{len(carried):,} Geni ids carried by Wikidata")

    targets = list(csv.DictReader(open(ROOT / "reports" / "multi-p2600-targets.tsv",
                                       encoding="utf-8"), delimiter="\t"))
    want = {g for r in targets for g in r["geni_ids"].split(";")}

    father, mother = {}, {}
    children = collections.defaultdict(set)
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            me = row["geni_id"]
            fa = (row.get("father") or "").strip()
            mo = (row.get("mother") or "").strip()
            if me in want:
                if fa:
                    father[me] = fa
                if mo:
                    mother[me] = mo
                for c in (row.get("children") or "").replace(",", ";").split(";"):
                    c = c.strip()
                    if c:
                        children[me].add(c)
    print(f"{len(father):,} of the targets' profiles have a father recorded, "
          f"{len(mother):,} a mother")

    def shared_item(a, b):
        """The Wikidata items carrying BOTH a and b, if any."""
        if not a or not b or a == b:
            return set()
        return carried.get(a, set()) & carried.get(b, set())

    rows = []
    tally = collections.Counter()
    for r in targets:
        gs = r["geni_ids"].split(";")
        if len(gs) != 2:
            continue
        a, b = gs
        support, against = [], []

        for slot, table in (("father", father), ("mother", mother)):
            ra, rb = table.get(a), table.get(b)
            if not ra or not rb:
                continue
            both = shared_item(ra, rb)
            if both:
                support.append(f"{slot}s {ra} + {rb} co-carried by {'/'.join(sorted(both))}")
            elif ra != rb and carried.get(ra) and carried.get(rb):
                against.append(f"{slot}s {ra} and {rb} on different items")

        for ca in children.get(a, ()):
            for cb in children.get(b, ()):
                both = shared_item(ca, cb)
                if both:
                    support.append(
                        f"children {ca} + {cb} co-carried by {'/'.join(sorted(both))}")
                    break
            if support and support[-1].startswith("children"):
                break

        verdict = ("CORROBORATED" if support else
                   "CONTRADICTED" if against else "NO EVIDENCE")
        tally[verdict] += 1
        rows.append({
            "verdict": verdict, "qid": r["qid"],
            "geni_a": a, "geni_b": b,
            "supporting": " | ".join(support),
            "against": " | ".join(against),
            "names": r["names"][:90],
        })

    rows.sort(key=lambda r: ({"CORROBORATED": 0, "CONTRADICTED": 1, "NO EVIDENCE": 2}[r["verdict"]],
                             r["qid"]))
    dest = ROOT / "reports" / "multi-p2600-lineage.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"\nwrote {dest.relative_to(ROOT)}  -- ranks pairs, never emits an edit\n")
    for k in ("CORROBORATED", "CONTRADICTED", "NO EVIDENCE"):
        print(f"   {tally[k]:>3}  {k}")

    print("\ncorroborated pairs -- the relatives are paired too, so these are one person:")
    for r in rows:
        if r["verdict"] != "CORROBORATED":
            break
        print(f"   {r['qid']:<12} {r['names'][:52]}")
        print(f"        {r['supporting'][:150]}")


if __name__ == "__main__":
    main()
