"""Spit out a random Geni id from a ball. Nothing else.

Ruled 2026-09-10: *"Monte Carlo means you write a script that spits out the ID and don't think at
all ... My idea wasn't 'is this a good person to do a descendant export from?' My idea was: does
this person have five thousand descendants? It can be a complete waste of time and I don't care,
because statistically it's going to work."*

⛔ **THIS SCRIPT MUST NOT GET CLEVERER.** No exclusion lists, no ranking, no names in the output,
no skipping people who look unpromising, no avoiding ones already tried. Every one of those is a
judgement, and the judgement is what the method exists to remove. A repeated pick is a wasted page
load and that is cheaper than deciding.

The only thing filtered is the root itself, because exporting from the person you sampled from is
not a sample.

    python scripts/monte-carlo-pick.py <ball.ged> [n]

Prints one id per line. The caller reads `descendants` off the profile and compares it to the
threshold. That is the whole decision.
"""

from __future__ import annotations

import pathlib
import random
import re
import sys

INDI = re.compile(r"^0 @I(\d+)@ INDI", re.M)


def main() -> int:
    ball = pathlib.Path(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    text = ball.read_text(encoding="utf-8", errors="replace")
    if ball.suffix.lower() == ".csv":
        # A descent CSV from `scripts/descent-from.py`: geni_id is the first column, and the root
        # is already excluded by that script, so every row is a descendant.
        ids = [ln.split(",", 1)[0].strip() for ln in text.splitlines()[1:] if ln.strip()]
        pool = [i for i in ids if i.isdigit()]
    else:
        ids = INDI.findall(text)
        seed = ids[0] if ids else None
        pool = [i for i in ids if i != seed]
    random.seed()
    for i in random.sample(pool, min(n, len(pool))):
        print(i)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
