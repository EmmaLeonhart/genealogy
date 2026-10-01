"""Court ranks (P14005) on people: the universe until 2027-06-01, anyone from then.

Emma, 2026-09-26 (the court-rank handoff item): the ranks go on people within the universe, and
*"from 2027-06-01, anyone becomes fair game ... Build that date switch in with a test on both
sides."* The generator came from shintowiki-scripts (`court-rank/README.md`).
"""
from __future__ import annotations

import datetime
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import wikidata_lockout  # noqa: E402


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gen = _load("court_rank_gen", ROOT / "court-rank" / "generate_court_rank_quickstatements.py")
loc = _load("check_batch_locality_cr", ROOT / "scripts" / "check-batch-locality.py")

BEFORE = datetime.date(2027, 5, 31)
ON = datetime.date(2027, 6, 1)


def test_the_switch_date_is_2027_06_01():
    assert wikidata_lockout.COURT_RANK_ANYONE_FROM == ON


def test_anyone_only_from_the_date():
    assert not wikidata_lockout.court_rank_anyone(BEFORE)
    assert wikidata_lockout.court_rank_anyone(ON)


def test_before_the_date_only_the_universe_and_its_ring(tmp_path, monkeypatch):
    uni = tmp_path / "edit-universe.json"
    uni.write_text(json.dumps({"universe": ["Q1"], "one_step": ["Q2"], "name_items": ["Q3"]}),
                   encoding="utf-8")
    monkeypatch.setattr(gen, "UNIVERSE", str(uni))
    assert gen.allowed_people(BEFORE) == {"Q1", "Q2"}
    assert gen.allowed_people(ON) is None


def test_before_the_date_a_missing_universe_means_nobody(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "UNIVERSE", str(tmp_path / "absent.json"))
    assert gen.allowed_people(BEFORE) == set()


def test_every_line_carries_the_jawiki_reference():
    line = gen.qs_line("Q5", "Q99", "https://ja.wikipedia.org/wiki/X")
    assert line == 'Q5\tP14005\tQ99\tS143\tQ177837\tS4656\t"https://ja.wikipedia.org/wiki/X"'


def test_the_locality_gate_follows_the_same_date():
    line = "Q5\tP14005\tQ99\tS143\tQ177837"
    assert not loc.court_rank_anywhere(line, BEFORE)
    assert loc.court_rank_anywhere(line, ON)
    assert not loc.court_rank_anywhere("Q5\tP31\tQ5", ON)
