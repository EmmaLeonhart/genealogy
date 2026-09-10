"""Wikidata's genealogy as a GEDCOM, so the synoptic tree merge absorbs it.

    PYTHONPATH=src python scripts/build-wikidata-gedcom.py
    PYTHONPATH=src python -m genimerge merge --also out/wikidata-tree.ged

**Sections 0 and 1 of `docs/unconnected-worklist.md`.** The dictation of 2026-09-09 opens *"I
don't think that the CI/CD currently combines the WikiData tree with the geni trees"* and that
was checked and is true: `rebuild-everything.py` merges `exports/**/*.ged` plus one small
correspondence overlay, and Wikidata's relationship edges are nowhere in `out/merged.ged`.

**Natively a GEDCOM, and that is the point rather than a format choice** -- *"the syntactic tree
now has a canonical form that is natively a Gedcom because that means that it preserves the
family IDs, which is important for some stuff."* `scripts/p2600-connectivity.py` answers the
connected/disconnected question with a union-find over edges, which destroys exactly that.

## WHY THE TREES ARE JOINED AT ALL, which is the thing the first version defeated

**Wikidata's own structure is what connects Geni people our exports leave disconnected**, and
the bridges are overwhelmingly people who exist ONLY on Wikidata -- the shared father of two
Geni-linked cousins, the medieval couple nobody has attached a Geni profile to. Drop them and
the join does nothing at all: the Geni people it was supposed to connect stay exactly as
disconnected as they were.

**The first version of this script dropped every one of them.** It emitted an edge only where
both ends carried a `P2600`, discarding **3,423,982 edges** and every Wikidata-only person. The
rule it cited does not cover this population: `build-scraped-gedcom.py` was deleted for minting
`NN` placeholders nobody had evidence for, and a Wikidata item is a real, identified person with
a stable identifier. That is the *Do not grab the first artifact that vaguely matches* failure
one level up -- a rule about invented people applied to people who are not invented.

**So every item is an `INDI`, and the xref says which identifier it carries:**

    a P2600 holder    @I<geni id>@   with  1 RFN geni:<id>   -- FUSES with the corpus, exact join
    everyone else     @IQ<digits>@   with  1 REFN Q<digits>  -- a Wikidata person, no Geni profile

**The `Q` is load-bearing.** `identity.GENI_ID_RE` is `^@[IFNS](\\d+)@$`, digits only, so
`@IQ12345@` cannot be mistaken for Geni profile `12345`. That is the `@NI04461@` trap `CLAUDE.md`
records, where a foreign xref parsed as a Geni id and would have produced a URL to a stranger's
profile.

**The FAMILY xrefs had that exact bug in the first version.** They were `@F9<n>@`, which parses
with `geni_id=9<n>` -- so Wikidata family 91 read as Geni family `91`, and small Geni ids are
real (`1015359` is a person in the corpus). They are `@FW<n>@` now, which cannot parse.

## `P40` DOES NOT NAME A SLOT, SO THE FILE ITSELF IS ASKED

`P22` *father* and `P25` *mother* name the slot. `P40` *child* does not, and `relations.tsv`
carries no `P21`. The first version dropped **246,251** such edges for want of a sex.

**It never needed one.** Wikidata states the same fact from both ends, so anybody who is
somebody's `P22` anywhere in the file is male and anybody's `P25` is female -- exact, free, and
read off the input rather than looked up. Our own tree's `sex` column fills in behind it. Only
where both are silent is the parent put in the `HUSB` slot, counted and reported: a single-parent
family with the slot picked wrong still carries the edge, and the edge is the thing that matters.

## What is NOT emitted, and why

Only structure: `FAMC`/`FAMS`, and the identifier. No labels, no dates, no notes, no sex. The
tree already holds Geni's values for anyone it knows, and *Later sources win value conflicts*
would let this overlay silently overwrite them, since the merge takes it LAST.

`P3373` *sibling* is read for the census and cannot be emitted: GEDCOM has no sibling edge --
`CLAUDE.md` *A sibling step is the worked example* -- and joining two siblings means inventing
the shared parent, which is a different thing from carrying a person Wikidata already names.
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

NL = chr(10)
TAB = chr(9)


def load_p2600(path):
    """qid -> [geni id]. A qid may name more than one profile and each is a real profile.

    *A second Geni ID on one Wikidata item is NOT a conflict*: 2,861 items carry more than one,
    which is the correct representation of two unmergeable Geni profiles.
    """
    out = collections.defaultdict(list)
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip(NL).split(TAB)
            if len(parts) >= 2 and parts[0].strip() and parts[1].strip():
                out[parts[0].strip()].append(parts[1].strip())
    return out


def load_sex(path):
    """geni id -> 'M'/'F', from OUR tree. Second source, behind the file's own P22/P25."""
    sex = {}
    if not path.exists():
        return sex
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            x = (row.get("sex") or "").strip().upper()
            if g and x in ("M", "F"):
                sex[g] = x
    return sex


def read_rows(path):
    """One pass, yielding (qid, {col: [qid]}). Read twice: once for sex, once to build."""
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=TAB):
            qid = (row.get("qid") or "").strip()
            if not qid:
                continue
            yield qid, {c: [v.strip() for v in (row.get(c) or "").split(";") if v.strip()]
                        for c in ("p22", "p25", "p40", "p26", "p3373")}


