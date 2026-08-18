"""Every person in the corpus whose name carries a regnal ordinal, one row each.

**Why this exists.** `P7338` *regnal ordinal* is in `CLAUDE.md`'s property table and
`genimerge.names.given_part` deliberately keeps the ordinal attached to the given name —
*"`name modelling.txt` puts `P7338` on the given name, so splitting it off here would
lose which name it qualifies"* — but nothing in the repo ever extracted or counted one.
So the size of the population was unknown, and so were its forms.

Emma's rule is that this is not a Samaritan special case. 2026-08-15: *"they should all
have the regnal orders put on their names as qualifiers"*, and **not only the
Samaritans** — anyone whose name carries an ordering.

**Reads `exports/` directly, never the merged tree.** The question is "what does this
person's name say", which is answered by one streaming pass over the corpus and a dict
keyed on the Geni ID. `scripts/find-chain-gaps.py` established the same shape for
presence: seconds instead of a five-minute, multi-gigabyte merge, and it cannot go stale
because it reads the corpus rather than a snapshot of it.

**Later file wins**, matching `genimerge.merge`'s later-sources-win rule and
`sources.find_exports`' path ordering — a profile edited on Geni between two exports
should read as the newer export has it.

## Two false-positive classes the first run found, and how they are excluded

**`DI` — 3,076 hits, every one the Italian preposition.** `Orsello signore di
Monterotondo`, `Bertone I Grimaldi, viceré di Calabria`. `DI` is a legal Roman numeral
(501) and `di` is the commonest particle in Italian noble styling. **Case settles it**:
a regnal ordinal is written upper-case — `Karl XII`, never `Karl xii` — so the token must
equal its own upper-casing.

**`LI` — 99 hits, every one the surname.** `Aleth /Li/`, `Amund Engebretsen /Li/`. These
came in because `names.given_part` strips GEDCOM slashes before splitting, which is right
for its own job and wrong here: it pulls the *surname* into the string being searched. So
the search runs on the portion **before the first slash** only, which is the given-name
part by GEDCOM's own convention.

Both were found by looking at the rows rather than trusting the regex, which is the
reason this is a census and not a one-line match.

## The single-letter trap, measured rather than assumed

`I`, `V`, `X`, `L`, `C`, `D` and `M` are valid Roman numerals *and* the commonest
middle initials in Anglophone records. `John C Smith` is not `John the 100th`. They are
therefore reported as their own class — `single-letter` — and never merged into the
`II`/`III`/`IV` counts. Anything two characters or longer is unambiguous as a numeral.

That split is the whole reason this is a census and not a one-line regex: the decision
about what to emit needs the two populations separated, and only the data can say how
large each is.

    PYTHONPATH=src python scripts/build-regnal-ordinal-census.py
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import sources
from genimerge.names import PATRONYMIC_PARTICLES, given_part, patronymic_chain

OUT_CSV = sources.REPO_ROOT / "reports" / "regnal-ordinals.csv"
OUT_MD = sources.REPO_ROOT / "reports" / "regnal-ordinals.md"

#: Strict Roman numeral, 1..3999. Anchored, so `Ivar` and `Max` cannot match.
ROMAN = re.compile(
    r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$", re.IGNORECASE)
ROMAN_VALUE = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

#: Arabic forms that appear in regnal position — `Karl 12`, `Louis 14th`.
ARABIC = re.compile(r"^(\d{1,3})(st|nd|rd|th)?$", re.IGNORECASE)

SINGLE_LETTERS = set("IVXLCDM")


def roman_value(token: str) -> int:
    """Value of a Roman numeral. Assumes `ROMAN` already matched."""
    token = token.upper()
    total = 0
    for i, ch in enumerate(token):
        v = ROMAN_VALUE[ch]
        nxt = ROMAN_VALUE.get(token[i + 1]) if i + 1 < len(token) else None
        total += -v if nxt and nxt > v else v
    return total


def ordinal_in(text: str) -> tuple[str, int, str, int, int] | None:
    """Find a regnal ordinal in a given-name string.

    Returns `(token, value, kind, index, token_count)` or `None`. `kind` is
    `roman`, `single-letter` or `arabic` — the caller keeps them apart.

    **The ordinal is never the first token.** A name that opens with a numeral is
    not somebody's regnal number; it is a record that begins oddly, and treating
    it as an ordinal would invent an ordering that the name does not carry.
    """
    tokens = text.split()
    for i, raw in enumerate(tokens):
        if i == 0:
            continue
        token = raw.strip(".,")
        if not token:
            continue
        if ARABIC.match(token):
            return token, int(ARABIC.match(token).group(1)), "arabic", i, len(tokens)
        # Case is what separates the numeral `DI` (501) from the Italian `di`.
        if token != token.upper():
            continue
        if ROMAN.match(token):
            kind = "single-letter" if len(token) == 1 and token.upper() in SINGLE_LETTERS else "roman"
            return token, roman_value(token), kind, i, len(tokens)
    return None


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
                        people.setdefault(current, {})
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
        # `given_part` stops at the first patronymic particle, so `Abisha III ben
        # Phinhas` yields `Abisha III` and the chain is not searched for numerals.
        # Search the given-name portion only: everything before the first GEDCOM
        # slash. `given_part` strips slashes, which pulls surnames like `/Li/` in.
        given = given_part(name.split("/")[0])
        hit = ordinal_in(given)
        if not hit:
            continue
        token, value, kind, index, count = hit
        chain = patronymic_chain(name)
        rows.append({
            "geni_id": geni_id,
            "sex": rec.get("sex", ""),
            "raw_name": name,
            "givn": rec.get("givn", ""),
            "surn": rec.get("surn", ""),
            "given_part": given,
            "ordinal_token": token,
            "ordinal_value": value,
            "kind": kind,
            "token_index": index,
            "given_tokens": count,
            "patronymic_links": len(chain),
            "source_file": rec.get("file", ""),
        })

    rows.sort(key=lambda r: (r["kind"], -r["ordinal_value"], r["raw_name"]))
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else
                                ["geni_id", "sex", "raw_name", "givn", "surn",
                                 "given_part", "ordinal_token", "ordinal_value",
                                 "kind", "token_index", "given_tokens",
                                 "patronymic_links", "source_file"])
        writer.writeheader()
        writer.writerows(rows)

    kinds = Counter(r["kind"] for r in rows)
    tokens = Counter(r["ordinal_token"].upper() for r in rows if r["kind"] == "roman")
    with_chain = sum(1 for r in rows if r["patronymic_links"])
    print(f"{len(people):,} people in the corpus")
    print(f"{len(rows):,} carry an ordinal in the given part")
    for kind, n in kinds.most_common():
        print(f"  {kind:<14} {n:,}")
    print(f"  of which with a patronymic chain: {with_chain:,}")
    print(f"top roman tokens: {tokens.most_common(12)}")
    print(f"wrote {OUT_CSV.relative_to(sources.REPO_ROOT)}")


if __name__ == "__main__":
    main()
