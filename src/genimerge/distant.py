"""Pairs of people who are far apart *in our tree* — candidates to ask Geni about.

**The idea is Emma's and it inverts how the other reports work.**
`frontier` and `density` look for where our data stops or thins, and propose an
export there. This looks for two people our data connects only by a very long
walk, on the reasoning that **Geni probably connects them by a much shorter
one** — and the people on that shorter route are, by construction, ones we do
not have. A large in-tree distance between two people is therefore a *prediction
that a community is missing*, and the Geni relationship path between them is
what tests it.

**Why this can find things the density report cannot.** Density measures how
often our exports covered a neighbourhood; it can only ever talk about places we
have already been. This measures a shape our data has — a long thin detour —
that is evidence about a place we have *not* been. It is also the only report
here whose output is a question for Geni rather than an answer from us.

**Distance is in hops, not generations.** The graph is parent/child *and*
spouse edges undirected, so a "hop" crosses a marriage as readily as a birth.
That is deliberate: a route through an in-law is exactly the kind of connection
a `Forest` export finds and a `BloodTree` one misses.

**The diameter is approximated, not computed.** Exact eccentricity on a
190k-node graph is a BFS per node. This uses the standard double sweep — BFS
from an arbitrary node to find a far endpoint, BFS again from there — which is
cheap and, on tree-like graphs, usually finds an endpoint of a true longest
path. It is a heuristic for *finding good candidates*, and nothing downstream
depends on the number being the exact diameter.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path

from .frontier import family_graph
from .identity import profile_url
from .model import Tree

__all__ = ["DistantPair", "bfs", "far_pairs", "render_markdown", "render_html"]

#: Names that identify nobody. A pair is only useful if Emma can recognise and
#: find the two people on Geni, and `Private` is Geni's redaction of a living
#: person — the profile exists but the page will not show a path.
_UNUSABLE = {"", "private", "n n", "nn", "?", "unknown"}

#: A pair below this share of the widest one is not evidence of anything: the
#: greedy search tails off, and two people five hops apart are near relatives.
MIN_SHARE_OF_WIDEST = 0.4

#: ...and an absolute floor, so a small or shallow tree cannot report a
#: three-hop pair merely because it is the widest one there.
MIN_HOPS = 12


def _usable(name: str) -> bool:
    return name.strip().lower().strip("<>") not in _UNUSABLE


@dataclass(frozen=True)
class DistantPair:
    a: str
    b: str
    a_name: str
    b_name: str
    distance: int

    @property
    def a_url(self) -> str:
        return profile_url(self.a)

    @property
    def b_url(self) -> str:
        return profile_url(self.b)


def bfs(graph: dict[str, list[str]], start: str) -> dict[str, int]:
    """Hop distance from `start` to everything reachable."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        step = dist[current] + 1
        for neighbour in graph.get(current, ()):
            if neighbour not in dist:
                dist[neighbour] = step
                queue.append(neighbour)
    return dist


def _farthest(
    dist: dict[str, int],
    tree: Tree,
    prefer_named: bool = True,
    exclude: set[str] | None = None,
) -> str:
    """The most distant node, preferring one a human can look up.

    A redacted `Private` profile is a dead end for the purpose this serves: the
    point is to open the pair on Geni and read the path between them.

    `exclude` skips people already spoken for. Choosing the farthest *available*
    node keeps every person in at most one pair without throwing away the sweep
    that found them — the alternative, discarding the pair and moving on, pays
    for a BFS over every person and gets nothing for it.
    """
    exclude = exclude or set()
    best_named = best_any = None
    for node, d in dist.items():
        if node in exclude:
            continue
        if best_any is None or d > dist[best_any]:
            best_any = node
        if prefer_named and _usable(tree.people[node].display_name or ""):
            if best_named is None or d > dist[best_named]:
                best_named = node
    return best_named or best_any or ""


