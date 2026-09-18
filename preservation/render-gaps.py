"""Render preservation/farm-ancestors.json as the Rogaland gaps page."""
import json, pathlib, html

d = json.loads(pathlib.Path("preservation/farm-ancestors.json").read_text(encoding="utf-8"))
c = d["counts"]
E = html.escape

def links(ids, first="open on Geni"):
    if not ids:
        return '<span class="noid">not in Geni</span>'
    out = []
    for i, g in enumerate(ids[:3]):
        txt = first if i == 0 else "alt %d" % (i + 1)
        out.append('<a href="https://www.geni.com/people/x/%s" target="_blank" rel="noopener">%s</a>'
                   % (E(g), E(txt)))
    return " &middot; ".join(out)

divs = []
for x in d["divergences"]:
    down = " &rarr; ".join(E(s["name"]) for s in x["down"]) or "Richard Borsheim"
    par = "".join('<li class="miss">%s</li>' % E(p) for p in x["missing_parents"])
    divs.append(
        '<article class="brk"><div class="brk-hd"><span class="gen">gen %d</span>'
        '<h3>%s</h3><span class="go">%s</span></div><div class="brk-body">'
        '<div><span class="lbl">descent to Richard</span><p class="down">&darr; %s</p></div>'
        '<div><span class="lbl">parents Hethel gives, Geni lacks</span><ul>%s</ul></div>'
        '</div></article>' % (x["gen"], E(x["name"]), links(x["ids"]), down, par))

gens = []
addable = 0
for g, rows in sorted(d["missing_by_gen"].items(), key=lambda kv: int(kv[0])):
    if int(g) > 30:
        continue
    items = []
    n_link = 0
    for r in rows:
        if r["child_ids"]:
            n_link += 1
            items.append('<li><span class="mn">%s</span>'
                         '<span class="via">add via %s &nbsp;%s</span></li>'
                         % (E(r["name"]), E(r["child"]), links(r["child_ids"], "open")))
        else:
            items.append('<li><span class="mn dim">%s</span></li>' % E(r["name"]))
    addable += n_link
    pin = '<span class="pin">%d addable</span>' % n_link if n_link else ""
    gens.append('<details class="gen-block"%s><summary><span class="g">gen %s</span>'
                '<span class="n">%d missing</span>%s</summary>'
                '<ul class="names">%s</ul></details>'
                % (" open" if n_link else "", E(g), len(rows), pin, "".join(items)))

deep = sum(len(v) for k, v in d["missing_by_gen"].items() if int(k) > 30)

CSS = """
:root{--ground:#EEF1F0;--panel:#FFFFFF;--ink:#16232A;--muted:#5A6E75;--line:#CBD5D4;
 --miss:#9B3B24;--have:#3C6E52;--accent:#2C5763;--shade:#E3E9E7}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
 --ground:#121A1D;--panel:#182327;--ink:#E6EDEB;--muted:#93A6AB;--line:#2B3A3F;
 --miss:#D9765A;--have:#6FA98A;--accent:#7FB3C0;--shade:#1D282C}}
:root[data-theme="dark"]{--ground:#121A1D;--panel:#182327;--ink:#E6EDEB;--muted:#93A6AB;
 --line:#2B3A3F;--miss:#D9765A;--have:#6FA98A;--accent:#7FB3C0;--shade:#1D282C}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font-family:"Source Sans 3",system-ui,sans-serif;
 font-size:16px;line-height:1.55;padding-inline:20px;margin:0}
a{color:var(--accent);text-underline-offset:2px}
a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.wrap{max-width:1000px;margin:0 auto;padding-block:40px 64px}
h1{font-family:Fraunces,Georgia,serif;font-weight:700;font-size:clamp(30px,5vw,44px);
 line-height:1.08;margin:0 0 8px;text-wrap:balance;letter-spacing:-.01em}
.sub{color:var(--muted);max-width:64ch;margin:0 0 26px}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:34px}
.stat{background:var(--panel);border:1px solid var(--line);padding:12px 16px;min-width:118px}
.stat b{font-family:Fraunces,Georgia,serif;font-size:26px;display:block;
 font-variant-numeric:tabular-nums;line-height:1.1}
.stat span{color:var(--muted);font-size:12.5px;text-transform:uppercase;letter-spacing:.07em}
.stat.m b{color:var(--miss)}
.stat.h b{color:var(--have)}
h2{font-family:Fraunces,Georgia,serif;font-size:22px;margin:40px 0 6px;font-weight:500}
.note{color:var(--muted);font-size:14.5px;max-width:66ch;margin:0 0 20px}
.brk{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--miss);
 margin-bottom:10px}
.brk-hd{display:flex;align-items:baseline;gap:12px;padding:12px 16px 6px;flex-wrap:wrap}
.brk-hd h3{margin:0;font-size:17px;font-weight:600;color:var(--have)}
.go{margin-left:auto;font-size:14px}
.gen{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted);
 background:var(--shade);padding:2px 7px;white-space:nowrap}
.brk-body{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:0 16px 14px}
@media (max-width:640px){.brk-body{grid-template-columns:1fr}.go{margin-left:0;width:100%}}
.lbl{display:block;font-size:11.5px;text-transform:uppercase;letter-spacing:.08em;
 color:var(--muted);margin-bottom:4px}
.down{margin:0;font-size:13px;color:var(--muted);font-family:"IBM Plex Mono",monospace;
 overflow-wrap:anywhere}
.brk-body ul{margin:0;padding-left:18px}
.miss{color:var(--miss);font-weight:600}
.gen-block{background:var(--panel);border:1px solid var(--line);margin-bottom:6px}
.gen-block summary{cursor:pointer;padding:10px 14px;display:flex;gap:14px;align-items:baseline;
 flex-wrap:wrap}
.gen-block summary:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.g{font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--accent);font-weight:600}
.n{color:var(--muted);font-size:13.5px;font-variant-numeric:tabular-nums}
.pin{margin-left:auto;font-size:12px;color:var(--have);border:1px solid var(--have);
 padding:1px 7px;border-radius:2px}
.names{margin:0;padding:0 16px 14px;list-style:none}
.names li{display:flex;gap:12px;flex-wrap:wrap;align-items:baseline;padding:5px 0;
 border-top:1px solid var(--line)}
.mn{font-weight:600;color:var(--miss)}
.mn.dim{color:var(--muted);font-weight:400}
.via{font-size:13px;color:var(--muted);margin-left:auto}
.noid{color:var(--muted);font-size:13px}
footer{margin-top:44px;border-top:1px solid var(--line);padding-top:16px;color:var(--muted);
 font-size:13.5px;max-width:68ch}
code{font-family:"IBM Plex Mono",monospace;font-size:.92em;background:var(--shade);padding:1px 4px}
"""

