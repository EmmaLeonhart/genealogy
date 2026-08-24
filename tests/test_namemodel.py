"""`scripts/namemodel.py` — the module that decides what property a name becomes.

It is the difference between `P735` *given name*, `P734` *family name* and `P5056`
*patronym or matronym* on every person the Garborg programme creates, and it shipped
with no tests at all.

The rules under test are Emma's, from `name modelling.txt` and `CLAUDE.md`, not
inventions here:

* **A patronymic is its own property.** `P5056`, parallel to `P735` and `P734` — not
  a `P735` carrying a qualifier, which is what this file used to say before she
  corrected it.
* **A middle name is a given name after the first that is NOT a patronymic**, so the
  patronymic test runs before the position test.
* **The last token is the family name unless it is itself patronymic.** `Jon
  Samuelsen` has no family name, and turning `Samuelsen` into one would invent a
  surname for a man who had none — the ordinary Norwegian case one generation before
  farm names settled.
* **One name item per usage.** `Eivindsen` as a given name and `Eivindsen` as a
  patronymic are different items, so the lookup key is `(token, usage)`.
* **An ambiguous token is never emitted.** `Maria` resolves to nine Wikidata items;
  guessing one is how a tenth nearly got created.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from namemodel import (  # noqa: E402
    FAMILY_NAME, GIVEN_NAME, MIDDLE_NAME, PATRONYM, SERIES_ORDINAL,
    USUAL_FORENAME, classify, statements_for,
)


def usages(label):
    return [(token, usage) for token, usage, _ordinal in classify(label)]


# --- classification --------------------------------------------------------

def test_the_ordinary_norwegian_three_part_name():
    assert usages("Samuel Eivindsen Garborg") == [
        ("Samuel", "given"), ("Eivindsen", "patronymic"), ("Garborg", "family")]


def test_a_second_given_name_is_a_middle_name_not_a_patronymic():
    """Emma: a middle name is a given name after the first that is NOT patronymic."""
    got = classify("Ane Oline Jonsdatter Raugstad")
    assert got == [("Ane", "given", 1), ("Oline", "given", 2),
                   ("Jonsdatter", "patronymic", 0), ("Raugstad", "family", 0)]


def test_a_patronymic_last_token_is_not_a_family_name():
    """`Jon Samuelsen` had no surname. Making one up is inventing data."""
    assert usages("Jon Samuelsen") == [("Jon", "given"), ("Samuelsen", "patronymic")]
    assert not [t for t, u in usages("Jon Samuelsen") if u == "family"]


def test_daughter_and_son_are_one_category():
    """Emma, on the Norwegian material: *"The daughter and son would be the same
    thing"* — `-datter` and `-sen`/`-son` are both patronymics, not two kinds."""
    for token in ("Eivindsdatter", "Eivindsen", "Eivindson", "Kristoffersdatter"):
        assert usages(f"Ola {token} Garborg")[1] == (token, "patronymic")


def test_a_two_part_name_is_given_plus_family():
    assert usages("Hulda Garborg") == [("Hulda", "given"), ("Garborg", "family")]


def test_a_quoted_nickname_keeps_the_name_and_drops_the_quotes():
    """Geni writes `Stine "Stena" …`; `CLAUDE.md` records that Emma took the nickname."""
    assert [t for t, _u in usages('Stine "Stena" Eivindsdatter Garborg')] == [
        "Stine", "Stena", "Eivindsdatter", "Garborg"]


def test_a_parenthesised_nickname_is_treated_the_same():
    assert [t for t, _u in usages("Ingvold (Pinkie) Remmie")] == [
        "Ingvold", "Pinkie", "Remmie"]


def test_an_empty_name_yields_nothing_rather_than_raising():
    assert classify("") == []
    assert classify(None) == []


def test_a_single_token_is_a_given_name():
    """A mononym is a forename, not a surname.

    Written as a test first and it caught the module: `classify` took the last token
    as the family name unconditionally, so `Amaterasu` came out as `P734` *family
    name* with no `P735` at all — a personal name filed as a surname. A family name
    needs something in front of it to be the family name **of**.
    """
    assert usages("Amaterasu") == [("Amaterasu", "given")]


