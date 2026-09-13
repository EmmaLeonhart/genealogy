"""Build the TRUNK roster for a descent, and say whether the uniform frame is broken.

    python scripts/trunk-roster.py                 # survey every descent roster
    python scripts/trunk-roster.py <geni id> ...   # build the trunk roster for these

**Ruled 2026-09-13**, after the Monte Carlo on `NN Father of Huaxu` `6000000227036719829` read
24 census pages and reported a largest descent of **43** — from a root holding 120,878. Emma:
*"Well do it"*, on applying the fix to the other deep roots.

## Why a uniform sample of a descent is a broken frame

`scripts/monte-carlo-pick.py` and the extension's `{type:"montecarlo"}` both draw uniformly from
the descent roster, which is right when the descent is shallow and wrong when it is deep. Huaxu's
runs to **156 generations with 78.6% of its people at generation 130 or below** — one generation
is 11,277 wide. A uniform draw of 40 therefore takes ~39 people from the fan-out and ~1 from
everything above it, and a person at generation 130 of 156 has at most 26 generations beneath
them: their true descent IS 12, 17, 43. **The sweep was measuring leaves and reporting that the
tree is small.**

Restricted to the trunk, the identical sweep — same root, same threshold, same 40 draws — went
from *top 43, zero hits* to **9,265 / 6,802 / 6,793**.

## Where the cut goes, and why 20%

The trunk is everyone above the fan-out. The cut is the deepest generation whose CUMULATIVE share
of the descent is still under **20%** — which on Huaxu lands at generation 115 (15.9%), the cut
that was chosen by hand and then validated by three sweeps. It is a share rather than a fixed
generation because roots differ enormously in depth: Aztec is 35 generations and Huaxu 156.

**A shallow root needs no roster and gets none.** If the whole descent is under `FLOOR` people or
the trunk would be most of it, the uniform frame is already fine and a second file would only be
something to keep in sync.
"""

from __future__ import annotations

import collections
import csv
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

#: The cumulative share the trunk stops at. See the module docstring.
SHARE = 0.20

#: Below this the descent is too small for the frame to matter at all.
FLOOR = 3000

#: A root whose trunk is this much of its descent is not deep enough to bother restricting.
NOT_DEEP = 0.60


def rows_of(path):
    with path.open(encoding="utf-8") as fh:
        return [(r["geni_id"], int(r["generation"]), r["name"])
                for r in csv.DictReader(fh)]


def cut_at(counts, total):
    """The deepest generation whose cumulative share is still under `SHARE`."""
    cum = 0
    keep = 0
    for gen in sorted(counts):
        cum += counts[gen]
        if cum / total > SHARE:
            break
        keep = gen
    return keep


def survey(path):
    rows = rows_of(path)
    if not rows:
        return None
    total = len(rows)
    counts = collections.Counter(g for _i, g, _n in rows)
    deepest = max(counts)
    peak = max(counts.items(), key=lambda kv: kv[1])
    keep = cut_at(counts, total)
    in_trunk = sum(v for g, v in counts.items() if g <= keep)
    return {"total": total, "generations": deepest, "peak_gen": peak[0], "peak_width": peak[1],
            "cut": keep, "trunk": in_trunk,
            "share": in_trunk / total if total else 0}


def build(geni_id):
    src = REPORTS / ("descent-from-%s.csv" % geni_id)
    stats = survey(src)
    out = REPORTS / ("descent-from-%s-trunk.csv" % geni_id)
    rows = [r for r in rows_of(src) if r[1] <= stats["cut"]]
    with io.open(out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["geni_id", "generation", "name"])
        writer.writerows(rows)
    print("  %s -> %s  (gen <= %d, %d people, %.1f%% of the descent)"
          % (geni_id, out.name, stats["cut"], len(rows), 100 * stats["share"]))
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ids = sys.argv[1:]
    if ids:
        for geni_id in ids:
            build(geni_id)
        return 0

    print("%-22s %8s %5s %8s %8s %7s  %s"
          % ("root", "descent", "gens", "peak gen", "cut at", "trunk", "verdict"))
    for path in sorted(REPORTS.glob("descent-from-*.csv")):
        if "-trunk" in path.name or "-gen" in path.name:
            continue
        geni_id = path.stem.replace("descent-from-", "")
        stats = survey(path)
        if not stats:
            continue
        if stats["total"] < FLOOR:
            verdict = "too small to matter"
        elif stats["share"] > NOT_DEEP:
            verdict = "shallow -- uniform is fine"
        else:
            verdict = "DEEP -- restrict the frame"
        print("%-22s %8d %5d %8d %8d %6.1f%%  %s"
              % (geni_id, stats["total"], stats["generations"], stats["peak_gen"],
                 stats["cut"], 100 * stats["share"], verdict))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
