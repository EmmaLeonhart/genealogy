"""Distant pairs — the report whose output is a question for Geni.

The claim each row makes is "our tree connects these two only the long way
round". So the things worth pinning are that the distance is real, that the
pairs are spread rather than ten names off one branch, and that redacted
profiles never appear — a `Private` page cannot be opened to read a path.
"""

import pytest

from genimerge import distant, gedcom
from genimerge.model import build_tree


def tree_from(records: str):
    return build_tree(list(gedcom.parse(records).records))


def chain(n: int) -> str:
    """A line of `n` people, each the child of the one before."""
    out = []
    for i in range(1, n + 1):
        out.append(f"0 @I{i}@ INDI\n1 NAME Person{i} /Chain/\n1 SEX M")
    for i in range(1, n):
        out.append(f"0 @F{i}@ FAM\n1 HUSB @I{i}@\n1 CHIL @I{i+1}@")
    return "0 HEAD\n" + "\n".join(out) + "\n0 TRLR\n"


def test_bfs_measures_hops_not_generations():
    tree = tree_from(chain(5))
    graph = {k: v for k, v in _graph(tree).items()}

    dist = distant.bfs(graph, "1")

    assert dist["5"] == 4


def _graph(tree):
    from genimerge.frontier import family_graph

    return family_graph(tree)


def test_the_widest_pair_of_a_chain_is_its_two_ends():
    # Long enough to clear MIN_HOPS: a chain of 8 is a legitimate tree but its
    # widest pair is 7 hops, which the floor correctly refuses to call distant.
    tree = tree_from(chain(40))

    pairs = distant.far_pairs(tree, count=1)

    assert len(pairs) == 1
    assert {pairs[0].a, pairs[0].b} == {"1", "40"}
    assert pairs[0].distance == 39


def test_a_spouse_edge_is_one_hop_like_any_other():
    """Deliberate: a route through an in-law is what a Forest export finds."""
    records = (
        "0 HEAD\n"
        "0 @I1@ INDI\n1 NAME A /X/\n"
        "0 @I2@ INDI\n1 NAME B /Y/\n"
        "0 @F1@ FAM\n1 HUSB @I1@\n1 WIFE @I2@\n"
        "0 TRLR\n"
    )
    tree = tree_from(records)

    assert distant.bfs(_graph(tree), "1")["2"] == 1


def test_redacted_and_placeholder_names_are_never_an_endpoint():
    """`Private` is Geni's redaction; the page will not show a path.

    The chain's far end is redacted, so the pair has to fall back to a person
    who can actually be looked up, even though that is a shorter distance.
    """
    records = (
        "0 HEAD\n"
        "0 @I1@ INDI\n1 NAME Alice /Real/\n"
        "0 @I2@ INDI\n1 NAME Bob /Real/\n"
        "0 @I3@ INDI\n1 NAME Private\n"
        "0 @F1@ FAM\n1 HUSB @I1@\n1 CHIL @I2@\n"
        "0 @F2@ FAM\n1 HUSB @I2@\n1 CHIL @I3@\n"
        "0 TRLR\n"
    )
    tree = tree_from(records)

    pairs = distant.far_pairs(tree, count=3)

    for pair in pairs:
        assert "private" not in pair.a_name.lower()
        assert "private" not in pair.b_name.lower()


def test_pairs_do_not_reuse_a_person():
    """Ten pairs sharing one endpoint would be one finding reported ten times."""
    tree = tree_from(chain(30))

    pairs = distant.far_pairs(tree, count=5)

    seen = [p.a for p in pairs] + [p.b for p in pairs]
    assert len(seen) == len(set(seen))


def test_pairs_come_back_widest_first():
    tree = tree_from(chain(30))

    pairs = distant.far_pairs(tree, count=5)

    assert [p.distance for p in pairs] == sorted((p.distance for p in pairs), reverse=True)


