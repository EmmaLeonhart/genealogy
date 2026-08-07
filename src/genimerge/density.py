"""Where the tree is thin: regions reached by few exports.

`genimerge.frontier` finds where the tree *stops* — people with no parents
recorded. That is a hard edge. This module finds something softer and, once
enough exports are in hand, more useful: **where the tree is thin rather than
absent**.

The measure is **presence**: for each person, how many exports contain them.
Every export is a breadth-first ball around one seed, so a person appearing in
many exports sits where many balls overlap — a neighbourhood covered from
several directions and probably recorded to some depth. A person appearing in
exactly one sits on the rim of a single ball, where the export ran out of budget
rather than out of relatives.

**One thin person means nothing; a contiguous stretch of them means a lot.** Any
ball has a rim, and its rim is thin by construction. What identifies an
under-covered region is a *connected run* of low-presence people — a piece of
graph that only one export ever brushed, large enough that its interior was
never reached. So this ranks connected components of the low-presence subgraph
by size, not individuals by presence.

**"Region" here means a region of the graph, never a place.** It is a
neighbourhood under parent/child/spouse edges. Nothing is classified
geographically: birthplace strings are mostly absent and inferring a place from
a name is the fuzzy matching this repo refuses everywhere else.

**What this cannot tell you.** Presence measures our sampling, not Geni's
content. A thin region is one *we* have barely covered; whether Geni holds much
more there is exactly what is unknown, and is why it is worth an export. A
region can also be thin because it genuinely is small — a family that really did
end. The doorway count per region is the check: a thin region with many
parentless people is under-sampled, while a thin region with none may simply be
finished.
"""

from __future__ import annotations

import re
from collections import Counter, deque
from dataclasses import dataclass
from math import ceil
from pathlib import Path

from .frontier import family_graph
from .identity import profile_url
from .model import Tree
from .seeds import GENI_EXPORT_CAP

__all__ = [
    "INDI_RE",
    "Region",
    "presence_counts",
    "sparse_regions",
    "render_markdown",
    "render_seed_list",
]

#: Level-0 INDI xrefs. Deliberately the same shape the rest of the repo relies
#: on rather than a full parse: presence only needs to know which profile IDs a
#: file contains, and parsing 54 exports properly to answer that costs minutes.
INDI_RE = re.compile(r"^0 @I(\d+)@ INDI", re.M)


def presence_counts(paths: list[str | Path]) -> Counter:
    """How many of these exports contain each Geni profile ID."""
    counts: Counter = Counter()
    for path in paths:
        text = Path(path).read_text(encoding="utf-8-sig")
        counts.update(set(INDI_RE.findall(text)))
    return counts


@dataclass(frozen=True)
class Region:
    """A connected run of people no more than `threshold` exports ever reached."""

    members: tuple[str, ...]
    parentless: int
    #: a few names, for recognising what this region *is*
    sample: tuple[str, ...]
    #: mean presence across the region
    mean_presence: float
    #: who to export from to cover this region, spread across it — see
    #: :func:`_representatives`. One entry for every export the region needs,
    #: best first, as ``(geni_id, display_name)``.
    seeds: tuple[tuple[str, str], ...] = ()

    @property
    def size(self) -> int:
        return len(self.members)

    @property
    def seed(self) -> str:
        """The first seed. Kept because a region needing one export is still
        the common case by a wide margin, and every caller wanting *the* seed
        would otherwise index into a tuple."""
        return self.seeds[0][0] if self.seeds else ""

    @property
    def seed_name(self) -> str:
        return self.seeds[0][1] if self.seeds else ""

    @property
    def exports_needed(self) -> int:
        """How many exports it would take to cover this region.

        An export is a ball of at most `GENI_EXPORT_CAP` people, so a region
        larger than that cannot be covered by one however well it is seeded.
        This is the count of seeds the region is given.
        """
        return max(1, ceil(self.size / GENI_EXPORT_CAP))


def _doorway_rank(
    geni_id: str, tree: Tree, graph: dict[str, list[str]], inside: set[str]
) -> tuple[int, int, int]:
    """How good a seed one person is, ranked on three things in order:

    1. **No parents recorded.** Everyone in the region is thin, but a person
       whose parents are missing is a doorway: Geni knows who they were and we
       do not, so a ball centred there grows upward into material we have none
       of rather than re-walking what we hold.
    2. **A usable name.** Geni redacts living people to ``Private``, and a
       region of them cannot be recognised or checked by a human deciding
       whether the export is worth taking.
    3. **Degree inside the region.** An export is a breadth-first ball, so
       seeding it at a well-connected member covers more of the region per hop
       than seeding it at a leaf.

    A heuristic for *where to start*, not a claim about who matters.
    """
    person = tree.people[geni_id]
    name = person.display_name or ""
    return (
        0 if person.has_known_parents else 1,
        0 if (not name or name.lower().strip("<> ") == "private") else 1,
        sum(1 for n in graph.get(geni_id, ()) if n in inside),
    )


