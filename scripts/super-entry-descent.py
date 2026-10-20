"""Trace each super entry point DOWN through the FamilySearch file to the owner's record.

Emma, 2026-10-19: the super entry points "all come from pretty much one family search file", and the
question is where each line comes down into real people, and where the lines join each other. Read from
the raw FamilySearch download only, never Wikidata.

    python scripts/super-entry-descent.py [gedcom]   ->  reports/super-entry-descent.tsv

One row per generation of each line: entry point, step, FamilySearch id, name, birth, death, and the
other entry points whose line passes through the same person. A line is cut before the first person born
from 1900 on (the repo is public).
"""
import collections
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GED = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "gedcom" / "familysearch" / "rootsmagic-PFR5-LDS-2026-09-30.ged"
OWNER = "PFR5-LDS"
#: The FamilySearch records of the super entry points (`reports/super-entry-points.tsv`; Vedrhall's from its note).
ENTRY = {"G5C9-SCV": "Safracht de Gothie", "L7J5-NNV": "Cendfindan mac Maith", "9H6Q-NX6": "Abba ben Marukba",
         "GL4P-RF9": "Vedrhall Himileigsson", "LC58-5QX": "Hocingas de Saxe", "GSMQ-8QW": "Frava De Gaule",
         "LCXK-GNP": "Clodius IV", "GZ1C-ZSY": "Pellinor Ewrawe", "PMGT-ZYB": "Burgerschaft"}

people, fams, fs_of = {}, {}, {}
for rec in re.split(r"\n(?=0 )", GED.read_text(encoding="utf-8", errors="replace")):
    m = re.match(r"0 (@[^@]+@) (INDI|FAM)", rec)
    if not m:
        continue
    x, kind = m.groups()
    if kind == "FAM":
        fams[x] = re.findall(r"\n1 CHIL (@[^@]+@)", rec)
        continue
    name = re.search(r"\n1 NAME (.*)", rec)
    def date(tag):
        d = re.search(rf"\n1 {tag}\n(?:2 (?!DATE).*\n)*2 DATE (.*)", rec)
        return d.group(1).strip() if d else ""
    fs = re.search(r"\n1 _FSFTID (\S+)", rec)
    people[x] = {"name": name.group(1).replace("/", "").strip() if name else "",
                 "birt": date("BIRT"), "deat": date("DEAT"), "fs": fs.group(1) if fs else "",
                 "fams": re.findall(r"\n1 FAMS (@[^@]+@)", rec)}
    if fs:
        fs_of[fs.group(1)] = x

def children(x):
    return [c for f in people[x]["fams"] for c in fams.get(f, [])]

owner = fs_of[OWNER]
# Everyone who has the owner below them, so the walk down never leaves her ancestry.
parents = collections.defaultdict(list)
for x in people:
    for c in children(x):
        parents[c].append(x)
above, todo = {owner}, [owner]
while todo:
    for p in parents[todo.pop()]:
        if p not in above:
            above.add(p)
            todo.append(p)

def descent(x):
    """The line from x down to the owner (first child in file order that leads to her)."""
    path = [x]
    while path[-1] != owner:
        nxt = [c for c in children(path[-1]) if c in above]
        if not nxt:
            return path, False
        path.append(nxt[0])
    return path, True

lines = {}
for fs, label in ENTRY.items():
    x = fs_of.get(fs)
    lines[fs] = descent(x) if x else ([], False)
through = collections.defaultdict(set)
for fs, (path, _) in lines.items():
    for x in path:
        through[x].add(ENTRY[fs])

out = ROOT / "reports" / "super-entry-descent.tsv"
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write("entry_point\tstep\tfs_id\tname\tbirth\tdeath\talso_on_line_of\n")
    for fs, (path, ok) in lines.items():
        if not path:
            f.write(f"{ENTRY[fs]}\t\t{fs}\tNOT IN THE FILE\t\t\t\n")
        for i, x in enumerate(path):
            p = people[x]
            # The repo is public: the line stops before anyone born from 1900 on (the owner's living family).
            y = re.search(r"\d{4}", p["birt"])
            if (int(y.group()) >= 1900) if y else not re.search(r"\d{4}", p["deat"]) and i > 30:
                f.write(f"{ENTRY[fs]}\t{i}\t\t(continues to {OWNER}; later generations not written)\t\t\t\n")
                break
            others = ", ".join(sorted(through[x] - {ENTRY[fs]}))
            f.write(f"{ENTRY[fs]}\t{i}\t{p['fs']}\t{p['name']}\t{p['birt']}\t{p['deat']}\t{others}\n")
        if path and not ok:
            f.write(f"{ENTRY[fs]}\t\t\tLINE ENDS: no child leads to {OWNER}\t\t\t\n")
print(f"wrote {out}")
