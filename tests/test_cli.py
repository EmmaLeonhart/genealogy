"""Tests for the command line, which had none.

Nine subcommands' worth of argument wiring, output paths and error handling
were exercised only by hand, so a broken command would have shipped green.

Everything here runs **offline** in a `tmp_path` workspace. Commands that need
Wikidata are covered for their wiring and for their "run the earlier step first"
error paths; whether Wikidata is up is not what these are testing.
"""

import pytest

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


def run(ws, *argv):
    """Run the CLI against the workspace, returning its exit code."""
    return cli.main(
        [
            *argv,
            "--data-lake",
            str(ws["lake"]),
            "--out",
            str(ws["out"]),
            "--reports",
            str(ws["reports"]),
        ]
    )


# -- the parser --------------------------------------------------------

COMMANDS = [
    "inventory",
    "merge",
    "export",
    "reconcile",
    "expand",
    "frontier",
    "coverage",
    "quickstatements",
    "names",
    "name-links",
    "crosscheck",
]


def test_every_command_is_registered():
    sub = next(
        a for a in cli.build_parser()._actions if hasattr(a, "choices") and a.choices
    )

    assert sorted(sub.choices) == sorted(COMMANDS)


@pytest.mark.parametrize("command", COMMANDS)
def test_every_command_dispatches_to_a_function(command):
    args = cli.build_parser().parse_args([command])

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
        [command, "--data-lake", "a", "--out", "b", "--reports", "c"]
    )
    ws = cli.Workspace.from_args(args)

    assert (ws.data_lake.name, ws.out.name, ws.reports.name) == ("a", "b", "c")


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


def test_an_empty_data_lake_fails_with_a_useful_message(tmp_path, capsys):
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
