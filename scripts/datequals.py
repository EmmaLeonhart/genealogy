"""The Wikidata qualifiers a GEDCOM date modifier turns into.

**Emma, 2026-08-29:** *"we very much need to have those qualifiers, and I don't know why it is
that you don't. That was almost a prerequisite for putting any Geni information on Wikidata."*

Every `ABT`, `BEF`, `AFT` and `BET x AND y` in the corpus was being emitted as a bare value, which
asserts a date the source explicitly hedges. Measured over `reports/derived-facts.csv`:
**70,665 `about`, 5,923 `after`, 5,907 `before`, 3,004 `between`**.

**The parse was never the missing part.** `derived-facts.csv` has carried `birth_date_modifier`
and `birth_date_year_end` all along and `genimerge.dates` is the authority on the grammar --
`CLAUDE.md` § *GEDCOM dates have a specification* is emphatic that nothing re-parses a date by
hand, and nothing here does. This turns an already-parsed modifier into qualifier text.

## The mapping, from `CLAUDE.md` § *Date qualifiers*, not re-derived

    ABT / EST / CAL   P1480 sourcing circumstances = Q5727902 circa
    BEF               P1326 latest date
    AFT               P1319 earliest date
    BET x AND y       P1319 earliest date + P1326 latest date

**`BEF` and `AFT` bound the value they carry**, so the value itself is the bound: `BEF 1850`
becomes a `P569` of 1850 qualified `P1326` 1850 — *no later than this*. It reads oddly beside the
value until you notice the alternative is asserting 1850 flatly, which is what was happening.

**`BET` needs the second year and has it.** `BET 5 JUL 1735 AND 5 JUL 1737` gives `P1319` at the
value's own precision and `P1326` at the end. **The end is a YEAR even when the start is a full
date**, so the upper bound goes out at precision 9 regardless — claiming day precision on a year
nobody recorded is the exact error this whole change exists against.
"""

#: `Q5727902` *circa* — the `P1480` *sourcing circumstances* value for an approximate date.
CIRCA = "Q5727902"

SOURCING_CIRCUMSTANCES = "P1480"   # sourcing circumstances
EARLIEST_DATE = "P1319"            # earliest date
LATEST_DATE = "P1326"              # latest date

#: A bare year, the only precision an end-year supports.
YEAR_PRECISION = "9"


def year_value(year):
    """`+1737-00-00T00:00:00Z/9` — a year with no month or day claimed."""
    y = str(year or "").strip()
    if not y.lstrip("-").isdigit():
        return ""
    sign = "-" if y.startswith("-") else "+"
    return f"{sign}{abs(int(y)):04d}-00-00T00:00:00Z/{YEAR_PRECISION}"


def date_quals(modifier, iso, precision, year_end=""):
    """Tab-prefixed qualifier text for one date statement, or `""` when unmodified.

    Returns the fragment that follows the value on a QuickStatements line, so the caller writes
    `LAST<TAB>P569<TAB><value><fragment><reference>`.
    """
    mod = (modifier or "").strip().lower()
    value = f"{iso}/{precision}" if iso and precision else ""
    if not value:
        return ""
    if mod in ("about", "estimated", "calculated"):
        return f"\t{SOURCING_CIRCUMSTANCES}\t{CIRCA}"
    if mod == "before":
        return f"\t{LATEST_DATE}\t{value}"
    if mod == "after":
        return f"\t{EARLIEST_DATE}\t{value}"
    if mod == "between":
        end = year_value(year_end)
        if not end:
            # No second year means the range was not parsed as one. Emitting `P1319` alone
            # would say *after* — a different claim from *between* — so nothing is added and
            # the date stands unqualified rather than mis-qualified.
            return ""
        return f"\t{EARLIEST_DATE}\t{value}\t{LATEST_DATE}\t{end}"
    return ""
