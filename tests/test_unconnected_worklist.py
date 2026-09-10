"""The unconnected-`P2600` worklist: its order, its carry-forward, and the attempt stamp.

`docs/unconnected-worklist.md` is the specification. Three of its properties are the kind that
break silently, so they are pinned here rather than eyeballed on an 11 MB file:

* **the order** (§ 7) — eligible block on top, the ineligible below it ordered by when they
  become eligible, and within either block neighbourhood size descending then qid ascending.
  A wrong order does not fail, it just hands the collector the wrong person for weeks.
* **the carry-forward** (§ 6) — `last_attempted` is read from the previous version of this same
  file, and *there is no second file*. A reader that drops it silently resets every cooldown and
  re-queues 266,201 people on their first day.
* **the stamp** (§ 5) — `scripts/attempt_ledger.py` writes the date on every attempt, touches
  nothing else, and **never invents a row**: membership is recalculated every run and never
  stored, so a Geni id with no row is a person this file says nothing about.
"""
from __future__ import annotations

import datetime
import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
TAB = chr(9)
NL = chr(10)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(REPO / "scripts" / path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def build():
    return load("build_unconnected_worklist", "build-unconnected-worklist.py")


@pytest.fixture(scope="module")
def ledger():
    return load("attempt_ledger", "attempt_ledger.py")


TODAY = datetime.date(2026, 9, 9)


def test_cooldown_is_thirty_days(build):
    assert build.COOLDOWN == datetime.timedelta(days=30)
    assert build.eligible_on("2026-08-10") == datetime.date(2026, 9, 9)


def test_the_seeds_are_the_two_placeholders(build):
    """Stated as placeholders in the spec, and they are still the placeholders it names."""
    assert build.SEED_ATTEMPTED == "2026-09-01"
    assert build.SEED_NEVER == "2026-01-01"


def test_eligible_block_comes_first_then_by_when_they_become_eligible(build):
    """§ 7. A huge neighbourhood does not promote somebody out of their cooldown."""
    rows = [
        ("Q1", "g1", 5000, "2026-09-08"),   # attempted yesterday -- waits until 2026-10-08
        ("Q2", "g2", 3, "2026-01-01"),      # eligible
        ("Q3", "g3", 4000, "2026-08-25"),   # waits until 2026-09-24, sooner than Q1
    ]
    order = [r[0] for r in sorted(rows, key=lambda r: build.sort_key(r, TODAY))]
    assert order == ["Q2", "Q3", "Q1"]


def test_within_a_block_size_descends_then_qid_ascends(build):
    rows = [
        ("Q500", "g1", 10, "2026-01-01"),
        ("Q100", "g2", 10, "2026-01-01"),
        ("Q200", "g3", 99, "2026-01-01"),
    ]
    order = [r[0] for r in sorted(rows, key=lambda r: build.sort_key(r, TODAY))]
    assert order == ["Q200", "Q100", "Q500"]


def test_the_key_is_total_and_deterministic(build):
    """`CLAUDE.md` § *SORTING MUST BE DETERMINISTIC* — same rows, same bytes, any input order."""
    rows = [("Q%d" % i, "g%d" % i, i % 7, "2026-0%d-01" % (1 + i % 9)) for i in range(1, 40)]
    one = sorted(rows, key=lambda r: build.sort_key(r, TODAY))
    two = sorted(reversed(rows), key=lambda r: build.sort_key(r, TODAY))
    assert one == two


def test_a_malformed_date_does_not_stop_the_build(build):
    """The column is written by the collector pipe; a bad value sorts first, it does not raise."""
    assert build.eligible_on("") == datetime.date.min
    assert build.eligible_on("yesterday") == datetime.date.min


def write_worklist(path, rows):
    path.write_text(
        TAB.join(["qid", "geni_id", "neighbourhood_size", "last_attempted"]) + NL
        + "".join(TAB.join(str(c) for c in r) + NL for r in rows),
        encoding="utf-8", newline="")


def test_dates_are_carried_forward_from_the_file_itself(build, tmp_path):
    """§ 6, and there is no second file: the previous version of this file is the input."""
    f = tmp_path / "unconnected-p2600.tsv"
    write_worklist(f, [("Q1", "100", 5, "2026-09-02"), ("Q2", "200", 4, "2026-01-01")])
    assert build.load_previous(f) == {"100": "2026-09-02", "200": "2026-01-01"}
    assert build.load_previous(tmp_path / "absent.tsv") == {}


def test_the_stamp_writes_today_on_that_row_and_nothing_else(ledger, tmp_path):
    f = tmp_path / "unconnected-p2600.tsv"
    write_worklist(f, [("Q1", "100", 5, "2026-01-01"),
                       ("Q2", "200", 4, "2026-01-01"),
                       ("Q3", "300", 3, "2026-09-01")])
    out = ledger.stamp(["200"], today=TODAY, path=f)
    assert out["stamped"] == 1 and out["rows"] == 3 and out["unmatched"] == []
    lines = f.read_text(encoding="utf-8").split(NL)
    assert lines[1] == TAB.join(["Q1", "100", "5", "2026-01-01"])
    assert lines[2] == TAB.join(["Q2", "200", "4", "2026-09-09"])
    assert lines[3] == TAB.join(["Q3", "300", "3", "2026-09-01"])


def test_the_stamp_keeps_the_file_order_and_the_lf_endings(ledger, tmp_path):
    """It does not re-sort — that is the build's job — and it must not CRLF 266,201 lines."""
    f = tmp_path / "unconnected-p2600.tsv"
    write_worklist(f, [("Q9", "900", 1, "2026-01-01"), ("Q1", "100", 9, "2026-01-01")])
    ledger.stamp(["100"], today=TODAY, path=f)
    raw = f.read_bytes()
    assert b"\r\n" not in raw
    assert [l.split(TAB)[0] for l in raw.decode("utf-8").rstrip(NL).split(NL)[1:]] == ["Q9", "Q1"]


def test_the_stamp_never_invents_a_row(ledger, tmp_path):
    """Membership is recalculated every run and never stored, so an absent id stays absent."""
    f = tmp_path / "unconnected-p2600.tsv"
    write_worklist(f, [("Q1", "100", 5, "2026-01-01")])
    out = ledger.stamp(["999"], today=TODAY, path=f)
    assert out["stamped"] == 0 and out["unmatched"] == ["999"]
    assert f.read_text(encoding="utf-8").count(NL) == 2
    assert "999" not in f.read_text(encoding="utf-8")


def test_the_stamp_is_a_no_op_when_the_file_is_not_on_disk(ledger, tmp_path):
    out = ledger.stamp(["100"], today=TODAY, path=tmp_path / "absent.tsv")
    assert out == {"present": False, "stamped": 0, "unmatched": ["100"], "rows": 0}
    assert "not on disk" in ledger.describe(out, "2026-09-09")


def test_the_stamp_refuses_a_file_that_is_not_this_file(ledger, tmp_path):
    """Four columns in that order, or nothing is written: the spec fixes the column order."""
    f = tmp_path / "unconnected-p2600.tsv"
    f.write_text("geni_id" + TAB + "qid" + NL + "100" + TAB + "Q1" + NL, encoding="utf-8")
    with pytest.raises(SystemExit):
        ledger.stamp(["100"], today=TODAY, path=f)
    assert not (tmp_path / "unconnected-p2600.tsv.tmp").exists()


def test_the_committed_worklist_has_the_spec_columns():
    """The real file, because every consumer joins on that column order."""
    f = REPO / "reports" / "unconnected-p2600.tsv"
    if not f.exists():
        pytest.skip("the worklist has not been built in this checkout")
    with f.open(encoding="utf-8") as fh:
        assert fh.readline().rstrip(NL).split(TAB) == [
            "qid", "geni_id", "neighbourhood_size", "last_attempted"]


def test_the_write_path_stamps_every_capture():
    """⛔ *Code that is WRITTEN but never CALLED is not done.* The pipe must call the stamp."""
    src = (REPO / "scripts" / "write-family-scrape.py").read_text(encoding="utf-8")
    assert "from attempt_ledger import" in src
    assert "stamp([gid]" in src
