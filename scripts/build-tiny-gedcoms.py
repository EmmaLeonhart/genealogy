"""Two operations, both producing tiny GEDCOMs, and NEITHER invents a person.

**Emma, 2026-09-06:** *"There's two distinct operations. Paths and profiles. Both ought to make
tiny gedcoms for each path or individual. Both have similar information. Many saved pages have the
info to make both tiny gedcoms from them."*

    profiles   one .ged per PERSON  <- geni-families/*.tsv, geni-scraping/*.html
    paths      one .ged per PATH    <- paths/*.tsv

## The ruling that changed: an unknown parent is an ABSENT SLOT, not an `NN` person

**Emma, 2026-09-06**, asked directly and choosing between placeholder people and empty slots:
**absent slot, no person.** That supersedes her 2026-08-29 *"Both parents are 'NN' placeholders"*,
which `scripts/build-scraped-gedcom.py` implements and which minted 4,928 of them.

A GEDCOM `FAM` needs neither partner. Siblings with no known parents are a family with `CHIL` and
no `HUSB`/`WIFE` -- which says *these people are siblings* and asserts nothing about who the
parents were. That is the whole difference between the two emitters, and it is hers to have made:
nothing here creates a human that was not named on a page.

## ⛔ WHY THE REDUNDANCY IS THE POINT, and it is an instruction rather than an accident

**Emma, 2026-09-06, twice over:** *"every single sibling pair gets the small scrape done on it ...
needs to be done on every single person, every single person in sibling pairs. And, yes, I know
this is slightly redundant, but I'm telling you to do it. I'm telling you to do it."*

And the reason, in her words: *"it'll create a gedcom for each one of the members of the sibling
pair, and then this links them as siblings with their parents in this new gedcom file, but they're
also linked as siblings in the path gedcom files."*

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
* **Names stay whole strings.** Emma, 2026-08-29: *"the names being present as strings makes
  things significantly harder... You'd probably be using spacing to figure out what the last name
  is."* No `GIVN`/`SURN` split.
* **A family xref is a digest of its members**, so one family is one family in every file that
  names it and re-running is byte-identical. Emma's own note on this: *"geni does not expose
  family ids ... I'm not sure how much it matters as wikidata does not use families"* -- it is
  bookkeeping, kept because it costs nothing over a counter, not a headline property.
* **A former marriage carries `1 DIV Y`, an engagement `1 ENGA Y`** -- kept from the script this
  supersedes, where it closed 58 of the 59 remaining broken path links.
"""

from __future__ import annotations

import hashlib
import io
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

PARENTS = {"parent"}
CHILDREN = {"child"}
SPOUSES = {"spouse", "partner", "ex-spouse"}
SIBLINGS = {"sibling", "half-sibling"}

#: The relation word on a path row, mapped to what it makes the row's person to the previous one.
PATH_REL = {
    "father": "parent", "mother": "parent",
    "son": "child", "daughter": "child",
    "husband": "spouse", "wife": "spouse", "partner": "spouse",
    "brother": "sibling", "sister": "sibling",
}
FORMER = re.compile(r"^ex-(husband|wife|partner)$", re.I)
ENGAGED = {"fiancee", "fiance"}


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
    for gid, nm in people.items():
        out.append("0 @I%s@ INDI" % gid)
        out.append("1 NAME %s" % (nm or "NN"))
        if gid in sex:
            out.append("1 SEX %s" % sex[gid])
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
        if f.get("div"):
            out.append("1 DIV Y")
        if f.get("enga"):
            out.append("1 ENGA Y")
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

    parents = [r["geni_id"] for r in rels if r["relation"] in PARENTS]
    children = [r["geni_id"] for r in rels if r["relation"] in CHILDREN]
    spouses = [r["geni_id"] for r in rels if r["relation"] in SPOUSES]
    siblings = [r["geni_id"] for r in rels if r["relation"] in SIBLINGS]

    fams = []
    if parents or siblings:
        # The birth family. With no parents named this is CHIL-only -- siblinghood stated, and
        # nothing claimed about who the parents were. Her ruling: absent slot, no person.
        fams.append({"husb": parents[0] if parents else None,
                     "wife": parents[1] if len(parents) > 1 else None,
                     "chil": [subject] + siblings})
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


