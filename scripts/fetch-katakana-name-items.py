"""Fetch the katakana Wikidata holds for name tokens our slice of it is missing.

    py scripts/fetch-katakana-name-items.py [--top N]

**The `ja` step's one remaining gap, and it is not a language problem.** A name is rendered only
when **every** token has a sourced katakana form, so **863,014 people fail on a partial**. The
commonest blockers are ordinary given names — `Carl` 11,236 people, `John` 7,437, `Anders` 6,714,
`Johansson` 6,656 — which **have** katakana on Wikidata but no name item inside
`out/wikidata/name-items-in-store.tsv`, a Geni-shaped slice downloaded for a different purpose.

So this fetches what Wikidata already knows. **Nothing is transliterated** — `CLAUDE.md` is
explicit that established Japanese spellings of European names are conventional rather than
derivable, and that CJK↔Latin is agentic, never programmatic.

## Why SPARQL and not `wbsearchentities`

One query answers 150 tokens. Searching per token would be thousands of requests for the same
answer, and § *Querying Wikidata is ALLOWED* asks for exactly this shape: batch where the API
offers batching, and do not fan out one request per item.

The query is restricted to **name items** — `Q202444` given name, `Q101352` family name,
`Q12308941` male given name, `Q11879590` female given name, `Q3409032` unisex given name,
`Q110874` patronymic. That restriction is doing real work: it is why `von`, `af`, `de` and `la`
return nothing instead of returning a place or a preposition. **Those particles need her ruling,
not a lookup** — they are not names and have conventional Japanese forms.

## What is rejected

* **A value that is not pure katakana.** `Carl` comes back as both `カール` and `カール/カレル`;
  the second is two readings in one string, which is not a name anybody is called.
* **A token with more than one distinct katakana form** is recorded with all of them and used
  only if one is unambiguous, because picking between two conventions is the thing this file
  refuses to do.

Writes `reports/katakana-name-items.tsv`, which `scripts/build-ja-labels.py` reads alongside the
store.
"""
from __future__ import annotations

import argparse
import collections
import csv
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

TAB = chr(9)
DERIVED = ROOT / "reports" / "derived-labels.csv"
STORE = ROOT / "out" / "wikidata" / "name-items-in-store.tsv"
OUT = ROOT / "reports" / "katakana-name-items.tsv"

ENDPOINT = "https://query.wikidata.org/sparql"
AGENT = "genimerge katakana name items (emma@topazcomputing.com)"

KATAKANA = re.compile(r"^[゠-ヿㇰ-ㇿ々・]+$")
LATIN_TOKEN = re.compile(r"^[A-Za-zÀ-ɏ'.-]+$")

#: The name classes. Restricting to these is what keeps particles out: `von` is not an instance
#: of any of them, so it returns nothing rather than returning something wrong.
NAME_CLASSES = ("Q202444", "Q101352", "Q12308941", "Q11879590", "Q3409032", "Q110874")

QUERY = """SELECT ?en ?ja WHERE {
  VALUES ?en { %s }
  VALUES ?cls { %s }
  ?item wdt:P31 ?cls ; rdfs:label ?en ; rdfs:label ?ja .
  FILTER(LANG(?ja)="ja")
}"""


def held_tokens():
    """The Latin tokens that already have katakana in our slice."""
    have = {}
    if not STORE.exists():
        return have
    with io.open(STORE, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=TAB):
            labs = [x for x in (r.get("labels") or "").split("|") if x]
            kana = [x for x in labs if KATAKANA.match(x)]
            if not kana:
                continue
            for lat in labs:
                if LATIN_TOKEN.match(lat):
                    have.setdefault(lat.casefold(), kana[0])
                    break
    return have


