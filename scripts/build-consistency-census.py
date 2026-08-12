"""Every "impossible" and "implausible" date finding, with its dates intact.

Emma, 2026-08-11, refusing to treat `reports/consistency.md` as a verdict:
*"it's your job to do analysis on these to figure out what's actually going on
with them. The chances are there is actually something going on with them, and
you're just deeming them impossible or whatever. The chances are there's
something going on with them that's good, and you're just bullshitting your way
around it, so you have to do the research on it."*

**The suspicion is specific and checkable.** `consistency.check` compares
`person.birth_year` against `parent.birth_year` — bare integers. `GedcomDate`
carries `raw`, `modifier` (`about` / `before` / `after` / `between`), `year_end`
for a `BET x AND y` range, and an `is_exact` flag, and **none of it reaches the
comparison**. So a child recorded `ABT 1500` against a parent recorded `ABT 1512`
is reported as born twelve years before their own parent, on two dates that are
each explicitly approximate.

This script does not judge that. It writes one row per finding carrying every
date involved in full, so the question can be answered from the data.

    py scripts/build-consistency-census.py

Writes `reports/consistency-findings.csv`. Offline; reads only the merged GEDCOM.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import consistency, gedcom, model  # noqa: E402

MERGED = REPO_ROOT / "out" / "merged.ged"
OUTPUT = REPO_ROOT / "reports" / "consistency-findings.csv"

#: Which check produced a finding, recovered from its wording. `Finding` does not
#: carry the rule that made it, and inferring it here beats changing the module
#: while its output is under question.
RULES = (
    ("born after their own death", "born-after-own-death"),
    ("a lifespan of", "lifespan-over-120"),
    ("was born in", "born-before-parent-born"),
    ("died in", "born-after-parent-died"),
)

COLUMNS = [
    "kind",
    "rule",
    "detail",
    "person",
    "person_name",
    "person_birth_raw",
    "person_birth_modifier",
    "person_birth_year",
    "person_birth_year_end",
    "person_death_raw",
    "person_death_modifier",
    "person_death_year",
    "person_death_year_end",
    "other",
    "other_name",
    "other_birth_raw",
    "other_birth_modifier",
    "other_birth_year",
    "other_birth_year_end",
    "other_death_raw",
    "other_death_modifier",
    "other_death_year",
    "other_death_year_end",
    "gap_years",
    "all_dates_exact",
    "modifiers_involved",
]


def rule_of(detail: str) -> str:
    for marker, name in RULES:
        if marker in detail:
            return name
    if "when their" in detail:
        return "parent-under-12"
    return "unclassified"


def date_fields(person, kind: str) -> tuple[str, str, str, str]:
    """(raw, modifier, year, year_end) for one event, blanks when absent."""
    if person is None:
        return "", "", "", ""
    event = (person.events or {}).get(kind)
    date = getattr(event, "date", None) if event else None
    if date is None:
        return "", "", "", ""
    return (
        date.raw or "",
        date.modifier or "",
        "" if date.year is None else str(date.year),
        "" if date.year_end is None else str(date.year_end),
    )


def main() -> int:
    print(f"loading {MERGED}", flush=True)
    tree = model.build_tree(gedcom.stream_file(MERGED))
    print(f"{len(tree.people):,} people", flush=True)

    print("running the consistency check", flush=True)
    report = consistency.check(tree)
    print(f"{len(report.findings):,} findings", flush=True)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    exact_total = 0
    with open(OUTPUT, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(COLUMNS)
        for finding in report.findings:
            person = tree.people.get(finding.person)
            other = tree.people.get(finding.other) if finding.other else None

            pb = date_fields(person, "birth")
            pd = date_fields(person, "death")
            ob = date_fields(other, "birth")
            od = date_fields(other, "death")

            modifiers = sorted({m for m in (pb[1], pd[1], ob[1], od[1]) if m})
            # "Exact" means every date that exists on either side of this
            # comparison is a plain date: no ABT, no BEF, no AFT, no range.
            all_exact = not modifiers
            exact_total += all_exact

            years = [int(v) for v in (pb[2], pd[2], ob[2], od[2]) if v]
            gap = max(years) - min(years) if len(years) > 1 else ""

            writer.writerow(
                [
                    finding.kind,
                    rule_of(finding.detail),
                    finding.detail,
                    finding.person or "",
                    getattr(person, "display_name", "") if person else "",
                    *pb,
                    *pd,
                    finding.other or "",
                    getattr(other, "display_name", "") if other else "",
                    *ob,
                    *od,
                    gap,
                    "yes" if all_exact else "no",
                    "+".join(modifiers),
                ]
            )

    size = OUTPUT.stat().st_size
    total = len(report.findings)
    print(f"wrote {OUTPUT} — {total:,} rows, {size/1024:.0f} KB")
    print(
        f"{exact_total:,} of {total:,} ({100.0*exact_total/max(total,1):.1f}%) "
        "involve only exact dates"
    )
    print(
        f"{total - exact_total:,} ({100.0*(total-exact_total)/max(total,1):.1f}%) "
        "involve at least one date the export itself marked approximate or open-ended"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
