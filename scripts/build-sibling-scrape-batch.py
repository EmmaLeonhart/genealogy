"""The next people the sibling scrape should land on, in worklist order.

    python scripts/build-sibling-scrape-batch.py --count 40

Prints one Geni id per line, newest-eligible first, for the agent loop in
`docs/sibling-scrape-loop.md` to navigate to. Nothing is fetched here; this is arithmetic over
committed files.

## What the campaign is

Ruled 2026-09-16: *"the list is something that we can do mass scraping on in the same way as the
relationship paths, although much more agentically due to dumb rules by the site."*

A path GEDCOM writes a sibling pair as a family with two `CHIL` and **no partners** -- Geni
records no sibling edge, so a path can only ever say *these two are siblings* -- and the parents
arrive from the members' own profile pages. `reports/sibling-pair-worklist.tsv` is who still
needs that, and `scripts/sibling-pair-worklist.py` builds it.

**Every member, not one of each pair.** Instructed, and not an oversight to optimise away:
scraping one side gets one side's account of the parents. Each member yields a GEDCOM linking the
pair as siblings *with* their parents, and the merge fuses the three on the Geni id so the
parentless family and the two parented ones become one family with real parents.

## ⛔ IT IS NOT THE PATH CAMPAIGN'S SHAPE, AND THAT IS WHY THIS PRINTS 40 AND NOT 2,400

`scripts/build-pathrun-batch.py` feeds a loop that lives in the page and does one `fetch` per
person against a search endpoint, which is why 1,040 an hour is safe and why its batch is 2,400.

**This is a real page load per person.** `CLAUDE.md` § *a census read costs a real page load* --
`fetch` returns zeros because the stats block is rendered after load -- and 500-odd back-to-back
reads is what got the account CAPTCHAd on 2026-09-12 and again on 2026-09-15. So the loop is the
AGENT's: navigate, dispatch, write, next, at the extension's pace. § *WHY IT IS AGENTIC AT ALL:
the CAPTCHA, and nothing else* -- navigating to the page agentically and then running the
extension is what counts as proper traffic, and a background fetch loop is the thing that gets
blocked.

A batch is therefore a working set for one sitting, not a queue to drain unattended.

## ⛔ THE QUEUE IS `parent_in_tree`, NOT `scraped`

`scraped` says a `geni-families/<id>-family.tsv` exists. That was the queue until 2026-09-16 and
it was the wrong test: a sibling pair's parents can arrive from any ordinary export under
`exports/`, from a Wikidata identification, or from another path entirely, and none of those
leaves a file in `geni-families/`. Scraping those people again spends a page load to learn
something the tree already knew.

**An older worklist has no `parent_in_tree` column**, because `tree.yml` has not rebuilt since the
column was added. This falls back to `scraped` and says so, rather than treating every row as
parentless and sending the collector at all 65,257.

## The cooldown is the same one, and it is the same ledger

`scripts/attempt_ledger.py` stamps `last_attempted` in `reports/unconnected-p2600.tsv` on every
capture -- `write-family-scrape.py` calls it -- and a stamped person waits out 30 days. A sibling
worklist member who is also a `P2600` holder is subject to it here too: re-landing on them inside
the window spends a page load for nothing.

⛔ **NOTHING REASONS ABOUT WHETHER A DATE IS REAL.** Ruled 2026-09-16: *"I don't give a shit about
whether attempt dates are 'real' so that information shouldn't even be accessible to you."*
Dates sort, dates age out, dates park.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKLIST = ROOT / "reports" / "sibling-pair-worklist.tsv"
ATTEMPTS = ROOT / "reports" / "unconnected-p2600.tsv"
FAMILIES = ROOT / "geni-families"
#: This campaign's own attempts. `write-sibling-scrapes.py` writes it, and it exists because
#: `attempt_ledger` covers only `P2600` holders -- see that file. Without it a private profile,
#: which times out and writes no family file, returns in every batch for ever.
LEDGER = ROOT / "reports" / "sibling-scrape-attempts.tsv"

#: The same 30 days `build-unconnected-worklist.py` uses. One constant's worth of duplication
#: against importing a hyphenated module by path; `CLAUDE.md` § *Duplication is deliberate here*.
COOLDOWN = datetime.timedelta(days=30)

TAB = chr(9)


def last_attempted(path=None):
    """`{geni_id: date}` from the attempt ledger. Absent file means nobody is on cooldown."""
    path = path or ATTEMPTS
    out = {}
    if not path.exists():
        return out
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=TAB):
            gid = (row.get("geni_id") or "").strip()
            raw = (row.get("last_attempted") or "").strip()
            if not (gid and raw):
                continue
            try:
                out[gid] = datetime.date.fromisoformat(raw)
            except ValueError:
                continue
    return out


def targets(path=None, today=None):
    """Every worklist member still needing a scrape, in file order, de-duplicated.

    Returns `(ids, column)` -- `column` names which test was used, so the caller can say so
    rather than let a fallback pass for the real thing.
    """
    path = path or WORKLIST
    today = today or datetime.date.today()
    if not path.exists():
        raise SystemExit("%s is absent -- tree.yml builds it" % path)

    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter=TAB))

    column = "parent_in_tree" if rows and "parent_in_tree" in rows[0] else "scraped"
    stamped = last_attempted()

    # ⛔ THE COLUMNS ARE A SNAPSHOT AND THE DIRECTORY IS NOW. `scraped` and `parent_in_tree` are
    # computed when `tree.yml` builds the worklist, so everybody scraped SINCE that build still
    # reads as needing one -- and the batch hands back the same ten people every time it is run,
    # for as long as it takes CI to come round. Measured the first sitting it was used on: ten
    # people scraped, and the next batch printed the same ten.
    #
    # The file on disk is the authoritative answer to *has this person been scraped*, it is free
    # to ask, and asking it makes the batch self-healing between rebuilds rather than dependent
    # on one.
    have_file = {q.name.split("-")[0] for q in FAMILIES.glob("*-family.tsv")} \
        if FAMILIES.exists() else set()
    # The campaign's own cooldown, for everyone the P2600 ledger has no row for.
    ours = last_attempted(LEDGER)

    out, seen = [], set()
    for row in rows:
        gid = (row.get("geni_id") or "").strip()
        if not gid or gid in seen:
            continue
        if (row.get(column) or "").strip():
            continue                       # the tree already knows, or it has been scraped
        if gid in have_file:
            continue                       # scraped since the worklist was last built
        when = stamped.get(gid) or ours.get(gid)
        if when is not None and when + COOLDOWN > today:
            continue                       # inside the 30-day window
        seen.add(gid)
        out.append(gid)
    return out, column


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--count", type=int, default=40,
                    help="how many to print. A working set for one sitting, not a drain queue.")
    ap.add_argument("--skip", type=int, default=0, help="how many to pass over first")
    args = ap.parse_args()

    ids, column = targets()
    batch = ids[args.skip:args.skip + args.count]

    print("# %d still need a scrape, by %s and the live geni-families/ directory; "
          "printing %d from offset %d" % (len(ids), column, len(batch), args.skip))
    if column == "scraped":
        print("# ⛔ FALLING BACK to `scraped`: this worklist has no `parent_in_tree` column, so "
              "tree.yml has not rebuilt since 2026-09-16. The list is wider than the real queue.")
    for gid in batch:
        print(gid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
