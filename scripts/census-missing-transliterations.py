"""Which name tokens block a `ja`/`zh` label, and how many people each one costs.

    python scripts/census-missing-transliterations.py

**Emma, 2026-08-26:** *"I'm confused why the created individuals are not getting their names
across different languages. Chinese and Japanese should be mandatory on the creations."*

**They are not getting them because the table is small and the rule is all-or-nothing.**
`reports/garborg-name-transliterations.tsv` holds **113 tokens**, built for the original Garborg
family, and `label_in()` returns nothing unless EVERY token of a name is in it — deliberately,
per `CLAUDE.md`: *"Partial is worse than absent: half a name in katakana and half in Latin is not
a Japanese label, it is a broken one."* So one unknown token costs the whole label. In the run of
2026-08-26 that was **32 of 36 creations**.

**The rule is right and the table is the problem**, so this measures the table's gap rather than
proposing to loosen anything.

## Why it counts BLOCKED PEOPLE, not token frequency

A token borne by fifty people who each carry three *other* unknown tokens unblocks nobody on its
own. The useful ranking is *how many people become fully covered if this token is added* —
counted both ways, so a token that is the last one missing for somebody sorts above one that is
merely common.

## Not every missing token is a name

The labels themselves carry text that should never be transliterated, and filling it in would be
closing a gap that ought not to exist:

* a **quoted nickname** — `Stine "Stena" Eivindsdatter Garborg` — which the name model makes
  `P1449` *nickname*, not part of any label;
* **titles** — `Queen of Sweden`, `margrave of Friuli, king of Italy` — where `of`, `Queen`,
  `Duke` and `margrave` are English office words.

They are marked rather than dropped: the real fix is upstream, in what gets handed to the
transliterator, and that is a labelling decision rather than a table one.

**The population is the ledger plus the current batch** — the hyperlocal neighbourhood the daily
run touches, not the whole 1.3M-person corpus, where the answer would be tens of thousands of
tokens and useless.

Writes `reports/missing-transliterations.tsv`, ready to be filled in and appended to the table.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "reports" / "garborg-name-transliterations.tsv"
OUT = ROOT / "reports" / "missing-transliterations.tsv"

#: English office words. A label carrying one is a name-plus-title string, and the title is
#: not something to render in katakana.
TITLE_WORDS = {"of", "the", "and", "&", "queen", "king", "duke", "duchess", "margrave",
               "count", "countess", "earl", "lord", "lady", "prince", "princess",
               "emperor", "empress", "baron", "baroness", "sir", "saint", "st"}


#: Place names that reach the token list through a TITLE -- `Duke of Estland, Blekinge and
#: Lolland`, `margrave of Friuli`, `Willa of Tuscany`. A place is not a person's name and does
#: not belong in a personal label at all, so transliterating it papers over the real problem.
PLACES = {"estland", "blekinge", "lolland", "danzig", "gdańsk", "italy", "sweden",
          "tuscany", "cysoing", "friuli", "näs", "austråt", "ivrea"}

#: Swedish `ätt` = clan. `Folkungaätten`, `Skarsholmsätten` and the bare fragment `ätt)` are
#: family-line words, not names.
CLAN_WORDS = ("ätten", "ätt", "ättens")


def kind(token):
    bare = token.strip(',.;')
    if token.startswith('"') or token.endswith('"'):
        return "quoted nickname -- P1449, not a label"
    if token != bare or "(" in token or ")" in token:
        return "punctuation artefact -- the label needs fixing, not transliterating"
    if bare.casefold() in TITLE_WORDS:
        return "title word, not a name"
    if bare.casefold() in PLACES:
        return "place from a title, not a name"
    if bare.casefold().endswith(CLAN_WORDS):
        return "clan word, not a name"
    if len(bare) <= 2 and bare.casefold() not in ("li",):
        return "particle or initial, not a name"
    return "name"


def table_tokens():
    with open(TABLE, encoding="utf-8") as f:
        return {row["token"] for row in csv.DictReader(f, delimiter="\t")}


def population():
    """Ledger people plus everybody the current batch creates -- the hyperlocal set."""
    ids = set()
    with open(ROOT / "reports" / "garborg-qids.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if (row.get("geni_id") or "").isdigit():
                ids.add(row["geni_id"])
    batch = ROOT / "reports" / "wikidata-garborg-day.qs"
    if batch.exists():
        ids |= set(re.findall(r'P2600\t"(\d+)"', batch.read_text(encoding="utf-8")))
    return ids


def main():
    known = table_tokens()
    ids = population()
    print(f"{len(known)} tokens in the table; {len(ids)} people in the ledger + batch")
    if not ids:
        sys.exit("no people found at all -- that is a broken join, not an empty ledger")

    labels = {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                labels[row["geni_id"]] = (row.get("label_en")
                                          or row.get("label_mul") or "")
    print(f"{len(labels)} of them have a Latin label to transliterate")

    missing_for = {}
    for gid, label in labels.items():
        gaps = [t for t in re.split(r"\s+", label.strip()) if t and t not in known]
        if gaps:
            missing_for[gid] = gaps
    print(f"{len(missing_for)} of {len(labels)} are blocked from a ja/zh label "
          f"by at least one token")

    appears, last_one = collections.Counter(), collections.Counter()
    for gaps in missing_for.values():
        uniq = set(gaps)
        for t in uniq:
            appears[t] += 1
        if len(uniq) == 1:
            last_one[next(iter(uniq))] += 1

    rows = [{"token": t, "kind": kind(t), "people_blocked": appears[t],
             "people_unblocked_alone": last_one[t], "ja": "", "zh": "", "note": ""}
            for t in sorted(appears, key=lambda t: (-last_one[t], -appears[t], t))]
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    by_kind = collections.Counter(r["kind"] for r in rows)
    print(f"\n{len(rows)} distinct tokens missing, of which:")
    for k, n in by_kind.most_common():
        print(f"   {n:>4}  {k}")
    print(f"\n{sum(last_one.values())} people would be unblocked by a SINGLE token each")
    print(f"\n{'token':<22}{'blocks':>8}{'alone':>7}  kind")
    for r in rows[:18]:
        print(f"{r['token']:<22}{r['people_blocked']:>8}{r['people_unblocked_alone']:>7}  "
              f"{r['kind']}")
    print(f"\nwrote {OUT.resolve().relative_to(ROOT)} -- fill `ja` and `zh` for the rows "
          f"whose kind is `name`, and append them to {TABLE.name}")


if __name__ == "__main__":
    main()
