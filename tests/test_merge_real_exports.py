"""The merge, run against the real exports, checked for data loss.

A merge that quietly drops lines is worse than no merge, and the unit tests
cannot catch that — the collapsing bug that made two `NAME` lines with the same
text into one was only visible here. So this asserts the property that actually
matters: **every line of every source survives in the merged tree.**

Skips when `data_lake/` is empty.
"""

from collections import Counter
from pathlib import Path

import pytest

from genimerge import gedcom, merge
from genimerge.identity import geni_id_of

DATA_LAKE = Path(__file__).resolve().parents[1] / "data_lake"
EXPORTS = sorted(DATA_LAKE.glob("*.ged"))

pytestmark = pytest.mark.skipif(not EXPORTS, reason="no GEDCOM exports in data_lake/")


@pytest.fixture(scope="module")
def merged():
    doc, report = merge.merge_files(EXPORTS)
    return doc, report, doc.by_xref()


def _lines(node, prefix=""):
    """Every (path, value) pair in a subtree — one entry per GEDCOM line."""
    path = f"{prefix}.{node.tag}" if prefix else node.tag
    yield (path, node.value)
    for child in node.children:
        yield from _lines(child, path)


def test_no_record_is_lost(merged):
    _, _, index = merged

    for path in EXPORTS:
        missing = {r.xref for r in gedcom.stream_file(path) if r.xref} - set(index)
        assert missing == set(), f"{path.name} lost {len(missing)} records"


def test_no_line_is_lost(merged):
    _, _, index = merged
    dropped: Counter = Counter()

    for path in EXPORTS:
        for record in gedcom.stream_file(path):
            if not record.xref or record.tag in ("HEAD", "TRLR"):
                continue
            present = set(_lines(index[record.xref]))
            for line in _lines(record):
                if line not in present:
                    dropped[line[0]] += 1

    assert dropped == Counter(), f"merged file is missing source lines: {dropped.most_common(5)}"


def test_the_merge_is_idempotent(merged):
    doc, _, _ = merged
    again = merge.Merger(merge.single_valued_paths(EXPORTS))
    again.add_source("merged", doc.records)
    again.add_source("merged-again", [r.copy() for r in doc.records])

    assert again.result().records == doc.records
    assert again.report.conflicts == []


def test_family_structure_resolves(merged):
    doc, _, _ = merged
    structural = {"CHIL", "HUSB", "WIFE", "FAMC", "FAMS"}
    broken = {
        path: n
        for path, n in merge.dangling_pointers(doc).items()
        if path.rsplit(".", 1)[-1] in structural
    }

    assert broken == {}


def test_every_merged_individual_still_agrees_with_its_own_rfn(merged):
    doc, _, _ = merged

    for record in doc.records:
        if record.tag == "INDI":
            assert geni_id_of(record)  # raises IdentityMismatch if xref != RFN


def test_the_merged_file_is_readable_gedcom(merged, tmp_path):
    doc, _, _ = merged
    path = tmp_path / "merged.ged"
    gedcom.write_file(doc, path)
    reparsed = gedcom.parse_file(path)

    assert reparsed.warnings == []
    assert reparsed.records == doc.records


def test_the_merge_is_worth_doing(merged):
    doc, report, _ = merged
    biggest = max(
        sum(1 for r in gedcom.stream_file(p) if r.tag == "INDI") for p in EXPORTS
    )

    assert report.totals["INDI"] > biggest
