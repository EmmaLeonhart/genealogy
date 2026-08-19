"""The path census, repeatable so two runs can be compared.

**Emma, 2026-08-18:** *"I'm curious do you have a census repeat here? Or can you run
one? ... I want to see how much progress the algorithm change added."*

The algorithm change is hers: seed the export on an ANCESTOR OF THE DESTINATION rather
than on a midpoint or on whoever blocks the most paths. This measures the same
quantities the first census did, so the two are directly comparable:

* how many relationship paths there are, and how many are complete;
* the average length of a path and the average number of missing people on one;
* the distribution of missing-counts;
* how many Wikidata-isolate destinations are still absent from the corpus.

Every number is measured against `exports/` directly rather than against a merge, so a
run costs about a minute rather than five.

    PYTHONPATH=src python scripts/census-paths.py
"""

from __future__ import annotations

import collections
import io
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import sources

REPO = sources.REPO_ROOT
OUT = REPO / "reports" / "path-census.md"
INDI_XREF = re.compile(rb"^0 @I(\d+)@ INDI", re.M)


def main() -> int:
    files = sources.find_exports(REPO / "exports")
    present: set[str] = set()
    for path in files:
        present.update(m.group(1).decode()
                       for m in INDI_XREF.finditer(path.read_bytes()))

    rows = []
    for path in sorted((REPO / "paths").glob("*.tsv")):
        ids = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#") or line.startswith("step"):
                continue
            for tok in line.split("\t")[-1].split():
                if tok.startswith("geni:"):
                    ids.append(tok[5:])
        if not ids:
            continue
        missing = [g for g in ids if g not in present]
        rows.append({
            "path": path.name,
            "steps": len(ids),
            "missing": len(missing),
            "destination": ids[-1],
            "destination_missing": ids[-1] not in present,
            "isolate": path.name.startswith("isolate-geni-"),
        })

    total = len(rows)
    complete = [r for r in rows if r["missing"] == 0]
    incomplete = [r for r in rows if r["missing"] > 0]
    isolates = [r for r in rows if r["isolate"]]
    iso_dest_missing = [r for r in isolates if r["destination_missing"]]

    held = sum(r["steps"] - r["missing"] for r in rows)
    steps = sum(r["steps"] for r in rows)

    buckets = collections.Counter()
    for r in rows:
        m = r["missing"]
        buckets["0 (complete)" if m == 0 else
                "1-3 (save pages)" if m <= 3 else
                "4-9" if m <= 9 else
                "10-19" if m <= 19 else
                "20+"] += 1

    lines = [
        "# Path census",
        "",
        "Emma, 2026-08-18: *\"I want to see how much progress the algorithm change "
        "added.\"* The change is hers -- seed the export on an **ancestor of the "
        "destination person** rather than on a midpoint or on whoever blocks the most "
        "paths.",
        "",
        f"Measured over **{len(files)} exports** holding **{len(present):,}** distinct "
        f"Geni profile IDs.",
        "",
        "| | |",
        "| --- | ---: |",
        f"| relationship paths | {total} |",
        f"| complete (0 missing) | {len(complete)} |",
        f"| incomplete | {len(incomplete)} |",
        f"| average steps per path | {statistics.fmean(r['steps'] for r in rows):.1f} |",
        f"| average missing per path | {statistics.fmean(r['missing'] for r in rows):.1f} |",
        f"| average missing per INCOMPLETE path | "
        f"{statistics.fmean(r['missing'] for r in incomplete):.1f} |"
        if incomplete else "| average missing per incomplete path | n/a |",
        f"| steps held | {held:,} of {steps:,} ({100*held/steps:.1f}%) |",
        f"| destinations still missing | {sum(1 for r in rows if r['destination_missing'])} |",
        "",
        "## Missing people per path",
        "",
        "| band | paths |",
        "| --- | ---: |",
    ]
    for band in ["0 (complete)", "1-3 (save pages)", "4-9", "10-19", "20+"]:
        lines.append(f"| {band} | {buckets.get(band, 0)} |")

    # Histogram of path LENGTHS -- Emma asked for this by name, twice:
    # "How many paths are there of each length?" and "I wanted the histogram of
    # lengths". It is the shape of the corpus of paths, and it does not move when
    # exports land -- only the missing-count histogram does. Both are printed so the
    # pair can be read together.
    lengths = collections.Counter(r["steps"] for r in rows)
    lines += ["", "## Histogram of path lengths", "",
              "Path length is the number of steps Geni walked, and it is fixed by the "
              "saved page -- exports never change it. Compare it against the "
              "missing-count histogram above, which is what an export moves.",
              "", "| steps | paths | |", "| ---: | ---: | --- |"]
    widest = max(lengths.values())
    for n in sorted(lengths):
        bar = "#" * max(1, round(40 * lengths[n] / widest))
        lines.append(f"| {n} | {lengths[n]} | `{bar}` |")

    band = collections.Counter()
    for r in rows:
        s = r["steps"]
        band["1-9" if s < 10 else "10-19" if s < 20 else "20-29" if s < 30 else
             "30-39" if s < 40 else "40-49" if s < 50 else "50-59" if s < 60 else
             "60-69" if s < 70 else "70-79" if s < 80 else "80+"] += 1
    lines += ["", "### Banded", "", "| steps | paths |", "| --- | ---: |"]
    for b in ["1-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]:
        lines.append(f"| {b} | {band.get(b, 0)} |")

    lines += [
        "",
        "## Wikidata isolates",
        "",
        f"{len(isolates)} of the paths run to a Wikidata isolate. "
        f"**{len(iso_dest_missing)}** of those destinations are still absent from the "
        f"corpus; {len(isolates)-len(iso_dest_missing)} are held.",
        "",
    ]
    io.open(OUT, "w", encoding="utf-8").write("\n".join(lines))

    print(f"{len(files)} exports, {len(present):,} distinct Geni IDs\n")
    print(f"  paths                          {total}")
    print(f"  complete                       {len(complete)}")
    print(f"  incomplete                     {len(incomplete)}")
    print(f"  avg steps/path                 {statistics.fmean(r['steps'] for r in rows):.1f}")
    print(f"  avg missing/path               {statistics.fmean(r['missing'] for r in rows):.1f}")
    if incomplete:
        print(f"  avg missing/incomplete path    "
              f"{statistics.fmean(r['missing'] for r in incomplete):.1f}")
    print(f"  steps held                     {held:,}/{steps:,} ({100*held/steps:.1f}%)")
    print(f"  destinations missing           {sum(1 for r in rows if r['destination_missing'])}")
    print(f"  isolate destinations missing   {len(iso_dest_missing)} of {len(isolates)}")
    print("\n  path LENGTH histogram (steps -> paths)")
    widest2 = max(band.values())
    for b in ["1-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]:
        n = band.get(b, 0)
        print(f"    {b:>6}  {n:>4}  {'#' * max(0, round(40 * n / widest2))}")
    print("\n  MISSING-count histogram (missing -> paths)")
    widest3 = max(buckets.values())
    for b in ["0 (complete)", "1-3 (save pages)", "4-9", "10-19", "20+"]:
        n = buckets.get(b, 0)
        print(f"    {b:>16}  {n:>4}  {'#' * max(0, round(40 * n / widest3))}")
    print(f"\nwrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
