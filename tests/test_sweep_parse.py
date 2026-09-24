"""`scripts/parse-sweep-trees.py`: the pieces the whole parse rests on.

A label-only person must never read as a Geni id -- the `@NI04461@` trap again -- and the
string forms measured on the real sweep (the `MP` badge, a nickname LIST after the years, the
percent-encoded slug, `Waldeck and Pyrmont` inside a name) are pinned here.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from genimerge.identity import geni_id_from_xref  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "parse_sweep_trees", REPO / "scripts" / "parse-sweep-trees.py")
sweep = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sweep)


def test_a_label_xref_never_parses_as_a_geni_id():
    for key in [("sp", "6000000012014864133", "christine"), ("pair", "1", "a", "M"), ("x",)]:
        for kind in "IF":
            x = sweep.label_xref(kind, key)
            assert x.startswith("@%sL" % kind)
            assert geni_id_from_xref(x) is None


def test_label_xref_is_stable():
    k = ("sp", "6000000012014864133", "christine")
    assert sweep.label_xref("I", k) == sweep.label_xref("I", k)


def test_the_master_profile_badge_and_a_nickname_list_come_off():
    assert sweep.split_name(
        'Name: Marie Dorothea von Kurland (1684 - 1743) "Maria", "Princess of Kurland"'
    ) == ("Marie Dorothea von Kurland", "1684", "1743")
    assert sweep.split_name("Name: Friedrich von Brandenburg-Schwedt MP (1710 - 1741)") == (
        "Friedrich von Brandenburg-Schwedt", "1710", "1741")
    assert sweep.split_name("Name: Albrecht Dobbin (c.1629 - 1665)")[1] == "ABT 1629"


def test_the_slug_matches_the_short_name_across_encoding_and_punctuation():
    assert sweep.slug("Marguerite d'Orléans") == sweep.slug("Marguerite-d-Orl%C3%A9ans")
    assert sweep.slug("Jacob Bibler") == sweep.slug("Jacob-Bibler")


def test_roles_split_on_the_closed_vocabulary():
    r = sweep.roles("Immediate Family: Son of Stephan Dobbin, II and Margarete Koch "
                    "Husband of Elisabeth Dobbin Father of Steffen Dobbin "
                    "Brother of Hieronymus Dobbin and Anna Sophie Dobbin")
    assert r["Son of"] == "Stephan Dobbin, II and Margarete Koch"
    assert r["Husband of"] == "Elisabeth Dobbin"
    assert sweep.listed(r["Brother of"]) == ["Hieronymus Dobbin", "Anna Sophie Dobbin"]


def test_generation_reads_words_and_digits():
    assert sweep.generation("Relationship: Christine's daughter") == 1
    assert sweep.generation("Relationship: Yuri's fifth great grandson") == 7
    assert sweep.generation("Relationship: Yuri's 12th great grandson") == 14
