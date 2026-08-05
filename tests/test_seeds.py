from pathlib import Path

import pytest

from genimerge import gedcom, seeds, sources
from genimerge.model import build_tree

# A -- B
#      |
#      C -- D
#           |
#      +----+----+
#      E         F
LINE = """0 HEAD
0 @I1@ INDI
1 NAME A /Root/
1 FAMS @F1@
0 @I2@ INDI
1 NAME B /Root/
1 FAMS @F1@
0 @I3@ INDI
1 NAME C /Root/
1 FAMC @F1@
1 FAMS @F2@
0 @I4@ INDI
1 NAME D /Other/
1 FAMS @F2@
0 @I5@ INDI
1 NAME E /Root/
1 FAMC @F2@
0 @I6@ INDI
1 NAME F /Root/
1 FAMC @F2@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
0 @F2@ FAM
1 HUSB @I3@
1 WIFE @I4@
1 CHIL @I5@
1 CHIL @I6@
0 TRLR
"""


def tree(*texts):
    records = []
    for text in texts:
        records += gedcom.parse(text).records
    return build_tree(records)


def _dense(children: int, start: int = 100) -> str:
    """A couple with many recorded children: a region with nothing open in it.

    Everyone but the couple has both parents recorded, so a ball centred here
    is almost all people we already hold -- the "bang in the middle of the
    graph" case, built rather than hand-written so the ball is big enough for
    the saturation threshold to be about proportion and not about small numbers.
    """
    husband, wife = start, start + 1
    lines = ["0 HEAD", f"0 @I{husband}@ INDI", "1 NAME Dense /Father/", "1 FAMS @F90@"]
    lines += [f"0 @I{wife}@ INDI", "1 NAME Dense /Mother/", "1 FAMS @F90@"]
    kids = [start + 2 + i for i in range(children)]
    for kid in kids:
        lines += [f"0 @I{kid}@ INDI", f"1 NAME Kid{kid} /Dense/", "1 FAMC @F90@"]
    lines += ["0 @F90@ FAM", f"1 HUSB @I{husband}@", f"1 WIFE @I{wife}@"]
    lines += [f"1 CHIL @I{kid}@" for kid in kids]
    lines += ["0 TRLR", ""]
    return "\n".join(lines)


# Two families sharing C1, so P1, P2 and P3 all sit in one ball.
CLUSTER = """0 HEAD
0 @I11@ INDI
1 NAME P1 /Cluster/
1 FAMS @F11@
0 @I12@ INDI
1 NAME P2 /Cluster/
1 FAMS @F11@
0 @I13@ INDI
1 NAME C1 /Cluster/
1 FAMC @F11@
1 FAMS @F12@
0 @I14@ INDI
1 NAME P3 /Cluster/
1 FAMS @F12@
0 @I15@ INDI
1 NAME C2 /Cluster/
1 FAMC @F12@
0 @F11@ FAM
1 HUSB @I11@
1 WIFE @I12@
1 CHIL @I13@
0 @F12@ FAM
1 HUSB @I13@
1 WIFE @I14@
1 CHIL @I15@
0 TRLR
"""

# A separate component entirely: no walk from CLUSTER ever reaches it.
FAR = """0 HEAD
0 @I21@ INDI
1 NAME P4 /Far/
1 FAMS @F21@
0 @I22@ INDI
1 NAME P5 /Far/
1 FAMS @F21@
0 @I23@ INDI
1 NAME C3 /Far/
1 FAMC @F21@
0 @F21@ FAM
1 HUSB @I21@
1 WIFE @I22@
1 CHIL @I23@
0 TRLR
"""


def _blood(t):
    return seeds.edges_for_style(t, "blood")


# --- the ball -------------------------------------------------------------


def test_the_ball_is_breadth_first_and_records_hop_distance():
    t = tree(LINE)
    ball = seeds.export_ball(_blood(t), "1")

    assert ball.reached[0] == "1"
    assert ball.hop == {"1": 0, "2": 1, "3": 1, "4": 2, "5": 2, "6": 2}
    assert ball.depth == 2
    # breadth-first: nothing at hop 2 precedes anything at hop 1
    assert [ball.hop[p] for p in ball.reached] == sorted(ball.hop[p] for p in ball.reached)


