"""Stamp `last_attempted` onto the unconnected-`P2600` worklist, once per attempt.

    PYTHONPATH=src python scripts/attempt_ledger.py 6000000074746020450
    PYTHONPATH=src python scripts/attempt_ledger.py --today 2026-09-09 <geni id> ...

**Piece 6 of `docs/unconnected-worklist.md`**, the last one that did not exist: *"Written by the
extension, automatically, every time it runs on somebody to try to connect them. Nothing
hand-maintained."*

## WHY IT IS HERE AND NOT IN THE EXTENSION, which is not a deviation from the spec

**Nothing downloads.** `queue.md` § *THE EIGHT THINGS THAT WILL WASTE A SESSION* is explicit:
roughly two files land per browser session and Chrome blocks the rest, the job returns its result
on a data attribute, and **a file tool writes it** — `saveBlob` has been deleted twice and must
not come back. So the extension cannot write into the repo at all, and every file the collector
loop produces is written by `scripts/write-family-scrape.py` instead.

This is that pipe, for this column. It is called from `write-family-scrape.py`, which runs
exactly once per person the collector runs on, so the date is written automatically on every
attempt and never by hand — which is the property the spec asks for.

## WHAT AN ATTEMPT IS

**Running on somebody.** Not finding a path, and not failing to: § 8 of the spec is built on a
failure costing one attempt — *"if we fail on an individual, we've attempted it and we move
on"* — so the stamp is the record that the person's turn was taken. A hit stamps too and then
leaves the file at the next build, because it is connected and membership is recalculated.

## ⛔ IT NEVER ADDS A ROW, AND THAT IS THE SPEC RATHER THAN CAUTION

Membership is **recalculated every run and never stored** (§ 3): *"they just wouldn't be
generated into the TSV file so we don't really have to statefully store whether we've been
successful."* A Geni id with no row is therefore a person this file says nothing about — already
connected, or not a `P2600` holder — and minting a row for them would be storing exactly the
state the design removes. The count of ids that matched nothing is returned and printed instead.

## ⛔ IT DOES NOT RE-SORT, EITHER

The ordering is § 7's and belongs to the build: two blocks, eligible on top, then neighbourhood
size descending and qid ascending. Re-deriving it here would mean recomputing eligibility on a
file the collector is reading down at the time, and the next CI run recomputes it anyway from a
fresh neighbourhood size. Only the one field changes; every other byte of the row is carried
through untouched.

The write goes through a temporary file and one `replace`, because this file is 11 MB and 266,201
rows of state whose only copy is the previous commit of itself (§ 6: *there is no second file*).
A rewrite interrupted in place would lose the dates for everybody.
"""

from __future__ import annotations

import argparse
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

WORKLIST = ROOT / "reports" / "unconnected-p2600.tsv"

#: The columns, in the order § 2 of the spec fixes them in. `last_attempted` is the last.
COLUMNS = ["qid", "geni_id", "neighbourhood_size", "last_attempted"]

NL = chr(10)
CR = chr(13)
TAB = chr(9)


def fields(line):
    """One line into its columns. Strips CR as well as LF: `newline=""` hands back whatever the
    file holds, and a stray CRLF would otherwise put a carriage return on the end of the date."""
    return line.rstrip(NL).rstrip(CR).split(TAB)


def stamp(geni_ids, today=None, path=WORKLIST):
    """Write `today` into `last_attempted` for every row naming one of `geni_ids`.

    Returns `{"present": bool, "stamped": n, "unmatched": [geni id], "rows": total}`.
    `unmatched` is the ids the file holds no row for, which is information rather than an error:
    see the docstring. `present` says whether the worklist was on disk at all -- a missing file
    and a file with no matching row are different facts and the summary line says which.

    The file is read and written as UTF-8 with LF line endings, matching what
    `build-unconnected-worklist.py` writes. Windows' CRLF default would rewrite all 266,201
    lines and show up as a whole-file diff on every capture.
    """
    wanted = {g.strip() for g in geni_ids if g and g.strip()}
    path = pathlib.Path(path)
    out = {"present": path.exists(), "stamped": 0, "unmatched": sorted(wanted), "rows": 0}
    if not wanted or not out["present"]:
        return out
    day = (today or datetime.date.today()).isoformat()

    # ⛔ THE HEADER IS CHECKED BEFORE THE TEMPORARY FILE IS OPENED, and the order matters on
    # Windows: a file that is still open cannot be unlinked there, so validating inside the
    # rewrite would leave a half-written `.tmp` behind on the one path that is supposed to
    # change nothing.
    with path.open(encoding="utf-8", newline="") as fh:
        header = fh.readline()
    if fields(header) != COLUMNS:
        raise SystemExit("⛔ %s does not carry the four columns of the spec: %r"
                         % (path, header.rstrip(NL)))

    seen = set()
    tmp = path.with_suffix(path.suffix + ".tmp")
    with path.open(encoding="utf-8", newline="") as src, \
            tmp.open("w", encoding="utf-8", newline=NL) as dst:
        dst.write(src.readline())
        for line in src:
            row = fields(line)
            if len(row) == len(COLUMNS) and row[1] in wanted:
                row[3] = day
                seen.add(row[1])
                out["stamped"] += 1
                line = TAB.join(row) + NL
            out["rows"] += 1
            dst.write(line)
    tmp.replace(path)
    out["unmatched"] = sorted(wanted - seen)
    return out


def describe(result, day):
    """One line, for the collector loop's summary. Silence about a no-op hides a stale file."""
    if not result["present"]:
        return "worklist not on disk; no attempt stamped"
    if result["stamped"]:
        note = "last_attempted=%s on %d row%s" % (
            day, result["stamped"], "" if result["stamped"] == 1 else "s")
    else:
        note = "no worklist row to stamp"
    if result["unmatched"]:
        note += " (not in the file: %s)" % ", ".join(result["unmatched"])
    return note


def main() -> int:
    ap = argparse.ArgumentParser(description="stamp last_attempted on the unconnected worklist")
    ap.add_argument("geni_ids", nargs="+")
    ap.add_argument("--today", default="", help="override today, for a reproducible run")
    ap.add_argument("--file", default=str(WORKLIST))
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    day = (datetime.date.fromisoformat(args.today) if args.today else datetime.date.today())
    result = stamp(args.geni_ids, today=day, path=pathlib.Path(args.file))
    print(describe(result, day.isoformat()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
