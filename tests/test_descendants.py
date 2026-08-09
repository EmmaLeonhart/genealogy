"""Ranking lines that stop early — the downward edge, bucketed by period."""

from genimerge import descendants, frontier, gedcom
from genimerge.model import build_tree


def _tree(text: str):
    return build_tree(list(gedcom.parse(text).records))


def _lines(text: str):
    """The measured tree, and the parent map `candidates` needs to drop nesting."""
    tree = _tree(text)
    return tree, descendants.build_lines(tree), descendants.parent_map(tree)


# A(1400) + B -> C(1430); C + D -> E(1460), F(1465). E and F are childless, so
# the line reaches 1465 and stops there with two places to carry on from.
#
# G(1410) + H -> I(1445), childless: a second, unrelated line in the same
# century, stalled slightly harder, so ranking inside a band has something to
# rank.
STALLED = """0 HEAD
0 @I1@ INDI
1 NAME A /Old/
1 BIRT
2 DATE 1400
1 FAMS @F1@
0 @I2@ INDI
1 NAME B /Old/
1 FAMS @F1@
0 @I3@ INDI
1 NAME C /Old/
1 BIRT
2 DATE 1430
1 FAMC @F1@
1 FAMS @F2@
0 @I4@ INDI
1 NAME D /Other/
1 FAMS @F2@
0 @I5@ INDI
1 NAME E /Old/
1 BIRT
2 DATE 1460
1 FAMC @F2@
0 @I6@ INDI
1 NAME F /Old/
1 BIRT
2 DATE 1465
1 FAMC @F2@
0 @I7@ INDI
1 NAME G /Second/
1 BIRT
2 DATE 1410
1 FAMS @F3@
0 @I8@ INDI
1 NAME H /Second/
1 FAMS @F3@
0 @I9@ INDI
1 NAME I /Second/
1 BIRT
2 DATE 1445
1 FAMC @F3@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
0 @F2@ FAM
1 HUSB @I3@
1 WIFE @I4@
1 CHIL @I5@
1 CHIL @I6@
0 @F3@ FAM
1 HUSB @I7@
1 WIFE @I8@
1 CHIL @I9@
0 TRLR
"""

# P(1500) -> Q, R; Q's child marries R's child and they have S. P descends to
# five distinct people, not six: the two lines rejoin.
DIAMOND = """0 HEAD
0 @I10@ INDI
1 NAME P /Cousin/
1 BIRT
2 DATE 1500
1 FAMS @F10@
0 @I11@ INDI
1 NAME PW /Cousin/
1 FAMS @F10@
0 @I12@ INDI
1 NAME Q /Cousin/
1 FAMC @F10@
1 FAMS @F11@
0 @I13@ INDI
1 NAME R /Cousin/
1 FAMC @F10@
1 FAMS @F12@
0 @I14@ INDI
1 NAME QC /Cousin/
1 FAMC @F11@
1 FAMS @F13@
0 @I15@ INDI
1 NAME RC /Cousin/
1 FAMC @F12@
1 FAMS @F13@
0 @I16@ INDI
1 NAME S /Cousin/
1 FAMC @F13@
0 @F10@ FAM
1 HUSB @I10@
1 WIFE @I11@
1 CHIL @I12@
1 CHIL @I13@
0 @F11@ FAM
1 HUSB @I12@
1 CHIL @I14@
0 @F12@ FAM
1 HUSB @I13@
1 CHIL @I15@
0 @F13@ FAM
1 HUSB @I14@
1 WIFE @I15@
1 CHIL @I16@
0 TRLR
"""


# ---------------------------------------------------------------- measures


def test_a_descendant_reached_down_two_lines_counts_twice():
    """The whole point of the measure, so pinned against the distinct count.

    S descends from P down both Q's line and R's line. `frontier` de-duplicates
    to five people; this module counts six paths, because six is how many lines
    run down from P and lines are what an export follows.
    """
    tree = _tree(DIAMOND)
    paths, _ = descendants.descent_paths(tree)
    assert paths["10"] == 6
    assert frontier.descendant_counts(tree)["10"] == 5


