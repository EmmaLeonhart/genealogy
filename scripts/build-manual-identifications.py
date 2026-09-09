"""Every identification Emma has made by hand, in one file the pipeline reads each run.

    py scripts/build-manual-identifications.py

**Her instruction, 2026-09-01:** *"I think we need to have the two identifications I did, and all
other things as being from a manual identification csv that the pipeline generates 10
quickstatements adding the geni id to the individuals at the beginning of each generation. The 10
quickstatements are 10 of the ones from the csv that are found not to be present in the thing."*

And, in the same breath: *"the right verdicts need to be actually implemented."*

## `RIGHT` counts, and it was being dropped

`reports/emma-judgments.tsv` holds 116 verdicts. The ledger fold in `build-garborg-day.py`
accepted **only `SAME`**, so **17 `RIGHT` verdicts were inert** -- all from the 2026-08-25
`zipper-sample` batch, all carrying a QID and a Geni id, every one an affirmation she made that
nothing acted on. `RIGHT` is the older word from before the deck settled on `SAME`; the fold never
learned it. Both are affirmative and both are hers.

`BROWSER` is deliberately NOT included: it reads as *go and look at this* rather than as a
verdict, and two rows is not worth guessing over. `UNSURE` and `WRONG` are excluded for the
obvious reason.

## Sources, in precedence order

1. **`reports/manual-identifications-extra.csv`** -- pairs she gives directly in conversation,
   which no deck produced. That is where the two Behm identifications live, and it is the file to
   append to when she names another.
2. **`reports/emma-judgments.tsv`**, verdict `SAME` or `RIGHT`.

A pair present in both keeps the extra file's note, because that is the one she typed.

Writes `reports/manual-identifications.csv` -- one row per distinct (qid, geni_id).
"""

from __future__ import annotations

import collections
import csv
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TAB = chr(9)
JUDGMENTS = REPO / "reports" / "emma-judgments.tsv"
EXTRA = REPO / "reports" / "manual-identifications-extra.csv"
OUT = REPO / "reports" / "manual-identifications.csv"

#: Verdicts that affirm the pair. `BROWSER` is not one -- it reads as an instruction to look,
#: not as a judgement -- and `UNSURE`/`WRONG` obviously are not.
AFFIRMATIVE = {"SAME", "RIGHT"}

FIELDS = ["qid", "geni_id", "name", "verdict", "batch", "date", "note"]


def main() -> int:
    pairs: dict[tuple[str, str], dict] = {}

    if JUDGMENTS.exists():
        with io.open(JUDGMENTS, encoding="utf-8") as fh:
            for r in csv.DictReader(fh, delimiter=TAB):
                if r.get("verdict") not in AFFIRMATIVE:
                    continue
                qid, geni = (r.get("qid") or "").strip(), (r.get("geni_id") or "").strip()
                if not (qid and geni):
                    continue
                pairs[(qid, geni)] = {
                    "qid": qid, "geni_id": geni,
                    "name": (r.get("our_name") or r.get("their_name") or "").strip(),
                    "verdict": r["verdict"], "batch": (r.get("batch") or "").strip(),
                    "date": (r.get("date") or "").strip(),
                    "note": (r.get("her_words") or "").strip(),
                }

    # The extra file wins, because those are the ones she typed rather than clicked.
    if EXTRA.exists():
        with io.open(EXTRA, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                qid, geni = (r.get("qid") or "").strip(), (r.get("geni_id") or "").strip()
                if not (qid and geni):
                    continue
                pairs[(qid, geni)] = {
                    "qid": qid, "geni_id": geni, "name": (r.get("name") or "").strip(),
                    "verdict": "SAME", "batch": "given in conversation",
                    "date": (r.get("date") or "").strip(),
                    "note": (r.get("note") or "").strip(),
                }

    rows = sorted(pairs.values(), key=lambda r: (r["date"], r["qid"]))
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    by_batch = collections.Counter(r["batch"] for r in rows)
    by_verdict = collections.Counter(r["verdict"] for r in rows)
    print(f"wrote {OUT.relative_to(REPO)} - {len(rows)} identifications")
    for k, v in by_verdict.most_common():
        print(f"   {v:>4}  verdict {k}")
    print()
    for k, v in by_batch.most_common():
        print(f"   {v:>4}  {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
