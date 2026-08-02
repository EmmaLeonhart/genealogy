"""Compare what this tree says about a person with what Wikidata says.

For the people already linked to a Wikidata item, both sides state parents,
spouses and dates. Comparing them is read-only and creates nothing, and the
**disagreements are the point**: each one is either our match being wrong or a
real error on one of the two sites. The three P2600 contradictions found the
same way turned out to be duplicate Geni profiles, which was the most useful
thing that run produced.

Every claim lands in exactly one bucket:

``AGREES``
    Both sides state it and they match.
``GAP``
    We state it, Wikidata does not — a candidate edit.
``CONFLICT``
    Both state it and they differ — for a human, never for a batch.
``NOT_COMPARABLE``
    We cannot say anything: we have no value, or the other end of a
    relationship is not itself linked to an item, so there is nothing to point
    P22 *at*.

Two deliberate asymmetries. A date our export marked approximate
("ABT 1275") is **never** called a conflict, because "about 1275" and "1278"
do not disagree. And a relationship is only comparable when *both* people are
linked — otherwise a missing P22 means "we don't know their father's item",
not "Wikidata is missing a father".
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable

from .model import Person, Tree
from .reconcile import YEAR_TOLERANCE, YEAR_TOLERANCE_APPROX, _year_of
from .wikidata import WikidataClient

__all__ = [
    "AGREES",
    "GAP",
    "CONFLICT",
    "NOT_COMPARABLE",
    "Finding",
    "CrossCheck",
    "LinkBalance",
    "link_balances",
    "suspect_links",
    "PROPERTIES",
    "fetch_claims",
    "cross_check",
    "render_markdown",
    "ClaimBatch",
    "build_claim_batch",
    "render_claim_markdown",
]

AGREES = "agrees"
GAP = "gap"
CONFLICT = "conflict"
NOT_COMPARABLE = "not comparable"

#: property -> (human label, kind). "item" claims point at another item;
#: "time" claims are dates.
PROPERTIES = {
    "P22": ("father", "item"),
    "P25": ("mother", "item"),
    "P26": ("spouse", "item"),
    "P569": ("date of birth", "time"),
    "P570": ("date of death", "time"),
}


@dataclass(frozen=True)
class Finding:
    geni_id: str
    qid: str
    prop: str
    verdict: str
    #: what we say, in readable form
    ours: str = ""
    #: what Wikidata says, in readable form
    theirs: str = ""
    person: str = ""
    #: for item claims, the QID we would point at
    target_qid: str | None = None
    #: for time claims, the value in Wikidata's format
    target_time: str | None = None
    detail: str = ""


@dataclass
class CrossCheck:
    findings: list[Finding] = field(default_factory=list)
    people_checked: int = 0

    def by_verdict(self, verdict: str) -> list[Finding]:
        return [f for f in self.findings if f.verdict == verdict]

    def counts(self) -> dict[str, Counter]:
        out: dict[str, Counter] = {prop: Counter() for prop in PROPERTIES}
        for finding in self.findings:
            out[finding.prop][finding.verdict] += 1
        return out


@dataclass(frozen=True)
class LinkBalance:
    """One linked person, and how their comparable properties came out.

    Only ``agrees`` and ``conflicts`` count. A gap is Wikidata not stating
    something, which is evidence about coverage rather than about the link, and
    *not comparable* is not evidence at all.
    """

    geni_id: str
    qid: str
    person: str
    agrees: int
    conflicts: int

    @property
    def comparable(self) -> int:
        return self.agrees + self.conflicts

    @property
    def margin(self) -> int:
        """How far conflicts outweigh agreements. Higher is more suspect."""
        return self.conflicts - self.agrees


def link_balances(check: CrossCheck) -> list[LinkBalance]:
    """Per-person agree/conflict tallies, most suspect first."""
    tally: dict[tuple[str, str], list] = {}
    for finding in check.findings:
        key = (finding.geni_id, finding.qid)
        entry = tally.setdefault(key, [finding.person, 0, 0])
        if finding.verdict == AGREES:
            entry[1] += 1
        elif finding.verdict == CONFLICT:
            entry[2] += 1

    balances = [
        LinkBalance(geni_id=geni_id, qid=qid, person=person, agrees=agrees, conflicts=conflicts)
        for (geni_id, qid), (person, agrees, conflicts) in tally.items()
    ]
    return sorted(balances, key=lambda b: (-b.margin, -b.conflicts, b.qid))


def suspect_links(check: CrossCheck, *, min_conflicts: int = 2) -> list[LinkBalance]:
    """Links where the disagreement is concentrated enough to be about the link.

    The report lists conflicts one property at a time, which reads as a set of
    independent errors. It is not always: a person whose father, mother, birth
    and death all disagree is one observation, not four, and what it is evidence
    about is the *link* rather than any of the four facts.

    The test is ``conflicts > agrees`` with at least ``min_conflicts`` of them.
    A single conflict is ordinary — two sources differing on one medieval date
    says nothing — and a person who agrees on more than they conflict on is a
    good link with a data disagreement inside it.

    This deliberately does **not** decide that a suspect link is wrong. See
    :func:`render_markdown` for the two readings it cannot separate.
    """
    return [
        balance
        for balance in link_balances(check)
        if balance.conflicts >= min_conflicts and balance.conflicts > balance.agrees
    ]


def fetch_claims(
    client: WikidataClient, qids: Iterable[str], batch_size: int = 150
) -> dict[str, dict[str, list[str]]]:
    """``qid -> {property -> [values]}`` for the properties we compare.

    Item values come back as bare QIDs, time values as the raw literal.
    """
    ordered = sorted(set(qids))
    claims: dict[str, dict[str, list[str]]] = {}
    props = " ".join(f"wdt:{p}" for p in PROPERTIES)

    for start in range(0, len(ordered), batch_size):
        batch = ordered[start : start + batch_size]
        values = " ".join(f"wd:{q}" for q in batch)
        query = (
            "SELECT ?item ?prop ?value WHERE {\n"
            f"  VALUES ?item {{ {values} }}\n"
            f"  VALUES ?prop {{ {props} }}\n"
            "  ?item ?prop ?value.\n"
            "}"
        )
        for row in client.sparql(query):
            qid = row["item"].rsplit("/", 1)[-1]
            prop = row["prop"].rsplit("/", 1)[-1]
            value = row["value"]
            if value.startswith("http://www.wikidata.org/entity/Q"):
                value = value.rsplit("/", 1)[-1]
            claims.setdefault(qid, {}).setdefault(prop, []).append(value)

    return claims


def _date_verdict(person: Person, kind: str, theirs: list[str]) -> tuple[str, str, str]:
    """Compare one of our dates with Wikidata's. Returns (verdict, ours, theirs)."""
    event = person.events.get(kind)
    our_date = event.date if event else None
    our_year = our_date.year if our_date else None
    their_years = [y for y in (_year_of(v) for v in theirs) if y is not None]
    their_text = ", ".join(str(y) for y in sorted(set(their_years)))

    if our_year is None:
        return NOT_COMPARABLE, "", their_text
    ours_text = our_date.raw
    if not their_years:
        return GAP, ours_text, ""

    # An approximate date is given more room, and never counted as a conflict:
    # "about 1275" and "1278" do not disagree.
    approximate = bool(our_date.modifier)
    tolerance = YEAR_TOLERANCE_APPROX if approximate else YEAR_TOLERANCE
    if any(abs(our_year - y) <= tolerance for y in their_years):
        return AGREES, ours_text, their_text
    if approximate:
        return NOT_COMPARABLE, ours_text, their_text
    return CONFLICT, ours_text, their_text


