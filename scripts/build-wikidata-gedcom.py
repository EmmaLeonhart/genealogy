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

## THE REDUCTIONS -- AND THE PRUNE IS A KLUDGE BEHIND A FLAG, NOT THE DESIGN

**⛔ `--prune-dead-ends` IS OFF BY DEFAULT AND MUST STAY OFF.** Ruled 2026-09-09: *"please don't
do that... that is not something I gave you permission to do. That's not something I want to be
done long term because you haven't established the degree of content that even comes from the
QID-only Wikidata people."* It is kept because it works and it is measured, and it is opt-in
because dropping a real person to save memory is a decision, not an optimisation — and the
question it presumes an answer to (*what is a QID-only person worth?*) has not been answered.

The overlay's job is to let a Geni person reach Charlemagne through Wikidata's structure. Three
populations cannot serve that job, measured rather than assumed away:

    a QID-only person in <= 1 family    272,987   a dead end: cannot be ON a path
    an overlay person in NO family      191,562   carries no edge at all
    a couple that is ALREADY a geni FAM   6,234   defer to the geni family id

**A dead end cannot be a bridge**, so removing it cannot disconnect anything — and removing one
can strand its neighbour, so the prune iterates to a fixed point. **Only QID-only people are
pruned**: a Geni-keyed person is a corpus join and stays even at degree 1.

**⛔ THE FAMILY DEFERRAL WAS A REAL DEFECT AND IT WAS NOT THE BIG ONE.** The first version minted
a fresh `@FW<n>@` for every Wikidata couple, so a couple who already share a Geni family got a
SECOND `FAM` record, the child a second `FAMC`, the parents a second `FAMS`. That is the
duplication to fix — the Wikidata family subordinates to the Geni family id. Measured, it is
**6,234 of 465,178** two-parent families, 1.3%, because both parents being corpus people is rare
when only 43,709 `P2600` holders are in the corpus at all. It is worth fixing and it is not what
makes the tree large; the size is inherent to carrying a million Wikidata people.

## NAMELESS NODES ARE THE DESIGN. `--with-content` is an option, not a fix

**⛔ STRUCTURE ONLY IS WHAT WAS ASKED FOR, and it is the default.** Ruled 2026-09-09: *"Of
course, there are supposed to be nameless nodes. This is literally what I wanted you to do."* A
QID-only person is a **routing node** -- it exists so a Geni person can reach Charlemagne through
Wikidata's structure -- and a router does not need a name to route.

**This section previously called that a defect of mine and it was not one.** Writing up a correct
implementation as a self-caught error is its own failure: it spends attention on a non-problem
and buries what the numbers actually say.

**What the store HOLDS for them, which is a fact about coverage and not a complaint:**

    with an EN label in the store     896,222   83%
    with a MUL label                  154,865   14%
    with a birth year                 498,060   46%
    with a death year                 395,334   36%

So the content is **available** if a reader of the merged tree ever needs it, and `--with-content`
emits `NAME` (mul first, then en) plus `BIRT`/`DEAT` years on the QID-only half. It costs 43 MB
on the overlay and is **off**.

**It could never be emitted on the Geni-keyed half**, whatever the flag says: the merge takes
this overlay LAST, so a `NAME` there would overwrite Geni's own under *Later sources win value
conflicts*. On the QID-only half there is nothing to overwrite, which is why the flag is
possible at all.

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
LABELS = ROOT / "out" / "wikidata" / "labels.tsv"
DATES = ROOT / "out" / "wikidata" / "dates.tsv"
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


