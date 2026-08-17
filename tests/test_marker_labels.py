"""What counts as a placeholder marker inside a label, and what does not.

`scripts/build-marker-label-census.py` decides which of 62,000 Geni labels and
31,000 Wikidata labels carry a marker rather than a name, and its output is what
Emma's *"normalizes them into proper things based on our rules"* item runs on. The
cost of getting it wrong is asymmetric: a missed marker leaves a bad label alone,
while a false positive **strips a real one** — so the guards are pinned here rather
than left to a rerun to notice.

Loaded by path; the script's name has hyphens in it and is not importable.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def census():
    spec = importlib.util.spec_from_file_location(
        "marker_label_census", REPO / "scripts" / "build-marker-label-census.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# -- the false positive that would have stripped real labels ----------------


@pytest.mark.parametrize("label", [
    "George Clark, II - farmer",
    "Birch, Charles Weldon (1821 - 1894), Naturalist",
])
def test_a_hyphen_inside_prose_is_not_a_marker(census, label):
    """289 rows over 112 Wikidata items, and stripping the hyphen mangles all of them.

    The first pass of the census treated bare punctuation as a marker wherever it
    sat. These are hyphenated prose, not people with a missing name.
    """
    assert census._classify(label) is None


@pytest.mark.parametrize("label,remainder", [
    ("Toeloes .", "Toeloes"),
    ("Siti Komara .", "Siti Komara"),
])
def test_punctuation_where_a_name_would_end_is_a_marker(census, label, remainder):
    """An Indonesian name with no surname, the dot standing in for one."""
    kind, _marker, _vocab, position, rest = census._classify(label)
    assert (kind, position, rest) == ("marker", "tail", remainder)


@pytest.mark.parametrize("label,remainder", [
    ("Nechama (?) Heller", "Nechama Heller"),
    ("Theodechildis (Unknown)", "Theodechildis"),
])
def test_a_parenthesised_stand_in_counts_wherever_it_sits(census, label, remainder):
    """Brackets are the difference between a stand-in and prose, and they are in
    the data rather than inferred — which is why the positional rule has this
    exception instead of a shorter punctuation list."""
    kind, _marker, _vocab, _position, rest = census._classify(label)
    assert (kind, rest) == ("marker", remainder)


# -- the three shapes, kept apart -------------------------------------------


def test_the_label_that_is_only_a_marker(census):
    assert census._classify("NN")[3] == "whole"
    assert census._classify("Private")[3] == "whole"


def test_a_marker_leading_a_real_surname_keeps_the_surname(census):
    """`CLAUDE.md`: throwing the surname away loses 3,605 of them."""
    for label, surname in (("NN Hildesheim", "Hildesheim"),
                           ("unknown Bloomfield", "Bloomfield"),
                           ("N.N. Andersdatter Skeel", "Andersdatter Skeel")):
        kind, _marker, _vocab, position, rest = census._classify(label)
        assert (kind, position, rest) == ("marker", "head", surname)


def test_a_marker_wins_over_a_description_in_the_same_label(census):
    """`NN wife of Aun` is reported as its marker, with the description as the
    remainder — so one row shows both rather than the two classes merging."""
    kind, marker, _vocab, _position, rest = census._classify("NN wife of Aun")
    assert (kind, marker, rest) == ("marker", "nn", "wife of Aun")


# -- descriptions, from the repo's own tables --------------------------------


def test_the_relationship_vocabulary_is_not_hand_written(census):
    """It is read out of `build-nn-label-batch.py`'s ten-language `WORDS` table.

    A label that reads like a phrase this project *generates* is a description by
    construction. Writing the list from memory is how a vocabulary becomes a guess.
    """
    assert len(census.RELATIONSHIP_PHRASES) > 100
    assert ("wife", "of") in census.RELATIONSHIP_PHRASES
    assert ("maka", "till") in census.RELATIONSHIP_PHRASES  # Swedish
    assert ("hija", "de") in census.RELATIONSHIP_PHRASES    # Spanish


@pytest.mark.parametrize("label,remainder", [
    ("Wife of Moshe Lazers", "Moshe Lazers"),
    ("Maka till Brynjolf Brandsson", "Brynjolf Brandsson"),
    ("hija de Pedro", "Pedro"),
])
def test_a_relationship_phrase_is_a_description(census, label, remainder):
    kind, _phrase, vocab, _position, rest = census._classify(label)
    assert (kind, vocab, rest) == ("description", "relationship", remainder)


def test_a_name_that_merely_contains_the_of_word_is_left_alone(census):
    """The pair must be adjacent, or every Iberian name becomes a description."""
    assert census._classify("Rodrigo de Vivar") is None
    assert census._classify("Afonso de Bragança 1º conde de Faro") is None


def test_cjk_descriptions_are_deliberately_not_detected(census):
    """`陳母` is *Chen's mother* and there is no table for it.

    Reading a trailing `母` as a relationship marker is a decision about Chinese
    naming rather than a lookup, so the census reports these as ordinary labels and
    the evidence for the decision comes out of the `remainder` column.
    """
    assert census._classify("陳母 Chan") is None


# -- the two vocabularies, and that they stay distinguishable ----------------


def test_the_narrow_and_wide_vocabularies_do_not_overlap(census):
    """`scripts/labels.py` is narrow on purpose — Emma refused `unknown` and `?`
    when they were added unasked. The census reports which set matched instead of
    merging them, because whether `wide` stands is her decision and it covers
    18,280 `unknown` labels on the Wikidata side."""
    assert not (census.NARROW & census.WIDE)
    assert census.VOCABULARY["nn"] == "narrow"
    assert census.VOCABULARY["unknown"] == "wide"
