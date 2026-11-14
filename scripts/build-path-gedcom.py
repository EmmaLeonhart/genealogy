"""Every harvested Geni relationship path, as one GEDCOM the synoptic tree's merge reads like an export.

    python scripts/build-path-gedcom.py

**Why (Emma, 2026-11-12, Genealogy 7):** "add in all of the like Jenny paths into like the data that builds the
synoptic tree". The paths are Geni's own chains (`harvested-paths/*.tsv`, read from the saved /paths permalinks, and
`paths/*.tsv`): one row per step, with the profile's Geni id and its relation to the step before. Every step is a real
Geni parent, child or spouse link, so the chains carry links the bulk exports may not.

**Keyed like an export.** People are `@I<geni id>@` with `1 RFN geni:<id>`, exactly as Geni's GEDCOM writes them, so the
merge joins them to the export records by Geni id and never by name. Families are new records: `@FP<n>@`, one per
(father, mother) pair seen in the chains, and one per couple.

**What a step becomes.** "his father" / "her mother" (the step is the previous person's parent) and "his son" / "her
daughter" (the previous person's child) become family links; "husband" / "wife" become a couple. Siblings are left
out (the chain does not say through which parents), and so are adoptive, step and in-law steps (this is the blood
tree). Steps with no Geni id (step 0, the viewer) are skipped.

Writes `exports/geni-paths/geni-paths.ged` and prints what was read and what was left out.
"""
from __future__ import annotations

import collections
import csv
import datetime
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exports" / "geni-paths" / "geni-paths.ged"
SOURCES = sorted(glob.glob(str(ROOT / "harvested-paths" / "*.tsv"))) + sorted(glob.glob(str(ROOT / "paths" / "*.tsv")))

PARENT = {"father": "M", "mother": "F"}
CHILD = {"son": "M", "daughter": "F"}
SPOUSE = {"husband": "M", "wife": "F"}
SKIP_WORDS = ("adoptive", "step", "in-law", "foster", "half")


def gid_of(note: str) -> str | None:
    m = re.search(r"geni:(\d+)", note or "")
    return m.group(1) if m else None


def rows(path: str):
    with open(path, encoding="utf-8") as fh:
        lines = [ln for ln in fh if not ln.startswith("#")]
    if not lines or "relation_to_previous" not in lines[0]:
        return []
    return list(csv.DictReader(lines, delimiter="\t"))


name, sex = {}, {}
father, mother = {}, {}            # child -> parent
couples = set()
pending = []                       # (child, parent) whose parent's sex is not known yet
counts = collections.Counter()
for src in SOURCES:
    prev = None
    for r in rows(src):
        g = gid_of(r.get("note", "")) or gid_of(r.get("geni", ""))
        rel = (r.get("relation_to_previous") or "").strip().lower()
        if not g:
            prev = None
            continue
        name.setdefault(g, (r.get("name") or "").strip())
        word = rel.split()[-1] if rel and rel != "-" else ""
        if prev and rel.startswith(("his ", "her ")):   # "his son": the previous person is a man
            sex.setdefault(prev, "M" if rel.startswith("his ") else "F")
        if prev and word:
            if any(w in rel for w in SKIP_WORDS):
                counts["left out: adoptive/step/in-law/foster/half"] += 1
            elif word in PARENT:
                sex.setdefault(g, PARENT[word])
                (father if word == "father" else mother).setdefault(prev, g)
                counts["parent links"] += 1
            elif word in CHILD:
                sex.setdefault(g, CHILD[word])
                if sex.get(prev) == "M":
                    father.setdefault(g, prev)
                elif sex.get(prev) == "F":
                    mother.setdefault(g, prev)
                else:
                    pending.append((g, prev))
                counts["child links"] += 1
            elif word in SPOUSE:
                sex.setdefault(g, SPOUSE[word])
                couples.add((g, prev) if word == "husband" else (prev, g))
                counts["spouse links"] += 1
            elif word in ("brother", "sister", "sibling"):
                counts["left out: siblings"] += 1
            else:
                counts[f"left out: other ({word})"] += 1
        prev = g
    counts["path files read"] += 1

# a parent's sex is often learned from a later chain; resolve the held child links now
for c, par in pending:
    if sex.get(par) == "M":
        father.setdefault(c, par)
    elif sex.get(par) == "F":
        mother.setdefault(c, par)
    else:
        counts["left out: child of a parent of unknown sex"] += 1

fams = collections.defaultdict(set)      # (husband, wife) -> children
for c in set(father) | set(mother):
    fams[(father.get(c), mother.get(c))].add(c)
for h, w in couples:
    fams.setdefault((h, w), set())
xref = {key: f"@FP{n}@" for n, key in enumerate(sorted(fams, key=lambda k: (k[0] or "", k[1] or "")), 1)}
famc = collections.defaultdict(list)
fams_of = collections.defaultdict(list)
for key, kids in fams.items():
    for c in kids:
        famc[c].append(xref[key])
    for p in key:
        if p:
            fams_of[p].append(xref[key])

today = datetime.date.today().strftime("%d %b %Y").upper()
out = ["0 HEAD", "1 SOUR genealogy/scripts/build-path-gedcom.py", "1 DATE " + today, "1 GEDC", "2 VERS 5.5.1",
       "2 FORM LINEAGE-LINKED", "1 CHAR UTF-8", "1 NOTE Geni relationship paths (harvested-paths/, paths/), one record per profile"]
people = set(name) | {p for k in fams for p in k if p}
for g in sorted(people, key=int):
    out.append(f"0 @I{g}@ INDI")
    out.append(f"1 NAME {name.get(g) or 'NN'}")
    if sex.get(g):
        out.append(f"1 SEX {sex[g]}")
    out += [f"1 FAMC {x}" for x in sorted(set(famc[g]))]
    out += [f"1 FAMS {x}" for x in sorted(set(fams_of[g]))]
    out.append(f"1 RFN geni:{g}")
for key, kids in sorted(fams.items(), key=lambda kv: xref[kv[0]]):
    out.append(f"0 {xref[key]} FAM")
    if key[0]:
        out.append(f"1 HUSB @I{key[0]}@")
    if key[1]:
        out.append(f"1 WIFE @I{key[1]}@")
    out += [f"1 CHIL @I{c}@" for c in sorted(kids, key=int)]
out.append("0 TRLR")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
print(f"{len(people):,} people, {len(fams):,} families -> {OUT.relative_to(ROOT)}")
for k, v in sorted(counts.items()):
    print(f"  {k}: {v:,}")
