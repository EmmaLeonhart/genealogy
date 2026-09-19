"""Richard Borsheim's ancestry: what Hethel has above him that the synoptic tree does not.

⛔ **POSITIONAL ONLY. THERE IS NO STRING MATCHING IN THE JOIN.** Ruled 2026-09-18, after the
previous version of this file matched on name-token overlap and was told exactly what that was
worth: *"fuzzy string matching is not a thing ... I do not give a shit about fuzzy string
matching that is the most retarded shit around, I only want to be able to see the geni name vs
hethel name so I can make the decision, since I actually understand this shit and you do not and
you will never be able to understand the names."*

So the join is ONE hand identification and then graph position, nothing else:

    @I160@ Richard Borsheim   <->   6000000177921459056 Richard Wade Borsheim

verified four generations deep on structure alone before being used --

    Hethel    Richard -> Randolph -> Reinhert -> Rasmus Paulson -> Paul Pederson
    synoptic  6000000177921459056 -> ...459078 -> 6000000032068841409 -> 6000000020344842981

-- and from there the walk is father-to-father and mother-to-mother. No name is consulted, ever,
to decide that two people are the same. Names appear in the OUTPUT and only in the output, side
by side, because deciding whether `Peder Paulson (Borr V) Borsheim Lye` is the same man as
`Peder Paulsson Borsheim` is hers to do and not a thing a program should be guessing at.

⛔ **A GAP IS AN EMPTY PARENT SLOT, NOT AN ABSENT NAME.** The question this answers is: walking
up both trees in step, where does Hethel record a parent and the synoptic tree record nobody?
That is a structural fact with no judgement in it. What hangs above the gap is counted the same
way -- every Hethel person reachable upward from the missing parent.

⛔ **THE WALK STOPS WHERE THE PAIRING STOPS.** If the synoptic side has a father and Hethel does
not, there is nothing to add and the branch simply ends. If neither has one, likewise. The walk
only continues through slots BOTH trees fill, which is what keeps a single wrong pairing from
propagating into a whole invented branch -- and `generation` is on every row so a wrong one can
be seen and cut.

⛔ **FILLER NODES ARE NOT ANCESTRY.** `Hethelo`, `A few generations`, `Several generations Diaz`,
`Sophia II -- 2000th Kroll`, `Audumbla I` at `1345294336 BC`. Ruled 2026-09-17: *"Hethelo is not
a real person."* Never proposed as a parent, never counted in what hangs above one.
"""
import collections
import csv
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
HETHEL = ROOT / "preservation" / "genealogy" / "dropbox" / "Hethel Pedigree.ged"
OUT_CSV = ROOT / "preservation" / "hethel-gaps.csv"
OUT_HTML = ROOT / "preservation" / "hethel-gaps.html"
OUT_JSON = ROOT / "preservation" / "hethel-absent.json"
SEP = " | "
csv.field_size_limit(1 << 30)

#: The one hand identification the whole walk stands on. Verified on structure over four
#: generations, not on the spelling of the name.
ANCHOR_HETHEL = "@I160@"                     # Richard Borsheim
ANCHOR_GENI = "6000000177921459056"          # Richard Wade Borsheim

FILLER = re.compile(r"generations|Kroll|arbitrary|Audumbla|Hethelo", re.I)

# ------------------------------------------------------------------ Hethel, parsed
name, sex, birth, death, bplace, dplace = {}, {}, {}, {}, {}, {}
fam = collections.defaultdict(lambda: {"P": [], "C": []})
famc = collections.defaultdict(list)

cur = curfam = mode = event = None
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
                    famc[cur].append(mm.group(1))
        elif event and line.startswith("2 DATE "):
            (birth if event == "B" else death).setdefault(cur, line[7:].strip())
        elif event and line.startswith("2 PLAC "):
            (bplace if event == "B" else dplace).setdefault(cur, line[7:].strip())
    elif mode == "FAM":
        mm = re.match(r"^1 (HUSB|WIFE|CHIL) (@[^@]+@)", line)
        if mm:
            fam[curfam]["P" if mm.group(1) in ("HUSB", "WIFE") else "C"].append(mm.group(2))

parents_of = collections.defaultdict(list)
for f, d in fam.items():
    for c in d["C"]:
        parents_of[c].extend(d["P"])


def real(x):
    return bool(name.get(x)) and not FILLER.search(name[x])


def h_parent(x, want):
    """Hethel's father (`M`) or mother (`F`) of `x`, by SEX. Position, not name."""
    for p in parents_of.get(x, ()):
        if sex.get(p) == want and real(p):
            return p
    return None


print("hethel people: %d" % len(name), flush=True)

# ------------------------------------------------------------------ synoptic, parsed
gfather, gmother = {}, {}
with (ROOT / "reports" / "derived-family.csv").open(encoding="utf-8", newline="") as fh:
    for row in csv.DictReader(fh):
        g = (row.get("geni_id") or "").strip()
        if not g:
            continue
        f = (row.get("father") or "").split(SEP)[0].strip()
        m = (row.get("mother") or "").split(SEP)[0].strip()
        if f:
            gfather[g] = f
        if m:
            gmother[g] = m
