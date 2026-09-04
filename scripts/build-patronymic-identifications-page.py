"""Build the review page for every patronymic identification the name model makes.

Emma, 2026-09-04: *"Can you give me the artifact for the identifications for me to go
through?"* -- so this is a page to READ, one row per (form, token), grouped by form,
carrying example bearers because spotting a wrong identification needs the person and
not the token. `Ni Choon` is a Chinese name; `Ni` alone tells you nothing.

It opens on the largest form the 2026-09-04 widening added, because that is the part
nothing has ever been read against.

Input  reports/patronymic-identifications.tsv     one row per token per person
       reports/patronymic-forms-newly-detected.tsv  which people the widening added
Output out/patronymic-identifications.html        self-contained, no libraries

Published unlinked beside the daily batch by `scripts/build-pages-site.py`, since
GitHub Pages is the one place Emma can open a page without signing in.
"""

from __future__ import annotations

import csv
import html
import io
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
IDENTS = ROOT / "reports" / "patronymic-identifications.tsv"
OUT = ROOT / "out" / "patronymic-identifications.html"

#: How many bearers to name per token. Three is enough to spot a `Ni Choon`.
EXAMPLES = 3


def rows():
    with IDENTS.open(encoding="utf-8", newline="") as fh:
        yield from csv.DictReader(fh, delimiter="\t")


def collect():
    """(form, token) -> bearers, status, examples. Deterministic throughout."""
    by_form: dict[str, dict[str, dict]] = {}
    for r in rows():
        form, token = r["form"], r["token"]
        seen = by_form.setdefault(form, {})
        cell = seen.get(token)
        if cell is None:
            cell = seen[token] = {"n": 0, "newn": 0, "new": False, "eg": []}
        cell["n"] += 1
        if r["status"] != "established":
            cell["new"] = True
            cell["newn"] += 1
        if len(cell["eg"]) < EXAMPLES:
            name = r["display_name"].strip()
            if name and name not in cell["eg"]:
                cell["eg"].append(name)
    return by_form


def payload(by_form):
    forms = []
    for form, tokens in by_form.items():
        # Total key: bearers descending, then the token itself, so two tokens with the
        # same count never swap places between runs (CLAUDE.md, deterministic sorting).
        listed = sorted(tokens.items(), key=lambda kv: (-kv[1]["n"], kv[0]))
        forms.append({
            "form": form,
            "bearers": sum(c["n"] for c in tokens.values()),
            "tokens": len(tokens),
            "new": sum(1 for _, c in listed if c["new"]),
            "newbearers": sum(c["newn"] for _, c in listed),
            "rows": [[t, c["n"], 1 if c["new"] else 0, c["eg"]] for t, c in listed],
        })
    forms.sort(key=lambda f: (-f["bearers"], f["form"]))
    # Open on the largest form the widening added, ranked by NEW BEARERS rather than by
    # whether any exist: `-sen` gained seven tokens (trailing-dot spellings like `Simonsen.`)
    # and would otherwise win on its 162,246 established ones, landing the page on the part
    # that has been read for months instead of the part nothing has been read against.
    added = sorted((f for f in forms if f["newbearers"]),
                   key=lambda f: (-f["newbearers"], f["form"]))
    opens = (added or forms)[0]["form"] if forms else ""
    return {"forms": forms, "opens": opens}


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Patronymic identifications</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Serif:wght@600&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#fbfaf8; --panel:#fff; --ink:#1b1a17; --dim:#6b6862; --rule:#e2ded6;
  --accent:#8a3b12; --new:#b45309; --newbg:#fdf3e3;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#16151300; --bg:#161513; --panel:#1e1d1a; --ink:#eceae5; --dim:#9b978f;
  --rule:#33312c; --accent:#e0a878; --new:#e0a878; --newbg:#2a2118;
}}
:root[data-theme="dark"]{
  --bg:#161513; --panel:#1e1d1a; --ink:#eceae5; --dim:#9b978f;
  --rule:#33312c; --accent:#e0a878; --new:#e0a878; --newbg:#2a2118;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.5 "IBM Plex Sans",system-ui,-apple-system,sans-serif}
header{padding:22px 24px 16px;border-bottom:1px solid var(--rule)}
h1{margin:0 0 4px;font:600 22px/1.25 "IBM Plex Serif",Georgia,serif}
.sub{color:var(--dim);font-size:13.5px}
.wrap{display:grid;grid-template-columns:230px 1fr;gap:0;min-height:calc(100vh - 88px)}
nav{border-right:1px solid var(--rule);padding:12px 0;overflow-y:auto;
  max-height:calc(100vh - 88px);position:sticky;top:0}
nav button{display:block;width:100%;text-align:left;background:none;border:0;
  color:inherit;font:inherit;padding:7px 14px 7px 20px;cursor:pointer;
  border-left:3px solid transparent}
nav button:hover{background:var(--panel)}
nav button[aria-current="true"]{background:var(--panel);border-left-color:var(--accent);
  font-weight:600}
nav .c{color:var(--dim);font-size:12px;font-family:"IBM Plex Mono",monospace}
nav .dot{color:var(--new)}
main{padding:16px 24px 60px;min-width:0}
.bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:14px}
input[type=search]{flex:1 1 240px;min-width:0;padding:8px 11px;border:1px solid var(--rule);
  border-radius:6px;background:var(--panel);color:inherit;font:inherit}
