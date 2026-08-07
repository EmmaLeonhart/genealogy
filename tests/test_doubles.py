"""Wikidata items claiming two of our people are one person.

The interesting behaviour is entirely selection and ranking, so these build a
tiny tree and a handful of (QID, Geni ID) pairs rather than going near the real
15 MB map.
"""

from pathlib import Path

import pytest

from genimerge import doubles, gedcom
from genimerge.model import build_tree

REPO = Path(__file__).resolve().parents[1]
REAL_PAIRS = REPO / "out" / "wikidata" / "p2600-all.tsv"

# Two profiles for what may be one man (they share a child), one unrelated
# woman, and a fourth person nobody claims.
TINY = """0 HEAD
0 @I100@ INDI
1 NAME Bracheslav /Polozki/
1 SEX M
1 BIRT
2 DATE 1104
1 FAMS @F1@
0 @I200@ INDI
1 NAME Bracheslav /Polozki/
1 SEX M
1 FAMS @F2@
0 @I300@ INDI
1 NAME Scribonia
1 SEX F
1 BIRT
2 DATE 70
0 @I400@ INDI
1 NAME Clodia /Pulchra/
1 SEX F
1 BIRT
2 DATE 1500
0 @I500@ INDI
1 NAME A Child
1 FAMC @F1@
1 FAMC @F2@
0 @F1@ FAM
1 HUSB @I100@
1 CHIL @I500@
0 @F2@ FAM
1 HUSB @I200@
1 CHIL @I500@
0 TRLR
"""


def tree():
    built = build_tree(list(gedcom.parse(TINY).records))
    built.resolve_relationships()
    return built


def test_an_item_with_one_id_is_not_a_double():
    found = doubles.find_doubles([("Q1", "100")], tree())

    assert found == []


def test_an_item_with_two_ids_we_hold_is_a_double():
    found = doubles.find_doubles([("Q1", "100"), ("Q1", "200")], tree())

    assert len(found) == 1
    assert [p.geni_id for p in found[0].people] == ["100", "200"]


def test_an_item_whose_second_id_we_do_not_hold_is_not_a_double():
    """The point of the report is two people *in our tree*. An ID we have never
    seen is a person to import, not a judgement to make."""
    found = doubles.find_doubles([("Q1", "100"), ("Q1", "999")], tree())

    assert found == []


def test_ids_we_lack_are_still_recorded_on_a_real_double():
    """An item naming three IDs of which we hold two is a different situation
    from one naming exactly the two we hold, so the count is kept."""
    found = doubles.find_doubles([("Q1", "100"), ("Q1", "200"), ("Q1", "999")], tree())

    assert found[0].absent_ids == ["999"]


def test_a_repeated_pair_counts_once():
    found = doubles.find_doubles([("Q1", "100"), ("Q1", "100"), ("Q1", "200")], tree())

    assert len(found) == 1
    assert len(found[0].people) == 2


# -- the signals a human reads -----------------------------------------


def test_sharing_a_child_is_sharing_a_relative():
    """The strongest evidence available without leaving our own data: two
    profiles for one person usually keep some of the same family."""
    found = doubles.find_doubles([("Q1", "100"), ("Q1", "200")], tree())

    assert found[0].shares_a_relative
    assert found[0].same_name


def test_two_unrelated_people_share_neither_kin_nor_name():
    found = doubles.find_doubles([("Q9", "300"), ("Q9", "400")], tree())

    assert not found[0].shares_a_relative
    assert not found[0].same_name


def test_births_more_than_a_lifetime_apart_are_flagged():
    """Scribonia at 70 against Clodia at 1500 cannot be one person."""
    found = doubles.find_doubles([("Q9", "300"), ("Q9", "400")], tree())

    assert found[0].years_conflict


def test_a_missing_year_never_triggers_the_conflict_flag():
    """Most of these profiles carry no year, and absence is not disagreement."""
    found = doubles.find_doubles([("Q1", "100"), ("Q1", "200")], tree())

    assert not found[0].years_conflict


def test_rows_that_share_a_relative_come_first():
    found = doubles.find_doubles(
        [("Q9", "300"), ("Q9", "400"), ("Q1", "100"), ("Q1", "200")], tree()
    )

    assert [d.qid for d in found] == ["Q1", "Q9"]


# -- rendering ---------------------------------------------------------


def test_the_page_links_both_profiles_and_the_item():
    found = doubles.find_doubles([("Q1", "100"), ("Q1", "200")], tree())

    page = doubles.render_html(found, tree(), 5)

    assert "https://www.wikidata.org/wiki/Q1" in page
    assert "https://www.geni.com/people/x/100" in page
    assert "https://www.geni.com/people/x/200" in page
    assert page.startswith("<!doctype html>")


def test_the_page_says_it_is_not_a_duplicate_list():
    """The one thing a reader must not take away from it."""
    page = doubles.render_html([], tree(), 5)

    assert "not a duplicate list" in page.casefold()


def test_markdown_renders_with_no_doubles_at_all():
    assert doubles.render_markdown([], tree(), 5)


# -- the real map ------------------------------------------------------


@pytest.mark.skipif(
    not REAL_PAIRS.exists(), reason="out/wikidata/p2600-all.tsv absent (run `overlap`)"
)
def test_the_real_pairs_file_parses():
    """`load_pairs` against the file `overlap` actually writes. `out/` is
    gitignored, so this skips on a clean checkout rather than failing."""
    pairs = doubles.load_pairs(REAL_PAIRS)

    assert pairs
    assert all(q.startswith("Q") for q, _ in pairs[:100])
