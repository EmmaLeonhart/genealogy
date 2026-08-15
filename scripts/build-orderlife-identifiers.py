"""order.life's genealogy identifiers that Wikidata lacks, as edit objects.

Queue item 6. Emma, 2026-08-15: *"look over all the order.life properties that
might be novel"* — and the ones from **P155 up are not novel at all**. They carry
the same number and the same meaning as Wikidata's, because order.life allocated
them by copying Wikidata's numbering above its own local block.
`reports/orderlife-properties.md` establishes that split.

**The premise turned out to be wrong, and that is this script's main result.**
`queue.md` called it *"the easiest remaining win… values Wikidata often lacks, on
items that already exist"*. Measured: of **48,102** identifier claims order.life
holds on people who also have a Wikidata item, **42,727 (89%) are already stated
on Wikidata** and **10** are addable. That is not a surprise once stated plainly —
order.life took these identifiers *from* Wikidata, which is also why the property
numbers match.

**Only `external-id` properties are emitted, and that is a deliberate narrowing.**
55 properties are numbered P155 or above and 45 of those are `external-id`; **27
carry any values at all**, of which 21 are `external-id`. The other six:
* **`P155` follows, `P156` followed by, `P460` said to be the same as** are
  `wikibase-item`, and their values are **order.life QIDs**, which mean something
  else entirely on Wikidata. `reports/orderlife-properties.md` calls this the
  worse of the two traps. 9 claims reach a person with a QID; none are emitted.
* **`P1317` floruit** is a time value in order.life's own format (20 people), and
  **`P1813` short name** / **`P1814` name in kana** are text. Left for the
  modelling that handles dates and labels; counted in the report, not emitted.

**Every candidate is checked against the local Wikidata store before it is
emitted**, so an identifier the item already states produces nothing. That check
is offline — `CLAUDE.md` § *Never query Wikidata to check something* — and an
item that is not in the store cannot be checked, so it is reported separately
rather than emitted blind.

**Citation.** order.life is not a source Wikidata knows, so a statement here
carries a `P2600` Geni reference when the person has a Geni ID and **no reference
at all** when they do not — the same rule as `build-orderlife-batch`, and for the
same reason: a reference to a source that does not exist makes the whole
statement unusable.

Writes `reports/wikidata-orderlife-identifiers.json` and a CSV of every candidate
including the ones held back.

    py scripts/build-orderlife-identifiers.py
"""

from __future__ import annotations

import argparse
import csv
import glob
import gzip
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import wikistore  # noqa: E402

OL = REPO / "orderlife"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
STORE = REPO / "wikidata" / "items"
JSON_OUT = REPO / "reports" / "wikidata-orderlife-identifiers.json"
CSV_OUT = REPO / "reports" / "orderlife-identifiers.csv"

#: order.life's own numbering stops below this; at and above it the numbers are
#: Wikidata's. See `reports/orderlife-properties.md`.
MIRRORED_FROM = 155

GENI_PROPERTY = "P2600"


def property_table() -> dict[str, tuple[str, str]]:
    out = {}
    for f in glob.glob(str(OL / "properties" / "*.json")):
        pid = os.path.basename(f)[:-5]
        d = json.load(open(f, encoding="utf-8"))
        lab = (d.get("labels") or {}).get("en")
        out[pid] = ((lab or {}).get("value") if isinstance(lab, dict) else lab or "",
                    d.get("datatype") or "")
    return out


