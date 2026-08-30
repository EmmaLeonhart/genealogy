"""One command for a day, in her order: individuals, then names, then relationships.

    python scripts/build-daily-batch.py [--refresh-ledger] [--seed N]

**Emma, 2026-08-26** — `docs/dictation/2026-08-26-daily-algorithm.md`:
*"Creation of individuals comes first, then creation of names, then the relationships between
the individuals. The reason why I'm specifically telling you, pretty rigidly, to go in this
order is that the order itself is structurally rigid… You need an individual to exist for their
name object to be linked to them."*

This is an **orchestrator**, not a fourth generator. It runs the two builders that already
exist, in her order, and prints the run order with the position of each file — because the
order is the part that is easy to get wrong by hand and impossible to see from the files
themselves.

## The three sections and where each one lives

| # | section | file |
| --- | --- | --- |
| 1 | **individuals** — 4 random parent pairs + 1 ancestral pair shuffled among them, 4 spouse-and-children fills, 5 couples with their entire children | `reports/wikidata-garborg-day.qs`, first section |
| 2 | **names** — 10 name items, each linked to every bearer who already holds a QID | `reports/wikidata-garborg-name-items.qs` |
| 3 | **relationships** — 10 `P3373` *sibling* pairs, every other relationship uncapped | `reports/wikidata-garborg-day.qs`, second section |

**Sections 1 and 3 share a file and that is deliberate.** `queue.md`: *"There is exactly ONE
live batch file"*, because two files creating the same people is how somebody runs both and
duplicates everybody. `build-garborg-day.py` concatenates its own two sections in her order at
write time, so the file reads 1 then 3; the names file is run between them.

**Section 2 has no dependency on section 1 and is still ordered after it.** A name item links
only to people who already held a QID *before* this run — a person created today gets their
name statements tomorrow, because `LAST` names the name item and the new person's QID is not
known. Her order is the general rule, not a per-day dependency graph, and following it is what
keeps the general rule true.

## Step 0 — the ledger, then the diff against the ideal state

`docs/daily-algorithm.md` § *Step 0* is two halves and only the first was ever run here:

1. **Check her Wikidata profile for everything she has edited**, and add it to the ledger.
2. **Take those out, and check what remains against the ideal state.**

`--refresh-ledger` runs `scripts/refresh-garborg-ledger.py` first: *"Check my wiki data profile
for all the things that I've edited. Grab the things that I've been editing and add them to a
thing."* It is **off by default** because it is the one network call in the day and needs
`BOT_CONTACT`; a run without it uses `reports/garborg-qids.tsv` as it stands and says how old
that is, because a stale ledger is what made a batch try to re-create 21 people she had just
made.

**Step 0c is the second half** — `scripts/model-vs-reality.py`, which builds what each item
*should* hold and diffs it against what the item does hold. Its `missing` column is the
emittable set; its `CONFLICT` column is a modelling rule that is wrong, repeated across people
rather than N separate errors. It runs **before** the three generators because that is what
makes it a check on the day rather than a post-mortem of it, and it **emits nothing** — the
generators are unchanged and do not read it.

Freshness is the reason it is bound to the same flag as the ledger. Without `--refetch` the
cached `out/model-vs-reality-items.json` is used, and a snapshot older than the ledger reports
its own gap as `ITEM NOT FETCHED` — 587 of 657 people on 2026-08-30, because the ledger grew
from 71 items while the snapshot sat still. A diff over 71 people is not a diff over the day.

## One file, and the spine variant is one flag away

`--compose` is the daily algorithm and it **overwrites** `reports/wikidata-garborg-day.qs`,
which is also where the one-off *whole spine in one batch* lands. That is not a collision to fix
by adding a second file: `queue.md` records that *"there is exactly ONE live batch file and that
is deliberate"*, because two files creating the same people is how somebody runs both and
duplicates everybody. Measured rather than assumed — the two share **2 of their creations**, so
they genuinely cannot coexist.

The spine variant is:

    python scripts/build-garborg-day.py --roster out/roster-spine.txt \n        --roster-is-frontier --known reports/spine-already-on-wikidata.tsv

Writes nothing itself. Emits no batch of its own.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "reports" / "garborg-qids.tsv"

#: The order is the whole point of this file. `(position, what, script, args, output)`.
STEPS = (
    (1, "individuals", "build-garborg-day.py", ["--compose"],
     "reports/wikidata-garborg-day.qs"),
    (2, "names", "build-garborg-name-items.py", [],
     "reports/wikidata-garborg-name-items.qs"),
    (3, "relationships", None, [],
     "reports/wikidata-garborg-day.qs"),
)


def run(script, args):
    cmd = [sys.executable, str(ROOT / "scripts" / script), *args]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    if proc.returncode:
        print(proc.stdout[-2000:])
        print(proc.stderr[-2000:], file=sys.stderr)
        sys.exit(f"{script} failed with exit code {proc.returncode}")
    return proc.stdout


def diff_summary(out):
    """The headline of a `model-vs-reality.py` run: freshness, the four totals, and the
    properties that actually move.

    Its full output tabulates every property any ledger item carries -- 90-odd rows, most of
    them a single `extra` from Emma's hand-work, which is the column this project never
    touches. What belongs in a summary whose job is to make the ORDER legible is `missing`
    (the emittable set) and `CONFLICT` (one modelling rule that is wrong, repeated).
    """
    keep, in_table = [], False
    for line in out.splitlines():
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("   property"):
            in_table = True
            keep.append(line)
            continue
        if in_table:
            cols = line.split()
            if len(cols) == 4 and cols[1] == "0" and cols[3] == "0":
                continue
            if line.startswith("   "):
                keep.append(line)
                continue
            in_table = False
        first = line.lstrip().split(" ", 1)[0].replace(",", "")
        if (line.startswith(("using the cached snapshot", "fetching full items", "wrote"))
                or "differences over" in line or first.isdigit()):
            keep.append(line if line.startswith(" ") else "        " + line)
    return "\n".join(keep)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh-ledger", action="store_true",
                    help="step 0: rebuild reports/garborg-qids.tsv from her Wikidata "
                         "contributions first. Needs BOT_CONTACT and is the day's one "
                         "network call.")
    ap.add_argument("--seed", default="", metavar="N",
                    help="passed to the individuals step so a day is reproducible.")
    args = ap.parse_args()

    if args.refresh_ledger:
        print("STEP 0a ledger <- Special:Contributions/日巫女")
        print(run("refresh-garborg-ledger.py", []).strip()[-600:])
        # **Both halves of "what is on Wikidata now", together.** The ledger says WHO has an
        # item; the live values say WHAT each item already states. Refreshing one and not the
        # other is how the batch came to be three-quarters duplicates: `garborg-live-state.tsv`
        # sat frozen at 2026-08-24 while the ledger was rebuilt daily.
        print("\nSTEP 0b live values <- full_entities over the ledger")
        print(run("refresh-live-values.py", []).strip()[-300:])
    else:
        age = (time.time() - LEDGER.stat().st_mtime) / 3600 if LEDGER.exists() else None
        values = ROOT / "reports" / "garborg-live-values.tsv"
        vage = ((time.time() - values.stat().st_mtime) / 3600
                if values.exists() else None)
        print(f"        reports/garborg-live-values.tsv is "
              f"{'MISSING' if vage is None else f'{vage:.1f} hours old'} -- it is what stops "
              f"the batch restating what an item already holds, and 229 of 306 statements "
              f"were duplicates before it existed.")
        print(f"STEP 0  SKIPPED. reports/garborg-qids.tsv is "
              f"{'missing' if age is None else f'{age:.1f} hours old'} -- pass "
              f"--refresh-ledger to rebuild it from her contributions. A stale ledger is "
              f"what made a batch try to re-create 21 people she had just made.")

    # **Step 0's second half**, `docs/daily-algorithm.md`: read her contributions, take those
    # out, then check what remains against the ideal state. It runs BEFORE the three
    # generators, because a diff read afterwards is a post-mortem of the day rather than a
    # check on it. It emits nothing and the generators do not read it.
    print(f"\nSTEP 0c diff vs the ideal state  (model-vs-reality.py"
          f"{' --refetch' if args.refresh_ledger else ''})")
    print(diff_summary(run("model-vs-reality.py",
                           ["--refetch"] if args.refresh_ledger else [])))

    for pos, what, script, extra, output in STEPS:
        if script is None:
            print(f"\nSTEP {pos}  {what}: written by step 1 into {output}, as its second "
                  f"section. Nothing to run.")
            continue
        cmd_args = list(extra) + (["--seed", args.seed] if args.seed and script ==
                                  "build-garborg-day.py" else [])
        print(f"\nSTEP {pos}  {what}  ({script} {' '.join(cmd_args)})")
        out = run(script, cmd_args)
        # Only the headline lines. The name step prints every token it proposes and the
        # individuals step prints its component tally; both belong in their own run, not
        # in a summary whose job is to make the ORDER legible.
        for line in out.splitlines():
            if line.startswith("wrote") or line.lstrip()[:2] in ("1.", "2.", "3.", "4."):
                print(f"        {line.strip()}")

    print("\nRUN THEM IN THIS ORDER. It is the spec, not a convenience:")
    for pos, what, _s, _a, output in STEPS:
        note = " (second section of the same file)" if pos == 3 else ""
        print(f"   {pos}. {what:<14} {output}{note}")
    print("\n   Individuals before names because a person must exist for a name item to be\n"
          "   linked to them; names before relationships for the same reason one step on.\n"
          "   Two items created in the SAME run cannot point at each other -- that is the\n"
          "   one real limit, and everything above is arranged around it.")


if __name__ == "__main__":
    main()
