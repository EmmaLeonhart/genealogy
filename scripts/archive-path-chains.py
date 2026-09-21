"""Bring the harvested path-chain files into the repo, and top up the aggregate.

The relationship-path campaign wrote `path-chains-NNN.tsv` into `~/Downloads` and nothing
carried them into the repo. On 2026-09-21, 372 files holding 26,203 people were found there,
**5,860 of them absent from `reports/path-chains.tsv`**, the aggregate forty scripts read.

Ruled the same day, after the Geni moratorium: keep BOTH forms -- the raw files as harvested,
and the aggregate brought up to date -- so the originals survive and nothing that reads the
aggregate has to change.

⛔ **`... (1).tsv` IS NOT A RE-DOWNLOAD HERE, AND SIZE MUST NOT PICK A WINNER.** This is the
one place `archive-sweep.py`'s rule is actively wrong. The runner restarts its own numbering, so
`path-chains-067.tsv` and `path-chains-067 (1).tsv` are DIFFERENT captures: measured at 63 and
82 people with **one** person in common. 69 such pairs exist. Taking the larger would have
dropped thousands of people, so every file is copied under its own exact name, parentheses and
all.

⛔ The Downloads copies are LEFT ALONE, and the aggregate is only ever APPENDED to: a person
already in it is never re-emitted, so re-running this changes nothing.
"""

from __future__ import annotations

import glob
import os
import shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(REPO, "reports", "path-chains")
AGG = os.path.join(REPO, "reports", "path-chains.tsv")


def to_ids(path):
    """Every to_id in a chain file, in order, read as bytes for exactness."""
    with open(path, "rb") as fh:
        fh.readline()
        for line in fh:
            if line.strip():
                yield line.split(b"\t")[0], line


def main() -> int:
    files = sorted(glob.glob(os.path.expanduser("~/Downloads/path-chains*.tsv")))
    if not files:
        print("no path-chain files in Downloads")
        return 0

    os.makedirs(RAW, exist_ok=True)
    copied = 0
    for src in files:
        dest = os.path.join(RAW, os.path.basename(src))
        if os.path.exists(dest) and os.path.getsize(dest) == os.path.getsize(src):
            continue
        shutil.copyfile(src, dest)
        copied += 1

    have = set()
    if os.path.exists(AGG):
        with open(AGG, "rb") as fh:
            fh.readline()
            for line in fh:
                if line.strip():
                    have.add(line.split(b"\t")[0])

    emitted, rows, people = set(), 0, 0
    with open(AGG, "ab") as out:
        for src in files:
            for tid, line in to_ids(src):
                if tid in have:
                    continue
                if tid not in emitted:
                    emitted.add(tid)
                    people += 1
                out.write(line if line.endswith(b"\n") else line + b"\n")
                rows += 1

    print("copied %d raw files into reports/path-chains/; appended %d rows for %d people "
          "to reports/path-chains.tsv" % (copied, rows, people))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
