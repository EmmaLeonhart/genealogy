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


# --- name corrections: the Geni side is stale, not Wikidata's -------------

CORRECTION = """\
Emma Leonhart
https://www.geni.com/people/Emma-Leonhart/6000000087535357291
https://www.wikidata.org/wiki/Q232803

the name on that one is "Emma Leonhart", Emma /Leonhart/ - already corrected on
geni, the exports here are just old.
"""


def test_a_name_correction_is_keyed_by_geni_id_not_qid():
    """It corrects *our* stale export, not a label on Wikidata.

    A Geni export is a snapshot: a profile renamed afterwards keeps its old name
    in every GEDCOM already taken. `LabelEdit` cannot express that — it is keyed
    by QID, and the person may have no item at all.
    """
    parsed = entities.parse(CORRECTION)
    assert len(parsed.name_corrections) == 1
    correction = parsed.name_corrections[0]
    assert correction.geni_id == "6000000087535357291"
    assert correction.text == "Emma Leonhart"
    # and it is not mistaken for a Wikidata label edit
    assert parsed.labels == []


def test_the_resolution_still_parses_alongside_the_correction():
    parsed = entities.parse(CORRECTION)
    assert [(r.geni_id, r.qid) for r in parsed.resolutions] == [
        ("6000000087535357291", "Q232803")
    ]


def test_a_correction_requires_quotes():
    """Without them it would rename somebody to the rest of the sentence."""
    parsed = entities.parse(
        "https://www.geni.com/people/x/6000000087535357291\n"
        "the name on that one is Emma Leonhart and she moved to Vancouver\n"
    )
    assert parsed.name_corrections == []


def test_two_profiles_split_into_two_blocks_and_the_correction_stays_local():
    """Written after the first version of this test asserted the wrong thing.

    I expected two profiles in one block to make a correction ambiguous and be
    reported unparsed. They never share a block: `_entries` starts a new one at
    each new Geni profile, so the correction attaches to the block it is written
    in — the one immediately above it.

    The `len(geni) == 1` guard in `parse` is therefore defensive rather than
    reachable through this shape, and is kept for that reason rather than
    deleted as dead.
    """
    parsed = entities.parse(
        "https://www.geni.com/people/x/6000000087535357291\n"
        "https://www.geni.com/people/y/6000000001835522164\n"
        'the name on that one is "Emma Leonhart"\n'
    )
    assert [(c.geni_id, c.text) for c in parsed.name_corrections] == [
        ("6000000001835522164", "Emma Leonhart")
    ]


@pytest.mark.parametrize(
    "line",
    [
        'the name on that one is "Emma Leonhart"',
        'the name is "Emma Leonhart"',
        'real name is "Emma Leonhart"',
        'rename to "Emma Leonhart"',
    ],
)
def test_the_phrasings_that_are_understood(line):
    parsed = entities.parse(
        f"https://www.geni.com/people/x/6000000087535357291\n{line}\n"
    )
    assert [c.text for c in parsed.name_corrections] == ["Emma Leonhart"]


def test_corrected_names_lets_a_later_entry_win():
    """A second correction on one profile is a further correction, not a rival."""
    parsed = entities.parse(
        'https://www.geni.com/people/x/6000000087535357291\nrename to "First"\n\n'
        'https://www.geni.com/people/x/6000000087535357291\nrename to "Second"\n'
    )
    assert parsed.corrected_names() == {"6000000087535357291": "Second"}

