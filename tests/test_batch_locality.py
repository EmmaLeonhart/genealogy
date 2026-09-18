"""Every edit in a batch is on an item in the universe, or one step beyond it.

⛔ **THIS TEST EXISTS BECAUSE THE RULE WAS BROKEN AND NOTHING NOTICED.** On 2026-09-18 nine `ja`
labels were written onto `Q135525010`, `Q135579354` and seven more — Jan-1 entry points, outside
the universe, deliberately inactive until 2027-01-01 — and were reverted by hand one at a time.
Behind them sat 936, 962 and 985 more non-local lines in the three day batches, on 300, 321 and
348 distinct items.

`CLAUDE.md` § *AN EDIT GOES ON AN ITEM IN THE UNIVERSE, OR ONE STEP BEYOND IT. ALL EDITS, NO
EXCEPTIONS.*

**The gate was written three times before it held**, each time over a path rather than over the
output: first only in the sender (which the pasted QuickStatements route never touches), then only
over `derived_labels` (so `P22`, `P40` and `P2600` sailed past), then only over `lines` (so 11
`Qperson P734 LAST` bearer links in the prepended name-items head sailed past). A guard applied to
a path is not a guard on the batch.

So this reads the written file, which is the only artifact that reaches Wikidata by every route —
the sender, the published page, a hand paste — and is the one thing no refactor can route around.
"""
from __future__ import annotations

import json
import pathlib
import re

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
UNIVERSE = REPO / "out" / "wikidata" / "edit-universe.json"
BATCHES = ("reports/wikidata-garborg-day.txt",
           "reports/wikidata-garborg-day-auto.txt",
           "reports/wikidata-garborg-day-manual.txt")

#: A batch line that acts on an EXISTING item names it first. `CREATE` and its `LAST` lines carry
#: no QID and are picked from inside the universe by `compose` already.
SUBJECT = re.compile(r"^(Q\d+)\t")


def universe():
    if not UNIVERSE.exists():
        pytest.skip("out/wikidata/edit-universe.json absent -- recompose to build it")
    d = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    allowed = set(d.get("universe") or ()) | set(d.get("one_step") or ())
    assert allowed, "the universe file is present but empty -- that is the absence of the gate"
    return allowed


@pytest.mark.parametrize("rel", BATCHES)
def test_no_edit_lands_outside_the_universe(rel):
    """Not one line in a batch may name a subject the universe does not hold."""
    path = REPO / rel
    if not path.exists():
        pytest.skip(f"{rel} not built")
    allowed = universe()
    offenders = {}
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        m = SUBJECT.match(line)
        if m and m.group(1) not in allowed:
            offenders.setdefault(m.group(1), n)
    assert not offenders, (
        f"{rel}: {len(offenders)} item(s) neither in the universe nor one step beyond it, "
        f"first at line {min(offenders.values())}: "
        + ", ".join(sorted(offenders)[:8])
        + (" ..." if len(offenders) > 8 else "")
        + " -- CLAUDE.md: ALL EDITS, NO EXCEPTIONS")


@pytest.mark.parametrize("rel", BATCHES)
def test_no_label_edit_on_an_item_holding_a_kanji_label(rel):
    """⛔ A kanji `ja` label marks a SINOSPHERE name, and those take no label edit at all.

    `CLAUDE.md` § *THE KANJI SIGNAL DECIDES WHICH LABEL UNIVERSE A PERSON IS IN*: a kanji `ja`
    label means a different universe of labels, so **no label edit in any language**; katakana or
    blank means ours. Writing katakana over kanji does not damage a label, it flips the
    classification — the person falls into the Latin pipeline and the corruption compounds.

    The live labels are what Wikidata actually holds; without them this cannot be judged and is
    skipped rather than guessed.
    """
    path = REPO / rel
    live = REPO / "reports" / "garborg-live-labels.tsv"
    if not path.exists() or not live.exists():
        pytest.skip("batch or reports/garborg-live-labels.tsv not built")
    # The Han ranges, written as ASCII escapes. CLAUDE.md § *Write a Han range as ASCII escapes* --
    # the literal form ate the Hangul block and cost 5,338 Korean people.
    # A regnal numeral is not a Sinosphere name: 2-plus-generation-kanji is how an ordinal is
    # written, so a katakana name ending in it is still katakana. Strip it before testing.
    ordinal = re.compile("[0-9]+\u4e16")
    han = re.compile("[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
    kanji_items = set()
    for row in live.read_text(encoding="utf-8").split("\n"):
        parts = row.split("\t")
        if len(parts) >= 3 and parts[1] == "ja" and han.search(ordinal.sub("", parts[2] or "")):
            kanji_items.add(parts[0])
    if not kanji_items:
        pytest.skip("no kanji ja labels in the live snapshot")
    bad = {}
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        m = re.match(r"^(Q\d+)\t[LAD](?:mul|en|ja|zh|ko)\t", line)
        if m and m.group(1) in kanji_items:
            bad.setdefault(m.group(1), n)
    assert not bad, (
        f"{rel}: label edits on {len(bad)} item(s) whose ja label is KANJI, which marks a "
        f"Sinosphere name and takes no label edit in any language: "
        + ", ".join(sorted(bad)[:8]))
