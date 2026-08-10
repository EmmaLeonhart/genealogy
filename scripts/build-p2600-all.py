"""Rebuild `out/wikidata/p2600-all.tsv` offline, in the format its consumers read.

`genimerge overlap` normally writes this file from sixteen SPARQL partitions.
The cached copy was lost with `out/` in the 2026-08-09 re-clone, and re-running
`overlap` would query Wikidata, which CLAUDE.md forbids. Every P2600 statement is
already in `wikidata/items/`, so the file is rebuilt from the store index here.

**The format is load-bearing and is not the same as `p2600-map.tsv`.** This file
is `qid<TAB>geni_id` with **no header**, because `_cmd_wikidata_ancestors`,
`doubles` and the other consumers read it positionally:

    qid, geni_id = line.rstrip("\\n").split("\\t")

`wikistore.write_p2600_map` writes the *other* artifact — `p2600-map.tsv`,
`geni_id<TAB>qid`, with a header. Writing map content into this path is a silent
failure, not a loud one: every join simply misses, and
`genimerge wikidata-ancestors` reports `0 of our people carry an item` while
exiting 0. That is exactly what happened on 2026-08-09, and it is why this
script exists instead of a one-line reuse of the map writer.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import wikistore  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "wikidata" / "items"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"
OUT = ROOT / "out" / "wikidata" / "p2600-all.tsv"


def main() -> int:
    if not INDEX.exists():
        print(f"{INDEX} not found - run `genimerge wikidata-index` first", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with wikistore.StoreReader(STORE, INDEX) as reader:
        pairs = sorted({(qid, geni_id) for geni_id, qid in reader.geni_pairs()})
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        for qid, geni_id in pairs:
            fh.write(f"{qid}\t{geni_id}\n")
            written += 1

    print(f"wrote {OUT} ({written:,} pairs, qid<TAB>geni_id, no header)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
