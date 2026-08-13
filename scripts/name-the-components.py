"""Name the disconnected components in the merged tree.

The merge prints component sizes (e.g. 322748 + 4088 + 4084 + 33) but not who
is in the small ones. This loads the built merged GEDCOM, computes connected
components, and for every component that is not the largest prints its size, a
few sample members (name + birth year), and which export each sample came from
-- which is how you see the seed the floating ball grew from.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

from genimerge import frontier, gedcom, model, sources

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
MERGED = REPO / "out" / "merged.ged"
INDI_XREF = re.compile(r"^0 @I(\d+)@ INDI", re.MULTILINE)


def which_exports(ids: set[str]) -> Counter:
    """For a set of geni ids, count which exports contain each -> which file dominates."""
    hits: Counter = Counter()
    for path in sources.find_exports():
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        present = set(INDI_XREF.findall(text)) & ids
        if present:
            hits[Path(path).name] += len(present)
    return hits


def main() -> None:
    print(f"loading {MERGED.name} ...")
    records = list(gedcom.parse_file(str(MERGED)).records)
    tree = model.build_tree(records)
    comps = frontier.components(tree)
    print(f"{len(comps)} components, sizes: {[c.size for c in comps]}\n")

    for i, comp in enumerate(comps):
        if i == 0:
            print(f"component 0 (the main tree): {comp.size} people -- skipped\n")
            continue
        print(f"=== component {i}: {comp.size} people ===")
        members = comp.members
        # sample: a few with the earliest and latest birth years, plus a few any
        people = [tree.people[m] for m in members if m in tree.people]
        dated = sorted(
            (p for p in people if p.birth_year is not None),
            key=lambda p: p.birth_year,
        )
        sample = (dated[:4] + dated[-4:]) if dated else people[:6]
        seen = set()
        for p in sample:
            if p.geni_id in seen:
                continue
            seen.add(p.geni_id)
            yr = p.birth_year if p.birth_year is not None else "?"
            print(f"  {p.display_name:<40} b.{yr:<6} {p.geni_id}")
        # which export(s) this ball came from
        top = which_exports(set(members)).most_common(3)
        print("  source exports (by members contained):")
        for name, n in top:
            print(f"    {n:>5}  {name}")
        print()


if __name__ == "__main__":
    main()
