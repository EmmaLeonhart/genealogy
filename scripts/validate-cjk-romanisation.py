"""Check the romanisations against Wikidata's own English labels.

**An external check, which the pipeline did not have.** Everything in
`build-cjk-romanisation.py` is validated against itself: the readings come from Wikidata
name items and the spot-probe compares characters whose Mandarin reading is not in dispute,
which is a list I wrote. That cannot catch a systematic error I share with my own probe.

**3,188 of the romanised people are linked to a Wikidata item, and 3,139 of those items
already carry an English label written by somebody else.** Comparing the two is a real
test, and it is free.

WHAT AGREEMENT MEANS HERE, AND WHAT IT DOES NOT

The two are not the same string and are not meant to be. Wikidata writes a whole name,
surname first and the given name run together -- `Sun Changqing`, `Zhang Biaochen`. This
pipeline romanises the **given name only** and separates the syllables -- `Chang Qing`,
`Biao Chen`. So the test is whether my syllables appear in their label, not whether the
strings match.

**A disagreement is usually not an error.** Wikidata catalogues emperors under regnal and
temple names: `世民` is romanised `Shi Min` here and Wikidata calls him
`Emperor Taizong of Tang`, which is the same man under the name history uses. `履` is
`Tang of Shang`, `昌` is `King Wen of Zhou`. Those are naming conventions, not readings, so
the disagreement column has to be read rather than counted.

    py scripts/validate-cjk-romanisation.py

Offline: `reports/cjk-romanisation.csv`, `reports/derived-family.csv`, and the local store.
Writes `reports/cjk-romanisation-validation.md`. Changes nothing.
"""

from __future__ import annotations

import csv
import io
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from genimerge import wikistore  # noqa: E402

ROM = REPO / "reports" / "cjk-romanisation.csv"
FAMILY = REPO / "reports" / "derived-family.csv"
STORE = REPO / "wikidata" / "items"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
OUT = REPO / "reports" / "cjk-romanisation-validation.md"

csv.field_size_limit(10 ** 7)


def bare(s: str) -> str:
    """Letters only, lowercased -- so `Chang Qing` and `changqing` compare equal."""
    return re.sub(r"[^a-z]", "", s.lower())


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    rom = {}
    with io.open(ROM, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("romanised"):
                rom[r["geni_id"]] = r
    qid = {}
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("qid") and r["geni_id"] in rom:
                qid[r["geni_id"]] = r["qid"]
    print(f"romanised people: {len(rom):,}; linked to an item: {len(qid):,}")

    ids = sorted(set(qid.values()))
    label = {}
    with wikistore.StoreReader(STORE, INDEX) as rd:
        for i in range(0, len(ids), 5000):
            for q, e in rd.entities(ids[i:i + 5000]).items():
                L = {k: v["value"] for k, v in (e.get("labels") or {}).items()}
                if L.get("en"):
                    label[q] = L["en"]
    print(f"  of those items, already carrying an English label: {len(label):,}")

    agree, differ = 0, []
    by_culture = Counter()
    for g, q in qid.items():
        en = label.get(q)
        if not en:
            continue
        mine, theirs = bare(rom[g]["romanised"]), bare(en)
        if not mine:
            continue
        if mine in theirs:
            agree += 1
            by_culture[(rom[g]["culture"], "agree")] += 1
        else:
            differ.append((q, rom[g]["cjk"], rom[g]["romanised"], en, rom[g]["culture"]))
            by_culture[(rom[g]["culture"], "differ")] += 1
    total = agree + len(differ)
    pct = 100 * agree / max(total, 1)

    md = [
        "# The romanisations, checked against Wikidata's own English labels", "",
        "Built by `scripts/validate-cjk-romanisation.py`. **An external check** — every "
        "other measurement of this pipeline compares it against sources it already uses, "
        "or against a list of characters I wrote myself.", "",
        f"- romanised people: **{len(rom):,}**",
        f"- of those, linked to a Wikidata item: **{len(qid):,}**",
        f"- whose item already carries an English label somebody else wrote: **{len(label):,}**",
        "",
        f"## My syllables appear in their label for **{agree:,} of {total:,}** — {pct:.1f}%",
        "",
        "The two strings are not meant to match. Wikidata writes the whole name, surname "
        "first and the given name run together — `Sun Changqing`. This pipeline romanises "
        "the **given name only**, syllables separated — `Chang Qing`. The test is whether "
        "my syllables occur in their label.", "",
        "| culture | agree | differ |", "| --- | ---: | ---: |",
    ]
    for c in sorted({k[0] for k in by_culture}):
        md.append(f"| {c} | {by_culture[(c, 'agree')]:,} | {by_culture[(c, 'differ')]:,} |")
    md += ["", f"## The {len(differ):,} that differ, and why most are not errors", "",
           "Wikidata catalogues rulers under **regnal and temple names**. `世民` is "
           "`Shi Min` here and `Emperor Taizong of Tang` there — the same man under the "
           "name history uses. `履` is `Tang of Shang`; `昌` is `King Wen of Zhou`. Those "
           "are naming conventions rather than readings, so this column is for reading, "
           "not for counting.", "",
           "| qid | name | this pipeline | Wikidata | culture |",
           "| --- | --- | --- | --- | --- |"]
    for q, cjk, mine, theirs, c in differ[:120]:
        md.append(f"| `{q}` | {cjk} | {mine} | {theirs} | {c} |")
    if len(differ) > 120:
        md.append("")
        md.append(f"*{len(differ) - 120:,} further row(s) not listed.*")
    md += ["", "## What this says about writing labels", "",
           "**Wikidata's label is better than ours wherever it exists.** It carries the "
           "surname, and for a ruler it carries the name history uses. So a label batch "
           "over this population must not overwrite: for the "
           f"**{len(label):,}** people whose item already has an English label there is "
           "nothing to add, and the romanisation's value is for the ones that do not."]
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nagreement: {agree:,} of {total:,} ({pct:.1f}%)")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