def test_a_radius_stops_the_walk_short_of_the_far_side():
    t = tree(LINE)
    ball = seeds.export_ball(_blood(t), "1", radius=1)

    assert set(ball.reached) == {"1", "2", "3"}
    assert ball.depth == 1
    assert not ball.capped


def test_the_cap_stops_the_walk_and_the_ball_says_it_did():
    t = tree(LINE)
    ball = seeds.export_ball(_blood(t), "1", cap=3)

    assert ball.size == 3
    assert ball.capped


def test_a_ball_that_fits_is_not_marked_capped():
    t = tree(LINE)
    ball = seeds.export_ball(_blood(t), "1", cap=100)

    assert ball.size == 6
    assert not ball.capped


def test_a_lone_person_has_a_ball_of_one():
    ball = seeds.export_ball({"9": []}, "9")

    assert ball.reached == ["9"]
    assert ball.depth == 0
    assert not ball.capped


# --- styles ---------------------------------------------------------------


def test_ancestor_and_descendant_styles_walk_opposite_directions():
    t = tree(LINE)
    up = seeds.export_ball(seeds.edges_for_style(t, "ancestors"), "5")
    down = seeds.export_ball(seeds.edges_for_style(t, "descendants"), "1")

    assert set(up.reached) == {"5", "3", "4", "1", "2"}   # E and everyone above
    assert set(down.reached) == {"1", "3", "5", "6"}      # A and everyone below


def test_blood_and_all_walk_the_same_edges():
    t = tree(LINE)

    assert seeds.edges_for_style(t, "blood") == seeds.edges_for_style(t, "all")


def test_an_unknown_style_is_refused_rather_than_guessed():
    t = tree(LINE)
    with pytest.raises(ValueError, match="unknown export style"):
        seeds.edges_for_style(t, "cousins")


# --- doorways and saturation ---------------------------------------------


def test_doorways_are_the_people_with_no_parents_recorded():
    t = tree(LINE)
    profile = seeds.profile_seed(t, "1", _blood(t))

    assert profile.doorways == {"1", "2", "4"}   # A, B and D; C, E, F have parents
    assert profile.open_count == 3
    assert profile.openness == pytest.approx(3 / 6)


def test_a_region_recorded_all_around_is_rejected_as_saturated():
    t = tree(_dense(children=60))
    kept, rejected = seeds.rank_seeds(t)

    # Only the couple is parentless, in a ball of 62.
    assert [p.seed for p in kept] == []
    assert {p.seed for p in rejected} == {"100", "101"}
    assert rejected[0].openness == pytest.approx(2 / 62)
    assert rejected[0].saturated


def test_a_seed_on_the_frontier_is_kept():
    t = tree(CLUSTER)
    kept, rejected = seeds.rank_seeds(t)

    assert rejected == []
    assert {p.seed for p in kept} == {"11", "12", "14"}
    assert kept[0].open_count == 3


def test_people_who_already_have_parents_are_never_candidates():
    t = tree(CLUSTER)
    kept, rejected = seeds.rank_seeds(t)

    assert "13" not in {p.seed for p in kept + rejected}   # C1 has parents


def test_saturated_and_kept_are_both_returned_so_the_count_can_be_reported():
    t = tree(CLUSTER, _dense(children=60))
    kept, rejected = seeds.rank_seeds(t)

    assert len(kept) == 3
    assert len(rejected) == 2


# --- choosing a set of exports -------------------------------------------


def test_the_second_pick_leaves_the_first_neighbourhood():
    # P1, P2 and P3 share one ball, so all three rank equally at 3 doorways;
    # the far component ranks lower at 2. Ranking alone would spend both
    # exports on the cluster and learn nothing the second time.
    t = tree(CLUSTER, FAR)
    kept, _ = seeds.rank_seeds(t)
    picks = seeds.choose_export_set(kept, 2)

    assert [p.seed for p in kept[:2]] == ["11", "12"]          # both in the cluster
    assert picks[0].profile.seed == "11"
    assert picks[1].profile.seed in {"21", "22"}               # the far component
    assert picks[1].fresh_count == 2


