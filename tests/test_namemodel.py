"""`scripts/namemodel.py` — the module that decides what property a name becomes.

It is the difference between `P735` *given name*, `P734` *family name* and `P5056`
*patronym or matronym* on every person the Garborg programme creates, and it shipped
with no tests at all.

The rules under test come from `name modelling.txt` and `CLAUDE.md`, not from
inventions here:

* **A patronymic is its own property.** `P5056`, parallel to `P735` and `P734` — not
  a `P735` carrying a qualifier, which is what this file used to say before it was
  corrected.
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

import namemodel  # noqa: E402
from namemodel import (  # noqa: E402
    FAMILY_NAME, GIVEN_NAME, MIDDLE_NAME, PATRONYM, PATRONYMIC, SERIES_ORDINAL,
    USUAL_FORENAME, classify, load_plan, statements_for,
)


def usages(label):
    return [(token, usage) for token, usage, _ordinal in classify(label)]


# --- classification --------------------------------------------------------

def test_the_ordinary_norwegian_three_part_name():
    assert usages("Samuel Eivindsen Garborg") == [
        ("Samuel", "given"), ("Eivindsen", "patronymic"), ("Garborg", "family")]


def test_a_second_given_name_is_a_middle_name_not_a_patronymic():
    """A middle name is a given name after the first that is NOT patronymic."""
    got = classify("Ane Oline Jonsdatter Raugstad")
    assert got == [("Ane", "given", 1), ("Oline", "given", 2),
                   ("Jonsdatter", "patronymic", 0), ("Raugstad", "family", 0)]


def test_a_patronymic_last_token_is_not_a_family_name():
    """`Jon Samuelsen` had no surname. Making one up is inventing data."""
    assert usages("Jon Samuelsen") == [("Jon", "given"), ("Samuelsen", "patronymic")]
    assert not [t for t, u in usages("Jon Samuelsen") if u == "family"]


def test_daughter_and_son_are_one_category():
    """On the Norwegian material the daughter and son forms are the same thing —
    `-datter` and `-sen`/`-son` are both patronymics, not two kinds."""
    for token in ("Eivindsdatter", "Eivindsen", "Eivindson", "Kristoffersdatter"):
        assert usages(f"Ola {token} Garborg")[1] == (token, "patronymic")


def test_a_two_part_name_is_given_plus_family():
    assert usages("Hulda Garborg") == [("Hulda", "given"), ("Garborg", "family")]


def test_a_quoted_nickname_keeps_the_name_and_drops_the_quotes():
    """Geni writes `Stine "Stena" …`; `CLAUDE.md` records that the nickname was taken."""
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


def test_usual_forename_is_never_emitted():
    """⛔ Ruled 2026-09-14: *"Please stop adding this to the first name in the given names. I
    do not think it is actually accurate most of the time ... just drop this item of the
    pipeline."*

    **Dropped entirely, and nothing already on Wikidata is corrected** — the instruction covers
    all three: stop emitting, leave what is there, and do not measure the population affected.

    This test has now asserted three different things, which is the history worth keeping. It
    first required a lone given name to carry `P7452`; that was the generator's bug written
    down as intent. On 2026-08-24 it was narrowed to *only where there is a middle name*, which
    was right as far as it went — a lone given name contrasts with nothing. The narrowing was
    still insufficient: having two given names does not tell you which one the person actually
    went by either, and asserting it from POSITION is § *Never parse a name positionally*
    wearing a qualifier.

    `USUAL_FORENAME` stays defined. `build-regnal-ordinals.py` uses the same pair for a
    different and still-valid purpose.
    """
    # One given name: NO ordinal and no usual-forename qualifier.
    #
    # **The ordinal half of this changed on 2026-08-25**, and the test previously required
    # the opposite. Reported as one reason the generated batches were being run only in part:
    # they consistently included unwanted things, a series ordinal of 1 on a person with only
    # one given name among them. `P1545` *series ordinal*
    # orders a person's several given names against each other; with one there is nothing to
    # order, and the qualifier asserts a sequence that does not exist. Same objection as the
    # usual-forename one directly below it.
    lines, _notes = statements_for("Samuel Eivindsen Garborg", PLAN, "1")
    given = [ln for ln in lines if ln[0] == GIVEN_NAME][0]
    assert given[1] == "Q629347"
    assert not any(q[0] == SERIES_ORDINAL for q in given[2]), (
        "a lone given name has nothing to be ordinal 1 OF")
    assert ("P7452", USUAL_FORENAME) not in given[2], (
        "a lone given name is not a *usual* forename — there is nothing to contrast it "
        "with")

    # Two given names: STILL not emitted. This is the assertion that flipped on 2026-09-14.
    lines, _notes = statements_for("Samuel Oline Garborg", PLAN, "1")
    first = [ln for ln in lines if ln[0] == GIVEN_NAME][0]
    assert ("P7452", USUAL_FORENAME) not in first[2], (
        "usual forename is dropped from the pipeline, middle name or not")
    # and the middle-name role is untouched by the drop
    second = [ln for ln in lines if ln[0] == GIVEN_NAME][1]
    assert ("P3831", MIDDLE_NAME) in second[2]


def test_a_later_given_name_is_marked_a_middle_name():
    lines, _notes = statements_for("Samuel Oline Garborg", PLAN, "1")
    second = [ln for ln in lines if ln[0] == GIVEN_NAME][1]
    assert (SERIES_ORDINAL, "2") in second[2]
    assert ("P3831", MIDDLE_NAME) in second[2]


def test_the_patronym_is_its_own_property_not_a_qualified_given_name():
    """The correction made to this file: `P5056`, parallel to `P735`."""
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


# --- the FIELDS, which is where name objects actually come from ---------------

from namemodel import (  # noqa: E402
    BIRTH_NAME_ROLE, MARRIED_NAME_ROLE, NICKNAME, aliases_for, classify_fields,
)


def usages_of(**fields):
    return [(t, u) for t, u, _o in classify_fields(**fields)]


def test_the_surname_is_read_not_inferred():
    """`SURN` is recorded data. The old parser took the last whitespace token instead.

    Caught 2026-08-24: name objects are resolved from the fields, not by choosing which
    name field to use as a source of the label. Agreeing by luck
    with a positional guess is not the same as reading the field.
    """
    got = usages_of(givn="Eivind Aadnesson", surn="Garborg")
    assert ("Garborg", "family") in got
    assert ("Aadnesson", "patronymic") in got
    assert ("Eivind", "given") in got


def test_a_patronym_in_the_SURN_field_is_still_a_patronym():
    """`name modelling.txt`: check the given names AND the surname for a patronym.

    A positional parser cannot do this — it only ever asks whether the *last* token
    looks patronymic. Here the field is read and the same test applied to it.
    """
    assert ("Samuelsen", "patronymic") in usages_of(givn="Jon", surn="Samuelsen")
    assert not [t for t, u in usages_of(givn="Jon", surn="Samuelsen") if u == "family"]


def test_a_quoted_token_inside_givn_is_a_nickname_not_a_middle_name():
    """Ruled 2026-08-24: it becomes `P1449` *nickname*.

    The old parser made `Stena` a second given name carrying `P1545` *series ordinal*
    2 and `P3831` → `Q245025` *middle name*. She is not called Stena as a middle
    name; it is what Stine was called.
    """
    got = classify_fields(givn='Stine "Stena" Eivindsdatter', surn="Garborg")
    assert ("Stena", "nickname", 0) in got
    assert ("Stine", "given", 1) in got
    assert not [t for t, u, _o in got if u == "given" and t == "Stena"]


def test_the_nickname_does_not_consume_an_ordinal():
    """Stripping it must not leave a hole in the numbering of the real given names."""
    got = classify_fields(givn='Inger Marie "Mary" Eivindsdatter', surn="Garborg")
    givens = [(t, o) for t, u, o in got if u == "given"]
    assert givens == [("Inger", 1), ("Marie", 2)], givens


def test_the_married_name_is_a_second_family_name_only_when_it_differs():
    """Ruled 2026-08-24, and sex is explicitly NOT a screen."""
    differs = usages_of(givn="Stine", surn="Garborg", marnm="Jacobson")
    assert ("Jacobson", "married") in differs
    assert ("Garborg", "family") in differs

    same = usages_of(givn="Eivind", surn="Garborg", marnm="Garborg")
    assert not [t for t, u in same if u == "married"], (
        "_MARNM equal to SURN is the 43% case CLAUDE.md measured — not a second name")


def test_a_married_man_gets_the_married_name_too():
    """The ruling was explicit: only when different; sex does not matter.

    The corpus measurement suggested screening on sex, because 25% of the differing
    `_MARNM` values are male. That was overridden, and the data model is the one
    specified.
    """
    assert ("Nyvold", "married") in usages_of(
        givn="Hans", surn="Garborg", marnm="Nyvold")


def test_the_two_family_names_carry_roles_that_say_which_is_which():
    plan = {("Garborg", "family"): ("Q30250555", "link"),
            ("Jacobson", "family"): ("Q900002", "link"),
            ("Stine", "given"): ("Q900003", "link")}
    # `sex="F"` because the married-name ROLE is only correct on a woman -- see
    # `test_a_mans_marnm_family_name_carries_no_married_role`.
    lines, _notes = statements_for("", plan, "1",
                                   fields={"givn": "Stine", "surn": "Garborg",
                                           "marnm": "Jacobson"}, sex="F")
    families = {value: dict(quals) for prop, value, quals in lines
                if prop == FAMILY_NAME}
    assert families["Q30250555"][("P3831")] == BIRTH_NAME_ROLE
    assert families["Q900002"][("P3831")] == MARRIED_NAME_ROLE


def test_a_lone_surname_carries_no_role_qualifier():
    """None of the eleven hand-made items qualifies a family name, so a bare one stays bare."""
    plan = {("Garborg", "family"): ("Q30250555", "link")}
    lines, _notes = statements_for("", plan, "1",
                                   fields={"givn": "Eivind", "surn": "Garborg"})
    assert [q for p, v, q in lines if p == FAMILY_NAME] == [[]]


def test_a_nickname_produces_an_alias_and_no_statement():
    """Ruled 2026-08-29: drop the nickname functionality; `Lmul` against `Amul` instead.

    This asserted `(NICKNAME, "Stena", [])` in `lines` until 2026-08-30. The property is
    monolingual text and the tag being emitted was `en`, declaring Norwegian words to be
    English; there is no right tag either, since the nickname sits on a person whose label is
    language-neutral `mul` and guessing a language per person is the inference this repo refuses.

    **The drop belongs in the model, which is what this pins.** It lived in
    `build-garborg-day.py` for a day, so the model went on producing `P1449` while nothing could
    emit it, and `model-vs-reality.py` reported 66 people as missing a nickname no batch would
    ever add. A phantom gap reads as work.

    The classification is untouched: the token is still recognised as a nickname, still kept out
    of the given names, and still reaches Wikidata as an alias.
    """
    lines, _notes = statements_for("", {}, "1",
                                   fields={"givn": 'Stine "Stena"', "surn": "Garborg"})
    assert not [ln for ln in lines if ln[0] == NICKNAME]
    # Still not a given name, and still not part of the label.
    assert "Stena" not in [v for p, v, _q in lines if p == GIVEN_NAME]


def test_aliases_cover_the_nickname_and_the_married_full_name():
    """The nickname alias carries the SURNAME. Ruled 2026-08-26.

    It used to assert the bare `"Stena"`, and that was overruled on seeing `Q141189102`
    *Sigrid "Sally" Manilva Tunheim* get an alias of `Sally` where it should have been
    `Sally Ekman`. A bare given-name token is not something
    anybody can look a person up by, and `Help:Aliases` says the purpose of an alias is
    only to find the entity in searches — so a form nobody would search is no alias at all.

    The surname used is the **married** one, because § *The MARRIED name is the real name*
    makes that the form the primary label takes; the alias is then the same person's name
    with the nickname swapped in rather than a different person's.

    `P1449` *nickname* still carries the bare token, and must: `Stena` IS the nickname.
    That is asserted in `test_a_quoted_given_token_is_a_nickname`.
    """
    got = aliases_for({"givn": 'Stine "Stena" Eivindsdatter', "surn": "Garborg",
                       "marnm": "Jacobson"})
    assert "Stena Jacobson" in got, f"nickname alias lost its surname: {got}"
    assert "Stine Jacobson" in got
    assert "Stena" not in got, f"the bare nickname is not an alias: {got}"


def test_the_nick_field_never_takes_the_surname():
    """Reported 2026-09-04 on `Carolina Gustafsdotter Wittfooth`: her surname was repeated
    twice in a `mul` alias — the created item carried
    `Amul "Wittfoth Wittfooth"`.

    Her record is `NICK Karolina`, `NICK Wittfoth`, `SURN Wittfooth`, `_MARNM Wittfooth`.
    The `NICK` field holds an alternate SPELLING of the surname, so appending the surname
    spells it twice — and the old `endswith` guard could not see it, because `Wittfoth`
    does not end with `Wittfooth`.

    The two sources of the usage `nickname` are different things and this pins both:
    Geni's `NICK` field is an *also known as*, already a name, emitted as it stands; a
    QUOTED token inside `GIVN` is a byname that is not findable bare, and still gains the
    surname. The test above is the second half and the `Sally` case is that shape
    — `Q141189102`'s `nick` column is empty.
    """
    got = aliases_for({"givn": "Carolina Gustafsdotter", "surn": "Wittfooth",
                       "nick": "Wittfoth", "marnm": "Wittfooth"})
    assert "Wittfoth" in got, f"the also-known-as was lost: {got}"
    assert "Wittfoth Wittfooth" not in got, f"the surname is spelled twice: {got}"

    # The variant spelling is not the only shape: `Eccleston` against `Eggleston`,
    # `Monradi` against `Monrad`, `Slason` against `Slawson`. A similarity threshold is
    # the other way to reach these and this repo does not have one.
    got = aliases_for({"givn": "Ichabod", "surn": "Eggleston",
                       "nick": "Eccleston", "marnm": "Eggleston"})
    assert got == ["Eccleston"], got

    # And the ordinary case, which is most of the 152,447 records carrying a `NICK`:
    # the field holds a whole alternate name that reads correctly on its own.
    got = aliases_for({"givn": "Sarah", "surn": "Miller",
                       "nick": "Sally Miller", "marnm": "Gross"})
    assert "Sally Miller" in got, got
    assert "Sally Miller Gross" not in got, got


def test_a_mans_marnm_family_name_carries_no_married_role():
    """Ruled 2026-08-24, on seeing a man with `Q28418670` *married name*.

    *"ontologically married name on a man means more like adopted surname. So men's
    'married names' should not have the role of married name."*

    He still gets the second `P734` — he bore the name — it just carries no `P3831`
    role. And **not** `Q118383793` *adoptive name* either: in this material the second
    surname is usually a farm name taken by residence. `Q141169072` is the case, *Ådne
    Olsen Grøtheim* becoming *Ådne Olsen Garborg* by moving to the Garborg farm.
    """
    plan = {("Grøtheim", "family"): ("Q900010", "link"),
            ("Garborg", "family"): ("Q30250555", "link"),
            ("Ådne", "given"): ("Q900011", "link")}
    fields = {"givn": "Ådne", "surn": "Grøtheim", "marnm": "Garborg"}

    lines, _n = statements_for("", plan, "1", fields=fields, sex="M")
    married = [ln for ln in lines if ln[0] == FAMILY_NAME and ln[1] == "Q30250555"]
    assert married, "a man still gets the second family name"
    assert married[0][2] == [], f"a man must carry no role, got {married[0][2]}"

    lines, _n = statements_for("", plan, "1", fields=fields, sex="F")
    married = [ln for ln in lines if ln[0] == FAMILY_NAME and ln[1] == "Q30250555"]
    assert ("P3831", MARRIED_NAME_ROLE) in married[0][2], (
        "a woman's married name keeps the married-name role")


def test_the_plan_covers_every_usage_the_classifier_asks_for():
    """A token the classifier calls `patronymic` must have a `patronymic` row in the plan.

    **The two components define patronymic differently, and both did it on purpose.**
    `namemodel.PATRONYMIC` matches `sen|son|sson|datter|sdatter`.
    `scripts/build-name-item-batch.py`'s `RELIABLE_PATRONYMIC` deliberately **excludes**
    `-son`/`-sen`, with its own stated reason: *"they also end ordinary inherited surnames
    and a few real given names (`Jefferson`, 30 bearers)"*.

    So the plan files `Gundersen` as `given` (63 bearers) and `family` (19, with `Q656767`),
    the classifier looks up `(Gundersen, patronymic)`, and the lookup misses an item that
    exists. The person then gets **no name statement at all** — which is what was reported on
    `Q141189052` Anna Carine Gundersen, whose three tokens all failed.

    Measured over `reports/name-item-plan.csv`: **1,051 tokens, 31,259 bearers**, led by
    `Olsen` 1,147, `Pedersen` 678, `Olson` 511, `Hansen` 503, `Andersen` 476, `Larsen` 442.
    **330 of them already carry a Wikidata item** under given/family, covering 12,798
    bearers — and per `CLAUDE.md` § *One name item per USAGE* a patronymic is a **different**
    item, so those cannot simply be linked.

    **FIXED 2026-08-27.** `scripts/build-name-item-batch.py` now emits a patronymic row for a
    `-sen`/`-son` token **as well as** its given/family rows, rather than instead of them.
    That is `CLAUDE.md` § *One name item per USAGE*: a token used two ways gets two items, and
    it is not an ambiguity to resolve. The father test then decides per person which of the
    two that person links to. Patronymic rows in the plan: 623 -> 1,677.

    **This assertion was a strict `xfail` for a day and never tested anything.** It failed with
    `NameError: name 'REPO' is not defined` -- a constant that file does not define -- so the
    marker was satisfied by a typo rather than by the defect. Exactly the failure the repo has
    been recording all week: a guard not seen to fail *for the right reason* is not known to
    guard.
    """
    plan_path = Path(__file__).resolve().parent.parent / "reports" / "name-item-plan.csv"
    if not plan_path.exists():
        pytest.skip("no name plan built")
    import csv as _csv
    rows = list(_csv.DictReader(open(plan_path, encoding="utf-8")))
    have_patronymic = {r["token"] for r in rows if r["usage"] == "patronymic"}
    missing = [r for r in rows
               if r["usage"] in ("given", "family")
               and PATRONYMIC.match(r["token"])
               and r["token"] not in have_patronymic]
    bearers = sum(int(r["bearers"]) for r in missing)
    assert not missing, (
        f"{len(missing)} tokens the classifier calls patronymic have no patronymic row "
        f"in the plan, covering {bearers:,} bearers, e.g. "
        + ", ".join(f"{r['token']}({r['bearers']})" for r in missing[:5]))


def test_the_father_decides_patronymic_from_inherited_surname():
    """The test as first stated, 2026-08-26, whose literal reading is 91% wrong.

    *"If father has -son or -sen then it's a surname lol that's the test same with other
    patronymic surnames."* Taken literally that calls 91% of these tokens surnames — because
    in a patronymic-naming society the father almost always carries one too. `Einar Jonsen
    Vestad`'s father is `John Kristiansen Jevne`; `Maria Christina Jakobsdotter`'s father is
    `Jakob Jakobsson`. Both are textbook patronymics.

    **What discriminates is the SAME token.** Measured over the 286,536 people with such a
    token and a known father: same token → surname 40,872 (14%); stem matches the father's
    given name → patronymic 213,898 (75%); neither → undecided 31,766 (11%), which keep the
    morphological answer rather than being guessed the other way.
    """
    # Father carries the SAME token -> inherited surname.
    got = dict((t, u) for t, u, _o in classify_fields(
        "Susannah", "Slawson", father_name="James Slawson"))
    assert got["Slawson"] == "family", got

    # Stem is the father's given name -> patronymic.
    got = dict((t, u) for t, u, _o in classify_fields(
        "John", "Kristiansen Jevne", father_name="Kristian Eriksen Jevne"))
    assert got["Kristiansen"] == "patronymic", got
    assert got["Jevne"] == "family", got

    # A `-datter` works the same way.
    got = dict((t, u) for t, u, _o in classify_fields(
        "Maria", "Jakobsdotter", father_name="Jakob Jakobsson"))
    assert got["Jakobsdotter"] == "patronymic", got


def test_without_a_father_the_classifier_is_unchanged():
    """Every existing caller passes no father, and must keep today's answer.

    The father test is additive: `father_name` defaults to empty and the morphological rule
    stands. Nine call sites rely on that, and a silent change to any of them would move name
    statements for people nobody was looking at.
    """
    got = dict((t, u) for t, u, _o in classify_fields("John", "Kristiansen Jevne"))
    assert got["Kristiansen"] == "patronymic"
    got = dict((t, u) for t, u, _o in classify_fields("Susannah", "Slawson"))
    assert got["Slawson"] == "patronymic", "morphology alone still says patronymic"


def test_the_swedish_dotter_is_a_patronymic_like_the_danish_datter():
    """`-dotter` is Swedish, `-datter` is Norwegian and Danish, and both mean daughter of.

    `PATRONYMIC` listed `datter` and not `dotter`, so **60,085 people** were classified as
    carrying a family name — `Johansdotter` 5,612 bearers, `Andersdotter` 5,472, `Olofsdotter`
    3,157, `Nilsdotter` 2,868 — when every one of them is a patronymic.

    **The repo already disagreed with itself.** `scripts/build-name-item-batch.py`'s
    `RELIABLE_PATRONYMIC` has listed `dotter` and `sdotter` from the start, so the plan builder
    and the classifier read the same token two different ways. It surfaced because the father
    test's own `PATRONYMIC_PARTS` included `dotter` while `PATRONYMIC` did not, and the two
    then disagreed on `Jakobsdotter`.
    """
    for token in ("Andersdotter", "Johansdotter", "Olofsdotter", "Jakobsdotter"):
        got = dict((t, u) for t, u, _o in classify_fields("Maria", token))
        assert got[token] == "patronymic", f"{token} -> {got[token]}"
    # The Norwegian form must not have regressed.
    got = dict((t, u) for t, u, _o in classify_fields("Ane", "Eivindsdatter"))
    assert got["Eivindsdatter"] == "patronymic"


def test_the_father_name_reaches_statements_for_and_changes_the_property():
    """End to end: the father decides whether a `-sen` token becomes `P734` or `P5056`.

    Passing `father_name` was the missing half. `classify_fields` gained the test on
    2026-08-26 and nothing handed it a father, so it was built and unused for a day.

    `Gundersen` is the worked case, and it shows the rule recovering a statement that was
    otherwise lost. The plan holds `(Gundersen, family) -> Q656767 link` and
    `(Gundersen, patronymic) -> create`:

    * **no father** — morphology says patronymic, whose item does not exist yet, so nothing
      is emitted. This is what every caller did before, and what still happens when the
      father is unknown.
    * **father `Gunder Olsen`** — the stem matches his given name, so it really is a
      patronymic. Still nothing, correctly: that item is waiting to be minted.
    * **father `Hans Gundersen`** — he carries the same token, so this is an inherited
      surname and `P734` -> `Q656767` goes out.

    The third case is the point: `Anna Gundersen` daughter of `Hans Gundersen` used to get no
    name statement at all.
    """
    plan = load_plan()
    if plan.get(("Gundersen", "family"), ("", ""))[0] != "Q656767":
        pytest.skip("the name plan no longer links Gundersen as a family name")
    fields = {"givn": "Anna", "surn": "Gundersen", "nick": "", "marnm": ""}

    def props(father_name):
        lines, _notes = statements_for("Anna Gundersen", plan, "1", fields=fields,
                                       father_name=father_name)
        return [(p, v) for p, v, _q in lines]

    # **Scoped to the GUNDERSEN token, which is what this test is about.** It asserted the
    # whole statement list was empty, and that rested on `Anna` having no given-name item --
    # incidental, and it stopped being true on 2026-08-30 when the name lookup started
    # answering from the 823,907 name items in the local store rather than from the plan
    # alone. `Anna` is `Q666578`, `Q11879590` *female given name*, and emitting it is a
    # statement we were previously missing, not a regression.
    def gundersen(father_name):
        """Which PROPERTY the GUNDERSEN token produces: a patronym, or its family item."""
        return [prop for prop, value in props(father_name)
                if value == "Q656767" or prop == PATRONYM]

    # **Asserted on the property, not on the statement list being empty.** Two of these read
    # `== []` until 2026-08-30, and that rested on no item existing for the patronymic
    # `Gundersen` -- which is time-varying state this repo actively changes: the name-item
    # generator created `Q141223748` and the test went red without any behaviour changing.
    # What the test is actually about is that `father_name` decides P5056 against P734, and
    # that is what it now says.
    assert gundersen("") == [PATRONYM], "no father, so the morphological reading stands"
    assert gundersen("Gunder Olsen") == [PATRONYM], (
        "stem matches his given name, so still a patronymic")
    assert gundersen("Hans Gundersen") == [FAMILY_NAME], (
        "the father carries the same token, so it is an inherited surname")


# --------------------------------------------------------------------------------------
# Markers in the GIVEN-NAME field, and stillbirth descriptions.
#
# Both fixed 2026-08-31 from `Q141224141`: an item created as `En dödfödd son Bielke`,
# which is simply wrong, and the ruling that names must not be assigned to a person who
# has no names at all.
#
# The item is the worked case for both. Our batch created it, gave it `P735` *given
# name* `En` -- the Swedish indefinite article -- with `P7452` *usual forename*. The
# statements were deleted by hand at 20:57 on 08-30, the next batch put them back at 22:32,
# and they were deleted again at 22:34.
# --------------------------------------------------------------------------------------

def test_a_marker_in_givn_is_not_a_given_name():
    """`name_shape` did not run on `GIVN` at all, so the marker set never fired there.

    15,101 people in `reports/display-names.csv` carry one of these in `GIVN`, and every
    one was a `P735` *given name* proposal.
    """
    for marker in ("NN", "Unknown", "okänd", "anonyma", "n.n.", "?"):
        usages = {u for _t, u, _o in namemodel.classify_fields(givn=marker, surn="Smith")}
        assert "given" not in usages, f"{marker!r} in GIVN still reads as a given name"
        assert "unknown" in usages, f"{marker!r} in GIVN is not recognised as a marker"


def test_the_surname_survives_a_marker_in_givn():
    """Detection is not suppression — `CLAUDE.md` § *An obvious unknown-word marker*.

    An `unknown Bloomfield` keeps a label and becomes `NN Bloomfield`, so the family
    name must still come through.
    """
    tokens = namemodel.classify_fields(givn="NN", surn="Bloomfield")
    assert ("Bloomfield", "family", 0) in tokens


def test_a_stillbirth_description_yields_no_given_name():
    """The WHOLE `GIVN` goes, not just the stillborn word.

    `En` and `son` are the rest of one phrase, not names sitting next to one. 470 people.
    """
    for givn in ("En dödfödd son", "dødfødt", "(--stillborn--)", "dödfött barn"):
        tokens = namemodel.classify_fields(givn=givn, surn="Bielke")
        assert not [t for t in tokens if t[1] == "given"], f"{givn!r} produced a given name"
        # ...and no nickname either: the bracketed form is read as a byname by `QUOTED`,
        # so without suppressing it too it reaches Wikidata as an `Amul` alias instead.
        assert not [t for t in tokens if t[1] == "nickname"], f"{givn!r} produced a nickname"
        assert ("Bielke", "family", 0) in tokens, f"{givn!r} lost the surname"


def test_an_ordinary_name_is_untouched_by_either_rule():
    """The guard against over-reach: neither rule may eat a real name."""
    tokens = namemodel.classify_fields(givn="Arne Olaus", surn="Garborg")
    assert ("Arne", "given", 1) in tokens
    assert ("Olaus", "given", 2) in tokens
    assert ("Garborg", "family", 0) in tokens


def test_a_nickname_still_survives_a_normal_given_field():
    """`Stine "Stena" Eivindsdatter` — the quoted byname is not collateral damage."""
    tokens = namemodel.classify_fields(givn='Stine "Stena" Eivindsdatter', surn="Garborg")
    assert ("Stena", "nickname", 0) in tokens
    assert ("Stine", "given", 1) in tokens


def test_fersen_needs_the_father_to_stop_being_a_patronymic():
    """`Q141223488` — `Fersen` created as `P31` `Q110874` *patronymic*, twice.

    The rule as stated 2026-08-26: if the father has `-son` or `-sen` then it is a surname. The
    classifier implements it and `build-garborg-name-items.py` was calling it without a
    father, so every `-sen` token fell through to `patronymic`.
    """
    assert namemodel.patronymic_or_surname("Fersen", "") == "patronymic"
    assert namemodel.patronymic_or_surname("Fersen", "Hans Axel von Fersen") == "family"
    # A genuine patronymic must not be reclassified by the same rule.
    assert namemodel.patronymic_or_surname("Olsen", "Ole Hansen") == "patronymic"


# --- drop_description_suffix: a description marker is not a name -----------------------
#
# **Ruled 2026-09-07** on `Q141313961`, live as *Helena Maria Linnerhielm ogift*: `ogift` is
# a suffix that should never have been treated as part of the name. `ogift` is
# Swedish for *unmarried*.
#
# Every case below fails if a specific guard is removed, which is the bar
# `CLAUDE.md` § *The NO-NEW-TESTS moratorium ENDED* sets — `test_namemodel.py:620` passes
# with its discriminator deleted and is the warning these are written against.


def test_the_marker_comes_off_the_label():
    """The reported case. Fails if the rule is not wired to `_DESCRIPTION` at all."""
    assert namemodel.drop_description_suffix(
        "Helena Maria Linnerhielm ogift", "ogift") == "Helena Maria Linnerhielm"


def test_a_title_is_not_a_description_and_stays():
    """Scope: the 631 description labels were chosen over the 7,075 `drop_title_suffix` takes.

    Fails the moment this is widened to `NAME_SUFFIX_TITLES`, which is the one-line change
    that would silently reverse § *A TITLE IS NOT A NAME*'s *"it does not touch the LABEL"*.
    """
    label = "Dániel IV Esterházy de Galántha Graf"
    assert namemodel.drop_description_suffix(label, "Graf") == label
    assert namemodel.drop_title_suffix(label, "Graf") != label   # the wider rule would take it


def test_a_bare_word_list_would_take_a_real_surname():
    """`Anna King` keeps her surname because the match is against her OWN `NSFX`.

    Fails if the implementation ever matches a trailing token against the word list
    directly — the failure `drop_title_suffix` already carries a comment about.
    """
    assert namemodel.drop_description_suffix("Sarah Twin", "") == "Sarah Twin"
    assert namemodel.drop_description_suffix("Infant Jones", "Jones") == "Infant Jones"


def test_the_comma_that_introduced_the_marker_goes_with_it():
    """`Josiah Wood I, twin`. Fails without the `rstrip`, leaving `Josiah Wood I,`."""
    assert namemodel.drop_description_suffix("Josiah Wood I, twin", "I, twin") == "Josiah Wood I"


def test_never_to_empty():
    """A label that is nothing but a marker keeps it — an unlabelled item is worse."""
    assert namemodel.drop_description_suffix("twin", "twin") == "twin"


def test_both_corpus_spellings_of_oa_are_listed():
    """`oä` 12 and `(o.ä)` 4 are the only two forms the corpus holds, and both must strip.

    Fails if the dotted form is dropped from `_DESCRIPTION` — nothing is dot-stripped here,
    because dot-stripping put `d.e.` onto the particle `de`.
    """
    assert namemodel.drop_description_suffix(
        "Ester Frideborg Karlsson (o.ä) (ogift)", "(o.ä) (ogift)") == "Ester Frideborg Karlsson"

# --- a generation suffix that exists ONLY inside a label -------------------------------


def test_a_suffix_is_found_inside_a_full_label():
    """`generation_suffix_key` reads an NSFX FIELD and matches the whole of it, so it cannot
    see `den yngre` sitting at the end of a label. `Q5797554` is the worked case: Geni files
    him `NAME Detlof /Heijkenskjold/` with NO `NSFX`, Wikidata's label is the only record that
    he is the younger, and the ja/zh/ko labels this pipeline wrote dropped the suffix.
    """
    assert namemodel.generation_suffix_in_label(
        "Detlof Heijkenskjold den yngre") == "den yngre"
    assert namemodel.generation_suffix_key("Detlof Heijkenskjold den yngre") == ""


def test_the_particle_de_is_not_a_suffix():
    """⛔ The trap this table already paid for once: `d.e.` matched onto the particle `de`,
    102,336 occurrences. Nothing here is dot-stripped, and a bare particle must not match.
    """
    assert namemodel.generation_suffix_in_label("Juan de Vega") == ""
    assert namemodel.generation_suffix_in_label("Louise de Capels") == ""


def test_a_clean_label_yields_nothing():
    assert namemodel.generation_suffix_in_label("Detlof Heijkenskjold") == ""
    assert namemodel.generation_suffix_in_label("") == ""
    assert namemodel.generation_suffix_in_label(None) == ""


def test_the_first_label_carrying_one_wins():
    """It takes several labels, en then mul, and answers with the first that has a suffix."""
    assert namemodel.generation_suffix_in_label(
        "Detlof Heijkenskjold", "Detlof Heijkenskjold den yngre") == "den yngre"


def test_the_found_key_drives_both_forms():
    """The point of finding it: `mul` takes the Roman numeral and `en` the abbreviation,
    which is the 2026-09-04 ruling on `Q106206114` and is unchanged here.
    """
    key = namemodel.generation_suffix_in_label("Detlof Heijkenskjold den yngre")
    assert namemodel.normalise_generation_suffix(
        "Detlof Heijkenskjold", "mul", key) == "Detlof Heijkenskjold II"
    assert namemodel.normalise_generation_suffix(
        "Detlof Heijkenskjold", "en", key) == "Detlof Heijkenskjold Jr."


def test_the_english_surface_form_is_found_too():
    """`the Younger` is in the same table and appears on Wikidata labels."""
    assert namemodel.generation_suffix_in_label(
        "Erik Benzelius the Younger") == "the younger"


# --------------------------------------------------------------------------------------
# **THE `/` FAMILY NAME, REPORTED OFF THE QUICKSTATEMENTS THEMSELVES.** Emma, 2026-09-12:
# *"I am just letting you know that this was in the quickstatements. It is not a surname
# lol"* -- above a `CREATE` labelled `/`, `P31` *family name*, with three bearers pointed
# at it: `Q20498971` Margareta von Thüringen, `Q76238135` Elizabeth Latimer, `Q16206914`
# Bagrat Bagrationi. Geni files all three with two spellings of one surname in one field.
# --------------------------------------------------------------------------------------

def test_a_slash_between_two_spellings_is_not_a_family_name():
    """`SURN` splits on whitespace, which leaves Geni's separator standing as a token."""
    for surn in ("Latimer / de Latimer", "Van Kleef / von Cleves"):
        usages = {(t, u) for t, u, _o in namemodel.classify_fields(givn="X", surn=surn)}
        assert ("/", "family") not in usages, f"{surn!r} still mints a `/` family name"
        assert ("/", "unknown") in usages, f"{surn!r} does not recognise the separator"


