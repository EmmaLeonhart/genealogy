"""Whether the tree's own dates can all be true at once.

Everything else in this package checks the *merge* — that nothing was lost, that
the result is one tree, that the reports match their inputs — or checks us
against *Wikidata*. Nothing asked whether the genealogy is internally coherent.

`genimerge.frontier.ancestry_cycles` already does this for one case, and its
framing is the right one for all of them: impossible in life, ordinary in a
genealogy database, a real defect in the source data rather than in our
handling of it. This module extends that to dates.

**Nothing here is fixed, and nothing should be.** These are errors in what Geni
holds. The output is a list to work from, with links to open.

**Why it is not merely tidiness.** `genimerge.crosscheck` proposes P569 and P570
statements to Wikidata *from these dates*, so a wrong year here becomes a wrong
year on a public database. A finding in this report is a reason to look at the
Geni profile before running a batch that repeats it.

Findings are split into two kinds, because they warrant different responses:

``IMPOSSIBLE``
    Cannot be true. Someone born before a parent, or after their mother died.
    Every one is an error somewhere.

``IMPLAUSIBLE``
    Could be true and probably is not — a parent of eleven, a lifespan of 130.
    Worth a human eye; some will turn out to be fine.

**Normalise by `people_with_a_year`, never by `people_checked`.** This is the
one number here that has actually misled, and it stayed on the queue for days as
"errors are growing faster than the tree". Going 10 → 54 exports grew the tree
3.9× and the impossible-date count 5.9×, which reads as the data getting worse.
It was the denominator: an impossible date requires a date, and the share of
people who have one is not constant across exports. Measured over 94 exports on
2026-08-05, the older 54 carry dates for 44.6% of their people and the newer 40
for 55.9%. Counting per *person* therefore attributes to error growth what is
really date-coverage growth.

Per dated person the rate is flat and falling: **4.26% in the old exports, 3.04%
in the new, 2.65% in the merged tree**. Newer material is better, not worse.

**The merge creates almost none of them, which was worth checking rather than
assuming.** An impossible date needs two values and after a merge those can come
from two exports taken days apart, so "merging manufactures contradictions" is a
plausible story. It is not what happens: of 2,618 people flagged in the merged
tree, **3** are flagged only after merging. Eleven go the other way — flagged
inside an export, not in the merge — because later-wins conflict resolution
replaced the offending value with a corrected one.

The merged rate being *lower* than either per-export rate is not a paradox:
someone in five exports is counted five times across five runs and once in the
merge, and people in many exports are the well-covered ones with better dates.

**Duplicate counts are a different story and do scale superlinearly.** They grew
3.0× (possible) and 3.8× (likely) against 1.8× more people from 54 to 94
exports. `duplicate_candidates` groups by normalised name, and the number of
same-name pairs grows with the square of the population, so ~3.2× is what 1.8×
more people predicts. That is the shape of the measure, not a change in the
data — do not read it as the tree getting dirtier.
"""

from __future__ import annotations

import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field

from .identity import profile_url
from .model import Person, Tree

__all__ = [
    "IMPOSSIBLE",
    "IMPLAUSIBLE",
    "LIKELY",
    "POSSIBLE",
    "MAX_LIFESPAN",
    "MIN_PARENT_AGE",
    "POSTHUMOUS_MONTHS_GRACE",
    "Finding",
    "Duplicate",
    "Report",
    "check",
    "duplicate_candidates",
    "render_markdown",
]

IMPOSSIBLE = "impossible"
IMPLAUSIBLE = "implausible"

#: Above this many years, a recorded lifespan is more likely a typo than a life.
#: The documented human maximum is 122; 120 keeps the report short without
#: pretending the boundary is precise.
MAX_LIFESPAN = 120

#: Below this age, a recorded parent is more likely a date error than a fact.
MIN_PARENT_AGE = 12

#: A child can be born after its father dies. Anything inside this window is
#: ordinary and is not reported — 16 such births are in the current tree, and
#: reporting them as defects would be wrong. There is no equivalent grace on
#: the mother's side, where a posthumous birth is not possible at all.
POSTHUMOUS_MONTHS_GRACE = 12


