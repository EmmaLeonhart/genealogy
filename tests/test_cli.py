"""Tests for the command line, which had none.

Nine subcommands' worth of argument wiring, output paths and error handling
were exercised only by hand, so a broken command would have shipped green.

Everything here runs **offline** in a `tmp_path` workspace. Commands that need
Wikidata are covered for their wiring and for their "run the earlier step first"
error paths; whether Wikidata is up is not what these are testing.
"""

from pathlib import Path

import pytest

from conftest import run_cli

from genimerge import cli, gedcom

SMALL = """0 HEAD
1 SOUR Geni.com
0 @I1@ INDI
1 NAME Ada /Alpha/
2 GIVN Ada
2 SURN Alpha
1 SEX F
1 BIRT
2 DATE 1900
1 FAMS @F1@
1 RFN geni:1
0 @I2@ INDI
1 NAME Bo /Beta/
2 GIVN Bo
2 SURN Beta
1 SEX M
1 FAMS @F1@
1 RFN geni:2
0 @I3@ INDI
1 NAME Cy /Alpha/
2 GIVN Cy
2 SURN Alpha
1 FAMC @F1@
1 RFN geni:3
0 @F1@ FAM
1 HUSB @I2@
1 WIFE @I1@
1 CHIL @I3@
0 TRLR
"""

# A second export overlapping on Ada and adding a fourth person.
OTHER = """0 HEAD
1 SOUR Geni.com
0 @I1@ INDI
1 NAME Ada /Alpha/
1 DEAT
2 DATE 1970
1 RFN geni:1
0 @I4@ INDI
1 NAME Di /Delta/
1 RFN geni:4
0 TRLR
"""


@pytest.fixture
def workspace(tmp_path):
    """A complete workspace: a data lake with two exports, empty out/reports."""
    lake = tmp_path / "lake"
    lake.mkdir()
    (lake / "one.ged").write_text(SMALL, encoding="utf-8", newline="\n")
    (lake / "two.ged").write_text(OTHER, encoding="utf-8", newline="\n")
    return {
        "lake": lake,
        "out": tmp_path / "out",
        "reports": tmp_path / "reports",
    }


#: Every CLI invocation in these tests goes through the shared helper, so the
#: workspace flag names live in exactly one place. They were written out here
#: and again in test_cli_wikidata.py until 2026-08-05, when renaming
#: --data-lake broke the copy nobody remembered.
run = run_cli


# -- the parser --------------------------------------------------------

COMMANDS = [
    "inventory",
    "merge",
    "export",
    "overlap",
    "reconcile",
    "expand",
    "frontier",
    "consistency",
    "seeds",
    "coverage",
    "quickstatements",
    "names",
    "profile-names",
    "wikidata-download",
    "name-links",
    "crosscheck",
    "entity-resolution",
    "density",
    "descendants",
    "distant",
    "remote",
    "doubles",
    "connectors",
    "path",
    "path-from-html",
]

#: Commands with a required positional argument, and something to satisfy it.
#: The dispatch test only checks that a command resolves to a function, so the
#: value is never opened and need not exist.
REQUIRED_ARGS = {
    "path": ["some-path-file.tsv"],
    "path-from-html": ["some-page.html", "-o", "some-path-file.tsv"],
}


def test_every_command_is_registered():
    sub = next(
        a for a in cli.build_parser()._actions if hasattr(a, "choices") and a.choices
    )

    assert sorted(sub.choices) == sorted(COMMANDS)


@pytest.mark.parametrize("command", COMMANDS)
def test_every_command_dispatches_to_a_function(command):
    args = cli.build_parser().parse_args([command] + REQUIRED_ARGS.get(command, []))

    assert callable(args.func)


@pytest.mark.parametrize("command", COMMANDS)
def test_every_command_has_help(command, capsys):
    with pytest.raises(SystemExit) as exit_info:
        cli.build_parser().parse_args([command, "--help"])

    assert exit_info.value.code == 0
    assert command.split("-")[0] in capsys.readouterr().out.lower()


