"""The descendant reports, parsed into a family tree the synoptic tree can merge.

    python scripts/parse-sweep-trees.py [--date YYYY-MM-DD] [--dry-run]

Queue item, ruled 2026-09-21: *"we can make the descendant reports into family trees through
parsing."* `reports/sweep-report-parsing.md` measured it feasible. This builds it.

## The ruling on how, 2026-09-24

*"The actual content is extremely regular with string matching plus the generation numbers.
You can pretty easily narrow down things almost entirely. ... we do create individuals based
solely on their names ... but we do zipper merging on the individuals that are created solely
based off of their label."*

So there are two kinds of person here and they never mix:

    a swept row      @I<geni id>@       the row's own Geni id -- EXACT join with the corpus
    a named parent   @IL<digits>@       no row, no id: an individual made from a label alone
    or spouse                            (`L` for label; `@IL…@` cannot parse as a Geni id)

## Step 1 -- string matching plus the generation number, inside one file

A row's `Son of X and Y` names its parents. Each name is looked up among the rows of the SAME
file, by the folded display name, and narrowed by the generation read from
`relationship_text`:

    a parent of a generation-g row has depth >= g-1, and at least one parent has depth g-1

That is an invariant of the report, not a heuristic: depth is the shortest descent from the
focus, so no parent can be shallower than g-1 and the parent the descent ran through is exactly
g-1. **A name resolves only when exactly one row satisfies it.** At generation 1 the parent who
is the focus resolves to `focus_id`.

The same child is swept in many files. Every file votes, and a child's parent slot takes a Geni
id only when the votes name exactly one; two different ids are a conflict and neither is used.

## Step 2 -- the label-only individuals

A name that does not resolve is almost always the spouse who married in and so has no row. It
becomes an individual made from its label, keyed on **its resolved co-parent and its folded
name**:

    ("sp", <co-parent geni id>, <folded name>)

`Husband of Z` on the co-parent's own row produces the same key, so every child and the
marriage line land on ONE label-only person, across every file, with no name comparison
outside that one co-parent's household. A couple where NEITHER name resolves -- measured, the
descendant parent is usually simply absent from a partial capture -- is made as two label-only
people keyed on the lowest id among the siblings in that file naming the same couple:

    ("pair", <sibling anchor>, <folded name>, M|F)

**Geni names the father first**, measured at 11,854 (M, F) against zero (F, M), so position
gives the sex wherever neither the row nor the corpus does.

## Step 3 -- the zipper, over the label-only individuals only

A label-only person has a slot -- parent of these children, spouse of this person -- and the
corpus (`out/family-structure.tsv.gz`, `reports/derived-*.csv.gz`) may already fill it:

    parent   the child's corpus father / mother. One -> identified (solo). Several -> the
             folded name must pick exactly one (name).
    spouse   the co-parent's corpus spouses not already accounted for. Solo, then name.

Solo, then name, inside a slot -- `CLAUDE.md` § *The zipper's one name exception lives inside
a slot*. A proposal refuted by sex is dropped; children disagreeing about who their label-only
parent is are a conflict and the person stays label-only. Every identification is written to
`reports/sweep-parsed-zipper.tsv` with its slot, method and the anchor it hung off.

## What is emitted -- only what the corpus lacks

    a swept person not in the corpus            a full INDI: NAME, SEX, years, FAMC/FAMS
    a swept person already in the corpus        a stub INDI carrying only the new pointers
    a label-only person the zipper left alone   a full INDI @IL…@
    a child whose corpus family exists          the missing HUSB/WIFE goes onto THAT family's
                                                xref, so the merge adds to it, not beside it
    a family the corpus does not have           @FL<digits>@

An edge the corpus already holds is never emitted, so merging the output adds edges and never
duplicates a household. The GEDCOM is written in shards under `exports/sweep-parsed/`,
each under GitHub's file limit, and **refuses to overwrite** an existing path.
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime
import glob
import gzip
import hashlib
import io
import os
import re
import sys
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWEEP = os.path.join(ROOT, "reports", "sweep")
STRUCTURE = os.path.join(ROOT, "out", "family-structure.tsv.gz")
FAMILY = os.path.join(ROOT, "reports", "derived-family.csv.gz")
FACTS = os.path.join(ROOT, "reports", "derived-facts.csv.gz")
LABELS = os.path.join(ROOT, "reports", "derived-labels.csv.gz")
OUT_DIR = os.path.join(ROOT, "exports", "sweep-parsed")
ZIPPER_OUT = os.path.join(ROOT, "reports", "sweep-parsed-zipper.tsv")

#: Shard size in records. 200,000 INDI/FAM records is ~20 MB of GEDCOM -- far under GitHub's
#: 100 MB refusal, which is what declined every push on 2026-09-19.
SHARD_RECORDS = 200_000

# ---------------------------------------------------------------------------------------------
# generation -- the same reader as analyse-sweep-generations.py, digits and words both

NTH = re.compile(r"(\d+)(?:st|nd|rd|th)\s+great\s+grand", re.I)
WORDS = {"second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7,
         "eighth": 8, "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12}
WORD_NTH = re.compile(r"(%s)\s+great\s+grand" % "|".join(WORDS), re.I)


def generation(rel: str) -> int:
    """Depth below the focus, or 0 when the string is not a descent."""
    r = rel.lower()
    m = NTH.search(r)
    if m:
        return int(m.group(1)) + 2
    m = WORD_NTH.search(r)
    if m:
        return WORDS[m.group(1).lower()] + 2
    if "great grand" in r:
        return 3
    if "grand" in r:
        return 2
    if re.search(r"'s (son|daughter|child)\b", r):
        return 1
    return 0


def sex_of_relationship(rel: str) -> str:
    r = rel.lower()
    if re.search(r"(son|grandson)\b", r):
        return "M"
    if re.search(r"(daughter|granddaughter)\b", r):
        return "F"
    return ""


# ---------------------------------------------------------------------------------------------
# the immediate-family string -- a closed role vocabulary

ROLES = ("Half brother of", "Half sister of", "Half sibling of", "Ex-husband of", "Ex-wife of",
         "Ex-partner of", "Son of", "Daughter of", "Child of", "Husband of", "Wife of",
         "Partner of", "Father of", "Mother of", "Parent of", "Brother of", "Sister of",
         "Sibling of", "Fiancé of", "Fiancée of")
ROLE_RE = re.compile(r"(?:^|(?<=\s))(%s) " % "|".join(re.escape(r) for r in ROLES))
PARENT_ROLES = {"Son of": "M", "Daughter of": "F", "Child of": ""}
#: The row person's sex implied by each spouse role; the spouse is then the other sex.
SPOUSE_ROLES = {"Husband of": "M", "Wife of": "F", "Ex-husband of": "M", "Ex-wife of": "F",
                "Partner of": "", "Ex-partner of": ""}
OWN_SEX = {"Father of": "M", "Mother of": "F", "Brother of": "M", "Sister of": "F",
           "Half brother of": "M", "Half sister of": "F"}
TRUNCATION = re.compile(r"(«\s*less|\band \d+ others?;?|\bmore »)")


def roles(text: str) -> dict[str, str]:
    """`Immediate Family: Son of X and Y Husband of Z` -> {"Son of": "X and Y", ...}."""
    text = text[len("Immediate Family:"):].strip() if text.startswith("Immediate Family:") \
        else text.strip()
    out: dict[str, str] = {}
    marks = list(ROLE_RE.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out.setdefault(m.group(1), text[m.end():end].strip())
    return out


def listed(cell: str) -> list[str]:
    """`A; B and C` -> [A, B, C], with Geni's truncation markers removed."""
    cell = TRUNCATION.sub("", cell).strip(" ;")
    parts = [p.strip() for p in cell.split(";") if p.strip()]
    if parts:
        a, sep, b = parts[-1].rpartition(" and ")
        if sep:
            parts[-1:] = [a.strip(), b.strip()]
    return [p for p in parts if p]


