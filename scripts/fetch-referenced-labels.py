"""Fetch English labels for every property and item our store references but lacks.

Emma, 2026-08-12: **"Great so it's labels on things we don't have, yes grab them
right now, properties and items."**

The store holds 1,408,401 people, fetched whole, because the download walked
P22/P25/P26/P40/P3373. It holds nothing those people merely *point at* — not the
name items `P735`/`P734` reference, not occupations, not places, not the
properties themselves, not even `Q5`.

This fetches **labels only**, which is far cheaper than fetching items, and is
what makes the stored data readable and a name string resolvable to an item.

**This is a live Wikidata run**, and the only one this repo permits. The rules it
follows, from `CLAUDE.md` and `todo.md` § 8a:

* **One request per batch, never per item.** `VALUES` takes thousands.
* **POST, not GET** — a few hundred IDs in a URL earns HTTP 414.
* **Exponential backoff on 429/503**, honouring `Retry-After`.
* **Saved after every batch**, so a crash or a kill loses at most one batch and
  a re-run resumes rather than restarting.
* A descriptive user agent with contact and purpose.

Writes `reports/wikidata-labels.tsv`, committed — repo size is not a constraint
here and this is the file every other report will read to become legible.

**Restarting is cheap.** The label file is written after every batch, and the
enumerated id list is cached to `reports/referenced-ids.txt` with a fingerprint of
the store it came from, so a re-run skips both the ~15-minute shard scan and every
label already fetched. The fingerprint is shard count, total bytes and newest
mtime: if the store changes, the cache is discarded rather than trusted.

    py scripts/fetch-referenced-labels.py            # resume, or scan then fetch
    py scripts/fetch-referenced-labels.py --count    # enumerate only, no network
    py scripts/fetch-referenced-labels.py --rescan   # ignore the cached id list
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import wikilabels, wikistore  # noqa: E402

STORE = REPO_ROOT / "wikidata" / "items"
OUT = REPO_ROOT / "reports" / "wikidata-labels.tsv"

#: The enumerated id list, cached so a restart does not repay the 15-minute scan
#: of 1,408 shards to rebuild an answer that only changes when the store does.
IDS = REPO_ROOT / "reports" / "referenced-ids.txt"


def store_fingerprint() -> str:
    """Cheap identity for the store: shard count, total bytes, newest mtime.

    Enough to notice a download adding, replacing or rewriting shards, and it
    costs a stat per file rather than a read. If it differs, the cache is
    discarded and the scan runs again — the cache must never be able to answer
    for a store it did not come from.
    """
    shards = wikistore.shards(STORE)
    total = sum(p.stat().st_size for p in shards)
    newest = max((p.stat().st_mtime_ns for p in shards), default=0)
    return f"{len(shards)}:{total}:{newest}"


def read_id_cache() -> set[str] | None:
    if not IDS.exists():
        return None
    with open(IDS, encoding="utf-8") as handle:
        header = handle.readline().strip()
        if header != f"# store {store_fingerprint()}":
            print("id cache is for a different store; re-scanning", flush=True)
            return None
        return {line.strip() for line in handle if line.strip()}


def write_id_cache(missing: set[str]) -> None:
    IDS.parent.mkdir(parents=True, exist_ok=True)
    with open(IDS, "w", encoding="utf-8") as handle:
        handle.write(f"# store {store_fingerprint()}\n")
        for ident in sorted(missing):
            handle.write(ident + "\n")
    print(f"wrote {IDS} ({len(missing):,} ids)", flush=True)

#: IDs per request. The docstring of `scripts/fetch-labels.py` records that
#: VALUES takes thousands comfortably over POST; this stays well under that so a
#: single failure costs little and `Retry-After` waits stay short.
BATCH = 2000

#: Seconds between batches. Deliberate politeness rather than a measured limit —
#: `todo.md` § 8a: "Wikidata is hostile - design for 429s from line one."
PAUSE = 1.0


def enumerate_referenced() -> tuple[set[str], int]:
    """Every P/Q id referenced anywhere in the store, and how many items were read.

    Walks mainsnaks, qualifiers and references alike — the genealogy lives beside
    the value as often as in it.
    """
    found: set[str] = set()
    stored: set[str] = set()
    items = 0
    shards = wikistore.shards(STORE)
    print(f"{len(shards):,} shards", flush=True)

    for n, shard in enumerate(shards, 1):
        for entity in wikistore.read_shard(shard):
            items += 1
            qid = entity.get("id")
            if isinstance(qid, str):
                stored.add(qid)
            found |= wikilabels.collect_ids(entity)
        if n % 200 == 0 or n == len(shards):
            print(f"  shard {n:,}/{len(shards):,}  {items:,} items  "
                  f"{len(found):,} distinct ids referenced", flush=True)

    # Properties are never "stored items", so they always need fetching.
    missing = {i for i in found if i.startswith("P")} | (
        {i for i in found if i.startswith("Q")} - stored
    )
    print(f"{len(found):,} distinct ids referenced; {len(stored):,} items stored")
    print(f"{len(missing):,} need a label fetched")
    return missing, items


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--count", action="store_true", help="enumerate only, no network")
    ap.add_argument("--batch", type=int, default=BATCH)
    ap.add_argument("--rescan", action="store_true",
                    help="ignore the cached id list and walk the shards again")
    args = ap.parse_args()

    missing = None if args.rescan else read_id_cache()
    if missing is None:
        missing, _ = enumerate_referenced()
        write_id_cache(missing)
    else:
        print(f"{len(missing):,} ids from {IDS} — scan skipped", flush=True)

    cache = wikilabels.LabelCache(OUT)
    todo = sorted(i for i in missing if i not in cache.labels)
    print(f"{len(cache.labels):,} already cached; {len(todo):,} to fetch")

    if args.count:
        print("--count: stopping before any request")
        return 0

    if not todo:
        print("nothing to fetch")
        return 0

    batches = (len(todo) + args.batch - 1) // args.batch
    print(f"fetching in {batches:,} batches of {args.batch:,}", flush=True)

    resolved = 0
    for index in range(batches):
        chunk = todo[index * args.batch : (index + 1) * args.batch]
        found = wikilabels._fetch(chunk)
        for ident in chunk:
            cache.labels[ident] = found.get(ident, "")
        # Saved every batch: a kill loses one batch, not the run.
        cache.save()
        resolved += len(found)
        print(f"  batch {index + 1:,}/{batches:,}  +{len(found):,} labels  "
              f"({resolved:,} so far, {len(cache.labels):,} cached)", flush=True)
        if index + 1 < batches:
            time.sleep(PAUSE)

    print(f"\nwrote {OUT}")
    print(f"{len(cache.labels):,} ids cached, {resolved:,} resolved this run")
    unresolved = sum(1 for v in cache.labels.values() if not v)
    print(f"{unresolved:,} have no English label on Wikidata (recorded as empty, "
          "so they are not re-requested)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
