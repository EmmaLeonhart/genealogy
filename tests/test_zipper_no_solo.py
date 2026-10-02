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


def test_a_different_verdict_refuses_the_pairing():
    """Adelus Eriksdatter (2026-10-02): the walk read only `SAME` verdicts. A pairing judged
    `DIFFERENT` is refused even when the years agree, and goes to the conflicts."""
    zj = _zipper()
    ours = {"c": {"father": "f", "mother": "", "spouses": "", "children": ""},
            "f": {"father": "", "mother": "", "spouses": "", "children": "c"}}
    theirs = {"FC": {"p22": "FF", "p25": "", "p26": "", "p40": ""},
              "FF": {"p22": "", "p25": "", "p26": "", "p40": "FC"}}
    args = (ours, theirs, {"c": {"FC"}}, {"FC": {"c"}},
            {"c": "Adelus", "f": "Erich Andersen Kruckow"},
            {"FC": "Adelus", "FF": "Erik Semundsson"}, {"f": 1430}, {"FF": 1430},
            lambda a, b: False)
    pairs, *_ = zj.zip_sides(*args, max_rounds=3, allow_solo=False)
    assert "f" in pairs
    pairs, _prov, conflicts, *_ = zj.zip_sides(*args, max_rounds=3, allow_solo=False,
                                               refused=frozenset({("f", "FF")}))
    assert "f" not in pairs
    assert any(c["geni_id"] == "f" and c["recorded_qid"] == "DIFFERENT" for c in conflicts)


def test_the_last_verdict_on_a_pair_wins(tmp_path):
    """Kari "Wind" Fornjotsson against `PXPY-MM4` (2026-10-02): SAME, then DIFFERENT, and the
    walk kept the SAME as an anchor while only blocking proposals on the DIFFERENT, so the whole
    Fornjot line was paired one generation off. `read_verdicts` keeps the last verdict per pair:
    a SAME later judged DIFFERENT is a refusal, and a DIFFERENT later judged SAME an anchor."""
    zj = _zipper()
    path = tmp_path / "judgments.tsv"
    path.write_text(
        "date\tbatch\tn\tround\tgeni_id\tour_name\tqid\ttheir_name\tverdict\ther_words\n"
        "2026-10-01\tfamilysearch-parent-deck\t\t\t1\tKari\tPXPY-MM4\tFrosti Kari\tSAME\t\n"
        "2026-10-01\tfamilysearch-parent-deck\t\t\t1\tKari\tPXPY-MM4\tFrosti Kari\tDIFFERENT\t\n"
        "2026-10-01\tfamilysearch-parent-deck\t\t\t2\tA\tAAAA-111\tA\tDIFFERENT\t\n"
        "2026-10-01\tfamilysearch-parent-deck\t\t\t2\tA\tAAAA-111\tA\tSAME\t\n"
        "2026-10-01\tfamilysearch-parent-deck\t\t\t3\tB\tBBBB-222\tB\tSAME\t\n"
        "2026-10-01\tparent-deck\t\t\t4\tC\tQ123\tC\tSAME\t\n",      # a Wikidata verdict, not ours
        encoding="utf-8")
    same, refused = zj.read_verdicts(path)
    assert same == {"AAAA-111": "2", "BBBB-222": "3"}
    assert refused == {("1", "PXPY-MM4")}
    assert zj.read_verdicts(tmp_path / "missing.tsv") == ({}, set())
