"""Reading Emma's free-form `entity_resolution.md`.

The file is prose by design — she wrote "they're a bit unstructured" at the top
of it — so these tests are mostly about what the parser refuses to guess, and
about the entries that are *not* laid out the way the tidy ones are.
"""

from pathlib import Path

import pytest

from genimerge import entities

REPO = Path(__file__).resolve().parents[1]
REAL = REPO / "entity_resolution.md"

TIDY = """\
Some preamble prose with no links in it at all.

https://www.geni.com/people/%E7%A8%9A/6000000001835522164?through=6000000001829589817 https://www.wikidata.org/wiki/Q11596350
"""

# The shape that broke the first parser: item, profile and instruction split
# across three blank-line-separated blocks.
SPREAD = """\
Her
https://www.wikidata.org/wiki/Q12598947

https://www.geni.com/people/%E6%89%B6%E9%A4%98/6000000186285688286?through=6000000001829589817

add engligh label "Buyeo Taebi"
"""


def test_a_profile_and_an_item_on_one_line_is_a_resolution():
    parsed = entities.parse(TIDY)

    assert [(r.geni_id, r.qid) for r in parsed.resolutions] == [
        ("6000000001835522164", "Q11596350")
    ]
    assert parsed.unparsed == []


def test_prose_with_no_links_is_not_an_error():
    """The file opens with two paragraphs of explanation. Those are not entries."""
    parsed = entities.parse("Just some notes.\n\nAnd some more notes.\n")

    assert parsed.resolutions == []
    assert parsed.unparsed == []


def test_an_entry_split_across_blank_lines_is_still_one_entry():
    """Blank lines are not boundaries; a second profile or item is.

    This is the case that made blank-line splitting wrong. Parsed that way, the
    item and the profile land in different blocks and both are reported
    unparsable — a complete entry, refused.
    """
    parsed = entities.parse(SPREAD)

    assert [(r.geni_id, r.qid) for r in parsed.resolutions] == [
        ("6000000186285688286", "Q12598947")
    ]
    assert [(e.qid, e.language, e.text) for e in parsed.labels] == [
        ("Q12598947", "en", "Buyeo Taebi")
    ]
    assert parsed.unparsed == []


def test_a_misspelled_english_stays_anchored_to_en():
    """"engligh" is accepted; a different language is not.

    The tolerance exists because the real file contains the typo. It must not
    widen into "any word before 'label'", or a French label instruction would
    silently produce an English one.
    """
    ok = entities.parse('https://www.wikidata.org/wiki/Q1\nset engligh label "X"\n')
    assert [(e.language, e.text) for e in ok.labels] == [("en", "X")]

    other = entities.parse('https://www.wikidata.org/wiki/Q1\nset french label "X"\n')
    assert other.labels == []


def test_two_profiles_in_one_entry_are_reported_not_paired_by_order():
    """The refusal that matters. Pairing by order would look plausible and be a guess."""
    text = (
        "https://www.geni.com/people/a/6000000000000001 "
        "https://www.geni.com/people/b/6000000000000002 "
        "https://www.wikidata.org/wiki/Q1\n"
    )
    parsed = entities.parse(text)

    assert parsed.resolutions == []
    assert len(parsed.unparsed) == 1
    assert "would be a guess" in parsed.unparsed[0].reason


def test_a_label_edit_with_no_item_is_reported_rather_than_dropped():
    parsed = entities.parse('change her name to "Nobody"\n')

    assert parsed.labels == []
    assert parsed.resolutions == []
    # Nothing machine-readable at all, so it is not even an entry — the point is
    # only that it never becomes an edit.
    assert all("Nobody" not in e.text for e in parsed.labels)


def test_quickstatements_puts_a_geni_reference_on_claims_but_not_on_labels():
    """QuickStatements rejects a reference on a label, so one must not be emitted."""
    parsed = entities.parse(SPREAD)
    text = entities.render_quickstatements(parsed, retrieved="2026-08-04")
    claim, label = text.strip().splitlines()

    assert claim.startswith("Q12598947\tP2600\t")
    assert "S854" in claim and "S813" in claim
    assert label == 'Q12598947\tLen\t"Buyeo Taebi"'


def test_the_report_flags_a_profile_the_tree_does_not_hold():
    parsed = entities.parse(TIDY)
    md = entities.render_markdown(parsed, source="x.md", retrieved="2026-08-04", known=set())

    assert "not in our tree" in md
    assert "does not\nhold" in md or "does not hold" in md


@pytest.mark.skipif(not REAL.exists(), reason="no entity_resolution.md")
def test_the_real_file_parses_completely():
    """Every entry Emma has written is understood.

    If this fails she has written one in a shape the parser does not know, and
    the fix is to teach the parser — not to reformat her file, which would
    defeat the point of letting it be unstructured.
    """
    parsed = entities.read_file(REAL)

    assert parsed.unparsed == [], [u.reason for u in parsed.unparsed]
    assert len(parsed.resolutions) >= 6
    assert {e.language for e in parsed.labels} == {"en"}
    # Every resolution names a distinct item: two Geni profiles resolving to one
    # Wikidata item would be a duplicate-profile claim, not a resolution.
    qids = [r.qid for r in parsed.resolutions]
    assert len(qids) == len(set(qids))
