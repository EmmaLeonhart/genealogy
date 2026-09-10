#!/usr/bin/env python3
"""Read the ruled `|` into `reports/title-label-proposals.tsv`. The step that CALLS `pipelabels`.

`scripts/pipelabels.py` was built and tested on 2026-09-09 — 24 tests, every ruled situation of
`name modelling.txt` § *A PIPE IN AN IMPORTED LABEL* — and then **nothing called it**.
`CLAUDE.md` § *Code that is WRITTEN but never CALLED is not done*: this is the caller, and it is
a step in `rebuild-everything.py`.

`propose-title-label-fixes.py` writes the proposals file with its OWN pipe reader, `split_pipe`,
which predates the ruling. That reader splits a piped label COLUMN-WISE and refuses two shapes
outright — a bracketed variant group (`hold=pipe-shape`) and a reading that comes back as a
single token (`hold=one-token`). Those two holds are exactly what the ruling answers. This script
reads them with `pipelabels.read` and writes the result back.

## ⛔ IT TOUCHES ONLY THE ROWS THAT ARE HELD, AND THAT SCOPE IS MEASURED RATHER THAN ASSUMED

1,640 rows carry a pipe. Running `pipelabels.read` over **all** of them was measured on
2026-09-10 and it is wrong in three separate ways, so it is not done:

    575 rows change, and among them --

    `knight Knud|Knut Gislason 'April'`  ->  the rank word comes BACK into the label.
        `pipelabels` knows nothing about titles; `propose-title-label-fixes` had already
        stripped it. § *A TITLE IS NOT A NAME* undone by the fix for a different defect.
    `Roger|Robert Debden, of Brampton, Suffolk`  ->  `Roger Debden, of Brampton`.
        `COMMA_TAIL` takes the LAST comma phrase only, so a two-comma tail is half-cut.
    `Joan|Julian (or Minell) Sambnel`  ->  `Joan or Minell Sambnel`.
        A bracket with no pipe in it folds into the name. Ruled for `of (Hastevere)`;
        an editorial `(or Minell)` is not that, and nobody ruled it.

The comma-tail ruling is the tell that settles the scope. It was ruled — *"KEEP IT IN THE `en`
LABEL, NOT IN `mul`"* — on **situation A of the bracketed shape, 34 rows**, and Emma ruled the
opposite way for the title batch the same day: *"Uhh bruh what? I'm asking you to remove the
prefix lol not the other stuff."* Restricted to the held rows the comma rule stays inside the
population it was ruled on; widened to all 1,640 it cuts a tail off 398 rows nobody asked about.

**201 rows are held for the pipe. 200 resolve and 1 does not**, which is the count the queue item
carries: `Q99707312` `Alice Willisham (Wellasham|Wyllasham` has an **unclosed bracket**, a
fifteenth situation nobody ruled on, and `pipelabels.read` refuses it on output.

## The leading title comes off first, because every other row in the file has had it off

10 of the 201 are `kind=title+pipe` and all ten carry `Sir`. `proposed_label` in this file is
built from the string with `leading_title` removed — that is what the column is for — so these
are stripped the same way before reading. Making the piped rows the one place a title survives
into `proposed_label` would be the inconsistency, not the fix.

## `proposed_en` is a NEW COLUMN and the ruling requires it

Situation A gives an item two different labels: `Lmul Isabel Fraunceys` and
`Len Isabel Fraunceys, Heiress of Giffords Hall`. `proposed_label` is one string and cannot
carry both. 36 of the 200 need it; everywhere else it is empty and English inherits `mul`.

## Idempotent, and it has to be

It reads `live_mul`/`live_en` and `leading_title` — never `proposed_label` — so a second run over
its own output computes the same strings. It also re-derives the hold from scratch, so a row that
stops resolving goes back to `pipe-shape` rather than keeping a stale proposal.
"""
import csv
import importlib.util
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "reports" / "title-label-proposals.tsv"

#: The two holds the pipe ruling answers. `leading-lowercase` is NOT here: that hold is about an
#: unruled rank word at the front of the label and the pipe ruling says nothing about it.
PIPE_HOLDS = ("pipe-shape", "one-token")

#: The column the comma-tail ruling needs, appended if the file predates it.
EN_COLUMN = "proposed_en"


def _pipelabels():
    """`scripts/pipelabels.py`, loaded by path — the filename is not importable as a module."""
    spec = importlib.util.spec_from_file_location(
        "pipelabels", str(ROOT / "scripts" / "pipelabels.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strip_title(live, leading_title):
    """The label as `proposed_label` is built from it: with the leading title removed.

    Only a genuine prefix is cut. A `leading_title` that does not open the string is left alone
    rather than removed from the middle — that would be a positional parse.
    """
    title = (leading_title or "").strip()
    if title and live.startswith(title):
        return live[len(title):].strip()
    return live


def apply(rows, pipes):
    """Rewrite the held piped rows in place. Returns `(resolved, still_held)`."""
    resolved, held = 0, 0
    for row in rows:
        live = row.get("live_mul") or row.get("live_en") or ""
        if "|" not in live or row.get("hold") not in PIPE_HOLDS:
            continue
        reading = pipes.read(strip_title(live, row.get("leading_title")))
        if reading.note.startswith("HELD") or not reading.mul:
            row["hold"] = "pipe-shape"
            row["proposed_label"] = ""
            row[EN_COLUMN] = ""
            row["proposed_aliases"] = ""
            held += 1
            continue
        row["hold"] = ""
        row["proposed_label"] = reading.mul
        row[EN_COLUMN] = reading.en or ""
        row["proposed_aliases"] = " | ".join(reading.aliases)
        resolved += 1
    return resolved, held


def main():
    if not SRC.exists():
        sys.exit(f"{SRC.relative_to(ROOT)} is missing -- run "
                 "scripts/propose-title-label-fixes.py (and the census before it)")

    pipes = _pipelabels()
    with SRC.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        columns = list(reader.fieldnames or [])
        rows = list(reader)
    if EN_COLUMN not in columns:
        columns.insert(columns.index("proposed_aliases"), EN_COLUMN)
    for row in rows:
        row.setdefault(EN_COLUMN, "")

    resolved, held = apply(rows, pipes)

    tmp = SRC.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows({k: row.get(k, "") for k in columns} for row in rows)
    os.replace(tmp, SRC)

    aliases = sum(len(r["proposed_aliases"].split(" | ")) for r in rows
                  if r["proposed_aliases"] and r["kind"].endswith("pipe"))
    en_rows = sum(1 for r in rows if r.get(EN_COLUMN))
    print(f"read the pipe into {SRC.relative_to(ROOT)}: {resolved} rows resolved, "
          f"{held} still held")
    print(f"    {en_rows} carry a comma tail, so `en` differs from `mul`")
    print(f"    {aliases} aliases across every piped row")
    remaining = Counter(r["hold"] for r in rows if r["hold"] in PIPE_HOLDS)
    for reason, n in remaining.most_common():
        print(f"    {n:5}  still {reason}")


if __name__ == "__main__":
    main()
