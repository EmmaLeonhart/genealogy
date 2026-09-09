"""What Geni-to-Wikidata pairs does `order.life` hold that our correspondence does not?

    python scripts/measure-orderlife-pairs.py

**`order.life` is a THIRD SOURCE, not a thing to wait on.** `todo.md` carried it as
BLOCKED-ON-EXTERNAL — *"another agent is editing it right now"* — which was true when written
and blocked nothing: it is explicitly the last source to touch, and everything ahead of it was
unfinished. Emma ruled on 2026-08-27 that nothing in that list is blocked. Its last commit is
2026-08-19, so it is not in flux either.

## What it holds

`wikibase/analysis/persons.tsv`, 106,747 rows, with both a `wikidata_qid` and a `geni_id`
column — so it answers exactly the question `reports/synoptic-correspondence.tsv` answers, from
a different direction. **7,415 of its rows carry both**, which is the joinable population.

**The identifier question is already settled and negative.** Measured 2026-08-16: of 48,102
identifier claims on people who also have a Wikidata item, 46,802 were already stated and 12
were addable — order.life took them *from* Wikidata. This script asks the other question, about
the pairing itself rather than the claims hanging off it.

## The overlap is the guard

7,179 of the 7,415 pairs are ones we already hold. **That number existing at all is what says
the join works** — a Geni id joined on the wrong column, or read as an int, would produce a
clean-looking zero and the 236 would read as "order.life adds 7,415 people". `CLAUDE.md`
§ *An empty join is indistinguishable from an absence of data* has cost this repo five findings;
the script exits non-zero rather than report a difference it cannot vouch for.

Writes `reports/orderlife-pairs.tsv` — one row per pair we do not hold, classified by whether
either end is already known to us. **It emits no edits.** Whether an order.life pairing is
evidence enough to act on is a separate question from whether it exists.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
ORDERLIFE = ROOT.parent / "order.life" / "wikibase" / "analysis" / "persons.tsv"
OURS = ROOT / "reports" / "synoptic-correspondence.tsv"
OUT = ROOT / "reports" / "orderlife-pairs.tsv"

#: Below this share of order.life's joinable pairs appearing in ours, assume the join broke
#: rather than that order.life is full of people we have never seen. Measured share: 96.8%.
MIN_OVERLAP = 0.5


def orderlife_pairs():
    if not ORDERLIFE.exists():
        sys.exit(f"order.life is not on this machine at {ORDERLIFE}")
    pairs, rows = {}, 0
    with open(ORDERLIFE, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            rows += 1
            qid = (row.get("wikidata_qid") or "").strip()
            geni = (row.get("geni_id") or "").strip()
            if qid.startswith("Q") and geni.isdigit():
                pairs[(qid, geni)] = (row.get("label") or "").strip()
    return pairs, rows


def our_pairs():
    pairs, by_qid, by_geni = set(), collections.defaultdict(set), collections.defaultdict(set)
    with open(OURS, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            qid, geni = row["qid"].strip(), row["geni_id"].strip()
            pairs.add((qid, geni))
            by_qid[qid].add(geni)
            by_geni[geni].add(qid)
    return pairs, by_qid, by_geni


def main() -> None:
    theirs, their_rows = orderlife_pairs()
    ours, by_qid, by_geni = our_pairs()
    print(f"order.life: {their_rows:,} rows, {len(theirs):,} carrying both a QID and a Geni id")
    print(f"ours:       {len(ours):,} pairs in {OURS.name}")

    overlap = set(theirs) & ours
    share = len(overlap) / len(theirs) if theirs else 0
    print(f"overlap:    {len(overlap):,} ({share:.1%})")
    if share < MIN_OVERLAP:
        sys.exit(f"only {share:.1%} of order.life's pairs appear in ours — that is a broken "
                 f"join, not a discovery. Check the column names and that neither side has "
                 f"been read as an integer.")

    new = sorted(p for p in theirs if p not in ours)
    rows = []
    for qid, geni in new:
        known_qid, known_geni = qid in by_qid, geni in by_geni
        kind = ("both ends known, pairing new" if known_qid and known_geni else
                "QID known, Geni id new to us" if known_qid else
                "Geni id known, QID new to us" if known_geni else
                "both ends new to us")
        rows.append({
            "qid": qid, "geni_id": geni, "label": theirs[(qid, geni)], "kind": kind,
            # What WE already pair each end with — the thing that makes a row readable without
            # a second lookup, and the thing that makes a contradiction visible.
            "our_geni_ids_for_qid": " | ".join(sorted(by_qid.get(qid, ()))),
            "our_qids_for_geni_id": " | ".join(sorted(by_geni.get(geni, ()))),
        })

    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else
                           ["qid", "geni_id", "label", "kind", "our_geni_ids_for_qid",
                            "our_qids_for_geni_id"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"\n{len(new):,} pairs order.life holds and we do not:")
    for kind, n in collections.Counter(r["kind"] for r in rows).most_common():
        print(f"  {n:>5}  {kind}")
    print(f"\nwrote {OUT.resolve().relative_to(ROOT)} — a measurement, not a batch")


if __name__ == "__main__":
    main()
