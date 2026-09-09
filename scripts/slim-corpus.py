"""Write a slimmed copy of every export, carrying only what the editing pipeline reads.

**The tag rules live in `genimerge.slim`, not here.** This is the standalone
corpus-copier used for measuring; `genimerge merge --slim` applies the same sets at
stream time and is what the pipeline actually runs. Two copies of a whitelist is how
they drift.

    python scripts/slim-corpus.py -o /tmp/slim

**Emma, 2026-09-03:** *"realistically anything that doesn't go into the editing pipeline isn't
needed in the synoptic tree."* This is that rule applied to the merge's input.

**Why it exists: the merge does not fit in a runner, measured.** Run 33808839371 was killed at
15,921 MB with 67 MB free after seven minutes pinned at the ceiling. The cause is structural
rather than a leak -- `Merger.records` holds the whole tree as Python objects at once, because
merging is keyed on the xref and any of the 607 exports can add to any record, so nothing can be
released until the last file is read. A tree of small Python objects costs 20-40x its source text:
409 MB of GEDCOM against a 13.3-16 GB peak.

**So the lever is the input, and the input is ours.** Measured over all 111,206,168 corpus lines:

    CONT   31.8%  |
    CONC   20.7%  |  note and text bodies
    FILE    7.3%  |  media references
    NOTE    4.5%  |
    TEXT    1.5%  |  ~67% of corpus bytes

against ~6% for names and ~6% for relationships. **`Node` folds `CONC`/`CONT` into `value`**, so
that 53% is not node overhead -- it is raw string payload sitting in RAM inside records the merge
holds anyway.

**Nothing here touches `exports/`.** The corpus is written once and never edited
(`CLAUDE.md` § *Never overwrite an existing `.ged`*); this writes copies elsewhere and the merge
is pointed at those. Every `.ged` stays committed, complete, with its notes.

**Bio QIDs are NOT lost, and that was checked rather than assumed.**
`scripts/extract-bio-qids.py` reads `find_exports()` -- the raw corpus -- not the merged tree, so
her Wikidata links in Geni *About Me* survive untouched. None of the eight steps of
`rebuild-everything.py` reads `NOTE` either: the tag lists of `build-display-names.py`,
`derive-labels.py`, `derive-family.py` and `derive-facts.py` are the whitelist below.

**The whitelist is a WHITELIST on purpose.** A tag nobody named is dropped with its whole subtree,
so a Geni tag added next month is excluded until somebody adds it here -- loud by omission rather
than silently swelling the merge again. `CONT`/`CONC` are on it so an `ADDR` continuation survives;
they only ever appear under a kept parent, because a dropped node takes its children with it.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from genimerge.slim import KEEP_RECORDS, KEEP_TAGS, DROP_INSIDE  # noqa: E402
from genimerge.sources import find_exports  # noqa: E402





def slim(text: str) -> tuple[str, int, int]:
    """Return the slimmed GEDCOM plus (lines in, lines out)."""
    out = []
    skip_depth = None          # drop every line deeper than this
    in_record = False          # inside a kept INDI/FAM (not HEAD)
    kept = total = 0

    for line in text.splitlines():
        total += 1
        if not line.strip():
            continue
        head, _, rest = line.partition(" ")
        if not head.isdigit():
            continue
        level = int(head)

        if skip_depth is not None:
            if level > skip_depth:
                continue
            skip_depth = None

        parts = rest.split(" ", 2)
        tag = parts[1] if parts and parts[0].startswith("@") and len(parts) > 1 else (parts[0] if parts else "")

        if level == 0:
            in_record = tag in {"INDI", "FAM"}
            if tag not in KEEP_RECORDS:
                skip_depth = 0
                continue
        elif in_record and tag in DROP_INSIDE:
            skip_depth = level
            continue
        elif tag not in KEEP_TAGS:
            skip_depth = level
            continue

        out.append(line)
        kept += 1

    return "\n".join(out) + "\n", total, kept


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-o", "--out", required=True, help="directory for the slimmed copies")
    args = ap.parse_args()

    dest = pathlib.Path(args.out)
    dest.mkdir(parents=True, exist_ok=True)

    files = list(find_exports())
    print(f"slimming {len(files)} exports -> {dest}", flush=True)
    tot_in = tot_out = bytes_in = bytes_out = 0

    for i, path in enumerate(files, 1):
        text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
        slimmed, n_in, n_out = slim(text)
        target = dest / pathlib.Path(path).name
        # exports collide by style; disambiguate on the source path so none is lost
        if target.exists():
            target = dest / (pathlib.Path(path).parent.name + "__" + pathlib.Path(path).name)
        target.write_text(slimmed, encoding="utf-8")
        tot_in += n_in
        tot_out += n_out
        bytes_in += len(text)
        bytes_out += len(slimmed)
        if i % 100 == 0:
            print(f"  {i}/{len(files)}", flush=True)

    print()
    print(f"lines  {tot_in:,} -> {tot_out:,}  ({100*tot_out/tot_in:.1f}% kept)")
    print(f"bytes  {bytes_in/1048576:.0f} MB -> {bytes_out/1048576:.0f} MB "
          f"({100*bytes_out/bytes_in:.1f}% kept)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
