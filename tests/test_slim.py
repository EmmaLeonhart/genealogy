"""What `--slim` keeps, and what it must never start keeping again.

`genimerge.slim` is a WHITELIST: a tag nobody named is dropped with its whole subtree. That is
what makes the merge run on a runner at all -- unslimmed it was killed at 15,921 MB of 16 GB.

**The bar for keeping a tag is that something READS what it becomes**, and it was not being
applied. The structured address block was kept because `derive-facts.py` reads it -- true, and
the wrong test: `derive-facts` writes `birth_address`, `death_address` and `burial_address`, and
nothing reads those columns. No place statement has ever reached Wikidata either.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from genimerge.slim import DROP_INSIDE, KEEP_RECORDS, KEEP_TAGS

REPO = Path(__file__).resolve().parents[1]

#: Dropped 2026-09-10: 124,880,269 bytes over 8,741,947 lines, 3.03% of the slimmed tree, and
#: three times the size of `PLAC`, for no consumer at all.
ADDRESS_BLOCK = {"ADDR", "ADR1", "ADR2", "ADR3", "CITY", "CTRY", "POST", "STAE"}


def test_the_address_block_is_not_kept():
    """⛔ It cost ~467 MB of a 15,428 MB peak and nothing read the columns it fed."""
    assert not (ADDRESS_BLOCK & KEEP_TAGS), sorted(ADDRESS_BLOCK & KEEP_TAGS)


def test_plac_is_still_kept_and_the_reason_is_not_places():
    """`build-cjk-romanisation.py` reads `birth_place`/`death_place` as CULTURE evidence -- the
    words in them decide whether a CJK person is classified ja, zh or ko, and that gate is
    load-bearing. Dropping `PLAC` would blind it to save 1%."""
    assert "PLAC" in KEEP_TAGS
    source = (REPO / "scripts" / "build-cjk-romanisation.py").read_text(encoding="utf-8")
    assert "birth_place" in source and "death_place" in source


def test_the_primary_key_and_the_structure_survive():
    """Whatever else is cut, these are what a tree IS -- `CLAUDE.md` § *The Geni profile ID is
    the primary key for everything*."""
    for tag in ("RFN", "SEX", "FAMC", "FAMS", "HUSB", "WIFE", "CHIL", "NAME", "GIVN", "SURN"):
        assert tag in KEEP_TAGS, tag
    for record in ("INDI", "FAM", "HEAD", "TRLR"):
        assert record in KEEP_RECORDS, record


def test_the_expensive_tags_stay_dropped():
    """Notes and media are ~67% of corpus bytes and are the whole reason slimming exists."""
    for tag in ("NOTE", "SOUR", "OBJE", "FILE", "TEXT"):
        assert tag in DROP_INSIDE, tag


def test_no_place_statement_has_ever_been_emitted():
    """The measurement behind the cut, kept as a test so a new place emitter has to notice it.

    If a `P19`/`P20`/`P119` emitter is ever added, the address block may need to come back --
    and this failing is how that conversation starts, instead of the columns silently being
    empty.
    """
    out = subprocess.run(
        ["git", "grep", "-lE", r"^Q[0-9]+\t(P19|P20|P119)\t", "--",
         "reports/*.qs", "reports/wikidata-garborg-day.txt"],
        cwd=REPO, capture_output=True, text=True)
    assert not out.stdout.strip(), (
        "a place statement is being emitted, so the address block may need to come back: "
        + out.stdout)
