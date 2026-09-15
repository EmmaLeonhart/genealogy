"""The id list `scripts/pathrun.js` requests, minus everyone already harvested.

Prints a `R.ids = [...]` line to paste under the RUN block. Nothing is fetched here; this is
arithmetic over files already on disk.

⛔ **THIS EXISTS BECAUSE THE TARGET LIST WAS AS UNSAVED AS THE RUNNER.** On 2026-09-14 both
lived only in a browser tab, and when the tab was lost at 20:33 there was no record of which
chunk the requester had reached — no cursor, no progress file, nothing. The list had to be
rebuilt from the chunk files and differenced against the harvest index. Doing that by hand once
is the reason it is a script now.

The sources, in order of authority:

* `<scratchpad>/path-chunks/chunk-NNNN.txt` — the requester's target lists, 133 files,
  **264,221 distinct ids**. These are the isolates, and they match the campaign's own figure of
  266,201 disconnected `P2600` holders closely enough to be the same population.
* `reports/geni-paths-harvest.tsv` — every path already found. 5,912 ids appear in it.

Difference: **261,084 still to request** as of 2026-09-14 21:40.

**Re-requesting somebody is not harmful**, which is what makes a lost cursor survivable: Geni
queues the search and an already-answered one costs a 202 and nothing else. The harvest
difference is an optimisation, not a correctness requirement.

    python scripts/build-pathrun-batch.py --count 800 > batch.js
"""

from __future__ import annotations

import argparse
import glob
import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARVEST = REPO / "reports" / "geni-paths-harvest.tsv"

#: Where the chunk files live. The scratchpad is session-scoped, so this is passed in when it
#: is not the default — another thing the 2026-09-14 loss made obvious.
DEFAULT_CHUNKS = Path(os.environ.get("PATH_CHUNKS", "")) if os.environ.get("PATH_CHUNKS") else None

ID = re.compile(r"\d{10,}")


def chunk_ids(chunk_dir: Path) -> list[str]:
    """Every distinct id the chunk files name, in file then line order."""
    out, seen = [], set()
    for path in sorted(glob.glob(str(chunk_dir / "chunk-*.txt"))):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                for gid in ID.findall(line):
                    if gid not in seen:
                        seen.add(gid)
                        out.append(gid)
    return out


def harvested() -> set:
    """Every id named anywhere in the harvest index — `from`, `to` and the permalink alike.

    Deliberately loose: over-matching only skips a person who would have cost a cheap 202, while
    under-matching re-requests somebody. The asymmetry favours the loose read.
    """
    if not HARVEST.exists():
        return set()
    with HARVEST.open(encoding="utf-8") as fh:
        return {gid for line in fh for gid in ID.findall(line)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS,
                    help="directory holding chunk-NNNN.txt")
    ap.add_argument("--count", type=int, default=800, help="how many ids to emit")
    ap.add_argument("--skip", type=int, default=0, help="how many to pass over first")
    args = ap.parse_args()

    if not args.chunks or not args.chunks.is_dir():
        raise SystemExit("pass --chunks <dir> (or set PATH_CHUNKS): the chunk files are in the "
                         "session scratchpad, which moves between sessions")

    every = chunk_ids(args.chunks)
    done = harvested()
    todo = [gid for gid in every if gid not in done]

    batch = todo[args.skip:args.skip + args.count]
    print("// %d ids across the chunks, %d already harvested, %d to go"
          % (len(every), len(done), len(todo)))
    print("// this batch: %d, starting at offset %d" % (len(batch), args.skip))
    print("R.ids = " + repr(batch).replace("'", '"') + ";")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
