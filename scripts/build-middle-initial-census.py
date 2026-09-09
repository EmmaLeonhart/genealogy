"""Every person in the corpus whose given names include a bare single letter.

**Why this exists.** Emma, 2026-08-18, on assembling person labels mechanically from
Wikidata name items: *"As far as the middle initial people, I'm not really sure what to
do with them, at least going into other languages."* That is an open question, and the
rule here is that an open question gets a census rather than a proposed rule --
`CLAUDE.md` § *"Analyse this" means build a CSV of every instance*.

The population is genuinely awkward. `John C Smith` has no middle *name*, only an
initial, and `C` has no Wikidata name item and no katakana rendering, because it is not
a name -- it is an abbreviation of one we were never told. So the mechanical translation
path that works for `John` -> the standard katakana rendering has nothing to work with
here, and the obvious outs -- drop the initial, transliterate the letter, or leave it in
Latin inside a non-Latin label -- are all decisions about how a person's name is
*presented*, which is hers to make.

**This is a superset of the `single-letter` class in `build-regnal-ordinal-census.py`.**
That script tests only `I V X L C D M`, because its question was Roman numerals; a
middle initial can be any letter, and `John Q Adams` is invisible to it. The two counts
are therefore not comparable, and this one is the real size of the population.

**Position is recorded, never interpreted.** A single letter that is the *only* given
token is not a middle initial at all -- it may be a whole name, a truncation, or noise --
so `position` and `given_tokens` are columns and the caller decides. Per `CLAUDE.md`
§ *name modelling.txt*, whether a non-first given token is a middle name also depends on
its not being a patronymic, which is why the patronymic chain length travels with each
row.

Reads `exports/` directly, later file winning, exactly as the regnal census does -- no
merge, and nothing that can go stale behind a snapshot.

    PYTHONPATH=src python scripts/build-middle-initial-census.py
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import sources
from genimerge.names import given_part, patronymic_chain

OUT_CSV = sources.REPO_ROOT / "reports" / "middle-initials.csv"
OUT_MD = sources.REPO_ROOT / "reports" / "middle-initials.md"

#: A single letter, optionally followed by a full stop. Unicode-aware on purpose:
#: a lone Cyrillic or Greek letter is the same phenomenon, and a Latin-only class
#: would silently scope the census to Latin records.
INITIAL = re.compile(r"^(\w)\.?$", re.UNICODE)

ROMAN_LETTERS = set("IVXLCDM")


def initials_in(text: str) -> list[tuple[str, int]]:
    """Every bare single-letter token in a given-name string, with its index."""
    out = []
    for i, raw in enumerate(text.split()):
        token = raw.strip(",")
        m = INITIAL.match(token)
        if m and not token.strip(".").isdigit():
            out.append((m.group(1), i))
    return out


def read_corpus() -> dict[str, dict[str, str]]:
    """Geni ID -> the person's name fields, later files winning."""
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
    rows = []
    for geni_id, rec in people.items():
        name = rec.get("name", "")
        if not name:
            continue
        # Given-name portion only: everything before the first GEDCOM slash.
        # `given_part` strips slashes, which would pull the surname in.
        given = given_part(name.split("/")[0])
        found = initials_in(given)
        if not found:
            continue
        count = len(given.split())
        chain = patronymic_chain(name)
        for letter, index in found:
            rows.append({
                "geni_id": geni_id,
                "sex": rec.get("sex", ""),
                "raw_name": name,
                "given_part": given,
                "initial": letter,
                "position": index,
                "given_tokens": count,
                "is_only_token": int(count == 1),
                "is_first": int(index == 0),
                "roman_letter": int(letter.upper() in ROMAN_LETTERS),
                "patronymic_links": len(chain),
                "surn": rec.get("surn", ""),
                "source_file": rec.get("file", ""),
            })

    if not rows:
        print("no single-letter given tokens found")
        return

    rows.sort(key=lambda r: (-r["is_only_token"], r["initial"], r["raw_name"]))
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    letters = Counter(r["initial"].upper() for r in rows)
    only = sum(r["is_only_token"] for r in rows)
    first = sum(r["is_first"] for r in rows if not r["is_only_token"])
    middle = len(rows) - only - first
    roman = sum(r["roman_letter"] for r in rows)
    holders = len({r["geni_id"] for r in rows})

    def pct(n: int) -> str:
        return f"{n / len(rows):.1%}"

    lines = [
        "# People whose given names include a bare single letter",
        "",
        f"**{len(rows):,} single-letter tokens across {holders:,} people**, out of "
        f"{len(people):,} in the corpus. One row per token, so somebody with two "
        "initials appears twice.",
        "",
        "Emma, 2026-08-18: *\"As far as the middle initial people, I'm not really "
        "sure what to do with them, at least going into other languages.\"* This is "
        "the size and shape of that population. It deliberately proposes nothing.",
        "",
        "The difficulty is that an initial is not a name. `John` has a Wikidata name "
        "item and a standard rendering in Japanese; `C` has neither, because it "
        "abbreviates a name the record never gives us. So these people cannot be "
        "labelled mechanically in a non-Latin language without a decision about what "
        "happens to the letter.",
        "",
        "| position | tokens | share |",
        "| --- | ---: | ---: |",
        f"| the only given token | {only:,} | {pct(only)} |",
        f"| first of several | {first:,} | {pct(first)} |",
        f"| after the first — the middle-initial case | {middle:,} | {pct(middle)} |",
        "",
        f"{roman:,} ({pct(roman)}) are one of `I V X L C D M`, so in isolation they "
        "are indistinguishable from a regnal ordinal; `reports/regnal-ordinals.md` "
        "counts that same overlap from the other side.",
        "",
        "## By letter",
        "",
        "| letter | tokens |",
        "| --- | ---: |",
    ]
    for letter, n in letters.most_common(30):
        lines.append(f"| `{letter}` | {n:,} |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"{len(people):,} people; {len(rows):,} single-letter tokens "
          f"on {holders:,} people")
    print(f"  only given token   {only:,}")
    print(f"  first of several   {first:,}")
    print(f"  middle initial     {middle:,}")
    print(f"  roman-ambiguous    {roman:,}")
    print(f"top letters: {letters.most_common(12)}")
    print(f"wrote {OUT_CSV.relative_to(sources.REPO_ROOT)}")


if __name__ == "__main__":
    main()
