"""Every label on every item Emma has made, against what our tree now says.

    BOT_CONTACT=you@example.com python scripts/audit-ledger-names.py

**Emma, 2026-08-28**, her last instruction before the crash: *"All the individuals that I've
worked on and any individuals that they've been merged into should basically always be all the
individuals that I've worked on, pretty much all of them. All the people that they've been merged
into should have audits done on their names to figure out the degree that we've messed them up."*

## Why there is damage to measure

Two changes landed on 2026-08-29, **after** most of her items were created:

* `derive-labels.py` made the **married** name the primary label — 251,707 labels flipped.
* the transliteration table went 218 → 3,261 tokens, so `ja`/`zh` became derivable for names that
  previously produced nothing.

An item created before either carries the **birth** name in `mul` and `en`, and — because `ja`/`zh`
are transliterated from `label_mul` — in Japanese and Chinese too. Her words: *"the CJK names are
being put in the birth name form"*.

## One row per item per language, which is the shape she asks for

`CLAUDE.md` § *"Analyse this" means build a CSV of every instance*: every instance, not a summary,
then decide. So a person with `mul`, `en`, `ja` and `zh` is four rows, each carrying what Wikidata
holds, what our tree says, and how they differ.

## Full items, not a summary, and not the local store

`genimerge.wikidata.full_entities`, batched 50 at a time — the pattern `CLAUDE.md` sanctions for
deciding what to emit, and the same call the daily builder already makes. The **local store is not
usable here**: it was downloaded 2026-08-25 and most of these items postdate it, which is exactly
how a previous session came to report that `Q467497` Arne Garborg had no parents.

## Merged items are followed, and that is half the instruction

*"any individuals that they've been merged into"*. A QID that has been merged away redirects, and
`wbgetentities` returns the **target** — so the audit reports the redirect explicitly rather than
silently auditing a different item than the ledger names. Those rows carry `redirected_to`.

Writes `reports/name-audit.csv` and prints the counts.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from bot_identity import agent as _bot_agent  # noqa: E402
from genimerge.wikidata import WikidataClient  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

LEDGER = ROOT / "reports" / "garborg-qids.tsv"
DERIVED = ROOT / "reports" / "derived-labels.csv"
OUT = ROOT / "reports" / "name-audit.csv"

#: The four the pipeline writes. `mul` first because it is the language-neutral label and the one
#: `CLAUDE.md` calls "the real label"; `ja`/`zh` last because they are derived from it, so a wrong
#: `mul` makes them wrong too and they are a consequence rather than an independent fault.
LANGS = ("mul", "en", "ja", "zh")


def main():
    if not _bot_agent():
        sys.exit("BOT_CONTACT is not set; Wikimedia answers an empty User-Agent with a bare 403")

    ledger = {}
    with LEDGER.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            g, q = (row.get("geni_id") or "").strip(), (row.get("qid") or "").strip()
            if g and q:
                ledger[q] = g
    print(f"{len(ledger)} items in the ledger")

    ours = {}
    with DERIVED.open(encoding="utf-8") as fh:
        want = set(ledger.values())
        for row in csv.DictReader(fh):
            if row["geni_id"] in want:
                ours[row["geni_id"]] = row
    print(f"{len(ours)} of them are in derived-labels.csv")

    # The transliterations, so `ja`/`zh` can be compared against what we WOULD emit rather than
    # only noticing they are absent.
    from importlib import import_module
    bgd = None
    table = {}
    tpath = ROOT / "reports" / "garborg-name-transliterations.tsv"
    if tpath.exists():
        for row in csv.DictReader(tpath.open(encoding="utf-8"), delimiter="\t"):
            table[row["token"]] = (row.get("ja", ""), row.get("zh", ""))

    def ours_label(geni_id, lang):
        row = ours.get(geni_id)
        if not row:
            return ""
        if lang in ("mul", "en"):
            return (row.get(f"label_{lang}") or row.get("label_mul") or "").strip()
        base = (row.get("label_mul") or "").strip()
        parts = []
        for token in base.split():
            if token not in table:
                return ""          # partial is worse than absent
            parts.append(table[token][0 if lang == "ja" else 1])
        sep = "・" if lang == "ja" else "·"
        return sep.join(parts)

    client = WikidataClient(ROOT / "out" / "wikidata" / "livecache")
    items = {}
    qids = sorted(ledger)
    for i in range(0, len(qids), 50):
        items.update(client.full_entities(qids[i:i + 50]))
        print(f"  fetched {min(i + 50, len(qids))}/{len(qids)}", flush=True)

    rows, counts = [], {"match": 0, "differs": 0, "absent_on_wikidata": 0, "we_have_none": 0}
    redirects = 0
    for qid in qids:
        item = items.get(qid) or {}
        geni_id = ledger[qid]
        landed = item.get("id", "")
        redirected = landed if landed and landed != qid else ""
        if redirected:
            redirects += 1
        labels = {k: v.get("value", "") for k, v in (item.get("labels") or {}).items()}
        aliases = {k: [a.get("value", "") for a in v]
                   for k, v in (item.get("aliases") or {}).items()}
        for lang in LANGS:
            live, mine = labels.get(lang, ""), ours_label(geni_id, lang)
            if not live and not mine:
                continue
            if not live:
                state = "absent_on_wikidata"
            elif not mine:
                state = "we_have_none"
            elif live == mine:
                state = "match"
            else:
                state = "differs"
            counts[state] += 1
            rows.append({
                "qid": qid, "redirected_to": redirected, "geni_id": geni_id, "lang": lang,
                "wikidata": live, "ours": mine, "state": state,
                # Whether the live label is one of the birth forms our own tree records. This
                # is what separates "our 08-29 flip has not reached this item" from "she wrote
                # something better than we can derive" -- the second must never be overwritten.
                "live_is_our_alias": str(
                    live in {a.strip() for a in
                             ((ours.get(geni_id) or {}).get("alias_names") or "").split(" | ")
                             if a.strip()}).lower(),
                "wikidata_aliases": " | ".join(aliases.get(lang, [])),
            })

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else
                           ["qid", "redirected_to", "geni_id", "lang", "wikidata", "ours",
                            "state", "live_is_our_alias", "wikidata_aliases"])
        w.writeheader()
        w.writerows(rows)

    print(f"\nwrote {OUT.relative_to(ROOT)} -- {len(rows):,} rows")
    for k, v in counts.items():
        print(f"  {k:20} {v:,}")
    print(f"  {'redirected items':20} {redirects:,}")
    fixable = sum(1 for r in rows if r["state"] == "differs" and r["live_is_our_alias"] == "true")
    print(f"\n{fixable:,} of the differences are Wikidata holding a birth name our tree "
          f"records as an alias -- those are ours to fix.")
    print(f"{counts['differs'] - fixable:,} differ some other way and must be read before "
          f"anything is emitted: Wikidata may simply be better.")


if __name__ == "__main__":
    main()
