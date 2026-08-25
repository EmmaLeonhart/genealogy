"""Does the item store still agree that these `P2600` values exist? Two extracts, two dates.

    python scripts/check-removal-batch-vintage.py

**Found while running the resolver, 2026-08-25.** The item store's copy of `Q102825194` carries
**no `P2600` at all**, while `out/wikidata/p2600-all.tsv` gives it two. Both are downloads of
Wikidata, so one of them is simply older -- and the batch in
`reports/wikidata-remove-wrong-p2600.json` deletes statements, which is the one kind of edit that
must not be computed from a stale read.

**The two extracts are measurably different vintages.** `p2600-all.tsv` is 2026-08-09 19:17. The
item store came down in tranches: 1,407 shards on 08-09, 1 on 08-12, 15 on 08-14 and **825 on
08-15**. So the dump predates 841 of the 2,248 shards, and an item whose `P2600` was added after
08-09 is invisible to the dump while an item edited after its shard was fetched is invisible to
the store. Neither is authoritative; they disagree in both directions.

**What this script measures, and what it deliberately does not.** For every removal in the batch
it asks whether the item's stored claims still carry the value being removed, and reports four
outcomes:

* `both agree` -- the store holds the value the dump proposed. The removal acts on something that
  was there in both reads.
* `store lacks the value` -- the dump saw a `P2600` the store does not. Either it was added after
  08-09 and the shard is older, or removed after the shard was fetched. **The removal may already
  be a no-op**, which is harmless, but it also means the *decision* rested on a value we cannot
  currently see.
* `store lacks the item` -- nothing to check against.
* `store has EXTRA values` -- the item carries `P2600` values the dump never listed, so the
  correspondence under-counted this item's candidates and the resolver may have chosen between
  two of three.

**It does not query Wikidata**, which is banned here, so it cannot say which extract is right --
only how far apart they are. The live answer comes from opening the item, the way the six pairs
were opened.

Writes `reports/removal-batch-vintage.tsv`.
"""
from __future__ import annotations

import collections
import csv
import gzip
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "wikidata" / "items"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"
GENI_ID = "P2600"


def main():
    batch = json.loads((ROOT / "reports" / "wikidata-remove-wrong-p2600.json")
                       .read_text(encoding="utf-8"))
    by_item = collections.defaultdict(list)
    for e in batch:
        by_item[e["subject"]["qid"]].append(e)
    print(f"{len(batch)} removals over {len(by_item)} items")

    # What the dump says each item carries, so "extra" can be measured against it.
    dump = collections.defaultdict(set)
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0] in by_item:
                dump[row[0]].add(row[1].strip())

    con = sqlite3.connect(str(INDEX))
    by_shard = collections.defaultdict(set)
    for qid in by_item:
        hit = con.execute("SELECT shard FROM items WHERE qid=?", (qid,)).fetchone()
        if hit:
            by_shard[hit[0]].add(qid)

    stored, shard_date = {}, {}
    for shard, wanted in by_shard.items():
        path = STORE / f"items-{shard:05d}.jsonl.gz"
        if not path.exists():
            continue
        import datetime
        shard_day = datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()
        with gzip.open(path, "rt", encoding="utf-8") as f:
            for line in f:
                if not wanted:
                    break
                for qid in list(wanted):
                    if f'"{qid}"' not in line:
                        continue
                    item = json.loads(line)
                    if item.get("id") != qid:
                        continue
                    wanted.discard(qid)
                    stored[qid] = {st["mainsnak"].get("datavalue", {}).get("value")
                                   for st in item.get("claims", {}).get(GENI_ID, [])}
                    shard_date[qid] = shard_day
                    break

    rows, tally = [], collections.Counter()
    for qid, edits in sorted(by_item.items()):
        have = stored.get(qid)
        listed = dump.get(qid, set())
        for e in edits:
            v = e["value"]
            if have is None:
                verdict = "store lacks the item"
            elif v in have:
                verdict = "both agree"
            else:
                verdict = "store lacks the value"
            tally[verdict] += 1
            extra = sorted((have or set()) - listed - {None})
            if extra:
                tally["store has EXTRA values"] += 1
            rows.append({
                "verdict": verdict, "qid": qid, "value_to_remove": v,
                "keeps": e["keeps"], "decided_by": e["decided_by"],
                "store_shard_downloaded": shard_date.get(qid, ""),
                "store_p2600": ";".join(sorted(x for x in (have or set()) if x)),
                "dump_p2600": ";".join(sorted(listed)),
                "store_has_extra": ";".join(extra),
            })

    dest = ROOT / "reports" / "removal-batch-vintage.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"\nwrote {dest.relative_to(ROOT)}")
    for k, n in tally.most_common():
        print(f"   {n:>4}  {k}")
    days = collections.Counter(shard_date.values())
    print("\n  the 30 items' shards were downloaded:")
    for d, n in sorted(days.items()):
        print(f"     {d}  {n}")
    print("\n  p2600-all.tsv is 2026-08-09 19:17, so a shard newer than that")
    print("  may hold statements the dump never saw, and vice versa.")

    bad = [r for r in rows if r["verdict"] != "both agree"]
    if bad:
        print(f"\n  {len(bad)} removals NOT corroborated by the store:")
        for r in bad:
            print(f"     {r['qid']:<12} remove {r['value_to_remove']:<20} "
                  f"[{r['verdict']}] store={r['store_p2600'] or '-'}")


if __name__ == "__main__":
    main()
