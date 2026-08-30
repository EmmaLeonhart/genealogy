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

OUT_DIR = "gedcom/scraped"
PAGES = "geni-scraping/*.html"


def emit(people, families, path, note):
    os.makedirs(OUT_DIR, exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("0 HEAD\n1 SOUR genimerge-scraped\n1 CHAR UTF-8\n")
        fh.write("1 NOTE %s\n" % note)
        fh.write("0 @SUB1@ SUBM\n1 NAME genimerge\n")
        for gid, name in sorted(people.items()):
            fh.write("0 @I%s@ INDI\n" % gid)
            fh.write("1 NAME %s\n" % name)
            fh.write("1 RFN geni:%s\n" % gid)
        for i, (husb, wife, kids) in enumerate(families, 1):
            fh.write("0 @FS%d@ FAM\n" % i)
            if husb:
                fh.write("1 HUSB @I%s@\n" % husb)
            if wife:
                fh.write("1 WIFE @I%s@\n" % wife)
            for k in sorted(kids):
                fh.write("1 CHIL @I%s@\n" % k)
        fh.write("0 TRLR\n")


def from_pages():
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
            # siblings are deliberately dropped: without the shared parents there is no
            # FAM to express them in, and inventing one would assert parents we do not have
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


def from_paths():
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
            elif kind == "spouse":
                pair = tuple(sorted((pid, prev_id)))
                if ("S", pair) in seen:
                    continue
                seen.add(("S", pair))
                fams.append((pid if word == "husband" else prev_id,
                             prev_id if word == "husband" else pid, set()))
    return {g: n for g, n in people.items() if n}, fams


def main():
    people, fams, bad = from_pages()
    out = os.path.join(OUT_DIR, "scraped-pages.ged")
    emit(people, fams, out,
         "built by scripts/build-scraped-gedcom.py from geni-scraping/ saved profile pages")
    print(f"saved pages: {len(glob.glob(PAGES))} read, {bad} unreadable")
    print(f"  people with a name : {len(people):,}")
    print(f"  families           : {len(fams):,}")
    print(f"  wrote {out} ({os.path.getsize(out):,} bytes)")

    ppl, pf = from_paths()
    out2 = os.path.join(OUT_DIR, "scraped-paths.ged")
    emit(ppl, pf, out2,
         "built by scripts/build-scraped-gedcom.py from paths/*.tsv relationship paths")
    print(f"paths: {len(glob.glob('paths/*.tsv'))} files")
    print(f"  people with a name : {len(ppl):,}")
    print(f"  families           : {len(pf):,}")
    print(f"  wrote {out2} ({os.path.getsize(out2):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