@dataclass(frozen=True)
class Finding:
    """One thing that cannot or probably did not happen."""

    kind: str
    person: str
    detail: str
    #: the other person involved, where there is one
    other: str | None = None

    @property
    def is_impossible(self) -> bool:
        return self.kind == IMPOSSIBLE


LIKELY = "likely"
POSSIBLE = "possible"


@dataclass(frozen=True)
class Duplicate:
    """People who look like one person recorded under several Geni profiles."""

    tier: str
    name: str
    geni_ids: tuple[str, ...]
    birth_year: int | None
    shares_parents: bool

    @property
    def size(self) -> int:
        return len(self.geni_ids)


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    duplicates: list[Duplicate] = field(default_factory=list)
    people_checked: int = 0
    people_with_a_year: int = 0
    #: same name and parents but different birth years — reused names, excluded
    reused_names: int = 0

    def of_kind(self, kind: str) -> list[Finding]:
        return [f for f in self.findings if f.kind == kind]

    def of_tier(self, tier: str) -> list[Duplicate]:
        return [d for d in self.duplicates if d.tier == tier]


def _named(person: Person) -> str:
    return person.display_name or person.geni_id


#: Letters Unicode decomposition cannot help with, transliterated by hand.
#:
#: NFKD splits `é` into `e` plus a combining accent, so dropping combining marks
#: handles it. It does nothing for `ø`, `æ`, `ð` or `þ`, which are single
#: codepoints with no ASCII base — and stripping them instead is not a small
#: loss in this tree. Counted over the merged data: **1302 `ø`, 210 `Ø`, 118
#: `æ`, 23 `ð`**. Dropping them turns `Sørbø` into `s rb`, which both hides real
#: matches and invents false ones between unrelated names reduced to the same
#: rubble.
NORDIC = str.maketrans({"ø": "o", "æ": "ae", "å": "a", "ð": "d", "þ": "th", "ł": "l"})


def _normalised(name: str | None) -> str:
    """A name flattened enough that spelling noise does not hide a match.

    Case folded, Nordic letters transliterated, accents dropped, punctuation
    removed. **Letters are never removed** — only punctuation — so the Cyrillic
    names in this tree compare against each other instead of collapsing to
    nothing.

    This is comparison for *human review*, never for merging. The merge joins on
    the Geni profile ID and nothing else, because the one time a looser rule was
    allowed here it turned the foreign xref `@NI04461@` into a link to a
    stranger's profile.
    """
    text = (name or "").casefold().translate(NORDIC)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^\w\s]|_", " ", text).split())


def duplicate_candidates(tree: Tree) -> tuple[list[Duplicate], int]:
    """People who may be one person under several Geni profiles.

    Returns the candidates and the number of groups **excluded** as reused
    names, because that exclusion is most of the work and a report that hides it
    reads as though nothing was missed.

    Two tiers, kept apart because they are not equally strong:

    ``LIKELY``
        Same name, same parents, same birth year. Two records for one person,
        barring a coincidence that would need siblings born the same year and
        given the same name.

    ``POSSIBLE``
        Same name and birth year, with parents differing or unrecorded. Could
        as easily be cousins named for the same grandparent.

    **What is deliberately not reported:** people sharing a name and parents but
    born in different years. There are 138 such groups in this tree, and they
    are the largest single pattern — in these families a dead child's name was
    routinely given to the next one, so those are two real siblings. Reporting
    on name-and-parents alone would return 202 groups and be wrong about most of
    them, which is the fastest way to make a report like this ignored.
    """
    by_name_year: dict[tuple[str, int], list[Person]] = defaultdict(list)
    by_name_parents: dict[tuple[str, str | None, str | None], list[Person]] = defaultdict(list)

    for person in tree.people.values():
        name = _normalised(person.display_name)
        if not name:
            continue
        if person.birth_year:
            by_name_year[(name, person.birth_year)].append(person)
        if person.father_id or person.mother_id:
            by_name_parents[(name, person.father_id, person.mother_id)].append(person)

    reused = sum(
        1
        for group in by_name_parents.values()
        if len(group) > 1 and len({p.birth_year for p in group if p.birth_year}) > 1
    )

    found: list[Duplicate] = []
    for (name, year), group in by_name_year.items():
        if len(group) < 2:
            continue
        parents = {(p.father_id, p.mother_id) for p in group}
        shares = len(parents) == 1 and any(parents.pop())
        found.append(
            Duplicate(
                tier=LIKELY if shares else POSSIBLE,
                name=name,
                geni_ids=tuple(sorted(p.geni_id for p in group)),
                birth_year=year,
                shares_parents=shares,
            )
        )

    found.sort(key=lambda d: (d.tier != LIKELY, -d.size, d.name))
    return found, reused


