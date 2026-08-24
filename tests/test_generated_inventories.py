"""A file that describes other files goes stale silently. These two now cannot.

Twice on 2026-08-23 an inventory in this repo was found describing a repo that no
longer existed, and in both cases nothing failed when it drifted — that is the
whole hazard. An inventory is only consulted when someone wants to know the state
of things, which is exactly when being wrong costs the most.

* **`reports/repo-freshness.csv`** listed `reports/missing-ancestors-check.csv` and
  `scripts/check-missing-ancestors.py`, neither of which exists. It had already sent
  one bloat review chasing files that were already gone.
* **`reports/built-batches.tsv`**'s predecessor — a table maintained by hand in
  `todo.md` — listed **14** of the 24 generated batches, and the ten it omitted
  included `wikidata-marker-label-fixes.json` at 56,369 edits, the largest batch in
  the repo.

What is pinned here is the property that failed, not the numbers:

* every path an inventory names still exists, and
* the batch inventory names **exactly** the batch files on disk — a new generator's
  output appearing without a row is the drift that hid the largest batch.

**Entry counts are deliberately not asserted.** A count changes whenever a
generator runs, which is ordinary mid-work, and a suite that goes red for that
teaches people to ignore it. Names are the invariant; the counts are refreshed by
re-running `scripts/audit-built-batches.py`.
"""
import csv
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
REPORTS = REPO / "reports"
FRESHNESS = REPORTS / "repo-freshness.csv"
BATCHES = REPORTS / "built-batches.tsv"


def batch_files_on_disk():
    """What `scripts/audit-built-batches.py` considers a batch."""
    return {f"reports/{p.name}" for p in
            list(REPORTS.glob("wikidata-*.json")) + list(REPORTS.glob("*.qs"))}


def listed_in(path):
    """The `batch` column of an inventory TSV."""
    with open(path, encoding="utf-8") as f:
        return {row["batch"] for row in csv.DictReader(f, delimiter="	")
                if row.get("batch")}


def drift(listed, actual):
    """(on disk but unlisted, listed but gone). The comparison, in one place."""
    return sorted(actual - listed), sorted(listed - actual)


@pytest.mark.skipif(not BATCHES.exists(), reason="no batch inventory generated yet")
def test_the_batch_inventory_names_exactly_the_batches_on_disk():
    listed = set()
    with open(BATCHES, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["batch"]:
                listed.add(row["batch"])

    actual = batch_files_on_disk()
    missing = sorted(actual - listed)
    extra = sorted(listed - actual)
    assert not missing and not extra, (
        "reports/built-batches.tsv is stale — re-run scripts/audit-built-batches.py. "
        f"On disk but unlisted: {missing[:5]}. Listed but gone: {extra[:5]}.")


@pytest.mark.skipif(not FRESHNESS.exists(), reason="no freshness report generated yet")
def test_the_freshness_report_names_no_file_that_has_been_deleted():
    gone = []
    with open(FRESHNESS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            path = (row.get("path") or "").strip()
            if path and not (REPO / path).exists():
                gone.append(path)
    assert not gone, (
        "reports/repo-freshness.csv lists files that no longer exist — re-run "
        f"scripts/build-repo-freshness.py: {gone[:5]}")


@pytest.mark.skipif(not FRESHNESS.exists(), reason="no freshness report generated yet")
def test_the_freshness_report_names_every_generator_that_still_exists():
    """A generator column pointing at a deleted script is the same failure inverted.

    The column holds a **semicolon-separated list** — a report written by more than
    one script names them all. A first cut treated the whole field as one path and
    failed on five rows that were perfectly correct; the data was right and the test
    was wrong about its shape.
    """
    gone = []
    with open(FRESHNESS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for gen in (row.get("generator") or "").split(";"):
                gen = gen.strip()
                if gen and not (REPO / gen).exists():
                    gone.append((row.get("path"), gen))
    assert not gone, (
        "reports/repo-freshness.csv names generators that no longer exist: "
        f"{gone[:5]}")


# --- the checks would notice, not merely pass on today's files ---------------

HEADER = "batch" + chr(9) + "entries" + chr(9) + "shape" + chr(10)


def _inventory(tmp_path, *names):
    """Write a minimal inventory TSV naming `names`."""
    inv = tmp_path / "built-batches.tsv"
    body = "".join(n + chr(9) + "1" + chr(9) + "x" + chr(10) for n in names)
    inv.write_text(HEADER + body, encoding="utf-8")
    return inv


def test_the_batch_check_notices_an_unlisted_file(tmp_path):
    """The drift that hid `wikidata-marker-label-fixes.json`."""
    inv = _inventory(tmp_path, "reports/a.qs")
    missing, extra = drift(listed_in(inv), {"reports/a.qs", "reports/b.json"})
    assert missing == ["reports/b.json"] and not extra


def test_the_batch_check_notices_a_listed_file_that_is_gone(tmp_path):
    """The other direction: `repo-freshness.csv` naming two deleted files."""
    inv = _inventory(tmp_path, "reports/a.qs", "reports/vanished.json")
    missing, extra = drift(listed_in(inv), {"reports/a.qs"})
    assert extra == ["reports/vanished.json"] and not missing


def test_the_batch_check_is_quiet_when_the_inventory_is_right(tmp_path):
    inv = _inventory(tmp_path, "reports/a.qs")
    assert drift(listed_in(inv), {"reports/a.qs"}) == ([], [])


def test_the_disk_reader_finds_both_batch_shapes():
    """JSON edit objects and QuickStatements files are both batches."""
    found = batch_files_on_disk()
    assert any(p.endswith(".qs") for p in found), "no .qs batch seen"
    assert any(p.endswith(".json") for p in found), "no JSON batch seen"
