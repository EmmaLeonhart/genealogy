"""The rule-encoding functions in `scripts/` that produce the derived data.

Every CSV Emma is being asked to make decisions from is written by a script in
`scripts/`, and the test suite reaches `src/genimerge/` only. That gap produced a
real defect: `derive-labels.py` fell back to a mixed Latin+CJK string when a
person had no pure Latin name, so an "English label" could contain CJK
characters. It was caught by two reports disagreeing, not by the code.

These pin the rules that turn Emma's instructions into data — the ones where a
silent change alters what gets written rather than crashing.

Scripts have hyphens in their filenames and are not importable, so they are
loaded by path.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def labels():
    return _load("derive-labels")


@pytest.fixture(scope="module")
def family():
    return _load("derive-family")


@pytest.fixture(scope="module")
def facts():
    return _load("derive-facts")


@pytest.fixture(scope="module")
def display():
    return _load("build-display-names")


# --- a typographic sign is not a writing system ----------------------------
#
# The one that cost 646 people their label, all of them Iberian nobles whose
# title carries an ordinal.


@pytest.mark.parametrize("name", [
    "Afonso de Bragança 1º conde de Faro e 2º de Odemira",
    "Maria da Cunha 3ª senhora de Basto",
    "Mª Manuela Fernández de Córdoba",
    "João Soares de Sousa 3.º Capitão donatário da ilha de Santa Maria",
])
def test_an_ordinal_indicator_does_not_make_a_name_mixed_script(display, labels, name):
    """`'º'.isalpha()` is True, and its Unicode name starts `MASCULINE`.

    The classifier read the first word of every character's Unicode name, so `º`
    invented a script called `Masculine`; `derive-labels.script_group` then called
    the name mixed and refused it as an `en` or `mul` label. 646 people, and the
    only visible symptom was structural placeholders with no label at all.
    """
    assert display.scripts_of(name) == "Latin"
    assert labels.script_group(display.scripts_of(name)) == "Latin"


def test_a_sign_that_is_not_a_script_contributes_nothing(display):
    """Not "counts as Latin" — `º` says nothing about which script a name is in."""
    assert display.scripts_of("º") == ""
    assert display.scripts_of("ª 3.º") == ""


def test_an_unnamed_character_is_still_reported(display):
    """`Unnamed` stays out of `NOT_A_SCRIPT`: it is a finding, not a sign.

    12 NAME records carry a character with no Unicode name. Skipping those would
    hide them, which is the opposite of what the classifier's own docstring says
    it is for.
    """
    assert "Unnamed" not in display.NOT_A_SCRIPT
    # U+17000 is a Tangut ideograph: a letter to Python, and `unicodedata` has no
    # name for it. A private-use codepoint will not do here — those are not
    # `isalpha()`, so they never reach the name lookup at all.
    assert display.scripts_of("\U00017000") == "Unnamed"


def test_a_real_mixed_script_name_is_still_mixed(display, labels):
    """The fix must not swallow the case the bucket exists for."""
    assert display.scripts_of("陳母 Chan") == "Han+Latin"
    assert labels.script_group("Han+Latin") == "mixed"


# --- script grouping: by script, never by language -------------------------


def test_a_pure_latin_name_is_latin(labels):
    assert labels.script_group("Latin") == "Latin"


def test_han_and_the_kana_are_one_cjk_bucket(labels):
    """Telling Japanese from Chinese is a decision, not a codepoint test.

    Han characters are shared, so this deliberately does not split them — the
    bucket is what the cataloguing is for.
    """
    for scripts in ("Han", "Hiragana", "Katakana", "Hangul", "Han+Hiragana"):
        assert labels.script_group(scripts) == "CJK", scripts


def test_latin_beside_cjk_is_mixed_not_latin(labels):
    """The regression. A mixed string is not a usable English label.

    `derive-labels.py` originally fell back to `mixed` when a person had no pure
    Latin name, which admitted 4,990 people and produced `en` labels containing
    CJK characters. It gained 8 exact matches against Wikidata out of 4,990,
    which is what exposed it.
    """
    assert labels.script_group("Han+Latin") == "mixed"
    assert labels.script_group("Latin+Cyrillic") == "mixed"


def test_a_non_latin_non_cjk_script_is_other(labels):
    assert labels.script_group("Cyrillic") == "other"
    assert labels.script_group("Arabic") == "other"


def test_no_letters_at_all(labels):
    assert labels.script_group("") == "none"


# --- Emma's dot rule -------------------------------------------------------


@pytest.mark.parametrize("token", [".", "..", "?", "-", "_"])
def test_a_placeholder_token_is_dropped(labels, token):
    """*"If the surname is just a single dot … we just pretend it doesn't exist."*"""
    assert labels.clean(f"Danureja I {token}") == "Danureja I"


def test_clean_keeps_a_real_name_whole(labels):
    assert labels.clean("Arne Olson Anda") == "Arne Olson Anda"


def test_clean_normalises_whitespace(labels):
    assert labels.clean("  Arne   Anda ") == "Arne Anda"


# --- the married-name alias ------------------------------------------------


def test_the_married_name_takes_the_surnames_place(labels):
    """*"Married name plugs into name to produce an alias."*

    Read as substitution rather than appending. The reading is flagged as an
    interpretation in `reports/labels.md`; this pins which one the code does, so
    changing it is a visible decision rather than a silent one.
    """
    assert labels.alias_from_married_name("Judith", "Flandre", "") == "Judith Flandre"


def test_the_alias_keeps_a_suffix(labels):
    """A noble suffix stays in — Emma, 2026-08-11."""
    assert labels.alias_from_married_name("Aénor", "Flandre", "Duchess of Aquitaine") == (
        "Aénor Flandre Duchess of Aquitaine"
    )


def test_a_placeholder_married_name_yields_nothing_usable(labels):
    assert labels.alias_from_married_name("Danureja I", ".", "") == "Danureja I"


# --- the invented-parent label, which becomes a created item ---------------


def test_two_children_read_as_emma_specified(family):
    """She gave the format as "father of x and y"; that case is fixed."""
    assert family.parent_label("father", ["Mary Payne", "Lucy Payne"]) == (
        "father of Mary Payne and Lucy Payne"
    )


def test_three_children_stay_on_and(family):
    assert family.join_names(["A", "B", "C"]) == "A and B and C"


def test_four_or_more_take_commas_with_a_final_and(family):
    assert family.join_names(["A", "B", "C", "D"]) == "A, B, C and D"


def test_the_mother_label_uses_the_same_joining(family):
    assert family.parent_label("mother", ["A", "B"]) == "mother of A and B"


def test_no_children_produces_no_name_list(family):
    assert family.join_names([]) == ""


# --- the address string, which becomes a P6375 value -----------------------


def test_a_typical_block_composes_narrowest_first(facts):
    """`CITY Erie / STAE PA / CTRY United States` is the ordinary shape."""
    assert facts.compose_address(
        {"CITY": "Erie", "STAE": "PA", "CTRY": "United States"}
    ) == "Erie, PA, United States"


def test_a_street_line_leads(facts):
    assert facts.compose_address(
        {"ADR1": "12 Main St", "CITY": "Erie", "CTRY": "United States"}
    ) == "12 Main St, Erie, United States"


def test_missing_parts_do_not_leave_empty_commas(facts):
    """Two thirds of blocks have no CITY; a gap must not become `, ,`."""
    assert facts.compose_address(
        {"STAE": "Sogn og Fjordane", "CTRY": "Norway"}
    ) == "Sogn og Fjordane, Norway"


def test_the_post_code_sits_before_the_country(facts):
    assert facts.compose_address(
        {"CITY": "Los Angeles", "STAE": "CA", "POST": "90012", "CTRY": "United States"}
    ) == "Los Angeles, CA, 90012, United States"


def test_an_empty_block_composes_to_nothing(facts):
    assert facts.compose_address({}) == ""


def test_unknown_subtags_are_ignored(facts):
    """`EMAIL` and `PHON` occur under submitter addresses and are not places."""
    assert facts.compose_address(
        {"CITY": "Oslo", "EMAIL": "someone@example.com", "PHON": "555"}
    ) == "Oslo"
