"""A local ancestry explorer: the path between any two people, and whether an id is in a file.

    python scripts/explore.py [--port 8765]      then open http://127.0.0.1:8765/

Asked for 2026-10-02: *"I do not have a decent ui to actually do this analysis on my own"*.
Read-only over the tree files, bound to 127.0.0.1, nothing written anywhere.

Three graphs, picked on the page:

* **tree**: the synoptic tree, `reports/derived-family.csv`. It already holds the FamilySearch
  people the renders put in it (`FS` + the id without its dash) and every paired one on its Geni id.
* **familysearch**: one raw download under `gedcom/familysearch/`, keyed on `_FSFTID`.
* **both**: the two joined by the tree's own `fs_id` rows (`reports/derived-family-sources.csv`),
  an identity step that costs nothing.

**Contested and impossible links stay in the graph, marked.** A second father or mother in the
`fathers`/`mothers` columns is *contested*; a parent `derive-family.py` dropped as impossible
(`reports/dropped-impossible-parents.csv`) is put back as *impossible*. Either can be avoided with
a checkbox, which reroutes the walk rather than hiding the answer.
"""
from __future__ import annotations

import argparse
import collections
import csv
import html
import json
import re
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAMILY = ROOT / "reports" / "derived-family.csv"
LABELS = ROOT / "reports" / "derived-labels.csv"
SOURCES = ROOT / "reports" / "derived-family-sources.csv"
IMPOSSIBLE = ROOT / "reports" / "dropped-impossible-parents.csv"
LEDGER = ROOT / "reports" / "garborg-qids.tsv"
P2600_ALL = ROOT / "out" / "wikidata" / "p2600-all.tsv"
P2889_ALL = ROOT / "out" / "wikidata" / "p2889-all.tsv"
FS_DIR = ROOT / "gedcom" / "familysearch"
FS_DEFAULT = "rootsmagic-PFR5-LDS-2026-09-30.ged"

csv.field_size_limit(10**9)


def split(cell):
    """` | ` is the separator and the strip is load-bearing (`CLAUDE.md`)."""
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def fs_key(fs_id):
    """`LHVW-YT5` -> `FSLHVWYT5`, the tree's key for a FamilySearch person."""
    return "FS" + fs_id.replace("-", "")


def fs_dashed(key):
    raw = key[2:]
    return raw[:4] + "-" + raw[4:]


class Graph:
    """Edges carry a relation read from the FIRST id's side and a mark: '', contested, impossible."""

    def __init__(self):
        self.adj = collections.defaultdict(dict)  # a -> {b: (relation, mark)}
        self.names = {}

    def link(self, child, parent, slot, mark=""):
        rel = "father" if slot == "father" else "mother"
        self._put(child, parent, rel, mark)
        self._put(parent, child, "child", mark)

    def spouse(self, a, b):
        self._put(a, b, "spouse", "")
        self._put(b, a, "spouse", "")

    def _put(self, a, b, rel, mark):
        old = self.adj[a].get(b)
        # A plain edge beats a marked one: if any source asserts the link cleanly, it is clean.
        if old is None or (old[1] and not mark):
            self.adj[a][b] = (rel, mark)


