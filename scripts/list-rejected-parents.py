"""Every parent the duplicate guard rejects, with the item it thinks they might be.

    python scripts/list-rejected-parents.py

**Emma, 2026-08-31:** *"this is solely around parent blockages… blocked because they're connected
as parents of an individual with p2600 on them but don't have a p2600 on them. Earlier algorithm
would have made a nearly certain duplicate of the parent, I freaked out and you disabled any
creation of parents… I'm trying to manually approve or reject all currently blocked parents and
you can get a better sample size as to the rules and edge cases."*

Then, on how to find them: *"you know you can use the mechanics of the algorithm to find the
rejected parent inclusions"*. She is right, and it matters — I had re-derived the population by
hand and got a different number three times. This runs **the guard's own second arm**, unchanged,
over every candidate instead of over one day's ring:

    a child of ours already has an item `cq`
    `cq` names parent items that nothing in `claimed` accounts for
    -> creating our person could duplicate one of them, so the guard refuses

`build-garborg-day.py` applies that to `to_create`, which is a single day's one-edge ring, so its
carry-forward shows only the handful reached that day. The rule is the same; only the candidate
set is wider here.

**A rejection is a QUESTION, not a verdict.** The guard cannot tell "our person IS that item"
from "our person is a genuinely different parent". That is the judgement Emma is making by hand,
and each answer she gives is a data point about where the line falls — which is why the output
carries the evidence rather than a recommendation.

Writes `reports/rejected-parents.tsv`.
"""

import csv
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RELATIONS = ROOT / "out" / "wikidata" / "relations.tsv"
FAMILY = ROOT / "reports" / "derived-family.csv"
LABELS = ROOT / "reports" / "derived-labels.csv"
OUT = ROOT / "reports" / "rejected-parents.tsv"

csv.field_size_limit(1 << 30)
SEP = "|"


def cell(row, column):
    return [x.strip() for x in (row.get(column) or "").split(SEP) if x.strip()]


def main():
    # --- Wikidata's side: who has a P2600, and who each item names as a parent ---------
    geni_of, parents_of = {}, {}
    with io.open(RELATIONS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            qid = row["qid"]
            if row.get("p2600"):
                geni_of[qid] = row["p2600"].split(SEP)[0].strip()
            ps = [x for x in (row.get("p22") or "").split(SEP) if x]
            ps += [x for x in (row.get("p25") or "").split(SEP) if x]
            if ps:
                parents_of[qid] = ps
    qid_of = {g: q for q, g in geni_of.items()}
    # `claimed`: an item already tied to some Geni profile is spoken for, whoever holds it.
    # Same widening as `build-garborg-day.py` got on 2026-08-31.
    claimed = set(geni_of)
    sys.stderr.write(f"{len(geni_of):,} items carry a P2600; "
                     f"{len(parents_of):,} name at least one parent\n")

    # --- our side: parents, and who our people's children are -------------------------
    our_parents, our_children = {}, {}
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = row["geni_id"]
            ps = cell(row, "fathers") + cell(row, "mothers")
            if ps:
                our_parents[g] = ps
            ks = cell(row, "children")
            if ks:
                our_children[g] = ks

    labels = {}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            labels[row["geni_id"]] = row.get("label_en") or row.get("label_mul") or ""

    # --- the guard's second arm, over every candidate ---------------------------------
    # A candidate is anybody who is a parent of somebody we can already point at, and who
    # has no item of their own. Minted placeholders are excluded: they are ours, not Geni's.
    candidates = set()
    for child, parents in our_parents.items():
        if child in qid_of:
            for p in parents:
                if p not in qid_of and not p.startswith(("9995", "9990")):
                    candidates.add(p)

    rows = []
    for g in sorted(candidates):
        for child in our_children.get(g, ()):
            cq = qid_of.get(child)
            if not cq:
                continue
            loose = [x for x in parents_of.get(cq, []) if x not in claimed]
            if loose:
                rows.append({
                    "our_geni": g,
                    "our_name": labels.get(g, ""),
                    "via_child_geni": child,
                    "via_child_name": labels.get(child, ""),
                    "via_child_qid": cq,
                    "candidate_parent_qids": SEP.join(loose),
                })
                break          # one question per person, not one per child

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", fieldnames=list(rows[0]) if rows else
                           ["our_geni", "our_name", "via_child_geni", "via_child_name",
                            "via_child_qid", "candidate_parent_qids"])
        w.writeheader()
        w.writerows(rows)

    print(f"{len(candidates):,} parents of somebody who has an item, with no item themselves")
    print(f"{len(rows):,} of those the guard REJECTS -- the child's item names a parent "
          f"nothing accounts for")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
