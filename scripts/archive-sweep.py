"""Copy finished sweep files out of Downloads and into the repo, ONE FILE PER PERSON.

Ruled 2026-09-20: *"And commit and push after current person. Should be done very
consistently."* The sweep writes one TSV per person into `~/Downloads`, which is outside the
repo and therefore preserved by nothing.

⛔ **EACH INDIVIDUAL GETS THEIR OWN FILE. NEVER CONCATENATED.** The first version merged 171
people into one gzipped batch and was refused on sight: *"Are you not sharding? ... Are you
for some reason having all the descendants reports being not descendants reports? But being
like one gigantic file?"* and *"Each individual gets their own file."* A descendant report is
a per-person object; merging them destroys the thing that makes it one, and it cannot be
handed back, diffed or re-run per person afterwards.

Sharded two levels by the last two digits of the id, because 29,388 files in one directory is
miserable to work with. Each file is ~60 KB gzipped and is written exactly once, so git stores
each blob once and nothing is ever rewritten.

A re-run of a person appears in Downloads as `... (1).tsv`; the LARGEST file wins, because
that is the complete capture and the smaller one is the truncated original.

⛔ The Downloads copies are LEFT ALONE. Ruled repeatedly the same day: nothing is deleted
without being asked.
"""

from __future__ import annotations

import glob
import gzip
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "reports", "sweep")


def shard(fid: str) -> str:
    return fid[-2:] if len(fid) >= 2 else "00"


def dest_for(fid: str) -> str:
    return os.path.join(OUT, shard(fid), fid + ".tsv.gz")


def main() -> int:
    pattern = os.path.expanduser("~/Downloads/sweep-descendants-*.tsv")
    todo = {}
    for path in sorted(glob.glob(pattern)):
        base = os.path.basename(path)
        fid = base.replace("sweep-descendants-", "").replace(".tsv", "").split(" (")[0]
        if os.path.exists(dest_for(fid)):
            continue
        if fid not in todo or os.path.getsize(path) > os.path.getsize(todo[fid]):
            todo[fid] = path
    if not todo:
        print("nothing new to archive")
        return 0

    rows = 0
    for fid in sorted(todo):
        dest = dest_for(fid)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with io.open(todo[fid], encoding="utf-8", errors="replace") as fh:
            body = fh.read()
        with gzip.open(dest, "wt", encoding="utf-8", newline="") as gz:
            gz.write(body)
        rows += max(0, body.count("\n") - 1)
    print("archived %d people, %d rows, one file each under reports/sweep/<shard>/"
          % (len(todo), rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
