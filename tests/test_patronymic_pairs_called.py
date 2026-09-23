"""Patronymics must be created in gendered pairs — the caller must exist."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / ".github" / "workflows" / "pipeline.yml"


def test_pipeline_or_name_items_calls_a_patronymic_pair_builder():
    """Ruled 2026-09-21: male and female patronymics are made together as pairs.

    `scripts/build-patronymic-items.py` and `scripts/build-patronymic-pairs.py` exist;
    § *Code that is WRITTEN but never CALLED is not done*. Narrow search over
    workflows + the name-items composer only (never the corpus).
    """
    pipeline = PIPELINE.read_text(encoding="utf-8") if PIPELINE.exists() else ""
    name_items = (ROOT / "scripts" / "build-garborg-name-items.py")
    name_txt = name_items.read_text(encoding="utf-8") if name_items.exists() else ""
    needles = (
        "build-patronymic-items.py",
        "build-patronymic-pairs.py",
        "wikidata-patronymic-pairs.qs",
    )
    hit = any(n in pipeline or n in name_txt for n in needles)
    called = (
        "python scripts/build-patronymic-items.py" in pipeline
        or "python scripts/build-patronymic-pairs.py" in pipeline
        or ("build-patronymic-pairs.py" in name_txt and "P5278" in name_txt and "emit" in name_txt.lower())
    )
    assert called or (hit and "python scripts/build-patronymic" in pipeline), (
        "pipeline.yml (or the name-items composer) must invoke "
        "build-patronymic-items.py or build-patronymic-pairs.py so P5278 pairs "
        "actually leave the repo. Measured: name-items batch had zero P5278."
    )
