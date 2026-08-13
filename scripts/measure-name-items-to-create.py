"""Which names would need a Wikidata item created, and which already have one.

Emma, 2026-08-12: *"I probably want you to do some analysis right now of which
names could have objects created for them that do not have those objects right
now."*

**A name is not a label.** Geni names are language-agnostic strings; this is
about the *name items* `P735` and `P734` point at, which are objects in their own
right. The question is which of our name strings already correspond to one.

The lookup is `reports/wikidata-labels.tsv` restricted to the name items our own
people's statements reference (`reports/name-items.csv`). It is therefore a
**floor**: a name Wikidata has an item for, which nobody in our store points at,
reads here as missing. That is stated rather than hidden, because it is the
difference between "needs creating" and "needs finding".

Ranked by how many people carry the name, since a name on 3,000 records is worth
creating and a name on one is probably a typo.

Writes `reports/name-items-to-create.csv` and `reports/name-items-to-create.md`.

    py scripts/measure-name-items-to-create.py
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NAMES = REPO_ROOT / "reports" / "display-names.csv"
NAME_ITEMS = REPO_ROOT / "reports" / "name-items.csv"
LABELS = REPO_ROOT / "reports" / "wikidata-labels.tsv"
OUT_CSV = REPO_ROOT / "reports" / "name-items-to-create.csv"
OUT_MD = REPO_ROOT / "reports" / "name-items-to-create.md"

csv.field_size_limit(10_000_000)

#: Strings that are not names and must never have an item proposed for them.
#: Every one of these is in the measured unresolved head of
#: `reports/name-resolution.md` — regnal ordinals, placeholders, particles.
NOT_A_NAME = {
    ".", "..", "?", "-", "_", "/", "//", "*", "nn", "n.n.", "n n", "unknown",
    "of", "de", "van", "von", "der", "den", "af", "av", "di", "da", "du", "des",
    "la", "le", "el", "the", "and", "or",
}
ORDINAL = re.compile(r"^[ivxlcdm]+$", re.I)
NUMERIC = re.compile(r"^[\d.,;:()\[\]]+$")


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(text.casefold().split())


def is_a_name(text: str) -> bool:
    folded = fold(text)
    if not folded or folded in NOT_A_NAME:
        return False
    if ORDINAL.match(folded) or NUMERIC.match(folded):
        return False
    return any(c.isalpha() for c in text)


def main() -> int:
    given_items: set[str] = set()
    family_items: set[str] = set()
    with open(NAME_ITEMS, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["as_given_name"] == "yes":
                given_items.add(row["qid"])
            if row["as_family_name"] == "yes":
                family_items.add(row["qid"])

    labels: dict[str, str] = {}
    with open(LABELS, encoding="utf-8") as handle:
        for line in handle:
            qid, _, label = line.rstrip("\n").partition("\t")
            if label:
                labels[qid] = label

    have: dict[str, dict[str, set[str]]] = {"given": defaultdict(set),
                                            "family": defaultdict(set)}
    for qid in given_items:
        if qid in labels:
            have["given"][fold(labels[qid])].add(qid)
    for qid in family_items:
        if qid in labels:
            have["family"][fold(labels[qid])].add(qid)

    counts: dict[str, Counter[str]] = {"given": Counter(), "family": Counter()}
    scripts: dict[str, dict[str, str]] = {"given": {}, "family": {}}
    with open(NAMES, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            for token in (row["givn"] or "").split():
                if is_a_name(token):
                    counts["given"][token] += 1
                    scripts["given"].setdefault(token, row["scripts"])
            surn = (row["surn"] or "").strip()
            if is_a_name(surn):
                counts["family"][surn] += 1
                scripts["family"].setdefault(surn, row["scripts"])

    rows = []
    summary: dict[str, Counter[str]] = {"given": Counter(), "family": Counter()}
    people: dict[str, Counter[str]] = {"given": Counter(), "family": Counter()}
    for kind in ("given", "family"):
        for text, count in counts[kind].items():
            qids = have[kind].get(fold(text), set())
            verdict = ("has an item" if len(qids) == 1
                       else "several items share the label" if qids
                       else "no item — could be created")
            summary[kind][verdict] += 1
            people[kind][verdict] += count
            rows.append([kind, text, count, scripts[kind].get(text, ""), verdict,
                         " | ".join(sorted(qids)[:3])])

    rows.sort(key=lambda r: (r[0], -r[2]))
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["kind", "name", "people", "scripts", "verdict", "qids"])
        writer.writerows(rows)

    L: list[str] = []
    add = L.append
    add("# Name items: which exist, which would have to be created")
    add("")
    add("Emma, 2026-08-12: *\"I probably want you to do some analysis right now of which")
    add("names could have objects created for them that do not have those objects right")
    add("now.\"*")
    add("")
    add("**A name is not a label.** This is about the *items* `P735` and `P734` point at.")
    add("")
    add("Strings that are not names are excluded before counting — regnal ordinals,")
    add("`NN`, `N.N.`, bare particles, punctuation. Every one of those was in the")
    add("measured unresolved head of `reports/name-resolution.md`, where they dragged the")
    add("resolution rate down without any real name having failed.")
    add("")
    for kind, title in (("given", "Given names"), ("family", "Surnames")):
        total = sum(summary[kind].values())
        ptotal = sum(people[kind].values())
        add(f"## {title}")
        add("")
        add("| | distinct names | share | people carrying them | share |")
        add("| --- | ---: | ---: | ---: | ---: |")
        for verdict in ("has an item", "several items share the label",
                        "no item — could be created"):
            n, p = summary[kind][verdict], people[kind][verdict]
            add(f"| {verdict} | {n:,} | {100.0*n/max(total,1):.1f}% | "
                f"{p:,} | {100.0*p/max(ptotal,1):.1f}% |")
        add(f"| **total** | **{total:,}** | | **{ptotal:,}** | |")
        add("")
        add(f"### The {title.lower()} most worth creating")
        add("")
        add("| name | people | script |")
        add("| --- | ---: | --- |")
        worst = [r for r in rows if r[0] == kind and r[4].startswith("no item")][:25]
        for r in worst:
            add(f"| {r[1]} | {r[2]:,} | {r[3]} |")
        add("")
    add("## The limit of this measure")
    add("")
    add("The lookup is built from name items **our own people already point at**. A name")
    add("Wikidata has an item for, which nobody in our store references, reads here as")
    add("*no item*. So the \"could be created\" column is an **upper bound** — some of it")
    add("is names that need finding, not creating, and telling those apart needs a")
    add("download wider than the family walk.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD} and {OUT_CSV} ({len(rows):,} rows)")
    for kind in ("given", "family"):
        total = sum(summary[kind].values())
        n = summary[kind]["no item — could be created"]
        p = people[kind]["no item — could be created"]
        print(f"  {kind:<7} {n:,} of {total:,} distinct names have no item "
              f"({100.0*n/max(total,1):.1f}%), carried by {p:,} people")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
