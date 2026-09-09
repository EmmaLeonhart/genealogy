"""Score "the Latin display name becomes the English label" against ground truth.

Emma, 2026-08-11: *"I don't know how bad it is to have it so that all the display
names just turn into English language labels like this or whatever... My
impression is that it's often kind of passable but not good. But it's your job to
figure it out. It's not mine. It's your job. I'm putting you on this job."*

It is scoreable rather than guessable, because 14,157 of our people carry a
Wikidata item and Wikidata already holds an English label chosen by a human. So
for those people the string the rule would produce can be compared against the
string somebody actually picked.

Reads `reports/display-names.csv`. Writes:

* `reports/display-names.md` — the finding
* `reports/display-name-vs-label.csv` — **every** scored person, one row each,
  with the verdict, so no bucket has to be taken on trust

Two measures are reported, because the rule as stated does not say which name to
use when a person has several Latin ones — and 4,167 of the scored do:

* **first** — the first Latin-script `NAME` record in the file.
* **best** — the best-matching of all the person's Latin names. This is an upper
  bound on any selection rule, not a proposal: nothing can pick better than the
  best available.

    py scripts/analyse-display-names.py
"""

from __future__ import annotations

import csv
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "reports" / "display-names.csv"
OUT_CSV = REPO_ROOT / "reports" / "display-name-vs-label.csv"
OUT_MD = REPO_ROOT / "reports" / "display-names.md"

csv.field_size_limit(10_000_000)

#: Ordered worst-to-best so `min` picks the best verdict a person can achieve.
VERDICTS = [
    "identical",
    "identical bar case/diacritics",
    "Geni is a superset",
    "Wikidata is a superset",
    "overlap, half or more",
    "overlap, under half",
    "nothing in common",
]
RANK = {v: i for i, v in enumerate(VERDICTS)}


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    for ch in ".,;:()":
        text = text.replace(ch, " ")
    return " ".join(text.casefold().split())


def tokens(text: str) -> set[str]:
    return {t for t in fold(text).split() if t}


def classify(produced: str, label: str) -> tuple[str, int]:
    """Verdict plus the token difference, signed: + Geni has more, - fewer."""
    if produced == label:
        return "identical", 0
    if fold(produced) == fold(label):
        return "identical bar case/diacritics", 0
    g, w = tokens(produced), tokens(label)
    diff = len(g) - len(w)
    if not g or not w:
        return "nothing in common", diff
    if w < g:
        return "Geni is a superset", diff
    if g < w:
        return "Wikidata is a superset", diff
    shared = g & w
    if not shared:
        return "nothing in common", diff
    if len(shared) >= min(len(g), len(w)) / 2:
        return "overlap, half or more", diff
    return "overlap, under half", diff


