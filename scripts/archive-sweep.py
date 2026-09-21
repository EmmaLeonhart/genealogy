"""Move finished sweep files out of Downloads and into the repo, append-only.

Ruled 2026-09-20: *"And commit and push after current person. Should be done very
consistently."* The sweep writes one TSV per person into `~/Downloads`, which is outside the
repo and therefore not preserved by anything.

⛔ **APPEND-ONLY, BECAUSE THE WHOLE THING IS ~15 GB.** 174 people are 89 MB raw and 10.8 MB
gzipped, so all 29,388 come to roughly 15 GB raw and 1.8 GB gzipped. Re-committing one
growing file would store a fresh ~1.8 GB blob every cycle. Instead each run gzips only the
people that are NEW since last time into their own numbered batch, which is written once and
never touched again -- git stores each blob exactly once.

`reports/sweep/manifest.tsv` records which focus ids are in which batch, so a person is never
archived twice and the set already captured can be answered without unpacking anything.

The Downloads copies are LEFT ALONE. Ruled the same day, repeatedly: nothing is deleted
without being asked.
"""

from __future__ import annotations

import glob
import gzip
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "reports", "sweep")
MANIFEST = os.path.join(OUT, "manifest.tsv")


def archived() -> set:
    got = set()
    if os.path.exists(MANIFEST):
        with io.open(MANIFEST, encoding="utf-8") as fh:
            fh.readline()
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if f:
                    got.add(f[0])
    return got


def next_batch() -> int:
    n = 0
    for p in glob.glob(os.path.join(OUT, "batch-*.tsv.gz")):
        m = re.search(r"batch-(\d+)", os.path.basename(p))
        if m:
            n = max(n, int(m.group(1)))
    return n + 1


def main() -> int:
    pattern = os.path.expanduser("~/Downloads/sweep-descendants-*.tsv")
    have = archived()
    todo = {}
    for path in sorted(glob.glob(pattern)):
        base = os.path.basename(path)
        fid = base.replace("sweep-descendants-", "").replace(".tsv", "").split(" (")[0]
        if fid in have:
            continue
        # a re-run writes "... (1).tsv"; keep the LARGEST, which is the complete one
        if fid not in todo or os.path.getsize(path) > os.path.getsize(todo[fid]):
            todo[fid] = path
    if not todo:
        print("nothing new to archive")
        return 0

    os.makedirs(OUT, exist_ok=True)
    n = next_batch()
    dest = os.path.join(OUT, "batch-%04d.tsv.gz" % n)
    rows = 0
    with gzip.open(dest, "wt", encoding="utf-8", newline="") as gz:
        gz.write("focus_id\tgeni_id\tpage\tchk_text\tchk_hrefs\tphoto_text\tphoto_hrefs\t"
                 "name_text\tname_hrefs\trelationship_text\trelationship_hrefs\t"
                 "managed_by_text\tmanaged_by_hrefs\timmediate_family_text\t"
                 "immediate_family_hrefs\tactions_text\tactions_hrefs\n")
        for fid in sorted(todo):
            with io.open(todo[fid], encoding="utf-8", errors="replace") as fh:
                fh.readline()
                for line in fh:
                    if line.strip():
                        gz.write(line)
                        rows += 1
    new = not os.path.exists(MANIFEST)
    with io.open(MANIFEST, "a", encoding="utf-8", newline="") as fh:
        if new:
            fh.write("focus_id\tbatch\n")
        for fid in sorted(todo):
            fh.write("%s\t%04d\n" % (fid, n))
    print("batch-%04d.tsv.gz: %d people, %d rows, %.1f MB"
          % (n, len(todo), rows, os.path.getsize(dest) / 1048576.0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
