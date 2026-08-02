"""Where the tree stops, and which profiles are worth exporting from next.

A Geni GEDCOM export holds a few thousand individuals — see
:data:`genimerge.seeds.GENI_EXPORT_CAP` for why the bound is not written as an
exact number — so covering this tree means many exports rather than a few, and
the question "which profile do I export from next?" is worth answering with
evidence instead of intuition.

The merged file is referentially closed — no family pointer dangles — so the
edge of the tree is not broken links. It is **people with no parents recorded**.
Each one is a place where Geni knows more than we do, and the good ones to
export from are those with the largest subtree hanging off them: exporting a
lone leaf adds a lone leaf, while exporting a well-connected ancestor extends a
whole branch.

Disconnected components matter for the same reason. A component nobody in
another component is related to needs its own export seed, because no walk
outward from the main tree will ever reach it.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field

from .model import Person, Tree

__all__ = [
    "Component",
    "BranchPoint",
    "components",
    "family_graph",
    "descendant_counts",
    "ancestor_depth",
    "ancestry_cycles",
    "branch_points",
    "render_markdown",
]


@dataclass
class Component:
    """A set of people connected to each other and to nobody else."""

    members: list[str]
    #: members with no parent recorded — the upward edge of this component
    parentless: list[str] = field(default_factory=list)

    @property
    def size(self) -> int:
        return len(self.members)


@dataclass
class BranchPoint:
    """A profile worth exporting from, and why."""

    person: Person
    descendants: int
    relatives: int
    component_size: int
    reason: str

    @property
    def score(self) -> int:
        return self.descendants


def family_graph(tree: Tree) -> dict[str, list[str]]:
    """Everyone who shares a family with each person: parents, spouses, children, siblings.

    Built by walking the *family* records, so the relation is symmetric by
    construction. Two earlier versions were not, and both invented a phantom
    one-person component: deriving neighbours from ``father_id``/``mother_id``
    loses the second family of a child who has two, and deriving them from the
    person's own ``FAMC``/``FAMS`` pointers loses a family that lists the person
    without the person listing it back.
    """
    graph: dict[str, set[str]] = {geni_id: set() for geni_id in tree.people}

    for family in tree.families.values():
        members = [
            m for m in family.parent_ids + family.child_ids if m in tree.people
        ]
        for member in members:
            graph[member].update(m for m in members if m != member)

    return {geni_id: sorted(others) for geni_id, others in graph.items()}


def _neighbours(person: Person, tree: Tree) -> list[str]:
    """One person's neighbours. Prefer :func:`family_graph` when doing many."""
    return family_graph(tree).get(person.geni_id, [])


def components(tree: Tree, graph: dict[str, list[str]] | None = None) -> list[Component]:
    """Connected components of the family graph, largest first."""
    graph = family_graph(tree) if graph is None else graph
    seen: set[str] = set()
    found: list[Component] = []

    for start in tree.people:
        if start in seen:
            continue
        members: list[str] = []
        queue = deque([start])
        seen.add(start)
        while queue:
            current = queue.popleft()
            members.append(current)
            for neighbour in graph.get(current, ()):
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        found.append(
            Component(
                members=members,
                parentless=[m for m in members if not tree.people[m].has_known_parents],
            )
        )

    return sorted(found, key=lambda c: c.size, reverse=True)


def _child_map(tree: Tree) -> dict[str, list[str]]:
    return {
        geni_id: [c for c in person.child_ids if c in tree.people]
        for geni_id, person in tree.people.items()
    }


def _parent_map(tree: Tree) -> dict[str, list[str]]:
    return {
        geni_id: [p for p in person.parent_ids if p in tree.people]
        for geni_id, person in tree.people.items()
    }


def _post_order(nodes: list[str], edges: dict[str, list[str]]) -> list[str]:
    """Nodes ordered so every node comes after everything it points to.

    Explicitly iterative and cycle-tolerant. Genealogies do contain cycles —
    somebody entered twice ends up their own ancestor — and a naive recursive
    walk either overflows the stack or never terminates. An edge back into a
    node still being expanded is ignored, which is the only sane reading: a
    person is not their own descendant.
    """
    order: list[str] = []
    done: set[str] = set()
    active: set[str] = set()

    for root in nodes:
        if root in done:
            continue
        stack = [(root, False)]
        while stack:
            node, expanded = stack.pop()
            if expanded:
                active.discard(node)
                if node not in done:
                    done.add(node)
                    order.append(node)
                continue
            if node in done or node in active:
                continue
            active.add(node)
            stack.append((node, True))
            for child in edges.get(node, ()):
                if child not in done and child not in active:
                    stack.append((child, False))
    return order


