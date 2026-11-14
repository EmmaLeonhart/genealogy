"""Shared test helpers.

**Why this file exists.** `test_cli.py` and `test_cli_wikidata.py` each had their
own `run()` helper spelling out the workspace flags. When `--data-lake` was
renamed to `--exports-dir` on 2026-08-05, one copy was updated and the other was
not, and every command in the second file exited 2 — 13 failures whose cause was
a flag name written down twice. That is the same shape as the bug
`genimerge.sources` was created to fix: knowledge of one thing kept in several
places, so a change updates some of them.

`run_cli` is now the only place the workspace flags are named in the tests.
"""

from __future__ import annotations

import pytest

from genimerge import cli

#: The workspace flags, in the order the CLI declares them. Named once.
WORKSPACE_FLAGS = ("--exports-dir", "--out", "--reports")


def run_cli(workspace: dict, *argv: str) -> int:
    """Run the CLI against a workspace dict, returning its exit code.

    `workspace` needs ``exports``/``lake``, ``out`` and ``reports`` keys — the
    two test modules named the first one differently, and both spellings are
    accepted rather than renaming fixtures in a change about flag names.
    """
    exports = workspace.get("exports", workspace.get("lake"))
    if exports is None:  # pragma: no cover - a fixture bug, not a code path
        raise KeyError("workspace needs an 'exports' or 'lake' key")
    values = (exports, workspace["out"], workspace["reports"])
    flags: list[str] = []
    for flag, value in zip(WORKSPACE_FLAGS, values):
        flags += [flag, str(value)]
    return cli.main([*argv, *flags])


@pytest.fixture
def run():
    """The `run_cli` helper, as a fixture, for tests that prefer injection."""
    return run_cli


# ── Tests of the removed Wikidata-editing automation ─────────────────────────────────────────────
# The offline merge (2026-10-29) removed the automated Wikidata editing: pipeline.yml, wikidata-edits.yml,
# daily-batch-email.yml and scripts/wikidata-edit-run.py. Wikidata is edited only through QuickStatements
# (Emma, 2026-11-14: "Obv only quickstatements"). The tests below check that removed machinery, so they are
# skipped while it is absent, instead of failing CI; if it ever comes back they run again unchanged.
from pathlib import Path as _Path

_REPO = _Path(__file__).resolve().parents[1]
_REMOVED_AUTOMATION = [
    ".github/workflows/pipeline.yml",
    ".github/workflows/wikidata-edits.yml",
    ".github/workflows/daily-batch-email.yml",
    "scripts/wikidata-edit-run.py",
]
_AUTOMATION_TESTS = (
    "tests/test_pacific_schedule.py",
    "tests/test_wikidata_start_date.py",
    "tests/test_batch_issue_assignment.py",
    "tests/test_daily_batch_wiring.py",
    "tests/test_editorder.py",
    "tests/test_bot_identity.py::test_the_bot_scripts_do_not_hand_write_an_agent",
    "tests/test_patronymic_pairs_called.py::test_pipeline_or_name_items_calls_a_patronymic_pair_builder",
    "tests/test_repo_invariants.py::test_the_push_exemption_names_a_workflow_that_exists_and_uses_it",
)


def pytest_collection_modifyitems(config, items):
    missing = [p for p in _REMOVED_AUTOMATION if not (_REPO / p).exists()]
    if not missing:
        return
    mark = pytest.mark.skip(reason="tests the Wikidata-editing automation removed 2026-10-29 "
                                   "(missing: " + ", ".join(missing) + "); Wikidata is edited only through QuickStatements")
    for item in items:
        nodeid = item.nodeid.replace("\\", "/")
        if any(nodeid == t or nodeid.startswith(t + "::") or nodeid.startswith(t + "[") for t in _AUTOMATION_TESTS):
            item.add_marker(mark)


# The 2026-10-20 Garborg day batch is stale and set aside (header of reports/wikidata-garborg-day.txt; Emma's
# 2026-11-12 reset of the entry points toward Brandon Reese Taylor's relatives). Its two content guards check that
# stale file against the moved-on ledger, so they skip while the file carries the STALE header.
_GARBORG_BATCH = _REPO / "reports" / "wikidata-garborg-day.txt"
_GARBORG_CONTENT_TESTS = (
    "tests/test_garborg_day_batch.py::test_every_explicit_subject_already_exists",
    "tests/test_garborg_day_batch.py::test_a_label_is_never_written_over_an_item_that_already_has_one",
)


def _garborg_batch_is_stale() -> bool:
    try:
        with _GARBORG_BATCH.open(encoding="utf-8") as fh:
            return fh.readline().startswith("# ⛔ STALE")
    except OSError:
        return False


_previous_modifyitems = pytest_collection_modifyitems


def pytest_collection_modifyitems(config, items):  # noqa: F811 - extends the hook above
    _previous_modifyitems(config, items)
    if not _garborg_batch_is_stale():
        return
    mark = pytest.mark.skip(reason="reports/wikidata-garborg-day.txt is the stale 2026-10-20 batch, set aside")
    for item in items:
        if item.nodeid.replace("\\", "/") in _GARBORG_CONTENT_TESTS:
            item.add_marker(mark)
