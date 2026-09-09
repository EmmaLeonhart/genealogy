"""Map every connected family component in the stored Wikidata graph.

Walking outward from one person answers "is this an island?" for that person and
costs a pass over the shards each time. Emma is going to ask it repeatedly —
*"I will look at other similar points as well"* — so this computes it once for
all 1,408,402 items and writes the component of each, making every later question
a lookup.

Connectivity is `P22`/`P25`/`P26`/`P40`/`P3373` — the same five the download
walked. Union-find over the edges, one streaming pass, no items held.

**An item's component size is the difference between joining the world tree and
joining a hamlet.** Trond Benkestok has a father and a child on Wikidata and his
whole component is three people; the Egede-Nissen cluster runs past 1,792.

Writes `reports/wikidata-components.csv` — qid, component id, component size —
and `reports/wikidata-components-summary.md`.

    py scripts/build-wikidata-components.py
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
OUT_CSV = REPO_ROOT / "reports" / "wikidata-components.csv"
OUT_MD = REPO_ROOT / "reports" / "wikidata-components-summary.md"

RELATION_PROPS = ("P22", "P25", "P26", "P40", "P3373")


class Union:
    """Union-find with path halving. Keyed by QID string."""

    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def main() -> int:
    uf = Union()
    stored: set[str] = set()
    edges = 0
    shards = wikistore.shards(STORE)
    print(f"{len(shards):,} shards", flush=True)

    for n, shard in enumerate(shards, 1):
        for entity in wikistore.read_shard(shard):
            qid = entity.get("id")
            if not isinstance(qid, str):
                continue
            stored.add(qid)
            uf.find(qid)
            claims = entity.get("claims") or {}
            for prop in RELATION_PROPS:
                for statement in claims.get(prop, []):
                    value = ((statement.get("mainsnak") or {}).get("datavalue") or {}).get("value") or {}
                    other = value.get("id")
                    if isinstance(other, str) and other.startswith("Q"):
                        uf.union(qid, other)
                        edges += 1
        if n % 200 == 0 or n == len(shards):
            print(f"  shard {n:,}/{len(shards):,}  {len(stored):,} items  {edges:,} edges",
                  flush=True)

    sizes: Counter[str] = Counter()
    for qid in uf.parent:
        sizes[uf.find(qid)] += 1

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["qid", "component", "component_size", "in_store"])
        for qid in sorted(uf.parent):
            root = uf.find(qid)
            writer.writerow([qid, root, sizes[root], "yes" if qid in stored else "no"])

    # Distribution. A component of one is a person Wikidata records no family for.
    buckets: Counter[str] = Counter()
    for qid in stored:
        size = sizes[uf.find(qid)]
        if size == 1:
            buckets["1 — isolate"] += 1
        elif size <= 5:
            buckets["2–5"] += 1
        elif size <= 20:
            buckets["6–20"] += 1
        elif size <= 100:
            buckets["21–100"] += 1
        elif size <= 1000:
            buckets["101–1,000"] += 1
        else:
            buckets["over 1,000"] += 1

    biggest = sizes.most_common(5)
    L: list[str] = []
    add = L.append
    add("# Connected components of the Wikidata family graph")
    add("")
    add("Computed once over the whole store so that asking whether a given person is on")
    add("an island is a lookup rather than a walk. Connectivity is")
    add("`P22`/`P25`/`P26`/`P40`/`P3373`.")
    add("")
    add(f"**{len(stored):,} stored items, {edges:,} relation edges, "
        f"{len(sizes):,} components** (including items referenced but not stored).")
    add("")
    add("## How big is the component a stored person sits in")
    add("")
    add("| component size | people | share |")
    add("| --- | ---: | ---: |")
    total = sum(buckets.values())
    for label in ("1 — isolate", "2–5", "6–20", "21–100", "101–1,000", "over 1,000"):
        n = buckets[label]
        add(f"| {label} | {n:,} | {100.0*n/max(total,1):.1f}% |")
    add("")
    add("## The largest components")
    add("")
    add("| component root | people |")
    add("| --- | ---: |")
    for root, size in biggest:
        add(f"| {root} | {size:,} |")
    add("")
    add("**This is what decides whether a link is worth making.** An ancestor whose")
    add("component is three people connects to three people. The world tree is the")
    add("component at the top of this table.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"\nwrote {OUT_CSV} and {OUT_MD}")
    print(f"  {len(stored):,} stored items, {edges:,} edges, {len(sizes):,} components")
    for label in ("1 — isolate", "2–5", "6–20", "21–100", "101–1,000", "over 1,000"):
        print(f"    {label:<14} {buckets[label]:>9,}")
    print(f"  largest: {biggest[0][1]:,} people")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
