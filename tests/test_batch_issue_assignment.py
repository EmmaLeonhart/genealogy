"""The daily batch issue is assigned to the owner until 2026-10-05 and to nobody from that day.

Queue item (Emma, 2026-09-25): ten days on, the QuickStatements are routine; keep opening the
issue, stop assigning it. Both workflows that open one carry the same one-line helper, and this
runs it with node on both sides of the date.
"""
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
WORKFLOWS = ["daily-batch-email.yml", "pipeline.yml"]
FN = re.compile(r"^\s*(function assigneesOn\(today, owner\) \{.*\})\s*$", re.M)


@pytest.mark.parametrize("name", WORKFLOWS)
def test_the_issue_is_assigned_through_the_dated_helper(name):
    src = (REPO / ".github" / "workflows" / name).read_text(encoding="utf-8")
    assert len(FN.findall(src)) == 1
    assert "assignees: [context.repo.owner]" not in src
    assert src.count("assignees: assigneesOn(new Date().toISOString().slice(0, 10), "
                     "context.repo.owner)") == src.count("issues.create(")


@pytest.mark.skipif(not shutil.which("node"), reason="node is not installed")
@pytest.mark.parametrize("name", WORKFLOWS)
@pytest.mark.parametrize("today,expected", [("2026-10-04", '["Owner"]'),
                                            ("2026-10-05", "[]"),
                                            ("2027-01-01", "[]")])
def test_both_sides_of_the_date(name, today, expected):
    src = (REPO / ".github" / "workflows" / name).read_text(encoding="utf-8")
    fn = FN.search(src).group(1)
    out = subprocess.run(["node", "-e", f"{fn}\nconsole.log(JSON.stringify(assigneesOn('{today}', 'Owner')))"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert out == expected
