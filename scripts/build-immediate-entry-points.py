"""The ONE file of entry points that are live today.

    PYTHONPATH=src python scripts/build-immediate-entry-points.py

⛔ **ONE CSV. Ruled 2026-09-20:** *"all the Bure people, plus Arne, plus all of the people that
we've added to the entry points for miscellaneous reasons all need to be in one single CSV file
for the immediate entry points."*

Writes `reports/entry-points-immediate.csv` -- `qid`, `geni_id`, `source` -- from:

    arne        Q11959067, the one root who is not Bure
    bureus      Q633094, who is himself in bureatten.csv
    bureatten   reports/bureatten.csv, every row carrying a Geni id -- 251 of 576
    added       reports/entry-points-now.tsv, and reports/entry-points.tsv where the
                per-person active_from has arrived

**Why one file rather than three reads.** `subgraph_roots()` used to assemble this at import
time and guarded `bureatten.csv` with `if roster.exists():` -- so a missing roster silently
dropped the universe from 252 roots to 2. Nothing printed, nothing failed, and the whole
campaign would have run against two people. Now there is one file, one read, and a hard refusal
if it is absent or short.

**It does not decide anything.** Every id here was already an entry point by somebody else's
ruling; this only gathers them. `ledgers.py` § *These IDs are accepted as gospel by you. You do
not question them.*
"""
from __future__ import annotations

import csv
import datetime
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "entry-points-immediate.csv"

ARNE_QID = "Q11959067"
BUREUS_QID = "Q633094"


def main() -> int:
    today = datetime.date.today()
    rows: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(qid, gid, source):
        qid = (qid or "").strip()
        gid = (gid or "").strip()
        if not qid.startswith("Q") or (qid, gid) in seen:
            return
        seen.add((qid, gid))
        rows.append({"qid": qid, "geni_id": gid, "source": source})

    add(ARNE_QID, "", "arne")
    add(BUREUS_QID, "", "bureus")

    roster = ROOT / "reports" / "bureatten.csv"
    if not roster.exists():
        raise SystemExit(f"{roster.relative_to(ROOT)} is missing -- it carries 251 of the roots")
    with io.open(roster, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if (r.get("geni_ids") or "").strip() and (r.get("qid") or "").strip():
                add(r["qid"], r["geni_ids"].strip(), "bureatten")

    now = ROOT / "reports" / "entry-points-now.tsv"
    if now.exists():
        with io.open(now, encoding="utf-8") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                add(r.get("qid"), r.get("geni_id"), "added")

    # The per-person file carries its own date; a row whose date has not arrived is not live.
    dated = ROOT / "reports" / "entry-points.tsv"
    if dated.exists():
        with io.open(dated, encoding="utf-8") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                try:
                    live = datetime.date.fromisoformat((r.get("active_from") or "").strip()) <= today
                except ValueError:
                    live = False
                if live:
                    add(r.get("qid"), r.get("geni_id"), "added")

    rows.sort(key=lambda r: (r["source"] != "arne", r["source"] != "bureus", r["qid"]))
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["qid", "geni_id", "source"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    import collections
    counts = collections.Counter(r["source"] for r in rows)
    print(f"{OUT.relative_to(ROOT)}: {len(rows)} immediate entry points")
    for k, v in counts.most_common():
        print(f"   {k:10s} {v}")
    if len(rows) < 200:
        raise SystemExit("fewer than 200 entry points -- the roster is about 250; refusing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