def _hops_within(
    start: str, inside: set[str], graph: dict[str, list[str]]
) -> dict[str, int]:
    """Breadth-first distances from `start`, never leaving the region.

    Staying inside matters: two seeds should be far apart *in the region being
    covered*, and a shortcut through well-covered graph outside it would report
    them as close when the export balls would not overlap at all.
    """
    seen = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbour in graph.get(current, ()):
            if neighbour in inside and neighbour not in seen:
                seen[neighbour] = seen[current] + 1
                queue.append(neighbour)
    return seen


def _representatives(
    members: list[str], tree: Tree, graph: dict[str, list[str]], want: int
) -> tuple[tuple[str, str], ...]:
    """`want` people to export from, spread across the region.

    A region larger than one export ball cannot be covered by one seed, and the
    report used to emit exactly one however large the region was — region 1 was
    10 051 people against a ~4 020 ball, so two thirds of it had no proposal at
    all and the reader had no way to ask for a second.

    **Seeds after the first are placed by distance, not by rank.** Taking the
    top `want` by :func:`_doorway_rank` would pick neighbours: a well-connected
    doorway's neighbours are usually also well-connected doorways, so the balls
    would land on top of each other and the second export would re-fetch the
    first. Each further seed is therefore the member *furthest from every seed
    already chosen* — farthest-point sampling — with the doorway rank used only
    to break ties between equally distant candidates.

    The first seed is still the best-ranked person in the region, so a
    one-export region behaves exactly as it did before this existed.
    """
    if not members:  # pragma: no cover - regions are never empty
        return ()
    inside = set(members)
    rank = {g: _doorway_rank(g, tree, graph, inside) for g in members}

    first = max(members, key=lambda g: (rank[g], g))
    chosen = [first]
    if want <= 1:
        return ((first, tree.people[first].display_name or ""),)

    # Distance from each member to the nearest seed chosen so far. A member the
    # walk cannot reach cannot happen — regions are connected by construction —
    # so a missing entry would be a bug; it is filled with a value larger than
    # any real distance rather than silently read as zero.
    ceiling = len(members)
    nearest = dict(_hops_within(first, inside, graph))
    while len(chosen) < want:
        remaining = [g for g in members if g not in chosen]
        if not remaining:
            break
        best = max(remaining, key=lambda g: (nearest.get(g, ceiling), rank[g], g))
        if nearest.get(best, ceiling) == 0:
            break  # every member is already a seed
        chosen.append(best)
        for node, distance in _hops_within(best, inside, graph).items():
            if distance < nearest.get(node, distance + 1):
                nearest[node] = distance

    return tuple((g, tree.people[g].display_name or "") for g in chosen)


def sparse_regions(
    tree: Tree,
    counts: Counter,
    threshold: int = 1,
    min_size: int = 2,
    graph: dict[str, list[str]] | None = None,
) -> list[Region]:
    """Connected components of the people whose presence is <= `threshold`.

    Ranked largest first. `min_size` drops the singletons, which are the rim of
    a ball rather than a region and would otherwise be most of the output.
    """
    graph = graph if graph is not None else family_graph(tree)
    thin = {g for g in tree.people if counts.get(g, 0) <= threshold}

    seen: set[str] = set()
    regions: list[Region] = []
    for start in thin:
        if start in seen:
            continue
        members: list[str] = []
        queue = deque([start])
        seen.add(start)
        while queue:
            current = queue.popleft()
            members.append(current)
            for neighbour in graph.get(current, ()):
                if neighbour in thin and neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        if len(members) < min_size:
            continue

        people = [tree.people[m] for m in members]
        named = [p.display_name for p in people if p.display_name]
        want = max(1, ceil(len(members) / GENI_EXPORT_CAP))
        regions.append(
            Region(
                members=tuple(members),
                parentless=sum(1 for p in people if not p.has_known_parents),
                sample=tuple(named[:6]),
                mean_presence=sum(counts.get(m, 0) for m in members) / len(members),
                seeds=_representatives(members, tree, graph, want),
            )
        )

    regions.sort(key=lambda r: (-r.size, -r.parentless))
    return regions


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    align = ["---"] + ["---:"] * (len(header) - 1)
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(align) + " |",
        *["| " + " | ".join(r) + " |" for r in rows],
    ]