def test_paths_are_emmas_recursion_child_by_child():
    """`sum over children of (1 + paths(child))`, asserted at each level."""
    paths, _ = descendants.descent_paths(_tree(STALLED))
    assert paths["5"] == 0  # E is childless
    assert paths["3"] == 2  # C: (1 + 0) for E, (1 + 0) for F
    assert paths["1"] == 3  # A: (1 + 2) for C


def test_open_paths_counts_only_paths_ending_at_someone_childless():
    """A path stopping at somebody who has children is a line already followed."""
    _, open_paths = descendants.descent_paths(_tree(STALLED))
    assert open_paths["1"] == 2  # ends at E and at F, not at C
    assert open_paths["5"] == 0  # E has nothing below them at all

    # In DIAMOND both of P's open paths end at the *same* person, S — and both
    # count, because they are two different lines reaching them.
    _, open_paths = descendants.descent_paths(_tree(DIAMOND))
    assert open_paths["10"] == 2


def test_childless_person_is_their_own_open_end():
    """`descent_paths` counts below someone, so a leaf has none of its own.

    Reporting `0` for a leaf would read as "nowhere to carry on" when the leaf
    itself is the place to carry on from.
    """
    lines = descendants.build_lines(_tree(STALLED))
    assert lines["5"].paths == 0
    assert lines["5"].open_paths == 1


def test_descendant_depth_is_the_longest_chain_below():
    depth = descendants.descendant_depth(_tree(STALLED))
    assert depth["1"] == 2  # A -> C -> E
    assert depth["3"] == 1
    assert depth["5"] == 0


def test_reach_is_the_latest_birth_at_or_below():
    reach, _ = descendants.line_reach(_tree(STALLED))
    assert reach["1"] == 1465
    assert reach["3"] == 1465
    assert reach["5"] == 1460


def test_tip_is_the_latest_born_childless_person_not_the_latest_born():
    """The two differ whenever the latest birth in a line has children recorded.

    In DIAMOND the latest-born dated person is P themselves; everyone below is
    undated, so the tip is the childless one with the lowest profile ID rather
    than a dated person who is not where the line stops.
    """
    _, tip = descendants.line_reach(_tree(STALLED))
    assert tip["1"] == "6"  # F, born 1465 — later than E and childless

    _, tip = descendants.line_reach(_tree(DIAMOND))
    assert tip["10"] == "16"  # S: the only childless descendant


def test_reach_is_none_when_nothing_in_the_line_carries_a_date():
    """Undated is not year zero and must not become a stall."""
    reach, tip = descendants.line_reach(_tree(DIAMOND))
    assert reach["12"] is None
    assert tip["12"] == "16"


# ---------------------------------------------------------------- candidates


def test_zero_descendants_is_not_a_candidate():
    """A leaf may be childless or unexplored, and our data cannot tell which."""
    lines = descendants.build_lines(_tree(STALLED))
    picked = descendants.candidates(lines, present=2026)
    assert all(line.paths > 0 for line in picked)
    assert "5" not in {line.geni_id for line in picked}


def test_small_ceiling_excludes_lines_we_have_already_walked():
    lines = descendants.build_lines(_tree(DIAMOND))
    assert lines["10"].paths == 6
    assert "10" in {c.geni_id for c in descendants.candidates(lines, present=2026, small=6)}
    assert "10" not in {c.geni_id for c in descendants.candidates(lines, present=2026, small=5)}


def _line(geni_id: str, **kw) -> descendants.Line:
    """A Line with every ranked field pinned, so a test can vary exactly one."""
    fields = dict(
        geni_id=geni_id, name="X", birth=1500, generation=0,
        paths=2, children=2, child_ids=(), depth=1,
        reach=1500, open_paths=2,
    )
    fields.update(kw)
    return descendants.Line(**fields)


