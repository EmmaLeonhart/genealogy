"""Every parenthesised `SURN`/`_MARNM` token, classified by Emma's four rulings.

    python scripts/census-paren-tokens.py

**Her rulings, 2026-08-26**, given case by case on raw records — `CLAUDE.md` § *A parenthesised
token in `SURN`/`_MARNM` is FOUR different things*:

| shape | example | ruling |
| --- | --- | --- |
| noble house beside a patronymic | `Turesson (Bielke)` | `P734` *family name*, parens stripped |
| particle or honorific | `(de) Worms`, `Henriques (D.)` | into the `mul` **label**, never an item |
| unknown-name marker | `(anonyma)`, `(?)` | an NN marker |
| any other name-shaped token | `Weirman (Weyerman)`, `Turesson (Bielke)` | **both** — a second `P734` *family name* with the parens stripped, **and** an `Amul` alias |

She asked to see more of the **particles** before the vocabulary is fixed: *"Show me more of
these first"* was the option offered and only `(de)` and `(D.)` have been put to her. This
census is that, and it classifies the rest by the rules she did give.

## How each shape is recognised, and which part is a guess

* **unknown marker** — an exact vocabulary. `anonyma`, `incognita`, `?` and the obvious
  siblings. Exact strings, no heuristic.
* **particle** — an exact vocabulary too, seeded from the nobiliary particles and honorifics
  that actually occur here. **This is the list she asked to see**, so it is reported rather
  than treated as settled.
* **name-shaped** — everything else. **It gets BOTH**: a `P734` *family name* item with the
  parens stripped, **and** an `Amul` alias on the person. Emma, 2026-08-26: *"they get both
  family names and the alias lol."*

## The discriminator this file used to need, and no longer does

Two of her rulings looked like they needed telling apart — `Turesson (Bielke)` a house, and
`Weirman (Weyerman)` a spelling variant — since the two shapes are identical, `X (Y)`.

**Two attempts, and the first was refuted by the census it was written for.** Bare-form
frequency said `Bielke` 311 against `Weyerman` 2 — but `Voehl` occurs 20 times and
`Loewenberg` 292, so `Vöhl (Voehl)` and `Levi (Loewenberg)` came out as family names when they
are plainly variants. Frequency measures how common a name is, not whether two strings are the
same name. The second attempt was string similarity to the neighbouring token, which did
separate every case she had ruled on — and it was a similarity heuristic, in a repo that bans
those.

**Her answer removed the question.** A token gets a family-name item *and* an alias, so nothing
has to decide which one it is. That is the same shape as § *One name item per USAGE* — a token
appearing in two roles is not an ambiguity to resolve — and as § *A second Geni ID on one
Wikidata item is NOT a conflict*.

Writes `reports/paren-tokens.tsv` — one row per distinct token, per `CLAUDE.md` § *"Analyse
this" means build a CSV of every instance* — and `reports/paren-tokens.md`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
NAMES = ROOT / "reports" / "display-names.csv"
OUT_TSV = ROOT / "reports" / "paren-tokens.tsv"
OUT_MD = ROOT / "reports" / "paren-tokens.md"

PAREN = re.compile(r"^\((.+)\)$")

#: Exact strings meaning *the name is not known*. `CLAUDE.md` § *`NN` is PRESERVED in `mul`*
#: already owns this population; these are a third route into it, alongside `Private` and `NN`.
UNKNOWN_MARKERS = {
    "?", "??", "???", "anonyma", "anonymus", "anonym", "incognita", "incognito",
    "okänd", "ukjent", "ukendt", "unknown", "n.n.", "nn", "no name", "namn okänt",
}

#: Nobiliary particles and honorifics. **This is the list Emma asked to see** before the
#: general rule is fixed; only `de` and `D.` have been put to her. Her ruling on those two:
#: *"These should be parts of the mul labels because they are integral parts of what the
#: people are called."*
PARTICLES = {
    "de", "d.", "du", "des", "del", "della", "di", "da", "das", "dos", "van", "von",
    "van der", "van den", "vander", "le", "la", "el", "af", "av", "ap", "ben", "bin",
    "ibn", "mac", "mc", "o'", "st.", "san", "santa", "sir", "dom", "don", "doña",
    "lord", "lady",
}

def main():
    paren = collections.Counter()
    bare = collections.Counter()
    fields_of = collections.defaultdict(collections.Counter)
    example = {}

    # Every unparenthesised token that has stood beside this one in the same field. Kept
    # because it is what a reader needs to judge a row by eye, no longer because anything
    # is decided by it.
    neighbours = collections.defaultdict(set)
    with open(NAMES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in ("surn", "marnm"):
                toks = (row.get(field) or "").split()
                inners = [PAREN.match(t).group(1) for t in toks if PAREN.match(t)]
                plains = [t for t in toks if not PAREN.match(t)]
                for t in plains:
                    bare[t] += 1
                for inner in inners:
                    paren[inner] += 1
                    fields_of[inner][field] += 1
                    example.setdefault(inner, row)
                    neighbours[inner].update(plains)

    if not paren:
        sys.exit("no parenthesised tokens found at all -- the join is broken, not the data. "
                 f"Check that {NAMES.name} still has `surn` and `marnm` columns.")
    print(f"{len(paren):,} distinct parenthesised tokens, {sum(paren.values()):,} occurrences")
    print(f"{sum(bare.values()):,} unparenthesised tokens, for the attestation test")

    rows = []
    for tok, n in paren.most_common():
        low = tok.casefold()
        attested = bare.get(tok, 0)
        if low in UNKNOWN_MARKERS:
            shape, ruling = "unknown marker", "NN marker; never a label, never an item"
        elif low in PARTICLES:
            shape, ruling = "particle", "into the mul LABEL; never an item"
        else:
            shape = "name"
            ruling = ("a coequal, unqualified P734 family name with the parens "
                      "stripped, AND an Amul alias carrying the bracketed form)")
        ex = example[tok]
        rows.append({
            "token": tok, "occurrences": n,
            "bare_elsewhere": attested,
            "in_surn": fields_of[tok]["surn"], "in_marnm": fields_of[tok]["marnm"],
            "shape": shape, "ruling": ruling,
            "example_geni_id": ex["geni_id"],
            "example_givn": ex.get("givn", ""), "example_surn": ex.get("surn", ""),
            "example_marnm": ex.get("marnm", ""),
        })

    with open(OUT_TSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    by_shape = collections.Counter(r["shape"] for r in rows)
    occ = collections.Counter()
    for r in rows:
        occ[r["shape"]] += r["occurrences"]

    def table(shape, limit=15):
        out = ["", f"## {shape} — {by_shape[shape]:,} tokens, {occ[shape]:,} occurrences", "",
               "| token | occurrences | bare elsewhere | example record |",
               "| --- | ---: | ---: | --- |"]
        for r in [x for x in rows if x["shape"] == shape][:limit]:
            rec = (f"`GIVN {r['example_givn'][:20]}` · `SURN {r['example_surn'][:24]}` · "
                   f"`_MARNM {r['example_marnm'][:24]}`")
            out.append(f"| `({r['token']})` | {r['occurrences']} | {r['bare_elsewhere']} | {rec} |")
        if by_shape[shape] > limit:
            out.append(f"| … and {by_shape[shape] - limit:,} more | | | |")
        return out

    lines = [
        "# Parenthesised `SURN`/`_MARNM` tokens, classified by her four rulings",
        "",
        f"{len(rows):,} distinct tokens, {sum(paren.values()):,} occurrences, over the "
        f"{sum(bare.values()):,} unparenthesised tokens that provide the attestation test.",
        "",
        "| shape | tokens | occurrences | ruling |",
        "| --- | ---: | ---: | --- |",
    ]
    for shape in ("name", "particle", "unknown marker"):
        r = next((x for x in rows if x["shape"] == shape), None)
        lines.append(f"| {shape} | {by_shape[shape]:,} | {occ[shape]:,} | "
                     f"{r['ruling'] if r else ''} |")
    lines += [
        "",
        "**The particle list is the one she asked to see.** Only `(de)` and `(D.)` were put to "
        "her; the rest of `PARTICLES` in `scripts/census-paren-tokens.py` is seeded from what "
        "occurs here and is a proposal, not a ruling.",
        "",
        "**Nothing has to tell a noble house from a spelling variant.** Emma, 2026-08-26: "
        "*\"they get both family names and the alias lol\"*. A name-shaped bracketed token "
        "becomes a second `P734` *family name* with the parens stripped **and** an `Amul` "
        "alias carrying the bracketed form as Geni shows it. Two earlier attempts at a "
        "discriminator — bare-form frequency, then string similarity — are recorded in the "
        "script; her answer removed the question rather than settling it.",
    ]
    for shape in ("name", "particle", "unknown marker"):
        lines += table(shape)

    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print()
    for shape in ("name", "particle", "unknown marker"):
        print(f"   {by_shape[shape]:>5,} tokens  {occ[shape]:>6,} occurrences  {shape}")
    print(f"\nwrote {OUT_MD.resolve().relative_to(ROOT)} and "
          f"{OUT_TSV.resolve().relative_to(ROOT)}")


if __name__ == "__main__":
    main()
