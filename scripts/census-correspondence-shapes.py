"""Every SHAPE of multiplicity in the QID<->Geni correspondence, counted not assumed.

    python scripts/census-correspondence-shapes.py

**Emma, 2026-08-24:** *"You conflated wiki data items having two Jenny links on them...
Now you're talking about wikidata items that link to the same Jenny item. That is a very
different phenomenon... and there might be some other things that you have here."*

She is right on both counts, and the second half is why this script exists rather than a
paragraph asserting there are three kinds. The shapes are **measured**.

**The two directions are opposites with opposite fixes.**

* **One Wikidata item carrying several Geni ids.** Her explanation of the cause, which is
  about how Geni behaves rather than about error: a profile gets isolated from the main
  tree, nobody can edit it, so somebody creates a new one -- *"Jenny doesn't have the
  ability to differentiate between multiple different contradictory facts."* Zerubbabel is
  the standing example. `CLAUDE.md` rules these **unmergeable and correct**: `P2600` is
  multi-valued and 2,861 stored items already carry more than one.
* **Several Wikidata items carrying one Geni id.** Wikidata duplication, fixed by merging
  **Wikidata** items. Nothing to do with Geni.

**And the shape nobody named: a component larger than a pair.** The two directions are
not exclusive -- a QID with two Geni ids, one of which also carries a second QID, is a
connected blob needing a Geni merge *and* a Wikidata merge. A per-row view cannot see one
of these at all, which is exactly the blind spot that let two phenomena be narrated as
one. So this walks connected components of the bipartite graph and reports `Q x G`.

`1x1` is clean. `1xN` is direction one. `Nx1` is direction two. Anything else is a tangle.

Provenance is carried through, because *who claims a pair* decides the fix: a competing
pair sourced only from `wikidata-p2600` is Wikidata's own contradiction, while one
sourced from `structural` is our inference and ours to withdraw.

Reads `reports/synoptic-correspondence.tsv`. Offline.
Writes `reports/correspondence-shapes.tsv`.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent

#: Sources that are Wikidata SPEAKING FOR ITSELF, as against our own joins. A conflict
#: among these is Wikidata contradicting Wikidata; a conflict involving anything else is
#: at least partly ours, and ours is the side that yields.
WIKIDATA_STATED = {"wikidata-p2600"}


def main():
    src = ROOT / "reports" / "synoptic-correspondence.tsv"
    pairs = {}
    with open(src, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            pairs[(row["qid"], row["geni_id"])] = set(row["sources"].split(";"))
    print(f"{len(pairs):,} pairs in {src.relative_to(ROOT)}")

    # Union-find over the bipartite graph. Nodes are ("Q", qid) and ("G", geni_id).
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for q, g in pairs:
        union(("Q", q), ("G", g))

    comps = collections.defaultdict(lambda: {"q": set(), "g": set(), "pairs": []})
    for (q, g), sources in pairs.items():
        c = comps[find(("Q", q))]
        c["q"].add(q)
        c["g"].add(g)
        c["pairs"].append((q, g, sources))

    shapes = collections.Counter()
    rows = []
    for root, c in comps.items():
        nq, ng = len(c["q"]), len(c["g"])
        shape = f"{nq}x{ng}"
        shapes[shape] += 1
        if nq == 1 and ng == 1:
            continue                      # clean; not worth a row
        flat = {s for _, _, ss in c["pairs"] for s in ss}
        if nq == 1:
            kind = "one item, several Geni profiles"
        elif ng == 1:
            kind = "several items, one Geni profile"
        else:
            kind = "TANGLE - needs both merges"
        who = ("wikidata only" if flat <= WIKIDATA_STATED
               else "ours only" if not (flat & WIKIDATA_STATED)
               else "mixed")
        for q, g, ss in sorted(c["pairs"]):
            rows.append({
                "shape": shape, "kind": kind, "claimed_by": who,
                "qid": q, "geni_id": g, "sources": ";".join(sorted(ss)),
                "component_qids": ";".join(sorted(c["q"])),
                "component_geni_ids": ";".join(sorted(c["g"])),
            })

    dest = ROOT / "reports" / "correspondence-shapes.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    total = sum(shapes.values())
    clean = shapes.get("1x1", 0)
    print(f"\n{total:,} connected components; {clean:,} are a clean 1x1 "
          f"({100 * clean / total:.1f}%)")
    print(f"{total - clean:,} carry multiplicity -> {dest.relative_to(ROOT)}\n")

    by_kind = collections.Counter((r["kind"], r["claimed_by"]) for r in rows)
    seen = set()
    print(f"  {'components':>10}  {'kind':<34} claimed by")
    per = collections.Counter()
    for r in rows:
        key = (r["component_qids"], r["component_geni_ids"])
        if key in seen:
            continue
        seen.add(key)
        per[(r["kind"], r["claimed_by"])] += 1
    for (kind, who), n in per.most_common():
        print(f"  {n:>10}  {kind:<34} {who}")

    print("\n  shapes bigger than a pair:")
    for shape, n in sorted(shapes.items(),
                           key=lambda kv: -kv[1]):
        nq, ng = (int(x) for x in shape.split("x"))
        if nq > 1 and ng > 1:
            print(f"    {shape:<8} {n}")


if __name__ == "__main__":
    main()