def main() -> int:
    by_person: dict[str, list[dict]] = defaultdict(list)
    script_counts: Counter[str] = Counter()
    total_rows = 0

    with open(SOURCE, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            total_rows += 1
            script_counts[row["scripts"]] += 1
            if row["qid"]:
                by_person[row["geni_id"]].append(row)

    print(f"{total_rows:,} NAME rows, {len(by_person):,} of them on linked people")

    first_counts: Counter[str] = Counter()
    best_counts: Counter[str] = Counter()
    examples: dict[str, list[tuple]] = defaultdict(list)
    no_latin = no_label = multi_latin = 0
    scored = 0

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "geni_id",
                "qid",
                "wikidata_en",
                "latin_name_count",
                "first_latin_name",
                "first_verdict",
                "first_token_diff",
                "best_latin_name",
                "best_verdict",
            ]
        )
        for geni_id, rows in by_person.items():
            label = rows[0]["wikidata_en"]
            if not label:
                no_label += 1
                continue
            latin = [r["display_name"] for r in rows if r["scripts"] == "Latin"]
            latin = [n for n in latin if n]
            if not latin:
                no_latin += 1
                continue
            if len(latin) > 1:
                multi_latin += 1

            first_verdict, diff = classify(latin[0], label)
            graded = sorted(
                ((classify(n, label)[0], n) for n in latin),
                key=lambda pair: RANK[pair[0]],
            )
            best_verdict, best_name = graded[0]

            first_counts[first_verdict] += 1
            best_counts[best_verdict] += 1
            scored += 1
            writer.writerow(
                [
                    geni_id,
                    rows[0]["qid"],
                    label,
                    len(latin),
                    latin[0],
                    first_verdict,
                    diff,
                    best_name,
                    best_verdict,
                ]
            )
            if len(examples[first_verdict]) < 15:
                examples[first_verdict].append((geni_id, rows[0]["qid"], latin[0], label))

    lines: list[str] = []
    add = lines.append
    add("# Display names, and whether they can be English labels")
    add("")
    add("**The question, from Emma on 2026-08-11:** *\"I don't know how bad it is to")
    add("have it so that all the display names just turn into English language labels")
    add("like this or whatever... My impression is that it's often kind of passable but")
    add("not good. But it's your job to figure it out.\"*")
    add("")
    add("**It is answerable rather than arguable.** 14,157 of our people carry a Wikidata")
    add("item, and Wikidata already holds an English label a human chose. So the string")
    add("the rule would produce can be scored against the string somebody picked.")
    add("")
    add("Built from `reports/display-names.csv` (444,874 rows, every `NAME` record in the")
    add("tree). Every scored person is in `reports/display-name-vs-label.csv` — no bucket")
    add("below has to be taken on trust.")
    add("")
    add("## The scoreable population, and what falls out of it")
    add("")
    add("| | people |")
    add("| --- | ---: |")
    add(f"| linked to a Wikidata item | {len(by_person):,} |")
    add(f"| …of which no English label on Wikidata | {no_label:,} |")
    add(f"| …of which **no Latin-script `NAME` at all** | {no_latin:,} |")
    add(f"| **scored** | **{scored:,}** |")
    add(f"| of the scored, carrying more than one Latin name | {multi_latin:,} |")
    add("")
    add(f"**{no_latin:,} people have no Latin-script name whatsoever.** Those are the")
    add("translation cases Emma named — *\"If there's only a name present in some sort of")
    add("other script, we have to do a translation\"* — and they are not a fringe: they are")
    add(f"{100.0 * no_latin / max(len(by_person), 1):.0f}% of the linked people.")
    add("")
    add("## How well the rule does")
    add("")
    add("**first** takes the first Latin `NAME` record. **best** takes the best-matching of")
    add("all the person's Latin names — an upper bound on any selection rule whatever, not")
    add("a proposal, since nothing can choose better than the best available.")
    add("")
    add("| verdict | first | | best | |")
    add("| --- | ---: | ---: | ---: | ---: |")
    for verdict in VERDICTS:
        f, b = first_counts[verdict], best_counts[verdict]
        add(
            f"| {verdict} | {f:,} | {100.0*f/max(scored,1):.1f}% "
            f"| {b:,} | {100.0*b/max(scored,1):.1f}% |"
        )
    usable_first = first_counts["identical"] + first_counts["identical bar case/diacritics"]
    usable_best = best_counts["identical"] + best_counts["identical bar case/diacritics"]
    add("")
    add(
        f"**Exactly right: {usable_first:,} of {scored:,} "
        f"({100.0*usable_first/max(scored,1):.1f}%) taking the first name, "
        f"{usable_best:,} ({100.0*usable_best/max(scored,1):.1f}%) taking the best.**"
    )
    add("")
    add("## Scripts across all 444,874 name records")
    add("")
    add("| script(s) | records |")
    add("| --- | ---: |")
    for script, n in script_counts.most_common(25):
        add(f"| {script or '(no letters)'} | {n:,} |")
    add("")
    add("## What each verdict actually looks like")
    add("")
    add("Raw, first-name measure, up to 15 each.")
    add("")
    for verdict in VERDICTS:
        if not examples[verdict]:
            continue
        add(f"### {verdict}")
        add("")
        add("| geni | item | the rule would produce | Wikidata's English label |")
        add("| --- | --- | --- | --- |")
        for geni_id, qid, produced, label in examples[verdict]:
            add(f"| `{geni_id}` | {qid} | {produced} | {label} |")
        add("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV} ({scored:,} rows)")
    print()
    print(f"scored {scored:,}; {no_latin:,} had no Latin name; {no_label:,} had no en label")
    for verdict in VERDICTS:
        print(f"  {first_counts[verdict]:6,}  {100.0*first_counts[verdict]/max(scored,1):5.1f}%   {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
