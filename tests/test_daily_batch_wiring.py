"""The batch path is written in three places, so pin them together.

⛔ **THIS TEST EXISTS BECAUSE NOT ONE EDIT HAD EVER GONE OUT.** `scripts/split-daily-batch.py`
cut `reports/wikidata-garborg-day.txt` into an AUTO half and a MANUAL half on 2026-09-14. The
split updated `DAILY_BATCH` in `.github/workflows/wikidata-edits.yml` and **neither of the two
other places that name the batch**, so the daily send failed twice over:

    2026-09-15  no such batch: .../reports/wikidata-garborg-day-auto.txt
                -- the sparse-checkout list still named the pre-split file
    2026-09-16  refusing a live run on reports/wikidata-garborg-day-auto.txt: not one of
                the reviewed batches
                -- REVIEWED_BATCHES still named the pre-split file

Both failures were red on the schedule and neither was noticed, because a red `wikidata-edits`
run had been ordinary all through the hold. Emma: *"why the fuck have I never seen any edits from
the account"*.

The rule this pins is not "these particular filenames". It is that **the file a scheduled run
sends must be checked out and must be reviewable**, whatever it is called next.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORKFLOW = REPO / ".github" / "workflows" / "wikidata-edits.yml"
RUNNER = REPO / "scripts" / "wikidata-edit-run.py"


def daily_batch() -> str:
    text = WORKFLOW.read_text(encoding="utf-8")
    m = re.search(r"^\s*DAILY_BATCH:\s*(\S+)\s*$", text, re.M)
    assert m, "wikidata-edits.yml has no DAILY_BATCH"
    return m.group(1).strip("\"'")


def sparse_paths() -> list[str]:
    text = WORKFLOW.read_text(encoding="utf-8")
    m = re.search(r"sparse-checkout:\s*\|\n((?:\s+\S.*\n)+)", text)
    assert m, "wikidata-edits.yml has no sparse-checkout block"
    return [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]


def reviewed() -> set:
    text = RUNNER.read_text(encoding="utf-8")
    m = re.search(r"REVIEWED_BATCHES = \{(.*?)\n\}", text, re.S)
    assert m, "wikidata-edit-run.py has no REVIEWED_BATCHES"
    return set(re.findall(r'"([^"]+)"', m.group(1)))


def test_the_daily_batch_is_committed():
    batch = daily_batch()
    assert (REPO / batch).exists(), (
        f"{batch} is what the schedule sends and it is not in the repo")


def test_the_daily_batch_is_checked_out():
    """The 2026-09-15 failure: `no such batch`, because sparse-checkout named another file."""
    batch = daily_batch()
    covered = False
    for pattern in sparse_paths():
        p = pattern.lstrip("/")
        if p.endswith("*") or "*" in p:
            covered = covered or re.fullmatch(p.replace("*", "[^/]*"), batch) is not None
        else:
            covered = covered or batch == p or batch.startswith(p.rstrip("/") + "/")
    assert covered, (
        f"DAILY_BATCH={batch} is not covered by the sparse-checkout list {sparse_paths()}; "
        "the run will die on 'no such batch'")


def test_the_daily_batch_may_be_executed_live():
    """The 2026-09-16 failure: `not one of the reviewed batches`."""
    batch = daily_batch()
    assert batch in reviewed(), (
        f"DAILY_BATCH={batch} is not in REVIEWED_BATCHES {sorted(reviewed())}; "
        "a live run refuses it")
