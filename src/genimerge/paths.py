"""How much of a Geni relationship path this tree already holds.

Geni will show you a chain of relationships between any two profiles it can
connect. That chain is **evidence from outside our data**: it names people Geni
knows about, in order, whether or not any export has ever reached them. Nothing
else in this repo can produce that. `frontier` and `seeds` rank doorways by what
is missing *behind* them, which is inference; a relationship path tells you what
is actually there.

So a path is worth keeping as data and re-checking as the merge grows, which is
what this module does: for each step, do we hold that person, and in which
component? The answer moves as exports arrive, and the interesting shape is not
the total but **where the run of held people stops** — that person is a doorway
with an observed payoff behind them.

**Matching is by name, and that is a compromise this repo otherwise refuses.**
`CLAUDE.md` is emphatic that the Geni profile ID is the primary key and merging
is an exact join, never fuzzy name matching. Nothing here merges anything: this
is a lookup whose output is a report for a human. It can still be wrong in both
directions — a namesake matches, a differently-spelled record does not — so
every result carries how it was matched, and an ambiguous one says so instead of
picking. If a path file ever gains real profile IDs (they are in the hrefs on
Geni's page, they just do not survive copy-paste), :func:`check` uses them and
the guessing stops for those rows.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from . import frontier
from .identity import profile_url
from .model import Person, Tree

__all__ = [
    "EXACT",
    "PARTIAL",
    "ABSENT",
    "AMBIGUOUS",
    "REPEAT",
    "NAME_MATCHING_IS_ADVISORY",
    "PathStep",
    "StepResult",
    "PathReport",
    "normalise",
    "parse_path",
    "load_path",
    "check",
    "render_markdown",
]

#: How a step was resolved. `BY_ID` never appears until a path file carries
#: profile IDs; it exists so the report can distinguish a real join from a
#: guess the moment that becomes possible.
BY_ID = "id"
EXACT = "exact"
PARTIAL = "partial"
AMBIGUOUS = "ambiguous"
UNRESOLVED = "unresolved"
ABSENT = "absent"

#: Held, and already walked earlier on this same path.
#:
#: A saved Geni page can carry more than one relationship path — a blood one and
#: an in-law one — and `path-from-html` writes them into a single file, so the
#: second chain restarts at "You" and re-walks the first few people.
#: `paths/nn-basse.tsv` does exactly this: steps 36-44 repeat steps 1-9.
#:
#: This exists because those rows used to be reported `ABSENT`. The `used` rule
#: below refuses a person to a second step, which is right for the name
#: fallback and wrong for an exact ID, and the two cases shared one branch. The
#: cost was not a cosmetic mislabel: `genimerge connectors` reads a run of
#: absent steps as a *bridge* and ranks an export by it, so the account owner
#: himself was being reported as a missing person to go and fetch from Geni.
REPEAT = "repeat"

#: Stated in the generated report, and asserted by `tests/test_paths.py`.
#:
#: A reader who sees "held: 30 of 83" will otherwise take it for a measurement
#: of the same kind as the merge counts, which are exact joins on the profile
#: ID. This one is not, and the difference is the whole reason `CLAUDE.md`
#: forbids name matching elsewhere.
NAME_MATCHING_IS_ADVISORY = (
    "Matched by name, not by Geni profile ID — so this is advisory. A namesake "
    "can match the wrong person and a differently-spelled record can be missed. "
    "The profile IDs are in the links on Geni's page; adding them to the path "
    "file replaces every guess below with an exact join."
)

#: Letters that carry meaning rather than accent, so NFKD leaves them alone.
#: Norwegian and Icelandic names in this tree are full of them, and `Øye` not
#: matching `Oye` would be a spurious absence rather than a real one.
_FOLD = {"ø": "o", "æ": "ae", "ð": "d", "þ": "th", "ł": "l", "ß": "ss"}

#: A partial match needs this many shared name tokens. Without a floor, the
#: unnamed people on a path — `n n`, `daughter of Smbat of Lori` — collect
#: hundreds of candidates each and the report becomes noise.
MIN_SHARED_TOKENS = 2

#: A token held by more than this many people identifies nobody. Measured from
#: the tree rather than written as a stoplist, because the words that carry no
#: information here are not the English ones: `no` (Japanese), `av`, `von`,
#: `datter`, `king`, `of` all rank alongside each other, and a hand-written list
#: would be a guess at a distribution the data already states.
COMMON_TOKEN_PEOPLE = 200

#: Above this many candidates, a name has told us nothing and the step is
#: `UNRESOLVED` rather than `AMBIGUOUS` — 73 people are called `n n`, and
#: counting that as "we hold this person" would inflate every total in the
#: report with the one kind of row that is guaranteed meaningless.
AMBIGUITY_LIMIT = 5


def normalise(text: str) -> str:
    """A name reduced to what two spellings of it would share.

    Case, accents, and punctuation go; CJK characters are left alone, since
    ``isalnum`` is true for them and there is nothing to fold.
    """
    folded = "".join(_FOLD.get(ch, ch) for ch in text.casefold())
    decomposed = unicodedata.normalize("NFKD", folded)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return " ".join("".join(ch if ch.isalnum() else " " for ch in stripped).split())


@dataclass(frozen=True)
class PathStep:
    """One row of a path file."""

    step: int
    name: str
    relation: str = ""
    note: str = ""
    #: Which of the file's paths this row belongs to, 1-based.
    #:
    #: **Emma, 2026-08-16:** *"You haven't been distinguishing the blood and
    #: marriage things. You've been treating them as one gigantic tree, one
    #: gigantic line? If so, that's really weird… It doesn't really matter that
    #: much whether you're distinguishing them, as long as you treat it as being
    #: two paths and not one."*
    #:
    #: Geni shows a pair both a blood path and an in-law path, and
    #: `path-from-html` writes them into one file end to end. The boundary is
    #: stated by the page rather than guessed: the first step of a path has no
    #: relation to a previous one, because there is no previous one, so a row
    #: with an empty relation after the first row starts a new chain.
    #: `paths/nn-basse.tsv` has exactly two, at steps 1 and 36, both `You`.
    chain: int = 1

    @property
    def geni_id(self) -> str:
        """A profile ID from the note column, if the file happens to carry one.

        Written as ``geni:6000000003243185408`` — the same spelling Geni's own
        ``RFN`` line uses, so there is one convention rather than two. Note that
        `identity.GENI_ID_RE` does not apply here: it matches a whole GEDCOM
        xref, ``@I123@``, and this is the bare ID.
        """
        for token in self.note.replace(",", " ").split():
            if token.startswith("geni:") and token[5:].isdigit():
                return token[5:]
        return ""

    @property
    def tokens(self) -> tuple[str, ...]:
        return tuple(normalise(self.name).split())


@dataclass
class StepResult:
    """What the tree had to say about one step."""

    step: PathStep
    how: str = ABSENT
    #: every person that matched, so an ambiguous row can be inspected rather
    #: than silently resolved to whichever sorted first
    candidates: list[Person] = field(default_factory=list)
    component: int | None = None

    @property
    def held(self) -> bool:
        """Whether we appear to hold this person at all.

        `AMBIGUOUS` counts as held: a handful of records matched, so the person
        is very likely one of them even though which is unsettled. `UNRESOLVED`
        does not — past `AMBIGUITY_LIMIT` the name has stopped identifying
        anyone and a match means nothing.

        `REPEAT` counts as held for the plainest possible reason: it is a person
        we hold, walked twice. Counting a repeat as a gap is what made
        `nn-basse` read 47 of 57 when it is 57 of 57.
        """
        return self.how not in (ABSENT, UNRESOLVED)

    @property
    def person(self) -> Person | None:
        """The single match, or nothing when there is a choice to be made."""
        return self.candidates[0] if len(self.candidates) == 1 else None


@dataclass
class PathReport:
    results: list[StepResult]
    #: sizes of the merged tree's components, largest first — a step's
    #: `component` indexes into this, 1-based
    component_sizes: list[int] = field(default_factory=list)

    @property
    def held(self) -> list[StepResult]:
        return [r for r in self.results if r.held]

    @property
    def absent(self) -> list[StepResult]:
        return [r for r in self.results if not r.held]

    @property
    def chains(self) -> list["PathReport"]:
        """One report per path in the file, because a file can hold two.

        Emma, 2026-08-16: *"as long as you treat it as being two paths and not
        one."* Geni shows a pair a blood path and an in-law path and
        `path-from-html` writes both into one file; `PathStep.chain` marks which
        is which. Every property here is per chain once it is read off a member
        of this list, which is what makes the split cost nothing at the call
        sites that only ever see one path.
        """
        out: list[PathReport] = []
        for result in self.results:
            if not out or result.step.chain != out[-1].results[0].step.chain:
                out.append(PathReport([], self.component_sizes))
            out[-1].results.append(result)
        return out

    @property
    def run_ends_at(self) -> StepResult | None:
        """The last step before the first gap, **within the first chain**.

        This is the number the project actually acts on. Everything up to here
        is a walk we could already make; the step after it is the doorway, and
        the people beyond it are the observed payoff for exporting from it.

        The chain bound is load-bearing rather than tidy: without it a file whose
        first path is entirely held keeps scanning into the *second* path, and
        reports a doorway belonging to a different chain of people. Read
        `report.chains[i].run_ends_at` for the others.
        """
        last = None
        chain = self.results[0].step.chain if self.results else 1
        for result in self.results:
            if result.step.chain != chain or not result.held:
                break
            last = result
        return last

    @property
    def held_beyond_the_gap(self) -> list[StepResult]:
        """Held steps after the run stops — the far side of a broken chain.

        Empty until an export lands past the gap. When it is not empty, the
        path has two anchored ends and a missing middle, which is a different
        and better situation than a path that simply runs out.

        **Bounded to the first chain**, for the same reason as `run_ends_at`: a
        second path in the same file being held is not the far side of the first
        path's gap, and reading it as one turns a plain reach-into-the-unknown
        into a bridge that does not exist.
        """
        chain = self.results[0].step.chain if self.results else 1
        mine = [r for r in self.results if r.step.chain == chain]
        first_gap = next((i for i, r in enumerate(mine) if not r.held), len(mine))
        return [r for r in mine[first_gap:] if r.held]

    @property
    def components_touched(self) -> list[int]:
        return sorted({r.component for r in self.held if r.component is not None})


def parse_path(text: str) -> list[PathStep]:
    """Read a path file: ``#`` comments, a header row, then tab-separated steps.

    Tolerant of missing trailing columns, because the note column is empty on
    most rows and trailing tabs are exactly what an editor strips.
    """
    steps: list[PathStep] = []
    chain = 1
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = line.split("\t")
        if cells[0].strip() == "step":  # the header
            continue
        cells += [""] * (4 - len(cells))
        number, name, relation, note = (c.strip() for c in cells[:4])
        if not name:
            continue
        relation = "" if relation == "-" else relation
        # A row with nothing to relate back to is the head of a path. The first
        # such row opens chain 1; every later one opens the next chain.
        if not relation and steps:
            chain += 1
        steps.append(
            PathStep(
                step=int(number) if number.isdigit() else len(steps) + 1,
                name=name,
                relation=relation,
                note=note,
                chain=chain,
            )
        )
    return steps


def load_path(path: str | Path) -> list[PathStep]:
    return parse_path(Path(path).read_text(encoding="utf-8"))


def _name_variants(person: Person) -> set[str]:
    """Every spelling of a person worth matching against.

    Geni records alternates freely — a Japanese emperor carries a romanised
    name, a kanji name and a posthumous title as three `NAME` lines — and a
    relationship path may quote any one of them.
    """
    variants: set[str] = set()
    for name in person.names:
        for raw in (name.display, name.full.replace("/", " "), name.married):
            key = normalise(raw)
            if key:
                variants.add(key)
        for nickname in name.nicknames:
            key = normalise(nickname)
            if key:
                variants.add(key)
    return variants


def check(tree: Tree, steps: list[PathStep]) -> PathReport:
    """Resolve every step of a path against the merged tree.

    Steps are resolved in order and a person settled by one step is not offered
    to a later one. A relationship path is a chain of *distinct* people — Geni
    walks from one to the next — so a second step landing on the same profile is
    a matching error rather than a discovery. That rule is not decoration: the
    first run of this report matched step 31, Jelena Urošević, to Elisabeth of
    Hungary, who is step 30, because Elisabeth carries the alternate name
    ``Queen consort of Hungary`` and the tokens are a subset. It reported the
    doorway itself as already held, which is the exact opposite of the truth and
    would have argued against taking the export that matters most.
    """
    by_name: dict[str, list[str]] = {}
    by_token: dict[str, set[str]] = {}
    for geni_id, person in tree.people.items():
        for variant in _name_variants(person):
            by_name.setdefault(variant, []).append(geni_id)
            for token in variant.split():
                by_token.setdefault(token, set()).add(geni_id)
    token_people = {token: len(ids) for token, ids in by_token.items()}

    comps = frontier.components(tree)
    component_of = {
        member: index
        for index, comp in enumerate(comps, start=1)
        for member in comp.members
    }

    results = []
    used: set[str] = set()
    for step in steps:
        result = _resolve(step, tree, by_name, by_token, token_people, component_of, used)
        if result.person is not None:
            used.add(result.person.geni_id)
        results.append(result)
    return PathReport(results=results, component_sizes=[c.size for c in comps])


def _resolve(
    step: PathStep,
    tree: Tree,
    by_name: dict[str, list[str]],
    by_token: dict[str, set[str]],
    token_people: dict[str, int],
    component_of: dict[str, int],
    used: set[str],
) -> StepResult:
    def finish(single_how: str, ids: list[str]) -> StepResult:
        people = [tree.people[i] for i in sorted(ids)]
        if len(people) == 1:
            return StepResult(
                step=step,
                how=single_how,
                candidates=people,
                component=component_of.get(people[0].geni_id),
            )
        how = AMBIGUOUS if len(people) <= AMBIGUITY_LIMIT else UNRESOLVED
        return StepResult(step=step, how=how, candidates=people)

    if step.geni_id:
        # An ID settles the row either way. Falling back to the name when the ID
        # is absent from the tree cannot find the right person — we know their
        # ID and it is not here — and can only find a wrong one: step 42 is
        # `n n`, which 73 profiles share.
        if step.geni_id not in tree.people:
            return StepResult(step=step, how=ABSENT)
        if step.geni_id in used:
            # Seen earlier on this path. The `used` rule exists to stop a *name*
            # landing twice on one profile, which is a matching error; an exact
            # ID landing twice is not an error at all, it is a file holding two
            # relationship paths end to end. Reporting it absent claimed we did
            # not hold somebody we demonstrably do.
            return StepResult(
                step=step,
                how=REPEAT,
                candidates=[tree.people[step.geni_id]],
                component=component_of.get(step.geni_id),
            )
        return finish(BY_ID, [step.geni_id])

    exact = [i for i in by_name.get(normalise(step.name), []) if i not in used]
    if exact:
        return finish(EXACT, exact)

    tokens = set(step.tokens)
    # Only distinctive tokens open the search, which both removes the noise and
    # keeps the candidate pool small — `of` alone would otherwise pull in
    # thousands of people for every titled name on the path.
    distinctive = {t for t in tokens if token_people.get(t, 0) <= COMMON_TOKEN_PEOPLE}
    if len(tokens) >= MIN_SHARED_TOKENS and distinctive:
        pool: set[str] = set()
        for token in distinctive:
            pool |= by_token.get(token, set())
        hits = [
            candidate
            for candidate in pool - used
            if _shares_a_name(tokens, distinctive, tree.people[candidate])
        ]
        if hits:
            return finish(PARTIAL, hits)

    return StepResult(step=step, how=ABSENT)


def _shares_a_name(tokens: set[str], distinctive: set[str], person: Person) -> bool:
    """Whether one of a person's names is a shortening of the path's, or vice versa.

    Subset either way, because Geni truncates in both directions: the path says
    ``Baron Jon Hafthorsson av Sørum`` where the record says
    ``Jon Hafthorsson Hafthorssen Sorum``, and says ``Okoshi Mononobe`` where
    the record says only ``Okoshi``.
    """
    for variant in _name_variants(person):
        other = set(variant.split())
        shared = tokens & other
        if (
            len(shared) >= MIN_SHARED_TOKENS
            and shared & distinctive
            and (tokens <= other or other <= tokens)
        ):
            return True
    return False


def to_json(report: PathReport) -> dict:
    """The machine-readable form: every step, its Geni link, and our verdict.

    This is the artifact to work from when deciding what to export. One row per
    step in path order, so the gaps are contiguous ranges rather than something
    to reconstruct.
    """
    steps = []
    for result in report.results:
        step = result.step
        person = result.person
        row = {
            "step": step.step,
            "chain": step.chain,
            "name": step.name,
            "relation_to_previous": step.relation,
            "geni_id": step.geni_id or None,
            "geni_url": profile_url(step.geni_id) if step.geni_id else None,
            "in_tree": result.held,
            "matched": result.how,
            "component": result.component,
            "matched_geni_id": person.geni_id if person else None,
            "matched_name": person.display_name if person else None,
            "candidates": [p.geni_id for p in result.candidates]
            if len(result.candidates) > 1
            else [],
        }
        steps.append(row)

    end = report.run_ends_at
    chains = report.chains
    return {
        "steps_total": len(report.results),
        "steps_in_tree": len(report.held),
        # A saved page can carry a blood path and an in-law path; both land in
        # one file, and the run below belongs to the first of them.
        "paths_in_this_file": len(chains),
        "chains": [
            {
                "chain": c.results[0].step.chain,
                "first_step": c.results[0].step.step,
                "last_step": c.results[-1].step.step,
                "steps_total": len(c.results),
                "steps_in_tree": len(c.held),
                "unbroken_run_ends_at": (c.run_ends_at.step.step
                                         if c.run_ends_at else None),
            }
            for c in chains
        ],
        "unbroken_run_ends_at": end.step.step if end else None,
        "components": {
            str(index): size for index, size in enumerate(report.component_sizes, 1)
        },
        "components_touched": report.components_touched,
        "gaps": [
            {"from": first, "to": last, "length": last - first + 1}
            for first, last in _gaps(report)
        ],
        "steps": steps,
    }


def _gaps(report: PathReport) -> list[tuple[int, int]]:
    """Contiguous runs of not-held steps, as (first, last) step numbers.

    A run never spans two chains: consecutive step numbers across the seam
    between a blood path and an in-law path are two separate gaps in two
    separate paths, not one long one.
    """
    runs: list[list[int]] = []
    chain_of: dict[int, int] = {}
    for result in report.results:
        if result.held:
            continue
        step = result.step.step
        previous_same_chain = (
            runs and runs[-1][1] == step - 1
            and chain_of.get(runs[-1][1]) == result.step.chain
        )
        if previous_same_chain:
            runs[-1][1] = step
        else:
            runs.append([step, step])
        chain_of[step] = result.step.chain
    return [(a, b) for a, b in runs]


def render_markdown(report: PathReport, title: str) -> str:
    """The report a person reads to decide which export to take next."""
    results = report.results
    held = report.held
    lines = [f"# {title}", ""]

    without_id = [r for r in results if not r.step.geni_id]
    if without_id:
        how = NAME_MATCHING_IS_ADVISORY
    else:
        how = (
            "Every step carries its Geni profile ID, so this is an exact join on "
            "this repo's primary key — not a name match, and not advisory."
        )
    lines += [
        f"**{len(held)} of {len(results)} steps** on this path are in the merged "
        f"tree. {how}",
        "",
    ]

    chains = report.chains
    if len(chains) > 1:
        # Emma, 2026-08-16: "as long as you treat it as being two paths and not
        # one." Geni gives a pair both a blood path and an in-law path and the
        # saved page carries both, so the counts above span two chains of people
        # and every "the run stops at" sentence below is about the first.
        counts = "; ".join(
            f"path {i} — steps {c.results[0].step.step}–{c.results[-1].step.step}, "
            f"{len(c.held)} of {len(c.results)} held"
            for i, c in enumerate(chains, start=1)
        )
        lines += [
            f"**This file holds {len(chains)} relationship paths, not one.** Geni "
            "shows a blood path and an in-law path for the same pair and the saved "
            f"page carries both: {counts}. The run and doorway below are the first "
            "path's.",
            "",
        ]

    # The run and the doorway are properties of ONE path, so they are read off
    # the first chain rather than off the whole file.
    first = chains[0] if chains else report
    end = report.run_ends_at
    if end is None:
        lines += ["The path is broken at its first step.", ""]
    elif len(first.held) == len(first.results):
        lines += ["Every step is held: this path is walkable inside our own data.", ""]
    else:
        # By position in the list, not by step number — a hand-edited path file
        # with a gap in its numbering would otherwise name the wrong person.
        first_gap = next(r for r in first.results if not r.held)
        lines += [
            f"**The unbroken run stops at step {end.step.step}, "
            f"{end.step.name}.** The next step, **{first_gap.step.name}**, is not "
            "in the tree — so that is the doorway, and everything past it that "
            "Geni shows is the payoff for exporting from there.",
            "",
        ]

    beyond = report.held_beyond_the_gap
    if beyond:
        lines += [
            f"**{len(beyond)} steps past the gap are held anyway** — "
            f"{beyond[0].step.name} onward. Both ends of this path are anchored "
            "and the middle is missing, which is a bridge to build rather than a "
            "reach into the unknown.",
            "",
        ]

    unresolved = [r for r in results if r.how == UNRESOLVED]
    if unresolved:
        lines += [
            f"**{len(unresolved)} steps are counted as not held because their "
            "name identifies nobody** — more than "
            f"{AMBIGUITY_LIMIT} people in the tree carry it. Geni records "
            "unnamed people as `n n` and similar, and 73 of them share that "
            "exact name, so these rows are unknown rather than absent.",
            "",
        ]

    touched = report.components_touched
    if len(touched) > 1:
        sizes = ", ".join(
            f"component {c} ({report.component_sizes[c - 1]} people)" for c in touched
        )
        lines += [
            f"The held steps fall in {len(touched)} disconnected components: "
            f"{sizes}. Until an export bridges them, no walk through our own "
            "data gets from one end of this path to the other.",
            "",
        ]

    lines += ["## Steps", ""]
    lines += _table(report)
    return "\n".join(lines) + "\n"


def _table(report: PathReport) -> list[str]:
    header = "| # | name | relation | in the tree | matched | component |"
    rows = [header, "| ---: | --- | --- | --- | --- | ---: |"]
    for result in report.results:
        step = result.step
        person = result.person
        if person is not None:
            who = f"[{person.display_name}]({person.url})"
        elif result.candidates:
            who = f"{len(result.candidates)} profiles share this name"
        else:
            who = "—"
        component = str(result.component) if result.component else "—"
        rows.append(
            f"| {step.step} | {_escape(step.name)} | {step.relation or '—'} "
            f"| {who} | {result.how} | {component} |"
        )
    return rows


def _escape(text: str) -> str:
    return text.replace("|", "\\|")
