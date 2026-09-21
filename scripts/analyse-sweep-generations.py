"""Marginal yield of the descendants sweep, by the GENERATION of the person swept.

The question, put 2026-09-21: *"likely it's almost always just the last generation that's
useful ... my prediction is that there's going to be a cutoff at a certain point where there's
going to be very consistently with a generation change essentially zero marginal returns."*

A **cliff** and **diminishing returns** are different shapes and the distinction is the point,
so this reports both: `new_per_focus` is the height of the curve at each depth, and
`marginal_new` is what that depth added that no shallower depth had already found.

Generation comes from Geni's own relationship string, never from positional parsing:

    NN's son                    1
    NN's grandson               2
    NN's great grandson         3
    NN's 11th great grandson    13

Writes `reports/sweep-generation-yield.csv` -- every generation, not a sample.
"""
from __future__ import annotations

import csv
import glob
import io
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOTS = {
    "6000000227822546944": os.path.join(REPO, "reports",
                                        "list-descendants-6000000227822546944.tsv"),
    "6000000002187826932": os.path.join(REPO, "reports", "sweep",
                                        "sweep-descendants-6000000002187826932.tsv"),
}
NTH = re.compile(r"(\d+)(?:st|nd|rd|th)\s+great\s+grand", re.I)
# Geni spells the small ordinals as WORDS and the large ones as digits, in the same list:
# `Yuri's fifth great grandson` sits beside `Yuri's 12th great grandson`. Reading only the
# digit form silently collapsed generations 4-7 into 3 and hid the whole middle of the curve.
WORDS = {"second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7,
         "eighth": 8, "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12}
WORD_NTH = re.compile(r"(%s)\s+great\s+grand" % "|".join(WORDS), re.I)


def generation(rel: str) -> int:
    """Depth in generations, or 0 when the string is not a descent."""
    r = rel.lower()
    m = NTH.search(r)
    if m:
        return int(m.group(1)) + 2
    m = WORD_NTH.search(r)
    if m:
        return WORDS[m.group(1).lower()] + 2
    if "great grand" in r:
        return 3
    if "grand" in r:
        return 2
    if re.search(r"'s (son|daughter|child)\b", r):
        return 1
    return 0


def main() -> int:
    gen = {}          # geni_id -> generation from its root
    in_root = set()   # everyone the two root lists already held

    for path in ROOTS.values():
        if not os.path.exists(path):
            continue
        with io.open(path, encoding="utf-8", errors="replace") as fh:
            head = fh.readline().rstrip("\n").split("\t")
            gi, ri = head.index("geni_id"), head.index(
                "relationship" if "relationship" in head else "relationship_text")
            for line in fh:
                c = line.rstrip("\n").split("\t")
                if len(c) <= max(gi, ri) or not c[gi]:
                    continue
                in_root.add(c[gi])
                g = generation(c[ri])
                if g and c[gi] not in gen:
                    gen[c[gi]] = g

    # every swept file, bucketed by the generation of its FOCUS
    buckets = {}
    for path in sorted(glob.glob(os.path.join(REPO, "reports", "sweep", "*.tsv"))):
        focus = os.path.basename(path)[len("sweep-descendants-"):-len(".tsv")]
        g = gen.get(focus)
        if g is None:
            continue
        b = buckets.setdefault(g, {"foci": 0, "rows": 0, "found": set()})
        b["foci"] += 1
        with io.open(path, encoding="utf-8", errors="replace") as fh:
            head = fh.readline().rstrip("\n").split("\t")
            try:
                gi = head.index("geni_id")
            except ValueError:
                continue
            for line in fh:
                c = line.rstrip("\n").split("\t")
                if len(c) > gi and c[gi]:
                    b["rows"] += 1
                    if c[gi] not in in_root:
                        b["found"].add(c[gi])

    out = os.path.join(REPO, "reports", "sweep-generation-yield.csv")
    seen: set = set()
    with io.open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["generation", "foci_swept", "rows_returned", "beyond_root",
                    "new_per_focus", "marginal_new", "cumulative_new"])
        for g in sorted(buckets):
            b = buckets[g]
            marginal = b["found"] - seen
            seen |= b["found"]
            w.writerow([g, b["foci"], b["rows"], len(b["found"]),
                        round(len(b["found"]) / b["foci"], 1) if b["foci"] else 0,
                        len(marginal), len(seen)])
    print("wrote %s -- %d generations, %d swept people bucketed"
          % (os.path.relpath(out, REPO), len(buckets),
             sum(b["foci"] for b in buckets.values())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
