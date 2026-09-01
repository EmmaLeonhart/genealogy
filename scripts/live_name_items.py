"""Ask Wikidata, right now, whether a name item already exists. Reuse beats creation.

**Emma, 2026-09-01:** *"I thought we reused name objects by default lol. The only hard situation
is patronymics which have an elaborate logic to them lol. Fuck you for defaulting to the
dangerous one lol."* And, 2026-08-29, on the same problem: *"Creating the name objects and having
them merged by somebody else (and this is important) is a thing that gets attention in a bad
way."*

## Why the existing check was not enough

`namemodel.store_name_item` resolves a token against `out/wikidata/name-items-in-store.tsv.gz`,
the **offline** download, plus `reports/created-name-items.tsv`, which holds 18 rows. Both are
snapshots. An item created since the download — by us, by her, or by anybody — is invisible to
them, and `CREATE` in QuickStatements never checks: it mints a new item every time.

Measured live on 2026-09-01, on the three tokens that day's batch was about to create:

    Voster     Q141244184 already exists
    Jonsson    Q21509276 (family name), plus Q141244185 and Q141242306
    Olofsson   Q23645132 (family name), plus Q141244186

So the batch would have made a fourth `Jonsson`. That is the exact shape another editor merged
away five times over — Tunheim, Ronneberg, Bø, Heigre, Nyvold.

## What this does, and the line it does not cross

One `wbsearchentities` call per token about to be **created**, then one batched `wbgetentities`
to read `P31` on the candidates. A candidate counts only when **the label matches exactly** after
case folding and **`P31` is the class this usage needs**. Nothing else is accepted:

* **No diacritic folding.** `CLAUDE.md` § *A diacritic makes a different name*: `María`, `Mária`
  and `Marià` are three names with three items, and folding them invented ambiguity for 1,312
  names once already.
* **No cross-usage reuse.** § *One name item per USAGE* — a given name and a family name spelled
  alike are genuinely two items, so a `Q101352` *family name* is never offered to a given-name
  slot.
* **Ambiguity is not resolved here.** Several qualifying candidates means the token is left to
  the existing ambiguous path, which holds it for her. Picking one would be the coin flip this
  repo refuses everywhere else.

**It is a small number of requests.** The batch creates a handful of tokens a day, so this is
courteous by construction — `CLAUDE.md` § *Querying Wikidata is ALLOWED* asks for batching and
for not fanning out, and this batches the entity reads.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request

API = "https://www.wikidata.org/w/api.php"

#: `P31` values that make an item the right kind of name for each usage.
CLASSES = {
    "family": {"Q101352"},
    "given": {"Q202444", "Q12308941", "Q11879590", "Q3409032"},
    "patronymic": {"Q110874"},
}

_CACHE: dict[tuple[str, str], str] = {}


def _get(params, agent):
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(API + "?" + q, headers={"User-Agent": agent})
    with urllib.request.urlopen(req, timeout=60) as fh:
        return json.loads(fh.read().decode("utf-8"))


def existing_item(token, usage, agent="genimerge name reuse (emma@topazcomputing.com)"):
    """The QID of an existing name item for `(token, usage)`, or `''`.

    Returns `''` both when nothing exists and when SEVERAL qualifying items do — an ambiguity
    belongs on her deck, not in a guess made here.
    """
    want = CLASSES.get(usage)
    if not want or not token:
        return ""
    key = (token.casefold(), usage)
    if key in _CACHE:
        return _CACHE[key]
    _CACHE[key] = ""
    try:
        found = _get({"action": "wbsearchentities", "search": token, "language": "en",
                      "type": "item", "limit": "12", "format": "json"}, agent)
    except Exception:                                               # noqa: BLE001
        return ""
    ids = [h["id"] for h in found.get("search", [])
           if (h.get("label") or "").casefold() == token.casefold()]
    if not ids:
        return ""
    time.sleep(0.3)
    try:
        ents = _get({"action": "wbgetentities", "ids": "|".join(ids[:12]),
                     "props": "claims|labels", "languages": "en|mul",
                     "format": "json"}, agent).get("entities", {})
    except Exception:                                               # noqa: BLE001
        return ""
    ok = []
    for qid, e in ents.items():
        labels = {v.get("value", "").casefold() for v in (e.get("labels") or {}).values()}
        if token.casefold() not in labels:
            continue
        classes = set()
        for st in (e.get("claims") or {}).get("P31", []):
            v = st.get("mainsnak", {}).get("datavalue", {}).get("value")
            if isinstance(v, dict) and v.get("id"):
                classes.add(v["id"])
        if classes & want:
            ok.append(qid)
    # Exactly one, or nothing. Several is an ambiguity and is hers.
    _CACHE[key] = ok[0] if len(ok) == 1 else ""
    return _CACHE[key]
