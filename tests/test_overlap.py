"""The two-sided P2600 overlap, without a network.

`genimerge.overlap` exists because `match_by_geni_id` can only ever answer half
the question — it asks Wikidata about IDs we already have, so it cannot see an
item whose Geni profile no export has reached. These tests pin the half that is
easy to get wrong: the partitioning that makes fetching all of P2600 possible,
and the arithmetic that keeps items, values and statements as three numbers
rather than one.
"""

import hashlib

import pytest

from genimerge import overlap


class FakeClient:
    """Answers a partition query from a fixed set of pairs.

    Partitions the pairs the same way the real endpoint would — by MD5 of the
    item URI — so a test that expects sixteen partitions to reassemble into the
    whole set is testing the split, not a stub that always returns everything.
    """

    def __init__(self, pairs):
        self.pairs = pairs
        self.queries = []

    def sparql(self, query):
        self.queries.append(query)
        prefix = query.split('MD5(STR(?item)), "')[1][0]
        out = []
        for qid, geni_id in self.pairs:
            uri = f"http://www.wikidata.org/entity/{qid}"
            if hashlib.md5(uri.encode()).hexdigest().startswith(prefix):
                out.append({"item": {"value": uri}, "g": {"value": geni_id}})
        return [{k: v["value"] for k, v in row.items()} for row in out]


PAIRS = [
    ("Q1", "1001"),
    ("Q2", "1002"),
    ("Q3", "1003"),
    ("Q4", "1004"),
    ("Q5", "9999"),
]


# -- partitioning ------------------------------------------------------


def test_the_sixteen_partitions_reassemble_into_every_pair():
    client = FakeClient(PAIRS)

    fetched = overlap.fetch_all_p2600(client)

    assert sorted(fetched) == sorted(PAIRS)
    assert len(client.queries) == 16


def test_no_pair_is_fetched_twice():
    """MD5 prefixes are disjoint, so a pair in two partitions means a bad split."""
    fetched = overlap.fetch_all_p2600(FakeClient(PAIRS))

    assert len(fetched) == len(set(fetched))


def test_the_partition_filter_names_the_prefix_it_was_asked_for():
    assert 'MD5(STR(?item)), "c"' in overlap.partition_query("c")
    assert "wdt:P2600" in overlap.partition_query("c")


def test_progress_is_reported_once_per_partition():
    seen = []
    overlap.fetch_all_p2600(FakeClient(PAIRS), progress=lambda d, t: seen.append((d, t)))

    assert seen[0] == (1, 16)
    assert seen[-1] == (16, 16)


# -- the arithmetic ----------------------------------------------------


def test_overlap_is_counted_from_both_sides():
    result = overlap.measure(PAIRS, our_ids={"1001", "1002", "5555"})

    assert result.both == {"1001", "1002"}
    assert result.ours_only == {"5555"}
    assert result.theirs_only == {"1003", "1004", "9999"}


def test_a_geni_id_on_two_items_is_kept_rather_than_collapsed():
    """Both readings — duplicate items, or a wrong P2600 — need a human."""
    result = overlap.measure([("Q1", "1001"), ("Q7", "1001")], our_ids={"1001"})

    assert result.id_on_several_items == {"1001": ["Q1", "Q7"]}
    assert result.theirs == {"1001"}          # still one ID, counted once


def test_an_item_with_two_geni_ids_is_kept_too():
    result = overlap.measure([("Q1", "1001"), ("Q1", "1002")], our_ids=set())

    assert result.item_with_several_ids == {"Q1": ["1001", "1002"]}
    assert result.theirs == {"1001", "1002"}


def test_a_repeated_statement_is_not_a_conflict():
    """The same (item, id) twice is one pair, not an item with two IDs."""
    result = overlap.measure([("Q1", "1001"), ("Q1", "1001")], our_ids=set())

    assert result.item_with_several_ids == {}
    assert result.id_on_several_items == {}


def test_a_non_numeric_p2600_value_is_excluded_and_named():
    """A URL or a slug on P2600 cannot join to a GEDCOM xref at all."""
    result = overlap.measure(
        [("Q1", "1001"), ("Q2", "profile-6000000012345"), ("Q3", "")],
        our_ids={"1001"},
    )

    assert result.theirs == {"1001"}
    assert result.non_numeric == [("Q2", "profile-6000000012345"), ("Q3", "")]


def test_the_reported_totals_are_carried_through_untouched():
    """They come from the endpoint, not from the rows — that is the point.

    If they were derived from the fetched pairs, a partition that silently came
    back empty would make Wikidata look smaller instead of making the run look
    wrong.
    """
    result = overlap.measure(PAIRS, our_ids=set(), reported={"items": 514822})

    assert result.reported["items"] == 514822


# -- the report --------------------------------------------------------