print("synoptic people with a father or mother: %d"
      % len(set(gfather) | set(gmother)), flush=True)

glabel = {}
with (ROOT / "reports" / "derived-labels.csv").open(encoding="utf-8", newline="") as fh:
    for row in csv.DictReader(fh):
        g = (row.get("geni_id") or "").strip()
        v = (row.get("label_en") or row.get("label_mul") or "").strip()
        if g and v:
            glabel[g] = v
print("synoptic labelled people: %d" % len(glabel), flush=True)

gborn, gdied, gbplace = {}, {}, {}
with (ROOT / "reports" / "derived-facts.csv").open(encoding="utf-8", newline="") as fh:
    for row in csv.DictReader(fh):
        g = (row.get("geni_id") or "").strip()
        if not g:
            continue
        if row.get("birth_date_year"):
            gborn[g] = row["birth_date_year"].strip()
        if row.get("death_date_year"):
            gdied[g] = row["death_date_year"].strip()
        if row.get("birth_place"):
            gbplace[g] = row["birth_place"].strip()
print("synoptic people with a birth year: %d" % len(gborn), flush=True)

# ------------------------------------------------------------------ what hangs above a gap
_above = {}


def above(start):
    if start in _above:
        return _above[start]
    seen, stack = set(), [start]
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        stack.extend(parents_of.get(x, ()))
    _above[start] = {x for x in seen if real(x)}
    return _above[start]


# ------------------------------------------------------------------ the lockstep walk
rows, paired, seen_pairs = [], [], set()
queue = collections.deque([(ANCHOR_HETHEL, ANCHOR_GENI, 0, "the anchor")])
while queue:
    h, g, depth, via = queue.popleft()
    if (h, g) in seen_pairs:
        continue
    seen_pairs.add((h, g))
    paired.append({
        "generation": depth, "via": via,
        "hethel_xref": h, "hethel_name": name.get(h, ""),
        "hethel_born": birth.get(h, ""), "hethel_died": death.get(h, ""),
        "hethel_birth_place": bplace.get(h, ""),
        "geni_id": g, "geni_name": glabel.get(g, ""),
        "geni_born": gborn.get(g, ""), "geni_died": gdied.get(g, ""),
        "geni_birth_place": gbplace.get(g, ""),
    })
    for role, want, gmap in (("father", "M", gfather), ("mother", "F", gmother)):
        hp = h_parent(h, want)
        gp = gmap.get(g)
        if hp and gp:
            queue.append((hp, gp, depth + 1, "%s of %s" % (role, name.get(h, h))))
        elif hp and not gp:
            rows.append({
                "generation": depth + 1,
                "new_ancestors": len(above(hp)),
                "missing_role": role,
                # the attach point, both sides, side by side -- this is the decision
                "geni_id": g,
                "geni_name": glabel.get(g, ""),
                "geni_url": "https://www.geni.com/people/x/%s" % g,
                "geni_born": gborn.get(g, ""),
                "geni_died": gdied.get(g, ""),
                "geni_birth_place": gbplace.get(g, ""),
                "hethel_name": name.get(h, ""),
                "hethel_born": birth.get(h, ""),
                "hethel_died": death.get(h, ""),
                "hethel_birth_place": bplace.get(h, ""),
                "hethel_xref": h,
                # what Hethel wants to attach there
                "parent_name": name.get(hp, ""),
                "parent_born": birth.get(hp, ""),
                "parent_died": death.get(hp, ""),
                "parent_birth_place": bplace.get(hp, ""),
                "parent_xref": hp,
                "path_from_richard": via,
            })

rows.sort(key=lambda r: (-r["new_ancestors"], r["generation"], r["parent_name"]))
print("paired positionally: %d people; gaps: %d" % (len(paired), len(rows)), flush=True)

with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["parent_name"])
    w.writeheader()
    w.writerows(rows)

with (ROOT / "preservation" / "hethel-pairs.csv").open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(paired[0].keys()) if paired else ["hethel_name"])
    w.writeheader()
    w.writerows(paired)

OUT_JSON.write_text(json.dumps({
    "anchor": {"hethel": ANCHOR_HETHEL, "geni": ANCHOR_GENI},
    "paired_positionally": len(paired),
    "gaps": len(rows),
    "people_only_in_hethel": len({x for r in rows for x in above(r["parent_xref"])}),
}, ensure_ascii=False), encoding="utf-8")

# ------------------------------------------------------------------ the page
E = html.escape


def cell(v):
    return E(str(v)) if v else '<span class="none">&mdash;</span>'


def years(b, d):
    if not b and not d:
        return '<span class="none">&mdash;</span>'
    return "%s &ndash; %s" % (E(b or "?"), E(d or "?"))


