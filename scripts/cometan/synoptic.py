# Small synoptic tree for Cometan: his Ancestry tree + the FamilySearch exports + the saved Geni pages, merged around
# the paths from him to his relatives who have Wikidata items. Read-only on every source (local files only).
# Matching is structural, never by name alone: Ancestry and FamilySearch are joined from Cometan outward (father to
# father, mother to mother, child to child of an already-joined pair); a Geni profile joins a person only when one of
# its Geni relatives also joins that person's relative.
# Writes reports/cometan/synoptic/cometan-synoptic.ged and research/cometan/synoptic/paths.md.
# Run: python scripts/cometan_synoptic.py
import collections, glob, html, os, re, sqlite3, unicodedata

DL = "targets/brandon-reese-taylor"
OUT = "reports/cometan/synoptic"
ANC_ME, FS_ME = "@I392130812432@", "PJ9Y-N11"
# Wikidata relatives (QID, Ancestry name prefix, Ancestry birth-year text) and the link that ties each to Wikidata.
TARGETS = [
    ("Q5567529", "Leo Baxendale", "Joseph Leo Baxendale", "1930", "tree record links his Wikipedia article; birth day agrees"),
    ("Q121760108", "Martin Baxendale", "Martin G Baxendale", "1952", "son of Leo on Wikidata"),
    ("Q767459", "William Clayton", "William Clayton", "1814", "birth and death days agree"),
    ("Q9002343", "Heber C. Kimball", "Heber Chase Kimball", "1801", "birth and death days agree; FS KWNP-GNM on Wikidata"),
    ("Q4719736", "Alexander Neibaur (father of Harriet)", "Harriet Ellen Neibaur", "1871", "birth and death days agree (Alexander)"),
    ("Q76131226", "Mary Powell (open match)", "Mary Powell", "1724", "medium: husband agrees, dates in the tree broken"),
    ("Q76080129", "Jasper Moon", "Jasper Moon", "1881", "whole immediate family agrees; Geni 6000000108014529960"),
    ("Q7795501", "Sir Thomas de Strickland", "Sir Thomas DeStrickland", "1369", "wife agrees"),
]

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r'["()\[\].,]', " ", s)
    s = re.sub(r"\b(sir|lady|lord|rev|dr|mr|mrs|de|of|the|jr|sr|junior|senior)\b", " ", s)
    return s.split()

def surname_key(w):
    w = w.rstrip("e")
    return w[:5]

def names_ok(a, b):
    """given names share a first word (or one is an initial), and surnames agree on their first letters."""
    A, B = norm(a), norm(b)
    if not A or not B:
        return False
    sa, sb = surname_key(A[-1]), surname_key(B[-1])
    if sa != sb and not (sa[:3] == sb[:3]):
        return False
    ga, gb = A[:-1] or [""], B[:-1] or [""]
    return any(x == y or (len(x) == 1 and y.startswith(x)) or (len(y) == 1 and x.startswith(y))
               for x in ga for y in gb if x and y) or (ga == [""] or gb == [""])

def years_ok(a, b, tol=5):
    # older dates are estimates ("bef. 1610", "abt 1555"): allow 10 years before 1700
    if a and b and min(a, b) < 1700: tol = max(tol, 10)
    return not a or not b or abs(a - b) <= tol

def year(s):
    m = re.search(r"\b(\d{3,4})\b", s or "")
    return int(m.group(1)) if m else None

# ---------- Ancestry ----------
anc = {}  # id -> dict(name, sex, by, dy, bt, dt, fams, famc)
fam = {}
cur = typ = ev = None
for line in open(f"{DL}/Cometan's Family Tree.ged", encoding="utf-8-sig", errors="replace"):
    line = line.rstrip("\n")
    m = re.match(r"0 (@[^@]+@) (INDI|FAM)", line)
    if m:
        cur, typ = m.groups(); ev = None
        (anc if typ == "INDI" else fam)[cur] = ({"name": "", "sex": "", "bt": "", "dt": ""} if typ == "INDI"
                                                 else {"H": None, "W": None, "C": []})
        continue
    if line.startswith("0 "):
        cur = None; continue
    if not cur:
        continue
    if typ == "INDI":
        p = anc[cur]
        if line.startswith("1 NAME") and not p["name"]:
            p["name"] = " ".join(line[7:].replace("/", " ").split())
        elif line.startswith("1 SEX"):
            p["sex"] = line[6:].strip()
        if line.startswith("1 "):
            ev = line[2:6]
        if line.startswith("2 DATE"):
            if ev == "BIRT" and not p["bt"]: p["bt"] = line[7:]
            if ev == "DEAT" and not p["dt"]: p["dt"] = line[7:]
    else:
        m = re.match(r"1 (HUSB|WIFE|CHIL) (@[^@]+@)", line)
        if m:
            k, v = m.groups()
            if k == "CHIL": fam[cur]["C"].append(v)
            else: fam[cur][k[0]] = v