def test_each_pick_is_credited_only_with_what_it_adds():
    t = tree(CLUSTER, FAR)
    kept, _ = seeds.rank_seeds(t)
    picks = seeds.choose_export_set(kept, 2)

    assert picks[0].fresh_count == 3
    assert picks[1].fresh_count == 2
    assert picks[0].fresh & picks[1].fresh == frozenset()


def test_selection_stops_when_nothing_new_would_be_covered():
    # Asking for five exports out of a tree holding two distinct neighbourhoods
    # returns two. Padding to five would propose exports that add nothing.
    t = tree(CLUSTER, FAR)
    kept, _ = seeds.rank_seeds(t)

    assert len(seeds.choose_export_set(kept, 5)) == 2


def test_choosing_none_is_allowed():
    t = tree(CLUSTER)
    kept, _ = seeds.rank_seeds(t)

    assert seeds.choose_export_set(kept, 0) == []


def test_selection_is_deterministic_when_candidates_tie():
    t = tree(CLUSTER, FAR)
    kept, _ = seeds.rank_seeds(t)
    once = [p.profile.seed for p in seeds.choose_export_set(kept, 2)]
    twice = [p.profile.seed for p in seeds.choose_export_set(list(reversed(kept)), 2)]

    assert once == twice


# --- GENI_EXPORT_CAP against the real exports -------------------------------
#
# The constant was 3836 because the first three exports each held exactly that,
# which read as a hard cap. The fourth held 3840. These tests exist so the next
# export to exceed the constant fails here rather than silently modelling a ball
# smaller than a real export.

_EXPORTS = sources.find_exports()


@pytest.mark.skipif(not _EXPORTS, reason="no GEDCOM exports in exports/")
def test_export_cap_is_at_least_the_largest_real_export():
    largest = max(
        sum(1 for r in gedcom.parse_file(p).records if r.tag == "INDI")
        for p in _EXPORTS
    )

    assert seeds.GENI_EXPORT_CAP >= largest, (
        f"an export in exports/ holds {largest} individuals, more than "
        f"GENI_EXPORT_CAP={seeds.GENI_EXPORT_CAP}. Raise the constant to the new "
        "largest observed — and do not describe it as a cap Geni enforces, "
        "which is the mistake 3836 encoded."
    )


def test_export_cap_bounds_the_modelled_ball():
    """The constant must actually bound `export_ball`, not just be documentation."""
    t = tree(CLUSTER, FAR)
    edges = seeds.edges_for_style(t, "blood")
    seed = next(iter(t.people))

    ball = seeds.export_ball(edges, seed, cap=2)

    assert ball.size <= 2
    assert ball.capped


# --- what the report tells you to actually do -------------------------------
#
# The listed people are doorways: in our data, parents not. Exporting from one
# centres Geni's walk on somebody we already hold. The 2026-08-01 export went
# one step further out, to the parent, and came back 95% new. The report has to
# say so, because "here is a profile link" reads as "export from this profile".


def test_the_report_tells_you_to_export_from_the_parent():
    """Asserted by identity, so rewording does not break this."""
    markdown = seeds.render_markdown(tree(CLUSTER, FAR))

    assert seeds.EXPORT_FROM_THE_PARENT in markdown


def test_the_parent_instruction_still_says_which_way_to_go():
    """Identity alone passes on an emptied constant, so pin the substance.

    "Up" is the whole instruction. Without it the sentence could survive a
    rewrite that left the reader exporting from the doorway again.
    """
    assert "go **up** to the parent" in seeds.EXPORT_FROM_THE_PARENT
    assert "not from the person listed" in seeds.EXPORT_FROM_THE_PARENT


def test_the_report_admits_the_ranking_is_unvalidated():
    markdown = seeds.render_markdown(tree(CLUSTER, FAR))

    assert seeds.RANKING_IS_UNVALIDATED in markdown


