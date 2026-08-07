"""Lines that stop early: who to export from to reach modern times.

`genimerge.frontier` ranks **parentless** people — the upward edge, where Geni
knows an ancestor we do not. `genimerge.density` ranks neighbourhoods **few
exports touched**, which knows nothing about when anyone lived. Neither answers
the question behind the `Descendants` campaign, which is Emma's and is about
time rather than thinness: *the tree is biased towards ancient and medieval
people, and the goal is to reach the present.*

This module ranks the **downward** edge, and it buckets by when people lived so
that the ranking can be read one period at a time.

**The signal is a small but nonzero descendant count.** Nonzero and small are
doing different jobs and both are load-bearing:

- **Nonzero** means the line demonstrably continues. Geni recorded at least one
  child, so there is something below to follow, and an export seeded here is not
  a bet on a childless couple.
- **Small** means we have barely followed it. A person with three recorded
  descendants either had three, or had three hundred and we walked one step.

A person with *zero* recorded descendants is the ambiguous case and is left out
of the candidate list on purpose: they may be a genuine leaf, and nothing in our
data separates "childless" from "unexplored". That is the same discriminator
`density` uses upward, where a thin region full of parentless people is
under-sampled and a thin region with none may simply be finished.

**`stall` is the measure that serves the campaign.** For each person it is the
number of years between the latest birth recorded anywhere at or below them and
the present. A person born in 1400 whose line reaches 1430 and stops has been
walked one generation; a person born in 1400 whose line reaches 1890 has been
followed for fifteen. Both look identical to a descendant *count* if the second
one's line is narrow. Stall separates them, and it is what makes a ranking
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

**What this cannot tell you** is the same limit `density` has. Our descendant
count measures *our* sampling. Whether Geni holds a large descent below a
stalled line is precisely the unknown an export resolves — a line can also stop
because it really did stop, and the `open tips` column is the check: a stalled
line whose end is several childless people is a line with several places to
carry on from, while one ending in a single person may just have ended.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date

from .frontier import _child_map, _parent_map, _post_order, ancestor_depth
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
    "descendant_and_tip_counts",
    "build_lines",
    "candidates",
    "band_by_birth",
    "band_by_generation",
    "bands",
    "render_markdown",
    "render_seed_list",
]

#: Default ceiling on "small". A line we hold this many people of or fewer is
#: one we have brushed rather than walked. Not a measured threshold — it is the
#: knob the report is meant to be re-run with, which is why it is a CLI flag.
SMALL = 20

#: Where counting stops. Above this a line's size is reported as unknown rather
#: than as a number, because :func:`descendant_and_tip_counts` abandons the walk
#: — see its docstring for why an exact count for everyone is not affordable at
#: this tree's size. Kept comfortably above :data:`SMALL` so the ceiling can be
#: raised on the command line without also raising this.
CAP = 200

#: Default width of a birth-year band, in years. Wide enough that a band holds
#: enough people to rank within, narrow enough that "born in this band" is a
#: real period rather than "the middle ages".
BAND_YEARS = 100


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


def descendant_and_tip_counts(
    tree: Tree, cap: int = CAP
) -> tuple[dict[str, int], dict[str, int]]:
    """For each person: how many people descend from them, and how many of
    those are childless — **exactly, up to `cap`, and no further**.

    Returns ``(sizes, tips)``. A person whose line exceeds `cap` is absent from
    both dicts, which is the caller's signal that the count is unknown rather
    than zero; :class:`Line` carries it as ``descendants_exact = False``.

    **Why this is bounded, when `genimerge.frontier.descendant_counts` is not.**
    Descendant sets overlap heavily — cousins marry, and the same ancestor is
    reached down several lines — so counts cannot be summed from children
    without double-counting. `frontier` solves that exactly for every person by
    carrying each set as a bitmask in a Python int, which costs one bit per
    person per person: at 8766 people that was about a kilobyte each, and at the
    257219 this tree now holds it is 32 KB each and tens of gigabytes in total.

    This module does not need the big numbers. Its entire question is *small but
    nonzero*, so counts above the ceiling are interchangeable and only need to
    be recognised as large. So each line is walked with a visited set and
    abandoned the moment it passes `cap`, and — the pruning that makes it cheap
    — **a person with a child whose line is over the cap is over it too**, which
    is exact and settles nearly every ancestor without a walk. Each remaining
    walk visits at most ``cap + 1`` people.

    Cycle-tolerant by the visited set: a person entered twice and linked to
    themselves is ordinary in a genealogy database.

    The person themselves is not in their own descendant set, so a childless
    person has zero open tips of their own — see :func:`build_lines`, which adds
    them back where that matters.
    """
    children = _child_map(tree)
    sizes: dict[str, int] = {}
    tips: dict[str, int] = {}
    over: set[str] = set()

    for node in _post_order(list(tree.people), children):
        kids = children[node]
        if any(child in over for child in kids):
            over.add(node)
            continue

        seen: set[str] = set()
        stack = list(kids)
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            if len(seen) > cap:
                over.add(node)
                break
            stack.extend(children[current])
        else:
            sizes[node] = len(seen)
            tips[node] = sum(1 for person in seen if not children[person])

    return sizes, tips


def descendant_depth(tree: Tree) -> dict[str, int]:
    """Longest chain of recorded descendants below each person.

    The mirror of :func:`genimerge.frontier.ancestor_depth`, and cycle-tolerant
    for the same reason: a person entered twice and linked to themselves is
    ordinary in a genealogy database, and a naive walk would not terminate.
    """
    children = _child_map(tree)
    depth: dict[str, int] = {}

    for node in _post_order(list(tree.people), children):
        known = [depth[c] for c in children[node] if c in depth]
        depth[node] = 1 + max(known) if known else 0

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
    #: distinct people below them in our data. Meaningless unless
    #: ``descendants_exact``, where it is the counting cap rather than a count.
    descendants: int
    #: whether the line was small enough to finish counting — see
    #: :func:`descendant_and_tip_counts`. A line we gave up on is large, which is
    #: all this module needs to know about it.
    descendants_exact: bool
    #: longest chain of generations below them
    depth: int
    #: latest birth year recorded at or below them
    reach: int | None
    #: descendants with no recorded child — the places the line could carry on
    open_tips: int
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

        A line whose size we never finished counting is not small, so it is not
        a candidate — which is the same answer it would get from an exact count,
        since the walk only gives up above :data:`CAP` and :data:`CAP` is above
        any sane ``small``.
        """
        return self.descendants_exact and 0 < self.descendants <= small

    @property
    def has_usable_name(self) -> bool:
        """Geni redacts living people to ``Private``.

        A candidate nobody can recognise cannot be sanity-checked by a human
        before an export is taken, so it loses ties. The same rule
        `density._doorway_rank` applies.
        """
        name = (self.name or "").lower().strip("<> ")
        return bool(name) and name != "private"


