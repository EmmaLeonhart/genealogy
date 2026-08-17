"""Checking a Geni relationship path against the tree.

The unit tests use a small synthetic tree; the tests at the bottom run the real
`paths/jimmu.tsv` against the real merge, because the two findings
this file exists to protect — where the path breaks, and that both of its ends
are held — are properties of the actual data.
"""

from pathlib import Path

import pytest

from genimerge import gedcom, paths, sources
from genimerge.model import build_tree

REPO = Path(__file__).resolve().parents[1]
JIMMU = REPO / "paths" / "jimmu.tsv"
EXPORTS = sources.find_exports()


# Elisabeth carries an alternate name that is a subset of Jelena's full style,
# which is how the first run of this report matched two different steps of the
# path to the same profile. `AMBIGUOUS_NAME` is shared by enough people to go
# past `AMBIGUITY_LIMIT`.
TINY = """0 HEAD
0 @I100@ INDI
1 NAME Elisabeth /Árpád dynasty/
2 GIVN Elisabeth
2 SURN Árpád dynasty
1 NAME Queen consort of Hungary
1 FAMS @F1@
0 @I200@ INDI
1 NAME Gulleik Jakobsson /Øye/
2 GIVN Gulleik Jakobsson
2 SURN Øye
1 FAMS @F1@
0 @I300@ INDI
1 NAME Okoshi /Mononobe/
2 GIVN Okoshi
2 SURN Mononobe
1 FAMC @F1@
0 @I400@ INDI
1 NAME Arayama
2 GIVN Arayama
0 @F1@ FAM
1 HUSB @I200@
1 WIFE @I100@
1 CHIL @I300@
0 TRLR
"""

CROWD = "0 HEAD\n" + "".join(
    f"0 @I{900 + n}@ INDI\n1 NAME n /n/\n2 GIVN n\n2 SURN n\n" for n in range(8)
) + "0 TRLR\n"


def tree(*texts):
    records = []
    for text in texts:
        records += gedcom.parse(text).records
    built = build_tree(records)
    built.resolve_relationships()
    return built


def check(text, source=TINY):
    return paths.check(tree(source), paths.parse_path(text))


def test_normalise_folds_case_accents_and_punctuation():
    assert paths.normalise("Gulleik Jakobsson Øye") == "gulleik jakobsson oye"
    assert paths.normalise("Håkon V Magnusson, King of Norway") == (
        "hakon v magnusson king of norway"
    )
    assert paths.normalise("Keiko-tenno (Otarashihiko'oshirowake)") == (
        "keiko tenno otarashihiko oshirowake"
    )


def test_normalise_leaves_cjk_alone():
    assert paths.normalise("播磨稲日大郎姫") == "播磨稲日大郎姫"


def test_parse_skips_comments_and_header():
    steps = paths.parse_path(
        "# a comment\n"
        "step\tname\trelation_to_previous\tnote\n"
        "1\tYou\t-\tgeni:6000000087535357291\n"
        "2\tRichard Wade Borsheim\tyour father\n"
    )
    assert [s.step for s in steps] == [1, 2]
    assert steps[0].relation == ""  # "-" means no relation, not a relation named "-"
    assert steps[0].geni_id == "6000000087535357291"
    assert steps[1].note == ""  # a missing trailing column is not an error
    assert steps[1].geni_id == ""


def test_a_note_without_an_id_yields_no_id():
    step = paths.PathStep(step=1, name="x", note="unnamed on Geni --- a description")
    assert step.geni_id == ""


def test_an_id_in_the_note_wins_over_the_name():
    report = check("1\tsomeone else entirely\t-\tgeni:100\n")
    assert report.results[0].how == paths.BY_ID
    assert report.results[0].person.geni_id == "100"


def test_a_person_walked_twice_is_held_both_times():
    """A saved Geni page can hold two relationship paths, so the second chain
    restarts at "You" and re-walks the first few people. `paths/nn-basse.tsv`
    does this at steps 36-44.

    Those rows used to be reported ABSENT, because the rule that refuses a
    person to a second step — right for a name, wrong for an exact ID — shared
    a branch with "the ID is not in the tree". It read the account owner
    himself as somebody we do not hold, and `connectors` then offered that run
    as a nine-person bridge worth taking an export for.
    """
    report = check("1\tsomeone\t-\tgeni:100\n2\tsomeone again\this son\tgeni:100\n")

    assert [r.how for r in report.results] == [paths.BY_ID, paths.REPEAT]
    assert all(r.held for r in report.results)
    assert report.absent == []


