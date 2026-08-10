"""Full-store count of the Geni-linked Wikidata items with no family at all — queue item 3.A.

`reports/wikidata-isolates.md` answered this from 24 of 1,408 shards because a
full pass was banned for laptop heat at the time. Every figure in it is a sample
proportion. This is the full count, and it exists as a committed script rather
than an ad-hoc pass because the sample's own `out/_isolates.json` was lost with
`out/` in the 2026-08-09 re-clone and could not be regenerated.

**The distinction is the whole point** (`queue.md` 2.E). Among items carrying a
Geni ID:

* **true isolate** — no P22/P25/P26/P40/P3373 statement whatsoever;
* **looks isolated** — has relation statements, but every target is a QID the
  download never fetched;
* **connected** — at least one relation target is an item we hold.

The middle case is the one that would have made 183,296 an artifact of stopping
the download early. The sample found zero of them in 9,000; this settles it over
the whole store.

Offline: one pass over `wikidata/items/`, plus the index for the set of QIDs we
hold and `out/merged.ged` for the Geni IDs in our tree. No network.

Also writes `out/_isolates.json` for `scripts/build-isolates-page.py`, since the
rows are already in hand on this pass and rebuilding them separately would mean
reading 2.7 GB twice.
"""

from __future__ import annotations

import io
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import wikistore  # noqa: E402
from genimerge.identity import GENI_ID_RE  # noqa: E402
from genimerge.wikidownload import relatives  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "wikidata" / "items"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"
MERGED = ROOT / "out" / "merged.ged"


def stored_qids(index: Path) -> set[str]:
    conn = sqlite3.connect(str(index))
    try:
        return {row[0] for row in conn.execute("SELECT qid FROM items")}
    finally:
        conn.close()


def tree_geni_ids(merged: Path) -> set[str]:
    ids: set[str] = set()
    with io.open(merged, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("0 @I"):
                continue
            match = GENI_ID_RE.match(line.split(" ", 2)[1].strip())
            if match:
                ids.add(match.group("geni_id"))
    return ids


def _year(entity: dict, prop: str) -> str:
    for statement in (entity.get("claims") or {}).get(prop) or []:
        snak = statement.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        value = (snak.get("datavalue") or {}).get("value")
        time = value.get("time") if isinstance(value, dict) else None
        if isinstance(time, str) and len(time) > 5:
            sign, rest = time[0], time[1:5]
            try:
                year = int(rest)
            except ValueError:
                continue
            return f"-{year}" if sign == "-" else str(year)
    return ""


def _label(entity: dict) -> str:
    labels = entity.get("labels") or {}
    for lang in ("en", "mul"):
        value = (labels.get(lang) or {}).get("value")
        if value:
            return value
    for entry in labels.values():
        value = (entry or {}).get("value")
        if value:
            return value
    return ""


def main() -> int:
    for path in (INDEX, MERGED):
        if not path.exists():
            print(f"{path} not found", file=sys.stderr)
            return 1

    held = stored_qids(INDEX)
    ours = tree_geni_ids(MERGED)
    print(f"index: {len(held):,} QIDs held; tree: {len(ours):,} Geni IDs")

    shards = wikistore.shards(STORE)
    items = geni_linked = connected = true_isolate = unfetched = 0
    rows: list[list] = []
    unfetched_qids: list[str] = []

    for n, shard in enumerate(shards, 1):
        for entity in wikistore.read_shard(shard):
            items += 1
            geni_ids = wikistore.geni_ids_of(entity)
            if not geni_ids:
                continue
            geni_linked += 1
            rels = relatives(entity)
            if not rels:
                true_isolate += 1
            elif any(qid in held for qid in rels):
                connected += 1
                continue
            else:
                unfetched += 1
                # There are two of these in the whole store. The sample of 9,000
                # found none and called the mechanism dead; it is not dead, it
                # is a rounding error. Naming them costs nothing on a pass that
                # is already running, and "2" with no QIDs attached is the kind
                # of number that gets re-investigated later from scratch.
                unfetched_qids.append(entity.get("id") or "")
                continue
            # true isolates only, for the page
            qid = entity.get("id") or ""
            birth, death = _year(entity, "P569"), _year(entity, "P570")
            years = f"{birth}–{death}" if (birth or death) else ""
            rows.append([
                qid,
                _label(entity),
                geni_ids[0],
                years,
                len(entity.get("sitelinks") or {}),
                geni_ids[0] in ours,
            ])
        if n % 100 == 0 or n == len(shards):
            print(f"  {n}/{len(shards)} shards, {items:,} items, "
                  f"{true_isolate:,} true isolates", flush=True)

    rows.sort(key=lambda r: (-r[4], r[0]))
    out_json = ROOT / "out" / "_isolates.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    io.open(out_json, "w", encoding="utf-8").write(
        json.dumps(rows, separators=(",", ":"), ensure_ascii=False)
    )

    mine = sum(1 for r in rows if r[5])
    pct = (100.0 * true_isolate / geni_linked) if geni_linked else 0.0
    print()
    print(f"items                : {items:,}")
    print(f"carrying a Geni ID   : {geni_linked:,}")
    print(f"  connected          : {connected:,}")
    print(f"  TRUE ISOLATE       : {true_isolate:,}  ({pct:.1f}% of Geni-linked)")
    print(f"  looks isolated     : {unfetched:,}"
          + (f"  {unfetched_qids}" if unfetched_qids else ""))
    print(f"isolates we hold     : {mine:,}")
    print(f"wrote {out_json} ({len(rows):,} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
