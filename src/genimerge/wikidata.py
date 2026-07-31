"""Talk to Wikidata: SPARQL for reconciliation, the API for labels.

514,567 Wikidata items carry a Geni.com profile ID (P2600), so the join is
genuinely worth doing — but pulling all half-million of them would be rude and
slow. Instead the reconciler asks only about the IDs we actually have, a few
hundred at a time, using a ``VALUES`` clause.

Every response is cached on disk under ``out/wikidata/cache/`` keyed by a hash
of the query, so re-running a report costs nothing and iterating on the analysis
does not mean hammering somebody else's public endpoint. Deleting the cache
directory is how you force a refresh.

Network access is injected (:class:`WikidataClient` takes a ``fetch``), so the
tests exercise the batching, caching and parsing without touching the network.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Sequence

__all__ = [
    "SPARQL_ENDPOINT",
    "API_ENDPOINT",
    "USER_AGENT",
    "WikidataClient",
    "Match",
    "match_by_geni_id",
]

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
API_ENDPOINT = "https://www.wikidata.org/w/api.php"

#: Wikimedia asks for a descriptive User-Agent that identifies the tool.
USER_AGENT = "genimerge/0.1 (Geni GEDCOM to Wikidata reconciliation; run by a researcher)"

#: How many Geni IDs to put in one ``VALUES`` clause. Large enough that 8766 IDs
#: is a couple of dozen queries, small enough to stay well inside the endpoint's
#: 60-second budget.
BATCH_SIZE = 400


@dataclass(frozen=True)
class Match:
    """One Wikidata item that claims one of our Geni IDs."""

    geni_id: str
    qid: str
    label: str = ""
    description: str = ""


def _http_fetch(url: str, data: bytes | None = None, headers: dict | None = None) -> bytes:
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Encoding": "gzip",
            **(headers or {}),
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = response.read()
        if response.headers.get("Content-Encoding") == "gzip":
            payload = gzip.decompress(payload)
        return payload


@dataclass
class WikidataClient:
    """A cached, polite, injectable client."""

    cache_dir: Path
    fetch: Callable[..., bytes] = _http_fetch
    delay: float = 1.0
    #: number of retries on a throttled or failing request
    retries: int = 3
    requests_made: int = field(default=0, init=False)
    cache_hits: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        self.cache_dir = Path(self.cache_dir)
        self._last_request = 0.0

    # -- caching -------------------------------------------------------

    def _cache_path(self, kind: str, key: str) -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:32]
        return self.cache_dir / kind / f"{digest}.json"

    def _cached(self, kind: str, key: str):
        path = self._cache_path(kind, key)
        if path.exists():
            self.cache_hits += 1
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def _store(self, kind: str, key: str, value) -> None:
        path = self._cache_path(kind, key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    # -- requests ------------------------------------------------------

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self._last_request = time.monotonic()

    def _request(self, url: str, data: bytes | None = None, headers: dict | None = None) -> bytes:
        last_error: Exception | None = None
        for attempt in range(self.retries):
            self._throttle()
            self.requests_made += 1
            try:
                return self.fetch(url, data, headers)
            except urllib.error.HTTPError as error:
                last_error = error
                # 429 too many requests, 500/503 endpoint under load: back off
                # and try again. Anything else is our fault, so stop.
                if error.code not in (429, 500, 502, 503, 504):
                    raise
                time.sleep(self.delay * (2 ** (attempt + 1)))
            except urllib.error.URLError as error:
                last_error = error
                time.sleep(self.delay * (2 ** (attempt + 1)))
        raise RuntimeError(f"giving up on {url[:120]} after {self.retries} attempts") from last_error

    # -- endpoints -----------------------------------------------------

    def sparql(self, query: str) -> list[dict]:
        """Run a SPARQL query and return its result bindings, flattened."""
        cached = self._cached("sparql", query)
        if cached is not None:
            return cached

        # POST rather than GET: a VALUES clause with 400 IDs makes a long URL.
        payload = urllib.parse.urlencode({"query": query, "format": "json"}).encode("utf-8")
        raw = self._request(
            SPARQL_ENDPOINT,
            payload,
            {
                "Accept": "application/sparql-results+json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        bindings = json.loads(raw)["results"]["bindings"]
        rows = [{k: v["value"] for k, v in row.items()} for row in bindings]
        self._store("sparql", query, rows)
        return rows

    def entities(self, ids: Sequence[str], languages: str = "en") -> dict:
        """Fetch labels and descriptions for up to 50 entity IDs."""
        key = f"{','.join(ids)}|{languages}"
        cached = self._cached("entities", key)
        if cached is not None:
            return cached

        url = API_ENDPOINT + "?" + urllib.parse.urlencode(
            {
                "action": "wbgetentities",
                "ids": "|".join(ids),
                "props": "labels|descriptions",
                "languages": languages,
                "languagefallback": "1",
                "format": "json",
            }
        )
        raw = self._request(url)
        entities = json.loads(raw).get("entities", {})
        self._store("entities", key, entities)
        return entities


def _qid(uri: str) -> str:
    """``http://www.wikidata.org/entity/Q42`` -> ``Q42``."""
    return uri.rsplit("/", 1)[-1]


def _batched(items: Sequence[str], size: int) -> Iterable[Sequence[str]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def match_by_geni_id(
    client: WikidataClient,
    geni_ids: Iterable[str],
    *,
    batch_size: int = BATCH_SIZE,
    progress: Callable[[int, int], None] | None = None,
) -> list[Match]:
    """Find Wikidata items whose P2600 is one of ``geni_ids``.

    Returns one :class:`Match` per (Geni ID, item) pair — deliberately not a
    dict, because the mapping is not guaranteed to be one-to-one and collapsing
    a double-match would hide exactly the cases a human needs to look at.
    """
    ordered = sorted(set(geni_ids), key=lambda s: (len(s), s))
    matches: list[Match] = []
    batches = list(_batched(ordered, batch_size))

    for index, batch in enumerate(batches, start=1):
        values = " ".join(f'"{gid}"' for gid in batch)
        query = (
            "SELECT ?item ?geni WHERE {\n"
            f"  VALUES ?geni {{ {values} }}\n"
            "  ?item wdt:P2600 ?geni.\n"
            "}"
        )
        for row in client.sparql(query):
            matches.append(Match(geni_id=row["geni"], qid=_qid(row["item"])))
        if progress is not None:
            progress(index, len(batches))

    return matches


def add_labels(client: WikidataClient, matches: list[Match], languages: str = "en") -> list[Match]:
    """Fill in labels and descriptions for matched items, 50 at a time."""
    qids = sorted({m.qid for m in matches})
    labels: dict[str, tuple[str, str]] = {}

    for batch in _batched(qids, 50):
        for qid, entity in client.entities(batch, languages).items():
            label = entity.get("labels", {}).get(languages, {}).get("value", "")
            description = entity.get("descriptions", {}).get(languages, {}).get("value", "")
            labels[qid] = (label, description)

    return [
        Match(
            geni_id=m.geni_id,
            qid=m.qid,
            label=labels.get(m.qid, ("", ""))[0],
            description=labels.get(m.qid, ("", ""))[1],
        )
        for m in matches
    ]
