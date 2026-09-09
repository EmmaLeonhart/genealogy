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


@pytest.mark.parametrize("label", ["Toeloes .", "Siti Komara .", "Nechama (?) Heller"])
def test_punctuation_inside_a_label_is_left_alone(census, label):
    """Emma, 2026-08-17: *"Words yes, punctuation no."*

    Her ruling goes further than the hyphen fix and leaves the tail dot and the
    bracketed hole alone as well — 3,102 `?`-at-tail rows an earlier pass would have
    rewritten. Stripping typography is guessing at it.
    """
    assert census._classify(label) is None


@pytest.mark.parametrize("label", ["?", "???", "-", "."])
def test_punctuation_as_the_whole_label_still_means_absent(census, label):
    """`derive-labels.ABSENT` has always read a label of nothing but punctuation
    that way, and her ruling is about not stripping it from *inside* a name."""
    kind, _marker, vocab, position, _rest = census._classify(label)
    assert (kind, vocab, position) == ("marker", "punctuation", "whole")


@pytest.mark.parametrize("label,remainder", [
    ("Без име", ""),
    ("ukendt Hansen", "Hansen"),
    ("unknown Bloomfield", "Bloomfield"),
])
def test_a_word_meaning_unknown_is_a_marker_in_any_language(census, label, remainder):
    """`Без име` — Bulgarian for *without name*, 52 people — was found by ranking
    label strings by how many different people carry them, not by being remembered."""
    kind, _marker, vocab, _position, rest = census._classify(label)
    assert (kind, vocab, rest) == ("marker", "word", remainder)


def test_anon_is_a_norwegian_name_and_not_a_marker(census):
    """89 people. `Anon Olsen Syverstad` and `Anon Mathisen Lund` are Norwegians and
    `Anon` is their given name, not an abbreviation of *anonymous*."""
    assert "anon" in census.NOT_MARKERS
    assert census._classify("Anon Olsen Syverstad") is None


def test_the_child_character_is_not_a_marker(census):
    """`子` ends 2,091 ordinary Japanese given names — `多恵子`, `英子`."""
    assert "子" in census.NOT_MARKERS
    assert census._classify("多恵子 加納") is None


@pytest.mark.parametrize("label,position", [
    ("N Пузына", "head"),
    ("N Lozinska", "head"),
])
def test_a_bare_n_leading_a_surname_is_a_marker(census, label, position):
    kind, marker, _vocab, pos, _rest = census._classify(label)
    assert (kind, marker, pos) == ("marker", "n", position)


@pytest.mark.parametrize("label", ["Gunteroda N", "Laura N"])
def test_a_trailing_single_letter_is_a_middle_initial_not_a_marker(census, label):
    """205 of them, and `f9b9f86` records 283 middle initials this repo nearly
    invented once already. Decided rather than asked: `n` is neither a word nor
    punctuation, so Emma's ruling does not reach it."""
    assert census._classify(label) is None


# -- the CJK description class ----------------------------------------------
#
# Emma, 2026-08-17, shown the measurement: descriptions, the same as the English
# ones. About 5,400 people, more than the 1,222 English descriptions.


@pytest.mark.parametrize("label,suffix,remainder", [
    ("信秀正室 織田", "正室", "織田"),       # principal wife of Nobuhide, of the Oda
    ("謝氏", "氏", "謝"),                  # the Xie-clan woman
    ("織田敏信娘", "娘", "織田敏信"),        # daughter of Oda Toshinobu
    ("母 陳", "母", "陳"),                 # mother, of the Chen
])
def test_a_cjk_relationship_suffix_is_a_description(census, label, suffix, remainder):
    """The remainder keeps the real surname, which `CLAUDE.md` insists is not thrown
    away — `謝氏` leaves `謝`, so `mul` can be `NN 謝` rather than bare `NN`."""
    kind, found, vocab, _position, rest = census._classify(label)
    assert (kind, found, vocab, rest) == ("description", suffix, "cjk", remainder)


def test_every_cjk_suffix_comes_off_the_remainder_not_just_the_matched_one(census):
    """`古河某妻` is *wife of a certain Kogawa* and carries two suffixes. Stripping
    only the matched `某` left `古河妻`, which is neither a name nor a description."""
    assert census._classify("古河某妻")[4] == "古河"


def test_the_clan_suffix_keeps_her_own_surname(census):
    """`氏` attaches to **her** surname, the other suffixes to the relative.

    `盧氏 Chan` is what exposed this: dropping the whole `盧氏` token left `Chan` and
    threw away `盧`, the woman's actual clan. Getting it wrong is silent in both
    directions — one loses a real surname, the other adopts a stranger's — which is
    why `CLAN_SUFFIX` is a separate list rather than a flag.
    """
    assert census.CLAN_SUFFIX == ("氏",)
    assert census._classify("盧氏 Chan")[4] == "盧"
    assert census._classify("大唐帝國 謝氏")[4] == "謝"


