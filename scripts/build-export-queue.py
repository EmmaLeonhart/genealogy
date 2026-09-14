"""The queue of Geni exports still owed, derived from what is on disk.

    python scripts/build-export-queue.py

**Asked for 2026-09-13:** *"for our wikidata isolates connection campaign: I want us to have a
set up queue of geni exports, a csv file, each one has the actual export target individual and
specifies the type (we only do descendants and forest to my knowledge)."*

Writes `reports/export-queue.csv`: one row per export still owed, naming the person the export
runs ON and the walk it runs. **Two walks and no others** — `Forest` and `Descendants` — which is
what the campaigns actually use of the five Geni offers.

## ⛔ NO NEW *ISOLATE* ROWS, AND DESCENDANTS OUTRANK FOREST. Ruled 2026-09-13

Emma, once the path GET was running: *"I still wanna complete the gedcom downloads... but I kind
of want to finish all of the queued ones and not queue up anymore, because this new method
doesn't really save anything from the pages, and as a result it is not going to get the census
information, and we don't really want the census information at this point."*

**That closes the ISOLATES side and nothing else.** 41 were owed when it landed and **37 of them
were `isolates` Forests** — the exact category the path GET replaces. They still run, because she
values the GEDCOMs; no new isolate row joins them, and what replaces the isolates Forest is the
relationship path saved as a tiny GEDCOM per person.

**⛔ IT DOES NOT CLOSE THE DESCENDANTS CAMPAIGN, AND READING IT THAT WAY WAS AN ERROR.**
Corrected the same evening, directly: *"This is not a ruling that I made. I did not make the
whole program is not started ruling. You did that."* § *THE WHOLE PROGRAM* is live — the eight
untouched seeds, Genghis, the Aztec, the Inca, more rounds on Näf, ben Ovadya and Dál Fiatach,
and `no-name` across rounds. New descendants seeds are queued as they are found.

**⛔ AND THE ORDER IS DESCENDANTS FIRST.** *"the descendants export things beat the forest people
later, if that makes sense."* The serial slot is the scarcest thing in this whole operation and
`Descendants` is the walk the time-sensitive campaign needs — the descendants of these people are
poorly documented and get removed abruptly. A `Forest` for an isolate now has a cheap substitute
and can wait; a `Descendants` ball does not. So the sort puts every `Descendants` row above every
`Forest` row, whatever campaign it belongs to.

## ⛔ DERIVED, NEVER HAND-EDITED

`CLAUDE.md` § *Progress is DERIVED, never stored*. A row disappears when its ball appears in
`exports/`, so the file cannot drift from the corpus and nothing has to be ticked off. Re-run it
after every collection.

## Where the rows come from, and which walk each gets

**The isolate campaign** — `reports/isolates.csv` rows flagged `exported=yes`, meaning the
collector's statistics gate cleared the 250 floor and an export is warranted. Their walk is
**`Forest`**: `docs/collector-run-loop.md` § *it iterates through the family tree to add the
individual and runs the `Forest` export*. Ruled again 2026-09-13 after three of them went out as
`Descendants` — *"Descendants was only a thing we were doing for the descendants campaign and it
is kinda useless for the wikidata isolates campaign"* — and fixed in extension 1.7.48.

**The descendants campaign** — the roster in `queue.md`. Their walk is **`Descendants`**, and
`CLAUDE.md` says so in capitals: *`Descendants`, NOT `Forest`* — `Forest` follows spouse links and
spends the 5,000 slots sideways when the ball needs to go down. Those seeds are listed by hand in
`reports/export-queue-seeds.csv` because they come from rulings rather than from a measurement.

## ⛔ THE EXPORT RUNS ON A CREATED ANCESTOR, NOT ON THE PERSON NAMED HERE

For anyone this account does not own, `https://www.geni.com/gedcom/export/<id>` answers *"You are
not allowed to export that profile."* The row names the person the export is FOR; the climb
creates an ancestor above them and the export is seeded there. `filed_as` records where the ball
landed, which is under the created ancestor's id and not this one.
"""

from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISOLATES = ROOT / "reports" / "isolates.csv"
SEEDS = ROOT / "reports" / "export-queue-seeds.csv"
LOG = ROOT / "reports" / "descendants-export-log.csv"
OUT = ROOT / "reports" / "export-queue.csv"

COLUMNS = ["geni_id", "label", "walk", "campaign", "why", "state"]


def already_exported():
    """Every person named in the export log, however the row phrases it."""
    if not LOG.exists():
        return set()
    text = LOG.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"\b(\d{10,})\b", text))


def rows():
    done = already_exported()
    out = []

    if ISOLATES.exists():
        with ISOLATES.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if (row.get("exported") or "").strip() != "yes":
                    continue
                gid = row["geni_id"]
                out.append([gid, row.get("label", ""), "Forest", "isolates",
                            "cleared the 250 floor with no path either way",
                            "done" if gid in done else "owed"])

    if SEEDS.exists():
        with SEEDS.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                gid = row["geni_id"]
                out.append([gid, row.get("label", ""), row.get("walk", "Descendants"),
                            "descendants", row.get("why", ""),
                            "done" if gid in done else "owed"])
    return out


WALK_RANK = {"Descendants": 0, "Forest": 1}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    all_rows = rows()
    owed = [r for r in all_rows if r[5] == "owed"]
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(COLUMNS)
        # owed first, then DESCENDANTS BEFORE FOREST -- ruled 2026-09-13, see the header.
        writer.writerows(sorted(
            all_rows,
            key=lambda r: (r[5] != "owed", WALK_RANK.get(r[2], 9), r[3], r[0])))
    by_walk = {}
    for r in owed:
        by_walk[r[2]] = by_walk.get(r[2], 0) + 1
    print("%d export(s) owed of %d row(s)" % (len(owed), len(all_rows)))
    for walk, n in sorted(by_walk.items()):
        print("  %-12s %d" % (walk, n))
    print("-> %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
