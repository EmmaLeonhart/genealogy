"""Join a clan roster to Geni profiles through the About Me Wikidata link.

    python scripts/build-clan-p2600-pairs.py

**Emma, 2026-08-24:** *"the tanba onakatomi izumo stuff is a prerequisite for the synoptic
rebuild"* — these joins are **inputs** to `reports/synoptic-correspondence.tsv`, so
rebuilding the correspondence before they exist rebuilds it from incomplete data.

`reports/izumo-p2600-pairs.tsv` already existed and is a source. Tanba and Onakatomi had
rosters but no join, so their people were invisible to the synoptic tree even though they
carry Wikidata items.

**The join is the key Emma put there herself.** Every one of these profiles carries
`1 NOTE {geni:about_me} https://wikidata.org/wiki/Special:EntityPage/Q…` in the GEDCOM,
extracted corpus-wide into `reports/geni-qid-links.tsv`. Nothing here matches on a name:
`CLAUDE.md` § *Join on the Geni ID; do not search by name*, and the roster names differ
from the Geni ones constantly and legitimately — `Higashitakakage` against `Takakage
Azuma` is 東 read two ways.

**The sister repo's rosters carry no Geni IDs at all** — 0 of 298 Izumo, 0 of 185 Tanba,
0 of 101 Onakatomi. They supply the Wikidata side; the join can only come from the About
Me links.

Writes `reports/<clan>-p2600-pairs.tsv` for each clan that gains at least one pair.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent
SISTER = Path("C:/Users/Emma/Documents/GitHub/roster-extraction/data_lake")

#: The sister repo's rosters. `roster.tsv` is Izumo -- its raw wiki opens on the Izumo
#: genealogy -- and the other two are named.
ROSTERS = [
    ("tanba", SISTER / "roster.tanba.tsv"),
    ("onakatomi", SISTER / "roster.onakatomi.tsv"),
    ("izumo-sister", SISTER / "roster.tsv"),
]


def main():
    # geni_id -> qid, from the About Me link she wrote into each profile.
    qid_of = {}
    with open(ROOT / "reports" / "geni-qid-links.tsv", encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].startswith("Q"):
                qid_of[parts[0]] = parts[1]
    by_qid = collections.defaultdict(set)
    for geni_id, qid in qid_of.items():
        by_qid[qid].add(geni_id)
    print(f"{len(qid_of)} About Me links, {len(by_qid)} distinct QIDs")

    names = {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in qid_of:
                names[row["geni_id"]] = row["label_en"] or row["label_mul"] or ""

    for clan, path in ROSTERS:
        if not path.exists():
            print(f"{clan:<14} roster missing at {path}")
            continue
        with open(path, encoding="utf-8") as f:
            roster = list(csv.DictReader(f, delimiter="\t"))
        qids = [r["qid"].strip() for r in roster if (r.get("qid") or "").strip()]
        label_of = {r["qid"].strip(): (r.get("english") or "").strip()
                    for r in roster if (r.get("qid") or "").strip()}

        rows = []
        for qid in qids:
            hits = sorted(by_qid.get(qid, ()))
            if hits:
                rows.append({
                    "qid": qid,
                    "roster_name": label_of.get(qid, ""),
                    "geni_ids": ";".join(hits),
                    "geni_names": " | ".join(names.get(g, "") for g in hits),
                })

        print(f"{clan:<14} roster {len(qids):>4} QIDs -> {len(rows):>4} joined "
              f"({100 * len(rows) // max(len(qids), 1)}%)")
        if not rows:
            continue
        dest = ROOT / "reports" / f"{clan}-p2600-pairs.tsv"
        with open(dest, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
            w.writeheader()
            w.writerows(rows)
        print(f"               wrote {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