def test_a_row_with_no_relation_starts_a_new_chain():
    """Emma, 2026-08-16: *"treat it as being two paths and not one."*

    Geni shows a pair a blood path and an in-law path, and `path-from-html`
    writes both into one file. The boundary is stated rather than guessed: only
    the head of a path has nothing to relate back to.
    """
    steps = paths.parse_path(
        "1\tYou\t-\tgeni:100\n"
        "2\ther mother\this mother\tgeni:200\n"
        "3\tYou\t-\tgeni:100\n"
        "4\ther husband\ther husband\tgeni:300\n"
    )
    assert [s.chain for s in steps] == [1, 1, 2, 2]


def test_the_run_and_the_doorway_belong_to_the_first_chain_only():
    """A fully-held first path must not borrow the second path's doorway.

    Without the chain bound the scan runs off the end of path one, and a file
    whose first path is complete reports a doorway belonging to a different chain
    of people — which `connectors` then ranks an export by.
    """
    report = check(
        "1\tsomeone\t-\tgeni:100\n"
        "2\this wife\this wife\tgeni:200\n"
        "3\tsomeone\t-\tgeni:100\n"
        "4\tghost\this son\tgeni:404\n"
    )
    chains = report.chains
    assert [len(c.results) for c in chains] == [2, 2]
    assert [len(c.held) for c in chains] == [2, 1]
    # Path one is whole, so its run ends at its own last step, not at step 3.
    assert report.run_ends_at.step.step == 2
    assert report.held_beyond_the_gap == []
    assert chains[1].run_ends_at.step.step == 3


def test_a_gap_never_spans_two_chains():
    """Consecutive step numbers across the seam are two gaps, not one."""
    report = check(
        "1\tsomeone\t-\tgeni:100\n"
        "2\tghost\this son\tgeni:404\n"
        "3\tghost two\t-\tgeni:405\n"
        "4\tghost three\this son\tgeni:406\n"
    )
    assert paths._gaps(report) == [(2, 2), (3, 4)]


def test_a_repeat_of_a_person_we_lack_is_still_absent():
    """The two conditions are independent, and only one of them means a gap."""
    report = check("1\tghost\t-\tgeni:404\n2\tghost again\this son\tgeni:404\n")

    assert [r.how for r in report.results] == [paths.ABSENT, paths.ABSENT]
    assert len(report.absent) == 2


def test_a_repeat_still_carries_the_person_and_their_component():
    report = check("1\tsomeone\t-\tgeni:100\n2\tsomeone again\this son\tgeni:100\n")
    second = report.results[1]

    assert second.person is not None and second.person.geni_id == "100"
    assert second.component == report.results[0].component


def test_exact_match_survives_accents_and_surname_slashes():
    report = check("1\tGulleik Jakobsson Oye\this father\n")
    assert report.results[0].how == paths.EXACT
    assert report.results[0].person.geni_id == "200"


def test_partial_match_when_the_path_is_longer_than_the_record():
    report = check("1\tOkoshi Mononobe no Muraji\ther father\n")
    assert report.results[0].how == paths.PARTIAL
    assert report.results[0].person.geni_id == "300"


def test_one_shared_token_is_not_enough_for_a_partial_match():
    """`MIN_SHARED_TOKENS` in practice.

    The record is the bare given name `Arayama`, and the path says
    `Arayama Mononobe`. One token in common is a coincidence as often as a
    match, and this report would rather miss a person than name the wrong one.
    """
    report = check("1\tArayama Mononobe\this father\n")
    assert report.results[0].how == paths.ABSENT


def test_absent_when_nobody_matches():
    report = check("1\tConstantine IX Monomachos\ther brother\n")
    assert report.results[0].how == paths.ABSENT
    assert report.results[0].held is False


def test_a_person_settled_by_one_step_is_not_offered_to_the_next():
    """The regression this module was rewritten for.

    Step 2's name shares `queen consort of hungary` with step 1's alternate
    name, so a subset match reaches it. Two steps of a relationship path are two
    different people, so the second must come back absent rather than reporting
    the doorway as already held.
    """
    report = check(
        "1\tElisabeth, princess of Hungary\ther mother\tgeni:100\n"
        "2\tJelena Urošević, Queen consort of Hungary\ther mother\n"
    )
    assert report.results[0].person.geni_id == "100"
    assert report.results[1].how == paths.ABSENT


def test_a_name_shared_by_a_crowd_is_unresolved_not_held():
    report = check("1\tn n\this mother\n", source=CROWD)
    result = report.results[0]
    assert result.how == paths.UNRESOLVED
    assert len(result.candidates) > paths.AMBIGUITY_LIMIT
    assert result.held is False, "an unidentifying name must not count as held"