def _order(*lines) -> list[str]:
    return [l.geni_id for l in descendants.candidates(list(lines), present=2026, small=99)]


def test_a_line_walked_fewer_generations_ranks_first():
    """Depth is the primary key: one generation down is a line we stopped at."""
    assert _order(
        _line("2", depth=3, open_paths=9, paths=9),
        _line("1", depth=1, open_paths=1, paths=1),
    ) == ["1", "2"]


def test_more_open_paths_breaks_a_tie_on_depth():
    """Each childless end is another place Geni may carry the line on from."""
    assert _order(
        _line("3", depth=2, open_paths=1),
        _line("4", depth=2, open_paths=4),
    ) == ["4", "3"]


def test_the_better_attested_family_breaks_a_tie_on_open_paths():
    """Documented as a judgement, so pinned: more descent paths ranks first.

    Ranking the other way would put the enormous tail of one-child stubs at the
    top of every band.
    """
    assert _order(
        _line("5", depth=2, open_paths=2, paths=3),
        _line("6", depth=2, open_paths=2, paths=8),
    ) == ["6", "5"]


def test_stall_no_longer_decides_the_order():
    """It sorted every band by birth year, which is where the band edge fell.

    The older person here is the shallower line and wins on depth; under the
    stall ranking they would have won for being older, whatever their depth.
    """
    old_and_deep = _line("7", birth=1200, reach=1260, depth=4)
    recent_and_shallow = _line("8", birth=1900, reach=1930, depth=1)
    assert old_and_deep.stall(2026) > recent_and_shallow.stall(2026)
    assert _order(old_and_deep, recent_and_shallow) == ["8", "7"]


def test_the_stalled_line_is_still_reported_even_though_it_is_not_ranked_on():
    _, lines, _ = _lines(STALLED)
    assert lines["1"].stall(2026) == 2026 - 1465
    assert lines["1"].followed == 1465 - 1400


def test_a_candidate_below_another_candidate_is_dropped():
    """C's whole line is inside A's, and an export from A covers both."""
    _, lines, parents = _lines(STALLED)
    picked = {c.geni_id for c in descendants.candidates(lines, present=2026, parents=parents)}
    assert "1" in picked  # A, the top of the chain
    assert "3" not in picked  # C, whose parent A is also a candidate


def test_nesting_is_not_dropped_without_a_parent_map():
    """The drop is opt-in: a caller that does not pass parents gets every line."""
    _, lines, _ = _lines(STALLED)
    picked = {c.geni_id for c in descendants.candidates(lines, present=2026)}
    assert {"1", "3"} <= picked


def test_a_line_with_no_dates_sorts_after_an_otherwise_identical_dated_one():
    """`followed` is unknown, not zero, and must not sort like a small number."""
    assert _order(
        _line("9", birth=None, reach=None),
        _line("10", birth=1500, reach=1600),
    ) == ["10", "9"]
    assert _line("9", birth=None, reach=None).followed is None


def test_min_stall_drops_lines_already_followed_close_to_now():
    lines = descendants.build_lines(_tree(STALLED))
    assert descendants.candidates(lines, present=2026, min_stall=1000) == []
    assert descendants.candidates(lines, present=2026, min_stall=500)


# ---------------------------------------------------------------- reachability


def test_a_seed_born_too_early_cannot_reach_the_target():
    """The constraint the 2026-08-07 backtest established, and it comes first.

    A ball carries about twelve generations. Eleven exports seeded on medieval
    people added 18,218 people and four of them were born after 1900 — so a
    ranking that sorts among unreachable seeds is sorting the wrong set.
    """
    medieval = _line("1", birth=1300)
    georgian = _line("2", birth=1800)
    assert medieval.can_reach(1900) is False
    assert georgian.can_reach(1900) is True


def test_the_screen_is_exactly_generations_times_years():
    """Stated as arithmetic in the docstring, so pinned as arithmetic."""
    edge = descendants.REACH_TARGET - descendants.REACH_GENERATIONS * descendants.GENERATION_YEARS
    assert _line("3", birth=edge).can_reach(descendants.REACH_TARGET) is True
    assert _line("4", birth=edge - 1).can_reach(descendants.REACH_TARGET) is False


