"""Wikidata's genealogy as a GEDCOM, so the synoptic tree merge absorbs it.

    PYTHONPATH=src python scripts/build-wikidata-gedcom.py
    PYTHONPATH=src python -m genimerge merge --also out/wikidata-tree.ged

**§ 0 and § 1 of `docs/unconnected-worklist.md`.** The dictation of 2026-09-09 opens *"I don't
think that the CI/CD currently combines the WikiData tree with the geni trees"* and that was
checked and is true: `rebuild-everything.py` merges `exports/**/*.ged` plus one small
correspondence overlay, and Wikidata's relationship edges are nowhere in `out/merged.ged`.

**Natively a GEDCOM, and that is the point rather than a format choice** — *"the syntactic tree
now has a canonical form that is natively a Gedcom because that means that it preserves the
family IDs, which is important for some stuff."* `scripts/p2600-connectivity.py` answers the
connected/disconnected question with a union-find over edges, which destroys exactly that.

## The xref is the Geni id, which is what makes this a merge and not an import

`CLAUDE.md`: *"The Geni profile ID is the primary key for everything."* So a `P2600` holder is
written as `@I<geni id>@` with `1 RFN geni:<geni id>`, and the merge fuses it with the corpus
person of the same id by exact join. Nobody is created twice and no name matching happens.

## ⛔ NO INVENTED PEOPLE. A QID WITH NO `P2600` IS AN ABSENT SLOT

A Wikidata item carrying no Geni id has no primary key here, so it cannot become an `INDI`
without minting an identifier for it. `queue.md` § *What this session settled*: **an unknown
parent is an ABSENT SLOT, never an `NN` person** — and `build-scraped-gedcom.py` was deleted for
inventing 4,928 of them.

So an edge is emitted only where **both** ends carry a `P2600`. That loses the case
`p2600-connectivity.py` deliberately keeps — two Geni-linked people joined only through an
unlinked Wikidata item — and losing it is the conservative error, because the alternative is
asserting people into the tree. The run counts what it drops, so the cost is measured rather
than assumed.

## ⛔ A PARENT EDGE NEEDS A SLOT, AND WIKIDATA'S `P40` DOES NOT SAY WHICH

`P22` *father* and `P25` *mother* name the slot. `P40` *child* does not: it says X is a parent
of C and nothing about whether X is the father or the mother, and `relations.tsv` carries no
`P21`. So a `P40` edge is placed by looking the parent's sex up in **our own tree**
(`reports/derived-facts.csv`), and where that is unknown the edge is **dropped and counted** —
guessing the slot would state somebody's sex as a side effect of a relationship import.

Most `P40` edges are redundant anyway: Wikidata states the same fact from both ends, so the
child's own `P22`/`P25` usually places it already.

## What is NOT emitted, and why

Only structure: `FAMC`/`FAMS` and the `RFN`. No labels, no dates, no notes, no sex. The tree
already holds Geni's values for anyone it knows, and § *Later sources win value conflicts* would
let this overlay silently overwrite them — the merge takes it LAST. Structure is what the
worklist needs and structure is all this writes.

`P3373` *sibling* is read for the census and cannot be emitted: GEDCOM has no sibling edge —
`CLAUDE.md` § *A sibling step is the worked example* — and joining two siblings means inventing
the shared parent, which is the thing forbidden above.
"""

from __future__ import annotations

import argparse
import collections
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

RELATIONS = ROOT / "out" / "wikidata" / "relations.tsv"
P2600 = ROOT / "out" / "wikidata" / "p2600-all.tsv"
FACTS = ROOT / "reports" / "derived-facts.csv"
OUT = ROOT / "out" / "wikidata-tree.ged"


def load_p2600(path):
    """qid -> [geni id]. A qid may name more than one profile and each is a real profile.

    § *A second Geni ID on one Wikidata item is NOT a conflict*: 2,861 items carry more than one,
    which is the correct representation of two unmergeable Geni profiles.
    """
    out = collections.defaultdict(list)
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[0].strip() and parts[1].strip():
                out[parts[0].strip()].append(parts[1].strip())
    return out


def load_sex(path):
    """geni id -> 'M'/'F', from OUR tree. Only used to place a `P40` edge in a slot."""
    sex = {}
    if not path.exists():
        return sex
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g, s = (row.get("geni_id") or "").strip(), (row.get("sex") or "").strip().upper()
            if g and s in ("M", "F"):
                sex[g] = s
    return sex


