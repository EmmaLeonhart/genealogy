"""Dates in the tree that contradict each other.

The asymmetry between fathers and mothers is the design decision worth testing
hardest: a child born shortly after its father dies is ordinary, and the same
thing on the mother's side is not possible. Sixteen such births are in the real
tree, and treating them together would report defects that are not there.
"""

import pytest

from genimerge import consistency, gedcom
from genimerge.model import build_tree


def tree(*texts):
    records = []
    for text in texts:
        records += gedcom.parse(text).records
    return build_tree(records)


def family(child_birth=None, father=None, mother=None, child_death=None):
    """A child with one or both parents, each with optional birth/death years.

    `father` and `mother` are (birth, death) pairs; either part may be None.
    """
    lines = ["0 HEAD"]

    def person(xref, name, years):
        block = [f"0 @{xref}@ INDI", f"1 NAME {name} /Test/"]
        birth, death = years or (None, None)
        if birth is not None:
            block += ["1 BIRT", f"2 DATE {birth}"]
        if death is not None:
            block += ["1 DEAT", f"2 DATE {death}"]
        return block

    lines += person("I1", "Child", (child_birth, child_death))
    lines += ["1 FAMC @F1@"]
    if father:
        lines += person("I2", "Father", father) + ["1 FAMS @F1@"]
    if mother:
        lines += person("I3", "Mother", mother) + ["1 FAMS @F1@"]
    lines += ["0 @F1@ FAM"]
    if father:
        lines += ["1 HUSB @I2@"]
    if mother:
        lines += ["1 WIFE @I3@"]
    lines += ["1 CHIL @I1@", "0 TRLR", ""]
    return "\n".join(lines)


def kinds(report):
    return [(f.kind, f.detail) for f in report.findings]


# --- one person's own dates -------------------------------------------------


def test_born_after_their_own_death_is_impossible():
    report = consistency.check(tree(family(child_birth=1900, child_death=1850)))

    assert [f.kind for f in report.findings] == [consistency.IMPOSSIBLE]
    assert "born after their own death" in report.findings[0].detail


def test_a_lifespan_over_the_maximum_is_implausible_not_impossible():
    report = consistency.check(tree(family(child_birth=1700, child_death=1900)))

    assert [f.kind for f in report.findings] == [consistency.IMPLAUSIBLE]
    assert "200 years" in report.findings[0].detail


def test_an_ordinary_lifespan_is_not_reported():
    assert consistency.check(tree(family(child_birth=1800, child_death=1870))).findings == []


def test_a_lifespan_exactly_at_the_maximum_is_not_reported():
    """The boundary is a judgement, so it must at least be a stated one."""
    at_limit = family(child_birth=1800, child_death=1800 + consistency.MAX_LIFESPAN)

    assert consistency.check(tree(at_limit)).findings == []


# --- against a parent -------------------------------------------------------


def test_born_before_a_parent_was_born_is_impossible():
    report = consistency.check(tree(family(child_birth=1800, mother=(1850, None))))

    assert [f.kind for f in report.findings] == [consistency.IMPOSSIBLE]
    assert "before their mother" in report.findings[0].detail


def test_a_parent_under_the_minimum_age_is_implausible():
    report = consistency.check(tree(family(child_birth=1808, father=(1800, None))))

    assert [f.kind for f in report.findings] == [consistency.IMPLAUSIBLE]
    assert "was 8" in report.findings[0].detail


def test_a_parent_of_ordinary_age_is_not_reported():
    assert consistency.check(tree(family(child_birth=1830, father=(1800, None)))).findings == []


# --- the father/mother asymmetry, which is the point ------------------------


def test_a_child_born_after_its_mother_died_is_impossible():
    report = consistency.check(tree(family(child_birth=1851, mother=(1800, 1850))))

    assert [f.kind for f in report.findings] == [consistency.IMPOSSIBLE]
    assert "after their mother" in report.findings[0].detail


def test_a_child_born_within_a_year_of_its_father_dying_is_ordinary():
    """Sixteen of these are in the real tree. Reporting them would be wrong."""
    report = consistency.check(tree(family(child_birth=1851, father=(1800, 1850))))

    assert report.findings == []


def test_a_child_born_well_after_its_father_died_is_still_impossible():
    report = consistency.check(tree(family(child_birth=1855, father=(1800, 1850))))

    assert [f.kind for f in report.findings] == [consistency.IMPOSSIBLE]
    assert "after their father" in report.findings[0].detail


def test_the_grace_window_is_not_extended_to_mothers():
    """The same year that is forgiven for a father must not be for a mother."""
    year = 1851
    father = consistency.check(tree(family(child_birth=year, father=(1800, 1850))))
    mother = consistency.check(tree(family(child_birth=year, mother=(1800, 1850))))

    assert father.findings == []
    assert [f.kind for f in mother.findings] == [consistency.IMPOSSIBLE]


# --- the report -------------------------------------------------------------


def test_findings_carry_both_people_so_a_row_can_be_opened():
    report = consistency.check(tree(family(child_birth=1800, mother=(1850, None))))
    finding = report.findings[0]

    assert finding.person == "1"
    assert finding.other == "3"


def test_a_clean_tree_reports_nothing_and_says_so():
    t = tree(family(child_birth=1830, father=(1800, 1880), mother=(1805, 1875)))
    report = consistency.check(t)

    markdown = consistency.render_markdown(t, report)

    assert report.findings == []
    assert "## Impossible (0)" in markdown
    assert "## Implausible (0)" in markdown


def test_the_report_says_the_errors_are_not_ours_to_fix():
    t = tree(family(child_birth=1800, mother=(1850, None)))

    markdown = consistency.render_markdown(t, consistency.check(t))

    assert "errors in Geni's data, not in the merge" in markdown
    assert "nothing here is fixed automatically" in markdown.lower()


def test_the_report_explains_the_father_allowance():
    """A reader must not think posthumous births were simply missed."""
    t = tree(family(child_birth=1800, mother=(1850, None)))

    markdown = consistency.render_markdown(t, consistency.check(t))

    assert "within a year of its father's death is ordinary" in markdown
    assert "no such allowance on the mother's side" in markdown


def test_the_report_warns_that_these_dates_reach_wikidata():
    t = tree(family(child_birth=1800, mother=(1850, None)))

    markdown = consistency.render_markdown(t, consistency.check(t))

    assert "P569" in markdown and "P570" in markdown


def test_impossible_findings_are_listed_before_implausible_ones():
    t = tree(
        family(child_birth=1808, father=(1800, None)),      # implausible
        family(child_birth=1700, mother=(1750, None)),      # impossible
    )

    report = consistency.check(t)

    assert report.findings[0].kind == consistency.IMPOSSIBLE


def test_the_listing_is_capped_but_the_count_is_not():
    t = tree(*[family(child_birth=1800, mother=(1850, None)) for _ in range(1)])
    report = consistency.check(t)
    report.findings = report.findings * 5          # five identical findings

    markdown = consistency.render_markdown(t, report, top=2)

    assert "## Impossible (5)" in markdown
    assert "Showing the first 2." in markdown


def test_people_with_no_dates_at_all_are_not_findings():
    """Most of this tree has no years; absence is not a contradiction."""
    report = consistency.check(tree(family()))

    assert report.findings == []
    assert report.people_with_a_year == 0
    assert report.people_checked == 1