cards = []
for r in rows:
    cards.append(
        '<article class="gap">'
        '<header><span class="gen">gen %d</span>'
        '<h3>attach a %s</h3>'
        '<span class="n">+%d above</span></header>'
        '<div class="body">'
        '<div class="who"><h4>is this the same man or woman?</h4><table>'
        '<tr><th>Geni</th><td class="nm">%s</td><td>%s</td><td>%s</td>'
        '<td><a href="%s" target="_blank" rel="noopener">open</a></td></tr>'
        '<tr><th>Hethel</th><td class="nm">%s</td><td>%s</td><td>%s</td><td></td></tr>'
        '</table></div>'
        '<div class="add"><h4>then Hethel gives this %s, and Geni has no one in that slot</h4>'
        '<p class="nm big">%s</p><p class="meta">%s &middot; %s</p>'
        '<p class="meta"><b>%d</b> people hang above &mdash; reachable only through Hethel</p>'
        '</div></div></article>' % (
            r["generation"], E(r["missing_role"]), r["new_ancestors"],
            cell(r["geni_name"]), years(r["geni_born"], r["geni_died"]),
            cell(r["geni_birth_place"]), E(r["geni_url"]),
            cell(r["hethel_name"]), years(r["hethel_born"], r["hethel_died"]),
            cell(r["hethel_birth_place"]),
            E(r["missing_role"]), cell(r["parent_name"]),
            years(r["parent_born"], r["parent_died"]), cell(r["parent_birth_place"]),
            r["new_ancestors"]))

STYLE = (
    ':root{--bg:#fbfaf8;--ink:#1d1b19;--mut:#6d6862;--line:#e2ddd6;--hot:#8c3b12;'
    '--warm:#f4efe7}'
    '@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){'
    '--bg:#171512;--ink:#ece7e0;--mut:#9a938b;--line:#332f2a;--hot:#e08a52;--warm:#201d19}}'
    ':root[data-theme="dark"]{--bg:#171512;--ink:#ece7e0;--mut:#9a938b;--line:#332f2a;'
    '--hot:#e08a52;--warm:#201d19}'
    'body{background:var(--bg);color:var(--ink);font:15px/1.55 ui-serif,Georgia,serif;'
    'margin:0;padding:24px 16px;max-width:900px;margin-inline:auto}'
    'h1{font-size:25px;margin:0 0 6px;line-height:1.25}'
    '.sub{color:var(--mut);margin:0 0 8px;font-size:14px}'
    '.anchor{font-size:13px;color:var(--mut);border-left:3px solid var(--hot);'
    'padding:6px 0 6px 12px;margin:0 0 26px}'
    '.gap{border:1px solid var(--line);border-radius:10px;margin:0 0 16px;overflow:hidden}'
    'header{display:flex;gap:12px;align-items:baseline;padding:9px 14px;'
    'border-bottom:1px solid var(--line);background:var(--warm)}'
    'header h3{font-size:15px;margin:0;flex:1;font-weight:600}'
    '.gen{font:600 11px ui-monospace,SFMono-Regular,monospace;color:var(--mut)}'
    '.n{font:600 13px ui-monospace,SFMono-Regular,monospace;color:var(--hot)}'
    '.body{display:grid;grid-template-columns:1.15fr 1fr}'
    '.who{padding:12px 14px;border-right:1px solid var(--line)}'
    '.add{padding:12px 14px}'
    'h4{font:600 11px ui-sans-serif,system-ui,sans-serif;text-transform:uppercase;'
    'letter-spacing:.06em;color:var(--mut);margin:0 0 8px}'
    'table{border-collapse:collapse;width:100%;font-size:13px}'
    'th{text-align:left;color:var(--mut);font-weight:600;padding:3px 10px 3px 0;'
    'white-space:nowrap;vertical-align:top}'
    'td{padding:3px 10px 3px 0;vertical-align:top}'
    '.nm{font-size:15px}.big{font-size:18px;margin:0 0 4px}'
    '.meta{font-size:13px;color:var(--mut);margin:0 0 3px}'
    '.none{color:var(--mut)}a{color:var(--hot)}'
    '@media(max-width:720px){.body{grid-template-columns:1fr}'
    '.who{border-right:0;border-bottom:1px solid var(--line)}}'
)

OUT_HTML.write_text(
    '<!doctype html><html lang="en"><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Borsheim Gaps</title><style>%s</style>'
    '<h1>Richard Borsheim&rsquo;s ancestry: parents Hethel records and Geni leaves empty</h1>'
    '<p class="sub"><b>%d gaps</b> &middot; %d people paired by position &middot; '
    '%d people reachable only through Hethel &middot; sorted by the size of the line above.</p>'
    '<p class="anchor">One hand identification and then graph position: '
    '<b>@I160@ Richard Borsheim</b> &harr; <b>6000000177921459056 Richard Wade Borsheim</b>, '
    'verified four generations on structure. After that the walk is father&rarr;father and '
    'mother&rarr;mother. <b>No name decides anything.</b> The two names sit side by side below '
    'so you can throw out a pairing I got wrong.</p>%s</html>' % (
        STYLE, len(rows), len(paired),
        len({x for r in rows for x in above(r["parent_xref"])}), "".join(cards)),
    encoding="utf-8")
print("wrote %s and %s" % (OUT_HTML.name, OUT_CSV.name), flush=True)
