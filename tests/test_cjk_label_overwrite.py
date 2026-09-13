"""A CJK label this pipeline never wrote is somebody else's and it stands.

**Reported 2026-09-12 on `Q45383466`**, Zhu Cao, a Tang-dynasty Chinese man. Emma: *"Look at
the shit that you did to this profile oh my god you bastard this is unacceptable"*.

The batch of 06:13 that morning replaced `朱操` — his name in Han characters, put there by
another editor in 2022 — with:

    Lja  ズフ・カオ      katakana of the Latin romanisation
    Lzh  兹胡·卡奥      Mandarin phonetic transcription of the Latin romanisation
    Lmul Zhu Cao

His son `Q11094143` `朱敬則` was in the same batch. The values were not wrong as
transliterations; they were transliterations of a romanisation of a name the item already
held correctly, in the very languages that name belongs to.

**The 2026-08-30 ruling that turned the CJK overwrite on is not reversed here.** It rests on
one premise — *"we wrote essentially all of them"* — and these tests are that premise made
into a per-item test rather than an assumption over the population.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location(
    "garborg_day", REPO / "scripts" / "build-garborg-day.py")
_day = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_day)

OURS = {("Q100", "Lja"), ("Q100", "Lzh")}


def test_a_label_we_never_emitted_is_not_overwritten():
    """The reported case, with its own values."""
    assert not _day.may_write_cjk_label(
        "Q45383466", "ja", "朱操", "ズフ・カオ", OURS)
    assert not _day.may_write_cjk_label(
        "Q45383466", "zh", "朱操", "兹胡·卡奥", OURS)


def test_a_label_we_did_emit_is_still_overwritten():
    """The 2026-08-30 ruling, which this must not break: a rule fix reaches our own labels."""
    assert _day.may_write_cjk_label("Q100", "ja", "モルクク", "モルク", OURS)


def test_an_empty_language_is_filled():
    """Nothing is being taken away, so there is nothing to protect."""
    assert _day.may_write_cjk_label("Q45383466", "ko", None, "주 카오", OURS)


def test_agreement_is_allowed_through_and_the_caller_drops_it():
    """`live == value` is a no-op the caller skips; the guard must not be what stops it."""
    assert _day.may_write_cjk_label("Q45383466", "ja", "朱操", "朱操", OURS)


def test_the_ledger_reader_keys_on_qid_and_slot_only():
    """Not on the value — see `_cap_label_edits`, which keys on the value for a different job."""
    ours = _day.cjk_slots_we_have_emitted()
    assert all(len(k) == 2 and k[1] in ("Lja", "Lzh", "Lko") for k in ours)
