"""Vendor order.life's 164,558 item JSONs into this repo as gzipped shards.

Emma, 2026-08-15: *"The data should be vendored here… we preserve the Order.life
QIDs because there's some important stuff about it. It should be here so that we
can easily reference it all the time."*

Until then both order.life scripts read an absolute path into a sibling checkout,
so a clean clone of this repo could not build the batch at all — the same failure
as the 37 gitignored GEDCOMs, where a fresh checkout silently measured something
different from every report in the repo.

**Sharded rather than copied file-for-file, which was Emma's call.** Every QID and
every claim is preserved either way; the difference is what git has to track.
164,558 loose files would take this working tree from 5,307 to ~175,000 and slow
every `status`, `add` and `checkout`. **`wikidata/items/` already uses this exact
layout** — `items-NNNNN.jsonl.gz`, ~1000 items a shard — which is why the tree is
only 5,307 files while holding 1.4M Wikidata items.

Shards are written in **sorted QID order**, numerically by the digits, so a
re-run produces byte-identical output and git sees no diff when nothing changed.

    py scripts/vendor-orderlife-items.py --source <path to order.life/wikibase>
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEST = REPO / "orderlife" / "items"

#: Matches `wikidata/items/`. A shard decompresses in one go, so this trades
#: file count against how much has to be read for a single lookup.
PER_SHARD = 1000

QID = re.compile(r"^Q(\d+)\.json$")


def qid_sort_key(name: str) -> tuple:
    m = QID.match(name)
    return (0, int(m.group(1))) if m else (1, name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="C:/Users/Emma/Documents/GitHub/order.life/wikibase",
                    help="the order.life wikibase directory to read from")
    ap.add_argument("--per-shard", type=int, default=PER_SHARD)
    args = ap.parse_args()

    src = Path(args.source) / "items"
    if not src.is_dir():
        print(f"no such directory: {src}", file=sys.stderr)
        return 1

    names = sorted((e.name for e in src.iterdir() if e.name.endswith(".json")),
                   key=qid_sort_key)
    print(f"{len(names):,} item files in {src}")

    DEST.mkdir(parents=True, exist_ok=True)
    for old in DEST.glob("items-*.jsonl.gz"):
        old.unlink()

    written = shard = skipped = 0
    buf: list[str] = []

    def flush(n: int) -> None:
        path = DEST / f"items-{n:05d}.jsonl.gz"
        # mtime=0 so the gzip header carries no timestamp: a re-run of unchanged
        # input then produces a byte-identical file and git sees no diff.
        with gzip.GzipFile(path, "wb", mtime=0) as fh:
            fh.write("".join(buf).encode("utf-8"))

    for name in names:
        try:
            text = (src / name).read_text(encoding="utf-8", errors="replace")
            item = json.loads(text)
        except (OSError, json.JSONDecodeError):
            skipped += 1
            continue
        if not isinstance(item, dict):
            # 81 of these are `null`, which is upstream's business, not ours.
            skipped += 1
            continue
        item.setdefault("id", name[:-5])
        buf.append(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
        written += 1
        if len(buf) >= args.per_shard:
            flush(shard)
            shard += 1
            buf = []
            if shard % 25 == 0:
                print(f"  {written:,} items in {shard} shards")
    if buf:
        flush(shard)
        shard += 1

    total = sum(p.stat().st_size for p in DEST.glob("items-*.jsonl.gz"))
    print(f"wrote {shard} shards, {written:,} items, {total / 1e6:.1f} MB "
          f"to {DEST}")
    if skipped:
        print(f"{skipped} files skipped: null or unreadable JSON")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
