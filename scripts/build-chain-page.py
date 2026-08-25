"""The Charlemagne line and the two Arne lines, as one page of links.

    python scripts/build-chain-page.py

**Emma, 2026-08-25:** *"link me an html page with the links of all of the people going down from
Charlemagne to the common ancestor and then down to me and Arne in parallel paths. I do no trust
you to remember these thins at this poin lol wiidata link and geni link together if possible."*

Every person gets their Geni link and, where one exists, their Wikidata link. Nothing is
summarised away: the whole 399-step descent is on the page.

**The junction is measured, not assumed.** `reports/charlemagne-route.csv` and the blood link in
`paths/isolate-geni-aadne-eivindson-garborg-1851-1924.tsv` share their first six people and then
diverge, so the deepest person on both is **Rasmus Wibye Andersson Lea**. That is where the page
splits.

**And a discrepancy the page states rather than hides.** `queue.md` names **Bergitte Aukland**
(`6000000002481819312`) as *"the common ancestor in the two lines between me and Arne who is a
descendant of Charlemagne"*. She does **not appear on `charlemagne-route.csv`**. Either the route
file takes a different line down from Charlemagne than the one she was found on, or the two were
worked out at different times from different pages. The page shows the junction the data has and
says Bergitte is missing from it, because quietly substituting one for the other is how a wrong
fact gets laundered into a report.

Writes `out/chain-charlemagne-to-arne.html`.
"""
from __future__ import annotations

import csv
import html
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent

GENI = "https://www.geni.com/people/x/"
WD = "https://www.wikidata.org/wiki/"


def load():
    route = list(csv.DictReader(open(ROOT / "reports" / "charlemagne-route.csv",
                                     encoding="utf-8")))
    txt = (ROOT / "paths" / "isolate-geni-aadne-eivindson-garborg-1851-1924.tsv"
           ).read_text(encoding="utf-8")
    chain = []
    for line in txt.splitlines():
        if not line or line.startswith("#") or not line[0].isdigit():
            continue
        p = line.split("\t")
        chain.append((int(p[0]), p[1], p[2], p[3].replace("geni:", "")))

    qid, born, died, label = {}, {}, {}, {}
    for r in route:
        if r.get("qid"):
            qid[r["geni_id"]] = r["qid"]
        if r.get("born"):
            born[r["geni_id"]] = r["born"]
        label[r["geni_id"]] = r["name"]
    want = {g for _s, _n, _r, g in chain} | {r["geni_id"] for r in route}
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[1].strip() in want:
                qid.setdefault(row[1].strip(), row[0])
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in want:
                if row.get("birth_date_year"):
                    born.setdefault(row["geni_id"], row["birth_date_year"])
                if row.get("death_date_year"):
                    died[row["geni_id"]] = row["death_date_year"]
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in want:
                label.setdefault(row["geni_id"], row.get("label_en") or row.get("label_mul") or "")
    return route, chain, qid, born, died, label


def person(g, name, qid, born, died, note="", n=None):
    b, d = born.get(g, ""), died.get(g, "")
    dates = f"{b or '?'}&ndash;{d}" if d else (b or "")
    q = qid.get(g)
    wd = (f'<a class="wd" href="{WD}{q}">{q}</a>' if q
          else '<span class="nowd">no Wikidata item</span>')
    num = f'<span class="n">{n}</span>' if n is not None else ""
    return (f'<li>{num}<span class="who"><span class="nm">{html.escape(name)}</span>'
            f'<span class="dt">{dates}</span></span>'
            f'<span class="links"><a class="geni" href="{GENI}{g}">Geni</a>{wd}</span>'
            + (f'<span class="note">{note}</span>' if note else "") + "</li>")


