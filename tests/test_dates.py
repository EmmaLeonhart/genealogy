import pytest

from genimerge.dates import parse_date


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("26 FEB 1996", (1996, 2, 26)),
        ("SEP 1930", (1930, 9, None)),
        ("1575", (1575, None, None)),
    ],
)
def test_exact_dates_parse_to_their_parts(raw, expected):
    date = parse_date(raw)

    assert (date.year, date.month, date.day) == expected
    assert date.modifier is None
    assert date.is_exact


@pytest.mark.parametrize(
    "raw,modifier,year",
    [
        ("ABT 1275", "about", 1275),
        ("EST 1275", "about", 1275),
        ("CAL 1275", "about", 1275),
        ("BEF 1490", "before", 1490),
        ("AFT 1120", "after", 1120),
        ("ABT 8 APR 1196", "about", 1196),
        ("BEF 3 AUG 1788", "before", 1788),
        ("ABT OCT 1138", "about", 1138),
    ],
)
def test_modifiers_are_kept_rather_than_flattened(raw, modifier, year):
    date = parse_date(raw)

    assert (date.modifier, date.year) == (modifier, year)
    assert not date.is_exact


def test_a_range_keeps_both_ends():
    date = parse_date("BET 1715 AND 1724")

    assert (date.modifier, date.year, date.year_end) == ("between", 1715, 1724)


def test_a_range_with_full_dates_keeps_the_start_precisely():
    date = parse_date("BET 25 JUL 1106 AND 25 JUL 1112")

    assert (date.year, date.month, date.day, date.year_end) == (1106, 7, 25, 1112)


def test_precision_follows_wikidatas_scale():
    assert parse_date("26 FEB 1996").precision == 11
    assert parse_date("SEP 1930").precision == 10
    assert parse_date("1575").precision == 9
    assert parse_date("gibberish").precision is None


def test_iso_form_pads_unknown_parts_with_zeroes():
    assert parse_date("26 FEB 1996").iso() == "+1996-02-26T00:00:00Z"
    assert parse_date("SEP 1930").iso() == "+1930-09-00T00:00:00Z"
    assert parse_date("1575").iso() == "+1575-00-00T00:00:00Z"


def test_an_unreadable_date_reports_nothing_rather_than_guessing():
    date = parse_date("sometime in the reign of Harald")

    assert date.year is None
    assert date.precision is None
    assert date.iso() is None
    assert date.raw == "sometime in the reign of Harald"


def test_a_day_with_no_month_drops_the_day_instead_of_inventing_one():
    # "7  2011" occurs twice in the corpus. A day is meaningless without a
    # month, and attaching it to a guessed month would be worse than losing it.
    date = parse_date("7  2011")

    assert (date.year, date.month, date.day) == (2011, None, None)


def test_an_empty_date_is_empty_not_an_error():
    assert parse_date("").year is None
    assert parse_date(None).raw == ""


def test_an_unknown_month_name_is_not_forced_into_a_number():
    assert parse_date("26 FOO 1996").year is None


def test_lowercase_input_is_accepted():
    assert parse_date("abt 1275").modifier == "about"


# --- BC years -------------------------------------------------------------
#
# Geni writes them with a minus rather than GEDCOM 5.5.1's "73 B.C.". The
# parser rejected every one until 2026-08-05, and since an unreadable date is
# dropped silently by design, 4,459 events -- the whole pre-Christian era,
# Jimmu and Makeda included -- carried year=None with nothing to show for it.


@pytest.mark.parametrize(
    "text, year",
    [
        ("-73", -73),
        ("-16", -16),
        ("-1310", -1310),
        ("-3112", -3112),
    ],
)
def test_a_negative_year_is_read_as_bc(text, year):
    assert parse_date(text).year == year


@pytest.mark.parametrize(
    "text, year, modifier",
    [
        ("ABT -95", -95, "about"),
        ("BEF -1310", -1310, "before"),
        ("AFT -500", -500, "after"),
    ],
)
def test_modifiers_apply_to_negative_years_too(text, year, modifier):
    date = parse_date(text)
    assert (date.year, date.modifier) == (year, modifier)


def test_a_bc_range_keeps_both_ends():
    date = parse_date("BET -100 AND -50")
    assert (date.year, date.year_end, date.modifier) == (-100, -50, "between")


def test_a_negative_year_formats_as_a_wikidata_time():
    """`iso()` always handled this; nothing ever reached it."""
    assert parse_date("-73").iso() == "-0073-00-00T00:00:00Z"
    assert parse_date("12 JAN -44").iso() == "-0044-01-12T00:00:00Z"


def test_a_bare_short_number_is_still_not_a_year():
    """The minus is what licenses 1-2 digits; a positive year still needs 3.

    Otherwise a stray "7" in a malformed date becomes the year 7, which is the
    reason the original regex demanded three digits.
    """
    assert parse_date("7").year is None
    assert parse_date("42").year is None
    assert parse_date("-7").year == -7
