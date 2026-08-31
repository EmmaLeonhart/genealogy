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
import csv
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


#: The account owner. Every Geni relationship path is measured from her profile, so a second
#: appearance of it inside one file is a second path rather than a step.
ACCOUNT_OWNER = "6000000087535357291"


def path_segments(rows):
    """Split one path FILE into the paths it actually holds.

    **278 of 699 files hold two relationship paths end to end**, and nothing was splitting them.
    `CLAUDE.md` records the shape for `paths/nn-basse.tsv` -- *"holds two relationship paths end
    to end, so its second chain re-walks steps 1-9"* -- but the general case was never handled,
    and the step numbers do NOT reset (they run 1..78 straight through), so the obvious detector
    finds nothing.

    **What it cost, and it is the third instrument error in this area in one day.** The seam
    joins the end of one path to the start of the next, which is always the account owner, and
    that pair is not a relationship. Counting it as a step scored 277 false breaks:

        667 of 695 files disconnected   -- sibling steps also miscounted
        344 of 699 files disconnected   -- siblings fixed, seams still counted
         87 of 977 PATHS disconnected   -- both fixed

    Nine per cent, not ninety-six. Each error was a definition that quietly excluded or invented
    a case, with a plausible number surviving at every stage -- `CLAUDE.md` § *Our side could
    never have two children*.

    **Two boundary signals, unioned, because neither is complete.** A start row carries `-` in
    the relation column, and a start row is the account owner; they agree on 684 of the 699
    files, and the disagreements are files missing one signal or the other. `rows` is a list of
    `(relation, geni_id)`.
    """
    out, cur = [], []
    for i, (relation, gid) in enumerate(rows):
        starts = i > 0 and ((relation or "").strip() == "-" or gid == ACCOUNT_OWNER)
        if starts and cur:
            out.append(cur)
            cur = [gid]
        else:
            cur.append(gid)
    if cur:
        out.append(cur)
    return [seg for seg in out if len(seg) > 1]


def load_adjacency():
    """Every father/mother/spouse/child edge in the merged tree, both directions.

    Cells are separated by ` | `, spaces included -- `CLAUDE.md` § *Our side could never have
    two children* is what splitting on the wrong thing costs here.
    """
    adj = collections.defaultdict(set)
    parents = {}
    with open(REPO / "reports" / "derived-family.csv", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            me = row["geni_id"]
            parents[me] = {x.strip() for col in ("father", "mother")
                           for x in (row.get(col) or "").split("|") if x.strip()}
            for col in ("father", "mother", "spouses", "children"):
                for other in (x.strip() for x in (row.get(col) or "").split("|")):
                    if other:
                        adj[me].add(other)
                        adj[other].add(me)
    return adj, parents


def connected(a, b, adj, parents):
    """Is a path's step from `a` to `b` carried by the tree?

    **A SIBLING step is connected and is not a direct edge.** Emma raised it, 2026-08-30:
    *"geni chains often have situations where they skip between siblings. How are the parents
    represented and how common is this situation?"* -- and it is common: **2,126 of the 30,361
    relation steps in `paths/`, 7.0%**, read `his brother`, `her sister` and so on.

    Geni records no sibling edge. Two siblings are joined through a shared parent, so they are
    two hops apart in `derived-family.csv` while being one step apart on the path. Counting only
    parent/child/spouse edges therefore scores every sibling step as broken.

    **It cost a published number.** The first run of this census reported *667 of 695 paths do
    not connect*; with sibling steps read correctly it is **344 of 699**. Nearly half the
    breakage was the instrument. `CLAUDE.md` § *Our side could never have two children* is the
    standing lesson and this is another instance of it -- a plausible figure measured with a
    definition that quietly excluded a whole relationship type.
    """
    if b in adj.get(a, ()):
        return True
    return bool(parents.get(a, ()) & parents.get(b, ()))


def main() -> int:
    files = sources.find_exports(REPO / "exports")
    present: set[str] = set()
    for path in files:
        present.update(m.group(1).decode()
                       for m in INDI_XREF.finditer(path.read_bytes()))

    adjacency, parents = load_adjacency()
    rows = []
    for path in sorted((REPO / "paths").glob("*.tsv")):
        rows_in = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#") or line.startswith("step"):
                continue
            cells = line.split("\t")
            gid = ""
            for cell in cells:
                for tok in cell.split():
                    if tok.startswith("geni:"):
                        gid = tok[5:]
            if gid:
                rows_in.append((cells[2] if len(cells) > 2 else "", gid))
        if not rows_in:
            continue
        ids = [g for _r, g in rows_in]
        segs = path_segments(rows_in)
        missing = [g for g in ids if g not in present]
        # **Presence is no longer the binding measure and must not be read as one.**
        # Measured 2026-08-30: all 699 paths report 0 missing people, because
        # `exports/0-scraped/scraped-paths.ged` (11,481 people) and `scraped-pages.ged`
        # (10,179) were ingested and those files are built FROM these paths. Every path
        # member is present by construction.
        #
        # **They are present WITHOUT THEIR LINKS.** A path can be 100% present and still not
        # connect anybody, which is the whole deliverable: `CLAUDE.md` records that the point
        # is *"the chain being connected"*, not that the people exist as records. Measured
        # with sibling steps read correctly (see `connected`): **344 of 699 paths** hold a
        # step the tree does not carry.
        #
        # `broken` is that measure: consecutive steps with no father/mother/spouse/child edge
        # between them in `derived-family.csv`. A path is complete when `broken` is 0, and
        # that is what the routing in `queue.md` § *THE TAIL ALGORITHM* must be applied to.
        # Scored per SEGMENT, so the seam between two concatenated paths is never a step.
        broken = sum(1 for seg in segs for a, b in zip(seg, seg[1:])
                     if not connected(a, b, adjacency, parents))
        rows.append({
            "path": path.name,
            "steps": len(ids),
            "paths_in_file": len(segs),
            "missing": len(missing),
            "held": len(ids) - len(missing),
            "broken": broken,
            "destination_missing": ids[-1] not in present,
            "isolate": path.name.startswith("isolate-geni-"),
        })

    total = len(rows)
    # Complete means CONNECTED, not merely populated. See the note where `broken` is built.
    covered = [r for r in rows if r["broken"] == 0]
    inc = [r for r in rows if r["broken"] > 0]
    present_but_broken = [r for r in rows if r["missing"] == 0 and r["broken"] > 0]
    if not inc:
        print("every path is connected end to end.")
        return 0
    print(f"{len(present_but_broken)} paths hold every person and still do not connect --"
          f" presence saturated, links did not")

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
