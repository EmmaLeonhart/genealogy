"""Pull every family relationship out of the downloaded store, once, into one file.

    python scripts/extract-wikidata-relations.py

**This is the thing whose absence made the zipper join half-exist.** Emma, 2026-08-25:
*"The zipper merge kinda half exists and is opaque I thought you meant something more clear and
substantive than just having never even tried to implement the feature. Implement it."*

Everything built so far read Wikidata's relationships **one item at a time**, opening a shard per
question — `resolve-multi-geni-by-parents.py` for a pair's parents,
`corroborate-pairs-by-lineage.py` for a pair's parents again, `build-add-p2600-batch.py` for a
proposal's parents. That is affordable for a few hundred items and impossible for a join, which
has to walk outward from half a million anchors and ask about children and spouses as well as
parents. So the join was never written; only its parent-shaped fragments were.

This reads all 2,248 shards **once** and writes a compact table of the four properties a
genealogical join needs:

| property | meaning |
| --- | --- |
| `P22` | father |
| `P25` | mother |
| `P40` | child |
| `P26` | spouse |

`P2600` *Geni.com profile ID* comes along too, so the zipper does not need a second file to know
which items are already anchored.

**Deprecated statements are dropped.** A deprecated `P22` is Wikidata saying "not this one", and
carrying it into a join would let a retracted parent link propose a merge.

Output is one row per item that has at least one of these, values semicolon-separated:

    qid  p22  p25  p40  p26  p2600

Writes `out/wikidata/relations.tsv`. Reads nothing but the store; makes no request.
"""
from __future__ import annotations

import gzip
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "wikidata" / "items"
DEST = ROOT / "out" / "wikidata" / "relations.tsv"

WANTED = ("P22", "P25", "P40", "P26", "P2600")


def values(claims, prop):
    out = []
    for st in claims.get(prop, []):
        if st.get("rank") == "deprecated":
            continue
        dv = st["mainsnak"].get("datavalue", {}).get("value")
        if isinstance(dv, dict):
            dv = dv.get("id")
        if dv:
            out.append(str(dv))
    return out


def main():
    shards = sorted(STORE.glob("items-*.jsonl.gz"))
    print(f"{len(shards)} shards")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    rows = items = 0
    with open(DEST, "w", encoding="utf-8", newline="\n") as out:
        out.write("qid\tp22\tp25\tp40\tp26\tp2600\n")
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
                    got = [values(claims, p) for p in WANTED]
                    if not any(got):
                        continue
                    out.write(qid + "\t" + "\t".join(";".join(v) for v in got) + "\n")
                    rows += 1
            if n % 200 == 0:
                rate = items / max(time.time() - started, 1)
                print(f"  {n}/{len(shards)} shards, {items:,} items, {rows:,} with "
                      f"relations, {rate:,.0f}/s", flush=True)
    print(f"\n{items:,} items read, {rows:,} carry at least one of {', '.join(WANTED)}")
    print(f"wrote {DEST} in {time.time() - started:.0f}s")


if __name__ == "__main__":
    main()