QUOTED = re.compile(r'\s*"[^"]*"')
#: The years, after nicknames are cut -- a nickname LIST `"A", "B"` leaves its commas behind.
DATES = re.compile(r"\s*\(([^()]*)\)[\s,]*$")
YEARS = re.compile(r"^(c\.\s*)?(\d{3,4})?\s*-\s*(c\.\s*)?(\d{3,4})?$")


def fold(name: str) -> str:
    """The comparison form: nicknames and whitespace out, case folded, diacritics KEPT."""
    return " ".join(QUOTED.sub(" ", name).split()).casefold()


def split_name(name_text: str) -> tuple[str, str, str]:
    """`Name: Albrecht Dobbin (c.1629 - 1665) "Albert"` -> (display, birth, death)."""
    s = name_text[len("Name:"):].strip() if name_text.startswith("Name:") else name_text.strip()
    s = QUOTED.sub("", s).strip()
    birth = death = ""
    m = DATES.search(s)
    if m:
        y = YEARS.match(m.group(1).strip())
        if y:
            birth = ("ABT " if y.group(1) else "") + y.group(2) if y.group(2) else ""
            death = ("ABT " if y.group(3) else "") + y.group(4) if y.group(4) else ""
        s = s[:m.start()].strip()
    # Geni's Master Profile badge. It is on the row's own name and never in the family text,
    # so leaving it on made every MP parent unmatchable.
    if s.endswith(" MP"):
        s = s[:-3].rstrip()
    return s, birth, death