def main() -> int:
    ap = argparse.ArgumentParser(description="Wikidata's genealogy as a mergeable GEDCOM")
    ap.add_argument("-o", "--out", default=str(OUT))
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    qid_geni = load_p2600(P2600)
    our_sex = load_sex(FACTS)
    print("%d qids carry a P2600 (%d profiles); %d sexes known from our tree"
          % (len(qid_geni), sum(len(v) for v in qid_geni.values()), len(our_sex)), flush=True)

    # PASS 1 -- sex from the file itself. Anybody's P22 is male, anybody's P25 is female.
    wd_sex = {}
    for _, cols in read_rows(RELATIONS):
        for q in cols["p22"]:
            wd_sex[q] = "M"
        for q in cols["p25"]:
            wd_sex[q] = "F"
    print("%d sexes read off the file's own P22/P25" % len(wd_sex), flush=True)

    def nodes(qid):
        """One node per Wikidata item: the Geni id where there is one, else the QID."""
        got = qid_geni.get(qid)
        return got if got else ["Q" + qid[1:]]

    def sex_of(qid):
        s = wd_sex.get(qid)
        if s:
            return s
        for g in qid_geni.get(qid, ()):
            if g in our_sex:
                return our_sex[g]
        return None

    couples = collections.defaultdict(set)      # (father, mother) -> {child}
    childless = set()
    people = set()
    n_sib = slot_guessed = 0

    for qid, cols in read_rows(RELATIONS):
        mine = nodes(qid)
        people.update(mine)
        n_sib += len(cols["p3373"])

        fathers = [n for q in cols["p22"] for n in nodes(q)]
        mothers = [n for q in cols["p25"] for n in nodes(q)]
        partners = [n for q in cols["p26"] for n in nodes(q)]

        # AS A CHILD -- P22/P25 name the slot, so this is unambiguous
        if fathers or mothers:
            for gid in mine:
                for f in fathers or [""]:
                    for m in mothers or [""]:
                        couples[(f, m)].add(gid)
            people.update(fathers)
            people.update(mothers)

        # AS A PARENT -- P40 names no slot, so it comes from the sex resolved above
        if cols["p40"]:
            kids = [n for q in cols["p40"] for n in nodes(q)]
            s = sex_of(qid)
            if s is None:
                slot_guessed += len(kids)
                s = "M"
            for gid in mine:
                couples[(gid, "") if s == "M" else ("", gid)].update(kids)
            people.update(kids)

        for gid in mine:
            for p in partners:
                childless.add(tuple(sorted((gid, p))))
        people.update(partners)

    for pair in childless:
        if pair not in couples and (pair[1], pair[0]) not in couples:
            couples[pair] = couples.get(pair, set())

    people.discard("")
    print("%d people, %d families | %d P40 edges whose parent slot had to be guessed | "
          "%d P3373 siblings read, not emittable in GEDCOM"
          % (len(people), len(couples), slot_guessed, n_sib), flush=True)

    fams = collections.defaultdict(list)
    famc = collections.defaultdict(list)
    ordered = sorted(couples.items())
    for i, ((f, m), kids) in enumerate(ordered, 1):
        x = "FW%d" % i
        if f:
            fams[f].append(x)
        if m:
            fams[m].append(x)
        for k in kids:
            if k:
                famc[k].append(x)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    n_geni = n_qid = 0
    with out.open("w", encoding="utf-8", newline=NL) as fh:
        fh.write("0 HEAD" + NL + "1 SOUR genimerge" + NL
                 + "2 NAME build-wikidata-gedcom.py" + NL
                 + "1 GEDC" + NL + "2 VERS 5.5.1" + NL + "2 FORM LINEAGE-LINKED" + NL
                 + "1 CHAR UTF-8" + NL)
        for node in sorted(people):
            fh.write("0 @I%s@ INDI%s" % (node, NL))
            if node.startswith("Q"):
                fh.write("1 REFN %s%s" % (node, NL))
                n_qid += 1
            else:
                fh.write("1 RFN geni:%s%s" % (node, NL))
                n_geni += 1
            for x in fams.get(node, ()):
                fh.write("1 FAMS @%s@%s" % (x, NL))
            for x in famc.get(node, ()):
                fh.write("1 FAMC @%s@%s" % (x, NL))
        for i, ((f, m), kids) in enumerate(ordered, 1):
            fh.write("0 @FW%d@ FAM%s" % (i, NL))
            if f:
                fh.write("1 HUSB @I%s@%s" % (f, NL))
            if m:
                fh.write("1 WIFE @I%s@%s" % (m, NL))
            for k in sorted(x for x in kids if x):
                fh.write("1 CHIL @I%s@%s" % (k, NL))
        fh.write("0 TRLR" + NL)
    print("wrote %s -- %d INDI (%d keyed on a Geni id, %d on a QID), %d FAM, %.1f MB"
          % (out, n_geni + n_qid, n_geni, n_qid, len(ordered), out.stat().st_size / 1e6))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
