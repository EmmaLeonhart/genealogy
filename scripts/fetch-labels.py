"""Fetch English labels for a list of QIDs in ONE SPARQL query.

`python scripts/fetch-labels.py Q5933 Q29265 ...`

**Why this is allowed when `CLAUDE.md` says never to query Wikidata.** The rule
exists to stop "just quickly checking" a fact that the downloaded store already
answers. This is the case the rule does not cover: the download walked
P22/P25/P26/P40/P3373, so it holds *people*. Places, buildings, source items and
qualifier values — `Q5933` Westminster Abbey, `Q29265` Canterbury Cathedral, the
items behind `P1534 end cause` — were never fetched and cannot be resolved
offline at all.

Emma, 2026-08-10: *"do a SPARQL query to get all of these ones at once. Wikidata
is great for getting large amounts of information all at once in sync, all at
once in a single query, and it sucks ass at giving you lots of information in
rapid sequential queries."*

So: **one query, many QIDs, labels only.** Never a loop of single lookups. If a
caller needs 400 labels that is still one request, not 400.
"""

from __future__ import annotations

import os
import pathlib
import json
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from bot_identity import agent as _bot_agent  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENDPOINT = "https://query.wikidata.org/sparql"

#: Descriptive, with contact and purpose, per Wikidata's user-agent policy and
#: `todo.md` 8a: "Wikidata is hostile - design for 429s from line one."
USER_AGENT = _bot_agent()

#: One query per run. VALUES takes thousands of QIDs comfortably.
QUERY = """SELECT ?item ?itemLabel ?itemDescription WHERE {
  VALUES ?item { %s }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}"""


def fetch(qids: list[str], attempt: int = 1) -> dict:
    """One request, however many QIDs.

    **POST, not GET.** A GET puts the whole VALUES clause in the URL and
    Wikidata answers `HTTP 414: URI Too Long` somewhere past a few hundred
    QIDs — 366 was fine, 30 cases' worth was not. Chunking would have meant
    several requests, which is the thing Emma asked this to avoid: *"Wikidata
    is great for getting large amounts of information all at once in a single
    query, and it sucks ass at giving you lots of information in rapid
    sequential queries."* The body has no such limit.
    """
    values = " ".join(f"wd:{q}" for q in qids)
    body = urllib.parse.urlencode({"query": QUERY % values, "format": "json"}).encode("ascii")
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/sparql-results+json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in (429, 503) and attempt <= 4:
            wait = int(exc.headers.get("Retry-After") or 2 ** attempt)
            print(f"  {exc.code}, waiting {wait}s", file=sys.stderr)
            time.sleep(wait)
            return fetch(qids, attempt + 1)
        raise


def main() -> int:
    qids = [q for q in sys.argv[1:] if q.startswith("Q")]
    if not qids:
        print(__doc__)
        return 2
    data = fetch(qids)
    found = {}
    for row in data["results"]["bindings"]:
        qid = row["item"]["value"].rsplit("/", 1)[-1]
        found[qid] = (row.get("itemLabel", {}).get("value", ""), row.get("itemDescription", {}).get("value", ""))
    for qid in qids:
        label, desc = found.get(qid, ("(no result)", ""))
        print(f"{qid:<12} {label:<40} {desc[:60]}")
    print(f"\n{len(found)}/{len(qids)} resolved in 1 query", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