def test_both_real_spellings_survive_the_separator():
    """Detection is not suppression, the same way it is not for an `NN` marker."""
    tokens = namemodel.classify_fields(givn="Elizabeth", surn="Latimer / de Latimer")
    assert ("Latimer", "family", 0) in tokens


def test_no_numeral_gets_a_name_item_in_any_notation():
    """Ruled 2026-09-13: *"why are you allowing any numerals at all? None of them are names."*

    And the scope, ruled in the same breath — *"This isn't even about what gets into labels.
    This is about what gets listed as a name and has an object made about it."* Neither
    `derive-labels.py` nor `labels.py` calls `name_shape`, so a regnal ordinal keeps its place
    in the label and loses only its `P734`/`P735` item.
    """
    for junk in ("/", "--", ".", "&", "()",           # punctuation
                 "3", "42", "1854", "(1)", "#2",      # digits
                 "I", "II", "III", "IV", "V", "XIV",  # Roman ordinals
                 "三", "十", "二世", "2世"):            # CJK numerals
        assert namemodel.name_shape(junk)[1] == "unknown", f"{junk!r} would get a name item"


def test_the_only_punctuation_in_a_name_is_a_hyphen():
    """Ruled 2026-09-14: *"The only valid punctuation in a name at all is a dash for a doible
    barred name."*

    **The test above this one has been RED since the day it was written**, 2026-09-13, on
    `'--' would get a name item` -- and eleven tests were red on `main` every day from at least
    2026-09-10, four of them the `HELD` gate, which is red on purpose while editing is held by
    hand. That is the mechanism the queue item was asking about: the guard was written, a test
    asserting the guard works was written, the test failed on its first run, and a suite with
    four permanently-red tests in it trains every reader to stop looking. Nothing was wrong with
    the reasoning in `namemodel`; what was missing was anyone reading the red.

    So this covers the classes by what they ARE, from the measurement over all 23,196 rows of
    `reports/name-item-plan.csv`, not by the five tokens that happened to be in the batch Emma
    read.
    """
    for junk in (".", "..", "-", "--", "(", ")", "[", "]", "{", "}", "#", ",", "()", ".,",
                 "Rd.", "NR.", "h.", "Mrs.", "кн.", "Svensdtr.", "Olsdtr.",   # trailing stop
                 "(Ulf", "(Wife", "(ou", "(Bupati", "[Versi", "II)", "?)",     # unmatched bracket
                 '"the', '"der', "«el", "“dit", "„gamli“",                # quote marks
                 "N/A", "vitad/Unknown", "1:", "Surname:", "#2", "[65]",       # separators
                 "&", "@", "+", "=", "…", "(?)", "孛兒只斤·",                 # the rest
                 "‎", "‏", "‎‏",                                           # INVISIBLE tokens
                 "R'", "'el", "ר'", "d´",                                   # edge apostrophe
                 "Chavez-", "Rodriguez-", "Romo-", "De-", "Nord-"):            # half a name
        assert namemodel.name_shape(junk)[1] == "unknown", f"{junk!r} would get a name item"