def test_a_wide_descent_reaches_less_far_than_a_narrow_one():
    """Width is what the flat twelve-generation screen was missing.

    A breadth-first ball costs ``branching ** k`` to reach generation k, so
    twenty children spend the whole budget in three generations where two
    children buy twelve. Ignoring this passed a person born 1670 with nineteen
    recorded children as able to reach 1900, when they land around 1755.
    """
    narrow = _line("1", birth=1670, children=2)
    wide = _line("2", birth=1670, children=19)
    assert narrow.generations_affordable() == descendants.REACH_GENERATIONS
    assert wide.generations_affordable() < 4
    assert narrow.can_reach(1900) is True
    assert wide.can_reach(1900) is False
    assert wide.arrives() < 1800


def test_a_late_birth_beats_width():
    """Twenty children born in 1858 still arrive; the same family in 1670 does not."""
    assert _line("3", birth=1858, children=20).can_reach(1900) is True
    assert _line("4", birth=1670, children=20).can_reach(1900) is False


def test_a_married_couple_is_one_export_not_two():
    """Ranks 1 and 2 of the campaign list were a couple with the same 20 children.

    Both parents descend to the identical set, so a `Descendants` export from
    either returns the same ball. Not an edge case at the top of this ranking —
    it rewards a large recorded family, and both parents of one score alike.
    """
    husband = _line("1", birth=1858, child_ids=("10", "11", "12"))
    wife = _line("2", birth=1855, child_ids=("10", "11", "12"))
    other = _line("3", birth=1860, child_ids=("20",))
    kept = descendants.drop_duplicate_balls([husband, wife, other])
    assert [line.geni_id for line in kept] == ["1", "3"]


def test_childless_candidates_are_never_merged_together():
    """An empty child set is not evidence of anything shared."""
    a = _line("4", child_ids=())
    b = _line("5", child_ids=())
    assert len(descendants.drop_duplicate_balls([a, b])) == 2


def test_the_browsable_page_is_self_contained():
    """`out/` is scratch opened straight off disk — no network at all."""
    page = descendants.render_html(
        [_line("1", birth=1858, children=6), _line("2", birth=1902, children=3)],
        target=1900, tree_size=275437,
    )
    assert "https://www.geni.com/people/x/1" in page  # profile links are fine
    for remote in ("<script src", "<link rel=stylesheet", "@import", "fonts.googleapis"):
        assert remote not in page
    assert "1850s" in page and "1900s" in page  # decade filters exist


def test_an_undated_person_is_kept_rather_than_screened_out():
    """Rejecting them would be inferring a date from silence.

    They cannot appear in the campaign section — it is a birth-year screen — but
    they must not be treated as born too early.
    """
    assert _line("5", birth=None).can_reach(1900) is True


def test_the_report_leads_with_the_reachable_seeds():
    tree = _tree(STALLED)
    lines = descendants.build_lines(tree)
    parents = descendants.parent_map(tree)
    by_birth, by_generation = descendants.bands(lines, present=2026, parents=parents)
    text = descendants.render_markdown(
        tree, lines, by_birth, by_generation,
        present=2026, small=20, width=100, min_stall=0,
        target=1900, parents=parents,
    )
    assert "## Seeds that can reach 1900" in text
    # Everyone in STALLED is born in the 1400s, so none of them can arrive.
    assert "None: no candidate is born" in text
    # And the section must come before the background it demotes.
    assert text.index("Seeds that can reach") < text.index("## By period")


