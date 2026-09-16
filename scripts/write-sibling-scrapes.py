"""Write a dumped batch of sibling scrapes into the repo, and stamp the attempts.

    python scripts/write-sibling-scrapes.py < ~/Downloads/sibling-scrapes-001.json

The other half of `scripts/siblingscrape.js`. That file drives the browser and blob-downloads
what it collected; this one puts it where it belongs. Nothing here touches the network.

## What it writes

  `geni-families/<geni id>-family.tsv`   the family file, step 1 of `docs/per-individual-loop.md`
  `last_attempted` in the worklist       `reports/unconnected-p2600.tsv`, through `attempt_ledger`

`scripts/build-tiny-gedcoms.py` then turns `geni-families/*-family.tsv` into
`exports/tiny-profiles/*.ged`, which is what puts the parents into the synoptic tree. That step is
not run from here: it is a corpus write and belongs in its own commit.

## Why the campaign exists at all

A path GEDCOM writes a sibling pair as a family with two `CHIL` and **no partners** -- Geni
records no sibling edge, so a path can only ever say *these two are siblings*. The parents arrive
from the members' own profile pages, and the merge fuses the parentless family with the two
parented ones on the Geni id, so one family with real parents comes out.

**Every member of a pair, not one of each.** Instructed, and not an oversight to optimise away:
scraping one side gets one side's account of the parents.

## ⛔ EVERY STATE IS STAMPED, INCLUDING THE ONES THAT FOUND NOTHING

`scripts/stamp-attempts.py` is explicit that a state the writer refuses to stamp is a state
somebody chose to un-attempt. A `private_profile` is Geni's final answer for that person and a
`timeout` is a page load already spent; both are attempts, and re-landing on them tomorrow costs
another page load to learn the same thing. Only the family FILE is conditional on there being a
family to write.

⛔ **`blocked` IS THE ONE THAT IS NOT AN ATTEMPT.** It is a CAPTCHA, and `GC.runFamily` checks for
it first precisely because a CAPTCHA scrapes as a person with no family and reports success.
Stamping it would record an attempt on a page that was never shown, and the person would then sit
out 30 days having never been looked at. They are counted and reported, and the run should stop.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAMILIES = ROOT / "geni-families"

#: `attempt_ledger.py` is an ordinary module name, but it lives in `scripts/` beside this file
#: rather than on the path.
_spec = importlib.util.spec_from_file_location(
    "attempt_ledger", ROOT / "scripts" / "attempt_ledger.py")
attempt_ledger = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(attempt_ledger)

#: Not an attempt: the page was never shown. See the docstring.
NOT_AN_ATTEMPT = {"blocked", "no_extension"}


def records(raw):
    """The dumped list, whatever shape the dump arrived in.

    A single record is accepted as well as a list, because a one-person dump is a reasonable
    thing to have and failing on it would be a papercut in the middle of a browser sitting.
    """
    blob = json.loads(raw)
    if isinstance(blob, dict):
        return [blob]
    if not isinstance(blob, list):
        raise SystemExit("expected a list of scrape records, got %s" % type(blob).__name__)
    return blob


def write_family(rec):
    """The family file for one person, or `None` when the scrape carries no file.

    ⛔ **NEVER OVERWRITE A SCRAPE WITH AN EMPTY ONE.** A `private_profile` or a `timeout` carries
    no `tsv`, and writing it as a zero-byte file would destroy a good capture from an earlier
    sitting and read as "we have this person" for ever after.
    """
    tsv = rec.get("tsv")
    gid = str(rec.get("geni_id") or "").strip()
    if not (gid and tsv):
        return None
    FAMILIES.mkdir(exist_ok=True)
    path = FAMILIES / ("%s-family.tsv" % gid)
    # LF, UTF-8, matching what the collector pipe already writes -- `CLAUDE.md` § *Windows:
    # never round-trip UTF-8 through Get-Content/Set-Content*.
    with path.open("w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(tsv if tsv.endswith(chr(10)) else tsv + chr(10))
    return path


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        # The final summary dies on a CJK name under cp1252, AFTER the files are on disk, which
        # reads as a failed capture and invites a re-run. Measured 2026-09-09.
        pass

    recs = records(sys.stdin.read())

    written, by_state, to_stamp, blocked = [], {}, [], 0
    for rec in recs:
        state = str(rec.get("state") or "unknown")
        by_state[state] = by_state.get(state, 0) + 1
        gid = str(rec.get("geni_id") or "").strip()
        if not gid:
            continue
        path = write_family(rec)
        if path:
            written.append(path)
        if state in NOT_AN_ATTEMPT:
            blocked += 1
            continue
        to_stamp.append(gid)

    result = attempt_ledger.stamp(to_stamp) if to_stamp else {
        "present": False, "stamped": 0, "unmatched": [], "rows": 0}

    print("%d records" % len(recs))
    for state in sorted(by_state):
        print("  %-18s %d" % (state, by_state[state]))
    print("%d family files written to %s" % (len(written), FAMILIES.relative_to(ROOT)))
    print("%d attempts stamped (%d rows in the worklist, %d ids it has no row for)"
          % (result.get("stamped", 0), result.get("rows", 0), len(result.get("unmatched", []))))
    if blocked:
        # ⛔ Loud, and last, so it is the thing left on the screen.
        print("⛔ %d records were BLOCKED or had no extension -- NOT stamped, and the run should "
              "stop: a CAPTCHA scrapes as a person with no family and reports success" % blocked)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
