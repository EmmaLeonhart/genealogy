"""No emitter may write a marker into a label slot.

queue.md carried this as a known defect: `build-edit-objects.py` wrote labels *"with
no marker guard, at both of its emission sites"*, and it was survivable only because
its output is `out/wikidata/edits.json`, which is gitignored and fires nothing. The
instruction attached to it was **fix it before anything reads that file**.

The same fault had already been found and fixed once, in `walk-structural-merge.py`'s
`ja`/`zh` branch, where 22 edits carried `未知` — Chinese for *unknown* — as a Japanese
and Chinese label. Two scripts, six label emission sites, one predicate needed at all
of them, and it existed at four. **A predicate copied per caller is a predicate that
will disagree with itself**, so `labels.is_marker_label` is now the single definition
and every site calls it.

What is pinned here is that rule, not any script's output. The corpus grows daily and
the counts move; a marker being a name never becomes acceptable.

Emma's rulings this rests on:

* 2026-08-16 — *"NN is always preserved in the multi-language label… no local language
  should have it."*
* 2026-08-18 — *"Ukjent and 未知 get the mul NN treatment"*, meaning `NN` in `mul` and a
  descriptive label elsewhere, never the marker itself in a local slot.
* `CLAUDE.md` — *"'Private' is a redaction marker, not a name, and an item labelled
  that asserts something false while being impossible to find."*
* 2026-08-17 — **words yes, punctuation no** for the leading-marker test, so a stray
  dot before a real surname is a typo and not a claim that the name is unknown.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"

sys.path.insert(0, str(SCRIPTS))
import labels as _labels  # noqa: E402


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_"), SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


#: Every spelling that has actually reached, or nearly reached, a label slot.
#: `未知` is the one that produced 22 live edits; `Private` is the redaction marker;
#: `Ukjent` is the Norwegian one Emma named in the same breath as `未知`.
MARKERS = ["NN", "N.N.", "nn", "Private", "<private>", "未知", "Ukjent",
           "unknown", "? ?", "NN .", "-", ".", "N"]

#: Labels that merely *look* marker-ish and must survive, because the surname after
#: the marker is real data — 3,605 surnames ride on this, per `CLAUDE.md`.
NOT_MARKERS = ["Maria Andersen", ". Weill", "Nechama (?) Heller",
               "George Clark, II - farmer", "? binti Pg Seri Lela",
               ". Bagration-Davitashvili", "Anon", "子"]


def test_the_marker_vocabulary_is_recognised():
    for text in MARKERS:
        assert _labels.is_marker_label(text), f"{text!r} should read as a marker"


def test_a_real_name_is_not_a_marker_because_of_its_punctuation():
    for text in NOT_MARKERS:
        assert not _labels.is_marker_label(text), f"{text!r} is a name, not a marker"


def test_a_leading_marker_does_not_make_the_surname_disappear():
    """`NN Hildesheim` is a marker *label* and `Hildesheim` is still real.

    The predicate says True — the label must not go into a local language — and the
    surname is kept by the NN pipeline, which writes `NN` to `mul` and a descriptive
    label elsewhere. Both halves matter, so both are stated here.
    """
    assert _labels.is_marker_label("NN Hildesheim")
    assert "hildesheim" not in _labels.PLACEHOLDER_FORMS


def test_walk_structural_merge_and_build_edit_objects_share_one_predicate():
    """Not a style check. The defect this file exists for was two callers disagreeing.

    `walk-structural-merge.py` kept its own copy and `build-edit-objects.py` had
    none; when `未知` was added to the vocabulary, only the callers that consulted
    the vocabulary picked it up.
    """
    walk = _load("walk-structural-merge")
    build = _load("build-edit-objects")
    for text in MARKERS + NOT_MARKERS:
        expected = _labels.is_marker_label(text)
        assert walk.is_placeholder_label(text) is expected, text
        assert build.is_marker(text) is expected, text


def test_build_edit_objects_drops_a_marker_from_every_label_slot():
    """Exercised through `label_slots`, the function both emission sites now call.

    The guard merely *existing* is not the property worth pinning — it existed in
    `walk-structural-merge.py` while the sibling branch two lines below went without
    it. So this calls the real function with real marker rows and asserts the slots
    come back empty, which fails if any site stops filtering.
    """
    build = _load("build-edit-objects")
    for marker in MARKERS:
        assert build.label_slots({"label_en": marker, "cjk_names": ""}) == {}, marker
        assert build.label_slots({"label_en": "", "cjk_names": marker}) == {}, marker
        # and a marker in one column must not drag the other down with it
        mixed = build.label_slots({"label_en": "Maria Andersen", "cjk_names": marker})
        assert mixed == {"en": "Maria Andersen", "mul": "Maria Andersen"}, marker


def test_build_edit_objects_still_emits_a_real_name_in_all_four_slots():
    """The guard must not be so eager that it empties the legitimate case."""
    build = _load("build-edit-objects")
    slots = build.label_slots({"label_en": "Maria Andersen", "cjk_names": "田中花子 | x"})
    assert slots == {"en": "Maria Andersen", "mul": "Maria Andersen",
                     "ja": "田中花子", "zh": "田中花子"}