def _our_relatives(person: Person, prop: str) -> list[str]:
    if prop == "P22":
        return [person.father_id] if person.father_id else []
    if prop == "P25":
        return [person.mother_id] if person.mother_id else []
    return list(person.spouse_ids)


def cross_check(
    tree: Tree, linked: dict[str, str], claims: dict[str, dict[str, list[str]]]
) -> CrossCheck:
    """Compare every linked person's claims against Wikidata's."""
    result = CrossCheck()

    for geni_id, qid in sorted(linked.items(), key=lambda kv: kv[1]):
        person = tree.people.get(geni_id)
        if person is None:
            continue
        result.people_checked += 1
        theirs = claims.get(qid, {})

        for prop, (label, kind) in PROPERTIES.items():
            if kind == "time":
                event_kind = "birth" if prop == "P569" else "death"
                verdict, ours, them = _date_verdict(person, event_kind, theirs.get(prop, []))
                event = person.events.get(event_kind)
                date = event.date if event else None
                result.findings.append(
                    Finding(
                        geni_id=geni_id,
                        qid=qid,
                        prop=prop,
                        verdict=verdict,
                        ours=ours,
                        theirs=them,
                        person=person.display_name,
                        target_time=date.iso() if date and date.is_exact else None,
                        detail="our date is approximate" if date and date.modifier else "",
                    )
                )
                continue

            # A relationship is only comparable when the other person is linked
            # too: without that there is nothing for P22 to point at, and a
            # missing statement says nothing about Wikidata.
            our_ids = _our_relatives(person, prop)
            our_qids = [linked[i] for i in our_ids if i in linked]
            their_qids = theirs.get(prop, [])

            if not our_qids:
                verdict = NOT_COMPARABLE
                detail = (
                    "we know the person but they are not linked to an item"
                    if our_ids
                    else ""
                )
            elif not their_qids:
                verdict, detail = GAP, ""
            elif set(our_qids) & set(their_qids):
                verdict, detail = AGREES, ""
            else:
                verdict, detail = CONFLICT, ""

            result.findings.append(
                Finding(
                    geni_id=geni_id,
                    qid=qid,
                    prop=prop,
                    verdict=verdict,
                    ours=", ".join(our_qids),
                    theirs=", ".join(their_qids),
                    person=person.display_name,
                    target_qid=our_qids[0] if len(our_qids) == 1 else None,
                    detail=detail,
                )
            )

    return result


