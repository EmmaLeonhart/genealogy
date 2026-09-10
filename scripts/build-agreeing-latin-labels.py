"""Where an item's Latin-alphabet LABELS agree with each other, that agreement is the `mul`.

    PYTHONPATH=src python scripts/build-agreeing-latin-labels.py

**The rule:** where an item has no `mul` label and several of its Latin-alphabet language labels
say the same thing, that agreed string becomes the `mul` label. Ruled *"the most important
labelling thing here"*.

## ⛔ THE SOURCE IS THE ITEM'S OWN LABELS. IT WAS GENI NAME RECORDS AND THAT WAS THE DEFECT

This script used to read `display-names.csv` and count agreeing Geni `NAME` records. Ruled
2026-09-09: *"geni names are confusing. I think we kinda agreed to not do anything with them for
better or worse."* The evidence is on the Wikidata item -- ten languages spelling a person the
same way is ten independent editors agreeing, and it needs no corpus join, no romanisation and
no relative.

**What the old source actually reached: ONE PERSON.** `reports/agreeing-latin-labels.tsv` had a
single row when this was rewritten, dated 2026-09-01, and its label was `(unknown)` -- a marker,
not a name -- with a null `qid`, so it could never have been applied to anything.

**AND NOTHING RAN IT.** Not `rebuild-everything.py`, not a workflow, not the batch builder;
nothing read its output either. `CLAUDE.md` § *Code that is WRITTEN but never CALLED is not
done*. It is a step in `rebuild-everything.py` now.

## THE POPULATION, measured over the ledger before this was written

    ledger items                              2,758
    ...with NO mul label at all               1,009
    ...of those, >=2 agreeing Latin labels      853

`Q102010` *Friedrich IV. von Oettingen* carries **ten** agreeing labels and no `mul`, which is
the case that raised this. Two items agree across **84** languages.

## WHAT COUNTS AS AGREEMENT

**Two languages are the minimum.** One label agreeing with itself is not evidence -- the same
`solo` bar the rest of the name work uses.

**Case and whitespace fold; nothing else does.** `María`, `Mária` and `Marià` are three different
names -- `CLAUDE.md` § *A diacritic makes a different name*.

**If two different Latin strings are each attested, this DECLINES.** It does not pick the more
frequent one. Picking would be the coin-flip that the uniqueness rule refuses everywhere else,
and the disagreement is recorded in the TSV so it can be looked at.

**Markers are excluded before agreement is tested**, or every unnamed person would come out
labelled `NN` or `unknown` in `mul` -- which is the opposite of what `mul` is for.

## ⛔ PURELY ADDITIVE

A `mul` is emitted **only where the item has none**. This never overwrites a label, so it cannot
touch a hand-edit and it restates `CLAUDE.md` § *The purpose is to ADD, not to correct* and
§ *Wikidata's label beats ours* rather than bending either.

Writes `reports/agreeing-latin-labels.tsv` and `reports/wikidata-agreeing-latin-labels.json`.
"""

from __future__ import annotations

import collections
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

from genimerge import wikistore  # noqa: E402

LEDGER = REPO / "reports" / "garborg-qids.tsv"
STORE = REPO / "wikidata" / "items"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
OUT_TSV = REPO / "reports" / "agreeing-latin-labels.tsv"
OUT_JSON = REPO / "reports" / "wikidata-agreeing-latin-labels.json"

#: Two languages are the minimum. One label agreeing with itself is not evidence.
MIN_LANGUAGES = 2

#: A label that is a placeholder rather than a name. Wider than the `NN` pattern on purpose:
#: `mul` is the language-neutral REAL name, so nothing that means *we do not know* may land in
#: it by this route. The NN protocol owns those people and puts the marker there deliberately.
MARKER = re.compile(
    r"^\s*(nn|n\.?\s?n\.?|\?+|\(?unknown\)?|anonymous|unnamed|no name|"
    r"private|<private>|ukjent|okänd|ukendt)\s*$", re.I)


