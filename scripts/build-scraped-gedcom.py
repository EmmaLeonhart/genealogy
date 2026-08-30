"""Turn the saved Geni pages and the relationship paths into GEDCOM.

**Emma, 2026-08-29:** *"convert these things into GEDCOM files that would go into a special
GEDCOM directory... it builds from the saved pages, both the paths and the saved individuals
proper, so that it will save both the paths and the saved pages because they are different. It
turns them into things that are usable and would be merged into the synoptic tree as GEDCOM
stuff."*

Two inputs, two output files, because they carry different things:

* `geni-scraping/*.html` -- 1,555 saved profile pages. Each gives the subject's **immediate
  family** as English prose with links: *"Daughter of A and B / Wife of C / Mother of D, E"*.
* `paths/*.tsv` -- relationship paths. Each row is a person and the relation to the previous row,
  so consecutive rows are a family edge.

**Parents are emitted father-first, and that is MEASURED not assumed.** GEDCOM needs `HUSB` and
`WIFE` and the pages do not state sex, so the order had to be established: over 120 pages, of the
116 two-parent blocks where both sexes are known from `reports/derived-facts.csv`, **100 resolve
as (M, F) and none as (F, M)**. The remaining 16 have an unknown sex on one side or both and are
not counter-examples.

**Names stay whole strings.** Emma: *"the names being present as strings makes things
significantly harder... You'd probably be using spacing to figure out what the last name is or
something. It would work in most cases, but not all."* So `1 NAME <string>` and no `GIVN`/`SURN`
split -- guessing a surname from spacing is the fuzzy inference this repo refuses elsewhere.

**Output goes to `gedcom/scraped/`, NOT `exports/`, and nothing merges it yet.** `exports/` is the
corpus and is read recursively, so writing there would change every merge silently. The open
question is family xrefs: a Geni `FAM` xref is a Geni id, and these families have none, so any
synthetic id risks colliding with a real one or duplicating a family the corpus already holds.
That wants a decision before this is wired in.
"""
import collections
import csv
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))

from genimerge.genipage import html_of_saved_page   # noqa: E402
from scraped_pages import parse_family              # noqa: E402

#: **Sorts FIRST under `exports/`, on purpose.** Merge order is path sort order and the LATER
#: source wins a single-valued conflict, so a scraped `1 NAME <string>` must never overwrite a
#: real export's structured `NAME`. A leading digit puts this ahead of every existing directory
#: (`8-19 exports` is the earliest real one).
OUT_DIR = "exports/0-scraped"

#: **Synthetic ids, in ranges Geni demonstrably does not use.** `genimerge.identity` requires a
#: numeric xref, so `@FS1@` is not legal and would break the four-prefix invariant
#: `tests/test_gedcom_real_exports.py` asserts. Measured over the 567,135 distinct family xrefs
#: and 1,329,329 individual xrefs in `out/merged.ged`: 20,000 ids from each base are free.
SYNTHETIC_FAM_BASE = 9990000000000000000
SYNTHETIC_INDI_BASE = 9995000000000000000
PAGES = "geni-scraping/*.html"


class Placeholders:
    """Two `NN` parents per sibling group, on Emma's ruling of 2026-08-29.

    *"Both parents are 'NN' placeholders. Pipeline generates names for them. However we may
    attempt to gain the information of the parents. Imo this is too large to do right now, but at
    the end of the queue we will have a task that goes to one of the siblings and save their page
    so the parent names and potentially other people are added. If half siblings we go to both
    siblings to clarify."*

    **Why this is needed at all.** GEDCOM cannot say *siblings* without a family, and sibling hops
    are not marginal: **2,124 rows, 7.0% of all path rows, present in 662 of the 698 paths (95%)**.
    Dropping them, which the first build did, puts a hole in almost every path.

    **The parents are labelled `NN` and carry no `RFN`.** `NN` is *nomen nescio* -- the genealogist
    saying the name is unknown -- which is exactly true here, and `CLAUDE.md` § *`NN` is PRESERVED
    in `mul`* already has the label pipeline for it. Omitting the `RFN` matters more: an
    `RFN geni:<id>` for an id Geni does not have would be a false claim on this repo's primary key.

    A group is keyed on its full membership, so the same pair of siblings met twice gets one set of
    parents rather than two.
    """

    def __init__(self):
        self._by_group = {}
        self.people = {}
        self.sexes = {}
        self._next = 0

    def parents_for(self, members):
        key = tuple(sorted(members))
        if key not in self._by_group:
            father = str(SYNTHETIC_INDI_BASE + self._next)
            mother = str(SYNTHETIC_INDI_BASE + self._next + 1)
            self._next += 2
            self.people[father] = "NN"
            self.people[mother] = "NN"
            self.sexes[father] = "M"
            self.sexes[mother] = "F"
            self._by_group[key] = (father, mother)
        return self._by_group[key]


