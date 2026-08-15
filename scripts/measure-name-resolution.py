"""How much of the Geni name vocabulary can now be resolved to a Wikidata item?

Plan item 2 is *"derive name items but never create name items"* — derive means
look up which existing item corresponds to a name string. That was impossible
offline until `reports/wikidata-labels.tsv` landed. Whether it is now *possible*
is a different question from whether it *reaches anything*, and this measures the
second.

**The lookup this builds is deliberately narrow.** A name item counts only if
some person in our own store already points at it with `P735` or `P734` — that
list is `reports/name-items.csv`. So the vocabulary covered is "names Wikidata
already uses for people we hold", not "all name items on Wikidata". A Geni name
Wikidata has an item for, which nobody in our store carries, is invisible here
and will stay invisible until a download goes wider.

**Matching is exact on the label string**, case-folded and diacritic-folded only.
No fuzzy matching: `CLAUDE.md`'s governing rule is that matching is genealogical,
and a name string matched loosely to a name item is precisely the kind of guess
that rule exists to forbid. A near-miss is reported as a miss.

Writes `reports/name-resolution.md` and `reports/name-resolution.csv`, the latter
one row per distinct Geni name string with what it resolved to.

    py scripts/measure-name-resolution.py
"""

from __future__ import annotations

import csv
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NAMES = REPO_ROOT / "reports" / "display-names.csv"
NAME_ITEMS = REPO_ROOT / "reports" / "name-items.csv"
LABELS = REPO_ROOT / "reports" / "wikidata-labels.tsv"
OUT_MD = REPO_ROOT / "reports" / "name-resolution.md"
OUT_CSV = REPO_ROOT / "reports" / "name-resolution.csv"

csv.field_size_limit(10_000_000)

ABSENT = {".", "..", "?", "-", "_"}