def main() -> int:
    ap = argparse.ArgumentParser(description="Wikidata's genealogy as a mergeable GEDCOM")
    ap.add_argument("-o", "--out", default=str(OUT))
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    qid_geni = load_p2600(P2600)
    sex = load_sex(FACTS)
    print("%d qids carry a P2600 (%d profiles); %d sexes known from our tree"
          % (len(qid_geni), sum(len(v) for v in qid_geni.values()), len(sex)), flush=True)

    couples = collections.defaultdict(set)      # (father, mother) -> {child}
    childless = set()                           # (a, b) spouse pairs with no recorded child
    people = set()
    dropped_no_p2600 = dropped_no_sex = n_sib = 0

    with open(RELATIONS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            qid = (row.get("qid") or "").strip()
            if not qid:
                continue
            mine = qid_geni.get(qid)
            cols = {c: [v.strip() for v in (row.get(c) or "").split(";") if v.strip()]
                    for c in ("p22", "p25", "p40", "p26", "p3373")}
            n_sib += len(cols["p3373"])
            if not mine:
                dropped_no_p2600 += sum(len(cols[c]) for c in ("p22", "p25", "p40", "p26"))
                continue

            def resolve(col):
                nonlocal dropped_no_p2600
                out = []
                for q in cols[col]:
                    got = qid_geni.get(q)
                    if got:
                        out.extend(got)
                    else:
                        dropped_no_p2600 += 1
                return out

            fathers, mothers = resolve("p22"), resolve("p25")
            partners, kids = resolve("p26"), resolve("p40")

            # this person AS A CHILD -- the slots are named, so this is unambiguous
            for gid in mine:
                people.add(gid)
                if fathers or mothers:
                    for f in fathers or [""]:
                        for m in mothers or [""]:
                            couples[(f, m)].add(gid)
                            people.update(x for x in (f, m) if x)

            # this person AS A PARENT, from P40 -- needs a slot, which P40 does not give
            for gid in mine:
                if not kids:
                    continue
                s = sex.get(gid)
                if s is None:
                    dropped_no_sex += len(kids)
                    continue
                key = (gid, "") if s == "M" else ("", gid)
                couples[key].update(kids)
                people.update(kids)

            # spouse pairs, so a childless marriage still joins the two components
            for gid in mine:
                for p in partners:
                    childless.add(tuple(sorted((gid, p))))
                    people.update((gid, p))

    for a, b in childless:
        if not any((a in k and b in k) for k in ((a, b), (b, a)) if k in couples):
            couples.setdefault((a, b), set())

    print("%d people, %d families | dropped: %d edges to a qid with no P2600, "
          "%d P40 edges with no known sex | %d P3373 siblings read and not emittable"
          % (len(people), len(couples), dropped_no_p2600, dropped_no_sex, n_sib), flush=True)

    fams = collections.defaultdict(list)
    famc = collections.defaultdict(list)
    ordered = sorted(couples.items())
    for i, ((f, m), kids) in enumerate(ordered, 1):
        x = "F9%d" % i
        if f:
            fams[f].append(x)
        if m:
            fams[m].append(x)
        for k in kids:
            famc[k].append(x)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("0 HEAD\n1 SOUR genimerge\n2 NAME build-wikidata-gedcom.py\n"
                 "1 GEDC\n2 VERS 5.5.1\n2 FORM LINEAGE-LINKED\n1 CHAR UTF-8\n")
        for gid in sorted(x for x in people if x):
            fh.write("0 @I%s@ INDI\n1 RFN geni:%s\n" % (gid, gid))
            for x in fams.get(gid, ()):
                fh.write("1 FAMS @%s@\n" % x)
            for x in famc.get(gid, ()):
                fh.write("1 FAMC @%s@\n" % x)
        for i, ((f, m), kids) in enumerate(ordered, 1):
            fh.write("0 @F9%d@ FAM\n" % i)
            if f:
                fh.write("1 HUSB @I%s@\n" % f)
            if m:
                fh.write("1 WIFE @I%s@\n" % m)
            for k in sorted(kids):
                fh.write("1 CHIL @I%s@\n" % k)
        fh.write("0 TRLR\n")
    print("wrote %s -- %d INDI, %d FAM, %.1f MB"
          % (out, len([x for x in people if x]), len(ordered), out.stat().st_size / 1e6))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
