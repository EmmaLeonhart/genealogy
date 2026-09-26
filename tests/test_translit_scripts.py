"""`scripts/translit_scripts.py` -- the sixteen standardized-label scripts.

The standard, from the module: letter for letter from the Latin form, nothing looked up. A
transcription a native reader would spell differently is acceptable; a different name is not.
These pin the shape each script must have, not a spelling.
"""
from __future__ import annotations

import sys
import unicodedata
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from translit_scripts import SCRIPTS, render  # noqa: E402

#: The Unicode script name every letter of a code's output must carry.
SCRIPT_OF = {
    "ru": "CYRILLIC", "uk": "CYRILLIC", "el": "GREEK", "hi": "DEVANAGARI", "ar": "ARABIC",
    "fa": "ARABIC", "bn": "BENGALI", "he": "HEBREW", "ta": "TAMIL", "chr": "CHEROKEE",
    "iu": "CANADIAN SYLLABICS", "am": "ETHIOPIC", "dv": "THAANA", "hy": "ARMENIAN",
    "ka": "GEORGIAN", "zgh": "TIFINAGH",
}
NAMES = ["Arne Garborg", "Maria Elisabet Wærn", "Christina Johansdotter", "Bjørn Åsulvsson",
         "Yngve Sylvia", "Ole Olsen Nesheim"]


def test_all_sixteen_are_registered():
    assert set(SCRIPTS) == set(SCRIPT_OF)


@pytest.mark.parametrize("code", sorted(SCRIPT_OF))
@pytest.mark.parametrize("name", NAMES)
def test_every_word_comes_out_whole_and_in_its_own_script(code, name):
    got = render(name, code)
    assert len(got.split()) == len(name.split()), (code, name, got)
    for ch in got:
        if ch.isspace() or ch == "'" or unicodedata.category(ch).startswith("M"):
            continue
        assert SCRIPT_OF[code] in unicodedata.name(ch, ""), (code, name, got, ch)


def test_georgian_is_never_upper_cased_into_mtavruli():
    assert render("Arne", "ka") == "არნე"


def test_a_vowel_y_is_not_the_tifinagh_glide():
    assert render("Yngve", "zgh").startswith("ⵉ")


def test_hebrew_takes_final_forms():
    assert render("Jon", "he").endswith("ן")
