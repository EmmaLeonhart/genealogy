"""A CJK person's `mul` label is their name in Han characters. No romanisation required.

    PYTHONPATH=src python scripts/build-cjk-mul-labels.py

**23,614 people carry a culture and no romanisation**, and 19,228 of those have a multi-character
name. They were being held back from a label because the reading table cannot romanise them --
`build-cjk-romanisation.py` measured why on 2026-08-19 and refuses: a kanji `ja` label does not
prove an item is Japanese, and where it is, `都築` has 23 attested readings and picking one is a
different person's name.

**None of that is a reason to leave `mul` empty.** `mul` is the language-neutral label, and for a
person recorded in Han characters that IS the Han string -- `CLAUDE.md` § *A title inside a label
takes the NATIVE form in CJK, never a transliteration* is the same principle one level down. The
romanisation is what `en` needs. Withholding the real name because we cannot spell it in Latin
gets the dependency backwards.

## ⛔ PURELY ADDITIVE, AND THE ITEM'S OWN LABEL WINS

A `mul` is emitted **only where the item has none**. `CLAUDE.md` § *Wikidata's label beats ours*
and § *The purpose is to ADD, not to correct*.

## THE POPULATION IS SMALL, AND THAT IS THE FINDING

Of the 23,614, only **2,003 carry a QID at all**. The other 21,611 have no Wikidata item, so
there is nothing to label and this cannot reach them -- they are a CREATION question, which is
capped, gated and not this file's business.

Writes `reports/wikidata-cjk-mul-labels.txt` and `reports/cjk-mul-labels.tsv`.
"""

from __future__ import annotations

import csv
import gzip
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

from genimerge import wikistore  # noqa: E402

CULTURE = REPO / "reports" / "cjk-culture.csv"
ROMANISED = REPO / "reports" / "cjk-romanisation.csv"
LABELS = REPO / "reports" / "derived-labels.csv"
STORE = REPO / "wikidata" / "items"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
OUT_QS = REPO / "reports" / "wikidata-cjk-mul-labels.txt"
OUT_TSV = REPO / "reports" / "cjk-mul-labels.tsv"

#: The reading language a culture code labels in, so the CJK string lands in its own language as
#: well as in `mul`. `CLAUDE.md` § *The gate is `ja` + `zh` + `ko`. CJK INCLUDES KOREAN*.
LANG = {"ja": "ja", "zh": "zh", "ko": "ko"}


def derived_rows():
    plain = LABELS
    if plain.exists():
        return csv.DictReader(plain.open(encoding="utf-8"))
    return csv.DictReader(io.TextIOWrapper(gzip.open(str(plain) + ".gz"), encoding="utf-8"))


def main() -> int:
    romanised = {r["geni_id"] for r in csv.DictReader(ROMANISED.open(encoding="utf-8"))}
    settled = [r for r in csv.DictReader(CULTURE.open(encoding="utf-8")) if r["culture"]]
    gap = [r for r in settled if r["geni_id"] not in romanised]
    print("%d carry a culture, %d of them unromanised" % (len(settled), len(gap)))

    qid_of = {}
    for row in derived_rows():
        if row.get("qid"):
            qid_of[row["geni_id"]] = row["qid"]

    candidates = [r for r in gap if r["geni_id"] in qid_of]
    print("%d of those carry a QID; %d have no item to label"
          % (len(candidates), len(gap) - len(candidates)))

    qids = sorted({qid_of[r["geni_id"]] for r in candidates})
    with wikistore.StoreReader(STORE, INDEX) as reader:
        items = reader.entities(qids)
    print("%d found in the store" % len(items))

    rows, lines = [], []
    already = missing = 0
    for r in sorted(candidates, key=lambda x: x["geni_id"]):
        qid = qid_of[r["geni_id"]]
        entity = items.get(qid)
        if not entity:
            missing += 1
            continue
        labels = entity.get("labels") or {}
        if ((labels.get("mul") or {}).get("value") or "").strip():
            already += 1
            continue
        name = " ".join((r["cjk"] or "").split())
        if not name or '"' in name:
            continue
        lang = LANG.get(r["culture"])
        rows.append([qid, r["geni_id"], name, r["culture"], r["evidence"]])
        lines.append('%s\tLmul\t"%s"' % (qid, name))
        # the same string in the reading language: a Japanese person's `ja` label IS their kanji
        if lang and not ((labels.get(lang) or {}).get("value") or "").strip():
            lines.append('%s\tL%s\t"%s"' % (qid, lang, name))

    OUT_TSV.write_text(
        "\n".join(["\t".join(["qid", "geni_id", "mul", "culture", "culture_evidence"])]
                  + ["\t".join(x) for x in rows]) + "\n",
        encoding="utf-8", newline="\n")
    OUT_QS.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print()
    print("%d already carry a mul and are left alone" % already)
    print("%d have a QID the local store does not hold" % missing)
    print("%d people gain a mul label -> %s" % (len(rows), OUT_TSV.name))
    print("%d statement lines -> %s" % (len(lines), OUT_QS.name))
    by = {}
    for x in rows:
        by[x[3]] = by.get(x[3], 0) + 1
    for code, n in sorted(by.items(), key=lambda kv: -kv[1]):
        print("    %s  %d" % (code, n))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
