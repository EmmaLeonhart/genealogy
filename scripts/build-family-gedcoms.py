"""One tiny GEDCOM per scraped person. The native format, and the actual result of a scrape.

**Emma, 2026-09-06:** *"you get basically these people from extremely small gedcom files. Like
Natalia Krebs (Salzmann) will produce a 3 person file with the name 'Natalia Krebs (Salzmann)' and
HUSB 'Max Krebs' and daughter 'Suzy Glaser' with the geni ids set up so that they end up getting
merged in. This is what is supposed to be the main result of the scrape. These tiny gedcoms only
contribute generally one or two families but they are significant and the entity resolution in
them means they significantly link things together."*

And: *"for all intents and purposes the native format of this project is the gedcom now."* The TSV
in `geni-families/` is fine as a record; it reaches nothing. A `.ged` under `exports/` is read by
`genimerge.sources` recursively, so it is in the synoptic tree with no wiring at all.

## IT INVENTS NOBODY. That is the whole point of it

It replaces `build-scraped-gedcom.py`, which minted a placeholder parent whenever a family needed
one. Measured 2026-09-06 over its two output files, which were **in the merge** -- 605 files read,
603 real Geni exports, those two the difference:

    4,928 invented `NN` people carrying non-Geni ids (`9995...`)
    5,750 children left with MORE THAN TWO parents
    and of those 5,750, every single one had at least two INVENTED parents

That is where the parent deck's `9995000000000000074` and `9995000000000102196` fathers came
from. A GEDCOM `FAM` does not require both partners: a family with one known parent is written
with one, and the missing side is simply absent. Nothing here creates a person who was not on the
page.

## The keys

**A person's xref is their Geni id** -- `CLAUDE.md`: *"The Geni profile ID is the primary key for
everything"*, so the merge is an exact join and these files fuse into the tree rather than sitting
beside it. That is what she means by the entity resolution in them doing the linking.

**A family xref is derived from its members rather than from a counter -- worth doing, NOT worth
much.** Emma, 2026-09-06: *"geni does not expose family ids. This is good to attempt but I'm not
sure how much it matters as wikidata does not use families."* She is right and this docstring
originally billed it as a headline property.

Geni exposes no family id, so any `FAM` xref here is ours either way. Wikidata has no family
object at all -- it models `P22` father, `P25` mother, `P40` child and `P26` spouse directly -- so
the same couple written as two `FAM` records yields the same parent and child edges and
deduplicates downstream. The digest costs nothing over a counter and makes re-running idempotent,
which is why it stays; it is not what was wrong with the thing this replaces.

**What WAS wrong with it was the invented people**, and that is a different order of problem:
4,928 fabricated `NN` humans carrying non-Geni ids, which corrupts the edges themselves rather
than the bookkeeping around them.

**Names are whole strings.** Emma, 2026-08-29: *"the names being present as strings makes things
significantly harder... You'd probably be using spacing to figure out what the last name is."* So
`1 NAME <string>` with no `GIVN`/`SURN` split.

**Parents are emitted father-first where sex is unknown**, which the superseded script established
by measurement and which is kept: over 120 pages, of the 116 two-parent blocks where both sexes
were known, **100 resolved (M, F) and none (F, M)**.
"""

from __future__ import annotations

import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAMILIES = ROOT / "geni-families"
OUT = ROOT / "exports" / "family-scrapes"

#: The subject's own role word gives the subject's sex.
SEX_OF_PHRASE = {
    "son": "M", "husband": "M", "father": "M", "brother": "M", "half brother": "M",
    "daughter": "F", "wife": "F", "mother": "F", "sister": "F", "half sister": "F",
}

PARENTS = {"parent"}
CHILDREN = {"child"}
SPOUSES = {"spouse", "partner", "ex-spouse"}
SIBLINGS = {"sibling", "half-sibling"}


def fam_xref(members):
    """A deterministic family id, so one family is one family in every file that names it.

    Numeric because a Geni `FAM` xref is numeric and `GENI_ID_RE` accepts only digits after the
    letter. Prefixed `9990` to stay clear of real Geni ids -- the convention the tests already
    know -- and the rest is a digest of the sorted members rather than a counter, which is what
    makes re-running idempotent and what stops one couple becoming two families.
    """
    key = "|".join(sorted(members))
    digest = int(hashlib.sha1(key.encode("utf-8")).hexdigest()[:12], 16)
    return "9990%015d" % (digest % 10 ** 15)


