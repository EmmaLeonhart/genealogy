"""`reports/synoptic-conflicts.tsv` must attribute each candidate QID separately.

The file used to carry one row per Geni profile with the sources of **every** candidate
flattened into one set. `structural;wikidata-p2600` then told you the conflict involved
both, but not which source proposed which QID — and that is the entire question, because
`wikidata-p2600` is a statement Wikidata carries while `structural` is our own inference
from tree position.

**It misled twice in one day.** Katharina von Braunschweig-Wolfenbüttel was reported as
the structural walk pairing a woman with `Q567039` *Henry IV, Duke of Brunswick*. The walk
never touched her: `P2600` supplied the correct `Q434771`, and the wrong candidate came
from `geni-wikidata-pairs`.
"""
from __future__ import annotations

import collections
import csv
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
CONFLICTS = REPO / "reports" / "synoptic-conflicts.tsv"

pytestmark = pytest.mark.skipif(not CONFLICTS.exists(), reason="no conflicts report")


def rows():
    with open(CONFLICTS, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def test_every_row_is_one_candidate_not_one_profile():
    """A conflicted profile contributes one row per competing QID."""
    got = rows()
    assert "qid" in got[0] and "competing_qids" in got[0], (
        "the file must name a single qid per row, with the rivals listed separately")
    by_profile = collections.Counter(r["geni_id"] for r in got)
    assert all(n >= 2 for n in by_profile.values()), (
        "a conflict needs at least two candidate rows; a single row means the "
        "candidates were collapsed again")


def test_sources_belong_to_that_qid_alone():
    """The flattening bug, as a regression.

    If sources were flattened, every row for one profile would carry the same source
    string. Real per-candidate provenance almost always differs — that is the point.
    """
    by_profile = collections.defaultdict(set)
    for r in rows():
        by_profile[r["geni_id"]].add(r["sources"])
    identical = [g for g, srcs in by_profile.items() if len(srcs) == 1]
    # Some genuinely do share a source -- two Wikidata items both asserting P2600 --
    # so this is a proportion, not an absolute.
    assert len(identical) < len(by_profile), (
        "every profile's candidates share one source string, which is what the "
        "flattened column looked like")


def test_the_shape_column_separates_our_inference_from_a_recorded_id():
    """`structural` is ours, `wikidata-p2600` is Wikidata's. Where they disagree the
    recorded identifier wins, so that case must be filterable without re-deriving it."""
    shapes = {r["shape"] for r in rows()}
    assert "inference vs recorded id" in shapes
    for r in rows():
        if r["shape"] == "both from Wikidata":
            assert r["sources"] == "wikidata-p2600", (
                f"row shaped 'both from Wikidata' has sources {r['sources']!r}")
