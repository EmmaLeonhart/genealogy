"""Check the sources against the Python floor `pyproject.toml` advertises.

**What this is not:** running the test suite on that floor. Only CI does that,
and CI has stopped running (a GitHub billing block — see `queue.md`). The only
interpreter on the development machine is 3.13, so without something like this
a 3.11-only construct could land and nothing would notice until somebody on the
floor version tried to install the package.

So this catches the cheap class of breakage — syntax the floor cannot parse, and
stdlib names that did not exist yet — and deliberately does not pretend to catch
the rest. Behavioural differences between versions are exactly what it misses.

The floor is read out of `pyproject.toml` rather than hardcoded, so raising it
updates this check too.
"""

import ast
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = sorted((REPO_ROOT / "src" / "genimerge").glob("*.py"))

#: The tests have to run on the floor too — CI runs them there — so they get the
#: syntax check. They do *not* get the name check: this very file lists the
#: forbidden names as data, and would report itself.
ALL_PYTHON = SOURCE_FILES + sorted((REPO_ROOT / "tests").glob("*.py"))

#: Stdlib names introduced after 3.10. Not exhaustive — a short list of the
#: things most likely to be reached for by habit.
TOO_NEW = {
    "tomllib": "3.11",
    "datetime.UTC": "3.11",
    "typing.Self": "3.11",
    "assert_never": "3.11",
    "ExceptionGroup": "3.11",
    "LiteralString": "3.11",
    "asyncio.TaskGroup": "3.11",
    "enum.StrEnum": "3.11",
    "hashlib.file_digest": "3.11",
    "itertools.batched": "3.12",
    "Path.walk": "3.12",
    "typing.override": "3.12",
    "warnings.deprecated": "3.13",
}


def floor() -> tuple[int, int]:
    """The minimum Python from `pyproject.toml`.

    Parsed with a regex rather than `tomllib`, because `tomllib` is itself
    3.11+ and importing it would stop this very test running on the floor it
    is checking.
    """
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'requires-python\s*=\s*"\s*>=\s*(\d+)\.(\d+)', text)
    assert match, "pyproject.toml does not declare a requires-python floor"
    return int(match.group(1)), int(match.group(2))


def test_the_floor_is_declared_and_plausible():
    major, minor = floor()

    assert major == 3
    assert 8 <= minor <= 20  # a sanity range, not a policy


def test_there_are_source_files_to_check():
    # Guards against this whole file passing vacuously if the layout moves.
    assert len(SOURCE_FILES) >= 10


@pytest.mark.parametrize("path", ALL_PYTHON, ids=lambda p: p.name)
def test_every_python_file_parses_at_the_declared_floor(path):
    source = path.read_text(encoding="utf-8")

    # feature_version rejects syntax newer than the floor: match statements
    # below 3.10, `except*` below 3.11, PEP 695 type parameters below 3.12.
    ast.parse(source, filename=str(path), feature_version=floor())


@pytest.mark.parametrize("path", SOURCE_FILES, ids=lambda p: p.name)
def test_no_source_file_reaches_for_a_too_new_stdlib_name(path):
    source = path.read_text(encoding="utf-8")
    major, minor = floor()

    offenders = []
    for name, introduced in TOO_NEW.items():
        if tuple(int(p) for p in introduced.split(".")) <= (major, minor):
            continue  # the floor has caught up; no longer a problem
        if re.search(rf"\b{re.escape(name)}\b", source):
            offenders.append(f"{name} (Python {introduced})")

    assert not offenders, (
        f"{path.name} uses names newer than the declared floor "
        f"{major}.{minor}: {', '.join(offenders)}"
    )


def test_the_parse_check_would_actually_reject_something_too_new():
    """Prove the check bites, so the parametrised passes above mean something."""
    match_statement = "match 1:\n    case 1:\n        pass\n"

    ast.parse(match_statement, feature_version=(3, 10))  # fine at the floor
    with pytest.raises(SyntaxError):
        ast.parse(match_statement, feature_version=(3, 9))


def test_the_name_check_would_actually_catch_an_offender(tmp_path):
    """Same again for the denylist: a file that offends must fail."""
    major, minor = floor()
    offending = "import tomllib\n"

    found = [
        name
        for name, introduced in TOO_NEW.items()
        if tuple(int(p) for p in introduced.split(".")) > (major, minor)
        and re.search(rf"\b{re.escape(name)}\b", offending)
    ]

    assert found == ["tomllib"]
