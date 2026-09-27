"""Resolve the places people were born and died in to Wikidata items.

    python scripts/resolve-places.py [--budget N]

`queue.md`, 2026-09-26: *"take the places of birth, death, marriage and so on (FamilySearch
standardises them) and resolve each to its Wikidata item so they link properly, as part of a
comprehensive ontology."* A later pipeline stage: this writes the mapping and emits no edit.

**Scope: the places of people who have an item** (`reports/garborg-qids.tsv`), read from
`reports/derived-places.csv`. That is 5,616 distinct strings where the whole tree has 235,045.

**Right to left, each part inside the one after it.** `Gjesdal, Rogaland, Norway` resolves
`Norway` first, then a `Rogaland` whose country (`P17`) or containing unit (`P131`) is that
item, then a `Gjesdal` inside `Rogaland`. A part that cannot be placed inside its parent stops
the walk, and the string resolves to the most specific part that WAS placed, with `depth`
saying how far that is from the full string. So a farm name that Wikidata does not have
(`Stokka, Gjesdal, Rogaland, Norway`) comes back as Gjesdal at depth 3 of 4, never as a guess.

**A lone name is resolved only when it is unambiguous.** `Stockholm` is a single place; `Bø` is
a dozen. With nothing to place it inside, a part with more than one place-like candidate of
that exact label is left unresolved.

**Incremental.** `reports/place-qids.tsv` is the cache and the output; a run resolves at most
`--budget` new strings, most-used first, so `places.yml` grows it a little every day on its own clock.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
try:
    from bot_identity import BOT_USER_AGENT
except Exception:                                                   # noqa: BLE001
    BOT_USER_AGENT = ""
UA = BOT_USER_AGENT or "genealogy-place-resolver/1.0"
API = "https://www.wikidata.org/w/api.php"
OUT = ROOT / "reports" / "place-qids.tsv"
FIELDS = ["place", "qid", "resolved_part", "depth", "parts", "method"]

#: `P31` values that make an item a country, which may stand at the right end with no parent.
COUNTRY_CLASSES = {"Q6256", "Q3624078", "Q3024240", "Q7275", "Q1763527", "Q417175"}
#: A current state wins over a historical one of the same name: `Norway` is `Q20`, not `Q2196956`.
CURRENT_STATE = {"Q6256", "Q3624078"}


def api(params, _tries=[0]):
    params = {**params, "format": "json", "maxlag": 5}
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}),
                                        timeout=60) as r:
                got = json.load(r)
            if got.get("error", {}).get("code") == "maxlag":
                time.sleep(10)
                continue
            time.sleep(0.2)  # serial requests; maxlag and 429 are honoured above
            return got
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(int(e.headers.get("Retry-After") or 30))
                continue
            raise
    raise RuntimeError("Wikidata kept refusing: " + url)


_search_cache: dict = {}
_entity_cache: dict = {}


def candidates(name):
    """Items whose label or alias is exactly `name`, in any language, with their claims."""
    if name in _search_cache:
        return _search_cache[name]
    ids = []
    for lang in ("en", "mul", "nb", "sv", "da", "de", "fr"):
        got = api({"action": "wbsearchentities", "search": name, "language": lang,
                   "strictlanguage": 0, "type": "item", "limit": 20})
        for hit in got.get("search", []):
            if hit.get("match", {}).get("text", "").casefold() == name.casefold():
                ids.append(hit["id"])
    ids = list(dict.fromkeys(ids))
    need = [q for q in ids if q not in _entity_cache]
    for i in range(0, len(need), 50):
        got = api({"action": "wbgetentities", "ids": "|".join(need[i:i + 50]),
                   "props": "claims"})
        for q, ent in got.get("entities", {}).items():
            claims = ent.get("claims", {})

            def vals(p):
                out = set()
                for c in claims.get(p, []):
                    v = c.get("mainsnak", {}).get("datavalue", {}).get("value")
                    if isinstance(v, dict) and v.get("id"):
                        out.add(v["id"])
                return out
            _entity_cache[q] = {"p31": vals("P31"), "p17": vals("P17"), "p131": vals("P131"),
                                "coords": "P625" in claims}
    out = [(q, _entity_cache[q]) for q in ids if q in _entity_cache]
    # A place has coordinates or sits in a country; everything else (a person, a ship, a
    # family name) is not a candidate for where somebody was born.
    out = [(q, e) for q, e in out if e["coords"] or e["p17"] or e["p31"] & COUNTRY_CLASSES]
    _search_cache[name] = out
    return out


def inside(e, parent):
    return parent in e["p17"] or parent in e["p131"]


def resolve(place):
    parts = [p.strip() for p in place.split(",") if p.strip()]
    if not parts:
        return None
    qid, part, depth, method = "", "", 0, "unresolved"
    parent = None
    for i, name in enumerate(reversed(parts)):
        cands = candidates(name)
        if parent is None:
            # The rightmost part stands alone: a country, or the one place-like item there is.
            countries = [q for q, e in cands if e["p31"] & COUNTRY_CLASSES]
            current = [q for q, e in cands if e["p31"] & CURRENT_STATE]
            pick = current or countries or [q for q, _e in cands]
            if len(pick) != 1:
                method = "ambiguous" if pick else "unresolved"
                break
            parent = pick[0]
        else:
            pick = [q for q, e in cands if inside(e, parent)]
            # Directly inside (`P131`) beats merely in the same country (`P17`): `Rogaland` the
            # county is `P131 Q20`; the other `Rogaland` only shares the country.
            direct = [q for q, e in cands if parent in e["p131"]]
            if len(pick) > 1 and len(direct) == 1:
                pick = direct
            if len(pick) != 1:
                break
            parent = pick[0]
        qid, part, depth = parent, name, i + 1
        method = "hierarchy" if len(parts) > 1 else "unique"
    return {"place": place, "qid": qid, "resolved_part": part, "depth": depth,
            "parts": len(parts), "method": method if qid else method}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=200, help="new strings to resolve this run")
    args = ap.parse_args()
    csv.field_size_limit(1 << 30)
    with open(ROOT / "reports" / "garborg-qids.tsv", encoding="utf-8") as f:
        ours = {r["geni_id"] for r in csv.DictReader(f, delimiter="\t") if r.get("qid")}
    uses = collections.Counter()
    with open(ROOT / "reports" / "derived-places.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["geni_id"] in ours:
                for k in ("birth_place", "death_place"):
                    v = (r.get(k) or "").strip()
                    if v:
                        uses[v] += 1
    done = {}
    if OUT.exists():
        with open(OUT, encoding="utf-8") as f:
            done = {r["place"]: r for r in csv.DictReader(f, delimiter="\t")}
    todo = [p for p, _n in sorted(uses.items(), key=lambda kv: (-kv[1], kv[0])) if p not in done]
    print(f"{len(uses)} places in scope, {len(done)} cached, {len(todo)} to go; "
          f"resolving {min(len(todo), args.budget)}")
    def save():
        rows = sorted(done.values(), key=lambda r: r["place"])
        tmp = OUT.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        tmp.replace(OUT)
        return rows

    # Saved after every place, so a run cut short by its time cap keeps what it resolved.
    for place in todo[:args.budget]:
        got = resolve(place)
        if got:
            done[place] = got
            save()
    rows = save()
    full = sum(1 for r in rows if r["qid"] and int(r["depth"]) == int(r["parts"]))
    part = sum(1 for r in rows if r["qid"] and int(r["depth"]) < int(r["parts"]))
    print(f"{len(rows)} cached: {full} resolved in full, {part} to a containing place, "
          f"{len(rows) - full - part} not resolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