def descendant_counts(tree: Tree) -> dict[str, int]:
    """How many distinct people descend from each person.

    Descendant *sets* overlap heavily — cousins marry, and the same ancestor is
    reached down several lines — so counts cannot be summed from children
    without double-counting, and walking the full set per person is O(n·m),
    which on 8766 people does not finish in any reasonable time.

    So each set is carried as a bitmask in a Python int: one bit per person,
    unioned with ``|`` up the post-order. Exact, no double-counting, and about a
    kilobyte per person.
    """
    children = _child_map(tree)
    index = {geni_id: i for i, geni_id in enumerate(tree.people)}
    masks: dict[str, int] = {}

    for node in _post_order(list(tree.people), children):
        mask = 0
        for child in children[node]:
            mask |= (1 << index[child]) | masks.get(child, 0)
        masks[node] = mask

    return {geni_id: mask.bit_count() for geni_id, mask in masks.items()}


def ancestor_depth(tree: Tree) -> dict[str, int]:
    """Longest chain of recorded ancestors above each person."""
    parents = _parent_map(tree)
    depth: dict[str, int] = {}

    for node in _post_order(list(tree.people), parents):
        known = [depth[p] for p in parents[node] if p in depth]
        depth[node] = 1 + max(known) if known else 0

    return depth


def ancestry_cycles(tree: Tree) -> list[list[str]]:
    """People who are their own ancestor.

    Impossible in life, ordinary in a genealogy database: it means the same
    person exists under two profiles and the two got linked as parent and child.
    Worth reporting rather than silently absorbing, because it is a real defect
    in the source data and it quietly distorts every generational measure.
    """
    parents = _parent_map(tree)
    state: dict[str, int] = {}
    found: list[list[str]] = []

    for start in tree.people:
        if state.get(start):
            continue
        path: list[str] = [start]
        state[start] = 1
        stack: list[tuple[str, list[str]]] = [(start, list(parents[start]))]

        while stack:
            node, pending = stack[-1]
            if not pending:
                state[node] = 2
                stack.pop()
                path.pop()
                continue
            parent = pending.pop()
            if state.get(parent) == 1:
                found.append(path[path.index(parent) :] + [parent])
            elif state.get(parent, 0) == 0:
                state[parent] = 1
                path.append(parent)
                stack.append((parent, list(parents[parent])))

    return found


def branch_points(
    tree: Tree,
    limit: int = 40,
    *,
    descendants: dict[str, int] | None = None,
    comps: list[Component] | None = None,
    graph: dict[str, list[str]] | None = None,
) -> list[BranchPoint]:
    """Parentless people ranked by how much of the tree hangs off them.

    ``descendants``, ``comps`` and ``graph`` are accepted so a caller that
    already computed them does not pay again; all three are expensive over 8766
    people.
    """
    graph = family_graph(tree) if graph is None else graph
    descendants = descendant_counts(tree) if descendants is None else descendants
    component_of: dict[str, int] = {}
    for component in comps if comps is not None else components(tree, graph):
        for member in component.members:
            component_of[member] = component.size

    ranked = []
    for person in tree.people.values():
        if person.has_known_parents:
            continue
        relatives = len(graph.get(person.geni_id, ()))
        ranked.append(
            BranchPoint(
                person=person,
                descendants=descendants.get(person.geni_id, 0),
                relatives=relatives,
                component_size=component_of.get(person.geni_id, 1),
                reason=_reason(person, descendants.get(person.geni_id, 0), relatives),
            )
        )

    ranked.sort(key=lambda b: (b.descendants, b.relatives), reverse=True)
    return ranked[:limit]


def _reason(person: Person, descendants: int, relatives: int) -> str:
    if descendants >= 100:
        return "no parents recorded, and a large branch hangs off them"
    if descendants > 0:
        return "no parents recorded, some descendants known"
    if relatives:
        return "no parents and no descendants recorded; only a spouse link"
    return "no relatives recorded at all"


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    sep = ["---", *["---:"] * (len(header) - 1)]
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
        *["| " + " | ".join(r) + " |" for r in rows],
    ]