def test_a_reachable_candidate_is_listed_with_its_own_target():
    text_tree = STALLED.replace("2 DATE 1400", "2 DATE 1840").replace(
        "2 DATE 1430", "2 DATE 1870").replace("2 DATE 1460", "2 DATE 1895"
    ).replace("2 DATE 1465", "2 DATE 1899")
    tree = _tree(text_tree)
    lines = descendants.build_lines(tree)
    parents = descendants.parent_map(tree)
    by_birth, by_generation = descendants.bands(lines, present=2026, parents=parents)
    text = descendants.render_markdown(
        tree, lines, by_birth, by_generation,
        present=2026, small=20, width=100, min_stall=0,
        target=1900, parents=parents,
    )
    assert "None: no candidate is born" not in text
    assert "candidates qualify" in text


# ---------------------------------------------------------------- bands


def test_bands_group_by_birth_year_and_keep_the_undated_separate():
    lines = descendants.build_lines(_tree(STALLED))
    banded = descendants.band_by_birth(lines, present=2026, width=100)
    labels = {b.label for b in banded}
    assert "1400–1499" in labels
    assert "undated" in labels
    assert banded[-1].label == "undated"


def test_bc_years_band_downwards_not_towards_zero():
    """-450 belongs to the band starting at -500, which floor division gives."""
    text = STALLED.replace("2 DATE 1400", "2 DATE -450")
    lines = descendants.build_lines(_tree(text))
    labels = [b.label for b in descendants.band_by_birth(lines, present=2026, width=100)]
    assert "500 BC–401 BC" in labels


def test_generation_bands_can_rank_people_the_period_view_cannot():
    """Every DIAMOND person below P is undated; the generation view still ranks them."""
    lines = descendants.build_lines(_tree(DIAMOND))
    banded = descendants.band_by_generation(lines, present=2026, width=5)
    assert sum(b.total_candidates for b in banded) > 0


def test_per_band_trims_picks_but_not_the_candidate_count():
    _, lines, parents = _lines(STALLED)
    banded = descendants.band_by_birth(
        lines, present=2026, width=100, per_band=1, parents=parents
    )
    band = next(b for b in banded if b.label == "1400–1499")
    assert len(band.picks) == 1
    assert band.total_candidates == 2  # A and G; C is nested inside A
    assert band.picks[0].geni_id == "7"  # G, the worse-followed of the two


# ---------------------------------------------------------------- rendering


def test_report_names_the_stall_year_and_both_views():
    tree = _tree(STALLED)
    lines = descendants.build_lines(tree)
    by_birth, by_generation = descendants.bands(lines, present=2026)
    text = descendants.render_markdown(
        tree, lines, by_birth, by_generation,
        present=2026, small=20, width=100, min_stall=0,
    )
    assert "## By period" in text
    assert "## By generation" in text
    assert "2026" in text
    # The caveat is the point of the report, not decoration.
    assert "not Geni's content" in text


def test_seed_list_offers_the_tip_as_well_as_the_candidate():
    """"Export from them **or near them**" is two different exports."""
    _, lines, parents = _lines(STALLED)
    banded = descendants.band_by_birth(
        lines, present=2026, width=100, per_band=1, parents=parents
    )
    text = descendants.render_seed_list(banded)
    assert "https://www.geni.com/people/x/7 |" in text  # G, the candidate
    assert "https://www.geni.com/people/x/9 |" in text  # I, where G's line stops
    assert "tip of" in text


def test_a_pipe_in_a_name_cannot_break_the_table():
    """257219 names typed by strangers, rendered into Markdown table cells."""
    tree = _tree(STALLED.replace("1 NAME G /Second/", "1 NAME G|X /Se[co]nd/"))
    lines = descendants.build_lines(tree)
    by_birth, by_generation = descendants.bands(
        lines, present=2026, parents=descendants.parent_map(tree)
    )
    text = descendants.render_markdown(
        tree, lines, by_birth, by_generation,
        present=2026, small=20, width=100, min_stall=0,
    )
    row = next(l for l in text.splitlines() if "G\\|X" in l)
    # The escaped pipe does not count as a cell boundary; 11 columns is 12 bars.
    assert row.replace("\\|", "").count("|") == len(descendants._HEADER) + 1
    assert "Se\\[co\\]nd" in row


