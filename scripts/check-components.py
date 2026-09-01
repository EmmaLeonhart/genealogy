"""Count connected components across the corpus, and say which one a person is in.

Answers "is this cluster still cut off?" without building the merged GEDCOM.
`python -m genimerge merge` writes a 409 MB file to answer the same question;
this streams the exports once and holds only a union-find, which is the whole
structure the question needs.

Edges are family membership: everyone named in a FAM record — HUSB, WIFE, CHIL —
is joined to everyone else in it. That is the same connectivity the merged tree
has, because the merge is an exact join on the profile id and adds no edges.

    py scripts/check-components.py [geni_id ...]
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import sources  # noqa: E402

WATCH = {
    "6000000227145774838": "wife of Baruch Jafe",
    "6000000227145420853": "wife of Samuel Standen",
    "6000000040078764766": "Baruch Jafe",
    "6000000107265740881": "Samuell Standen",
    "6000000001846508982": "Empress Jingū (the main tree)",
}


class DSU:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        root = x
        while self.parent.setdefault(root, root) != root:
            root = self.parent[root]
        while self.parent[x] != root:          # path compression
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def main() -> int:
    watch = dict(WATCH)
    for extra in sys.argv[1:]:
        watch.setdefault(extra, extra)

    dsu = DSU()
    indi = re.compile(r"^0 @I(\d+)@ INDI", re.M)
    fam_start = re.compile(r"^0 @F(\d+)@ FAM$")
    member = re.compile(r"^1 (?:HUSB|WIFE|CHIL) @I(\d+)@$")

    files = sources.find_exports()
    for n, path in enumerate(files, 1):
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        # every INDI is a component even if it is in no family
        for gid in indi.findall(text):
            dsu.find(gid)
        members: list[str] = []
        in_fam = False
        for line in text.split("\n"):
            line = line.rstrip("\r")
            if line.startswith("0 "):
                if in_fam and len(members) > 1:
                    for m in members[1:]:
                        dsu.union(members[0], m)
                members = []
                in_fam = bool(fam_start.match(line))
                continue
            if in_fam:
                m = member.match(line)
                if m:
                    members.append(m.group(1))
        if in_fam and len(members) > 1:
            for m in members[1:]:
                dsu.union(members[0], m)
        if n % 40 == 0:
            print(f"  {n}/{len(files)} exports", file=sys.stderr)

    sizes = Counter(dsu.find(p) for p in dsu.parent)
    print(f"\n{len(files)} exports, {len(dsu.parent)} people, "
          f"{len(sizes)} connected components")
    print("\nlargest components:")
    for root, size in sizes.most_common(8):
        print(f"  {size:>7} people   root {root}")

    print("\nwatched people:")
    for gid, label in watch.items():
        if gid not in dsu.parent:
            print(f"  {label:<32} {gid}  NOT IN CORPUS")
            continue
        root = dsu.find(gid)
        rank = [r for r, _ in sizes.most_common()].index(root) + 1
        print(f"  {label:<32} {gid}  component #{rank}, {sizes[root]} people")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