def test_a_conjunction_joins_one_family_name_rather_than_separating_two():
    """`Mangold von Thurgau und Nellenburg` is ONE family name, and `und` is not a surname.

    Refusing `und` stops the junk item and does nothing for the man, who still ends up with
    `Thurgau` and `Nellenburg` as two unrelated surnames instead of the one he has. Censused
    over `reports/display-names.csv`: **10,741 of 1,020,983 non-empty `SURN` fields are
    conjunction-joined**, and they are real houses -- `Natt och Dag` 167, `Oxenstierna af
    Korsholm och Wasa` 49, `Durán y Chávez` 43, `de Castilla y León` 29.
    """
    def families(surn):
        return [t for t, usage, _o in namemodel.classify_fields(givn="X", surn=surn)
                if usage == "family"]

    assert families("von Thurgau und Nellenburg") == ["Thurgau und Nellenburg"]
    assert families("Natt och Dag") == ["Natt och Dag"]
    assert families("Durán y Chávez") == ["Durán y Chávez"]
    assert families("Grant of Freuchie") == ["Grant of Freuchie"]
    assert families("Oxenstierna af Korsholm och Wasa") == ["Oxenstierna af Korsholm och Wasa"]
    # a connector needs a name on BOTH sides; a trailing one joins nothing
    assert families("Natt och") == ["Natt"]
    assert families("af Sweden") == ["Sweden"]


