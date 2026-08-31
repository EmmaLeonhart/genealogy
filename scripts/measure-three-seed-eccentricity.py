"""Is Emma eccentric on the SYNOPTIC TREE, once all three seeds are taken together?

    python scripts/measure-three-seed-eccentricity.py [--limit 5000]

**Emma's hypothesis, 2026-08-30.** The Wikidata measurement put her at the graph's maximum
eccentricity, at the end of a filament. Her expectation is that this is an artefact of Wikidata
being *incomplete*, and that on the synoptic tree — where the family structure is dense rather
than traced — she is neither eccentric nor central.

Her reasoning for measuring here rather than there: *"over time, wikidata is going to converge to
our synoptic tree."* So the synoptic tree is the better predictor of the eventual shape, and the
Wikidata reading is a snapshot of a transient state.

**Three seeds, not one, and that is the point.** A BFS of `--limit` people from each of Johannes
Bureus, Arne Garborg and Emma, unioned. Her design decision, stated the same day: *"the
particular reason why I actually did three spines to me instead of one is actually specifically
because three spines makes it less eccentric."* A node at the convergence of three filaments is
closer to everything than a node at the end of one, so the test has to include all three regions
or it measures the wrong graph.

**Convergence is not uniform and the report says so.** Her expectation of which parts of Wikidata
catch up first: the Bure people, then Arne's, then hers. The eventual shape arrives in that
order, so a reading taken today sits somewhere along it.

Edges are `father`, `mother`, `spouses` and `children` from `reports/derived-family.csv`, both
directions. Cells are separated by ` | `, spaces included — `CLAUDE.md` § *Our side could never
have two children* is what splitting on the wrong thing costs.
"""
from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

FAMILY = ROOT / "reports" / "derived-family.csv"
LABELS = ROOT / "reports" / "derived-labels.csv"

SEEDS = {
    "Johannes Bureus": "6000000004334763223",
    "Arne Garborg": "6000000003492005116",
    "Emma": "6000000087535357291",
}


def cells(value):
    return [v.strip() for v in (value or "").split("|") if v.strip()]


def load_adjacency():
    adj = collections.defaultdict(set)
    with FAMILY.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            me = row["geni_id"]
            for col in ("father", "mother", "spouses", "children"):
                for other in cells(row.get(col)):
                    adj[me].add(other)
                    adj[other].add(me)
    return adj


def bfs(adj, src, limit):
    seen = {src: 0}
    queue = collections.deque([src])
    while queue and len(seen) < limit:
        x = queue.popleft()
        for n in adj.get(x, ()):
            if n not in seen:
                seen[n] = seen[x] + 1
                queue.append(n)
                if len(seen) >= limit:
                    break
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=5000)
    args = ap.parse_args()

    print("loading the synoptic tree ...", flush=True)
    adj = load_adjacency()
    print(f"{len(adj):,} people with at least one relationship\n")

    reached = {}
    for name, seed in SEEDS.items():
        d = bfs(adj, seed, args.limit)
        reached[name] = d
        print(f"{name:<18}{len(d):,} people within {max(d.values())} hops")

    union = set().union(*(set(d) for d in reached.values()))
    print(f"\nunion of the three: {len(union):,} people")
    for a in SEEDS:
        for b in SEEDS:
            if a < b:
                overlap = len(set(reached[a]) & set(reached[b]))
                print(f"   {a} n {b}: {overlap:,}")

    ind = {q: {n for n in adj.get(q, ()) if n in union} for q in union}
    labels = {}
    with LABELS.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["geni_id"] in union:
                labels[row["geni_id"]] = row.get("label_mul") or row.get("label_en") or ""

    def ecc(src):
        seen = {src: 0}
        queue = collections.deque([src])
        while queue:
            x = queue.popleft()
            for n in ind.get(x, ()):
                if n not in seen:
                    seen[n] = seen[x] + 1
                    queue.append(n)
        return max(seen.values()), len(seen)

    print(f"\n{'':<18}{'degree':>7}{'eccentricity':>14}{'reaches':>9}")
    for name, seed in SEEDS.items():
        e, r = ecc(seed)
        print(f"{name:<18}{len(ind.get(seed, ())):>7}{e:>14}{r:>9}")

    # Where does Emma fall in the distribution? Sample, because all-pairs is too costly.
    import random
    random.seed(20260830)
    sample = random.sample(sorted(union), min(400, len(union)))
    eccs = sorted(ecc(q)[0] for q in sample)
    emma_e = ecc(SEEDS["Emma"])[0]
    below = sum(1 for e in eccs if e < emma_e)
    print(f"\nover a 400-person sample of the union:")
    print(f"   eccentricity min {eccs[0]}, median {eccs[len(eccs)//2]}, max {eccs[-1]}")
    print(f"   Emma's is {emma_e} — {100*below/len(eccs):.0f}% of the sample is LESS eccentric")
    deg = collections.Counter({q: len(v) for q, v in ind.items()})
    print(f"\n   Emma's degree {len(ind.get(SEEDS['Emma'], ()))}; "
          f"median degree {sorted(deg.values())[len(deg)//2]}")


if __name__ == "__main__":
    main()
