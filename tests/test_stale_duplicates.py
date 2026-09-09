"""`reports/geni-stale-duplicates.tsv` — people Geni merged and our corpus did not.

Built from Emma's own Geni activity feed, which is ground truth for which profiles she
has merged. `CLAUDE.md`: the duplicate merges are hers — this flags, never merges.
"""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
REPORT = REPO / "reports" / "geni-stale-duplicates.tsv"
MERGES = REPO / "reports" / "geni-merges-performed.tsv"

pytestmark = pytest.mark.skipif(
    not REPORT.exists() or not MERGES.exists(), reason="no stale-duplicate report")


def rows():
    with open(REPORT, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def test_evidence_compares_parent_NAMES_not_ids():
    """The bug this report shipped with, kept as a regression.

    The first version compared the two profiles' father **ids**. Where the father is
    himself duplicated — which is the normal case here, because whole lineages were
    re-created — the ids differ and the check said "not the same father" for every
    single row. It reported `same_father: no` 27 times and hid 13 strong matches.

    `Kuiko Haji-no-muraji` is the case: both profiles name a father called *Otori
    Haji-no-muraji*, and Otori is himself in this report. Comparing ids was the wrong
    test exactly where the evidence is strongest.
    """
    kuiko = [r for r in rows() if r["name"] == "Kuiko Haji-no-muraji"]
    if not kuiko:
        pytest.skip("Kuiko not in this corpus")
    assert kuiko[0]["father_name_matches"] == "yes", (
        "the father names are identical; only their ids differ")
    assert kuiko[0]["evidence"] == "strong"


def test_every_survivor_really_came_from_the_merge_feed():
    """No row may invent a merge. The feed is the only source of survivors."""
    survivors = {ln.strip() for ln in MERGES.read_text(encoding="utf-8").splitlines()
                 if ln.strip() and not ln.startswith("#") and ln.strip() != "geni_id"}
    bad = [r["merged_survivor"] for r in rows() if r["merged_survivor"] not in survivors]
    assert not bad, f"survivors not in the activity feed: {bad[:5]}"


def test_a_profile_is_never_paired_with_itself():
    assert not [r for r in rows() if r["merged_survivor"] == r["stale_twin"]]


def test_placeholder_names_are_excluded():
    """Two `NN no Mikoto` profiles are two unnamed people, not one person twice."""
    bad = [r["name"] for r in rows()
           if r["name"].strip().lower().split()[:1] in ([("nn")], [("n")])
           or "<private>" in r["name"].lower()]
    assert not bad, f"placeholder names treated as duplicates: {bad[:5]}"


def test_weak_evidence_is_kept_rather_than_dropped():
    """Amram V has two different fathers recorded. That is for Emma to judge, not for
    this report to hide by only publishing what it is confident about."""
    kinds = {r["evidence"] for r in rows()}
    assert kinds <= {"strong", "medium", "weak"}
    assert "weak" in kinds or len(rows()) < 5, (
        "no weak rows at all suggests they were filtered out")
