"""How far out on the graph each person sits --- the "eccentric" people, measured.

**Emma, 2026-09-03:** *"George RR Martin is interesting due to his eccentricity… Might be worth
measuring the most eccentric people in the synoptic tree."*

**Eccentricity has been doing two jobs in this repo and they are not the same number**, so both
are computed and both are columns. Conflating them is how a ranking ends up measuring one thing
and being read as the other.

* `dist_charlemagne` --- **distance from the centre.** Emma's own claim is that *"Charlemagne is
  the most central person in the Jenny graph"*, and it is his centrality that makes him the
  anchor for the path campaign. One BFS. This is the sense in which a Geni path query times out:
  the far side of the graph is expensive to reach from the middle.
* `ecc_lower_bound` --- **graph eccentricity proper**, the greatest distance from a person to
  anyone else. Exact eccentricity is a BFS per person, which is 1.45M BFS runs and not happening.
  A **landmark lower bound** is standard and tight in practice: BFS from a set of landmarks, take
  each person's maximum distance to any of them. It never over-states.

**The landmarks are chosen by double sweep, not by taste.** BFS from Charlemagne gives the
farthest person `u`; BFS from `u` gives the farthest `v`; `u` and `v` are near-diametral, and
further landmarks are taken as the farthest point from everything chosen so far. That is the
usual construction for a diameter lower bound and it needs no judgement about who *looks*
peripheral.

**The two rankings do NOT agree, and that is the finding rather than a defect.** A person in a
small component has a small eccentricity because there is nobody far away to be far from ---
being isolated makes you *less* eccentric by the graph measure while being exactly the person the
word is reaching for. So a small component is reported by its size and excluded from the
eccentricity ranking rather than allowed to sit at the bottom of it looking well-connected.
`CLAUDE.md` § *A small component is IGNORED* governs what is then done about them: nothing.

**Edges are parent, child and spouse, undirected.** Geni records no sibling edge --- siblings are
two hops through a shared parent --- so nothing is added for them; `CLAUDE.md` § *A sibling step
is the worked example* is the long form. Multi-valued cells are split on **` | `, spaces
included**, which is the separator that has silently truncated this repo's joins before: § *Our
side could never have two children*.

    python scripts/measure-eccentricity.py [--landmarks N]

Writes `reports/tree-eccentricity.csv` --- one row per person, every person, per `CLAUDE.md`
§ *"Analyse this" means build a CSV of every instance*.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import sys
from collections import deque
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
csv.field_size_limit(10_000_000)

FAMILY_GZ = REPO / "reports" / "derived-family.csv.gz"
FAMILY_CSV = REPO / "reports" / "derived-family.csv"
LABELS_GZ = REPO / "reports" / "derived-labels.csv.gz"
LABELS_CSV = REPO / "reports" / "derived-labels.csv"
OUT = REPO / "reports" / "tree-eccentricity.csv"

SEP = " | "
LINK_COLUMNS = ("father", "mother", "spouses", "children", "fathers", "mothers")

#: `Q3044` Charlemagne. Emma, 2026-09-03: *"Charlemagne is the most central person in the Jenny
#: graph"*, which is why the path campaign anchors on him.
CHARLEMAGNE = "6000000002457013227"


def _open(gz: Path, plain: Path):
    return open(plain, encoding="utf-8") if plain.exists() else gzip.open(gz, "rt", encoding="utf-8")


def load_graph():
    """`(index, neighbours)` --- geni id to int, and an adjacency list of ints.

    Built undirected: every edge is added in both directions, because a parent link read only
    downward makes a tree rather than the graph these distances are about.
    """
    index: dict[str, int] = {}
    edges: list[tuple[int, int]] = []

    def idx(g: str) -> int:
        i = index.get(g)
        if i is None:
            i = len(index)
            index[g] = i
        return i

    with _open(FAMILY_GZ, FAMILY_CSV) as fh:
        for row in csv.DictReader(fh):
            a = idx(row["geni_id"])
            for col in LINK_COLUMNS:
                cell = row.get(col) or ""
                if not cell:
                    continue
                for other in cell.split(SEP):
                    other = other.strip()
                    if other:
                        edges.append((a, idx(other)))

    # **Dedupe, or `degree` is doubled.** Every relationship appears on BOTH people's rows --- a
    # father on the child's `father`, the child on the father's `children` --- so appending
    # blindly counts each edge twice. Distances are unaffected (a repeated neighbour is just
    # revisited and skipped), which is what makes it easy to miss: the tell was **0 people with
    # degree 1** in a tree of 1.45M, which cannot be true and was the doubling, not a finding.
    sets: list[set[int]] = [set() for _ in range(len(index))]
    for a, b in edges:
        if a != b:
            sets[a].add(b)
            sets[b].add(a)
    neighbours: list[list[int]] = [sorted(s) for s in sets]
    return index, neighbours


def bfs(start: int, neighbours) -> list[int]:
    """Hop distance from `start`; -1 for anyone in another component."""
    dist = [-1] * len(neighbours)
    dist[start] = 0
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        d = dist[cur] + 1
        for n in neighbours[cur]:
            if dist[n] < 0:
                dist[n] = d
                queue.append(n)
    return dist


def components(neighbours) -> list[int]:
    """Component id per person, and it is the thing that makes the ranking honest.

    A two-person component has eccentricity 1. Ranking on eccentricity alone therefore puts the
    most isolated people at the *bottom*, which inverts the question being asked.
    """
    comp = [-1] * len(neighbours)
    cid = 0
    for s in range(len(neighbours)):
        if comp[s] >= 0:
            continue
        comp[s] = cid
        queue = deque([s])
        while queue:
            cur = queue.popleft()
            for n in neighbours[cur]:
                if comp[n] < 0:
                    comp[n] = cid
                    queue.append(n)
        cid += 1
    return comp


def load_labels(index):
    lab: dict[int, tuple[str, str]] = {}
    with _open(LABELS_GZ, LABELS_CSV) as fh:
        for row in csv.DictReader(fh):
            i = index.get(row["geni_id"])
            if i is not None:
                lab[i] = (row.get("qid", ""), row.get("label_en", ""))
    return lab


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--landmarks", type=int, default=8, help="landmark BFS runs (default 8)")
    args = ap.parse_args()

    index, neighbours = load_graph()
    print(f"graph: {len(index):,} people, {sum(len(n) for n in neighbours) // 2:,} edges",
          file=sys.stderr)

    comp = components(neighbours)
    sizes: dict[int, int] = {}
    for c in comp:
        sizes[c] = sizes.get(c, 0) + 1
    big = max(sizes, key=lambda c: sizes[c])
    print(f"components: {len(sizes):,}; largest {sizes[big]:,} people", file=sys.stderr)

    start = index.get(CHARLEMAGNE)
    if start is None:
        print(f"Charlemagne {CHARLEMAGNE} is not in the tree", file=sys.stderr)
        return 1
    dist_c = bfs(start, neighbours)
    print(f"BFS from Charlemagne: reaches {sum(1 for d in dist_c if d >= 0):,}, "
          f"max hop {max(dist_c)}", file=sys.stderr)

    # Double sweep, then greedy-farthest for the rest. Each landmark is the person currently
    # farthest from every landmark already chosen, which is what makes the bound tight.
    best = [d if d >= 0 else 0 for d in dist_c]
    landmarks: list[int] = []
    for n in range(args.landmarks):
        nxt = max(range(len(best)), key=lambda i: best[i])
        landmarks.append(nxt)
        d = bfs(nxt, neighbours)
        for i, v in enumerate(d):
            if v > best[i]:
                best[i] = v
        print(f"  landmark {n + 1}: max distance now {max(best)}", file=sys.stderr)

    lab = load_labels(index)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".csv.tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["geni_id", "qid", "label_en", "degree", "component_size",
                    "in_largest_component", "dist_charlemagne", "ecc_lower_bound"])
        # Sorted by geni_id, a total key, so a rebuild is byte-identical ---
        # `CLAUDE.md` § *SORTING MUST BE DETERMINISTIC*.
        for g, i in sorted(index.items()):
            qid, label = lab.get(i, ("", ""))
            w.writerow([g, qid, label, len(neighbours[i]), sizes[comp[i]],
                        1 if comp[i] == big else 0,
                        dist_c[i], best[i]])
    tmp.replace(OUT)
    print(f"wrote {OUT.relative_to(REPO)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