def test_a_surn_that_is_entirely_bracketed_is_the_name_inside_the_brackets():
    """`(Ulf af Horsnäs)` is a family name in brackets, not `(Ulf` plus two words.

    `(Ulf` was a `P734` with five bearers -- Christer, Johan, Erik, Johan and Märta -- because
    the field was whitespace-split before anything looked at it. 3,471 `SURN` fields carry a
    bracket. Only the whole-field case is unwrapped: `Høeg (Banner)` asks whether the bracketed
    half is a variant or a second family, and that is a naming question, not a splitting one.
    """
    def families(surn):
        return [t for t, usage, _o in namemodel.classify_fields(givn="X", surn=surn)
                if usage == "family"]

    assert families("(Ulf af Horsnäs)") == ["Ulf af Horsnäs"]
    assert families("Høeg (Banner)") == ["Høeg", "Banner"]     # left alone, deliberately

    # the brackets come off whatever the content turns out to BE: `Sigurðarson` unwraps and is
    # then read by form, which makes it a patronymic and not a family name at all.
    assert ("Sigurðarson", "patronymic", 0) in namemodel.classify_fields(
        givn="X", surn="[Sigurðarson]")


def test_a_joined_token_is_several_words_and_that_is_allowed():
    """The punctuation rule walked characters and refused the space, for about an hour.

    `join_particles` has produced multi-word tokens since it was written, and
    `name modelling.txt`'s own worked example is one: `Abisha III ben Phinhas ben Yittzhaq`,
    one `P5056` per link. Refusing the space turned every one of them into `unknown` -- the
    patronymic chain the joiner exists to preserve, dropped silently.
    """
    for joined in ("ben Phinhas", "ap Thomas", "bin Haji Muhammad", "Natt och Dag"):
        assert namemodel.name_shape(joined)[1] != "unknown", f"{joined!r} lost to the space"
    got = namemodel.classify_fields(givn="Abisha", surn="ben Phinhas")
    assert ("ben Phinhas", "patronymic", 0) in got
    # but a compound of nothing but non-name words still names nobody
    assert namemodel.name_shape("und und")[1] == "unknown"


