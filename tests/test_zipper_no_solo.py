"""The FamilySearch zipper never pairs a one-against-one slot on position alone.

`b26c7259c` (Emma, 2026-10-01): position alone fused differently named lines -- Kerstin
Olofsdotter with Elisabet Matsdotter above Eric Ericsson, rounds 7-9 -- and the Adelus
Eriksdatter mix-up of 2026-09-30. `zip_sides(..., allow_solo=False)` makes a 1 x 1 slot need a
matching year or name like any other slot. These pin both sides of that rule.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _zipper():
    spec = importlib.util.spec_from_file_location("zj", ROOT / "scripts" / "zipper-join.py")
    zj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(zj)
    return zj


def _run(our_father, their_father, our_year=None, their_year=None, allow_solo=False):
    """One anchored child on each side, one father on each side: a 1 x 1 father slot."""
    zj = _zipper()
    ours = {"c": {"father": "f", "mother": "", "spouses": "", "children": ""},
            "f": {"father": "", "mother": "", "spouses": "", "children": "c"}}
    theirs = {"FC": {"p22": "FF", "p25": "", "p26": "", "p40": ""},
              "FF": {"p22": "", "p25": "", "p26": "", "p40": "FC"}}
    stated_g = {"c": {"FC"}}
    stated_q = {"FC": {"c"}}
    pairs, *_ = zj.zip_sides(ours, theirs, stated_g, stated_q,
                             {"c": "Eric Ericsson", "f": our_father},
                             {"FC": "Eric Ericsson", "FF": their_father},
                             {"f": our_year} if our_year else {},
                             {"FF": their_year} if their_year else {},
                             lambda a, b: False, max_rounds=3, allow_solo=allow_solo)
    return pairs


def test_familysearch_one_against_one_with_nothing_in_common_is_refused():
    assert "f" not in _run("Olof Eriksson", "Mats Henriksson")


def test_familysearch_one_against_one_with_a_matching_name_pairs():
    assert _run("Olof Eriksson", "Olof Eriksson").get("f", (None,))[0] == "FF"


def test_familysearch_one_against_one_with_a_matching_year_pairs():
    assert _run("Olof Eriksson", "Mats Henriksson", 1692, 1692).get("f", (None,))[0] == "FF"


def test_position_only_pairing_is_what_allow_solo_true_would_do():
    """The Geni-Wikidata join keeps `allow_solo=True`; this shows the flag is what differs."""
    assert _run("Olof Eriksson", "Mats Henriksson", allow_solo=True).get("f", (None,))[0] == "FF"


def test_the_familysearch_run_passes_allow_solo_false():
    src = (ROOT / "scripts" / "zipper-join.py").read_text(encoding="utf-8")
    assert "FS_MAX_ROUNDS, allow_solo=False)" in src
