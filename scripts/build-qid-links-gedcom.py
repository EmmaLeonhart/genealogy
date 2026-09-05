"""Three people's Wikidata links, as GEDCOM notes.

    python scripts/build-qid-links-gedcom.py

**A bio Wikidata link is a specific entity-resolution strategy, not a property of the tree.**
Emma, 2026-08-29: *"the tree shouldnt bio wikidata links are just a specific entity resolution
strategy"*. The technique is hers and it already exists in the other direction — she writes a
Wikidata URL into a Geni About Me by hand, Geni exports it as a `NOTE`, and
`scripts/build-geni-qid-links.py` reads the QID back out. This file applies that same technique
to **three people she identified where the link was never written**, so the correspondence has
somewhere to live besides her scratchpad.

**It is three records. Do not let it become an architecture.** An earlier version of this
docstring said the file existed so the synoptic tree *"ALWAYS"* carried QID links, which is the
tree-wide framing she rejected — and the code under it emitted 83,988 people. Both were
generalisations of *"When the synoptic tree is merged we change all of their bios to links to
their qids"*, where *their* meant the people named below and nobody else.

## THREE people, not the whole correspondence

**Emma, 2026-08-29:** *"it was supposed to be to three individuals lol."* The first version of
this script emitted every pairing in `reports/synoptic-correspondence.tsv` that landed on somebody
in our tree -- **83,988 individuals**. That was a generalisation of a specific instruction and she
never asked for it.

The three are the residue of a retired side file: identities she *"put a lot of effort into
creating identification with"*, whose Wikidata items carry **no `P2600`**, so the pairing exists
nowhere outside that scratchpad. Checked live 2026-08-29. The rest of the file's nine pairs are
already handled and are deliberately absent here -- `Q11443857` Futohime is in `CJK_CLAN_BLOCK`,
`Q19657284` and `Q12598947` already carry their `P2600`, the two Kitajima items are in
`NEVER_TOUCH_QID`, and the ninth is Emma herself, who must never enter the traversable graph.

**Widening this to the full correspondence is a decision, not a default.** It is one constant
below and the filtering already works, but 84,000 links is a different act from three and wants
her word first.

## `exports/post-merge/`, her choice when asked

`sources._post_merge_last` sorts that directory to the **end** of merge order explicitly — she
asked for a directory whose records *"overwrite earlier ones from other repos in the synoptic
tree"*, and alphabetical order would have put `post-merge` before `samaritans` and `tanba`. So
this applies last, which is what an overlay wants.

Being under `exports/` makes it corpus: `sources.find_exports` globs the directory, so the three
links reach the tree without anything having to be run afterwards. That is the right trade at
three records; it is the reason the count matters and the reason widening it is a decision rather
than a default.

## Why it merges rather than duplicating

Records are keyed on the xref, which is the Geni profile id — `CLAUDE.md`'s primary key. So
`0 @I6000000001846508982@ INDI` here is **the same record** as that person in every other export,
and its `NOTE` joins theirs. `merge.ALWAYS_REPEATABLE` holds `NOTE`, so nothing is overwritten:
repeatable paths with a value are matched on that value, an identical line collapses, a different
one is kept alongside. Re-generating and re-merging is therefore idempotent.

## The source is her hand identifications, and the first attempt got that wrong too

Reading `reports/synoptic-correspondence.tsv` and filtering it to the three returned **0 of 3** —
which is not a bug, it is the point restated. That report joins five places a pairing can live
and that side file was not one of them, so these three are invisible to it. They exist in
her scratchpad and nowhere else, which is exactly why writing them into the tree is worth doing.

The pairs are inlined below, because the parser that read them and the file it read are both
file parses with zero unparsed entries.

## Every record must already exist in the tree

An `INDI` whose xref the merge has not seen is a **new person**, so an unfiltered emit would mint
people rather than annotate them. Checked against `reports/derived-labels.csv`, one row per person
in the merged tree, and an id that fails the check is printed as a finding rather than skipped
quietly.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

IN_TREE = ROOT / "reports" / "derived-labels.csv"
OUT = ROOT / "exports" / "post-merge" / "wikidata-qid-links.ged"

#: The three, by Geni id. Named explicitly rather than derived: they are the ones whose Wikidata
#: item carries no `P2600`, and that is a live fact about Wikidata which will stop being true the
#: moment these links are acted on -- so a rule that recomputed it would empty this file and look
#: like success. An explicit list says what was decided and when.
#: **The pairs themselves, since the side file is gone.** It was deleted in `12f3134a`
#: and the deletion was right -- `CLAUDE.md` § *LEGACY CODE IS DELETED* -- but this script kept
#: reading it and had no guard, so it crashed with `FileNotFoundError` and stayed crashed through
#: four dead-item sweeps.
#:
#: **The correspondence is not a substitute: 0 of these 3 are in
#: `reports/synoptic-correspondence.tsv`.** Checked rather than assumed. They are hers by hand,
#: from identities she *"put a lot of effort into creating identification with"*, and no
#: automated source reaches them -- which is exactly why they were in a hand-written file.
#:
#: So they live here as a constant, which is what `queue.md` already says: *"widening this beyond
#: the three is her call and is one constant."*
PAIRS = {
    "6000000001835522164": "Q11596350",   # 稚武彦命 Wakatakehiko
    "6000000001844033355": "Q11078587",   # 播磨稲日大郎姫 Harima no Inabi, his daughter
    "6000000002039751362": "Q24890131",   # 物部伊莒弗 Mononobe no Ikofutsu

    # **Empress Jingū, added 2026-09-01 on her instruction:** *"add to the identifications
    # gedcom so that Jingu is linked on geni and wiki data in the future"*.
    #
    # `Q232803` is 神功皇后 — 38 sitelinks, no `P2600`, so nothing joins her by id and the
    # zipper cannot reach her either. **Geni holds two profiles for her**, which is the
    # ordinary unmergeable-duplicate case `CLAUDE.md` records, so both are linked to the one
    # item rather than one being picked.
    "6000000001846508982": "Q232803",   # 神功皇后 Jingū-kōgō (Okinagatarashi-hime)
    "6000000045545840003": "Q232803",   # the same person, Geni's second profile
}
ONLY = set(PAIRS)

LINK = "https://www.wikidata.org/wiki/{qid}"


def main():
    in_tree = set()
    with IN_TREE.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("geni_id"):
                in_tree.add(row["geni_id"].strip())
    print(f"{len(in_tree):,} people in the merged tree")

    pairs = collections.defaultdict(set)
    for geni_id, qid in PAIRS.items():
        pairs[geni_id].add(qid)
    print(f"{len(pairs)} pairs, from the constant in this file")

    absent = sorted(g for g in pairs if g not in in_tree)
    if absent:
        # Never silently: emitting one of these would CREATE the person rather than annotate
        # them, which is the failure the tree filter exists to stop.
        print(f"REFUSING -- not in the merged tree, would be minted as new people: {absent}")
        for g in absent:
            pairs.pop(g)
    for g in sorted(ONLY - set(pairs)):
        print(f"not emitted: {g}")

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