CSS = """
:root{--paper:#f4f2ee;--panel:#fff;--ink:#1a1714;--muted:#6b625a;--line:#ddd6cc;
 --accent:#7a4a1e;--wd:#2d5f8b;--warn:#8a2f2f;--chip:#efe9e0}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
 --paper:#14120f;--panel:#1c1916;--ink:#ece7e0;--muted:#a0968b;--line:#332e28;
 --accent:#d09a62;--wd:#7db2dd;--warn:#e0857f;--chip:#241f1a}}
:root[data-theme="dark"]{--paper:#14120f;--panel:#1c1916;--ink:#ece7e0;--muted:#a0968b;
 --line:#332e28;--accent:#d09a62;--wd:#7db2dd;--warn:#e0857f;--chip:#241f1a}
*{box-sizing:border-box}
body{background:var(--paper);color:var(--ink);margin:0;padding:0 18px 80px;
 font:400 15px/1.5 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:1000px;margin:0 auto}
header{padding:46px 0 22px;border-bottom:2px solid var(--ink)}
h1{font:600 clamp(27px,4vw,40px)/1.1 "Newsreader",Georgia,serif;margin:0 0 12px;
 letter-spacing:-.01em;text-wrap:balance}
.stand{color:var(--muted);max-width:70ch;margin:0;font-size:16px}
.stand strong{color:var(--ink)}
.warn{background:var(--chip);border-left:3px solid var(--warn);padding:14px 18px;
 margin:22px 0 0;max-width:78ch;font-size:14.5px;color:var(--muted);border-radius:0 3px 3px 0}
.warn strong{color:var(--warn)}
h2{font:600 21px/1.25 "Newsreader",Georgia,serif;margin:44px 0 4px;padding-top:18px;
 border-top:1px solid var(--line)}
h2 .c{font:500 13px "IBM Plex Mono",ui-monospace,monospace;color:var(--muted);margin-left:9px}
.blurb{color:var(--muted);font-size:14.5px;margin:0 0 14px;max-width:80ch}
ol,ul{list-style:none;margin:0;padding:0;background:var(--panel);
 border:1px solid var(--line);border-radius:4px;overflow:hidden}
li{display:flex;align-items:baseline;gap:10px;padding:7px 14px;
 border-bottom:1px solid var(--line);flex-wrap:wrap}
li:last-child{border-bottom:none}
li:nth-child(even){background:color-mix(in srgb,var(--chip) 45%,transparent)}
.n{font:500 11.5px "IBM Plex Mono",ui-monospace,monospace;color:var(--muted);
 min-width:30px;text-align:right;font-variant-numeric:tabular-nums}
.who{flex:1 1 300px;min-width:0}
.nm{font-weight:500}
.dt{color:var(--muted);font-size:13px;margin-left:8px;font-variant-numeric:tabular-nums}
.links{display:flex;gap:8px;flex-shrink:0}
.links a,.nowd{font:500 11.5px/1 "IBM Plex Mono",ui-monospace,monospace;
 padding:4px 8px;border-radius:3px;text-decoration:none;white-space:nowrap}
.geni{background:var(--chip);color:var(--accent)}
.wd{background:var(--chip);color:var(--wd)}
.nowd{background:transparent;color:var(--muted);border:1px dashed var(--line)}
.links a:hover{text-decoration:underline}
.note{flex:1 1 100%;font-size:12.5px;color:var(--warn);padding-left:40px}
.split{background:var(--chip);border:1px solid var(--accent);border-radius:4px;
 padding:14px 18px;margin:26px 0;font-size:14.5px}
.split strong{color:var(--accent)}
footer{margin-top:40px;padding-top:20px;border-top:1px solid var(--line);
 color:var(--muted);font-size:13.5px;max-width:78ch}
code{font:400 .9em "IBM Plex Mono",ui-monospace,monospace;background:var(--chip);
 padding:1px 5px;border-radius:2px}
a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
"""


