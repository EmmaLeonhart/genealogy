"""Remoteness — the ranking that replaced a greedy list of pairs.

The claim each row makes is stronger than `distant`'s, so there is more to pin.
Row 1 must really be the most remote person, not the first one found; the
reported number must never exceed the truth, since it is offered as "how far
apart our tree says these two are"; and any two rows must be genuinely far
apart rather than the same lineage listed twice, which is the specific failure
that made the earlier report read as arbitrary.
"""

import pytest

from genimerge import gedcom, remote
from genimerge.frontier import family_graph
from genimerge.model import build_tree


def tree_from(records: str):
    return build_tree(list(gedcom.parse(records).records))


def chain(n: int, first: int = 1, surname: str = "Chain") -> str:
    """A line of `n` people, each the child of the one before."""
    out = []
    for i in range(first, first + n):
        out.append(f"0 @I{i}@ INDI\n1 NAME Person{i} /{surname}/\n1 SEX M")
    for i in range(first, first + n - 1):
        out.append(f"0 @F{i}@ FAM\n1 HUSB @I{i}@\n1 CHIL @I{i+1}@")
    return "\n".join(out)


def wrap(body: str) -> str:
    return "0 HEAD\n" + body + "\n0 TRLR\n"


def exact_eccentricity(graph, node):
    dist = remote.bfs(graph, node)
    return max(dist.values())


# --- the measurement --------------------------------------------------------


def test_the_ends_of_a_chain_are_its_most_remote_people():
    tree = tree_from(wrap(chain(60)))

    people = remote.most_remote(tree, count=2)

    assert people[0].geni_id in {"1", "60"}
    assert people[0].remoteness == 59


def test_the_number_is_never_larger_than_the_true_eccentricity():
    """It is a max over landmarks, and a landmark is a real person.

    This is the property the report leans on when it says the figure is a lower
    bound: a row may understate how remote someone is, never overstate it.
    """
    tree = tree_from(wrap(chain(40) + "\n" + chain(30, first=100, surname="Branch")))
    graph = family_graph(tree)

    for person in remote.most_remote(tree, count=10):
        assert person.remoteness <= exact_eccentricity(graph, person.geni_id)


def test_the_partner_really_is_that_far_away():
    """The pair is what gets opened on Geni, so the hop count must be theirs."""
    tree = tree_from(wrap(chain(60)))
    graph = family_graph(tree)

    person = remote.most_remote(tree, count=1)[0]

    assert remote.bfs(graph, person.geni_id)[person.partner_id] == person.remoteness


# --- the separation guarantee -----------------------------------------------


def test_two_rows_are_never_near_neighbours():
    """The failure that made the pair report read as arbitrary.

    A star of long arms: everyone at the tip of an arm has nearly the maximum
    eccentricity, so an unfiltered ranking lists one arm's last twenty people
    before it reaches a second arm.
    """
    body = [chain(40)]
    # three more arms, each joined to person 1. The joining family needs a
    # numeric xref like any other: `@FJ1@` parses to no Geni ID, the family is
    # dropped, and the star silently becomes four separate chains.
    for arm, first in enumerate((100, 200, 300), start=1):
        body.append(chain(40, first=first, surname=f"Arm{arm}"))
        body.append(f"0 @F{9000 + arm}@ FAM\n1 HUSB @I1@\n1 CHIL @I{first}@")
    tree = tree_from(wrap("\n".join(body)))
    graph = family_graph(tree)

    people = remote.most_remote(tree, count=4)

    assert len(people) >= 2
    for i, one in enumerate(people):
        for other in people[i + 1:]:
            assert remote.bfs(graph, one.geni_id)[other.geni_id] >= 15


