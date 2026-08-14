"""Rank the upward frontier of a cut-off component: the tops of its deepest lines.

Corpus only — no Wikidata, no QIDs, no name matching.

A flat list of parentless people in the cluster is the wrong instrument, because
most of them are interior: an in-law who married in, a childless sibling, a leaf.
Exporting up from those refills the cluster. What continues the *ancestry* is the
person sitting at the top of a long recorded line — parentless in our data, with
many generations of descent beneath them inside the cluster.

So rank parentless people by **generations of descent below them**, and report
descendant count and birth year beside it. Depth is the ranking key: a person
with fourteen generations under them is the head of a line we have followed a
long way down and never followed up. Descendant count alone rewards a wide
recent family, which is not the same thing.

Spouse edges are ignored on purpose. A spouse link joins two people already in
the same component, so it cannot leave one.

    py scripts/cluster-upward-frontier.py [component_number]   (default 2)
"""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import sources  # noqa: E402
from genimerge.dates import parse_date  # noqa: E402

OUT = REPO / "reports" / "cluster-upward-frontier.csv"


class DSU:
    def __init__(self) -> None:
        self.p: dict[str, str] = {}

    def find(self, x: str) -> str:
        r = x
        while self.p.setdefault(r, r) != r:
            r = self.p[r]
        while self.p[x] != r:
            self.p[x], x = r, self.p[x]
        return r

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def scan():
    """One pass over the corpus: names, birth years, parent and child maps, components."""
    dsu = DSU()
    name: dict[str, str] = {}
    born: dict[str, int] = {}
    father: dict[str, str] = {}
    mother: dict[str, str] = {}
    children: dict[str, set[str]] = defaultdict(set)

    indi = re.compile(r"^0 @I(\d+)@ INDI", re.M)
    files = sources.find_exports()
    for n, path in enumerate(files, 1):
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        for gid in indi.findall(text):
            dsu.find(gid)

        cur = None
        in_birt = False
        fam_id = None
        parents: dict[str, list[tuple[str, str]]] = defaultdict(list)
        kids: dict[str, list[str]] = defaultdict(list)
        famc: dict[str, list[str]] = defaultdict(list)

        for line in text.split("\n"):
            line = line.rstrip("\r")
            if line.startswith("0 "):
                cur = fam_id = None
                in_birt = False
                m = re.match(r"^0 @I(\d+)@ INDI$", line)
                if m:
                    cur = m.group(1)
                    continue
                m = re.match(r"^0 @F(\d+)@ FAM$", line)
                if m:
                    fam_id = m.group(1)
                continue
            if cur:
                if line.startswith("1 NAME ") and cur not in name:
                    name[cur] = line[7:].replace("/", "").strip()
                elif line == "1 BIRT":
                    in_birt = True
                elif line.startswith("1 "):
                    in_birt = False
                    m = re.match(r"^1 FAMC @F(\d+)@$", line)
                    if m:
                        famc[m.group(1)].append(cur)
                elif in_birt and line.startswith("2 DATE ") and cur not in born:
                    d = parse_date(line[7:])
                    y = getattr(d, "year", None) if d else None
                    if y is not None:
                        born[cur] = y
            elif fam_id:
                m = re.match(r"^1 (HUSB|WIFE|CHIL) @I(\d+)@$", line)
                if m:
                    tag, gid = m.groups()
                    if tag == "CHIL":
                        kids[fam_id].append(gid)
                    else:
                        parents[fam_id].append(("F" if tag == "HUSB" else "M", gid))

        for fid, members in kids.items():
            group = [g for _, g in parents.get(fid, [])] + members
            for g in group[1:]:
                dsu.union(group[0], g)
            for kid in members:
                for role, pid in parents.get(fid, []):
                    (father if role == "F" else mother).setdefault(kid, pid)
                    children[pid].add(kid)
        for fid, members in famc.items():
            group = [g for _, g in parents.get(fid, [])] + members
            for g in group[1:]:
                dsu.union(group[0], g)
            for kid in members:
                for role, pid in parents.get(fid, []):
                    (father if role == "F" else mother).setdefault(kid, pid)
                    children[pid].add(kid)
        for fid, ps in parents.items():
            group = [g for _, g in ps]
            for g in group[1:]:
                dsu.union(group[0], g)

        if n % 60 == 0:
            print(f"  {n}/{len(files)} exports", file=sys.stderr)

    return dsu, name, born, father, mother, children


def descent(children, people):
    """depth = generations below; size = distinct descendants. Iterative, cycle-safe.

    A node still being expanded contributes 0 rather than nothing, so a cycle
    truncates the measure instead of making a person look childless — the trap
    `genimerge.descendants` documents.
    """
    depth: dict[str, int] = {}
    size: dict[str, int] = {}
    for root in people:
        if root in depth:
            continue
        stack = [(root, False)]
        active = set()
        while stack:
            node, expanded = stack.pop()
            if expanded:
                active.discard(node)
                d = 0
                kids = children.get(node, ())
                total = set()
                for c in kids:
                    d = max(d, 1 + depth.get(c, 0))
                    total.add(c)
                    total.update(range(0))  # placeholder, size folded below
                depth[node] = d
                size[node] = sum(1 + size.get(c, 0) for c in kids)
                continue
            if node in depth or node in active:
                continue
            active.add(node)
            stack.append((node, True))
            for c in children.get(node, ()):
                if c not in depth and c not in active:
                    stack.append((c, False))
    return depth, size


def main() -> int:
    want = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    dsu, name, born, father, mother, children = scan()

    groups: dict[str, list[str]] = defaultdict(list)
    for g in dsu.p:
        groups[dsu.find(g)].append(g)
    ordered = sorted(groups.values(), key=len, reverse=True)
    print(f"\n{len(ordered)} components: {[len(c) for c in ordered]}")
    cluster = set(ordered[want - 1])
    print(f"component #{want}: {len(cluster)} people")

    depth, size = descent(children, cluster)

    rows = []
    for g in cluster:
        if g in father or g in mother:
            continue                      # not a top — we already hold a parent
        rows.append({
            "geni_id": g,
            "name": name.get(g, ""),
            "born": born.get(g, ""),
            "generations_below": depth.get(g, 0),
            "descendants": size.get(g, 0),
            "geni_url": f"https://www.geni.com/people/x/{g}",
        })
    rows.sort(key=lambda r: (-r["generations_below"], -r["descendants"]))

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} people in the cluster have no parent recorded")
    deep = [r for r in rows if r["generations_below"] >= 5]
    print(f"{len(deep)} of them head a line 5+ generations deep\n")
    print(f"{'gens':>4} {'desc':>6}  {'born':>5}  name")
    for r in rows[:30]:
        print(f"{r['generations_below']:>4} {r['descendants']:>6}  {str(r['born']):>5}  "
              f"{r['name'][:40]:<40} {r['geni_id']}")
    print(f"\nwrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
