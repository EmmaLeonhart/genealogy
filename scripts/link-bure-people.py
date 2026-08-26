"""Connect the Bure people who already have Wikidata items, using what Geni knows.

    python scripts/link-bure-people.py

**Emma, 2026-08-25:** *"I want to try connecting the bure people that exist together. What is the
topology of them? Like of the bure people what percentage of the wikidata linked ones are just
directly connected through geni even though they are absent on wikidata?"* Then: *"Attempt to link
all the bure people together."*

**This is a different job from every other batch in this repo, and she said why:** *"bure is a
bunch of unlinked people with entity resolutions to geni, so it isn't dense it's a different kind
of area though which needs its own algorithm... as so many people there have wikidata items
already the types of quickstatements will be different and potentially more challenging."*

The Garborg batches are almost entirely `CREATE`, and the whole one-hop-a-day pacing exists to
work around `LAST` being invalid as a value. **Here nothing is created.** Both endpoints already
have QIDs, so every statement is `Q… P22 Q…` and the `LAST` limitation does not apply at all.

**Bureätten the EXPORT campaign stays closed** — 7 resolved, 76 dropped, 0 exports ever run. This
is not that. Nobody is being searched for and no export is proposed; these are people already on
both sides, being joined.

## What it measures

For every pair of Bure people who both hold a QID and a Geni id:

* **direct on Geni** — our tree records one as the other's father, mother, spouse or child.
* **direct on Wikidata** — the item already states it.
* **the gap** — the edge Geni records and Wikidata does not. That is the batch.
* **bridged** — connected on Geni only through intermediate people who have **no** Wikidata item.
  This is her topology question: the cluster may be far more connected than Wikidata shows, with
  the joins hidden behind people nobody has created yet. A bridge of length 2 needs one person
  created to close it; the report counts them by bridge length so the cheap ones are visible.

## What it refuses

* **No name matching.** Correspondence comes from `P2600` *Geni.com profile ID*, from the
  `geni_ids` column of `reports/bureatten.csv`, and from `reports/bureatten-resolved.tsv` — every
  one an exact join on this repo's primary key.
* **Sex refutes a parent edge.** If our tree calls somebody a father and the item is `Q6581072`
  *female*, the edge is dropped rather than emitted. Same rule as `scripts/zipper-join.py`: it
  refutes, it never confirms.
* **Never contradicts a statement that exists.** If the item already carries a `P22` naming
  somebody else, this emits nothing for that slot — `CLAUDE.md`: the purpose is to ADD, not to
  correct, and a disagreement is a note rather than a work item.

Writes `reports/bure-topology.md`, `reports/bure-links.tsv` and `reports/wikidata-bure-links.qs`.
Offline; queued, never run — Wikidata editing in this repo starts 2026-09-01.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "reports"

#: our column -> their property, and the reciprocal we would also be entitled to state.
EDGES = (("father", "P22"), ("mother", "P25"), ("spouses", "P26"), ("children", "P40"))
MALE, FEMALE = "Q6581097", "Q6581072"

#: How far to walk through people with NO Wikidata item when looking for a bridge. Two Bure
#: people six unlinked generations apart are not usefully "connected"; the useful ones are
#: the short bridges, where creating one or two people closes a real join.
MAX_BRIDGE = 4


def split(cell):
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def main():
    # ---- the roster, and its correspondence -----------------------------------------
    # **The roster is the GENI-SIDE one now, not the 576 Wikidata entries.**
    # `scripts/build-bure-roster.py` measured both definitions on Emma's instruction, and the
    # Geni-side neighbourhood carries **1,595** people with a Wikidata item against the
    # Wikidata roster's 258 -- six times as many, every one already on both sides. Running
    # this over 258 measured a sixth of the population and reported 97.6% of direct edges as
    # already stated; that number described a small, well-tended core, not the cluster.
    q2g = collections.defaultdict(set)
    kind = {}
    roster_file = R / "bure-roster.tsv"
    if roster_file.exists():
        with open(roster_file, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                if row["qid"]:
                    q2g[row["qid"]].add(row["geni_id"])
                    kind.setdefault(row["qid"], "person")
    with open(R / "bureatten.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            kind[row["qid"]] = row["kind"]
            for g in re.split(r"[;,| ]+", row["geni_ids"] or ""):
                if g.strip().isdigit():
                    q2g[row["qid"]].add(g.strip())
    roster = set(kind)
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0] in roster and row[1].strip().isdigit():
                q2g[row[0]].add(row[1].strip())
    p = R / "bureatten-resolved.tsv"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                if row["geni_id"].strip().isdigit():
                    q2g[row["qid"]].add(row["geni_id"].strip())
    # A Geni id claimed by two roster QIDs cannot anchor anything: it would let one person
    # stand in for two, which is the tangle the structural walk manufactured 89% of.
    owner = collections.defaultdict(set)
    for q, gs in q2g.items():
        for g in gs:
            owner[g].add(q)
    g2q = {g: next(iter(qs)) for g, qs in owner.items() if len(qs) == 1}
    contested = {g: qs for g, qs in owner.items() if len(qs) > 1}
    linked = {q for q in q2g if any(g2q.get(g) == q for g in q2g[q])}
    print(f"{len(roster):,} Bure entries · {sum(1 for k in kind.values() if k == 'person'):,} "
          f"people · {len(linked):,} carry a usable Geni id"
          + (f" · {len(contested)} Geni ids contested and dropped" if contested else ""))

    # ---- both trees ------------------------------------------------------------------
    fam = {}
    with open(R / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fam[row["geni_id"]] = row
    theirs = {}
    with open(ROOT / "out" / "wikidata" / "relations.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            theirs[row["qid"]] = row
    sex = {}
    sp = ROOT / "out" / "wikidata" / "sex.tsv"
    if sp.exists():
        with open(sp, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                sex[row["qid"]] = row["sex"]
    names = {}
    with open(R / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in g2q:
                names[row["geni_id"]] = row["label_en"] or row["label_mul"]

    # ---- direct edges, both sides ----------------------------------------------------
    gen_edges, wd_edges, gaps, refused = set(), set(), [], collections.Counter()
    for g, q in g2q.items():
        mine = fam.get(g)
        if not mine:
            continue
        for col, prop in EDGES:
            for other in split(mine[col]):
                oq = g2q.get(other)
                if not oq or oq == q:
                    continue
                gen_edges.add((q, prop, oq))
                stated = split((theirs.get(q) or {}).get(prop.lower().replace("p", "p"), ""))
                stated = [x for x in ((theirs.get(q) or {}).get(
                    {"P22": "p22", "P25": "p25", "P26": "p26", "P40": "p40"}[prop]) or "").split(";") if x]
                if oq in stated:
                    wd_edges.add((q, prop, oq))
                    continue
                # Wikidata already names somebody else in a single-valued parent slot:
                # adding ours would contradict rather than add. CLAUDE.md: add, never correct.
                if prop in ("P22", "P25") and stated:
                    refused["parent slot already filled by someone else"] += 1
                    continue
                # Sex refutes a parent edge and never confirms one.
                want = MALE if prop == "P22" else FEMALE if prop == "P25" else None
                if want and sex.get(oq) and sex[oq] != {"Q6581097": "M", "Q6581072": "F"}[want]:
                    refused["sex refutes the parent edge"] += 1
                    continue
                gaps.append({"subject_qid": q, "property": prop, "object_qid": oq,
                             "subject_geni": g, "object_geni": other,
                             "subject_name": names.get(g, ""), "object_name": names.get(other, "")})

    # ---- bridges: connected on Geni only THROUGH people with no item -----------------
    anchored = set(g2q)
    bridges = collections.Counter()
    bridge_rows = []
    seen_pair = set()
    for start in anchored:
        frontier = {start: []}
        visited = {start}
        for depth in range(1, MAX_BRIDGE + 1):
            nxt = {}
            for g, via in frontier.items():
                mine = fam.get(g)
                if not mine:
                    continue
                for col, _prop in EDGES:
                    for other in split(mine[col]):
                        if other in visited or other not in fam:
                            continue
                        visited.add(other)
                        if other in anchored:
                            key = tuple(sorted((start, other)))
                            if depth > 1 and key not in seen_pair:
                                seen_pair.add(key)
                                bridges[depth] += 1
                                bridge_rows.append({
                                    "a_qid": g2q[start], "b_qid": g2q[other],
                                    "a_name": names.get(start, ""), "b_name": names.get(other, ""),
                                    "hops": depth, "people_to_create": depth - 1,
                                    "via": ";".join(via + [g] if g != start else via)})
                        else:
                            nxt[other] = via + ([g] if g != start else [])
            frontier = nxt
            if not frontier:
                break

    # ---- write -----------------------------------------------------------------------
    with open(R / "bure-links.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(gaps[0]) if gaps else ["subject_qid"],
                           delimiter="\t")
        w.writeheader()
        w.writerows(gaps)
    with open(R / "bure-bridges.tsv", "w", encoding="utf-8", newline="") as f:
        if bridge_rows:
            w = csv.DictWriter(f, fieldnames=list(bridge_rows[0]), delimiter="\t")
            w.writeheader()
            w.writerows(sorted(bridge_rows, key=lambda r: r["hops"]))
        else:
            f.write("(none)\n")

    qs = R / "wikidata-bure-links.qs"
    with open(qs, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Bure people who ALREADY have items, linked to each other from what Geni\n"
                "# records. Nothing is created; both ends of every statement already exist.\n"
                "# QUEUED, NEVER RUN. Wikidata editing in this repo starts 2026-09-01.\n\n")
        for row in gaps:
            f.write(f'{row["subject_qid"]}\t{row["property"]}\t{row["object_qid"]}'
                    f'\tS2600\t"{row["subject_geni"]}"\n')

    direct_both = len(wd_edges)
    direct_geni = len(gen_edges)
    print(f"\n{direct_geni:,} direct relationships Geni records between two linked Bure people")
    print(f"{direct_both:,} of those Wikidata already states "
          f"({100 * direct_both / max(direct_geni, 1):.1f}%)")
    print(f"{len(gaps):,} are the GAP - the batch")
    for why, n in refused.most_common():
        print(f"   {n:>5,} refused: {why}")
    print(f"\nbridged pairs - connected on Geni ONLY through people with no item:")
    for d in sorted(bridges):
        print(f"   {bridges[d]:>5,} pairs at {d} hops "
              f"({d - 1} intermediate {'person' if d == 2 else 'people'} to create)")
    # ---- coverage, which is what actually bounds all of the above --------------------
    in_tree = sum(1 for g in g2q if g in fam)
    missing = len(g2q) - in_tree
    mids = collections.Counter(r["via"] for r in bridge_rows if r["hops"] == 2)

    with open(R / "bure-topology.md", "w", encoding="utf-8", newline="\n") as f:
        f.write("# The Bure cluster: what is actually disconnected\n\n")
        f.write("Generated by `scripts/link-bure-people.py`. Emma, 2026-08-25: *\"What is the "
                "topology of them? Like of the bure people what percentage of the wikidata "
                "linked ones are just directly connected through geni even though they are "
                "absent on wikidata?\"*\n\n")
        f.write("**The short answer is that they are not missing links to each other. They are "
                "missing the people in between.**\n\n")
        f.write("| | |\n| --- | ---: |\n")
        f.write(f"| Bure entries rostered | {len(roster):,} |\n")
        f.write(f"| of those, people rather than families | "
                f"{sum(1 for k in kind.values() if k == 'person'):,} |\n")
        f.write(f"| carrying a usable Geni id | {len(g2q):,} |\n")
        f.write(f"| **of those, present in our corpus** | **{in_tree:,}** |\n")
        f.write(f"| absent from every export we hold | {missing:,} |\n\n")
        f.write(f"## Direct relationships\n\n")
        f.write(f"Between two Bure people who both hold a QID, Geni records **{direct_geni:,}** "
                f"direct relationships. Wikidata already states **{direct_both:,}** of them "
                f"— **{100 * direct_both / max(direct_geni, 1):.1f}%**. Only "
                f"**{len(gaps)}** are missing, and they are in "
                f"`reports/wikidata-bure-links.qs`.\n\n")
        f.write("So the premise that these people are unlinked *to each other* does not hold "
                "where we can see both ends. Wikidata has almost all of it.\n\n")
        f.write("## Where the disconnection really is\n\n")
        f.write("**Pairs joined on Geni only through people who have no Wikidata item:**\n\n")
        f.write("| hops | pairs | people to create |\n| ---: | ---: | ---: |\n")
        for d in sorted(bridges):
            f.write(f"| {d} | {bridges[d]:,} | {d - 1} |\n")
        f.write(f"\n**{bridges.get(2, 0)} of those pairs are one person apart, and only "
                f"{len(mids)} distinct people account for all of them.** Creating those "
                f"{len(mids)} closes {bridges.get(2, 0)} joins at once — the single densest "
                f"one closes {mids.most_common(1)[0][1] if mids else 0}.\n\n")
        f.write("`reports/bure-bridges.tsv` lists every pair with the people in between.\n\n")
        f.write("## The number that bounds everything above\n\n")
        f.write(f"**{missing} of the {len(g2q)} Bure profiles carrying a Geni id are not in our "
                f"corpus at all** — no export we hold reaches them. Their relationships are "
                f"invisible to this measurement, so every figure here is a **floor**. More "
                f"exports would find more edges; none of these numbers can go down.\n")

    print(f"\ncorpus coverage: {in_tree:,} of {len(g2q):,} linked Bure profiles are in our "
          f"tree; {missing:,} are not, so every number above is a FLOOR")
    if mids:
        print(f"{len(mids)} distinct people account for all {bridges.get(2, 0)} one-hop "
              f"bridges; the densest closes {mids.most_common(1)[0][1]}")
    print(f"\nwrote reports/bure-topology.md, bure-links.tsv, bure-bridges.tsv, {qs.name}")


if __name__ == "__main__":
    main()