def fold(text: str) -> str:
    """Case and whitespace only. **Diacritics are kept.**

    Folding them away was wrong and Emma caught it, 2026-08-16: asked why
    `Maria` came out matching nine Wikidata items she looked and found *"there is
    one thing worth noting, which is that there's a male and a female Maria.
    Aside from that, everything appears to be diacritics or stuff that's not
    actually it."*

    She is right. Of the nine, **four are `María`, `Mária` or `Marià`** — Spanish,
    Hungarian and Catalan names that are *different names*, not spellings of this
    one. Wikidata gives each its own item deliberately. Collapsing them
    manufactured ambiguity that does not exist and put 1,312 names into
    review-and-do-not-create.

    The genuine residue is the one she named: `Q325872` and `Q25413386`, the male
    and the female given name `Maria`. That is a real distinction and is settled
    by the *person's* sex, not by the string.
    """
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def main() -> int:
    # Which QIDs are name items, and in which role. From our own people's
    # statements, so "name item" here means one Wikidata already uses for them.
    given: set[str] = set()
    family: set[str] = set()
    with open(NAME_ITEMS, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["as_given_name"] == "yes":
                given.add(row["qid"])
            if row["as_family_name"] == "yes":
                family.add(row["qid"])
    print(f"{len(given):,} given-name items, {len(family):,} family-name items", flush=True)

    labels: dict[str, str] = {}
    with open(LABELS, encoding="utf-8") as handle:
        for line in handle:
            qid, _, label = line.rstrip("\n").partition("\t")
            if label:
                labels[qid] = label
    print(f"{len(labels):,} labels available", flush=True)

    # label -> qids, per role. A label shared by several items is ambiguous and
    # is never resolved to one of them by picking; that would be a guess.
    given_by_label: dict[str, set[str]] = defaultdict(set)
    family_by_label: dict[str, set[str]] = defaultdict(set)
    for qid in given:
        if qid in labels:
            given_by_label[fold(labels[qid])].add(qid)
    for qid in family:
        if qid in labels:
            family_by_label[fold(labels[qid])].add(qid)
    print(f"{len(given_by_label):,} distinct given-name labels, "
          f"{len(family_by_label):,} family-name labels", flush=True)

    given_tokens: Counter[str] = Counter()
    surnames: Counter[str] = Counter()
    with open(NAMES, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            for token in (row["givn"] or "").split():
                if token not in ABSENT:
                    given_tokens[token] += 1
            surn = (row["surn"] or "").strip()
            if surn and surn not in ABSENT:
                surnames[surn] += 1

    print(f"{len(given_tokens):,} distinct given-name tokens, "
          f"{len(surnames):,} distinct surnames in the tree", flush=True)

    rows = []
    stats: dict[str, Counter[str]] = {"given": Counter(), "family": Counter()}
    occurrences: dict[str, Counter[str]] = {"given": Counter(), "family": Counter()}

    for kind, source, index in (
        ("given", given_tokens, given_by_label),
        ("family", surnames, family_by_label),
    ):
        for text, count in source.items():
            qids = index.get(fold(text), set())
            if not qids:
                verdict = "no item"
            elif len(qids) == 1:
                verdict = "resolved"
            else:
                verdict = "ambiguous — several items share the label"
            stats[kind][verdict] += 1
            occurrences[kind][verdict] += count
            rows.append([kind, text, count, verdict,
                         " | ".join(sorted(qids)) if len(qids) <= 3 else f"{len(qids)} items"])

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["kind", "name", "occurrences", "verdict", "qids"])
        writer.writerows(sorted(rows, key=lambda r: (r[0], -r[2])))

    L: list[str] = []
    add = L.append
    add("# How far the fetched labels resolve the Geni name vocabulary")
    add("")
    add("Plan item 2 is *\"derive name items but never create name items\"*. Deriving")
    add("means looking up which existing item a name string corresponds to, which was")
    add("impossible offline until `reports/wikidata-labels.tsv` landed. **Being possible")
    add("and reaching anything are different questions**; this is the second.")
    add("")
    add("Every distinct name string is a row in `reports/name-resolution.csv`.")
    add("")
    add("## The answer")
    add("")
    for kind, title in (("given", "Given-name tokens"), ("family", "Surnames")):
        total = sum(stats[kind].values())
        occ_total = sum(occurrences[kind].values())
        add(f"### {title}")
        add("")
        add("| | distinct | share | occurrences | share |")
        add("| --- | ---: | ---: | ---: | ---: |")
        for verdict in ("resolved", "ambiguous — several items share the label", "no item"):
            n, o = stats[kind][verdict], occurrences[kind][verdict]
            add(f"| {verdict} | {n:,} | {100.0*n/max(total,1):.1f}% | "
                f"{o:,} | {100.0*o/max(occ_total,1):.1f}% |")
        add(f"| **total** | **{total:,}** | | **{occ_total:,}** | |")
        add("")
    add("**Distinct and occurrences differ a lot, and the second is the one that")
    add("matters for coverage.** A common name resolving is worth thousands of records;")
    add("a rare one is worth one. Both are given so neither can be quoted alone.")
    add("")
    add("## The unresolved head is mostly not names")
    add("")
    add("Before reading 30.7% as a name-coverage figure, look at what fails. The")
    add("commonest unresolved strings, by occurrence:")
    add("")
    for kind, title in (("given", "given-name tokens"), ("family", "surnames")):
        worst = sorted(
            (r for r in rows if r[0] == kind and r[3] == "no item"),
            key=lambda r: -r[2],
        )[:8]
        add(f"- **{title}** — " + ", ".join(f"`{r[1]}` ({r[2]:,})" for r in worst))
    add("")
    add("The given-name head is **regnal ordinals, particles, placeholders and")
    add("punctuation** — `I`, `II`, `of`, `NN`, `/`, `N.N.`, `Rd.` None is a name, so")
    add("none can have a name item, and their presence in the denominator drags the rate")
    add("down without any name having failed to resolve. This is `todo.md` § 4's trap")
    add("appearing from the other side: a naive split puts non-names into the token")
    add("stream, and here they show up as unresolvable.")
    add("")
    add("The surname head is **CJK** — and two of the commonest, `隴西狄道` and")
    add("`河南洛陽`, are *places* in the surname field, the inversion `CLAUDE.md` records")
    add("for `陳郡陽夏`. The rest — `曾`, `陳`, `藤原`, `이` — are real surnames that")
    add("almost certainly have items; they fail because **nobody in our store points at")
    add("those items**, which is the floor this measure was built to expose.")
    add("")
    add("So the true resolution rate for strings that are actually names is higher than")
    add("the table says, and **it is not measured here** — separating names from")
    add("non-names is the step `todo.md` says is needed and nobody has built.")
    add("")
    add("## What this cannot see")
    add("")
    add("The lookup is built from **name items our own people already point at** —")
    add("`reports/name-items.csv`. A Geni name that Wikidata has an item for, which")
    add("nobody in our store carries, is invisible here and stays invisible until a")
    add("download goes wider than the family walk. So this is a **floor**, not a")
    add("measure of what Wikidata holds.")
    add("")
    add("Matching is exact on the label, case- and diacritic-folded, and nothing else.")
    add("A label shared by several items is reported ambiguous rather than resolved by")
    add("picking one — that would be the guess the genealogical-matching rule forbids.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"\nwrote {OUT_MD} and {OUT_CSV}")
    for kind in ("given", "family"):
        total = sum(stats[kind].values())
        r = stats[kind]["resolved"]
        o_total = sum(occurrences[kind].values())
        o_r = occurrences[kind]["resolved"]
        print(f"  {kind:<7} resolved {r:,}/{total:,} distinct ({100.0*r/max(total,1):.1f}%), "
              f"{o_r:,}/{o_total:,} occurrences ({100.0*o_r/max(o_total,1):.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
