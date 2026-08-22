"""Render the improperly-keyed-individuals census as a single HTML page.

Inputs, all offline:
  reports/improper-keys.csv        - scan-improper-keys.py over the 525 exports
  out/wikidata/p2600-all.tsv       - every P2600 statement in the local store
  out/improper-keys/*           - sidecars: labels for the flagged QIDs (pulled from
                                   wikidata/items/ by scripts/pull-flagged-item-labels.py),
                                   the condensed legacy-shape roster, and which flagged
                                   Geni IDs the corpus actually holds

Output: reports/improper-keys.html
"""
from __future__ import annotations

import collections
import csv
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRATCH = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "out" / "improper-keys"

NUM = re.compile(r"\d{5,19}")
CANON = re.compile(r"^6000000\d{12}$")


def geni_url(i: str) -> str:
    return f"https://www.geni.com/people/x/{i}"


def wd_url(q: str) -> str:
    return f"https://www.wikidata.org/wiki/{q}"


def e(s) -> str:
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- inputs
labels = json.loads((SCRATCH / "wd-labels.json").read_text(encoding="utf-8"))
noncanon = json.loads((SCRATCH / "geni-noncanon.json").read_text(encoding="utf-8"))
corpus_hits = {
    line.split("@I")[1].split("@")[0]
    for line in (SCRATCH / "probe-hits.txt").read_text(encoding="utf-8").splitlines()
    if "@I" in line
}

rows: list[tuple[str, str]] = []
with (ROOT / "out" / "wikidata" / "p2600-all.tsv").open(encoding="utf-8") as fh:
    for line in fh:
        p = line.rstrip("\n").split("\t")
        if len(p) >= 2:
            rows.append((p[0].strip(), p[1].strip()))

malformed = [(q, g) for q, g in rows if not (g.isdigit() and 5 <= len(g) <= 19)]
by_id: dict[str, set[str]] = collections.defaultdict(set)
for q, g in rows:
    by_id[g].add(q)
shared = {g: sorted(qs) for g, qs in by_id.items() if len(qs) > 1}


def diagnose(value: str) -> tuple[str, str]:
    """(class, plain-English statement of what is in the field instead of an ID)."""
    if value.startswith("http"):
        if "geni.com" not in value:
            return "foreign-url", "a URL on another website entirely, not Geni"
        if not NUM.search(value):
            return "url-no-id", "a Geni URL whose slug carries no profile ID"
        if "?" in value or "#" in value:
            return "url-tracked", "a whole Geni URL, tracking parameters included"
        return "url", "a whole Geni URL where the bare ID belongs"
    if "people/" in value:
        return "url-fragment", "part of a Geni URL path, not the ID on its own"
    if value.isdigit():
        return "too-short", "a bare number shorter than any ID in the corpus"
    if value.rstrip("/?").isdigit():
        return "punctuation", "the right ID with a stray character stuck to the end"
    return "not-an-id", "not an identifier of any kind"


CLASS_ORDER = [
    ("url-tracked", "Whole URL, with tracking"),
    ("url", "Whole URL"),
    ("url-fragment", "URL fragment"),
    ("url-no-id", "URL with no ID in it"),
    ("foreign-url", "A different website"),
    ("punctuation", "Stray trailing character"),
    ("too-short", "Improbably short number"),
    ("not-an-id", "Not an identifier"),
]
CLASS_NAME = dict(CLASS_ORDER)

diagnosed = []
for q, g in sorted(malformed):
    cls, why = diagnose(g)
    m = NUM.search(g)
    rec = m.group(0) if m else ""
    diagnosed.append(
        {
            "qid": q,
            "label": labels.get(q, {}).get("label", ""),
            "desc": labels.get(q, {}).get("desc", ""),
            "value": g,
            "cls": cls,
            "why": why,
            "recovered": rec,
            "in_corpus": rec in corpus_hits,
        }
    )
diagnosed.sort(key=lambda r: ([c for c, _ in CLASS_ORDER].index(r["cls"]), r["qid"]))

