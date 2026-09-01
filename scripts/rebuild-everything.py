"""Rebuild the synoptic tree and everything derived from it, ending with the batch.

    python scripts/rebuild-everything.py

**Emma, 2026-08-29, and this script exists because she is right:** *"this explains why it's so
hard: because it's not one script it's a bunch of scripts that you need to remember to run in the
right order. Nope make it one script that always ends by calling the script that regenerates the
quickstatements."*

**The order is not arbitrary and getting it wrong fails SILENTLY**, which is the whole reason a
human should not be holding it in their head:

1. `genimerge merge` — `exports/**/*.ged` → `out/merged.ged`.
2. `build-display-names.py` — `merged.ged` → `display-names.csv`.
3. `derive-labels.py` — reads **`display-names.csv`**, not the merge. `CLAUDE.md` records the cost
   of missing this: correcting the exports and re-running the analysers left the old surname in
   place, because `derive-labels.py` does not build the file it reads.
4. `derive-family.py` and `derive-facts.py` — `merged.ged` → `derived-family.csv`,
   `derived-facts.csv`. **`derive-family.py` also reads `derived-labels.csv`**, which is why it
   now runs *after* step 3 rather than before it; see below.
5. The label chain — `relationship-label-preview.py` → `build-placeholder-label-batch.py` →
   `build-en-label-batch.py` → `build-mul-label-batch.py`. These consume `derived-family.csv`
   and `derived-labels.csv`, so they are downstream of the tree and belong here.
6. `pack-derived.py` — gzips the four CSVs that exceed GitHub's 100 MiB limit.
7. `build-garborg-day.py --compose` — the QuickStatements batch.

**Step 3 used to run fourth, after the two `derive-*` steps, and that was a real bug.**
`derive-family.py` line ~75 reads `reports/derived-labels.csv` to name the people it reports —
behind an `if LABELS.exists()` that silently contributes nothing when the file is absent. Running
it *before* the script that writes that file meant every rebuild fed it the **previous
generation's** labels, and on a first run fed it none at all. Nothing failed; the labels were
simply one merge out of date. That is the same shape as every other defect `CLAUDE.md` records
in this area — *a guard against a malformed case, paid for with real values that then vanish
without trace*.

**Step 5 exists because the chain rotted in exactly the way this script was written to prevent.**
Emma, 2026-09-01, on being shown it: *"Just that it was so stale lol."*
`reports/relationship-label-preview.csv` was dated **2026-08-19** against a tree rebuilt on
**08-31** — twelve days — and it is the sole source of the `relationship label` rows in the `en`
batch. Measured before the rebuild: it held 39,691 people, of whom only **9,996** were still
unlabelled, and it missed **52,526 of the 62,522** people who currently have no label at all.
Re-running it took the placeholder batch from 39,691 edits to **158,618**, and `en` labels from
32,129 to **137,528**. Being a step here is what stops that recurring.

**What it costs.** Step 1 is ~14 minutes and peaks near **17 GB**; it has been killed twice on this
machine when something else was running. This script runs the steps one at a time for that reason
and stops at the first failure rather than carrying on with stale inputs — a half-rebuilt chain is
what produced `P1810 "Private"` for a man Geni now calls `<private> Dokken`.

`--skip-merge` reuses an existing `out/merged.ged`, for when only the derived layer is stale.
"""
import argparse
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: `(label, argv)`, in dependency order. Anything added here must be added in the right place:
#: the ordering is the point of the script.
STEPS = [
    # **NO `-o`, and that is load-bearing.** `cli.py` sends the merge reports next to the
    # output file *whenever `--output` is given* -- deliberately, so a merge written elsewhere
    # cannot overwrite the workspace's description of a different merge. Its comment records
    # the cost: *"reports/merge.md spent twelve commits claiming 8766 people while
    # out/merged.ged held 12422."*
    #
    # The `-o out/merged.ged` here was redundant AND harmful: `Workspace.merged` already
    # resolves to exactly that path, so the flag changed nothing about where the GEDCOM went
    # and everything about where the reports went. Every run of this script left
    # `reports/merge.md` stale, which is what
    # `test_merge_real_exports.py::test_the_committed_merge_report_still_describes_these_exports`
    # was failing on in the 2026-08-31 slow lane.
    ("merge the corpus", [sys.executable, "-m", "genimerge", "merge"]),
    ("display names", [sys.executable, os.path.join("scripts", "build-display-names.py")]),
    # **Before `derive-family.py`, not after.** That script reads `derived-labels.csv` behind an
    # `if LABELS.exists()`, so running it first is silent and merely wrong: the names it reports
    # are one merge stale, and empty on a first run.
    ("derived labels", [sys.executable, os.path.join("scripts", "derive-labels.py")]),
    ("derived family", [sys.executable, os.path.join("scripts", "derive-family.py")]),
    ("derived facts", [sys.executable, os.path.join("scripts", "derive-facts.py")]),
    # The label chain. Every one of these reads a derived CSV and nothing else reruns them, which
    # is how the preview came to be twelve days older than the tree it describes.
    ("relationship label preview",
     [sys.executable, os.path.join("scripts", "build-relationship-label-preview.py")]),
    ("placeholder labels",
     [sys.executable, os.path.join("scripts", "build-placeholder-label-batch.py")]),
    ("en labels", [sys.executable, os.path.join("scripts", "build-en-label-batch.py")]),
    ("mul labels", [sys.executable, os.path.join("scripts", "build-mul-label-batch.py")]),
    ("pack the big CSVs", [sys.executable, os.path.join("scripts", "pack-derived.py")]),
    ("the QuickStatements batch",
     [sys.executable, os.path.join("scripts", "build-garborg-day.py"), "--compose"]),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--skip-merge", action="store_true",
                    help="reuse the existing out/merged.ged; only the derived layer is rebuilt.")
    args = ap.parse_args()

    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        [os.path.join(ROOT, "src"), os.path.join(ROOT, "scripts"), env.get("PYTHONPATH", "")])

    steps = STEPS[1:] if args.skip_merge else STEPS
    if args.skip_merge:
        merged = os.path.join(ROOT, "out", "merged.ged")
        if not os.path.exists(merged) or os.path.getsize(merged) == 0:
            print(f"REFUSING: --skip-merge but {merged} is missing or empty. "
                  f"A rebuild from an empty tree produces empty derived data that looks fine.")
            return 1

    started = time.time()
    for i, (label, argv) in enumerate(steps, 1):
        t0 = time.time()
        print(f"\n=== [{i}/{len(steps)}] {label} ===", flush=True)
        rc = subprocess.call(argv, cwd=ROOT, env=env)
        if rc != 0:
            print(f"\nFAILED at step {i}, {label} (exit {rc}). Stopping rather than "
                  f"running the rest against stale inputs.")
            return rc
        print(f"--- {label}: {time.time() - t0:.0f}s", flush=True)

    print(f"\nall {len(steps)} steps done in {(time.time() - started) / 60:.1f} min")
    print("batch is at reports/wikidata-garborg-day.qs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
