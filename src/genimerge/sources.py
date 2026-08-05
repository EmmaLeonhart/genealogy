"""Where the corpus of Geni exports lives.

**This is the only place that answers "which GEDCOMs are the corpus?".** It
exists because that question previously had six answers: `cli.Workspace` globbed
`data_lake/*.ged`, and five test modules each built the same glob for
themselves. Six copies of a path is five chances for them to disagree.

**`data_lake/` is gone, and was never meant to be load-bearing.** It was
scaffolding from the first session, when the job was to sort a pile of dropped
zips into somewhere tidy. It then acquired a naming scheme, an ingest ritual and
a rule that the merge read from it and nowhere else — none of which was ever a
decision, and all of which meant a newly downloaded export was invisible to
every command until it had been copied into a second location under a third
name. The exports are now read where they actually are.

**Duplicates are real and must be dropped by content.** `exports/` holds the
same file more than once as a matter of course: a download taken twice, a zip
extracted into two directories. Three exports in the 2026-08-05 batch were
byte-identical to a sibling. Counting one export twice would not change the
merged tree, which is keyed on the profile ID and idempotent, but it would
corrupt every *measurement* over the corpus — `inventory`'s overlap figures and
`density`'s presence counts both divide by how many exports contain a person.

**Order is by path, and that is not export order.** `merge` resolves conflicts
in favour of the later source, so the order here decides which value wins. Path
order is deterministic and stable, which is what a re-runnable merge needs, but
it is not the order the exports were taken in. If "later" ever needs to mean
"more recently exported", sort by the `HEAD` date inside each file — the same
caveat that applied when this was a flat directory.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path

__all__ = ["EXPORTS_DIR", "REPO_ROOT", "find_exports", "duplicate_groups"]

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Everything under here is corpus. Subdirectories are Emma's filing — one per
#: seed she exported from, plus `archive/` and `fleshing-out/` for bulk takes —
#: and carry no meaning for the merge.
EXPORTS_DIR = REPO_ROOT / "exports"


def _digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _distinct(paths: list[Path]) -> tuple[list[Path], dict[str, list[Path]]]:
    """Drop byte-identical repeats, keeping the first in path order.

    Files are grouped by size before anything is hashed. Two GEDCOMs of
    different length cannot be identical, and export sizes are mostly unique, so
    this reads a handful of files rather than the whole corpus — which matters
    because every command calls this on startup and the corpus is ~600 MB.
    """
    by_size: dict[int, list[Path]] = defaultdict(list)
    for p in paths:
        by_size[p.stat().st_size].append(p)

    kept: list[Path] = []
    dupes: dict[str, list[Path]] = {}
    for size, group in by_size.items():
        if len(group) == 1:
            kept.append(group[0])
            continue
        seen: dict[str, Path] = {}
        for p in group:
            d = _digest(p)
            if d in seen:
                dupes.setdefault(d, [seen[d]]).append(p)
            else:
                seen[d] = p
                kept.append(p)
    return sorted(kept), dupes


def find_exports(root: Path | None = None) -> list[Path]:
    """Every distinct export GEDCOM under `root`, in a stable order.

    Returns an empty list when `root` does not exist, so a checkout without the
    exports still runs — the tests skip on this rather than failing.
    """
    root = Path(root) if root is not None else EXPORTS_DIR
    if not root.exists():
        return []
    kept, _ = _distinct(sorted(root.rglob("*.ged")))
    return kept


def duplicate_groups(root: Path | None = None) -> dict[str, list[Path]]:
    """Byte-identical repeats under `root`, keyed by digest.

    Reported rather than silently dropped: a duplicate is usually a download
    taken twice, which is worth seeing.
    """
    root = Path(root) if root is not None else EXPORTS_DIR
    if not root.exists():
        return {}
    _, dupes = _distinct(sorted(root.rglob("*.ged")))
    return dupes
