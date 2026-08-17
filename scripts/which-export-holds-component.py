"""Name the export file each small component came from, off the corpus.

`scripts/check-components.py` counts components and answers "which one is this
person in?". This answers the other half: for every component that is not the
largest, which `.ged` under `exports/` actually holds those people. A separate
component exists because some export reached somewhere nothing else did, so the
file that seeded it is the file to open.

Reads `exports/` directly rather than `out/merged.ged` -- the merged tree is 409 MB,
takes minutes and 4.5 GB to load, and adds no edges the exports do not already
carry (the merge is an exact join on the profile id). Same reasoning as
`scripts/find-chain-gaps.py`.

    py scripts/which-export-holds-component.py [--write out/small-components.tsv]
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import sources  # noqa: E402

INDI = re.compile(r"^0 @I(\d+)@ INDI", re.M)
FAM_START = re.compile(r"^0 @F(\d+)@ FAM$")
MEMBER = re.compile(r"^1 (?:HUSB|WIFE|CHIL) @I(\d+)@$")
NAME = re.compile(r"^1 NAME (.*)$")


class DSU:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        root = x
        while self.parent.setdefault(root, root) != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def union_families(text: str, dsu: DSU) -> None:
    for gid in INDI.findall(text):
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
            in_fam = bool(FAM_START.match(line))
            continue
        if in_fam:
            m = MEMBER.match(line)
            if m:
                members.append(m.group(1))
    if in_fam and len(members) > 1:
        for m in members[1:]:
            dsu.union(members[0], m)


def main() -> int:
    files = [Path(p) for p in sources.find_exports()]
    texts: dict[Path, str] = {}
    dsu = DSU()
    for n, path in enumerate(files, 1):
        text = path.read_text(encoding="utf-8", errors="replace")
        texts[path] = text
        union_families(text, dsu)
        if n % 40 == 0:
            print(f"  {n}/{len(files)} exports", file=sys.stderr)

    sizes = Counter(dsu.find(p) for p in dsu.parent)
    largest, _ = sizes.most_common(1)[0]
    print(f"\n{len(files)} exports, {len(dsu.parent)} people, {len(sizes)} components")

    small_roots = [r for r, _ in sizes.most_common() if r != largest]
    if not small_roots:
        print("no component but the largest -- the corpus is one connected tree")
        return 0

    members: dict[str, set[str]] = defaultdict(set)
    for gid in dsu.parent:
        root = dsu.find(gid)
        if root != largest:
            members[root].add(gid)

    rows: list[str] = []
    for root in small_roots:
        ids = members[root]
        print(f"\n=== component of {len(ids)} people (root {root}) ===")
        holders: Counter = Counter()
        for path, text in texts.items():
            present = set(INDI.findall(text)) & ids
            if present:
                holders[path] = len(present)
        for path, count in holders.most_common():
            share = 100.0 * count / len(ids)
            print(f"  {count:>6} of {len(ids)} ({share:5.1f}%)  {path.relative_to(REPO)}")
            rows.append(f"{len(ids)}\t{root}\t{count}\t{path.relative_to(REPO)}")
        # a couple of names so the component is recognisable
        shown = 0
        for path, _ in holders.most_common(1):
            for block in texts[path].split("\n0 ")[1:]:
                head = block.split("\n", 1)[0]
                if not head.endswith(" INDI"):
                    continue
                gid = head.split("@I", 1)[-1].split("@", 1)[0]
                if gid not in ids:
                    continue
                for line in block.split("\n"):
                    m = NAME.match(line)
                    if m:
                        print(f"      {gid}  {m.group(1)}")
                        shown += 1
                        break
                if shown >= 8:
                    break

    if "--write" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--write") + 1])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            "component_size\troot\tpeople_in_file\tfile\n" + "\n".join(rows) + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
