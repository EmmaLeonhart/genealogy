"""Ahnentafel slot occupancy: Hethel against the synoptic tree. No name comparison anywhere.

⛔ **NAMES DECIDE NOTHING HERE.** Every earlier attempt compared strings, and in Rogaland that
cannot work: the farm is the discriminator, Hethel records it inconsistently, and `Peder Paulson`
versus `peder paulsen` is the same man. A string test flagged Richard Borsheim himself as absent.

So this asks one question per ahnentafel position:

    is there ANYBODY at slot N in Hethel, and is there ANYBODY at slot N in the synoptic tree?

Position 1 is Richard, a father is 2n, a mother is 2n+1. The two trees are anchored at position 1
by hand -- Hethel `Richard Borsheim`, Geni `6000000177921459056` Richard Wade Borsheim -- and
after that nothing is matched by name. Names appear in the output only as labels for a slot that
has already been decided by occupancy.

A slot filled in Hethel and empty in Geni is a real gap whatever anyone is called.
"""
import re, csv, json, collections, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
HETHEL = ROOT / "preservation" / "genealogy" / "dropbox" / "Hethel Pedigree.ged"
GENI_ROOT = "6000000177921459056"          # Richard Wade Borsheim
SEP = " | "
MAXGEN = 20

# ---------------------------------------------------------------- Hethel ahnentafel
name = {}
child_of = collections.defaultdict(list)
fam = collections.defaultdict(lambda: {"H": None, "W": None})
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
        mm = re.match(r"^1 (HUSB|WIFE) (@[^@]+@)", line)
        if mm: fam[curfam]["H" if mm.group(1) == "HUSB" else "W"] = mm.group(2)

FILLER = re.compile(r"generations|Kroll|arbitrary|Audumbla|Hethelo", re.I)
hroot = [k for k, v in name.items() if v.strip().lower() == "richard borsheim"][0]
hethel = {1: hroot}
q = collections.deque([1])
while q:
    n = q.popleft()
    if n.bit_length() > MAXGEN: continue
    for f in child_of.get(hethel[n], ()):
        for slot, who in ((2 * n, fam[f]["H"]), (2 * n + 1, fam[f]["W"])):
            if who and slot not in hethel and name.get(who) and not FILLER.search(name[who]):
                hethel[slot] = who; q.append(slot)

# ---------------------------------------------------------------- synoptic ahnentafel
father, mother, lab = {}, {}, {}
csv.field_size_limit(1 << 30)
with (ROOT / "reports" / "derived-family.csv").open(encoding="utf-8", newline="") as fh:
    for row in csv.DictReader(fh):
        g = (row.get("geni_id") or "").strip()
        if not g: continue
        f = (row.get("father") or "").strip()
        m = (row.get("mother") or "").strip()
        if not f:
            fs = (row.get("fathers") or "").strip()
            f = fs.split(SEP)[0].strip() if fs else ""
        if not m:
            ms = (row.get("mothers") or "").strip()
            m = ms.split(SEP)[0].strip() if ms else ""
        if f: father[g] = f
        if m: mother[g] = m
with (ROOT / "reports" / "derived-labels.csv").open(encoding="utf-8", newline="") as fh:
    for row in csv.DictReader(fh):
        g = (row.get("geni_id") or "").strip()
        v = (row.get("label_en") or row.get("label_mul") or "").strip()
        if g and v: lab[g] = v

geni = {1: GENI_ROOT}
q = collections.deque([1])
while q:
    n = q.popleft()
    if n.bit_length() > MAXGEN: continue
    g = geni[n]
    for slot, who in ((2 * n, father.get(g)), (2 * n + 1, mother.get(g))):
        if who and slot not in geni:
            geni[slot] = who; q.append(slot)

# ---------------------------------------------------------------- compare by slot
rows, gaps = [], []
for gen in range(0, MAXGEN + 1):
    lo, hi = 2 ** gen, 2 ** (gen + 1)
    h = [n for n in range(lo, hi) if n in hethel]
    gg = [n for n in range(lo, hi) if n in geni]
    both = [n for n in h if n in geni]
    only_h = [n for n in h if n not in geni]
    only_g = [n for n in gg if n not in hethel]
    if not h and not gg: break
    rows.append({"gen": gen, "slots": hi - lo, "hethel": len(h), "geni": len(gg),
                 "both": len(both), "only_hethel": len(only_h), "only_geni": len(only_g)})
    for n in only_h:
        gaps.append({"n": n, "gen": gen, "hethel": name.get(hethel[n], ""),
                     "child_slot": n // 2,
                     "child_geni": lab.get(geni.get(n // 2), ""),
                     "child_geni_id": geni.get(n // 2, "")})

print("%-4s %8s %8s %8s %8s %10s %9s" % ("gen", "slots", "hethel", "geni", "both",
                                          "only hethel", "only geni"))
for r in rows:
    print("%-4d %8d %8d %8d %8d %10d %9d" % (r["gen"], r["slots"], r["hethel"], r["geni"],
                                             r["both"], r["only_hethel"], r["only_geni"]))
print("\nslots Hethel fills that the synoptic tree does not: %d" % len(gaps))
print("of those, the CHILD slot is occupied in Geni (so there is a profile to add from): %d"
      % sum(1 for g in gaps if g["child_geni_id"]))
pathlib.Path(ROOT / "preservation" / "slot-gaps.json").write_text(
    json.dumps({"rows": rows, "gaps": gaps}, ensure_ascii=False), encoding="utf-8")
print("\n--- the shallow ones ---")
for g in gaps[:30]:
    print("  ahn %-6d gen %-3d %-40s   add to: %s"
          % (g["n"], g["gen"], g["hethel"][:40], g["child_geni"][:34] or "(child not in Geni)"))
