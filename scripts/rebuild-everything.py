"""Rebuild the synoptic tree — the GENI UNION, every `.ged` under `exports/` merged — and
everything derived from it, ending with the batch.

    python scripts/rebuild-everything.py

**This script exists because the rebuild was a set of scripts that had to be run in the right
remembered order.** It is now one script, and it always ends by calling the script that
regenerates the QuickStatements.

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
5. `build-cjk-romanisation.py` — reads the three derived CSVs, and its output feeds both the
   preview and the `en` batch below. Added 2026-09-01 for the same reason as the chain in
   step 6: it was not a step, so it aged against the tree.
6. The label chain — `relationship-label-preview.py` → `build-placeholder-label-batch.py` →
   `build-en-label-batch.py` → `build-mul-label-batch.py`. These consume `derived-family.csv`
   and `derived-labels.csv`, so they are downstream of the tree and belong here.
7. `apply-pipe-labels.py` — reads the ruled `|` into `reports/title-label-proposals.tsv`, whose
   resolved rows `build-garborg-day.py` emits. Before the batch, and after nothing in particular.
8. `pack-derived.py` — gzips the four CSVs that exceed GitHub's 100 MiB limit.
9. `build-garborg-day.py --compose` — the QuickStatements batch.

**Step 3 used to run fourth, after the two `derive-*` steps, and that was a real bug.**
`derive-family.py` line ~75 reads `reports/derived-labels.csv` to name the people it reports —
behind an `if LABELS.exists()` that silently contributes nothing when the file is absent. Running
it *before* the script that writes that file meant every rebuild fed it the **previous
generation's** labels, and on a first run fed it none at all. Nothing failed; the labels were
simply one merge out of date. That is the same shape as every other defect `CLAUDE.md` records
in this area — *a guard against a malformed case, paid for with real values that then vanish
without trace*.

**Step 5 exists because the chain rotted in exactly the way this script was written to prevent.**
`reports/relationship-label-preview.csv` had gone badly stale: it was dated **2026-08-19** against a tree rebuilt on
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
    # `--slim` is appended by `main()` when asked for. It drops what the editing pipeline never
    # reads: measured 2026-09-03, peak RSS 13.30 GB and KILLED without it against 8.79 GB in
    # 7.7 min with it, for the same 1,451,993 people and 630,053 families. It is what lets this
    # script run on a GitHub runner at all -- see `genimerge.slim`.
    # **BEFORE the merge, because the merge consumes what it writes.** The long-term shape for
    # the manual parental zipper correspondences is that the pipeline generates them into a
    # gitignored GEDCOM that is part of the synoptic tree merge, with QIDs in bios as a
    # fundamental part of the pipeline.
    #
    # It is generated IN ADDITION: `build-garborg-day.ledger()` still reads
    # `reports/manual-identifications.csv` directly, so the pipeline cannot break. The direct
    # read goes only once the tree route is shown to carry the same pairs.
    ("the manual correspondences as a GEDCOM",
     [sys.executable, os.path.join("scripts", "build-correspondence-gedcom.py")]),
    ("merge the corpus", [sys.executable, "-m", "genimerge", "merge",
                          "--also", os.path.join("out", "manual-parental-correspondences.ged")]),
    # **The four family maps, so the scheduled pipeline can run without the GEDCOM.**
    # `build-garborg-day.read_tree` needs them and `out/merged.ged` is 409 MB and
    # gitignored, so a runner can never have it. Written once here, gzipped by
    # `pack-derived.py`, read as a fallback when the merge is absent -- and verified
    # byte-identical to reading the GEDCOM on 2026-09-01.
    ("family structure",
     [sys.executable, os.path.join("scripts", "build-family-structure.py")]),
    ("display names", [sys.executable, os.path.join("scripts", "build-display-names.py")]),
    # **Before `derive-family.py`, not after.** That script reads `derived-labels.csv` behind an
    # `if LABELS.exists()`, so running it first is silent and merely wrong: the names it reports
    # are one merge stale, and empty on a first run.
    ("derived labels", [sys.executable, os.path.join("scripts", "derive-labels.py")]),
    ("derived family", [sys.executable, os.path.join("scripts", "derive-family.py")]),
    ("derived facts", [sys.executable, os.path.join("scripts", "derive-facts.py")]),
    # **The CJK romanisation, and it is the same trap again.** `build-cjk-romanisation.py` reads
    # `derived-labels.csv`, `derived-facts.csv` and `derived-family.csv`, and its output is read
    # by BOTH `build-relationship-label-preview.py` and `build-en-label-batch.py` -- two steps
    # below. It was not a step itself, so it aged against the tree exactly as the preview did.
    # Found 2026-09-01 while fixing the culture classifier: the same shape, the same day.
    ("cjk romanisation",
     [sys.executable, os.path.join("scripts", "build-cjk-romanisation.py")]),
    # The label chain. Every one of these reads a derived CSV and nothing else reruns them, which
    # is how the preview came to be twelve days older than the tree it describes.
    ("relationship label preview",
     [sys.executable, os.path.join("scripts", "build-relationship-label-preview.py")]),
    # ⛔ **AGREEING LATIN LABELS -> `mul`, AND NOTHING RAN IT UNTIL NOW.** Ruled 2026-09-09 as
    # *"the most important labelling thing here"*, and it was written, committed and then called
    # by nothing: not this file, not a workflow, not the batch builder, and nothing read its
    # output either. `CLAUDE.md` § *Code that is WRITTEN but never CALLED is not done*.
    #
    # Where an item has no `mul` and several of its own Latin-alphabet labels agree, that string
    # is the language-neutral label. Measured over the ledger: 1,001 items carry no `mul` and
    # **397 gain one** from labels already on the item -- `Q102010` agrees across ten languages,
    # two items across eighty-four.
    #
    # It reads the Wikidata store, so it must follow `wikidata-index`; it touches no derived CSV,
    # so it has no ordering constraint against the label chain around it.
    ("agreeing latin labels",
     [sys.executable, os.path.join("scripts", "build-agreeing-latin-labels.py")]),
    ("placeholder labels",
     [sys.executable, os.path.join("scripts", "build-placeholder-label-batch.py")]),
    ("en labels", [sys.executable, os.path.join("scripts", "build-en-label-batch.py")]),
    ("mul labels", [sys.executable, os.path.join("scripts", "build-mul-label-batch.py")]),
    # ⛔ **THE `|` READING, AND IT IS THE AGREEING-LATIN SHAPE ALL OVER AGAIN.** `pipelabels.py`
    # was written and tested on 2026-09-09 -- 24 tests, every ruled situation of
    # `name modelling.txt` § *A PIPE IN AN IMPORTED LABEL* -- and then called by nothing.
    # `CLAUDE.md` § *Code that is WRITTEN but never CALLED is not done*.
    #
    # It rewrites `reports/title-label-proposals.tsv` in place: 200 of the 201 rows held for
    # the pipe resolve, and `Q99707312` stays held on an unclosed bracket. `build-garborg-day.py`
    # reads the resolved rows in `_piped_label_fixes`, so this must run BEFORE the batch.
    #
    # It touches no derived CSV and reads no store, so it has no other ordering constraint. It
    # is idempotent -- it reads `live_mul`/`leading_title`, never its own `proposed_label`.
    ("the piped labels",
     [sys.executable, os.path.join("scripts", "apply-pipe-labels.py")]),
    ("pack the big CSVs", [sys.executable, os.path.join("scripts", "pack-derived.py")]),
    ("the QuickStatements batch",
     [sys.executable, os.path.join("scripts", "build-garborg-day.py"), "--compose"]),
    # **The adjudication deck, AFTER the batch.** The HTML is regenerated every time the
    # pipeline runs. It reads the derived CSVs plus
    # `reports/emma-judgments.tsv`, so it must follow the derived layer; it goes after the batch
    # so a deck rendered here describes the same state the batch was built from.
    #
    # It was reachable only through `refresh-drift.py` picking it up by chance, which is why
    # `out/parent-review.html` rendered **0 cards** on 2026-09-01 while 709 candidates sat in
    # `reports/parent-candidates.tsv` -- and 207 of them were answered off the raw TSV instead.
    #
    # It makes ~15 batched Wikidata requests for the candidates' sex and dates. The ruling, asked
    # directly: run it in both this and the scheduled pipeline, and carry the whole deck with no
    # cap -- a cap is what hid the work the first time.
    ("the adjudication deck",
     [sys.executable, os.path.join("scripts", "build-parent-candidates.py")]),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slim", action="store_true",
                    help="merge only what the editing pipeline reads: 8.79 GB peak instead of 13.30 GB and killed. Required on a GitHub runner.")
    ap.add_argument("--skip-merge", action="store_true",
                    help="reuse the existing out/merged.ged; only the derived layer is rebuilt.")
    args = ap.parse_args()

    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        [os.path.join(ROOT, "src"), os.path.join(ROOT, "scripts"), env.get("PYTHONPATH", "")])

    # **`--skip-merge` drops the merge AND the step that feeds it**, by label rather than by
    # index. It was `STEPS[1:]`, which silently meant *drop whatever happens to be first* — and
    # the moment the correspondence generator went in front of the merge, that slice dropped the
    # generator and ran the merge against a file it had not written.
    SKIPPED_BY_SKIP_MERGE = {"merge the corpus", "the manual correspondences as a GEDCOM"}
    steps = ([s for s in STEPS if s[0] not in SKIPPED_BY_SKIP_MERGE]
             if args.skip_merge else STEPS)
    if args.slim and not args.skip_merge:
        steps = [(label, argv + ["--slim"]) if label == "merge the corpus" else (label, argv)
                 for label, argv in steps]
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
    print("batch is at reports/wikidata-garborg-day.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