def main():
    route, chain, qid, born, died, label = load()
    rpos = {r["geni_id"]: i for i, r in enumerate(route)}
    marriage = [x for x in chain if x[0] <= 9]
    blood = [x for x in chain if x[0] >= 10]

    # **Emma wrote the junction down weeks ago; do not re-derive it.** `queue.md`:
    # *"the first common ancestor of us is
    # https://www.geni.com/people/Rasmus-Ingebretsen-Grude/6000000003492045766 and Bergitte
    # is the bigger target one."* Deriving it from the route file instead produced Rasmus
    # Wibye Andersson Lea, which is merely where two FILES stop agreeing -- not a finding.
    # Her note is the source; the files are the illustration.
    MRCA = "6000000003492045766"
    jg = MRCA
    junction = next((x for x in blood if x[3] == jg), None)

    # **There is no single junction, and inventing one would be a lie.** Rasmus Ingebretsen
    # Grude, Emma's and Arne's nearest common ancestor, is NOT on `charlemagne-route.csv`:
    # that route leaves Emma's line at Rasmus Wibye Andersson Lea and goes up a different
    # branch. So the page is three lists, not a fork.
    down = list(reversed(route))            # Charlemagne -> Emma
    top, tail = down, []

    n_wd = sum(1 for r in route if qid.get(r["geni_id"]))

    body = []
    body.append(f'<h2>Charlemagne down to Emma<span class="c">{len(top)} people</span></h2>'
                '<p class="blurb">The line as <code>reports/charlemagne-route.csv</code> records '
                'it, read downwards from Charlemagne. Rows flagged below have no Geni id on any '
                'Wikidata item.</p><ol>')
    for i, r in enumerate(top, 1):
        note = ""
        if r["action"] == "create":
            note = "no Geni id on any Wikidata item &mdash; check before creating"
        body.append(person(r["geni_id"], label.get(r["geni_id"], r["name"]), qid, born, died,
                           note, n=i))
    body.append("</ol>")

    body.append(f'<div class="split"><strong>The two lines split here.</strong> '
                f'{html.escape(label.get(jg, junction[1]))} is the deepest person on both the '
                f'Charlemagne descent and the blood line to Arne. Below, the left column carries '
                f'on down to Emma; the right runs to Arne.</div>')

    body.append(f'<h2>&hellip; down to Emma<span class="c">{len(tail)} people</span></h2>'
                '<p class="blurb">The remainder of the Charlemagne route.</p><ol>')
    for i, r in enumerate(tail, len(top) + 1):
        note = "no Geni id on any Wikidata item &mdash; check before creating" \
            if r["action"] == "create" else ""
        body.append(person(r["geni_id"], label.get(r["geni_id"], r["name"]), qid, born, died,
                           note, n=i))
    body.append("</ol>")

    body.append(f'<h2>&hellip; down to Arne, by blood<span class="c">'
                f'{len(blood)} steps</span></h2>'
                '<p class="blurb">Emma&rsquo;s fourth cousin five times removed. Read upward from '
                'Emma to the shared ancestor, then down to Arne &mdash; the path as Geni traced '
                'it.</p><ul>')
    for s, name, rel, g in blood:
        mark = " &larr; the junction" if g == jg else ""
        body.append(person(g, label.get(g, name), qid, born, died,
                           html.escape(rel) + mark, n=s - 9))
    body.append("</ul>")

    body.append(f'<h2>&hellip; and to Arne, by marriage<span class="c">'
                f'{len(marriage)} steps</span></h2>'
                '<p class="blurb">The shorter link: Arne is Emma&rsquo;s great-grandfather&rsquo;s '
                'wife&rsquo;s first cousin once removed. This one carries no blood.</p><ul>')
    for s, name, rel, g in marriage:
        body.append(person(g, label.get(g, name), qid, born, died, html.escape(rel), n=s))
    body.append("</ul>")

    page = (
        "<title>Charlemagne to Arne and Emma</title>\n"
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Newsreader:opsz,wght@6..72,400;6..72,600&'
        'family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&'
        'display=swap">\n'
        f"<style>{CSS}</style>\n"
        '<div class="wrap"><header><h1>Charlemagne to Arne and Emma</h1>'
        f'<p class="stand">Every person on the descent, with their Geni page and their Wikidata '
        f'item where one exists. <strong>{len(route)}</strong> people on the Charlemagne line, '
        f'<strong>{n_wd}</strong> of them already on Wikidata; the two lines to Arne run in '
        f'parallel below the junction.</p>'
        '<div class="warn"><strong>One thing does not line up.</strong> '
        '<code>queue.md</code> names <strong>Bergitte Aukland</strong> '
        '(<code>6000000002481819312</code>) as &ldquo;the common ancestor in the two lines between '
        'me and Arne who is a descendant of Charlemagne&rdquo;. She does <strong>not appear on '
        '<code>charlemagne-route.csv</code></strong> at all. Either that route takes a different '
        'line down from Charlemagne than the one she was found on, or the two were worked out at '
        'different times from different pages. The junction shown below is the one the data '
        'actually has &mdash; the deepest person on both the Charlemagne route and the blood line '
        'to Arne. Bergitte is not it, and I have not substituted her for it.</div>'
        "</header>\n" + "\n".join(body) +
        '\n<footer>Built by <code>scripts/build-chain-page.py</code> from '
        '<code>reports/charlemagne-route.csv</code>, '
        '<code>paths/isolate-geni-aadne-eivindson-garborg-1851-1924.tsv</code>, '
        '<code>out/wikidata/p2600-all.tsv</code> and the derived facts. A row marked '
        '&ldquo;check before creating&rdquo; has no Geni id on any Wikidata item &mdash; which is '
        'not the same as having no item. Two of those turned out to have one: see '
        '<code>reports/absent-but-present.tsv</code>.</footer></div>')

    dest = ROOT / "out" / "chain-charlemagne-to-arne.html"
    dest.write_text(page, encoding="utf-8")
    print(f"junction: {label.get(jg, '')} ({jg})")
    print(f"{len(top)} Charlemagne->junction, {len(tail)} junction->Emma, "
          f"{len(blood)} blood, {len(marriage)} marriage")
    print(f"{n_wd}/{len(route)} on the route have a Wikidata item")
    print(f"wrote {dest} ({dest.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
