import pytest

from genimerge import gedcom, seeds
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
