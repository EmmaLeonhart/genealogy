from genimerge import frontier, gedcom
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

# Two people connected to nobody else.
SEPARATE = """0 HEAD
0 @I7@ INDI
1 NAME G /Alone/
1 FAMS @F3@
0 @I8@ INDI
1 NAME H /Alone/
1 FAMC @F3@
0 @F3@ FAM
1 HUSB @I7@
1 CHIL @I8@
0 TRLR
"""


def tree(*texts):
    records = []
    for text in texts:
        records += gedcom.parse(text).records
    return build_tree(records)


def test_descendants_are_counted_without_double_counting():
    counts = frontier.descendant_counts(tree(LINE))

    assert counts["1"] == 3          # C, E, F
    assert counts["3"] == 2          # E, F
    assert counts["5"] == 0


def test_a_person_reachable_two_ways_is_counted_once():
    # E is a descendant of both A and B, and A and B are spouses; counting by
    # summing children would count E twice for the couple's line.
    counts = frontier.descendant_counts(tree(LINE))

    assert counts["1"] == counts["2"] == 3


def test_ancestor_depth_is_the_longest_chain():
    depth = frontier.ancestor_depth(tree(LINE))

    assert depth["1"] == 0
    assert depth["3"] == 1
    assert depth["5"] == 2


def test_components_separate_unrelated_families():
    comps = frontier.components(tree(LINE, SEPARATE))

    assert [c.size for c in comps] == [6, 2]
    assert set(comps[1].members) == {"7", "8"}


def test_a_child_in_two_families_does_not_split_the_graph():
    # The bug this exists for: keeping only the first family's father made the
    # relation asymmetric -- the father listed the child, the child did not
    # list the father -- and the second father fell out as a lone "component".
    extra = """0 @I9@ INDI
1 NAME I /Second/
1 FAMS @F4@
0 @F4@ FAM
1 HUSB @I9@
1 CHIL @I5@
0 TRLR
"""
    t = tree(LINE, extra)

    assert [c.size for c in frontier.components(t)] == [7]
    assert set(t.people["5"].parent_ids) == {"3", "4", "9"}


def test_the_primary_parents_still_name_one_father_and_one_mother():
    # parent_ids is for the graph; father_id/mother_id is what a P22/P25
    # statement would use, and must stay single-valued.
    t = tree(LINE)

    assert (t.people["5"].father_id, t.people["5"].mother_id) == ("3", "4")


def test_neighbours_include_siblings():
    t = tree(LINE)

    assert set(frontier._neighbours(t.people["5"], t)) == {"3", "4", "6"}


def test_parentless_people_are_the_edge_of_the_tree():
    comps = frontier.components(tree(LINE))

    assert set(comps[0].parentless) == {"1", "2", "4"}


def test_branch_points_rank_by_how_much_hangs_off_them():
    points = frontier.branch_points(tree(LINE, SEPARATE))
    ranked = [(p.person.geni_id, p.descendants) for p in points]

    assert ranked[0][1] == 3
    assert ranked[0][0] in {"1", "2"}
    # Everyone listed has no parents; people with parents are not branch points.
    assert all(not p.person.has_known_parents for p in points)


def test_branch_point_reasons_describe_what_was_found():
    points = {p.person.geni_id: p for p in frontier.branch_points(tree(LINE))}

    assert "descendants" in points["1"].reason
    assert points["1"].component_size == 6


def test_a_cycle_does_not_hang_the_walk():
    # Somebody entered as their own ancestor. Real genealogies contain this.
    cyclic = """0 @I1@ INDI
1 FAMC @F2@
1 FAMS @F1@
0 @I2@ INDI
1 FAMC @F1@
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 CHIL @I2@
0 @F2@ FAM
1 HUSB @I2@
1 CHIL @I1@
0 TRLR
"""
    t = tree(cyclic)

    assert frontier.descendant_counts(t)["1"] >= 1
    assert set(frontier.ancestor_depth(t)) == {"1", "2"}
    assert [c.size for c in frontier.components(t)] == [2]