page = (
 '<title>Rogaland Gaps</title>\n'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
 'family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Source+Sans+3:wght@400;600'
 '&family=IBM+Plex+Mono:wght@400&display=swap">\n'
 '<style>' + CSS + '</style>\n'
 '<div class="wrap">\n'
 "<h1>Rogaland gaps in Richard Borsheim's line</h1>\n"
 '<p class="sub">Farm and patronymic ancestors that <em>Hethel Pedigree.ged</em> carries and the '
 'Geni corpus does not. Every name you already hold links to its Geni profile, so each row is a '
 'place to go and add somebody. Anything reached through a placeholder (Hethelo, &ldquo;a few '
 'generations&rdquo;, Audumbla) is excluded.</p>\n'
 '<div class="stats">'
 '<div class="stat"><b>@ANC@</b><span>ancestors, real</span></div>'
 '<div class="stat"><b>@NORDIC@</b><span>Nordic farm lines</span></div>'
 '<div class="stat m"><b>@MISSING@</b><span>absent from Geni</span></div>'
 '<div class="stat m"><b>@DIV@</b><span>broken links</span></div>'
 '<div class="stat h"><b>@ADDABLE@</b><span>have a child to hang from</span></div>'
 '</div>\n'
 '<h2>Where the lines break</h2>\n'
 '<p class="note">Each is a person <strong>already in Geni</strong> whose Hethel parents are not. '
 'Open the profile, add the parents named on the right. These are the highest-value additions '
 'because every one is a join rather than an orphan.</p>\n'
 '@DIVS@\n'
 '<h2>Everything missing, by generation</h2>\n'
 '<p class="note">Counted from Richard. Where the missing person has a child who <em>is</em> in '
 'Geni, that child is the profile to add them from, and it is linked. Generations 1&ndash;30 '
 'shown; a further @DEEP@ sit deeper, where the pedigree is legendary rather than parish '
 'record.</p>\n'
 '@GENS@\n'
 '<footer>Matched against <code>reports/derived-labels.csv</code> by normalised label, because '
 'Hethel carries MyHeritage <code>RIN</code>/<code>_UID</code> identifiers and no Geni ids. A name '
 'spelled differently on the two sides reads as missing when it is not, and a common name can '
 'match the wrong person &mdash; alternates are offered where several matched. Treat every row as '
 'a lead to verify on the profile, not a fact. Source: Hethel Pedigree.ged, a 2017 MyHeritage '
 'export of 31,320 people.</footer>\n</div>'
)

for k, v in (("@ANC@", format(c['ancestors_total'], ',')), ("@NORDIC@", str(c['nordic'])),
             ("@MISSING@", str(c['missing'])), ("@DIV@", str(c['divergences'])),
             ("@ADDABLE@", str(addable)), ("@DEEP@", str(deep)),
             ("@DIVS@", "\n".join(divs)), ("@GENS@", "\n".join(gens))):
    page = page.replace(k, v)

pathlib.Path("preservation/rogaland-gaps.html").write_text(page, encoding="utf-8")
print("wrote %d bytes | %d divergences | %d addable" % (len(page), len(divs), addable))
