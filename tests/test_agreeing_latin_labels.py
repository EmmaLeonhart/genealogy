"""Agreeing Latin labels become the `mul` label. Ruled *"the most important labelling thing"*.

Where an item has no `mul` and several of its own Latin-alphabet labels say the same thing, that
string is the language-neutral label. `Q102010` *Friedrich IV. von Oettingen* carries ten
agreeing labels and no `mul`, which is the case that raised it.

**The source is the ITEM'S OWN LABELS.** It used to be agreeing Geni `NAME` records, and that was
the defect -- ruled 2026-09-09, *"geni names are confusing… we kinda agreed to not do anything
with them"*. The old source reached exactly one person, labelled `(unknown)`, with a null `qid`.

Loaded by path; the script's name has hyphens in it and is not importable.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def agree():
    spec = importlib.util.spec_from_file_location(
        "build_agreeing_latin_labels",
        str(REPO / "scripts" / "build-agreeing-latin-labels.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def labels(**kwargs):
    return {lang: {"value": value} for lang, value in kwargs.items()}


def test_agreeing_languages_give_the_label(agree):
    got = agree.agreement(labels(en="Detlof Heijkenskjöld", nl="Detlof Heijkenskjöld",
                                 sv="Detlof Heijkenskjöld"))
    assert got == ("Detlof Heijkenskjöld", 3, 1)


def test_one_language_is_not_agreement(agree):
    """The `solo` bar: one label agreeing with itself is not evidence."""
    value, count, distinct = agree.agreement(labels(en="Detlof Heijkenskjöld"))
    assert count == 1
    assert count < agree.MIN_LANGUAGES


def test_disagreement_declines_rather_than_voting(agree):
    """⛔ Two attested strings means NO label, not the more frequent one.

    Picking would be the coin-flip the uniqueness rule refuses everywhere else. Measured: 457
    ledger items are declined for exactly this, against 397 that agree.
    """
    _value, _count, distinct = agree.agreement(
        labels(en="Algot Bryniolfsson", nl="Algot Bryniolfsson", sv="Algot Brynolfsson"))
    assert distinct == 2


def test_a_diacritic_is_a_different_name(agree):
    """`CLAUDE.md` § *A diacritic makes a different name*. Case folds; nothing else does."""
    _value, _count, distinct = agree.agreement(labels(en="Maria", nl="María"))
    assert distinct == 2
    value, count, distinct = agree.agreement(labels(en="maria", nl="Maria"))
    assert distinct == 1 and count == 2 and value in ("maria", "Maria")


def test_an_existing_mul_is_never_touched(agree):
    """⛔ Purely additive. `Wikidata's label beats ours` and this cannot overwrite a hand-edit."""
    assert agree.agreement(labels(mul="Andreas NN", en="Andreas", nl="Andreas")) is None


def test_a_non_latin_label_does_not_count(agree):
    """The rule is explicitly about the Latin alphabet, and a mixed string is not one."""
    assert not agree.is_latin("徳川家康")
    assert not agree.is_latin("Gerard Spencerの娘")
    assert agree.is_latin("Detlof Heijkenskjöld")
    value, count, _ = agree.agreement(
        labels(en="Anna Snakenborg", nl="Anna Snakenborg", ja="アンナ"))
    assert (value, count) == ("Anna Snakenborg", 2)


def test_markers_never_reach_mul(agree):
    """`mul` is the language-neutral REAL name. The NN protocol owns the unnamed and puts the
    marker there deliberately; nothing may arrive there by this route instead."""
    for marker in ("NN", "N.N.", "unknown", "(unknown)", "private", "?", "Ukjent"):
        assert agree.MARKER.match(marker), marker
    assert agree.agreement(labels(en="unknown", nl="unknown")) is None


def test_a_real_name_is_not_a_marker(agree):
    for name in ("Anna Snakenborg", "Private Smith", "Unknown Wife of Brand"):
        assert not agree.MARKER.match(name), name


def test_whitespace_folds(agree):
    value, count, distinct = agree.agreement(labels(en="Anna  Snakenborg", nl="Anna Snakenborg"))
    assert distinct == 1 and count == 2
    assert value == "Anna Snakenborg"


def test_the_rebuild_actually_calls_it(agree):
    """⛔ *Code that is WRITTEN but never CALLED is not done.* It was called by nothing at all --
    not the rebuild, not a workflow, not the batch builder -- for eight days."""
    source = (REPO / "scripts" / "rebuild-everything.py").read_text(encoding="utf-8")
    assert "build-agreeing-latin-labels.py" in source


def test_it_emits_mul_and_not_en(agree):
    """`en` absent is a gap in English; `mul` absent on an item ten languages agree about is the
    language-neutral label missing. The old version wrote both and they are different claims."""
    source = (REPO / "scripts" / "build-agreeing-latin-labels.py").read_text(encoding="utf-8")
    assert '"language": "mul"' in source
    assert '"language": "en"' not in source