#: `/people/Jacob-Bibler/6000000003154669752?through=…`. The family text names a parent by
#: Geni's SHORT name -- `Jacob Bibler` for the row `Jacob Asa Bibler` -- and the URL slug is
#: that short name with hyphens for spaces, so it is the second index a name is looked up in.
SLUG = re.compile(r"^/people/([^/]+)/\d+")


def slug(name: str) -> str:
    """Both sides go through this: Geni's slug is percent-encoded and drops punctuation --
    `d'Orléans` is `d-Orl%C3%A9ans` -- so any non-word run becomes one hyphen."""
    return "-".join(re.findall(r"\w+", urllib.parse.unquote(QUOTED.sub(" ", name)))).casefold()


def label_xref(kind: str, key: tuple) -> str:
    """A stable, unparseable-as-Geni xref for a label-only record."""
    digest = hashlib.sha1("\x1f".join(key).encode("utf-8")).hexdigest()[:15]
    return "@%sL%d@" % (kind, int(digest, 16))


# ---------------------------------------------------------------------------------------------
# step 1 -- parse every file

class Parse:
    def __init__(self):
        self.name: dict[str, str] = {}        # geni id -> display name
        self.years: dict[str, tuple] = {}     # geni id -> (birth, death)
        self.sex: dict[str, str] = {}         # geni id -> M/F from its own row
        # child -> {geni ids voted as parent}, and the label-only names voted
        self.parent_ids: dict[str, set] = collections.defaultdict(set)
        # child -> {(co-parent id, folded name, display name, sex by position)}
        self.parent_labels: dict[str, set] = collections.defaultdict(set)
        # child -> {(sibling anchor, folded father, father, folded mother, mother)}: a couple
        # neither of whom resolved, made as TWO label-only people
        self.pair_labels: dict[str, set] = collections.defaultdict(set)
        # person -> {(folded spouse name, display, implied spouse sex)} and resolved spouse ids
        self.spouse_labels: dict[str, set] = collections.defaultdict(set)
        self.spouse_ids: dict[str, set] = collections.defaultdict(set)
        self.stats = collections.Counter()
        self.order = collections.Counter()   # (sex of first-named, sex of second) when both resolve

    def file(self, path: str) -> None:
        focus = os.path.basename(path)[len("sweep-descendants-"):-len(".tsv")]
        rows = []
        with io.open(path, encoding="utf-8", errors="replace") as fh:
            head = fh.readline().rstrip("\n").split("\t")
            try:
                gi, ni = head.index("geni_id"), head.index("name_text")
                hi = head.index("name_hrefs")
                ri, fi = head.index("relationship_text"), head.index("immediate_family_text")
            except ValueError:
                self.stats["files without the columns"] += 1
                return
            width = max(gi, ni, ri, fi, hi)
            for line in fh:
                c = line.rstrip("\n").split("\t")
                if len(c) <= width or not c[gi].isdigit():
                    continue
                rows.append((c[gi], c[ni], c[ri], c[fi], c[hi]))
        self.stats["files"] += 1
        by_name: dict[str, list] = collections.defaultdict(list)
        by_slug: dict[str, list] = collections.defaultdict(list)
        depth: dict[str, int] = {}
        for gid, name_text, rel, fam, href in rows:
            display, birth, death = split_name(name_text)
            if display:
                self.name.setdefault(gid, display)
                by_name[fold(display)].append(gid)
            m = SLUG.match(href)
            if m:
                by_slug[slug(m.group(1))].append(gid)
            if birth or death:
                self.years.setdefault(gid, (birth, death))
            depth[gid] = generation(rel)
            s = sex_of_relationship(rel)
            if s:
                self.sex.setdefault(gid, s)
        focus_fold = fold(self.name.get(focus, ""))
        orphans: dict[tuple, list] = collections.defaultdict(list)

        def resolve(name: str, floor: int) -> str | None:
            f = fold(name)
            if floor == 0 and focus_fold and f == focus_fold:
                return focus
            for index, k in ((by_name, f), (by_slug, slug(name))):
                hits = {g for g in index.get(k, ()) if depth.get(g, 0) >= floor}
                if hits:
                    return next(iter(hits)) if len(hits) == 1 else None
            return None

        for gid, _name, rel, fam, _href in rows:
            self.stats["rows"] += 1
            g = depth[gid]
            r = roles(fam)
            for role, own in list(OWN_SEX.items()) + [(k, v) for k, v in SPOUSE_ROLES.items()]:
                if role in r and own:
                    self.sex.setdefault(gid, own)
            for role, own in PARENT_ROLES.items():
                if role in r and own:
                    self.sex.setdefault(gid, own)
            cell = next((r[k] for k in PARENT_ROLES if k in r), None)
            if cell is not None and g:
                self.stats["rows naming parents"] += 1
                self._parents(gid, g, cell, resolve, orphans)
            for role, own in SPOUSE_ROLES.items():
                if role not in r:
                    continue
                other = {"M": "F", "F": "M"}.get(self.sex.get(gid, own) or own, "")
                for spouse in listed(r[role]):
                    sid = resolve(spouse, 1)
                    if sid:
                        self.spouse_ids[gid].add(sid)
                    else:
                        self.spouse_labels[gid].add((fold(spouse), spouse, other))
        # siblings in this file naming the same unresolved couple share one pair of people,
        # anchored on the lowest sibling id so the key does not depend on row order
        for (fa, fb, _g), kids in orphans.items():
            anchor = min(k for k, _a, _b in kids)
            for kid, a, b in kids:
                self.pair_labels[kid].add((anchor, fa, a, fb, b))

    def _parents(self, gid, g, cell, resolve, orphans):
        cell = TRUNCATION.sub("", cell).strip()
        pieces = cell.split(" and ")
        splits = [(" and ".join(pieces[:k]), " and ".join(pieces[k:]))
                  for k in range(1, len(pieces))] or [(cell, "")]
        chosen = None
        for a, b in splits:
            ra, rb = resolve(a, g - 1), (resolve(b, g - 1) if b else None)
            if len(splits) == 1 or ra or rb:
                if chosen is not None:
                    self.stats["parent strings split ambiguously"] += 1
                    return
                chosen = (a, b, ra, rb)
        if chosen is None:
            self.stats["parent strings with no resolvable split"] += 1
            return
        a, b, ra, rb = chosen
        if ra and rb:
            self.order[(self.sex.get(ra, ""), self.sex.get(rb, ""))] += 1
        # the invariant: at least one parent sits at exactly g-1 (or is the focus, at g=1)
        # Geni names the FATHER FIRST. Measured over 300 files where both names resolved:
        # 11,854 (M, F) and not one (F, M). So position supplies the sex wherever the tree
        # has none -- a fact about Geni's rendering, not a parse of the name.
        resolved = [(x, s) for x, s in ((ra, "M"), (rb, "F")) if x]
        if not resolved:
            if a and b:
                self.stats["couples with neither parent resolved (made as a label pair)"] += 1
                orphans[(fold(a), fold(b), g)].append((gid, a, b))
            return
        for x in resolved:
            self.parent_ids[gid].add(x)
        self.stats["parents resolved to a geni id"] += len(resolved)
        if ra and rb:
            return
        co, name, pos = (ra, b, "F") if ra else (rb, a, "M")
        if not name:
            return
        self.stats["parents made from a label"] += 1
        self.parent_labels[gid].add((co, fold(name), name, pos))


