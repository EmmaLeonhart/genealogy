"""Render the ahnentafel frontier page from preservation/ahnentafel.json."""
import json, pathlib, html, collections

d = json.loads(pathlib.Path("preservation/ahnentafel.json").read_text(encoding="utf-8"))
slots = {int(k): v for k, v in d["slots"].items()}
rows = d["rows"]
E = html.escape

frontier = []
for n, v in sorted(slots.items()):
    f, m = 2 * n in slots, 2 * n + 1 in slots
    if f and m:
        continue
    miss = "father & mother" if not f and not m else ("father" if not f else "mother")
    frontier.append({"n": n, "gen": n.bit_length() - 1, "name": v["name"],
                     "in_geni": v["in_geni"], "miss": miss})

def row_html(r):
    cls = "has" if r["in_geni"] else "no"
    tag = "in Geni" if r["in_geni"] else "not matched"
    return ('<tr><td class="ahn">%d</td><td class="gen">%d</td><td class="nm">%s</td>'
            '<td class="ms">%s</td><td class="%s">%s</td></tr>'
            % (r["n"], r["gen"], E(r["name"]), E(r["miss"]), cls, tag))

shallow = [r for r in frontier if 2 <= r["gen"] <= 7]
mid = [r for r in frontier if 8 <= r["gen"] <= 11]
deep = [r for r in frontier if r["gen"] >= 12]

fill_rows = "".join(
    '<tr><td class="gen">%d</td><td class="num">%d</td><td class="num">%d</td>'
    '<td class="num"><span class="bar" style="--w:%.4f"></span>%.1f%%</td>'
    '<td class="num">%d</td></tr>'
    % (g, tot, got, got / tot, 100 * got / tot, ing)
    for g, tot, got, ing in rows)

CSS = """
:root{--ground:#F3F1EC;--panel:#FFF;--ink:#1C1A17;--muted:#6B6560;--line:#DAD5CC;
 --gap:#8C3A2B;--has:#3E6B4F;--accent:#3A5A6B;--shade:#E8E4DC;--rule:#C8C1B6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
 --ground:#161513;--panel:#1F1D1A;--ink:#EDEAE4;--muted:#9C958C;--line:#33302B;
 --gap:#D98070;--has:#79A98A;--accent:#7FA6BA;--shade:#242220;--rule:#3A3630}}
:root[data-theme="dark"]{--ground:#161513;--panel:#1F1D1A;--ink:#EDEAE4;--muted:#9C958C;
 --line:#33302B;--gap:#D98070;--has:#79A98A;--accent:#7FA6BA;--shade:#242220;--rule:#3A3630}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font-family:"Source Sans 3",system-ui,sans-serif;
 font-size:16px;line-height:1.5;padding-inline:20px;margin:0}
.wrap{max-width:940px;margin:0 auto;padding-block:40px 64px}
h1{font-family:Fraunces,Georgia,serif;font-weight:700;font-size:clamp(28px,5vw,42px);
 line-height:1.1;margin:0 0 10px;text-wrap:balance}
.sub{color:var(--muted);max-width:64ch;margin:0 0 30px}
h2{font-family:Fraunces,Georgia,serif;font-size:21px;margin:38px 0 4px;font-weight:500}
.note{color:var(--muted);font-size:14.5px;max-width:66ch;margin:0 0 16px}
table{width:100%;border-collapse:collapse;font-size:14.5px;background:var(--panel);
 border:1px solid var(--line)}
caption{text-align:left;color:var(--muted);font-size:13px;padding:8px 10px}
th{text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.07em;
 color:var(--muted);font-weight:600;padding:8px 10px;border-bottom:1px solid var(--rule)}
td{padding:6px 10px;border-bottom:1px solid var(--line);vertical-align:baseline}
tr:last-child td{border-bottom:0}
.ahn{font-family:"IBM Plex Mono",monospace;color:var(--accent);font-weight:600;
 font-variant-numeric:tabular-nums;width:4.5em}
.gen{font-family:"IBM Plex Mono",monospace;color:var(--muted);font-variant-numeric:tabular-nums;
 width:3.5em}
.num{font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}
.nm{font-weight:600}
.ms{color:var(--gap);font-size:13.5px;white-space:nowrap}
.no{color:var(--gap);font-size:13px;white-space:nowrap}
.has{color:var(--has);font-size:13px;white-space:nowrap}
.bar{display:inline-block;height:7px;width:calc(var(--w)*70px);background:var(--accent);
 margin-right:8px;vertical-align:middle;min-width:1px}
.scroll{overflow-x:auto}
details{margin-top:10px}
summary{cursor:pointer;color:var(--accent);font-size:14.5px;padding:6px 0}
summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.cliff{background:var(--shade);border-left:3px solid var(--gap);padding:12px 16px;
 margin:20px 0;font-size:14.5px}
footer{margin-top:44px;border-top:1px solid var(--line);padding-top:16px;color:var(--muted);
 font-size:13.5px;max-width:68ch}
code{font-family:"IBM Plex Mono",monospace;font-size:.92em;background:var(--shade);padding:1px 4px}
"""

