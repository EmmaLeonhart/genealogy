"""The day-batch composer must drop Tanba lines entirely — never comment them out."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "scripts" / "build-garborg-day.py"


def test_tanba_gate_import_or_inline_present():
    text = BUILD.read_text(encoding="utf-8")
    assert (
        "from tanba_batch_block import tanba_blocked_qids" in text
        or "def tanba_blocked_qids(" in text
    ), "build-garborg-day.py must load tanba_blocked_qids (import or inline)"


def test_tanba_gate_drops_comment_lines():
    text = BUILD.read_text(encoding="utf-8")
    assert 'if "tanba" in line.lower():' in text, (
        "names_excluded must treat any line containing 'tanba' as excluded, "
        "including annotation comments — never leave a # CREATE/LAST wall"
    )


def test_tanba_qids_in_excluded_set():
    text = BUILD.read_text(encoding="utf-8")
    assert "tanba_blocked_qids()" in text
    assert "excluded" in text


def test_usable_rejects_given_nn_token():
    text = BUILD.read_text(encoding="utf-8")
    assert "single_word" in text or "tokens = low.replace" in text, (
        "usable() must reject Given-NN relatives (Margreta NN), not only NN-prefix shapes"
    )
