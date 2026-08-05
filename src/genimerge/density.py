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
from pathlib import Path

from .frontier import family_graph
from .identity import profile_url
from .model import Tree

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
    #: who to export from to cover this region — see :func:`_representative`
    seed: str = ""
    seed_name: str = ""

    @property
    def size(self) -> int:
        return len(self.members)


def _representative(
    members: list[str], tree: Tree, graph: dict[str, list[str]]
) -> tuple[str, str]:
    """One person to export from, to cover this region.

    Ranked on three things, in order:

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

    This is a heuristic for *where to start*, not a claim that this person is
    the most important in the region.
    """
    inside = set(members)
    best: tuple[tuple[int, int, int], str] | None = None
    for geni_id in members:
        person = tree.people[geni_id]
        name = person.display_name or ""
        rank = (
            0 if person.has_known_parents else 1,
            0 if (not name or name.lower().strip("<> ") == "private") else 1,
            sum(1 for n in graph.get(geni_id, ()) if n in inside),
        )
        if best is None or rank > best[0]:
            best = (rank, geni_id)
    if best is None:  # pragma: no cover - regions are never empty
        return "", ""
    return best[1], tree.people[best[1]].display_name or ""


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
        seed, seed_name = _representative(members, tree, graph)
        regions.append(
            Region(
                members=tuple(members),
                parentless=sum(1 for p in people if not p.has_known_parents),
                sample=tuple(named[:6]),
                mean_presence=sum(counts.get(m, 0) for m in members) / len(members),
                seed=seed,
                seed_name=seed_name,
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
        lines += [
            "The **seed** column is one person to export from, per region: a "
            "doorway where possible, preferring someone with a real name over a "
            "redacted `Private`, and best-connected within the region. It is a "
            "heuristic for where to start, not a claim about who matters.",
            "",
        ]
        lines += _table(
            ["#", "people", "doorways", "seed to export from", "who else is in it"],
            [
                [
                    str(i),
                    str(r.size),
                    str(r.parentless),
                    (
                        f"[{r.seed_name or r.seed}]({profile_url(r.seed)})"
                        if r.seed
                        else "—"
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
        if not region.seed:
            continue
        name = region.seed_name or "NN"
        lines.append(f"{profile_url(region.seed)} | Geni - {name}")
    return "\n".join(lines) + ("\n" if lines else "")
