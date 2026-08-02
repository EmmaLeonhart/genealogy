"""Which profiles to export from next, modelled on what a Geni export is.

A Geni GEDCOM export is a **breadth-first ball**: pick a profile, pick a style
— ancestors, descendants, blood relatives, everything — and Geni walks outward
from that profile until the export is full, at somewhere around 3840 people.
See :data:`GENI_EXPORT_CAP` for why that bound is written as "around" and not
as a number we know. So the question "who do I export from next?" is really
"whose ball would contain the most material we do not already have?".

:mod:`genimerge.frontier` answers a different question. It ranks parentless
people by the descendant count *already in our data*, which measures the known
tree rather than the unknown one, and it has no notion of two candidates
sharing a neighbourhood — its top forty can all hang off the same branch, which
would spend forty exports on one region.

What this module measures instead:

- **Openness.** Within a candidate's ball, how many people have no parents
  recorded. Each of those is a doorway: Geni knows who their parents are and we
  do not. A ball packed with doorways is worth walking through; a ball with
  almost none is a region already recorded several layers deep, and exporting
  from its middle re-fetches what we have.
- **Non-overlap.** Two candidates three hops apart have nearly the same ball,
  so ranking alone hands back one neighbourhood repeatedly.
  :func:`choose_export_set` picks greedily on *newly covered* doorways, which
  is what makes k picks into k useful exports.

**Openness counts doorways, not what is behind them.** We cannot know how many
people sit above a parentless person — not knowing is precisely why they are
worth exporting from. Nothing here predicts how many individuals an export
returns, and the report says so.

**Why doorways are parentless people and not childless ones.** A missing parent
is evidence of missing data: everyone had two. A missing child is not — most
people who appear as leaves really were leaves. Counting childlessness as a
doorway would rank every leaf in the tree as an opportunity.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from .frontier import _child_map, _parent_map, family_graph
from .model import Tree

__all__ = [
    "EXPORT_FROM_THE_PARENT",
    "RANKING_IS_UNVALIDATED",
    "GENI_EXPORT_CAP",
    "STYLES",
    "Ball",
    "SeedProfile",
    "Pick",
    "edges_for_style",
    "export_ball",
    "profile_seed",
    "rank_seeds",
    "choose_export_set",
    "render_markdown",
]

#: Individuals to model one Geni export as holding: **the largest export we have
#: actually seen**, not a cap we know Geni enforces.
#:
#: The distinction is not pedantry, because the obvious reading was wrong. The
#: first three exports each held exactly 3836, and since they are three
#: different styles of one seed that reach largely different people — they share
#: only 354 — three separate walks stopping on the same number read as a hard
#: cap. The fourth export holds **3840**, so it is not one.
#:
#: What actually bounds an export is **not established**. Candidates that fit
#: the evidence equally well: Geni raised the limit between 2026-07-30 and
#: 2026-08-01; the limit is per-account and the account changed; the limit is on
#: something other than individual count (bytes, families, requests) that merely
#: lands near 3836; or the walk overshoots a floor by however much it takes to
#: finish the generation it is on. Four exports cannot separate these, so none
#: is encoded here.
#:
#: Used only to bound the modelled ball in :func:`export_ball`, where being off
#: by a few people out of ~3840 does not move a ranking.
#: ``tests/test_seeds.py`` asserts this stays >= the largest export in
#: ``data_lake/``, so the next export to exceed it fails loudly instead of
#: silently modelling a ball that is too small.
GENI_EXPORT_CAP = 3840

#: The step between reading this report and running an export.
#:
#: Load-bearing, and learned the hard way. The people listed below are
#: *doorways* — they are in our data and their parents are not. Exporting from a
#: doorway centres Geni's walk on somebody we already hold, so a large part of
#: the ball comes back as material we have. Centring it one step further out, on
#: the parent we do not hold, is what the one export with measured results
#: actually did, and it returned 95% new people.
#:
#: A constant for the same reason as
#: :data:`genimerge.quickstatements.NOT_AN_ERROR_RATE`: a test asserts it
#: reaches the report, and a copy of the sentence in the test would break on any
#: rewording.
EXPORT_FROM_THE_PARENT = (
    "**Export from the parent, not from the person listed.** Every profile "
    "below is a *doorway*: we hold them, and we do not hold their parents. "
    "Open the profile on Geni, go **up** to the parent Geni knows and we do "
    "not, and export from there. Exporting from the doorway itself centres the "
    "walk on somebody already in our data, so much of the ball returns as "
    "material we hold; centring one step beyond the frontier is what made the "
    "2026-08-01 export 95% new. The listed person is the signpost, not the "
    "destination."
)

#: What the one measured export says about this ranking, which is not much and
#: not flattering. Kept in the report so the numbers above are not read as more
#: validated than they are.
RANKING_IS_UNVALIDATED = (
    "**No export has yet been taken from a seed this ranking chose, so none of "
    "it is validated.** The one export with measured results — 2026-08-01, 3656 "
    "new people — was seeded on the parent of Hågen Iversen "
    "`6000000019312592888`, who placed **2255 of 2336** here, on a ball of 5 "
    "with a single doorway. That is a reason for doubt rather than a verdict: "
    "the ranking never scored the actual seed, because he was not in our data "
    "to score, and no rival seed was tried against him. But the mechanism is "
    "worth stating, because ranking by *absolute* doorway count favours large "
    "balls, and a large ball is a densely recorded neighbourhood — which is the "
    "opposite of where Geni has most to add. A sparse corner scores near zero "
    "precisely because we know little there. One data point is not enough to "
    "re-rank on, and it is not being re-ranked on; it is enough to say the list "
    "below is a hypothesis."
)

#: Export shapes Geni offers, as edge sets over our data.
STYLES = ("blood", "all", "ancestors", "descendants")

#: Hops used when screening candidates. Deep enough to see whether a
#: neighbourhood is recorded "several layers" out, cheap enough to run over
#: every candidate.
SCREEN_RADIUS = 3

#: A ball with a smaller share of doorways than this is saturated — the region
#: is already recorded, and an export seeded in it would mostly return people
#: we hold. Deliberately low: the point is to reject the clearly-pointless, not
#: to fine-tune a ranking that is a proxy in the first place.
SATURATED_BELOW = 0.05


@dataclass(frozen=True)
class Ball:
    """The people a breadth-first export from ``seed`` would reach."""

    seed: str
    #: reached in breadth-first order, seed first
    reached: list[str]
    #: hop distance from the seed, per person
    hop: dict[str, int]
    #: True if the export cap stopped the walk before the ball was exhausted
    capped: bool
    #: the largest hop actually walked
    depth: int

    @property
    def size(self) -> int:
        return len(self.reached)


@dataclass(frozen=True)
class SeedProfile:
    """A candidate export seed, and what its ball is made of."""

    seed: str
    ball: Ball
    #: people in the ball with no parents recorded — the doorways
    doorways: frozenset[str]

    @property
    def size(self) -> int:
        return self.ball.size

    @property
    def open_count(self) -> int:
        return len(self.doorways)

    @property
    def openness(self) -> float:
        return self.open_count / self.size if self.size else 0.0

    @property
    def saturated(self) -> bool:
        """Everything around this seed is already recorded several layers out."""
        return self.openness < SATURATED_BELOW


@dataclass
class Pick:
    """One export in a planned sequence, and what it adds over its predecessors."""

    profile: SeedProfile
    #: doorways this pick covers that no earlier pick covered
    fresh: frozenset[str] = field(default_factory=frozenset)

    @property
    def fresh_count(self) -> int:
        return len(self.fresh)


def edges_for_style(tree: Tree, style: str, *, graph: dict[str, list[str]] | None = None):
    """The adjacency a given export style walks.

    ``blood`` and ``all`` are the undirected family graph — the distinction
    Geni draws between them is about *whose* profiles are included, not about
    which links are followed, and our data cannot tell the two apart.
    ``ancestors`` walks parent links only, ``descendants`` child links only.
    """
    if style not in STYLES:
        raise ValueError(f"unknown export style {style!r}; expected one of {STYLES}")
    if style in ("blood", "all"):
        return family_graph(tree) if graph is None else graph
    if style == "ancestors":
        return _parent_map(tree)
    return _child_map(tree)


def export_ball(
    edges: dict[str, list[str]],
    seed: str,
    *,
    cap: int | None = GENI_EXPORT_CAP,
    radius: int | None = None,
) -> Ball:
    """Breadth-first walk from ``seed``, stopped by ``cap`` or ``radius``.

    The cap is Geni's, and whether it bit matters: a ball that fills before it
    reaches a boundary is an export that never gets to the interesting part.
    """
    reached = [seed]
    hop = {seed: 0}
    queue = deque([seed])
    capped = False

    while queue:
        current = queue.popleft()
        next_hop = hop[current] + 1
        if radius is not None and next_hop > radius:
            continue
        for neighbour in edges.get(current, ()):
            if neighbour in hop:
                continue
            if cap is not None and len(reached) >= cap:
                capped = True
                queue.clear()
                break
            hop[neighbour] = next_hop
            reached.append(neighbour)
            queue.append(neighbour)

    return Ball(
        seed=seed,
        reached=reached,
        hop=hop,
        capped=capped,
        depth=max(hop.values()) if hop else 0,
    )


def profile_seed(
    tree: Tree,
    seed: str,
    edges: dict[str, list[str]],
    *,
    cap: int | None = GENI_EXPORT_CAP,
    radius: int | None = None,
) -> SeedProfile:
    """Walk one seed's ball and count the doorways in it."""
    ball = export_ball(edges, seed, cap=cap, radius=radius)
    doorways = frozenset(
        person_id
        for person_id in ball.reached
        if person_id in tree.people and not tree.people[person_id].has_known_parents
    )
    return SeedProfile(seed=seed, ball=ball, doorways=doorways)