def test_a_particle_stays_a_particle():
    """`von` is in `_LEADING_TITLES`, and wiring that list into `name_shape` reclassified it.

    125,328 occurrences moved from `particle` to `unknown`. Both are terminal and neither mints
    a name item, so nothing reached Wikidata -- but `particle` is what it is, and a refusal list
    swallowing the corpus's commonest particle is not a thing to leave standing. `PARTICLES` is
    consulted before both refusal lists.
    """
    for particle in ("von", "de", "van", "af", "di", "ben"):
        assert namemodel.name_shape(particle)[1] == "particle", particle


def test_a_title_is_not_a_name_and_the_title_list_is_actually_read():
    """`Count` is in `_LEADING_TITLES` AND in `NAME_SUFFIX_TITLES` and had 226 bearers.

    Both lists were written for § *A TITLE IS NOT A NAME* and `name_shape` read neither, so the
    rule was true in the vocabulary and false in the code -- § *Code that is WRITTEN but never
    CALLED is not done*. 113 title tokens, 3,555 bearers.
    """
    for title in ("Count", "Countess", "Graf", "Gräfin", "Freiin", "Pangeran", "Khatun",
                  "Saint", "Rabbi", "Capt", "Kung", "親王", "Stillborn", "Infant"):
        assert namemodel.name_shape(title)[1] == "unknown", f"{title!r} would get a name item"
    # The lists are consulted, not copied: a token added to either must take effect here.
    #
    # ⛔ `particle` counts as refused, and `von` is why. It is in `_LEADING_TITLES` -- a
    # nobiliary particle reasonably reads as a title -- AND in `PARTICLES`, which is consulted
    # first, so it answers `particle`. Both are terminal and neither mints a name item. Pinning
    # the exact string here is pinning an implementation detail, which is the same mistake that
    # made `test_the_pieces_of_a_split_name_are_not_names` go red on `das` the same day.
    for token in list(namemodel._LEADING_TITLES)[:50] + list(namemodel.NAME_SUFFIX_TITLES)[:50]:
        usage = namemodel.name_shape(token)[1]
        assert usage in ("unknown", "particle"), (
            f"{token!r} escaped the title list ({usage})")


def test_the_pieces_of_a_split_name_are_not_names():
    """`Mangold von Thurgau und Nellenburg` split on whitespace and `und` became a family name.

    Eight bearers pointed at it in the batch Emma read. The real fault is positional parsing in
    whatever splits the field -- § *PARSE PATRONYMICS BY FORM* -- and this is the guard that
    holds while that is still true. It is free to hold: *"There’s effectively zero cost for
    not creating a name object."*
    """
    # ⛔ **THE TEST IS *DOES THIS GET AN ITEM*, NOT *IS THE USAGE EXACTLY `unknown`*.** `das`,
    # `der`, `la`, `le`, `el` and `los` are also in `PARTICLES`, and the particle-precedence fix
    # of the same day makes `name_shape` answer `particle` for those. Both answers are terminal
    # and neither mints a name item, so pinning the exact string was pinning an implementation
    # detail -- and it went red on `das` within the hour. The usages that DO mint an item are
    # `None` (an ordinary name) and the real name usages; everything else is a refusal.
    for word in ("und", "and", "et", "ou", "och", "og", "or",
                 "the", "der", "die", "das", "el", "la", "le", "los", "las",
                 "aka", "alias", "dit", "dite", "genannt", "nee", "born", "known"):
        usage = namemodel.name_shape(word)[1]
        assert usage in ("unknown", "particle"), f"{word!r} would get a name item ({usage})"


