"""How many people have we CREATED on Wikidata carrying a marker as their surname?

**Emma, 2026-08-29**, on finding `Q141217396` labelled *Maria No name*:
*"Like us to do some level of audit to see the degree that we've created individuals with
that error."*

The defect is in `labels.is_marker_label`, which tests the whole label or a LEADING marker
and never a trailing one. Geni writes the unknown-name marker into `SURN`, which lands at
the end, so `Maria /No name/` is emitted verbatim as a label while `unknown Bloomfield` is
caught.

Entirely offline: the ledger, `reports/display-names.csv`, `reports/derived-labels.csv`.
Writes `reports/marker-surname-audit.tsv`.
"""
import csv
import io
import sys

sys.path.insert(0, "scripts")
import labels  # noqa: E402

LEDGER = "reports/garborg-qids.tsv"
NAMES = "reports/display-names.csv"
DERIVED = "reports/derived-labels.csv"
OUT = "reports/marker-surname-audit.tsv"


def main():
    ledger = {}
    for r in csv.DictReader(io.open(LEDGER, encoding="utf-8"), delimiter="\t"):
        if r.get("qid"):
            ledger[r["geni_id"]] = r

    # every person in the corpus whose SURNAME is a marker but whose whole label is not,
    # which is exactly the population is_marker_label misses
    afflicted = {}
    for row in csv.reader(io.open(NAMES, encoding="utf-8")):
        if len(row) < 11:
            continue
        geni, raw, display, surn = row[0], row[3], row[4], row[10]
        if not surn or not labels.is_marker_label(surn):
            continue
        if labels.is_marker_label(display):
            continue          # already caught by the whole-label test
        afflicted[geni] = (raw, display, surn)

    emitted = {}
    for r in csv.DictReader(io.open(DERIVED, encoding="utf-8")):
        if r["geni_id"] in afflicted:
            emitted[r["geni_id"]] = (r.get("label_en") or "", r.get("label_mul") or "")

    rows = []
    for geni, (raw, display, surn) in sorted(afflicted.items()):
        led = ledger.get(geni)
        rows.append({
            "geni_id": geni,
            "qid": (led or {}).get("qid", ""),
            "on_wikidata": "yes" if led else "no",
            "ours": ("yes" if led and "added to an existing item" not in (led.get("note") or "")
                     else ("no" if led else "")),
            "raw_name": raw,
            "marker_surname": surn,
            "our_label_en": emitted.get(geni, ("", ""))[0],
            "our_label_mul": emitted.get(geni, ("", ""))[1],
            "wikidata_label": (led or {}).get("label", ""),
        })

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    live = [r for r in rows if r["on_wikidata"] == "yes"]
    ours = [r for r in live if r["ours"] == "yes"]
    bad = [r for r in live if labels.is_marker_label(r["wikidata_label"]) is False
           and r["wikidata_label"] and r["wikidata_label"] == r["our_label_mul"]]
    print(f"corpus people with a marker in the surname slot : {len(rows):,}")
    print(f"  ...of those, HAVE a Wikidata item             : {len(live)}")
    print(f"  ...of those, items WE created                 : {len(ours)}")
    print(f"  ...whose Wikidata label is still our bad form : {len(bad)}")
    print()
    for r in live[:25]:
        flag = "OURS" if r["ours"] == "yes" else "pre-existing"
        print(f"  {r['qid']:<12} {r['wikidata_label'][:34]:<34} "
              f"raw={r['raw_name'][:26]:<26} {flag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
