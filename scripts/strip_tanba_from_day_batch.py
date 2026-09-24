"""Remove Tanba lines from the day batch and both of its halves, in place.

    python scripts/strip_tanba_from_day_batch.py [FILE ...]

Ruled 2026-09-22: day QuickStatements must not edit Tanba people, and a matching line is
DROPPED -- comments included, never left as a `#` line.

⛔ **THE COMPOSER'S GATE IS NOT THE LAST WRITER.** `build-garborg-day.py` drops Tanba lines as it
composes, and then `pipeline.yml` splits the batch and appends five more `.qs` files to all three
files. On 2026-09-24 the published site still carried 178 Tanba QIDs in 879 lines, all from
halves nothing re-checked. So this runs LAST -- after the appends, before the site is built --
and again in `wikidata-edits.yml` before anything is sent. § *A GUARD IN ONE EMITTER IS NOT A
GUARD*.

It FAILS CLOSED: with no Tanba roster on disk it cannot tell a Tanba QID from any other, so it
exits non-zero rather than passing the batch as clean.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tanba_batch_block import tanba_blocked_qids  # noqa: E402

DAY_FILES = [ROOT / "reports" / n for n in (
    "wikidata-garborg-day.txt", "wikidata-garborg-day-auto.txt",
    "wikidata-garborg-day-manual.txt")]
_QID = re.compile("Q[0-9]+")


def main(argv: list[str]) -> int:
    qids = tanba_blocked_qids()
    if not qids:
        print("REFUSING: no Tanba QIDs loaded (reports/tanba-qids.json, "
              "reports/tanba-p2600-pairs.tsv) -- cannot tell what to drop")
        return 1
    for path in [Path(a) for a in argv] or DAY_FILES:
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        kept = [ln for ln in lines
                if "tanba" not in ln.lower() and not (set(_QID.findall(ln)) & qids)]
        path.write_text("".join(kept), encoding="utf-8")
        print(f"{path.name}: dropped {len(lines) - len(kept)} Tanba lines; {len(kept)} remain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
