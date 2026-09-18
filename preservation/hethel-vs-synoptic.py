"""The Hethel pedigree's ancestry that the synoptic tree does not have, per person.

⛔ **THE OUTPUT IS AN IDENTIFICATION DECISION, NOT A LIST OF NAMES.** Rebuilt 2026-09-18 on
instruction: *"Here is the person in the synoptic tree and their geni link, here is the person
from the hethel pedigree, here is the parent(s) of that person in the hethel pedigree that are
absent in the synoptic tree ... Your only providing the geni link and saying 'add them here' was
insufficient since I need to even know if the figure in the hethel pedigree is the same person."*

So a row is a JOIN and it carries both sides in full -- name, years, places, spouse and children
on the Hethel side; label, Geni link and the alternates on the synoptic side; and what the match
was made on. Nothing here asserts an identification. It hands over what is needed to make one.

⛔ **AND THE POINT IS THE LINE, NOT THE PERSON.** *"entire lines only in the hethel pedigree are
things I want"*, and *"people whose parents are entirely absent are often more important"*. Each
gap carries `new_ancestors` -- how many real Hethel people hang above that missing parent and are
absent from the synoptic tree -- and both-parents-missing sorts first. A missing parent with 400
ancestors behind them is a branch; one with two is a correction.

⛔ **MATCHED ON STRUCTURE, NOT ON A STRING.** Hethel carries MyHeritage `RIN`/`_UID` and no Geni
ids, so there is no exact key, and `CLAUDE.md` § *Merging is an exact join, never fuzzy name
matching* is why this writes a report and merges nothing. Matching on the name alone was shown to
be useless: it called Richard Borsheim himself missing, and it could not separate `Peder Paulson`
from `peder paulsen` nor `Anders Rasmusson Bore` from `Anders Rasmusson Horpestad`. In Rogaland
naming the farm is the discriminator and Hethel records it inconsistently.

A Hethel person counts as PRESENT when some synoptic person shares

    at least 2 distinctive name tokens          -- the person themselves
    AND at least 1 token with a parent or child -- the edge around them

which is the zipper's own principle: a matched parent-child pair is far stronger evidence than a
matched string. **OR** when one token agrees and the BIRTH YEAR agrees within two, which is
`CLAUDE.md` § *solo, then date, then name* -- *1600-1900 is the band where names lie and years
decide*.

⛔ **THE YEAR TEST IS NOT AN OPTIMISATION, IT IS WHAT MAKES THE OUTPUT READABLE.** Without it the
first run of this rebuild opened with `Felipe VI King of Spain`, `Beatrix of the Netherlands` and
`Edward Earl of Wessex` as ancestry the synoptic tree lacks, each carrying a claimed ~4,990 new
people. They are all in the tree. Two distinctive tokens is a high bar for a royal, because the
two trees write the same monarch differently -- `Felipe VI King of Spain` against
`Felipe VI de Borbon y Grecia` shares exactly one -- so the whole of European royalty came back
absent and sorted itself to the top by dragging its own ancestry along as `new_ancestors`. A
report whose first screen is false is the complaint this rebuild is answering.

⛔ **A THIN NAME IS `thin`, NOT ABSENT, AND THE LAST VERSION DROPPED IT.** `len(tokens) < 2` used
to `continue`, so every one-token person vanished from the output -- which is how somebody whose
parents are entirely absent became unreachable rather than prominent. They are emitted now,
because "we cannot tell" and "not there" are different answers and only one of them is work.

⛔ **FILLER NODES ARE NOT ANCESTRY.** `Hethelo`, `A few generations`, `Several generations Diaz`,
`Sophia II -- 2000th Kroll`, `Audumbla I` at `1345294336 BC`. Ruled 2026-09-17: *"Hethelo is not a
real person."* They are excluded from every count and never proposed as a parent to add.
"""
import collections
import csv
import html
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
HETHEL = ROOT / "preservation" / "genealogy" / "dropbox" / "Hethel Pedigree.ged"
OUT_CSV = ROOT / "preservation" / "hethel-gaps.csv"
OUT_HTML = ROOT / "preservation" / "hethel-gaps.html"
OUT_JSON = ROOT / "preservation" / "hethel-absent.json"
SEP = " | "
csv.field_size_limit(1 << 30)
sys.setrecursionlimit(100000)


