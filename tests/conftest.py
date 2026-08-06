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
