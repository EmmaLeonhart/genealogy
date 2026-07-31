"""The tree's name vocabulary, and which of it Wikidata already has items for.

Wikidata does not store a person's name as text. It points at *items*: P735
given name and P734 family name each take an item, and that item has to exist
before anyone can be linked to it. So "add name links to these people" is
really two questions, and only the second is a decision:

1. which names does this tree actually use, and how often — measurable now;
2. which of those have no Wikidata item, and is creating them worth it —
   the user's call.

This module answers the first and measures the second. **It proposes nothing
and creates nothing.**

Two things about Geni's data shape the code. Its ``GIVN`` field holds a whole
given string — "Ragnhild Rasmusdatter", not "Ragnhild" — while P735 takes one
item per given name, so both the full string and its individual tokens are
recorded. And this is a Norwegian tree, so most of what looks like a surname is
a **patronymic**: Torsteinson, Olavsdotter, Rasmusdatter. Those are counted
separately, because they are the bulk of the vocabulary and the least likely to
have items.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from .model import Tree

__all__ = [
    "NameUse",
    "Vocabulary",
    "PATRONYMIC_SUFFIXES",
    "is_patronymic",
    "build_vocabulary",
    "summarise",
    "find_name_items",
    "render_markdown",
    "NAME_ITEM_TYPES",
    "NAME_LANGUAGES",
]

#: Languages to look names up in. Names are rarely translated, but Wikidata
#: labels a name item in whichever languages someone got round to.
NAME_LANGUAGES = ("en", "no", "nb", "nn", "sv", "da", "de")

#: Norwegian, Swedish and Danish patronymic endings, longest first so that
#: "-sdatter" is not mistaken for "-datter" of some other stem.
PATRONYMIC_SUFFIXES = (
    "sdatter",
    "sdotter",
    "sdottir",
    "sdóttir",
    "datter",
    "dotter",
    "dottir",
    "dóttir",
    "sson",
    "ssøn",
    "sson",
    "sen",
    "son",
    "søn",
)

#: Wikidata types that make an item a name item. Exact `P31` values rather than
#: a subclass walk: the walk is far slower on the public endpoint and these five
#: cover what P734/P735 values actually use.
NAME_ITEM_TYPES = (
    "Q101352",  # family name
    "Q202444",  # given name
    "Q12308941",  # male given name
    "Q11879590",  # female given name
    "Q3409032",  # unisex given name
)

_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def is_patronymic(name: str) -> bool:
    """Does this look like a patronymic rather than an inherited surname?

    A heuristic, and it will call some genuine surnames patronymic — plenty of
    Scandinavian families took a frozen patronymic as a hereditary surname, and
    nothing in the text distinguishes the two. It is used only to *group* the
    report, never to decide anything.
    """
    lowered = name.strip().lower()
    if len(lowered) < 5:
        return False
    return any(lowered.endswith(suffix) for suffix in PATRONYMIC_SUFFIXES)


@dataclass
class NameUse:
    """One name string, and who uses it."""

    text: str
    count: int = 0
    #: Geni IDs of people carrying it, capped — the report only shows examples
    examples: list[str] = field(default_factory=list)
    patronymic: bool = False

    def note(self, geni_id: str, example_limit: int = 5) -> None:
        self.count += 1
        if len(self.examples) < example_limit:
            self.examples.append(geni_id)


@dataclass
class Vocabulary:
    """Every name the tree uses, split by how Wikidata would model it."""

    #: values that would become P734 family name
    surnames: dict[str, NameUse] = field(default_factory=dict)
    #: whole GIVN strings, e.g. "Ragnhild Rasmusdatter"
    given_full: dict[str, NameUse] = field(default_factory=dict)
    #: individual given-name tokens, which is what P735 actually takes
    given_tokens: dict[str, NameUse] = field(default_factory=dict)
    #: people with no usable name at all
    unnamed: int = 0

    def top(self, which: str, limit: int = 50, only: str | None = None) -> list[NameUse]:
        """Most frequent names. ``only`` filters to ``patronymic``/``inherited``."""
        source = getattr(self, which)
        uses = list(source.values())
        if only == "patronymic":
            uses = [u for u in uses if u.patronymic]
        elif only == "inherited":
            uses = [u for u in uses if not u.patronymic]
        return sorted(uses, key=lambda u: (-u.count, u.text))[:limit]

    def all_strings(self) -> list[str]:
        """Every distinct name string, for one round of Wikidata lookups."""
        return sorted(set(self.surnames) | set(self.given_full) | set(self.given_tokens))


def _record(store: dict[str, NameUse], text: str, geni_id: str, patronymic: bool) -> None:
    use = store.get(text)
    if use is None:
        use = store[text] = NameUse(text=text, patronymic=patronymic)
    use.note(geni_id)


def build_vocabulary(tree: Tree, people: Iterable[str] | None = None) -> Vocabulary:
    """Collect every surname and given name in the tree.

    Counts *people*, not name records: someone with three `NAME` lines all
    saying "Borsheim" counts once for Borsheim, because the question being asked
    is how many people would gain a link.
    """
    vocabulary = Vocabulary()
    ids = list(people) if people is not None else list(tree.people)

    for geni_id in ids:
        person = tree.people.get(geni_id)
        if person is None:
            continue

        surnames: set[str] = set()
        given_full: set[str] = set()
        given_tokens: set[str] = set()

        for name in person.names:
            surname = name.surname.strip()
            if surname:
                surnames.add(surname)
            given = " ".join(name.given.split())
            if given:
                given_full.add(given)
                given_tokens.update(_WORD.findall(given))

        if not surnames and not given_full:
            vocabulary.unnamed += 1
            continue

        for text in surnames:
            _record(vocabulary.surnames, text, geni_id, is_patronymic(text))
        for text in given_full:
            _record(vocabulary.given_full, text, geni_id, is_patronymic(text))
        for text in given_tokens:
            _record(vocabulary.given_tokens, text, geni_id, is_patronymic(text))

    return vocabulary


def find_name_items(
    client,
    strings: Iterable[str],
    *,
    languages: Iterable[str] = NAME_LANGUAGES,
    types: Iterable[str] = NAME_ITEM_TYPES,
    literals_per_query: int = 700,
    progress=None,
) -> dict[str, list[tuple[str, str, str]]]:
    """Which of these name strings already have a Wikidata *name item*.

    Returns ``name -> [(qid, type qid, "label" | "alias"), ...]``.

    Restricting to the five name types matters: without it, "Eikeland" matches a
    village and "Ragnhild" matches a queen, and neither is something P734 or
    P735 could point at.

    Whether the match was on the item's **label** or on one of its **aliases**
    is reported rather than flattened, because the two are not equally strong.
    An alias is usually a spelling variant of the same name, but it is a weaker
    assertion than a label, so callers that go on to *propose edits* use label
    matches only and set the rest aside for review. Callers that are only
    measuring coverage can use both.
    """
    ordered = sorted({s for s in strings if s.strip()})
    languages = list(languages)
    type_values = " ".join(f"wd:{t}" for t in types)
    found: dict[str, list[tuple[str, str, str]]] = defaultdict(list)

    per_batch = max(1, literals_per_query // max(len(languages), 1))
    batches = [ordered[i : i + per_batch] for i in range(0, len(ordered), per_batch)]

    for index, batch in enumerate(batches, start=1):
        values = " ".join(
            '"{}"@{}'.format(name.replace("\\", "\\\\").replace('"', '\\"'), lang)
            for name in batch
            for lang in languages
        )
        # Two plain queries rather than one with a UNION. The UNION form times
        # the public endpoint out (504) on batches this size, while each of
        # these is a straight index lookup.
        for predicate, kind in (("rdfs:label", "label"), ("skos:altLabel", "alias")):
            query = (
                "SELECT DISTINCT ?item ?type ?label WHERE {\n"
                f"  VALUES ?label {{ {values} }}\n"
                f"  VALUES ?type {{ {type_values} }}\n"
                f"  ?item {predicate} ?label.\n"
                "  ?item wdt:P31 ?type.\n"
                "}"
            )
            for row in client.sparql(query):
                qid = row["item"].rsplit("/", 1)[-1]
                type_qid = row["type"].rsplit("/", 1)[-1]
                entry = (qid, type_qid, kind)
                if entry not in found[row["label"]]:
                    found[row["label"]].append(entry)
        if progress is not None:
            progress(index, len(batches))

    return dict(found)


def summarise(vocabulary: Vocabulary) -> dict[str, Counter]:
    """Headline counts, for the report and for tests to assert against."""
    out: dict[str, Counter] = defaultdict(Counter)
    for which in ("surnames", "given_full", "given_tokens"):
        store: dict[str, NameUse] = getattr(vocabulary, which)
        out[which]["distinct"] = len(store)
        out[which]["patronymic"] = sum(1 for u in store.values() if u.patronymic)
        out[which]["uses"] = sum(u.count for u in store.values())
    return dict(out)


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    sep = ["---", *["---:"] * (len(header) - 1)]
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
        *["| " + " | ".join(r) + " |" for r in rows],
    ]


def _pct(part: int, whole: int) -> str:
    return f"{100.0 * part / whole:.1f}%" if whole else "n/a"


def render_markdown(
    vocabulary: Vocabulary,
    items: dict[str, list[tuple[str, str]]],
    *,
    top: int = 40,
) -> str:
    """The evidence for deciding whether creating name items is worth doing."""
    lines = [
        "# Name vocabulary",
        "",
        "Generated by `genimerge.names` — re-run `python -m genimerge names`.",
        "",
        "Wikidata does not store a name as text. P735 (given name) and P734",
        "(family name) point at *items*, and the item has to exist before anyone",
        "can be linked to it. So this measures which of the tree's names already",
        "have one. **Nothing here proposes creating anything** — it is the",
        "evidence for deciding whether that is worth doing, and how big a job it",
        "would be.",
        "",
    ]

    sections = [
        ("surnames", "Surnames", "P734"),
        ("given_tokens", "Given names (single tokens, which is what P735 takes)", "P735"),
        ("given_full", "Whole given-name strings, as Geni stores them", "—"),
    ]

    lines += ["## Overview", ""]
    rows = []
    for which, label, prop in sections:
        store: dict[str, NameUse] = getattr(vocabulary, which)
        have = sum(1 for name in store if items.get(name))
        rows.append(
            [
                f"{label} ({prop})",
                str(len(store)),
                str(have),
                _pct(have, len(store)),
                str(sum(1 for u in store.values() if u.patronymic)),
            ]
        )
    lines += _table(
        ["", "distinct", "with a Wikidata item", "share", "look patronymic"], rows
    )
    lines += [
        "",
        f"{vocabulary.unnamed} people in the tree carry no usable name at all.",
        "",
        "\"Look patronymic\" is a suffix heuristic (`-sson`, `-sdatter`, `-sen`,",
        "…). It will call some genuine inherited surnames patronymic, because",
        "plenty of Scandinavian families froze a patronymic into a hereditary",
        "surname and nothing in the text tells the two apart. It is used to group",
        "this report and for nothing else.",
        "",
    ]

    for which, label, prop in sections:
        store = getattr(vocabulary, which)
        missing = [u for u in store.values() if not items.get(u.text)]
        missing.sort(key=lambda u: (-u.count, u.text))

        lines += [
            f"## {label} — most common with no Wikidata item",
            "",
            f"{len(missing)} of {len(store)} have no name item. Ranked by how many",
            f"people would gain a {prop} link if one existed.",
            "",
        ]
        lines += _table(
            ["name", "people", "looks patronymic"],
            [
                [use.text, str(use.count), "yes" if use.patronymic else ""]
                for use in missing[:top]
            ],
        )
        lines += [""]

        present = [(u, items[u.text]) for u in store.values() if items.get(u.text)]
        present.sort(key=lambda pair: (-pair[0].count, pair[0].text))
        if present:
            lines += [
                f"### {label} that already have items",
                "",
                f"The {min(len(present), top)} most used, of {len(present)}.",
                "",
            ]
            lines += _table(
                ["name", "people", "item(s)"],
                [
                    [
                        use.text,
                        str(use.count),
                        ", ".join(
                            f"[{qid}](https://www.wikidata.org/wiki/{qid})"
                            + ("" if kind == "label" else " *(alias)*")
                            for qid, _type, kind in found[:3]
                        )
                        + (" …" if len(found) > 3 else ""),
                    ]
                    for use, found in present[:top]
                ],
            )
            lines += [""]

    return "\n".join(lines)
