"""Park every CBDB person at `2026-10-31` in `reports/unconnected-p2600.tsv`.

Emma, 2026-09-10: *"cbdb people can all get their date last edited set to October 31, 2026 so
that we don't need to deal with their bullshit. This means every wikidata item with 'cbdb' in its
English description."* The population comes from `scripts/scan-cbdb-items.py`.

⛔ **THIS ADDS NO STATE AND NEEDS NO FILTER.** `last_attempted` is the one column a rebuild
carries (`load_previous`); membership, the neighbourhood size and the six statistics are all
recomputed from the connectivity graph every run. Emma, the same day: *"you can just add bullshit
people into the tsv as long as the geni id and qid match and they will be removed lol while the
cbdb people who belong will stay."* So a CBDB person who is not actually a disconnected `P2600`
holder simply drops out of the next build, and one who is keeps the date. Nothing here decides
which is which, and nothing here is allowed to.

The statistics columns on an appended row are written as the builder's own placeholders --
`200 200 200 200 200 no` -- because those are recomputed, and inventing a different filler would
be inventing state.
"""

from __future__ import annotations

import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKLIST = ROOT / "reports" / "unconnected-p2600.tsv"
CBDB = ROOT / "reports" / "cbdb-items.tsv"

PARK = "2026-10-31"
PLACEHOLDER = ["200", "200", "200", "200", "200", "no"]


def main() -> int:
    pairs = {}
    with CBDB.open(encoding="utf-8") as fh:
        rd = csv.reader(fh, delimiter="\t")
        next(rd)
        for row in rd:
            if len(row) >= 2 and row[1]:
                pairs[row[1]] = row[0]          # geni_id -> qid

    with WORKLIST.open(encoding="utf-8") as fh:
        rd = csv.reader(fh, delimiter="\t")
        header = next(rd)
        rows = [r for r in rd if r]

    seen, restamped = set(), 0
    for r in rows:
        gid = r[1]
        if gid in pairs:
            seen.add(gid)
            if r[3] != PARK:
                r[3] = PARK
                restamped += 1

    appended = 0
    width = len(header)
    for gid, qid in sorted(pairs.items()):
        if gid in seen:
            continue
        row = [qid, gid, "0", PARK] + PLACEHOLDER
        rows.append((row + [""] * width)[:width])
        appended += 1

    with WORKLIST.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")

    print("cbdb people with a Geni id: %d" % len(pairs))
    print("  already in the worklist, re-stamped to %s: %d" % (PARK, restamped))
    print("  already in the worklist, already parked:   %d" % (len(seen) - restamped))
    print("  appended (the rebuild drops any that do not belong): %d" % appended)
    print("worklist rows now: %d" % len(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