A_par = collections.defaultdict(lambda: {"F": None, "M": None}); A_ch = collections.defaultdict(set)
A_sp = collections.defaultdict(set)
for f in fam.values():
    for c in f["C"]:
        if f["H"]: A_par[c]["F"] = A_par[c]["F"] or f["H"]; A_ch[f["H"]].add(c)
        if f["W"]: A_par[c]["M"] = A_par[c]["M"] or f["W"]; A_ch[f["W"]].add(c)
    if f["H"] and f["W"]:
        A_sp[f["H"]].add(f["W"]); A_sp[f["W"]].add(f["H"])

# ---------- FamilySearch exports (union by FS ID) ----------
fs = {}
F_par = collections.defaultdict(lambda: {"F": None, "M": None}); F_ch = collections.defaultdict(set)
F_sp = collections.defaultdict(set); F_files = collections.defaultdict(set)
for path in sorted(glob.glob(f"{DL}/*.rmtree")):
    base = os.path.basename(path)
    c = sqlite3.connect(f"file:{path}?mode=ro&immutable=1", uri=True)
    ids = dict(c.execute("select rmID, fsID from FamilySearchTable"))
    sex = dict(c.execute("select PersonID, Sex from PersonTable"))
    for oid, g, s, by, dy in c.execute("select OwnerID, Given, Surname, BirthYear, DeathYear from NameTable where IsPrimary=1"):
        f_ = ids.get(oid)
        if not f_: continue
        p = fs.setdefault(f_, {"name": f"{g or ''} {s or ''}".strip(), "by": by or None, "dy": dy or None,
                               "sex": {0: "M", 1: "F"}.get(sex.get(oid), "")})
        p["by"] = p["by"] or by or None; p["dy"] = p["dy"] or dy or None
        F_files[f_].add(base)
    for fid, fa, mo in c.execute("select FamilyID, FatherID, MotherID from FamilyTable"):
        fa, mo = ids.get(fa), ids.get(mo)
        if fa and mo: F_sp[fa].add(mo); F_sp[mo].add(fa)
        for (ch,) in c.execute("select ChildID from ChildTable where FamilyID=?", (fid,)):
            ch = ids.get(ch)
            if not ch: continue
            if fa: F_par[ch]["F"] = F_par[ch]["F"] or fa; F_ch[fa].add(ch)
            if mo: F_par[ch]["M"] = F_par[ch]["M"] or mo; F_ch[mo].add(ch)

# ---------- Geni saved pages ----------
geni = {}   # geni id -> dict(name, by, dy)
G_rel = collections.defaultdict(list)  # geni id -> [(relation, geni id)]
for path in sorted(glob.glob(f"{DL}/Geni - *.html")):
    s = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r'<link rel="canonical" href="https://www\.geni\.com/people/[^/]+/(\d+)"', s) or \
        re.search(r"geni\.com/people/[^/\"]+/(\d{10,})\?through", s)
    title = os.path.basename(path)[len("Geni - "):-len(".html")]
    rows = re.findall(r'<span itemprop="name"[^>]*>\s*(.*?)\s*</span>\s*<span itemprop="birthDate"[^>]*>\s*(.*?)\s*</span>'
                      r'\s*<span itemprop="deathDate"[^>]*>\s*(.*?)\s*</span>.*?data-profile-id="(\d+)".*?'
                      r'<div class="quiet">(.*?)</div>', s, re.S)
    if " is related to " in title or not rows:
        continue
    mid = re.search(r"through=(\d{10,})", s)
    main = re.search(r'data-onclick-bound="openIFSLightbox\(\'(\d+)\'\)', s)
    gid = main.group(1) if main else (mid.group(1) if mid else None)
    tm = re.match(r"(.*?) \((.*?)\)", title)
    yrs = re.findall(r"\d{4}", tm.group(2)) if tm else []
    geni[gid] = {"name": html.unescape(tm.group(1) if tm else title), "by": int(yrs[0]) if yrs else None,
                 "dy": int(yrs[1]) if len(yrs) > 1 else None, "page": os.path.basename(path)}
    for nm, b, d, rid, rel in rows:
        if rid == gid: continue
        geni.setdefault(rid, {"name": html.unescape(nm), "by": year(b.replace("u", "")), "dy": year(d.replace("u", "")),
                              "page": None})
        G_rel[gid].append((rel.strip(), rid))

