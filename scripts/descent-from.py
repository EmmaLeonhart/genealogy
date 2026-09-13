"""Everyone in the corpus who descends from a given person, walked offline.

Ruled 2026-09-10: *"for descendants of Abul Hamza, imo focus on descendants of
`6000000006101354745` [Alix de Lampron] ... the people I actually want are going to be descended
from this individual."* — together with *"Do not try to run a descendants export on them
yourself. Please don't do that."*

⛔ **SO THIS RUNS NO EXPORT AND TOUCHES GENI NOT AT ALL.** It reads `.ged` files already on disk
and walks `FAM` links downward. The question *who descends from her* is answerable from the
corpus, and an export is a different operation that was explicitly refused.

    python scripts/descent-from.py <geni id> [exports/subdir ...]
    python scripts/descent-from.py --roots <id>,<id>,... [exports/subdir ...]

The `--roots` form reads the corpus ONCE and walks each root against it. The corpus read is the
whole cost of a single-root run, so asking about six roots one at a time costs six times what it
has to; the generation histogram is the only property that has been shown to separate a root
worth sweeping from one that is not, and it is wanted for several roots at a time.

The walk is `HUSB`/`WIFE` -> `FAM` -> `CHIL`, breadth-first, recording the generation at which
each person is first reached. A person reachable by two routes keeps the SHORTEST, because the
generation number is used to read how far down the descent a person sits and the shortest is the
one that answers that.
"""

from __future__ import annotations

import collections
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDI = re.compile(r"^0 @I(\d+)@ INDI")
FAM = re.compile(r"^0 @F(\d+)@ FAM")
LINK = re.compile(r"^1 (HUSB|WIFE|CHIL) @I(\d+)@")
NAME = re.compile(r"^1 NAME (.+)")


def read(paths):
    """`(name_by_id, families)` where a family is `(partners, children)`."""
    names, fams = {}, []
    for path in paths:
        cur_indi = cur_fam = None
        partners, children = [], []
        with path.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = INDI.match(line)
                if m:
                    if cur_fam is not None:
                        fams.append((partners, children))
                        partners, children = [], []
                    cur_indi, cur_fam = m.group(1), None
                    continue
                m = FAM.match(line)
                if m:
                    if cur_fam is not None:
                        fams.append((partners, children))
                    cur_indi, cur_fam = None, m.group(1)
                    partners, children = [], []
                    continue
                if cur_indi:
                    m = NAME.match(line)
                    if m:
                        names.setdefault(cur_indi, m.group(1).replace("/", "").strip())
                    continue
                if cur_fam:
                    m = LINK.match(line)
                    if m:
                        (children if m.group(1) == "CHIL" else partners).append(m.group(2))
        if cur_fam is not None:
            fams.append((partners, children))
    return names, fams


def descent(children_of, root_id):
    """`{geni_id: generation}` for everyone below `root_id`, shortest generation kept."""
    gen = {root_id: 0}
    queue = collections.deque([root_id])
    while queue:
        cur = queue.popleft()
        for kid in children_of.get(cur, ()):
            if kid not in gen:
                gen[kid] = gen[cur] + 1
                queue.append(kid)
    return gen


def report(names, children_of, root_id):
    gen = descent(children_of, root_id)
    out = ROOT / "reports" / ("descent-from-%s.csv" % root_id)
    rows = sorted(((g, k) for k, g in gen.items() if k != root_id))
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geni_id", "generation", "name"])
        for g, k in rows:
            w.writerow([k, g, names.get(k, "")])

    print()
    print("root: %s  %s" % (root_id, names.get(root_id, "(not in these files)")))
    print("descendants found: %d" % len(rows))
    by_gen = collections.Counter(g for g, _ in rows)
    for g in sorted(by_gen):
        print("  generation %-2d %5d" % (g, by_gen[g]))
    print("-> %s" % out.relative_to(ROOT))


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[1:]
    if argv and argv[0] == "--roots":
        root_ids = [x for x in argv[1].replace(",", " ").split() if x]
        subdirs = argv[2:] or ["exports"]
    else:
        root_ids = [argv[0]]
        subdirs = argv[1:] or ["exports"]
    paths = sorted({p for d in subdirs for p in (ROOT / d).rglob("*.ged")})
    print("reading %d files ..." % len(paths), flush=True)
    names, fams = read(paths)
    print("people %d, families %d" % (len(names), len(fams)), flush=True)

    children_of = collections.defaultdict(set)
    for partners, children in fams:
        for p in partners:
            for c in children:
                children_of[p].add(c)

    for root_id in root_ids:
        report(names, children_of, root_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