@pytest.mark.parametrize("command", COMMANDS)
def test_every_command_accepts_the_workspace_options(command):
    # Added in a loop precisely so a new command cannot miss them.
    args = cli.build_parser().parse_args(
        [command]
        + REQUIRED_ARGS.get(command, [])
        + ["--exports-dir", "a", "--out", "b", "--reports", "c"]
    )
    ws = cli.Workspace.from_args(args)

    assert (ws.exports_dir.name, ws.out.name, ws.reports.name) == ("a", "b", "c")


def test_an_unknown_command_is_rejected():
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["nonsense"])


def test_the_workspace_falls_back_to_the_repo_paths():
    ws = cli.Workspace.from_args(cli.build_parser().parse_args(["merge"]))

    assert ws.out == cli.OUT and ws.reports == cli.REPORTS


# -- the offline pipeline ----------------------------------------------


def test_inventory_writes_a_report(workspace, capsys):
    assert run(workspace, "inventory") == 0

    report = workspace["reports"] / "inventory.md"
    assert report.exists()
    assert "# Export inventory" in report.read_text(encoding="utf-8")
    assert "2 exports" in capsys.readouterr().out


def test_merge_writes_the_gedcom_and_both_reports(workspace):
    assert run(workspace, "merge") == 0

    merged = workspace["out"] / "merged.ged"
    assert merged.exists()
    assert (workspace["out"] / "merge-report.md").exists()
    assert (workspace["reports"] / "merge.md").exists()

    doc = gedcom.parse_file(merged)
    assert doc.warnings == []
    assert sorted(r.xref for r in doc.records if r.tag == "INDI") == [
        "@I1@",
        "@I2@",
        "@I3@",
        "@I4@",
    ]


def test_the_merge_actually_merged_the_two_exports(workspace):
    run(workspace, "merge")
    doc = gedcom.parse_file(workspace["out"] / "merged.ged")
    ada = doc.by_xref()["@I1@"]

    # Birth from one export, death from the other, on one record.
    assert ada.path_value("BIRT", "DATE") == "1900"
    assert ada.path_value("DEAT", "DATE") == "1970"


def test_export_writes_both_jsonl_files(workspace):
    run(workspace, "merge")
    assert run(workspace, "export") == 0

    people = workspace["out"] / "people.jsonl"
    families = workspace["out"] / "families.jsonl"
    assert len(people.read_text(encoding="utf-8").strip().splitlines()) == 4
    assert len(families.read_text(encoding="utf-8").strip().splitlines()) == 1


def test_export_merges_the_lake_when_there_is_no_merged_file(workspace):
    # No `merge` run first: it should still produce a full dataset.
    assert run(workspace, "export") == 0

    people = (workspace["out"] / "people.jsonl").read_text(encoding="utf-8")
    assert len(people.strip().splitlines()) == 4


def test_frontier_writes_its_report(workspace):
    run(workspace, "merge")
    assert run(workspace, "frontier") == 0

    text = (workspace["reports"] / "frontier.md").read_text(encoding="utf-8")
    assert "# Expansion frontier" in text


def test_descendants_writes_its_report_and_a_seed_list(workspace):
    run(workspace, "merge")
    assert run(workspace, "descendants", "--present", "2026") == 0

    text = (workspace["reports"] / "descendants.md").read_text(encoding="utf-8")
    assert "# Lines that stop early" in text
    assert "## By period" in text
    # `--present` is honoured, so the report is reproducible year to year.
    assert "2026" in text
    assert (workspace["out"] / "stalled-line-seeds.txt").exists()


def test_seeds_writes_a_report_and_a_csv(workspace):
    run(workspace, "merge")
    assert run(workspace, "seeds") == 0

    text = (workspace["reports"] / "seeds.md").read_text(encoding="utf-8")
    assert "# Export seeds" in text
    assert "What this cannot tell you" in text  # the limits stay in the report

    rows = (workspace["out"] / "seeds.csv").read_text(encoding="utf-8").splitlines()
    assert rows[0].startswith("order,geni_id,name,url")
    assert len(rows) > 1


def test_seeds_accepts_each_export_style(workspace):
    run(workspace, "merge")
    for style in ("blood", "all", "ancestors", "descendants"):
        assert run(workspace, "seeds", "--style", style) == 0


def test_seeds_refuses_a_style_geni_does_not_offer(workspace):
    run(workspace, "merge")
    with pytest.raises(SystemExit):
        run(workspace, "seeds", "--style", "cousins")


