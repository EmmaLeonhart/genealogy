"""Split the daily batch into the part CI/CD sends itself and the part a person pastes.

Ruled 2026-09-14: *"Make the CICD do about half the edits every day automatically. Produce
disjoint quickstatements on the github page too."* **Disjoint** is the hard word: the Pages site
publishes the daily batch, and once the scheduled run starts sending part of it, anyone pasting
the page re-sends what the runner already did. Duplicate statements are mostly harmless, but a
duplicate `CREATE` mints a second item for somebody who now exists, and that is the one failure
in this design that cannot be undone by running it correctly next time.

## The split is computed ONCE, here, and written as two files

Not as a fraction applied twice. `wikidata-edit-run.py` could take `--fraction` and the page
builder could take the complement, and the two would agree only while the arithmetic, the file
and the ordering all stayed identical in three places. That is the shape of every drift bug this
repo has hit — the two copies of the start date, the clan gate that lived in one emitter, the
batch inventory nothing regenerated. So:

    reports/wikidata-garborg-day-auto.txt     what the schedule sends, unattended
    reports/wikidata-garborg-day-manual.txt   what the Pages site publishes

Together they are exactly the input, in order, with no edit in both and none dropped — which
this script asserts before writing anything.

## Why a third

The caps were raised 50% on 2026-09-14 and CI/CD takes a third of the result, so the share it
sends by itself is exactly the increase and the hand-run keeps the volume it always had:
`1.5 / 3 = 0.5`. Ruled the same day: *"you are specifically making 50% more quickstatements and
then segregating out a third of that to be run by cicd."*

## ⛔ A `CREATE` BLOCK IS NOT ONE LINE

QuickStatements V1 binds the lines after a `CREATE` to it positionally through `LAST`. Splitting
on line count would cut a creation away from the statements that describe it, and the tail would
then bind to whatever `CREATE` happened to precede it in the other half — silently attaching one
person's name and dates to another. So the split is made over EDIT OBJECTS parsed by `qs_v1`,
never over text, and a block moves whole.

    PYTHONPATH=src python scripts/split-daily-batch.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import qs_v1  # noqa: E402

SRC = REPO / "reports" / "wikidata-garborg-day.txt"
AUTO = REPO / "reports" / "wikidata-garborg-day-auto.txt"
MANUAL = REPO / "reports" / "wikidata-garborg-day-manual.txt"

#: The share the schedule sends by itself. One third; see the module docstring for why.
AUTO_SHARE = 1.0 / 3.0

#: The scheduled run's own ceiling, mirrored so the split never hands it more than it will send.
#: If it did, the surplus would be in neither file: the runner would stop at its limit and the
#: page would not carry the remainder.
RUN_LIMIT = 100


def blocks(text):
    """The batch as a list of (lines, is_create) in order.

    A `CREATE` and everything up to the next `CREATE` or the next explicitly-subjected line is
    one block, because `LAST` binds backwards.
    """
    # **A block runs from one `CREATE` to the NEXT `CREATE`, and that is the only safe cut.**
    # The first attempt ended a block at the first line that did not start with `LAST`, which
    # cut the bearer lines away: `Q141451028 P5056 LAST` starts with `Q`, and on its own it is
    # `LAST as a value with no CREATE above it`. Anything between two `CREATE`s may bind
    # backwards, so nothing between them may be separated from the first.
    out, cur = [], []
    for line in text.splitlines():
        if line.strip().upper() == "CREATE":
            if cur:
                out.append(cur)
            cur = [line]
        elif cur:
            cur.append(line)
        else:
            out.append([line])
    if cur:
        out.append(cur)
    return out


def main() -> int:
    if not SRC.exists():
        raise SystemExit(f"{SRC.relative_to(REPO)} is missing; compose the batch first")
    text = SRC.read_text(encoding="utf-8")

    edits = qs_v1.edit_objects(qs_v1.parse(text))
    share = min(math.ceil(len(edits) * AUTO_SHARE), RUN_LIMIT)

    bs = blocks(text)
    # Walk blocks until the auto half holds `share` edits. A block is never split.
    auto, manual, taken = [], [], 0
    for b in bs:
        joined = "\n".join(b)
        n = len(qs_v1.edit_objects(qs_v1.parse(joined))) if joined.strip() else 0
        if taken < share:
            auto.append(joined)
            taken += n
        else:
            manual.append(joined)

    a_text = "\n".join(auto).rstrip() + "\n"
    m_text = "\n".join(manual).rstrip() + "\n"

    # ⛔ Disjoint and complete, asserted rather than assumed.
    a_edits = qs_v1.edit_objects(qs_v1.parse(a_text))
    m_edits = qs_v1.edit_objects(qs_v1.parse(m_text))
    if len(a_edits) + len(m_edits) != len(edits):
        raise SystemExit(f"split lost or duplicated edits: {len(a_edits)} + {len(m_edits)} "
                         f"!= {len(edits)}")

    AUTO.write_text(a_text, encoding="utf-8", newline="\n")
    MANUAL.write_text(m_text, encoding="utf-8", newline="\n")
    print(f"{len(edits)} edits -> {len(a_edits)} automatic ({AUTO.name}), "
          f"{len(m_edits)} for the page ({MANUAL.name})")
    print(f"   share asked for: {share} (a third, capped at RUN_LIMIT {RUN_LIMIT})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