page = (
 '<title>Borsheim Ahnentafel</title>\n'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
 'family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Source+Sans+3:wght@400;600'
 '&family=IBM+Plex+Mono:wght@400;600&display=swap">\n'
 '<style>' + CSS + '</style>\n'
 '<div class="wrap">\n'
 "<h1>Where Richard Borsheim's pedigree runs out</h1>\n"
 '<p class="sub">Ahnentafel positions from <em>Hethel Pedigree.ged</em>: position 1 is Richard, '
 "a father is 2n, a mother is 2n+1. Counting by position rather than by name shows exactly which "
 "slots are empty and at which generation the pedigree stops being a pedigree. Everything through "
 'a placeholder (Hethelo, &ldquo;a few generations&rdquo;, Audumbla) is excluded.</p>\n'
 '<h2>Fill rate by generation</h2>\n'
 '<p class="note">Of the slots each generation could hold, how many Hethel fills &mdash; and how '
 'many of those are matched in the Geni corpus.</p>\n'
 '<div class="scroll"><table><caption>338 slots filled in total.</caption>'
 '<tr><th>gen</th><th class="num">slots</th><th class="num">filled</th>'
 '<th class="num">fill rate</th><th class="num">in Geni</th></tr>'
 + fill_rows + '</table></div>\n'
 '<div class="cliff"><strong>The cliff is generation 6.</strong> Generations 3 to 5 are 88%, 75% '
 'and 66% full &mdash; ordinary parish-record completeness. At generation 6 it drops to 39%, then '
 '23%, then 14%. Past generation 11 the pedigree is under 3% full: a handful of traced noble '
 'lines rather than an ancestry.</div>\n'
 '<h2>The frontier &mdash; @SHALLOW@ positions in parish-record territory</h2>\n'
 '<p class="note">A filled position missing one or both parents. Generations 2 to 7 only: these '
 'are the ones where Norwegian parish registers and the bygdebøker actually reach, so they are '
 'the gaps worth working. @ANH5@</p>\n'
 '<div class="scroll"><table>'
 '<tr><th>ahn</th><th>gen</th><th>position holder</th><th>missing</th><th>corpus</th></tr>'
 + "".join(row_html(r) for r in shallow) + '</table></div>\n'
 '<details><summary>Generations 8&ndash;11 &mdash; @MID@ more positions</summary>'
 '<div class="scroll"><table>'
 '<tr><th>ahn</th><th>gen</th><th>position holder</th><th>missing</th><th>corpus</th></tr>'
 + "".join(row_html(r) for r in mid) + '</table></div></details>\n'
 '<details><summary>Generation 12 and deeper &mdash; @DEEP@ positions, legendary territory</summary>'
 '<div class="scroll"><table>'
 '<tr><th>ahn</th><th>gen</th><th>position holder</th><th>missing</th><th>corpus</th></tr>'
 + "".join(row_html(r) for r in deep) + '</table></div></details>\n'
 '<footer><p><strong>Two names in here are corrupted in the source file.</strong> '
 '<code>TorbjJørnevikrnsdatter Yksen</code> and <code>Jørnevikrn Yksen</code> are '
 '<em>Torbjørnsdatter</em> and <em>Torbjørn</em> with the string &ldquo;Jørnevik&rdquo; spliced '
 'through them &mdash; a find-and-replace accident in Hethel itself, not in this reading.</p>'
 '<p>The corpus column matches by normalised label, because Hethel carries MyHeritage '
 '<code>RIN</code>/<code>_UID</code> identifiers and no Geni ids. A different spelling reads as '
 'unmatched, so treat <em>not matched</em> as &ldquo;look for them&rdquo; rather than &ldquo;they '
 'are absent&rdquo;. The position numbers are exact; only the corpus column is a guess.</p></footer>\n'
 '</div>')

anh5 = ('Position 5 &mdash; Teoline henrikksdtr Birkiland, Richard&rsquo;s own great-grandmother '
        '&mdash; is missing her mother, which is the shallowest gap in the whole pedigree.')
for k, v in (("@SHALLOW@", str(len(shallow))), ("@MID@", str(len(mid))),
             ("@DEEP@", str(len(deep))), ("@ANH5@", anh5)):
    page = page.replace(k, v)

pathlib.Path("preservation/borsheim-ahnentafel.html").write_text(page, encoding="utf-8")
print("wrote %d bytes | frontier %d (shallow %d, mid %d, deep %d)"
      % (len(page), len(frontier), len(shallow), len(mid), len(deep)))
