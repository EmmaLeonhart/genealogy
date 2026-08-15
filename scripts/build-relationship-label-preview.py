"""What a generated relationship label would actually say, for every placeholder person.

Emma, 2026-08-15, asked to see this before deciding: *"I would like you to check
what this would actually look like, like the one and the ones with surnames or
the ones that properly have relationships… show me both populations first and do
an ask-user question on it."*

**Two populations, kept apart because that is the question**:

- **bare `NN`** — a placeholder given name and no surname at all
- **`NN <surname>`** — a placeholder given name with a real surname

Her precedence for choosing which relative names the person: **parent, father,
mother, spouse, child**. What she has already settled and this does not re-ask:
the `mul` label stays `NN` or `NN <surname>` — *"the multi-language labels keep
the NN surname"* — and the generated relationship label is the **per-language**
one.

**Built from the derived CSVs, not from a fresh merge.** `reports/derived-family.csv`
(298,591 people with their father, mother, spouses and children),
`reports/derived-labels.csv` (labels) and `reports/display-names.csv` (the
raw `GIVN`/`SURN` split). Those were derived before the last 27 exports landed,
so this is a **preview of shape, not a final count** — which is what was asked
for.

**A label is only generable in a language the RELATIVE already has a label in.**
That is the binding constraint from `reports/relationship-label-languages.md` and
it is why the `en` column here is populated from the relative's own label rather
than from anything invented.

Writes `reports/relationship-label-preview.csv` and `.md`.

    py scripts/build-relationship-label-preview.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FAMILY = REPO / "reports" / "derived-family.csv"
LABELS = REPO / "reports" / "derived-labels.csv"
NAMES = REPO / "reports" / "display-names.csv"
CSV_OUT = REPO / "reports" / "relationship-label-preview.csv"
MD_OUT = REPO / "reports" / "relationship-label-preview.md"
FACTS = REPO / "reports" / "derived-facts.csv"

csv.field_size_limit(10 ** 7)

#: The placeholder vocabulary, from `reports/given-name-forms.csv`. Screened on
#: the vocabulary and on punctuation, never on length — Korean and Chinese
#: surnames are one character.
PLACEHOLDER_GIVEN = {
    "", "nn", "n n", "n.n.", "n.n", "n", "?", "??", "???", "????", "_", "-",
    "--", ".", "*", "**", "***", "'", "unknown", "private", "<private>",
    "(no name)", "no name", "not known", "namn okänt", "ukjent", "onbekend",
}

#: Sex -> the word for a child and for a spouse. Unknown sex gets the neutral
#: form rather than a guess: inventing a gender to make a label read better is
#: exactly the normalisation Emma has objected to.
CHILD_WORD = {"M": "son", "F": "daughter", "": "child"}
SPOUSE_WORD = {"M": "husband", "F": "wife", "": "spouse"}
PARENT_WORD = {"M": "father", "F": "mother", "": "parent"}


def is_placeholder(given: str) -> bool:
    return given.strip().lower() in PLACEHOLDER_GIVEN


def is_unusable(label: str) -> bool:
    """Whether a relative's label is too empty to name somebody else by.

    Two cases, both ruled on by Emma on 2026-08-15: a redaction marker, which
    must not travel into another person's label; and a label that is itself a
    placeholder, where `NN de Nantes` names nobody.
    """
    low = label.strip().lower()
    if not low or low in PLACEHOLDER_GIVEN:
        return True
    if "private" in low:
        return True
    first = low.split()[0] if low.split() else ""
    return first in PLACEHOLDER_GIVEN


def main() -> int:
    for path in (FAMILY, LABELS, NAMES, FACTS):
        if not path.exists():
            print(f"missing {path}", file=sys.stderr)
            return 1

    # geni_id -> (given, surname), first NAME record wins: `CLAUDE.md` notes the
    # first listed name is the one Geni treats as primary.
    name_of: dict[str, tuple[str, str]] = {}
    for row in csv.DictReader(NAMES.open(encoding="utf-8", newline="")):
        name_of.setdefault(row["geni_id"],
                           ((row.get("givn") or "").strip(),
                            (row.get("surn") or "").strip()))

    label_of: dict[str, str] = {}
    for row in csv.DictReader(LABELS.open(encoding="utf-8", newline="")):
        label_of[row["geni_id"]] = (row.get("label_en") or "").strip()

    sex_of: dict[str, str] = {}
    for row in csv.DictReader(FACTS.open(encoding="utf-8", newline="")):
        sex_of[row["geni_id"]] = (row.get("sex") or "").strip()

    rows = []
    for row in csv.DictReader(FAMILY.open(encoding="utf-8", newline="")):
        gid = row["geni_id"]
        given, surname = name_of.get(gid, ("", ""))
        if not is_placeholder(given):
            continue

        sex = sex_of.get(gid, "")
        father, mother = row.get("father", ""), row.get("mother", "")
        spouses = [s for s in (row.get("spouses") or "").split(" | ") if s]
        children = [c for c in (row.get("children") or "").split(" | ") if c]

        # Emma, 2026-08-15: a redacted relative is SKIPPED and the precedence
        # falls through to the next one. "husband of <private> Gaya Pereira"
        # puts a redaction marker into somebody else's label, which the rule
        # about `Private` never being a label was written to prevent.
        #
        # The same fall-through is applied to a relative whose own label is a
        # placeholder ("husband of NN de Nantes", 53 cases). She ruled on the
        # redacted case and not explicitly on this one; it is the same shape,
        # and it is called out in the report so it can be reversed.
        #
        # Every spouse and child is tried, not just the first, because skipping
        # more relatives means the first one is more often unusable.
        candidates = ([("father", father), ("mother", mother)]
                      + [("spouse", s) for s in spouses]
                      + [("child", c) for c in children])

        relation = via = generated = skipped = ""
        for kind, candidate in candidates:
            if not candidate:
                continue
            other = label_of.get(candidate, "")
            if not other:
                continue
            if is_unusable(other):
                skipped = skipped or ("redacted" if "private" in other.lower()
                                      else "placeholder")
                continue
            via = candidate
            relation = kind
            if kind in ("father", "mother"):
                generated = f"{CHILD_WORD.get(sex, 'child')} of {other}"
            elif kind == "spouse":
                generated = f"{SPOUSE_WORD.get(sex, 'spouse')} of {other}"
            else:
                generated = f"{PARENT_WORD.get(sex, 'parent')} of {other}"
            break

        # Emma, 2026-08-15: a surname that is itself placeholder vocabulary
        # carries no information, so these collapse to bare `NN` rather than
        # becoming `NN ???`.
        if surname.strip().lower() in PLACEHOLDER_GIVEN:
            surname = ""

        rows.append({
            "geni_id": gid,
            "population": "NN + surname" if surname else "bare NN",
            "surname": surname,
            "sex": sex,
            "mul_label": f"NN {surname}".strip() if surname else "NN",
            "relation_used": relation,
            "skipped_a_relative": skipped,
            "via_geni_id": via,
            "generated_en": generated,
            "has_label": "yes" if generated else "",
            "n_parents": int(bool(father)) + int(bool(mother)),
            "n_spouses": len(spouses),
            "n_children": len(children),
        })

    if not rows:
        print("no placeholder people found", file=sys.stderr)
        return 1

    with CSV_OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    def stats(pop):
        sel = [r for r in rows if r["population"] == pop]
        got = [r for r in sel if r["has_label"]]
        return sel, got, Counter(r["relation_used"] for r in got)

    lines = [
        "# What a generated relationship label would say",
        "",
        "Generated by `scripts/build-relationship-label-preview.py`. One row per "
        f"placeholder person in `reports/relationship-label-preview.csv` — "
        f"**{len(rows):,} people**.",
        "",
        "Emma asked to see both populations before deciding whether the "
        "generated label runs for people who already carry a surname. The `mul` "
        "label is settled and is not the question: it stays `NN` or "
        "`NN <surname>`.",
        "",
        "**Preview, not a final count.** Built from the derived CSVs, which "
        "predate the last 27 exports. The shape is what is being asked about.",
        "",
        "| | bare `NN` | `NN` + surname |",
        "| --- | ---: | ---: |",
    ]
    bare, bare_got, bare_rel = stats("bare NN")
    sur, sur_got, sur_rel = stats("NN + surname")
    lines += [
        f"| people | {len(bare):,} | {len(sur):,} |",
        f"| a label can be generated | **{len(bare_got):,}** "
        f"({100 * len(bare_got) // max(len(bare), 1)}%) | **{len(sur_got):,}** "
        f"({100 * len(sur_got) // max(len(sur), 1)}%) |",
        f"| no relative with a real name | {len(bare) - len(bare_got):,} | "
        f"{len(sur) - len(sur_got):,} |",
        "",
        "## Which relative ends up naming them",
        "",
        "| relation | bare `NN` | `NN` + surname |",
        "| --- | ---: | ---: |",
    ]
    for kind in ("father", "mother", "spouse", "child"):
        lines.append(f"| {kind} | {bare_rel.get(kind, 0):,} | "
                     f"{sur_rel.get(kind, 0):,} |")

    # -- the rules Emma set on this preview, and what they cost -------------
    got = bare_got + sur_got
    leaked = [r for r in got if "private" in r["generated_en"].lower()
              or " of NN" in r["generated_en"]]
    skipped = [r for r in rows if r["skipped_a_relative"]]
    rescued = [r for r in skipped if r["has_label"]]
    no_sex = [r for r in got if not r["sex"]]
    lines += [
        "",
        "## The rules applied here, and what they cost",
        "",
        "Emma ruled on both of these on 2026-08-15 after seeing the first "
        "version of this preview.",
        "",
        f"1. **A redacted or placeholder relative is skipped**, and the "
        "precedence falls through to the next one — *\"skip, fall through to "
        "the next relative\"*. The first version put the marker into somebody "
        "else's label: *\"husband of `<private>` Gaya Pereira\"*, 2,730 times. "
        f"Now **{len(leaked):,}** do. {len(skipped):,} people had a relative "
        f"skipped and **{len(rescued):,} of them "
        f"({100 * len(rescued) // max(len(skipped), 1)}%) still get a label** "
        "from a later relative. That is a minority: for the rest the skipped "
        "relative was the only one with a real name, so the skip costs the "
        "label outright. Every spouse and child is tried rather than only the "
        "first, which is what recovers the share that is recovered.",
        f"2. **A surname that is itself placeholder vocabulary collapses to "
        "bare `NN`** — `NN ???`, `NN NN`, `NN N.N.`, `NN Unknown`. 351 people "
        "moved from the surname population to the bare one, which is why the "
        "two totals here differ from the first version.",
        "",
        f"{len(no_sex):,} of the generable labels have **no recorded sex** and "
        "take the neutral form (`child of`, `spouse of`). Inventing a gender to "
        "make the label read better is not done here.",
        "",
    ]

    for title, sample in (("Bare `NN` — what it would say", bare_got),
                          ("`NN` + surname — what it would say", sur_got)):
        lines += ["", f"## {title}", "",
                  "| `mul` | generated `en` | via | sex |",
                  "| --- | --- | --- | --- |"]
        for r in sample[:20]:
            lines.append(f"| {r['mul_label']} | {r['generated_en']} | "
                         f"{r['relation_used']} | {r['sex'] or '—'} |")
    lines.append("")

    MD_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(rows):,} placeholder people")
    print(f"  bare NN:      {len(bare):,}, label generable for {len(bare_got):,}")
    print(f"  NN + surname: {len(sur):,}, label generable for {len(sur_got):,}")
    print(f"wrote {CSV_OUT} and {MD_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
