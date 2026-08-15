"""Propose P735 / P734 links to name items that **already exist** on Wikidata.

Wikidata models a person's name as a link to a name *item*: P735 given name,
P734 family name. Creating the missing name items is a decision nobody has made
yet — but 874 of this tree's surnames and 1950 of its given names already have
items, and linking a person to an item that exists creates nothing and decides
nothing. That is the part that can be done now.

Everything here is conservative on purpose, because a wrong name link is quiet
and hard to notice:

- **Only names that resolve to exactly one item, by that item's label.** "Anders"
  is several Wikidata items; picking one would be guessing, so every ambiguous
  name is set aside for a human. A match on an *alias* is also set aside — not
  because aliases are usually wrong (they are usually a spelling variant of the
  same name) but because an alias is a weaker assertion than a label, and this
  file proposes edits. The two alias-only matches in the current run are listed
  for review rather than dropped.
- **Only the person's primary name record.** People here carry several, and the
  order of given names across records is not meaningful — within one record it
  is.
- **Only items with no P735/P734 at all.** Adding a *second* given name to an
  item that already has one risks duplicating what is there under a different
  spelling. An item that already says something is left alone and reported.
- **Patronymics in the given-name field are never proposed.** Geni's ``GIVN``
  routinely holds "Ragnhild Rasmusdatter", and calling ``Rasmusdatter`` a given
  name would be wrong. They are listed separately.

Nothing here is written to Wikidata. The output is a file to review.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable

from .model import Tree
from .names import is_patronymic
from .claims import Statement, geni_reference

__all__ = ["NameLink", "Skipped", "NameBatch", "build_name_links", "render_markdown"]

GIVEN_NAME = "P735"
FAMILY_NAME = "P734"
SERIES_ORDINAL = "P1545"

_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


@dataclass(frozen=True)
class NameLink:
    qid: str
    prop: str
    name_item: str
    #: the name text this came from, for the readable report
    text: str
    geni_id: str
    person: str = ""
    ordinal: int | None = None


@dataclass(frozen=True)
class Skipped:
    geni_id: str
    person: str
    text: str
    reason: str
    detail: str = ""


@dataclass
class NameBatch:
    links: list[NameLink] = field(default_factory=list)
    skipped: list[Skipped] = field(default_factory=list)
    retrieved: str = ""
    #: how many people were considered at all
    considered: int = 0

    @property
    def people_touched(self) -> int:
        return len({link.geni_id for link in self.links})


def existing_name_claims_from_store(reader, qids: Iterable[str]) -> dict[str, set[str]]:
    """Which of P735/P734 each item already states, from the downloaded store.

    This was the offline half of a pair; the SPARQL half, `_existing_name_claims`,
    was deleted on 2026-08-15 when Emma chose *"make it offline, keep the logic"*
    for `name-links`. It is now the only implementation.

    `queue.md` 2.B, ported by question rather than by emulating SPARQL. The
    question is only "which of P735/P734 does this item already state" — the
    *values* are never read here, so it does not matter that the name items
    themselves are absent from the store.

    That absence is real and worth stating next to this function, because it is
    what stops `names.py` being ported the same way: the download walked
    P22/P25/P26/P40/P3373, so it holds people and not name items. Measured over
    40 shards on 2026-08-10 — of 13,683 distinct P735/P734 targets referenced,
    **55 were in the store, 0.4%**.

    Truthy semantics, as in :func:`genimerge.crosscheck.claims_from_store`: a
    deprecated statement is not something the item states.
    """
    have: dict[str, set[str]] = {}
    for qid, entity in reader.entities(qids).items():
        claims = entity.get("claims") or {}
        for prop in (GIVEN_NAME, FAMILY_NAME):
            for statement in claims.get(prop) or []:
                if statement.get("rank") == "deprecated":
                    continue
                snak = statement.get("mainsnak") or {}
                if snak.get("snaktype") != "value":
                    continue
                have.setdefault(qid, set()).add(prop)
                break
    return have


def name_items_from_resolution(rows: Iterable[dict]) -> dict[str, list[tuple[str, str, str]]]:
    """`reports/name-resolution.csv` in the shape :func:`build_name_links` wants.

    That file is built by matching **exactly on an item's label**, case- and
    diacritic-folded — never on an alias. So every entry here is a ``"label"``
    match, which is *stricter* than the SPARQL lookup it replaces rather than
    looser: the alias-only matches this module deliberately sets aside simply
    never appear. The middle element is the item type, which the CSV does not
    carry; it is empty and nothing reads it.
    """
    out: dict[str, list[tuple[str, str, str]]] = {}
    for row in rows:
        name = (row.get("name") or "").strip()
        qids = [q.strip() for q in (row.get("qids") or "").split("|") if q.strip()]
        if not name or not qids:
            continue
        out.setdefault(name, []).extend((q, "", "label") for q in qids)
    return out


def build_name_links(
    existing: dict[str, set[str]],
    tree: Tree,
    linked: dict[str, str],
    name_items: dict[str, list[tuple[str, str, str]]],
    *,
    retrieved: str,
) -> NameBatch:
    """Build the batch.

    ``existing`` is ``qid -> {properties it already states}``, from
    :func:`existing_name_claims_from_store`. ``linked`` is geni_id -> qid;
    ``name_items`` is from :func:`name_items_from_resolution`. **Nothing here
    takes a client** — this module stopped touching the network on 2026-08-15.
    """
    batch = NameBatch(retrieved=retrieved)

    def resolve(text: str) -> tuple[str | None, str]:
        """The single name item whose *label* is this text, or why there isn't one."""
        found = name_items.get(text) or []
        if not found:
            return None, "no Wikidata name item exists"

        # An alias is a weaker assertion than a label, and this file proposes
        # edits, so alias-only matches are reported rather than acted on.
        by_label = [entry for entry in found if entry[2] == "label"]
        if not by_label:
            return None, "matches only as an alias of another name"
        if len(by_label) > 1:
            return None, f"{len(by_label)} name items share this text"
        return by_label[0][0], ""

    for geni_id, qid in sorted(linked.items(), key=lambda kv: kv[1]):
        person = tree.people.get(geni_id)
        if person is None or not person.names:
            continue
        batch.considered += 1
        display = person.display_name
        primary = person.names[0]
        already = existing.get(qid, set())

        surname = primary.surname.strip()
        if surname:
            if FAMILY_NAME in already:
                batch.skipped.append(
                    Skipped(geni_id, display, surname, "item already states a family name")
                )
            else:
                item, why = resolve(surname)
                if item is None:
                    batch.skipped.append(Skipped(geni_id, display, surname, why))
                else:
                    batch.links.append(
                        NameLink(qid, FAMILY_NAME, item, surname, geni_id, display)
                    )

        tokens = _WORD.findall(primary.given)
        if tokens and GIVEN_NAME in already:
            batch.skipped.append(
                Skipped(geni_id, display, primary.given, "item already states a given name")
            )
        elif tokens:
            resolved: list[tuple[str, str]] = []
            blocked = False
            for token in tokens:
                if is_patronymic(token):
                    batch.skipped.append(
                        Skipped(
                            geni_id,
                            display,
                            token,
                            "patronymic in the given-name field",
                            "Geni's GIVN holds the whole given string; this token is "
                            "not a given name",
                        )
                    )
                    blocked = True
                    continue
                item, why = resolve(token)
                if item is None:
                    batch.skipped.append(Skipped(geni_id, display, token, why))
                    blocked = True
                    continue
                resolved.append((token, item))

            # All or nothing per person: proposing the second given name without
            # the first would put a wrong series ordinal on the item.
            if resolved and not blocked:
                for index, (token, item) in enumerate(resolved, start=1):
                    batch.links.append(
                        NameLink(
                            qid,
                            GIVEN_NAME,
                            item,
                            token,
                            geni_id,
                            display,
                            ordinal=index if len(resolved) > 1 else None,
                        )
                    )
            elif resolved and blocked:
                for token, _item in resolved:
                    batch.skipped.append(
                        Skipped(
                            geni_id,
                            display,
                            token,
                            "held back: another given name in the same record could "
                            "not be resolved",
                            "proposing part of a name would put a wrong order on the item",
                        )
                    )

    return batch


