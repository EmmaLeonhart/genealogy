"""Who still needs the collector. DERIVED on every run -- no list is ever hand-edited.

**Asked how progress is tracked and how to mark the skipped people undone**, the answer was
*"really just mark the skipped people all as not done yet ... and then run it on them again
alongside the other people, order is actually not important and it is best for them to just be
normal queue members in this thing lol."*

**So nothing is deleted to mark work undone.** That matters: a person who came back a blood-only
miss still has a real family scrape on disk, and removing them from a list -- or removing the
list row -- would either destroy that or require a second bookkeeping file to remember it. The
worklist is recomputed from what is on disk, so changing the DEFINITION of done re-queues people
automatically. It already did: the moment `via` became the record of which search answered, every
blood-only miss re-entered the pool without a row being touched.

Two reasons a person is outstanding, and they are rules 1 and 2:

    never scraped     no `geni-families/<id>-family.tsv`
    blood-only miss   an `isolates.csv` row with path_found=no whose `via` does not record
                      that the other-ways search was run -- *"If blood did not hit and there
                      is no path then redo it."*

⛔ **A PERSON WHO ALREADY HAS A BLOOD PATH IS NOT RE-QUEUED.** Rule 3, and it is an accepted
cost rather than an oversight: *"I do not care about non-blood relationships among people
already connected because I am time conscious and this shit is taking way too long and I do not
want you to do that massive work. These first people covered just get worse coverage and that is
life."* So `path_found=yes` is done, whatever `via` says.

⛔ **ORDER IS NOT IMPORTANT AND THE TWO REASONS ARE NOT SEPARATE CAMPAIGNS.** *"it is best for
them to just be normal queue members."* The output is one pool; the `why` column is there to be
read, not to be sorted on.
"""

from __future__ import annotations

import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAMILIES = ROOT / "geni-families"
ISOLATES = ROOT / "reports" / "isolates.csv"
OUT = ROOT / "reports" / "collector-worklist.tsv"

#: Every roster the collector draws targets from. A person in any of them is in scope.
#:
#: ⛔ **THE FIRST ENTRY IS THE POPULATION. THE OTHER TWO ARE PILOT ROSTERS AND WERE NEVER IT.**
#: Emma, 2026-09-09, asked what the scope actually is: *"Every p2600 holder who is disconnected
#: from Charlemagne in the synoptic tree (combination of our geni exports and what exists on
#: wikidata). The idea is that all p2600 people should either be confirmed impossible to connect,
#: or connected. Connection to Charlemagne is our proxy for connection to the main graph as
#: Charlemagne is one of the most central people."*
#:
#: This tuple held ONLY the two pilot files until then -- 4,360 people between them -- so the
#: campaign ran over **0.8%** of the population, chosen by which roster happened to be on disk.
#: `scripts/p2600-connectivity.py` computes the real one: of **518,889** holders, 252,688 are
#: already connected and **266,201 are not**. A connected person needs no capture at all, which
#: is the half the old question could not ask.
#:
#: The pilot rosters STAY. Everyone in them who is genuinely disconnected is in the new file
#: anyway, and a person already captured is filtered by `scraped()` either way -- so keeping them
#: costs nothing and dropping them would silently retire work in flight.
ROSTERS = (
    ("reports/p2600-disconnected.tsv", "geni_id"),
    ("reports/sibling-pair-worklist.tsv", "geni_id"),
    ("reports/isolate-path-pilot.tsv", "geni_id"),
)


def scraped(gid: str) -> bool:
    return (FAMILIES / ("%s-family.tsv" % gid)).exists()


def isolate_rows() -> dict:
    if not ISOLATES.exists():
        return {}
    with ISOLATES.open(encoding="utf-8") as fh:
        return {r["geni_id"]: r for r in csv.DictReader(fh) if r.get("geni_id")}


def targets() -> dict:
    """geni_id -> label, over every roster. Later rosters do not overwrite an earlier label."""
    out = {}
    for rel, key in ROSTERS:
        p = ROOT / rel
        if not p.exists():
            continue
        with p.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                gid = (row.get(key) or "").strip()
                if not gid:
                    continue
                label = (row.get("name") or row.get("label") or "").strip()
                if gid not in out or (label and not out[gid]):
                    out[gid] = label
    return out


def outstanding():
    iso = isolate_rows()
    rows = []
    for gid, label in targets().items():
        row = iso.get(gid)
        if not scraped(gid):
            rows.append((gid, label, "never-scraped"))
            continue
        if not row:
            continue
        verdict = (row.get("path_found") or "").strip()
        via = (row.get("via") or "").strip().lower()
        # Rule 3: a blood path is done, whatever `via` says. Rule 2: a blood-only miss is not.
        if verdict == "no" and via not in ("inlaw", "both", "neither"):
            rows.append((gid, label or row.get("label", ""), "blood-only-miss"))
        # ⛔ A BLANK VERDICT MEANS *COME BACK LATER*, AND NOTHING WAS COMING BACK.
        #
        # `write-family-scrape.py` is explicit that the blank is load-bearing -- *"blank costs a
        # revisit and `yes` costs the measurement"*, and *"a pending search folded into the miss
        # column is the failure `geni-paths/README.md` records"*. It writes blank precisely so
        # the person is asked again. This function tested `verdict == "no"` and nothing else, so
        # a scraped person with no verdict matched no reason at all and left the pool for good --
        # the one outcome the three-valued column exists to prevent.
        #
        # Measured 2026-09-08: **11 rows**, every one of them scraped, every one with a blank
        # anchor as well -- Asser de Haan, Julius Hohenberger, Natalia Krebs, Bohumil Eisner,
        # Jakob Bettmann among them. `queue.md` even counted them, as *"11 with no verdict yet"*
        # excluded from the reach rate, without anything noticing they could never be revisited.
        #
        # A requested search DECAYS back to unrequested within hours, so this is not a rare
        # transient: any person whose search had not landed when the tab was harvested lands
        # here. Same rule, one state further along: if the question has no answer yet,
        # it has not been answered.
        elif not verdict:
            rows.append((gid, label or row.get("label", ""), "pending-no-verdict"))
    # Sorted on the geni id for a deterministic file -- CLAUDE.md SORTING MUST BE DETERMINISTIC.
    # This is NOT a priority order; rule 4 is that order does not matter.
    return sorted(rows, key=lambda r: r[0])


def main() -> int:
    rows = outstanding()
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["geni_id", "label", "why"])
        w.writerows(rows)
    by = {}
    for _, _, why in rows:
        by[why] = by.get(why, 0) + 1
    print("%d outstanding -> %s" % (len(rows), OUT.relative_to(ROOT)))
    for why in sorted(by):
        print("   %-16s %d" % (why, by[why]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