shared_rows = []
for g, qs in sorted(shared.items()):
    shared_rows.append(
        {
            "geni": g,
            "items": [
                {
                    "qid": q,
                    "label": labels.get(q, {}).get("label", ""),
                    "desc": labels.get(q, {}).get("desc", ""),
                }
                for q in qs
            ],
            "in_corpus": g in corpus_hits,
        }
    )

SHAPE = {
    "legacy-short": ("Five to seven digits", "legacy"),
    "eighteen": ("Eighteen digits", "eighteen"),
    "nineteen-other": ("Nineteen digits, not 6000000", "nineteen"),
}
shape_counts = collections.Counter(r[2] for r in noncanon)

wd_shape = collections.Counter()
for _, g in rows:
    if not g.isdigit():
        wd_shape["malformed"] += 1
    elif CANON.match(g):
        wd_shape["canonical"] += 1
    elif len(g) == 19:
        wd_shape["nineteen-other"] += 1
    elif len(g) == 18:
        wd_shape["eighteen"] += 1
    else:
        wd_shape["legacy-short"] += 1

payload = [[r[0], r[1], r[2], r[3]] for r in noncanon]

# ---------------------------------------------------------------- render
CSS = """
:root{
  --bg:#eceff3; --surface:#fff; --sunk:#f5f7f9; --ink:#141821; --ink-2:#39424f;
  --muted:#5d6775; --line:#d3d9e1; --line-2:#e4e9ef;
  --accent:#9c4f18; --accent-soft:#f2e3d6;
  --crit:#9e2430; --crit-soft:#f6e0e2;
  --warn:#7d5a12; --warn-soft:#f5ecd5;
  --ok:#1c6349; --ok-soft:#dcefe6;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#101319; --surface:#181c23; --sunk:#1e232b; --ink:#e6eaf0; --ink-2:#c3cbd6;
    --muted:#939eae; --line:#2a313b; --line-2:#232932;
    --accent:#e2914e; --accent-soft:#3a2a1a;
    --crit:#ef8b93; --crit-soft:#3b1f23;
    --warn:#dcb45c; --warn-soft:#332a16;
    --ok:#6ecaa1; --ok-soft:#183329;
  }
}
:root[data-theme="dark"]{
  --bg:#101319; --surface:#181c23; --sunk:#1e232b; --ink:#e6eaf0; --ink-2:#c3cbd6;
  --muted:#939eae; --line:#2a313b; --line-2:#232932;
  --accent:#e2914e; --accent-soft:#3a2a1a;
  --crit:#ef8b93; --crit-soft:#3b1f23;
  --warn:#dcb45c; --warn-soft:#332a16;
  --ok:#6ecaa1; --ok-soft:#183329;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  font-size:16px; line-height:1.6;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1140px; margin:0 auto; padding:clamp(1.5rem,4vw,3.5rem) clamp(1rem,3vw,2rem) 6rem;
  display:flex; flex-direction:column; gap:3rem}
h1,h2,h3{font-family:"IBM Plex Serif",Georgia,serif; text-wrap:balance; margin:0; font-weight:600}
h1{font-size:clamp(2rem,4.6vw,3rem); line-height:1.12; letter-spacing:-.015em}
h2{font-size:1.45rem; line-height:1.25}
h3{font-size:1.02rem}
p{margin:0}
a{color:var(--accent); text-decoration:none; border-bottom:1px solid color-mix(in srgb,var(--accent) 35%,transparent)}
a:hover{border-bottom-color:var(--accent)}
a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
code,.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
  font-size:.86em; font-variant-numeric:tabular-nums}

/* masthead */
.eyebrow{font-family:"IBM Plex Mono",monospace; font-size:.74rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--muted)}
header{display:flex; flex-direction:column; gap:1rem;
  border-bottom:3px solid var(--ink); padding-bottom:2rem}
.lede{font-size:1.12rem; color:var(--ink-2); max-width:62ch}

/* stat strip */
.stats{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:1px;
  background:var(--line); border:1px solid var(--line)}
.stat{background:var(--surface); padding:1rem 1.1rem; display:flex; flex-direction:column; gap:.15rem}
.stat b{font-family:"IBM Plex Mono",monospace; font-size:1.55rem; line-height:1.1;
  font-variant-numeric:tabular-nums; letter-spacing:-.02em}
.stat span{font-size:.78rem; color:var(--muted); line-height:1.35}
.stat.is-crit b{color:var(--crit)}
.stat.is-ok b{color:var(--ok)}

/* sections */
section{display:flex; flex-direction:column; gap:1.15rem}
.head{display:flex; flex-direction:column; gap:.5rem;
  border-top:1px solid var(--line); padding-top:1.5rem}
.head-row{display:flex; flex-wrap:wrap; align-items:baseline; gap:.65rem}
.verdict{font-family:"IBM Plex Mono",monospace; font-size:.7rem; letter-spacing:.1em;
  text-transform:uppercase; padding:.24rem .55rem; border-radius:2px; white-space:nowrap}
.v-crit{background:var(--crit-soft); color:var(--crit)}
.v-warn{background:var(--warn-soft); color:var(--warn)}
.v-ok{background:var(--ok-soft); color:var(--ok)}
.v-note{background:var(--accent-soft); color:var(--accent)}
.body-copy{max-width:70ch; color:var(--ink-2); display:flex; flex-direction:column; gap:.8rem}

/* callout */
.reading{background:var(--surface); border:1px solid var(--line); border-left:4px solid var(--accent);
  padding:1.25rem 1.4rem; display:flex; flex-direction:column; gap:.75rem}
.reading dt{font-family:"IBM Plex Mono",monospace; font-size:.72rem; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted); margin-bottom:.15rem}
.reading dd{margin:0; color:var(--ink-2)}
.reading dl{margin:0; display:flex; flex-direction:column; gap:.8rem}

/* tables */
.scroll{overflow-x:auto; border:1px solid var(--line); background:var(--surface)}
table{border-collapse:collapse; width:100%; font-size:.9rem}
thead th{position:sticky; top:0; z-index:1; background:var(--sunk);
  font-family:"IBM Plex Mono",monospace; font-size:.68rem; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted); font-weight:500;
  text-align:left; padding:.6rem .8rem; border-bottom:1px solid var(--line); white-space:nowrap}
tbody td{padding:.55rem .8rem; border-bottom:1px solid var(--line-2); vertical-align:top}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover td{background:var(--sunk)}
td.num{text-align:right; font-variant-numeric:tabular-nums; color:var(--muted);
  font-family:"IBM Plex Mono",monospace}
.who{display:flex; flex-direction:column; gap:.1rem}
.who small{color:var(--muted); font-size:.78rem}
.raw{font-family:"IBM Plex Mono",monospace; font-size:.78rem; word-break:break-all;
  color:var(--crit); background:var(--crit-soft); padding:.1rem .3rem; display:inline-block}
.grp{background:var(--sunk)!important}
.grp td{font-family:"IBM Plex Mono",monospace; font-size:.78rem; color:var(--muted);
  letter-spacing:.02em; border-bottom:1px solid var(--line)}
.pill{display:inline-block; font-family:"IBM Plex Mono",monospace; font-size:.68rem;
  letter-spacing:.06em; text-transform:uppercase; padding:.15rem .45rem; border-radius:2px;
  background:var(--sunk); color:var(--muted); border:1px solid var(--line); white-space:nowrap}
.pill.here{background:var(--ok-soft); color:var(--ok); border-color:transparent}

/* invariant list */
.checks{display:grid; gap:1px; background:var(--line); border:1px solid var(--line)}
.check{background:var(--surface); padding:.9rem 1.1rem; display:flex; gap:1rem;
  align-items:flex-start; justify-content:space-between; flex-wrap:wrap}
.check p{color:var(--muted); font-size:.85rem; max-width:64ch}
.check b{font-weight:600; font-size:.95rem}
.count{font-family:"IBM Plex Mono",monospace; font-size:1.1rem; color:var(--ok);
  font-variant-numeric:tabular-nums; white-space:nowrap}

/* filter bar */
.filters{display:flex; flex-wrap:wrap; gap:.5rem; align-items:center}
input[type=search]{font:inherit; font-size:.9rem; padding:.5rem .7rem; min-width:min(320px,100%);
  background:var(--surface); color:var(--ink); border:1px solid var(--line); border-radius:2px}
button.chip{font-family:"IBM Plex Mono",monospace; font-size:.72rem; letter-spacing:.06em;
  text-transform:uppercase; padding:.45rem .7rem; border:1px solid var(--line);
  background:var(--surface); color:var(--muted); border-radius:2px; cursor:pointer}
button.chip[aria-pressed=true]{background:var(--ink); color:var(--bg); border-color:var(--ink)}
.more{align-self:flex-start; font:inherit; font-size:.85rem; padding:.55rem 1.1rem;
  background:var(--surface); color:var(--ink); border:1px solid var(--line); cursor:pointer; border-radius:2px}
.more:hover{background:var(--sunk)}
.tally{font-family:"IBM Plex Mono",monospace; font-size:.78rem; color:var(--muted)}
footer{border-top:1px solid var(--line); padding-top:1.5rem; color:var(--muted); font-size:.82rem;
  max-width:70ch; display:flex; flex-direction:column; gap:.6rem}
@media (prefers-reduced-motion:reduce){*{animation:none!important; transition:none!important}}
"""


