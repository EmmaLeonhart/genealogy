"""The channel for a label EMMA DICTATES, `reports/label-applications.tsv`.

**What is worth pinning is that her value is the one that lands.** A hand row is usually
correcting a value the rule wrote earlier, so the derived emitters go on proposing their own
version of the same slot — and a derived edit emitted beside hers is applied second and silently
wins, in a batch that reads as though her correction went out.

The other half is the format's own hazard: it could carry a `D` row, and `CLAUDE.md` § *NO
descriptions and NO edit summaries* is categorical.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _bgd():
    sys.path.insert(0, str(ROOT / "src"))
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location("bgd", ROOT / "scripts" / "build-garborg-day.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write(tmp_path, body):
    p = tmp_path / "label-applications.tsv"
    p.write_text("qid\tkind\tlang\tvalue\tsource\tdate\tnote\n" + body, encoding="utf-8")
    return p


def test_the_shipped_file_parses_and_emits_verbatim():
    mod = _bgd()
    rows = mod.hand_label_applications()
    assert ("Q140568870", "L", "zh", "李命玥", rows[0][4]) == rows[0]
    lines = mod._hand_label_applications(live_labels={})
    # Exactly what she wrote, with no transliteration, no title rule and no consensus vote.
    assert 'Q140568870\tLzh\t"李命玥"' in lines
    assert 'Q140568870\tLja\t"エマ・レオンハート"' in lines
    assert 'Q140568870\tAja\t"閻魔獅心"' in lines
    assert 'Q140568870\tLko\t"엠마 레온하트"' in lines


def test_a_description_row_is_refused(tmp_path):
    mod = _bgd()
    path = _write(tmp_path, "Q1\tD\ten\tsomething\tEmma\t2026-09-08\t\n")
    assert mod.hand_label_applications(path) == []


def test_a_malformed_row_is_refused_rather_than_repaired(tmp_path):
    mod = _bgd()
    body = ("Q2\tL\ten\tsay \"hi\"\tEmma\t2026-09-08\t\n"     # QS V1 cannot carry the quote
            "notaqid\tL\ten\tv\tEmma\t2026-09-08\t\n"
            "Q3\tL\tENGLISH\tv\tEmma\t2026-09-08\t\n"
            "Q4\tL\ten\t\tEmma\t2026-09-08\t\n")
    assert mod.hand_label_applications(_write(tmp_path, body)) == []


def test_a_label_already_live_is_skipped_and_an_alias_is_not(tmp_path):
    mod = _bgd()
    path = _write(tmp_path, "Q7\tL\tja\tテスト\tEmma\t2026-09-08\t\n"
                            "Q7\tA\tja\tテスト\tEmma\t2026-09-08\t\n")
    # `read_live_labels()` is keyed on the (qid, lang) PAIR.
    lines = mod._hand_label_applications({("Q7", "ja"): "テスト"}, path)
    assert 'Q7\tLja\t"テスト"' not in lines          # a label REPLACES; it already says this
    assert 'Q7\tAja\t"テスト"' in lines              # an alias ADDS, and live aliases are unknown


def test_a_derived_edit_for_a_slot_she_sets_by_hand_is_dropped():
    mod = _bgd()
    covered = mod._hand_covered_slots(['Q1\tLja\t"hers"', 'Q1\tAja\t"her alias"'])
    assert covered == {("Q1", "Lja")}               # an alias is not covered: it adds
    derived = ["#   Q1: set the ja label", 'Q1\tLja\t"ours"',
               "#   Q1: an alias", 'Q1\tAja\t"ours"',
               "#   Q2: set the ja label", 'Q2\tLja\t"someone else"']
    kept = mod._without_hand_covered(derived, covered)
    assert 'Q1\tLja\t"ours"' not in kept
    assert "#   Q1: set the ja label" not in kept   # the comment goes with the edit it names
    assert 'Q1\tAja\t"ours"' in kept
    assert 'Q2\tLja\t"someone else"' in kept