def test_the_documented_pipeline_runs_end_to_end(workspace):
    # The offline half of the sequence in README.md, in order.
    for command in ("inventory", "merge", "export", "frontier"):
        assert run(workspace, command) == 0, command

    for path in (
        workspace["reports"] / "inventory.md",
        workspace["out"] / "merged.ged",
        workspace["out"] / "people.jsonl",
        workspace["out"] / "families.jsonl",
        workspace["reports"] / "frontier.md",
    ):
        assert path.exists() and path.stat().st_size > 0, path


def test_nothing_is_written_outside_the_workspace(workspace, tmp_path):
    run(workspace, "merge")
    written = {p for p in tmp_path.rglob("*") if p.is_file()}

    assert written  # the run did something
    assert all(
        workspace["out"] in p.parents
        or workspace["reports"] in p.parents
        or workspace["lake"] in p.parents
        for p in written
    )


# -- explicit output paths ---------------------------------------------


def test_an_explicit_output_path_is_honoured(workspace, tmp_path):
    target = tmp_path / "elsewhere" / "inv.md"
    assert run(workspace, "inventory", "-o", str(target)) == 0

    assert target.exists()
    assert not (workspace["reports"] / "inventory.md").exists()


def test_export_can_be_pointed_at_another_directory(workspace, tmp_path):
    target = tmp_path / "jsonl"
    assert run(workspace, "export", "-o", str(target)) == 0

    assert (target / "people.jsonl").exists()


# -- failure paths -----------------------------------------------------


def test_an_empty_exports_dir_fails_with_a_useful_message(tmp_path, capsys):
    empty = {"lake": tmp_path / "empty", "out": tmp_path / "o", "reports": tmp_path / "r"}
    empty["lake"].mkdir()

    assert run(empty, "inventory") == 1
    assert "no .ged files" in capsys.readouterr().err


def test_expand_refuses_to_run_before_reconcile(workspace, capsys):
    assert run(workspace, "expand") == 1
    assert "run `genimerge reconcile` first" in capsys.readouterr().err


def test_quickstatements_refuses_to_run_before_expand(workspace, capsys):
    assert run(workspace, "quickstatements") == 1
    assert "expand" in capsys.readouterr().err


def test_crosscheck_refuses_to_run_before_there_are_matches(workspace, capsys):
    assert run(workspace, "crosscheck") == 1
    assert "reconcile" in capsys.readouterr().err


def test_name_links_refuses_to_run_before_there_are_matches(workspace, capsys):
    assert run(workspace, "name-links") == 1
    assert "reconcile" in capsys.readouterr().err


def test_coverage_refuses_to_run_before_there_are_matches(workspace, capsys):
    assert run(workspace, "coverage") == 1
    assert "reconcile" in capsys.readouterr().err


# -- merge reports connectivity ----------------------------------------


def test_merge_says_whether_the_result_is_still_one_tree(workspace, capsys):
    """The conflict count cannot answer this, so `merge` prints it separately.

    The workspace fixture happens to be exactly the case worth catching: `two.ged`
    adds Di Delta with no family links, so the merge succeeds with zero conflicts
    and still produces two trees. That is what an export seeded outside the tree
    looks like from the merge's point of view — nothing contradicts anything, the
    halves simply never meet.
    """
    assert run(workspace, "merge") == 0

    out = capsys.readouterr().out
    assert "0 conflicts" in out
    assert "2 separate trees, not one: 3, 1 people" in out


def test_merge_reports_one_tree_when_everything_connects(workspace, capsys):
    (workspace["lake"] / "two.ged").unlink()

    assert run(workspace, "merge") == 0

    assert "one connected tree, all 3 people" in capsys.readouterr().out


# -- merge --output keeps its reports with its output ------------------------
#
# `reports/merge.md` is tracked in git. A merge written somewhere else must not
# overwrite the workspace's description of a different merge — that is exactly
# what happened when a three-export tree was rebuilt into a scratch directory
# and the repository's merge.md came back saying 8766 people while
# out/merged.ged held 12422.