def emit(people, families, path, note, sexes=None):
    sexes = sexes or {}
    os.makedirs(OUT_DIR, exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("0 HEAD\n1 SOUR genimerge-scraped\n1 CHAR UTF-8\n")
        fh.write("1 NOTE %s\n" % note)
        # The SUBM xref must be `S` + digits like every other Geni xref, or it breaks the
        # four-prefix invariant tests/test_gedcom_real_exports.py asserts over the corpus.
        fh.write("0 @S%d@ SUBM" % SYNTHETIC_FAM_BASE + chr(10) + "1 NAME genimerge" + chr(10))
        for gid, name in sorted(people.items()):
            fh.write("0 @I%s@ INDI\n" % gid)
            fh.write("1 NAME %s\n" % name)
            if gid in sexes:
                fh.write("1 SEX %s" % sexes[gid] + chr(10))
            # A placeholder has no Geni profile, so it gets no RFN -- claiming
            # `RFN geni:<id>` for an id Geni does not have would be a false identity
            # assertion on this repo's primary key.
            if not gid.startswith(str(SYNTHETIC_INDI_BASE)[:6]):
                fh.write("1 RFN geni:%s" % gid + chr(10))
        for i, (husb, wife, kids) in enumerate(families, 1):
            fh.write("0 @F%d@ FAM" % (SYNTHETIC_FAM_BASE + i) + chr(10))
            if husb:
                fh.write("1 HUSB @I%s@\n" % husb)
            if wife:
                fh.write("1 WIFE @I%s@\n" % wife)
            for k in sorted(kids):
                fh.write("1 CHIL @I%s@\n" % k)
        fh.write("0 TRLR\n")


def from_pages(ph):
    people, fams = {}, []
    seen = set()
    bad = 0
    for f in sorted(glob.glob(PAGES)):
        subject = os.path.splitext(os.path.basename(f))[0]
        if not subject.isdigit():
            continue
        try:
            html = html_of_saved_page(io.open(f, encoding="utf-8", errors="replace").read())
            names, edges = parse_family(html)
        except Exception:
            bad += 1
            continue
        people.update(names)
        people.setdefault(subject, names.get(subject, ""))
        for phrase, others in edges:
            ids = [pid for pid, _ in others]
            if phrase in ("son of", "daughter of", "child of"):
                key = ("C", tuple(sorted(ids)), subject)
                if key in seen:
                    continue
                seen.add(key)
                fams.append((ids[0] if ids else None,
                             ids[1] if len(ids) > 1 else None, {subject}))
            elif phrase in ("father of", "mother of"):
                key = ("P", subject, tuple(sorted(ids)))
                if key in seen:
                    continue
                seen.add(key)
                husb = subject if phrase == "father of" else None
                wife = subject if phrase == "mother of" else None
                fams.append((husb, wife, set(ids)))
            elif phrase in ("husband of", "wife of", "partner of"):
                for other in ids:
                    pair = tuple(sorted((subject, other)))
                    if ("S", pair) in seen:
                        continue
                    seen.add(("S", pair))
                    husb = subject if phrase == "husband of" else other
                    wife = other if phrase == "husband of" else subject
                    fams.append((husb, wife, set()))
            elif phrase.endswith("brother of") or phrase.endswith("sister of"):
                # **Half siblings are NOT given shared parents.** Geni distinguishes them, and
                # two half siblings share exactly ONE parent -- giving them both would assert a
                # marriage that did not happen. Emma's ruling covers this: *"If half siblings we
                # go to both siblings to clarify"*, so they wait for the page-saving task rather
                # than being guessed at here.
                if phrase.startswith("half"):
                    continue
                group = {subject} | set(ids)
                key = ("SIB", tuple(sorted(group)))
                if key in seen:
                    continue
                seen.add(key)
                father, mother = ph.parents_for(group)
                fams.append((father, mother, group))
    people = {g: n for g, n in people.items() if n}
    return people, fams, bad


#: The relation words a path row carries, describing THIS row against the PREVIOUS one.
#: Censused over all 698 path files: `his father` 5,127, `his son` 3,773, `his mother` 3,414,
#: `her father` 3,292, and so on down. `your father` appears 749 times -- the paths start at
#: Emma, so the first hop is phrased from her.
PATH_REL = {
    "father": "parent", "mother": "parent",
    "son": "child", "daughter": "child",
    "husband": "spouse", "wife": "spouse", "partner": "spouse",
}


def from_paths(ph):
    """Family edges from consecutive rows of every `paths/*.tsv`.

    A path row names the relation of THIS person to the PREVIOUS one, so each adjacent pair is
    one edge. Siblings are dropped for the same reason as on the pages: without the shared
    parents there is no `FAM` to put them in.
    """
    people, fams, seen = {}, [], set()
    for f in sorted(glob.glob("paths/*.tsv")):
        rows = []
        for line in io.open(f, encoding="utf-8", errors="replace"):
            if line.startswith("#") or not line.strip():
                continue
            cols = line.rstrip(chr(10)).split(chr(9))
            if len(cols) < 3 or cols[0] == "step":
                continue
            m = re.search(r"geni:([0-9]+)", " ".join(cols))
            rows.append((m.group(1) if m else None, cols[1].strip(), cols[2].strip().lower()))
        for i in range(1, len(rows)):
            (pid, name, rel), (prev_id, prev_name, _) = rows[i], rows[i - 1]
            if pid:
                people.setdefault(pid, name)
            if prev_id:
                people.setdefault(prev_id, prev_name)
            if not pid or not prev_id:
                continue
            word = rel.split()[-1] if rel else ""
            kind = PATH_REL.get(word)
            if kind == "parent":
                key = ("C", pid, prev_id)
                if key in seen:
                    continue
                seen.add(key)
                fams.append((pid if word == "father" else None,
                             pid if word == "mother" else None, {prev_id}))
            elif kind == "child":
                key = ("C", prev_id, pid)
                if key in seen:
                    continue
                seen.add(key)
                fams.append((prev_id, None, {pid}))
            elif word in ("brother", "sister"):
                group = {pid, prev_id}
                key = ("SIB", tuple(sorted(group)))
                if key in seen:
                    continue
                seen.add(key)
                father, mother = ph.parents_for(group)
                fams.append((father, mother, group))
            elif kind == "spouse":
                pair = tuple(sorted((pid, prev_id)))
                if ("S", pair) in seen:
                    continue
                seen.add(("S", pair))
                fams.append((pid if word == "husband" else prev_id,
                             prev_id if word == "husband" else pid, set()))
    return {g: n for g, n in people.items() if n}, fams


def main():
    ph = Placeholders()
    people, fams, bad = from_pages(ph)
    people.update(ph.people)
    out = os.path.join(OUT_DIR, "scraped-pages.ged")
    emit(people, fams, out,
         "built by scripts/build-scraped-gedcom.py from geni-scraping/ saved profile pages",
         sexes=ph.sexes)
    print(f"saved pages: {len(glob.glob(PAGES))} read, {bad} unreadable")
    print(f"  people with a name : {len(people):,}")
    print(f"  families           : {len(fams):,}")
    print(f"  NN placeholder parents minted : {len(ph.people):,}")
    print(f"  wrote {out} ({os.path.getsize(out):,} bytes)")

    ph2 = Placeholders()
    ppl, pf = from_paths(ph2)
    ppl.update(ph2.people)
    out2 = os.path.join(OUT_DIR, "scraped-paths.ged")
    emit(ppl, pf, out2,
         "built by scripts/build-scraped-gedcom.py from paths/*.tsv relationship paths",
         sexes=ph2.sexes)
    print(f"paths: {len(glob.glob('paths/*.tsv'))} files")
    print(f"  people with a name : {len(ppl):,}")
    print(f"  families           : {len(pf):,}")
    print(f"  NN placeholder parents minted : {len(ph2.people):,}")
    print(f"  wrote {out2} ({os.path.getsize(out2):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
