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

#: `Rasmusdtr`, `Rasmusdtr.`, `Ormsd`, `Johansdr`, `Olsdt.` — the stem plus the abbreviation,
#: optionally a full stop.
#:
#: **`dtr` was the only form until 2026-09-04, and it is not the only form.** Emma corrected
#: `Q141271379` by hand — *"I changed her name to correct the issue of an abbreviation of
#: Ormsdatter"* — from `Anna Ormsd Byre`. `Ormsd` matched nothing here, so nothing expanded it
#: and the batch went out with the abbreviation in the label. Widening to the genitive-preserving
#: family adds **897 occurrences over 317 distinct tokens**: `dr` 382, `d` 317, `dr.` 71, `d.` 60,
#: `dt.` 39, `dt` 28.
#:
#: **The `s` is load-bearing and is why this is safe.** A patronymic always carries the genitive,
#: so `Orms` + `d`. Allowing a bare `d` instead matched `Svend` 606, `Halvard` 322, `Hand` 92 and
#: `Old` 19 — real given names whose stem happens to be attested with `datter`. Requiring the
#: `s` removes every one of them and loses nothing.
#:
#: **The male side was measured and is NOT here.** The same shape on `sen`/`son` stems matches
#: `Foss` 762, `Ross` 498, `Strauss` 324, `Hess` 241, `Moss` 199, `Voss` 139 — surnames, not
#: abbreviations, 3,704 occurrences of them. There is no safe male pattern in this data and
#: guessing one would rewrite strangers' names.
#: **The lookahead must exclude EVERY letter, not an ASCII range.** `(?![a-zø])` let
#: `Þorbjörg Ormsdóttir` match as `Ormsd` — the Icelandic full form — and the census offered to
#: "expand" it to `Ormsdatter`, rewriting an Icelandic name into a Norwegian one. `\w` with
#: `re.UNICODE` covers `ó`, `ø`, `ä` and the rest.
ABBREV = re.compile(r"\b(\w+?)(dtr|s(?:d|dr|dt|dtt|dttr))\.?(?!\w)", re.I)

#: The forms added on 2026-09-04. They are held to a stricter standard than `dtr`: see the
#: `no evidence` guard in `main`.
NEW_FORMS = ("sd", "sdr", "sdt", "sdtt", "sdttr")
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
                # **The genitive `s` belongs to the STEM, whichever form matched.** `FULL` reads
                # `Ormsdatter` as stem `Orms`, so an `Ormsd` split as `Orm` + `sd` would look up
                # a stem the corpus has never seen and fall through to the no-evidence branch.
                # `Larsdtr` already carries its `s` in group 1; the `s…` family does not.
                if m.group(2)[:1].lower() == "s":
                    stem = stem + m.group(2)[0]
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
                        # **A NEW form with no evidence is skipped, not guessed.** The `dr`
                        # family is largely DUTCH — `Willemsdr`, `Cornelisdr`, `Jansdr`,
                        # `Bruijstensdr` — where the full form is `dochter`, and defaulting to
                        # `datter` turns a Dutch woman into a Norwegian one. 433 of the 1,314
                        # new rows landed here on the first run. `dtr` keeps the old fallback
                        # because it predates this and is Norwegian by construction.
                        if m.group(2).lower() in NEW_FORMS:
                            continue
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
