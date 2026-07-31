from genimerge import coverage, gedcom
from genimerge.coverage import CoverageInput
from genimerge.model import build_tree

TREE = """0 HEAD
0 @I1@ INDI
1 NAME Old /King/
1 BIRT
2 DATE 1100
1 FAMS @F1@
0 @I2@ INDI
1 NAME Queen /Consort/
1 BIRT
2 DATE 1105
1 FAMS @F1@
0 @I3@ INDI
1 NAME Middle /Noble/
1 BIRT
2 DATE 1140
1 FAMC @F1@
0 @I4@ INDI
1 NAME Recent /Farmer/
1 BIRT
2 DATE 1780
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
0 TRLR
"""


def _input(**kwargs):
    return CoverageInput(tree=build_tree(gedcom.parse(TREE).records), **kwargs)


def test_link_sources_are_counted_separately():
    # An exact identifier match and an inferred one are not the same claim, and
    # a single "matched" number would say they are.
    text = coverage.render_markdown(
        _input(by_p2600={"1": "Q1"}, by_expansion={"2": "Q2"})
    )

    assert "| **linked by P2600** (exact Geni ID on the Wikidata item) | 1 | 25.0% |" in text
    assert "| **linked by expansion** (family structure + name + dates) | 1 | 25.0% |" in text
    assert "| **linked, total** | 2 | 50.0% |" in text


def test_proposals_are_reported_but_not_counted_as_linked():
    text = coverage.render_markdown(
        _input(
            by_p2600={"1": "Q1"},
            proposals=[("3", "Q3", "medium", "name-search")],
        )
    )

    assert "| **linked, total** | 1 | 25.0% |" in text
    assert "| proposed, awaiting review | 1 | 25.0% |" in text
    assert "Nothing here has been accepted." in text


def test_a_proposal_for_an_already_linked_person_is_not_double_counted():
    text = coverage.render_markdown(
        _input(by_p2600={"1": "Q1"}, proposals=[("1", "Q9", "low", "name-search")])
    )

    assert "| proposed, awaiting review | 0 | 0.0% |" in text


def test_the_remainder_adds_up():
    text = coverage.render_markdown(
        _input(by_p2600={"1": "Q1"}, proposals=[("3", "Q3", "high", "father")])
    )

    # 4 people: 1 linked, 1 proposed, 2 neither.
    assert "| no link and no proposal | 2 | 50.0% |" in text
    assert "| **tree total** | 4 | 100% |" in text


def test_coverage_is_broken_down_by_century():
    text = coverage.render_markdown(_input(by_p2600={"1": "Q1"}))

    assert "| 1100s | 3 | 1 | 33.3%" in text
    assert "| 1700s | 1 | 0 | 0.0%" in text


def test_people_with_no_birth_year_get_their_own_bucket():
    no_dates = TREE.replace("1 BIRT\n2 DATE 1780\n", "")
    tree = build_tree(gedcom.parse(no_dates).records)

    assert "| unknown | 1 |" in coverage.render_markdown(CoverageInput(tree=tree))


def test_distance_from_a_link_is_reported():
    text = coverage.render_markdown(_input(by_p2600={"1": "Q1"}))

    # Queen and Middle are one step from Old King; Recent Farmer is unreachable.
    assert "| 1 | 2 |" in text
    assert "| unreachable | 1 |" in text


def test_the_biggest_gaps_are_ranked_by_descendants():
    text = coverage.render_markdown(_input(by_p2600={"1": "Q1"}), top_gaps=3)
    body = text.split("biggest unlinked people")[1]

    # Queen Consort has a descendant; the others have none, so she leads.
    assert body.index("Queen Consort") < body.index("Recent Farmer")


def test_an_empty_input_still_renders():
    text = coverage.render_markdown(_input())

    assert "# Wikidata coverage" in text
    assert "| **linked, total** | 0 | 0.0% |" in text
