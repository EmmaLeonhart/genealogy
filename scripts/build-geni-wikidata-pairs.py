"""Pair Geni profiles with Wikidata items from the `wikidata.org/wiki/Q...` links
Emma put in their Geni `about_me`, and emit the `add_geni_id` batch.

**These pairs are hand-curated identity claims, not inference.** Somebody wrote
the Wikidata URL onto the Geni profile. That is the same kind of evidence as
`entity_resolution.md` and it is the only thing in this repo that can link an
item carrying no P2600 to a Geni profile.

The QID is taken from the individual's own record, so the pairing is exact:
profile ID from the xref, item from the URL inside that record. No name matching.

Each pair is then checked against the local Wikidata store, offline:

* the item already carries this Geni ID  -> nothing to do
* the item carries a *different* Geni ID -> **emitted as an ADDITIONAL P2600**
* the item is absent from the store      -> still emitted; the store is a
  Geni-seeded slice and an unlinked item is exactly what falls outside it

**A second Geni ID on one item is normal and permanent, not a conflict.**
Emma, 2026-08-14: *"it is impossible to merge these geni profiles, simple as
that."* Geni forbids connecting biblical people to living people, so users
repeatedly create fresh biblical profiles and attach their own lines to those.
The duplicates cannot be merged and will keep appearing. Aaron has two
(`6000000000792907064` and `6000000227239142939`); Zerubbabel has two
(`6000000000961704850` and `6000000206646432835`).

P2600 takes multiple values — the local store already counts **2861 items
carrying more than one Geni ID** — so the correct edit is to add the second
statement, never to replace the first. That is also CLAUDE.md § *The purpose is
to ADD to Wikidata, not to correct it*: prefer a second statement cited to Geni
over editing an existing one.

    py scripts/build-geni-wikidata-pairs.py
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import sources  # noqa: E402

INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
QID_URL = re.compile(r"wikidata\.org/wiki/(Q\d+)")
INDI = re.compile(r"^0 @I(\d+)@ INDI")


def scan(path: Path) -> dict[str, dict]:
    """geni_id -> {qids, name, occu}. A record's QIDs are its own."""
    found: dict[str, dict] = {}
    cur = None
    for raw in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        m = INDI.match(raw)
        if m:
            cur = m.group(1)
            continue
        if raw.startswith("0 "):
            cur = None
            continue
        if cur is None:
            continue
        rec = found.setdefault(cur, {"qids": set(), "name": "", "occu": ""})
        if raw.startswith("1 NAME ") and not rec["name"]:
            rec["name"] = raw[7:].strip()
        elif raw.startswith("1 OCCU "):
            rec["occu"] = raw[7:].strip()
        for q in QID_URL.findall(raw):
            rec["qids"].add(q)
    return {g: r for g, r in found.items() if r["qids"]}


def store_geni_ids(qids: set[str]) -> dict[str, list[str]]:
    """qid -> the Geni IDs the local store has on it. Missing qid = absent."""
    if not INDEX.exists():
        return {}
    conn = sqlite3.connect(INDEX)
    out: dict[str, list[str]] = {}
    for q in qids:
        rows = conn.execute("select geni_id from geni where qid=?", (q,)).fetchall()
        if conn.execute("select 1 from items where qid=?", (q,)).fetchone():
            out[q] = [r[0] for r in rows]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv-out", default="reports/geni-wikidata-pairs.csv")
    ap.add_argument("--batch-out", default="reports/wikidata-add-geni-id.json")
    args = ap.parse_args()

    merged: dict[str, dict] = {}
    for path in sources.find_exports():
        for g, rec in scan(path).items():
            m = merged.setdefault(g, {"qids": set(), "name": "", "occu": "",
                                      "exports": set()})
            m["qids"] |= rec["qids"]
            m["name"] = m["name"] or rec["name"]
            m["occu"] = m["occu"] or rec["occu"]
            m["exports"].add(str(path.relative_to(REPO)))
    print(f"{len(merged)} Geni profiles carry a Wikidata URL")

    all_qids = {q for r in merged.values() for q in r["qids"]}
    known = store_geni_ids(all_qids)
    print(f"{len(all_qids)} distinct items; {len(known)} of them are in the local store")

    rows, batch, duplicates = [], [], []
    for g, rec in sorted(merged.items()):
        for q in sorted(rec["qids"]):
            in_store = q in known
            on_item = known.get(q, [])
            if g in on_item:
                status = "already linked"
            elif on_item:
                status = (f"additional P2600 - item already carries "
                          f"{','.join(on_item)}, unmergeable Geni duplicate")
                duplicates.append((g, q, on_item))
            elif in_store:
                status = "in store, no Geni ID -> add"
            else:
                status = "not in local store -> add"
            rows.append({
                "geni_id": g, "qid": q, "name": rec["name"], "occupation": rec["occu"],
                "in_local_store": "yes" if in_store else "no",
                "item_geni_ids": " ".join(on_item), "status": status,
                "exports": " ".join(sorted(rec["exports"])),
            })
            if status.startswith(("in store", "not in", "additional")):
                batch.append({
                    # The Geni id is in the name because one QID can carry two
                    # of them -- `Q694696` does -- and `P2600` is multi-valued, so
                    # both edits are correct while one name for both is not.
                    "id": f"add_geni_id:{q}:{g}",
                    "type": "add_geni_id",
                    "priority": False,
                    "subject": {"qid": q, "geni_id": g},
                    "requires": [],
                    "statement": {"property": "P2600", "value": g, "references": []},
                    "note": rec["name"],
                })

    out = REPO / args.csv_out
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["geni_id"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out} ({len(rows)} rows)")

    b = REPO / args.batch_out
    b.write_text(json.dumps(batch, indent=1, ensure_ascii=False) + "\n",
                 encoding="utf-8")
    print(f"wrote {b} ({len(batch)} add_geni_id entries)")

    qs = b.with_suffix(".qs")
    qs.write_text("\n".join(
        f'{e["subject"]["qid"]}\tP2600\t"{e["subject"]["geni_id"]}"' for e in batch
    ) + "\n", encoding="utf-8")
    print(f"wrote {qs}")

    if duplicates:
        print(f"\n{len(duplicates)} items get an ADDITIONAL P2600 "
              f"(unmergeable Geni duplicates, not conflicts):")
        for g, q, on in duplicates:
            print(f"  {q} already carries {on}; adding {g} alongside it")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
