"""Where the corpus comes from.

`genimerge.sources` replaced six copies of a `data_lake/*.ged` glob — one in the
CLI and one in each of five test modules. These check the two things that were
not true of the glob it replaced: it recurses, and it drops byte-identical
repeats.
"""

from pathlib import Path

import pytest

from genimerge import sources

GED = "0 HEAD\n1 SOUR Geni.com\n0 @I{n}@ INDI\n1 NAME A /B/\n0 TRLR\n"


def write(path: Path, n: int) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(GED.format(n=n), encoding="utf-8")
    return path


def test_it_finds_exports_in_subdirectories(tmp_path):
    """The exports live one directory per batch, which a flat glob missed.

    This is the bug that made the whole thing necessary: a newly downloaded
    export sat in `exports/fleshing-out/` and no command could see it until it
    had been copied to a second place under a third name.
    """
    write(tmp_path / "archive" / "export-geni" / "a.ged", 1)
    write(tmp_path / "fleshing-out" / "export-geni" / "b.ged", 2)
    write(tmp_path / "originals" / "c.ged", 3)

    found = sources.find_exports(tmp_path)

    assert [p.name for p in found] == ["a.ged", "b.ged", "c.ged"]


def test_byte_identical_repeats_are_dropped(tmp_path):
    """A download taken twice must count once.

    The merge would not care — it keys on the profile ID and is idempotent — but
    `inventory` and `density` both divide by how many exports contain a person,
    so a double-counted file silently corrupts every presence figure.
    """
    write(tmp_path / "one" / "export-Forest.ged", 7)
    write(tmp_path / "two" / "export-Forest.ged", 7)
    write(tmp_path / "three" / "different.ged", 8)

    found = sources.find_exports(tmp_path)

    assert len(found) == 2
    assert {p.name for p in found} == {"export-Forest.ged", "different.ged"}


def test_the_kept_copy_of_a_duplicate_is_the_first_in_path_order(tmp_path):
    """Which copy survives has to be deterministic, not filesystem order.

    `merge` resolves conflicts in favour of the later source, so an unstable
    choice here would make the merged output depend on directory iteration.
    """
    write(tmp_path / "zzz" / "dup.ged", 5)
    write(tmp_path / "aaa" / "dup.ged", 5)

    found = sources.find_exports(tmp_path)

    assert len(found) == 1
    assert found[0].parent.name == "aaa"


def test_duplicates_are_reported_rather_than_only_dropped(tmp_path):
    write(tmp_path / "one" / "x.ged", 4)
    write(tmp_path / "two" / "y.ged", 4)

    groups = sources.duplicate_groups(tmp_path)

    assert len(groups) == 1
    assert {p.name for p in next(iter(groups.values()))} == {"x.ged", "y.ged"}


def test_files_of_the_same_size_but_different_content_are_both_kept(tmp_path):
    """Size grouping is an optimisation and must not become the identity test.

    Only files of equal size are hashed, so a bug here would look like
    correct behaviour until two different exports happened to match in length.
    """
    (tmp_path / "a.ged").write_text("0 HEAD\n0 @I1@ INDI\n0 TRLR\n", encoding="utf-8")
    (tmp_path / "b.ged").write_text("0 HEAD\n0 @I2@ INDI\n0 TRLR\n", encoding="utf-8")
    assert (tmp_path / "a.ged").stat().st_size == (tmp_path / "b.ged").stat().st_size

    assert len(sources.find_exports(tmp_path)) == 2


def test_a_missing_directory_is_empty_rather_than_an_error(tmp_path):
    """A checkout without the exports still has to run; the tests skip on this."""
    assert sources.find_exports(tmp_path / "nope") == []
    assert sources.duplicate_groups(tmp_path / "nope") == {}


def test_non_gedcom_files_are_ignored(tmp_path):
    write(tmp_path / "a.ged", 1)
    (tmp_path / "export-geni.zip").write_bytes(b"PK\x03\x04not really")
    (tmp_path / "notes.txt").write_text("hello", encoding="utf-8")

    assert [p.name for p in sources.find_exports(tmp_path)] == ["a.ged"]


