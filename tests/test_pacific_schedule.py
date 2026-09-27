"""The scheduled pipeline and edit runs start at 06:00 and 18:00 Pacific (queue item, 2026-09-26).

GitHub cron is UTC and ignores daylight saving, so both workflows schedule all four UTC slots and
a one-line `pacific_slot` keeps the two that are 06:00 and 18:00 Pacific on the day. This runs
that line with bash on both sides of the November and March switches.
"""
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
WORKFLOWS = ["pipeline.yml", "wikidata-edits.yml"]
SLOTS = {"0 13 * * *", "0 1 * * *", "0 14 * * *", "0 2 * * *"}
FN = re.compile(r"^\s*(pacific_slot\(\) \{.*\})\s*$", re.M)


def _src(name):
    return (REPO / ".github" / "workflows" / name).read_text(encoding="utf-8")


@pytest.mark.parametrize("name", WORKFLOWS)
def test_all_four_utc_slots_are_scheduled_and_gated(name):
    crons = re.findall(r'^\s*- cron: "([^"]+)"', _src(name), re.M)
    assert sorted(crons) == sorted(SLOTS)
    assert len(FN.findall(_src(name))) == 1
    assert '! pacific_slot "${{ github.event.schedule }}"' in _src(name)


# (UTC instant the cron fires, cron, runs?)
CASES = [
    ("2026-09-28 13:05:00", "0 13 * * *", True),    # 06:05 PDT
    ("2026-09-28 14:00:00", "0 14 * * *", False),   # 07:00 PDT
    ("2026-09-29 01:00:00", "0 1 * * *", True),     # 18:00 PDT
    ("2026-09-29 02:00:00", "0 2 * * *", False),    # 19:00 PDT
    ("2026-09-28 14:40:00", "0 13 * * *", True),    # a late start still runs
    ("2026-11-02 14:00:00", "0 14 * * *", True),    # 06:00 PST
    ("2026-11-02 13:00:00", "0 13 * * *", False),   # 05:00 PST
    ("2026-11-03 02:00:00", "0 2 * * *", True),     # 18:00 PST
    ("2026-11-03 01:00:00", "0 1 * * *", False),    # 17:00 PST
    ("2027-03-15 13:00:00", "0 13 * * *", True),    # PDT again
    ("2027-03-15 14:00:00", "0 14 * * *", False),
]


@pytest.mark.skipif(not shutil.which("bash"), reason="bash is not installed")
@pytest.mark.parametrize("name", WORKFLOWS)
@pytest.mark.parametrize("instant,cron,runs", CASES)
def test_both_sides_of_the_switch(name, instant, cron, runs):
    fn = FN.search(_src(name)).group(1)
    now = subprocess.run(["date", "-u", "-d", instant + " UTC", "+%s"],
                         capture_output=True, text=True, check=True).stdout.strip()
    rc = subprocess.run(["bash", "-c", f'{fn}\npacific_slot "{cron}"'],
                        env={"NOW": now, "PATH": "/usr/bin:/bin"}).returncode
    assert (rc == 0) == runs
