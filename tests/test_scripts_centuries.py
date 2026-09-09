"""The century labelling in `scripts/build-centuries.py`.

**Why this file exists.** `scripts/` holds report generators and none of them
had tests, on the reasoning that they are one-shot and their output gets read by
a human. `century_of` fell straight through that gap on 2026-08-10: it returned
the century *ordinal* formatted as a year range, so 1950 came out `2000s` and
2001 came out `2100s`. Every label in `reports/centuries.md` was a hundred years
late, the report claimed 225 Wikidata items were born in the 2100s, and the
conclusion drawn about which era each tree covers was inverted. The table looked
entirely reasonable — internally consistent, plausibly shaped — and the error
surfaced only because Emma asked to look at the future birth dates.

A pure function with an obvious contract is exactly what a test is cheap for.
The rest of the script reads 2.7 GB and is not tested here.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build-centuries.py"
_spec = importlib.util.spec_from_file_location("build_centuries", _PATH)
build_centuries = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_centuries)

century_of = build_centuries.century_of
_gedcom_year = build_centuries._gedcom_year


@pytest.mark.parametrize(
    "year,label",
    [
        (1950, "1900s"),   # the bug: this returned "2000s"
        (2001, "2000s"),   # the bug: this returned "2100s", and read as impossible
        (1900, "1900s"),
        (1999, "1900s"),
        (1800, "1800s"),
        (1801, "1800s"),
        (100, "100s"),
        (999, "900s"),
        (2026, "2000s"),
    ],
)
def test_a_year_lands_in_the_range_that_contains_it(year, label):
    assert century_of(year) == label


def test_the_label_is_a_year_range_not_a_century_ordinal():
    # 1950 is in the 20th century and in the 1900s. The label is the second
    # thing. Conflating them is what produced a report a hundred years out.
    assert century_of(1950) == "1900s"
    assert century_of(1950) != "2000s"


def test_every_year_in_a_range_gets_the_same_label():
    assert {century_of(y) for y in range(1800, 1900)} == {"1800s"}


def test_bce_and_the_first_century_do_not_fall_off_the_end():
    assert century_of(0) == "BCE"
    assert century_of(-44) == "BCE"
    assert century_of(50) == "0s"


@pytest.mark.parametrize(
    "text,year",
    [
        ("1950", 1950),
        ("3 OCT 270", 270),
        ("ABT 1420", 1420),
        # A range reports its *start*; `GedcomDate.year_end` carries the other
        # end. The first version of this test asserted 1410, from a comment I
        # had written claiming dates.py took the end. It does not.
        ("BET 1400 AND 1410", 1400),
        # The one that mattered: Geni writes BC as a minus, and the hand-rolled
        # parser this replaced used `str.isdigit()`, which is False for "-73".
        # It dropped all 4,750 negative-year DATE lines in the corpus in silence.
        ("-73", -73),
        ("ABT -95", -95),
        ("BEF -1310", -1310),
        ("", None),
        ("ABT", None),
    ],
)
def test_the_gedcom_year_comes_from_the_repos_own_parser(text, year):
    assert _gedcom_year(text) == year
