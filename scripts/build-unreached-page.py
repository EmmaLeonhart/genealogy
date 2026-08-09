"""Build `out/wikidata-unreached.html` from `reports/wikidata-unreached.tsv`.

This page went missing once. It was written straight into gitignored `out/` by
the session that first made it, and `reports/wikidata-unreached.md` said
"regenerate rather than commit" while no script to regenerate it existed. A
fresh clone therefore lost it with no way back. This file is that way back: the
source data is tracked, so the page is reproducible from a clean checkout with
no store pass and no network.

Same shape as `build-isolates-page.py` — virtual-scrolled, data as a JSON array
rather than a string literal, and the script handed to `node --check` before
anyone opens it. Both earlier pages of this kind shipped broken and were found
by a human staring at a blank screen.

Columns are what the TSV holds: item and Geni profile, sorted by QID. Names and
years would need a pass over `wikidata/items/`; this runs in about a second
without one.
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>Wikidata items with a Geni ID we have never exported</title>
<style>
:root{--bg:#fff;--fg:#111;--mut:#666;--line:#e3e3e3;--acc:#0b57d0}
@media(prefers-color-scheme:dark){:root{--bg:#151517;--fg:#e8e8e8;--mut:#9a9a9a;--line:#2c2c30;--acc:#8ab4f8}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,sans-serif}
header{padding:16px 22px;border-bottom:1px solid var(--line)}
h1{margin:0 0 4px;font-size:17px}
p{margin:0;color:var(--mut);font-size:13px;max-width:70em}
.controls{margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
input{padding:7px 10px;font:inherit;border:1px solid var(--line);
  border-radius:7px;background:var(--bg);color:var(--fg);width:min(360px,100%)}
#scroller{height:calc(100vh - 168px);overflow-y:auto;overflow-x:auto}
#sizer{position:relative;min-width:560px}
.row{display:flex;gap:14px;padding:0 22px;border-bottom:1px solid var(--line);
  position:absolute;left:0;right:0;height:31px;align-items:center;white-space:nowrap}
.n{color:var(--mut);width:74px;text-align:right;font-variant-numeric:tabular-nums}
.qid{width:120px}
.gid{width:200px}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
</style></head><body>
<header>
<h1>Wikidata items with a Geni ID we have never exported</h1>
<p>Wikidata names a Geni profile for each of these and our tree does not hold
it. Click the Geni link to open the profile and run an export that would reach
it. Sorted by item.</p>
<p id="count"></p>
<div class="controls">
  <input id="q" placeholder="filter by QID or Geni ID&hellip;" autocomplete="off">
</div>
</header>
<div id="scroller"><div id="sizer"></div></div>
<script>
const DATA=__PAYLOAD__;
let view=DATA;
const H=31,sizer=document.getElementById("sizer"),wrap=document.getElementById("scroller"),
      q=document.getElementById("q"),count=document.getElementById("count");
function apply(){
  const t=q.value.trim().toLowerCase();
  view=t?DATA.filter(function(r){
    return r[0].toLowerCase().indexOf(t)>=0 || r[1].indexOf(t)>=0;
  }):DATA;
  wrap.scrollTop=0; draw();
}
function draw(){
  const top=wrap.scrollTop,
        first=Math.max(0,Math.floor(top/H)-6),
        last=Math.min(view.length,Math.ceil((top+wrap.clientHeight)/H)+6);
  sizer.style.height=(view.length*H)+"px";
  let h="";
  for(let i=first;i<last;i++){
    const r=view[i];
    h+='<div class="row" style="top:'+(i*H)+'px">'
      +'<span class="n">'+(i+1).toLocaleString()+'</span>'
      +'<span class="qid"><a href="https://www.wikidata.org/wiki/'+r[0]+'" target="_blank">'+r[0]+'</a></span>'
      +'<span class="gid"><a href="https://www.geni.com/people/x/'+r[1]+'" target="_blank"><code>'+r[1]+'</code></a></span>'
      +'</div>';
  }
  sizer.innerHTML=h;
  count.textContent=view.length.toLocaleString()+" of "+DATA.length.toLocaleString()
    +" pairs \\u00b7 columns: Wikidata item, Geni profile to export from";
}
wrap.addEventListener("scroll",draw,{passive:true});
window.addEventListener("resize",draw);
q.addEventListener("input",apply);
draw();
</script></body></html>"""


def main() -> int:
    src = ROOT / "reports" / "wikidata-unreached.tsv"
    if not src.exists():
        print(f"{src} not found", file=sys.stderr)
        return 1

    rows = []
    with io.open(src, encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        if header != ["qid", "geni_id"]:
            print(f"unexpected header {header!r}", file=sys.stderr)
            return 1
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            qid, _, geni_id = line.partition("\t")
            rows.append([qid, geni_id])

    out_dir = ROOT / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    page = PAGE.replace("__PAYLOAD__", json.dumps(rows, separators=(",", ":"), ensure_ascii=False))
    out = out_dir / "wikidata-unreached.html"
    io.open(out, "w", encoding="utf-8").write(page)

    # Hand the script to node before anyone opens it.
    check = out_dir / "_check_unreached.js"
    io.open(check, "w", encoding="utf-8").write(page[page.index("<script>") + 8 : page.index("</script>")])
    print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB, {len(rows):,} rows)")
    print(f"syntax-check with: node --check {check}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
