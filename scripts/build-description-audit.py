"""Every description we would write, and whether they are unique.

    PYTHONPATH=src python scripts/build-description-audit.py

⛔ **THE DESCRIPTIONS NEED TO BE UNIQUE, AND THIS MEASURES IT RATHER THAN ASSUMING IT.** Ruled
2026-09-20: *"mass generating descriptions, the descriptions that you'd be making for
individuals, perhaps in a committed CSV file, so that you could then look through it to figure
out the degree that the descriptions are unique. Because the descriptions need to be unique."*

**Why it is not cosmetic.** Wikibase refuses a creation only when the label AND a non-empty
description both match, so the description is the ONLY thing standing between us and a duplicate
item. Measured 2026-09-19: eleven live items labelled `Margareta` and four labelled
`Hans Larsson` coexist, because blank descriptions never refused anything. A description that
repeats across two different people is a guard that does not guard -- it looks like protection
and provides none.

**The unit is the PAIR, not the description.** Two people may share a description freely if their
labels differ; Wikibase only refuses on label-plus-description. So the collision this counts is
`(label, description)`, and a bare description count would badly overstate the problem.

**It calls `life_description` rather than reimplementing it**, because a second copy of the
formatting would drift from the emitter and then measure the wrong thing -- `CLAUDE.md`
§ *A GUARD IN ONE EMITTER IS NOT A GUARD*.

Writes `reports/description-audit.csv`: `geni_id,label,description,pair_count,is_collision`.
"""
from __future__ import annotations

import collections
import csv
import importlib.util
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#: ⛔ **TWO FILES, AND THE BIG ONE IS NOT COMMITTED.** The full audit is **109 MB** over
#: 1.76M people -- past GitHub's 100 MB hard limit, which on 2026-09-19 made the pre-receive
#: hook decline every pipeline push for hours. It is also not what anyone reads: 99.85% of it
#: says *unique*, and a reviewer wants the exceptions.
#:
#: So the full file is written for inspection and gitignored, and the COLLISIONS are committed.
#: 1,872 rows is a file a person can actually look through, which is what was asked for.
FULL = os.path.join(ROOT, "reports", "description-audit.csv")
OUT = os.path.join(ROOT, "reports", "description-collisions.csv")
SUMMARY = os.path.join(ROOT, "reports", "description-uniqueness.md")

csv.field_size_limit(10 ** 9)


def _emitter():
    """`life_description` from the composer itself, never a copy of it."""
    spec = importlib.util.spec_from_file_location(
        "bgd", os.path.join(ROOT, "scripts", "build-garborg-day.py"))
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    spec.loader.exec_module(m)
    return m.life_description


def _places():
    p = os.path.join(ROOT, "reports", "derived-places.csv")
    out = {}
    if not os.path.exists(p):
        return out
    with io.open(p, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            if g:
                out[g] = row
    return out


def _labels():
    p = os.path.join(ROOT, "reports", "derived-labels.csv")
    out = {}
    if not os.path.exists(p):
        return out
    with io.open(p, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            if g:
                # `mul` is the label the batch writes; `en` is the fallback it also writes.
                out[g] = (row.get("label_mul") or row.get("label_en") or "").strip()
    return out


def main() -> int:
    life = _emitter()
    places, labels = _places(), _labels()

    rows = []
    facts = os.path.join(ROOT, "reports", "derived-facts.csv")
    with io.open(facts, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            if not g:
                continue
            desc = life(row, places.get(g))
            rows.append((g, labels.get(g, ""), desc))

    pair = collections.Counter((lab, d) for _g, lab, d in rows if d and lab)
    blank = sum(1 for _g, _l, d in rows if not d)

    with io.open(FULL, "w", encoding="utf-8", newline="") as fh, \
         io.open(OUT, "w", encoding="utf-8", newline="") as ch:
        w = csv.writer(fh, lineterminator="\n")
        c = csv.writer(ch, lineterminator="\n")
        head = ["geni_id", "label", "description", "pair_count", "is_collision"]
        w.writerow(head)
        c.writerow(head)
        for g, lab, d in rows:
            n = pair.get((lab, d), 0) if (d and lab) else 0
            rec = [g, lab, d, n, "yes" if n > 1 else ""]
            w.writerow(rec)
            if n > 1:
                c.writerow(rec)

    colliding_pairs = sum(1 for _k, v in pair.items() if v > 1)
    people_in_collision = sum(v for _k, v in pair.items() if v > 1)
    described = len(rows) - blank
    with io.open(SUMMARY, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Description uniqueness\n\n")
        fh.write("Regenerated by `scripts/build-description-audit.py`. The unit is the PAIR\n")
        fh.write("`(label, description)`, because Wikibase refuses a creation only when BOTH match,\n")
        fh.write("so a description that repeats under a different label costs nothing.\n\n")
        fh.write("| | |\n|---|---|\n")
        fh.write(f"| people | {len(rows):,} |\n")
        fh.write(f"| with a description | {described:,} ({100*described/max(len(rows),1):.1f}%) |\n")
        fh.write(f"| **no description at all** | **{blank:,}** ({100*blank/max(len(rows),1):.1f}%) |\n")
        fh.write(f"| distinct (label, description) | {len(pair):,} |\n")
        fh.write(f"| colliding pairs | {colliding_pairs:,} |\n")
        fh.write(f"| people in a collision | {people_in_collision:,} |\n\n")
        fh.write("## The worst collisions\n\n| count | label | description |\n|---|---|---|\n")
        for (lab, d), n in pair.most_common(40):
            if n > 1:
                fh.write(f"| {n} | {lab} | {d} |\n")
    print(f"{os.path.relpath(FULL, ROOT)}: {len(rows):,} people "
          f"({os.path.getsize(FULL)/1048576:.0f} MB, not committed)")
    print(f"  with a description      {described:,} ({100*described/max(len(rows),1):.1f}%)")
    print(f"  NO description at all   {blank:,}  <- no dedup guard whatsoever")
    print(f"  distinct (label, desc)  {len(pair):,}")
    print(f"  colliding pairs         {colliding_pairs:,}")
    print(f"  people in a collision   {people_in_collision:,}")
    if colliding_pairs:
        print("  worst:")
        for (lab, d), n in pair.most_common(8):
            if n > 1:
                print(f"    x{n:<5} {lab[:34]:34s} | {d[:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