@dataclass
class ClaimBatch:
    statements: list = field(default_factory=list)
    #: gaps we chose not to propose, and why
    withheld: list[tuple[Finding, str]] = field(default_factory=list)
    retrieved: str = ""


def build_claim_batch(
    check: CrossCheck,
    tree: Tree,
    exact_links: set[str],
    *,
    retrieved: str,
) -> ClaimBatch:
    """Turn gaps into statements, refusing everything that is not clearly safe.

    ``exact_links`` is the set of Geni IDs matched by **P2600**. A relationship
    is proposed only when both ends are in it: an expansion match is an
    inference, and inferring a parent onto a real Wikidata item is exactly the
    error that would be hardest for anyone to notice afterwards.
    """
    from .quickstatements import Statement, geni_reference

    batch = ClaimBatch(retrieved=retrieved)

    for finding in check.by_verdict(GAP):
        _label, kind = PROPERTIES[finding.prop]

        if kind == "item":
            if finding.target_qid is None:
                batch.withheld.append(
                    (finding, "more than one possible value; choosing would be guessing")
                )
                continue
            if finding.geni_id not in exact_links:
                batch.withheld.append(
                    (finding, "this person is linked by inference, not by their Geni ID")
                )
                continue
            other = next(
                (
                    gid
                    for gid in _our_relatives(tree.people[finding.geni_id], finding.prop)
                    if gid in exact_links
                ),
                None,
            )
            if other is None:
                batch.withheld.append(
                    (finding, "the other person is linked by inference, not by their Geni ID")
                )
                continue
            value = finding.target_qid
        else:
            if finding.target_time is None:
                batch.withheld.append(
                    (finding, "our date is approximate, so there is no exact value to state")
                )
                continue
            if finding.geni_id not in exact_links:
                batch.withheld.append(
                    (finding, "this person is linked by inference, not by their Geni ID")
                )
                continue
            value = finding.target_time

        batch.statements.append(
            Statement(
                qid=finding.qid,
                prop=finding.prop,
                value=value,
                references=geni_reference(finding.geni_id, retrieved),
            )
        )

    return batch