def test_the_unvalidated_note_keeps_both_the_evidence_and_its_limit():
    """One export from a seed ranked 2255/2336 is a doubt, not a verdict.

    Both halves are load bearing. Drop the first and the ranking reads as
    tested; drop the second and a single data point reads as grounds to rebuild
    the model, which is the mistake already made once with the 3836 cap.
    """
    note = seeds.RANKING_IS_UNVALIDATED

    assert "2255 of 2336" in note
    assert "One data point is not enough to re-rank on" in note


def test_the_ranking_note_appears_even_when_there_is_nothing_to_rank():
    """An empty tree must not silently drop the caveat with the table."""
    markdown = seeds.render_markdown(tree())

    assert seeds.RANKING_IS_UNVALIDATED in markdown


# --- the size bias, measured -----------------------------------------------
#
# The ranking sorts on absolute doorway count, and doorways live inside the
# ball, so a bigger ball has more chances to hold one. Whether that makes the
# sort a proxy for neighbourhood size is a fact about the data, so it is
# measured rather than asserted.


def test_correlation_is_one_when_doorways_track_ball_size_exactly():
    """The degenerate case the real question is measured against."""
    balls = [10.0, 20.0, 30.0, 40.0]
    doorways = [1.0, 2.0, 3.0, 4.0]

    assert seeds._pearson(balls, doorways) == pytest.approx(1.0)


def test_correlation_is_negative_when_doorways_fall_as_the_ball_grows():
    assert seeds._pearson([10.0, 20.0, 30.0], [3.0, 2.0, 1.0]) == pytest.approx(-1.0)


def test_correlation_is_zero_rather_than_undefined_when_a_side_is_constant():
    """A flat column has no variance; returning 0.0 beats dividing by it."""
    assert seeds._pearson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]) == 0.0
    assert seeds._pearson([5.0], [5.0]) == 0.0


def test_size_bias_counts_large_balls_in_the_pool_and_in_the_picks():
    t = tree(CLUSTER, FAR, _dense(children=60))
    kept, _ = seeds.rank_seeds(t)
    picks = seeds.choose_export_set(kept, 3)

    bias = seeds.size_bias(kept, picks)

    assert bias.candidates == len(kept)
    assert bias.picked == len(picks)
    # these fixtures are all small balls, so nothing crosses the threshold
    assert bias.large == 0
    assert bias.large_share == 0.0
    assert bias.picked_large_share == 0.0


def test_size_bias_survives_an_empty_pool_without_dividing_by_zero():
    bias = seeds.size_bias([], [])

    assert bias.candidates == 0
    assert bias.large_share == 0.0
    assert bias.picked_large_share == 0.0
    assert bias.most_open_rank == 0


def test_the_report_shows_the_measurement_and_its_limit():
    markdown = seeds.render_markdown(tree(CLUSTER, FAR))

    assert seeds.SIZE_BIAS_IS_MEASURED in markdown
    assert seeds.SIZE_BIAS_LIMIT in markdown


def test_the_limit_note_keeps_the_claim_it_refuses_to_make():
    """Identity alone passes on an emptied constant, so pin the substance.

    The measurement says how the sort behaves. It cannot say whether openness
    predicts a richer export, because that is a fact about Geni's data and we
    cannot see behind a doorway without exporting through it. Losing that
    sentence turns a description into a verdict.
    """
    assert "does not show is that the ranking is wrong" in seeds.SIZE_BIAS_LIMIT
    assert "a claim about Geni's data, not about ours" in seeds.SIZE_BIAS_LIMIT


def test_the_unvalidated_note_no_longer_asserts_the_mechanism_as_fact():
    """That sentence moved out and got measured; it must not linger unmeasured."""
    assert "favours large balls" not in seeds.RANKING_IS_UNVALIDATED
    assert "2255 of 2336" in seeds.RANKING_IS_UNVALIDATED


# --- the ordering against the one result we have ----------------------------
#
# The single export with measured results was taken through a doorway this
# report ranks 2261 of 2336. That is the most decision-relevant fact in the
# file, so it has to survive in the output rather than only in the devlog.


