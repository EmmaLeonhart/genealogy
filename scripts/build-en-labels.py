"""The `en` step: an English label for every CJK-named individual, or `unknown`.

    py scripts/build-en-labels.py

**Her order, `queue.md` § LABELS:** *"makes en labels for every individual (so Japanese gets
transcribed), and then mul gets made for every individual (almost always derived from en)"* — one
step over the whole population, not a per-person loop.

**Emma, 2026-09-02, on how to finish it:** *"just finish I'm not asking for categorization lol
just list these as unknowns if they are unclear lol"*. So there is no adjudication here. A person
either has an English form this repo can stand behind, or the row says `unknown` and moves on.

## Where a romanisation is allowed to come from

**Only `reports/cjk-romanisation.csv`**, which reads Latin forms out of **Wikidata's own name
items**. Emma: *"from CJK to English do not remotely try to do any kind of programmatic
transliteration because they all suck."* Nothing here transliterates — `pykakasi` and the Unihan
pinyin are used for *aliases* and for measurement, never to manufacture an English label.

## What becomes `unknown`, and it is a roster rather than a failure

* nobody has a Latin form for the name;
* the culture walk reached no verdict — 1,274 people;
* the person is on `reports/japanese-in-zh.tsv`, where a Mandarin reading would be a wrong name.

Those rows are the deck for later work, agentic or by hand, and they shrink as cultures get
confirmed by network proximity. They are not blocked on anything.

Writes `reports/label-en.tsv`.
"""
from __future__ import annotations

import collections
import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

TAB = chr(9)
LABELS = ROOT / "reports" / "derived-labels.csv"
ROMAN = ROOT / "reports" / "cjk-romanisation.csv"
CULTURE = ROOT / "reports" / "cjk-culture.csv"
HOLD = ROOT / "reports" / "japanese-in-zh.tsv"
OUT = ROOT / "reports" / "label-en.tsv"

HAN = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]")
LATIN = re.compile(r"[A-Za-z]")


def main() -> int:
    if not LABELS.exists():
        print("no %s" % LABELS.relative_to(ROOT), file=sys.stderr)
        return 1

    romanised = {}
    if ROMAN.exists():
        with io.open(ROMAN, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get("romanised"):
                    romanised[r["geni_id"]] = r["romanised"]
    culture = {}
    if CULTURE.exists():
        with io.open(CULTURE, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                culture[r["geni_id"]] = (r.get("culture") or "").strip()
    hold = set()
    if HOLD.exists():
        with io.open(HOLD, encoding="utf-8", newline="") as fh:
            hold = {r["geni_id"] for r in csv.DictReader(fh, delimiter=TAB)}
    print("%s romanisations, %s culture verdicts, %s held"
          % (format(len(romanised), ","), format(len(culture), ","), format(len(hold), ",")))

    rows, tally = [], collections.Counter()
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            cjk = (row.get("cjk_names") or "").strip()
            if not HAN.search(cjk):
                continue
            geni = row["geni_id"]
            existing = (row.get("label_en") or "").strip()
            if existing and LATIN.search(existing):
                state, label = "already has an English label", existing
            elif geni in hold:
                state, label = "unknown: held, a Mandarin reading would be wrong", ""
            elif geni in romanised:
                state, label = "romanised from Wikidata name items", romanised[geni]
            elif not culture.get(geni):
                state, label = "unknown: the culture walk reached no verdict", ""
            else:
                state, label = "unknown: no Latin form for this name", ""
            tally[state] += 1
            rows.append([geni, row.get("qid", ""), cjk, label,
                         culture.get(geni, ""), state])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["geni_id", "qid", "cjk_names", "label_en", "culture", "state"])
        w.writerows(sorted(rows, key=lambda x: (x[5], x[0])))

    print("\nwrote %s - %s people" % (OUT.relative_to(ROOT), format(len(rows), ",")))
    for k, v in tally.most_common():
        print("   %-52s %6s" % (k, format(v, ",")))
    known = sum(v for k, v in tally.items() if not k.startswith("unknown"))
    print("\n%s have an English label, %s are unknown and rostered"
          % (format(known, ","), format(len(rows) - known, ",")))
    with_qid = sum(1 for r in rows if r[1] and r[3])
    print("%s of the labelled ones already have a Wikidata item" % format(with_qid, ","))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
