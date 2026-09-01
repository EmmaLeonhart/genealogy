"""The gap finder, which answers presence without building the merged tree.

Emma, 2026-08-17, on the merge I ran unasked: *"rebuilding the synoptic tree right now
is just going to create another tree that's going to become out of date pretty soon."*
The rules pinned here are the ones that make the cheap answer the correct one.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def gaps():
    spec = importlib.util.spec_from_file_location(
        "find_chain_gaps", REPO / "scripts" / "find-chain-gaps.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_xref_pattern_reads_geni_ids_and_only_those(gaps):
    """`0 @I…@ INDI` is the xref Geni writes and this repo's primary key.

    Anchored at the line start and to `INDI`, so a `FAM`, a `NOTE` or an ID mentioned
    inside a record's text cannot be mistaken for a person.
    """
    text = (b"0 HEAD\n"
            b"0 @I6000000001846508982@ INDI\n"
            b"1 NAME Emma /Leonhart/\n"
            b"0 @F123@ FAM\n"
            b"1 NOTE see @I999@ INDI for details\n"
            b"0 @I42@ INDI\n"
            b"0 TRLR\n")
    found = [m.group(1).decode() for m in gaps.INDI_XREF.finditer(text)]
    assert found == ["6000000001846508982", "42"]


def test_the_url_is_the_family_tree_index_not_the_profile(gaps):
    """Emma, 2026-08-17: the family-tree page is *"a better page to open up for them
    rather than the pages you opened"*. The profile shows one person; the index shows
    the neighbourhood she has to work in to place a placeholder and export."""
    url = gaps.FAMILY_TREE_URL.format("6000000085113755501")
    assert url == "https://www.geni.com/family-tree/index/6000000085113755501"
    assert "/people/" not in url


def test_chains_reads_the_id_out_of_the_note_column(gaps, tmp_path, monkeypatch):
    """A path row carries its Geni ID as `geni:<id>` in the note column, which is what
    makes checking a path an exact join rather than a name match."""
    monkeypatch.setattr(gaps, "PATHS_DIR", tmp_path)
    (tmp_path / "a.tsv").write_text(
        "# a comment\n"
        "step\tname\trelation_to_previous\tnote\n"
        "1\tYou\t-\tgeni:100\n"
        "2\ther father\ther father\tgeni:200\n"
        "3\tno id here\this son\t\n",
        encoding="utf-8")
    (tmp_path / "b.tsv").write_text(
        "1\tYou\t-\tgeni:100\n", encoding="utf-8")

    found = gaps.chains()

    assert found["100"] == {"a.tsv", "b.tsv"}, "a person on two paths fills two slots"
    assert found["200"] == {"a.tsv"}
    assert "" not in found, "a row with no ID contributes nothing"


def test_a_person_counts_once_per_path_not_once_per_step(gaps, tmp_path, monkeypatch):
    """A saved page can walk one person twice — `paths/nn-basse.tsv` re-walks its
    opening — and that is one slot on one path, not two."""
    monkeypatch.setattr(gaps, "PATHS_DIR", tmp_path)
    (tmp_path / "a.tsv").write_text(
        "1\tYou\t-\tgeni:100\n"
        "2\tsomebody\this father\tgeni:200\n"
        "3\tYou again\t-\tgeni:100\n",
        encoding="utf-8")

    assert gaps.chains()["100"] == {"a.tsv"}