def test_the_two_exceptions_to_the_punctuation_rule():
    """The apostrophe inside a word, and combining marks, which are letters and not punctuation.

    The apostrophe was put to Emma with the counts -- 196 tokens, about half of them real --
    and ruled *allow it INSIDE a word only*: a letter on each side keeps `d'Aragona` (90
    bearers), `Ja'far` (77) and `O'Brien`, while `R'` (179) and `'el` (74) stay refused by the
    test above.

    The combining marks are not a carve-out but a correct classification. NFC composes the
    Latin ones, so `A`+U+030A really is `Å` -- but Arabic harakat have no composed form, and
    `عَبْدُ` arrived as five letters and four marks. Both spellings of `Ådneson` must also
    reach the SAME token, or Geni's encoding decides how many name items a surname gets.
    """
    for real in ("d'Aragona", "d'Auvergne", "Ja'far", "O'Brien", "Rabi'a", "d’Ardres",
                 "Anne-Marie", "عَبْدُ", "بْن", "Strömberg", "María", "Oñate", "伏羲"):
        assert namemodel.name_shape(real)[1] != "unknown", f"{real!r} lost its name item"

    composed, decomposed = "Ådneson", "Ådneson"
    assert composed != decomposed                       # genuinely two different strings
    assert namemodel.name_shape(composed)[1] is None
    assert namemodel.name_shape(decomposed)[1] is None


def test_the_roman_rule_is_the_ordinal_SEQUENCE_and_not_the_alphabet():
    """`di` is 21,960 occurrences and `Li` is a Chinese surname — both are all-Roman letters.

    A blanket *every character is one of IVXLCDM* refuses them. The pattern is the ordinal
    sequence, uppercase, `I`/`V`/`X` only.

    ⛔ **`D`, `M`, `C` AND `L` MOVED OUT OF THE `name_shape` LIST ON 2026-09-18, AND THEY ARE
    STILL TESTED.** They were here because a blanket Roman rule refuses them, and they are
    4,736 / 2,562 / 1,647 / 1,344 in the corpus. They are now refused anyway, by a DIFFERENT
    rule ruled 2026-09-17 -- *"a single Latin letter is an initial, not a name"*, written after
    a `given name` item labelled `L` and a human item labelled `n` were created off this
    corpus. Two rules, two reasons, and asserting the wrong one here made the suite red for a
    day. So what this test owns is asserted directly against `is_numeral`: the numeral rule
    must not be the thing that refuses them.
    """
    for real in ("di", "Li", "Di", "il", "im", "ll", "Liv", "DILL",
                 "Bure", "孔", "Ærø", "Ólafsdóttir", "O'Brien"):
        assert namemodel.name_shape(real)[1] != "unknown", f"{real!r} lost its name item"
    for initial in ("D", "M", "C", "L"):
        assert not namemodel.is_numeral(initial), f"{initial!r} read as a Roman ordinal"


def test_the_gaelic_particles_mac_and_o():
    """`mac` is the commonest Gaelic patronymic particle and was missing until 2026-09-15.

    Censused over `reports/display-names.csv`, counting only a token that IS the particle with
    another name after it: `mac` 609, `ó` 95.

    **The standalone-token test is what makes this safe.** `MacDonald` written as one word is a
    surname and is untouched; `Mac Donald` as two tokens is the construction. That is why the
    count is 609 and not the tens of thousands of `Mac...` surnames in the corpus.
    """
    def usage(givn, surn):
        return {t: u for t, u, _o in namemodel.classify_fields(givn=givn, surn=surn)}

    assert usage("Domhnall", "Mac Cathail").get("Mac Cathail") == "patronymic"
    assert usage("Sean", "Ó Briain").get("Ó Briain") == "patronymic"
    # one word is a surname, not a construction
    assert usage("Domhnall", "MacDonald").get("MacDonald") == "family"


def test_abu_and_abd_are_NOT_patronymic_particles():
    """Both were added on 2026-09-15 and taken back out in the same edit.

    They are Semitic and they sit where a particle sits, which is exactly why they looked
    right — and neither means *son of*:

        abd   "servant of". `Abd Allah` and `Abd al-Rahman` are GIVEN names, theophoric ones.
              Classifying them patronymic renames the person after a father called Allah.
        abu   "father of". `Abu Bakr` is a teknonym: it names his SON, pointing the opposite
              way down the line from every other particle in the set.

    Caught by running `classify_fields` on them rather than by re-reading the list.
    """
    given = {t: u for t, u, _o in namemodel.classify_fields(givn="Abd Allah",
                                                            surn="ibn Muhammad")}
    assert given.get("Abd") == "given", "Abd is a given-name element, not a particle"
    assert given.get("ibn Muhammad") == "patronymic", "the real particle still works"
    assert "abu" not in namemodel.PATRONYMIC_PARTICLE
    assert "abd" not in namemodel.PATRONYMIC_PARTICLE


def test_a_marker_in_GIVN_means_the_field_holds_no_given_names():
    """`6000000007645527815` / `Q141451100`: `GIVN` is `konenes navn ukjent`.

    Norwegian for *the wife's name is unknown*. `ukjent` was refused correctly and the other two
    tokens went out as `P735` given names, so the person was given the forenames **`konenes`**
    and **`navn`** — *wives'* and *name*. The marker was removing its own token instead of
    condemning the field.

    **It suppresses GIVEN names only.** 3,460 fields carry a marker beside other tokens, and the
    other token is either a descriptive word (`Unknown Wife` 41, `Ukendt hustru` 13) or a real
    patronymic (`NN Olsdatter` 18, `N.N. Nielsdatter` 11). Dropping the whole field would throw
    those patronymics away, and on a record whose given name is unknown they are the most useful
    thing on it.
    """
    def usages(givn, surn=""):
        return [(t, u) for t, u, _o in namemodel.classify_fields(givn=givn, surn=surn)]

    assert not [u for _t, u in usages("konenes navn ukjent") if u == "given"]
    assert not [u for _t, u in usages("Unknown Wife") if u == "given"]
    assert not [u for _t, u in usages("nn ektefelle") if u == "given"]
    # the patronymic survives
    assert ("Olsdatter", "patronymic") in usages("NN Olsdatter")
    # and an ordinary name is untouched
    assert ("Ole", "given") in usages("Ole")
    assert ("Peter", "given") in usages("Anders Peter", "Olsen")


def test_a_roman_name_gets_no_name_items():
    """Ruled 2026-09-14: *"never actually apply names and given names to Roman people since they
    always get undone, I think due to the weird naming structure of them."*

    `Gaius Julius Caesar` is praenomen, nomen and cognomen — a personal name, a CLAN name and a
    branch name. None of the three is a given name or a surname in the sense `P735` and `P734`
    mean, which is why editors revert them.

    **The praenomen alone is not the test, and `Marcus` is why**: 116 people in the corpus are
    called simply `Marcus`, and `Marcus Marcusson` and `Marcus Olofsson` are Scandinavian. The
    discriminator is the tria nomina shape — 1,630 match it, 616 carry a praenomen without one.
    """
    for givn, surn in (("Gaius Julius", "Caesar"), ("Appius Claudius", "Pulcher"),
                       ("Marcus Aemilius", "Lepidus"), ("Sextus Julius", "Caesar")):
        assert namemodel.classify_fields(givn=givn, surn=surn) == [], f"{givn} {surn}"

    # Scandinavians called Marcus keep everything
    got = [(t, u) for t, u, _o in namemodel.classify_fields(givn="Marcus", surn="Olofsson")]
    assert ("Marcus", "given") in got and ("Olofsson", "patronymic") in got
    assert namemodel.classify_fields(givn="Marcus", surn="") != []


def test_romance_patronymics_are_a_curated_set_and_Johannes_is_not_one():
    """Ruled 2026-09-14 that Romance support was missing and *"they are the hardest and the most
    dead"*. Measured 2026-09-15; right on both counts.

    3,381 distinct Romance-ending tokens -> 93 after locality -> 10 after the father test -> 3
    after the ratio. **The ratio guard is the one this case needed and the pairs did not.**

    `Johannes` passes the first two: it ends `-es`, and `Johann` is a given name in the universe.
    And it is used as a given name **10,742 times against once as a surname**. A rule making it a
    patronymic would rename ten thousand people after a father called Johann.

    `Hughes` is refused at 48% — English, fossilised, the same class as the `Williamson` the
    pairs rejected.

    Three tokens is why this is a set and not a regex: the universe is Scandinavian, so Iberian
    patronymics barely occur in it, and a rule would carry all the risk of `-es` for no more
    coverage than naming them.
    """
    for real in ("Fernandez", "Alvarez", "Fernandes", "fernandez"):
        assert namemodel.is_patronymic(real), real
    for refused in ("Johannes", "Hughes", "Mendes", "Torres"):
        assert not namemodel.is_patronymic(refused), refused

    got = [(t, u) for t, u, _o in namemodel.classify_fields(givn="Diego", surn="Fernandez")]
    assert ("Fernandez", "patronymic") in got
    # the one that matters: Johannes stays a given name
    got = [(t, u) for t, u, _o in namemodel.classify_fields(givn="Johannes", surn="Olsen")]
    assert ("Johannes", "given") in got


# ---------------------------------------------------------------------------------------
# An abbreviated patronymic is never written down as a name. Ruled 2026-09-15.
# ---------------------------------------------------------------------------------------