def far_pairs(tree: Tree, count: int = 10, graph=None) -> list[DistantPair]:
    """`count` pairs that are far apart, spread around the graph.

    One double sweep gives a single long path, and its two endpoints are one
    pair. Taking the next `count` pairs from the *same* sweep would return
    near-neighbours of the same endpoint — ten names off one branch, the
    mistake `seeds` explicitly avoids. So each pair is seeded from a different
    far-flung node and swept independently.
    """
    graph = graph if graph is not None else family_graph(tree)
    if not graph:
        return []

    start = min(graph, key=int)
    first = bfs(graph, start)
    anchor = _farthest(first, tree)
    spread = bfs(graph, anchor)

    # Candidate seeds: the farthest nodes from the anchor, which sit around the
    # rim rather than in one direction from it.
    rim = sorted(
        (n for n in spread if _usable(tree.people[n].display_name or "")),
        key=lambda n: -spread[n],
    )

    pairs: list[DistantPair] = []
    used: set[str] = set()
    for seed in rim:
        if len(pairs) >= count:
            break
        if seed in used:
            continue
        dist = bfs(graph, seed)
        other = _farthest(dist, tree, exclude=used)
        if not other or other == seed:
            continue
        pairs.append(
            DistantPair(
                a=seed,
                b=other,
                a_name=tree.people[seed].display_name or seed,
                b_name=tree.people[other].display_name or other,
                distance=dist[other],
            )
        )
        # Retire this seed's whole neighbourhood, not just the two endpoints.
        #
        # Without this the next rim candidate is a *neighbour* of the seed just
        # used — the rim is sorted by distance from one anchor, so its top
        # entries are all in the same corner — and it resolves to the same far
        # endpoint. That costs a full BFS over every person to discover a pair
        # already found. On a 190k-person tree it was the difference between
        # ten sweeps and hundreds: the first real run was killed after 21
        # minutes of CPU without producing a row.
        #
        # Both ends are retired, not just the seed's. Retiring only the seed
        # gave twelve pairs with twelve different seeds and *ten* whose far end
        # was a different member of the same Chinese lineage: that clan is the
        # graph's deepest branch, so it wins "farthest from here" from almost
        # anywhere. Distances from the seed cannot say which nodes are near
        # `other`, but everything in the outermost shell is, near enough.
        #
        # The radius scales with the pair, so "a different corner" means
        # something proportional to how wide the graph is rather than a
        # constant that would be wrong at either size.
        radius = max(2, dist[other] // 6)
        far = dist[other] - radius
        used.update(node for node, d in dist.items() if d <= radius or d >= far)
        used.add(other)
    pairs.sort(key=lambda p: -p.distance)

    # Drop pairs that are not actually distant.
    #
    # Greedy retirement shrinks the pool it draws from, so the run tails off:
    # a first pass gave 311, 173, 120, 76, 49, 33, 18, 10, 8 and 5 hops. A
    # five-hop pair is two people who are nearly related, and listing it under
    # "distant pairs" would invite exactly the wrong export. The floor is
    # relative because the graph's width is not known in advance.
    if pairs:
        floor = max(MIN_HOPS, int(pairs[0].distance * MIN_SHARE_OF_WIDEST))
        kept = [p for p in pairs if p.distance >= floor]
        dropped = len(pairs) - len(kept)
        if dropped:
            # Never a silent cap: the caller reports this.
            far_pairs.dropped_as_too_close = dropped
            far_pairs.floor = floor
        pairs = kept
    return pairs


_LEDE = (
    "Each row is two people our tree connects only by a long walk. **Geni very "
    "likely connects them by a shorter one**, and the people on that shorter "
    "route are ones we do not hold — so the relationship path between a pair is "
    "a prediction about a community missing from our data, and saving that page "
    "is how to test it."
)

_METHOD = (
    "Distance is hops over parent/child *and* spouse edges, undirected, so a hop "
    "crosses a marriage as readily as a birth. The endpoints come from an "
    "approximate diameter (double-sweep BFS) with each pair seeded from a "
    "different far node, so these are ten different corners rather than ten "
    "names off one branch. Redacted `Private` profiles are skipped: the point is "
    "to open both people on Geni and read the path."
)


def render_markdown(pairs: list[DistantPair], tree_size: int) -> str:
    lines = [
        "# Distant pairs — where to ask Geni for a path",
        "",
        "Generated by `genimerge.distant` — re-run `python -m genimerge distant`.",
        "",
        _LEDE,
        "",
        f"Measured over {tree_size:,} people.",
        "",
    ]
    if not pairs:
        lines += ["No pairs found — the graph is empty or entirely redacted.", ""]
        return "\n".join(lines) + "\n"

    lines += [
        "| # | hops | one end | the other end |",
        "| ---: | ---: | --- | --- |",
    ]
    for i, p in enumerate(pairs, 1):
        lines.append(
            f"| {i} | {p.distance} | [{p.a_name}]({p.a_url}) | [{p.b_name}]({p.b_url}) |"
        )
    lines += ["", "## How this was measured", "", _METHOD, ""]
    return "\n".join(lines) + "\n"


def render_html(pairs: list[DistantPair], tree_size: int) -> str:
    """A page to open and work through, one pair at a time."""
    import html as _html

    rows = "\n".join(
        f"<tr><td class=num>{i}</td><td class=num>{p.distance}</td>"
        f'<td><a href="{p.a_url}" target="_blank">{_html.escape(p.a_name)}</a>'
        f"<br><code>{p.a}</code></td>"
        f'<td><a href="{p.b_url}" target="_blank">{_html.escape(p.b_name)}</a>'
        f"<br><code>{p.b}</code></td></tr>"
        for i, p in enumerate(pairs, 1)
    )
    lede = _LEDE.replace("**", "")
    return (
        "<!doctype html><html><head><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        "<title>Distant pairs</title><style>"
        ":root{color-scheme:light dark;--bg:#fff;--fg:#1a1a1a;--line:#d8d8d8;"
        "--muted:#666;--link:#0b5cad}"
        "@media(prefers-color-scheme:dark){:root{--bg:#15171a;--fg:#e8e8e8;"
        "--line:#33383e;--muted:#9aa0a6;--link:#79b8ff}}"
        "body{margin:0 auto;padding:2rem 1.25rem 4rem;max-width:900px;background:var(--bg);"
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
        "<h1>Distant pairs — where to ask Geni for a path</h1>"
        f"<p>{lede}</p>"
        f"<p class=note>Measured over {tree_size:,} people. {_METHOD}</p>"
        "<table><thead><tr><th>#</th><th>hops<br>in our tree</th><th>one end</th>"
        "<th>the other end</th></tr></thead><tbody>"
        f"{rows}</tbody></table></body></html>"
    )
