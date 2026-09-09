"""English labels for QIDs and property IDs, fetched once and cached on disk.

Emma, 2026-08-11, looking at a raw Wikidata item: *"the Wikidata stuff is not
human-readable at all. You absolutely need to fetch the English-language labels
of the stuff it's referencing for both the properties and these other things."*

**Why this is allowed when `CLAUDE.md` says never to query Wikidata.** Same
carve-out `scripts/fetch-labels.py` already documents: the download walked
P22/P25/P26/P40/P3373, so the store holds *people*. Occupations, places,
qualifier values and the properties themselves were never fetched and cannot be
resolved offline at all. This is not "just quickly checking" a fact the store
answers — the store cannot answer it.

The rules that keep it cheap:

* **One request for everything missing**, never a loop of single lookups.
* **Cached to disk**, so a second case costs nothing. Labels do not move.
* Anything unresolved is recorded as unresolved rather than retried per call.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

__all__ = ["LabelCache", "collect_ids", "PRECISION"]

from genimerge import wikidata as _wd

ENDPOINT = "https://query.wikidata.org/sparql"

USER_AGENT = _wd.USER_AGENT

#: `wd:` resolves properties as entities too, so P-ids and Q-ids go in one query.
QUERY = """SELECT ?item ?itemLabel WHERE {
  VALUES ?item { %s }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}"""

#: Wikidata time precision codes. The day components of a low-precision date are
#: padding, so `+1894-01-01` at precision 9 means "1894", not "1 January".
PRECISION = {
    0: "billion years",
    6: "millennium",
    7: "century",
    8: "decade",
    9: "year",
    10: "month",
    11: "day",
    12: "hour",
    13: "minute",
    14: "second",
}


def collect_ids(entity: dict) -> set[str]:
    """Every property ID and item ID mentioned anywhere in a stored item.

    Walks mainsnaks, qualifiers and references alike, because the genealogy
    lives in the qualifiers and references as much as in the values — the point
    `CLAUDE.md` makes about Henry III's marriage.
    """
    found: set[str] = set()

    def visit_snak(snak: dict) -> None:
        prop = snak.get("property")
        if isinstance(prop, str):
            found.add(prop)
        value = (snak.get("datavalue") or {}).get("value")
        if isinstance(value, dict):
            ident = value.get("id")
            if isinstance(ident, str) and ident[:1] in "QP":
                found.add(ident)

    for prop, statements in (entity.get("claims") or {}).items():
        found.add(prop)
        for statement in statements:
            visit_snak(statement.get("mainsnak") or {})
            for snaks in (statement.get("qualifiers") or {}).values():
                for snak in snaks:
                    visit_snak(snak)
            for reference in statement.get("references") or []:
                for snaks in (reference.get("snaks") or {}).values():
                    for snak in snaks:
                        visit_snak(snak)
    return found


class LabelCache:
    """Disk-backed English labels. ``resolve`` fetches only what is missing."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.labels: dict[str, str] = {}
        if self.path.exists():
            with open(self.path, encoding="utf-8") as handle:
                for line in handle:
                    ident, _, label = line.rstrip("\n").partition("\t")
                    if ident:
                        self.labels[ident] = label

    def __getitem__(self, ident: str) -> str:
        return self.labels.get(ident, "")

    def describe(self, ident: str) -> str:
        """``Q5 (human)`` — the ID kept, because the ID is what gets written."""
        label = self.labels.get(ident)
        return f"{ident} ({label})" if label else ident

    def resolve(self, ids, *, verbose: bool = True) -> int:
        """Fetch every unknown ID in one request. Returns how many were added."""
        missing = sorted({i for i in ids if i and i not in self.labels})
        if not missing:
            return 0
        if verbose:
            print(f"  fetching {len(missing)} labels in one query")
        found = _fetch(missing)
        # Record a miss as an empty label so it is not re-requested every run.
        for ident in missing:
            self.labels[ident] = found.get(ident, "")
        self.save()
        return len(found)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as handle:
            for ident in sorted(self.labels):
                handle.write(f"{ident}\t{self.labels[ident]}\n")


def _fetch(ids: list[str], attempt: int = 1) -> dict[str, str]:
    """One POST for the whole list.

    POST rather than GET because a few hundred IDs in a URL earns HTTP 414 —
    the reason `scripts/fetch-labels.py` already gives.
    """
    values = " ".join(f"wd:{i}" for i in ids)
    body = urllib.parse.urlencode({"query": QUERY % values, "format": "json"}).encode("ascii")
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "User-Agent": _wd.require_agent(),
            "Accept": "application/sparql-results+json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in (429, 503) and attempt <= 4:
            wait = int(exc.headers.get("Retry-After") or 2**attempt)
            print(f"  {exc.code}, waiting {wait}s")
            time.sleep(wait)
            return _fetch(ids, attempt + 1)
        raise

    out: dict[str, str] = {}
    for row in data["results"]["bindings"]:
        ident = row["item"]["value"].rsplit("/", 1)[-1]
        label = row.get("itemLabel", {}).get("value", "")
        # The label service echoes the ID back when there is no English label.
        if label and label != ident:
            out[ident] = label
    return out
