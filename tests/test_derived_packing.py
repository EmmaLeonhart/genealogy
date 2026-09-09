"""The four big derived CSVs live in git gzipped. The two forms must not drift.

**Emma's call, 2026-08-24:** *"Imo gzip because this is long term and we aren't adding
any more data into our tree. Just processing."* Regenerated from the 546-export merge
they are 108–184 MiB each, and GitHub refuses anything over 100 MiB, so the plain
`.csv` is gitignored and the `.csv.gz` is committed.

That arrangement has one failure mode and it is silent: **a `.gz` that is missing or
stale while the working tree has a fresh `.csv`.** Everything keeps working for whoever
regenerated it, and a clean checkout gets nothing, or worse, gets a months-old version
of the file every emitter reads. This is the same shape as `6eddadd`, which moved 37
exports out of git and left a cloud session measuring a corpus half the size of the one
the reports described.

So: every named CSV has a committed `.gz`, no plain one is tracked, and each `.gz` is
under the limit it exists to respect.

**Freshness is deliberately not asserted.** A `.gz` older than its `.csv` is the normal
state while someone is regenerating, and a suite that goes red for that trains people to
ignore it. `scripts/pack-derived.py` is one command; what is pinned is that the pair
exists at all.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
LIMIT = 100 * 1024 * 1024

DERIVED = [
    "reports/display-names.csv",
    "reports/derived-facts.csv",
    "reports/derived-family.csv",
    "reports/derived-labels.csv",
]


def tracked(rel: str) -> bool:
    out = subprocess.run(["git", "ls-files", "--error-unmatch", rel],
                         cwd=REPO, capture_output=True, text=True)
    return out.returncode == 0


@pytest.mark.parametrize("rel", DERIVED)
def test_the_gzip_is_committed(rel):
    assert tracked(rel + ".gz"), (
        f"{rel}.gz is not tracked. A clean checkout would have no {rel} at all — "
        f"run scripts/pack-derived.py and commit it.")


@pytest.mark.parametrize("rel", DERIVED)
def test_the_plain_csv_is_not_tracked(rel):
    assert not tracked(rel), (
        f"{rel} is tracked and is over GitHub's 100 MiB limit; the push will fail. "
        f"It belongs in .gitignore with the .gz committed instead.")


@pytest.mark.parametrize("rel", DERIVED)
def test_the_gzip_is_under_the_limit_it_exists_for(rel):
    path = REPO / (rel + ".gz")
    if not path.exists():
        pytest.skip(f"{rel}.gz not present in this checkout")
    size = path.stat().st_size
    assert size < LIMIT, (
        f"{rel}.gz is {size / 1048576:.1f} MiB — gzip is no longer enough, and the "
        f"push will fail. Splitting is the next option in queue.md.")


def test_the_packer_names_exactly_the_files_gitignore_excludes():
    """Two lists of the same four files, in different files. Pin them together."""
    packer = (REPO / "scripts" / "pack-derived.py").read_text(encoding="utf-8")
    ignore = (REPO / ".gitignore").read_text(encoding="utf-8")
    for rel in DERIVED:
        assert f'"{rel}"' in packer, f"{rel} missing from pack-derived.py DERIVED"
        assert any(line.strip() == rel for line in ignore.splitlines()), (
            f"{rel} is not gitignored, so a regeneration would try to commit it")