def geni_reference(geni_id: str, retrieved: str) -> list[dict]:
    return [{"property": "P854",
             "value": f"https://www.geni.com/people/x/{geni_id}"},
            {"property": "P813", "value": f"+{retrieved}T00:00:00Z/11"}]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--retrieved", default="2026-08-15")
    args = ap.parse_args()

    props = property_table()
    high = {p for p in props if int(p[1:]) >= MIRRORED_FROM}
    emittable = {p for p in high if props[p][1] == "external-id"}
    print(f"{len(high)} properties from P{MIRRORED_FROM} up, "
          f"{len(emittable)} of them external-id")

    # order.life qid -> (wikidata qid, geni id)
    ids: dict[str, tuple[str, str]] = {}
    with (OL / "analysis" / "persons.tsv").open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE):
            w = (r.get("wikidata_qid") or "").strip()
            if w.startswith("Q") and w[1:].isdigit():
                ids[r["qid"]] = (w, (r.get("geni_id") or "").strip())
    print(f"{len(ids):,} order.life persons carry a Wikidata QID")

    # Gather candidates: (wikidata qid, property, value, geni id, ol qid)
    candidates = []
    skipped_kind: Counter = Counter()
    for path in sorted(glob.glob(str(OL / "items" / "items-*.jsonl.gz"))):
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            for line in fh:
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                q = item.get("id")
                target = ids.get(q)
                if not target:
                    continue
                claims = item.get("claims") or {}
                for prop in high & claims.keys():
                    for st in claims[prop]:
                        snak = st.get("mainsnak") or {}
                        if snak.get("snaktype") != "value":
                            continue
                        value = snak.get("datavalue", {}).get("value")
                        if prop not in emittable:
                            skipped_kind[props[prop][1]] += 1
                            continue
                        if not isinstance(value, str) or not value:
                            continue
                        candidates.append((target[0], prop, value, target[1], q))
    print(f"{len(candidates):,} external-id candidates on people with a QID")

    # What does the store already say? Offline, and an item we do not hold is
    # reported rather than guessed at.
    wanted = sorted({c[0] for c in candidates})
    have: dict[str, dict[str, set[str]]] = {}
    seen: set[str] = set()
    with wikistore.StoreReader(STORE, INDEX) as reader:
        for qid, entity in reader.entities(wanted).items():
            seen.add(qid)
            claims = entity.get("claims") or {}
            per: dict[str, set[str]] = defaultdict(set)
            for prop in high:
                for st in claims.get(prop) or []:
                    snak = st.get("mainsnak") or {}
                    if snak.get("snaktype") == "value":
                        v = snak.get("datavalue", {}).get("value")
                        if isinstance(v, str):
                            per[prop].add(v)
            have[qid] = per
    print(f"{len(seen):,} of {len(wanted):,} target items are in the local store")

    rows, edits = [], []
    verdicts: Counter = Counter()
    by_prop: Counter = Counter()
    # **Dedupe on the edit, not on the source row.** Several order.life items can
    # carry the same Wikidata QID - they are separate people there and one person
    # here - so the same identifier arrives more than once. The first run emitted
    # 30 edits for 10 distinct (item, property, value) triples, which would have
    # added the same statement three times.
    emitted: set = set()
    for qid, prop, value, geni_id, ol_qid in candidates:
        if qid not in seen:
            verdict = "item not in the local store - cannot check"
        elif value in have.get(qid, {}).get(prop, ()):
            verdict = "already stated"
        elif have.get(qid, {}).get(prop):
            verdict = "item states a DIFFERENT value for this property"
        else:
            verdict = "addable"
        verdicts[verdict] += 1
        rows.append({"wikidata_qid": qid, "property": prop,
                     "label": props[prop][0], "value": value,
                     "geni_id": geni_id, "orderlife_qid": ol_qid,
                     "verdict": verdict})
        if verdict != "addable":
            continue
        key = (qid, prop, value)
        if key in emitted:
            verdicts["addable (duplicate of another order.life item)"] += 1
            verdicts["addable"] -= 1
            rows[-1]["verdict"] = "addable, but already emitted for this item"
            continue
        emitted.add(key)
        by_prop[prop] += 1
        edits.append({
            "id": f"orderlife_identifier:{ol_qid}:{prop}",
            "type": "add_statement",
            "source": "order.life",
            "subject": {"qid": qid, "geni_id": geni_id or None,
                        "orderlife_qid": ol_qid},
            "requires": [],
            "statements": [{
                "property": prop,
                "value": value,
                "references": geni_reference(geni_id, args.retrieved) if geni_id else [],
            }],
        })

    JSON_OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1),
                        encoding="utf-8")
    with CSV_OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    print(f"\nwrote {JSON_OUT} ({len(edits):,} add_statement edits)")
    print(f"wrote {CSV_OUT} ({len(rows):,} candidates, addable and not)\n")
    for v, n in verdicts.most_common():
        print(f"  {n:>7,}  {v}")
    print("\naddable by property:")
    for p, n in by_prop.most_common():
        print(f"  {n:>7,}  {p} {props[p][0]}")
    if skipped_kind:
        print("\nheld back by datatype, none emitted:")
        for dt, n in skipped_kind.most_common():
            print(f"  {n:>7,}  {dt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
