"""Finding thin regions — connected runs of people few exports reached."""

from collections import Counter
from pathlib import Path

import pytest

from genimerge import density, gedcom
from genimerge.model import build_tree

REPO = Path(__file__).resolve().parents[1]
DATA_LAKE = REPO / "data_lake"
EXPORTS = sorted(DATA_LAKE.glob("*.ged")) if DATA_LAKE.exists() else []


def _tree(text: str):
    return build_tree(list(gedcom.parse(text).records))


# Two families joined by a shared child, plus an unrelated pair. The shared
# child is what makes the first four one region rather than two.
CHAIN = """\
0 HEAD
0 @I1@ INDI
1 NAME A /X/
1 FAMS @F1@
0 @I2@ INDI
1 NAME B /X/
1 FAMS @F1@
0 @I3@ INDI
1 NAME C /X/
1 FAMC @F1@
1 FAMS @F2@
0 @I4@ INDI
1 NAME D /X/
1 FAMC @F2@
0 @I9@ INDI
1 NAME Z /Y/
1 FAMS @F9@
0 @I8@ INDI
1 NAME Y /Y/
1 FAMS @F9@
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
0 @F2@ FAM
1 HUSB @I3@
1 CHIL @I4@
0 @F9@ FAM
1 HUSB @I9@
1 WIFE @I8@
0 TRLR
"""


def test_presence_counts_one_file_per_person_not_one_per_mention(tmp_path):
    """A person named twice in one export counts once for that export."""
    a = tmp_path / "a.ged"
    a.write_text("0 @I1@ INDI\n0 @I1@ INDI\n0 @I2@ INDI\n", encoding="utf-8")
    b = tmp_path / "b.ged"
    b.write_text("0 @I2@ INDI\n", encoding="utf-8")

    counts = density.presence_counts([a, b])

    assert counts["1"] == 1
    assert counts["2"] == 2


def test_a_thin_run_is_one_region_and_the_unrelated_pair_is_another():
    tree = _tree(CHAIN)
    counts = Counter()  # nobody appears anywhere: everyone is thin

    regions = density.sparse_regions(tree, counts, threshold=1, min_size=2)

    assert [r.size for r in regions] == [4, 2]
    assert set(regions[0].members) == {"1", "2", "3", "4"}
    assert set(regions[1].members) == {"8", "9"}


def test_a_well_covered_person_splits_a_region_in_two():
    """The point of the measure. C is covered, so the run through C is broken.

    Without this, "thin region" would just mean "connected component" and the
    presence count would be doing nothing.
    """
    tree = _tree(CHAIN)
    counts = Counter({"3": 9})

    regions = density.sparse_regions(tree, counts, threshold=1, min_size=1)
    sizes = sorted(r.size for r in regions)

    assert "3" not in {m for r in regions for m in r.members}
    assert sizes == [1, 2, 2]  # D alone, A+B, and Y+Z


def test_singletons_are_dropped_because_every_ball_has_a_rim():
    """D is thin but isolated, so it is not a region. Y+Z still are."""
    tree = _tree(CHAIN)
    counts = Counter({"1": 9, "2": 9, "3": 9})  # of the ABCD run only D is thin

    kept = density.sparse_regions(tree, counts, threshold=1, min_size=2)
    assert [sorted(r.members) for r in kept] == [["8", "9"]]

    with_singletons = density.sparse_regions(tree, counts, threshold=1, min_size=1)
    assert sorted(sorted(r.members) for r in with_singletons) == [["4"], ["8", "9"]]


def test_regions_are_ranked_by_size_then_doorways():
    tree = _tree(CHAIN)
    regions = density.sparse_regions(tree, Counter(), threshold=1, min_size=2)

    assert regions == sorted(regions, key=lambda r: (-r.size, -r.parentless))


def test_doorways_counts_people_with_no_parents_recorded():
    tree = _tree(CHAIN)
    regions = density.sparse_regions(tree, Counter(), threshold=1, min_size=2)
    big = regions[0]

    # A and B have no FAMC; C and D do.
    assert big.parentless == 2