@pytest.fixture
def report():
    result = overlap.measure(
        [*PAIRS, ("Q8", "1001"), ("Q9", "2001"), ("Q9", "2002"), ("Q10", "bad")],
        our_ids={"1001", "1002", "5555"},
        reported={"items": 514822, "values": 516913, "statements": 516983,
                  "humans": 514692},
    )
    return overlap.render_markdown(result, people=3, exports=99)


def test_the_report_states_both_denominators(report):
    assert "of our tree" in report
    assert "of Wikidata's Geni IDs" in report


def test_the_report_carries_the_endpoint_totals(report):
    assert "514,822" in report
    assert "516,983" in report


def test_the_report_lists_the_rows_a_human_has_to_look_at(report):
    assert "Geni IDs on more than one Wikidata item" in report
    assert "Wikidata items carrying more than one Geni ID" in report
    assert "P2600 values that are not a profile ID" in report


def test_the_report_marks_which_conflicted_ids_are_ours(report):
    """A double-linked ID that is in our tree is the one worth chasing first."""
    assert "in our tree" in report


def test_the_report_warns_that_a_through_url_carries_two_people(report):
    """The `?through=` trap: the ID after the `?` is a different person.

    Recovering an ID from a pasted URL looks like safe parsing right up to that
    case, which is exactly why the warning is generated rather than remembered.
    """
    assert "?through=" in report
    assert "different person" in report


def test_a_recoverable_id_inside_a_bad_value_is_counted():
    result = overlap.measure(
        [("Q1", "https://www.geni.com/people/X/6000000012345678901"),
         ("Q2", "18 декабря 1918")],
        our_ids=set(),
    )

    rendered = overlap.render_markdown(result, people=0, exports=1)

    assert "**2** values are not all digits" in rendered
    assert "**1** of them have a profile ID inside" in rendered


def test_two_of_our_people_on_one_item_are_singled_out():
    """The subset that is evidence about *our* data, not about Wikidata's."""
    result = overlap.measure(
        [("Q1", "1001"), ("Q1", "1002"),      # both ours -- the interesting case
         ("Q2", "1003"), ("Q2", "4004")],     # only one ours -- not
        our_ids={"1001", "1002", "1003"},
    )

    assert result.pairs_in_our_tree == {"Q1": ["1001", "1002"]}


def test_the_pairs_section_gives_both_readings_and_picks_neither():
    """Geni holding a duplicate and Wikidata holding a wrong P2600 look the same."""
    result = overlap.measure(
        [("Q1", "1001"), ("Q1", "1002")], our_ids={"1001", "1002"}
    )

    rendered = overlap.render_markdown(
        result, people=2, exports=1, names={"1001": "Ada Alpha", "1002": "Ada A."}
    )

    assert "## Two of our people, one Wikidata item" in rendered
    assert "Geni holds the same person twice" in rendered
    assert "The P2600 on that item is wrong" in rendered
    assert "Ada Alpha `1001` == Ada A. `1002`" in rendered


def test_the_pairs_section_is_absent_when_no_item_holds_two_of_ours():
    result = overlap.measure([("Q1", "1001"), ("Q1", "1002")], our_ids={"1001"})

    assert "## Two of our people" not in overlap.render_markdown(
        result, people=1, exports=1
    )


def test_a_short_digit_run_is_not_mistaken_for_a_profile_id():
    """A year is digits too. A Geni profile ID is 13-19 of them."""
    assert not overlap.EMBEDDED_ID.search("born 1918")
    assert overlap.EMBEDDED_ID.search("people/X/6000000012345678901")


def test_a_clean_dataset_gets_no_review_sections():
    result = overlap.measure([("Q1", "1001")], our_ids={"1001"})

    rendered = overlap.render_markdown(result, people=1, exports=1)

    assert "## Geni IDs on more than one Wikidata item" not in rendered
    assert "## Wikidata items carrying more than one Geni ID" not in rendered
    assert "## P2600 values that are not a profile ID" not in rendered


def test_endpoint_totals_read_as_not_fetched_when_offline():
    """An offline run has no honest value for the four endpoint-reported
    totals, and printing 0 would read as "Wikidata carries no Geni IDs" —
    the opposite of true."""
    result = overlap.measure([("Q1", "100"), ("Q2", "200")], {"100"})

    text = overlap.render_markdown(result, people=1, exports=1, fetched="2026-08-06")

    assert "not fetched (offline)" in text
    assert "cached 2026-08-06" in text


def test_a_live_run_prints_the_endpoint_totals():
    result = overlap.measure(
        [("Q1", "100")], {"100"}, reported={"items": 7, "humans": 5, "values": 7, "statements": 9}
    )

    text = overlap.render_markdown(result, people=1, exports=1)

    assert "not fetched (offline)" not in text
    assert "| 7 |" in text
