"""Tests for `genimerge.identity` — the module the whole merge rests on.

It had none. `IdentityMismatch`, the exception that stops a record whose xref
and `RFN` disagree from being treated as one person, had never been raised
anywhere in the suite: its only mention was a comment claiming it would, on data
where it never does. A guard nobody has seen fire is a guard nobody has checked.
"""

import pytest

from genimerge import gedcom
from genimerge.identity import (
    IdentityMismatch,
    geni_id_from_pointer,
    geni_id_from_xref,
    geni_id_of,
    profile_url,
    xref_for,
)


def record(text: str):
    return gedcom.parse(text + "0 TRLR\n").records[0]


# -- reading an ID out of an xref --------------------------------------


@pytest.mark.parametrize(
    "xref,expected",
    [
        ("@I6000000001846508982@", "6000000001846508982"),
        ("@F4056@", "4056"),
        ("@S123@", "123"),
        ("@N9@", "9"),
        ("@NI04461@", None),  # letters after the type prefix: not a Geni ID
        ("@I@", None),
        ("I123", None),
        ("", None),
        (None, None),
    ],
)
def test_an_id_is_read_from_the_xref_or_not_at_all(xref, expected):
    assert geni_id_from_xref(xref) == expected


def test_a_pointer_yields_the_id_it_points_at():
    node = record("0 @I1@ INDI\n1 FAMC @F900@\n").get("FAMC")

    assert geni_id_from_pointer(node) == "900"


def test_a_non_pointer_value_yields_nothing():
    node = record("0 @I1@ INDI\n1 RFN geni:1\n").get("RFN")

    assert geni_id_from_pointer(node) is None
    assert geni_id_from_pointer(None) is None


# -- the cross-check ---------------------------------------------------


def test_an_agreeing_xref_and_rfn_give_the_id():
    assert geni_id_of(record("0 @I123@ INDI\n1 RFN geni:123\n")) == "123"


def test_a_disagreeing_xref_and_rfn_raise(capsys):
    # THE test this file exists for. Resolving this silently -- picking either
    # side -- would merge two different people under one key.
    with pytest.raises(IdentityMismatch) as raised:
        geni_id_of(record("0 @I123@ INDI\n1 RFN geni:456\n"))

    message = str(raised.value)
    assert "123" in message and "456" in message


def test_the_mismatch_can_be_waived_explicitly():
    # strict=False is for callers that only want the xref and know what they
    # are doing; the default is to raise.
    node = record("0 @I123@ INDI\n1 RFN geni:456\n")

    assert geni_id_of(node, strict=False) == "123"


def test_a_record_with_no_rfn_is_fine():
    # Only INDI records carry an RFN, so this is the normal case for FAM,
    # SUBM and NOTE.
    assert geni_id_of(record("0 @F900@ FAM\n1 CHIL @I1@\n")) == "900"


def test_an_rfn_that_is_not_a_geni_reference_is_ignored():
    assert geni_id_of(record("0 @I123@ INDI\n1 RFN something-else\n")) == "123"


def test_the_rfn_is_the_fallback_when_the_xref_carries_no_id():
    assert geni_id_of(record("0 @NI04461@ INDI\n1 RFN geni:789\n")) == "789"


def test_a_record_with_neither_a_usable_xref_nor_an_rfn_yields_nothing():
    assert geni_id_of(record("0 @NI04461@ INDI\n1 SEX M\n")) is None


def test_surrounding_whitespace_in_the_rfn_does_not_cause_a_false_mismatch():
    assert geni_id_of(record("0 @I123@ INDI\n1 RFN geni:123 \n")) == "123"


# -- building identifiers back -----------------------------------------


def test_an_xref_round_trips():
    assert xref_for("I", "123") == "@I123@"
    assert geni_id_from_xref(xref_for("I", "6000000001846508982")) == "6000000001846508982"


def test_the_profile_url_names_the_profile():
    url = profile_url("6000000001846508982")

    assert url.startswith("https://www.geni.com/")
    assert url.endswith("/6000000001846508982")


# -- what the merge actually keys on -----------------------------------


def test_the_merge_keys_on_the_xref_and_does_not_run_the_cross_check():
    """A deliberate decision, asserted here so it stays one.

    `Merger.add_source` keys records on `record.xref` directly. It never calls
    `geni_id_of`, so a record whose `RFN` contradicted its xref would merge on
    the xref without complaint rather than raising. That is the right call --
    the xref is the identifier and a merge that refused to run over one odd
    record would be useless -- but it means the cross-check is *not* a merge-time
    guard. It runs in `inventory`, in `model`, and over the merged output in
    `test_merge_real_exports.py`, which is where a real mismatch would surface.
    """
    from collections import Counter

    from genimerge import merge

    contradictory = "0 @I123@ INDI\n1 NAME A /B/\n1 RFN geni:456\n0 TRLR\n"
    doc = gedcom.parse(contradictory)
    worst: Counter = Counter()
    for rec in doc.records:
        merge._walk_multiplicity(rec, "", worst)

    merger = merge.Merger(merge.collapse_single_valued(worst))
    merger.add_source("odd.ged", doc.records)  # does not raise
    result = merger.result()

    assert [r.xref for r in result.records] == ["@I123@"]
    # And the cross-check, run separately over that same record, does object.
    with pytest.raises(IdentityMismatch):
        geni_id_of(result.records[0])