def load_tree():
    g = Graph()
    with open(FAMILY, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            c = row["geni_id"]
            for slot in ("father", "mother"):
                main = row.get(slot) or ""
                for p in split(row.get(slot + "s")) or split(main):
                    g.link(c, p, slot, "" if p == main else "contested")
            for s in split(row.get("spouses")):
                g.spouse(c, s)
            for k in split(row.get("children")):
                g._put(c, k, "child", "")
                g.adj[k].setdefault(c, ("parent", ""))
    if IMPOSSIBLE.exists():
        with open(IMPOSSIBLE, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                g.link(row["child"], row["parent"], row["slot"], "impossible")
    with open(LABELS, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            g.names[row["geni_id"]] = row.get("label_en") or row.get("label_mul") or ""
    return g


def load_fs(path):
    """One raw FamilySearch download, keyed `FS` + `_FSFTID` like the tree."""
    recs, cur = {}, None
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        for line in fh:
            m = re.match(r"0 (@[^@]+@) (\w+)", line)
            if m:
                cur = recs.setdefault(m.group(1), {"type": m.group(2), "lines": []})
            elif cur is not None:
                cur["lines"].append(line.rstrip("\r\n"))
    key, g = {}, Graph()
    for x, r in recs.items():
        if r["type"] != "INDI":
            continue
        fid = next((l.split()[-1] for l in r["lines"] if "_FSFTID" in l), "")
        key[x] = fs_key(fid) if fid else "FSX" + x.strip("@")
        name = next((l[7:] for l in r["lines"] if l.startswith("1 NAME ")), "")
        g.names[key[x]] = name.replace("/", "").strip()
    for r in recs.values():
        if r["type"] != "FAM":
            continue
        tags = collections.defaultdict(list)
        for l in r["lines"]:
            parts = l.split()
            if len(parts) == 3 and parts[0] == "1" and parts[2] in key:
                tags[parts[1]].append(key[parts[2]])
        for h in tags["HUSB"]:
            for w in tags["WIFE"]:
                g.spouse(h, w)
        for k in tags["CHIL"]:
            for h in tags["HUSB"]:
                g.link(k, h, "father")
            for w in tags["WIFE"]:
                g.link(k, w, "mother")
    return g


def load_qids():
    geni, fs = {}, {}
    for path in (LEDGER,):
        with open(path, encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                if row.get("qid"):
                    geni[row["geni_id"]] = row["qid"]
    for path, out, conv in ((P2600_ALL, geni, str), (P2889_ALL, fs, fs_key)):
        if path.exists():
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    p = line.rstrip("\n").split("\t")
                    if len(p) >= 2 and p[0].startswith("Q"):
                        out.setdefault(conv(p[1]), p[0])
    return {**fs, **geni}


def identities():
    """Tree id -> FamilySearch key, from the tree's own `fs_id` rows."""
    out = collections.defaultdict(set)
    if SOURCES.exists():
        with open(SOURCES, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row["relation"] == "fs_id":
                    out[row["geni_id"]].add(fs_key(row["relative"]))
    return out


class Explorer:
    def __init__(self):
        print("loading the synoptic tree ...", flush=True)
        self.tree = load_tree()
        print(f"  {len(self.tree.adj):,} people", flush=True)
        self.qids = load_qids()
        self.ident = identities()
        self.fs = {}

    def fs_graph(self, name):
        path = (FS_DIR / name).resolve()
        if path.parent != FS_DIR.resolve() or not path.exists():
            raise ValueError(f"no FamilySearch file {name!r} in gedcom/familysearch/")
        if name not in self.fs:
            self.fs[name] = load_fs(path)
        return self.fs[name]

    def resolve(self, raw):
        """A Geni id, a FamilySearch id (dashed or not), or a QID, to a node key."""
        raw = raw.strip()
        if re.fullmatch(r"Q\d+", raw):
            hits = [k for k, q in self.qids.items() if q == raw]
            return hits[0] if hits else raw
        if raw.isdigit():
            return raw
        if raw.upper().startswith("FS"):
            return raw.upper()
        return fs_key(raw.upper())

    def walk(self, a, b, graph, fs_file, avoid):
        graphs = []
        if graph in ("tree", "both"):
            graphs.append(self.tree)
        if graph in ("familysearch", "both"):
            graphs.append(self.fs_graph(fs_file))

        def neighbours(x):
            for g in graphs:
                for y, (rel, mark) in g.adj.get(x, {}).items():
                    if mark and mark in avoid:
                        continue
                    yield y, rel, mark
            if graph == "both":
                for y in self.ident.get(x, ()):
                    yield y, "same person (FamilySearch)", ""
                if x.startswith("FS"):
                    for y in self._rev_ident().get(x, ()):
                        yield y, "same person (tree)", ""

        a, b = self.resolve(a), self.resolve(b)
        for who in (a, b):
            if not any(who in g.adj for g in graphs):
                return {"error": f"{who} is not in the chosen graph at all: an absent person, "
                                 f"not an absent path"}
        prev, seen, queue = {}, {a}, collections.deque([a])
        while queue and b not in seen:
            cur = queue.popleft()
            for nxt, rel, mark in sorted(neighbours(cur)):
                if nxt not in seen:
                    seen.add(nxt)
                    prev[nxt] = (cur, rel, mark)
                    queue.append(nxt)
        if b not in seen:
            return {"error": f"no path: {len(seen):,} people are reachable from {a}, "
                             f"and {b} is not among them"}
        steps, x = [], b
        while x != a:
            p, rel, mark = prev[x]
            steps.append((x, rel, mark))
            x = p
        steps.append((a, "", ""))
        steps.reverse()
        return {"steps": [self.describe(x, rel, mark, graphs) for x, rel, mark in steps]}

    _rev = None

    def _rev_ident(self):
        if self._rev is None:
            self._rev = collections.defaultdict(set)
            for g, fss in self.ident.items():
                for f in fss:
                    self._rev[f].add(g)
        return self._rev

    def describe(self, x, rel, mark, graphs):
        name = next((g.names[x] for g in graphs if g.names.get(x)), "") or self.tree.names.get(x, "")
        links = {}
        if x.isdigit():
            links["Geni"] = f"https://www.geni.com/people/x/{x}"
        fss = [x] if x.startswith("FS") and not x.startswith("FSX") else sorted(self.ident.get(x, ()))
        for f in fss:
            links[f"FamilySearch {fs_dashed(f)}"] = \
                f"https://www.familysearch.org/tree/person/details/{fs_dashed(f)}"
        q = self.qids.get(x) or next((self.qids[f] for f in fss if f in self.qids), "")
        if q:
            links[f"Wikidata {q}"] = f"https://www.wikidata.org/wiki/{q}"
        return {"id": x, "name": name, "relation": rel, "mark": mark, "links": links}

    def lookup(self, raw, where, fs_file):
        key = self.resolve(raw)
        if where == "tree":
            g = self.tree
        else:
            g = self.fs_graph(fs_file)
        present = key in g.adj or key in g.names
        return {"id": key, "present": present, "name": g.names.get(key, ""),
                "file": "reports/derived-family.csv" if where == "tree"
                else f"gedcom/familysearch/{fs_file}"}


PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ancestry explorer</title><style>
:root{--bg:#fff;--fg:#1d1d1f;--mut:#6b6b70;--line:#ddd;--warn:#b25c00;--bad:#b00020;--acc:#0b57d0}
@media (prefers-color-scheme:dark){:root{--bg:#161618;--fg:#ececf0;--mut:#9a9aa2;--line:#333;
--warn:#f0a040;--bad:#ff6b7f;--acc:#8ab4ff}}
body{background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif;margin:0;padding:16px;max-width:900px}
h1{font-size:20px;margin:0 0 12px}fieldset{border:1px solid var(--line);border-radius:8px;margin:0 0 14px;padding:10px 12px}
input,select,button{font:inherit;padding:6px 8px;margin:3px 4px 3px 0;max-width:100%}
a{color:var(--acc)}.mut{color:var(--mut)}.contested{color:var(--warn);font-weight:600}
.impossible{color:var(--bad);font-weight:600}ol{padding-left:22px}li{margin:6px 0}
</style></head><body><h1>Ancestry explorer</h1>
<fieldset><legend>Path between two people</legend>
<input id=a placeholder="Geni id, FamilySearch id or QID" size=28>
<input id=b placeholder="Geni id, FamilySearch id or QID" size=28><br>
<select id=graph><option value=tree>synoptic tree</option><option value=familysearch>FamilySearch file</option>
<option value=both>both, joined</option></select>
<select id=fs>FSFILES</select><br>
<label><input type=checkbox id=nc> avoid contested parents</label>
<label><input type=checkbox id=ni checked> avoid impossible parents</label><br>
<button onclick=path()>Find path</button></fieldset>
<fieldset><legend>Is this id in a file?</legend>
<input id=q placeholder="Geni id, FamilySearch id or QID" size=28>
<select id=where><option value=tree>synoptic tree</option><option value=familysearch>FamilySearch file (above)</option></select>
<button onclick=look()>Check</button></fieldset>
<div id=out></div><script>
const $=id=>document.getElementById(id), esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
async function get(u){$('out').innerHTML='<p class=mut>working ...</p>';const r=await fetch(u);return r.json()}
async function path(){const av=[$('nc').checked?'contested':'',$('ni').checked?'impossible':''].filter(Boolean).join(',');
const d=await get(`/path?a=${encodeURIComponent($('a').value)}&b=${encodeURIComponent($('b').value)}&graph=${$('graph').value}&fs=${encodeURIComponent($('fs').value)}&avoid=${av}`);
if(d.error){$('out').innerHTML=`<p class=impossible>${esc(d.error)}</p>`;return}
$('out').innerHTML=`<p>${d.steps.length} people, ${d.steps.length-1} steps</p><ol>`+d.steps.map(s=>
`<li>${s.relation?`<span class="mut ${esc(s.mark)}">${esc(s.relation)}${s.mark?' ('+esc(s.mark)+')':''}:</span> `:''}<b>${esc(s.name||'(no name)')}</b> <span class=mut>${esc(s.id)}</span><br>`+
Object.entries(s.links).map(([k,v])=>`<a href="${esc(v)}" target=_blank rel=noopener>${esc(k)}</a>`).join(' · ')+'</li>').join('')+'</ol>'}
async function look(){const d=await get(`/lookup?q=${encodeURIComponent($('q').value)}&where=${$('where').value}&fs=${encodeURIComponent($('fs').value)}`);
$('out').innerHTML=`<p>${esc(d.id)} is <b>${d.present?'in':'NOT in'}</b> ${esc(d.file)}${d.name?' as '+esc(d.name):''}.</p>`}
</script></body></html>"""


def serve(port):
    ex = Explorer()
    files = sorted(p.name for p in FS_DIR.glob("*.ged") if p.stat().st_size)
    opts = "".join(f'<option{" selected" if f == FS_DEFAULT else ""}>{html.escape(f)}</option>'
                   for f in files)
    page = PAGE.replace("FSFILES", opts).encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            u = urllib.parse.urlparse(self.path)
            q = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
            try:
                if u.path == "/":
                    return self.send(page, "text/html; charset=utf-8")
                if u.path == "/path":
                    out = ex.walk(q.get("a", ""), q.get("b", ""), q.get("graph", "tree"),
                                  q.get("fs", FS_DEFAULT), set(filter(None, q.get("avoid", "").split(","))))
                elif u.path == "/lookup":
                    out = ex.lookup(q.get("q", ""), q.get("where", "tree"), q.get("fs", FS_DEFAULT))
                else:
                    return self.send(b"not found", "text/plain", 404)
            except ValueError as exc:
                out = {"error": str(exc)}
            self.send(json.dumps(out).encode("utf-8"), "application/json")

        def send(self, body, ctype, code=200):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    print(f"open http://127.0.0.1:{port}/", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--port", type=int, default=8765)
    serve(ap.parse_args().port)


if __name__ == "__main__":
    sys.exit(main())
