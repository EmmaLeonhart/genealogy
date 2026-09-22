"""The `NN` descriptive label: which relative names the person, and whose name survives.

`docs/rules/names.md` § *The NN/Private label algorithm applies to EVERY unnamed person* is the
spec, and `scripts/build-nn-label-batch.py` is the one emitter of the prose form. Two rulings of
2026-09-09 are pinned here because both were wrong in the shipped code and both are silent
failures — a label that reads perfectly well and names the wrong thing.

**The worked case is `Q141403481`.** It went live reading `husband of Gölug` when his daughter
Malin was sitting in the same graph, and the right English is **`Andreas father of Malin`**.

Loaded by path; the script's name has hyphens in it and is not importable.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def nn():
    spec = importlib.util.spec_from_file_location(
        "build_nn_label_batch", str(REPO / "scripts" / "build-nn-label-batch.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- which relative names the person -------------------------------------------------


def test_the_search_order_is_father_mother_spouse_child(nn):
    """⛔ Ruled 2026-09-15, superseding the 2026-09-09 child-first order this used to pin.

    Emma wrote the precedence out as a list -- Father, Mother, Spouse, Child -- with the
    reason: *"child and spouse both can mean multiple people. Parents are the most stable
    identifiers. Father is generally most stable"*. **Cardinality is the argument**, and the
    superseded one never addressed it: a person has at most one father and one mother and may
    have any number of children and spouses, so *father of Malin* identifies a man only if
    Malin is his only child.

    The 2026-09-09 ruling that stood here is not deleted from the record -- it is in
    `nearest`'s own docstring, marked superseded -- but a test may only pin what is current,
    and a revert to child-first fails here.

    Read off the source, because the order lives in a tuple inside a closure and there is no
    other way to reach it.
    """
    source = (REPO / "scripts" / "build-nn-label-batch.py").read_text(encoding="utf-8")
    block = source[source.index("def nearest("):]
    block = block[:block.index("# **The long-range pass.**")]
    seen = [key for key in re.findall(r'\("(\w+_of)",', block)]
    assert seen[:4] == ["child_of", "spouse_of", "parent_of", "sibling_of"], seen


def test_all_three_emitters_of_a_description_agree_on_the_order(nn):
    """⛔ § *A GUARD IN ONE EMITTER IS NOT A GUARD*, and here there are three.

    `build-nn-label-batch.nearest`, `build-garborg-day.describe_all` and
    `build-orderlife-batch._describe_from_relatives` all pick a relative to name somebody by,
    and on 2026-09-15 they disagreed: two had parents first and this one had been inverted to
    children on 2026-09-09. One model, three emitters, drifted apart exactly as the rule
    predicts. Parents before spouse before child, in all three.
    """
    day = (REPO / "scripts" / "build-garborg-day.py").read_text(encoding="utf-8")
    block = day[day.index("    BY = (("):]
    block = block[:block.index(chr(10) + chr(10))]
    assert [k for k in re.findall(r'\("(\w+_of)"', block)] == [
        "child_of", "spouse_of", "parent_of", "sibling_of"], block

    life = (REPO / "scripts" / "build-orderlife-batch.py").read_text(encoding="utf-8")
    seq = re.search(r'for relation, table in \((.*?)\):', life, re.S).group(1)
    assert [k for k in re.findall(r'"(\w+)"', seq)] == ["parent", "spouse", "child"], seq


def test_the_father_is_preferred_over_the_mother(nn):
    """*"NN people with a mother and a father always get it from their father"* -- 2026-09-15.

    `FATHER` before `MOTHER` inside the parent step was already how the tuple happened to be
    typed; this makes it the ruled behaviour rather than an accident, in both emitters.
    """
    for name in ("build-nn-label-batch.py", "build-garborg-day.py"):
        source = (REPO / "scripts" / name).read_text(encoding="utf-8")
        assert re.search(r"FATHER.*MOTHER|father\.get\(geni_id\), mother\.get\(geni_id\)",
                         source), name


def test_the_relation_keys_mean_what_the_order_says(nn):
    """`parent_of` means *this person is the parent of X*, so its candidates are the CHILDREN.

    The naming is the trap: `child_of` sounds like children and means parents. If these two
    are ever swapped the order test above passes while the behaviour inverts.
    """
    source = (REPO / "scripts" / "build-nn-label-batch.py").read_text(encoding="utf-8")
    assert '("parent_of", targets(ent, CHILD))' in source
    assert '("child_of", targets(ent, FATHER) + targets(ent, MOTHER))' in source


def test_every_language_has_a_word_for_all_six_relations(nn):
    """A missing key would raise at emit time, on one language, for one person."""
    relations = ("child_of", "spouse_of", "parent_of", "sibling_of",
                 "grandchild_of", "grandparent_of")
    for lang, words in nn.WORDS.items():
        for relation in relations:
            assert relation in words, f"{lang} has no {relation}"
            table = words[relation]
            assert table.get("") or table.get("M"), f"{lang}/{relation} has no neutral form"


def test_unknown_sex_takes_the_neutral_word_and_never_a_guess(nn):
    """Inventing a gender to make a label read better is unrequested normalisation."""
    for lang, words in nn.WORDS.items():
        assert words["parent_of"][""], f"{lang} has no neutral parent word"
    assert nn.WORDS["en"]["parent_of"][""] == "parent"
    assert nn.WORDS["en"]["parent_of"]["M"] == "father"


# --- whose name survives -------------------------------------------------------------


def test_a_given_name_in_mul_is_recovered(nn):
    """⛔ `Andreas father of Malin`, not `father of Malin`. His given name IS known and only
    the surname is missing, so a bare clause throws away the one thing the record says."""
    assert nn.GIVEN_WITH_MARKER.match("Andreas NN").group(1) == "Andreas"
    assert nn.GIVEN_WITH_MARKER.match("Sigrid NN").group(1) == "Sigrid"
    assert nn.GIVEN_WITH_MARKER.match("Maria N. N.").group(1) == "Maria"


def test_a_bare_marker_yields_no_name(nn):
    """The fully unnamed person. The clause stays bare, which is correct for them."""
    for bare in ("NN", "N.N.", "N. N.", "  nn  "):
        assert nn.NN_LABEL.match(bare), bare
        assert not nn.GIVEN_WITH_MARKER.match(bare), bare


def test_a_leading_marker_is_not_a_given_name(nn):
    """⛔ `NN Garborg` is the OTHER half of the protocol -- surname known, given name missing.

    If it matched here the SURNAME would be emitted as though it were a given name, producing
    `Garborg father of Malin`. The two forms are mirrors and must not collapse into each other.
    """
    for surname_form in ("NN Garborg", "NN Andersson", "N.N. Skjelbrei"):
        assert not nn.GIVEN_WITH_MARKER.match(surname_form), surname_form


def test_a_real_name_is_never_touched(nn):
    """Neither pattern may match somebody who simply has a name."""
    for real in ("Ann Bincks", "Arne Garborg", "Malin Andersdotter"):
        assert not nn.GIVEN_WITH_MARKER.match(real), real
        assert not nn.NN_LABEL.match(real), real


def test_the_clause_is_built_from_the_recovered_name(nn):
    """The assembled English, end to end, for the worked case.

    ⛔ **THE SEPARATOR IS A COMMA, CHANGED 2026-09-21**: `Andreas, father of Malin`. This
    test pinned a bare space from 2026-09-09, and the `Tora NN` ruling reversed it -- the
    assertion moved with the rule rather than being left to fail. The half that was never in
    question is the ORDER: the person's own name comes first, because a label that is only a
    relation names the relative.
    """
    from namemodel import lead_with_given_name
    word = nn.WORDS["en"]["parent_of"]["M"]
    joiner = nn.WORDS["en"]["of"]
    clause = nn._join(word, joiner, "Malin")
    assert clause == "father of Malin"
    given = nn.GIVEN_WITH_MARKER.match("Andreas NN").group(1)
    assert lead_with_given_name(given, clause, "en") == "Andreas, father of Malin"


def test_the_emitter_actually_uses_the_recovered_name(nn):
    """⛔ *Code that is WRITTEN but never CALLED is not done.* The value must be the prefixed
    clause and not the bare join."""
    source = (REPO / "scripts" / "build-nn-label-batch.py").read_text(encoding="utf-8")
    assert "GIVEN_WITH_MARKER.match(value(\"mul\")" in source
    assert '"value": clause}' in source
    # ⛔ And it goes through the MODEL, so the two emitters cannot drift apart again.
    assert "lead_with_given_name(known.group(1).strip(), clause, lang)" in source
