"""How much of Wikidata's Geni-linked population do we hold, and vice versa.

Emma's ask, 2026-08-06: "do a SPARQL on wikidata to find the overlap of our tree
with the total number of wikidata items with geni id property".

**Why this pulls all of P2600 rather than asking about our IDs.**
:func:`genimerge.wikidata.match_by_geni_id` answers "which of *our* people have
an item?" by putting our IDs in a ``VALUES`` clause a few hundred at a time —
203,323 IDs is around 510 queries, and it can only ever report the half of the
overlap that faces us. The other half — Wikidata items with a Geni ID we have
never seen — is the more interesting one for a world tree, and no ``VALUES``
query over our own IDs can produce it.

So this fetches **every** P2600 statement instead. That is about 517,000 rows,
which is too many for one response, so the statements are split sixteen ways on
``MD5`` of the item URI. Hashing gives even partitions where the obvious splits
do not: Geni IDs nearly all begin ``6000000``, so a prefix split would put
almost everything in one bucket. Sixteen partitions of ~32k rows each run in
about 25 seconds apiece, comfortably inside the endpoint's budget, and every
response goes through the same on-disk cache as everything else — so an
interrupted run resumes for free and a re-render costs nothing.

**Counts are reported three ways because they genuinely differ.** Items,
distinct ID values, and statements are not the same number: an item can carry
several Geni IDs and a Geni ID can appear on several items. Collapsing them
would hide exactly the rows a human needs to look at, which is the same reason
:func:`~genimerge.wikidata.match_by_geni_id` returns pairs rather than a dict.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Iterable, Sequence

__all__ = [
    "PARTITIONS",
    "partition_query",
    "COUNT_QUERIES",
    "fetch_all_p2600",
    "Overlap",
    "measure",
    "render_markdown",
]

#: Hex digits MD5 output starts with. Sixteen partitions of roughly 32k rows.
PARTITIONS = "0123456789abcdef"

#: The three totals that differ from each other, asked directly rather than
#: derived from the fetched rows — so a partition that silently returned short
#: shows up as a mismatch instead of as a smaller world.
COUNT_QUERIES = {
    "items": "SELECT (COUNT(DISTINCT ?item) AS ?n) WHERE { ?item wdt:P2600 ?g }",
    "values": "SELECT (COUNT(DISTINCT ?g) AS ?n) WHERE { ?item wdt:P2600 ?g }",
    "statements": "SELECT (COUNT(*) AS ?n) WHERE { ?item wdt:P2600 ?g }",
    "humans": (
        "SELECT (COUNT(DISTINCT ?item) AS ?n) WHERE "
        "{ ?item wdt:P2600 ?g ; wdt:P31 wd:Q5 }"
    ),
}


def partition_query(prefix: str) -> str:
    """Every P2600 statement whose item URI hashes to ``prefix``."""
    return (
        "SELECT ?item ?g WHERE { ?item wdt:P2600 ?g . "
        f'FILTER(STRSTARTS(MD5(STR(?item)), "{prefix}")) }}'
    )


def _qid(uri: str) -> str:
    return uri.rsplit("/", 1)[-1]


def fetch_all_p2600(
    client,
    *,
    partitions: Sequence[str] = PARTITIONS,
    progress: Callable[[int, int], None] | None = None,
) -> list[tuple[str, str]]:
    """Every (QID, Geni ID) pair on Wikidata, as a list of pairs.

    A list rather than a dict in either direction, because the relation is not
    a function either way — see the module docstring.
    """
    pairs: list[tuple[str, str]] = []
    for index, prefix in enumerate(partitions, start=1):
        for row in client.sparql(partition_query(prefix)):
            pairs.append((_qid(row["item"]), row["g"]))
        if progress is not None:
            progress(index, len(partitions))
    return pairs


#: Geni's own profile IDs are digits. Anything else on P2600 is a data problem
#: on Wikidata's side -- a URL, a vanity slug -- and cannot join to our xrefs.
NUMERIC = re.compile(r"^[0-9]+$")


@dataclass
class Overlap:
    """The two-sided count. Every field is a set size, not an estimate."""

    #: what the endpoint says, independently of the rows we fetched
    reported: dict[str, int] = field(default_factory=dict)

    ours: set[str] = field(default_factory=set)
    theirs: set[str] = field(default_factory=set)

    #: Geni ID -> the QIDs carrying it, only where there is more than one
    id_on_several_items: dict[str, list[str]] = field(default_factory=dict)
    #: QID -> the Geni IDs on it, only where there is more than one
    item_with_several_ids: dict[str, list[str]] = field(default_factory=dict)
    #: P2600 values that are not all digits, so cannot join to a GEDCOM xref
    non_numeric: list[tuple[str, str]] = field(default_factory=list)

    @property
    def both(self) -> set[str]:
        return self.ours & self.theirs

    @property
    def ours_only(self) -> set[str]:
        return self.ours - self.theirs

    @property
    def theirs_only(self) -> set[str]:
        return self.theirs - self.ours


def measure(pairs: Iterable[tuple[str, str]], our_ids: Iterable[str],
            reported: dict[str, int] | None = None) -> Overlap:
    by_id: dict[str, list[str]] = defaultdict(list)
    by_item: dict[str, list[str]] = defaultdict(list)
    non_numeric: list[tuple[str, str]] = []

    for qid, geni_id in pairs:
        if not NUMERIC.match(geni_id):
            non_numeric.append((qid, geni_id))
            continue
        if qid not in by_id[geni_id]:
            by_id[geni_id].append(qid)
        if geni_id not in by_item[qid]:
            by_item[qid].append(geni_id)

    return Overlap(
        reported=dict(reported or {}),
        ours=set(our_ids),
        theirs=set(by_id),
        id_on_several_items={k: sorted(v) for k, v in by_id.items() if len(v) > 1},
        item_with_several_ids={k: sorted(v) for k, v in by_item.items() if len(v) > 1},
        non_numeric=sorted(non_numeric),
    )


def _pct(part: int, whole: int) -> str:
    return f"{100 * part / whole:.2f}%" if whole else "—"


def render_markdown(o: Overlap, *, people: int, exports: int) -> str:
    both, ours_only, theirs_only = len(o.both), len(o.ours_only), len(o.theirs_only)
    lines = [
        "# Our tree against every Wikidata item with a Geni ID",
        "",
        "Generated by `python -m genimerge overlap`. Every figure is an exact join",
        "on the Geni profile ID — this repo's primary key — never a name match.",
        "",
        f"Measured over the **{people:,}-person merge ({exports} exports)** and",
        "**every P2600 statement on Wikidata**, fetched in sixteen MD5 partitions",
        "rather than by asking about our own IDs, so the count faces both ways.",
        "",
        "## The two sides",
        "",
        "| | count |",
        "| --- | ---: |",
        f"| Wikidata items carrying a Geni ID | {o.reported.get('items', 0):,} |",
        f"| …of those, instances of human (Q5) | {o.reported.get('humans', 0):,} |",
        f"| distinct Geni ID **values** on Wikidata | {o.reported.get('values', 0):,} |",
        f"| P2600 **statements** | {o.reported.get('statements', 0):,} |",
        f"| joinable Geni IDs fetched (all digits) | {len(o.theirs):,} |",
        f"| people in our tree | {len(o.ours):,} |",
        "",
        "The first four differ from each other on purpose: an item can carry more",
        "than one Geni ID and a Geni ID can sit on more than one item. They are",
        "reported separately rather than collapsed, because the rows that make them",
        "differ are the rows a human has to look at.",
        "",
        "## The overlap",
        "",
        "| | count | of our tree | of Wikidata's Geni IDs |",
        "| --- | ---: | ---: | ---: |",
        f"| **in both** | {both:,} | {_pct(both, len(o.ours))} | {_pct(both, len(o.theirs))} |",
        f"| ours only | {ours_only:,} | {_pct(ours_only, len(o.ours))} | — |",
        f"| Wikidata only | {theirs_only:,} | — | {_pct(theirs_only, len(o.theirs))} |",
        "",
        "**The second and third columns are the whole point and they are not the",
        "same question.** Column two asks how much of our genealogy Wikidata",
        "already knows. Column three asks how much of Wikidata's Geni-linked",
        f"population we hold — {theirs_only:,} people whose Geni profile Wikidata",
        "names and no export here has reached.",
        "",
    ]

    if o.id_on_several_items:
        lines += [
            "## Geni IDs on more than one Wikidata item",
            "",
            f"**{len(o.id_on_several_items)}** of them. Each is either a duplicate",
            "pair of items that should be merged, or a wrong P2600 — and nothing",
            "here can tell which, so nothing here guesses.",
            "",
            "| Geni ID | items |",
            "| --- | --- |",
        ]
        for geni_id, qids in sorted(o.id_on_several_items.items())[:40]:
            mine = " ← **in our tree**" if geni_id in o.ours else ""
            lines.append(f"| `{geni_id}` | {', '.join(qids)}{mine} |")
        if len(o.id_on_several_items) > 40:
            lines.append(f"\n…and {len(o.id_on_several_items) - 40} more.")
        lines.append("")

    if o.item_with_several_ids:
        lines += [
            "## Wikidata items carrying more than one Geni ID",
            "",
            f"**{len(o.item_with_several_ids)}** of them. Usually a person with two",
            "Geni profiles that Geni itself has not merged.",
            "",
            "| item | Geni IDs |",
            "| --- | --- |",
        ]
        for qid, ids in sorted(o.item_with_several_ids.items())[:40]:
            marks = ", ".join(f"`{i}`" + ("*" if i in o.ours else "") for i in ids)
            lines.append(f"| {qid} | {marks} |")
        if len(o.item_with_several_ids) > 40:
            lines.append(f"\n…and {len(o.item_with_several_ids) - 40} more.")
        lines += ["", "`*` marks an ID that is in our tree.", ""]

    if o.non_numeric:
        lines += [
            "## P2600 values that are not a profile ID",
            "",
            f"**{len(o.non_numeric)}** values are not all digits, so they cannot join",
            "to a GEDCOM xref at all. They are excluded from every count above.",
            "",
            "| item | value |",
            "| --- | --- |",
            *[f"| {q} | `{v}` |" for q, v in o.non_numeric[:25]],
            "",
        ]

    lines += [
        "## What this does not say",
        "",
        "A Geni ID on a Wikidata item is a claim by whoever added it, and this",
        "report takes it at face value. `reports/wikidata-crosscheck.md` is where",
        "links are tested against the genealogy; two are flagged there as worth",
        "re-checking despite being exact P2600 matches.",
        "",
        "And the Wikidata-only figure is not a queue of people to create — they",
        "already have items. It is the measure of how much of the Geni-linked",
        "world our exports have not reached, which is the number to watch as the",
        "corpus grows.",
    ]
    return "\n".join(lines) + "\n"