def render_markdown(tree: Tree, limit: int = 40) -> str:
    graph = family_graph(tree)
    comps = components(tree, graph)
    depth = ancestor_depth(tree)
    counts = descendant_counts(tree)
    points = branch_points(tree, limit, descendants=counts, comps=comps, graph=graph)
    parentless = [p for p in tree.people.values() if not p.has_known_parents]
    isolated = [p for p in parentless if not graph.get(p.geni_id)]

    lines = [
        "# Expansion frontier",
        "",
        "Generated by `genimerge.frontier` — re-run `python -m genimerge frontier`.",
        "",
        "A Geni GEDCOM export holds a few thousand individuals — the four taken",
        "so far held 3836, 3836, 3836 and 3840 — so covering this tree means",
        "many exports. The merged file has no dangling family pointers, so",
        "the edge of what we know is not broken links — it is **people with no",
        "parents recorded**. Those are the places Geni knows more than we do.",
        "",
        "## Where the tree stops",
        "",
    ]
    lines += _table(
        ["", "count", "share"],
        [
            ["people", str(len(tree.people)), "100%"],
            [
                "with no parents recorded",
                str(len(parentless)),
                f"{100.0 * len(parentless) / max(len(tree.people), 1):.1f}%",
            ],
            [
                "with no relatives at all",
                str(len(isolated)),
                f"{100.0 * len(isolated) / max(len(tree.people), 1):.1f}%",
            ],
            ["connected components", str(len(comps)), ""],
        ],
    )

    lines += [
        "",
        "## Components",
        "",
        "A component nobody outside it is related to needs its own export seed —",
        "no walk outward from the main tree will ever reach it.",
        "",
    ]
    lines += _table(
        ["component", "people", "of which parentless", "largest branch point"],
        [
            [
                str(i),
                str(c.size),
                str(len(c.parentless)),
                _name_of(tree, _biggest(c, counts)),
            ]
            for i, c in enumerate(comps[:15], start=1)
        ],
    )
    if len(comps) > 15:
        smaller = comps[15:]
        lines += [
            "",
            f"{len(smaller)} further components, holding "
            f"{sum(c.size for c in smaller)} people between them.",
        ]

    cycles = ancestry_cycles(tree)
    if cycles:
        lines += [
            "",
            "## People recorded as their own ancestor",
            "",
            f"**{len(cycles)}** — impossible in life, and a sign the same person "
            "exists under two Geni profiles that were then linked as parent and "
            "child. Each one quietly distorts the generational measures below, "
            "and each is worth fixing on Geni.",
            "",
        ]
        lines += _table(
            ["cycle"],
            [
                [" → ".join(_name_of(tree, g) for g in cycle)]
                for cycle in cycles[:20]
            ],
        )

    lines += [
        "",
        "## Generational depth",
        "",
        "Longest recorded ancestor chain above each person. The deepest chains",
        "are where the tree is already well developed; the shallow ones with many",
        "descendants are where an export would add the most.",
        "",
    ]
    buckets = Counter(depth.values())
    lines += _table(
        ["generations above", "people"],
        [[str(d), str(n)] for d, n in sorted(buckets.items())],
    )

    lines += [
        "",
        f"## Best {len(points)} profiles to export from next",
        "",
        "Ranked by how many people descend from them: exporting the ancestors of",
        "a well-connected person extends a whole branch, while exporting a lone",
        "leaf adds a lone leaf.",
        "",
    ]
    lines += _table(
        ["#", "name", "born", "descendants", "relatives", "component", "Geni profile"],
        [
            [
                str(i),
                point.person.display_name or "*(unnamed)*",
                str(point.person.birth_year or ""),
                str(point.descendants),
                str(point.relatives),
                str(point.component_size),
                f"[{point.person.geni_id}]({point.person.url})",
            ]
            for i, point in enumerate(points, start=1)
        ],
    )

    return "\n".join(lines) + "\n"


def _biggest(component: Component, counts: dict[str, int]) -> str | None:
    if not component.parentless:
        return None
    return max(component.parentless, key=lambda m: counts.get(m, 0))


def _name_of(tree: Tree, geni_id: str | None) -> str:
    if geni_id is None:
        return "*(none)*"
    person = tree.people.get(geni_id)
    return person.display_name if person and person.display_name else f"`{geni_id}`"
