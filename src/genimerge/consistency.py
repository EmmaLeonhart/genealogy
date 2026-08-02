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
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .identity import profile_url
from .model import Person, Tree

__all__ = [
    "IMPOSSIBLE",
    "IMPLAUSIBLE",
    "MAX_LIFESPAN",
    "MIN_PARENT_AGE",
    "POSTHUMOUS_MONTHS_GRACE",
    "Finding",
    "Report",
    "check",
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


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    people_checked: int = 0
    people_with_a_year: int = 0

    def of_kind(self, kind: str) -> list[Finding]:
        return [f for f in self.findings if f.kind == kind]


def _named(person: Person) -> str:
    return person.display_name or person.geni_id


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

    return "\n".join(lines) + "\n"
