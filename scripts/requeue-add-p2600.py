"""Put the `build-add-p2600-batch` decision back in front of her, once, on 2026-09-13.

**Emma, 2026-09-06, asked to rule on it:** *"Ngl I have so little context set up github actions
to add asking this into the queue again a week from now (appending it) because I'm incapable of
making a decision now."*

So the deferral is a **DATE**, not a memory. `CLAUDE.md` § *Entry points DRIP IN on a date* is
the same mechanism for the same reason: a session-local cron dies with its session, and every
cron in this repo has died at least once — the 2026-08-28 crash took all of them, and on
2026-09-05 a session ran for hours with none. A workflow on a schedule plus a date in a file
survives all of that, needs nobody to remember anything, and moving the date is a one-line edit.

**It appends ONCE.** The marker is checked first, so a daily schedule cannot append a duplicate
every morning. If she defers again, move `WHEN` forward and delete the appended item.
"""

from __future__ import annotations

import datetime
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUEUE = ROOT / "queue.md"

#: A week after she deferred it.
WHEN = datetime.date(2026, 9, 13)

#: Written into the appended item as an HTML comment, so the check is on the queue's own content
#: rather than on any state this script would otherwise have to keep somewhere.
MARKER = "requeued-add-p2600-2026-09-13"

ITEM = """- **DECIDE: what happens to `build-add-p2600-batch`.** <!-- {marker} -->
  Deferred by her on 2026-09-06 — *"I have so little context... because I'm incapable of making
  a decision now"* — and re-queued on {when} by `.github/workflows/requeue-add-p2600.yml`.

  It writes **7,166 `P2600` statements** inferred from parent-anchor proof into
  `reports/wikidata-add-p2600.qs`, and **nothing runs it**. The four options as they stood: fold
  it into the daily batch under a cap; give it its own scheduled workflow; delete it; or leave it
  as a hand-run tool. `reports/qs-batch-audit.md` carries the measurement.

  The other five generators in that audit were settled on 2026-09-06 —
  `build-missing-reciprocals`, `build-qid-link-p2600`, `build-label-corrections` and
  `build-sibling-batch` deleted at her instruction, `build-from-diff` given its own review item.
  This is the last one open.
"""


def main() -> int:
    text = QUEUE.read_text(encoding="utf-8")
    if MARKER in text:
        print("already re-queued; nothing to do")
        return 0
    today = datetime.date.today()
    if today < WHEN:
        print("not yet %s (today is %s); nothing to do" % (WHEN.isoformat(), today.isoformat()))
        return 0
    item = ITEM.format(marker=MARKER, when=WHEN.isoformat())
    QUEUE.write_text(text.rstrip("\n") + "\n\n" + item, encoding="utf-8")
    print("appended the add-p2600 decision to queue.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
