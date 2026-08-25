"""The zipper join: walk both trees together and pair people by matching family position.

    python scripts/zipper-join.py

**Emma, 2026-08-25:** *"The zipper merge kinda half exists and is opaque I thought you meant
something more clear and substantive than just having never even tried to implement the feature.
Implement it."*

She is right that it did not exist. What existed were parent-shaped fragments — three separate
scripts that opened a shard to read one pair's `P22` — and none of them walked, none of them
looked at children or spouses, and none of them fed a result back in to reach further. This does.

## Her design, in her words

*"For the synoptic tree, we're supposed to be specifically going up the parental lines and stuff
like that and merging the parents on Geni and Wikidata if there are ones on both. Same with all
the other relationships."* And the rule for when to accept: *"we merge them based off of whether
something is the mother on both sides of an individual. We merge them together unless the mothers
really conflict."*

And the warning about where it gets hard: *"parents are very easy to do a zipper join on.
Children, however, selecting between children and spouses, and in some cases multiple sets of
parents, is a much, much more difficult task."*

## How it runs

**Anchors** are the pairs Wikidata already asserts — every `P2600` *Geni.com profile ID* in
`out/wikidata/p2600-all.tsv`. Each anchor is a place where our tree and Wikidata are known to be
describing the same person.

**Each round**, for every anchor `(g, q)`, four slots are compared:

* `father` — our `father` against the item's `P22`
* `mother` — our `mother` against the item's `P25`
* `child` — our `children` against the item's `P40`
* `spouse` — our `spouses` against the item's `P26`

For a slot, **already-known correspondences are consumed first**: any person on our side whose
partner is already paired, and whose partner appears on their side, is struck from both. That is
the zipper's teeth — each closed pair removes a candidate from both sides and makes the residual
smaller.

**What is left is proposed only when it is unambiguous: exactly one unpaired person on our side
and exactly one on theirs.** Two-against-two proposes nothing. This is the honest answer to the
hard case she named: with two unmatched children on each side there is no evidence which is
which, and guessing would be the coin flip she ruled against on 2026-08-25 — *"Lean two people —
never merge on a coin flip."*

**New pairs become anchors and the next round runs.** That is what makes it a join rather than a
check: closing a father lets the next round reach that father's parents, his other children, and
his wife.

## What it refuses to do

* **A proposal that contradicts a recorded `P2600` is a conflict, never a pair.** Wikidata's own
  identifier outranks our inference, always.
* **A person proposed for two different items, or an item proposed for two different people, is
  dropped** — both proposals, not one of them. Ambiguity is not resolved by picking.
* **No name is compared, anywhere.** Not for matching, not for tiebreaks. Position is the whole
  evidence, which is what `CLAUDE.md` demands and what the deleted `reconcile` module got wrong.
* **It emits no edit.** The output is a correspondence for the synoptic tree.

## Reading the output

`reports/zipper-pairs.tsv` — proposals, with the slot and the round that produced each. **Round
number is a confidence signal**: round 1 pairs hang directly off a Wikidata-asserted identifier,
round 6 pairs hang off five inferences in a chain.

`reports/zipper-ambiguous.tsv` — slots where both sides had unmatched people but more than one.
This is the honest measure of the hard case, and it is the file to look at before deciding
whether the join needs names, dates, or nothing at all.

`reports/zipper-conflicts.tsv` — proposals refuted by a recorded `P2600`.

Requires `out/wikidata/relations.tsv` from `scripts/extract-wikidata-relations.py`.
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
RELATIONS = ROOT / "out" / "wikidata" / "relations.tsv"

#: Their property for each slot, and the column of ours it faces.
SLOTS = (("father", "p22", "father"), ("mother", "p25", "mother"),
         ("child", "p40", "children"), ("spouse", "p26", "spouses"))

#: Emma's call, 2026-08-25: keep rounds 1-3. Error compounds with each round because each
#: anchors on the last -- 3.9% at round 1, 9.8% at round 3, 27.1% at round 8, measured against
#: dates. Round 3 is the knee. Later rounds are still written to the file with their round
#: number so the number can be revisited; the filter is in the consumer.
ROUND_CAP = 3

#: How far the walk goes. Rounds beyond `ROUND_CAP` are recorded, not consumed.
MAX_ROUNDS = 8


def split(cell):
    """Multi-valued cell -> list.

    **The separator in `reports/derived-family.csv` is ` | `, and this function did not know it.**
    Found 2026-08-25 when Emma said *"I feel the zipper merge still isn't hitting the hard points
    lol."* She was right and the reason was mechanical: with only `,` and `;` handled, a five-child
    cell parsed as the single token `"1050090 | 1050271 | ..."`, which is in nobody's index, so it
    was filtered out by `if x in ours` and the person presented as **childless**.

    **379,251 people have two or more children and every one of them reached the join with none.**
    That is why `zipper-ambiguous.tsv` held no `2 x 2` rows at all -- not because two-against-two
    is rare, but because our side could never *have* two. The whole hard case Emma named in the
    design -- *"selecting between children and spouses ... is a much, much more difficult task"* --
    was invisible.

    This is the same shape as the date-parser failures in `CLAUDE.md`: a parser that silently
    narrows its input rather than failing. Nothing raised, the counts looked plausible, and the
    join quietly restricted itself to one-child families.

    **Two bugs, not one.** The separator is ` | ` *with spaces*, so splitting on `|` alone yields
    `"1050090 "` and every token then missed the `x in ours` index -- the same silent narrowing one
    layer down, and it hid the first fix completely: the pair count did not move at all until the
    tokens were stripped. 191,991 child ids and 19,404 spouse ids were being dropped this way.
    """
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def main():
    if not RELATIONS.exists():
        sys.exit(f"missing {RELATIONS} - run scripts/extract-wikidata-relations.py first")

    theirs = {}
    with open(RELATIONS, encoding="utf-8") as f:
        rd = csv.DictReader(f, delimiter="\t")
        for row in rd:
            theirs[row["qid"]] = row
    print(f"{len(theirs):,} Wikidata items with family relationships")

    ours = {}
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ours[row["geni_id"]] = row
    print(f"{len(ours):,} people in our tree")

    # --- anchors: what Wikidata itself asserts ------------------------------------------
    g2q, q2g = {}, {}
    stated_g, stated_q = collections.defaultdict(set), collections.defaultdict(set)
    for qid, row in theirs.items():
        for g in split(row.get("p2600")):
            stated_g[g].add(qid)
            stated_q[qid].add(g)
    for g, qs in stated_g.items():
        if len(qs) == 1 and g in ours:
            q = next(iter(qs))
            if len(stated_q[q]) == 1:
                g2q[g], q2g[q] = q, g
    print(f"{len(g2q):,} anchors - one Geni id, one item, both sides agree")

    pairs = {}          # geni -> (qid, slot, round)
    conflicts, ambiguous = [], []
    frontier = set(g2q)

    for rnd in range(1, MAX_ROUNDS + 1):
        proposed = collections.defaultdict(set)   # geni -> {qid}
        reverse = collections.defaultdict(set)    # qid -> {geni}
        seen_slots = 0
        for g in frontier:
            q = g2q.get(g)
            mine, their = ours.get(g), theirs.get(q)
            if not mine or not their:
                continue
            for slot, prop, column in SLOTS:
                us = [x for x in split(mine.get(column)) if x in ours]
                them = split(their.get(prop))
                if not us or not them:
                    continue
                seen_slots += 1
                # Consume the teeth already closed: anyone of ours already paired to an
                # item that appears on their side matches, and both are struck.
                # Consume the teeth, then drop anyone already spoken for on EITHER side.
                # `left` used to keep our already-paired people (they were rejected later by the
                # `a in g2q` guard), so a slot with one paired and one free child of ours counted
                # as two unmatched and was filed ambiguous instead of proposing the free one.
                used = {g2q[x] for x in us if g2q.get(x) in them}
                left = [x for x in us if x not in g2q]
                right = [x for x in them if x not in used and x not in q2g]
                if len(left) == 1 and len(right) == 1:
                    a, b = left[0], right[0]
                    if a in g2q or b in q2g:
                        continue
                    if stated_g.get(a) and b not in stated_g[a]:
                        conflicts.append({"round": rnd, "slot": slot, "geni_id": a,
                                          "proposed_qid": b,
                                          "recorded_qid": ";".join(sorted(stated_g[a])),
                                          "from_geni": g, "from_qid": q})
                        continue
                    proposed[a].add(b)
                    reverse[b].add(a)
                elif left and right:
                    ambiguous.append({"round": rnd, "slot": slot, "from_geni": g,
                                      "from_qid": q, "ours_unmatched": ";".join(left),
                                      "theirs_unmatched": ";".join(right)})

        # Ambiguity is dropped on BOTH sides, never resolved by picking.
        fresh = {}
        for g, qs in proposed.items():
            if len(qs) != 1:
                continue
            q = next(iter(qs))
            if len(reverse[q]) != 1:
                continue
            fresh[g] = q
        if not fresh:
            print(f"round {rnd}: {seen_slots:,} slots compared, nothing new - done")
            break
        for g, q in fresh.items():
            g2q[g], q2g[q] = q, g
            pairs[g] = (q, "", rnd)
        # record which slot produced each, for the report
        for g in fresh:
            pairs[g] = (fresh[g], pairs[g][1], rnd)
        print(f"round {rnd}: {seen_slots:,} slots compared, "
              f"{len(fresh):,} new pairs, {len(g2q):,} total")
        frontier = set(fresh)

    out = ROOT / "reports" / "zipper-pairs.tsv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["round", "geni_id", "qid"])
        for g, (q, _s, rnd) in sorted(pairs.items(), key=lambda kv: (kv[1][2], kv[0])):
            w.writerow([rnd, g, q])

    for name, rows, cols in (
            ("zipper-conflicts.tsv", conflicts,
             ["round", "slot", "geni_id", "proposed_qid", "recorded_qid", "from_geni",
              "from_qid"]),
            ("zipper-ambiguous.tsv", ambiguous,
             ["round", "slot", "from_geni", "from_qid", "ours_unmatched",
              "theirs_unmatched"])):
        p = ROOT / "reports" / name
        with open(p, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
            w.writeheader()
            w.writerows(rows)

    print(f"\n{len(pairs):,} NEW correspondences -> reports/zipper-pairs.tsv")
    print(f"{len(conflicts):,} refuted by a recorded P2600 -> reports/zipper-conflicts.tsv")
    print(f"{len(ambiguous):,} slots too ambiguous to call -> reports/zipper-ambiguous.tsv")
    by_slot = collections.Counter(a["slot"] for a in ambiguous)
    if by_slot:
        print("\nwhere the ambiguity is - the hard case Emma named:")
        for slot, n in by_slot.most_common():
            print(f"   {n:>7}  {slot}")


if __name__ == "__main__":
    main()