def build_lines(tree: Tree, cap: int = CAP) -> dict[str, Line]:
    """Every person, measured. One pass of each underlying walk, not one per person."""
    counts, tips = descendant_and_tip_counts(tree, cap)
    depth = descendant_depth(tree)
    reach, tip_of = line_reach(tree)
    generation = ancestor_depth(tree)

    lines: dict[str, Line] = {}
    for geni_id, person in tree.people.items():
        tip = tip_of.get(geni_id, "")
        tip_person = tree.people.get(tip) if tip else None
        exact = geni_id in counts
        # A childless person is their own open tip. The walk collects
        # descendants only, so it cannot count them, and reporting `0 open tips`
        # for a leaf would read as "nowhere to carry on" when the leaf itself is
        # the place to carry on from.
        open_tips = tips.get(geni_id, 0) + (0 if _has_child(tree, geni_id) else 1)
        lines[geni_id] = Line(
            geni_id=geni_id,
            name=person.display_name,
            birth=person.birth_year,
            generation=generation.get(geni_id, 0),
            descendants=counts.get(geni_id, cap),
            descendants_exact=exact,
            depth=depth.get(geni_id, 0),
            reach=reach.get(geni_id),
            open_tips=open_tips,
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

    2. **Open tips** — how many childless people the line ends in. Each is a
       place Geni may carry on from; one is a line that may genuinely have
       ended, several is a line we stopped walking.

    3. **Descendants, most first** — a judgement rather than a measurement, so
       worth stating which way and why. Every candidate is already below the
       ``small`` ceiling; among lines walked equally far that end in equally
       many places, the one with *more* recorded people is the better-attested
       family, and one with six recorded members is likelier to have a real
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
        -line.open_tips,
        -line.descendants,
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
    descendant counts rise monotonically upward and an ancestor above a
    non-candidate parent cannot itself be small.

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
                inside[p].descendants > line.descendants
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
    #: every line in the band with a nonzero descendant count
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
                    if not line.descendants_exact or line.descendants > 0
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
                    str(line.descendants),
                    str(line.open_tips),
                    _year(line.reach),
                    "—" if stall is None else str(stall),
                ]
            )
    return rows


_HEADER = [
    "band",
    "people",
    "with a descendant",
    "candidates",
    "export from",
    "born",
    "generations followed",
    "descendants",
    "open tips",
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
    cap: int = CAP,
) -> str:
    total = len(tree.people)
    dated = sum(1 for line in lines.values() if line.birth is not None)
    histogram: Counter = Counter()
    for line in lines.values():
        histogram[min(line.descendants, 50) if line.descendants_exact else 50] += 1
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
        "**The signal is a descendant count that is small but not zero.** Nonzero "
        "means the line demonstrably continues, so there is something below to "
        "follow. Small means we have barely followed it: a person with three "
        "recorded descendants either had three, or had three hundred and we walked "
        "one step. People with *zero* recorded descendants are left out on purpose "
        "— nothing in our data separates a childless person from an unexplored one.",
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
                f"candidates (1–{small} descendants, none inside another's line)",
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
        "## Descendants per person",
        "",
        f"Counting stops at {cap}. A line bigger than that is recorded as large "
        "rather than measured: this report's whole question is *small*, and an "
        "exact count for everybody costs tens of gigabytes at this tree's size. "
        "The last row is therefore everyone with 50 or more **plus** everyone we "
        "stopped counting.",
        "",
    ]
    out += _table(
        ["descendants", "people"],
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
        "least-followed first. **Read `generations followed` and `open tips` "
        "together**: a line walked one generation that ends in several childless "
        "people is a line we stopped walking, while one ending in a single person "
        "may simply have ended. The profile linked is the one to export from; "
        "*near them* is its line's forward edge, which the seed file also lists.",
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
        "The descendant counts measure **our** sampling, not Geni's content. A "
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