def to_statements(batch: NameBatch) -> list[Statement]:
    return [
        Statement(
            qid=link.qid,
            prop=link.prop,
            value=link.name_item,
            qualifiers=(
                ((SERIES_ORDINAL, f'"{link.ordinal}"'),) if link.ordinal else ()
            ),
            references=geni_reference(link.geni_id, batch.retrieved),
        )
        for link in batch.links
    ]


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    sep = ["---", *["---:"] * (len(header) - 1)]
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
        *["| " + " | ".join(r) + " |" for r in rows],
    ]


def render_markdown(batch: NameBatch, *, top: int = 60) -> str:
    from collections import Counter

    lines = [
        "# Proposed claims: name links",
        "",
        "Generated by `genimerge.namelinks` — re-run `python -m genimerge name-links`.",
        "",
        "**Nothing here has been sent to Wikidata**, and nothing runs before",
        "1 September 2026. This is a list to read and check; the executable",
        "form is the JSON edit objects, specified in `edit-objects.md`.",
        "",
        "Every statement links a person to a name item that **already exists**.",
        "Nothing is created. The rules that keep this safe, all enforced:",
        "",
        "- only names resolving to exactly one Wikidata item **by that item's",
        "  label** — an ambiguous name is set aside, never picked between, and a",
        "  match that is only an alias is listed for review rather than acted",
        "  on, since an alias is a weaker assertion than a label;",
        "- only the person's primary name record, since order across records is",
        "  not meaningful;",
        "- only items stating no P735/P734 at all, so nothing already there is",
        "  duplicated under a different spelling;",
        "- patronymics sitting in Geni's given-name field are never proposed as",
        "  given names.",
        "",
    ]

    lines += _table(
        ["", "count"],
        [
            ["people considered", str(batch.considered)],
            ["**statements proposed**", str(len(batch.links))],
            ["people they cover", str(batch.people_touched)],
            ["names set aside", str(len(batch.skipped))],
        ],
    )

    reasons = Counter(s.reason for s in batch.skipped)
    if reasons:
        lines += ["", "## Why names were set aside", ""]
        lines += _table(
            ["reason", "names"], [[reason, str(n)] for reason, n in reasons.most_common()]
        )

    if batch.links:
        lines += [
            "",
            "## Statements in the batch",
            "",
            f"Showing {min(len(batch.links), top)} of {len(batch.links)}.",
            "",
        ]
        lines += _table(
            ["item", "property", "name item", "from", "person"],
            [
                [
                    f"[{link.qid}](https://www.wikidata.org/wiki/{link.qid})",
                    "family name" if link.prop == FAMILY_NAME else "given name",
                    f"[{link.name_item}](https://www.wikidata.org/wiki/{link.name_item})",
                    link.text,
                    link.person,
                ]
                for link in batch.links[:top]
            ],
        )

    ambiguous = [s for s in batch.skipped if "share this text" in s.reason]
    if ambiguous:
        lines += [
            "",
            "## Ambiguous names — for a human",
            "",
            "Each of these matches more than one Wikidata name item. Choosing",
            "between them is a judgement about which item is the right one, so",
            "none of these are in the batch.",
            "",
        ]
        seen: set[str] = set()
        rows = []
        for skip in ambiguous:
            if skip.text in seen:
                continue
            seen.add(skip.text)
            rows.append([skip.text, skip.reason])
        lines += _table(["name", "why"], rows[:top])

    return "\n".join(lines) + "\n"
