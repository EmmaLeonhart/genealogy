"""Remove Tanba lines from reports/wikidata-garborg-day.txt in place.

    python scripts/strip_tanba_from_day_batch.py

Ruled 2026-09-22: day QuickStatements must not edit Tanba people.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tanba_batch_block import tanba_blocked_qids

DAY = ROOT / "reports" / "wikidata-garborg-day.txt"
_QID = re.compile("Q[0-9]+")


def main() -> None:
    qids = tanba_blocked_qids()
    lines = DAY.read_text(encoding="utf-8").splitlines(keepends=True)
    kept = []
    dropped = 0
    for line in lines:
        if "tanba" in line.lower() or (set(_QID.findall(line)) & qids):
            dropped += 1
            continue
        kept.append(line)
    DAY.write_text("".join(kept), encoding="utf-8")
    print(f"dropped {dropped} lines; {len(kept)} remain; {len(qids)} Tanba QIDs loaded")


if __name__ == "__main__":
    main()