def render_claim_markdown(batch: ClaimBatch, *, top: int = 80) -> str:
    from .quickstatements import Statement  # noqa: F401  (documented shape)

    lines = [
        "# QuickStatements batch: parents, spouses and dates",
        "",
        "Generated by `genimerge.crosscheck` — re-run `python -m genimerge crosscheck`.",
        "",
        "**Nothing here has been sent to Wikidata.** Read it, check it, and run",
        "it yourself at <https://quickstatements.toolforge.org/> if you agree.",
        "",
        "Only *gaps* are proposed — statements this tree holds that the Wikidata",
        "item does not. Conflicts are never proposed; they are in",
        "`reports/wikidata-crosscheck.md` for a human.",
        "",
        "Eligibility, enforced rather than assumed:",
        "",
        "- a relationship needs **both** people linked by their Geni ID (P2600),",
        "  never by inference — putting an inferred parent on a real item is the",
        "  error that would be hardest to notice afterwards;",
        "- a date must be **exact** in our export; anything marked `ABT`, `BEF`,",
        "  `AFT` or `BET` offers no value worth stating;",
        "- a claim with more than one possible value is withheld, not guessed.",
        "",
    ]
    lines += _table(
        ["", "count"],
        [
            ["**statements proposed**", str(len(batch.statements))],
            ["gaps withheld", str(len(batch.withheld))],
        ],
    )

    if batch.withheld:
        reasons = Counter(reason for _f, reason in batch.withheld)
        lines += ["", "## Why gaps were withheld", ""]
        lines += _table(
            ["reason", "gaps"], [[reason, str(n)] for reason, n in reasons.most_common()]
        )

    if batch.statements:
        lines += ["", "## Statements in the batch", ""]
        lines += _table(
            ["item", "property", "value"],
            [
                [_wd(s.qid), f"{s.prop} {PROPERTIES[s.prop][0]}", s.value]
                for s in batch.statements[:top]
            ],
        )

    return "\n".join(lines) + "\n"


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    sep = ["---", *["---:"] * (len(header) - 1)]
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
        *["| " + " | ".join(r) + " |" for r in rows],
    ]


def _wd(qid: str) -> str:
    return f"[{qid}](https://www.wikidata.org/wiki/{qid})"


def _year_gap(finding: Finding) -> int | None:
    """How many years apart a date conflict is; ``None`` for item conflicts."""
    if PROPERTIES[finding.prop][1] != "time":
        return None
    from .dates import parse_date

    ours = parse_date(finding.ours).year
    theirs = [int(t) for t in finding.theirs.replace(",", " ").split() if t.lstrip("-").isdigit()]
    if ours is None or not theirs:
        return None
    return min(abs(ours - t) for t in theirs)


def _severity(finding: Finding) -> tuple:
    """Rank conflicts: structural first, then by how far apart the dates are.

    A different parent is a disagreement about who someone *is*; a five-year
    difference on a medieval birth is two sources rounding differently. Sorting
    them together by nothing in particular would bury the first kind under the
    second.
    """
    gap = _year_gap(finding)
    if gap is None:
        return (1, 0)
    return (0, gap)


def _gap_text(finding: Finding) -> str:
    gap = _year_gap(finding)
    return "structural" if gap is None else f"{gap} yr"