def rank_seeds(
    tree: Tree,
    *,
    style: str = "blood",
    radius: int = SCREEN_RADIUS,
    limit: int | None = None,
    edges: dict[str, list[str]] | None = None,
) -> tuple[list[SeedProfile], list[SeedProfile]]:
    """Score every parentless person as an export seed.

    Returns ``(kept, rejected)`` — rejected being the saturated ones, returned
    rather than dropped so the report can say how many candidates were
    discarded and why.

    Candidates are the parentless people only. A seed that is certainly not
    terminal sits inside what we already hold, and walking outward from it
    spends most of the cap before reaching an edge.
    """
    edges = edges_for_style(tree, style) if edges is None else edges

    kept: list[SeedProfile] = []
    rejected: list[SeedProfile] = []
    for geni_id, person in tree.people.items():
        if person.has_known_parents:
            continue
        profile = profile_seed(tree, geni_id, edges, cap=None, radius=radius)
        (rejected if profile.saturated else kept).append(profile)

    kept.sort(key=lambda p: (-p.open_count, -p.openness, p.seed))
    rejected.sort(key=lambda p: (-p.size, p.seed))
    return (kept if limit is None else kept[:limit]), rejected


def choose_export_set(profiles: list[SeedProfile], k: int) -> list[Pick]:
    """Pick ``k`` seeds whose balls overlap as little as possible.

    Greedy on newly-covered doorways. Ranking alone would return one
    neighbourhood over and over, because neighbours share a ball; what matters
    for a *sequence* of exports is what each one adds to the ones before it.

    Stops early when no remaining candidate adds a doorway — returning fewer
    picks than asked for is the correct answer when the candidates are
    exhausted, and padding the list with redundant seeds would not be.
    """
    covered: set[str] = set()
    picks: list[Pick] = []
    remaining = list(profiles)

    while remaining and len(picks) < k:
        best = max(
            remaining,
            key=lambda p: (len(p.doorways - covered), p.open_count, -_ordinal(p.seed)),
        )
        fresh = best.doorways - covered
        if not fresh:
            break
        picks.append(Pick(profile=best, fresh=frozenset(fresh)))
        covered |= fresh
        remaining.remove(best)

    return picks