def test_an_abbreviated_patronymic_is_not_a_name():
    """⛔ *"Feminine patronymic abbreviations like "Olsdtr." really should at this point be only
    present at all in the "subject named as" in the geni id."* Ruled 2026-09-15.

    298 of these were planned as permanent name items, 108 of them classified `given` and 41
    `family` -- `Olsdtr` is not a given name in any register. A name item's label IS its
    identity, so § *it's better to create no name object than a bad one* applies at its
    strongest.
    """
    from namemodel import is_abbreviated_patronymic as abbrev
    for token in ("Olsdtr", "Olsdtr.", "Ormsd", "Johansdr", "Larsdtr.", "Pedersdt"):
        assert abbrev(token), token
    for token in ("Olsdatter", "Olsdotter", "Jónsdóttir", "Willemsdochter",
                  "Olsen", "Olsson", "Svend", "Halvard", "Hand", "David", "Ingrid"):
        assert not abbrev(token), token


def test_the_abbreviation_is_refused_at_the_classifier():
    """`classify_fields` is the choke point every emitter that classifies goes through."""
    from namemodel import name_shape
    assert name_shape("Olsdtr") == ("Olsdtr", "unknown")
    assert name_shape("Olsdtr.") == ("Olsdtr.", "unknown")
    # A full form is untouched -- the refusal must not widen.
    assert name_shape("Olsdatter") != ("Olsdatter", "unknown")


def test_the_patronymic_predicates_still_match_abbreviations():
    """⛔ The refusal is a SEPARATE question and must not leak into the others.

    `PATRONYMIC` and `is_daughter_patronymic` answer *is this token a patronymic*, and
    `patronymic_or_surname` and the `_MARNM` rule both depend on them still matching the
    abbreviated forms. Only *may this string be written down as a name* is refused.
    """
    from namemodel import PATRONYMIC, is_daughter_patronymic
    assert PATRONYMIC.match("Olsdtr")
    assert is_daughter_patronymic("Ljødelsdtr.")


def test_every_name_item_emitter_refuses_the_abbreviation():
    """⛔ § *A GUARD IN ONE EMITTER IS NOT A GUARD* -- and it caught this one.

    The guard went into `classify_fields` first; `build-name-item-batch.py` does not call it,
    reads `namemodel.PATRONYMIC` directly and builds its own usages, so all 298 abbreviated
    tokens were still in the plan on the re-run. The other two emitters read the plan and are
    covered by it being clean.
    """
    import re
    from pathlib import Path
    repo = Path(__file__).resolve().parent.parent
    batch = (repo / "scripts" / "build-name-item-batch.py").read_text(encoding="utf-8")
    assert "is_abbreviated_patronymic" in batch, "the plan builder has no guard"

    plan = repo / "reports" / "name-item-plan.csv"
    if plan.exists():
        import csv
        abbrev = re.compile(r"^(.+?)s(dtr|dt|dtt|dttr|dr|d)\.?$", re.I)
        with plan.open(encoding="utf-8") as fh:
            bad = [r["token"] for r in csv.DictReader(fh) if abbrev.match(r["token"])]
        assert not bad, f"abbreviated tokens planned as name items: {bad[:10]}"


# ---------------------------------------------------------------------------------------
# Finnish patronymics. Ruled 2026-09-15, queue.md § *Implementing non-Scandinavian
# Patronymics*: "I keep on telling you to do this and you keep on not doing it."
# ---------------------------------------------------------------------------------------

def test_finnish_patronymics_are_recognised():
    """⛔ 45,187 occurrences and `PATRONYMIC` matched none of them until 2026-09-15.

    For scale, Icelandic `-dóttir` is 1,424 in the same corpus and has been modelled from the
    start. `-poika` is 22,632 and `-tytär` 22,555.
    """
    from namemodel import PATRONYMIC, is_finnish_patronymic
    for token in ("Juhonpoika", "Matinpoika", "Antinpoika",
                  "Juhontytär", "Matintytär", "Heikinpoika"):
        assert PATRONYMIC.match(token), token
        assert is_finnish_patronymic(token), token


def test_the_finnish_genitive_n_is_required():
    """⛔ The `n` does the same work the Scandinavian genitive `s` does.

    Finnish builds a patronymic from the father's given name in the GENITIVE plus `poika` or
    `tytär`: `Juho` -> `Juhon` + `poika`. Requiring it is what keeps the bare words out --
    `poika` and `tytär` are simply Finnish for *son* and *daughter*, a relation word and not a
    name, and they occur 31 times in the corpus as bare tokens.

    Measured: 22,605 of 22,632 `-poika` and 22,530 of 22,555 `-tytär` carry the `n`, which is
    100% to the rounding; the remainder are exactly those bare words.
    """
    from namemodel import PATRONYMIC, is_finnish_patronymic
    for bare in ("poika", "Poika", "tytär", "Tytär"):
        assert not is_finnish_patronymic(bare), bare
        assert not PATRONYMIC.match(bare), bare


def test_the_finnish_pair_shares_the_genitive():
    """`Juhonpoika` <-> `Juhontytär`, never `Juhonntytär`.

    The same rule as the Scandinavian genitive `s`, which `Rasmussen -> Rasmusdatter` pins.
    402 stems in the corpus carry both forms.
    """
    from namemodel import patronymic_counterpart
    assert patronymic_counterpart("Juhonpoika") == "Juhontytär"
    assert patronymic_counterpart("Juhontytär") == "Juhonpoika"
    assert patronymic_counterpart("Matinpoika") == "Matintytär"
    # and the Scandinavian rule is untouched
    assert patronymic_counterpart("Rasmussen") == "Rasmusdatter"


def test_tytar_is_a_daughter_form_and_poika_is_not():
    """A woman takes her husband's name and no husband is called *daughter of*.

    So `-tytär` is impossible as a married name, exactly as `-datter` is. `-poika` is
    deliberately absent for the same reason `-son` is: a Finnish woman marrying a man called
    `Juhonpoika` does take it.
    """
    from namemodel import is_daughter_patronymic
    assert is_daughter_patronymic("Matintytär")
    assert is_daughter_patronymic("Juhontytär")
    assert not is_daughter_patronymic("Juhonpoika")
    assert is_daughter_patronymic("Olsdatter")
    assert not is_daughter_patronymic("Olsson")


def test_finnish_is_a_reliable_patronymic_in_the_plan():
    """⛔ § *A GUARD IN ONE EMITTER IS NOT A GUARD* -- the plan carries its own suffix list.

    `RELIABLE_PATRONYMIC` is the set where the suffix ALONE settles that a token is a
    patronymic; `-son`/`-sen` are deliberately absent because they are also inherited surnames.
    `-npoika` and `-ntytär` carry no such ambiguity -- no Finnish family name takes that shape.
    """
    from pathlib import Path
    repo = Path(__file__).resolve().parent.parent
    source = (repo / "scripts" / "build-name-item-batch.py").read_text(encoding="utf-8")
    block = source[source.index("RELIABLE_PATRONYMIC = ("):]
    block = block[:block.index(")")]
    assert "npoika" in block and "ntyt" in block, block


def test_the_contaminated_families_are_not_modelled():
    """⛔ Measured and REFUSED, and the refusal is the point.

    The census found other families and they are noise, not signal: Slavic `-ić` 8,179
    unmatched is `Eric` 1,864, `Henric` 1,205, `Fredric` 748 -- given names; Greek `-ides` 784
    is `Benavides` 438, a Spanish surname; Hungarian `-fi` 727 is `Al-Thaqafi` and `Al-Hanafi`,
    Arabic nisbas. Matching any of them would put a `P5056` on thousands of people who have no
    patronymic at all.
    """
    from namemodel import PATRONYMIC
    for token in ("Eric", "Henric", "Fredric", "Ulric",
                  "Benavides", "Benevides", "Ridolfi", "Al-Thaqafi"):
        assert not PATRONYMIC.match(token), token


# ---------------------------------------------------------------------------
# ⛔ A LABEL THAT IS ONLY A RELATION NAMES SOMEBODY ELSE. Ruled 2026-09-21.
#
# *"You still are producing wrong things where a person's first name is known, but their
# labels that they're given are relational. That is not supposed to be happening. And you're
# doing that as the biggest issue of this entire fucking campaign."*
#
# The rule already existed -- `build-nn-label-batch` has emitted `Andreas father of Malin`
# since 2026-09-09 -- and `build-garborg-day.describe_all` never got it, which is exactly the
# shape § *A GUARD IN ONE EMITTER IS NOT A GUARD* describes. These tests pin the rule in the
# MODEL so the next emitter is covered without being told.
# ---------------------------------------------------------------------------

def test_a_known_given_name_leads_the_descriptive_label():
    """`Tora mother of Brita`, never a bare `mother of Brita`.

    A label that is only a relation names the RELATIVE, so the item cannot be found and
    cannot be told apart from every other item labelled the same way. That is what makes it
    useless rather than merely untidy.
    """
    from namemodel import lead_with_given_name
    assert lead_with_given_name("Andreas", "father of Malin") == "Andreas, father of Malin"
    assert lead_with_given_name("Tora", "mother of Brita Danielsdotter Berg") == (
        "Tora, mother of Brita Danielsdotter Berg")
    # ⛔ **A COMMA, ruled 2026-09-21** -- the `Tora NN` item's own form, which reversed the
    # bare space of 2026-09-09. `tests/test_nn_label_batch.py` moved to match, because one
    # form across both emitters is the reason this lives in the model.
    assert lead_with_given_name("Andreas", "father of Malin").startswith("Andreas,")


