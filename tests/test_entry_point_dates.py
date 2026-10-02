"""The entry-point gate: everything that waited for 2027-01-01 starts on 2026-09-01.

Emma, 2026-09-30: "add https://www.wikidata.org/wiki/Q701641 https://www.wikidata.org/wiki/Q144348
https://www.wikidata.org/wiki/Q185152 to entry points and enable all Jan 1 entry points right now, as
in to say make them start at September 1 over Dec 1". Both sides of the date are pinned: the January
bucket and every group are live on 2026-09-01 and not the day before.
"""
from __future__ import annotations

import csv
import datetime
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import ledgers  # noqa: E402

START = datetime.date(2026, 9, 1)


def test_the_january_bucket_starts_on_september_first():
    assert ledgers.JAN1_DATE == START


def test_every_group_starts_on_or_before_september_first():
    with (ROOT / "reports" / "entry-point-groups.tsv").open(encoding="utf-8") as fh:
        dates = {row["group"]: row["active_from"] for row in csv.DictReader(fh, delimiter="\t")}
    assert dates
    assert all(datetime.date.fromisoformat(d) <= START for d in dates.values()), dates


def test_the_gate_opens_on_the_date_and_not_before():
    before = set(ledgers.entry_points(START - datetime.timedelta(days=1)))
    on = set(ledgers.entry_points(START))
    jan1 = set(ledgers.jan1_pairs())
    assert jan1
    assert jan1 <= on
    assert not (jan1 & before)


def test_the_three_new_entry_points_are_listed():
    with (ROOT / "reports" / "entry-points.tsv").open(encoding="utf-8") as fh:
        rows = {row["qid"]: row for row in csv.DictReader(fh, delimiter="\t")}
    for qid in ("Q701641", "Q144348", "Q185152"):
        assert qid in rows
        assert rows[qid]["active_from"] == "2026-09-01"


def test_sunjong_is_an_entry_point_from_now():
    """Emma, 2026-09-30: `Q334111` Sunjong of the Korean Empire, starting now like the three above."""
    with (ROOT / "reports" / "entry-points.tsv").open(encoding="utf-8") as fh:
        rows = {row["qid"]: row for row in csv.DictReader(fh, delimiter="	")}
    assert rows["Q334111"]["active_from"] == "2026-09-01"
    assert rows["Q334111"]["geni_id"] == "6000000028714712399"