def test_merge_output_elsewhere_does_not_touch_the_workspace_reports(workspace, tmp_path):
    run(workspace, "merge")
    summary = workspace["reports"] / "merge.md"
    before = summary.read_text(encoding="utf-8")

    # A different merge — one export, not two — sent somewhere else entirely.
    elsewhere = tmp_path / "side" / "other.ged"
    assert run(workspace, "merge", str(workspace["lake"] / "one.ged"), "-o", str(elsewhere)) == 0

    assert summary.read_text(encoding="utf-8") == before


def test_merge_output_elsewhere_writes_its_reports_beside_itself(workspace, tmp_path):
    elsewhere = tmp_path / "side" / "other.ged"

    assert run(workspace, "merge", "-o", str(elsewhere)) == 0

    assert elsewhere.exists()
    assert (elsewhere.parent / "merge.md").exists()
    assert (elsewhere.parent / "merge-report.md").exists()


def test_merge_without_output_still_writes_into_the_workspace(workspace):
    assert run(workspace, "merge") == 0

    assert (workspace["out"] / "merged.ged").exists()
    assert (workspace["out"] / "merge-report.md").exists()
    assert (workspace["reports"] / "merge.md").exists()


def test_the_redirected_report_describes_the_redirected_merge(workspace, tmp_path):
    """Not just placed correctly — about the right merge.

    The bug was a report describing a different set of sources from the GEDCOM
    beside it, so placement alone is not the property worth asserting.
    """
    elsewhere = tmp_path / "side" / "other.ged"

    run(workspace, "merge", str(workspace["lake"] / "one.ged"), "-o", str(elsewhere))

    side = (elsewhere.parent / "merge.md").read_text(encoding="utf-8")
    assert "one.ged" in side
    assert "two.ged" not in side


# -- a redirected run must not touch the repository --------------------------
#
# README promises: "Every command also takes --exports-dir, --out and --reports,
# so a second dataset can be processed without touching the first."
#
# This asserts that promise for the family, so a new or edited command writing
# to a workspace-independent path fails here rather than silently overwriting
# tracked files.
#
# **It would not have caught the bug that prompted it**, and the distinction
# matters. `reports/merge.md` went stale because `merge -o elsewhere` was run
# *without* `--reports`, so the reports fell back to the repository default
# while the GEDCOM went to the target. Every run here passes all three
# directories, which was always the safe case. That specific shape is covered by
# `test_merge_output_elsewhere_does_not_touch_the_workspace_reports` above.
# What this adds is the README's stated guarantee, which is adjacent to that bug
# rather than the same thing.
#
# Five of the eleven commands. `reconcile`, `expand`, `coverage`, `crosscheck`,
# `names` and `name-links` need Wikidata and this suite is offline on purpose —
# they are also the ones that write cache files, so they are the likelier place
# for a stray path. Uncovered, and said so rather than implied.

REPO_ROOT = Path(__file__).resolve().parents[1]
OFFLINE_COMMANDS = ["inventory", "merge", "export", "frontier", "seeds"]


def _stamp(*directories):
    """Size and mtime of every file under `directories`.

    Not a content hash: any write updates mtime, and hashing the tens of
    megabytes in merged.ged and people.jsonl on every run buys nothing.
    """
    seen = {}
    for directory in directories:
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                info = path.stat()
                seen[str(path)] = (info.st_size, info.st_mtime_ns)
    return seen


def test_a_redirected_run_leaves_the_repository_untouched(workspace):
    repo_dirs = (REPO_ROOT / "reports", REPO_ROOT / "out")
    before = _stamp(*repo_dirs)

    for command in OFFLINE_COMMANDS:
        assert run(workspace, command) == 0, f"{command} failed in a redirected workspace"

    after = _stamp(*repo_dirs)

    changed = sorted(k for k in before if before[k] != after.get(k))
    appeared = sorted(k for k in after if k not in before)
    assert not changed, f"a redirected run rewrote tracked files: {changed}"
    assert not appeared, f"a redirected run created files in the repository: {appeared}"


def test_the_redirected_run_did_write_its_own_workspace(workspace):
    """Guards the guard: if the commands wrote nothing, the check above is vacuous."""
    for command in OFFLINE_COMMANDS:
        run(workspace, command)

    written = _stamp(workspace["out"], workspace["reports"])

    assert len(written) >= len(OFFLINE_COMMANDS)
    assert any(k.endswith("merged.ged") for k in written)
    assert any(k.endswith("seeds.md") for k in written)
