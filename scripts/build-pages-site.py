"""Generate the GitHub Pages site that documents what this repo does.

    py scripts/build-pages-site.py

**Emma, 2026-09-01:** *"a github pages site built with actions that documents generally what the
repo is doing with different things, its data modeling and algorithms and such."*

**Generated from the repo, not written by hand.** The queue item is explicit about why: prose
written once goes stale, and `CLAUDE.md`'s sections and the module docstrings already carry the
content. So the headings and the standing rules are lifted from `CLAUDE.md`, the corpus figures
are **counted** from the files at build time, and the algorithm descriptions come from the
docstrings of the scripts that implement them. Nothing here restates a number from memory.

**Counted, never quoted:** exports on disk, people and families in the derived tables, ledger
size, `P2600` coverage. If a figure moves, the next build says so without anyone editing prose.

Writes `out/site/index.html`. The workflow in `.github/workflows/pages.yml` publishes it.
"""
from __future__ import annotations

import csv
import datetime
import gzip
import html
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

TAB = chr(9)
OUT = ROOT / "out" / "site" / "index.html"
CLAUDE = ROOT / "CLAUDE.md"

#: The batches she actually runs. Emma, 2026-09-02: *"idk what a github artifact is but a
#: non-attached zip file in the email is way worse than having the quickstatements just on a
#: page on github pages lol, that's kinda why I made github pages."* So the QuickStatements go
#: ON the site as text she can select and copy, not into a zip she has to find in a run.
#:
#: `pipeline.yml` calls the Pages workflow AFTER `--compose`, so the page carries the batch
#: that run just built rather than whatever the last schedule happened to see.
BATCHES = [
    ("The daily batch", "reports/wikidata-garborg-day.qs"),
    ("Name items", "reports/wikidata-garborg-name-items.qs"),
]


def esc(s):
    return html.escape(str(s or ""), quote=True)


def n(x):
    return format(x, ",")


def count_lines(path, gz_fallback=True):
    """Rows in a CSV/TSV, reading the committed `.gz` when the plain file is absent."""
    p = ROOT / path
    if p.exists():
        with io.open(p, encoding="utf-8", errors="replace") as fh:
            return max(sum(1 for _ in fh) - 1, 0)
    gz = ROOT / (path + ".gz")
    if gz_fallback and gz.exists():
        with gzip.open(gz, "rt", encoding="utf-8", errors="replace") as fh:
            return max(sum(1 for _ in fh) - 1, 0)
    return None


