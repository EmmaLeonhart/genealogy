"""A GEDCOM that is nothing but Wikidata links, so the synoptic tree ALWAYS carries them.

    python scripts/build-qid-links-gedcom.py

**Emma, 2026-08-29:** *"Overwrite the bio in every one of the gedcoms or make a gedcom that's
just a thing that gives gedcom notes with the links like this. Wherever you do just please hurry
the fuck up in making the thing do the synoptic tree always gets these things."*

**This is the second option, and `always` is the reason.** A post-processing pass over
`out/merged.ged` is a step someone has to remember to run, and the first time it is forgotten the
tree silently loses every link. A GEDCOM in `exports/` is corpus: `genimerge.sources.find_exports`
globs it, so *every* merge from now on includes the links whether or not anybody thought about it.

## Where it goes, and why that directory

`exports/post-merge/`. `sources._post_merge_last` sorts that directory to the **end** of merge
order explicitly — Emma asked for a directory whose records *"overwrite earlier ones from other
repos in the synoptic tree"*, and alphabetical order would have put `post-merge` before
`samaritans`, `tanba` and three others. So this file is applied last, which is what an overlay
wants.

## Why it merges rather than duplicating

Records are keyed on the xref, which is the Geni profile id — `CLAUDE.md`'s primary key. So
`0 @I6000000087535357291@ INDI` here is **the same record** as that person in every other export,
and its `NOTE` joins theirs. `merge.ALWAYS_REPEATABLE` holds `NOTE`, so nothing is overwritten:
repeatable paths with a value are matched on that value, an identical line collapses, a different
one is kept alongside. Re-generating and re-merging is therefore idempotent.

## Only people we actually have

**The correspondence covers 563,938 Geni ids and most of them are not in our tree.**
`out/wikidata/p2600-all.tsv` is a slice of Wikidata, not of our corpus, so emitting an `INDI` for
every row would *create* several hundred thousand people who exist nowhere in the genealogy —
the merge would happily mint them, because a record with an unseen xref is a new person. Filtered
against `reports/derived-labels.csv`, which is one row per person actually in the merged tree.

## A person with several QIDs gets several `NOTE`s

Never a choice between them. 772 such cases are in `reports/synoptic-conflicts.tsv`, and picking
one would be an entity resolution this script has no standing to make — the mirror of `CLAUDE.md`
§ *A second Geni ID on one Wikidata item is NOT a conflict*: multiplicity is recorded, not
adjudicated.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

PAIRS = ROOT / "reports" / "synoptic-correspondence.tsv"
IN_TREE = ROOT / "reports" / "derived-labels.csv"
OUT = ROOT / "exports" / "post-merge" / "wikidata-qid-links.ged"

LINK = "https://www.wikidata.org/wiki/{qid}"


def main():
    in_tree = set()
    with IN_TREE.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("geni_id"):
                in_tree.add(row["geni_id"].strip())
    print(f"{len(in_tree):,} people in the merged tree")

    pairs = collections.defaultdict(set)
    with PAIRS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            g, q = (row.get("geni_id") or "").strip(), (row.get("qid") or "").strip()
            if g in in_tree and q:
                pairs[g].add(q)
    print(f"{len(pairs):,} of them carry at least one QID")

    multi = sum(1 for qs in pairs.values() if len(qs) > 1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        # A minimal but valid 5.5.1 header. `SOUR` names this script so the file is
        # traceable to what made it rather than looking like a Geni download.
        out.write("0 HEAD\n")
        out.write("1 SOUR genimerge\n")
        out.write("2 NAME scripts/build-qid-links-gedcom.py\n")
        out.write("1 GEDC\n")
        out.write("2 VERS 5.5.1\n")
        out.write("2 FORM LINEAGE-LINKED\n")
        out.write("1 CHAR UTF-8\n")
        written = 0
        for geni_id in sorted(pairs):
            out.write(f"0 @I{geni_id}@ INDI\n")
            for qid in sorted(pairs[geni_id]):
                out.write(f"1 NOTE {LINK.format(qid=qid)}\n")
                written += 1
        out.write("0 TRLR\n")

    print(f"{written:,} NOTE links over {len(pairs):,} individuals")
    print(f"{multi:,} people carry more than one QID; each gets one NOTE per QID")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