@pytest.mark.parametrize("label,clan", [
    ("Li Shi 李氏", "李"),                                  # `Shi` IS 氏, romanised
    ("Fang Shi (concubine of Lü Daqi) 方氏", "方"),          # a bracketed description
    ("Xiao Shi of Yangdi) 蕭氏(炀帝后)", "蕭"),                # unbalanced paren debris
    ("17. Lady Shi 施氏", "施"),
])
def test_a_clan_label_keeps_only_the_clan(census, label, clan):
    """Everything else in a `氏` label is annotation, and the Wikidata side is what
    showed it.

    An earlier version of this test asserted `盧氏 Chan` → `盧 Chan`, on the reasoning
    that a stray token might be a real surname. Then 113 clan rows turned up carrying
    `Shi` — the romanisation of `氏` itself — and others carrying a bracketed
    description or broken parentheses, all of which would have gone into `mul` behind
    an `NN`. The clan character is the only part of these labels that is hers.
    """
    assert census._classify(label)[4] == clan


def test_a_relative_suffix_does_not_carry_the_relative_into_her_label(census):
    """`信秀正室 織田` is *principal wife of Nobuhide, of the Oda*. `信秀` is her
    husband's given name and must not end up in her `mul`; `織田` is the surname."""
    assert census._classify("信秀正室 織田")[4] == "織田"


def test_the_consort_ranks_are_not_folded_together(census):
    """`正室` principal wife, `側室` concubine, `室` consort are different statements
    about a person, so the census reports which one the source used."""
    assert census._classify("信秀正室 織田")[1] == "正室"
    assert census._classify("南殿(豊臣秀吉側室)")[1] == "側室"


def test_an_honorific_leading_a_label_is_a_description(census):
    """`Mrs. Isaak Guggenheim` is a woman named by her husband; 249 of them. And
    `Daughter Charif` carries no *of* for the relationship pair rule to find."""
    for label, remainder in (("Mrs. Isaak Guggenheim", "Isaak Guggenheim"),
                             ("Daughter Charif", "Charif")):
        kind, _head, vocab, _position, rest = census._classify(label)
        assert (kind, vocab, rest) == ("description", "honorific", remainder)


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


def test_cjk_descriptions_are_detected_since_emmas_ruling(census):
    """This test asserted the opposite until 2026-08-17, and the reason it flipped
    is a decision rather than a bug.

    The census shipped with CJK deliberately undetected, because reading a trailing
    `母` as a relationship marker is a claim about Chinese naming and not a lookup.
    Measuring the population — 室 2,565 · 氏 1,613 · 娘 617 · 某 311 · 妻 210 ·
    母 100 — and putting it to Emma got *"Descriptions, same as English"*. So the
    evidence the old test was waiting for arrived and she ruled on it.
    """
    kind, suffix, vocab, _position, rest = census._classify("陳母 Chan")
    assert (kind, suffix, vocab, rest) == ("description", "母", "cjk", "Chan")


# -- the two vocabularies, and that they stay distinguishable ----------------


def test_the_marker_classes_stay_distinguishable(census):
    """A row says which class matched, so her ruling stays legible in the output:
    `narrow` is `NN`/`Private`, `word` is the 18,280 `unknown` labels and their
    equivalents in eight other languages."""
    assert not (census.NARROW & census.WORDS_MEANING_UNKNOWN)
    assert not (census.NOT_MARKERS & census.WORDS_MEANING_UNKNOWN)
    assert census.VOCABULARY["nn"] == "narrow"
    assert census.VOCABULARY["unknown"] == "word"
    assert "子" not in census.CJK_RELATIONSHIP


# -- the normalisation, which is where a wrong class says a wrong thing ------


