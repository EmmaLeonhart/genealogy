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
