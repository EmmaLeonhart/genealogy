"""What is actually *in* the profiles — the evidence the enrichment pipeline needs.

Items 4 and 6 of `todo.md` turn profiles into Wikidata statements: a new item
carries a label, sex, dates and the link structure; an existing item gets the
Geni ID, name links and any missing claims backfilled. Both are bounded by one
question this module answers and nothing else did — **for each field a statement
could carry, on what share of people is it actually present?** A pipeline
scoped around a field only a tenth of the tree has will mostly emit nothing.

Two measurements, because two different things gate the pipeline.

**Field fill rates.** Per *person* (not per NAME record), does the canonical
tree hold a given name, a surname, sex, a birth date, and so on. Counting people
is the right denominator: the question is how many people a batch could touch,
and someone with three NAME lines all saying "Borsheim" is one person who would
gain one link.

**Name scripts.** The tree is not one language. A Japanese or Chinese profile is
the hard case for reconciling against Wikidata, and the fear was that those
people might be stored romanized-only, with the native name lost. They are not:
they are overwhelmingly stored in native script, and it is the *romanization*
that is often missing. This module measures that directly by classifying every
name form by Unicode block, so "how many CJK people have no Latin form" is a
number rather than a guess.

**It proposes nothing and creates nothing** — like `names`, it is evidence for a
decision, not the decision.

Three things this module deliberately does not do, recorded because each is a
trap the pipeline that consumes this must handle rather than one this report
resolves:

- **It does not split ``GIVN`` into given-name tokens.** A multi-token given
  string is the P1545 (series ordinal) case in European names — "Jean Paul" is
  two given-name items in order — but most multi-token strings here are
  romanized CJK/steppe names where the extra tokens are honorifics, particles
  and titles ("Lady", "no", "Chanyu"), not names. The count of multi-token
  people is reported; the *splitting* is left to a step that can tell a name
  from an honorific, because doing it naively emits wrong P735 statements.

- **It trusts the NAME as a name.** Geni's NAME field is really a display
  *label*. Some of what it holds ("Unknown Wife", "NN", "daughter of …") is a
  description, and on Wikidata would be a label or an alias, not a P735/P734
  name. This module counts what is present; which strings are names is a
  judgement it does not make.

- **It reads ``_MARNM`` as one field with one meaning, and it does not have
  one.** Geni's custom married-name tag genuinely holds a married surname for
  much of the Norwegian tree, but in CJK records it doubles as the romanized
  surname slot. Its value is counted toward script coverage (a Latin ``_MARNM``
  on a CJK person *is* that person's romanization) but never read as "the
  married name".
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .model import Tree

__all__ = [
    "SCRIPT_RANGES",
    "FIELDS",
    "scripts_of",
    "Coverage",
    "measure",
    "summarise",
    "render_markdown",
]

#: Unicode ranges that decide which script a name form is written in, checked in
#: order. CJK folds kana and the ideograph blocks together on purpose — a
#: Japanese name mixing kana and kanji is one native form, not two — while
#: Hangul is kept separate because Korean romanisation behaves differently
#: again. "latin" is last of the writing systems so that a mostly-native string
#: with a stray ASCII digit still classifies by its script, not by the digit.
SCRIPT_RANGES: tuple[tuple[str, str], ...] = (
    # name, character-class body (inside a [...])
    ("cjk", r"぀-ヿ㐀-䶿一-鿿豈-﫿\U00020000-\U0002ffff"),
    ("hangul", r"가-힣ᄀ-ᇿ㄰-㆏"),
    ("cyrillic", r"Ѐ-ӿԀ-ԯ"),
    ("arabic", r"؀-ۿݐ-ݿ"),
    ("hebrew", r"֐-׿"),
    ("greek", r"Ͱ-Ͽἀ-῿"),
    ("latin", r"A-Za-zÀ-ɏ"),
)

_SCRIPT_RES = {name: re.compile(f"[{body}]") for name, body in SCRIPT_RANGES}

#: The enrichment fields, each with the Wikidata property a statement built from
#: it would use, and a predicate over a resolved :class:`~genimerge.model.Person`.
#: Order is the order the report shows them in.
FIELDS: tuple[tuple[str, str, str], ...] = (
    ("any name", "label", "name"),
    ("given name", "P735", "given"),
    ("surname", "P734", "surname"),
    ("multi-token given name", "P1545", "given_multi"),
    ("sex", "P21", "sex"),
    ("birth date", "P569", "birth_date"),
    ("birth place", "P19", "birth_place"),
    ("death date", "P570", "death_date"),
    ("death place", "P20", "death_place"),
    ("burial", "P119", "burial"),
    ("occupation", "P106", "occupation"),
    ("noble title", "P97", "title"),
    ("biography text", "—", "about"),
    ("parents recorded", "P22/P25", "parents"),
    ("marriage recorded", "P26", "marriage"),
)


def scripts_of(person) -> set[str]:
    """Every script that appears in any of a person's name forms.

    Looks at the whole NAME value, the given and surname slots, the ``_MARNM``
    romanisation slot and the nicknames — a person written natively but
    romanised in ``_MARNM`` counts as carrying both scripts, which is the whole
    point of the measurement.
    """
    found: set[str] = set()
    for name in person.names:
        for text in (name.full, name.given, name.surname, name.married, *name.nicknames):
            if not text:
                continue
            for script, pattern in _SCRIPT_RES.items():
                if pattern.search(text):
                    found.add(script)
    return found


def _has(person, key: str) -> bool:
    if key == "name":
        return any(n.given or n.surname or n.full.strip() for n in person.names)
    if key == "given":
        return any(n.given.strip() for n in person.names)
    if key == "surname":
        return any(n.surname.strip() for n in person.names)
    if key == "given_multi":
        return any(len(n.given.split()) > 1 for n in person.names)
    if key == "sex":
        return bool(person.sex.strip())
    if key == "birth_date":
        e = person.events.get("birth")
        return e is not None and e.date is not None
    if key == "birth_place":
        e = person.events.get("birth")
        return e is not None and bool(e.where.strip())
    if key == "death_date":
        e = person.events.get("death")
        return e is not None and e.date is not None
    if key == "death_place":
        e = person.events.get("death")
        return e is not None and bool(e.where.strip())
    if key == "burial":
        return "burial" in person.events
    if key == "occupation":
        return bool(person.occupations)
    if key == "title":
        return bool(person.titles)
    if key == "about":
        return bool(person.about.strip())
    if key == "parents":
        return bool(person.child_of)
    if key == "marriage":
        return bool(person.spouse_in)
    raise KeyError(key)


@dataclass
class Coverage:
    """The two measurements, plus the totals they are shares of."""

    people: int = 0
    #: field key -> people with it present
    fields: dict[str, int] = field(default_factory=dict)
    #: script name -> people carrying at least one form in it
    scripts: dict[str, int] = field(default_factory=dict)
    #: CJK people split by whether they also carry a Latin (romanised) form
    cjk_only: int = 0
    cjk_and_latin: int = 0
    #: people with no usable name at all
    unnamed: int = 0
    #: multi-token given people, split by the script of their names — the P1545
    #: trap is that the CJK share is romanised titles, not given names
    multi_given_latin: int = 0
    multi_given_cjk: int = 0


def measure(tree: Tree) -> Coverage:
    """Walk the canonical tree once and count everything the report shows."""
    cov = Coverage()
    cov.fields = {key: 0 for _, _, key in FIELDS}
    cov.scripts = {name: 0 for name, _ in SCRIPT_RANGES}

    for person in tree.people.values():
        cov.people += 1
        for _, _, key in FIELDS:
            if _has(person, key):
                cov.fields[key] += 1

        scripts = scripts_of(person)
        for script in scripts:
            cov.scripts[script] += 1

        if not _has(person, "name"):
            cov.unnamed += 1
        if "cjk" in scripts:
            if "latin" in scripts:
                cov.cjk_and_latin += 1
            else:
                cov.cjk_only += 1

        if _has(person, "given_multi"):
            if "cjk" in scripts:
                cov.multi_given_cjk += 1
            elif "latin" in scripts:
                cov.multi_given_latin += 1

    return cov


def summarise(cov: Coverage) -> dict[str, int]:
    """A flat dict of the headline numbers, for tests to assert against."""
    out = {"people": cov.people, "unnamed": cov.unnamed}
    out.update({f"field:{k}": v for k, v in cov.fields.items()})
    out.update({f"script:{k}": v for k, v in cov.scripts.items()})
    out["cjk_only"] = cov.cjk_only
    out["cjk_and_latin"] = cov.cjk_and_latin
    return out


def _pct(part: int, whole: int) -> str:
    return f"{100.0 * part / whole:.1f}%" if whole else "n/a"


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    sep = ["---", *["---:"] * (len(header) - 1)]
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
        *["| " + " | ".join(r) + " |" for r in rows],
    ]


def render_markdown(cov: Coverage) -> str:
    """The evidence for scoping the Wikidata enrichment pipeline."""
    n = cov.people
    lines = [
        "# What is in the profiles",
        "",
        "Generated by `genimerge.profilenames` — re-run `python -m genimerge profile-names`.",
        "",
        "Two measurements over the canonical tree, both per *person*: how often",
        "each field a Wikidata statement could carry is actually present, and",
        "which scripts the names are written in. **Nothing here proposes or",
        "creates anything** — it is what the enrichment pipeline (`todo.md` items",
        "4 and 6) can draw on, measured rather than assumed.",
        "",
        f"Measured over **{n:,} people**.",
        "",
        "## Field fill rates",
        "",
        "The share of people carrying each field, and the Wikidata property a",
        "statement built from it would use. This is the ceiling on how many people",
        "a batch for that property could touch.",
        "",
    ]
    rows = []
    for label, prop, key in FIELDS:
        c = cov.fields[key]
        rows.append([label, prop, f"{c:,}", _pct(c, n)])
    lines += _table(["field", "property", "people", "share"], rows)
    lines += [
        "",
        "Read the top and bottom of that table together. Sex and a given name are",
        "near-universal, so a per-person batch is mostly P21 + P735, with a",
        "surname and dates on roughly half. Occupation, burial and title are",
        "present on a small minority: real where they appear, but not something to",
        "scope the pipeline around.",
        "",
        "**`multi-token given name` is not a count of P1545 statements to emit.**",
        "It counts people whose `GIVN` has more than one whitespace token. In a",
        "European name that is the P1545 case — \"Jean Paul\" is two given-name",
        "items with series ordinals 1 and 2 — but most multi-token strings here",
        "are romanised CJK or steppe names where the extra tokens are honorifics,",
        "particles and titles (\"Lady\", \"no\", \"Chanyu\"), which are not given",
        f"names at all. Of the {cov.fields['given_multi']:,} multi-token people, "
        f"{cov.multi_given_cjk:,} also carry a CJK",
        f"form and {cov.multi_given_latin:,} are Latin-script; splitting `GIVN` on",
        "spaces is only safe once a step can tell a name from an honorific.",
        "",
        "## Name scripts",
        "",
        "Every person classified by the scripts their name forms use. A person can",
        "count under more than one script — that overlap is the point for CJK.",
        "",
    ]
    script_labels = {
        "cjk": "CJK (kanji/kana/hanzi)",
        "hangul": "Hangul (Korean)",
        "cyrillic": "Cyrillic",
        "arabic": "Arabic",
        "hebrew": "Hebrew",
        "greek": "Greek",
        "latin": "Latin",
    }
    rows = [
        [script_labels.get(name, name), f"{cov.scripts[name]:,}", _pct(cov.scripts[name], n)]
        for name, _ in SCRIPT_RANGES
    ]
    lines += _table(["script", "people", "share"], rows)

    cjk_total = cov.cjk_only + cov.cjk_and_latin
    lines += [
        "",
        f"{cov.unnamed:,} people carry no usable name at all.",
        "",
        "### The CJK romanisation gap",
        "",
        "The fear was that Japanese and Chinese people might be stored",
        "English-only, with the native name lost. The data says the opposite:",
        "",
        f"- **{cjk_total:,} people carry a CJK name form** ({_pct(cjk_total, n)} of the tree).",
        f"- Of those, **{cov.cjk_only:,} are native-script only** "
        f"({_pct(cov.cjk_only, cjk_total)} of CJK people) —",
        "  they have no romanised form at all.",
        f"- Only **{cov.cjk_and_latin:,} also carry a Latin/romanised form** "
        f"({_pct(cov.cjk_and_latin, cjk_total)}).",
        "",
        "So the native name — the hard thing to recover — is the well-covered one,",
        "and it matches Wikidata's own native labels directly. What is often",
        "missing is the *English* label, which Wikidata frequently supplies from",
        "its side. The non-Latin, non-CJK tails (Cyrillic, Arabic, Hebrew, Hangul)",
        "are the other native-script populations, and the same holds for them:",
        "they carry their own script, which is what entity resolution needs.",
        "",
        "## What this does not say",
        "",
        "A field being present is not a field being *right*: `reports/consistency.md`",
        "holds the dates that are impossible, and an uncorrected one here becomes a",
        "wrong statement on Wikidata. And a NAME being present is not a name being",
        "present — Geni's NAME is a display label, and some of it (\"Unknown Wife\",",
        "\"NN\") is a description that belongs in a label or alias, not in a P735 or",
        "P734 link. Which strings are names is a judgement this report does not make.",
        "",
    ]
    return "\n".join(lines)