label.chk{display:inline-flex;gap:6px;align-items:center;color:var(--dim);font-size:13.5px}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--rule);
  vertical-align:top}
th{color:var(--dim);font-size:12px;font-weight:600;text-transform:uppercase;
  letter-spacing:.04em}
td.tok{font-family:"IBM Plex Mono",monospace;font-weight:600;white-space:nowrap}
td.n{font-family:"IBM Plex Mono",monospace;text-align:right;white-space:nowrap;
  color:var(--dim)}
td.eg{color:var(--dim);font-size:13.5px}
tr.new td.tok{color:var(--new)}
tr.new{background:var(--newbg)}
.tag{display:inline-block;margin-left:8px;padding:1px 6px;border-radius:4px;
  background:var(--newbg);color:var(--new);font-size:11px;font-weight:600;
  text-transform:uppercase;letter-spacing:.04em}
.scroll{overflow-x:auto}
.empty{color:var(--dim);padding:24px 0}
@media (max-width:720px){
  .wrap{grid-template-columns:1fr}
  nav{position:static;max-height:none;border-right:0;border-bottom:1px solid var(--rule);
    display:flex;flex-wrap:wrap;padding:8px}
  nav button{width:auto;border-left:0;border-bottom:3px solid transparent;padding:6px 10px}
  nav button[aria-current="true"]{border-left:0;border-bottom-color:var(--accent)}
  td.eg{display:none}
}
</style></head><body>
<header>
  <h1>Patronymic identifications</h1>
  <div class="sub">__SUB__</div>
</header>
<div class="wrap">
  <nav id="nav" aria-label="Forms"></nav>
  <main>
    <div class="bar">
      <input type="search" id="q" placeholder="Search tokens and bearers, across every form">
      <label class="chk"><input type="checkbox" id="only"> only forms the widening added</label>
    </div>
    <div class="scroll"><table>
      <thead><tr><th>Token</th><th style="text-align:right">Bearers</th><th>Example bearers</th></tr></thead>
      <tbody id="body"></tbody>
    </table></div>
    <div class="empty" id="empty" hidden>Nothing matches.</div>
  </main>
</div>
<script type="application/json" id="data">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById("data").textContent);
const nav = document.getElementById("nav"), body = document.getElementById("body");
const q = document.getElementById("q"), only = document.getElementById("only");
const empty = document.getElementById("empty");
let current = DATA.opens;

function drawNav(){
  nav.innerHTML = "";
  for (const f of DATA.forms){
    const b = document.createElement("button");
    b.type = "button";
    b.setAttribute("aria-current", String(f.form === current));
    b.innerHTML = esc(f.form) + ' <span class="c">' + f.bearers.toLocaleString() + "</span>"
      + (f.newbearers ? ' <span class="dot" title="' + f.newbearers.toLocaleString()
          + ' identifications the widening added">&bull;</span>' : "");
    b.onclick = () => { current = f.form; drawNav(); draw(); };
    nav.appendChild(b);
  }
}
function esc(s){ return String(s).replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c])); }

function draw(){
  const term = q.value.trim().toLowerCase();
  const newOnly = only.checked;
  const forms = term ? DATA.forms : DATA.forms.filter(f => f.form === current);
  const out = [];
  for (const f of forms){
    for (const [tok, n, isNew, eg] of f.rows){
      if (newOnly && !isNew) continue;
      if (term){
        const hay = (tok + " " + f.form + " " + eg.join(" ")).toLowerCase();
        if (!hay.includes(term)) continue;
      }
      out.push('<tr class="' + (isNew ? "new" : "") + '"><td class="tok">' + esc(tok)
        + (term ? ' <span class="tag">' + esc(f.form) + "</span>" : "")
        + (isNew ? ' <span class="tag">new</span>' : "")
        + '</td><td class="n">' + n.toLocaleString() + '</td><td class="eg">'
        + esc(eg.join(" \\u00b7 ")) + "</td></tr>");
      if (out.length >= 4000) break;
    }
    if (out.length >= 4000) break;
  }
  body.innerHTML = out.join("");
  empty.hidden = out.length > 0;
}
q.addEventListener("input", draw);
only.addEventListener("change", draw);
drawNav(); draw();
</script></body></html>
"""


def main() -> int:
    if not IDENTS.exists():
        print("no %s -- run the identifications census first" % IDENTS, file=sys.stderr)
        return 1
    by_form = collect()
    data = payload(by_form)
    people = sum(f["bearers"] for f in data["forms"])
    tokens = sum(f["tokens"] for f in data["forms"])
    added = sum(f["newbearers"] for f in data["forms"])
    sub = ("%s identifications &middot; %s distinct tokens &middot; %s forms &middot; "
           "%s the 2026-09-04 widening added, shaded"
           % (f"{people:,}", f"{tokens:,}", f"{len(data['forms']):,}", f"{added:,}"))
    page = (TEMPLATE
            .replace("__SUB__", sub)
            .replace("__DATA__", html.escape(json.dumps(data, ensure_ascii=False,
                                                        separators=(",", ":")),
                                             quote=False)))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".html.tmp")
    with io.open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(page)
    os.replace(tmp, OUT)
    print("%s -- %s identifications, %s tokens, %s forms, %s bytes"
          % (OUT, f"{people:,}", f"{tokens:,}", len(data["forms"]), f"{len(page):,}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