def test_an_empty_tree_yields_no_pairs():
    tree = tree_from("0 HEAD\n0 TRLR\n")

    assert distant.far_pairs(tree) == []
    assert "No pairs found" in distant.render_markdown([], 0)


def test_the_report_says_what_a_row_means_and_how_it_was_measured():
    """A reader who takes a row as "these people are unrelated" has it backwards.

    The row is a prediction that Geni holds a *shorter* route through people we
    lack, so the text carrying that has to reach the rendered report.
    """
    tree = tree_from(chain(40))
    text = distant.render_markdown(distant.far_pairs(tree, count=1), len(tree.people))

    assert "shorter one" in text
    assert "double-sweep" in text
    assert "spouse edges" in text


def test_html_and_markdown_describe_the_same_pairs():
    tree = tree_from(chain(12))
    pairs = distant.far_pairs(tree, count=2)

    md = distant.render_markdown(pairs, len(tree.people))
    page = distant.render_html(pairs, len(tree.people))

    for pair in pairs:
        assert pair.a_url in md and pair.a_url in page
        assert pair.b_url in md and pair.b_url in page


@pytest.mark.parametrize("count", [1, 3, 7])
def test_count_is_respected(count):
    tree = tree_from(chain(40))

    assert len(distant.far_pairs(tree, count=count)) <= count


def test_a_used_seeds_neighbourhood_is_retired_not_just_its_endpoints():
    """Otherwise every rim candidate is a neighbour of the last seed.

    The rim is sorted by distance from a single anchor, so its top entries all
    sit in one corner and each resolves to the same far endpoint — a full BFS
    over every person to rediscover a pair already found. On the real tree that
    was hundreds of sweeps instead of ten, and the first run was killed after
    21 minutes of CPU without emitting a row.

    Pinned by the observable consequence: on a plain chain, consecutive pairs
    must not start at adjacent people.
    """
    tree = tree_from(chain(60))

    pairs = distant.far_pairs(tree, count=4)

    starts = sorted(int(p.a) for p in pairs)
    assert all(b - a > 1 for a, b in zip(starts, starts[1:])), starts


def test_every_person_appears_in_at_most_one_pair():
    tree = tree_from(chain(60))

    pairs = distant.far_pairs(tree, count=6)
    seen = [p.a for p in pairs] + [p.b for p in pairs]

    assert len(seen) == len(set(seen))


def test_both_ends_are_retired_not_only_the_seed():
    """Retiring one end leaves every pair sharing the graph's deepest branch.

    On the real tree, retiring only the seed produced twelve pairs with twelve
    different seeds and ten whose far end was a different member of the same
    Chinese lineage — the deepest branch wins "farthest from here" from almost
    anywhere, so it appeared over and over.

    On a chain the same failure shows as every pair ending at the same tip.
    """
    tree = tree_from(chain(80))

    pairs = distant.far_pairs(tree, count=4)

    ends = sorted(int(p.b) for p in pairs)
    assert all(b - a > 1 for a, b in zip(ends, ends[1:])), ends


def test_pairs_that_are_not_actually_distant_are_dropped():
    """The greedy search tails off, and the tail is misleading.

    A real run gave 311, 173, 120, 76, 49, 33, 18, 10, 8 and 5 hops. Two people
    five hops apart are near relatives; listing them as a "distant pair" would
    invite exactly the wrong export, since the whole premise is that a long
    in-tree walk predicts a missing community.
    """
    tree = tree_from(chain(200))

    pairs = distant.far_pairs(tree, count=20)

    assert pairs, "a 200-person chain should yield at least one distant pair"
    floor = pairs[0].distance * distant.MIN_SHARE_OF_WIDEST
    assert all(p.distance >= floor for p in pairs)


def test_a_shallow_tree_reports_nothing_rather_than_its_widest_near_pair():
    """MIN_HOPS is absolute, so a small tree cannot promote a 3-hop pair."""
    tree = tree_from(chain(6))

    assert distant.far_pairs(tree, count=5) == []
