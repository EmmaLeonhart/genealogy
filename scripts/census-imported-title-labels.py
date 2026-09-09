#!/usr/bin/env python3
"""Every store item that is a PERSON and whose Latin label carries a rank word or a `|`.

**`Q110731142` reads `noble Nike|Victoria Soutzaina`, and it is one of a great many.** A large
number of people on Wikidata carry the prefix `noble`, all imported by one editor in 2022, and
all of them have the title inside the `mul` label, where it reads as an English label rather
than a language-neutral one. The local Wikidata export holds all of these people, so their
labels can be redone properly from it.

**Two artefacts, both on that one item.** `noble` is a RANK, not a name — Genealogics files it in
its own column and `GZWDer`'s semi-automatic import of January 2022 carried it into the label
verbatim; `Kristbaumbot` then copied `en` into `mul` in June 2025, so the language-neutral label
is now an English sentence. And `Nike|Victoria` is Genealogics' separator for two spellings of one
name, which nobody searches for.

**A CLASS IS NOT A PERSON, and it is the guard that matters most here.** `Q113291098` is *noble
women* and `Q13417114` is *noble family*; both open with the word and neither is anybody. Every
row is `P31` = `Q5` *human*, tested on the ITEM rather than on the string.

**This script only READS.** It is the expensive half — one pass over all 2,427 shards, ~20
minutes — and it deliberately proposes nothing: `scripts/propose-title-label-fixes.py` computes
what each label should become, from this file, in seconds. Splitting them is what makes the
proposal rule reviewable without paying for the scan again, and the scan is the part that cannot
be iterated on.

**The bound on the answer.** The store is a Geni-shaped slice of Wikidata — 2.4M items seeded
from `P2600` holders and their neighbours — so a count here is *of our export*, never of
Wikidata. § *"Is X present?"* requires that be said rather than implied.
"""
import csv
import gzip
import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from namemodel import _LEADING_TITLES  # noqa: E402

#: `noble` and its cognates. Absent from `_LEADING_TITLES` because that set was read off Geni's
#: own name fields, where the word does not occur — it is Genealogics' rank column, and it
#: reaches us only through Wikidata.
EXTRA_TITLES = frozenset({
    "noble", "nobile", "noblewoman", "nobleman", "edler", "edle",
})

TITLES = frozenset(t.casefold() for t in _LEADING_TITLES) | EXTRA_TITLES

#: The languages a Latin label of this shape sits in, in the order `Q110731142` shows them.
#: `mul` first, because that is the one that must not read as English.
LANGS = ("mul", "en", "en-ca", "en-us", "fr", "de", "nl", "sv", "da", "nb", "no",
         "fi", "et", "es", "it", "pt", "la", "pl", "cs", "hu")

HUMAN = "Q5"
COLS = ["qid", "kind", "leading_title", "live_mul", "live_en",
        "langs_carrying_live", "geni_ids", "created_by", "created_at"]


def leading_title_run(label):
    """The leading rank tokens, and the rest. `noble Nike Soutzaina` -> (`noble`, `Nike Soutzaina`).

    **Never to empty**, the floor `namemodel.drop_leading_title` already keeps: a label whose
    only token is a rank word keeps it, which is what protects a genuine surname `Noble`.
    """
    toks = (label or "").split()
    taken = []
    while len(toks) > 1 and toks[0].strip("()[]{},.").casefold() in TITLES:
        taken.append(toks.pop(0))
    return " ".join(taken), " ".join(toks)


def _ids(claims, prop):
    out = []
    for st in (claims or {}).get(prop, []):
        v = ((st.get("mainsnak") or {}).get("datavalue") or {}).get("value") or {}
        if isinstance(v, dict) and v.get("id"):
            out.append(v["id"])
    return out


def _strings(claims, prop):
    out = []
    for st in (claims or {}).get(prop, []):
        v = ((st.get("mainsnak") or {}).get("datavalue") or {}).get("value")
        if isinstance(v, str):
            out.append(v)
    return out


def main():
    shards = sorted((ROOT / "wikidata" / "items").glob("items-*.jsonl.gz"))
    if not shards:
        sys.exit("no store shards under wikidata/items/ -- this needs the full export")

    dest = ROOT / "reports" / "imported-title-labels.tsv"
    words = Counter()
    kinds = Counter()
    rows = []
    scanned = 0

    for k, shard in enumerate(shards):
        with gzip.open(shard, "rt", encoding="utf-8") as f:
            for line in f:
                scanned += 1
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                labs = d.get("labels") or {}
                mul = (labs.get("mul") or {}).get("value") or ""
                en = (labs.get("en") or {}).get("value") or ""
                primary = mul or en
                if not primary:
                    continue
                title, _rest = leading_title_run(primary)
                piped = "|" in primary
                if not title and not piped:
                    continue
                if HUMAN not in _ids(d.get("claims"), "P31"):
                    continue
                kind = ("title+pipe" if title and piped
                        else "title" if title else "pipe")
                kinds[kind] += 1
                if title:
                    words[title.split()[0].casefold()] += 1
                rows.append({
                    "qid": d.get("id", ""),
                    "kind": kind,
                    "leading_title": title,
                    "live_mul": mul,
                    "live_en": en,
                    "langs_carrying_live": " ".join(
                        lg for lg in LANGS
                        if (labs.get(lg) or {}).get("value") == primary),
                    "geni_ids": " ".join(_strings(d.get("claims"), "P2600")),
                    # Provenance, so *"the same guy in 2022"* is checkable rather than assumed.
                    # The store carries no revision author, so these stay blank here and are
                    # filled by a live read if that question is ever worth the requests.
                    "created_by": "",
                    "created_at": "",
                })
        if k % 300 == 0:
            print(f"  shard {k}/{len(shards)}  items {scanned:,}  matched {len(rows):,}",
                  flush=True)

    # **ONE ROW PER ITEM, and the store does not guarantee that on its own.** 6 items appear in
    # two shards each -- an artefact of how the download was partitioned, not of the data: all 9
    # duplicate rows are byte-identical. Left alone they emit each label edit twice and make the
    # census report 44,099 items where there are 44,090.
    seen = {}
    for r in rows:
        seen[r["qid"]] = r
    dropped = len(rows) - len(seen)
    rows = list(seen.values())

    # § *SORTING MUST BE DETERMINISTIC* -- the QID is unique, so numeric order on it is total.
    rows.sort(key=lambda r: (int(r["qid"][1:]) if r["qid"][1:].isdigit() else 0, r["qid"]))

    tmp = dest.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, dest)

    print(f"\nscanned {scanned:,} store items")
    if dropped:
        print(f"{dropped} duplicate shard row(s) collapsed -- the store holds these items twice")
    print(f"{len(rows):,} of them are `P31` Q5 human AND carry a rank word or a `|`")
    for kind, n in kinds.most_common():
        print(f"    {n:7,}  {kind}")
    print(f"wrote {dest.relative_to(ROOT)}")
    print("\nleading rank word, most common first -- READ THIS before widening the vocabulary:")
    for word, n in words.most_common(80):
        print(f"  {n:7,}  {word}")


if __name__ == "__main__":
    main()