# ---------------------------------------------------------------------------------------------
# the corpus side

def read_corpus():
    corpus = set()
    fathers, mothers, spouses = {}, {}, {}
    with gzip.open(FAMILY, "rt", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = row["geni_id"]
            corpus.add(g)
            split = lambda c: [x.strip() for x in re.split(r"[,;|]", c or "") if x.strip()]
            fathers[g] = split(row.get("fathers") or row.get("father"))
            mothers[g] = split(row.get("mothers") or row.get("mother"))
            spouses[g] = split(row.get("spouses"))
    sex = {}
    with gzip.open(FACTS, "rt", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["sex"]:
                sex[row["geni_id"]] = row["sex"]
    label = {}
    with gzip.open(LABELS, "rt", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            label[row["geni_id"]] = row["label_en"] or row["label_mul"]
    fam_p, fam_c, fams, famc = {}, {}, {}, {}
    maps = {"fam_p": fam_p, "fam_c": fam_c, "fams": fams, "famc": famc}
    with gzip.open(STRUCTURE, "rt", encoding="utf-8") as fh:
        fh.readline()
        for line in fh:
            m, k, v = line.rstrip("\n").split("\t")
            maps[m][k] = v.split()
    return corpus, fathers, mothers, spouses, sex, label, fam_p, fam_c, fams, famc


# ---------------------------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="parse only the first N files")
    args = ap.parse_args()

    p = Parse()
    files = sorted(glob.glob(os.path.join(SWEEP, "sweep-descendants-*.tsv")))
    if args.limit:
        files = files[:args.limit]
    for i, path in enumerate(files):
        p.file(path)
        if i % 1000 == 999:
            print("  parsed %d/%d files" % (i + 1, len(files)), flush=True)
    st = p.stats

    (corpus, c_fathers, c_mothers, c_spouses, c_sex, c_label,
     fam_p, fam_c, fams, famc) = read_corpus()
    sex = lambda g: c_sex.get(g) or p.sex.get(g, "")

    # --- the child's parent slots from the votes -------------------------------------------
    father, mother = {}, {}          # child -> geni id or label key
    for child, ids in sorted(p.parent_ids.items()):
        by_sex = collections.defaultdict(set)
        for x, pos in sorted(ids):
            by_sex[sex(x) or pos].add(x)
        for s, slot in (("M", father), ("F", mother)):
            if len(by_sex[s]) == 1:
                slot[child] = next(iter(by_sex[s]))
            elif len(by_sex[s]) > 1:
                st["parent slots with conflicting geni ids (dropped)"] += 1

    # --- the label-only individuals --------------------------------------------------------
    labels: dict[tuple, dict] = {}   # key -> {display, sex, children, co}
    for child, found in sorted(p.parent_labels.items()):
        for co, f, display, pos in sorted(found):
            s = {"M": "F", "F": "M"}.get(sex(co), "") or pos
            slot = father if s == "M" else mother
            if child in slot:
                continue     # another file resolved this slot to a real row
            key = ("sp", co, f)
            rec = labels.setdefault(key, {"display": display, "sex": s, "children": set(),
                                          "co": co})
            rec["children"].add(child)
            slot[child] = key
    for child, found in sorted(p.pair_labels.items()):
        for anchor, fa, a, fb, b in sorted(found):
            if child in father or child in mother:
                continue     # a parent resolved somewhere else; the pair is not needed
            ka, kb = ("pair", anchor, fa, "M"), ("pair", anchor, fb, "F")
            for key, display, s, other, slot in ((ka, a, "M", kb, father),
                                                 (kb, b, "F", ka, mother)):
                rec = labels.setdefault(key, {"display": display, "sex": s,
                                              "children": set(), "co": other})
                rec["children"].add(child)
                slot[child] = key
    for person, found in sorted(p.spouse_labels.items()):
        for f, display, s in sorted(found):
            key = ("sp", person, f)
            if key not in labels and s:
                labels[key] = {"display": display, "sex": s, "children": set(), "co": person}

    # --- step 3: the zipper, over the label-only people only -------------------------------
    ident: dict[tuple, str] = {}
    zrows = []
    taken_spouse = collections.defaultdict(set)
    by_co = collections.defaultdict(list)
    for key in labels:
        by_co[labels[key]["co"]].append(key)
    for key in sorted(labels):
        rec = labels[key]
        props, method = set(), ""
        for child in sorted(rec["children"]):
            cands = (c_fathers if rec["sex"] == "M" else c_mothers).get(child, [])
            if len(cands) == 1:
                props.add(cands[0]); method = method or "solo"
            elif cands:
                hit = [c for c in cands if fold(c_label.get(c, "")) == key[2]]
                if len(hit) == 1:
                    props.add(hit[0]); method = "name"
        slot = "parent"
        if not props:
            slot = "spouse"
            co = rec["co"]
            known = set(p.spouse_ids.get(co, ())) | taken_spouse[co]
            open_ = [s for s in c_spouses.get(co, []) if s not in known
                     and sex(s) in (rec["sex"], "")]
            if len(open_) == 1 and len(by_co[co]) == 1:
                props.add(open_[0]); method = "solo"
            elif open_:
                hit = [s for s in open_ if fold(c_label.get(s, "")) == key[2]]
                if len(hit) == 1:
                    props.add(hit[0]); method = "name"
        if len(props) > 1:
            st["label people the zipper found conflicting (kept as labels)"] += 1
            continue
        if not props:
            continue
        g = next(iter(props))
        if sex(g) and sex(g) != rec["sex"]:
            st["zipper proposals refuted by sex"] += 1
            continue
        if g in taken_spouse[rec["co"]]:
            st["zipper proposals claimed twice (dropped)"] += 1
            continue
        taken_spouse[rec["co"]].add(g)
        ident[key] = g
        co = rec["co"]
        anchor = label_xref("I", co).strip("@") if isinstance(co, tuple) else co
        zrows.append((rec["display"], anchor, slot, method, g, c_label.get(g, ""),
                      " ".join(sorted(rec["children"]))))
    st["label people made"] = len(labels)
    st["label people identified by the zipper"] = len(ident)
    resolve_node = lambda n: ident.get(n, n) if isinstance(n, tuple) else n
    for slot in (father, mother):
        for c in list(slot):
            slot[c] = resolve_node(slot[c])

    # --- families: onto the corpus's own family when it exists, else a new one -------------
    fam_parents: dict[str, dict] = collections.defaultdict(dict)   # fam xref -> role -> node
    fam_children: dict[str, set] = collections.defaultdict(set)
    person_famc = collections.defaultdict(set)
    person_fams = collections.defaultdict(set)

    def corpus_fam_of(f, m):
        if isinstance(f, str) and isinstance(m, str) and f and m:
            both = set(fams.get(f, ())) & set(fams.get(m, ()))
            if len(both) == 1:
                return next(iter(both))
        return None

    def new_fam(f, m):
        key = tuple("L" + "|".join(x) if isinstance(x, tuple) else (x or "")
                    for x in (f, m))
        return label_xref("F", ("fam",) + key)

    def place(fx, role, node):
        if node is None:
            return
        have = fam_parents[fx].get(role)
        if have is None:
            fam_parents[fx][role] = node
            person_fams[node].add(fx)

    for child in sorted(set(father) | set(mother)):
        f, m = father.get(child), mother.get(child)
        cf = famc.get(child, [])
        if len(cf) == 1:
            fid = cf[0]
            parents = fam_p.get(fid, [])
            fx = "@F%s@" % fid
            for role, node, want in (("HUSB", f, "M"), ("WIFE", m, "F")):
                if node is None or node in parents:
                    continue
                if len(parents) >= 2 or any(sex(x) == want for x in parents):
                    st["corpus family already holds another %s (not added)" % role] += 1
                    continue
                place(fx, role, node)
                st["parents added onto an existing corpus family"] += 1
            continue
        if len(cf) > 1:
            st["children with several corpus families (skipped)"] += 1
            continue
        fid = corpus_fam_of(f, m)
        fx = "@F%s@" % fid if fid else new_fam(f, m)
        if not fid:
            place(fx, "HUSB", f)
            place(fx, "WIFE", m)
        fam_children[fx].add(child)
        person_famc[child].add(fx)
        st["child edges added"] += 1

    # marriages with no child here: the spouse line alone
    for key, rec in labels.items():
        if key in ident or rec["children"]:
            continue
        co = rec["co"]
        f, m = (key, co) if rec["sex"] == "M" else (co, key)
        fx = new_fam(f, m)
        place(fx, "HUSB", f)
        place(fx, "WIFE", m)
        st["childless label marriages"] += 1

    # --- write -------------------------------------------------------------------------------
    records = []
    people = set(person_famc) | set(person_fams)
    for node in sorted(people, key=lambda n: (isinstance(n, tuple), str(n))):
        lines = []
        if isinstance(node, tuple):
            rec = labels[node]
            lines += ["0 %s INDI" % label_xref("I", node), "1 NAME %s" % rec["display"],
                      "1 SEX %s" % rec["sex"]]
            st["label INDI written"] += 1
        else:
            lines.append("0 @I%s@ INDI" % node)
            lines.append("1 RFN geni:%s" % node)
            if node not in corpus:
                if node in p.name:
                    lines.append("1 NAME %s" % p.name[node])
                if p.sex.get(node):
                    lines.append("1 SEX %s" % p.sex[node])
                b, d = p.years.get(node, ("", ""))
                for tag, v in (("BIRT", b), ("DEAT", d)):
                    if v:
                        lines += ["1 %s" % tag, "2 DATE %s" % v]
                st["new geni people written"] += 1
            else:
                st["corpus people given a new pointer"] += 1
        for fx in sorted(person_famc.get(node, ())):
            lines.append("1 FAMC %s" % fx)
        for fx in sorted(person_fams.get(node, ())):
            lines.append("1 FAMS %s" % fx)
        records.append(lines)
    ptr = lambda n: label_xref("I", n) if isinstance(n, tuple) else "@I%s@" % n
    for fx in sorted(set(fam_parents) | set(fam_children)):
        lines = ["0 %s FAM" % fx]
        for role in ("HUSB", "WIFE"):
            if role in fam_parents[fx]:
                lines.append("1 %s %s" % (role, ptr(fam_parents[fx][role])))
        for c in sorted(fam_children.get(fx, ())):
            lines.append("1 CHIL @I%s@" % c)
        records.append(lines)
        st["FAM written"] += 1

    print("order of the two parent names when both resolve:", dict(p.order))
    for k in sorted(st):
        print("%-60s %12s" % (k, "{:,}".format(st[k])))
    if args.dry_run:
        return 0

    os.makedirs(OUT_DIR, exist_ok=True)
    shards = [records[i:i + SHARD_RECORDS] for i in range(0, len(records), SHARD_RECORDS)]
    paths = [os.path.join(OUT_DIR, "sweep-parsed-%s-%02d.ged" % (args.date, n + 1))
             for n in range(len(shards))]
    for path in paths:
        if os.path.exists(path):
            print("REFUSING: %s exists -- a new parse is always a new file" % path)
            return 1
    for path, shard in zip(paths, shards):
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("0 HEAD\n1 SOUR sweep-parsed\n1 GEDC\n2 VERS 5.5.1\n1 CHAR UTF-8\n")
            for lines in shard:
                fh.write("\n".join(lines) + "\n")
            fh.write("0 TRLR\n")
        print("wrote %s (%d records)" % (os.path.relpath(path, ROOT), len(shard)))
    with io.open(ZIPPER_OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["label", "anchor", "slot", "method", "geni_id", "corpus_label",
                    "children"])
        w.writerows(sorted(zrows))
    print("wrote %s (%d identifications)" % (os.path.relpath(ZIPPER_OUT, ROOT), len(zrows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
