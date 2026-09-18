"""The three identification ledgers, each rendered as a GEDCOM the merge reads.

    python scripts/build-identification-gedcoms.py

⛔ **THREE FLAT TSVs. NOTHING ELSE. Ruled 2026-09-17, and the reason is me.**

    reports/entry-points-now.tsv    an entry point TODAY
    reports/entry-points-jan1.tsv   an entry point on 2027-01-01
    reports/identifications.tsv     passive: a QID identification and nothing more

Every one of them is the same two columns — `qid` and `geni_id` — and every one of them does the
same thing to the tree: it puts a Wikidata link in a bio, which is a QID-to-Geni identification.
**The only difference between the three is when, or whether, the person becomes an entry point.**

*"basically all of these get built into GEDCOMs ... with the difference being that one cohort of
them is immediate entry points, one cohort of them is passive, and one cohort of them is entry
points that occur at January 1st."*

## ⛔ WHY IT LOOKS LIKE THIS, WHICH IS NOT A TECHNICAL REASON

*"we are doing this because of the fact that you aren't able to hold these things consistently
together ... it's clear to me that this stuff is way too fucking confusing for you ... despite the
fact it was working fine, you were always consistently breaking it because it was not transparent
enough to you what it was."*

The scheme this replaces worked. It was a constant inside `build-qid-links-gedcom.py`, seven
roster files, `reports/entry-point-groups.tsv` carrying an `active_from` per group, and
`reports/entry-points.tsv` carrying an `active_from` per person — and answering *is this person an
entry point, and when* meant holding all four in your head at once. Every session it was touched,
it was described wrongly: *"in the GEDCOM"* is technically true and **fundamentally
misrepresents what is going on**, so the next reader invents something. This file exists so the
answer is *which of three TSVs is the pair in*, and nothing else.

## ⛔ A PAIR MAY BE IN ALL THREE. ANY CHECK THAT BLOCKS THAT IS WRONG

*"something can be in every single one of these buckets. If there's any kind of check that somehow
blocks anything from happening in the January 1st one, it's wrong."*

There is no de-duplication across the ledgers here and there must not be one. The passive
identification is **contained within** the other two: an entry point is also an identification, so
a pair appearing in `entry-points-jan1.tsv` and again in `identifications.tsv` is the normal case,
not a conflict to resolve. 38 pairs were in both the day this was built.

And a January-1st pair is not fenced off before its date. *"If any one of the January 1st one is
eligible to be edited, it can have the Geni ID added to it before it's an entry point."* The date
governs entry-point status alone — never whether a statement may be written.

## ⛔ NO PROVENANCE. THE IDS ARE GOSPEL

*"There's a ton of Providence TSV stuff present there. It should all be completely fucking removed
because of the fact that specifically there is no reason why you, the agent, should have any
knowledge of where it is that any of these IDs came from ... These IDs are accepted as gospel by
you. You do not question them. You do not question them. I add to them."*

So the ledgers carry two columns. No label, no note, no date, no batch, no verdict, no source
file. Every pair that used to arrive through `izumo-p2600-pairs.tsv`, `tanba-p2600-pairs.tsv`, the
emperor rosters, the Samaritan lists or a hand-written constant is simply a row now. Where it came
from is not a question this repo answers, and a column inviting it is a column that gets reasoned
about wrongly.

## ⛔ THE GEDCOMs ARE BUILD OUTPUT AND ARE GITIGNORED

*"All of them get built into gitignored GEDCOM files that then get merged together into the
synoptic tree, placing a Wikidata ID link in one of the bios in the synoptic tree."*

`CLAUDE.md` § *never gitignore a `.ged`* is about the CORPUS — a real Geni export, which exists
nowhere else and cannot be regenerated. These three are neither: they are a rendering of three
committed TSVs, reproducible byte-for-byte by running this file. Committing them would mean the
same pairs living in two places and drifting, which is the failure the whole change is against.
The three paths are named individually in `.gitignore`; **no `*.ged` pattern is written**, because
that rule stands and a pattern would swallow the corpus.

⛔ **AND THEY GO IN `out/`, NOT `exports/`.** `exports/` is the corpus and every `.ged` in it is
committed — `tests/test_repo_invariants.py` compares `git ls-files` against `find`, so a generated
file there fails the suite the moment it is written. This is the same placement, and the same
reasoning, as `out/manual-parental-correspondences.ged` and `out/wikidata-tree.ged`.

⛔ **THE SLIM TREE DROPS `NOTE`, SO THE BIO LINK DOES NOT SURVIVE THE REBUILD CI RUNS.**
`genimerge.slim.DROP_INSIDE` holds `NOTE` and `tree.yml` runs `--slim`. Measured, not reasoned —
`devlog.md` 2026-09-08. These three files are therefore correct in a plain merge and inert in the
slimmed one, exactly as `out/manual-parental-correspondences.ged` already is. **That is why the
TSVs are the operative source**: every consumer reads the ledger directly, and the GEDCOM route is
the tree-side overlay, not the mechanism entry points depend on.

**So this has to RUN before the merge does.** `rebuild-everything.py` calls it. A generated file
that nothing generates is an empty directory in CI and a silently smaller tree.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "out"

#: ledger -> the GEDCOM it renders to. The names say which bucket, so a file listing answers the
#: question this whole change exists to make answerable.
LEDGERS = (
    ("entry-points-now.tsv", "identifications-now.ged",
     "entry points effective immediately"),
    ("entry-points-jan1.tsv", "identifications-jan1.ged",
     "entry points effective 2027-01-01"),
    ("identifications.tsv", "identifications-passive.ged",
     "passive identifications: a QID link and no entry-point status"),
)


def pairs(path: Path):
    """`(qid, geni_id)` rows, in file order, skipping anything malformed.

    Two columns and no judgement. A row that is not a `Q`-prefixed id beside a digit string is
    skipped rather than repaired: this file does not adjudicate the ledgers, it renders them.
    """
    if not path.exists():
        return []
    out = []
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            qid = (row.get("qid") or "").strip()
            gid = (row.get("geni_id") or "").strip()
            if qid.startswith("Q") and gid.isdigit():
                out.append((qid, gid))
    return out


def render(rows, note):
    """One `INDI` per Geni id, carrying one `NOTE` per QID. No relationship data.

    A Geni id appearing twice with different QIDs gets both notes under one `INDI`, because two
    `INDI` records with the same xref is a broken GEDCOM. The same pair twice is written once.
    """
    by_id: dict[str, list[str]] = {}
    for qid, gid in rows:
        seen = by_id.setdefault(gid, [])
        if qid not in seen:
            seen.append(qid)
    lines = [
        "0 HEAD",
        "1 SOUR genimerge",
        "2 NAME scripts/build-identification-gedcoms.py",
        "1 NOTE Generated from a two-column TSV ledger. Do not edit: edit the TSV and rebuild.",
        "2 CONT " + note,
        "1 GEDC",
        "2 VERS 5.5.1",
        "2 FORM LINEAGE-LINKED",
        "1 CHAR UTF-8",
    ]
    for gid in sorted(by_id, key=lambda g: (len(g), g)):
        lines.append("0 @I%s@ INDI" % gid)
        for qid in by_id[gid]:
            lines.append("1 NOTE https://www.wikidata.org/wiki/%s" % qid)
    lines.append("0 TRLR")
    return "\n".join(lines) + "\n", len(by_id)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for ledger, ged, note in LEDGERS:
        rows = pairs(ROOT / "reports" / ledger)
        text, people = render(rows, note)
        (OUT_DIR / ged).write_text(text, encoding="utf-8")
        total += len(rows)
        print("%-24s %5d pairs, %5d people -> out/%s"
              % (ledger, len(rows), people, ged))
    print("%d pairs over three ledgers. A pair may appear in more than one; that is allowed."
          % total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
