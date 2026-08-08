"""Lines that stop early: who to export from to reach modern times.

`genimerge.frontier` ranks **parentless** people — the upward edge, where Geni
knows an ancestor we do not. `genimerge.density` ranks neighbourhoods **few
exports touched**, which knows nothing about when anyone lived. Neither answers
the question behind the `Descendants` campaign, which is Emma's and is about
time rather than thinness: *the tree is biased towards ancient and medieval
people, and the goal is to reach the present.*

This module ranks the **downward** edge, and it buckets by when people lived so
that the ranking can be read one period at a time.

**The signal is a small but nonzero count of descent paths.** Nonzero and small
are doing different jobs and both are load-bearing:

- **Nonzero** means the line demonstrably continues. Geni recorded at least one
  child, so there is something below to follow, and an export seeded here is not
  a bet on a childless couple.
- **Small** means we have barely followed it. A person with three recorded
  descent paths either had three, or had three hundred and we walked one step.

A person with *zero* recorded descendants is the ambiguous case and is left out
of the candidate list on purpose: they may be a genuine leaf, and nothing in our
data separates "childless" from "unexplored". That is the same discriminator
`density` uses upward, where a thin region full of parentless people is
under-sampled and a thin region with none may simply be finished.

**Descent paths, not distinct people — Emma's call, 2026-08-07.** The measure is
her recursion: a person's count is, over each recorded child, *one for the child
plus the child's own count*. Someone reachable down two lines is therefore
counted twice, and that is the point rather than a defect to correct. What this
report is looking for is **lines coming down from a person**, and a descendant
reached twice is two lines. Distinct-person counting was the first
implementation and she ruled it out as not merely irrelevant here but plausibly
worse: pedigree collapse is dense in this tree, and de-duplicating it makes a
person at the top of a wide, repeatedly-intermarried descent look like a narrow
one. :func:`genimerge.frontier.descendant_counts` still counts distinct people
for callers that want that.

The change also made this module cheap. Distinct counting needs a set union per
person, which does not scale at 257219 people — it wanted a bitmask per person
(32 KB each, tens of gigabytes) or a walk abandoned above a cap. This module
carried that capped walk, a ``CAP`` constant, a ``--cap`` flag and a
``descendants_exact`` flag purely to work around it; Emma's recursion is a plain
post-order sum, O(V+E), exact at every size, and deleted all of them.

**`stall` is the measure that serves the campaign.** For each person it is the
number of years between the latest birth recorded anywhere at or below them and
the present. A person born in 1400 whose line reaches 1430 and stops has been
walked one generation; a person born in 1400 whose line reaches 1890 has been
followed for fifteen. Both look identical to a *count* if the second one's line
is narrow. Stall separates them, and it is what makes a ranking
inside a birth-year band mean "least followed" rather than "oldest".

**Two axes, because neither covers everyone.** People are bucketed by recorded
birth year where there is one, and by :func:`genimerge.frontier.ancestor_depth`
— generations of recorded ancestors above them — where there is not. The
generation axis is not a better clock and is not offered as one: it measures our
own sampling upward, so a person whose ancestry we have not traced looks recent
when they are not. It is here because a large part of this tree carries no date
at all, and those people are invisible to the time axis entirely.

**Nothing here is inferred from a name or a place, and no date is guessed.** A
person with no recorded birth year has no birth year in this module; they are
counted in an `undated` bucket that the report prints rather than hides.

**What this cannot tell you** is the same limit `density` has. Our path count
measures *our* sampling. Whether Geni holds a large descent below a stalled line
is precisely the unknown an export resolves — a line can also stop because it
really did stop, and the `open paths` column is the check: a stalled line whose
paths end at several different childless people has several places to carry on
from, while one ending in a single person may just have ended.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from math import log

from .frontier import _child_map, _parent_map, _post_order, ancestor_depth
from .seeds import GENI_EXPORT_CAP
from .identity import profile_url
from .model import Tree

#: Who each person's recorded parents are, for :func:`candidates` to drop a
#: candidate sitting inside another one's line. Re-exported rather than left as
#: `frontier`'s private helper so callers passing ``parents=`` have somewhere
#: public to get it from.
parent_map = _parent_map

__all__ = [
    "Line",
    "Band",
    "parent_map",
    "present_year",
    "line_reach",
    "descendant_depth",
    "descent_paths",
    "build_lines",
    "candidates",
    "band_by_birth",
    "band_by_generation",
    "bands",
    "REACH_TARGET",
    "REACH_GENERATIONS",
    "render_markdown",
    "render_seed_list",
]

#: Default ceiling on "small". A line we hold this many people of or fewer is
#: one we have brushed rather than walked. Not a measured threshold — it is the
#: knob the report is meant to be re-run with, which is why it is a CLI flag.
SMALL = 20

#: Where the arithmetic saturates. Path counts are sums over a graph that shares
#: subtrees heavily, so they grow like ``branching ** depth`` and a deep, densely
#: intermarried ancestor can carry a number thousands of digits long. Python
#: would compute it, slowly, and nothing here would use it: every question this
#: module asks is about counts near :data:`SMALL`. So the sums stop at this
#: value, which is a display ceiling and never a candidacy one — it is thirteen
#: orders of magnitude above any usable ``small``.
PATH_CEILING = 10**12

#: Default width of a birth-year band, in years. Wide enough that a band holds
#: enough people to rank within, narrow enough that "born in this band" is a
#: real period rather than "the middle ages".
BAND_YEARS = 100

#: How many generations a `Descendants` export can carry, and how many years a
#: generation is worth.
#:
#: **This is the constraint the 2026-08-07 backtest established, and it outranks
#: every ranking heuristic in this module.** A `Descendants` export is a
#: breadth-first ball with a budget of about
#: :data:`genimerge.seeds.GENI_EXPORT_CAP` people. Breadth-first means it fills
#: generation *k* before starting *k+1*, so the budget goes to the generations
#: nearest the seed — and a descent branching twice per couple reaches 4096
#: people at generation 12 unaided. So a ball carries roughly a dozen
#: generations forward and no choice of seed changes that.
#:
#: Eleven exports seeded on ancient and undated people added 18218 people whose
#: median birth year was 1582 and produced **four** born after 1900. Twelve
#: generations from a seed in 1300 lands around 1660, which is exactly where
#: they landed. See `reports/descendants-backtest-2026-08-07.md`.
#:
#: Both numbers are deliberately round. 30 years per generation is the ordinary
#: demographic figure and the arithmetic is a reachability screen, not a
#: prediction: it exists to rule out seeds that cannot arrive, not to promise
#: that the ones left will.
REACH_GENERATIONS = 12
GENERATION_YEARS = 30

#: The year the campaign is trying to arrive at. 1900 rather than "now" because
#: Geni redacts living people, so the reachable frontier stops well short of the
#: present whatever the budget allows.
REACH_TARGET = 1900


def present_year() -> int:
    """This year. A parameter everywhere it is used, never read at import."""
    return date.today().year


def _has_child(tree: Tree, geni_id: str) -> bool:
    """Whether this person has a child *we hold*.

    A child pointer to a profile no export has reached is not a recorded child
    for the purposes here: we cannot walk to it, so it cannot be part of a line
    we are measuring the length of.
    """
    return any(c in tree.people for c in tree.people[geni_id].child_ids)


def descent_paths(
    tree: Tree, ceiling: int = PATH_CEILING
) -> tuple[dict[str, int], dict[str, int]]:
    """For each person: how many lines of descent run down from them, and how
    many of those end at somebody childless.

    Returns ``(paths, open_paths)``.

    **`paths` is Emma's recursion**, and it is the measure this whole module is
    built on::

        paths(person) = sum over each recorded child c of (1 + paths(c))

    One for the child, plus everything below the child. A descendant reachable
    down two separate lines is therefore counted **twice**, which is deliberate:
    the question is how many lines come down from a person, and a person reached
    twice is two lines. See the module docstring for why distinct-person
    counting was tried first and dropped.

    **`open_paths`** counts the same paths but only those terminating at a
    person with no recorded child — the places a `Descendants` export could
    carry the line on from. A path that ends at somebody who *does* have
    children recorded is a line we have already followed to its end.

    Exact and O(V+E): one post-order, one addition per edge. Nothing here needs
    a set, a bitmask or a counting cap, which is the practical reason the change
    was worth making at 257219 people.

    **Saturating at `ceiling`.** Sums over a graph that shares subtrees compound,
    so a deep and densely intermarried ancestor's true path count can run to
    thousands of digits. It is arithmetic nobody reads and everybody waits for.
    Both counts stop at the ceiling, which is far above any usable ``small``, so
    no candidate is ever affected.

    Cycle-tolerant through :func:`genimerge.frontier._post_order`, which ignores
    an edge back into a node still being expanded — the only sane reading, since
    a person is not their own descendant, and the alternative for a path count
    is a number that is genuinely infinite. A cycle therefore makes these counts
    *low*, not wrong-in-an-unbounded-way, and cycles are already reported by
    :func:`genimerge.frontier.ancestry_cycles`.
    """
    children = _child_map(tree)
    paths: dict[str, int] = {}
    open_paths: dict[str, int] = {}

    for node in _post_order(list(tree.people), children):
        total = 0
        open_total = 0
        for child in children[node]:
            below = paths.get(child, 0)
            total += 1 + below
            # A childless child is one path, ending here. Otherwise the child
            # contributes only the open paths below it — the child itself is not
            # an open end, because we already know who came after them.
            open_total += 1 if not children[child] else open_paths.get(child, 0)
        paths[node] = min(total, ceiling)
        open_paths[node] = min(open_total, ceiling)

    return paths, open_paths


def descendant_depth(tree: Tree) -> dict[str, int]:
    """Longest chain of recorded descendants below each person.

    The mirror of :func:`genimerge.frontier.ancestor_depth`, and cycle-tolerant
    for the same reason: a person entered twice and linked to themselves is
    ordinary in a genealogy database, and a naive walk would not terminate.

    **Anyone with a recorded child has depth at least 1, and getting that wrong
    put a data artefact at the top of the report.** :func:`_post_order` drops an
    edge back into a node still being expanded, which is the right call — a
    person is not their own descendant — but it means a child inside a cycle is
    simply missing from ``depth`` when the parent is processed. Reading that as
    "no known depth" and falling through to ``0`` made a person with twelve
    descent paths indistinguishable from a childless leaf, and since depth is
    this module's primary ranking key **ascending**, every such person sorted
    above every genuine candidate: the top pick of the `undated` band, 136953
    people, was one of them.

    So an unresolved child contributes ``0`` rather than nothing, and the ``1 +``
    is applied whenever there is a child at all. A cycle now makes depth *low*,
    which is a truncated measurement, rather than *zero*, which is a false one.
    :func:`genimerge.frontier.ancestry_cycles` is what actually reports these
    people as the defects they are.
    """
    children = _child_map(tree)
    depth: dict[str, int] = {}

    for node in _post_order(list(tree.people), children):
        kids = children[node]
        depth[node] = 1 + max((depth.get(c, 0) for c in kids), default=0) if kids else 0

    return depth


def line_reach(tree: Tree) -> tuple[dict[str, int | None], dict[str, str]]:
    """How far forward in time each line has been followed, and where it ends.

    Returns ``(reach, tip)``:

    - **reach** — the latest birth year recorded at or below this person, or
      ``None`` when neither they nor anyone below them carries one. This is a
      fact about our data, not an estimate of when the line really ended.
    - **tip** — the childless person at or below them with the latest recorded
      birth, which is the forward edge of the line and the answer to "export
      from them *or near them*". A line whose members are all undated still gets
      a tip, chosen by lowest profile ID so the report is reproducible; a line
      with no childless member at all — which takes a cycle — gets none.

    ``reach`` and ``tip`` are deliberately not the same person. The latest birth
    in a line often belongs to someone who has children recorded, and that
    person is not where the line stops.
    """
    children = _child_map(tree)
    reach: dict[str, int | None] = {}
    tip: dict[str, str] = {}

    for node in _post_order(list(tree.people), children):
        own_birth = tree.people[node].birth_year

        years = [own_birth] if own_birth is not None else []
        years += [reach[c] for c in children[node] if reach.get(c) is not None]
        reach[node] = max(years) if years else None

        # Candidate tips: this person if childless, plus each child's tip.
        # Ranked by birth year, undated last, profile ID to break the tie.
        options: list[str] = []
        if not children[node]:
            options.append(node)
        options += [tip[c] for c in children[node] if c in tip]
        if options:
            tip[node] = min(
                options,
                key=lambda g: (
                    -(tree.people[g].birth_year if tree.people[g].birth_year is not None else -10**9),
                    int(g),
                ),
            )

    return reach, tip


@dataclass(frozen=True)
class Line:
    """One person, and how far their descendant line has been followed."""

    geni_id: str
    name: str
    #: recorded birth year, or None. Never inferred.
    birth: int | None
    #: generations of recorded ancestors above — see the module docstring on why
    #: this is a second axis rather than a substitute clock
    generation: int
    #: lines of descent running down from them — see :func:`descent_paths`.
    #: Not distinct people: somebody reached down two lines counts twice.
    paths: int
    #: children we hold. The branching estimate :meth:`generations_affordable`
    #: needs, and a lower bound on the real figure.
    children: int
    #: longest chain of generations below them
    depth: int
    #: latest birth year recorded at or below them
    reach: int | None
    #: how many of those paths end at somebody with no recorded child — the
    #: places a `Descendants` export could carry the line on from
    open_paths: int
    #: the childless person at the forward edge of the line, to export from or near
    tip: str = ""
    tip_name: str = ""
    tip_birth: int | None = None

    def stall(self, present: int) -> int | None:
        """Years between the last birth recorded in this line and now.

        ``None`` when the line carries no date at all — which is not a stall of
        zero and must not sort like one.

        **Reported, not ranked on.** Stall is ``present - reach`` and ``reach``
        is at least this person's own birth year, so within a band stall is
        mostly a restatement of when they were born: ranking a 100-year band by
        it put someone born in the band's first year at the top of every single
        band, which is an artefact of the band edge and not a finding. What it
        is good for is reading a row — a line stalling 400 years short of now is
        400 years short however it got there.
        """
        return None if self.reach is None else present - self.reach

    @property
    def followed(self) -> int | None:
        """Years of descent traced from this person: ``reach - birth``.

        The date-carrying companion to :attr:`depth`, and ``None`` unless both
        ends are recorded. Unlike :meth:`stall` it does not move with the band,
        because it is measured from the person rather than from now.
        """
        if self.birth is None or self.reach is None:
            return None
        return self.reach - self.birth

    def is_candidate_shape(self, small: int) -> bool:
        """Small but nonzero: the line continues and we have barely followed it.

        Measured on descent paths, so somebody at the top of a densely
        intermarried descent counts every line down to it rather than every
        person — see :func:`descent_paths`.
        """
        return 0 < self.paths <= small

    def generations_affordable(self, budget: int = GENI_EXPORT_CAP) -> int:
        """How many generations a ball seeded here can carry, given how wide
        this person's recorded descent already is.

        A breadth-first ball fills generation *k* before starting *k+1*, so a
        descent branching `b` times per couple costs ``b ** k`` to reach
        generation *k* and the budget buys ``log(budget) / log(b)`` of them.
        :data:`REACH_GENERATIONS` is that figure at ``b = 2``; it is a ceiling,
        not a constant, and **width is what moves it**.

        Ignoring width got the report wrong in both directions on 2026-08-07: a
        person born 1670 with nineteen recorded children passed a flat
        twelve-generation screen, when nineteen-fold branching spends the whole
        budget in under three generations and lands in 1755. Their recorded
        child count is the only branching estimate available and it is a lower
        bound — Geni may know more children than we do — so this errs towards
        saying a seed reaches *further* than it will.
        """
        # Rounded, not truncated: at ``b = 2`` the quotient is 11.99, and
        # truncating gave 11 where :data:`REACH_GENERATIONS` says 12. The two
        # are the same formula and must not disagree by a rounding mode.
        branching = max(2, self.children)
        return max(1, round(log(budget) / log(branching)))

    def arrives(self, budget: int = GENI_EXPORT_CAP, years: int = GENERATION_YEARS) -> int | None:
        """The year a ball seeded here plausibly reaches. ``None`` if undated."""
        if self.birth is None:
            return None
        return self.birth + self.generations_affordable(budget) * years

    def can_reach(
        self,
        target: int,
        generations: int = REACH_GENERATIONS,
        years: int = GENERATION_YEARS,
    ) -> bool:
        """Whether a `Descendants` ball seeded here could arrive at `target`.

        The screen the 2026-08-07 backtest says comes first: a person born too
        early to arrive is not a bad seed for the campaign, they are an
        impossible one. Width-aware — see :meth:`generations_affordable`.

        An undated person cannot be screened and is **kept**, not dropped. We do
        not know when they lived, and rejecting them would be inferring a date
        from silence — the thing this module refuses everywhere else. They are
        marked in the report instead.
        """
        if self.birth is None:
            return True
        reachable = min(generations, self.generations_affordable())
        return self.birth + reachable * years >= target

    @property
    def has_usable_name(self) -> bool:
        """Geni redacts living people to ``Private``.

        A candidate nobody can recognise cannot be sanity-checked by a human
        before an export is taken, so it loses ties. The same rule
        `density._doorway_rank` applies.
        """
        name = (self.name or "").lower().strip("<> ")
        return bool(name) and name != "private"


def build_lines(tree: Tree, ceiling: int = PATH_CEILING) -> dict[str, Line]:
    """Every person, measured. One pass of each underlying walk, not one per person."""
    paths, open_paths = descent_paths(tree, ceiling)
    depth = descendant_depth(tree)
    reach, tip_of = line_reach(tree)
    generation = ancestor_depth(tree)

    lines: dict[str, Line] = {}
    for geni_id, person in tree.people.items():
        tip = tip_of.get(geni_id, "")
        tip_person = tree.people.get(tip) if tip else None
        # A childless person is their own open end. `descent_paths` counts paths
        # *below* someone, and a leaf has none, so reporting `0 open paths` for
        # one would read as "nowhere to carry on" when the leaf itself is the
        # place to carry on from.
        open_below = open_paths.get(geni_id, 0)
        lines[geni_id] = Line(
            geni_id=geni_id,
            name=person.display_name,
            birth=person.birth_year,
            generation=generation.get(geni_id, 0),
            paths=paths.get(geni_id, 0),
            children=len([c for c in person.child_ids if c in tree.people]),
            depth=depth.get(geni_id, 0),
            reach=reach.get(geni_id),
            open_paths=open_below if _has_child(tree, geni_id) else 1,
            tip=tip,
            tip_name=tip_person.display_name if tip_person else "",
            tip_birth=tip_person.birth_year if tip_person else None,
        )
    return lines


def _rank_key(line: Line, present: int):
    """How good an export seed one stalled line is, best first. Written as a
    plain ascending key with the signs already applied.

    In order:

    1. **Depth, fewest generations first** — how far down the line we have
       actually walked. Depth 1 means we know this person's children and
       nothing at all below them, which is a line we stopped at the first step.
       This is the primary key because it is available for **everyone**, dated
       or not, and because it does not move with the band.

       It replaced :meth:`Line.stall`, which was primary at first and is a trap:
       stall is measured from the present, and a person's own birth year is a
       floor on their line's reach, so ranking a 100-year band by stall sorted
       it by birth year. Every band's top pick came out born in the band's first
       year — an artefact of where the band edge fell, reported as a finding.

    2. **Open paths** — how many of the descent paths end at somebody with no
       recorded child. Each is a place Geni may carry on from; one is a line
       that may genuinely have ended, several is a line we stopped walking.

    3. **Descent paths, most first** — a judgement rather than a measurement, so
       worth stating which way and why. Every candidate is already below the
       ``small`` ceiling; among lines walked equally far that end in equally
       many places, the one with *more* lines running down from it is the
       better-attested family, and one with six is likelier to have a real
       descent below it than a couple with a single recorded child. Ranking the
       other way would fill the report with the enormous tail of one-child
       stubs, which are also the likeliest to be fragments or genuine dead ends.
       It costs nothing at export time either: the ball is capped whatever it is
       seeded on.

    4. **Years followed** — the dated corroboration of depth, where there is
       any. Weak by design and placed last of the measures: at depth 1 it is
       just the gap to the youngest child's birth and says nothing about how
       much line is left. Unknown sorts last.

    5. **A usable name**, then profile ID, for recognisability and determinism.

    ``present`` is unused here and kept in the signature because every other
    per-line calculation in this module takes it and a caller should not have to
    know which ones need it. If a future key does rank on stall again, read (1)
    first.
    """
    followed = line.followed
    return (
        line.depth,
        -line.open_paths,
        -line.paths,
        0 if followed is not None else 1,
        followed if followed is not None else 0,
        0 if line.has_usable_name else 1,
        int(line.geni_id),
    )


def candidates(
    lines: dict[str, Line] | list[Line],
    *,
    present: int | None = None,
    small: int = SMALL,
    min_stall: int = 0,
    parents: dict[str, list[str]] | None = None,
) -> list[Line]:
    """Small-but-nonzero lines, worst-followed first, with nested ones dropped.

    ``min_stall`` drops lines already followed close to the present. It defaults
    to 0 — off — because "close enough" is a judgement about the campaign rather
    than a property of the data, and the stall column lets a reader apply their
    own.

    **A candidate whose parent is also a candidate is dropped**, and this is not
    cosmetic. A stalled line of six people would otherwise be reported six
    times, once per member, ranked worst-first so the *bottom* of the line
    appeared above its own ancestor — and an export seeded on the ancestor
    covers the whole subtree including branches we never saw, so the ancestor is
    strictly the better seed. Checking parents alone is enough to keep only the
    topmost of a chain: a person's line strictly contains each child's, so
    path counts rise strictly upward — a parent's is at least ``1 +`` their
    child's — and an ancestor above a non-candidate parent cannot itself be
    small.

    ``parents`` is accepted so a caller banding the same tree many times pays
    for the parent map once.
    """
    present = present_year() if present is None else present
    values = list(lines.values() if isinstance(lines, dict) else lines)
    picked = [
        line
        for line in values
        if line.is_candidate_shape(small)
        and (line.stall(present) is None or line.stall(present) >= min_stall)
    ]

    inside = {line.geni_id: line for line in picked}
    if parents is not None:
        picked = [
            line
            for line in picked
            # Strictly larger, so a cycle — where two people are each other's
            # ancestor and hold the identical set — drops neither rather than
            # both. Losing both would be silent.
            if not any(
                inside[p].paths > line.paths
                for p in parents.get(line.geni_id, ())
                if p in inside
            )
        ]

    picked.sort(key=lambda line: _rank_key(line, present))
    return picked


@dataclass(frozen=True)
class Band:
    """One period or generation range, and the lines inside it."""

    #: ``"1400–1499"``, ``"undated"``, ``"generations 10–14"``
    label: str
    #: sorts bands into reading order; undated sorts last
    order: tuple[int, int]
    people: int
    #: every line in the band with at least one descent path below it
    with_descendants: int
    #: candidates, best first, already trimmed to the report's per-band limit
    picks: tuple[Line, ...]
    #: how many candidates the band has in total, before trimming
    total_candidates: int

    @property
    def is_undated(self) -> bool:
        return self.label == "undated"


def _band_label(start: int, width: int) -> str:
    return f"{_year(start)}–{_year(start + width - 1)}"


def band_by_birth(
    lines: dict[str, Line],
    *,
    present: int | None = None,
    small: int = SMALL,
    width: int = BAND_YEARS,
    per_band: int = 5,
    min_stall: int = 0,
    parents: dict[str, list[str]] | None = None,
) -> list[Band]:
    """Group by recorded birth year, and rank candidates inside each group.

    People with no recorded birth year go to a single ``undated`` band rather
    than being dropped or given a guessed date. That band is usually large and
    is the reason :func:`band_by_generation` exists.
    """
    present = present_year() if present is None else present
    buckets: dict[tuple[int, int], list[Line]] = {}
    for line in lines.values():
        if line.birth is None:
            key = (1, 0)
        else:
            # Floor division floors towards negative infinity, which is what BC
            # years need: -450 belongs to the band starting at -500, not -400.
            key = (0, (line.birth // width) * width)
        buckets.setdefault(key, []).append(line)

    return _sorted_bands(
        [
            ("undated" if key[0] else _band_label(key[1], width), key, members)
            for key, members in buckets.items()
        ],
        present=present, small=small, per_band=per_band,
        min_stall=min_stall, parents=parents,
    )


def band_by_generation(
    lines: dict[str, Line],
    *,
    present: int | None = None,
    small: int = SMALL,
    width: int = 5,
    per_band: int = 5,
    min_stall: int = 0,
    parents: dict[str, list[str]] | None = None,
) -> list[Band]:
    """Group by generations of recorded ancestry above, and rank inside each.

    This covers the undated people, who are invisible to
    :func:`band_by_birth`. It is not a clock: depth is a fact about how far
    *we* have traced upward, so an untraced person looks shallow.
    """
    present = present_year() if present is None else present
    buckets: dict[tuple[int, int], list[Line]] = {}
    for line in lines.values():
        buckets.setdefault((0, (line.generation // width) * width), []).append(line)

    return _sorted_bands(
        [
            (f"{key[1]}–{key[1] + width - 1} generations above", key, members)
            for key, members in buckets.items()
        ],
        present=present, small=small, per_band=per_band,
        min_stall=min_stall, parents=parents,
    )


def _sorted_bands(
    groups: list[tuple[str, tuple[int, int], list[Line]]],
    *,
    present: int,
    small: int,
    per_band: int,
    min_stall: int,
    parents: dict[str, list[str]] | None,
) -> list[Band]:
    """Rank inside each group and put the groups in reading order.

    **Candidates are deduplicated within a band, not across the report.** A
    parent and child in different bands are two answers to two different
    questions — "who is the best seed among people who lived in the 1400s" is
    asked once per band — and collapsing across bands would empty a band of its
    own best pick because someone a century earlier subsumes it.
    """
    out: list[Band] = []
    for label, order, members in groups:
        picks = candidates(
            members, present=present, small=small,
            min_stall=min_stall, parents=parents,
        )
        out.append(
            Band(
                label=label,
                order=order,
                people=len(members),
                with_descendants=sum(
                    1 for line in members
                    if line.paths > 0
                ),
                picks=tuple(picks[:per_band]),
                total_candidates=len(picks),
            )
        )
    out.sort(key=lambda b: b.order)
    return out


def bands(
    lines: dict[str, Line],
    *,
    present: int | None = None,
    small: int = SMALL,
    width: int = BAND_YEARS,
    per_band: int = 5,
    min_stall: int = 0,
    parents: dict[str, list[str]] | None = None,
) -> tuple[list[Band], list[Band]]:
    """Both views: ``(by birth year, by generations above)``."""
    present = present_year() if present is None else present
    common = dict(present=present, small=small, per_band=per_band,
                  min_stall=min_stall, parents=parents)
    return (
        band_by_birth(lines, width=width, **common),
        band_by_generation(lines, **common),
    )


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    align = ["---"] + ["---:"] * (len(header) - 1)
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(align) + " |",
        *["| " + " | ".join(r) + " |" for r in rows],
    ]


def _year(value: int | None) -> str:
    if value is None:
        return "—"
    return f"{-value} BC" if value < 0 else str(value)


def _link(geni_id: str, name: str) -> str:
    """A profile link whose text cannot break the table it sits in.

    Geni names are free text and this report puts them inside a Markdown table
    cell inside a link label, where an unescaped ``|`` ends the cell and a ``]``
    ends the label. Neither is hypothetical for a corpus carrying 257219 names
    typed by strangers, and the damage is silent: the row simply renders wrong.
    """
    text = (name or geni_id).replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")
    return f"[{text}]({profile_url(geni_id)})"


def _band_rows(band_list: list[Band], present: int) -> list[list[str]]:
    rows: list[list[str]] = []
    for band in band_list:
        head = [band.label, str(band.people), str(band.with_descendants),
                str(band.total_candidates)]
        if not band.picks:
            rows.append(head + ["—"] * (len(_HEADER) - len(head)))
            continue
        for i, line in enumerate(band.picks):
            stall = line.stall(present)
            rows.append(
                [
                    *(head if i == 0 else [""] * len(head)),
                    _link(line.geni_id, line.name),
                    _year(line.birth),
                    str(line.depth),
                    str(line.paths),
                    str(line.open_paths),
                    _year(line.reach),
                    "—" if stall is None else str(stall),
                ]
            )
    return rows


_HEADER = [
    "band",
    "people",
    "with a descent",
    "candidates",
    "export from",
    "born",
    "generations followed",
    "descent paths",
    "open paths",
    "line reaches",
    "stall",
]


def render_markdown(
    tree: Tree,
    lines: dict[str, Line],
    by_birth: list[Band],
    by_generation: list[Band],
    *,
    present: int,
    small: int,
    width: int,
    min_stall: int,
    per_band: int = 5,
    target: int = REACH_TARGET,
    parents: dict[str, list[str]] | None = None,
) -> str:
    total = len(tree.people)
    dated = sum(1 for line in lines.values() if line.birth is not None)
    histogram: Counter = Counter()
    for line in lines.values():
        histogram[min(line.paths, 50)] += 1
    zero = histogram.get(0, 0)
    # Counted from the bands the tables are actually built from, not from a
    # second global call: nesting is collapsed per band, so a global collapse
    # gives a smaller number, and the report would then carry two different
    # figures both called "candidates".
    candidate_total = sum(band.total_candidates for band in by_birth)

    out = [
        "# Lines that stop early",
        "",
        "Generated by `genimerge.descendants` — re-run `python -m genimerge descendants`.",
        "",
        "`frontier.md` ranks the **upward** edge: people whose parents Geni knows "
        "and we do not. This ranks the **downward** one, and buckets it by period, "
        "because the `Descendants` campaign is about time — the tree is biased "
        "towards ancient and medieval people and the goal is to reach the present.",
        "",
        f"> **Read § Seeds that can reach {target} first, and treat the rest of "
        "this report as background.** A `Descendants` export is a breadth-first "
        f"ball of about {GENI_EXPORT_CAP:,} people, so it carries roughly "
        f"{REACH_GENERATIONS} generations — about "
        f"{REACH_GENERATIONS * GENERATION_YEARS} years — forward from its seed "
        "and no further. Eleven exports seeded on ancient people added 18,218 "
        "people in 2026-08-07 and **four** of them were born after 1900. "
        "Choosing well among seeds that cannot arrive does not help; "
        "`reports/descendants-backtest-2026-08-07.md` has the measurement.",
        "",
        "**The signal is a descent-path count that is small but not zero.** "
        "Nonzero means the line demonstrably continues, so there is something "
        "below to follow. Small means we have barely followed it: a person with "
        "three recorded paths either had three, or had three hundred and we "
        "walked one step. People with *zero* recorded descendants are left out on "
        "purpose — nothing in our data separates a childless person from an "
        "unexplored one.",
        "",
        "**Ranking inside a band is by `generations followed`** — how far down "
        "the line we have actually walked. `1` means we know a person's children "
        "and nothing whatever below them. It is the primary measure because "
        "every person has one, dated or not.",
        "",
        f"**`stall` is a column to read, not the ranking.** It is how many years "
        f"short of {present} the line stops, and it was the ranking first: "
        "because a person's own birth year is a floor on how far their line "
        "reaches, sorting a band by stall sorted it by birth year, and every "
        "band's top pick came out born in the band's first year. That is where "
        "the band edge fell, not a finding.",
        "",
        f"## Seeds that can reach {target}",
        "",
        f"Candidates whose ball can arrive at {target}. The screen is "
        "**width-aware**: the generations a ball carries is "
        "``log(budget) / log(branching)``, so the earliest a *narrow* seed can "
        f"be born and still arrive is {target - REACH_GENERATIONS * GENERATION_YEARS}, "
        "and a wide one has to be much later. This is a **reachability screen, "
        "not a promise**: it rules "
        "out seeds that cannot arrive rather than claiming the rest will. A wide "
        "descent exhausts the budget sooner than a narrow one, so the later-born "
        "a seed is, the more certain the arrival.",
        "",
        "**This list is untested.** Two methods have already been refuted by "
        "measurement here, and the honest position is that this one is a "
        "constraint plus an unvalidated ranking rather than a demonstrated "
        "improvement. To test it, take one of these exports and diff the tree "
        "the way the backtest did.",
        "",
    ]
    reachable = [
        line for line in candidates(
            lines, present=present, small=small, min_stall=min_stall, parents=parents
        )
        if line.birth is not None and line.can_reach(target)
    ]
    if reachable:
        # Most open ends first, among seeds the width-aware screen says arrive.
        # Both simpler orderings were tried against the real tree and both
        # failed: by open ends alone put people born 1670 with nineteen children
        # at the top, whose ball actually lands in 1755; by birth year alone put
        # people born in the 1960s at the top, whose lines already reach 1996 and
        # who have nothing left to add. The screen removes the first, and
        # `reach` removes nothing — it is a column, because a line already past
        # the target is still worth an export for the generations after it.
        reachable = sorted(
            reachable,
            key=lambda line: (-line.open_paths, -(line.birth or 0), int(line.geni_id)),
        )
        out += [
            f"{len(reachable):,} candidates qualify, most **open ends** first — "
            "the seeds with the most places a walk could carry on from.",
            "",
            "**`ball reaches ~` is width-aware and is what makes the screen "
            f"work.** The {REACH_GENERATIONS}-generation figure is the "
            "*narrowest* case, a descent branching twice per couple; one "
            "branching twenty times spends the same budget in three generations "
            "and travels 90 years instead of 360. So a person born in 1670 with "
            "nineteen recorded children does **not** qualify, and one born in "
            "1858 with twenty does. A recorded child count is the only branching "
            "estimate available and it is a lower bound — Geni may know more "
            "children than we do — so this errs towards saying a seed reaches "
            "further than it will.",
            "",
        ]
        out += _table(
            ["#", "export from", "born", "children", "ball reaches ~",
             "generations followed", "descent paths", "open paths",
             "line reaches"],
            [
                [
                    str(i),
                    _link(line.geni_id, line.name),
                    _year(line.birth),
                    str(line.children),
                    _year(line.arrives()),
                    str(line.depth),
                    str(line.paths),
                    str(line.open_paths),
                    _year(line.reach),
                ]
                for i, line in enumerate(reachable[: per_band * 6], start=1)
            ],
        )
    else:
        out += [
            f"None: no candidate is born {target - REACH_GENERATIONS * GENERATION_YEARS} "
            "or later. Every seed available would run out of budget before "
            f"{target}.",
            "",
        ]
    out += [
        "",
        "Undated people are **not** screened out of the bands below — we do not "
        "know when they lived, and rejecting them would be inferring a date from "
        "silence. They simply cannot appear in this section.",
        "",
        "## How much of the tree this can see",
        "",
    ]
    out += _table(
        ["measure", "people", "share"],
        [
            ["in the tree", str(total), "100.0%"],
            ["with a recorded birth year", str(dated), f"{dated / total:.1%}"],
            ["with no recorded descendant", str(zero), f"{zero / total:.1%}"],
            [
                f"candidates (1–{small} descent paths, none inside another's line)",
                str(candidate_total),
                f"{candidate_total / total:.1%}",
            ],
        ],
    )
    out += [
        "",
        f"**{total - dated} people ({(total - dated) / total:.1%}) carry no birth "
        "year at all.** No date is inferred for them here — they are in the "
        "`undated` band below, and the generation view is the axis that can rank "
        "them.",
        "",
        "## Descent paths per person",
        "",
        "A person's count is, over each recorded child, **one for the child plus "
        "the child's own count** — so this counts *lines coming down from* "
        "someone, not distinct people, and a descendant reachable down two lines "
        "counts twice. That is the intent: pedigree collapse is dense here, and "
        "de-duplicating it makes the top of a wide, repeatedly-intermarried "
        "descent look narrow. Every count is exact; the table's last row is "
        "everyone at 50 or above.",
        "",
    ]
    out += _table(
        ["descent paths", "people"],
        [
            [("50 or more" if k == 50 else str(k)), str(histogram[k])]
            for k in sorted(histogram)
        ],
    )
    out += [
        "",
        "## By period",
        "",
        f"Birth-year bands of {width} years, best {per_band} candidates each, "
        "least-followed first. **Read `generations followed` and `open paths` "
        "together**: a line walked one generation whose paths end at several "
        "different childless people is a line we stopped walking, while one "
        "ending in a single person may simply have ended. The profile linked is "
        "the one to export from; *near them* is its line's forward edge, which "
        "the seed file also lists.",
        "",
        "**A candidate whose own parent is also a candidate is not shown**, "
        "within a band: an export seeded on the ancestor covers the descendant's "
        "line as well, plus branches off it we have never seen. Nesting is "
        "collapsed per band rather than across the report, so a band still gets "
        "its own best pick even when someone a century earlier subsumes it.",
        "",
        "**Expect the `generations followed` column to read `1` all the way "
        "down.** Lines walked exactly one step are much the most numerous, so "
        "they fill every band's top places, and the column being constant is the "
        "ranking working rather than a bug. Raise `--per-band` to see past them.",
        "",
        (
            f"`--min-stall {min_stall}`: lines already followed to within "
            f"{min_stall} years of {present} are excluded."
            if min_stall
            else "`--min-stall` is off, so lines already followed close to the "
            "present are still listed. The `stall` column is there to apply "
            "your own threshold by eye."
        ),
        "",
    ]
    out += _table(_HEADER, _band_rows(by_birth, present))
    out += [
        "",
        "## By generation",
        "",
        "Generations of *recorded* ancestry above, which covers the undated "
        "people the period view cannot rank. **This is not a second clock.** "
        "Depth measures how far we have traced upward, so a person whose "
        "ancestry we have not followed looks shallow whenever they lived.",
        "",
    ]
    out += _table(_HEADER, _band_rows(by_generation, present))
    out += [
        "",
        "## What this does not say",
        "",
        "**A person who is their own ancestor truncates every measure here.** "
        "That is impossible in life and ordinary in a genealogy database — it "
        "means one person exists under two profiles and the two got linked as "
        "parent and child. The walks drop the edge back into a cycle, so such a "
        "person's `generations followed` is a floor rather than a count. It used "
        "to be reported as **zero**, which put these people at the top of every "
        "band, the ranking being on fewest generations; they now truncate rather "
        "than falsify. `reports/frontier.md` § cycles lists them as the defects "
        "they are.",
        "",
        "The path counts measure **our** sampling, not Geni's content. A "
        "stalled line is one *we* stopped following; whether Geni holds a large "
        "descent below it is exactly the unknown an export resolves, and a line "
        "can also stop because it really did stop. Nothing here is inferred from "
        "a name or a place, and no birth year is guessed.",
        "",
    ]
    return "\n".join(out) + "\n"


def render_seed_list(band_list: list[Band], *, newest_first: bool = True) -> str:
    """One line per candidate, in the shape of `individuals I can easily export.txt`.

    Both the candidate and their line's forward tip, because "export from them
    **or near them**" is two different exports: seeding on the ancestor takes
    the whole descent including branches we never saw, and seeding on the tip
    grows forward from where the line actually stops. The tip is omitted when it
    is the candidate themselves.

    **Most recent band first**, which is the reverse of the report's reading
    order and is deliberate: the report is a survey and reads oldest to newest,
    while this file is a work list for a campaign whose whole point is reaching
    the present. Undated candidates go last either way — they are the ones the
    period axis cannot place.
    """
    ordered = sorted(
        band_list,
        key=lambda b: (b.is_undated, [-v for v in b.order] if newest_first else b.order),
    )
    lines: list[str] = []
    for band in ordered:
        for line in band.picks:
            lines.append(f"{profile_url(line.geni_id)} | Geni - {line.name or 'NN'}")
            if line.tip and line.tip != line.geni_id:
                lines.append(
                    f"{profile_url(line.tip)} | Geni - {line.tip_name or 'NN'} "
                    f"(tip of {line.name or line.geni_id})"
                )
    return "\n".join(lines) + ("\n" if lines else "")
