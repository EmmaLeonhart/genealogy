"""Who is in Hethel Pedigree.ged and NOT in the synoptic tree.

⛔ **MATCHED ON STRUCTURE, NOT ON A STRING.** Hethel carries MyHeritage `RIN`/`_UID` and no Geni
ids, so there is no exact key -- and matching on the name alone was shown to be useless: it called
Richard Borsheim himself missing, and it could not separate `Peder Paulson` from `peder paulsen`
nor `Anders Rasmusson Bore` from a different `Anders Rasmusson Horpestad`. In Rogaland naming the
farm is the discriminator and Hethel records it inconsistently.

So a Hethel person counts as PRESENT only when some synoptic person shares

    at least 2 distinctive name tokens          -- the person themselves
    AND at least 1 token with a parent or child -- the edge around them

which is the zipper's own principle: a matched parent-child pair is far stronger evidence than a
matched string. A lone name agreement is not enough and is reported separately as `name only`, so
the two kinds of evidence never get added together.
"""
import re, csv, json, collections, unicodedata, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HETHEL = ROOT / "preservation" / "genealogy" / "dropbox" / "Hethel Pedigree.ged"
SEP = " | "

def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()

STOP = {"the", "von", "van", "king", "queen", "duke", "lord", "earl", "jarl", "saint",
        "count", "prince", "baron", "graf", "herr", "datter", "dotter", "sson", "unknown"}
def toks(s):
    return {t for t in norm(s).split() if len(t) > 3 and t not in STOP}

# ---------------------------------------------------------------- Hethel
name, child_of, fam = {}, collections.defaultdict(list), collections.defaultdict(
    lambda: {"P": [], "C": []})
cur = curfam = mode = None
for line in HETHEL.open(encoding="utf-8-sig", errors="replace"):
    line = line.rstrip("\n")
    m = re.match(r"^0 (@[^@]+@) (INDI|FAM)\s*$", line)
    if m:
        mode = m.group(2); cur = m.group(1)
        if mode == "FAM": curfam = cur
        continue
    if mode == "INDI":
        if line.startswith("1 NAME ") and cur not in name:
            name[cur] = re.sub(r"\s+", " ", line[7:].replace("/", " ")).strip()
        mm = re.match(r"^1 FAMC (@[^@]+@)", line)
        if mm: child_of[cur].append(mm.group(1))
    elif mode == "FAM":
        mm = re.match(r"^1 (HUSB|WIFE|CHIL) (@[^@]+@)", line)
        if mm:
            fam[curfam]["P" if mm.group(1) in ("HUSB", "WIFE") else "C"].append(mm.group(2))

FILLER = re.compile(r"generations|Kroll|arbitrary|Audumbla|Hethelo", re.I)
kin = collections.defaultdict(set)          # person -> names of parents and children
for f, d in fam.items():
    for c in d["C"]:
        for p in d["P"]:
            kin[c].add(name.get(p, "")); kin[p].add(name.get(c, ""))
print("hethel people: %d" % len(name), flush=True)

# ---------------------------------------------------------------- synoptic tree
lab = {}
with (ROOT / "reports" / "derived-labels.csv").open(encoding="utf-8", newline="") as fh:
    for row in csv.DictReader(fh):
        g = (row.get("geni_id") or "").strip()
        v = (row.get("label_en") or row.get("label_mul") or "").strip()
        if g and v: lab[g] = v
print("synoptic labelled people: %d" % len(lab), flush=True)

index = collections.defaultdict(list)       # token -> [geni_id]
for g, v in lab.items():
    for t in toks(v):
        if len(index[t]) < 4000: index[t].append(g)

gkin = collections.defaultdict(set)
csv.field_size_limit(1 << 30)
with (ROOT / "reports" / "derived-family.csv").open(encoding="utf-8", newline="") as fh:
    for row in csv.DictReader(fh):
        me = (row.get("geni_id") or "").strip()
        if me not in lab: continue
        rel = set()
        for col in ("father", "mother", "fathers", "mothers", "children"):
            raw = (row.get(col) or "").strip()
            if raw:
                for pid in raw.split(SEP):
                    pl = lab.get(pid.strip())
                    if pl: rel |= toks(pl)
        if rel: gkin[me] = rel
print("synoptic people with kin tokens: %d" % len(gkin), flush=True)

# ---------------------------------------------------------------- compare
absent, name_only, present = [], [], 0
for x, nm in name.items():
    if not nm or FILLER.search(nm): continue
    mt = toks(nm)
    if len(mt) < 2:
        continue                             # too thin to decide either way
    cand = collections.Counter()
    for t in mt:
        for g in index.get(t, ()): cand[g] += 1
    hits = [g for g, k in cand.items() if k >= 2]
    if not hits:
        absent.append(nm); continue
    kt = set()
    for r in kin.get(x, ()):
        kt |= toks(r)
    if not kt:
        name_only.append(nm); continue
    if any(gkin.get(g, set()) & kt for g in hits):
        present += 1
    else:
        name_only.append(nm)

print("\nstructurally PRESENT (name + an edge): %d" % present)
print("name agrees but no edge agrees      : %d" % len(name_only))
print("ABSENT, no name match at all        : %d" % len(absent))
pathlib.Path(ROOT / "preservation" / "hethel-absent.json").write_text(
    json.dumps({"absent": sorted(absent), "name_only": sorted(name_only),
                "present": present}, ensure_ascii=False), encoding="utf-8")
print("\n--- sample ABSENT ---")
for n in absent[:25]: print("   %s" % n[:72])