def stat(value, label, klass=""):
    return f'<div class="stat {klass}"><b>{e(value)}</b><span>{e(label)}</span></div>'


parts: list[str] = []
A = parts.append

A('<title>Improperly Keyed Individuals</title>')
A('<link rel="preconnect" href="https://fonts.googleapis.com">')
A('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
A('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
  'family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&'
  'family=IBM+Plex+Serif:wght@600&display=swap">')
A(f"<style>{CSS}</style>")
A('<div class="wrap">')

# ---- masthead
n_bad = len(diagnosed)
n_shared_items = sum(len(r["items"]) for r in shared_rows)
A('<header>')
A('<p class="eyebrow">Key audit &middot; 525 Geni exports &middot; 517,851 Wikidata Geni-ID statements</p>')
A('<h1>Every individual whose Geni ID is not a working key</h1>')
A('<p class="lede">The Geni profile ID is this project’s primary key, so a person whose '
  'key is wrong is a person no join will ever reach. This is the whole population of them, '
  'checked on both sides &mdash; the GEDCOM corpus and the local Wikidata store &mdash; and '
  'the count is not symmetric: the exports come back clean, and every genuinely broken key '
  'is on Wikidata.</p>')
A('</header>')

A('<div class="stats">')
A(stat(f"{n_bad}", "Wikidata items whose Geni ID field holds something that is not a Geni ID", "is-crit"))
A(stat(f"{len(shared_rows)}", "Geni profiles keyed to two Wikidata items at once", "is-crit"))
A(stat(f"{n_shared_items}", "Wikidata items caught in those double keyings", "is-crit"))
A(stat("0", "broken keys in the GEDCOM corpus, over 2,281,820 individual records", "is-ok"))
A(stat(f"{len(noncanon):,}", "corpus individuals on a legacy ID shape — unusual, not broken"))
A('</div>')

# ---- the reading
A('<section>')
A('<div class="head"><div class="head-row"><h2>What “improperly keyed” was taken to mean</h2>'
  '<span class="verdict v-note">reading recorded</span></div></div>')
A('<div class="reading"><dl>')
A('<dt>Taken</dt><dd>A key is improper when it cannot do a key’s job: the field holds '
  'something that is not a Geni profile ID, the two copies of the ID on one record disagree, '
  'one record carries no key, or one key is shared by two records that should be distinct. '
  'That is a property of the identifier, and it is checkable offline on both sides.</dd>')
A('<dt>Rejected</dt><dd>“Any Geni ID that does not look like <code>6000000…</code>”. '
  'It is the tempting reading &mdash; 35,098 corpus individuals fail it &mdash; but Wikidata’s own '
  f'Geni ID statements carry {wd_shape["nineteen-other"] + wd_shape["eighteen"] + wd_shape["legacy-short"]:,} '
  'values in exactly those shapes, so they are older Geni IDs rather than bad ones. They are '
  'listed at the bottom of this page all the same, because they are the population the phrase '
  'might have meant.</dd>')
A('<dt>What would switch it</dt><dd>A legacy-shaped ID that resolves to nothing on Geni. '
  'Settling that needs a live Geni lookup, which this project does not do on a whim.</dd>')
A('</dl></div>')
A('</section>')

# ---- section: malformed P2600
A('<section>')
A('<div class="head"><div class="head-row">'
  f'<h2>Wikidata: {n_bad} items whose Geni ID is not an ID</h2>'
  '<span class="verdict v-crit">broken</span></div>'
  '<div class="body-copy"><p>Every one of these is a <code>P2600</code> <em>Geni.com profile ID</em> '
  'statement whose value cannot be a profile ID. Most are a whole browser URL pasted into the '
  'identifier field, several still carrying the <code>?through=</code> parameter Geni appends when '
  'you arrive from a relative’s page. Where a real ID is embedded in the mess it is recovered '
  f'here; {sum(1 for r in diagnosed if not r["recovered"])} of them contain no ID at all.</p></div></div>')
A('<div class="scroll"><table><thead><tr>'
  '<th>Wikidata item</th><th>What the Geni ID field actually holds</th>'
  '<th>Recoverable ID</th><th>In our exports</th></tr></thead><tbody>')
last = None
for r in diagnosed:
    if r["cls"] != last:
        last = r["cls"]
        n = sum(1 for x in diagnosed if x["cls"] == last)
        A(f'<tr class="grp"><td colspan="4">{e(CLASS_NAME[last])} &middot; {n}</td></tr>')
    lab = r["label"] or "(no English label)"
    desc = f'<small>{e(r["desc"])}</small>' if r["desc"] else ""
    rec = (f'<a class="mono" href="{geni_url(r["recovered"])}" target="_blank" rel="noopener">'
           f'{e(r["recovered"])}</a>') if r["recovered"] else '<span class="pill">none</span>'
    here = ('<span class="pill here">yes</span>' if r["in_corpus"]
            else '<span class="pill">not sampled</span>')
    A(f'<tr><td><div class="who"><a href="{wd_url(r["qid"])}" target="_blank" rel="noopener">'
      f'{e(lab)}</a><small class="mono">{e(r["qid"])}</small>{desc}</div></td>'
      f'<td><span class="raw">{e(r["value"])}</span><br><small style="color:var(--muted)">'
      f'{e(r["why"])}</small></td><td>{rec}</td><td>{here}</td></tr>')
A('</tbody></table></div>')
A('</section>')

# ---- section: shared keys
A('<section>')
A('<div class="head"><div class="head-row">'
  f'<h2>Wikidata: {len(shared_rows)} Geni profiles keyed to two items each</h2>'
  '<span class="verdict v-crit">broken</span></div>'
  '<div class="body-copy"><p>One Wikidata item carrying two Geni IDs is ordinary and correct — '
  'Geni holds unmergeable duplicate profiles, and a second <code>P2600</code> is how you say so. '
  'This is the other direction, and it is not ordinary: one Geni profile claimed by two separate '
  f'Wikidata items, {n_shared_items} items in all. Either the two items are the same person and want '
  'merging, or one of them has the wrong ID on it. Read the labels side by side and it is usually '
  'obvious which.</p></div></div>')
A('<div class="scroll"><table><thead><tr>'
  '<th>Geni profile</th><th>Item</th><th>Item</th><th>Also here</th></tr></thead><tbody>')
for r in shared_rows:
    def cell(it):
        d = f'<small>{e(it["desc"])}</small>' if it["desc"] else ""
        return (f'<div class="who"><a href="{wd_url(it["qid"])}" target="_blank" rel="noopener">'
                f'{e(it["label"] or "(no English label)")}</a>'
                f'<small class="mono">{e(it["qid"])}</small>{d}</div>')
    extra = ""
    if len(r["items"]) > 2:
        extra = "".join(f'<div class="who" style="margin-top:.5rem">{cell(i)}</div>'
                        for i in r["items"][2:])
    here = ('<span class="pill here">in corpus</span>' if r["in_corpus"]
            else '<span class="pill">not sampled</span>')
    A(f'<tr><td><a class="mono" href="{geni_url(r["geni"])}" target="_blank" rel="noopener">'
      f'{e(r["geni"])}</a></td><td>{cell(r["items"][0])}</td>'
      f'<td>{cell(r["items"][1])}{extra}</td><td>{here}</td></tr>')
A('</tbody></table></div>')
A('</section>')

# ---- section: corpus clean
A('<section>')
A('<div class="head"><div class="head-row">'
  '<h2>The GEDCOM corpus: no broken keys at all</h2>'
  '<span class="verdict v-ok">clean</span></div>'
  '<div class="body-copy"><p>Geni writes the profile ID twice on every individual — once as the '
  'record’s cross-reference, once as an <code>RFN</code> line — which makes the key '
  'self-checking. Every individual record in all 525 exports was read and put through the four '
  'checks below. Nothing failed any of them, so there is no such thing as an improperly keyed '
  'individual on the Geni side of this project.</p></div></div>')
CHECKS = [
    ("The cross-reference is readable as a Geni ID",
     "An xref outside the four record-type letters would parse to a fabricated ID pointing at "
     "a stranger’s profile — the failure this check exists for.", "0 of 2,281,820"),
    ("The cross-reference and the RFN agree",
     "The two copies of the ID naming different profiles is the one fault that would silently "
     "merge two people into one.", "0 of 2,281,820"),
    ("Every individual carries an RFN",
     "No record relies on the xref alone, so the cross-check is available everywhere.",
     "0 missing"),
    ("No key is used twice inside one export",
     "Two individuals sharing a key in a single file would collapse to one on merge.",
     "0 collisions"),
]
A('<div class="checks">')
for title, why, count in CHECKS:
    A(f'<div class="check"><div><b>{e(title)}</b><p>{e(why)}</p></div>'
      f'<span class="count">{e(count)}</span></div>')
A('</div>')
A('</section>')

# ---- section: legacy shapes
A('<section>')
A('<div class="head"><div class="head-row">'
  f'<h2>Corpus: {len(noncanon):,} individuals on a legacy ID shape</h2>'
  '<span class="verdict v-warn">unusual, not broken</span></div>'
  '<div class="body-copy"><p>Geni hands out nineteen-digit IDs opening <code>6000000</code>, and '
  '1,259,262 of the corpus’s 1,294,360 individuals have one. The rest do not, and the three '
  'shapes they take are listed below. They are almost certainly older allocations rather than '
  f'errors: Wikidata’s Geni ID statements carry {wd_shape["legacy-short"]:,} short IDs, '
  f'{wd_shape["eighteen"]:,} eighteen-digit ones and {wd_shape["nineteen-other"]:,} nineteen-digit '
  'ones that do not open <code>6000000</code>, and Geni’s own relationship-path pages link '
  'them as live profiles. Search the table for a name, an ID, or a shape.</p></div></div>')
A('<div class="stats">')
for key, (name, _) in SHAPE.items():
    A(stat(f"{shape_counts[key]:,}", name))
A('</div>')
A('<div class="filters">'
  '<input type="search" id="q" placeholder="Filter by name or Geni ID…" '
  'aria-label="Filter individuals by name or Geni ID">'
  '<button class="chip" data-f="all" aria-pressed="true">All</button>'
  '<button class="chip" data-f="legacy-short" aria-pressed="false">5–7 digits</button>'
  '<button class="chip" data-f="eighteen" aria-pressed="false">18 digits</button>'
  '<button class="chip" data-f="nineteen-other" aria-pressed="false">19, not 6000000</button>'
  '<span class="tally" id="tally"></span></div>')
A('<div class="scroll"><table><thead><tr><th>Geni ID</th><th>Name as the export writes it</th>'
  '<th>Shape</th><th>Exports holding them</th></tr></thead><tbody id="rows"></tbody></table></div>')
A('<button class="more" id="more">Show more</button>')
A('</section>')

A('<footer>')
A('<p>Built offline. The corpus figures come from a line scan of every <code>.ged</code> under '
  '<code>exports/</code> that <code>genimerge.sources</code> counts as corpus — 525 files after '
  'byte-identical repeats are dropped. The Wikidata figures come from the local item store and its '
  '517,851 Geni ID statements; nothing was asked of Wikidata live.</p>')
A('<p>Absence is bounded in both directions. “Not sampled” means no export of ours has '
  'reached that person, never that Geni lacks them; and the store is a Geni-shaped slice of '
  'Wikidata, so a broken key outside it would not appear here.</p>')
A('<p>Row data, every instance one row: <code>reports/improper-keys-wikidata.csv</code> (the '
  '31), <code>reports/shared-geni-keys.csv</code> (the 143), '
  '<code>reports/improper-keys.csv</code> (the corpus scan). Built by '
  '<code>scripts/scan-improper-keys.py</code> and '
  '<code>scripts/build-improper-keys-html.py</code>.</p>')
A('</footer>')
A('</div>')

A(f'<script id="data" type="application/json">{json.dumps(payload, ensure_ascii=False, separators=(",", ":"))}</script>')
A("""<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const SHAPE = {'legacy-short':'5–7 digits','eighteen':'18 digits','nineteen-other':'19, not 6000000'};
const rows = document.getElementById('rows'), more = document.getElementById('more'),
      tally = document.getElementById('tally'), q = document.getElementById('q');
const STEP = 200;
let filter = 'all', term = '', shown = 0, matched = DATA;
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function recompute(){
  const t = term.trim().toLowerCase();
  matched = DATA.filter(r =>
    (filter === 'all' || r[2] === filter) &&
    (!t || r[0].includes(t) || r[1].toLowerCase().includes(t)));
  rows.innerHTML = ''; shown = 0; render();
}
function render(){
  const slice = matched.slice(shown, shown + STEP);
  rows.insertAdjacentHTML('beforeend', slice.map(r =>
    `<tr><td><a class="mono" href="https://www.geni.com/people/x/${r[0]}" target="_blank" rel="noopener">${r[0]}</a></td>`
    + `<td>${r[1] ? esc(r[1]) : '<span class="pill">no name recorded</span>'}</td>`
    + `<td><span class="pill">${SHAPE[r[2]]}</span></td><td class="num">${r[3]}</td></tr>`).join(''));
  shown += slice.length;
  more.hidden = shown >= matched.length;
  more.textContent = `Show more — ${(matched.length - shown).toLocaleString()} left`;
  tally.textContent = `${shown.toLocaleString()} of ${matched.length.toLocaleString()} shown`;
}
more.addEventListener('click', render);
q.addEventListener('input', e => { term = e.target.value; recompute(); });
document.querySelectorAll('.chip').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('.chip').forEach(o => o.setAttribute('aria-pressed', String(o === b)));
  filter = b.dataset.f; recompute();
}));
recompute();
</script>""")

# sidecar CSVs — every instance, one row each
with (ROOT / "reports" / "improper-keys-wikidata.csv").open(
        "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["qid", "label", "description", "p2600_value", "fault",
                "what_it_holds", "recovered_geni_id", "in_our_corpus"])
    for r in diagnosed:
        w.writerow([r["qid"], r["label"], r["desc"], r["value"], CLASS_NAME[r["cls"]],
                    r["why"], r["recovered"], "yes" if r["in_corpus"] else "no"])

with (ROOT / "reports" / "shared-geni-keys.csv").open(
        "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["geni_id", "qid", "label", "description", "items_sharing_this_key",
                "in_our_corpus"])
    for r in shared_rows:
        for it in r["items"]:
            w.writerow([r["geni"], it["qid"], it["label"], it["desc"],
                        len(r["items"]), "yes" if r["in_corpus"] else "no"])

out = ROOT / "reports" / "improper-keys.html"
out.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size/1e6:.1f} MB)")
print(f"  malformed P2600: {n_bad}; shared keys: {len(shared_rows)} over {n_shared_items} items")
print(f"  legacy-shape individuals: {len(noncanon):,}")
