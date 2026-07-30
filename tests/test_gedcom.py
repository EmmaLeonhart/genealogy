"""Tests for the GEDCOM reader/writer.

Fixtures are hand-written and tiny on purpose — the real exports are 24 MB and
using them here would turn a unit test into an integration test that fails for
reasons unrelated to the parser.
"""

from genimerge import gedcom
from genimerge.gedcom import Node, parse, serialize

# A cut-down but faithful sample of what Geni emits: the profile ID is the
# xref, and RFN repeats it.
SAMPLE = """0 HEAD
1 SOUR Geni.com
2 VERS 1.0
1 CHAR UTF-8
0 @I6000000087535357291@ INDI
1 NAME Eric /Borsheim/
2 GIVN Eric
2 SURN Borsheim
1 SEX M
1 BIRT
2 DATE 26 FEB 1996
2 PLAC Vancouver
1 FAMC @F6000000177921459249@
1 RFN geni:6000000087535357291
0 @F6000000177921459249@ FAM
1 HUSB @I6000000177921459056@
1 WIFE @I6000000177921459052@
1 CHIL @I6000000087535357291@
0 TRLR
"""


def test_parses_header_and_records():
    doc = parse(SAMPLE)

    assert doc.header is not None
    assert doc.header.path_value("SOUR") == "Geni.com"
    assert [r.tag for r in doc.records] == ["INDI", "FAM"]
    assert doc.warnings == []


def test_trailer_is_not_a_record():
    # TRLR carries no information and is re-created on write.
    assert "TRLR" not in [r.tag for r in parse(SAMPLE).records]


def test_xref_carries_the_geni_profile_id():
    indi = parse(SAMPLE).records[0]

    assert indi.xref == "@I6000000087535357291@"
    assert indi.value_of("RFN") == "geni:6000000087535357291"


def test_nested_values_are_reachable_by_path():
    indi = parse(SAMPLE).records[0]

    assert indi.path_value("BIRT", "DATE") == "26 FEB 1996"
    assert indi.path_value("BIRT", "PLAC") == "Vancouver"
    assert indi.path_value("BIRT", "NOWHERE", default="?") == "?"
    assert indi.path("NOPE") is None


def test_pointer_values_are_recognised():
    doc = parse(SAMPLE)
    indi, fam = doc.records

    assert indi.get("FAMC").pointer == "@F6000000177921459249@"
    assert [c.pointer for c in fam.all("CHIL")] == ["@I6000000087535357291@"]
    # A plain value is not a pointer, even though it contains a colon.
    assert indi.get("RFN").pointer is None
    assert indi.get("NAME").pointer is None


def test_all_returns_every_matching_child_in_order():
    doc = parse("0 @F1@ FAM\n1 CHIL @I1@\n1 CHIL @I2@\n0 TRLR\n")

    assert [c.value for c in doc.records[0].all("CHIL")] == ["@I1@", "@I2@"]
    assert doc.records[0].value_of("CHIL") == "@I1@"


def test_cont_becomes_a_newline_and_conc_a_straight_join():
    doc = parse(
        "0 @N1@ NOTE first line\n"
        "1 CONT second line\n"
        "1 CONC  continued\n"
        "0 TRLR\n"
    )

    assert doc.records[0].value == "first line\nsecond line continued"


def test_cont_folding_does_not_swallow_following_siblings():
    doc = parse("0 @I1@ INDI\n1 NOTE a\n2 CONT b\n2 SOUR @S1@\n1 SEX M\n0 TRLR\n")
    indi = doc.records[0]

    assert indi.value_of("NOTE") == "a\nb"
    assert indi.get("NOTE").value_of("SOUR") == "@S1@"
    assert indi.value_of("SEX") == "M"


def test_round_trip_is_a_fixpoint():
    once = parse(SAMPLE)
    twice = parse(serialize(once))

    assert twice.header == once.header
    assert twice.records == once.records


def test_round_trip_preserves_multiline_and_overlong_values():
    long_value = "x" * (gedcom.MAX_VALUE_LEN * 2 + 7)
    doc = gedcom.Gedcom()
    note = Node(tag="NOTE", xref="@N1@", value=f"{long_value}\nsecond\n\nfourth")
    doc.records.append(note)

    text = serialize(doc)
    reparsed = parse(text)

    assert reparsed.records[0].value == note.value
    # The wrapping actually happened rather than one 400-char physical line.
    assert max(len(line) for line in text.splitlines()) <= gedcom.MAX_VALUE_LEN + 16


def test_round_trip_preserves_a_value_with_leading_space():
    doc = parse("0 @N1@ NOTE first\n1 CONC  spaced\n0 TRLR\n")

    assert parse(serialize(doc)).records[0].value == "first spaced"


def test_unicode_line_separator_inside_a_value_is_not_a_line_break():
    # The Ancestors export carries U+2028 inside note text. str.splitlines()
    # treats it as a line ending; a file read with newline="" does not. If
    # parse() disagrees with parse_file() here, the round trip silently
    # rewrites those notes.
    doc = parse("0 @N1@ NOTE before\u2028after\n0 TRLR\n")

    assert doc.records[0].value == "before\u2028after"
    assert parse(serialize(doc)).records[0].value == "before\u2028after"


def test_serialize_always_emits_a_trailer():
    assert serialize(gedcom.Gedcom()).splitlines()[-1] == "0 TRLR"


def test_unparseable_lines_are_warned_about_not_fatal():
    doc = parse("0 @I1@ INDI\nthis is not a gedcom line\n1 SEX F\n0 TRLR\n")

    assert doc.records[0].value_of("SEX") == "F"
    assert len(doc.warnings) == 1
    assert "line 2" in doc.warnings[0]


def test_level_jumps_are_clamped_rather_than_dropped():
    doc = parse("0 @I1@ INDI\n3 SEX M\n0 TRLR\n")

    assert doc.records[0].value_of("SEX") == "M"
    assert any("clamped" in w for w in doc.warnings)


def test_blank_lines_and_a_bom_are_tolerated():
    doc = parse("﻿0 @I1@ INDI\n\n1 SEX M\n\n0 TRLR\n")

    assert doc.records[0].xref == "@I1@"
    assert doc.warnings == []


def test_copy_is_deep():
    original = parse(SAMPLE).records[0]
    clone = original.copy()
    clone.get("BIRT").get("DATE").value = "1 JAN 1900"

    assert original.path_value("BIRT", "DATE") == "26 FEB 1996"


def test_by_xref_indexes_records():
    doc = parse(SAMPLE)

    assert set(doc.by_xref()) == {"@I6000000087535357291@", "@F6000000177921459249@"}
    assert [r.tag for r in doc.by_tag("FAM")] == ["FAM"]


def test_walk_yields_self_then_descendants_in_file_order():
    tags = [n.tag for n in parse(SAMPLE).records[0].walk()]

    assert tags == ["INDI", "NAME", "GIVN", "SURN", "SEX", "BIRT", "DATE", "PLAC", "FAMC", "RFN"]
