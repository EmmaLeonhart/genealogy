"""Read Emma's RootsMagic hourglass of Abul Hamza (FamilySearch `GRWG-G82`), read-only, from the archived copy.

Queue item (Emma, 2026-10-08): who `GRWG-G82` is, where he sits in the FamilySearch tree, and above all whether any
of his descendants are in Scandinavia. The live file is never opened: the archive copy is read with
`mode=ro&immutable=1`.

    python scripts/abul-hamza-hourglass.py [rmtree]
        -> reports/abul-hamza-hourglass.md               the person, his family, the counts by generation
        -> reports/abul-hamza-scandinavian-descendants.tsv  descendants born or dying in Scandinavia (before 1900)
"""
import collections
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RM = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"C:\Users\Emma\Documents\rootsmagic-archive\2026-10-19\test.abu-hamza-hourglass.rmtree")
SEED = "GRWG-G82"
NORDIC = re.compile(r"Sweden|Sverige|Norway|Norge|Denmark|Danmark|Finland|Suomi|Iceland|Ísland|Suède|Norvège|"
                    r"Schweden|Norwegen|Dänemark|Faroe|Færøerne", re.I)

db = sqlite3.connect(f"file:{RM.as_posix()}?mode=ro&immutable=1", uri=True)
db.create_collation("RMNOCASE", lambda a, b: (a.lower() > b.lower()) - (a.lower() < b.lower()))

name = {pid: f"{(g or '').strip()} {(s or '').strip()}".strip()
        for pid, g, s in db.execute("SELECT OwnerID, Given, Surname FROM NameTable WHERE IsPrimary=1")}
sex = dict(db.execute("SELECT PersonID, Sex FROM PersonTable"))
fs = {rm: f for rm, f in db.execute("SELECT rmID, fsID FROM FamilySearchTable WHERE LinkType=0")}
place = dict(db.execute("SELECT PlaceID, Name FROM PlaceTable"))
ev = collections.defaultdict(dict)
for owner, etype, date, pl in db.execute(
        "SELECT OwnerID, EventType, Date, PlaceID FROM EventTable WHERE OwnerType=0 AND EventType IN (1,2)"):
    y = re.search(r"\d{3,4}", (date or "")[3:] if date else "")
    ev[owner]["b" if etype == 1 else "d"] = ((y.group() if y else ""), place.get(pl, "") or "")
fam = {fid: (f, m) for fid, f, m in db.execute("SELECT FamilyID, FatherID, MotherID FROM FamilyTable")}
kids = collections.defaultdict(list)
parents_of = collections.defaultdict(list)
for child, fid in db.execute("SELECT ChildID, FamilyID FROM ChildTable"):
    f, m = fam.get(fid, (0, 0))
    for p in (f, m):
        if p:
            kids[p].append(child)
            parents_of[child].append(p)
spouses = collections.defaultdict(set)
for f, m in fam.values():
    if f and m:
        spouses[f].add(m)
        spouses[m].add(f)

def who(p):
    b, d = ev[p].get("b", ("", "")), ev[p].get("d", ("", ""))
    return (f"{name.get(p, '?')} [{fs.get(p, '-')}] {'MFU'[sex.get(p, 2)] if sex.get(p, 2) in (0, 1, 2) else '?'} "
            f"b. {b[0] or '?'} {b[1]} / d. {d[0] or '?'} {d[1]}").strip()

seed = next(p for p, f in fs.items() if f == SEED)
gens_down, gen, seen = [], [seed], {seed}
while gen:
    gens_down.append(gen)
    gen = [c for p in gen for c in kids[p] if c not in seen and not seen.add(c)]
gens_up, gen, seen_up = [], [seed], {seed}
while gen:
    gens_up.append(gen)
    gen = [p for c in gen for p in parents_of[c] if p not in seen_up and not seen_up.add(p)]

nordic = []
for g, people in enumerate(gens_down[1:], 1):
    for p in people:
        b, d = ev[p].get("b", ("", "")), ev[p].get("d", ("", ""))
        if (NORDIC.search(b[1]) or NORDIC.search(d[1])) and b[0] and int(b[0]) < 1900:
            nordic.append((g, p))

out = ROOT / "reports" / "abul-hamza-hourglass.md"
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(f"# Abul Hamza in the RootsMagic hourglass (`{SEED}`)\n\nRead {RM.name}: {len(name):,} people.\n\n")
    f.write(f"**The person:** {who(seed)}\n\n")
    for label, group in (("Parents", parents_of[seed]), ("Spouses", sorted(spouses[seed])), ("Children", kids[seed])):
        f.write(f"**{label}:**\n\n" + "".join(f"- {who(p)}\n" for p in group) + "\n")
    f.write("## Generations\n\n| generation | above | below |\n| ---: | ---: | ---: |\n")
    for i in range(1, max(len(gens_up), len(gens_down))):
        f.write(f"| {i} | {len(gens_up[i]) if i < len(gens_up) else ''} | "
                f"{len(gens_down[i]) if i < len(gens_down) else ''} |\n")
    f.write(f"\n## Descendants born or dying in Scandinavia, born before 1900: {len(nordic):,}\n\n"
            "`reports/abul-hamza-scandinavian-descendants.tsv` has every one.\n")
with open(ROOT / "reports" / "abul-hamza-scandinavian-descendants.tsv", "w", encoding="utf-8", newline="\n") as f:
    f.write("generation\tfs_id\tname\tbirth_year\tbirth_place\tdeath_year\tdeath_place\n")
    for g, p in nordic:
        b, d = ev[p].get("b", ("", "")), ev[p].get("d", ("", ""))
        f.write(f"{g}\t{fs.get(p, '')}\t{name.get(p, '')}\t{b[0]}\t{b[1]}\t{d[0]}\t{d[1]}\n")
print(out.read_text(encoding="utf-8")[:6000])
