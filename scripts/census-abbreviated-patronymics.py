"""Every abbreviated patronymic in our labels, and what the full form should be.

    python scripts/census-abbreviated-patronymics.py

**Emma, 2026-08-27:** *"any abbreviations like -dtr (i.e. "Rasmusdtr." instead of "Rasmusdatter")
should be fixd since wikidata mul labels ae supposed to have the full form. This is a part of the
compliance stuff I mentioned earlier"*.

`CLAUDE.md` § *"Analyse this" means build a CSV of every instance* — so this is every instance,
one row each, before anything is emitted.

## The expansion is NOT a single rule, and the corpus says so

`-dtr` expands to Norwegian `-datter` or Swedish `-dotter`, and which one is a fact about the
person, not about the abbreviation. Measured over `reports/derived-labels.csv`: **81,530** full
`-datter` against **57,085** full `-dotter`, and the split runs the other way for individual stems —
`Olsdtr` is `Olsdatter` 6,981 to 1,058, while `Andersdtr` is `Andersdotter` 5,172 to 3,126.

So a global "always `-datter`" would be wrong several thousand times, and her own example
(`Rasmusdtr.` → `Rasmusdatter`) happens to be one of the stems where `-datter` wins 10:1.

## Evidence per person first, population second

1. **The person's own other name records.** Geni gives many people several `NAME` records, and the
   abbreviation usually appears beside a full spelling. That is this person's own evidence and it
   outranks everything.
2. **The stem's dominant form across the corpus**, only when the person offers nothing. Recorded in
   the `basis` column so a row settled this way is visibly weaker than one settled by (1).

Nothing is guessed silently: every row carries `basis` and the counts behind it.

Writes `reports/abbreviated-patronymics.csv`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

LABELS = ROOT / "reports" / "derived-labels.csv"
NAMES = ROOT / "reports" / "display-names.csv"
OUT = ROOT / "reports" / "abbreviated-patronymics.csv"

#: `Rasmusdtr`, `Rasmusdtr.` — the stem plus the abbreviation, optionally a full stop.
ABBREV = re.compile(r"\b(\w+?)(dtr)\.?", re.I)
#: `Rasmusdatter` / `Rasmusdotter`, for learning what a stem expands to.
FULL = re.compile(r"\b(\w+?)(datter|dotter)\b", re.I)


def main():
    stem_full = collections.Counter()
    with LABELS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            for field in ("label_mul", "further_latin_names", "alias_names"):
                for m in FULL.finditer(row.get(field) or ""):
                    stem_full[(m.group(1).lower(), m.group(2).lower())] += 1
    print(f"{sum(stem_full.values()):,} full -datter/-dotter tokens give the corpus its priors")

    # Every NAME record per person, so a person's own spelling can be consulted.
    own = collections.defaultdict(list)
    with NAMES.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("display_name"):
                own[row["geni_id"]].append(row["display_name"])

    rows = []
    by_basis = collections.Counter()
    with LABELS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            label = row.get("label_mul") or ""
            for m in ABBREV.finditer(label):
                stem, token = m.group(1), m.group(0)
                low = stem.lower()
                # (1) this person's own records
                mine = collections.Counter()
                for other in own.get(row["geni_id"], ()):
                    for f in FULL.finditer(other):
                        if f.group(1).lower() == low:
                            mine[f.group(2).lower()] += 1
                if mine:
                    suffix, basis = mine.most_common(1)[0][0], "own name record"
                else:
                    d, o = stem_full.get((low, "datter"), 0), stem_full.get((low, "dotter"), 0)
                    if not d and not o:
                        suffix, basis = "datter", "no evidence; her example"
                    else:
                        suffix, basis = ("datter" if d >= o else "dotter"), "corpus stem majority"
                by_basis[basis] += 1
                rows.append({
                    "geni_id": row["geni_id"], "qid": row.get("qid", ""),
                    "label": label, "token": token, "stem": stem,
                    "expansion": stem + suffix, "basis": basis,
                    "corpus_datter": stem_full.get((low, "datter"), 0),
                    "corpus_dotter": stem_full.get((low, "dotter"), 0),
                })

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT.relative_to(ROOT)} -- {len(rows):,} abbreviated tokens "
          f"over {len({r['geni_id'] for r in rows}):,} people")
    for basis, n in by_basis.most_common():
        print(f"  {basis:26} {n:,}")
    linked = sum(1 for r in rows if r["qid"])
    print(f"\n{linked:,} of them are on people who already carry a Wikidata item.")


if __name__ == "__main__":
    main()
