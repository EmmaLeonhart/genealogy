"""Unit tests for the profile-content measurement.

The logic — script classification, field presence, the CJK romanisation split —
is pinned on hand-written trees so a change to what the report claims fails here.
A single real export is used only as a smoke test that `measure` runs over
Geni's actual data and produces internally consistent totals; the numbers over
the full merge live in `reports/profile-names.md`, not in an assertion.
"""

from __future__ import annotations

import pytest

from genimerge import gedcom, profilenames, sources
from genimerge.model import build_tree

# A small tree exercising every branch: a romanised-and-native CJK person, a
# native-only CJK person, a Latin person with a multi-token given name, a
# Cyrillic person, and a person with no name at all.
TREE = """0 HEAD
0 @I1@ INDI
1 NAME Yuzuki no Kimi /Hata/
2 GIVN Yuzuki no Kimi
2 _MARNM Hata
1 NAME 弓月君 /秦/
2 GIVN 弓月君
2 SURN 秦
1 SEX M
1 BIRT
2 DATE 283
2 PLAC Baekje
1 FAMS @F1@
1 RFN geni:1
0 @I2@ INDI
1 NAME 意美 /秦/
2 GIVN 意美
2 SURN 秦
1 SEX F
1 FAMC @F1@
1 RFN geni:2
0 @I3@ INDI
1 NAME Jean Paul /Braut/
2 GIVN Jean Paul
2 SURN Braut
1 SEX M
1 OCCU Farmer
1 DEAT
2 DATE 1901
1 RFN geni:3
0 @I4@ INDI
1 NAME Владимир /Мономах/
2 GIVN Владимир
2 SURN Мономах
1 SEX M
1 RFN geni:4
0 @I5@ INDI
1 RFN geni:5
0 TRLR
"""


def cov():
    return profilenames.measure(build_tree(gedcom.parse(TREE).records))


def test_every_person_is_counted():
    assert cov().people == 5


def test_scripts_are_classified_by_unicode_block():
    c = cov()
    assert c.scripts["cjk"] == 2       # I1 (also latin) and I2
    assert c.scripts["cyrillic"] == 1  # I4
    # I1 carries both a native and a romanised form, I3 is Latin.
    assert c.scripts["latin"] == 2


def test_the_cjk_romanisation_gap_is_split_out():
    c = cov()
    # I1 has both scripts, I2 is native-only.
    assert c.cjk_and_latin == 1
    assert c.cjk_only == 1


def test_a_latin_marnm_on_a_cjk_person_counts_as_their_romanisation():
    # I1's only Latin form is the _MARNM 'Hata' and the romanised NAME value;
    # dropping _MARNM from the script scan would misreport them as native-only.
    person = build_tree(gedcom.parse(TREE).records).people["1"]
    assert "latin" in profilenames.scripts_of(person)
    assert "cjk" in profilenames.scripts_of(person)


def test_field_presence_tracks_the_model():
    f = cov().fields
    assert f["sex"] == 4          # everyone but the unnamed I5
    assert f["given"] == 4
    assert f["surname"] == 4      # I1 native, I2, I3, I4
    assert f["birth_date"] == 1   # I1
    assert f["birth_place"] == 1  # I1
    assert f["death_date"] == 1   # I3
    assert f["occupation"] == 1   # I3
    assert f["parents"] == 1      # I2 is a child in F1
    assert f["marriage"] == 1     # I1 is a spouse in F1


def test_multi_token_given_is_split_by_script_not_lumped():
    c = cov()
    # I1 "Yuzuki no Kimi" is the romanised-CJK trap; I3 "Jean Paul" is the real
    # P1545 case. They must not be counted as the same thing.
    assert c.multi_given_cjk == 1
    assert c.multi_given_latin == 1
    assert c.fields["given_multi"] == 2


def test_people_with_no_name_are_counted_not_dropped():
    assert cov().unnamed == 1


def test_summary_is_a_flat_consistent_dict():
    c = cov()
    s = profilenames.summarise(c)
    assert s["people"] == 5
    assert s["cjk_only"] + s["cjk_and_latin"] == c.scripts["cjk"]
    assert s["field:sex"] == 4


def test_an_empty_tree_measures_to_zero():
    from genimerge.model import Tree

    c = profilenames.measure(Tree())
    assert c.people == 0 and c.cjk_only == 0
    assert profilenames.render_markdown(c)  # renders without dividing by zero


def test_the_report_states_it_proposes_nothing_and_names_the_traps():
    text = profilenames.render_markdown(cov())
    assert "# What is in the profiles" in text
    assert "creates anything" in text or "creates nothing" in text
    assert "P1545" in text                 # the multi-token trap is explained
    assert "romanisation gap" in text.lower()


# -- smoke test against real data --------------------------------------

# **`geni_exports`, not `find_exports`.** This asserts something about what a GENI export
# is, and `exports/0-scraped/` is built by us from saved pages and paths -- it is in the
# merge on purpose but is not something Geni returned. See `sources.DERIVED_DIR`.
_EXPORTS = sources.geni_exports()


@pytest.mark.skipif(not _EXPORTS, reason="no GEDCOM exports in exports/")
def test_measure_runs_over_a_real_export_with_consistent_totals():
    tree = build_tree(gedcom.stream_file(_EXPORTS[0]))
    c = profilenames.measure(tree)
    assert c.people > 0
    # Every field count is a share of the whole population.
    for key, count in c.fields.items():
        assert 0 <= count <= c.people, key
    # The CJK split partitions the CJK population exactly.
    assert c.cjk_only + c.cjk_and_latin == c.scripts["cjk"]
    # Sex and a given name are near-universal in Geni data; assert only that
    # they are the common case, not an exact rate that would rot.
    assert c.fields["sex"] > 0.5 * c.people
