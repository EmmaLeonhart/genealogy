"""Who actually appears in the paths, and which of them are connectors rather than kin.

    PYTHONPATH=src python scripts/build-path-frequency.py

Writes `reports/path-frequency.csv`: one row per person who appears as a STEP in
`reports/path-chains.tsv`, with enough columns to tell the two populations apart.

⛔ **WITHIN PATHS, NOT WITHIN EXPORTS.** The corpus says who has been exported; this says who the
relationship search keeps routing THROUGH, which is a different and more useful question.

## The judgement this file exists to support

Every chain starts at the account owner, so her parents, grandparents and their siblings appear
in nearly every chain and top any raw frequency count. They are not connectors -- they are the
first few steps of the only road out. Counting them as hubs would make the report useless.

⛔ **THE SEPARATOR IS DEPTH SPREAD, AND A DEPTH CUT-OFF IS THE WRONG ONE.** The first version
of this script called anything below step 4 the spine and everything else a connector, which put
83,249 of 83,441 people in the "connector" class and was therefore worthless. The account owner's
own ancestral line runs sixteen-plus steps deep; depth does not separate anything.

**A person who appears at exactly ONE step depth in every chain is a trunk link.** That is what
`min_step == max_step` means: every path reaches them by the same route, because there IS only
one route. 77,596 of 83,441 people are that. They are not hubs, whatever their raw count.

**A person reached at SEVERAL depths is reached by several different branches**, and that is the
whole definition of a connector. 5,845 people qualify, and they split again by how wide:

    trunk       spread 0        one fixed position in every chain it appears in
    junction    spread 1-5      a few branches converging -- the genuinely interesting ones
    corridor    spread 6+       a long line entered at many points, e.g. a dynasty walked
                                from both ends; large numbers, less leverage per person

`reach` -- distinct destinations whose chain passes through the person -- ranks within a class.
"""

from __future__ import annotations

import collections
import csv
import io
import os
import statistics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAINS = os.path.join(ROOT, "reports", "path-chains.tsv")
OUT = os.path.join(ROOT, "reports", "path-frequency.csv")

#: Where a junction stops being a junction and becomes a corridor. Set from the observed
#: distribution: the Portuguese and Gyntersberg convergences sit at spread 1-3, and the Seljuk
#: and Turgesh lines at 48-60, with almost nothing between.
CORRIDOR_SPREAD = 6


def main() -> int:
    chains: dict = {}
    names: dict = {}
    rel: dict = collections.defaultdict(collections.Counter)

    with io.open(CHAINS, encoding="utf-8") as fh:
        rd = csv.reader(fh, delimiter="\t")
        next(rd, None)
        for row in rd:
            if len(row) < 6:
                continue
            to_id, kind, step, pid, name, relation = row[:6]
            if not pid or step == "-1":
                continue
            try:
                step_n = int(step)
            except ValueError:
                continue
            chains.setdefault(pid, []).append((to_id, kind, step_n))
            if name and pid not in names:
                names[pid] = name
            if relation:
                rel[pid][relation] += 1

    total_chains = len({(t, k) for v in chains.values() for t, k, _ in v})

    rows = []
    for pid, seen in chains.items():
        steps = [s for _, _, s in seen]
        dests = {t for t, _, _ in seen}
        med = statistics.median(steps)
        rows.append({
            "geni_id": pid,
            "name": names.get(pid, ""),
            "appearances": len(seen),
            "reach": len(dests),
            "min_step": min(steps),
            "median_step": med,
            "max_step": max(steps),
            "depth_spread": max(steps) - min(steps),
            # A function of SPREAD, not of depth. See the header.
            "kind": ("trunk" if max(steps) == min(steps)
                     else "corridor" if max(steps) - min(steps) >= CORRIDOR_SPREAD
                     else "junction"),
            "top_relation": rel[pid].most_common(1)[0][0] if rel[pid] else "",
        })

    rows.sort(key=lambda r: (-r["reach"], -r["appearances"], r["geni_id"]))

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("%s: %d people over %d chains" % (OUT, len(rows), total_chains))
    for kind in ("trunk", "junction", "corridor"):
        print("%-9s %d" % (kind, sum(1 for r in rows if r["kind"] == kind)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