# ---------- join Ancestry <-> FamilySearch from Cometan outward ----------
a2f, f2a, how = {ANC_ME: FS_ME}, {FS_ME: ANC_ME}, {ANC_ME: "seed (Cometan)"}
def try_join(a, f, why):
    if a in a2f or f in f2a or not a or not f: return False
    pa, pf = anc[a], fs[f]
    if not names_ok(pa["name"], pf["name"]) or not years_ok(year(pa["bt"]), pf["by"], 6):
        return False
    a2f[a], f2a[f], how[a] = f, a, why
    return True
q = collections.deque([ANC_ME])
while q:
    a = q.popleft(); f = a2f[a]
    for role in "FM":
        pa, pf = A_par[a][role], F_par[f][role]
        if try_join(pa, pf, f"{'father' if role == 'F' else 'mother'} of {anc[a]['name']}"): q.append(pa)
    for ca in A_ch[a]:
        for cf in F_ch[f]:
            if try_join(ca, cf, f"child of {anc[a]['name']}"): q.append(ca); break
    for sa in A_sp[a]:
        for sf in F_sp[f]:
            if try_join(sa, sf, f"spouse of {anc[a]['name']}"): q.append(sa); break

# ---------- join Geni profiles to joined people (needs a relative to agree) ----------
REL = {"father": "F", "mother": "M", "son": "C", "daughter": "C", "husband": "S", "wife": "S"}
a2g, g_how = {}, {}
def a_rel(a, k):
    if k in "FM": return {A_par[a][k]} - {None}
    if k == "C": return A_ch[a]
    return A_sp[a]
for gid, g in geni.items():
    if not g.get("page"): continue
    for a, p in anc.items():
        if a in a2g or not names_ok(p["name"], g["name"]) or not years_ok(year(p["bt"]), g["by"], 3): continue
        agree = [(rel, rid) for rel, rid in G_rel[gid] if REL.get(rel) and any(
            names_ok(anc[x]["name"], geni[rid]["name"]) and years_ok(year(anc[x]["bt"]), geni[rid]["by"], 5)
            for x in a_rel(a, REL[rel]))]
        if agree:
            a2g[a] = gid; g_how[a] = f"Geni page {g['page']}; agrees on " + ", ".join(f"{r} {geni[i]['name']}" for r, i in agree)
            for rel, rid in agree:  # the agreeing relatives get their Geni IDs too
                for x in a_rel(a, REL[rel]):
                    if x not in a2g and names_ok(anc[x]["name"], geni[rid]["name"]):
                        a2g[x] = rid; g_how[x] = f"listed as {rel} on Geni page {g['page']}"
            break
# Geni IDs Emma matched by hand (identifications.md, the Moon male line), attached only where the FS ID agrees.
HAND = {"LDY2-VHZ": "6000000144077151851", "94WX-XF2": "6000000144075705834", "LZYQ-7HR": "6000000188561986824",
        "L63B-TX2": "6000000006150455340", "L7YT-3LC": "6000000025156748366"}
for f_, gid in HAND.items():
    if f_ in f2a and f2a[f_] not in a2g:
        a2g[f2a[f_]] = gid; g_how[f2a[f_]] = "identifications.md (Emma), via the FS ID"

# ---------- paths ----------
def find(prefix, y):
    c = [i for i, p in anc.items() if p["name"].startswith(prefix) and y in p["bt"]]
    return c[0] if c else None
def anc_up(x):
    d = {x: 0}; q = [x]
    while q:
        y = q.pop()
        for p in A_par[y].values():
            if p and (p not in d or d[p] > d[y] + 1): d[p] = d[y] + 1; q.append(p)
    return d
mine = anc_up(ANC_ME)
def chain_down(a, t):
    prev = {a: None}; q = collections.deque([a])
    while q:
        x = q.popleft()
        if x == t: break
        for c in A_ch[x]:
            if c not in prev: prev[c] = x; q.append(c)
    if t not in prev: return None
    p, x = [], t
    while x: p.append(x); x = prev[x]
    return p[::-1]
def path_to(t):
    best = None
    for via in [t] + sorted(A_sp[t]):
        up = anc_up(via)
        for a in up:
            if a in mine:
                k = (mine[a] + up[a], a, via)
                if best is None or k < best: best = k
    if not best: return None
    _, top, via = best
    left = chain_down(top, ANC_ME)[::-1]          # Cometan ... top
    right = chain_down(top, via)[1:]               # below top ... via
    return left + right + ([t] if via != t else [])

def edge_src(x, y):
    """how the step x-y is supported: FS when FamilySearch links the two joined people the same way."""
    s = ["Ancestry"]
    fx, fy = a2f.get(x), a2f.get(y)
    if fx and fy and (fy in F_ch[fx] or fx in F_ch[fy] or fy in F_sp[fx]): s.append("FamilySearch")
    gx, gy = a2g.get(x), a2g.get(y)
    if gx and gy and any(r == gy for _, r in G_rel.get(gx, [])) or gx and gy and any(r == gx for _, r in G_rel.get(gy, [])):
        s.append("Geni")
    return s