def test_the_second_row_is_never_the_first_one_backwards():
    """A's furthest person is B, so B's furthest person is A.

    Without retiring both ends, the two most remote people in any tree are the
    same pair listed twice — which is what the first run against the real merge
    produced at rows 1 and 2.
    """
    tree = tree_from(wrap(chain(60)))

    people = remote.most_remote(tree, count=5)

    named = [p.geni_id for p in people]
    assert len(named) == len(set(named))
    for person in people[1:]:
        assert person.geni_id != people[0].partner_id


def test_the_number_folded_away_is_reported():
    """A short table must read as "few distinct corners", not "found little"."""
    tree = tree_from(wrap(chain(60)))

    remote.most_remote(tree, count=5)

    assert remote.most_remote.suppressed > 0
    assert remote.most_remote.considered >= remote.most_remote.suppressed


def test_the_separation_is_recorded_so_the_report_can_state_it():
    tree = tree_from(wrap(chain(60)))

    remote.most_remote(tree, count=3)

    assert remote.most_remote.separation >= remote.MIN_SEPARATION


# --- who is left out --------------------------------------------------------


def test_a_redacted_profile_is_never_reported():
    """A `Private` page cannot be opened to read a path, at either end."""
    # Geni redacts a living person to the single name `Private`, so the surname
    # is empty — `Private /Private/` would display as "Private Private" and is
    # a different string from the one `_UNUSABLE` knows.
    body = chain(60).replace("Person60 /Chain/", "Private //")
    records = wrap(body.replace("Person1 /Chain/", "Private //"))
    tree = tree_from(records)

    people = remote.most_remote(tree, count=10)

    names = {p.name for p in people} | {p.partner_name for p in people}
    assert not any("Private" in name for name in names)


def test_a_component_too_small_to_matter_is_skipped():
    tree = tree_from(wrap(chain(60) + "\n" + chain(4, first=500, surname="Islet")))

    people = remote.most_remote(tree, count=20)

    assert not any(p.geni_id.startswith("50") for p in people)


def test_a_second_real_component_is_measured_on_its_own_landmarks():
    """A BFS cannot leave its component, so each one needs landmarks placed in it."""
    tree = tree_from(wrap(chain(60) + "\n" + chain(60, first=500, surname="Other")))

    people = remote.most_remote(tree, count=20)

    assert {p.geni_id for p in people} & {"500", "559"}
    assert {p.geni_id for p in people} & {"1", "60"}


# --- determinism and shape --------------------------------------------------


def test_the_same_tree_gives_the_same_answer_twice():
    """Ties are broken by ID: a report Emma works through must not reshuffle."""
    tree = tree_from(wrap(chain(60)))

    first = [p.geni_id for p in remote.most_remote(tree, count=5)]
    second = [p.geni_id for p in remote.most_remote(tree, count=5)]

    assert first == second


def test_an_empty_tree_reports_nothing_rather_than_raising():
    assert remote.most_remote(tree_from(wrap("0 @I1@ INDI\n1 NAME A /B/"))) == []


def test_the_path_url_is_the_one_geni_writes():
    """Copied from the `href` on a saved profile page, not invented."""
    url = remote.path_url("6000000210521076830", "6000000002517586322", "inlaw")

    assert url == (
        "https://www.geni.com/inconsistencies/for_path"
        "?from_id=6000000210521076830&to_id=6000000002517586322&path_type=inlaw"
    )


def test_the_report_names_the_people_and_offers_both_path_types():
    tree = tree_from(wrap(chain(60)))
    people = remote.most_remote(tree, count=3)

    markdown = remote.render_markdown(people, len(tree.people))
    page = remote.render_html(people, len(tree.people))

    assert people[0].name in markdown
    assert "path_type=blood" in markdown and "path_type=inlaw" in markdown
    assert people[0].geni_id in page
    assert page.startswith("<!doctype html>")


@pytest.mark.parametrize("count", [1, 3, 25])
def test_it_never_returns_more_than_asked_for(count):
    tree = tree_from(wrap(chain(80)))

    assert len(remote.most_remote(tree, count=count)) <= count
