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


def test_usual_forename_is_emitted_ONLY_where_there_is_a_middle_name():
    """Emma, 2026-08-24: *"usual forename only applies when there is a middle name"*.

    `P7452` → `Q3409033` exists to say which of several given names is the one actually
    used. On a person with a single given name it distinguishes nothing and asserts a
    contrast that does not exist.

    **This test previously asserted the opposite** — that a lone given name carries it —
    which is exactly what the generator was doing when she corrected it.
    """
    # One given name: NO ordinal and no usual-forename qualifier.
    #
    # **The ordinal half of this changed on 2026-08-25**, and the test previously required
    # the opposite. Emma, on why she had been running the generated batches only in part:
    # *"they have consistently included things I did not want, such as the series orginal 1
    # on peoples given names when there is only one given name"*. `P1545` *series ordinal*
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

    # Two given names: the first genuinely is the usual one.
    lines, _notes = statements_for("Samuel Oline Garborg", PLAN, "1")
    first = [ln for ln in lines if ln[0] == GIVEN_NAME][0]
    assert ("P7452", USUAL_FORENAME) in first[2]


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


# --- the FIELDS, which is where name objects actually come from ---------------

from namemodel import (  # noqa: E402
    BIRTH_NAME_ROLE, MARRIED_NAME_ROLE, NICKNAME, aliases_for, classify_fields,
)


def usages_of(**fields):
    return [(t, u) for t, u, _o in classify_fields(**fields)]


def test_the_surname_is_read_not_inferred():
    """`SURN` is recorded data. The old parser took the last whitespace token instead.

    Emma, 2026-08-24: *"I thought we were resolving name objects but now we're
    determining which name field to use as a source of the label?"* Agreeing by luck
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
    """Emma's ruling, 2026-08-24: it becomes `P1449` *nickname*.

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
    """Emma, 2026-08-24, and sex is explicitly NOT a screen."""
    differs = usages_of(givn="Stine", surn="Garborg", marnm="Jacobson")
    assert ("Jacobson", "married") in differs
    assert ("Garborg", "family") in differs

    same = usages_of(givn="Eivind", surn="Garborg", marnm="Garborg")
    assert not [t for t, u in same if u == "married"], (
        "_MARNM equal to SURN is the 43% case CLAUDE.md measured — not a second name")


def test_a_married_man_gets_the_married_name_too():
    """Her ruling was explicit: *"only when different sex does not matter"*.

    The corpus measurement suggested screening on sex, because 25% of the differing
    `_MARNM` values are male. She overrode that, and it is her data model.
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
    """None of Emma's eleven items qualifies a family name, so a bare one stays bare."""
    plan = {("Garborg", "family"): ("Q30250555", "link")}
    lines, _notes = statements_for("", plan, "1",
                                   fields={"givn": "Eivind", "surn": "Garborg"})
    assert [q for p, v, q in lines if p == FAMILY_NAME] == [[]]


def test_a_nickname_needs_no_name_item():
    """`P1449` takes text, so a missing plan entry can never block it."""
    lines, _notes = statements_for("", {}, "1",
                                   fields={"givn": 'Stine "Stena"', "surn": "Garborg"})
    assert (NICKNAME, "Stena", []) in lines


def test_aliases_cover_the_nickname_and_the_married_full_name():
    """The nickname alias carries the SURNAME. Emma, 2026-08-26.

    It used to assert the bare `"Stena"`, and she overruled that on seeing `Q141189102`
    *Sigrid "Sally" Manilva Tunheim* get an alias of `Sally`: *"this person was given an
    alias of 'Sally' instead of 'Sally Ekman'"*. A bare given-name token is not something
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


def test_a_mans_marnm_family_name_carries_no_married_role():
    """Emma, 2026-08-24, on seeing a man with `Q28418670` *married name*.

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
    exists. The person then gets **no name statement at all** — which is what Emma saw on
    `Q141189052` Anna Carine Gundersen, whose three tokens all failed.

    Measured over `reports/name-item-plan.csv`: **1,051 tokens, 31,259 bearers**, led by
    `Olsen` 1,147, `Pedersen` 678, `Olson` 511, `Hansen` 503, `Andersen` 476, `Larsen` 442.
    **330 of them already carry a Wikidata item** under given/family, covering 12,798
    bearers — and per `CLAUDE.md` § *One name item per USAGE* a patronymic is a **different**
    item, so those cannot simply be linked.

    **FIXED 2026-08-27.** `scripts/build-name-item-batch.py` now emits a patronymic row for a
    `-sen`/`-son` token **as well as** its given/family rows, rather than instead of them.
    That is `CLAUDE.md` § *One name item per USAGE*: a token used two ways gets two items, and
    it is not an ambiguity to resolve. Emma's father test then decides per person which of the
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
    """Emma's test, 2026-08-26, and the literal reading of it is 91% wrong.

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

    assert props("") == [], "with no father the morphological patronymic has no item yet"
    assert props("Gunder Olsen") == [], "stem matches his given name, so still a patronymic"
    assert props("Hans Gundersen") == [(FAMILY_NAME, "Q656767")], (
        "the father carries the same token, so it is an inherited surname")
