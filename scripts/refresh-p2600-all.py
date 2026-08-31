"""Refresh `out/wikidata/p2600-all.tsv` from live Wikidata, without merging the tree.

    BOT_CONTACT=you@example.com python scripts/refresh-p2600-all.py

**The file is the master QID-to-Geni correspondence** — every Wikidata item carrying `P2600`
*Geni.com profile ID*, as `qid<TAB>geni_id` with no header. **Forty scripts and three modules
read it**, including `build-garborg-day.py`, `refresh-garborg-ledger.py`, `derive-family.py` and
`zipper-join.py`.

**Why this exists rather than `genimerge overlap`.** That command does the same fetch and then
merges the whole corpus to produce `reports/wikidata-overlap.md` — 837 seconds and 16.8 GB for a
report nobody asked for here. This does the fetch, checks it, and writes the file.

**The staleness it fixes was invisible, which is the point.** The committed copy was a
**2026-08-09** rebuild — done offline from the local store because querying Wikidata was banned
at the time, a ban Emma lifted on 2026-08-29. A join through a stale copy does not fail; it
silently returns fewer rows.

**Measured on the first refresh, 2026-08-30: `reports/garborg-qids.tsv` went from 258 of 849
items resolving to 849 of 849.** Five hundred and ninety-one of her own items were invisible to
the forty scripts that read this file. The row count moved only +1,124 (517,851 → 518,975),
which is why the staleness never announced itself — the file looked the same size and was
missing most of the work of three weeks.

**What it did NOT fix, and the difference matters.** The Izumo roster's 204 QIDs resolve to
**2** Geni ids both before and after. That is not staleness: only 2 of those 204 items carry a
`P2600` on live Wikidata at all. This docstring asserted the opposite before the refresh was
run — a cause assumed rather than tested, which is exactly what `CLAUDE.md` § *CHECK before you
alarm her* forbids.

**Sixteen partitioned queries, by MD5 prefix**, which is `overlap.PARTITIONS`. That is the whole
politeness story: a handful of large queries rather than one that times out or half a million
small ones. `CLAUDE.md` § *Querying Wikidata is ALLOWED* — batch where the API offers batching,
and do not hammer to finish faster.

**A short fetch is reported and does not silently overwrite.** The endpoint is asked how many
`P2600` statements it holds before the partitions run, and a fetch that lands far under that
means a partition failed rather than that Wikidata shrank. Wikidata is live, so small drift is
ordinary; the threshold below is deliberately loose about drift and strict about collapse.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from genimerge import overlap as overlap_mod  # noqa: E402
from genimerge.wikidata import WikidataClient, require_agent  # noqa: E402

OUT = ROOT / "out" / "wikidata" / "p2600-all.tsv"
CACHE = ROOT / "out" / "wikidata" / "cache"

#: A fetch below this share of what the endpoint reports is a failed partition, not drift.
#: Loose enough that ordinary churn between the count query and the partitions passes.
MIN_SHARE = 0.90


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="fetch and report, but do not write the file")
    args = ap.parse_args()

    # `require_agent` fails loudly when BOT_CONTACT is unset: an empty User-Agent gets a bare
    # 403 from Wikimedia, and six call sites once shared that mystery.
    require_agent()
    CACHE.mkdir(parents=True, exist_ok=True)
    client = WikidataClient(cache_dir=CACHE, delay=1.0)

    before = 0
    if OUT.exists():
        before = sum(1 for _ in OUT.open(encoding="utf-8"))
        print(f"current file: {before:,} rows, "
              f"modified {__import__('datetime').date.fromtimestamp(OUT.stat().st_mtime)}")

    reported = {}
    for name, query in overlap_mod.COUNT_QUERIES.items():
        reported[name] = int(client.sparql(query)[0]["n"])
        print(f"  wikidata {name}: {reported[name]:,}", flush=True)

    def progress(done, total):
        print(f"  partition {done}/{total}", flush=True)

    pairs = overlap_mod.fetch_all_p2600(client, progress=progress)
    print(f"\nfetched {len(pairs):,} statements")

    expected = reported["statements"]
    if len(pairs) < expected * MIN_SHARE:
        sys.exit(f"REFUSING to write: fetched {len(pairs):,} against {expected:,} reported "
                 f"({len(pairs) / expected:.1%}). A partition failed; the old file is intact.")
    if len(pairs) != expected:
        print(f"note: {len(pairs):,} fetched against {expected:,} reported — Wikidata is live, "
              "so drift between the count query and the partitions is ordinary")

    if args.dry_run:
        print("--dry-run: not writing")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(f"{qid}\t{gid}" for qid, gid in sorted(pairs)) + "\n"
    OUT.write_text(text, encoding="utf-8")
    after = len(pairs)
    print(f"\nwrote {OUT.relative_to(ROOT)}: {before:,} -> {after:,} rows "
          f"({after - before:+,})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