@pytest.fixture(scope="module")
def fixes():
    spec = importlib.util.spec_from_file_location(
        "marker_label_fixes", REPO / "scripts" / "build-marker-label-fixes.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _row(**kw):
    row = {"kind": "marker", "position": "whole", "marker": "nn",
           "vocabulary": "narrow", "remainder": "", "label": "", "qid": "",
           "geni_id": "1"}
    row.update(kw)
    return row


def test_a_repaired_name_never_becomes_nn(census, fixes):
    """`Catherine unknown` is a woman called Catherine, not an unnamed person.

    A marker at the tail or inside means the name is *there* with a hole punched in
    it. Classing these as unnamed would erase a given name sitting in the same
    string, and the edit would look entirely reasonable while doing it.
    """
    out = fixes.classify_row(
        _row(position="tail", marker="unknown", remainder="Catherine"),
        census.CLAN_SUFFIX)
    assert out == {"rule": "name repaired", "mul": "Catherine", "name": "Catherine"}


def test_a_leading_marker_keeps_the_surname_beside_nn(census, fixes):
    """`CLAUDE.md`: discarding these loses 3,605 real surnames."""
    out = fixes.classify_row(
        _row(position="head", marker="unknown", remainder="Bloomfield"),
        census.CLAN_SUFFIX)
    assert out["mul"] == "NN Bloomfield"
    assert out["name"] == ""


def test_the_clan_suffix_puts_her_surname_beside_nn(census, fixes):
    """`盧氏 Chan` → `NN 盧 Chan`. `氏` is her own clan, so it belongs in her label."""
    out = fixes.classify_row(
        _row(kind="description", position="tail", marker="氏",
             vocabulary="cjk", remainder="盧 Chan"),
        census.CLAN_SUFFIX)
    assert out == {"rule": "description+clan", "mul": "NN 盧 Chan", "name": ""}


@pytest.mark.parametrize("marker,remainder", [
    ("娘", "織田敏信"),          # her father
    ("正室", "織田"),
    ("wife", "William Lantham"),
    ("mrs.", "Isaak Guggenheim"),
])
def test_a_relative_form_never_puts_the_relative_in_her_label(census, fixes,
                                                              marker, remainder):
    """The remainder here is somebody else. `織田敏信娘` is *daughter of Oda
    Toshinobu* — putting `織田敏信` in her `mul` labels her with her father's name."""
    out = fixes.classify_row(
        _row(kind="description", position="tail", marker=marker,
             vocabulary="cjk", remainder=remainder),
        census.CLAN_SUFFIX)
    assert out["mul"] == "NN"
    assert out["name"] == ""


def test_an_unrecognised_description_form_does_not_guess(census, fixes):
    """A form this script has no rule for keeps the marker label bare rather than
    assuming whose name the remainder is."""
    out = fixes.classify_row(
        _row(kind="description", position="tail", marker="something-new",
             vocabulary="relationship", remainder="Somebody"),
        census.CLAN_SUFFIX)
    assert out["mul"] == "NN"


@pytest.mark.parametrize("remainder", ["Daughter (name Biard", "(Female)", "Kal ]"])
def test_a_repair_that_leaves_wreckage_falls_back_to_nn(census, fixes, remainder):
    """Taking a marker out of the *middle* of a label can leave a broken string, and
    the output looks like a name until you read it.

        Daughter (name unknown) Biard  ->  "Daughter (name Biard"   unbalanced
        (Female) Unknown               ->  "(Female)"               names nobody

    Both faults are objective — brackets balance or they do not — so the repair is
    refused and the person gets `NN`. The rule keeps its own name, `repair rejected`,
    so the population stays countable rather than merging into the genuinely unnamed.
    """
    assert not fixes.is_a_plausible_name(remainder)
    out = fixes.classify_row(
        _row(position="inside", marker="unknown", remainder=remainder),
        census.CLAN_SUFFIX)
    assert out == {"rule": "repair rejected", "mul": "NN", "name": ""}


def test_a_repair_keeping_balanced_brackets_is_allowed(census, fixes):
    """`Asbjoern (Asbjørn) Inconnu` → `Asbjoern (Asbjørn)`: the bracket is a spelling
    variant the record itself carries, and it balances."""
    assert fixes.is_a_plausible_name("Asbjoern (Asbjørn)")
    out = fixes.classify_row(
        _row(position="tail", marker="inconnu", remainder="Asbjoern (Asbjørn)"),
        census.CLAN_SUFFIX)
    assert out["rule"] == "name repaired"


@pytest.mark.parametrize("text,cleaned", [
    ("Guttormsdatter Ålesdatter?)", "Guttormsdatter Ålesdatter?"),
    ("Given Name) Unknown", "Given Name Unknown"),
    ("Heiress) of Bactria", "Heiress of Bactria"),
    ("de Villela y Ajanguiz (heredera de la", "de Villela y Ajanguiz heredera de la"),
    ("河東柳)", "河東柳"),
])
def test_unpartnered_brackets_are_dropped(fixes, text, cleaned):
    """Two causes, same wreckage. The source label was already broken — Geni carries
    `NN Guttormsdatter Ålesdatter?)` and Wikidata `NN Wife of Quintus Pedius
    Publicola)` — or removing the marker broke it: `(Unknown Given Name) Unknown`
    loses `(unknown` and leaves `Given Name)`.

    Dropping an unpartnered bracket is not a guess; the character was noise before
    this script touched it. Balanced brackets are left alone.
    """
    assert fixes.drop_bracket_debris(text) == cleaned


def test_balanced_brackets_survive_the_clean(fixes):
    assert fixes.drop_bracket_debris("Asbjoern (Asbjørn)") == "Asbjoern (Asbjørn)"


def test_the_guard_covers_every_rule_that_writes_a_remainder(census, fixes):
    """The first version guarded the repair branch alone, and 28 labels still
    shipped with unbalanced brackets through `marker+surname` and
    `description+clan` — the same defect arriving by a different door."""
    head = fixes.classify_row(
        _row(position="head", marker="nn", remainder="Guttormsdatter Ålesdatter?)"),
        census.CLAN_SUFFIX)
    assert head["mul"] == "NN Guttormsdatter Ålesdatter?"

    clan = fixes.classify_row(
        _row(kind="description", position="tail", marker="氏",
             vocabulary="cjk", remainder="河東柳)"),
        census.CLAN_SUFFIX)
    assert clan["mul"] == "NN 河東柳"
