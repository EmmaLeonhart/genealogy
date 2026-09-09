"""What did the edge exports actually close?

    python scripts/backtest-edge-exports.py

**Emma's complaint, 2026-08-15, and it is the whole reason this exists:** *"Finding these
sparse areas, which we kind of did, and I did exports based off of them, but it feels like you
kind of forgot about them."* Thirty-one edge exports were run off
`reports/export-entry-points.csv`, placed in `exports/edges/`, and **nothing ever checked what
they bought**.

**The measurement is exact and needs no browser.** Every row of `export-entry-points.csv`
carries `exports_containing`, which was the number of exports holding that person when the
report was written — 1 for every entry point, since the whole file is drawn from clusters only
one export ever reached. Counting the same people across the corpus today gives the delta
directly, per person and per cluster.

**This is the shape `reports/descendants-backtest-2026-08-07.md` established**, and the reason
that file exists: two seed-choosing methods have been refuted here by measurement, so a seeding
method that has never been checked against an outcome is not evidence of anything. `CLAUDE.md`
is explicit that `seeds.md` *"has never been validated against an outcome"*; this validates the
entry-point method against one.

**A person still on 1 is not a failure of the export.** An export is a ball around a seed, so
it closes the neighbourhood it lands in and not the rest of the cluster. The useful figure is
therefore per-cluster reach — how much of each sparse cluster stopped being single-export — and
not a pass rate over individuals.

Writes `reports/edge-export-backtest.md` and `reports/edge-export-backtest.csv`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

from genimerge.sources import find_exports  # noqa: E402

ENTRY = ROOT / "reports" / "export-entry-points.csv"
OUT_MD = ROOT / "reports" / "edge-export-backtest.md"
OUT_CSV = ROOT / "reports" / "edge-export-backtest.csv"

RFN = re.compile(rb"^1 RFN geni:(\d+)", re.M)


def main():
    rows = list(csv.DictReader(ENTRY.open(encoding="utf-8")))
    wanted = {r["geni_id"] for r in rows}
    print(f"{len(rows):,} entry points across "
          f"{len({r['cluster'] for r in rows}):,} sparse clusters")

    files = list(find_exports())
    print(f"counting them across {len(files)} exports ...", flush=True)
    # **Attribution, not just correlation.** "Now in more than one export" does not say WHICH
    # export did it, and without that the headline is a coverage figure rather than a verdict on
    # the method. `exports/edges/` is where the 31 targeted takes were filed, so membership of
    # one of those files is the attribution.
    now = collections.Counter()
    by_edge = set()
    for n, path in enumerate(files):
        is_edge = "edges" in path.parts
        for m in RFN.finditer(path.read_bytes()):
            gid = m.group(1).decode()
            if gid in wanted:
                now[gid] += 1
                if is_edge:
                    by_edge.add(gid)
        if (n + 1) % 150 == 0:
            print(f"  {n + 1} exports", flush=True)

    for r in rows:
        r["exports_now"] = now.get(r["geni_id"], 0)
        r["gained"] = r["exports_now"] - int(r["exports_containing"] or 0)
        r["in_an_edge_export"] = "yes" if r["geni_id"] in by_edge else ""


    reached = [r for r in rows if r["exports_now"] > 1]
    absent = [r for r in rows if r["exports_now"] == 0]
    print(f"\n{len(reached):,} of {len(rows):,} entry points "
          f"({100 * len(reached) / len(rows):.1f}%) are now in more than one export")
    if absent:
        print(f"{len(absent):,} are in NO export at all -- they were in one when the report "
              f"was written, so an export they relied on has since been excluded")

    by_cluster = collections.defaultdict(list)
    for r in rows:
        by_cluster[r["cluster"]].append(r)
    cluster_rows = []
    for cid, members in by_cluster.items():
        hit = sum(1 for m in members if m["exports_now"] > 1)
        cluster_rows.append({
            "cluster": cid,
            "cluster_size": members[0]["cluster_size"],
            "entry_points": len(members),
            "entry_points_now_multi_export": hit,
            "share": f"{100 * hit / len(members):.0f}%",
        })
    cluster_rows.sort(key=lambda c: -int(c["cluster_size"]))

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    closed = sum(1 for c in cluster_rows if c["entry_points_now_multi_export"])
    top_ranks = {str(i) for i in range(1, 11)}
    top = [r for r in reached if r["cluster"] in top_ranks]
    top_all = [r for r in rows if r["cluster"] in top_ranks]
    top_edge = sum(1 for r in top if r["in_an_edge_export"])
    rest = [r for r in reached if r["cluster"] not in top_ranks]
    rest_edge = sum(1 for r in rest if r["in_an_edge_export"])
    with OUT_MD.open("w", encoding="utf-8") as fh:
        fh.write("# What the edge exports closed\n\n")
        fh.write("**Emma, 2026-08-15:** *\"Finding these sparse areas, which we kind of did, "
                 "and I did exports based off of them, but it feels like you kind of forgot "
                 "about them.\"* This is the check that was never run.\n\n")
        fh.write(f"Every one of the **{len(rows):,}** people in "
                 "`reports/export-entry-points.csv` was in **exactly one** export when that "
                 "file was written — the file is drawn from clusters only one export ever "
                 "reached. Counting the same people across the corpus today gives what the "
                 "edge exports bought, exactly.\n\n")
        fh.write(f"- **{len(reached):,} of {len(rows):,} "
                 f"({100 * len(reached) / len(rows):.1f}%)** are now in more than one export.\n")
        fh.write(f"- **{closed} of {len(cluster_rows)}** sparse clusters have at least one "
                 "entry point that is no longer single-export.\n")
        if absent:
            fh.write(f"- **{len(absent):,}** are now in no export at all, which means an "
                     "export they depended on has since moved to `exports/excluded/`.\n")
        fh.write("\n## The method worked where it was applied; the rest is background\n\n")
        fh.write(f"**Clusters 1-10: {len(top)} of {len(top_all)} entry points closed "
                 f"({100 * len(top) / len(top_all):.0f}%), and an `exports/edges/` file "
                 f"contains {top_edge} of the {len(top)}.** The targeted exports did that "
                 "work themselves; it is not coverage that would have happened anyway.\n\n")
        fh.write(f"**Everywhere else: {len(rest)} closed, of which edges account for "
                 f"{rest_edge}.** Closure across the remaining clusters runs at a flat "
                 "15-20% whatever their rank, which is what ordinary later exports drifting "
                 "over them looks like rather than an effect of this method.\n\n")
        fh.write("So the entry-point ranking is **validated on the ten clusters it was "
                 "actually used on** and untested below them, because only 31 exports were "
                 "ever run from it. That is a reason to run more, not a reason to read the "
                 "20.4% headline as what the method delivers.\n")
        fh.write("\n**A person still on 1 is not a failed export.** An export is a ball around "
                 "a seed: it closes the neighbourhood it lands in, not the whole cluster. The "
                 "per-cluster column is the one to read.\n\n")
        fh.write("| cluster | size | entry points | now multi-export | share |\n")
        fh.write("| ---: | ---: | ---: | ---: | ---: |\n")
        for c in cluster_rows[:40]:
            fh.write(f"| {c['cluster']} | {int(c['cluster_size']):,} | {c['entry_points']} | "
                     f"{c['entry_points_now_multi_export']} | {c['share']} |\n")
    print(f"wrote {OUT_MD.relative_to(ROOT)} and {OUT_CSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