def is_latin(text):
    """True when every letter in `text` is a Latin-script letter.

    Digits, spaces and punctuation carry no script and are ignored, but a single Han or Cyrillic
    letter disqualifies the string: this rule is explicitly about the Latin alphabet, and a mixed
    string is not one.
    """
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    return all("LATIN" in unicodedata.name(c, "") for c in letters)


def agreement(labels):
    """`(value, languages, distinct)` for one item's labels, or `None` if there is no `mul` room.

    `labels` is Wikidata's `{lang: {"value": ...}}`. Returns `None` when the item already has a
    `mul` -- this is additive and an existing label is not ours to touch.
    """
    if ((labels.get("mul") or {}).get("value") or "").strip():
        return None
    folded = collections.Counter()
    display = {}
    for lang, entry in labels.items():
        if lang == "mul":
            continue
        text = " ".join(((entry or {}).get("value") or "").split())
        if not text or not is_latin(text) or MARKER.match(text):
            continue
        key = text.casefold()
        folded[key] += 1
        display.setdefault(key, text)
    if not folded:
        return None
    best, count = folded.most_common(1)[0]
    return display[best], count, len(folded)


def main() -> int:
    qids = []
    with LEDGER.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            qid = (row.get("qid") or "").strip()
            if qid.startswith("Q"):
                qids.append(qid)
    qids = sorted(set(qids))
    print("%d ledger items" % len(qids), flush=True)

    with wikistore.StoreReader(STORE, INDEX) as reader:
        items = reader.entities(qids)
    print("%d found in the store" % len(items), flush=True)

    rows, agreed = [], {}
    no_mul = 0
    for qid in qids:
        entity = items.get(qid)
        if not entity:
            continue
        result = agreement(entity.get("labels") or {})
        if result is None:
            continue
        no_mul += 1
        value, count, distinct = result
        if count < MIN_LANGUAGES:
            rows.append({"qid": qid, "label": "", "languages": count,
                         "distinct_latin": distinct, "verdict": "one language only"})
            continue
        if distinct != 1:
            rows.append({"qid": qid, "label": "", "languages": count,
                         "distinct_latin": distinct, "verdict": "labels disagree"})
            continue
        agreed[qid] = value
        rows.append({"qid": qid, "label": value, "languages": count,
                     "distinct_latin": 1, "verdict": "agreed"})

    with OUT_TSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, delimiter="\t",
                                fieldnames=["qid", "label", "languages",
                                            "distinct_latin", "verdict"])
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: (-r["languages"], r["qid"])))

    # ⛔ `mul` ONLY. The old version wrote `en` as well, and that is a different claim: an item
    # whose `en` is absent is a gap in English, while `mul` absent on an item ten languages agree
    # about is the language-neutral label missing. `en` has its own emitters and its own sources.
    edits = []
    for qid, value in sorted(agreed.items()):
        edits.append({
            "id": "mul_label_agreed:%s" % qid,
            "type": "set_label",
            "source": "agreeing Latin labels on the item itself",
            "subject": {"qid": qid, "geni_id": None},
            "requires": [],
            "label": {"language": "mul", "value": value},
            "kind": "add",
            "derived_from": "two or more of the item's own Latin-alphabet labels, agreeing",
        })
    OUT_JSON.write_text(json.dumps(edits, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")

    disagree = sum(1 for r in rows if r["verdict"] == "labels disagree")
    solo = sum(1 for r in rows if r["verdict"] == "one language only")
    print()
    print("wrote %s and %s" % (OUT_TSV.relative_to(REPO), OUT_JSON.relative_to(REPO)))
    print("  %6d items carry no mul at all" % no_mul)
    print("  %6d gain one from agreeing Latin labels" % len(agreed))
    print("  %6d have Latin labels that disagree, so nothing is claimed" % disagree)
    print("  %6d have only one Latin label, which is not agreement" % solo)
    by = collections.Counter(r["languages"] for r in rows if r["verdict"] == "agreed")
    for n in sorted(by, reverse=True)[:6]:
        print("    %6d items agreed across %d languages" % (by[n], n))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