def render_markdown(
    check: CrossCheck, *, top: int = 100, exact_links: set[str] | None = None
) -> str:
    counts = check.counts()
    lines = [
        "# Cross-check: this tree against Wikidata",
        "",
        "Generated by `genimerge.crosscheck` — re-run",
        "`python -m genimerge crosscheck`.",
        "",
        f"For each of the **{check.people_checked}** people linked to a Wikidata",
        "item, what both sides say about their parents, spouse and dates.",
        "",
        "**The conflicts are the point.** Each one is either our match being",
        "wrong or a real error on one of the two sites — the same check on",
        "P2600 turned up three duplicate Geni profiles.",
        "",
        "A relationship counts as *not comparable* when the other person is not",
        "linked to an item: there is nothing for the statement to point at, so",
        "its absence on Wikidata says nothing. A date we hold only approximately",
        "is never counted as a conflict.",
        "",
        "## Summary",
        "",
    ]
    lines += _table(
        ["property", "agrees", "gap", "conflict", "not comparable"],
        [
            [
                f"{prop} {label}",
                str(counts[prop][AGREES]),
                str(counts[prop][GAP]),
                str(counts[prop][CONFLICT]),
                str(counts[prop][NOT_COMPARABLE]),
            ]
            for prop, (label, _kind) in PROPERTIES.items()
        ],
    )

    conflicts = sorted(check.by_verdict(CONFLICT), key=_severity, reverse=True)
    lines += ["", f"## Conflicts ({len(conflicts)})", ""]
    if not conflicts:
        lines += ["None. Everything both sides state, they agree on."]
    else:
        lines += [
            "**A different parent or spouse is a structural disagreement and is",
            "listed first.** A date counts as conflicting when the years differ",
            f"by more than {YEAR_TOLERANCE}, which is deliberately tight — for",
            "medieval people a five-year difference between two sources is",
            "ordinary rather than alarming, so the list is ranked by how far",
            "apart the two sides actually are and the small ones sink to the",
            "bottom. The threshold is not widened to make this table shorter.",
            "",
        ]
        lines += _table(
            ["person", "item", "property", "we say", "Wikidata says", "apart"],
            [
                [
                    f.person or f.geni_id,
                    _wd(f.qid),
                    PROPERTIES[f.prop][0],
                    f.ours or "—",
                    f.theirs or "—",
                    _gap_text(f),
                ]
                for f in conflicts[:top]
            ],
        )

    suspect = suspect_links(check)
    lines += ["", f"## Links worth re-checking ({len(suspect)})", ""]
    if not suspect:
        lines += [
            "None. Every linked person agrees with their item on at least as "
            "many properties as they conflict on, so each conflict above stands "
            "alone as a disagreement about a fact.",
        ]
    else:
        lines += [
            "The table above lists conflicts one property at a time, which makes "
            "them read as independent errors. Sometimes they are not. Where a "
            "person's father, mother, birth *and* death all disagree, that is one "
            "observation rather than four, and what it is evidence about is the "
            "**link** — not any of the four facts.",
            "",
            "Listed here: people who conflict on more properties than they agree "
            "on, with at least two conflicts. A single conflict is ordinary, and "
            "someone who agrees on more than they conflict on is a sound link "
            "with a data disagreement inside it.",
            "",
        ]
        lines += _table(
            ["person", "item", "agrees", "conflicts", "link"],
            [
                [
                    b.person or b.geni_id,
                    _wd(b.qid),
                    str(b.agrees),
                    str(b.conflicts),
                    ("exact P2600" if exact_links and b.geni_id in exact_links else "inferred")
                    if exact_links is not None
                    else "—",
                ]
                for b in suspect
            ],
        )
        lines += [
            "",
            "**This does not say the links are wrong.** Two readings fit every "
            "row and nothing here separates them: the link is mistaken, or it is "
            "correct and one side's data is badly wrong. For early-medieval "
            "people the second is entirely ordinary — a birth year three "
            "centuries out is a copied error, not proof of mistaken identity. "
            "The `link` column is the one thing that shifts the odds: an "
            "inferred link failing this test is weak evidence twice over, while "
            "an exact P2600 link failing it means the Geni ID on the item is "
            "under as much suspicion as the match.",
        ]

    gaps = check.by_verdict(GAP)
    lines += [
        "",
        f"## Gaps ({len(gaps)})",
        "",
        "Statements we hold that the Wikidata item does not. The eligible ones",
        "are in `out/wikidata/add-claims.qs`; the rest are here for the record.",
        "",
    ]
    by_prop = Counter(f.prop for f in gaps)
    lines += _table(
        ["property", "gaps"],
        [[f"{prop} {PROPERTIES[prop][0]}", str(n)] for prop, n in by_prop.most_common()],
    )

    return "\n".join(lines) + "\n"
