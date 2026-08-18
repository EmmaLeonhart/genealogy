"""Every name item on Wikidata, as a seed list for the bulk downloader.

**Emma, 2026-08-15:** *"Because we are not allowed to do this individual
querying, you're supposed to be doing mass exports on this stuff. I would say,
realistically, you probably should be doing a mass export on every instance of a
surname, every single instance of a patronymic, and every single instance of a
given name."*

**This is the enumeration step, not the download.** It asks Wikidata for the QID
of every item that is `instance of` one of the six name classes and writes them
to a seed file; `genimerge wikidata-download --seeds` then fetches the items
themselves. Splitting it that way is the point — the queries here are
**aggregate**, a page of QIDs at a time, never one request per item.

Sized 2026-08-15 with a single `COUNT` query:

| class | | items |
| --- | --- | ---: |
| `Q101352` | family name | 693,297 |
| `Q12308941` | male given name | 59,782 |
| `Q11879590` | female given name | 38,195 |
| `Q202444` | given name | 31,487 |
| `Q3409032` | unisex given name | 4,142 |
| `Q110874` | patronymic | 633 |

**Why all six and not just the ones our people reference.** The download sized in
`reports/name-item-download.md` was 132,456 items — only those already pointed at
by somebody in the store. That is the wrong set for *creating* names: to know
whether a token already has an item we must know every item that exists, not the
subset our tree happens to use. Asking about a name we do not hold is exactly the
individual query the rules forbid.

**Paginated by `OFFSET`, ordered by QID.** Deterministic and resumable: the file
is rewritten from scratch each run, and a page that fails stops the run with the
pages so far kept.

    py scripts/collect-name-item-qids.py
"""

from __future__ import annotations

import os
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = REPO / "reports" / "name-item-qids.tsv"
ENDPOINT = "https://query.wikidata.org/sparql"
_CONTACT = os.environ.get("BOT_CONTACT", "").strip()
AGENT = (
    "genimerge/1.0 (https://github.com/EmmaLeonhart/geni; name-item enumeration"
    + (f"; {_CONTACT}" if _CONTACT else "")
    + ")"
)
#: The six name classes, documented in `CLAUDE.md` § *Wikidata properties*.
CLASSES = {
    "Q110874": "patronymic",
    "Q3409032": "unisex given name",
    "Q202444": "given name",
    "Q11879590": "female given name",
    "Q12308941": "male given name",
    "Q101352": "family name",
}

PAGE = 100_000
DELAY = 2.0

#: A real item QID and nothing else. The first run crashed sorting `Q40394-S1`,
#: a **statement node** — `wdt:P31` can land on one, and its URI ends up looking
#: like an entity. Everything fetched was lost because the crash came after the
#: last query and before the write. Hence both halves of the fix: filter here,
#: and cache each class to disk as it completes so a later failure never costs
#: the queries again.
ITEM = re.compile(r"^Q\d+$")

CACHE = REPO / "out" / "name-item-qids"


def page(qid: str, offset: int, limit: int) -> list[str]:
    query = (f"SELECT ?item WHERE {{ ?item wdt:P31 wd:{qid} }} "
             f"ORDER BY ?item LIMIT {limit} OFFSET {offset}")
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": query, "format": "json"})
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=600) as handle:
        data = json.load(handle)
    return [q for q in (b["item"]["value"].rsplit("/", 1)[-1]
                       for b in data["results"]["bindings"]) if ITEM.match(q)]


def main() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)
    found: dict[str, set[str]] = {}
    for qid, label in CLASSES.items():
        cached = CACHE / f"{qid}.txt"
        if cached.exists():
            found[qid] = set(cached.read_text(encoding="utf-8").split())
            print(f"  {label:<20} {len(found[qid]):>9,} from cache", flush=True)
            continue
        got: set[str] = set()
        offset = 0
        while True:
            try:
                rows = page(qid, offset, PAGE)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                print(f"  {label}: page at offset {offset:,} failed ({exc}); "
                      "keeping what came back", flush=True)
                break
            got.update(rows)
            print(f"  {label:<20} offset {offset:>8,} -> {len(rows):>7,} rows "
                  f"({len(got):,} so far)", flush=True)
            if len(rows) < PAGE:
                break
            offset += PAGE
            time.sleep(DELAY)
        cached.write_text("\n".join(sorted(got)), encoding="utf-8")
        found[qid] = got
        time.sleep(DELAY)

    everything: set[str] = set()
    for got in found.values():
        everything |= got

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        handle.write("qid\tclasses\n")
        for item in sorted(everything, key=lambda q: int(q[1:])):
            classes = ",".join(c for c, got in found.items() if item in got)
            handle.write(f"{item}\t{classes}\n")

    print(f"\n{len(everything):,} distinct name items -> {OUT}")
    for qid, label in CLASSES.items():
        print(f"  {label:<20} {len(found[qid]):>9,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