def norm(s):
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


STOP = {"the", "von", "van", "king", "queen", "duke", "lord", "earl", "jarl", "saint",
        "count", "prince", "baron", "graf", "herr", "datter", "dotter", "sson", "unknown"}


def toks(s):
    return {t for t in norm(s).split() if len(t) > 3 and t not in STOP}


FILLER = re.compile(r"generations|Kroll|arbitrary|Audumbla|Hethelo", re.I)

# ------------------------------------------------------------------ Hethel
name, birth, death, bplace, dplace, sex = {}, {}, {}, {}, {}, {}
child_of = collections.defaultdict(list)
fam = collections.defaultdict(lambda: {"P": [], "C": []})

cur = curfam = mode = None
event = None
for raw in HETHEL.open(encoding="utf-8-sig", errors="replace"):
    line = raw.rstrip("\n")
    m = re.match(r"^0 (@[^@]+@) (INDI|FAM)\s*$", line)
    if m:
        mode, cur, event = m.group(2), m.group(1), None
        if mode == "FAM":
            curfam = cur
        continue
    if line.startswith("0 "):
        mode = event = None
        continue
    if mode == "INDI":
        if line.startswith("1 "):
            event = None
            tag = line[2:6]
            if line.startswith("1 NAME ") and cur not in name:
                name[cur] = re.sub(r"\s+", " ", line[7:].replace("/", " ")).strip()
            elif line.startswith("1 SEX "):
                sex[cur] = line[6:].strip()
            elif tag in ("BIRT", "BAPM", "CHR "):
                event = "B"
            elif tag in ("DEAT", "BURI"):
                event = "D"
            else:
                mm = re.match(r"^1 FAMC (@[^@]+@)", line)
                if mm:
                    child_of[cur].append(mm.group(1))
        elif event and line.startswith("2 DATE "):
            (birth if event == "B" else death).setdefault(cur, line[7:].strip())
        elif event and line.startswith("2 PLAC "):
            (bplace if event == "B" else dplace).setdefault(cur, line[7:].strip())
    elif mode == "FAM":
        mm = re.match(r"^1 (HUSB|WIFE|CHIL) (@[^@]+@)", line)
        if mm:
            fam[curfam]["P" if mm.group(1) in ("HUSB", "WIFE") else "C"].append(mm.group(2))

kin = collections.defaultdict(set)
parents_of = collections.defaultdict(list)
children_of = collections.defaultdict(list)
partners_of = collections.defaultdict(list)
for f, d in fam.items():
    for c in d["C"]:
        for p in d["P"]:
            kin[c].add(p)
            kin[p].add(c)
            parents_of[c].append(p)
            children_of[p].append(c)
    if len(d["P"]) > 1:
        for a in d["P"]:
            for b in d["P"]:
                if a != b:
                    partners_of[a].append(b)


def real(x):
    """A Hethel xref that names somebody rather than spanning a gap."""
    n = name.get(x, "")
    return bool(n) and not FILLER.search(n)


print("hethel people: %d, of which filler: %d"
      % (len(name), sum(1 for x in name if not real(x))), flush=True)

# ------------------------------------------------------------------ synoptic tree
lab = {}
with (ROOT / "reports" / "derived-labels.csv").open(encoding="utf-8", newline="") as fh:
    for row in csv.DictReader(fh):
        g = (row.get("geni_id") or "").strip()
        v = (row.get("label_en") or row.get("label_mul") or "").strip()
        if g and v:
            lab[g] = v
print("synoptic labelled people: %d" % len(lab), flush=True)

index = collections.defaultdict(list)
for g, v in lab.items():
    for t in toks(v):
        if len(index[t]) < 4000:
            index[t].append(g)

gkin = {}
with (ROOT / "reports" / "derived-family.csv").open(encoding="utf-8", newline="") as fh:
    for row in csv.DictReader(fh):
        me = (row.get("geni_id") or "").strip()
        if me not in lab:
            continue
        rel = set()
        for col in ("father", "mother", "fathers", "mothers", "children"):
            raw = (row.get(col) or "").strip()
            if raw:
                for pid in raw.split(SEP):
                    pl = lab.get(pid.strip())
                    if pl:
                        rel |= toks(pl)
        if rel:
            gkin[me] = rel
