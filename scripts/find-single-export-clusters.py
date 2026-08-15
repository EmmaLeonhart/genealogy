"""Clusters only ONE export ever reached, and the deepest people inside them.

**Emma's item, 2026-08-15, in her words:** *"we are going to look over the geni
exports to try to find large clusters like the Javanese ones that have only one
geni export covering them. My perception here is that such areas are more likely
to have important links that were not covered and that with a different entry
point and a larger export window thing, particularly looking at the deepest
members of such clusters of people only in one export."*

**The case that prompted it.** The excluded `BloodTree` of `6000000227240714964`
held **1,091 people no other export had** — Mataram and Demak royalty, reached
once by a walk that went up out of the Samaritan cluster and never returned.

**Two halves, and only the second is new.** `genimerge.density` already finds
connected runs of people at or below a presence threshold; run at `threshold=1`
those runs are exactly "clusters one export covered". What it ranks them by is a
**doorway** count — people whose parents are unrecorded — which is the right
question for *coverage*. Emma is asking a different one: which member is
**deepest**, because that is where a differently-seeded export would reach past
what the single existing one stopped at.

**Deepest means generations of recorded ancestry above them**,
`frontier.ancestor_depth`. A person deep inside a thin cluster sits at the end of
a long line we have followed exactly once — the far edge of one ball, and the
place a new entry point buys the most.

**Presence measures our sampling, never Geni's content** — `CLAUDE.md`. A cluster
reached once is one *we* barely covered; whether Geni holds more there is the
unknown an export resolves.

Writes `reports/single-export-clusters.md` and `.csv`.

    py scripts/find-single-export-clusters.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import density, frontier, sources  # noqa: E402
from genimerge.gedcom import stream_file  # noqa: E402
from genimerge.model import build_tree  # noqa: E402

MERGED = REPO / "out" / "merged.ged"
OUT_MD = REPO / "reports" / "single-export-clusters.md"
OUT_CSV = REPO / "reports" / "single-export-clusters.csv"

#: How many of the deepest members to record per cluster. Enough to choose an
#: entry point by eye; the CSV carries every member's depth regardless.
DEEPEST = 8

#: Clusters smaller than this are the rim of a ball rather than a neighbourhood
#: — `density`'s own reasoning, and the same number it defaults to.
MIN_SIZE = 25


def main() -> int:
    paths = sources.find_exports()
    print(f"{len(paths)} exports", flush=True)
    counts = density.presence_counts(paths)
    print(f"presence counted for {len(counts):,} people", flush=True)

    print(f"loading {MERGED.name}", flush=True)
    tree = build_tree(stream_file(MERGED))
    print(f"{len(tree.people):,} people", flush=True)

    graph = density.family_graph(tree)
    regions = density.sparse_regions(tree, counts, threshold=1,
                                     min_size=MIN_SIZE, graph=graph)
    print(f"{len(regions):,} clusters reached by one export or none", flush=True)

    depth = frontier.ancestor_depth(tree)

    def name_of(gid: str) -> str:
        """`Person.name` is a `Name` object, not a string — use its `display`."""
        person = tree.people.get(gid)
        if person is None or person.name is None:
            return ""
        return person.name.display or ""

    rows = []
    for rank, region in enumerate(regions, 1):
        members = sorted(region.members, key=lambda g: -depth.get(g, 0))
        for gid in members:
            rows.append([rank, region.size, gid, name_of(gid),
                         depth.get(gid, 0), counts.get(gid, 0)])

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["cluster", "cluster_size", "geni_id", "name",
                         "generations_above", "exports_containing"])
        writer.writerows(rows)
    print(f"wrote {OUT_CSV} ({len(rows):,} rows)")

    total = sum(r.size for r in regions)
    L: list[str] = []
    add = L.append
    add("# Clusters only one export ever reached")
    add("")
    add("**Emma's item, in her words:** *\"we are going to look over the geni exports")
    add("to try to find large clusters like the Javanese ones that have only one geni")
    add("export covering them… particularly looking at the deepest members of such")
    add("clusters of people only in one export.\"*")
    add("")
    add(f"**{len(regions):,} clusters, {total:,} people**, each reached by at most one")
    add(f"export, each cluster at least {MIN_SIZE} people. Every member is a row in")
    add("`reports/single-export-clusters.csv` with its depth.")
    add("")
    add("**Deepest = generations of recorded ancestry above the person.** That is the")
    add("far edge of the one ball that reached this cluster, and the place a different")
    add("entry point buys the most. It is a different ranking from `reports/density.md`,")
    add("which ranks by **doorways** — people whose parents are unrecorded — because")
    add("that answers coverage rather than reach.")
    add("")
    add("**Presence measures our sampling, never Geni's content.** A cluster reached")
    add("once is one *we* barely covered; whether Geni holds more there is exactly the")
    add("unknown an export resolves.")
    add("")
    add("## The clusters")
    add("")
    for rank, region in enumerate(regions[:30], 1):
        members = sorted(region.members, key=lambda g: -depth.get(g, 0))
        add(f"### {rank}. {region.size:,} people — "
            f"{region.parentless:,} with no parents recorded")
        add("")
        add(f"Sample: {', '.join(region.sample[:4])}")
        add("")
        add("| deepest members | generations above |")
        add("| --- | ---: |")
        for gid in members[:DEEPEST]:
            add(f"| {name_of(gid)[:60]} (`{gid}`) | {depth.get(gid, 0)} |")
        add("")
    if len(regions) > 30:
        add(f"…and {len(regions) - 30:,} more clusters in the CSV.")
        add("")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD}")

    print(f"\ntop clusters by size:")
    for rank, region in enumerate(regions[:10], 1):
        members = sorted(region.members, key=lambda g: -depth.get(g, 0))
        top = members[0] if members else ""
        print(f"  {rank:>2}. {region.size:>6,} people   deepest: "
              f"{name_of(top)[:38]:<40} {depth.get(top, 0):>3} generations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
