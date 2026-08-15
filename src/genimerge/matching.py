"""The offline pieces that outlived ``reconcile``.

``reconcile`` was deleted on 2026-08-15 on Emma's instruction. It held a live
Wikidata client and searched for people **by name**, which she had ordered
removed on 2026-08-12: *"no fucking clue why there's a fuzzy matcher that sounds
like something you made with zero consent from me."* The whole module went,
command and tests included.

Four things in it never touched the network and three other modules still need
them, so they live here rather than being deleted alongside. Nothing in this
module makes a request, and nothing here compares names — that was the point of
the deletion.
"""

from __future__ import annotations

from collections import deque
from typing import Iterable

from .model import Tree

#: How far apart two birth or death years may be and still corroborate. Wider
#: for dates the export itself marked approximate. Read by ``crosscheck`` when
#: it decides whether Geni and Wikidata agree about a date.
YEAR_TOLERANCE = 3
YEAR_TOLERANCE_APPROX = 10


def year_of(value: str | None) -> int | None:
    """Pull the year out of a Wikidata time literal like ``+1130-01-01T00:00:00Z``.

    Wikidata sometimes returns a blank node instead of a date ("some value"), so
    anything that is not a plain literal has to be discarded rather than parsed.

    This is for **Wikidata** literals only. A GEDCOM date goes to
    :func:`genimerge.dates.parse_date` — never to a regex, and never here.
    """
    if not value or "genid" in value:
        return None
    text = value.lstrip("+")
    negative = value.startswith("-")
    head = text.split("-", 1)[0] if not negative else text.split("-", 2)[1]
    try:
        year = int(head)
    except ValueError:
        return None
    return -year if negative else year


def _neighbour_ids(person, tree: Tree) -> list[str]:
    # parent_ids rather than father_id/mother_id: a child in two families keeps
    # only the first family's father in the primary fields, which would make
    # this relation asymmetric and distort the distance measure.
    ids = person.spouse_ids + person.child_ids + person.parent_ids
    return [i for i in ids if i in tree.people]


def distance_from_matched(tree: Tree, matched: Iterable[str]) -> dict[str, int]:
    """How many family steps each person is from the nearest matched person."""
    distance = {geni_id: 0 for geni_id in matched if geni_id in tree.people}
    queue = deque(distance)
    while queue:
        current = queue.popleft()
        for neighbour in _neighbour_ids(tree.people[current], tree):
            if neighbour not in distance:
                distance[neighbour] = distance[current] + 1
                queue.append(neighbour)
    return distance
