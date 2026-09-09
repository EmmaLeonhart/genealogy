"""Ask Wikidata, right now, whether a name item already exists. Reuse beats creation.

**Name objects are REUSED by default.** The only hard case is patronymics, which have their own
elaborate logic; defaulting to creation is the dangerous choice and is wrong. And, on the same
problem: *"Creating the name objects and having
them merged by somebody else (and this is important) is a thing that gets attention in a bad
way."*

## Why the existing check was not enough

`namemodel.store_name_item` resolves a token against `out/wikidata/name-items-in-store.tsv.gz`,
the **offline** download, plus `reports/created-name-items.tsv`, which holds 18 rows. Both are
snapshots. An item created since the download — by us or by anybody — is invisible to
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
  the existing ambiguous path, which holds it for review. Picking one would be the coin flip this
  repo refuses everywhere else.

## ⛔ THIS CANNOT SEE AN ITEM CREATED MINUTES AGO, and those are the ones a daily batch duplicates

`wbsearchentities` reads the **search index**, which Wikidata populates asynchronously. An item
that exists is retrievable by `wbgetentities` immediately and may not be findable by search for
some time after. So this check is blind in exactly the window that matters: the duplicate a daily
cadence produces is one created by yesterday's batch or by an earlier run of today's.

The failure, 2026-09-05: *"the quickstatements I most recently ran tried to make duplicate surnames
again lol"* — `Låge-Håland`, refused because `Q141257135` already held that label and
description. All four lookups missed it, each for its own reason: the offline store predates the
item, the bearers do not point at it yet, `created-name-items.tsv` was never being refreshed, and
this function could not see it.

**`refresh-created-name-items.py` is the source with no lag**, because it reads the account's
contributions
rather than the index. It is now run as part of `build-garborg-day.py --compose`, beside the
ledger refresh. This function stays as the last resort it always was — it catches items created
by *other people*, which contributions cannot.

**It is a small number of requests.** The batch creates a handful of tokens a day, so this is
courteous by construction — `CLAUDE.md` § *Querying Wikidata is ALLOWED* asks for batching and
for not fanning out, and this batches the entity reads.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.error
import urllib.request

API = "https://www.wikidata.org/w/api.php"

#: `P31` values that make an item the right kind of name for each usage.
CLASSES = {
    "family": {"Q101352"},
    "given": {"Q202444", "Q12308941", "Q11879590", "Q3409032"},
    "patronymic": {"Q110874"},
}

_CACHE: dict[tuple[str, str], str] = {}


class LookupUnavailable(Exception):
    """The question could not be ASKED. Distinct from asking and finding nothing.

    **This exists because the two were the same value and the answer to both was "create it".**
    Every request here was wrapped in `except Exception: return ""`, so a 429, a timeout, a
    blocked proxy and a genuinely absent item were indistinguishable — and `""` means *no item
    exists*, which sends the token straight to `CREATE`. A network blip therefore minted a
    duplicate of something that was already on Wikidata, silently, on the one code path where
    duplicates are the whole thing being guarded against.

    `CLAUDE.md` § *Our side could never have two children*: an empty join is indistinguishable
    from an absence of data, and absence is exactly what these checks exist to detect. So a
    failed lookup raises, and the caller HOLDS the token — the carry-forward already exists for
    "not today", and holding is free while a duplicate is permanent and gets merged away by
    somebody else.
    """


#: The floor between two requests from this process, in seconds, and the 429 back-off ladder.
#:
#: **Measured 2026-09-07, pipeline run 246: EVERY live read in the name-items generator failed
#: with `HTTP Error 429: Your bot is making too many requests`** — all 137 chunks of the
#: description check over 6,833 items, and then all 2 chunks of the `P144` check, which inherited
#: the rate-limited state. So the whole existing-item enrichment emitted nothing: *"0 P144
#: statement(s) to add; 89 item(s) held, the live read failed"*, and the same for `P460` and for
#: the `P144` REMOVALS ruled on the `Junna` items.
#:
#: `CLAUDE.md` § *Querying Wikidata is ALLOWED. Be polite about the rate* is the rule this broke:
#: *"do not fan out one request per item when one request would do, and do not hammer to finish
#: faster."* 137 `wbgetentities` calls back to back with no pause is hammering, and Wikimedia
#: said so.
#:
#: **It lands in `_get` because that is the one place every caller goes through.** Pacing it at a
#: call site would leave the next caller written to hammer again — the same reasoning that puts
#: `given_name_run` and `drop_description_suffix` each in one place.
_MIN_INTERVAL = 0.25
_BACKOFF = (2, 5, 15, 45)
_last_request = 0.0


def _get(params, agent):
    """One paced, 429-aware GET against the Wikidata API.

    **A 429 is retried, never swallowed.** The callers here treat a failed lookup as *hold this
    item* rather than as *nothing is there* — which is right and is why run 246 emitted no wrong
    statement — but a hold that fires on every item every run is indistinguishable from the
    feature not existing. Retrying is what makes the hold mean what it says.

    `Retry-After` is honoured when Wikimedia sends one, because their number is better than ours.
    """
    global _last_request
    for attempt, wait in enumerate((0,) + _BACKOFF):
        if wait:
            time.sleep(wait)
        gap = _MIN_INTERVAL - (time.monotonic() - _last_request)
        if gap > 0:
            time.sleep(gap)
        q = urllib.parse.urlencode(params)
        req = urllib.request.Request(API + "?" + q, headers={"User-Agent": agent})
        try:
            with urllib.request.urlopen(req, timeout=60) as fh:
                return json.loads(fh.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            # 429 too many requests, 503 service unavailable: ours to wait out. Anything else
            # -- a 400 on a malformed id, a 404 -- is a real answer and is raised at once.
            if exc.code not in (429, 503) or attempt == len(_BACKOFF):
                raise
            retry_after = (exc.headers or {}).get("Retry-After")
            try:
                if retry_after and int(retry_after) > 0:
                    time.sleep(min(int(retry_after), 120))
            except (TypeError, ValueError):
                pass
        finally:
            _last_request = time.monotonic()


def existing_item(token, usage, agent="genimerge name reuse (emma@topazcomputing.com)"):
    """The QID of an existing name item for `(token, usage)`, or `''`.

    Returns `''` both when nothing exists and when SEVERAL qualifying items do — an ambiguity
    belongs on the adjudication deck, not in a guess made here.

    **Raises `LookupUnavailable` when the question could not be asked at all**, which is a
    different thing from either and must not reach the caller as `''`. See that class.
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
    except Exception as exc:                                        # noqa: BLE001
        del _CACHE[key]          # never cache a non-answer as "nothing exists"
        raise LookupUnavailable(f"wbsearchentities {token!r}: {exc}") from exc
    ids = [h["id"] for h in found.get("search", [])
           if (h.get("label") or "").casefold() == token.casefold()]
    if not ids:
        return ""
    time.sleep(0.3)
    try:
        ents = _get({"action": "wbgetentities", "ids": "|".join(ids[:12]),
                     "props": "claims|labels", "languages": "en|mul",
                     "format": "json"}, agent).get("entities", {})
    except Exception as exc:                                        # noqa: BLE001
        del _CACHE[key]
        raise LookupUnavailable(f"wbgetentities {token!r}: {exc}") from exc
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
    # Exactly one, or nothing. Several is an ambiguity and is decided by hand.
    _CACHE[key] = ok[0] if len(ok) == 1 else ""
    return _CACHE[key]
