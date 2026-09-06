"""Where to actually seed an export: the people furthest from anything covered.

**Emma, 2026-08-15:** *"can you please find people who are most distant from
people that are not exported otherwise, so that I can actually run the exports out
of them? You can't just tell me what these clusters are without even giving geni
IDs… Give me doorway status or something."*

`find-single-export-clusters.py` answered *where* the thin regions are and ranked
their members by **generations of recorded ancestry**, which was the wrong measure
for her purpose: it tied thousands of people at the same depth, so the "deepest
member" of a cluster was arbitrary among them.

**The measure here is graph distance from covered ground.** Everybody with
presence ≥ 2 — reached by more than one export — is a source. A breadth-first
walk out from *all* of them at once over the family graph gives every thin person
their distance to the nearest well-covered person. The furthest are the deep
interior of a region only one export ever touched, and seeding there is what
reaches material no existing export came near.

**Everybody is a candidate, including redacted profiles.** Emma, 2026-08-15:
*"we are including redacted profiles. Redacted profiles are important, and it's
kinda stupid to me that you're absolutely refusing to do anything with them."* A
first version excluded them on my own reasoning; that was the reflex `CLAUDE.md`
§ *Redacted people go in* already forbids. Redaction is a **column**, not a filter.

Two things are reported alongside the distance:

* **Doorway status** — no parents recorded. `density`'s reasoning: a person whose
  parents are missing is a doorway, because Geni knows who they were and we do
  not. It breaks ties on distance.
* **A profile URL per candidate**, because the deliverable is something to open
  and export from, not a table of identifiers.

Writes `reports/export-entry-points.md` and `.csv`, plus
`out/export-entry-points.txt` — one URL per line, for opening in a browser.

    py scripts/find-export-entry-points.py
"""

from __future__ import annotations

import csv
import sys
from collections import deque
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import density, sources  # noqa: E402
from genimerge.gedcom import stream_file  # noqa: E402
from genimerge.model import build_tree  # noqa: E402

MERGED = REPO / "out" / "merged.ged"
OUT_MD = REPO / "reports" / "export-entry-points.md"
OUT_CSV = REPO / "reports" / "export-entry-points.csv"
OUT_URLS = REPO / "out" / "export-entry-points.txt"

#: Presence at or above this is "covered ground" and seeds the walk.
COVERED = 2

#: Clusters smaller than this are the rim of a ball, not a neighbourhood.
MIN_SIZE = 25

#: Candidates recorded per cluster, and clusters carried into the URL list.
PER_CLUSTER = 6
TOP_CLUSTERS = 20

def is_redacted(name: str) -> bool:
    """Reported as a column, **never used to exclude anybody.**

    A first version dropped `Private` profiles from the candidates on the
    reasoning that a redacted person makes a poor seed. Emma, 2026-08-15:
    *"we are including redacted profiles. Redacted profiles are important, and
    it's kinda stupid to me that you're absolutely refusing to do anything with
    them."* That was my rule, not hers, and it is the same reflex `CLAUDE.md`
    § *Redacted people go in* already forbids — the structure around a redacted
    person is not redacted, and an export seeded there returns their relatives.
    """
    low = name.strip().casefold()
    return not low or low.split()[0] in {"private", "<private>"}