print("synoptic people with kin tokens: %d" % len(gkin), flush=True)

gyear = {}
with (ROOT / "reports" / "derived-facts.csv").open(encoding="utf-8", newline="") as fh:
    for row in csv.DictReader(fh):
        g = (row.get("geni_id") or "").strip()
        y = (row.get("birth_date_year") or "").strip()
        if g in lab and y.lstrip("-").isdigit():
            gyear[g] = int(y)
print("synoptic people with a birth year: %d" % len(gyear), flush=True)

YEAR = re.compile(r"\b(\d{3,4})\b")


def hethel_year(x):
    """The birth year Hethel records, or None. `1345294336 BC` is not a year."""
    raw = birth.get(x, "")
    if not raw or "BC" in raw.upper():
        return None
    m = YEAR.search(raw)
    return int(m.group(1)) if m else None


# ------------------------------------------------------------------ the match
verdict = {}
for x, nm in name.items():
    if not real(x):
        continue
    mt = toks(nm)
    hy = hethel_year(x)
    cand = collections.Counter()
    for t in mt:
        for g in index.get(t, ()):
            cand[g] += 1
    # the year test: ONE token agreeing plus a birth year within two
    dated = [g for g in cand if hy is not None and g in gyear and abs(gyear[g] - hy) <= 2]
    if dated:
        verdict[x] = ("date", dated[:4])
        continue
    if len(mt) < 2:
        verdict[x] = ("thin", [])
        continue
    hits = [g for g, k in cand.items() if k >= 2]
    if not hits:
        verdict[x] = ("absent", [])
        continue
    kt = set()
    for r in kin.get(x, ()):
        kt |= toks(name.get(r, ""))
    strong = [g for g in hits if gkin.get(g, set()) & kt] if kt else []
    verdict[x] = ("structural", strong[:4]) if strong else ("name", hits[:4])

counts = collections.Counter(v[0] for v in verdict.values())
print("verdicts: %s" % dict(counts), flush=True)

# ------------------------------------------------------------------ what hangs above a gap
_above = {}


def ancestors_above(start):
    """Every real Hethel person at or above `start`, parents only, iteratively."""
    if start in _above:
        return _above[start]
    seen, stack = set(), [start]
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        stack.extend(parents_of.get(x, ()))
    out = {x for x in seen if real(x)}
    _above[start] = out
    return out


# ------------------------------------------------------------------ whose ancestry it is
# ⛔ **"MY OWN ANCESTRY" IS A DIFFERENT QUESTION FROM "THE SYNOPTIC TREE", AND BOTH WERE ASKED.**
# *"I am not sure if there are any lines that are present in hethel pedigree but not in my own
# ancestry."* So every gap is additionally flagged by whether the person it hangs off is an
# ancestor of Eric Borsheim as HETHEL records the descent, and that flag sorts first. A gap on
# somebody else's branch of European royalty is still a gap; it is not the thing being asked
# about.
SUBJECT = "eric borsheim"
subject = max((x for x in name if norm(name[x]) == SUBJECT),
              key=lambda x: len(parents_of.get(x, ())), default=None)
your_line = ancestors_above(subject) if subject else set()
print("subject %s -- %d ancestors in Hethel" % (subject, len(your_line)), flush=True)