def test_a_single_patronymic_token_is_still_a_patronymic():
    assert usages("Eivindsen") == [("Eivindsen", "patronymic")]


# --- statements ------------------------------------------------------------

PLAN = {
    ("Samuel", "given"): ("Q629347", "link"),
    ("Eivindsen", "patronymic"): ("Q900001", "link"),
    ("Garborg", "family"): ("Q30250555", "link"),
    ("Oline", "given"): ("Q11993741", "link"),
    ("Marie", "given"): ("", "AMBIGUOUS - review, do not create"),
}


def test_the_first_given_name_is_marked_the_usual_forename():
    lines, _notes = statements_for("Samuel Eivindsen Garborg", PLAN, "1")
    given = [ln for ln in lines if ln[0] == GIVEN_NAME][0]
    assert given[1] == "Q629347"
    assert (SERIES_ORDINAL, "1") in given[2]
    assert (("P7452", USUAL_FORENAME)) in given[2]


def test_a_later_given_name_is_marked_a_middle_name():
    lines, _notes = statements_for("Samuel Oline Garborg", PLAN, "1")
    second = [ln for ln in lines if ln[0] == GIVEN_NAME][1]
    assert (SERIES_ORDINAL, "2") in second[2]
    assert ("P3831", MIDDLE_NAME) in second[2]


def test_the_patronym_is_its_own_property_not_a_qualified_given_name():
    """The correction Emma made to this file: `P5056`, parallel to `P735`."""
    lines, _notes = statements_for("Samuel Eivindsen Garborg", PLAN, "1")
    assert [ln[0] for ln in lines] == [GIVEN_NAME, PATRONYM, FAMILY_NAME]


def test_the_patronym_points_at_the_father_when_he_has_an_item():
    """`name modelling.txt`: `P144` *based on* names the PERSON, not a name item."""
    lines, _notes = statements_for("Samuel Eivindsen Garborg", PLAN, "1",
                                   father_qid="Q141152512")
    patronym = [ln for ln in lines if ln[0] == PATRONYM][0]
    assert ("P144", "Q141152512") in patronym[2]


def test_the_patronym_carries_no_p144_when_the_father_has_no_item():
    """Omitted rather than guessed — an unknown father is not a wrong father."""
    lines, _notes = statements_for("Samuel Eivindsen Garborg", PLAN, "1")
    patronym = [ln for ln in lines if ln[0] == PATRONYM][0]
    assert patronym[2] == []


def test_an_ambiguous_token_becomes_a_note_and_never_a_statement():
    """`Maria` resolves to nine items. Emitting one is how a tenth nearly appeared."""
    lines, notes = statements_for("Marie Garborg", PLAN, "1")
    assert [ln[0] for ln in lines] == [FAMILY_NAME]
    assert any("Marie" in n and "AMBIG" in n.upper() for n in notes)


def test_a_token_the_plan_has_never_seen_is_a_note_not_a_guess():
    lines, notes = statements_for("Zzzz Garborg", PLAN, "1")
    assert [ln[0] for ln in lines] == [FAMILY_NAME]
    assert any("Zzzz" in n for n in notes)


def test_the_same_spelling_in_two_usages_needs_two_items():
    """`CLAUDE.md` § One name item per USAGE — the lookup key is (token, usage).

    `Eivindsen` has a Wikidata item as a *given* name and needs a separate one as a
    *patronymic*. A lookup keyed on the token alone would link the wrong object.
    """
    plan = {("Eivindsen", "given"): ("Q111", "link"),
            ("Garborg", "family"): ("Q30250555", "link")}
    lines, notes = statements_for("Ola Eivindsen Garborg", plan, "1")
    assert not [ln for ln in lines if ln[1] == "Q111"], (
        "the given-name item must not be used for the patronymic")
    assert any("Eivindsen" in n for n in notes)
