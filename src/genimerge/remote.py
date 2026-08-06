"""The most remote people in the tree, ranked — not pairs, and not greedy.

**Why this exists alongside `distant`.** `distant` answers "give me some pairs
that are far apart" by running a double sweep and then retiring the whole
neighbourhood of each pair it emits. That works, but the answer it gives depends
on where the first sweep happened to land: pair 2 is whatever survived pair 1's
retirement, pair 3 whatever survived pair 2, and so on down a list that visibly
tails off. Emma read the result as arbitrary, which is a fair reading of a
greedy sequence — nothing in it says *these* are the most remote people, only
that they were far from each other in the order they were picked.

This asks the question the other way round and about **people, not pairs**: for
every person, how far is the person they are *furthest* from? That number is
their eccentricity, and ranking by it gives a list where row 1 really is the
most remote person the measurement can find, row 2 the next, and so on. There is
no ordering artefact to explain away.

**Eccentricity is approximated from below, and the bound is one-sided.** Exact
eccentricity is a BFS per person — 200,000 sweeps. Instead a small set of
**landmarks** is chosen and one BFS is run from each, giving every person a
vector of distances to the landmarks. Their reported remoteness is the largest
entry in that vector. Since a landmark is a real person, that distance is a real
distance: **the number is never an overestimate**, and it is exact whenever a
landmark happens to sit at the far end. It can understate someone whose true
antipode is in a direction no landmark covers, which is what makes the landmark
choice matter.

**Landmarks are chosen by farthest-point sampling**, the standard k-centre
greedy: start at a double-sweep endpoint, then repeatedly take the person
furthest from every landmark chosen so far. That drives landmarks onto the rim
and spreads them around it, which is exactly the placement that makes "max
distance to a landmark" a tight lower bound on eccentricity.

**The separation rule is a proof, not a heuristic.** The raw ranking is useless
on its own: the top of it is one deep lineage listed forty times, because
everyone near a diameter endpoint has nearly the same eccentricity. So a person
is kept only if their landmark vector differs from every already-kept person's
by at least `SEPARATION` in some coordinate. Distances obey
``|d(u,L) − d(v,L)| ≤ d(u,v)`` for any landmark ``L``, so a vector gap of *k*
**proves** the two people are at least *k* hops apart. Every row of the output
is therefore provably in a different part of the graph from every other row —
which is the property `distant`'s retirement radius was reaching for and could
only approximate. The converse does not hold: two people with similar vectors
might still be far apart in a direction no landmark sees, so the filter can drop
someone it need not have. It errs toward a shorter, cleaner list.

**What a row is for.** The person, plus the landmark they are furthest from,
is a pair to open on Geni. Our tree says they are that many hops apart; Geni
will very likely show a much shorter chain, and the people on it are ones we do
not hold — the same prediction `distant` makes, from a ranking that can say why
these people and not others.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path

from .distant import _usable, bfs
from .frontier import family_graph
from .identity import profile_url
from .model import Tree

__all__ = [
    "RemotePerson",
    "components",
    "landmarks",
    "most_remote",
    "path_url",
    "render_html",
    "render_markdown",
]

#: How many landmarks to place across the whole tree. Each one costs a BFS over
#: every person, and the gain from more of them falls off quickly: they are
#: chosen to be far apart, so the tenth is already covering a direction the
#: first nine nearly did. Twelve is a few seconds on a 200k-person tree.
LANDMARKS = 12

#: Minimum landmarks in any component large enough to be measured at all. Two
#: is the floor because one landmark measures distance *from one place*, which
#: says nothing about the far side of it.
MIN_LANDMARKS_PER_COMPONENT = 2

#: Components smaller than this are skipped. Remoteness inside a hamlet of
#: twenty people is a fact about the hamlet, and the point of the report is to
#: find long walks.
MIN_COMPONENT = 50

#: Two listed people must differ by at least this many hops, proved via the
#: landmark vectors. Relative to the widest measurement because the tree's width
#: is not known in advance, with a floor so a small tree cannot report cousins.
#:
#: A quarter, not a tenth. The first real run used 0.12, which on a 311-hop
#: graph means 37 — technically a proof that two rows are different people, and
#: useless as a report: rows 3 to 22 were all the same Chinese lineage, each
#: legitimately 37-odd hops from the last, all pointing at the same partner.
#: The share has to be large enough that "a different part of the graph" means
#: different at the scale the graph actually is.
SEPARATION_SHARE = 0.25
MIN_SEPARATION = 20


@dataclass(frozen=True)
class RemotePerson:
    geni_id: str
    name: str
    #: hops to the landmark they are furthest from — a lower bound on their
    #: true eccentricity, never an overestimate
    remoteness: int
    #: that landmark: the other half of the pair to open on Geni
    partner_id: str
    partner_name: str
    #: how many people are in this person's component, so a big number from a
    #: small island is readable as one
    component_size: int

    @property
    def url(self) -> str:
        return profile_url(self.geni_id)

    @property
    def partner_url(self) -> str:
        return profile_url(self.partner_id)

    def path_url(self, kind: str = "blood") -> str:
        return path_url(self.partner_id, self.geni_id, kind)


def path_url(from_id: str, to_id: str, kind: str = "blood") -> str:
    """Geni's page for the relationship path between two profiles.

    Taken from the `href` Geni itself writes on a profile page rather than
    guessed — see the saved pages in `geni_pages/`, every one of which carries
    this link with the profile the path was drawn from as `from_id`.

    `kind` is `blood` or `inlaw`. Blood is the shorter, cleaner chain when one
    exists; in-law is the one that matches how distance is measured here, since
    a hop crosses a marriage as readily as a birth.
    """
    return (
        "https://www.geni.com/inconsistencies/for_path"
        f"?from_id={from_id}&to_id={to_id}&path_type={kind}"
    )


def components(graph: dict[str, list[str]]) -> list[list[str]]:
    """Connected components, largest first.

    Landmarks have to be placed per component: a BFS cannot leave the component
    it starts in, so a person in a component holding no landmark would have no
    measurement at all rather than a small one.
    """
    seen: set[str] = set()
    found: list[list[str]] = []
    for start in graph:
        if start in seen:
            continue
        members = []
        queue = deque([start])
        seen.add(start)
        while queue:
            current = queue.popleft()
            members.append(current)
            for neighbour in graph[current]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        found.append(members)
    found.sort(key=len, reverse=True)
    return found


def _pick(dist: dict[str, int], tree: Tree | None) -> str:
    """The furthest person in `dist` who is not a redacted profile.

    Every landmark is half of a reported pair — the person the row says to open
    on Geni alongside the remote one — so a `Private` landmark makes its whole
    row unusable. That applies to the first landmark as much as the rest: the
    first is a double-sweep endpoint, and a diameter endpoint of a real tree is
    quite often a redacted living person at the young end of a line.

    Falls back to the furthest of any name if none are usable, so a wholly
    redacted component still yields a measurement rather than nothing.
    """
    if not dist:
        return ""
    if tree is None:
        return max(dist, key=lambda n: dist[n])
    named = [n for n in dist if _usable(tree.people[n].display_name or "")]
    pool = named or list(dist)
    return max(pool, key=lambda n: dist[n])


def landmarks(
    graph: dict[str, list[str]],
    members: list[str],
    count: int,
    tree: Tree | None = None,
) -> tuple[list[str], dict[str, dict[str, int]]]:
    """`count` landmarks in one component, plus the BFS from each.

    Farthest-point sampling. The first landmark is a double-sweep endpoint
    rather than an arbitrary node, because starting the greedy at the rim is
    what puts the rest of it there too.

    Returns the landmarks in the order chosen and their distance maps, so the
    caller does not pay for the sweeps twice.
    """
    if not members:
        return [], {}

    start = min(members, key=int)
    first = bfs(graph, start)
    seed = _pick(first, tree)
    if not seed:
        return [], {}

    chosen = [seed]
    sweeps = {seed: bfs(graph, seed)}
    # Distance from each person to the nearest landmark so far; the next
    # landmark is whoever maximises it.
    nearest = dict(sweeps[seed])

    while len(chosen) < count:
        candidate = _pick(nearest, tree)
        if not candidate or nearest[candidate] == 0:
            break  # every reachable person is already a landmark
        chosen.append(candidate)
        sweeps[candidate] = bfs(graph, candidate)
        for node, d in sweeps[candidate].items():
            if d < nearest.get(node, d + 1):
                nearest[node] = d

    return chosen, sweeps


def _vectors(
    chosen: list[str], sweeps: dict[str, dict[str, int]], members: list[str]
) -> dict[str, tuple[int, ...]]:
    """Each person's distance to every landmark, in landmark order.

    A person unreachable from a landmark cannot happen inside one component, so
    a missing entry would be a bug; it is filled with the component's size,
    which is larger than any real distance, rather than silently read as zero.
    """
    ceiling = len(members)
    return {
        node: tuple(sweeps[lm].get(node, ceiling) for lm in chosen) for node in members
    }


def most_remote(
    tree: Tree,
    count: int = 20,
    landmark_count: int = LANDMARKS,
    graph=None,
) -> list[RemotePerson]:
    """The `count` most remote people, each provably far from all the others."""
    graph = graph if graph is not None else family_graph(tree)
    if not graph:
        return []

    parts = [c for c in components(graph) if len(c) >= MIN_COMPONENT]
    if not parts:
        return []
    total = sum(len(c) for c in parts)

    scored: list[tuple[int, str, str, int, tuple[int, ...], int]] = []
    for members in parts:
        share = max(
            MIN_LANDMARKS_PER_COMPONENT,
            round(landmark_count * len(members) / total),
        )
        chosen, sweeps = landmarks(graph, members, min(share, len(members)), tree)
        if not chosen:
            continue
        vectors = _vectors(chosen, sweeps, members)
        for node in members:
            if not _usable(tree.people[node].display_name or ""):
                continue
            vector = vectors[node]
            best = max(range(len(chosen)), key=lambda i: vector[i])
            if vector[best] <= 0:
                continue
            scored.append(
                (vector[best], node, chosen[best], len(members), vector, id(members))
            )

    if not scored:
        return []

    # Rank by remoteness, then by ID so a tie is settled the same way every run.
    scored.sort(key=lambda row: (-row[0], int(row[1])))
    separation = max(MIN_SEPARATION, int(scored[0][0] * SEPARATION_SHARE))

    kept: list[RemotePerson] = []
    keep_vectors: list[tuple[int, tuple[int, ...]]] = []
    spoken_for: set[str] = set()
    suppressed = 0
    for remoteness, node, partner, size, vector, part in scored:
        if len(kept) >= count:
            break
        # Somebody already named in a row, at either end. Without this the
        # second row is the first one backwards: A's furthest person is B, so
        # B's furthest person is A, and the two most remote people in the tree
        # are always the same pair twice.
        if node in spoken_for:
            suppressed += 1
            continue
        # Same component: the vectors are comparable and a gap proves distance.
        # Different components: no walk connects them at all, so keep.
        if any(
            other_part == part
            and max(abs(a - b) for a, b in zip(vector, other_vector)) < separation
            for other_part, other_vector in keep_vectors
        ):
            suppressed += 1
            continue
        spoken_for.add(node)
        spoken_for.add(partner)
        kept.append(
            RemotePerson(
                geni_id=node,
                name=tree.people[node].display_name or node,
                remoteness=remoteness,
                partner_id=partner,
                partner_name=tree.people[partner].display_name or partner,
                component_size=size,
            )
        )
        keep_vectors.append((part, vector))

    # Never a silent cap: the report states how many candidates were folded
    # away, so a short table reads as "the graph has few distinct corners"
    # rather than "the measurement found little".
    most_remote.suppressed = suppressed
    most_remote.considered = len(scored)
    most_remote.separation = separation
    most_remote.landmarks_placed = sum(
        min(
            max(MIN_LANDMARKS_PER_COMPONENT, round(landmark_count * len(c) / total)),
            len(c),
        )
        for c in parts
    )
    return kept


_LEDE = (
    "Every row is a person our tree can only reach the long way round, and the "
    "partner beside them is the person they are furthest from. **Geni very "
    "likely connects the two by a much shorter chain**, and the people on that "
    "chain are ones we do not hold — so each row is a prediction that a "
    "community is missing, and saving the path page is how to test it."
)

_METHOD = (
    "Ranked by eccentricity — how far each person is from the person they are "
    "furthest from — approximated by placing landmarks with farthest-point "
    "sampling and taking the largest distance to one. A landmark is a real "
    "person, so the number is never an overestimate. Rows are then filtered so "
    "that any two differ by at least the separation below in their distances to "
    "some landmark, which *proves* they are that far apart and stops the list "
    "being one deep lineage repeated. Hops cross parent/child and spouse edges "
    "alike; redacted `Private` profiles are skipped, since the point is to open "
    "both people on Geni."
)


def render_markdown(people: list[RemotePerson], tree_size: int) -> str:
    lines = [
        "# Most remote people — ranked",
        "",
        "Generated by `genimerge.remote` — re-run `python -m genimerge remote`.",
        "",
        _LEDE,
        "",
        f"Measured over {tree_size:,} people.",
        "",
    ]
    if not people:
        lines += ["No one to report — the graph is empty or entirely redacted.", ""]
        return "\n".join(lines) + "\n"

    lines += [
        "| # | hops | the remote person | furthest from | path |",
        "| ---: | ---: | --- | --- | --- |",
    ]
    for i, p in enumerate(people, 1):
        lines.append(
            f"| {i} | {p.remoteness} | [{p.name}]({p.url}) `{p.geni_id}` "
            f"| [{p.partner_name}]({p.partner_url}) `{p.partner_id}` "
            f"| [blood]({p.path_url('blood')}) · [in-law]({p.path_url('inlaw')}) |"
        )

    separation = getattr(most_remote, "separation", None)
    lines += ["", "## How this was measured", "", _METHOD, ""]
    if separation is not None:
        lines += [
            f"Separation for this run: **{separation} hops**, from "
            f"**{getattr(most_remote, 'landmarks_placed', '?')}** landmarks. "
            f"**{getattr(most_remote, 'suppressed', '?')}** further candidates "
            f"were folded into a row already listed — that is the report "
            f"working, not a cap: they are near neighbours of someone above, or "
            f"the mirror image of a row already given.",
            "",
        ]
    return "\n".join(lines) + "\n"


def render_html(people: list[RemotePerson], tree_size: int) -> str:
    """A page to work through, one person at a time."""
    import html as _html

    rows = "\n".join(
        f"<tr><td class=num>{i}</td><td class=num>{p.remoteness}</td>"
        f'<td><a href="{p.url}" target="_blank">{_html.escape(p.name)}</a>'
        f"<br><code>{p.geni_id}</code></td>"
        f'<td><a href="{p.partner_url}" target="_blank">{_html.escape(p.partner_name)}</a>'
        f"<br><code>{p.partner_id}</code></td>"
        f'<td><a href="{p.path_url("blood")}" target="_blank">blood</a><br>'
        f'<a href="{p.path_url("inlaw")}" target="_blank">in-law</a></td></tr>'
        for i, p in enumerate(people, 1)
    )
    lede = _LEDE.replace("**", "")
    separation = getattr(most_remote, "separation", None)
    note = f"Measured over {tree_size:,} people. {_METHOD}".replace("**", "").replace(
        "`Private`", "Private"
    )
    if separation is not None:
        note += f" Separation for this run: {separation} hops."
    return (
        "<!doctype html><html><head><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        "<title>Most remote people</title><style>"
        ":root{color-scheme:light dark;--bg:#fff;--fg:#1a1a1a;--line:#d8d8d8;"
        "--muted:#666;--link:#0b5cad}"
        "@media(prefers-color-scheme:dark){:root{--bg:#15171a;--fg:#e8e8e8;"
        "--line:#33383e;--muted:#9aa0a6;--link:#79b8ff}}"
        "body{margin:0 auto;padding:2rem 1.25rem 4rem;max-width:1000px;background:var(--bg);"
        "color:var(--fg);font:16px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}"
        "h1{font-size:1.5rem;margin:0 0 .5rem}p{margin:.2rem 0 1rem}"
        ".note{color:var(--muted);font-size:.9rem}"
        "table{border-collapse:collapse;width:100%;font-size:.94rem}"
        "th,td{text-align:left;padding:.5rem .6rem;border-bottom:1px solid var(--line);"
        "vertical-align:top}"
        "th{font-size:.8rem;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}"
        "td.num{text-align:right;font-variant-numeric:tabular-nums}"
        "code{font:12px ui-monospace,Menlo,monospace;color:var(--muted)}"
        "a{color:var(--link);text-decoration:none;font-weight:600}a:hover{text-decoration:underline}"
        "</style></head><body>"
        "<h1>Most remote people — ranked</h1>"
        f"<p>{lede}</p>"
        f"<p class=note>{note}</p>"
        "<table><thead><tr><th>#</th><th>hops<br>in our tree</th>"
        "<th>the remote person</th><th>furthest from</th><th>open path</th>"
        "</tr></thead><tbody>"
        f"{rows}</tbody></table></body></html>"
    )