# ------------------------------------------------------------------ the gaps
rows = []
for x, (conf, hits) in verdict.items():
    if conf not in ("structural", "name", "date"):
        continue                                   # an anchor has to be somewhere to anchor to
    ps = [p for p in parents_of.get(x, ()) if real(p)]
    if not ps:
        continue
    gaps = [p for p in ps if verdict.get(p, ("absent", []))[0] in ("absent", "thin")]
    if not gaps:
        continue
    both = len(gaps) == len(ps) and len(ps) > 1
    for p in gaps:
        new = {a for a in ancestors_above(p)
               if verdict.get(a, ("absent", []))[0] in ("absent", "thin")}
        rows.append({
            "on_your_line": "yes" if x in your_line else "no",
            "both_parents_missing": "yes" if both else "no",
            "new_ancestors": len(new),
            "confidence": conf,
            "synoptic_geni_id": hits[0] if hits else "",
            "synoptic_label": lab.get(hits[0], "") if hits else "",
            "geni_url": ("https://www.geni.com/people/x/%s" % hits[0]) if hits else "",
            "synoptic_alternates": SEP.join(
                "%s %s" % (g, lab.get(g, "")) for g in hits[1:4]),
            "hethel_xref": x,
            "hethel_name": name.get(x, ""),
            "hethel_born": birth.get(x, ""),
            "hethel_birth_place": bplace.get(x, ""),
            "hethel_died": death.get(x, ""),
            "hethel_death_place": dplace.get(x, ""),
            "hethel_spouse": SEP.join(
                name.get(s, "") for s in partners_of.get(x, ())[:3] if real(s)),
            "hethel_children": SEP.join(
                name.get(c, "") for c in children_of.get(x, ())[:6] if real(c)),
            "missing_parent_role": {"M": "father", "F": "mother"}.get(sex.get(p), "parent"),
            "missing_parent_name": name.get(p, ""),
            "missing_parent_born": birth.get(p, ""),
            "missing_parent_birth_place": bplace.get(p, ""),
            "missing_parent_died": death.get(p, ""),
            "missing_parent_spouse": SEP.join(
                name.get(s, "") for s in partners_of.get(p, ())[:3] if real(s)),
            "missing_parent_verdict": verdict.get(p, ("absent", []))[0],
            "missing_parent_xref": p,
        })

rows.sort(key=lambda r: (r["on_your_line"] != "yes", r["both_parents_missing"] != "yes",
                         -r["new_ancestors"], r["hethel_name"]))

fields = list(rows[0].keys()) if rows else ["hethel_name"]
with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print("wrote %s -- %d gap rows" % (OUT_CSV.name, len(rows)), flush=True)

reachable = {r["missing_parent_xref"] for r in rows}
both_n = sum(1 for r in rows if r["both_parents_missing"] == "yes")
mine_n = sum(1 for r in rows if r["on_your_line"] == "yes")
OUT_JSON.write_text(json.dumps({
    "verdicts": dict(counts),
    "gap_rows": len(rows),
    "both_parents_missing": both_n,
    "on_your_line": mine_n,
    "distinct_missing_parents": len(reachable),
}, ensure_ascii=False), encoding="utf-8")

# ------------------------------------------------------------------ the page
E = html.escape


def cell(v):
    return E(str(v)) if v else '<span class="none">&mdash;</span>'


def place(v):
    return (" &middot; " + E(v)) if v else ""


cards = []
for r in rows[:400]:
    alt = ('<p class="alt">other candidates: %s</p>' % E(r["synoptic_alternates"])
           if r["synoptic_alternates"] else "")
    mine = '<span class="mine">your line</span>' if r["on_your_line"] == "yes" else ""
    cards.append(
        '<article class="gap %s">'
        '<header><span class="n">+%d</span><h3>%s</h3>' + mine +
        '<span class="conf">%s match</span></header>'
        '<div class="cols">'
        '<section><h4>in the synoptic tree</h4><p class="lab">%s</p>'
        '<p><a href="%s" target="_blank" rel="noopener">%s</a></p>%s</section>'
        '<section><h4>the same person in Hethel?</h4><p class="lab">%s</p>'
        '<dl><dt>born</dt><dd>%s%s</dd><dt>died</dt><dd>%s%s</dd>'
        '<dt>spouse</dt><dd>%s</dd><dt>children</dt><dd>%s</dd></dl></section>'
        '<section class="miss"><h4>%s Hethel gives, the tree lacks</h4><p class="lab">%s</p>'
        '<dl><dt>born</dt><dd>%s%s</dd><dt>died</dt><dd>%s</dd>'
        '<dt>spouse</dt><dd>%s</dd>'
        '<dt>line above</dt><dd><b>%d</b> people only in Hethel</dd></dl></section>'
        '</div></article>' % (
            "both" if r["both_parents_missing"] == "yes" else "one",
            r["new_ancestors"], E(r["hethel_name"]), E(r["confidence"]),
            cell(r["synoptic_label"]),
            E(r["geni_url"]), E(r["synoptic_geni_id"] or "no id"), alt,
            cell(r["hethel_name"]),
            cell(r["hethel_born"]), place(r["hethel_birth_place"]),
            cell(r["hethel_died"]), place(r["hethel_death_place"]),
            cell(r["hethel_spouse"]), cell(r["hethel_children"]),
            E(r["missing_parent_role"]), cell(r["missing_parent_name"]),
            cell(r["missing_parent_born"]), place(r["missing_parent_birth_place"]),
            cell(r["missing_parent_died"]), cell(r["missing_parent_spouse"]),
            r["new_ancestors"]))

