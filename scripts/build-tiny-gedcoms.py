"""Two operations, both producing tiny GEDCOMs, and NEITHER invents a person.

**There are two distinct operations: paths and profiles.** Both make tiny GEDCOMs, one per path
or per individual. Both carry similar information, and many saved pages hold enough to make both
kinds from the one page.

    profiles   one .ged per PERSON  <- geni-families/*.tsv, geni-scraping/*.html
    paths      one .ged per PATH    <- paths/*.tsv

## The ruling that changed: an unknown parent is an ABSENT SLOT, not an `NN` person

Asked directly, and choosing between placeholder people and empty slots: **absent slot, no
person.** That supersedes the 2026-08-29 ruling that both parents are `NN` placeholders, which
`scripts/build-scraped-gedcom.py` implements and which minted 4,928 of them.

A GEDCOM `FAM` needs neither partner. Siblings with no known parents are a family with `CHIL` and
no `HUSB`/`WIFE` -- which says *these people are siblings* and asserts nothing about who the
parents were. That is the whole difference between the two emitters:
nothing here creates a human that was not named on a page.

## ⛔ WHY THE REDUNDANCY IS THE POINT, and it is an instruction rather than an accident

**Every single sibling pair gets the small scrape done on it, on every single member.** The
redundancy is instructed and deliberate.

The reason: it creates a GEDCOM for each member of the sibling pair, and that links them as
siblings *with their parents* in the new file, while they are also linked as siblings in the path
GEDCOMs.

So the two operations say different things about the same pair and both are wanted:

    path gedcom      A and B are siblings.            parents UNKNOWN -- empty slot
    profile gedcom   A's parents are X and Y.         from A's own page
    profile gedcom   B's parents are X and Y.         from B's own page

The merge is keyed on the Geni id, so the parentless sibling family from the path and the
parented family from each profile fuse into one family with real parents. **Scraping both members
is how the parents arrive at all** -- a path names a sibling hop and never names the parents, and
`CLAUDE.md` § *A sibling step is the worked example* measures those hops at 7% of all path rows
across 95% of paths. `scripts/sibling-pair-worklist.py` is the list of who still needs it.

## What is emitted

* **Every `INDI` xref is a real Geni id**, so the merge is an exact join -- `CLAUDE.md`: *"The
  Geni profile ID is the primary key for everything."*
* **Names stay whole strings.** Splitting them would mean guessing from spacing which token is
  the surname, which is significantly harder and is not done. No `GIVN`/`SURN` split.
* **A family xref is a digest of its members**, so one family is one family in every file that
  names it and re-running is byte-identical. Geni does not expose family ids, and Wikidata does
  not use families at all, so this matters little -- it is
  bookkeeping, kept because it costs nothing over a counter, not a headline property.
* **A former marriage carries a bare `1 DIV` beside its `1 MARR`, both attested; an
  engagement carries NOTHING** -- `ENGA` occurs zero times in the corpus, so it is not ours
  to write. See the vocabulary note on `render`.
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROFILE_OUT = ROOT / "exports" / "tiny-profiles"
PATH_OUT = ROOT / "exports" / "tiny-paths"

SEX_OF_PHRASE = {
    "son": "M", "husband": "M", "father": "M", "brother": "M", "half brother": "M",
    "daughter": "F", "wife": "F", "mother": "F", "sister": "F", "half sister": "F",
}

#: ⛔ **THE SCRAPE SAYS MORE THAN THIS READ.** Measured 2026-09-15 over the 120 files in
#: `geni-families/`: the `relation` column carries `child` 270, `sibling` 232, `parent` 171,
#: `spouse` 103, **`step-parent` 12**, `half-sibling` 7, **`adoptive-parent` 6**, `ex-spouse` 5,
#: **`step-child` 3** and **`adopted-child` 1**. Four of those were in no set here, so 22 edges
#: were dropped on the floor -- not mis-stated, simply absent from the output.
#:
#: `adoptive-parent` and `adopted-child` are added, and they carry the attested adoption shape.
#: **`step-parent` and `step-child` are deliberately NOT added**: the corpus attests `PEDI
#: adopted` and `PEDI foster` and nothing else, so there is no reading of a step-relationship to
#: copy. Ruled 2026-09-13 for exactly this case -- *"we have to do a `Forest` export on that point
#: in order to get that relationship so we know how to represent it"* -- and inventing one is the
#: thing the whole item forbids. Queued as an export rather than guessed.
PARENTS = {"parent"}
ADOPTIVE_PARENTS = {"adoptive-parent"}
CHILDREN = {"child"}
ADOPTED_CHILDREN = {"adopted-child"}
SPOUSES = {"spouse", "partner", "ex-spouse"}
SIBLINGS = {"sibling", "half-sibling"}

#: The `phrase` column names the RELATIVE and states their sex outright -- `father`, `mother`,
#: `son`, `daughter`. It was read only for the SUBJECT's sex and thrown away for everyone else,
#: which is what made the parent slots positional. Same table, one more caller.
PHRASE_SEX = {
    "father": "M", "mother": "F", "adoptive father": "M", "adoptive mother": "F",
    "son": "M", "daughter": "F", "brother": "M", "sister": "F",
    "husband": "M", "wife": "F", "ex-husband": "M", "ex-wife": "F",
    "half brother": "M", "half sister": "F",
}

#: The relation word on a path row, mapped to what it makes the row's person to the previous one.
#: ⛔ THE SEX OF THE PARENT IS IN THE WORD AND IT WAS BEING THROWN AWAY. Fixed 2026-09-13.
#: `father` and `mother` both mapped to one `parent` kind and `path_gedcom` wrote every parent as
#: `HUSB`, so EVERY MOTHER in every tiny path GEDCOM was recorded as a husband -- 1,007 files with
#: not one `WIFE` line among the parent edges. The TSV had it right the whole time (`his mother`),
#: which is why this is a re-run and not a re-scrape.
PATH_REL = {
    "father": ("parent", "M"), "mother": ("parent", "F"),
    "son": ("child", "M"), "daughter": ("child", "F"),
    "husband": ("spouse", "M"), "wife": ("spouse", "F"),
    "partner": ("spouse", None),
    "brother": ("sibling", "M"), "sister": ("sibling", "F"),
    # Geni renders the sexless forms too. They carry no sex, so they make the edge and assert
    # nothing about which slot the person belongs in.
    "parent": ("parent", None), "child": ("child", None),
}

#: The possessive opens the row and states the sex of the PREVIOUS person -- *his mother* means
#: the previous person is male. That is the only place a child-edge learns which parent slot to
#: use, and it was being dropped with the rest.
POSSESSIVE = {"his": "M", "her": "F"}
FORMER = re.compile(r"^ex-(husband|wife|partner)$", re.I)
# The accented spellings are what Geni actually renders; the ASCII pair alone missed 7 rows.
ENGAGED = {"fiancee", "fiance", "fiancée", "fiancé"}


def fam_xref(members):
    key = "|".join(sorted(members))
    return "9990%015d" % (int(hashlib.sha1(key.encode("utf-8")).hexdigest()[:12], 16) % 10 ** 15)


def render(subject_note, people, sex, fams, source):
    out = [
        "0 HEAD",
        "1 SOUR genimerge-tiny",
        "1 CHAR UTF-8",
        "1 NOTE %s. Built by scripts/build-tiny-gedcoms.py. Invents nobody: every INDI is a real "
        "Geni profile and an unknown parent is an absent slot." % source,
        "1 NOTE %s" % subject_note,
    ]
    #: ⛔ EVERY TAG BELOW IS ATTESTED IN `exports/` AND NONE IS COMPOSED. Ruled 2026-09-13:
    #: *"don't make up some kind of a way of implementing the relationships. Use the actual
    #: relationships that are present within our data... No guessing on the representations."*
    #: Measured across the corpus outside the tiny directories, the ENTIRE vocabulary is:
    #:     1 MARR 514,155   1 DIV 10,071   2 PEDI 2,966   1 ADOP 2,185
    #:     2 PEDI adopted 2,185 / foster 781      3 ADOP BOTH 2,185 -- the only ADOP value
    adopt_famc = {}
    for f in fams:
        if not f.get("adopted"):
            continue
        members = [m for m in [f.get("husb"), f.get("wife")] + f.get("chil", []) if m]
        if len(members) < 2:
            continue
        for c in f.get("chil", []):
            adopt_famc.setdefault(c, []).append(fam_xref(members))
    for gid, nm in people.items():
        out.append("0 @I%s@ INDI" % gid)
        out.append("1 NAME %s" % (nm or "NN"))
        if gid in sex:
            out.append("1 SEX %s" % sex[gid])
        # The attested adoption shape, copied from a real Geni export rather than composed --
        # `exports/8-19 exports/export-Ancestors-6000000227331261851.ged` carries exactly this.
        for fx in adopt_famc.get(gid, []):
            out.append("1 FAMC @F%s@" % fx)
            out.append("2 PEDI adopted")
            out.append("1 ADOP")
            out.append("2 FAMC @F%s@" % fx)
            out.append("3 ADOP BOTH")
        out.append("1 RFN geni:%s" % gid)
    for f in fams:
        members = [m for m in [f.get("husb"), f.get("wife")] + f.get("chil", []) if m]
        if len(members) < 2:
            continue
        out.append("0 @F%s@ FAM" % fam_xref(members))
        if f.get("husb"):
            out.append("1 HUSB @I%s@" % f["husb"])
        if f.get("wife"):
            out.append("1 WIFE @I%s@" % f["wife"])
        for c in f.get("chil", []):
            out.append("1 CHIL @I%s@" % c)
        # `1 MARR` is bare in every one of the corpus's 514,155 occurrences, and so is `1 DIV`
        # in all 10,071. `DIV Y` was written here and is attested NOWHERE.
        if f.get("marr"):
            out.append("1 MARR")
        if f.get("div"):
            out.append("1 DIV")
        # ⛔ NO `ENGA`. It does not occur once in the corpus, and `1 ENGA Y` was being emitted.
        # An engagement therefore has NO attested representation and is written as the couple
        # with no marriage event asserted, which is what a `FAM` without `MARR` already means.
        # Learning a real one needs a `Forest` export on a profile that has an engagement.
    out.append("0 TRLR")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- profiles

def read_family_tsv(path):
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
    return subject, name, rows


def profile_gedcom(subject, name, rels):
    if not subject or not rels:
        return None
    people = {subject: name}
    for r in rels:
        people.setdefault(r["geni_id"], r["name"])
    sex = {}
    for r in rels:
        s = SEX_OF_PHRASE.get(r["phrase"].strip().lower())
        if s:
            sex[subject] = s
            break

    def phrase_sex(r):
        return PHRASE_SEX.get((r.get("phrase") or "").strip().lower())

    parents = [r for r in rels if r["relation"] in PARENTS]
    adoptive = [r for r in rels if r["relation"] in ADOPTIVE_PARENTS]
    children = [r["geni_id"] for r in rels if r["relation"] in CHILDREN]
    adopted_children = [r["geni_id"] for r in rels if r["relation"] in ADOPTED_CHILDREN]
    spouses = [r["geni_id"] for r in rels if r["relation"] in SPOUSES]
    siblings = [r["geni_id"] for r in rels if r["relation"] in SIBLINGS]

    # ⛔ **THE PARENT SLOT COMES FROM THE PHRASE, NEVER FROM THE POSITION.** This read
    # `parents[0]` into `HUSB` and `parents[1]` into `WIFE`, so which slot a parent landed in was
    # whichever order the scrape happened to list them -- a mother first made her the husband.
    # That is the same defect fixed on the PATH side on 2026-09-13, where it had made *every*
    # mother in 1,007 files a husband; the profile side was never touched, and § *A GUARD IN ONE
    # EMITTER IS NOT A GUARD* is the reason to expect that.
    #
    # The `phrase` column said `father` or `mother` the whole time, which is why this is a re-run
    # of the emitter and not a re-scrape.
    def split_parents(rows):
        husb = wife = None
        unplaced = []
        for r in rows:
            s = phrase_sex(r)
            if s == "M" and husb is None:
                husb = r["geni_id"]
            elif s == "F" and wife is None:
                wife = r["geni_id"]
            else:
                unplaced.append(r["geni_id"])
        # A parent whose phrase names no sex fills whichever slot is still empty. It asserts the
        # PARENTHOOD, which is attested, and the slot is the only thing being guessed -- and an
        # absent slot would lose the edge entirely.
        for gid in unplaced:
            if husb is None:
                husb = gid
            elif wife is None:
                wife = gid
        return husb, wife

    fams = []
    if parents or siblings:
        # The birth family. With no parents named this is CHIL-only -- siblinghood stated, and
        # nothing claimed about who the parents were. The ruling: absent slot, no person.
        husb, wife = split_parents(parents)
        fams.append({"husb": husb, "wife": wife, "chil": [subject] + siblings})
    if adoptive:
        # The adoptive family is its OWN family, never merged with the birth one: the child is
        # `CHIL` of both, and the `PEDI adopted` / `ADOP BOTH` block on the child's `INDI` is what
        # says which is which. That is the shape `render` already emits, copied from
        # `exports/8-19 exports/export-Ancestors-6000000227331261851.ged`.
        a_husb, a_wife = split_parents(adoptive)
        fams.append({"husb": a_husb, "wife": a_wife, "chil": [subject], "adopted": True})
    if adopted_children:
        fams.append({"husb": subject if sex.get(subject) != "F" else None,
                     "wife": subject if sex.get(subject) == "F" else None,
                     "chil": adopted_children, "adopted": True})
    if spouses or children:
        for i, sp in enumerate(spouses or [None]):
            if sex.get(subject) == "F":
                husb, wife = sp, subject
            else:
                husb, wife = subject, sp
            fams.append({"husb": husb, "wife": wife, "chil": children if i == 0 else []})
    return render("subject geni:%s" % subject, people, sex, fams,
                  "one tiny GEDCOM per scraped Geni profile")


# ---------------------------------------------------------------- paths

def read_path_tsv(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or line.startswith("step\t"):
            continue
        f = line.split("\t")
        if len(f) >= 4 and f[3].startswith("geni:"):
            rows.append({"name": f[1], "rel": f[2].strip().lower(), "gid": f[3][5:].strip()})
    return rows


def path_gedcom(name, rows, source="one tiny GEDCOM per Geni relationship path"):
    """Consecutive rows are one family edge; a sibling hop is a CHIL-only family."""
    if len(rows) < 2:
        return None
    people = {r["gid"]: r["name"] for r in rows}
    fams = []
    sex = {}
    for prev, cur in zip(rows, rows[1:]):
        parts = cur["rel"].split() if cur["rel"] else []
        word = parts[-1] if parts else ""
        owner = POSSESSIVE.get(parts[0].lower()) if parts else None
        former = bool(FORMER.match(word))
        if former:
            word = word.split("-", 1)[1]
        kind, own_sex = PATH_REL.get(word, (None, None))
        # ⛔ **BOTH SPELLINGS, and only one was matched.** Measured 2026-09-15 over
        # `reports/path-chains.tsv`: **775 rows carry an adoption word**, not the 136 recorded
        # when this was written. `adoptive` covers 736 of them -- `her adoptive mother` alone is
        # 726 -- but **39 say `adopted`**: `his adopted son` 29, `her adopted daughter` 7, `her
        # adopted son` 2, `his adopted daughter` 1. Those are all CHILD edges, which is the other
        # half of why they were missed: the child branch below never carried the flag either, so
        # an adopted child was written as a birth child.
        adopted = bool({"adoptive", "adopted"} & {w.lower() for w in parts})
        if kind is None and word in ENGAGED:
            kind, former = "spouse", False
        if kind is None:
            continue
        if own_sex:
            sex[cur["gid"]] = own_sex
        if owner:
            sex.setdefault(prev["gid"], owner)
        if kind == "parent":
            slot = "wife" if own_sex == "F" else "husb"
            fams.append({slot: cur["gid"], "chil": [prev["gid"]], "adopted": adopted})
        elif kind == "child":
            # The possessive states the PARENT's sex: *his son* -> the previous person is male.
            slot = "wife" if owner == "F" else "husb"
            fams.append({slot: prev["gid"], "chil": [cur["gid"]], "adopted": adopted})
        elif kind == "spouse":
            # `partner` and a fiance(e) assert no marriage; `husband`/`wife` do, and an `ex-`
            # asserts one that ended, which is `1 MARR` + `1 DIV` exactly as the corpus writes it.
            married = word in ("husband", "wife")
            if own_sex == "M":
                fams.append({"husb": cur["gid"], "wife": prev["gid"],
                             "marr": married, "div": former})
            else:
                fams.append({"husb": prev["gid"], "wife": cur["gid"],
                             "marr": married, "div": former})
        elif kind == "sibling":
            # ⛔ No parents are invented. The pair is a family with two children and no partners;
            # their real parents arrive from each member's own profile scrape, which is why the
            # scrape is required on BOTH members of every sibling pair.
            fams.append({"chil": [prev["gid"], cur["gid"]]})
    if not fams:
        return None
    return render("path %s" % name, people, sex, fams, source)


# ---------------------------------------------------------------- saved pages

def saved_page_gedcom(subject, names, edges):
    """A tiny GEDCOM from one saved `geni-scraping/<id>.html`.

    **These are made from every saved Geni HTML page, to start with.** The 1,555 pages already
    on disk are the starting population -- no browser, no rate limit, no CAPTCHA.

    Same rules as the extension's TSVs: every `INDI` is a real Geni profile, and an unknown parent
    is an absent slot. Where `build-scraped-gedcom.py` minted two `NN` parents to hold a sibling
    group, this writes the group as a `FAM` with `CHIL` and no partners.

    **Half-siblings are still skipped**, and that ruling is unchanged: two half-siblings share
    exactly one parent, so giving them both would assert a marriage that did not happen. Where a
    pair is half-siblings, both siblings are visited to clarify.
    """
    people = dict(names)
    people.setdefault(subject, names.get(subject, ""))
    fams = []
    seen = set()
    for phrase, others in edges:
        ids = [pid for pid, _ in others]
        if phrase in ("son of", "daughter of", "child of"):
            key = ("C", tuple(sorted(ids)), subject)
            if key in seen or not ids:
                continue
            seen.add(key)
            fams.append({"husb": ids[0], "wife": ids[1] if len(ids) > 1 else None,
                         "chil": [subject]})
        elif phrase in ("father of", "mother of"):
            key = ("P", subject, tuple(sorted(ids)))
            if key in seen:
                continue
            seen.add(key)
            fams.append({"husb": subject if phrase == "father of" else None,
                         "wife": subject if phrase == "mother of" else None,
                         "chil": ids})
        elif phrase in ("husband of", "wife of", "partner of"):
            for other in ids:
                pair = tuple(sorted((subject, other)))
                if ("S", pair) in seen:
                    continue
                seen.add(("S", pair))
                fams.append({"husb": subject if phrase == "husband of" else other,
                             "wife": other if phrase == "husband of" else subject,
                             "chil": []})
        elif (phrase.endswith("brother of") or phrase.endswith("sister of"))                 and not phrase.startswith("half"):
            group = sorted({subject} | set(ids))
            key = ("SIB", tuple(group))
            if key in seen:
                continue
            seen.add(key)
            # No parents are invented. Siblinghood stated, parentage not claimed.
            fams.append({"chil": group})
    if not fams:
        return None
    return render("subject geni:%s" % subject, people, {}, fams,
                  "one tiny GEDCOM per saved Geni profile page")


def main():
    PROFILE_OUT.mkdir(parents=True, exist_ok=True)
    PATH_OUT.mkdir(parents=True, exist_ok=True)

    n_prof = n_path = 0
    for p in sorted((ROOT / "geni-families").glob("*-family.tsv")):
        subject, name, rels = read_family_tsv(p)
        text = profile_gedcom(subject, name, rels)
        if text:
            (PROFILE_OUT / ("%s.ged" % subject)).write_text(text, encoding="utf-8")
            n_prof += 1
    # `geni-families/` is deleted; this glob finds nothing until the collector writes there again.

    # ⛔ THE SAVED-PAGE SECTIONS ARE GONE. Ruled 2026-09-10, "structured only, delete the prose
    # parser". Both of them read a saved page's PROSE -- the immediate-family cell for profiles,
    # the relationship panel for paths -- and the relation was inferred from an opener governing a
    # run of anchors. Every defect that reader had came from that shape, and the extension now
    # reads the card grid, where the relation is an attribute of each card.
    #
    # `scripts/scraped_pages.py`, `scripts/prove-saved-page-equivalence.py` and
    # `scripts/family-scrape-js.py` are deleted with them, and so are the 457
    # `exports/tiny-paths/saved-*.ged` they produced. Emma: *"No rescraping just deleting them.
    # They will be rescraped later if determined by the algorithm."*
    n_pages = n_bad = 0

    # ⛔ THE PATH SECTION STAYS. It was deleted with the profile section on 2026-09-10 and put
    # straight back: Emma, *"what the fuck is tiny paths lol that sounds like not immediate family
    # scraping"*, and she is right. These are RELATIONSHIP PATHS -- a chain from the subject to
    # whoever Geni was asked about -- read by `genimerge.genipage.read_relationship_path` from the
    # relationship panel. That is a different panel and a different reader from the
    # immediate-family prose, it has none of the opener/phrase-table problems that got the family
    # parser deleted, and it is the same extractor that produced `paths/*.tsv`, so the two cannot
    # disagree.
    from genimerge.genipage import read_relationship_path
    n_page_paths = 0
    for p in sorted((ROOT / "geni-scraping").glob("*.html")):
        if not p.stem.isdigit():
            continue
        out_path = PATH_OUT / ("saved-%s.ged" % p.stem)
        if out_path.exists():
            continue
        try:
            links = read_relationship_path(p)
        except Exception:
            continue
        rows = [{"name": l.name, "rel": (l.relation or "").strip().lower(), "gid": l.geni_id}
                for l in links if l.geni_id]
        text = path_gedcom("saved-%s" % p.stem, rows,
                           "one tiny GEDCOM per relationship path, read off a saved profile page")
        if text:
            out_path.write_text(text, encoding="utf-8")
            n_page_paths += 1

    # Both directories: `paths/` is Emma's, from 2026-08-05; `harvested-paths/` is where
    # scripts/split-path-chains.py puts the machine-written ones, separated 2026-09-14.
    for p in sorted(list((ROOT / "paths").glob("*.tsv"))
                    + list((ROOT / "harvested-paths").glob("*.tsv"))):
        rows = read_path_tsv(p)
        text = path_gedcom(p.stem, rows)
        if text:
            (PATH_OUT / ("%s.ged" % p.stem)).write_text(text, encoding="utf-8")
            n_path += 1

    print("profiles: %d from extension scrapes, %d from saved pages (%d unparseable) in %s"
          % (n_prof, n_pages, n_bad, PROFILE_OUT.relative_to(ROOT)))
    print("paths:    %d from paths/*.tsv, %d from saved pages in %s"
          % (n_path, n_page_paths, PATH_OUT.relative_to(ROOT)))
    print("invented people: 0 -- an unknown parent is an absent slot")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
