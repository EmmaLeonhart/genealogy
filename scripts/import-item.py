"""Fetch one Wikidata item into the local store.

Emma, 2026-08-12: **"impprt Q140568870 don't just acknowledge and not do it."**

Her item is matched to a Geni profile by hand but carries no `P2600`, so the
family walk that built the store never had a route to it. Nothing about her can
be checked — or emitted safely — while the item is absent.

**This is a live Wikidata request**, which the repo permits only for the bulk
download and for label lookups the store cannot answer. This is neither, and it
is done because she asked for it directly and it is a single item.

The item is written as its own shard so nothing existing is rewritten, and the
index is updated rather than rebuilt.

    py scripts/import-item.py Q140568870 [Q...]
"""

from __future__ import annotations

import gzip
import json
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import wikidata as _wd, wikistore  # noqa: E402

STORE = REPO_ROOT / "wikidata" / "items"
INDEX = REPO_ROOT / "out" / "wikidata" / "store-index.sqlite3"

USER_AGENT = _wd._agent(
    "geni-merge/0.1", "https://github.com/EmmaLeonhart/geni; single-item import"
)


def fetch(qid: str) -> dict:
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload["entities"][qid]


def main() -> int:
    qids = [a for a in sys.argv[1:] if a.startswith("Q")]
    if not qids:
        print(__doc__)
        return 2

    entities = []
    for qid in qids:
        entity = fetch(qid)
        entities.append(entity)
        labels = entity.get("labels") or {}
        name = (labels.get("en") or labels.get("mul") or {}).get("value", "(no label)")
        claims = entity.get("claims") or {}
        print(f"fetched {qid}  {name}")
        print(f"  {len(claims)} properties, {len(labels)} labels, "
              f"{len(entity.get('sitelinks') or {})} sitelinks")
        print(f"  P2600: {'yes' if 'P2600' in claims else 'NO'}")
        for prop, role in (("P22", "father"), ("P25", "mother"), ("P26", "spouse"),
                           ("P40", "child"), ("P3373", "sibling")):
            for statement in claims.get(prop, []):
                value = ((statement.get("mainsnak") or {}).get("datavalue") or {}).get("value") or {}
                if value.get("id"):
                    print(f"  {role}: {value['id']}")

    # A new shard rather than rewriting an existing one: the download's shards are
    # its own record and this import is not part of it.
    existing = wikistore.shards(STORE)
    number = max((int(p.stem.split(".")[0].split("-")[-1]) for p in existing), default=0) + 1
    shard = STORE / f"items-{number:06d}.jsonl.gz"
    with gzip.open(shard, "wt", encoding="utf-8") as handle:
        for entity in entities:
            handle.write(json.dumps(entity, ensure_ascii=False) + "\n")
    print(f"\nwrote {shard.name} ({len(entities)} item(s))")

    stats = wikistore.build_index(STORE, INDEX)
    print(f"index rebuilt: {stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