def path_gedcom(name, rows):
    """Consecutive rows are one family edge; a sibling hop is a CHIL-only family."""
    if len(rows) < 2:
        return None
    people = {r["gid"]: r["name"] for r in rows}
    fams = []
    for prev, cur in zip(rows, rows[1:]):
        word = cur["rel"].split()[-1] if cur["rel"] else ""
        former = bool(FORMER.match(word))
        if former:
            word = word.split("-", 1)[1]
        kind = PATH_REL.get(word)
        if kind is None and word in ENGAGED:
            kind, former = "spouse", False
        if kind is None:
            continue
        if kind == "parent":
            fams.append({"husb": cur["gid"], "chil": [prev["gid"]]})
        elif kind == "child":
            fams.append({"husb": prev["gid"], "chil": [cur["gid"]]})
        elif kind == "spouse":
            fams.append({"husb": prev["gid"], "wife": cur["gid"],
                         "div": former, "enga": word in ENGAGED})
        elif kind == "sibling":
            # ⛔ No parents are invented. The pair is a family with two children and no partners;
            # their real parents arrive from each member's own profile scrape, which is why she
            # requires the scrape on BOTH members of every sibling pair.
            fams.append({"chil": [prev["gid"], cur["gid"]]})
    if not fams:
        return None
    return render("path %s" % name, people, {}, fams,
                  "one tiny GEDCOM per Geni relationship path")


# ---------------------------------------------------------------- saved pages

def saved_page_gedcom(subject, names, edges):
    """A tiny GEDCOM from one saved `geni-scraping/<id>.html`.

    **Emma, 2026-09-06:** *"we save them on every saved geni html page to start."* The 1,555 pages
    already on disk are the starting population -- no browser, no rate limit, no CAPTCHA.

    Same rules as the extension's TSVs: every `INDI` is a real Geni profile, and an unknown parent
    is an absent slot. Where `build-scraped-gedcom.py` minted two `NN` parents to hold a sibling
    group, this writes the group as a `FAM` with `CHIL` and no partners.

    **Half-siblings are still skipped**, which is hers and unchanged: two half-siblings share
    exactly one parent, so giving them both would assert a marriage that did not happen. Her
    ruling: *"If half siblings we go to both siblings to clarify."*
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

    from genimerge.genipage import html_of_saved_page
    from scraped_pages import parse_family
    n_pages = n_bad = 0
    for p in sorted((ROOT / "geni-scraping").glob("*.html")):
        subject = p.stem
        if not subject.isdigit():
            continue
        out_path = PROFILE_OUT / ("%s.ged" % subject)
        if out_path.exists():
            continue          # an extension scrape is fresher; do not overwrite it
        try:
            names, edges = parse_family(
                html_of_saved_page(io.open(p, encoding="utf-8", errors="replace").read()))
            text = saved_page_gedcom(subject, names, edges)
        except Exception:
            n_bad += 1
            continue
        if text:
            out_path.write_text(text, encoding="utf-8")
            n_pages += 1

    for p in sorted((ROOT / "paths").glob("*.tsv")):
        rows = read_path_tsv(p)
        text = path_gedcom(p.stem, rows)
        if text:
            (PATH_OUT / ("%s.ged" % p.stem)).write_text(text, encoding="utf-8")
            n_path += 1

    print("profiles: %d from extension scrapes, %d from saved pages (%d unparseable) in %s"
          % (n_prof, n_pages, n_bad, PROFILE_OUT.relative_to(ROOT)))
    print("paths:    %d tiny gedcoms in %s" % (n_path, PATH_OUT.relative_to(ROOT)))
    print("invented people: 0 -- an unknown parent is an absent slot")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
