"""Birth and death years out of the store, once, so the zipper can order siblings.

    python scripts/extract-wikidata-dates.py

**Emma, 2026-08-25, on how the zipper should resolve a sibling set that position alone cannot
separate:** *"Dates first then names but also bruh providence of zipper merges should be
recorded."*

Dates first requires dates, and nothing had extracted them: `out/wikidata/relations.tsv` carries
`P22`/`P25`/`P40`/`P26`/`P2600` and `out/wikidata/labels.tsv` carries labels and identifiers, but
neither carries `P569` *date of birth* or `P570` *date of death*. So "dates first" was not a
policy the join could have followed even in principle.

**Only the year is kept, and only its sign and magnitude.** Wikidata time literals are
`+1582-10-15T00:00:00Z` with a `precision` field; anything coarser than a year (century, decade)
is dropped rather than rounded, because a rounded century would silently order siblings that
nothing separates -- the same silent-narrowing failure `CLAUDE.md` records for the date parser.

**Deprecated statements are dropped**, matching `extract-wikidata-relations.py`: a deprecated
`P569` is Wikidata saying "not this one".

Output, one row per item that has either:

    qid  birth_year  death_year

Writes `out/wikidata/dates.tsv`. Reads only the store; makes no request.
"""
from __future__ import annotations

import gzip
import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "wikidata" / "items"
DEST = ROOT / "out" / "wikidata" / "dates.tsv"

#: `+1582-10-15T00:00:00Z` and `-0044-03-15T00:00:00Z`. The sign is part of the year.
TIME = re.compile(r"^([+-])(\d{4,})-")

#: Wikidata precision: 9 = year, 10 = month, 11 = day. Coarser than a year is not a year.
YEAR_PRECISION = 9


def year(claims, prop):
    """The best year for `prop`, or `''`. Preferred rank wins; deprecated never counts."""
    best = ""
    for st in claims.get(prop, []):
        if st.get("rank") == "deprecated":
            continue
        dv = st.get("mainsnak", {}).get("datavalue", {}).get("value")
        if not isinstance(dv, dict):
            continue
        if (dv.get("precision") or 0) < YEAR_PRECISION:
            continue
        m = TIME.match(dv.get("time") or "")
        if not m:
            continue
        y = ("-" if m.group(1) == "-" else "") + str(int(m.group(2)))
        if st.get("rank") == "preferred":
            return y
        best = best or y
    return best


def main():
    shards = sorted(STORE.glob("items-*.jsonl.gz"))
    print(f"{len(shards)} shards")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    items = rows = 0
    with open(DEST, "w", encoding="utf-8", newline="\n") as out:
        out.write("qid\tbirth_year\tdeath_year\n")
        for n, shard in enumerate(shards, 1):
            with gzip.open(shard, "rt", encoding="utf-8") as f:
                for line in f:
                    if not line.startswith("{"):
                        continue
                    try:
                        item = json.loads(line)
                    except ValueError:
                        continue
                    qid = item.get("id")
                    if not qid:
                        continue
                    items += 1
                    claims = item.get("claims", {})
                    b, d = year(claims, "P569"), year(claims, "P570")
                    if not (b or d):
                        continue
                    out.write(f"{qid}\t{b}\t{d}\n")
                    rows += 1
            if n % 400 == 0:
                print(f"  {n}/{len(shards)} shards, {items:,} items, {rows:,} dated",
                      flush=True)
    print(f"\n{items:,} items read, {rows:,} with a birth or death year")
    print(f"wrote {DEST} in {time.time() - started:.0f}s")


if __name__ == "__main__":
    main()
