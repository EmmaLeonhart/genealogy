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


def test_no_place_tag_survives_at_all():
    """⛔ **THIS ASSERTED THE OPPOSITE YESTERDAY AND THE RULE CHANGED UNDER IT**, which is worth
    saying out loud: it is not a test being loosened to make a change pass.

    `PLAC` was kept for one reason -- it was culture evidence 1 in `build-cjk-romanisation.py`,
    deciding ja/zh/ko for CJK people -- and that argument was withdrawn by the person who owns
    it: *"there was an algorithm, and it failed miserably"*, and *"keeping the places in the
    synoptic tree is a horrible idea"*. The replacement is manual review.

    The bar is unchanged: a tag is kept when something reads what it becomes. Nothing does.
    """
    assert "PLAC" not in KEEP_TAGS
    assert not (ADDRESS_BLOCK & KEEP_TAGS)


def test_the_cjk_classifier_keeps_its_other_evidence():
    """Evidence 1 of five goes; the other four are untouched, so this narrows the classifier
    rather than disabling it."""
    source = (REPO / "scripts" / "build-cjk-romanisation.py").read_text(encoding="utf-8")
    assert source.count("culture evidence") >= 4


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
