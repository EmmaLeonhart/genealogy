"""What is in `order.life` that is not in this project's tree.

**Not a merge, and not a synoptic tree.** Emma, 2026-08-14: the synoptic tree is
already built and she does not want another one — she wants to know *what the
order.life repository holds that this one does not*. This produces that list and
stops.

**order.life is a Wikibase carrying two different kinds of thing in one graph.**
Its `Q1` is "Aster / Our Greatest Grandmother", dated −13,000,000,000: the Gaiad
epic's cosmological root. Real genealogy and invented genealogy share the same
item space, so **tree shape cannot be used to tell them apart**. The only
anchors to reality are the two identifier columns its own export carries:

* `geni_id`     — a Geni profile ID, joinable against this repo's corpus exactly
* `wikidata_qid`— a Wikidata QID, joinable against the local store exactly

Everything with neither is local to order.life and this script says so rather
than guessing what it is.

Source: `order.life/wikibase/analysis/persons.tsv`.

    py scripts/build-orderlife-diff.py
"""

from __future__ import annotations

import argparse
import csv
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from genimerge import sources  # noqa: E402

ORDERLIFE = Path("C:/Users/Emma/Documents/GitHub/order.life")
PERSONS = ORDERLIFE / "wikibase" / "analysis" / "persons.tsv"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
INDI = re.compile(r"^0 @I(\d+)@ INDI")


def corpus_geni_ids() -> set[str]:
    ids: set[str] = set()
    paths = sources.find_exports()
    for n, path in enumerate(paths, 1):
        with path.open(encoding="utf-8-sig", errors="replace") as fh:
            for raw in fh:
                m = INDI.match(raw)
                if m:
                    ids.add(m.group(1))
        if n % 40 == 0:
            print(f"  read {n}/{len(paths)} exports, {len(ids):,} profiles")
    return ids


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="reports/orderlife-diff.csv")
    args = ap.parse_args()

    if not PERSONS.exists():
        raise SystemExit(f"no persons.tsv at {PERSONS}")

    # `quoting=QUOTE_NONE`: a `"` in an order.life label is literal data, not an
    # opening quote. The default swallowed 128 rows of this file, merging each
    # with the row after it. See `build-orderlife-batch.read_tsv`.
    rows = list(csv.DictReader(PERSONS.open(encoding="utf-8", newline=""),
                               delimiter="\t", quoting=csv.QUOTE_NONE))
    print(f"{len(rows):,} persons in order.life")

    ours = corpus_geni_ids()
    print(f"{len(ours):,} distinct Geni profiles in this corpus")

    store_qids: set[str] = set()
    store_linked: set[str] = set()
    if INDEX.exists():
        conn = sqlite3.connect(INDEX)
        store_qids = {r[0] for r in conn.execute("select qid from items")}
        store_linked = {r[0] for r in conn.execute("select qid from geni")}
    print(f"{len(store_qids):,} items in the local Wikidata store, "
          f"{len(store_linked):,} of them carrying a Geni ID")

    out_rows = []
    counts = {}
    for r in rows:
        gid = (r.get("geni_id") or "").strip()
        qid = (r.get("wikidata_qid") or "").strip()
        if gid and gid in ours:
            bucket = "held: geni id in our corpus"
        elif gid:
            bucket = "MISSING: has a geni id we have never exported"
        elif qid and qid in store_linked:
            bucket = "held via wikidata: item carries a geni id we may hold"
        elif qid and qid in store_qids:
            bucket = "MISSING: on wikidata, no geni link, not in our tree"
        elif qid:
            bucket = "MISSING: wikidata qid outside our store"
        else:
            bucket = "order.life only: no geni id and no wikidata qid"
        counts[bucket] = counts.get(bucket, 0) + 1
        out_rows.append({
            "orderlife_qid": r.get("qid", ""),
            "label": r.get("label", ""),
            "birth": r.get("birth", ""),
            "death": r.get("death", ""),
            "gedcom_name": r.get("gedcom", ""),
            "wikidata_qid": qid,
            "geni_id": gid,
            "bucket": bucket,
        })

    p = REPO / args.out
    with p.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0]))
        w.writeheader()
        w.writerows(out_rows)
    print(f"\nwrote {p} ({len(out_rows):,} rows)\n")
    for b, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:>7,}  {b}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