def test_a_person_who_is_their_own_ancestor_is_reported():
    cyclic = """0 @I1@ INDI
1 FAMC @F2@
1 FAMS @F1@
0 @I2@ INDI
1 FAMC @F1@
1 FAMS @F2@
0 @F1@ FAM
1 HUSB @I1@
1 CHIL @I2@
0 @F2@ FAM
1 HUSB @I2@
1 CHIL @I1@
0 TRLR
"""
    cycles = frontier.ancestry_cycles(tree(cyclic))

    assert len(cycles) == 1
    assert cycles[0][0] == cycles[0][-1]
    assert set(cycles[0]) == {"1", "2"}
    assert "own ancestor" in frontier.render_markdown(tree(cyclic))


def test_a_clean_tree_reports_no_cycles():
    assert frontier.ancestry_cycles(tree(LINE)) == []
    assert "own ancestor" not in frontier.render_markdown(tree(LINE))


def test_the_report_agrees_with_itself():
    text = frontier.render_markdown(tree(LINE, SEPARATE))

    assert "# Expansion frontier" in text
    assert "| people | 8 | 100% |" in text
    assert "| connected components | 2 |  |" in text


def test_the_report_survives_an_empty_tree():
    from genimerge.model import Tree

    assert "# Expansion frontier" in frontier.render_markdown(Tree())


# --- describe_connectivity -------------------------------------------------
#
# `genimerge merge` prints this. Conflicts tell you whether the exports
# disagree; this tells you whether they joined up. An export seeded outside
# everything we already hold merges with zero conflicts and still leaves two
# trees, so the merge's own counters cannot surface it.

TWO_TREES = """0 HEAD
0 @I1@ INDI
1 NAME A /Root/
1 FAMS @F1@
0 @I2@ INDI
1 NAME B /Root/
1 FAMS @F1@
0 @I7@ INDI
1 NAME G /Island/
1 FAMS @F9@
0 @I8@ INDI
1 NAME H /Island/
1 FAMS @F9@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
0 @F9@ FAM
1 HUSB @I7@
1 WIFE @I8@
0 TRLR
"""


def test_one_component_reads_as_one_tree():
    comps = frontier.components(build_tree(gedcom.parse(LINE).records))

    assert len(comps) == 1
    assert frontier.describe_connectivity(comps) == "one connected tree, all 6 people"


def test_a_disconnected_export_is_named_with_its_sizes():
    """The sizes matter: a 3656-person island is not a 2-person one."""
    comps = frontier.components(build_tree(gedcom.parse(TWO_TREES).records))

    line = frontier.describe_connectivity(comps)

    assert len(comps) == 2
    assert "2 separate trees, not one: 2, 2 people" in line


def test_a_split_tree_is_reported_without_being_called_an_error():
    """More than one component is legitimate, so the wording must not blame it.

    `frontier` exists partly to say that a component nobody outside it is
    related to needs its own seed. Wording this as a failure would push someone
    to silence it later.

    The blame-word check needs no constant and gets none: it never depended on
    the wording, which makes it the stronger of the two assertions here.
    """
    line = frontier.describe_connectivity(
        frontier.components(build_tree(gedcom.parse(TWO_TREES).records))
    )

    assert frontier.SPLIT_IS_NOT_AN_ERROR in line
    for blame in ("error", "invalid", "failed", "corrupt"):
        assert blame not in line.lower()


def test_the_split_caveat_still_says_a_split_needs_its_own_seed():
    """Identity alone would pass on an emptied constant, so pin its substance."""
    assert "needs its own export seed" in frontier.SPLIT_IS_NOT_AN_ERROR
    assert "components do not conflict" in frontier.SPLIT_IS_NOT_AN_ERROR


def test_many_components_are_summarised_rather_than_all_listed():
    comps = [frontier.Component(members=[str(i)]) for i in range(9)]

    line = frontier.describe_connectivity(comps, show=3)

    assert "1, 1, 1, and 6 more people" in line


def test_an_empty_tree_says_so_instead_of_claiming_one_tree():
    assert frontier.describe_connectivity([]) == "no people, so nothing to connect"