@pytest.mark.skipif(not sources.find_exports(), reason="no GEDCOM exports in exports/")
def test_the_real_corpus_has_no_byte_identical_duplicates():
    """Not a law — a statement about the repo right now, and worth knowing.

    Duplicates are dropped either way, so this failing is information rather
    than breakage: a download arrived twice. Three files in the 2026-08-05
    batch were repeats and were deleted once identified.
    """
    groups = sources.duplicate_groups()
    assert not groups, "byte-identical exports: " + "; ".join(
        ", ".join(str(p) for p in v) for v in groups.values()
    )


def test_post_merge_exports_are_merged_last(tmp_path):
    """`exports/post-merge/` must win a value conflict, and its NAME does not do that.

    Emma's design, 2026-08-24: exports taken after she merged the duplicate profiles
    they contain, whose records *"overwrite earlier ones from other repos in the
    synoptic tree"*.

    `merge._merge_into` already gives a single-valued conflict to the **later** source,
    and "later" means later in `find_exports`. But that was path-sort order, and
    `post-merge` sorts at position 17 of the 22 directories under `exports/` — before
    `samaritans`, `sparse_filling`, `stragglers` and `tanba`. A post-merge export would
    have lost to `tanba/`, the clan with the most stale duplicates and the very case the
    directory exists for.

    So this is a regression guard against the failure being silent: the ordering is
    explicit, not alphabetical luck.
    """
    for name in ("tanba", "post-merge", "samaritans", "aaa-first"):
        d = tmp_path / name
        d.mkdir()
        # Distinct sizes so `_distinct` keeps them all rather than de-duplicating.
        (d / f"export-{name}.ged").write_text(
            "0 HEAD\n" + f"0 @I{name}@ INDI\n" * (len(name) + 1), encoding="utf-8")

    got = sources.find_exports(tmp_path)
    names = [p.parent.name for p in got]
    assert names[-1] == "post-merge", (
        f"post-merge must be merged last so it wins value conflicts; got {names}")
    assert "tanba" in names[:-1] and "samaritans" in names[:-1]


def test_the_order_outside_post_merge_is_still_path_sorted(tmp_path):
    """Only post-merge moves. Everything else keeps the stable path order the merge
    report and the density counts have always assumed."""
    for name in ("bbb", "aaa", "ccc"):
        d = tmp_path / name
        d.mkdir()
        (d / f"export-{name}.ged").write_text(
            "0 HEAD\n" + f"0 @I{name}@ INDI\n" * (len(name) + len(name[0])),
            encoding="utf-8")
    names = [p.parent.name for p in sources.find_exports(tmp_path)]
    assert names == sorted(names)


def test_inside_post_merge_the_newest_export_wins_not_the_name(tmp_path):
    """A refresh of the same seed must beat the file it supersedes.

    Two exports can share a seed: one taken before Emma merged a duplicate on Geni and
    one after. The later file carries Geni's current state and must win the value
    conflict, which means it must be merged LAST.

    **Name order gets this exactly backwards.** `…141824-refresh.ged` sorts *before*
    `…141824.ged`, because `-` is 0x2D and `.` is 0x2E — so the refresh would have lost
    to the very file it replaces, silently. Ordering the privileged directory by mtime
    says what the directory means: most recently exported is most current.
    """
    import os
    d = tmp_path / "post-merge"
    d.mkdir()
    older = d / "export-Forest-111.ged"
    newer = d / "export-Forest-111-refresh.ged"
    older.write_text("0 HEAD\n0 @I1@ INDI\n", encoding="utf-8")
    newer.write_text("0 HEAD\n0 @I1@ INDI\n0 @I2@ INDI\n", encoding="utf-8")
    os.utime(older, (1_000_000, 1_000_000))
    os.utime(newer, (2_000_000, 2_000_000))

    assert newer.name < older.name, (
        "the premise of this test: the refresh sorts FIRST by name, which is the bug")

    got = [p.name for p in sources.find_exports(tmp_path)]
    assert got[-1] == newer.name, (
        f"the newest post-merge export must be merged last; got {got}")
