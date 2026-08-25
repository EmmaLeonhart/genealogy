"""Judge the structural walk's pairings by dates — the one independent signal we have.

    python scripts/validate-structural-walk.py

**Emma, 2026-08-24:** *"It's not clear to me that you've ever been doing the zipper join
correctly, especially since you never really explain how it is that you're doing it."*

`docs/structural-walk.md` is the explanation. This is the check.

**Why dates and not something else.** The walk pairs people by *position* alone — our
father against the item's `P22` — consulting no name and no date. So dates are independent
of how the pairing was made and can judge it. Two other signals were tried and neither
works:

* **`P2600` as ground truth is biased by construction.** The walk only proposes a pair
  when our person's QID is missing or does not match, so anyone with a usable `P2600` is
  excluded. The handful that remain checkable are exactly the disagreements, which is why
  they score 1.3% and why that number must never be quoted as precision.
* **Name-token overlap measures orthography.** `Regintrude` ↔ `Ragnétrude`, `Katarzyna` ↔
  `Catherine`, `Siemomysł` ↔ `Siemomysl` — the last differing only by `ł`.

**`TOLERANCE_YEARS` is 15 and it is deliberately loose.** Geni and Wikidata disagree about
medieval dates constantly and legitimately; the aim is to catch pairings that are
*impossible*, not ones that are merely inconsistent. `Eric Jedvardsson of Sweden IX`
(1120–1160) paired with `Sigurd Snake-in-the-Eye` (801–891) is three centuries out. A
five-year difference is one person recorded twice, which is the ordinary case.

**A `conflict` verdict does not authorise deletion.** It marks a pair that cannot be right
and should not be emitted from. `unknown` is the largest population and means only that we
hold no dates to judge with — never that the pair is good.

Writes `reports/structural-walk-validation.tsv`.
"""
from __future__ import annotations

import collections
import csv
import gzip
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "wikidata" / "items"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"

#: Loose on purpose — see the module docstring.
TOLERANCE_YEARS = 15


def wikidata_years(qids):
    """`{qid: (birth, death)}` as ints, read once per shard."""
    con = sqlite3.connect(str(INDEX))
    by_shard = collections.defaultdict(set)
    for qid in qids:
        hit = con.execute("SELECT shard FROM items WHERE qid=?", (qid,)).fetchone()
        if hit:
            by_shard[hit[0]].add(qid)

    out = {}
    for shard, wanted in by_shard.items():
        path = STORE / f"items-{shard:05d}.jsonl.gz"
        if not path.exists():
            continue
        with gzip.open(path, "rt", encoding="utf-8") as f:
            for line in f:
                for qid in list(wanted):
                    if f'"{qid}"' not in line:
                        continue
                    item = json.loads(line)
                    if item.get("id") == qid:
                        def year(prop):
                            for st in item.get("claims", {}).get(prop, []):
                                t = (st["mainsnak"].get("datavalue", {})
                                     .get("value", {}).get("time", ""))
                                if t:
                                    # `+1120-00-00T…` / `-0801-…`; keep the sign.
                                    sign = -1 if t.startswith("-") else 1
                                    digits = t[1:5]
                                    return sign * int(digits) if digits.isdigit() else None
                            return None
                        out[qid] = (year("P569"), year("P570"))
                    wanted.discard(qid)
                    break
    return out


def main():
    with open(ROOT / "reports" / "structural-correspondence.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"{len(rows):,} structural correspondences")

    geni_ids = {r["geni_id"] for r in rows}
    geni_years = {}
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] not in geni_ids:
                continue
            def year(key):
                v = (row.get(key) or "").strip()
                return int(v) if v.lstrip("-").isdigit() else None
            geni_years[row["geni_id"]] = (year("birth_date_year"),
                                          year("death_date_year"))

    wd = wikidata_years({r["qid"] for r in rows})
    print(f"dates read for {len(wd):,} Wikidata items")

    out, tally = [], collections.Counter()
    for r in rows:
        ours = geni_years.get(r["geni_id"], (None, None))
        theirs = wd.get(r["qid"], (None, None))
        gaps = [abs(a - b) for a, b in zip(ours, theirs) if a is not None and b is not None]
        if not gaps:
            verdict, gap = "unknown", ""
        elif min(gaps) <= TOLERANCE_YEARS:
            verdict, gap = "agree", min(gaps)
        else:
            verdict, gap = "conflict", min(gaps)
        tally[verdict] += 1
        out.append({
            "verdict": verdict,
            "years_apart": gap,
            "geni_id": r["geni_id"],
            "geni_name": r["geni_name"],
            "geni_years": "-".join(str(x) if x is not None else "?" for x in ours),
            "qid": r["qid"],
            "wikidata_label": r["wikidata_label"],
            "wikidata_years": "-".join(str(x) if x is not None else "?" for x in theirs),
            "position": r["position"],
            "anchor_name": r.get("anchor_name", ""),
        })

    out.sort(key=lambda r: (r["verdict"] != "conflict",
                            -(r["years_apart"] or 0)))
    dest = ROOT / "reports" / "structural-walk-validation.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter="\t")
        w.writeheader()
        w.writerows(out)

    judged = tally["agree"] + tally["conflict"]
    print(f"\nwrote {dest.relative_to(ROOT)}")
    for k in ("agree", "conflict", "unknown"):
        print(f"   {tally[k]:>6}  {k}")
    if judged:
        print(f"\nof the {judged:,} with comparable dates, "
              f"{100 * tally['agree'] / judged:.0f}% agree")
    print(f"{tally['unknown']:,} cannot be judged — no dates, not a clean bill of health")
    print("\nworst conflicts:")
    for r in out[:8]:
        if r["verdict"] != "conflict":
            break
        print(f"   {r['years_apart']:>4}y  {r['geni_name'][:30]:<30} {r['geni_years']:<11}"
              f" <-> {r['wikidata_label'][:28]:<28} {r['wikidata_years']}")


if __name__ == "__main__":
    main()
