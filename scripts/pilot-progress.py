"""How far the 100-target isolate pilot has got. One line, measured, never stored.

`queue.md` carried the figure as prose and it went stale twice in one night — **5 of 100** while
nine were on disk, then **9** an hour after it was corrected to nine. A progress number written
into a queue item is wrong from the moment the next target lands, and a wrong number in a live
item is what sends the next session to redo work or to skip it.

So the item names this script instead of a count. `CLAUDE.md` § *Emma edits the tree and the items
BY HAND, continuously* is the same rule for a different file: a photograph of a moving thing is
stale on arrival, and the fix is to measure at read time rather than to refresh more often.

A target counts as touched when EITHER artifact exists — a family scrape in `geni-families/`, or
one of the six `geni-paths/*.html` captures the earlier page-saving method left. The two are
counted separately because they answer different halves of the loop.
"""

from __future__ import annotations

import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    ids = [r["geni_id"] for r in csv.DictReader(
        (ROOT / "reports" / "isolate-path-pilot.tsv").open(encoding="utf-8"), delimiter="\t")]
    fam = {p.name.split("-")[0] for p in (ROOT / "geni-families").glob("*-family.tsv")}
    html = {re.split(r"[-.]", p.name)[0] for p in (ROOT / "geni-paths").glob("*.html")}
    seen = set(ids)
    f, h = fam & seen, html & seen
    print("%d of %d touched — %d with a family scrape, %d with a saved path capture"
          % (len(f | h), len(ids), len(f), len(h)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
