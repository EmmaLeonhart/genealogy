"""One Wikidata item, several Geni profiles — the roster, and where an export would land.

    python scripts/multi-geni-item-roster.py

**Emma, 2026-08-25:** *"I came here wanting to do the one item several geni profiles and
gave detailed instructions earlier about it so do them."*

Her cause for the shape, which is about how Geni behaves rather than about error: *"Jenny
profiles get isolated from the main tree. Because they're isolated from the main tree,
nobody can edit them, so people add a new one because Jenny doesn't have the ability to
differentiate between multiple different contradictory facts."* Zerubbabel is the standing
example.

**Her algorithm, and it deliberately does NOT need to know which id was merged:** *"the
algorithm I provided you revolves around Providence of Entries... we have a separate
directory that is privileged over the other ones for this stuff. This means that we aren't
really removing the merged profile from the synoptic tree... We're just linking everything
to the proper thing there."* So the work is **exports into `exports/post-merge/`**, whose
records win by `sources._post_merge_last`, until the first-degree relatives of the affected
people are present. And: *"merged individuals cluster together so we will not need to run
an export on every one of them."*

**This script does the counting that decides where those exports go.** It answers three
things per item, all offline:

* **how many of its Geni profiles we actually hold** — an export refreshes people already
  in the tree, so an item whose profiles are all absent is not export work at all;
* **whether the profiles sit near each other in our tree** — measured as graph distance
  over parent/child/spouse edges, capped, because two profiles a few hops apart are one
  export and two profiles in different centuries are two;
* **how many first-degree relatives are missing**, which is Emma's stopping condition.

**The weakness she named is checked, not assumed:** *"we need to be sure that wiki data
stuff might potentially give the wrong ID... our wiki data mapping might be a bit wrong if
the ID changed."* The `in_corpus` column is exactly that check — a `P2600` naming a profile
no export has ever seen is either a stale id or a region we have not sampled, and the two
look identical from here, so it is reported rather than resolved.

Reads `reports/correspondence-shapes.tsv`, `reports/derived-family.csv`,
`reports/derived-labels.csv`. Writes `reports/multi-geni-items.tsv`.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from genimerge.sources import POST_MERGE_DIR  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent

#: Far enough that one export's ball plausibly covers both, and no further. A `Forest`
#: export walks parents, children and spouses outward, so hops here are the same edges.
NEAR_HOPS = 4


def main():
    # --- the population -------------------------------------------------------------
    comps = collections.defaultdict(lambda: {"q": set(), "g": set(), "src": set()})
    with open(ROOT / "reports" / "correspondence-shapes.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if not r["kind"].startswith("one item"):
                continue
            c = comps[r["component_qids"]]
            c["q"].add(r["qid"])
            c["g"].add(r["geni_id"])
            c["src"] |= set(r["sources"].split(";"))
    print(f"{len(comps):,} items carrying several Geni profiles")

    # --- the tree -------------------------------------------------------------------
    adj = collections.defaultdict(set)
    everyone = set()
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            me = row["geni_id"]
            # **Membership is having your OWN row**, never being named in someone else's.
            # Building `everyone` from the adjacency instead made every relative a member
            # by construction, so the "missing first-degree relatives" count came out 0
            # for every item -- a number that could not have been anything else.
            everyone.add(me)
            for col in ("father", "mother", "spouses", "children"):
                for other in (row.get(col) or "").replace(",", ";").split(";"):
                    other = other.strip()
                    if other:
                        adj[me].add(other)
                        adj[other].add(me)
    print(f"{len(everyone):,} people in the merged tree")

    # **Emma's stopping condition is about the PRIVILEGED directory, not the tree.**
    # *"export until all first-degree relatives of merged individuals are present"* --
    # present in `exports/post-merge/`, whose records win. A relative already in the tree
    # from a two-week-old export is exactly the stale snapshot the re-export exists to
    # replace, so counting them as present answers the wrong question.
    refreshed = set()
    post = ROOT / "exports" / POST_MERGE_DIR
    for ged in sorted(post.glob("*.ged")) if post.exists() else []:
        with open(ged, encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("0 @I") and "INDI" in line:
                    refreshed.add(line[4:line.index("@", 4)])
    print(f"{len(refreshed):,} people covered by exports/{POST_MERGE_DIR}/")

    names = {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            names[row["geni_id"]] = (row.get("label_en") or row.get("label_mul") or "")

    def hops(a, b, cap=NEAR_HOPS):
        """Graph distance a->b over family edges, or `''` beyond `cap`."""
        if a == b:
            return 0
        seen, frontier = {a}, [a]
        for d in range(1, cap + 1):
            nxt = []
            for node in frontier:
                for other in adj.get(node, ()):
                    if other == b:
                        return d
                    if other not in seen:
                        seen.add(other)
                        nxt.append(other)
            frontier = nxt
            if not frontier:
                break
        return ""

    rows = []
    for qids, c in comps.items():
        held = sorted(g for g in c["g"] if g in everyone)
        absent = sorted(g for g in c["g"] if g not in everyone)
        # Distance between the held profiles: min over pairs, since one export seeded
        # anywhere in the group covers the group if any pair is close.
        dists = [hops(a, b) for i, a in enumerate(held) for b in held[i + 1:]]
        near = [d for d in dists if d != ""]
        # Emma's stopping condition, measured per held profile: a first-degree relative
        # is "present" only when the privileged directory covers them.
        kin = {k for g in held for k in adj.get(g, ())}
        missing_kin = len(kin - refreshed)
        rows.append({
            "qid": qids,
            "n_geni": len(c["g"]),
            "n_in_corpus": len(held),
            "n_absent": len(absent),
            "closest_hops": min(near) if near else "",
            "one_export_covers": "yes" if near and min(near) <= NEAR_HOPS else "no",
            "missing_first_degree": missing_kin,
            "first_degree_total": len({k for g in held for k in adj.get(g, ())}),
            "already_refreshed": "yes" if all(g in refreshed for g in held) and held
                                 else "no",
            "sources": ";".join(sorted(c["src"])),
            "geni_in_corpus": ";".join(held),
            "geni_absent": ";".join(absent),
            "names": " | ".join((names.get(g, "") or "?")[:34] for g in held),
        })

    rows.sort(key=lambda r: (-r["n_in_corpus"], r["closest_hops"] == "",
                             -r["missing_first_degree"]))
    dest = ROOT / "reports" / "multi-geni-items.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    both = [r for r in rows if r["n_in_corpus"] >= 2]
    one = [r for r in rows if r["n_in_corpus"] == 1]
    none = [r for r in rows if r["n_in_corpus"] == 0]
    covered = [r for r in both if r["one_export_covers"] == "yes"]
    print(f"\nwrote {dest.relative_to(ROOT)}\n")
    print(f"  {len(both):>5}  items with TWO OR MORE of their profiles in our corpus")
    print(f"  {len(covered):>5}    ... of which one export reaches both "
          f"(<={NEAR_HOPS} hops apart)")
    print(f"  {len(one):>5}  items with exactly one profile held - the other is unsampled "
          f"or a stale id")
    print(f"  {len(none):>5}  items with no profile held - not export work")
    print(f"\n  {sum(r['missing_first_degree'] for r in both):,} first-degree relatives "
          f"missing across the actionable items")


if __name__ == "__main__":
    main()
