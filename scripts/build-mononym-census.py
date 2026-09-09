"""Every person in the corpus Geni records as having no surname at all.

**Emma's definition, 2026-08-18: mononyms are `Name /./`.** Geni writes an explicit
full stop in the GEDCOM surname slot to mean *this person has no surname*, which is a
positive statement and not the same as an empty slot. **10,695** NAME lines carry it.

**The first version of this script missed every one of them.** It treated the surname
slot as a string and skipped anyone whose slot was non-empty, so `Anna /./` — the exact
shape being looked for — was discarded as "has a surname `.`", and what got measured
instead was the empty-slot population. Both are reported below now, apart, because they
are different statements: `/./` is Geni saying there is no surname, and `//` is Geni
saying nothing.

**Emma's rule for what they get, same day:** *"if it repeats, it's a name. If it repeats
over 10 times, I think that was our actual criterion. […] People with mononyms get a
first name if it's a repeated name."* So a mononym is not a defect to pad out with an
`NN` surname — the person gets a `P735` *given name*, and only when the token repeats,
because a token carried once is as likely to be a fragment or a place as a name. The
threshold matches `MIN_BEARERS` in `scripts/build-name-item-batch.py`.

**The marker vocabulary is imported, never redefined.** The first version carried its own
English-only set and so ranked `Ukjent` (Norwegian) and `未知` (Chinese) — both meaning
*unknown* — among Anna, Anders and Lars as though they were names. `scripts/labels.py`
already held `ukjent`, which is Emma's *"I thought that was in the logic"*; `未知` was
genuinely missing and has been added there. That module is the single place that decides
what a marker is, per `CLAUDE.md`, and the whole failure came from having a second copy.

Those people are not dropped. Emma: *"Ukjent and 未知 get the mul NN treatment"* — the
shape in `CLAUDE.md` § *`NN` is PRESERVED in `mul`*, where `NN` stays in `mul` and
descriptive labels are added in other languages. They are counted here as markers so they
do not become a `P735` given name; what they *do* get is that treatment, elsewhere.

    PYTHONPATH=src python scripts/build-mononym-census.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from genimerge import sources
from genimerge.names import given_part
from labels import (NARROW_MARKERS, PUNCTUATION_MARKERS, SINGLE_LETTER_MARKERS,
                    WORDS_MEANING_UNKNOWN)

OUT_CSV = sources.REPO_ROOT / "reports" / "mononyms.csv"
OUT_MD = sources.REPO_ROOT / "reports" / "mononyms.md"

#: Emma's number, kept in step with `MIN_BEARERS` in build-name-item-batch.py.
MIN_BEARERS = 10

#: Everything `scripts/labels.py` calls a marker. One vocabulary, imported.
MARKERS = (NARROW_MARKERS | WORDS_MEANING_UNKNOWN | PUNCTUATION_MARKERS
           | SINGLE_LETTER_MARKERS)


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
                        people[current] = {"name": "", "surn": "", "sex": "",
                                           "file": path.name}
                elif current is None:
                    continue
                elif line.startswith("0 "):
                    current = None
                elif line.startswith("1 NAME "):
                    people[current]["name"] = line[7:].strip()
                elif line.startswith("2 SURN "):
                    people[current]["surn"] = line[7:].strip()
                elif line.startswith("1 SEX "):
                    people[current]["sex"] = line[6:].strip()
    return people


def surname_slot(gedcom_name: str) -> str:
    """What sits between the GEDCOM slashes, verbatim."""
    _, sep, rest = gedcom_name.partition("/")
    if not sep:
        return ""
    return rest.partition("/")[0].strip()


def main() -> None:
    people = read_corpus()

    rows_in: list[tuple[str, str, str, dict[str, str]]] = []
    empty_slot = 0
    for geni_id, rec in people.items():
        name = rec.get("name", "")
        if not name:
            continue
        slot = surname_slot(name)
        if slot and slot != ".":
            continue
        form = "dot" if slot == "." else "empty"
        if form == "empty" and (rec.get("surn") or "").strip():
            continue
        if form == "empty":
            empty_slot += 1
        given = given_part(name.partition("/")[0]).strip()
        if not given:
            continue
        rows_in.append((geni_id, given, form, rec))

    # Bearers are counted over the whole given string, which is what a label is
    # built from. A multi-token given name is still a mononym in Geni's sense --
    # `#1 Dewi Saroh (Sarah) /./` has no surname -- so it is not filtered out.
    counts = Counter(g for _, g, _, _ in rows_in)

    rows = []
    for geni_id, given, form, rec in rows_in:
        low = given.strip().lower()
        marker = low in MARKERS
        n = counts[given]
        rows.append({
            "geni_id": geni_id,
            "name": given,
            "surname_slot": form,
            "sex": rec.get("sex", ""),
            "tokens": len(given.split()),
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

    dot = sum(1 for r in rows if r["surname_slot"] == "dot")
    qual = sum(r["qualifies"] for r in rows)
    qual_dot = sum(r["qualifies"] for r in rows if r["surname_slot"] == "dot")
    markers = sum(r["is_marker"] for r in rows)
    once = sum(1 for r in rows if r["bearers_in_corpus"] == 1 and not r["is_marker"])
    distinct_qual = len({r["name"] for r in rows if r["qualifies"]})
    one_token = sum(1 for r in rows if r["tokens"] == 1)

    lines = [
        "# People Geni records as having no surname",
        "",
        "Emma, 2026-08-18: **\"Mononyms are `Name /./`\"** — Geni writes an explicit "
        "full stop in the GEDCOM surname slot to say *this person has no surname*. "
        "That is a positive statement, and different from an empty slot, which says "
        "nothing. Both are counted here and kept apart.",
        "",
        "| surname slot | people |",
        "| --- | ---: |",
        f"| `/./` — Geni says there is no surname | {dot:,} |",
        f"| `//` — the slot is simply empty | {len(rows) - dot:,} |",
        f"| **total** | **{len(rows):,}** |",
        "",
        "The first version of this script measured only the second row, because it "
        "read a `.` as a surname and skipped exactly the people it was looking for.",
        "",
        "## What they get",
        "",
        "Emma, same day: *\"if it repeats, it's a name. If it repeats over 10 times, "
        "I think that was our actual criterion. […] People with mononyms get a first "
        "name if it's a repeated name.\"*",
        "",
        "| | people |",
        "| --- | ---: |",
        f"| qualify for a `P735` given name | {qual:,} |",
        f"| …of those, in the `/./` form | {qual_dot:,} |",
        f"| a marker rather than a name | {markers:,} |",
        f"| the name appears exactly once | {once:,} |",
        "",
        f"The qualifying people share **{distinct_qual:,} distinct names**, which is why "
        "the rule is worth having: a few name items cover thousands of people. "
        f"{one_token:,} of all these people have a single given token; the rest have "
        "several and still no surname, which is ordinary in the Indonesian and Javanese "
        "records this form is common in.",
        "",
        "**The marker vocabulary is imported from `scripts/labels.py`, not redefined.** "
        "The first version carried its own English-only list and ranked `Ukjent` "
        "(Norwegian) and `未知` (Chinese) among Anna, Anders and Lars as if they were "
        "names. `ukjent` was already in `labels.py` — Emma: *\"I thought that was in "
        "the logic\"* — and `未知` was the real gap, now added there at 204 occurrences. "
        "Those people are not discarded: *\"Ukjent and 未知 get the mul NN treatment\"*, "
        "so they keep `NN` in `mul` and gain descriptive labels in other languages. "
        "They are excluded here only from becoming a given name.",
        "",
        "## The most common qualifying names",
        "",
        "| name | people |",
        "| --- | ---: |",
    ]
    top = Counter({r["name"]: r["bearers_in_corpus"] for r in rows if r["qualifies"]})
    for name, n in top.most_common(40):
        lines.append(f"| {name} | {n:,} |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"{len(people):,} people; {len(rows):,} with no surname "
          f"({dot:,} written /./, {len(rows)-dot:,} empty slot)")
    print(f"  qualify for P735   {qual:,}  ({distinct_qual:,} distinct names)")
    print(f"  markers            {markers:,}")
    print(f"  appear once        {once:,}")
    print(f"top: {top.most_common(12)}")
    print(f"wrote {OUT_CSV.relative_to(sources.REPO_ROOT)}")


if __name__ == "__main__":
    main()
