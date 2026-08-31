"""Which missing RELATIONSHIP blocks the most relationship paths?

    python scripts/rank-broken-links.py

**This is the successor to the bridge-people ranking in `queue.md` § THE AGENDA**, whose numbers
are from 2026-08-15 and no longer describe anything. That ranking asked *which absent PERSON
blocks the most paths* — 8,650 bridge people, 511 of them missing and on more than one path. The
answer today is **none of them**: `exports/0-scraped/scraped-paths.ged` and `scraped-pages.ged`
were built from these paths and ingested, so every path member is present by construction.

**What is missing now is not people, it is edges.** A consecutive pair on a path can have no
relationship between them in our tree, so the question that used to be *who do we lack* is now
*which link do we lack*, and this ranks exactly that. Measured with sibling steps and
concatenated files both handled: **87 of 977 paths, 9%**.

**Rank by paths blocked, never by how many links a path is missing.** That is the rule
`CLAUDE.md` states for `connectors` and it survives the change of unit: one edge blocking eleven
paths is worth more than eleven edges private to one. A path is unblocked only when every one of
its steps is carried, so a path with several breaks is counted against each of them.

**Two definitions are reused from `census-paths`, never restated, and both were got wrong
first.** `connected` knows a sibling step is carried through the shared parent; `path_segments`
knows one file can hold two paths end to end. Written out here independently, the first scored
all 2,126 sibling steps broken and the second scored 277 seams as breaks.

Writes `reports/broken-links.tsv` and `reports/broken-links.md`.
"""
from __future__ import annotations

import collections
import csv
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

_spec = importlib.util.spec_from_file_location(
    "census_paths", ROOT / "scripts" / "census-paths.py")
_census = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_census)

PATHS = ROOT / "paths"
LABELS = ROOT / "reports" / "derived-labels.csv"
OUT_TSV = ROOT / "reports" / "broken-links.tsv"
OUT_MD = ROOT / "reports" / "broken-links.md"

GENI = re.compile(r"geni:(\d+)")


def main():
    print("loading the tree ...", flush=True)
    adj, parents = _census.load_adjacency()
    print(f"{len(adj):,} people with a relationship", flush=True)

    files = sorted(PATHS.glob("*.tsv"))
    blocked = collections.defaultdict(set)
    broken_paths = set()
    total_paths = 0
    for path in files:
        rows_in = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#") or line.startswith("step"):
                continue
            cells = line.split("\t")
            found = GENI.findall(line)
            if found:
                rows_in.append((cells[2] if len(cells) > 2 else "", found[-1]))
        # One FILE is not one path: 278 of 699 hold two end to end. See `path_segments`.
        for n, seg in enumerate(_census.path_segments(rows_in)):
            total_paths += 1
            name = f"{path.name}#{n + 1}"
            for a, b in zip(seg, seg[1:]):
                if not _census.connected(a, b, adj, parents):
                    blocked[(a, b)].add(name)
                    broken_paths.add(name)

    print(f"{len(files)} files -> {total_paths} paths, "
          f"{len(broken_paths)} with at least one break")
    print(f"{len(blocked):,} distinct missing links", flush=True)

    label = {}
    wanted = {x for pair in blocked for x in pair}
    with LABELS.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["geni_id"] in wanted:
                label[row["geni_id"]] = (row.get("label_en") or row.get("label_mul") or "")

    rows = []
    for (a, b), where in blocked.items():
        rows.append({
            "paths_blocked": len(where),
            "from_geni": a,
            "from_name": label.get(a, ""),
            "to_geni": b,
            "to_name": label.get(b, ""),
            "example_path": sorted(where)[0],
        })
    rows.sort(key=lambda r: (-r["paths_blocked"], r["from_geni"]))

    # **Zero broken links is a RESULT, not an error.** `list(rows[0])` raised `IndexError` the
    # first time every path connected -- after the `ex-` fix put the former-partner families into
    # `exports/0-scraped/scraped-paths.ged` -- and it raised *inside* the open-for-write, so it
    # truncated `broken-links.tsv` on the way out and destroyed the list it was replacing. A
    # script that crashes on success and takes its own previous output with it is worse than one
    # that reports nothing.
    FIELDS = ["paths_blocked", "from_geni", "from_name", "to_geni", "to_name", "example_path"]
    with OUT_TSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    # How much of the breakage sits in the top of the ranking? That is what says whether
    # working this list is worth anything -- a flat distribution would mean it is not.
    cover, seen = [], set()
    for r in rows:
        seen |= blocked[(r["from_geni"], r["to_geni"])]
        cover.append(len(seen))

    with OUT_MD.open("w", encoding="utf-8") as fh:
        fh.write("# The links that block the paths\n\n")
        fh.write("**`queue.md` § THE AGENDA asked which absent PERSON blocks the most paths.** "
                 "That question no longer has an answer: every path member is present, because "
                 "`exports/0-scraped/scraped-paths.ged` and `scraped-pages.ged` were built from "
                 "these paths and ingested. What is missing is **edges**.\n\n")
        fh.write(f"- **{len(broken_paths)} of {total_paths} paths** hold a step the "
                 "tree does not carry.\n")
        fh.write(f"- **{len(rows):,} distinct missing links** cause it.\n")
        for n in (10, 50, 200):
            if len(cover) >= n:
                fh.write(f"- The top **{n}** links unblock **{cover[n - 1]}** paths between "
                         f"them.\n")
        fh.write("\n**A sibling step is carried through the shared parent** and is not counted "
                 "as a break — `census-paths.connected` is the definition, reused here. Scored "
                 "without it, all 2,126 sibling steps read as broken and the headline nearly "
                 "doubles.\n\n")
        fh.write("| paths blocked | from | to |\n| ---: | --- | --- |\n")
        for r in rows[:40]:
            fh.write(f"| {r['paths_blocked']} | {r['from_name'] or r['from_geni']} "
                     f"| {r['to_name'] or r['to_geni']} |\n")

    print(f"top link blocks {rows[0]['paths_blocked']} paths" if rows
          else "no broken links -- every step of every path is carried by the tree")
    print(f"wrote {OUT_TSV.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
