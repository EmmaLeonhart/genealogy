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

**⛔ AND THE ORDER IS THE DESCENDANTS CAMPAIGN FIRST, NOT THE `Descendants` WALK FIRST.**
*"the descendants export things beat the forest people later"*, then, when the first version of
this sorted on the walk and buried the Chinese root's `Forest` among the isolates:
*"the forest exports on the paths ... we have this list of good people to export, and in my eyes
we probably shouldn't be completely abandoning them, but they aren't that high a priority for us
relative to the descendants campaign, because the descendants campaign stuff generally gives us
actually useful information about, like, descendants of figures."*

**The axis is the CAMPAIGN.** A `Forest` that is step one of a three-step descendants root is not
an isolate `Forest` and must not sort with them. So the key is

    owed  ->  PRIORITY  ->  campaign  ->  walk  ->  id

`PRIORITY` is a column on `reports/export-queue-seeds.csv`, default 50, and it exists for
rulings that are not derivable — the Chinese root `NN Father of Huaxu` is **0**, because
*"this is the most important one"*, and its `Forest` therefore heads the whole queue despite
being a `Forest`. The isolate rows have no priority column and take the default, which puts them
behind every descendants row of either walk.

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

COLUMNS = ["geni_id", "label", "walk", "campaign", "priority", "why", "state"]


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
                            DEFAULT_PRIORITY,
                            "cleared the 250 floor with no path either way",
                            "done" if gid in done else "owed"])

    if SEEDS.exists():
        with SEEDS.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                gid = row["geni_id"]
                out.append([gid, row.get("label", ""), row.get("walk", "Descendants"),
                            "descendants",
                            int(row.get("priority") or DEFAULT_PRIORITY),
                            row.get("why", ""),
                            "done" if gid in done else "owed"])
    return out


WALK_RANK = {"Descendants": 0, "Forest": 1}
CAMPAIGN_RANK = {"descendants": 0, "isolates": 1}
DEFAULT_PRIORITY = 50


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    all_rows = rows()
    owed = [r for r in all_rows if r[6] == "owed"]
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(COLUMNS)
        # owed first, then DESCENDANTS BEFORE FOREST -- ruled 2026-09-13, see the header.
        writer.writerows(sorted(
            all_rows,
            key=lambda r: (r[6] != "owed", int(r[4]), CAMPAIGN_RANK.get(r[3], 9),
                           WALK_RANK.get(r[2], 9), r[0])))
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