def main() -> int:
    paths = sources.find_exports()
    counts = density.presence_counts(paths)
    print(f"{len(paths)} exports, presence for {len(counts):,} people", flush=True)

    tree = build_tree(stream_file(MERGED))
    print(f"{len(tree.people):,} people", flush=True)
    graph = density.family_graph(tree)

    def name_of(gid: str) -> str:
        person = tree.people.get(gid)
        return (person.display_name if person is not None else "") or ""

    # -- distance from covered ground -----------------------------------
    #
    # Multi-source BFS: every well-covered person starts at 0 and the wave
    # spreads through the family graph. One pass, O(V+E), rather than a search
    # per candidate.
    dist: dict[str, int] = {}
    queue: deque[str] = deque()
    for gid in tree.people:
        if counts.get(gid, 0) >= COVERED:
            dist[gid] = 0
            queue.append(gid)
    print(f"{len(queue):,} people are covered ground (presence >= {COVERED})",
          flush=True)
    while queue:
        cur = queue.popleft()
        step = dist[cur] + 1
        for nxt in graph.get(cur, ()):
            if nxt not in dist:
                dist[nxt] = step
                queue.append(nxt)
    unreached = [g for g in tree.people if g not in dist]
    print(f"furthest distance found: {max(dist.values()) if dist else 0}; "
          f"{len(unreached):,} people in no component containing covered ground",
          flush=True)

    regions = density.sparse_regions(tree, counts, threshold=1,
                                     min_size=MIN_SIZE, graph=graph)
    print(f"{len(regions):,} clusters", flush=True)

    def has_parents(gid: str) -> bool:
        person = tree.people.get(gid)
        return bool(person is not None and person.has_known_parents)

    def url_of(gid: str) -> str:
        person = tree.people.get(gid)
        return (person.url if person is not None else "") or ""

    rows = []
    picks = []
    for rank, region in enumerate(regions, 1):
        usable = list(region.members)
        # Furthest from covered ground first; a doorway breaks a tie, because a
        # person whose parents are unrecorded is where Geni has more than we do.
        usable.sort(key=lambda g: (-dist.get(g, 10**6), has_parents(g)))
        chosen = usable[:PER_CLUSTER]
        for gid in chosen:
            row = [rank, region.size, gid, name_of(gid), dist.get(gid, -1),
                   "doorway" if not has_parents(gid) else "has parents",
                   "redacted" if is_redacted(name_of(gid)) else "named",
                   counts.get(gid, 0), url_of(gid)]
            rows.append(row)
            if rank <= TOP_CLUSTERS:
                picks.append(row)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["cluster", "cluster_size", "geni_id", "name",
                         "distance_from_covered", "doorway", "redaction",
                         "exports_containing", "url"])
        writer.writerows(rows)

    OUT_URLS.parent.mkdir(parents=True, exist_ok=True)
    OUT_URLS.write_text("\n".join(r[8] for r in picks) + "\n", encoding="utf-8")

    L: list[str] = []
    add = L.append
    add("# Where to seed the next exports")
    add("")
    add("**Emma, 2026-08-15:** *\"find people who are most distant from people that")
    add("are not exported otherwise, so that I can actually run the exports out of")
    add("them… Give me doorway status or something.\"*")
    add("")
    add(f"**Distance from covered ground** — a breadth-first walk out from all")
    add(f"{sum(1 for g in tree.people if counts.get(g, 0) >= COVERED):,} people")
    add(f"reached by {COVERED}+ exports, through the family graph. A candidate")
    add("far from all of them sits in the deep interior of a region one export")
    add("touched once, which is where a new seed reaches material nothing else came")
    add("near.")
    add("")
    add("**Redacted profiles are INCLUDED**, and flagged in their own column. Emma:")
    add("*\"we are including redacted profiles. Redacted profiles are important.\"* The")
    add("structure around a redacted person is not redacted, so an export seeded there")
    add("still returns their relatives.")
    add("")
    add("**Doorway** means no parents recorded: Geni knows who they were and we do")
    add("not. It breaks ties on distance.")
    add("")
    add("| cluster | size | candidate | dist | doorway | redaction | open |")
    add("| ---: | ---: | --- | ---: | --- | --- | --- |")
    for row in picks:
        add(f"| {row[0]} | {row[1]:,} | {row[3][:38] or '(unnamed)'} "
            f"`{row[2]}` | {row[4]} | {row[5]} | {row[6]} | [open]({row[8]}) |")
    add("")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"\nwrote {OUT_CSV} ({len(rows)} rows), {OUT_MD}, {OUT_URLS}")
    print("\ntop entry points:")
    for row in picks[:20]:
        print(f"  cluster {row[0]:>3} ({row[1]:>6,})  dist {row[4]:>3}  "
              f"{row[5]:<12} {row[6]:<9} {row[3][:30]:<32} {row[8]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
