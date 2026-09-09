"""Which paths to export for next, longest-first, per Emma's tail algorithm.

**Emma, 2026-08-18:** *"you should be trying to target it by going from the longest
paths to the smallest paths… we can very easily run it with the top five longest paths
having their exports done and then we rebuild and so on and so on."*

Her algorithm in full:

* a gap of **<=3 missing people** is NOT an export. Save each path member's Geni page
  into `geni-scraping/` instead --- *"It is not worth six minutes to fill in something
  on the flat tail that is just covering one or two individuals."*
* a gap of **>=4** is an export, and it is seeded **on an ancestor of the DESTINATION
  person**, not on a midpoint --- *"When I say run on the individual, it means you
  create an ancestor of the individual and then you export from that ancestor."*
* if the destination-seeded export does not close it, attempt the **midpoint** of what
  remains, and recurse until the gap is <=3.

So the ranking is one row per path, sorted by how many of its steps are missing from the
corpus. `destination_missing` is the discriminating column: the destination is the last
row of the path, and Emma's method needs an ancestor of a person we do not hold, which
is exactly the case this campaign is working.

    PYTHONPATH=src python scripts/rank-destination-targets.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import sources

REPO = sources.REPO_ROOT
PATHS_DIR = REPO / "paths"
EXPORTS = REPO / "exports"
OUT = REPO / "reports" / "destination-targets.csv"

INDI_XREF = re.compile(rb"^0 @I(\d+)@ INDI", re.M)


def corpus_ids() -> set[str]:
    files = sources.find_exports(EXPORTS)
    present: set[str] = set()
    for path in files:
        present.update(m.group(1).decode()
                       for m in INDI_XREF.finditer(path.read_bytes()))
    print(f"{len(files)} corpus exports, {len(present):,} distinct Geni IDs")
    return present


def rows_of(path: Path) -> list[tuple[str, str, str]]:
    """(step, name, geni_id) for every walked row that carries an ID."""
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or line.startswith("step"):
            continue
        cells = line.split("\t")
        if len(cells) < 2:
            continue
        gid = ""
        for token in cells[-1].split():
            if token.startswith("geni:"):
                gid = token[5:]
        if gid:
            out.append((cells[0], cells[1], gid))
    return out


def main() -> int:
    present = corpus_ids()
    rows = []
    for path in sorted(PATHS_DIR.glob("*.tsv")):
        steps = rows_of(path)
        if not steps:
            continue
        missing = [s for s in steps if s[2] not in present]
        dest = steps[-1]
        rows.append({
            "missing": len(missing),
            "steps": len(steps),
            "destination": dest[1],
            "destination_geni_id": dest[2],
            "destination_missing": int(dest[2] not in present),
            "action": ("export" if len(missing) >= 4
                       else ("save-pages" if missing else "complete")),
            "path": path.name,
            "first_missing": missing[0][1] if missing else "",
            "first_missing_geni_id": missing[0][2] if missing else "",
        })

    rows.sort(key=lambda r: (-r["missing"], r["path"]))
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    exp = [r for r in rows if r["action"] == "export"]
    sav = [r for r in rows if r["action"] == "save-pages"]
    print(f"\n{len(rows)} paths: {len(exp)} export (>=4 missing), "
          f"{len(sav)} save-pages (1-3 missing), "
          f"{len(rows)-len(exp)-len(sav)} already complete")
    print(f"{sum(1 for r in exp if r['destination_missing'])} of the export rows "
          f"still lack the destination person\n")
    print(f"{'miss':>4} {'steps':>5}  destination")
    for r in exp[:20]:
        flag = "*" if r["destination_missing"] else " "
        print(f"{r['missing']:>4} {r['steps']:>5} {flag} {r['destination'][:44]:<44} "
              f"{r['destination_geni_id']}")
    print(f"\nwrote {OUT.relative_to(REPO)}  (* = destination itself missing)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