def test_seed_list_does_not_repeat_a_candidate_who_is_their_own_tip():
    lines = descendants.build_lines(_tree(DIAMOND))
    banded = descendants.band_by_birth(lines, present=2026, width=100)
    text = descendants.render_seed_list(banded)
    for line in text.splitlines():
        assert line.count("http") == 1


# ---------------------------------------------------------------- saturation


def test_the_sum_saturates_rather_than_growing_without_bound():
    """Path counts compound through shared subtrees; the ceiling caps display only."""
    paths, open_paths = descendants.descent_paths(_tree(DIAMOND), ceiling=3)
    assert paths["10"] == 3  # would be 6
    assert paths["12"] == 2  # under the ceiling, so untouched
    assert open_paths["10"] == 2


def test_saturation_is_far_enough_above_small_to_never_decide_candidacy():
    """The ceiling is a display bound, not a filter — pinned so it stays one."""
    assert descendants.PATH_CEILING > descendants.SMALL * 10**9


def test_the_default_ceiling_leaves_real_counts_untouched():
    lines = descendants.build_lines(_tree(DIAMOND))
    assert lines["10"].paths == 6


# ---------------------------------------------------------------- robustness


def test_someone_with_a_child_in_a_cycle_is_never_reported_as_a_leaf():
    """The bug that put a data artefact at the top of the largest band.

    `_post_order` drops the edge back into a node still being expanded, so a
    child inside a cycle is missing from `depth` when the parent is measured.
    Falling through to 0 made a person with descent paths look childless — and
    depth is ranked **ascending**, so they sorted above every real candidate.
    """
    # W -> X, and X <-> Y are each other's parent and child. X's depth is
    # truncated by the cycle; it must not come out as zero, and neither may W's.
    cyclic = """0 HEAD
0 @I30@ INDI
1 NAME W /Top/
1 FAMS @F30@
0 @I31@ INDI
1 NAME X /Loop/
1 FAMC @F30@
1 FAMS @F31@
1 FAMC @F32@
0 @I32@ INDI
1 NAME Y /Loop/
1 FAMC @F31@
1 FAMS @F32@
0 @F30@ FAM
1 HUSB @I30@
1 CHIL @I31@
0 @F31@ FAM
1 HUSB @I31@
1 CHIL @I32@
0 @F32@ FAM
1 HUSB @I32@
1 CHIL @I31@
0 TRLR
"""
    tree = _tree(cyclic)
    depth = descendants.descendant_depth(tree)
    paths, _ = descendants.descent_paths(tree)

    # The invariant, stated once and checked for everyone: recorded children
    # and zero depth cannot both be true.
    for geni_id in tree.people:
        assert (paths[geni_id] > 0) == (depth[geni_id] > 0), geni_id
    assert depth["30"] >= 1


def test_ancestor_depth_has_the_same_invariant():
    """One line apart from the above, written the same day, same fall-through.

    Compared against the *filtered* parent map, not ``Person.parent_ids``: a
    pointer to a profile no export has reached is not an ancestor we can walk,
    and treating it as one would make this assertion fail for a reason that has
    nothing to do with the bug it pins.
    """
    tree = _tree(STALLED)
    depth = frontier.ancestor_depth(tree)
    parents = descendants.parent_map(tree)
    for geni_id in tree.people:
        assert bool(parents[geni_id]) == (depth[geni_id] > 0), geni_id


def test_a_cycle_does_not_hang_the_walks():
    """Somebody entered twice and linked to themselves is ordinary here."""
    cyclic = """0 HEAD
0 @I20@ INDI
1 FAMC @F21@
1 FAMS @F20@
0 @I21@ INDI
1 FAMC @F20@
1 FAMS @F21@
0 @F20@ FAM
1 HUSB @I20@
1 CHIL @I21@
0 @F21@ FAM
1 HUSB @I21@
1 CHIL @I20@
0 TRLR
"""
    lines = descendants.build_lines(_tree(cyclic))
    assert set(lines) == {"20", "21"}
