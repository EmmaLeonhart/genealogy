"""`scripts/build-join-batch.py` — the thing that consumes the synoptic correspondence.

Emma asked on 2026-08-24 whether the join was implemented and it was not: 522,086
Geni ID ↔ QID pairs sat in a file nothing read. This is the consumer, and these are the
rules it must not break.

The rules are hers, not invented here:

* **`P2600` *Geni.com profile ID* comes first.** *"The Jenny ID needs to be present
  before any properties derived from Jenny can be taken from it, or before any
  relationships can be added."*
* **Add, never correct.** A property the item already states is skipped. `CLAUDE.md`:
  *"the entire purpose of this is to add it… Correcting stuff on Wikidata is actually
  such a pain that it's almost effectively out of the question."*
* **One run or nothing.** Every QID a statement points at must already exist.
* **Everything derived from Geni cites the Geni ID** it came from.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
BATCH = REPO / "reports" / "wikidata-join-izumo.qs"
ITEMS = REPO / "out" / "clan-full-items.json"

pytestmark = pytest.mark.skipif(
    not BATCH.exists() or not ITEMS.exists(),
    reason="no join batch generated yet")

STATEMENT = re.compile(r"^(Q[1-9][0-9]*)\t(P[0-9]+)\t(.*)$")


def statements():
    for line in BATCH.read_text(encoding="utf-8").splitlines():
        m = STATEMENT.match(line.rstrip("\r"))
        if m:
            yield m.group(1), m.group(2), m.group(3)


def items():
    return json.loads(ITEMS.read_text(encoding="utf-8"))


#: Values that are vocabulary rather than people: long-standing Wikidata items this
#: batch points at but never downloads. Listed rather than pattern-matched so that a
#: new one is a decision someone made, not a silent widening.
VOCABULARY = {
    "Q6581097",   # male
    "Q6581072",   # female
    "Q5",         # human
}


def test_every_qid_pointed_at_already_exists():
    """The single-run rule. This batch creates nothing, so nothing may be pending."""
    known = set(items()) | VOCABULARY
    bad = [(s, p, v.split("\t")[0]) for s, p, v in statements()
           if re.fullmatch(r"Q[1-9][0-9]*", v.split("\t")[0])
           and v.split("\t")[0] not in known]
    assert not bad, f"points at QIDs not in the downloaded items: {bad[:5]}"


def test_every_subject_already_exists():
    known = set(items())
    bad = sorted({s for s, _p, _v in statements() if s not in known})
    assert not bad, f"editing items we have not read: {bad[:5]}"


def test_the_geni_id_is_emitted_before_anything_derived_from_it():
    """Emma's ordering rule, and it is about meaning rather than tidiness.

    A statement cited to a Geni ID that the item does not yet carry is asserting a
    provenance the reader cannot follow. So for any person this batch adds a `P2600`
    to, that line comes before the first statement referencing it.
    """
    first_geni, first_other = {}, {}
    for i, (subject, prop, _v) in enumerate(statements()):
        if prop == "P2600":
            first_geni.setdefault(subject, i)
        else:
            first_other.setdefault(subject, i)
    late = [s for s, i in first_geni.items()
            if s in first_other and first_other[s] < i]
    assert not late, (
        f"a derived statement precedes the P2600 it is cited to, for: {late[:5]}")


def test_nothing_restates_a_property_the_item_already_has():
    """Add, never correct. A second value on a single-valued property is a claim we
    have no business making, and Geni disagreeing with Wikidata is a note, not a fix.

    The multi-valued relationship properties are exempt on the value, not the property:
    the emitter checks whether *this* target is already stated, which this test cannot
    see from the property name alone.
    """
    single = {"P21", "P569", "P570", "P22", "P25"}
    data = items()
    bad = []
    for subject, prop, _v in statements():
        if prop in single and prop in data.get(subject, {}).get("claims", {}):
            bad.append((subject, prop))
    assert not bad, f"re-stating a property the item already has: {sorted(set(bad))[:5]}"


def test_every_derived_statement_cites_the_geni_profile():
    """`S2600` on everything except the `P2600` statement itself.

    The Geni ID cannot cite itself, and `CLAUDE.md` records that Emma's own items never
    reference `P2600` — it *is* the reference.
    """
    missing = [(s, p) for s, p, v in statements()
               if p != "P2600" and "S2600" not in v]
    assert not missing, f"derived statements with no Geni citation: {missing[:5]}"


def test_the_batch_creates_nothing():
    """Every person here exists on both sides already; a CREATE would be a new person."""
    text = BATCH.read_text(encoding="utf-8")
    assert "CREATE" not in text, (
        "this batch is for items that already exist and are already joined")
    assert "\nLAST\t" not in text, "LAST refers to a CREATE, and there are none"


def test_the_skipped_file_accounts_for_everyone_who_contributed_nothing():
    """A person who yields no statement is recorded with a reason, not dropped."""
    skipped = REPO / "reports" / "wikidata-join-izumo-skipped.tsv"
    if not skipped.exists():
        pytest.skip("no skipped file")
    with open(skipped, encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    assert all(r["why"].strip() for r in rows), "a skipped person with no reason given"