def blocking_tokens(have):
    """`[(token, people it blocks)]`, commonest first, over people who fail on a PARTIAL only.

    A person with no renderable token at all is not unblocked by one lookup, so they are not
    what this ranks. A person missing one token of four is.
    """
    blocked = collections.Counter()
    with io.open(DERIVED, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            en = (row.get("label_en") or "").strip()
            if not en:
                continue
            toks = en.split()
            if not all(LATIN_TOKEN.match(t) for t in toks):
                continue
            missing = [t for t in toks if t.casefold() not in have]
            if missing and len(missing) < len(toks):
                blocked.update(missing)
    return blocked.most_common()


def ask(tokens):
    """`{token: {katakana forms}}` for one chunk."""
    vals = " ".join('"%s"@en' % t.replace('"', '') for t in tokens)
    cls = " ".join("wd:" + c for c in NAME_CLASSES)
    url = ENDPOINT + "?" + urllib.parse.urlencode(
        {"query": QUERY % (vals, cls), "format": "json"})
    req = urllib.request.Request(url, headers={
        "User-Agent": AGENT, "Accept": "application/sparql-results+json"})
    with urllib.request.urlopen(req, timeout=180) as fh:
        data = json.loads(fh.read().decode("utf-8"))
    out = collections.defaultdict(set)
    for r in data["results"]["bindings"]:
        ja = r["ja"]["value"].strip()
        # Not pure katakana means it is not a single reading -- `カール/カレル` is two.
        if KATAKANA.match(ja):
            out[r["en"]["value"]].add(ja)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--top", type=int, default=3000,
                    help="how many of the commonest blocking tokens to look up")
    ap.add_argument("--chunk", type=int, default=150)
    args = ap.parse_args()

    have = held_tokens()
    print("%s tokens already carry katakana in our slice" % format(len(have), ","))
    ranked = blocking_tokens(have)
    print("%s distinct tokens block at least one person" % format(len(ranked), ","))
    want = [t for t, _n in ranked[:args.top]]
    covered = sum(n for _t, n in ranked[:args.top])
    print("looking up the top %s, which account for %s token-blocks"
          % (format(len(want), ","), format(covered, ",")))

    found, ambiguous = {}, {}
    for i in range(0, len(want), args.chunk):
        chunk = want[i:i + args.chunk]
        try:
            got = ask(chunk)
        except Exception as exc:                                       # noqa: BLE001
            print("  chunk at %d failed (%s); those tokens stay unresolved" % (i, exc),
                  file=sys.stderr)
            time.sleep(3)
            continue
        for tok, forms in got.items():
            if len(forms) == 1:
                found[tok] = next(iter(forms))
            else:
                ambiguous[tok] = sorted(forms)
        print("  %5d/%d  found %s" % (min(i + args.chunk, len(want)), len(want),
                                      format(len(found), ",")), file=sys.stderr)
        time.sleep(1.0)

    rank = {t: n for t, n in ranked}
    rows = [[t, k, rank.get(t, 0), "single"] for t, k in found.items()]
    rows += [[t, " | ".join(v), rank.get(t, 0), "ambiguous, NOT used"]
             for t, v in ambiguous.items()]
    rows.sort(key=lambda r: (-r[2], r[0]))
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["token", "katakana", "people_blocked", "state"])
        w.writerows(rows)

    print("\nwrote %s" % OUT.relative_to(ROOT))
    print("   %s tokens resolved to ONE katakana form" % format(len(found), ","))
    print("   %s came back with more than one and are NOT used" % format(len(ambiguous), ","))
    print("   %s of the %s asked for returned nothing -- mostly particles and surnames "
          "Wikidata has no name item for"
          % (format(len(want) - len(found) - len(ambiguous), ","), format(len(want), ",")))
    unblocked = sum(rank.get(t, 0) for t in found)
    print("\nthose %s tokens sit on %s token-blocks" % (format(len(found), ","),
                                                        format(unblocked, ",")))
    print("\nthe twelve biggest wins:")
    for r in rows[:12]:
        if r[3] == "single":
            print("   %-16s %-14s %s people" % (r[0], r[1], format(r[2], ",")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
