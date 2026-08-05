"""The merge, run against the real exports, checked for data loss.

A merge that quietly drops lines is worse than no merge, and the unit tests
cannot catch that — the collapsing bug that made two `NAME` lines with the same
text into one was only visible here. So this asserts the property that actually
matters: **every line of every source survives in the merged tree.**

Skips when `exports/` is empty.
"""

from collections import Counter
from pathlib import Path

import pytest

from genimerge import gedcom, merge, sources
from genimerge.identity import geni_id_of

EXPORTS = sources.find_exports()

pytestmark = pytest.mark.skipif(not EXPORTS, reason="no GEDCOM exports in exports/")


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


def test_no_line_is_lost_except_where_a_conflict_replaced_it(merged):
    """Every source line survives, minus exactly the ones a conflict displaced.

    This asserted `dropped == Counter()` outright until 2026-08-04, which held
    while the real exports produced no conflicts at all. At 45 exports they
    produce some, and a conflict *is* a dropped line by definition — the merge
    keeps one of two values for a single-valued path. Asserting zero would now
    fail for a reason the merge is designed to have.

    So the assertion is not weakened to "some lines may go missing". It is
    tightened to: a line may only go missing on a **path the conflict report
    names**, and that path must be single-valued. A line disappearing anywhere
    else still fails, which is what this test was for.

    The counts deliberately are not compared. One conflict can strand the same
    superseded value in many sources at once — 45 exports of one profile may all
    carry the old `CHAN.DATE`, and every one of them counts as a dropped line
    while only the transitions count as conflicts. Asserting equality of counts
    was tried first and fails for that reason, not for a real one.
    """
    doc, report, index = merged
    dropped: Counter = Counter()

    for path in EXPORTS:
        for record in gedcom.stream_file(path):
            if not record.xref or record.tag in ("HEAD", "TRLR"):
                continue
            present = set(_lines(index[record.xref]))
            for line in _lines(record):
                if line not in present:
                    dropped[line[0]] += 1

    unexplained = set(dropped) - {c.path for c in report.conflicts}
    assert unexplained == set(), (
        f"merged file is missing source lines on paths no conflict explains: {sorted(unexplained)[:5]}"
    )
    assert set(dropped) <= merge.single_valued_paths(EXPORTS), (
        "a line went missing on a multi-valued path, where nothing should ever be replaced: "
        f"{sorted(set(dropped) - merge.single_valued_paths(EXPORTS))[:5]}"
    )


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


# --- the committed report, against the exports it claims to describe ---------
#
# `reports/merge.md` is generated and tracked in git, and nothing checked that
# it still matched the corpus. It spent twelve commits describing an
# 8766-person, three-export merge while `out/merged.ged` held 12422 across four.
# The suite passed throughout and `git status` was clean, because the wrong file
# had been committed. What found it was running the pipeline and asking whether
# the output changed — which no test did.
#
# `test_the_merge_is_idempotent` above covers the merge *function*. This covers
# the *artifact*, and it is nearly free: the module fixture has already done the
# merge for the other tests here.
#
# Only merge.md. `inventory.md`, `frontier.md` and `seeds.md` are also pure
# functions of the corpus and could be checked the same way, but each needs
# its own regeneration and `seeds` alone takes about a minute — several-folding
# the suite for reports that have not gone wrong yet. `names.md`,
# `wikidata-coverage.md` and `wikidata-crosscheck.md` cannot be checked offline
# at all: they depend on live Wikidata. The omissions are deliberate, not
# oversights.

COMMITTED_MERGE_REPORT = Path(__file__).resolve().parents[1] / "reports" / "merge.md"


@pytest.mark.skipif(
    not COMMITTED_MERGE_REPORT.exists(), reason="reports/merge.md absent from this checkout"
)
def test_the_committed_merge_report_still_describes_these_exports(merged):
    doc, report, _ = merged

    expected = merge.render_report(report, detail=False, doc=doc)
    actual = COMMITTED_MERGE_REPORT.read_text(encoding="utf-8")

    assert actual == expected, (
        "reports/merge.md no longer matches what merging exports/ produces. "
        "Re-run `python -m genimerge merge` and commit the result. If you did not "
        "change exports/, check what did write this file — a merge sent "
        "elsewhere with --output used to overwrite it with a different merge."
    )


def test_the_report_names_every_export_in_the_corpus(merged):
    """The failure that happened, asserted directly as well as by equality.

    Byte equality covers this, but it fails as an opaque diff. A missing source
    file is the specific thing that went wrong, and it is worth its own message.
    """
    _, report, _ = merged
    text = merge.render_report(report, detail=False, doc=merged[0])

    for export in EXPORTS:
        assert export.name in text, f"{export.name} is in exports/ but not in the report"