def test_the_report_says_what_the_measure_cannot_tell_you():
    """The caveat is load-bearing, not decoration.

    Presence measures our sampling, not Geni's content. A reader who takes a
    thin region as "Geni has little here" has it exactly backwards.
    """
    tree = _tree(CHAIN)
    counts = Counter()
    regions = density.sparse_regions(tree, counts, threshold=1, min_size=2)
    text = density.render_markdown(tree, counts, regions, export_count=2, threshold=1)

    assert "not Geni's content" in text
    assert "geographic" in text
    assert "doorway" in text.lower()


@pytest.mark.skipif(not EXPORTS, reason="no exports in data_lake/")
def test_presence_never_exceeds_the_number_of_exports():
    counts = density.presence_counts(EXPORTS)

    assert counts
    assert max(counts.values()) <= len(EXPORTS)


# --- picking one person to export from, per region -------------------------

# A region where the choice is not the obvious one: P is best-connected but has
# parents; Q is a doorway with a name; R is a doorway whose name is redacted.
PICK = """\
0 HEAD
0 @I10@ INDI
1 NAME Root /X/
1 FAMS @F10@
0 @I11@ INDI
1 NAME P /X/
1 FAMC @F10@
1 FAMS @F11@
0 @I12@ INDI
1 NAME Q /X/
1 FAMS @F11@
0 @I13@ INDI
1 NAME Private
1 FAMS @F12@
0 @I14@ INDI
1 NAME Kid /X/
1 FAMC @F11@
1 FAMC @F12@
0 @F10@ FAM
1 HUSB @I10@
1 CHIL @I11@
0 @F11@ FAM
1 HUSB @I11@
1 WIFE @I12@
1 CHIL @I14@
0 @F12@ FAM
1 HUSB @I13@
1 CHIL @I14@
0 TRLR
"""


def test_the_seed_is_a_doorway_even_when_a_non_doorway_is_better_connected():
    """P has the most relatives in the region and is not chosen: P has parents.

    The whole point of the seed is to grow *outward* into what Geni knows and we
    do not, and a person whose parents we already hold cannot do that upward.
    """
    tree = _tree(PICK)
    regions = density.sparse_regions(tree, Counter(), threshold=1, min_size=2)
    big = max(regions, key=lambda r: r.size)

    assert "11" in big.members  # P is in the region
    assert big.seed != "11"
    assert not tree.people[big.seed].has_known_parents


def test_a_redacted_name_loses_to_a_real_one_among_doorways():
    """Both Q and R are doorways; `Private` is useless to a human deciding."""
    tree = _tree(PICK)
    regions = density.sparse_regions(tree, Counter(), threshold=1, min_size=2)
    big = max(regions, key=lambda r: r.size)

    assert big.seed == "12"
    assert big.seed_name == "Q X"


def test_the_seed_list_is_in_the_shape_of_emmas_handwritten_file():
    """`<url> | Geni - <name>`, so it pastes straight into the file she keeps."""
    tree = _tree(PICK)
    regions = density.sparse_regions(tree, Counter(), threshold=1, min_size=2)
    text = density.render_seed_list(regions)

    assert text.endswith("\n")
    for line in text.strip().splitlines():
        url, name = line.split(" | ")
        assert url.startswith("https://www.geni.com/people/")
        assert name.startswith("Geni - ")


@pytest.mark.skipif(not EXPORTS, reason="no exports in data_lake/")
def test_every_listed_region_gets_a_seed_and_it_is_inside_the_region():
    """A seed from outside its own region would send an export to the wrong place."""
    from genimerge import merge as merge_mod
    from genimerge.model import build_tree as _build

    doc, _ = merge_mod.merge_files(EXPORTS)
    tree = _build(doc.records)
    counts = density.presence_counts(EXPORTS)
    regions = [r for r in density.sparse_regions(tree, counts) if r.size >= 100]

    assert regions
    for region in regions:
        assert region.seed, f"region of {region.size} has no seed"
        assert region.seed in region.members
        # The picker must never pass over a doorway when the region has one.
        if region.parentless:
            assert not tree.people[region.seed].has_known_parents