def read_scrape(path):
    subject = name = ""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# subject\t"):
            parts = line.split("\t")
            subject = parts[1]
            name = parts[2] if len(parts) > 2 else ""
        elif line and not line.startswith("#") and not line.startswith("subject_geni_id"):
            f = line.split("\t")
            if len(f) == 5:
                rows.append({"relation": f[1], "phrase": f[2], "geni_id": f[3], "name": f[4]})
    return {"subject": subject, "name": name, "relatives": rows}


def gedcom_for(scrape):
    subject = scrape["subject"]
    rels = scrape["relatives"]
    if not subject or not rels:
        return None

    people = {subject: scrape["name"]}
    for r in rels:
        people.setdefault(r["geni_id"], r["name"])

    sex = {}
    for r in rels:
        s = SEX_OF_PHRASE.get(r["phrase"].strip().lower())
        if s:
            sex[subject] = s
            break

    parents = [r["geni_id"] for r in rels if r["relation"] in PARENTS]
    children = [r["geni_id"] for r in rels if r["relation"] in CHILDREN]
    spouses = [r["geni_id"] for r in rels if r["relation"] in SPOUSES]
    siblings = [r["geni_id"] for r in rels if r["relation"] in SIBLINGS]

    fams = []
    if parents or siblings:
        # The family the subject was born into. One known parent is written with one; the missing
        # side stays absent rather than being invented.
        fams.append({"husb": parents[0] if len(parents) > 0 else None,
                     "wife": parents[1] if len(parents) > 1 else None,
                     "chil": [subject] + siblings})
    if spouses or children:
        # The family the subject made. Children hang off the first spouse only: the scrape does
        # not say which child belongs to which marriage, and guessing would assert a parentage
        # nothing on the page supports.
        for i, sp in enumerate(spouses or [None]):
            if sex.get(subject) == "F":
                husb, wife = sp, subject
            else:
                husb, wife = subject, sp
            fams.append({"husb": husb, "wife": wife, "chil": children if i == 0 else []})

    out = [
        "0 HEAD",
        "1 SOUR genimerge-family-scrape",
        "1 CHAR UTF-8",
        "1 NOTE one tiny GEDCOM per scraped Geni profile, built by "
        "scripts/build-family-gedcoms.py. Invents nobody: every INDI is a real Geni profile.",
        "1 NOTE subject geni:%s" % subject,
    ]
    for gid, nm in people.items():
        out.append("0 @I%s@ INDI" % gid)
        out.append("1 NAME %s" % (nm or "NN"))
        if gid in sex:
            out.append("1 SEX %s" % sex[gid])
        out.append("1 RFN geni:%s" % gid)
    for f in fams:
        members = [m for m in [f["husb"], f["wife"]] + f["chil"] if m]
        if len(members) < 2:
            continue
        out.append("0 @F%s@ FAM" % fam_xref(members))
        if f["husb"]:
            out.append("1 HUSB @I%s@" % f["husb"])
        if f["wife"]:
            out.append("1 WIFE @I%s@" % f["wife"])
        for c in f["chil"]:
            out.append("1 CHIL @I%s@" % c)
    out.append("0 TRLR")
    return "\n".join(out) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    written = skipped = indi = fam = 0
    for path in sorted(FAMILIES.glob("*-family.tsv")):
        scrape = read_scrape(path)
        text = gedcom_for(scrape)
        if text is None:
            skipped += 1
            continue
        (OUT / ("%s.ged" % scrape["subject"])).write_text(text, encoding="utf-8")
        written += 1
        indi += text.count("\n0 @I")
        fam += text.count("\n0 @F")
    print("wrote %d tiny gedcoms into %s" % (written, OUT.relative_to(ROOT)))
    print("  %d INDI, %d FAM, %d skipped for having no relatives" % (indi, fam, skipped))
    print("  invented people: 0 -- every INDI carries a real Geni id")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
