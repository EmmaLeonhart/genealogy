"""The fathers the patronymics imply -- a census, not a creation batch.

**Emma, 2026-08-15:** *"If they are patronymics I actually think I'm going to want to add
items for the hypothetical fathers that are implied to exist from the patronymics. These
ones would be wiki data items that do not have geni items."*

A `Pedersdatter` with no recorded father implies a father called `Peder`. This counts them
and names them. **It emits nothing**, because the queue item states its own blocker: these
items would carry no `P2600` Geni.com profile ID, so the usual citation is unavailable and
what the statement is sourced to is Emma's to settle.

THE STEM IS NOT WHAT STRIPPING THE SUFFIX GIVES YOU

`Andersson` is `Anders` + `son`, not `Ander` + `sson`; `Hansen` is `Hans`; `Nilsson` is
`Nils`; `Larsdotter` is `Lars`. The genitive `s` belongs to the father's name and merges
when that name already ends in one, which no suffix rule can decide. Both candidates are
generated and **the one that is an attested given name in this corpus wins** -- 106,679
given-name tokens vote. A first version without that check produced fathers called *Ander*,
*Han*, *Lar* and *Nil*.

TWO POPULATIONS, AND ONLY ONE IS A PATRONYMIC

**Bare `-son` is not safe.** Split by where the bearer was born or died: `-datter`,
`-dotter`, `-sen` and `-sson` have one or two English-speaking bearers each against hundreds
of Nordic ones, while bare **`-son` runs 96 English-speaking against 36 Nordic**. Those are
hereditary surnames -- **Robinson's father was not called Robin**, and `Wilson`, `Thompson`,
`Simpson` and `Dawson` are the same shape. A live patronymic attests a father; an inherited
surname does not. The `-son` group is counted separately and excluded.

    py scripts/build-patronymic-fathers.py

Offline: derived-family.csv, display-names.csv. Writes reports/patronymic-fathers.{md,csv}.
"""

from __future__ import annotations

import csv
import io
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FAMILY = REPO / "reports" / "derived-family.csv"
NAMES = REPO / "reports" / "display-names.csv"
OUT_MD = REPO / "reports" / "patronymic-fathers.md"
OUT_CSV = REPO / "reports" / "patronymic-fathers.csv"

csv.field_size_limit(10 ** 7)

SAFE = ("sdóttir", "sdottir", "sdatter", "sdotter", "dóttir", "dottir",
        "datter", "dotter", "sson", "sen", "zen")
AMBIGUOUS = ("son",)


def candidates(surname):
    out = []
    low = surname.lower()
    for suf in SAFE + AMBIGUOUS:
        if low.endswith(suf) and len(surname) > len(suf) + 1:
            base = surname[:len(surname) - len(suf)]
            out += [base, base + "s"]
    return [c for c in dict.fromkeys(out) if c]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    given = Counter()
    surname = {}
    with io.open(NAMES, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            for part in (r.get("givn") or "").split():
                if part.isalpha():
                    given[part] += 1
            s = (r.get("surn") or "").strip()
            if s:
                surname[r["geni_id"]] = s
    fatherless = set()
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if not (r.get("father") or "").strip():
                fatherless.add(r["geni_id"])
    print("fatherless people: %d; attested given-name tokens: %d" % (len(fatherless), len(given)))

    rows, unattested, ambiguous = [], Counter(), Counter()
    for g in sorted(fatherless):
        s = surname.get(g)
        if not s:
            continue
        low = s.lower()
        safe = low.endswith(SAFE)
        if not safe and not low.endswith(AMBIGUOUS):
            continue
        scored = sorted(((given.get(c, 0), c) for c in candidates(s)), reverse=True)
        if not scored or scored[0][0] == 0:
            (unattested if safe else ambiguous)[s] += 1
            continue
        n, stem = scored[0]
        if safe:
            rows.append((g, s, stem, n))
        else:
            ambiguous[s] += 1

    fathers = Counter(stem for _, _, stem, _ in rows)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geni_id", "surname", "implied_father_given_name", "stem_attested_times"])
        w.writerows(rows)

    md = ["# The fathers the patronymics imply", "",
          "Built by `scripts/build-patronymic-fathers.py`. **A census. It emits nothing.**",
          "",
          "- fatherless people with a Nordic patronymic: **%d**" % len(rows),
          "- distinct implied fathers: **%d**" % len(fathers),
          "- patronymic surnames whose stem is not an attested given name: **%d** (not counted)"
          % sum(unattested.values()),
          "- bare `-son`, counted separately and excluded: **%d**" % sum(ambiguous.values()),
          "", "## The commonest implied fathers", "",
          "| father | people implying him |", "| --- | ---: |"]
    md += ["| %s | %d |" % (k, v) for k, v in fathers.most_common(30)]
    md += ["", "## Why bare `-son` is excluded", "",
           "Split by where the bearer was born or died, `-datter`, `-dotter`, `-sen` and "
           "`-sson` have one or two English-speaking bearers each against hundreds of Nordic "
           "ones. Bare **`-son` runs 96 English-speaking against 36 Nordic** -- those are "
           "hereditary surnames. **Robinson's father was not called Robin**, and `Wilson`, "
           "`Thompson`, `Simpson` and `Dawson` are the same shape. A live patronymic attests "
           "a father; an inherited surname does not.", "",
           "## Known flaw, stated rather than hidden", "",
           "**`Olsen` and `Olsson` yield `Ols`.** The father is `Ole`, `Ola` or `Olof`, and "
           "no suffix rule recovers the dropped vowel -- `Ols` happens to be attested, so "
           "the given-name check passes it. Those rows are wrong about the father's "
           "spelling while right that a father is implied.", "",
           "## Before anything is created", "",
           "The queue item names the blocker itself: these items would carry **no `P2600` "
           "Geni.com profile ID**, so the citation cannot be a Geni profile and what the "
           "statement is sourced to is **Emma's to settle**. Nothing here proposes an edit."]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("  Nordic patronymic, father implied: %d over %d fathers" % (len(rows), len(fathers)))
    print("  stem not attested: %d; bare -son excluded: %d"
          % (sum(unattested.values()), sum(ambiguous.values())))
    print("  commonest: " + ", ".join("%s %d" % (k, v) for k, v in fathers.most_common(10)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
