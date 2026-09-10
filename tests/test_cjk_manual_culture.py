"""A hand assignment outranks every tier of the CJK culture classifier.

`reports/cjk-culture-manual.tsv` is filled from the CJK culture queue — the artifact that shows a
person's CJK name beside their romanised relatives and asks which reading language applies. The
classifier refused 1,270 people; 137 of them have a romanised relative to judge from.

**The ordering is the whole point of these tests.** Every evidence tier writes into one `culture`
dict, and evidence 2 overwrites unconditionally on the stated grounds that character facts
outrank family inference. A hand verdict applied before that is silently overruled and still
looks honoured, so it is applied last — and that is what these pin.

Loaded by path; the script's name has hyphens in it and is not importable.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def cjk():
    sys.path.insert(0, str(REPO / "scripts"))
    spec = importlib.util.spec_from_file_location(
        "build_cjk_romanisation", str(REPO / "scripts" / "build-cjk-romanisation.py"))
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except SystemExit:
        pass
    return module


NEED = {"g1": "磐之媛命", "g2": "高野新笠", "g3": "敦実親王"}


def test_a_hand_verdict_overrules_the_classifier(cjk):
    """⛔ The number that matters: the classifier was confident and wrong."""
    culture, why, unsettled = {"g1": "zh"}, {}, {}
    assigned, skipped, overruled = cjk._apply_manual_culture(
        NEED, culture, why, unsettled, {"g1": "ja"})
    assert culture["g1"] == "ja"
    assert (assigned, skipped, overruled) == (1, 0, 1)
    assert "by hand" in why["g1"]


def test_agreement_is_not_counted_as_an_overrule(cjk):
    """`overruled` is the classifier's error rate on its hardest cases, so agreement must not
    inflate it."""
    culture, why, unsettled = {"g1": "ja"}, {}, {}
    assigned, _skipped, overruled = cjk._apply_manual_culture(
        NEED, culture, why, unsettled, {"g1": "ja"})
    assert (assigned, overruled) == (1, 0)


def test_an_unassigned_person_is_filled_in(cjk):
    culture, why, unsettled = {}, {}, {"g2": "no evidence reached this person"}
    assigned, _s, overruled = cjk._apply_manual_culture(
        NEED, culture, why, unsettled, {"g2": "ko"})
    assert culture["g2"] == "ko"
    assert (assigned, overruled) == (1, 0)
    assert "g2" not in unsettled, "a settled person must stop being listed as unsettled"


def test_skip_assigns_nothing_and_discards_nothing(cjk):
    """⛔ *Looked and could not tell* is not a culture, and it is not a reason to throw away what
    the classifier concluded either. It only stops the row reading as unreviewed."""
    culture, why, unsettled = {"g3": "zh"}, {}, {}
    assigned, skipped, overruled = cjk._apply_manual_culture(
        NEED, culture, why, unsettled, {"g3": "skip"})
    assert culture["g3"] == "zh", "skip must not wipe a classifier verdict"
    assert (assigned, skipped, overruled) == (0, 1, 0)

    culture, why, unsettled = {}, {}, {}
    cjk._apply_manual_culture(NEED, culture, why, unsettled, {"g3": "skip"})
    assert "g3" not in culture
    assert "could not tell" in unsettled["g3"]


def test_somebody_outside_the_population_is_ignored(cjk):
    """The file outlives any one run; a person who is no longer CJK-named is not resurrected."""
    culture, why, unsettled = {}, {}, {}
    assigned, skipped, _o = cjk._apply_manual_culture(
        NEED, culture, why, unsettled, {"someone-else": "ja"})
    assert (assigned, skipped) == (0, 0)
    assert culture == {}


def test_only_the_four_verdicts_are_accepted(cjk, tmp_path):
    """A typo in the file must not become a language code on Wikidata."""
    path = tmp_path / "manual.tsv"
    path.write_text(
        "geni_id\tculture\tcjk\tdecided_at\n"
        "g1\tja\t磐之媛命\t2026-09-10\n"
        "g2\tJapanese\t高野新笠\t2026-09-10\n"
        "g3\tskip\t敦実親王\t2026-09-10\n"
        "g4\t\t某\t2026-09-10\n",
        encoding="utf-8", newline="")
    loaded = cjk._load_manual_culture(path)
    assert loaded == {"g1": "ja", "g3": "skip"}


def test_an_absent_file_is_not_an_error(cjk, tmp_path):
    """Nothing reviewed yet is the normal state, not a failure."""
    assert cjk._load_manual_culture(tmp_path / "nothing-here.tsv") == {}


def test_the_file_exists_with_the_four_columns():
    """The committed file, because the pipeline reads it every run."""
    path = REPO / "reports" / "cjk-culture-manual.tsv"
    assert path.exists(), "the hand-assignment file must exist for the pipeline to read"
    header = path.read_text(encoding="utf-8").splitlines()[0]
    assert header.split("\t") == ["geni_id", "culture", "cjk", "decided_at"]


def test_the_pipeline_actually_calls_it():
    """⛔ *Code that is WRITTEN but never CALLED is not done.*"""
    source = (REPO / "scripts" / "build-cjk-romanisation.py").read_text(encoding="utf-8")
    assert "_apply_manual_culture(" in source.split("def _apply_manual_culture")[-1], \
        "the override is defined but never invoked"