def test_a_person_with_no_given_name_keeps_the_bare_relation():
    """The descriptive label was never wrong in itself.

    Someone with no name at all has nothing else to be called, and `CLAUDE.md` § *The
    NN/Private label algorithm applies to EVERY unnamed person* asks for exactly this. The
    defect was narrower: a given name in hand and thrown away.
    """
    from namemodel import lead_with_given_name
    assert lead_with_given_name("", "daughter of Olof Larsson") == "daughter of Olof Larsson"
    assert lead_with_given_name(None, "wife of Rostaing Arbald") == "wife of Rostaing Arbald"


def test_leading_with_the_given_name_is_idempotent():
    """Applied at two layers it must not double the name.

    `build-nn-label-batch` already prefixes from `mul`; if the model is applied over the top
    the result has to stay `Andreas father of Malin`, never `Andreas Andreas father of Malin`.
    """
    from namemodel import lead_with_given_name
    once = lead_with_given_name("Andreas", "father of Malin")
    assert lead_with_given_name("Andreas", once) == once


def test_the_cjk_name_goes_last_because_that_is_where_it_goes():
    """⛔ The CJK apposition follows the noun. Ruled 2026-09-21: the NATIVE order.

    `マリンの父アンドレアス` is *Malin's father Andreas*, name LAST -- the reverse of the
    European `Andreas, father of Malin`. Japanese and Chinese take no joiner at all; Korean
    takes a space.
    """
    from namemodel import lead_with_given_name
    assert lead_with_given_name("アンドレアス", "マリンの父", "ja") == "マリンの父アンドレアス"
    assert lead_with_given_name("安德烈斯", "馬林之父", "zh") == "馬林之父安德烈斯"
    assert lead_with_given_name("안드레아스", "마린의 아버지", "ko") == "마린의 아버지 안드레아스"
    # No comma anywhere in CJK -- the European separator does not travel.
    assert "," not in lead_with_given_name("アンドレアス", "マリンの父", "ja")


def test_the_cjk_tail_is_idempotent_too():
    """Applied twice it must not repeat the name at the end."""
    from namemodel import lead_with_given_name
    once = lead_with_given_name("アンドレアス", "マリンの父", "ja")
    assert lead_with_given_name("アンドレアス", once, "ja") == once


def test_the_model_never_transliterates_for_cjk():
    """⛔ The CALLER renders the name into the script; this only places it.

    A Latin name handed in for a `ja` label would produce the mixed-script label the
    2026-09-03 `ソン・オフ・` ruling forbids, so `describe_all` transliterates first and
    DROPS all three CJK labels when it cannot -- § *Partial is worse than absent*. This test
    records that the model is not the place that guard lives.
    """
    from namemodel import lead_with_given_name
    # It places whatever it is given, faithfully -- which is exactly why the caller must not
    # hand it a Latin token for a CJK language.
    assert lead_with_given_name("Tora", "マリンの母", "ja") == "マリンの母Tora"
    source = (Path(__file__).resolve().parents[1]
              / "scripts" / "build-garborg-day.py").read_text(encoding="utf-8")
    assert "own_ja, own_zh, own_ko = label_in(own, table)" in source
    assert "out.pop(code, None)" in source


def test_own_given_name_refuses_a_marker_and_a_relatives_name():
    """What counts as the person's OWN given name, and the two things that are not.

    `NN` is a marker, not a name. `NN ektefelle Søren Jonson` is her HUSBAND -- the
    `Q141352505` case `names_a_relative` exists for. A marker beside a real given name is
    stripped rather than refused, because `NN Tora` and `Tora` are the same person's given
    name with the unknown half written out.
    """
    from namemodel import own_given_name
    assert own_given_name({"givn": "Tora"}) == "Tora"
    assert own_given_name({"givn": "NN Tora"}) == "Tora"
    assert own_given_name({"givn": "NN"}) == ""
    assert own_given_name({"givn": "NN ektefelle Søren Jonson"}) == ""
    assert own_given_name({}) == ""
    assert own_given_name(None) == ""


def test_a_woman_goes_under_her_maiden_name_and_a_man_under_his_married_one():
    """Ruled 2026-09-21: *"women are made under their maiden names ... Men are still under their
    married names."* Unknown sex keeps the rule as it stood."""
    from namemodel import married_is_primary
    assert married_is_primary("F") is False
    assert married_is_primary("M") is True
    assert married_is_primary("") is True


def test_own_given_name_refuses_what_is_not_a_first_name():
    """2026-09-24, from a dry run of the relational-label correction over the live ledger:
    `???`, `konenes navn` (*the wife's name*), `mm`, `n` and a bare patronymic all passed as a
    given name and would have led a label -- `???, wife of Peder Bjornson Grude`."""
    from namemodel import own_given_name
    for givn in ("???", "konenes navn", "mm", "n", "N", "Olavsdatter", "NN"):
        assert own_given_name({"givn": givn}) == "", givn
    assert own_given_name({"givn": "Tora NN"}) == "Tora"
    assert own_given_name({"givn": "Anna Olsdatter"}) == "Anna Olsdatter"
    assert own_given_name({"givn": "Mariet"}) == "Mariet"


def test_a_particle_filed_on_both_sides_of_the_seam_is_said_once():
    """`GIVN Grimus von` + `SURN von Rügen` (2026-09-24). A capitalised repeat is a name and
    stays: `Joseph Thomas Thomas`."""
    from namemodel import drop_doubled_particle as drop
    assert drop("Grimus von von Rügen", "Grimus von", "von Rügen") == "Grimus von Rügen"
    assert drop("Gwrddwfin ap ap Cwrrig", "Gwrddwfin ap", "ap Cwrrig") == "Gwrddwfin ap Cwrrig"
    assert drop("Joseph Thomas Thomas", "Joseph Thomas", "Thomas") == "Joseph Thomas Thomas"
    assert drop("Per Andersson", "Per", "Andersson") == "Per Andersson"


def test_the_languages_that_write_d_y_and_d_e_get_their_own_label():
    """Queued 2026-09-24: `mul` says `II`, `en` says `Jr.`, and the Scandinavian languages say
    the form they actually use -- suffix last, `d.ä.` for the Swedish elder."""
    young = namemodel.native_generation_labels("Lars Jonson d.y. Skrudland")
    assert set(young) == {"nb", "nn", "no", "da", "sv"}
    assert young["sv"] == "Lars Jonson Skrudland d.y."
    assert namemodel.native_generation_labels("Per Olsen d.e.") == {
        c: "Per Olsen d.e." for c in ("nb", "nn", "no", "da")}
    assert namemodel.native_generation_labels("Johan Andersson d.ä.") == {
        "sv": "Johan Andersson d.ä."}
    assert namemodel.native_generation_labels("Elias Lagerheim", "Jr.") == {}
    assert namemodel.native_generation_labels("Anna Berg") == {}


@pytest.mark.parametrize("givn, father, token, kind", [
    ("Ericus Petri", "Per", "Petri", "patronymic"),     # father in the vernacular
    ("Petrus Olai", "Olof", "Olai", "patronymic"),
    ("Anders Olavi", "Olof", "Olavi", "patronymic"),
    ("Andreas Erici", "Erik", "Erici", "patronymic"),
    ("Laurentius Petri", "Petrus", "Petri", "patronymic"),  # father in Latin, as before
    ("Olavi", "Juho", "Olavi", "given"),                 # a Finnish given name stays one
])
def test_a_latin_patronymic_is_confirmed_by_a_vernacular_father(givn, father, token, kind):
    """Reviewed 2026-09-24: `Erici`/`Olai`/`Petri`/`Olavi` were second given names whenever the
    father was recorded as `Erik`/`Olof`/`Per` -- the usual case -- so bearers got `P735`."""
    got = {t: k for t, k, _ in namemodel.classify_fields(givn=givn, surn="", father_given=father)}
    assert got[token] == kind


@pytest.mark.parametrize("givn, surn, kept, gone", [
    ("Lars W", "", "Lars", None),
    ("Robert VI", "", "Robert", None),
    ("Hugues I", "d'Amboise", "Hugues", None),
    ("Carl I.", "Berg", "Carl", None),
    ("Anna M", "Olsdotter", "Anna", None),
    ("NN Anna", "Berg", None, "Anna"),        # a real marker still suppresses, as designed
])
def test_an_initial_or_a_numeral_does_not_suppress_the_given_names(givn, surn, kept, gone):
    """Measured 2026-09-24: 31,401 people lost their given name to a letter or numeral beside
    it arming the marker rule. `reports/middle-initials.csv` is the census."""
    got = {t: k for t, k, _ in namemodel.classify_fields(givn=givn, surn=surn)}
    if kept:
        assert got.get(kept) == "given"
    if gone:
        assert gone not in got