def check(tree: Tree) -> Report:
    """Every date in the tree that contradicts another date in the tree."""
    report = Report(people_checked=len(tree.people))
    people = tree.people

    for person in people.values():
        birth, death = person.birth_year, person.death_year
        if birth or death:
            report.people_with_a_year += 1

        if birth and death:
            if birth > death:
                report.findings.append(
                    Finding(
                        IMPOSSIBLE,
                        person.geni_id,
                        f"born {birth}, died {death} — born after their own death",
                    )
                )
            elif death - birth > MAX_LIFESPAN:
                report.findings.append(
                    Finding(
                        IMPLAUSIBLE,
                        person.geni_id,
                        f"born {birth}, died {death} — a lifespan of {death - birth} years",
                    )
                )

    for person in people.values():
        birth = person.birth_year
        if not birth:
            continue
        for role, parent_id in (("father", person.father_id), ("mother", person.mother_id)):
            parent = people.get(parent_id) if parent_id else None
            if parent is None:
                continue
            report.findings.extend(_against_parent(person, birth, parent, role))

    report.findings.sort(key=lambda f: (f.kind != IMPOSSIBLE, f.detail, f.person))
    report.duplicates, report.reused_names = duplicate_candidates(tree)
    return report


def _against_parent(person: Person, birth: int, parent: Person, role: str) -> list[Finding]:
    """One child's birth year against one parent's dates."""
    found: list[Finding] = []
    parent_birth, parent_death = parent.birth_year, parent.death_year

    if parent_birth is not None:
        if birth < parent_birth:
            found.append(
                Finding(
                    IMPOSSIBLE,
                    person.geni_id,
                    f"born {birth}, before their {role} {_named(parent)} was born "
                    f"in {parent_birth}",
                    other=parent.geni_id,
                )
            )
        elif birth - parent_birth < MIN_PARENT_AGE:
            found.append(
                Finding(
                    IMPLAUSIBLE,
                    person.geni_id,
                    f"born {birth}, when their {role} {_named(parent)} was "
                    f"{birth - parent_birth}",
                    other=parent.geni_id,
                )
            )

    if parent_death is not None and birth > parent_death:
        # A father can die before the birth; a mother cannot. The grace window
        # covers a pregnancy and applies to fathers only.
        grace = POSTHUMOUS_MONTHS_GRACE // 12 if role == "father" else 0
        if birth > parent_death + grace:
            found.append(
                Finding(
                    IMPOSSIBLE,
                    person.geni_id,
                    f"born {birth}, after their {role} {_named(parent)} died "
                    f"in {parent_death}",
                    other=parent.geni_id,
                )
            )

    return found


def _link(tree: Tree, geni_id: str | None) -> str:
    if not geni_id:
        return "—"
    person = tree.people.get(geni_id)
    label = _named(person) if person else geni_id
    return f"[{label}]({profile_url(geni_id)})"


