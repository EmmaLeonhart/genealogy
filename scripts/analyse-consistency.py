"""What is actually going on with the "impossible" dates.

Emma, 2026-08-11: *"The chances are there is actually something going on with
them, and you're just deeming them impossible or whatever… you have to do the
research on it."*

**The finding, in one line:** `consistency.check` compares bare integers, so a
child recorded `ABT 1500` against a parent recorded `ABT 1512` is reported as an
impossibility on two dates neither of which the source asserts.

This re-checks every finding treating a date as the **interval it actually
denotes**:

* `ABT` / `EST` / `CAL` → year ± a tolerance
* `BEF y` → (−∞, y]
* `AFT y` → [y, +∞)
* `BET x AND y` → [x, y]
* a plain year → [y, y]

A contradiction is only real when the intervals **cannot** be reconciled. The
tolerance for `ABT` is not a constant this file invents — survival is reported
at 0, 2, 5 and 10 years so the sensitivity is visible and Emma can choose.

Reads `reports/consistency-findings.csv`. Writes `reports/consistency-analysis.md`
and `reports/consistency-surviving.csv` — every finding that survives at ±5, one
row each.

    py scripts/analyse-consistency.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "reports" / "consistency-findings.csv"
OUT_MD = REPO_ROOT / "reports" / "consistency-analysis.md"
OUT_CSV = REPO_ROOT / "reports" / "consistency-surviving.csv"

TOLERANCES = (0, 2, 5, 10)
INF = 10**9


def interval(year: str, year_end: str, modifier: str, tolerance: int):
    """The span a GEDCOM date actually denotes, or None when there is no year."""
    if not year:
        return None
    y = int(year)
    if modifier == "about":
        return (y - tolerance, y + tolerance)
    if modifier == "before":
        return (-INF, y)
    if modifier == "after":
        return (y, INF)
    if modifier == "between":
        return (y, int(year_end) if year_end else y)
    return (y, y)


def can_be_at_most(span, other) -> bool:
    """Could a value in ``span`` be <= a value in ``other``?"""
    return span[0] <= other[1]


def survives(row: dict, tolerance: int) -> bool:
    """True when the contradiction holds even reading dates as intervals."""
    pb = interval(row["person_birth_year"], row["person_birth_year_end"], row["person_birth_modifier"], tolerance)
    pd = interval(row["person_death_year"], row["person_death_year_end"], row["person_death_modifier"], tolerance)
    ob = interval(row["other_birth_year"], row["other_birth_year_end"], row["other_birth_modifier"], tolerance)
    od = interval(row["other_death_year"], row["other_death_year_end"], row["other_death_modifier"], tolerance)
    rule = row["rule"]

    if rule == "born-after-own-death":
        # Real only if birth cannot possibly precede death.
        return not (pb and pd and can_be_at_most(pb, pd))
    if rule == "lifespan-over-120":
        # Real only if even the shortest compatible lifespan exceeds 120.
        if not (pb and pd):
            return False
        return pd[0] - pb[1] > 120
    if rule == "born-before-parent-born":
        return not (pb and ob and can_be_at_most(ob, pb))
    if rule == "parent-under-12":
        if not (pb and ob):
            return False
        # The finding survives only if the parent is *necessarily* under 12 —
        # that is, even the widest reading of both dates cannot make them older.
        # Asking whether the *minimum* age is under 12 instead makes every
        # finding survive at every tolerance, which is how this was caught.
        return pb[1] - ob[0] < 12
    if rule == "born-after-parent-died":
        # A father gets a year of grace for a posthumous birth.
        grace = 1 if "father" in row["detail"] else 0
        if not (pb and od):
            return False
        return pb[0] > od[1] + grace
    return True


def main() -> int:
    rows = list(csv.DictReader(open(SOURCE, encoding="utf-8", newline="")))
    total = len(rows)
    print(f"{total:,} findings")

    by_rule: Counter[str] = Counter()
    by_rule_kind: dict[str, str] = {}
    exact_by_rule: Counter[str] = Counter()
    survival: dict[int, Counter[str]] = {t: Counter() for t in TOLERANCES}
    examples: dict[str, list[dict]] = defaultdict(list)
    killed: dict[str, list[dict]] = defaultdict(list)

    for row in rows:
        rule = row["rule"]
        by_rule[rule] += 1
        by_rule_kind[rule] = row["kind"]
        if row["all_dates_exact"] == "yes":
            exact_by_rule[rule] += 1
        for t in TOLERANCES:
            if survives(row, t):
                survival[t][rule] += 1
        if survives(row, 5):
            if len(examples[rule]) < 8:
                examples[rule].append(row)
        elif len(killed[rule]) < 8:
            killed[rule].append(row)

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            if survives(row, 5):
                writer.writerow(row)

    def fmt(row: dict) -> str:
        who = f"`{row['person']}` {row['person_name']}"
        dates = f"b {row['person_birth_raw'] or '—'} / d {row['person_death_raw'] or '—'}"
        if row["other"]:
            dates += f" · other `{row['other']}` {row['other_name']}: b {row['other_birth_raw'] or '—'} / d {row['other_death_raw'] or '—'}"
        return f"| {who} | {dates} |"

    L: list[str] = []
    add = L.append
    add("# The \"impossible\" dates: what is actually going on with them")
    add("")
    add("**Emma, 2026-08-11:** *\"it's your job to do analysis on these to figure out")
    add("what's actually going on with them. The chances are there is actually something")
    add("going on with them, and you're just deeming them impossible or whatever… you have")
    add("to do the research on it.\"*")
    add("")
    add("She was right, and the mechanism is specific.")
    add("")
    add("## The defect")
    add("")
    add("`consistency.check` compares `person.birth_year` against `parent.birth_year` —")
    add("**bare integers**. `GedcomDate` already carries `raw`, `modifier`, `year_end` and")
    add("`is_exact`, and none of it reaches the comparison. So a child recorded `ABT 1500`")
    add("against a parent recorded `ABT 1512` is reported as born twelve years before their")
    add("own parent, on two dates that the source explicitly declines to assert.")
    add("")
    add(f"**{total - sum(1 for r in rows if r['all_dates_exact'] == 'yes'):,} of {total:,} findings")
    add(f"({100.0*(total - sum(1 for r in rows if r['all_dates_exact'] == 'yes'))/total:.1f}%)")
    add("involve at least one date carrying `ABT`, `BEF`, `AFT` or `BET`.**")
    add("")
    add("## What survives when a date is read as the interval it denotes")
    add("")
    add("`ABT` becomes year ± tolerance; `BEF y` becomes (−∞, y]; `AFT y` becomes [y, +∞);")
    add("`BET x AND y` becomes [x, y]; a plain year stays a point. A contradiction is real")
    add("only when the intervals cannot be reconciled at all.")
    add("")
    add("**The `ABT` tolerance is not chosen here.** Survival is given at four values so")
    add("the sensitivity is visible and the choice is Emma's.")
    add("")
    header = "| rule | kind | findings | all dates exact |" + "".join(f" ±{t} |" for t in TOLERANCES)
    add(header)
    add("| --- | --- | ---: | ---: |" + " ---: |" * len(TOLERANCES))
    for rule, n in by_rule.most_common():
        cells = "".join(f" {survival[t][rule]:,} |" for t in TOLERANCES)
        add(f"| {rule} | {by_rule_kind[rule]} | {n:,} | {exact_by_rule[rule]:,} |{cells}")
    tot_cells = "".join(f" {sum(survival[t].values()):,} |" for t in TOLERANCES)
    add(f"| **total** | | **{total:,}** | **{sum(exact_by_rule.values()):,}** |{tot_cells}")
    add("")
    at5 = sum(survival[5].values())
    add(f"**At ±5 years, {at5:,} of {total:,} findings survive — {100.0*at5/total:.1f}%.**")
    add(f"The other {total-at5:,} are artefacts of comparing approximations as if they were")
    add("assertions.")
    add("")
    add("## What the surviving findings look like")
    add("")
    add("Every one is in `reports/consistency-surviving.csv`. Up to eight per rule here.")
    add("")
    for rule, _ in by_rule.most_common():
        if not examples[rule]:
            continue
        add(f"### {rule} — survives")
        add("")
        add("| person | dates |")
        add("| --- | --- |")
        for row in examples[rule]:
            add(fmt(row))
        add("")
    add("## What the check was reporting that it should not have been")
    add("")
    add("Up to eight per rule, all of them dissolved by reading the modifier.")
    add("")
    for rule, _ in by_rule.most_common():
        if not killed[rule]:
            continue
        add(f"### {rule} — dissolves")
        add("")
        add("| person | dates |")
        add("| --- | --- |")
        for row in killed[rule]:
            add(fmt(row))
        add("")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV} ({at5:,} rows)")
    for t in TOLERANCES:
        s = sum(survival[t].values())
        print(f"  tolerance ±{t:2}: {s:,} survive ({100.0*s/total:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
