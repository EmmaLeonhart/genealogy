"""The permalink batch `scripts/pathchains.js` walks, minus the chains already harvested.

Prints a `window.__chains.seed([...])` line to paste after the fetcher. Nothing is fetched
here; this is arithmetic over committed files.

    python scripts/build-chain-batch.py --count 2000 > batch.js
    python scripts/build-chain-batch.py --count 2000 --skip 2000

**The list is `reports/path-permalinks.tsv`** -- 47,692 saved path objects recovered from the
Takeout mbox by `scripts/parse-path-emails.py`. That file replaces the `/paths` walk, which
costs 28 minutes for thirty permalinks a page; these cost one mbox parse and no Geni traffic
at all.

⛔ **THE CURSOR IS `--skip` AND IT IS ONLY SOUND BECAUSE THE FILE IS SORTED.**
`parse-path-emails.merge` sorts on the hash -- a total order over a fixed-width hex key -- so
row N is row N on every run, and a new harvest INSERTS rather than appending. That is the
right trade: an insert shifts the cursor by at most the number of new rows, whereas an
append-ordered file would renumber nothing but could never be diffed. Re-walking a permalink
is a page load and a duplicate row, not a defect -- `merge-path-chains.py` dedupes -- so a
cursor that slips slightly is survivable. A cursor that cannot be reconstructed is not.

**What is differenced out.** Every `(to_id, kind)` already in `reports/path-chains-*.tsv` is a
chain we hold, so any permalink resolving to it is a wasted page load. ⛔ **But the permalink
does not say which `to_id` it resolves to** -- that is only known after the redirect, which is
the fetch this is trying to avoid. So the difference is applied on the way OUT, by
`merge-path-chains.py`, and what this can skip is only what a previous batch covered. The
`--skip` cursor is the whole mechanism, which is why the paragraph above is about it.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PERMALINKS = REPO / "reports" / "path-permalinks.tsv"


def rows():
    if not PERMALINKS.exists():
        sys.exit(f"{PERMALINKS.relative_to(REPO)} is missing -- run "
                 "scripts/parse-path-emails.py over a Takeout mbox first")
    with PERMALINKS.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def covered_names() -> dict:
    """`{final-segment name: how many held chains end on it}`.

    A chain's LAST segment is the person the path was found to, and
    `reports/path-permalinks.tsv` carries that same person as `subject_name` -- so the two
    join on the name without fetching anything. Rows with step `-1` are the `EMPTY` marker
    and carry no person, so they are skipped.
    """
    last: dict = {}
    for path in sorted((REPO / "reports").glob("path-chains-*.tsv")):
        try:
            with path.open(encoding="utf-8", newline="") as fh:
                for row in csv.DictReader(fh, delimiter="\t"):
                    try:
                        step = int(row.get("step", ""))
                    except (TypeError, ValueError):
                        continue
                    if step < 0:
                        continue
                    key = (row.get("to_id", ""), row.get("kind", ""))
                    if key not in last or step > last[key][0]:
                        last[key] = (step, row.get("name", ""))
        except OSError:
            continue
    freq: dict = {}
    for _, name in last.values():
        if name:
            freq[name] = freq.get(name, 0) + 1
    return freq


def held_chains() -> set:
    """`{(to_id, kind)}` already on disk, for the count line only.

    Not a filter -- see the module docstring. It is printed so the operator can see whether a
    batch is likely to be mostly new, which is the question `--skip` is being set against.
    """
    held = set()
    for path in sorted((REPO / "reports").glob("path-chains-*.tsv")):
        try:
            with path.open(encoding="utf-8", newline="") as fh:
                for row in csv.DictReader(fh, delimiter="\t"):
                    held.add((row.get("to_id", ""), row.get("kind", "")))
        except OSError:
            continue
    return held


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--count", type=int, default=2000,
                    help="how many permalinks to emit (default 2000)")
    ap.add_argument("--skip", type=int, default=0,
                    help="how many to pass over first -- the cursor")
    ap.add_argument("--skip-covered", action="store_true",
                    help="drop permalinks whose subject_name already ends a held chain. "
                         "⛔ ONLY when that name is held by EXACTLY ONE chain -- see the note "
                         "on ambiguous names in the source.")
    ap.add_argument("--kind", choices=("blood", "inlaw", "both"), default="both",
                    help="⛔ BOTH by default. CLAUDE.md § BOTH TIES, ALWAYS: a blood chain AND "
                         "a marriage chain, and the redundancy is the point.")
    args = ap.parse_args()

    all_rows = rows()
    if args.kind != "both":
        all_rows = [r for r in all_rows if r.get("kind") == args.kind]

    dropped = 0
    if args.skip_covered:
        # ⛔ **THE UNIQUENESS TEST IS THE WHOLE SAFETY OF THIS.** Measured 2026-09-20: 20,856
        # unwalked permalinks name-match a held chain, but only **13,031** match a name held by
        # exactly one chain. The other 7,825 match an ambiguous one, and the ambiguity is not
        # spread evenly -- it is concentrated in placeholders, `NN` on 21 chains, `N.N.` on 10,
        # `<private> Schottenstein` on 7. Skipping on a bare name match would throw away a real
        # person because an unrelated `NN` is already held, which is § *PARSE PATRONYMICS BY
        # FORM* in another costume: a name is not an identifier.
        freq = covered_names()
        keep = [r for r in all_rows if freq.get(r.get("subject_name", ""), 0) != 1]
        dropped = len(all_rows) - len(keep)
        all_rows = keep
    batch = [r["url"] for r in all_rows[args.skip:args.skip + args.count]]

    held = held_chains()
    blood = sum(1 for r in all_rows if r.get("kind") == "blood")
    print("// %d permalinks%s, %d blood and %d in-law; %d (to_id, kind) chains already on disk"
          % (len(all_rows),
             (" after dropping %d already covered" % dropped) if dropped else " held",
             blood, len(all_rows) - blood, len(held)))
    print("// this batch: %d, starting at offset %d, %d left after it"
          % (len(batch), args.skip, max(0, len(all_rows) - args.skip - len(batch))))
    print("// next:  python scripts/build-chain-batch.py --count %d --skip %d"
          % (args.count, args.skip + len(batch)))
    print("window.__chains.seed(" + repr(batch).replace("'", '"') + ");")
    return 0


if __name__ == "__main__":
    sys.exit(main())
