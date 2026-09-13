"""Would a `Descendants` ball seeded above this subject repeat one we already hold?

    python scripts/ball-collision-check.py <subject geni id> <exports/root-dir>
    python scripts/ball-collision-check.py --list <exports/root-dir>

**Run this AFTER the climb, on the subject the climb landed on, and BEFORE spending the slot.**
The hit id the Monte Carlo sweep reported says nothing about this: the climb walks upward from
the hit and can arrive anywhere, and the collision is a property of where it arrived.

The check is: *is the subject already inside a `Descendants` ball filed under the same root
directory?* Measured over 65 balls on 2026-09-13, it fired 9 times and **8 of those 9 returned
exactly 1 new person** out of 5,000. Balls it did not fire on had a median of 1,626 new. The one
exception returned 1,238, so this is a warning and not a refusal — but the expected value of
spending a slot through it is about one person.

Why it works: a ball seeded on a created ancestor of P contains P and P's descent. If P already
sits inside an earlier ball for this root, that earlier ball already walked down through P. The
two balls differ only in the parent slot the climb took, which is the duplicate-parent collision
this repo has now hit nine times.

Exit status is 1 when a collision is found, so it can gate a shell step.

`--list` prints every id inside those balls, one per line, which is the `avoidSubjects` list the
extension takes with `seedwalk` and `montecarlo` from 1.7.44. **That is the version of this check
that is worth having**: asked here it is a post-mortem, asked by the climb it stops the landing
before a placeholder is written and before a slot is spent.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDI = re.compile(r"^0 @I(\d+)@")


def contains(path: pathlib.Path, subject: str) -> bool:
    with path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = INDI.match(line)
            if m and m.group(1) == subject:
                return True
    return False


def everyone(subdir: str) -> set:
    """Every id inside the `Descendants` balls filed under `subdir`."""
    out = set()
    for ball in sorted((ROOT / subdir).glob("export-Descendants-*.ged")):
        with ball.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = INDI.match(line)
                if m:
                    out.add(m.group(1))
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1] == "--list":
        for pid in sorted(everyone(sys.argv[2])):
            print(pid)
        return 0
    subject, subdir = sys.argv[1], sys.argv[2]
    balls = sorted((ROOT / subdir).glob("export-Descendants-*.ged"))
    if not balls:
        print("no Descendants balls under %s -- nothing to collide with" % subdir)
        return 0
    hits = [b for b in balls if contains(b, subject)]
    print("subject %s against %d ball(s) under %s" % (subject, len(balls), subdir))
    for b in hits:
        print("  COLLISION: already inside %s" % b.relative_to(ROOT))
    if hits:
        print("\n-> expect about 1 new person. Spend the slot only for a stated reason.")
        return 1
    print("  clear")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
