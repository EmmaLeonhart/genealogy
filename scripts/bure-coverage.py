"""Which Bureätten people are in the corpus, and which still need an export.

    python scripts/bure-coverage.py

**Emma, 2026-08-28, and it changes the shape of the campaign:** *"the bure people here we
don't need to export from all of them we just need to get all of them in exports"*.

The target is **coverage of the 251**, not one export per person. A `Forest` export returns
up to 5000 people and the Bureätten are one kinship network, so a single export seeded
anywhere inside it can sweep in dozens of them at once. Exporting from all 100 absent people
would therefore be mostly redundant work.

So the loop is: seed one absent person, export, **re-measure**, and only seed for whoever is
still missing. This script is the re-measure step, and the reason it exists as a script rather
than a grep is that it has to run after every single export.

**The campaign ends when the list is empty, and that is her stopping rule.** Emma, same day:
*"we can search through all of the people as we add more since we want all these bureatten
people in the geni synoptic tree and once everyone is covered the campaign is over. Because
these people are quite linked as they are a family relationship to each other."*

## The measurement, and why it is two sources

`reports/derived-labels.csv` carries one row per person in the **merged** tree, so it is the
baseline -- but a freshly downloaded `.ged` is not in it until the merge is re-run, which is
the better part of an hour.

The gap is closed by scanning every `.ged` **modified more recently than the MERGE**, wherever it
sits under `exports/`. Naming directories was the first version and silently under-reported
anything filed elsewhere.

**The freshness mark is `out/merged.ged`, not `reports/derived-labels.csv`, and getting that wrong
cost a day.** `derived-labels.csv` is *derived from* the merge, so regenerating it stamps it with
today's date while the tree behind it may be days old. On 2026-08-29 the merge was **Aug 24 18:20**
and `derived-labels.csv` was **Aug 28 18:24** -- so all 40 campaign exports, run on Aug 28 between
01:25 and 14:00, fell in the gap: too old to be scanned raw, too new to be in the tree. Every one
was invisible, and this script reported **100 of 251 still absent** for a campaign whose own log
ends *"CAMPAIGN COMPLETE: all 251 Bureatten people with a Geni id are now in exports/"*. The true
number was 0, confirmed by scanning every `.ged` directly.

That is `CLAUDE.md` § *Correcting her own record in an export does nothing until the tree is
re-merged* in a new place: **running the analysers is not running the generator**, and a file's
mtime says when it was written, never how fresh its inputs were.

If the merge is missing the script falls back to `derived-labels.csv` and says so, because a
checkout without `out/merged.ged` should still measure something rather than crash.

Rereading the whole corpus would be ~13 GB; this reads only what is new, which is usually one
file.

Writes `reports/bure-coverage.tsv` (all 251, with where each was found) and rewrites
`reports/bure-to-export.tsv` (the still-absent ones, which is what the loop consumes).
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
BUREATTEN = ROOT / "reports" / "bureatten.csv"
DERIVED = ROOT / "reports" / "derived-labels.csv"
COVERAGE = ROOT / "reports" / "bure-coverage.tsv"
TO_EXPORT = ROOT / "reports" / "bure-to-export.tsv"


INDI = re.compile(r"^0 @I(\d+)@ INDI", re.M)


def main() -> None:
    people = []
    with open(BUREATTEN, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            qid = (row.get("qid") or "").strip()
            title = (row.get("sv_title") or "").strip()
            # The column is `geni_ids`, plural.  Every row holds at most one today -- checked,
            # 251 of 576 rows, no separator character in any of them -- but a person with two
            # unmergeable Geni profiles is ordinary here (CLAUDE.md: a second P2600 is not a
            # conflict), so the split is written now rather than after it silently truncates.
            for gid in re.split(r"[|;,]", row.get("geni_ids") or ""):
                gid = gid.strip()
                if gid and qid:
                    people.append((gid, qid, title))
    if not people:
        sys.exit(f"no Bureatten rows carried both a geni id and a QID -- that is a broken read "
                 f"of {BUREATTEN.name}, not an empty category")

    wanted = {gid for gid, _, _ in people}
    where: dict[str, str] = {}

    with open(DERIVED, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            gid = (row.get("geni_id") or "").strip()
            if gid in wanted:
                where.setdefault(gid, "merged tree")

    # Every export the merge has not seen yet, wherever it was filed.
    # The MERGE's own timestamp -- see the docstring. `derived-labels.csv` is derived from it and
    # can be far newer than the tree it describes, which is how 40 exports went unseen.
    merged_ged = ROOT / "out" / "merged.ged"
    if merged_ged.exists():
        merged_at = merged_ged.stat().st_mtime
    else:
        merged_at = DERIVED.stat().st_mtime
        print("out/merged.ged is absent; falling back to derived-labels.csv as the freshness "
              "mark, which UNDER-reports coverage if the merge is older than it")
    fresh = [g for g in sorted((ROOT / "exports").rglob("*.ged"))
             if g.stat().st_mtime > merged_at and "excluded" not in g.relative_to(ROOT).parts]
    for ged in fresh:
        text = ged.read_text(encoding="utf-8", errors="replace")
        rel = ged.relative_to(ROOT).as_posix()
        for gid in INDI.findall(text):
            if gid in wanted:
                where.setdefault(gid, rel)

    rows = [{"geni_id": g, "qid": q, "sv_title": t,
             "in_corpus": "yes" if g in where else "no", "found_in": where.get(g, "")}
            for g, q, t in people]
    rows.sort(key=lambda r: (r["in_corpus"] == "yes", r["geni_id"]))

    with open(COVERAGE, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["geni_id", "qid", "sv_title", "in_corpus", "found_in"],
                           delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    absent = [r for r in rows if r["in_corpus"] == "no"]
    with open(TO_EXPORT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["geni_id", "qid", "sv_title"], delimiter="\t")
        w.writeheader()
        w.writerows([{k: r[k] for k in ("geni_id", "qid", "sv_title")} for r in absent])

    held = len(rows) - len(absent)
    print(f"{len(fresh)} export(s) newer than the merge were scanned raw")
    print(f"{len(rows)} Bureatten people carrying both a Geni id and a QID")
    print(f"   {held} in the corpus, {len(absent)} still absent")
    for r in rows:
        if r["found_in"].startswith("exports/"):
            print(f"   {r['geni_id']} {r['sv_title']} <- {r['found_in']}")
    print(f"\nwrote {COVERAGE.name} (all {len(rows)}) and {TO_EXPORT.name} ({len(absent)})")


if __name__ == "__main__":
    main()
