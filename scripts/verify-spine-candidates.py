"""Judge the spine's name candidates by STRUCTURE, never by the name that found them.

    python scripts/verify-spine-candidates.py

Three of the sixteen chain steps called absent turned out to be existing Wikidata items on
2026-08-25, and what settled them was not the name. The name search supplied a candidate; then
`P22` *father*, `P25` *mother*, `P26` *spouse* and `P40` *child* on the item were compared against
our tree's relatives for the same person. Helena Guttormsdatter matched on her father, her spouse
**Esbern Snare**, and two named children — none of which a label comparison could have produced.

Emma's framing of why this mattered at all: *"we didn't actually establish in any meaningful sense
that the people are absent in that chain... We might basically find that that one single daughter
is the only person absent in the line in Wikidata, but it's just that the Wikidata ones are not
genealogically linked."*

This does the same check over every candidate in `reports/spine-name-candidates.tsv`.

## How a relative is matched

Only by identifier, never by name — three routes, all exact:

* the relative carries a `P2600` *Geni.com profile ID* naming our relative,
* the relative is another chain step whose QID is already known,
* the relative appears in `reports/synoptic-correspondence.tsv` against our relative.

**A candidate is scored by how many DISTINCT relatives corroborate it**, and by nothing else. The
name that produced the candidate contributes zero to the score — it has already done its only job.

## What it will not do

* **It decides nothing.** `CLAUDE.md` deleted a module for using names to decide identity and it
  stays deleted. Rows with two or more corroborating relatives are worth Emma's glance; rows with
  none are named as name coincidences rather than quietly dropped.
* **It never writes to `reports/spine-already-on-wikidata.tsv`.** That file holds judged rows with
  the evidence spelled out; a script that appended to it automatically would turn a candidate into
  a conclusion by writing it down.

Writes `reports/spine-candidate-evidence.tsv` and prints the shortlist.
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

SLOTS = (("father", "p22"), ("mother", "p25"), ("spouses", "p26"), ("children", "p40"))

#: Two independent relatives is the bar for a human glance. One is a coincidence waiting to
#: happen -- a father called Knut in thirteenth-century Sweden narrows nothing.
WORTH_A_LOOK = 2


def split(cell):
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def main():
    cands = list(csv.DictReader(open(R / "spine-name-candidates.tsv", encoding="utf-8"),
                                delimiter="\t"))
    print(f"{len(cands):,} candidate rows over "
          f"{len({c['geni_id'] for c in cands})} people still called absent")

    fam = {}
    with open(R / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fam[row["geni_id"]] = row
    theirs = {}
    with open(ROOT / "out" / "wikidata" / "relations.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            theirs[row["qid"]] = row

    # ---- the correspondence, by every exact route we hold ----------------------------
    g2q = collections.defaultdict(set)
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0].startswith("Q") and row[1].strip().isdigit():
                g2q[row[1].strip()].add(row[0])
    syn = R / "synoptic-correspondence.tsv"
    if syn.exists():
        with open(syn, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                g2q[row["geni_id"]].add(row["qid"])
    # the chain's own known items, including the seven already judged
    for path, gcol, qcol in ((R / "spine-already-on-wikidata.tsv", "geni_id", "candidate_qid"),
                             (R / "garborg-qids.tsv", "geni_id", "qid")):
        if path.exists():
            with open(path, encoding="utf-8") as f:
                for row in csv.DictReader(f, delimiter="\t"):
                    g2q[row[gcol]].add(row[qcol])
    print(f"{len(g2q):,} Geni profiles we can point at an item, by exact identifier")

    names = {}
    with open(R / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            names[row["geni_id"]] = row["label_en"] or row["label_mul"]
    wlab = {}
    with open(ROOT / "out" / "wikidata" / "labels.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            wlab[row["qid"]] = (row["en"] or row["mul"] or row["sv"] or row["no"]
                                or row["nb"] or row["da"])

    out = []
    for c in cands:
        mine, their = fam.get(c["geni_id"]), theirs.get(c["candidate_qid"])
        if not mine or not their:
            continue
        hits = []
        for col, prop in SLOTS:
            stated = [x for x in (their.get(prop) or "").split(";") if x]
            if not stated:
                continue
            for rel in split(mine[col]):
                shared = g2q.get(rel, set()) & set(stated)
                if shared:
                    q = sorted(shared)[0]
                    hits.append(f"{col.rstrip('s')}: {names.get(rel, rel)} = "
                                f"{wlab.get(q, q)} {q}")
        if not hits:
            continue
        out.append({
            "step": c["step"], "geni_id": c["geni_id"], "our_name": c["our_name"],
            "candidate_qid": c["candidate_qid"], "candidate_label": c["candidate_label"],
            "corroborating_relatives": len(hits),
            "evidence": " · ".join(hits),
            "shared_words": c["shared_words"],
        })

    # ---- IS THE WINNER ALONE AT ITS SCORE? -------------------------------------------
    # **The check that step 18 needed and did not get.** It was recorded as near-certain on
    # "both parents match" -- and three sisters, Ingeborg `Q86458153`, Ingegerd `Q101247444`
    # and Ingrid `Q4955768`, each matched both parents. Evidence that every candidate shares
    # cannot choose between them, however convincing the row reads.
    #
    # This is the zipper's own rule, `mutually_unique`, applied to a judged file: an
    # assignment that is not unique proposes nothing. A candidate that ties on structure is
    # not thereby wrong -- it means the STRUCTURE did not decide, and whatever did (usually
    # the given name inside a closed sibling set) has to be named as the real evidence.
    best = {}
    for r in out:
        b = best.get(r["geni_id"], 0)
        best[r["geni_id"]] = max(b, r["corroborating_relatives"])
    at_best = collections.Counter(r["geni_id"] for r in out
                                  if r["corroborating_relatives"] == best[r["geni_id"]])
    for r in out:
        tied = at_best[r["geni_id"]]
        r["alone_at_this_score"] = ("yes" if tied == 1
                                    and r["corroborating_relatives"] == best[r["geni_id"]]
                                    else "")
        r["candidates_tied_at_top"] = tied if r["corroborating_relatives"] == best[r["geni_id"]] else ""

    out.sort(key=lambda r: (-r["corroborating_relatives"], int(r["step"])))
    with open(R / "spine-candidate-evidence.tsv", "w", encoding="utf-8", newline="") as f:
        if out:
            w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter="\t")
            w.writeheader()
            w.writerows(out)
        else:
            f.write("(no candidate has a single corroborating relative)\n")

    strong = [r for r in out if r["corroborating_relatives"] >= WORTH_A_LOOK]
    tied_top = sorted({r["geni_id"] for r in out
                       if r["corroborating_relatives"] == best[r["geni_id"]]
                       and at_best[r["geni_id"]] > 1})
    if tied_top:
        print("\nSTRUCTURE DID NOT DECIDE for these -- more than one candidate ties at the "
              "top score, so anything claiming otherwise is claiming more than it has:")
        for g in tied_top:
            rs = [r for r in out if r["geni_id"] == g
                  and r["corroborating_relatives"] == best[g]]
            print(f"   step {rs[0]['step']:>2}  {rs[0]['our_name'][:38]:<38} "
                  f"{len(rs)} candidates tied at {best[g]} relatives")
            for r in rs:
                print(f"        {r['candidate_label'][:52]:<52} {r['candidate_qid']}")

    print(f"\n{len(out)} candidates have at least one corroborating relative")
    print(f"{len(strong)} have {WORTH_A_LOOK} or more -- worth a human glance\n")
    for r in strong:
        print(f"  step {r['step']:>2}  {r['our_name'][:40]:<40} -> "
              f"{r['candidate_label'][:38]:<38} {r['candidate_qid']}")
        print(f"          {r['corroborating_relatives']} relatives: {r['evidence'][:150]}")

    seen = {r["geni_id"] for r in strong}
    print(f"\n{len(seen)} of the still-absent people have a candidate worth looking at")
    print("wrote reports/spine-candidate-evidence.tsv")
    print("\nNOTHING IS DECIDED. reports/spine-already-on-wikidata.tsv is written by hand, "
          "after a human looks.")


if __name__ == "__main__":
    main()
