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
3. `derive-family.py` and `derive-facts.py` — `merged.ged` → `derived-family.csv`,
   `derived-facts.csv`.
4. `derive-labels.py` — reads **`display-names.csv`**, not the merge. `CLAUDE.md` records the cost
   of missing this: correcting the exports and re-running the analysers left the old surname in
   place, because `derive-labels.py` does not build the file it reads.
5. `pack-derived.py` — gzips the four CSVs that exceed GitHub's 100 MiB limit.
6. `build-garborg-day.py --compose` — the QuickStatements batch.

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
    ("merge the corpus", [sys.executable, "-m", "genimerge", "merge",
                          "-o", os.path.join("out", "merged.ged")]),
    ("display names", [sys.executable, os.path.join("scripts", "build-display-names.py")]),
    ("derived family", [sys.executable, os.path.join("scripts", "derive-family.py")]),
    ("derived facts", [sys.executable, os.path.join("scripts", "derive-facts.py")]),
    ("derived labels", [sys.executable, os.path.join("scripts", "derive-labels.py")]),
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