def _ordinal(geni_id: str) -> int:
    """Tie-break key that is stable across runs and independent of dict order."""
    return int(geni_id) if geni_id.isdigit() else 0


def render_markdown(
    tree: Tree,
    *,
    style: str = "blood",
    radius: int = SCREEN_RADIUS,
    exports: int = 10,
    top: int = 40,
) -> str:
    """The report: what to export next, in what order, and what it cannot tell you."""
    kept, rejected = rank_seeds(tree, style=style, radius=radius)
    picks = choose_export_set(kept, exports)
    edges = edges_for_style(tree, style)
    parentless = sum(1 for p in tree.people.values() if not p.has_known_parents)

    lines = [
        "# Export seeds",
        "",
        "Generated by `genimerge.seeds` — re-run `python -m genimerge seeds`.",
        "",
        "A Geni export is a **breadth-first ball**: one profile, one style, and "
        f"Geni walks outward until the export is full, modelled here at "
        f"{GENI_EXPORT_CAP} individuals. "
        "So the useful question is not who has the biggest subtree in our data — "
        "that is what we already hold — but whose ball would contain the most of "
        "what we do not.",
        "",
        "**Doorways** are people in a ball with no parents recorded. Each is a "
        "place Geni can walk further than we can. **Openness** is their share of "
        "the ball.",
        "",
        f"Screened over a {radius}-hop ball in the `{style}` style.",
        "",
        "## Candidates",
        "",
    ]
    lines += _table(
        ["", "count"],
        [
            ["people in the tree", str(len(tree.people))],
            ["with no parents recorded — the candidates", str(parentless)],
            ["kept", str(len(kept))],
            [f"rejected as saturated (openness < {SATURATED_BELOW:.0%})", str(len(rejected))],
        ],
    )

    lines += [
        "",
        "Saturation rejects the seeds sitting inside a region already recorded "
        "several layers out, where an export would mostly return people we hold. "
        "It fires rarely, and that is worth saying rather than tuning: ranking by "
        "doorway count already keeps interior candidates away from the top, so "
        "the rejection is a floor under the list, not the thing that shapes it.",
        "",
        f"## The next {len(picks)} exports",
        "",
        "Chosen greedily on **newly covered** doorways, not by rank. Neighbours "
        "share a ball, so a ranked list hands back one neighbourhood repeatedly; "
        "what matters across a sequence of exports is what each one adds to the "
        "ones before it. `adds` counts doorways no earlier pick had.",
        "",
        EXPORT_FROM_THE_PARENT,
        "",
    ]
    running = 0
    rows = []
    for i, pick in enumerate(picks, 1):
        person = tree.people[pick.profile.seed]
        running += pick.fresh_count
        rows.append(
            [
                str(i),
                f"[{person.display_name}]({person.url})",
                f"`{pick.profile.seed}`",
                str(pick.profile.size),
                str(pick.profile.open_count),
                f"{pick.profile.openness:.0%}",
                str(pick.fresh_count),
                str(running),
            ]
        )
    lines += _table(
        ["#", "profile", "geni id", "ball", "doorways", "openness", "adds", "running"],
        rows,
    )

    if picks:
        naive: set[str] = set()
        for profile in kept[: len(picks)]:
            naive |= profile.doorways
        lines += [
            "",
            f"Those {len(picks)} picks reach **{running}** distinct doorways. The "
            f"{len(picks)} highest-ranked seeds, taken without regard to overlap, "
            f"reach **{len(naive)}** between them.",
        ]

        full = export_ball(edges, picks[0].profile.seed, cap=GENI_EXPORT_CAP)
        lines += [
            "",
            "## What the size limit does",
            "",
            f"Walking the top seed as far as Geni would take it reaches "
            f"**{full.size}** people already in our data"
            + (
                f", filling the export at hop {full.depth}."
                if full.capped
                else f", exhausting its component at hop {full.depth} without filling the export."
            ),
            "",
            "That number is not a prediction of waste. Geni's graph holds our "
            "people *and* the ones we are missing, and its walk reaches both at "
            "each hop — so a full export is a mix, and the doorway density near "
            "the seed is the best available proxy for how rich that mix is.",
            "",
            f"The {GENI_EXPORT_CAP} used above is **the largest export we have "
            "seen, not a limit we know Geni enforces**. Three exports held "
            "exactly 3836, which read as a hard cap until a fourth held 3840. "
            "What actually bounds an export is unestablished — a raised limit, "
            "a per-account limit, a limit on something other than head count, "
            "or a walk that overshoots a floor all fit the four exports we "
            "have. Being off by a few people out of ~3840 does not move this "
            "ranking, so the uncertainty is recorded rather than resolved by "
            "guessing.",
        ]

    lines += ["", "## How well this ranking has actually done", "", RANKING_IS_UNVALIDATED]

    lines += [
        "",
        f"## Ranked candidates (top {top})",
        "",
        "By doorways in the screening ball. Useful for picking a seed by hand; "
        "the sequence above is what to actually export, because these overlap.",
        "",
    ]
    lines += _table(
        ["profile", "geni id", "ball", "doorways", "openness"],
        [
            [
                f"[{tree.people[p.seed].display_name}]({tree.people[p.seed].url})",
                f"`{p.seed}`",
                str(p.size),
                str(p.open_count),
                f"{p.openness:.0%}",
            ]
            for p in kept[:top]
        ],
    )

    lines += [
        "",
        "## What this cannot tell you",
        "",
        "Doorways count what an export can reach, never what is behind them. "
        "Nobody knows how many people sit above a parentless person — not knowing "
        "is the whole reason to export from them — so nothing here predicts how "
        "many new individuals an export returns. A seed with 25 doorways is a "
        "better bet than one with 3; it is not a promise of eight times the "
        "material.",
        "",
        "Openness is also measured over *our* graph. A region Geni records "
        "thinly looks identical to one it records richly, until the export lands.",
    ]

    return "\n".join(lines) + "\n"


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    sep = ["---", *["---:"] * (len(header) - 1)]
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
        *["| " + " | ".join(row) + " |" for row in rows],
    ]
