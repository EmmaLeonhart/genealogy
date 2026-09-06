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

__all__ = ["EXPORTS_DIR", "EXCLUDED_DIR", "DERIVED_DIR", "DERIVED_DIRS", "REPO_ROOT",
           "find_exports", "geni_exports",
           "duplicate_groups", "excluded_files"]

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Everything under here is corpus **except `excluded/`**. Subdirectories are
#: Emma's filing — one per seed she exported from, plus `archive/` and
#: `fleshing-out/` for bulk takes — and carry no meaning for the merge.
EXPORTS_DIR = REPO_ROOT / "exports"

#: **The one subdirectory that is not corpus.** An export lands here when Geni
#: has since changed a relationship it records and the old edge would otherwise
#: survive forever: the merge unions `FAMC`/`CHIL` and never drops one, so a
#: parent link Geni has deleted cannot be removed by any later export. Excluding
#: the file is the only way it goes away.
#:
#: **The files stay in git.** `CLAUDE.md`'s rule is that a GEDCOM is never
#: deleted, and this does not weaken it — the export is still tracked, still
#: readable, still the record of what Geni said that day. It is only kept out of
#: the merge.
#:
#: **Emma's instruction, 2026-08-15**, after I proposed excluding them *once* a
#: later export covered their people: *"I want to exclude these particular ones,
#: not stop reading them once Export 204 covers their people. That is stupid.
#: It's a prediction of something that may or may not happen. I want you to move
#: them into an excluded directory or something like Samaritan's excluded and
#: check to see if every single individual there is present in at least one
#: other export."* The check is the condition, and it is checked **now** against
#: the corpus as it actually stands — `tests/test_repo_invariants.py` asserts
#: it, so an exclusion that would strand somebody fails the suite.
#:
#: `excluded/samaritans/` — four exports taken before `Yitzhaq I ben Tsedaka`
#: (`6000000227245553985`) existed on Geni. Geni had linked **Tsedaka II →
#: Abram** directly, skipping him; when Emma added him, Geni rewrote family
#: `F6000000178795360833` in place, swapping the child from Abram to Yitzhaq I.
#: The union of old and new gave that family both children and gave Abram two
#: fathers, one of them the other's father.
EXCLUDED_DIR = EXPORTS_DIR / "excluded"

#: **`exports/family-scrapes/` is corpus but is NOT a Geni export.** One tiny GEDCOM per scraped
#: profile, built by `scripts/build-family-gedcoms.py` -- Emma, 2026-09-06: *"this is what is
#: supposed to be the main result of the scrape ... the geni ids set up so that they end up
#: getting merged in"*. It belongs in the merge; it is not something Geni handed back, and must
#: not be measured as though it were.
#:
#: **It replaces `exports/0-scraped/`, which was DELETED on her instruction 2026-09-06** --
#: *"just delete them"*. Those two files were built by `build-scraped-gedcom.py`, which minted a
#: placeholder parent whenever a family wanted one, and they were in the merge the whole time:
#:
#:   * **4,928 invented `NN` people** carrying non-Geni `9995...` ids;
#:   * **5,750 children with more than two parents**, and every one of those 5,750 had at least
#:     two INVENTED parents.
#:
#: That is the source of the `9995000000000000074` fathers `CLAUDE.md` records in the parent deck.
#: The replacement invents nobody: every `INDI` it writes is a real Geni profile, and a family
#: with one known parent is written with one rather than being completed with a fiction.
#:
#: The two tests that caught the old directory the day it landed were both RIGHT and both still
#: apply to this one -- a generated file must not be measured against `GENI_EXPORT_CAP`, nor have
#: its sex coverage read as a corpus statistic. So the fix remains a name for the distinction
#: rather than a looser assertion: `find_exports` returns these (the merge wants them),
#: `geni_exports` excludes them (corpus-shape checks want only real ones).
#: ⛔ THERE ARE SEVERAL DERIVED DIRECTORIES NOW, and a single one was silently wrong.
#: `DERIVED_DIR` named one directory; the tiny GEDCOMs landed in two others, so on 2026-09-06
#: `geni_exports()` returned **1,309 files against `find_exports()`'s 1,309** -- 708 generated
#: files counted as things Geni handed back. That is the exact failure the distinction exists to
#: prevent: a generated file measured against `GENI_EXPORT_CAP`, or its sex coverage read as a
#: corpus statistic. `DERIVED_DIR` stays as the historical name; `DERIVED_DIRS` is the set every
#: caller should use.
DERIVED_DIRS = (
    EXPORTS_DIR / "tiny-profiles",   # one .ged per scraped profile
    EXPORTS_DIR / "tiny-paths",      # one .ged per relationship path
    EXPORTS_DIR / "0-scraped",       # the earlier aggregate pair, still in the merge
)
DERIVED_DIR = DERIVED_DIRS[0]


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


