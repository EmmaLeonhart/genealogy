"""Show one path's remaining gap and its midpoint, for seeding the next export.

The workhorse of the closing campaign. Emma's procedure per qualifying path is
endpoint, then midpoint of what remains, then page-saving; this prints what is still
missing and names the midpoint so the next seed can be chosen without re-deriving it.

    PYTHONPATH=src python scripts/path-gap.py <path-file-or-fragment>

Measured against `exports/` directly rather than a merge, so it costs about a minute.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import sources

INDI_XREF = re.compile(rb"^0 @I(\d+)@ INDI", re.M)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    frag = sys.argv[1]
    paths = sorted((sources.REPO_ROOT / "paths").glob("*.tsv"))
    hits = [p for p in paths if frag.lower() in p.name.lower()]
    if not hits:
        print(f"no path file matching {frag!r}")
        return 1
    if len(hits) > 1:
        print(f"{len(hits)} matches:")
        for p in hits[:20]:
            print(f"  {p.name}")
        return 1
    target = hits[0]

    present: set[str] = set()
    for p in sources.find_exports(sources.REPO_ROOT / "exports"):
        present.update(m.group(1).decode() for m in INDI_XREF.finditer(p.read_bytes()))

    rows = []
    for line in target.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or line.startswith("step"):
            continue
        c = line.split("\t")
        gid = c[-1].split("geni:")[-1].strip()
        rows.append((c[0], c[1], c[2] if len(c) > 2 else "", gid, gid in present))

    missing = [r for r in rows if not r[4]]
    print(f"{target.name}")
    print(f"{len(rows)} steps, {len(missing)} missing\n")
    for s, n, rel, gid, ok in rows:
        if not ok:
            print(f"  {s:>3}  {n[:44]:<44} {rel[:16]:<16} {gid}")
    if missing:
        mid = missing[len(missing) // 2]
        print(f"\nMIDPOINT: step {mid[0]}  {mid[1]}  {mid[3]}")
        print(f"  https://www.geni.com/family-tree/index/{mid[3]}")
        dest = rows[-1]
        print(f"\nDESTINATION: {dest[1]}  {dest[3]}  "
              f"{'MISSING' if not dest[4] else 'held'}")
        print(f"  https://www.geni.com/family-tree/index/{dest[3]}")
    else:
        print("\nCOMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