def render_markdown(tree: Tree, report: Report, *, top: int = 100) -> str:
    impossible = report.of_kind(IMPOSSIBLE)
    implausible = report.of_kind(IMPLAUSIBLE)

    lines = [
        "# Internal consistency",
        "",
        "Generated by `genimerge.consistency` — re-run",
        "`python -m genimerge consistency`.",
        "",
        "Whether this tree's own dates can all be true at once. Everything else "
        "here checks the merge, or checks us against Wikidata; this checks the "
        "genealogy against itself.",
        "",
        "**These are errors in Geni's data, not in the merge, and nothing here "
        "is fixed automatically.** Each row links both people so it can be "
        "opened and corrected at the source.",
        "",
        "It is not only tidiness. `genimerge crosscheck` proposes P569 and P570 "
        "statements to Wikidata *from these dates*, so a wrong year here becomes "
        "a wrong year on a public database — a finding below is a reason to "
        "check the profile before running a batch that repeats it.",
        "",
        "## Summary",
        "",
        f"| | count |",
        "| --- | ---: |",
        f"| people in the tree | {report.people_checked} |",
        f"| of those, carrying any year | {report.people_with_a_year} |",
        f"| **impossible** — cannot be true | **{len(impossible)}** |",
        f"| **implausible** — could be, probably is not | **{len(implausible)}** |",
        "",
        "A child born within a year of its father's death is ordinary and is "
        "**not** reported. There is no such allowance on the mother's side, "
        "where a birth after death is not possible at all — counting the two "
        "together would invent defects and slander real births.",
        "",
    ]

    for title, findings, blurb in (
        (
            "Impossible",
            impossible,
            "Every one of these is an error somewhere — in a date, or in a link "
            "between two people who are not really parent and child.",
        ),
        (
            "Implausible",
            implausible,
            f"A parent under {MIN_PARENT_AGE}, or a lifespan over {MAX_LIFESPAN} "
            "years. Some of these will be correct; they are here for a human to "
            "judge, not to be taken as defects.",
        ),
    ):
        lines += ["", f"## {title} ({len(findings)})", ""]
        if not findings:
            lines.append("None.")
            continue
        lines += [blurb, ""]
        if len(findings) > top:
            lines += [f"Showing the first {top}.", ""]
        lines += ["| person | what | other |", "| --- | --- | --- |"]
        for finding in findings[:top]:
            lines.append(
                f"| {_link(tree, finding.person)} "
                f"| {finding.detail} "
                f"| {_link(tree, finding.other)} |"
            )

    lines += _duplicate_section(tree, report, top=top)
    return "\n".join(lines) + "\n"


def _duplicate_section(tree: Tree, report: Report, *, top: int) -> list[str]:
    likely = report.of_tier(LIKELY)
    possible = report.of_tier(POSSIBLE)

    lines = [
        "",
        "## The same person, twice",
        "",
        "The merge guarantees one record per Geni **profile**, which is not one "
        "record per **person**: two profiles for the same human merge to two "
        "records and always will, because the profile ID is the join key. "
        "`reports/frontier.md` already reports one ancestry cycle as evidence of "
        "exactly this — that is the symptom; these are candidates for the cause.",
        "",
        f"| | groups |",
        "| --- | ---: |",
        f"| **likely** — same name, same parents, same birth year | **{len(likely)}** |",
        f"| **possible** — same name and year, parents differ or unknown | **{len(possible)}** |",
        f"| excluded as reused names — see below | {report.reused_names} |",
        "",
        f"**{report.reused_names} groups share a name and both parents but were born in "
        "different years, and are deliberately not listed.** In these families a "
        "dead child's name was routinely given to the next child, so those are "
        "two real siblings. Matching on name and parents alone would return them "
        "all as duplicates and be wrong about nearly every one — the exclusion is "
        "most of the work here, not an oversight.",
        "",
        "**Nothing is merged, and nothing here should be.** Names are evidence "
        "for a human, never a join: this project keys on the Geni profile ID "
        "precisely because looser matching once produced a link to a stranger's "
        "profile. Merging two profiles is an edit on Geni, made by somebody who "
        "has opened both.",
    ]

    for title, group, blurb in (
        (
            "Likely",
            likely,
            "Same name, same parents, same birth year. Short of siblings born in "
            "one year and given one name, these are one person recorded twice.",
        ),
        (
            "Possible",
            possible,
            "Same name and birth year, but the parents differ or are not "
            "recorded. Could as easily be cousins named for the same "
            "grandparent — worth opening, not worth assuming.",
        ),
    ):
        lines += ["", f"### {title} ({len(group)})", ""]
        if not group:
            lines.append("None.")
            continue
        lines += [blurb, ""]
        if len(group) > top:
            lines += [f"Showing the first {top}.", ""]
        lines += ["| born | people |", "| ---: | --- |"]
        for duplicate in group[:top]:
            links = " · ".join(_link(tree, geni_id) for geni_id in duplicate.geni_ids)
            lines.append(f"| {duplicate.birth_year or '—'} | {links} |")

    return lines
