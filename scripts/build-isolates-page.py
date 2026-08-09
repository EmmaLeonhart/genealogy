"""Build `out/wikidata-isolates.html` from the isolate list.

Kept as a script rather than inlined into a shell heredoc because the last two
pages of this kind shipped broken — one with 504k rows carrying literal newlines
inside a JS string literal, which is a parse error, and one built from unfiltered
data. Both were found by a human looking at a blank page. A file can be
syntax-checked before it is opened; a heredoc cannot.

Reads `out/_isolates.json` (written by the full store pass) and writes a page
whose data is a JSON array, so there is no escaping to get wrong.
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>Geni-linked Wikidata people with no family recorded</title>
<style>
:root{--bg:#fff;--fg:#111;--mut:#666;--line:#e3e3e3;--acc:#0b57d0;--have:#0a7a3d}
@media(prefers-color-scheme:dark){:root{--bg:#151517;--fg:#e8e8e8;--mut:#9a9a9a;--line:#2c2c30;--acc:#8ab4f8;--have:#5bd48b}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,sans-serif}
header{padding:16px 22px;border-bottom:1px solid var(--line)}
h1{margin:0 0 4px;font-size:17px}
p{margin:0;color:var(--mut);font-size:13px;max-width:70em}
.controls{margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
input,button{padding:7px 10px;font:inherit;border:1px solid var(--line);
  border-radius:7px;background:var(--bg);color:var(--fg)}
input{width:min(360px,100%)}
button{cursor:pointer}
button[aria-pressed="true"]{border-color:var(--acc);color:var(--acc)}
#scroller{height:calc(100vh - 186px);overflow-y:auto;overflow-x:auto}
#sizer{position:relative;min-width:900px}
.row{display:flex;gap:14px;padding:0 22px;border-bottom:1px solid var(--line);
  position:absolute;left:0;right:0;height:31px;align-items:center;white-space:nowrap}
.n{color:var(--mut);width:74px;text-align:right;font-variant-numeric:tabular-nums}
.qid{width:110px}
.name{flex:1;min-width:220px;overflow:hidden;text-overflow:ellipsis}
.yrs{width:104px;color:var(--mut);font-variant-numeric:tabular-nums}
.sl{width:52px;text-align:right;color:var(--mut);font-variant-numeric:tabular-nums}
.gid{width:186px}
.have{color:var(--have);font-weight:600}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
</style></head><body>
<header>
<h1>Geni-linked Wikidata people with no family recorded</h1>
<p>Wikidata has an item and a Geni profile ID for each of these, and <strong>no
parent, spouse, child or sibling</strong> on its side. Not an error &mdash; the
genealogy was simply never added. Sorted by number of Wikipedia articles, so the
best-documented come first. <span class="have">Green</span> marks the few we
already hold; the rest would need a Geni export first.</p>
<p id="count"></p>
<div class="controls">
  <input id="q" placeholder="filter by name, QID or Geni ID&hellip;" autocomplete="off">
  <button id="mine" aria-pressed="false">only ones we already hold</button>
</div>
</header>
<div id="scroller"><div id="sizer"></div></div>
<script>
const DATA=__PAYLOAD__;
let view=DATA, onlyMine=false;
const H=31,sizer=document.getElementById("sizer"),wrap=document.getElementById("scroller"),
      q=document.getElementById("q"),count=document.getElementById("count"),
      mine=document.getElementById("mine");
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function apply(){
  const t=q.value.trim().toLowerCase();
  view=DATA.filter(function(r){
    if(onlyMine && !r[5]) return false;
    if(!t) return true;
    return r[0].toLowerCase().indexOf(t)>=0 || r[1].toLowerCase().indexOf(t)>=0 || r[2].indexOf(t)>=0;
  });
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
      +'<span class="name'+(r[5]?' have':'')+'">'+esc(r[1]||"(no label)")+'</span>'
      +'<span class="yrs">'+esc(r[3])+'</span>'
      +'<span class="sl">'+r[4]+'</span>'
      +'<span class="gid"><a href="https://www.geni.com/people/x/'+r[2]+'" target="_blank"><code>'+r[2]+'</code></a></span>'
      +'</div>';
  }
  sizer.innerHTML=h;
  count.textContent=view.length.toLocaleString()+" of "+DATA.length.toLocaleString()
    +" people \\u00b7 columns: item, name, years, Wikipedia articles, Geni profile";
}
wrap.addEventListener("scroll",draw,{passive:true});
window.addEventListener("resize",draw);
q.addEventListener("input",apply);
mine.addEventListener("click",function(){
  onlyMine=!onlyMine; mine.setAttribute("aria-pressed",String(onlyMine)); apply();
});
draw();
</script></body></html>"""


def main() -> int:
    src = ROOT / "out" / "_isolates.json"
    if not src.exists():
        print(f"{src} not found - run the store pass first", file=sys.stderr)
        return 1
    rows = json.load(io.open(src, encoding="utf-8"))
    page = PAGE.replace("__PAYLOAD__", json.dumps(rows, separators=(",", ":"), ensure_ascii=False))
    out = ROOT / "out" / "wikidata-isolates.html"
    io.open(out, "w", encoding="utf-8").write(page)

    # Hand the script to node before anyone opens it. Two earlier pages were
    # shipped broken and found by a human staring at a blank screen.
    check = ROOT / "out" / "_check_isolates.js"
    io.open(check, "w", encoding="utf-8").write(page[page.index("<script>") + 8 : page.index("</script>")])
    print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB, {len(rows):,} rows)")
    print(f"syntax-check with: node --check {check}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
