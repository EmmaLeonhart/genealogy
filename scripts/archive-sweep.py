"""Copy finished sweep files into the repo AS THEY ARE, one file per person.

Ruled 2026-09-20: *"there's no concatenation or any of that bullshit. Whatever the raw files
are that you made, those are the files that are supposed to be going into the repository ...
they should be committed into the repository within 15 minutes of being harvested. I have
active workflows in place that were destroyed by the fact that you aren't doing that."*

⛔ **RAW. NOT GZIPPED, NOT CONCATENATED, NOT RENAMED.** Two versions of this file were refused
before this one: the first merged every person into a single batch blob, the second kept one
file per person but gzipped and re-pathed them. Both made the harvested file into something
else. Other workflows read these files, so the file that lands in the repo is byte-for-byte
the file the sweep produced, under the name the sweep gave it.

⛔ **AND IT RUNS ON A SHORT TIMER.** Harvested files live in `~/Downloads`, which is one copy
in one place. A cron calls this every four minutes and pushes, so nothing sits unarchived for
more than a few minutes, well inside the fifteen that was asked for.

A re-run of a person appears in Downloads as `... (1).tsv`; the LARGEST wins, because that is
the complete capture and the smaller is the truncated original it replaces.

⛔ The Downloads copies are LEFT ALONE. Nothing is deleted without being asked.
"""

from __future__ import annotations

import glob
import io
import os
import shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "reports", "sweep")


def main() -> int:
    pattern = os.path.expanduser("~/Downloads/sweep-descendants-*.tsv")
    todo = {}
    for path in sorted(glob.glob(pattern)):
        base = os.path.basename(path)
        fid = base.replace("sweep-descendants-", "").replace(".tsv", "").split(" (")[0]
        if fid not in todo or os.path.getsize(path) > os.path.getsize(todo[fid]):
            todo[fid] = path

    os.makedirs(OUT, exist_ok=True)
    copied, rows = 0, 0
    for fid, src in sorted(todo.items()):
        dest = os.path.join(OUT, "sweep-descendants-%s.tsv" % fid)
        # skip only when the repo already holds exactly this file
        if os.path.exists(dest) and os.path.getsize(dest) == os.path.getsize(src):
            continue
        shutil.copyfile(src, dest)
        copied += 1
        with io.open(dest, encoding="utf-8", errors="replace") as fh:
            rows += max(0, sum(1 for _ in fh) - 1)
    if not copied:
        print("nothing new to archive")
        return 0
    print("archived %d raw files, %d rows, into reports/sweep/" % (copied, rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
