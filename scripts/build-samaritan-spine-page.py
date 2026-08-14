"""Render `gedcom/samaritan-itamar-spine.ged` as a generation-numbered page.

This is a view of the file, not a second opinion about it: the same walk, the
same numbering, the same descriptive labels. Itamar ben Aaron at the top, Tabia
ha'Abta'i at the bottom, and Aaron shown above them greyed out because he is
generation 1 but deliberately not in the file.

    py scripts/build-samaritan-spine-page.py
"""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from samaritan_spine import (  # noqa: E402
    REPO, ROOT, display, generation_label, is_placeholder, parse, spine,
)


def row(n: int, label: str, cls: str, occu: str = "", titl: str = "",
        note: str = "") -> str:
    bits = [f'<div class="who">{html.escape(label)}</div>']
    if titl:
        bits.append(f'<div class="titl">{html.escape(titl)}</div>')
    if occu:
        bits.append(f'<div class="occu">{html.escape(occu)}</div>')
    if note:
        bits.append(f'<div class="note">{html.escape(note)}</div>')
    return (f'<li class="{cls}"><span class="gen">{n}</span>'
            f'<div class="cell">{"".join(bits)}</div></li>')


def render(people, aaron) -> str:
    named = [r for _, r in people if not is_placeholder(r)]
    blank = len(people) - len(named)

    rows = [row(1, display(aaron["name"]), "absent",
                occu=aaron["occu"],
                note="Generation 1, and where the count starts — but NOT in the "
                     "spine file. He is already on Geni; emitting him again "
                     "would invite a duplicate. Attach Itamar to this Aaron.")]

    for n, rec in people:
        if is_placeholder(rec):
            extra = " ".join(" ".join(rec["note"]).split())
            note = ("No source names this person. The record asserts a position "
                    "in the descent and nothing else.")
            if "may be zero" in extra:
                note = ("No source names this person, and this generation's "
                        "distance MAY BE ZERO — 'Abed Ela may simply be Yusef's "
                        "father. Not attested either way.")
            rows.append(row(n, generation_label(n), "placeholder", note=note))
        else:
            rows.append(row(n, display(rec["name"]), "named",
                            occu=rec["occu"], titl=rec["titl"],
                            note=" ".join(" ".join(rec["note"]).split())))

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Samaritan Itamar line</title>
<style>
  :root {{
    --bg: #fbfaf7; --fg: #1b1a17; --muted: #6b675e; --rule: #ded9cf;
    --card: #ffffff; --accent: #7a5c1e; --ghost: #f2efe8; --faint: #a29c90;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg: #16151a; --fg: #ecebe6; --muted: #9c968a; --rule: #2f2d35;
      --card: #1e1d23; --accent: #d8b45e; --ghost: #1a1920; --faint: #6d6860;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--fg);
    font: 16px/1.5 "Iowan Old Style", Georgia, "Times New Roman", serif; }}
  main {{ max-width: 48rem; margin: 0 auto; padding: 3rem 1.25rem 5rem; }}
  h1 {{ font-size: 2rem; line-height: 1.12; margin: 0 0 .4rem; letter-spacing: -.015em; }}
  .sub {{ color: var(--muted); margin: 0 0 2rem; }}
  .counts {{ display: flex; flex-wrap: wrap; gap: .75rem; margin: 0 0 2.25rem;
    padding: 0; list-style: none; }}
  .counts li {{ background: var(--card); border: 1px solid var(--rule);
    border-radius: .5rem; padding: .6rem .9rem; min-width: 8rem; }}
  .counts b {{ display: block; font-size: 1.5rem; font-variant-numeric: tabular-nums; }}
  .counts span {{ color: var(--muted); font-size: .8rem; text-transform: uppercase;
    letter-spacing: .06em; }}
  .warn {{ border-left: 3px solid var(--accent); background: var(--ghost);
    padding: .9rem 1.1rem; margin: 0 0 2.5rem; border-radius: 0 .4rem .4rem 0; }}
  .warn p {{ margin: 0 0 .6rem; }} .warn p:last-child {{ margin: 0; }}
  ol.chain {{ list-style: none; margin: 0; padding: 0; }}
  ol.chain li {{ display: flex; gap: 1rem; align-items: flex-start;
    padding: .3rem 0; position: relative; }}
  ol.chain li::before {{ content: ""; position: absolute; left: 1.35rem; top: 0;
    bottom: 0; width: 1px; background: var(--rule); }}
  ol.chain li:first-child::before {{ top: 1.1rem; }}
  ol.chain li:last-child::before {{ bottom: calc(100% - 1.1rem); }}
  .gen {{ position: relative; z-index: 1; flex: 0 0 2.7rem; text-align: center;
    font-variant-numeric: tabular-nums; font-size: .78rem; color: var(--muted);
    background: var(--bg); padding: .15rem 0; border-radius: 1rem; }}
  .cell {{ flex: 1 1 auto; min-width: 0; padding-bottom: .15rem; }}
  .named .cell, .absent .cell {{ background: var(--card); border: 1px solid var(--rule);
    border-radius: .5rem; padding: .7rem .9rem; margin: .15rem 0 .55rem; }}
  .absent .cell {{ border-style: dashed; opacity: .8; }}
  .named .gen {{ color: var(--accent); font-weight: 700; }}
  .who {{ font-size: 1.05rem; }}
  .named .who, .absent .who {{ font-weight: 600; }}
  .placeholder .who {{ color: var(--faint); font-size: .92rem; }}
  .titl {{ font-size: .9rem; margin-top: .1rem; }}
  .occu {{ color: var(--accent); font-size: .8rem; text-transform: uppercase;
    letter-spacing: .06em; margin-top: .15rem; }}
  .note {{ color: var(--muted); font-size: .86rem; margin-top: .45rem; }}
  .placeholder .note {{ font-size: .78rem; margin-top: .1rem; }}
  footer {{ margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid var(--rule);
    color: var(--muted); font-size: .88rem; }}
  code {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .85em; }}