def test_the_report_states_where_the_known_good_seed_ranked():
    markdown = seeds.render_markdown(tree(CLUSTER, FAR))

    assert seeds.THE_ONE_RESULT in markdown


def test_the_one_result_keeps_every_ordering_it_compared():
    """Identity alone passes on an emptied constant, so pin the substance.

    All four ranks are load bearing together. Quoting only the bottom-3% figure
    reads as "the ranking is broken, use openness"; quoting only the
    smallest-ball figure reads as a rule discovered. The point is that the
    obvious repair fails and the one that works rests on a single observation.
    """
    note = seeds.THE_ONE_RESULT

    assert "2261 of 2336" in note      # what the report sorts on
    assert "1303 of 2336" in note      # openness, the obvious repair
    assert "38 of 2336" in note        # smallest ball, the only one that finds him
    assert "is **not** adopted here" in note
    assert "One observation cannot establish a ranking rule" in note


def test_the_small_ball_shortlist_is_counted_in_the_report():
    markdown = seeds.render_markdown(tree(CLUSTER, FAR))

    assert seeds.SMALL_BALL_IS_TESTABLE in markdown
    assert f"ball of {seeds.SMALL_BALL} or fewer" in markdown


def test_the_report_proposes_the_experiment_rather_than_the_conclusion():
    markdown = seeds.render_markdown(tree(CLUSTER, FAR))

    assert "worth *testing*, not worth adopting" in markdown
    assert "two observations instead of one" in markdown


# --- the small-ball shortlist, named ----------------------------------------
#
# The report proposes comparing an export from the main sequence against one
# from the small-ball shortlist. It used to give the first arm as names and the
# second as a count, which is not an experiment anyone can run.


def test_the_shortlist_names_people_not_just_a_count():
    """Every table is sorted by doorway count, which buries small balls."""
    t = tree(CLUSTER, FAR)
    markdown = seeds.render_markdown(t)

    kept, _ = seeds.rank_seeds(t)
    small = [p for p in kept if p.size <= seeds.SMALL_BALL]
    assert small, "fixture must contain at least one small-ball candidate"
    for profile in small:
        assert f"`{profile.seed}`" in markdown


def test_the_shortlist_is_labelled_as_the_experiment_not_a_recommendation():
    markdown = seeds.render_markdown(tree(CLUSTER, FAR))

    assert seeds.SMALL_BALL_IS_THE_OTHER_ARM in markdown


def test_the_other_arm_note_refuses_to_recommend_and_says_why():
    """Identity alone passes on an emptied constant, so pin the substance.

    Naming people makes a hypothesis look endorsed. The note has to say that a
    list of names adds no evidence, or the shortlist reads as a second
    recommendation with the authority of the first.
    """
    note = seeds.SMALL_BALL_IS_THE_OTHER_ARM

    assert "not a recommendation" in note
    assert "one observation" in note


def test_the_shortlist_repeats_the_export_from_the_parent_instruction():
    """It is a separate section; a reader arriving here must not miss the step."""
    markdown = seeds.render_markdown(tree(CLUSTER, FAR))

    assert markdown.count(seeds.EXPORT_FROM_THE_PARENT) == 2


def test_the_shortlist_is_bounded_so_it_stays_a_shortlist():
    t = tree(CLUSTER, FAR)

    markdown = seeds.render_markdown(t, small_top=1)

    kept, _ = seeds.rank_seeds(t)
    small = sorted(
        [p for p in kept if p.size <= seeds.SMALL_BALL],
        key=lambda p: (p.size, -p.open_count, seeds._ordinal(p.seed)),
    )
    assert len(small) > 1, "fixture must have more candidates than the cap"
    assert f"`{small[0].seed}`" in markdown
    assert "### The small-ball shortlist (1 of" in markdown


def test_no_shortlist_section_when_no_candidate_is_small_enough():
    markdown = seeds.render_markdown(tree(_dense(children=60)))

    assert "The small-ball shortlist" not in markdown
