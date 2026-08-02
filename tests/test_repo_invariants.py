"""Two invariants `CLAUDE.md` states, whose failure costs money or a cold clone.

Both were enforced only by a sentence asking someone to remember, which is the
form already replaced elsewhere in this suite for the xref prefixes and the
Wikidata property table.

**The CI trigger is a billing invariant.** `CLAUDE.md`: "Never add a `push:` or
`pull_request:` trigger to `.github/workflows/`. Actions minutes are free on
public repos but billable on private ones once the monthly allowance is used,
and a surprise bill is not worth a green tick." Its failure mode is the nasty
kind — adding `on: push` makes the repository start producing green ticks, so
the thing going wrong looks exactly like the thing going right, and the first
real signal is an invoice.

**Stdlib-only is a cold-clone invariant.** `pyproject.toml` declares
`dependencies = []`. A stray third-party import keeps working for whoever
already has the package installed and fails for everybody else.

What these cannot check, stated rather than left to be discovered: whether the
workflow is *also* disabled at the GitHub end, which `CLAUDE.md` claims and
which is a remote setting no local test can see; and dependencies pulled in at
runtime rather than by import.
"""

import ast
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = REPO_ROOT / ".github" / "workflows"
PACKAGE = REPO_ROOT / "src" / "genimerge"

#: Triggers that make GitHub run a workflow without anybody asking, which on a
#: private repository means billable minutes per event.
AUTOMATIC_TRIGGERS = {"push", "pull_request", "pull_request_target", "schedule"}


def _triggers(text: str) -> set[str]:
    """The top-level keys under a workflow's `on:`.

    Scanned as text on purpose. Reading YAML properly would mean adding PyYAML,
    and adding a dependency to check that no dependencies were added is a poor
    trade. Comments are stripped first because `ci.yml` explains *why* it has no
    `push:` trigger, and a naive search finds that explanation.
    """
    lines = [line.split("#", 1)[0].rstrip() for line in text.splitlines()]
    for index, line in enumerate(lines):
        if not re.match(r"""^(on|"on"|'on'):""", line):
            continue
        inline = line.split(":", 1)[1].strip()
        if inline:                                   # `on: push` or `on: [push]`
            return set(re.findall(r"[A-Za-z_]+", inline))
        found = set()
        for rest in lines[index + 1:]:
            if not rest.strip():
                continue
            if not rest.startswith((" ", "\t")):     # dedent ends the block
                break
            key = re.match(r"[ \t]{1,2}([A-Za-z_]+):", rest)
            if key:
                found.add(key.group(1))
        return found
    return set()


def _imports(path: Path) -> set[tuple[int, str]]:
    """Absolute imports, as (line number, top-level module).

    Parsed rather than pattern-matched. The first version scanned lines for
    `^(import|from)\\s+(\\w+)` and reported `seeds.py:5` importing a module
    called `that` — the docstring there wraps onto a line beginning "from that
    profile until the export is full". Prose that looks like code is exactly the
    trap the trigger reader above strips comments for, and a regex cannot tell
    the difference. `ast` can, and it is standard library.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add((node.lineno, alias.name.split(".")[0]))
        elif isinstance(node, ast.ImportFrom):
            # level > 0 is a relative import: `.model`, not a dependency.
            if node.level == 0 and node.module:
                found.add((node.lineno, node.module.split(".")[0]))
    return found


# --- the workflow triggers --------------------------------------------------


@pytest.mark.skipif(not WORKFLOWS.exists(), reason="no .github/workflows in this checkout")
def test_no_workflow_runs_automatically():
    offenders = {}
    for workflow in sorted(WORKFLOWS.glob("*.y*ml")):
        automatic = _triggers(workflow.read_text(encoding="utf-8")) & AUTOMATIC_TRIGGERS
        if automatic:
            offenders[workflow.name] = sorted(automatic)

    assert not offenders, (
        f"workflows now run without being asked: {offenders}. This repository is "
        "private, where Actions minutes are billable once the free allowance is "
        "gone. That is a cost decision, not a config detail — if it is being made "
        "on purpose, change CLAUDE.md in the same commit."
    )


@pytest.mark.skipif(not WORKFLOWS.exists(), reason="no .github/workflows in this checkout")
def test_every_workflow_can_still_be_run_by_hand():
    """The other half: manual-only must not become never."""
    for workflow in sorted(WORKFLOWS.glob("*.y*ml")):
        assert "workflow_dispatch" in _triggers(workflow.read_text(encoding="utf-8")), (
            f"{workflow.name} has no trigger at all and can never run."
        )


def test_the_trigger_reader_ignores_prose_about_triggers():
    """`ci.yml` explains why it has no `push:`; a naive search finds that text.

    This is the assertion that keeps the guard honest — without it, the check
    could be reading comments and nobody would know until it failed on one.
    """
    commented = "# Re-adding a `push:` trigger means billing\non:\n  workflow_dispatch:\n"

    assert _triggers(commented) == {"workflow_dispatch"}


def test_the_trigger_reader_catches_every_form_a_trigger_can_take():
    assert _triggers("on:\n  push:\n    branches: [main]\n") == {"push"}
    assert _triggers("on: push\n") == {"push"}
    assert _triggers("on: [push, pull_request]\n") == {"push", "pull_request"}
    assert _triggers('"on":\n  schedule:\n    - cron: "0 0 * * *"\n') == {"schedule"}
    # nested keys are not triggers
    assert "branches" not in _triggers("on:\n  push:\n    branches: [main]\n")


# --- stdlib only ------------------------------------------------------------


def test_the_package_imports_nothing_outside_the_standard_library():
    third_party = {}
    for module in sorted(PACKAGE.glob("*.py")):
        for number, name in sorted(_imports(module)):
            if name not in sys.stdlib_module_names and name != "genimerge":
                third_party.setdefault(f"{module.name}:{number}", name)

    assert not third_party, (
        f"the package imports something outside the standard library: {third_party}. "
        "pyproject.toml declares dependencies = [], so this passes for whoever "
        "installed it and fails on a cold clone. Add it to pyproject.toml and to "
        "CLAUDE.md's stdlib-only note, or do without it."
    )


def test_the_import_reader_finds_a_third_party_import(tmp_path):
    """Proof it is not vacuous: every real module passes, so a broken reader looks fine."""
    module = tmp_path / "example.py"
    module.write_text(
        "import json\nimport requests\nfrom .local import thing\nimport os.path\n",
        encoding="utf-8",
    )

    names = {name for _, name in _imports(module)}

    assert "requests" in names
    assert "json" in names
    assert "os" in names                 # dotted imports report their root
    assert "local" not in names          # relative imports are not dependencies
    assert "requests" not in sys.stdlib_module_names


def test_the_import_reader_is_not_fooled_by_prose_that_looks_like_an_import(tmp_path):
    """The false positive the first version of this actually produced.

    `seeds.py`'s docstring wraps onto a line starting "from that profile until
    the export is full", which a line-based reader reported as importing `that`.
    """
    module = tmp_path / "prose.py"
    module.write_text(
        '"""A ball is walked outward\n'
        'from that profile until the export is full.\n'
        '\n'
        'import nothing at all\n'
        '"""\n'
        "import json\n",
        encoding="utf-8",
    )

    assert {name for _, name in _imports(module)} == {"json"}
