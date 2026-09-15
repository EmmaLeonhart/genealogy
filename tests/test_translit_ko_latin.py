"""Latin names into Hangul, and the `ng` that went missing from 126 of them.

`scripts/translit_ko_latin.py` had no test file at all, which is how a defect this visible --
`Inger` rendering as 이에르 -- survived in 127 live labels until Emma read four items and said
*"I think the -datter words might be systematically messed up."*

Loaded by path; the module lives in `scripts/`, which is not a package.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def ko():
    sys.path.insert(0, str(REPO / "scripts"))
    import translit_ko_latin

    return translit_ko_latin


# ---------------------------------------------------------------------------------------
# The `ng` before a vowel. Ruled 2026-09-15, queue.md § *Questionable cjk-izations*.
# ---------------------------------------------------------------------------------------

#: `(name, hangul)` -- the cases that were wrong, from `reports/cjk-korean-dropped-ng.csv`.
NG_BEFORE_VOWEL = [
    ("Inger", "잉에르"),
    ("Bunge", "붕에"),
    ("Stangaland", "스탕아란드"),
    ("Tengesdal", "텡에스달"),
    ("Ingeborg", "잉에보륵"),
    ("Hakunge", "하쿵에"),
]

#: These were ALREADY right, and they are the proof the table was never the problem: here the
#: `ng` is followed by a consonant or by nothing, so the general rule put it in the final slot
#: on its own. A fix that "helps" these has changed something it should not have.
NG_ALREADY_CORRECT = [
    ("Ingrid", "잉리드"),
    ("Lang", "랑"),
    ("Long", "롱"),
]


@pytest.mark.parametrize("name,want", NG_BEFORE_VOWEL)
def test_ng_before_a_vowel_keeps_the_nasal(ko, name, want):
    """⛔ Korean has no `ng` ONSET, so a following vowel used to strand it entirely.

    A consonant followed by a vowel normally becomes the next syllable's initial rather than
    this one's final -- `Peter` is 피터, not 핏어. But `ng` is not in `_I` at all: ㅇ in initial
    position is silent. So the general rule gave `ng` neither slot and it vanished.

    **127 of the 225 `ko` labels whose name contains `ng` had lost it.**
    """
    assert ko.render_word(name) == want


@pytest.mark.parametrize("name,want", NG_ALREADY_CORRECT)
def test_ng_elsewhere_is_untouched(ko, name, want):
    """The fix is about PLACEMENT and must not widen. These already worked."""
    assert ko.render_word(name) == want


def test_the_final_slot_test_is_written_once(ko):
    """⛔ § *A GUARD IN ONE EMITTER IS NOT A GUARD* -- the test was inline five times.

    `render_word` spelled out `c in _CAN_BE_FINAL and not (after and after[0] == "V")` in five
    branches. Five copies of one rule is how a sixth branch added later comes to disagree with
    the other five, so the rule is now `_takes_final_slot` and the branches call it.
    """
    source = (REPO / "scripts" / "translit_ko_latin.py").read_text(encoding="utf-8")
    body = source[source.index("def render_word("):]
    assert 'c in _CAN_BE_FINAL and not (after' not in body, (
        "the final-slot test is inline again; it belongs in _takes_final_slot")
    assert body.count("_takes_final_slot(c, after)") >= 5


def test_ng_takes_the_final_slot_whatever_follows(ko):
    """The rule itself, directly: `ng` is the one consonant a vowel cannot steal."""
    assert ko._takes_final_slot("ng", ("V", "e"))
    assert ko._takes_final_slot("ng", None)
    # and the general rule is unchanged for everything else
    assert not ko._takes_final_slot("n", ("V", "e"))
    assert ko._takes_final_slot("n", ("C", "t"))
    assert not ko._takes_final_slot("t", ("V", "e"))


# ---------------------------------------------------------------------------------------
# Regressions: cases the module's own docstrings name as correct.
# ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("name,want", [
    # The epenthetic 으 on a trailing consonant -- the module docstring's worked example.
    ("Garborg", "가르보륵"),
    # A stop before a liquid does NOT take the final slot: 시그리드, never 식리드.
    ("Sigrid", "시그리드"),
    # `ts` is a patronymic boundary, not the affricate: 크누트손, never 크누촌.
    ("Knutsson", "크누트손"),
    ("Mattsson", "마트손"),
    # A branch that used to drop the final slot entirely: 아드윈, not 아드위느.
    ("Adwin", "아드윈"),
])
def test_the_documented_renderings_still_hold(ko, name, want):
    assert ko.render_word(name) == want