def test_run_ends_at_the_last_step_before_the_first_gap():
    report = check(
        "1\tGulleik Jakobsson Oye\t-\n"
        "2\tNobody At All\this father\n"
        "3\tOkoshi Mononobe no Muraji\this father\n"
    )
    assert report.run_ends_at.step.step == 1
    assert [r.step.step for r in report.held_beyond_the_gap] == [3]


def test_report_says_it_is_advisory():
    report = check("1\tGulleik Jakobsson Oye\t-\n")
    text = paths.render_markdown(report, "t")
    assert paths.NAME_MATCHING_IS_ADVISORY in text
    assert "profile ID" in text


# --- the real path against the real merge ------------------------------------

#: **`slow` is part of this**: these are the tests that load the real merge, and
#: they take minutes. The pure-logic tests above carry neither mark and stay in the
#: fast lane. Not skipped by default — `-m "not slow"` is a deliberate opt-out.
pytestmark_real = pytest.mark.skipif(
    not EXPORTS or not JIMMU.exists(), reason="no exports or no path file"
)


def _real(func):
    """`skipif` plus `slow`, so the real-merge tests carry both."""
    return pytestmark_real(pytest.mark.slow(func))


@pytest.fixture(scope="module")
def jimmu():
    from genimerge import merge

    if not EXPORTS or not JIMMU.exists():
        pytest.skip("no exports or no path file")
    doc, _ = merge.merge_files(EXPORTS)
    built = build_tree(doc.records)
    return paths.check(built, paths.load_path(JIMMU))


@_real
def test_the_path_file_runs_from_the_account_owner_to_jimmu(jimmu):
    first, last = jimmu.results[0], jimmu.results[-1]
    assert first.person.geni_id == "6000000087535357291", "step 1 is Emma Leonhart"
    assert last.step.name == "Emperor Jimmu"
    assert last.person.geni_id == "6000000001829589817"


@_real
def test_both_ends_of_the_path_are_held_in_one_component(jimmu):
    """The two ends met on 2026-08-04.

    This assertion used to read `first.component != last.component` and
    `len(components_touched) == 2`, with a docstring saying that if the two ever
    landed in the same component an export had bridged the trees and it should
    be rewritten rather than deleted. That is what happened, so it is rewritten.
    It now guards the other direction: a future export must not *split* the
    tree, and a merge that loses the bridging records fails here.
    """
    first, last = jimmu.results[0], jimmu.results[-1]
    assert first.held and last.held
    assert first.component == last.component
    assert len(jimmu.components_touched) == 1


@_real
def test_there_is_no_gap_left_in_the_path(jimmu):
    """Nothing absent, where a 21-step block used to be.

    The history this replaces, because the numbers are the record of how the
    tree was actually built:

    - The block was **steps 31-51**, Jelena Urošević through Li Hong 李宏, and
      this test read `range(31, 52)`.
    - The `n n` export took 31-36 and the `Li Hong` forest export took 43-51,
      from opposite ends, leaving `range(37, 43)`.
    - Two `Forest` exports seeded in that six-person window closed it. The path
      crosses `her brother`, `his partner` and `her husband` links there, so
      only a style that follows marriages could have bridged it.

    A failure here means an absence has reappeared: either an export was
    dropped from `exports/` or the merge stopped keeping something it kept.
    """
    absent = [r.step.step for r in jimmu.results if not r.held]
    assert absent == []


@_real
def test_the_path_is_unbroken_the_whole_way_to_jimmu(jimmu):
    """All 83 steps, with the checkpoints that were once the end of the run.

    Steps 1-30 are the original claim, measured exactly: this is the assertion
    that vindicates the summary an earlier session wrote from the Geni page and
    could not re-check. Matching the same path by *name* put eleven holes in
    that run; every one was a spelling difference rather than an absence, and
    joining on the profile ID removes all eleven.

    Elisabeth (30) and Helena (36) are each kept below because each was, in
    turn, the last held step on this path.
    """
    assert [r.step.step for r in jimmu.results if r.held] == list(range(1, 84))
    assert jimmu.run_ends_at.step.step == 83
    assert jimmu.results[29].person.geni_id == "6000000003243185408"  # Elisabeth
    assert jimmu.results[35].person.geni_id == "6000000002837351971"  # Helena


@_real
def test_every_step_joins_on_the_profile_id(jimmu):
    """No row falls back to name matching, so nothing here is advisory.

    `path-from-html` is what guarantees this. If a future path file is built by
    hand and loses an ID, this fails rather than the report quietly degrading to
    guesswork.
    """
    assert all(r.step.geni_id for r in jimmu.results)
    assert {r.how for r in jimmu.results} <= {paths.BY_ID, paths.ABSENT}
