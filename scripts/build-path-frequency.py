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

⛔ **THE DEPTH TAXONOMY THIS FILE FIRST CARRIED WAS AN ARTEFACT OF THE SEARCHER.** It sorted
people into trunk / junction / corridor by how many distinct step-depths they were reached at,
on the reasoning that several depths meant several branches converging. Emma, 2026-09-16:
*"I'm not sure if hub vs trunk is a real thing in our data. As the search logic basically makes
everything a trunk and it's just in-law vs blood closest connection."* Measured, and it is so:

    83,441  people in the chains
    77,596  appear at exactly ONE depth                one shortest path each
     4,646  vary only between blood and in-law         two searches, not two branches
     1,199  vary within a single kind                  and mostly by 1-3 steps

**Geni returns one shortest chain per destination per kind.** Every chain starts at the same
person, so a person's depth is their distance from that root and is near enough fixed. Counting
distinct depths counts the searcher, not the graph.

## What IS in the data

**`reach` -- how many destinations' chains pass through a person.** That is a real property of
the harvest: Berengaria of Portugal is on 1,271 of 12,905 chains, so a tenth of every path found
runs through her. It is a statement about the shortest-path tree rather than about the underlying
graph, and that is exactly what makes it useful -- **a high-reach person is a cut vertex on the
routes we have.** If their record is wrong, or they come unconnected, everything behind them goes
with it.

**`blood_reach` / `inlaw_reach`** split that by search, because the split is the one distinction
the data genuinely offers.
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
        blood = {t for t, k, _ in seen if k == "blood"}
        inlaw = {t for t, k, _ in seen if k != "blood"}
        rows.append({
            "geni_id": pid,
            "name": names.get(pid, ""),
            "reach": len(dests),
            "blood_reach": len(blood),
            "inlaw_reach": len(inlaw),
            "appearances": len(seen),
            "depth": min(steps),
            "median_step": statistics.median(steps),
            "max_step": max(steps),
            "top_relation": rel[pid].most_common(1)[0][0] if rel[pid] else "",
        })

    rows.sort(key=lambda r: (-r["reach"], -r["appearances"], r["geni_id"]))

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("%s: %d people over %d chains" % (OUT, len(rows), total_chains))
    both = sum(1 for r in rows if r["blood_reach"] and r["inlaw_reach"])
    print("on both a blood and an in-law chain: %d" % both)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
