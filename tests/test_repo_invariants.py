"""Three invariants `CLAUDE.md` states, whose failure costs money, a cold clone,
or the corpus itself.

All three were enforced only by a sentence asking someone to remember, which is
the form already replaced elsewhere in this suite for the xref prefixes and the
Wikidata property table.

**Every GEDCOM committed is the corpus invariant.** `CLAUDE.md`: "Every GEDCOM
is committed. Never gitignore a `.ged`." It failed once, in `6eddadd`, which
moved 37 exports out of git on a size argument. Its failure mode is silent in
the worst way: the files stay on disk, every local run keeps working, and the
loss only shows up somewhere else — a clean checkout measuring 57 exports
against reports that describe 98, which is exactly what happened in a cloud
session on 2026-08-06.

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
#: **The repo went PUBLIC on 2026-09-01**, so Actions minutes are free and the cost
#: argument this set encoded no longer applies. Emma: *"The repo is public now lol"*, and
#: earlier that day *"I want to make this a public repo so we don't need to waste your
#: attention on the tests shit"*. `pull_request` and `schedule` are now wanted.
#:
#: **`push` stays out, for a different reason that survives the visibility change.** This
#: repo takes large generated files many times a day -- the 2026-09-01 label rebuild alone
#: rewrote three million lines -- so a run per push would queue behind itself and tell
#: nobody anything. That is a signal argument, not a billing one.
AUTOMATIC_TRIGGERS = {"push", "pull_request_target"}


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
        f"workflows now run on every push: {offenders}. The repo is public so this "
        "is no longer a billing question, but this repo commits large generated "
        "files many times a day and a run per push queues behind itself for no "
        "signal. Use schedule: or workflow_dispatch:. If it is being changed on "
        "purpose, change CLAUDE.md in the same commit."
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


# --- every GEDCOM is committed ----------------------------------------------


def _git(*args: str) -> str:
    """A git command in the repo, or "" if git cannot answer.

    Returns empty rather than raising so a checkout without git — a zip
    download, a sandbox — skips instead of failing on something that is not
    about the corpus at all.
    """
    import subprocess

    try:
        done = subprocess.run(
            ["git", "-C", str(REPO_ROOT), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return done.stdout if done.returncode == 0 else ""


def test_every_gedcom_on_disk_is_tracked_by_git():
    """The corpus on disk and the corpus in git must be the same set.

    Checked as a set difference rather than two counts, so the failure message
    names the files instead of a number that has to be chased down. Reported
    both ways: a `.ged` on disk and not in git is the `6eddadd` failure, and a
    `.ged` in git and not on disk means a file was deleted from the working
    tree.
    """
    listed = _git("ls-files", "exports")
    if not listed:
        pytest.skip("git cannot list files here")

    tracked = {line for line in listed.splitlines() if line.endswith(".ged")}
    on_disk = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "exports").rglob("*.ged")
    }
    if not on_disk and not tracked:
        pytest.skip("no exports in this checkout")

    untracked = sorted(on_disk - tracked)
    missing = sorted(tracked - on_disk)

    assert not untracked, (
        f"{len(untracked)} GEDCOMs are on disk but not in git, starting with "
        f"{untracked[:5]}. Tracking the exports is what this repo is for, and "
        "an untracked one is invisible to every other checkout while every "
        "local run keeps working — the reports then describe a corpus nobody "
        "else can read. Commit them; do not gitignore a .ged."
    )
    assert not missing, (
        f"{len(missing)} GEDCOMs are in git but gone from disk, starting with "
        f"{missing[:5]}. CLAUDE.md: never delete a GEDCOM. Restore them with "
        "`git checkout -- exports/` before anything else."
    )


def test_no_gitignore_rule_hides_a_gedcom():
    """The other half: nothing on disk is ignored *and* nothing new would be.

    The test above passes the moment a file is committed, even if the rule that
    hid it is still there — and a rule left in place silently swallows the next
    export to land in that directory. `git check-ignore --no-index` asks the
    rules directly rather than asking about the files that happen to exist now.
    """
    if not _git("rev-parse", "--git-dir"):
        pytest.skip("git cannot answer here")

    probes = [
        "exports/fleshing-out/export-geni/export-Forest-0.ged",
        "exports/stragglers/export-geni/export-Forest-40.ged",
        "exports/a-new-batch/export-geni/export-Forest-99.ged",
    ]
    hidden = [
        probe for probe in probes if _git("check-ignore", "--no-index", probe).strip()
    ]

    assert not hidden, (
        f".gitignore still hides GEDCOMs: {hidden}. Two of these are real files "
        "that 6eddadd hid on a size argument; the third is a path that does not "
        "exist yet, and it is there because a rule broad enough to hide it will "
        "swallow the next batch to arrive. Remove the rule. The zip lines are a "
        "separate, deliberate thing and stay."
    )


def test_no_gitignore_pattern_hides_a_zip_that_has_not_arrived_yet():
    """Zips are ignored one full path per line, and that is the whole point.

    An unlisted zip showing up in `git status` is how Emma sees a download has
    landed. A `*.zip` pattern would be tidier and would make every future
    download silent — the same class of loss as the `.ged` rule above, in the
    opposite direction. So the probe is a path that does not exist: any rule
    that matches it is a pattern, not a listing.
    """
    if not _git("rev-parse", "--git-dir"):
        pytest.skip("git cannot answer here")

    unarrived = "exports/a-new-batch/export-geni (999).zip"

    assert not _git("check-ignore", "--no-index", unarrived).strip(), (
        f".gitignore matches {unarrived}, a zip that does not exist, so it holds "
        "a pattern rather than a list. Zips are ignored one full path per line "
        "on purpose: an unlisted one appears in `git status`, which is the "
        "signal that a download has arrived. A pattern destroys that signal."
    )


def test_every_zip_on_disk_is_listed_in_gitignore():
    """The other half of the zip rule: listed, and listed individually.

    Read from `.gitignore` as text rather than via `check-ignore`, because
    `check-ignore` cannot tell "matched by its own line" from "matched by a
    pattern" and this test is about the first.
    """
    gitignore = REPO_ROOT / ".gitignore"
    if not gitignore.exists():
        pytest.skip("no .gitignore in this checkout")

    listed = {
        line.strip()
        for line in gitignore.read_text(encoding="utf-8").splitlines()
        if line.strip().endswith(".zip") and not line.lstrip().startswith("#")
    }
    on_disk = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in REPO_ROOT.rglob("*.zip")
        if ".git" not in path.parts
    }
    if not on_disk:
        pytest.skip("no zips in this checkout")

    unlisted = sorted(on_disk - listed)

    assert not unlisted, (
        f"{len(unlisted)} zips are on disk without a line of their own: "
        f"{unlisted[:5]}. That is the signal working — a new download is "
        "supposed to show up here. Add one line per file to .gitignore (never a "
        "pattern), extract the GEDCOM beside it, and commit the .ged."
    )


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


# -- exports/excluded/ ---------------------------------------------------


def _individual_ids(path):
    import re
    pattern = re.compile(r"^0 @I(\d+)@ INDI")
    with open(path, encoding="utf-8-sig", errors="replace") as handle:
        return {m.group(1) for m in
                (pattern.match(line) for line in handle) if m}


def test_no_excluded_export_strands_a_person():
    """Excluding a file must not remove anybody from the tree.

    **Emma's condition, 2026-08-15:** *"I want you to move them into an excluded
    directory or something like Samaritan's excluded and check to see if every
    single individual there is present in at least one other export."*

    She said it after I proposed excluding them *once* a later export covered
    their people — *"That is stupid. It's a prediction of something that may or
    may not happen."* So the check runs against the corpus as it stands, here,
    and an exclusion that would strand somebody fails the suite rather than
    quietly shrinking the tree.

    The four Samaritan exports were only excludable because
    `export-BloodTree-6000000178794141887.ged` arrived and covered the last
    1,091 — before it, exclusion would have lost Zipporah, Gershom, Eliezer and
    the Itamar-line placeholders.
    """
    from genimerge import sources

    excluded = sources.excluded_files()
    if not excluded:
        pytest.skip("nothing excluded")

    corpus = set()
    for path in sources.find_exports():
        corpus |= _individual_ids(path)
    assert corpus, "no corpus exports found"

    for path in excluded:
        stranded = _individual_ids(path) - corpus
        assert not stranded, (
            f"{path.name} is excluded from the merge but holds {len(stranded)} "
            f"people no corpus export has, e.g. {sorted(stranded)[:5]} - "
            "excluding it would delete them from the tree")


def test_excluded_exports_are_still_tracked_in_git():
    """Excluded from the merge is not deleted. `CLAUDE.md`: never lose a GEDCOM."""
    import subprocess

    from genimerge import sources

    excluded = sources.excluded_files()
    if not excluded:
        pytest.skip("nothing excluded")
    tracked = subprocess.run(
        ["git", "ls-files", "exports/excluded"],
        cwd=sources.REPO_ROOT, capture_output=True, text=True, check=True).stdout
    for path in excluded:
        assert path.name in tracked, f"{path.name} is excluded and untracked"