def load_content(labels_path, dates_path, wanted):
    """qid -> (name, birth_year, death_year) for the QID-only people, from the offline store.

    Only the people asked for, because the label store is 196 MB and holding all of it is a
    quarter of the memory the merge itself needs.

    `mul` before `en`: `mul` is the language-neutral label this project treats as the real one
    (*The MARRIED name is the real name*), and `en` is the fallback where no `mul` exists.
    """
    name, born, died = {}, {}, {}
    if labels_path.exists():
        with open(labels_path, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter=TAB):
                q = row["qid"]
                if q in wanted:
                    v = (row.get("mul") or "").strip() or (row.get("en") or "").strip()
                    if v:
                        name[q] = v
    if dates_path.exists():
        with open(dates_path, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter=TAB):
                q = row["qid"]
                if q in wanted:
                    b = (row.get("birth_year") or "").strip()
                    d = (row.get("death_year") or "").strip()
                    if b:
                        born[q] = b
                    if d:
                        died[q] = d
    return name, born, died


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
    ap.add_argument("--with-content", action="store_true",
                    help="ALSO emit NAME and BIRT/DEAT years on the QID-only half. OFF by "
                         "default: nameless routing nodes are the design, not a shortfall.")
    ap.add_argument("--prune-dead-ends", action="store_true",
                    help="KLUDGE, off by default and ruled so. Drop QID-only people in <=1 "
                         "family and people in no family at all. Preserves connectivity between "
                         "Geni people, and drops real people to save memory, which is a decision "
                         "rather than an optimisation.")
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

    # --- the reductions, in the docstring's order --------------------------------
    members = {k: {x for x in (f, m) if x} | {x for x in v if x}
               for k, (f, m, v) in
               ((k, (k[0], k[1], v)) for k, v in couples.items())}
    in_fams = collections.defaultdict(set)
    for k, ms in members.items():
        for p in ms:
            in_fams[p].add(k)

    pruned = 0
    stack = ([p for p in in_fams if p.startswith("Q") and len(in_fams[p]) <= 1]
             if args.prune_dead_ends else [])
    while stack:
        p = stack.pop()
        if p not in in_fams or not p.startswith("Q") or len(in_fams[p]) > 1:
            continue
        for k in list(in_fams[p]):
            members[k].discard(p)
            if len(members[k]) <= 1:
                for q in list(members[k]):
                    in_fams[q].discard(k)
                    if q.startswith("Q") and len(in_fams[q]) <= 1:
                        stack.append(q)
                members.pop(k, None)
                couples.pop(k, None)
            else:
                for q in members[k]:
                    if q.startswith("Q") and len(in_fams[q]) <= 1:
                        stack.append(q)
        in_fams.pop(p, None)
        people.discard(p)
        pruned += 1
    # a pruned person must also leave the couples they were a member of
    for k in list(couples):
        f, m = k
        kids = {x for x in couples[k] if x in people}
        if (f and f not in people) or (m and m not in people):
            couples[k] = kids
        else:
            couples[k] = kids
    couples = {k: v for k, v in couples.items() if k in members}

    edgeless = {p for p in people if p not in in_fams or not in_fams[p]}
    if args.prune_dead_ends:
        people -= edgeless
        print("PRUNED (kludge, --prune-dead-ends): %d dead-end QID-only connectors, %d edgeless "
              "people -> %d people, %d families"
              % (pruned, len(edgeless), len(people), len(couples)), flush=True)
    else:
        print("kept: %d QID-only people sit in <=1 family and %d carry no edge at all; "
              "--prune-dead-ends would drop them and is off by design"
              % (sum(1 for p in in_fams if p.startswith("Q") and len(in_fams[p]) <= 1),
                 len(edgeless)), flush=True)

    # a couple that is ALREADY a geni family defers to the geni family id
    corpus_fam = {}
    fs = ROOT / "out" / "family-structure.tsv"
    if fs.exists():
        with open(fs, encoding="utf-8") as fh:
            next(fh, None)
            for line in fh:
                p = line.rstrip(NL).split(TAB)
                if len(p) >= 3 and p[0] == "fam_p":
                    corpus_fam[frozenset(p[2].split())] = p[1]

    fams = collections.defaultdict(list)
    famc = collections.defaultdict(list)
    ordered = sorted(couples.items())
    deferred = 0
    xrefs = {}
    for i, ((f, m), kids) in enumerate(ordered, 1):
        got = corpus_fam.get(frozenset(x for x in (f, m) if x)) if f and m else None
        xrefs[(f, m)] = ("F" + got) if got else ("FW%d" % i)
        if got:
            deferred += 1
    print("%d wikidata couples defer to an existing geni family id" % deferred, flush=True)
    for i, ((f, m), kids) in enumerate(ordered, 1):
        x = xrefs[(f, m)]
        if f:
            fams[f].append(x)
        if m:
            fams[m].append(x)
        for k in kids:
            if k:
                famc[k].append(x)

    if args.with_content:
        wd_name, wd_born, wd_died = load_content(
            LABELS, DATES, {p for p in people if p.startswith("Q")})
        print("--with-content: %d names, %d birth years, %d death years"
              % (len(wd_name), len(wd_born), len(wd_died)), flush=True)
    else:
        wd_name = wd_born = wd_died = {}

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    n_geni = n_qid = n_named = 0
    with out.open("w", encoding="utf-8", newline=NL) as fh:
        fh.write("0 HEAD" + NL + "1 SOUR genimerge" + NL
                 + "2 NAME build-wikidata-gedcom.py" + NL
                 + "1 GEDC" + NL + "2 VERS 5.5.1" + NL + "2 FORM LINEAGE-LINKED" + NL
                 + "1 CHAR UTF-8" + NL)
        for node in sorted(people):
            fh.write("0 @I%s@ INDI%s" % (node, NL))
            if node.startswith("Q"):
                fh.write("1 REFN %s%s" % (node, NL))
                # ⛔ CONTENT ONLY ON THIS HALF. A QID-only person is not in the corpus, so there
                # is no Geni value for `Later sources win` to overwrite -- see the docstring.
                nm = wd_name.get(node)
                if nm:
                    fh.write("1 NAME %s%s" % (nm.replace("/", " ").strip(), NL))
                    n_named += 1
                b, d = wd_born.get(node), wd_died.get(node)
                if b:
                    fh.write("1 BIRT%s2 DATE %s%s" % (NL, b, NL))
                if d:
                    fh.write("1 DEAT%s2 DATE %s%s" % (NL, d, NL))
                n_qid += 1
            else:
                fh.write("1 RFN geni:%s%s" % (node, NL))
                n_geni += 1
            for x in fams.get(node, ()):
                fh.write("1 FAMS @%s@%s" % (x, NL))
            for x in famc.get(node, ()):
                fh.write("1 FAMC @%s@%s" % (x, NL))
        for i, ((f, m), kids) in enumerate(ordered, 1):
            fh.write("0 @%s@ FAM%s" % (xrefs[(f, m)], NL))
            if f:
                fh.write("1 HUSB @I%s@%s" % (f, NL))
            if m:
                fh.write("1 WIFE @I%s@%s" % (m, NL))
            for k in sorted(x for x in kids if x):
                fh.write("1 CHIL @I%s@%s" % (k, NL))
        fh.write("0 TRLR" + NL)
    print("wrote %s -- %d INDI (%d keyed on a Geni id, %d on a QID of which %d NAMED), "
          "%d FAM, %.1f MB"
          % (out, n_geni + n_qid, n_geni, n_qid, n_named, len(ordered),
             out.stat().st_size / 1e6))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