def _corpus_files(root: Path) -> list[Path]:
    """Every `.ged` under `root` that is corpus — i.e. not under `excluded/`.

    Matched on the path relative to `root` rather than absolutely, so a test
    pointing this at a temporary directory gets the same rule.
    """
    out = []
    for path in sorted(root.rglob("*.ged")):
        try:
            parts = path.relative_to(root).parts
        except ValueError:  # pragma: no cover - root is always a parent here
            parts = path.parts
        if EXCLUDED_DIR.name in parts[:-1]:
            continue
        out.append(path)
    return out


#: Exports taken AFTER Emma merged the duplicate profiles they contain. Everything in
#: here must be merged LAST, because `merge._merge_into` gives a single-valued conflict
#: to the later source and "later" means later in this list.
POST_MERGE_DIR = "post-merge"


def _post_merge_last(paths: list[Path], root: Path) -> list[Path]:
    """`exports/post-merge/` sorts to the END, whatever its name would do alphabetically.

    **Emma's design needs this and the obvious implementation does not provide it.**
    She asked for a directory whose records *"overwrite earlier ones from other repos in
    the synoptic tree"*. The merge already gives a conflict to the later source — but
    merge order is **path sort order**, and `post-merge` sorts at position 17 of 22
    under `exports/`: *before* `samaritans`, `sparse_filling`, `stragglers` and
    `tanba`.

    So a post-merge export would have lost to `tanba/` — the clan carrying the most
    stale duplicates, and the exact case the directory exists to fix. Naming it
    `post-merge` would have failed silently precisely where it was needed.

    Ordering it explicitly rather than renaming it `zz-post-merge` keeps the name
    meaningful and puts the rule where a reader will find it.
    """
    tail, head = [], []
    for path in paths:
        try:
            parts = path.relative_to(root).parts
        except ValueError:  # pragma: no cover - root is always a parent here
            parts = path.parts
        (tail if POST_MERGE_DIR in parts[:-1] else head).append(path)

    # **Inside the privileged directory, NEWEST wins — so order by mtime, not name.**
    # Two exports can be seeded on the same person: one taken before Emma merged a
    # duplicate and one after. Path order puts them in an arbitrary order, and worse, a
    # descriptive suffix reverses it -- `…141824-refresh.ged` sorts BEFORE
    # `…141824.ged`, because `-` is 0x2D and `.` is 0x2E. The refresh would have lost
    # to the very file it supersedes.
    #
    # Sorting by mtime says what the directory means: this is Geni's current state, and
    # the most recently exported file is the most current. Name order is kept as the
    # tiebreak so the result stays deterministic when two files share a timestamp.
    tail.sort(key=lambda p: (p.stat().st_mtime, p.name))
    return head + tail


def excluded_files(root: Path | None = None) -> list[Path]:
    """The exports deliberately kept out of the merge. Tracked, never read."""
    root = Path(root) if root is not None else EXPORTS_DIR
    excluded = root / EXCLUDED_DIR.name
    return sorted(excluded.rglob("*.ged")) if excluded.exists() else []


def find_exports(root: Path | None = None) -> list[Path]:
    """Every distinct export GEDCOM under `root`, in a stable order.

    Returns an empty list when `root` does not exist, so a checkout without the
    exports still runs — the tests skip on this rather than failing.
    """
    root = Path(root) if root is not None else EXPORTS_DIR
    if not root.exists():
        return []
    kept, _ = _distinct(_corpus_files(root))
    return _post_merge_last(kept, root)


def geni_exports(root: Path | None = None) -> list[Path]:
    """`find_exports` minus anything derived — only files Geni actually returned.

    Use this for any check about what a Geni export *is*: its size, its field coverage, its
    xref prefixes. Use `find_exports` for the merge, which wants the derived files too.
    """
    base = Path(root) if root is not None else EXPORTS_DIR
    derived = [base / d.name for d in DERIVED_DIRS]
    return [p for p in find_exports(root)
            if not any(d in p.parents for d in derived)]


def duplicate_groups(root: Path | None = None) -> dict[str, list[Path]]:
    """Byte-identical repeats under `root`, keyed by digest.

    Reported rather than silently dropped: a duplicate is usually a download
    taken twice, which is worth seeing.
    """
    root = Path(root) if root is not None else EXPORTS_DIR
    if not root.exists():
        return {}
    _, dupes = _distinct(_corpus_files(root))
    return dupes
