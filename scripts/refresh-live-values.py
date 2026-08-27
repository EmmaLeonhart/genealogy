"""What each ledger item ALREADY states, by value, so the batch stops re-emitting it.

    BOT_CONTACT=you@example.com python scripts/refresh-live-values.py

**Emma, 2026-08-27**, on the relationship section never shrinking: *"the relationship one is
questionable that it's always gonna be so huge and growing."* Measured the same day: **229 of
306** statements on existing items in that day's batch were **already on Wikidata**. Only 77
were new. The section is three-quarters noise.

## Two defects, and the stale file is only one

* **`P40` *child*, `P26` *spouse* and `P3373` *sibling* were emitted with no check at all.**
  The additions loop tests `absent()` for `P22` *father* and `P25` *mother* and for nothing
  else, so every child link the ledger implies went out every single run.
* **`absent()` is property-level and stale.** `reports/garborg-live-state.tsv` records which
  *properties* an item carries, not which values, and was frozen at **2026-08-24**. Property
  level cannot tell a second father from an existing one; a frozen file cannot tell that Emma
  ran yesterday's batch.

This writes the missing half: `qid`, `property`, `value`, one row per statement actually on
the item, read through `genimerge.wikidata.full_entities` — whole items, never a summary, per
`CLAUDE.md` § *A SUMMARY of a Wikidata item is not the item*.

**QuickStatements merges a duplicate rather than failing on it**, which is exactly why this went
unnoticed: nothing broke, the batches were simply three-quarters things she had already done.

Writes `reports/garborg-live-values.tsv`.
"""
from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
LEDGER = ROOT / "reports" / "garborg-qids.tsv"
OUT = ROOT / "reports" / "garborg-live-values.tsv"

#: `full_entities` returns `{}` above this many ids rather than erroring, which reads as
#: "these items hold nothing" -- the absence-versus-broken-join trap. Chunked well under it.
CHUNK = 40


def main():
    if not os.environ.get("BOT_CONTACT", "").strip():
        sys.exit("BOT_CONTACT is not set; Wikimedia answers an empty User-Agent with a 403")
    from genimerge.wikidata import WikidataClient

    qids = sorted({r["qid"] for r in csv.DictReader(open(LEDGER, encoding="utf-8"),
                                                    delimiter="\t")
                   if (r.get("qid") or "").startswith("Q")})
    try:
        from genimerge import entities
        for r in entities.read_file(ROOT / "entity_resolution.md").resolutions:
            if r.qid:
                qids.append(r.qid)
    except Exception:                                               # noqa: BLE001
        pass
    qids = sorted(set(qids))
    print(f"{len(qids)} items to read")

    client = WikidataClient(ROOT / "out" / "wikidata" / "livecache")
    items = {}
    for i in range(0, len(qids), CHUNK):
        items.update(client.full_entities(qids[i:i + CHUNK]))
        print(f"  {min(i + CHUNK, len(qids))}/{len(qids)}", flush=True)
    if not items:
        sys.exit("no items came back at all -- that is a broken fetch, not empty items")
    print(f"{len(items)} of {len(qids)} fetched")

    rows = []
    for qid, item in sorted(items.items()):
        for prop, statements in sorted(item.get("claims", {}).items()):
            for st in statements:
                if st.get("rank") == "deprecated":
                    continue
                v = st.get("mainsnak", {}).get("datavalue", {}).get("value")
                if isinstance(v, dict):
                    value = v.get("id") or v.get("text") or (
                        v["time"].split("T")[0] if v.get("time") else "")
                elif isinstance(v, str):
                    value = v
                else:
                    value = ""
                if value:
                    rows.append({"qid": qid, "property": prop, "value": value})

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["qid", "property", "value"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"\n{len(rows):,} statements over {len(items)} items "
          f"-> {OUT.resolve().relative_to(ROOT)}")


if __name__ == "__main__":
    main()
