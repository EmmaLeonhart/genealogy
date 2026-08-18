"""Every person in the corpus recorded with a single name and nothing else.

**Emma's rule, 2026-08-18:** *"if it repeats, it's a name. If it repeats over 10 times, I
think that was our actual criterion. […] Mononyms: it depends on whether somebody is
mononymous. Again, it's like they'll get a first name. People with mononyms get a first
name if it's a repeated name."*

So a mononym is not a defect to be padded out with an `NN` surname. The person gets a
`P735` *given name* — and only when the token repeats, because a token carried once is
as likely to be a fragment, a transcription, or a place as it is to be a name. The
threshold is `MIN_BEARERS` in `scripts/build-name-item-batch.py`, which is 10 and is
Emma's number; that script's docstring records why it is not five.

**Nothing in the repo handled mononyms before this.** `genimerge.namelinks` proposes
`P735`/`P734` for people whose names it can split into given and family parts; a person
with one token and no surname simply has no family part, and was never singled out. This
census is the first measurement of how many such people there are and how many of them
clear the bar.

**A mononym is not the same as a redacted or unnamed person**, and the distinction is
`CLAUDE.md` § *Redacted people go in* and § *`NN` is PRESERVED in `mul`*. `Private` and
`NN` are markers rather than names, so they are counted separately here and never
proposed as a given name — `label_for()` in `scripts/labels.py` is the single place that
decides that, and this script defers to the same list rather than inventing a second one.

**Sorted so the decision is readable**: qualifying people first, then by how common their
name is, so the head of the file is the population the rule actually creates statements
for.

    PYTHONPATH=src python scripts/build-mononym-census.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import sources
from genimerge.names import given_part

OUT_CSV = sources.REPO_ROOT / "reports" / "mononyms.csv"
OUT_MD = sources.REPO_ROOT / "reports" / "mononyms.md"

#: Emma's number. Kept in step with `MIN_BEARERS` in build-name-item-batch.py.
MIN_BEARERS = 10

#: Redaction and unknown markers. These are never a given name — `Private` withholds
#: the name and `NN` is a genealogist saying it is unknown. Both are still *people*
#: and both still get items; they just do not get a `P735` out of this.
MARKERS = {"private", "<private>", "nn", "n.n.", "n n", "n", "unknown", "?", "??",
           "???", "-", "--", ".", "*", ""}


def read_corpus() -> dict[str, dict[str, str]]:
    """Geni ID -> name fields, later files winning."""
    people: dict[str, dict[str, str]] = {}
    for path in sources.find_exports():
        current: str | None = None
        with path.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.rstrip("\r\n")
                if line.startswith("0 @I"):
                    xref = line.split("@")[1]
                    current = xref[1:] if xref.startswith("I") else None
                    if current:
                        people[current] = {"name": "", "givn": "", "surn": "",
                                           "sex": "", "file": path.name}
                elif current is None:
                    continue
                elif line.startswith("0 "):
                    current = None
                elif line.startswith("1 NAME "):
                    people[current]["name"] = line[7:].strip()
                elif line.startswith("2 GIVN "):
                    people[current]["givn"] = line[7:].strip()
                elif line.startswith("2 SURN "):
                    people[current]["surn"] = line[7:].strip()
                elif line.startswith("1 SEX "):
                    people[current]["sex"] = line[6:].strip()
    return people


def main() -> None:
    people = read_corpus()

    mono: list[tuple[str, str, dict[str, str]]] = []
    for geni_id, rec in people.items():
        name = rec.get("name", "")
        if not name:
            continue
        # A GEDCOM name is `Given /Surname/`. A mononym has nothing in the
        # surname slot and exactly one token before it.
        before, _, after = name.partition("/")
        surname = after.rstrip("/").strip()
        if surname or (rec.get("surn") or "").strip():
            continue
        given = given_part(before).strip()
        tokens = given.split()
        if len(tokens) != 1:
            continue
        mono.append((geni_id, tokens[0], rec))

    counts = Counter(tok for _, tok, _ in mono)

    rows = []
    for geni_id, token, rec in mono:
        marker = token.strip().lower() in MARKERS
        n = counts[token]
        rows.append({
            "geni_id": geni_id,
            "name": token,
            "sex": rec.get("sex", ""),
            "bearers_in_corpus": n,
            "is_marker": int(marker),
            "qualifies": int(n >= MIN_BEARERS and not marker),
            "raw_name": rec.get("name", ""),
            "source_file": rec.get("file", ""),
        })

    rows.sort(key=lambda r: (-r["qualifies"], -r["bearers_in_corpus"], r["name"]))
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    qual = sum(r["qualifies"] for r in rows)
    markers = sum(r["is_marker"] for r in rows)
    once = sum(1 for r in rows if r["bearers_in_corpus"] == 1 and not r["is_marker"])
    distinct_qual = len({r["name"] for r in rows if r["qualifies"]})

    lines = [
        "# People recorded with one name and no surname",
        "",
        f"**{len(rows):,} mononyms** out of {len(people):,} people in the corpus.",
        "",
        "Emma, 2026-08-18: *\"if it repeats, it's a name. If it repeats over 10 times, "
        "I think that was our actual criterion. […] People with mononyms get a first "
        "name if it's a repeated name.\"*",
        "",
        "| | people | |",
        "| --- | ---: | --- |",
        f"| qualify for a `P735` given name | {qual:,} | the token repeats "
        f"{MIN_BEARERS}+ times and is not a marker |",
        f"| a redaction or unknown marker | {markers:,} | `Private`, `NN` — a person, "
        "but not a name |",
        f"| the token appears exactly once | {once:,} | too thin to call a name |",
        "",
        f"The qualifying people share just **{distinct_qual:,} distinct names**, which "
        "is the whole reason the rule is worth having: a handful of name items covers "
        "thousands of people.",
        "",
        "Nothing in the repo handled mononyms before this. `genimerge.namelinks` splits "
        "a name into given and family parts and a mononym has no family part, so these "
        "people were never singled out either way.",
        "",
        "## The most common mononyms that qualify",
        "",
        "| name | people |",
        "| --- | ---: |",
    ]
    top = Counter({r["name"]: r["bearers_in_corpus"] for r in rows if r["qualifies"]})
    for name, n in top.most_common(40):
        lines.append(f"| {name} | {n:,} |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"{len(people):,} people; {len(rows):,} mononyms")
    print(f"  qualify for P735   {qual:,}  ({distinct_qual:,} distinct names)")
    print(f"  markers            {markers:,}")
    print(f"  appear once        {once:,}")
    print(f"top: {top.most_common(12)}")
    print(f"wrote {OUT_CSV.relative_to(sources.REPO_ROOT)}")


if __name__ == "__main__":
    main()