STYLE = (
    ':root{--bg:#fbfaf8;--ink:#1d1b19;--mut:#6d6862;--line:#e2ddd6;--hot:#8c3b12}'
    '@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){'
    '--bg:#171512;--ink:#ece7e0;--mut:#9a938b;--line:#332f2a;--hot:#e08a52}}'
    ':root[data-theme="dark"]{--bg:#171512;--ink:#ece7e0;--mut:#9a938b;'
    '--line:#332f2a;--hot:#e08a52}'
    'body{background:var(--bg);color:var(--ink);'
    'font:15px/1.5 ui-serif,Georgia,serif;margin:0;padding:24px 16px;'
    'max-width:1100px;margin-inline:auto}'
    'h1{font-size:25px;margin:0 0 4px;line-height:1.25}'
    '.sub{color:var(--mut);margin:0 0 26px;font-size:14px}'
    '.gap{border:1px solid var(--line);border-radius:10px;margin:0 0 14px;overflow:hidden}'
    '.gap.both{border-color:var(--hot)}'
    'header{display:flex;gap:12px;align-items:baseline;padding:10px 14px;'
    'border-bottom:1px solid var(--line)}'
    'header h3{font-size:17px;margin:0;flex:1}'
    '.n{font:600 13px ui-monospace,SFMono-Regular,monospace;color:var(--hot)}'
    '.conf{font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.07em}'
    '.mine{font:600 11px ui-sans-serif,system-ui,sans-serif;text-transform:uppercase;'
    'letter-spacing:.07em;color:var(--bg);background:var(--hot);padding:2px 7px;'
    'border-radius:99px}'
    '.cols{display:grid;grid-template-columns:repeat(3,1fr)}'
    '.cols section{padding:12px 14px;border-right:1px solid var(--line)}'
    '.cols section:last-child{border-right:0}'
    '.miss{background:color-mix(in srgb,var(--hot) 8%,transparent)}'
    'h4{font:600 11px ui-sans-serif,system-ui,sans-serif;text-transform:uppercase;'
    'letter-spacing:.07em;color:var(--mut);margin:0 0 6px}'
    '.lab{font-size:16px;margin:0 0 6px}'
    'dl{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;margin:0;font-size:13px}'
    'dt{color:var(--mut)}dd{margin:0}.none{color:var(--mut)}'
    '.alt{font-size:12px;color:var(--mut);margin:6px 0 0}'
    'a{color:var(--hot)}'
    '@media(max-width:760px){.cols{grid-template-columns:1fr}'
    '.cols section{border-right:0;border-bottom:1px solid var(--line)}}'
)

OUT_HTML.write_text(
    '<!doctype html><html lang="en"><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Hethel Gaps</title><style>%s</style>'
    '<h1>What the Hethel pedigree has above people the synoptic tree already holds</h1>'
    '<p class="sub"><b>%d gaps on your own line</b> (badged, first) &middot; %d gaps in all '
    '&middot; %d with BOTH parents missing (outlined) &middot; %d distinct people reachable only '
    'through Hethel. Sorted by your line, then both-parents-missing, then the size of the line '
    'hanging above the gap. Showing the first %d; all of them are in '
    '<code>preservation/hethel-gaps.csv</code>. Nothing here is an identification &mdash; the '
    'two middle columns are there so the identification can be made.</p>%s</html>' % (
        STYLE, mine_n, len(rows), both_n, len(reachable), min(400, len(rows)),
        "".join(cards)),
    encoding="utf-8")
print("wrote %s" % OUT_HTML.name, flush=True)