def render_markdown(
    tree: Tree,
    counts: Counter,
    regions: list[Region],
    export_count: int,
    threshold: int,
) -> str:
    total = len(tree.people)
    histogram = Counter(counts.get(g, 0) for g in tree.people)
    thin_people = sum(v for k, v in histogram.items() if k <= threshold)

    lines = [
        "# Where the tree is thin",
        "",
        "Generated by `genimerge.density` — re-run `python -m genimerge density`.",
        "",
        f"**Presence** is how many of the {export_count} exports contain a person. "
        "Every export is a breadth-first ball around one seed, so presence measures "
        "how many directions we have covered a neighbourhood from — not how much "
        "Geni holds there, which is exactly what is unknown.",
        "",
        "## Presence across the tree",
        "",
    ]
    lines += _table(
        ["in this many exports", "people", "share"],
        [
            [str(k), str(histogram[k]), f"{histogram[k] / total:.1%}"]
            for k in sorted(histogram)
        ],
    )
    lines += [
        "",
        f"**{thin_people} people ({thin_people / total:.1%}) are in {threshold} export "
        "or fewer.**",
        "",
        "## Thin regions",
        "",
        "A *region* is a connected run of those people under parent/child/spouse "
        "edges — a piece of graph only one export ever brushed. One thin person is "
        "just the rim of a ball and means nothing; a large connected run of them is "
        "a neighbourhood we have sampled once and never returned to.",
        "",
        "**Read the doorway column before exporting.** A thin region full of "
        "parentless people is under-sampled and worth an export. A thin region with "
        "few is plausibly just a small family that really did end, and exporting "
        "there buys little.",
        "",
    ]

    if regions:
        many = [r for r in regions[:60] if r.exports_needed > 1]
        lines += [
            "The **seeds** column is who to export from: a doorway where "
            "possible, preferring someone with a real name over a redacted "
            "`Private`, and best-connected within the region. A heuristic for "
            "where to start, not a claim about who matters.",
            "",
            f"**A region larger than ~{GENI_EXPORT_CAP:,} people needs more than "
            "one export**, because that is the largest ball Geni has yet "
            "returned — so those regions get one seed per export they need, and "
            "the extra seeds are placed as far apart *inside the region* as the "
            "graph allows. Ranking would have put them next to each other: a "
            "well-connected doorway's neighbours are usually also "
            "well-connected doorways, and the second ball would land on the "
            "first. **Take them one at a time and re-run `density` in "
            "between** — the later seeds are computed against the region as it "
            "is now, and the first export changes it.",
            "",
        ]
        if many:
            lines += [
                f"{len(many)} of the regions shown need more than one export; "
                f"the largest needs {max(r.exports_needed for r in many)}.",
                "",
            ]
        lines += _table(
            ["#", "people", "doorways", "exports", "seeds to export from", "who else is in it"],
            [
                [
                    str(i),
                    str(r.size),
                    str(r.parentless),
                    str(r.exports_needed),
                    (
                        "<br>".join(
                            f"[{name or geni_id}]({profile_url(geni_id)})"
                            for geni_id, name in r.seeds
                        )
                        or "—"
                    ),
                    ", ".join(r.sample[:4]) or "—",
                ]
                for i, r in enumerate(regions[:60], start=1)
            ],
        )
        if len(regions) > 60:
            lines += ["", f"{len(regions) - 60} smaller regions not shown."]
    else:
        lines += ["None: no connected run of thin people reaches the minimum size."]

    lines += [
        "",
        "## What this does not say",
        "",
        "Presence measures our sampling, not Geni's content. A thin region is one "
        "**we** have barely covered; whether Geni knows more there is the open "
        "question an export answers. Nothing here classifies anyone "
        "geographically — a region is a neighbourhood in the family graph.",
        "",
    ]
    return "\n".join(lines) + "\n"


def render_seed_list(regions: list[Region]) -> str:
    """One line per region, in the shape of `individuals I can easily export.txt`.

    ``<url> | Geni - <name>``, so the output drops straight into the file Emma
    already keeps by hand and can be pasted back into a browser.
    """
    lines = []
    for region in regions:
        for geni_id, seed_name in region.seeds:
            lines.append(f"{profile_url(geni_id)} | Geni - {seed_name or 'NN'}")
    return "\n".join(lines) + ("\n" if lines else "")
