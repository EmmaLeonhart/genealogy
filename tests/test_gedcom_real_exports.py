"""Integration check against the actual Geni exports in `data_lake/`.

The unit tests in `test_gedcom.py` use hand-written fixtures. This file exists
because the fixtures are what we *think* Geni emits, and these files are what it
*actually* emitted — the U+2028 handling in `parse` was found here, not there.

Skips when the exports are absent so a checkout without `data_lake/` still runs.
"""

import re
from pathlib import Path

import pytest

from genimerge import gedcom

DATA_LAKE = Path(__file__).resolve().parents[1] / "data_lake"
EXPORTS = sorted(DATA_LAKE.glob("*.ged"))

pytestmark = pytest.mark.skipif(not EXPORTS, reason="no GEDCOM exports in data_lake/")


@pytest.fixture(scope="module", params=[p.name for p in EXPORTS])
def export(request):
    return gedcom.parse_file(DATA_LAKE / request.param)


def test_the_only_parse_warnings_are_lines_that_never_claimed_to_be_gedcom(export):
    """Nothing structural is ever skipped.

    This read `warnings == []` until 2026-08-04, which held for the first ten
    exports and stopped holding at 45: one profile has an RTF blob pasted into a
    note, and RTF carries literal newlines, so the blob's continuation lines
    arrive as GEDCOM lines with no level number in front of them.

    Zero warnings is therefore not achievable and not the property worth
    asserting — Geni's data contains what its users pasted into it. The property
    that matters is that the parser only ever skips lines that were *not*
    GEDCOM: every warning must be an "unparseable" one whose text does not begin
    with a level number. A skipped line that did start with a level number would
    mean real structure was dropped, and that still fails here.
    """
    structural = [
        w
        for w in export.warnings
        if "unparseable" not in w or re.search(r": '(\d+) ", w)
    ]
    assert structural == [], f"parser skipped or mangled real GEDCOM structure: {structural[:3]}"


def test_export_has_a_geni_header(export):
    assert export.header is not None
    assert export.header.value_of("SOUR") == "Geni.com"


def test_every_individual_xref_encodes_its_geni_profile_id(export):
    # This is the assumption the entire merge rests on: the xref IS the ID, and
    # RFN says the same thing. If Geni ever changes that, fail here and loudly.
    individuals = export.by_tag("INDI")
    assert individuals

    for indi in individuals:
        assert indi.xref and indi.xref.startswith("@I") and indi.xref.endswith("@")
        geni_id = indi.xref[2:-1]
        assert geni_id.isdigit()
        assert indi.value_of("RFN") == f"geni:{geni_id}"


def test_record_xrefs_are_unique(export):
    xrefs = [r.xref for r in export.records if r.xref]
    assert len(xrefs) == len(set(xrefs))


def test_round_trip_of_the_real_file_is_a_fixpoint(export):
    reparsed = gedcom.parse(gedcom.serialize(export))

    assert reparsed.header == export.header
    assert reparsed.records == export.records


# The premise GENI_ID_RE is designed around, checked against what Geni actually
# sends rather than against what we assume it sends.
#
# `test_identity.py` covers the regex thoroughly, but only on hand-written
# fixtures. If a future export introduces a fifth prefix, that regex does not
# raise — it silently declines to find an ID, or worse finds the wrong one. That
# is not hypothetical: when it accepted any letters, the foreign xref
# `@NI04461@` parsed as Geni ID `04461`, a real and unrelated profile.
#
# This lived in CLAUDE.md as "re-measure when an export lands", which is a note
# asking someone to remember. A test does not forget.

XREF_PREFIXES = {"I": "INDI", "F": "FAM", "N": "NOTE", "S": "SUBM"}


def _prefix(xref: str) -> str:
    """The leading letters of an xref: `@I123@` -> `I`, `@NI04461@` -> `NI`."""
    inner = xref.strip("@")
    letters = ""
    for char in inner:
        if not char.isalpha():
            break
        letters += char
    return letters


def _prefixes_by_tag(records) -> dict[str, set[str]]:
    """Every xref prefix in `records`, mapped to the record tags carrying it."""
    seen: dict[str, set[str]] = {}
    for record in records:
        if record.xref:
            seen.setdefault(_prefix(record.xref), set()).add(record.tag)
    return seen


def _unknown(seen: dict[str, set[str]]) -> dict[str, list[str]]:
    return {p: sorted(tags) for p, tags in seen.items() if p not in XREF_PREFIXES}


def test_only_the_four_known_xref_prefixes_occur(export):
    unexpected = _unknown(_prefixes_by_tag(export.records))

    assert not unexpected, (
        f"Geni has started using xref prefixes this project does not know: "
        f"{unexpected}. GENI_ID_RE accepts only {sorted(XREF_PREFIXES)} and will "
        f"silently misread the rest — add the prefix to genimerge.identity and to "
        f"XREF_PREFIXES here, and check what it does to the Geni IDs parsed from it."
    )


def test_each_xref_prefix_stays_bound_to_one_record_type(export):
    seen = _prefixes_by_tag(export.records)

    for prefix, tags in sorted(seen.items()):
        assert tags == {XREF_PREFIXES[prefix]}, (
            f"xref prefix {prefix!r} appears on {sorted(tags)}, but this project "
            f"assumes it means {XREF_PREFIXES[prefix]} and nothing else."
        )


def test_every_known_prefix_is_actually_present(export):
    """A prefix that stopped appearing is also a format change worth noticing.

    Not every export needs every record type, so this asserts the weaker thing
    that matters: INDI and FAM are what a genealogy is made of, and an export
    without them is not one.
    """
    seen = {_prefix(r.xref) for r in export.records if r.xref}

    assert {"I", "F"} <= seen


def test_the_prefix_reader_distinguishes_the_xref_that_caused_the_bug():
    """`@NI04461@` is `NI`, not `N`. That difference is the whole guard.

    If `_prefix` stopped at one letter, the foreign xref would read as a NOTE,
    land in the known set, and these tests would pass while GENI_ID_RE went on
    parsing `04461` out of it — the exact failure they exist to catch.
    """
    assert _prefix("@NI04461@") == "NI"
    assert _prefix("@N1040@") == "N"
    assert _prefix("@I6000000087535357291@") == "I"


def test_the_guard_fires_on_a_document_carrying_a_foreign_xref():
    """Proof it is not vacuous: run the real check over a document that fails it.

    The exports in `data_lake/` all pass, so without this the guard could be
    broken in any number of ways and still look green.
    """
    doc = gedcom.parse(
        "0 HEAD\n"
        "0 @I123@ INDI\n"
        "1 NAME Fine /Person/\n"
        "0 @NI04461@ INDI\n"
        "1 NAME Foreign /Record/\n"
        "0 TRLR\n"
    )

    seen = _prefixes_by_tag(doc.records)

    assert _unknown(seen) == {"NI": ["INDI"]}
    assert "I" in seen and seen["I"] == {"INDI"}


def test_the_binding_check_fires_when_a_prefix_lands_on_two_record_types():
    doc = gedcom.parse(
        "0 HEAD\n"
        "0 @I123@ INDI\n"
        "1 NAME Fine /Person/\n"
        "0 @I456@ FAM\n"
        "0 TRLR\n"
    )

    seen = _prefixes_by_tag(doc.records)

    assert seen["I"] == {"INDI", "FAM"}
    assert seen["I"] != {XREF_PREFIXES["I"]}