</style></head><body><main>

<h1>The Samaritan Itamar line</h1>
<p class="sub">Itamar ben Aaron down to Tabia ha'Abta'i, generation by
generation — a view of <code>gedcom/samaritan-itamar-spine.ged</code>, the file
built for entering into Geni.</p>

<ul class="counts">
  <li><b>{len(people)}</b><span>records</span></li>
  <li><b>{len(named)}</b><span>named</span></li>
  <li><b>{blank}</b><span>numbered generations</span></li>
  <li><b>2 – 112</b><span>generations spanned</span></li>
</ul>

<div class="warn">
  <p><strong>Five people here are named by a source. The other {blank} are
  positions, not people.</strong> They are labelled
  <em>&ldquo;{html.escape(generation_label(4))}&rdquo;</em> and so on because
  that is exactly what the record asserts — a place in a named lineage. It is not
  a personal name and no name has been invented anywhere.</p>
  <p>The <strong>length</strong> of the unnamed stretch is borrowed from the
  parallel Phinhas line, which the source gives as <strong>112 generations
  father-to-son from Aaron</strong> to 1624. Nobody counted this line. Do not
  read these numbers as a measurement of it.</p>
  <p>Generation 110 is weaker still: the source does not state the distance
  between 'Abed Ela ben Shalma and Yusef, and <strong>it may be zero</strong>.</p>
</div>

<ol class="chain">
{chr(10).join(rows)}
</ol>

<footer>
<p>Below Tabia the descent continues into the 33 Samaritan priests Geni already
holds as a component disconnected from everything else — he is profile
<code>6000000220294810877</code>, and attaching this line above him is what
connects them.</p>
<p>Source: <em>The High Priesthood and the Israelite Samaritan Priests</em>,
Benyamim Tsedaka, A.B. — The Samaritan News / The Samaritan Update,
March–April 2012. See <code>reports/samaritan-priesthood.md</code>.</p>
<p>Generated by <code>scripts/build-samaritan-spine-page.py</code>.</p>
</footer>
</main></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="reports/samaritan-spine.html")
    args = ap.parse_args()

    indi, fam = parse()
    people = spine(indi, fam)
    out = REPO / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(people, indi[ROOT]), encoding="utf-8")
    print(f"generations {people[0][0]}-{people[-1][0]}, {len(people)} records -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
