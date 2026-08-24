"""The name items the Garborg batches need and Wikidata does not have.

    python scripts/build-garborg-name-items.py

Emma, 2026-08-24: *"we should be modelling the names properly, which he didn't
do."* `P735` given name, `P734` family name and `P5056` patronym all point at
**items**, and a link cannot be written before the item exists.

**A patronymic is its own item even when the spelling already exists.**
`CLAUDE.md` § *One name item per USAGE*: `Eivindsen` has a Wikidata item as a given
name, and the patronymic `Eivindsen` is *"a different object"*. Her own `Q141152710`
*Aadnesson* is the pattern — labels, `P31` → `Q110874` *patronymic*, and nothing else.
That minimalism is copied deliberately: the measurement in `CLAUDE.md` found `P1705`,
`P282` and `P407` on most existing patronymic items and **she does not add them**.

**Ambiguous tokens are never created.** Where `reports/name-item-plan.csv` says a
token already resolves to several items — `Marie`, `Olga`, `Anton` — creating one more
is the `Maria` failure that would have made a tenth. They are listed for Emma instead.

Runs first, on its own, because QuickStatements V1 cannot point at an item a `CREATE`
in the same batch has just minted. Writes `reports/wikidata-garborg-name-items.qs`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
csv.field_size_limit(1 << 30)
sys.stdout.reconfigure(encoding="utf-8")

from namemodel import PATRONYMIC_CLASS, classify, load_plan  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

#: `CLAUDE.md` § Wikidata properties and items.
INSTANCE_OF = "P31"
FAMILY_NAME_CLASS = "Q101352"     # family name
GIVEN_NAME_CLASS = "Q202444"      # given name

CLASS_FOR = {
    "patronymic": PATRONYMIC_CLASS,
    "family": FAMILY_NAME_CLASS,
    "given": GIVEN_NAME_CLASS,
}

#: The live day batch. The earlier `wikidata-garborg.qs` and `-hop2.qs` were retired
#: on 2026-08-24: their creations are recorded in `reports/garborg-qids.tsv` and
#: re-running them would mint duplicates, which
#: `test_no_two_batches_create_the_same_person` caught.
BATCHES = ["reports/wikidata-garborg-day.qs"]


def people_in_batches():
    ids = set()
    for rel in BATCHES:
        path = ROOT / rel
        if path.exists():
            ids |= set(re.findall(r'P2600\t"(\d+)"',
                                  path.read_text(encoding="utf-8")))
    return ids


def main():
    ids = people_in_batches()
    print(f"{len(ids)} people across {len(BATCHES)} Garborg batches")

    labels = {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                labels[row["geni_id"]] = row["label_en"] or row["label_mul"]

    plan = load_plan()
    need = collections.Counter()
    ambiguous = collections.Counter()
    linked = collections.Counter()
    for label in labels.values():
        for token, usage, _ordinal in classify(label):
            qid, action = plan.get((token, usage), ("", "not in the plan"))
            if qid:
                linked[(token, usage)] += 1
            elif "AMBIG" in action.upper():
                ambiguous[(token, usage)] += 1
            else:
                need[(token, usage)] += 1

    print(f"{len(linked)} tokens already have an item and are linked, not created")
    print(f"{len(need)} need creating, {len(ambiguous)} are ambiguous and are not")

    lines = [
        "# Name items the Garborg batches need. RUN THIS FIRST -- QuickStatements",
        "# cannot point at an item a CREATE in the same batch just minted.",
        "#",
        "# A patronymic is its own item even where the spelling exists as a given",
        "# name: CLAUDE.md, one name item per USAGE. Emma's Q141152710 Aadnesson is",
        "# the pattern -- labels, P31, nothing else.",
        "",
    ]
    for (token, usage), bearers in sorted(need.items(),
                                          key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"# {token} -- {usage}, {bearers} bearer(s) in the batches")
        lines.append("CREATE")
        lines.append(f'LAST\tLen\t"{token}"')
        lines.append(f'LAST\tLmul\t"{token}"')
        lines.append(f"LAST\t{INSTANCE_OF}\t{CLASS_FOR[usage]}")
        lines.append("")

    if ambiguous:
        lines.append("# NOT created -- the plan says these already resolve to more than")
        lines.append("# one item, and creating another is the Maria failure that would")
        lines.append("# have made a tenth. Emma picks, the person's sex decides.")
        for (token, usage), bearers in sorted(ambiguous.items()):
            lines.append(f"#   {token} ({usage}), {bearers} bearer(s)")

    out = ROOT / "reports" / "wikidata-garborg-name-items.qs"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"\nwrote {out.relative_to(ROOT)}: {lines.count('CREATE')} name items")
    for (token, usage), n in sorted(need.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  create  {token:<20} {usage:<12} {n}")
    for (token, usage), n in sorted(ambiguous.items()):
        print(f"  AMBIG   {token:<20} {usage:<12} {n}")


if __name__ == "__main__":
    main()
