"""Composed labels go into the batch for the switched languages, and only into empty slots.

Label composition from the name items (queue, Emma's ruling 2026-09-27: strictly); `en` switched
first. A composed label never overwrites a live one somebody wrote.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
spec = importlib.util.spec_from_file_location("bgd_composed", ROOT / "scripts" / "build-garborg-day.py")
bgd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bgd)


def test_composed_en_fills_only_empty_slots(tmp_path, monkeypatch):
    tsv = tmp_path / "composed.tsv"
    tsv.write_text("qid\tlang\tcomposed\tlive\n"
                   "Q1\ten\tAnders Nilsson\t\n"
                   "Q2\ten\tEfraim Wilhelm\tEfraim Wilhelm Otto\n"
                   "Q3\tja\tアンデシュ\t\n", encoding="utf-8")
    monkeypatch.setattr(bgd, "COMPOSED_LABELS_OUT", tsv)
    lines = [ln for ln in bgd._composed_labels_fill() if ln.startswith("Q")]
    assert lines == ['Q1\tLen\t"Anders Nilsson"']
