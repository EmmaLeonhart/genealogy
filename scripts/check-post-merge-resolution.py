"""Which stale duplicates has `exports/post-merge/` actually resolved? All 29, not just 13.

    python scripts/check-post-merge-resolution.py

**Emma's design, 2026-08-24.** Geni has merged people our corpus still holds twice. Rather
than throw away the earlier exports — they carry thousands of people the merge needs — a fresh
export goes into `exports/post-merge/`, where **a Geni record overwrites the same Geni ID from
any other export**, because post-merge is newest and therefore right. Her stopping rule is not
a count of exports: *"export until every first-degree relative of every merged individual is
present"*.

## What resolution looks like

Geni holds ONE person where our older exports hold two. So a post-merge ball that reaches the
pair should contain the **survivor** and not the **stale twin**:

| survivor | twin | reading |
| --- | --- | --- |
| present | absent | **resolved** — our snapshot now matches Geni |
| present | present | the ball reached them before the merge propagated, or the twin is a real second person |
| absent | either | the ball never reached them; nothing is said |

**A twin that is still present is not necessarily wrong.** `CLAUDE.md` § *The question is
whether OUR TREE MATCHES GENI*: if Geni holds two, we should hold two. This report says what
our snapshot holds, never who is right.

## Why this exists rather than the number already in `queue.md`

That number — *"survivor present, twin absent, on 12 of the 13"* — was measured against **one**
export, `export-Forest-6000000227413001839.ged`, on the day it landed. There are **seven** files
in `exports/post-merge/` now, including two seeded on Aaron III's own survivor, and the 16
`medium` and `weak` rows were never measured at all. Re-running the measurement over the whole
directory is cheaper than an export and was the thing actually outstanding.

Writes `reports/post-merge-resolution.tsv` — one row per duplicate pair, every evidence grade.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
PAIRS = ROOT / "reports" / "geni-stale-duplicates.tsv"
POST_MERGE = ROOT / "exports" / "post-merge"
OUT = ROOT / "reports" / "post-merge-resolution.tsv"

#: Geni writes the profile id as the GEDCOM xref. `CLAUDE.md`: the xref is the merge key.
XREF = re.compile(rb"^0 @I(\d+)@ INDI", re.M)


def ids_in(path):
    """Every INDI xref in one GEDCOM, read as bytes -- these files are 14 MB each."""
    return set(XREF.findall(path.read_bytes()))


def main():
    if not POST_MERGE.is_dir():
        sys.exit(f"{POST_MERGE} does not exist")
    files = sorted(POST_MERGE.glob("*.ged"))
    print(f"{len(files)} exports in {POST_MERGE.name}/")

    per_file, everywhere = {}, set()
    for path in files:
        got = ids_in(path)
        per_file[path.name] = got
        everywhere |= got
        print(f"   {len(got):>6,}  {path.name}")
    print(f"{len(everywhere):,} distinct people across the directory")

    rows = list(csv.DictReader(open(PAIRS, encoding="utf-8"), delimiter="\t"))
    # An empty join is indistinguishable from an absence of data, and this whole report is
    # a set of absences. So: assert the ids on both sides are the same shape before
    # believing any "absent" below.
    survivors = {r["merged_survivor"].encode() for r in rows}
    sample = survivors & everywhere
    # One survivor may carry SEVERAL stale twins, so rows outnumber survivors and the two
    # counts must not be compared as if they were the same thing: 29 rows against 27
    # survivors is `6000000227350557852` Yorimoto Tanba, who has three.
    print(f"{len(rows)} pairs over {len(survivors)} distinct survivors "
          f"(a survivor may have several twins); {len(sample)} of those survivors are "
          f"somewhere in post-merge/, so an 'absent' below means absent")
    if not sample:
        sys.exit("NO survivor id matched any export: the join is broken, not the data")

    out, tally = [], collections.Counter()
    for r in rows:
        surv, twin = r["merged_survivor"].encode(), r["stale_twin"].encode()
        # Resolution is judged per FILE, not over the union: one ball holding the survivor
        # and another holding the twin is not a ball that resolved anything. The directory
        # resolves a pair when some single export reached the survivor without the twin.
        resolving = [n for n, got in per_file.items() if surv in got and twin not in got]
        both = [n for n, got in per_file.items() if surv in got and twin in got]
        if resolving:
            verdict = "resolved"
        elif both:
            verdict = "both still present"
        elif any(twin in got for got in per_file.values()):
            verdict = "only the twin reached"
        else:
            verdict = "not reached"
        tally[(r["evidence"], verdict)] += 1
        out.append({
            "evidence": r["evidence"], "name": r["name"],
            "merged_survivor": r["merged_survivor"], "stale_twin": r["stale_twin"],
            "verdict": verdict,
            "resolved_by": ";".join(resolving),
            "both_present_in": ";".join(both),
        })

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter="\t")
        w.writeheader()
        w.writerows(out)

    print(f"\n{'evidence':<9}{'verdict':<22}{'n':>4}")
    for (ev, v), n in sorted(tally.items()):
        print(f"{ev:<9}{v:<22}{n:>4}")
    unresolved = [r for r in out if r["verdict"] != "resolved"]
    print(f"\n{len(out) - len(unresolved)} of {len(out)} resolved. Still open:")
    for r in unresolved:
        print(f"   [{r['evidence']:<6}] {r['name'][:44]:<44} {r['verdict']}")
    print(f"\nwrote {OUT.resolve().relative_to(ROOT)}")


if __name__ == "__main__":
    main()
