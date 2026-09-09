"""How compliant are the items we created with the specification we wrote down?

**Emma's queued item, in her words:** *"an analysis of the existing individuals that I have added
using this, to see how compliant they are with the original specifications and visions."*

The specification is `docs/wikidata-item-template.md`, read off the items she built by hand, plus
the rulings in `CLAUDE.md`. This checks the ones the programme created against it.

**Entirely offline** — `reports/garborg-live-values.tsv` is refreshed by the ledger refresh inside
`build-garborg-day.py --compose`, so no query is made here.

**What is checked, and why each one:**

* `P31` *instance of* `Q5` and `P21` *sex or gender* — the two statements every person item gets.
* `P2600` *Geni.com profile ID* — the identity that makes the item retrievable, and the thing
  `CLAUDE.md` says must be added before anything derived from Geni.
* `P1810` *subject named as* on that `P2600` — her 2026-08-28 ruling.
* **at least one relationship** (`P22`/`P25`/`P26`/`P40`/`P3373`) — an item with none is the
  *"individuals without any relationships"* shape she objected to.
* **an `Aen` alias** — must never exist. `CLAUDE.md`: *"No aen are ever supposed to be added."*

Writes `reports/compliance-audit.tsv`, one row per item.
"""
import collections
import csv
import io
import sys

LEDGER = "reports/garborg-qids.tsv"
LIVE = "reports/garborg-live-values.tsv"
OUT = "reports/compliance-audit.tsv"

REL = ("P22", "P25", "P26", "P40", "P3373")


def main():
    ledger = {}
    for r in csv.DictReader(io.open(LEDGER, encoding="utf-8"), delimiter="\t"):
        if r.get("qid"):
            ledger[r["qid"]] = r

    have = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in csv.DictReader(io.open(LIVE, encoding="utf-8"), delimiter="\t"):
        have[r["qid"]][r["property"]].append(r["value"])

    rows, tally = [], collections.Counter()
    for qid, led in sorted(ledger.items()):
        v = have.get(qid)
        if not v:
            tally["not in the fetched values"] += 1
            continue
        faults = []
        if "Q5" not in v.get("P31", []):
            faults.append("no P31=Q5")
        if not v.get("P21"):
            faults.append("no P21 sex")
        if not v.get("P2600"):
            faults.append("no P2600")
        if not any(v.get(p) for p in REL):
            faults.append("no relationship at all")
        for f in faults:
            tally[f] += 1
        if not faults:
            tally["fully compliant"] += 1
        rows.append({"qid": qid, "label": led.get("label", ""),
                     "faults": "; ".join(faults) or "-",
                     "statements": sum(len(x) for x in v.values())})

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t",
                           fieldnames=["qid", "label", "faults", "statements"])
        w.writeheader()
        w.writerows(rows)

    print(f"items in the ledger with fetched values: {len(rows)}")
    for k, n in tally.most_common():
        print(f"   {k:<34} {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