def label(i):
    p = anc[i]
    yrs = "-".join(v for v in (str(year(p["bt"]) or ""), str(year(p["dt"]) or "")) if v) or "?"
    return f"{p['name']} ({yrs})"

os.makedirs(OUT, exist_ok=True)
keep, md = set(), []
md.append("# Cometan: small synoptic tree, paths to relatives on Wikidata\n")
md.append("Built by `scripts/cometan_synoptic.py` from local files only: his Ancestry tree "
          "(`targets/brandon-reese-taylor/Cometan's Family Tree.ged`), the five FamilySearch exports (`*.rmtree`), and the saved Geni "
          "pages (`Geni - *.html`). Ancestry and FamilySearch people are joined structurally from Cometan (PJ9Y-N11) outward; "
          "a Geni profile joins only where one of its Geni relatives also joins. The tree is "
          "`reports/cometan/synoptic/cometan-synoptic.ged`.\n")
md.append(f"Joined: {len(a2f)} Ancestry people to FamilySearch; {len(a2g)} to Geni.\n")
md.append("Each step says which sources link the two people: **FS** = FamilySearch links them (both are joined and "
          "parent/child or spouse there), **Geni** = a saved Geni page links them, otherwise Ancestry only.\n")
summary = []
for qid, label_, pre, y, why in TARGETS:
    t = find(pre, y)
    if not t:
        md.append(f"\n## {label_} ({qid})\n\nNot found in the Ancestry tree.\n"); continue
    p = path_to(t)
    if not p:
        md.append(f"\n## {label_} ({qid})\n\nNo path from Cometan in the Ancestry tree.\n"); continue
    keep |= set(p)
    md.append(f"\n## {label_} ({qid})\n\nWikidata link: {why}.\n")
    md.append("| # | Person | FamilySearch | Geni | Step from the line above |")
    md.append("|---|---|---|---|---|")
    weak = 0
    for k, i in enumerate(p):
        step = "" if k == 0 else " + ".join(edge_src(p[k - 1], i))
        if k and step == "Ancestry": weak += 1
        md.append(f"| {k} | {label(i)} | {a2f.get(i, '')} | {a2g.get(i, '')} | {step} |")
    summary.append((label_, qid, len(p) - 1, weak))
md.insert(4, "\n## Summary\n\n| Relative | Wikidata | Steps | Steps on Ancestry only |\n|---|---|---|---|\n" +
          "\n".join(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in summary) + "\n")

# GEDCOM of the path people, with every source ID
xid = {i: f"@P{n}@" for n, i in enumerate(sorted(keep), 1)}
g = ["0 HEAD", "1 SOUR cometan_synoptic.py", "1 GEDC", "2 VERS 5.5.1", "1 CHAR UTF-8"]
for i in sorted(keep):
    p = anc[i]
    g += [f"0 {xid[i]} INDI", f"1 NAME {p['name']}"]
    if p["sex"]: g.append(f"1 SEX {p['sex']}")
    if p["bt"]: g += ["1 BIRT", f"2 DATE {p['bt']}"]
    if p["dt"]: g += ["1 DEAT", f"2 DATE {p['dt']}"]
    g.append(f"1 REFN {i}"); g.append("2 TYPE Ancestry")
    if i in a2f: g += [f"1 _FSFTID {a2f[i]}", f"2 NOTE joined: {how[i]}"]
    if i in a2g: g += [f"1 _GENI {a2g[i]}", f"2 NOTE {g_how[i]}"]
fams = {}
for i in keep:
    for role in "FM":
        par = A_par[i][role]
        if par in keep:
            key = (A_par[i]["F"] if A_par[i]["F"] in keep else None, A_par[i]["M"] if A_par[i]["M"] in keep else None)
            fams.setdefault(key, set()).add(i)
for i in keep:
    for s_ in A_sp[i]:
        if s_ in keep:
            key = (i, s_) if anc[i]["sex"] == "M" else (s_, i)
            fams.setdefault(key, set())
for n, ((h, w), kids) in enumerate(sorted(fams.items(), key=str), 1):
    g.append(f"0 @F{n}@ FAM")
    if h: g.append(f"1 HUSB {xid[h]}")
    if w: g.append(f"1 WIFE {xid[w]}")
    g += [f"1 CHIL {xid[c]}" for c in sorted(kids)]
g.append("0 TRLR")
open(f"{OUT}/cometan-synoptic.ged", "w", encoding="utf-8", newline="\n").write("\n".join(g) + "\n")
open(f"{OUT}/paths.md", "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")
print(f"joined FS {len(a2f)}, Geni {len(a2g)}; {len(keep)} people on the paths")
for s in summary: print(s)