def facts():
    """Every figure on the page, counted at build time."""
    f = {}
    f["exports"] = len(list((ROOT / "exports").rglob("*.ged")))
    f["people"] = count_lines("reports/derived-labels.csv")
    # **NOT a family count.** derived-family.csv is one row PER PERSON carrying their kin, so
    # reading its length as "families" printed 1,451,964 -- exactly the people figure, which is
    # what gave it away. The honest thing this file measures is how many people have kin at all.
    f["with_kin"] = 0
    fam = ROOT / "reports" / "derived-family.csv"
    if fam.exists():
        with io.open(fam, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if any((r.get(k) or "").strip() for k in ("father","mother","spouses","children")):
                    f["with_kin"] += 1
    f["ledger"] = count_lines("reports/garborg-qids.tsv")
    f["paths"] = len(list((ROOT / "paths").glob("*.tsv"))) if (ROOT / "paths").exists() else 0
    f["p2600"] = count_lines("out/wikidata/p2600-all.tsv")
    f["han_chars"] = count_lines("reports/han-readings.tsv")
    f["ja_labels"] = None
    p = ROOT / "reports" / "label-ja.tsv"
    if p.exists():
        with io.open(p, encoding="utf-8", newline="") as fh:
            f["ja_labels"] = sum(1 for r in csv.DictReader(fh, delimiter=TAB) if r.get("label_ja"))
    f["scripts"] = len(list((ROOT / "scripts").glob("*.py")))
    return f


def claude_sections():
    """`[(heading, first paragraph)]` for the standing rules, straight out of `CLAUDE.md`.

    The headings ARE the documentation -- they are written as rules with their reasons, and
    lifting them keeps the site honest to whatever the repo currently believes.
    """
    if not CLAUDE.exists():
        return []
    out, heading, buf = [], None, []
    for line in io.open(CLAUDE, encoding="utf-8"):
        if line.startswith("### "):
            if heading and buf:
                out.append((heading, " ".join(buf).strip()))
            heading, buf = line[4:].strip(), []
        elif heading is not None and line.strip() and not line.startswith(("#", "|", "```")):
            if len(" ".join(buf)) < 320:
                buf.append(line.strip())
    if heading and buf:
        out.append((heading, " ".join(buf).strip()))
    return out


def docstring_of(rel):
    """The first paragraph of a script's module docstring."""
    p = ROOT / rel
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8", errors="replace")
    m = re.match(r'\s*"""(.*?)"""', text, re.S)
    if not m:
        return None
    body = m.group(1).strip()
    first = body.split("\n\n")[0].replace("\n", " ").strip()
    return re.sub(r"\s+", " ", first)


#: The algorithms the queue item asks for, each named by the file that implements it so the
#: description cannot drift from the code.
ALGORITHMS = [
    ("The daily ring", "scripts/build-garborg-day.py"),
    ("The zipper join", "scripts/zipper-join.py"),
    ("Provenance chains", "scripts/zipper-provenance.py"),
    ("Where to export from next", "src/genimerge/density.py"),
    ("Reaching modern times", "src/genimerge/descendants.py"),
    ("Han character readings", "scripts/build-han-readings.py"),
    ("Japanese labels", "scripts/build-ja-labels.py"),
    ("The merges page", "scripts/build-merges-page.py"),
]

MODELLING = [
    ("A person", "P31 Q5 <em>human</em>, P21 <em>sex or gender</em>, P2600 <em>Geni.com profile "
     "ID</em> with P1810 <em>subject named as</em> as a qualifier carrying what Geni renders."),
    ("A name", "P735 <em>given name</em> and P734 <em>family name</em> point at name ITEMS, "
     "ordered by P1545 <em>series ordinal</em>. The first given name carries P7452 → Q3409033 "
     "<em>usual forename</em>; a middle name carries P3831 → Q245025."),
    ("A patronymic", "P5056 <em>patronym or matronym</em> — its own property, parallel to P735, "
     "never a qualifier on one. It carries P144 <em>based on</em> pointing at the PERSON that "
     "link names: the father, then the grandfather for a chained patronymic."),
    ("A date", "A GEDCOM modifier becomes a qualifier. ABT/EST/CAL → P1480 <em>sourcing "
     "circumstances</em> = Q5727902 <em>circa</em>; BEF → P1326 <em>latest date</em>; AFT → "
     "P1319 <em>earliest date</em>; BET x AND y → both."),
    ("The label", "<code>mul</code> is the real label and carries the MARRIED name; the birth "
     "name is an <code>Amul</code> alias. No <code>Aen</code> is ever added, and no descriptions "
     "go on people."),
    ("A redacted person", "The person is created and the structure kept — Geni ID, sex, parents, "
     "children, dates — but <em>Private</em> never becomes a label. An unnamed person keeps the "
     "NN marker in <code>mul</code> and gains a descriptive label in other languages."),
]


BATCH_PAGE = """
<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s — QuickStatements</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
:root{--bg:#f4f6f8;--surface:#fff;--ink:#141820;--muted:#5f6875;--line:#dce1e8;--accent:#2f4f8f}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0e1116;--surface:#161a21;--ink:#e7eaf0;--muted:#98a1b0;--line:#262d38;--accent:#8aa9e8}}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);margin:0;padding:24px 20px 60px;
  font:15px/1.6 "IBM Plex Sans",system-ui,sans-serif}
.wrap{max-width:1000px;margin:0 auto}
h1{font:600 22px/1.2 "IBM Plex Sans",sans-serif;margin:0 0 4px}
.sub{color:var(--muted);font-size:13.5px;margin-bottom:16px}
.bar{display:flex;gap:9px;align-items:center;margin-bottom:14px;flex-wrap:wrap}
button,a.btn{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:9px 15px;
  font:500 13.5px "IBM Plex Sans",sans-serif;cursor:pointer;text-decoration:none}
pre{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px;
  overflow:auto;max-height:74vh;font:400 12.5px/1.5 "IBM Plex Mono",monospace;
  white-space:pre;tab-size:8}
a{color:var(--accent)}
</style></head><body><div class="wrap">
<h1>%s</h1>
<p class="sub">%s statement lines · generated %s · paste into
<a href="https://quickstatements.toolforge.org/#/batch" target="_blank" rel="noopener">QuickStatements</a>
(version 1 syntax, tab-separated)</p>
<div class="bar">
  <button id="copy">Copy all</button>
  <a class="btn" href="./">Back to the site</a>
  <span class="sub" id="said"></span>
</div>
<pre id="qs">%s</pre>
<script>
document.getElementById("copy").addEventListener("click", function () {
  var t = document.getElementById("qs").textContent;
  navigator.clipboard.writeText(t).then(function () {
    document.getElementById("said").textContent = "copied " + t.split("
").length + " lines";
  }, function () {
    document.getElementById("said").textContent = "could not copy - select the text instead";
  });
});
</script>
</div></body></html>
"""


def batch_pages():
    """`[(title, rel, statements, html filename)]`, one page per QuickStatements batch."""
    made = []
    for title, rel in BATCHES:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        stmts = sum(1 for l in text.splitlines()
                    if l.strip() and not l.lstrip().startswith("#"))
        name = Path(rel).stem + ".html"
        page = BATCH_PAGE % (esc(title), esc(title), n(stmts),
                             datetime.date.today().isoformat(), esc(text))
        (OUT.parent / name).parent.mkdir(parents=True, exist_ok=True)
        io.open(OUT.parent / name, "w", encoding="utf-8", newline="").write(page)
        made.append((title, rel, stmts, name))
    return made


def main() -> int:
    f = facts()
    batches = batch_pages()
    secs = claude_sections()
    batch_html = "".join(
        '<article><h3><a href="%s">%s</a></h3><p>%s statement lines, ready to paste '
        'into QuickStatements &mdash; on the page, not in a zip.</p>'
        '<p class="src"><code>%s</code></p></article>'
        % (esc(name), esc(title), n(stmts), esc(rel))
        for title, rel, stmts, name in batches) or (
        '<article><p>No batch has been generated yet.</p></article>')
    print("%d rule sections read from CLAUDE.md" % len(secs))

    rows = "".join(
        '<div class="stat"><b>%s</b><span>%s</span></div>' % (esc(v), esc(k))
        for k, v in [
            ("GEDCOM exports", n(f["exports"])),
            ("people in the tree", n(f["people"]) if f["people"] else "—"),
            ("people with recorded kin", n(f["with_kin"]) if f["with_kin"] else "—"),
            ("relationship paths", n(f["paths"])),
            ("Geni IDs on Wikidata", n(f["p2600"]) if f["p2600"] else "—"),
            ("items in the ledger", n(f["ledger"]) if f["ledger"] else "—"),
            ("Han characters read", n(f["han_chars"]) if f["han_chars"] else "—"),
            ("Japanese labels", n(f["ja_labels"]) if f["ja_labels"] else "—"),
            ("generator scripts", n(f["scripts"])),
        ])

    algos = ""
    for title, rel in ALGORITHMS:
        d = docstring_of(rel)
        if not d:
            continue
        algos += ('<article><h3>%s</h3><p>%s</p><p class="src"><code>%s</code></p></article>'
                  % (esc(title), esc(d[:400]), esc(rel)))

    model = "".join('<article><h3>%s</h3><p>%s</p></article>' % (esc(t), body)
                    for t, body in MODELLING)

    # The standing rules, the ones whose headings read as rules rather than as history.
    wanted = [s for s in secs if len(s[0]) < 96 and not s[0].lower().startswith("historical")]
    rules = "".join('<details><summary>%s</summary><p>%s</p></details>'
                    % (esc(h), esc(p[:400])) for h, p in wanted[:40])

    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>geni — a genealogy reconciled against Wikidata</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
:root{--bg:#f4f6f8;--surface:#fff;--raise:#eef1f5;--ink:#141820;--muted:#5f6875;
  --line:#dce1e8;--accent:#2f4f8f}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0e1116;--surface:#161a21;--raise:#1d222b;--ink:#e7eaf0;--muted:#98a1b0;
  --line:#262d38;--accent:#8aa9e8}}
:root[data-theme="dark"]{--bg:#0e1116;--surface:#161a21;--raise:#1d222b;--ink:#e7eaf0;
  --muted:#98a1b0;--line:#262d38;--accent:#8aa9e8}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);margin:0;padding:0 20px 80px;
  font:16px/1.6 "IBM Plex Sans",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:860px;margin:0 auto}
header{padding:56px 0 8px}
h1{font:600 34px/1.15 "Newsreader",Georgia,serif;margin:0 0 10px;letter-spacing:-.01em}
.lede{color:var(--muted);font-size:17px;max-width:62ch}
h2{font:600 13px/1 "IBM Plex Sans",sans-serif;letter-spacing:.09em;text-transform:uppercase;
  color:var(--muted);margin:46px 0 14px;padding-bottom:9px;border-bottom:1px solid var(--line)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px}
.stat b{display:block;font:600 22px/1.1 "IBM Plex Sans",sans-serif;
  font-variant-numeric:tabular-nums}
.stat span{color:var(--muted);font-size:13px}
article{background:var(--surface);border:1px solid var(--line);border-radius:10px;
  padding:15px 17px;margin:0 0 10px}
article h3{font:600 16px/1.3 "IBM Plex Sans",sans-serif;margin:0 0 6px}
article p{margin:0;color:var(--muted);font-size:14.5px}
.src{margin-top:8px!important;font-size:12.5px}
code{font-family:"IBM Plex Mono",monospace;font-size:.92em;background:var(--raise);
  padding:1px 5px;border-radius:4px}
details{background:var(--surface);border:1px solid var(--line);border-radius:10px;
  padding:12px 15px;margin:0 0 8px}
summary{cursor:pointer;font-weight:500}
details p{color:var(--muted);font-size:14px;margin:9px 0 0}
footer{color:var(--muted);font-size:13px;margin-top:52px;padding-top:18px;
  border-top:1px solid var(--line)}
a{color:var(--accent)}
</style></head><body><div class="wrap">
<header>
<h1>geni</h1>
<p class="lede">Merge every Geni.com GEDCOM export into one genealogy, reconcile it against
Wikidata, and generate the edits that create the people Wikidata is missing. The Geni profile
ID is the primary key throughout, so joining is exact rather than fuzzy name matching.</p>
</header>

<h2>The QuickStatements to run</h2>
%s

<h2>The corpus, counted at build time</h2>
<div class="stats">%s</div>

<h2>How a person is modelled</h2>
%s

<h2>The algorithms</h2>
<p class="lede" style="margin-bottom:14px">Each described by the docstring of the file that
implements it, so the description cannot drift from the code.</p>
%s

<h2>The standing rules</h2>
<p class="lede" style="margin-bottom:14px">Lifted from <code>CLAUDE.md</code>, which records
the decisions this project runs on and why each was made.</p>
%s

<footer>Generated by <code>scripts/build-pages-site.py</code> from the repository itself —
every figure above is counted at build time rather than written down.</footer>
</div></body></html>
""" % (batch_html, rows, model, algos, rules)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="").write(page)
    print("wrote %s (%s bytes)" % (OUT.relative_to(ROOT), n(len(page))))
    print("   %d algorithm docstrings, %d rule sections, %d stats"
          % (algos.count("<article>"), rules.count("<details>"), rows.count("<div class=")))
    for k, v in f.items():
        print("   %-14s %s" % (k, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
