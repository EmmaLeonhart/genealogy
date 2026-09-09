"""Farm-name abbreviations, expanded only where the CORPUS attests the full form.

**Emma, 2026-09-04, on `Q141216388` *Jon Hansson St. Vatne*:** *"I think in this one St. Stands
for Store"* -- and *"St. Gives a misinpression"*, because it reads as *Saint*. She is right, and
the corpus says so rather than the reasoning: `Store Vatne` is written out **42 times**.

**A blanket rule would be badly wrong.** `St.` heads 358 labels and most of them really are
saints -- `St. Laurent`, `St. Leger`, `St. Adelaide von Bourgogne`, `St. Donats Castle`. So the
discriminator is not the abbreviation, it is whether **this** place is attested in full anywhere
in the tree: `Store Laurent` is not, so `St. Laurent` is left alone by construction.

That is `CLAUDE.md` § *An abbreviated patronymic is EXPANDED* and its refusal in the same breath:
*"A new form with no corpus evidence is SKIPPED, not defaulted"*, which is why the `dr` family
was not turned into Norwegian `datter`. Here the same rule cuts the other way and lets the
Norwegian farm names through.

**Exactly one expansion must be attested**, or the pair is skipped: `Ø.` is `Øvre` or `Østre` and
nothing in the abbreviation says which, so it is settled per place-name or not at all.

Writes `reports/farm-abbreviations.tsv`, sorted on a total key, one row per pair.
"""
from __future__ import annotations

import collections
import csv
import gzip
import os
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "reports" / "derived-labels.csv"
PACKED = ROOT / "reports" / "derived-labels.csv.gz"
OUT = ROOT / "reports" / "farm-abbreviations.tsv"

csv.field_size_limit(10_000_000)

#: The abbreviations seen in this corpus, with the full forms worth testing for. Norwegian farm
#: qualifiers: upper/lower, outer/inner, big/little, north/south. `Nd.` is included because
#: `Nedre` is its only plausible reading; it is settled by attestation like everything else.
EXPANSIONS = {
    "St": ["Store", "Stor"],
    "Ø": ["Øvre", "Østre"],
    "Yt": ["Ytre"],
    "Lt": ["Litle", "Lille"],
    "Nr": ["Nedre", "Nordre"],
    "Nd": ["Nedre"],
}
ABBREV = re.compile(r"(?:^|\s)(" + "|".join(EXPANSIONS) + r")\.\s+(\S+)")


def main() -> int:
    path = SOURCE if SOURCE.exists() else PACKED
    opener = (lambda: open(path, encoding="utf-8", newline="")) if path is SOURCE else (
        lambda: gzip.open(path, "rt", encoding="utf-8", newline=""))

    bigrams: collections.Counter = collections.Counter()
    seen: dict[tuple[str, str], int] = collections.Counter()
    with opener() as handle:
        for row in csv.DictReader(handle):
            label = row["label_mul"] or ""
            tokens = label.split()
            for i in range(len(tokens) - 1):
                bigrams[(tokens[i], tokens[i + 1])] += 1
            for m in ABBREV.finditer(label):
                seen[(m.group(1), m.group(2))] += 1

    rows = []
    for (abbrev, word), n in seen.items():
        attested = [(full, bigrams.get((full, word), 0)) for full in EXPANSIONS[abbrev]]
        hits = [a for a in attested if a[1] > 0]
        if len(hits) != 1:
            continue
        full, times = hits[0]
        rows.append({"abbreviated": f"{abbrev}. {word}", "expanded": f"{full} {word}",
                     "people": n, "attested": times})

    # Total sort key: the pair is unique, so it is its own tiebreaker.
    rows.sort(key=lambda r: (r["abbreviated"].casefold(), r["abbreviated"]))
    tmp = OUT.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["abbreviated", "expanded", "people", "attested"],
            delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(tmp, OUT)
    print(f"{len(seen):,} abbreviated pairs seen; {len(rows):,} settled by exactly one "
          f"attested expansion, covering {sum(r['people'] for r in rows):,} labels")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
