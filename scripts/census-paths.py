"""The path census, in the shape Emma asked for, repeatable so runs compare.

**Emma, 2026-08-18**, having been shown the wrong thing twice: *"My god that's not
the path census"*, then *"I wanted the histogram of lengths"*, then a screenshot of
the census she meant with *"This is what I wanted."*

So the format is hers and is not to be redesigned:

1. **Paths overall** --- how many files, how many fully covered, how many still
   incomplete, each with a percentage.
2. **Incomplete paths** --- and this is the part the first rewrite got wrong: every
   statistic here is over the **incomplete** paths only, not over all of them.
   Average full length, average missing, average already held, the resulting
   "the average incomplete path is N% complete", and the extremes.
3. **Missing-count distribution** --- one row per exact missing count, not bands,
   with the `<=3 -> save pages` threshold marked.
4. **Length histogram** --- banded, because 99 distinct lengths is not a histogram
   anyone can read.

**Averaging over all paths instead of the incomplete ones is the trap.** It mixes
the 148 completed paths in as zeros and makes both the length and the missing
figure meaningless: 43.9 steps and 7.0 missing over everything, against 38.9 and
8.9 over the incomplete ones. The completed paths are done; the question is what
is left.

Measured against `exports/` directly, so a run is about a minute rather than the
five a merge costs.

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
            "held": len(ids) - len(missing),
            "destination_missing": ids[-1] not in present,
            "isolate": path.name.startswith("isolate-geni-"),
        })

    total = len(rows)
    covered = [r for r in rows if r["missing"] == 0]
    inc = [r for r in rows if r["missing"] > 0]

    # Every figure below is over `inc`, the INCOMPLETE paths. See the module note.
    avg_len = statistics.fmean(r["steps"] for r in inc)
    med_len = statistics.median(r["steps"] for r in inc)
    avg_missing = statistics.fmean(r["missing"] for r in inc)
    med_missing = statistics.median(r["missing"] for r in inc)
    avg_held = statistics.fmean(r["held"] for r in inc)
    pct_complete = 100 * avg_held / avg_len
    longest = max(inc, key=lambda r: r["steps"])
    shortest = min(inc, key=lambda r: r["steps"])
    most = max(inc, key=lambda r: r["missing"])
    fewest = min(inc, key=lambda r: r["missing"])

    dist = collections.Counter(r["missing"] for r in inc)
    lengths = collections.Counter(r["steps"] for r in rows)
    band = collections.Counter()
    for r in rows:
        s = r["steps"]
        band["1-9" if s < 10 else "10-19" if s < 20 else "20-29" if s < 30 else
             "30-39" if s < 40 else "40-49" if s < 50 else "50-59" if s < 60 else
             "60-69" if s < 70 else "70-79" if s < 80 else "80+"] += 1

    isolates = [r for r in rows if r["isolate"]]
    iso_missing = [r for r in isolates if r["destination_missing"]]

    L = []
    L += [f"# Path census", "",
          f"Measured over **{len(files)} exports** holding "
          f"**{len(present):,}** distinct Geni profile IDs.", "",
          f"## Paths overall --- {total} files", "", "```",
          f"fully covered   {len(covered):>5}   ({100*len(covered)/total:.0f}%)",
          f"still incomplete{len(inc):>5}   ({100*len(inc)/total:.0f}%)", "```", "",
          "## Incomplete paths", "",
          "**Every figure here is over the incomplete paths only.** Averaging over "
          "all of them mixes the completed paths in as zeros and answers a question "
          "nobody asked.", "", "```",
          f"average full length   {avg_len:>6.1f} steps   (median {med_len:.0f})",
          f"average missing       {avg_missing:>6.1f}         (median {med_missing:.0f})",
          f"average already held  {avg_held:>6.1f}",
          f"-> the average incomplete path is {pct_complete:.0f}% complete",
          f"longest path          {longest['steps']:>6} steps   "
          f"shortest {shortest['steps']}",
          f"most missing          {most['missing']:>6}         "
          f"fewest {fewest['missing']}", "```", "",
          "## Missing-count distribution", "", "```"]
    for n in sorted(dist):
        tag = "   <= 3 -> save pages" if n <= 3 else ""
        L.append(f"{n:>3} missing : {dist[n]:>4} paths{tag}")
    L += ["```", "", "## Histogram of path lengths", "",
          "Length is fixed by the saved page --- an export never changes it. Only the "
          "missing-count distribution above moves.", "", "```"]
    widest = max(band.values())
    for b in ["1-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69",
              "70-79", "80+"]:
        n = band.get(b, 0)
        L.append(f"{b:>6} steps : {n:>4} paths  {'#' * round(40 * n / widest)}")
    L += ["```", "", "## Wikidata isolates", "",
          f"{len(isolates)} paths run to a Wikidata isolate; "
          f"**{len(iso_missing)}** of those destinations are still absent from the "
          f"corpus.", ""]
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L))

    print(f"{len(files)} exports, {len(present):,} distinct Geni IDs\n")
    print(f"Paths overall --- {total} files\n")
    print(f"  fully covered    {len(covered):>5}   ({100*len(covered)/total:.0f}%)")
    print(f"  still incomplete {len(inc):>5}   ({100*len(inc)/total:.0f}%)")
    print("\nIncomplete paths\n")
    print(f"  average full length   {avg_len:>6.1f} steps   (median {med_len:.0f})")
    print(f"  average missing       {avg_missing:>6.1f}         (median {med_missing:.0f})")
    print(f"  average already held  {avg_held:>6.1f}")
    print(f"  -> the average incomplete path is {pct_complete:.0f}% complete")
    print(f"  longest path          {longest['steps']:>6} steps   "
          f"shortest {shortest['steps']}")
    print(f"  most missing          {most['missing']:>6}         "
          f"fewest {fewest['missing']}")
    print("\nMissing-count distribution\n")
    for n in sorted(dist):
        tag = "   <= 3 -> save pages" if n <= 3 else ""
        print(f"  {n:>3} missing : {dist[n]:>4} paths{tag}")
    print("\nHistogram of path lengths\n")
    for b in ["1-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69",
              "70-79", "80+"]:
        n = band.get(b, 0)
        print(f"  {b:>6} steps : {n:>4} paths  {'#' * round(40 * n / widest)}")
    print(f"\nwrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
