"""Render the Aaron → 'Abed Ela ben Shalma descent as a generation-numbered page.

The chain comes from `gedcom/samaritan-sources.ged` and nothing else. Most of it
is explicit placeholders: no source names the stretch between Itamar ben Aaron
and Shalma, so those people exist in the file as unnamed records carrying a NOTE
that says what they are. This page numbers the generations and shows the shape —
it does not name anybody the GEDCOM does not name.

    py scripts/build-samaritan-spine-page.py -o out/samaritan-spine.html
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GED = REPO / "gedcom" / "samaritan-sources.ged"

#: Aaron ben Amram, the head of both priestly lines.
ROOT = "@I1@"

#: "The forefather of the current priestly families was the priest 'Abed Ela b.
#: Shalma" — A.B. / The Samaritan Update, March-April 2012. That sentence is why
#: the walk stops here rather than at Tabia or at the current High Priest.
TARGET_NAME = "'Abed Ela"


def parse(path: Path):
    """The subset of GEDCOM this file uses: INDI/FAM, NAME, SEX, OCCU, NOTE."""
    indi: dict[str, dict] = {}
    fam: dict[str, dict] = {}
    cur = None
    kind = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\d+) (?:(@[^@]+@) )?(\w+)(?: (.*))?$", raw)
        if not m:
            continue
        level, xref, tag, val = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        if level == "0":
            if tag == "INDI":
                cur = indi.setdefault(xref, {"id": xref, "famc": None, "fams": [],
                                             "name": "", "occu": "", "note": []})
                kind = "indi"
            elif tag == "FAM":
                cur = fam.setdefault(xref, {"id": xref, "husb": None, "wife": None,
                                            "chil": []})
                kind = "fam"
            else:
                cur, kind = None, None
            continue
        if cur is None:
            continue
        if kind == "indi":
            if tag == "NAME":
                cur["name"] = val
            elif tag == "OCCU":
                cur["occu"] = val
            elif tag == "NOTE":
                cur["note"] = [val]
            elif tag == "CONT" and cur["note"]:
                cur["note"].append(val)
            elif tag == "FAMC":
                cur["famc"] = val
            elif tag == "FAMS":
                cur["fams"].append(val)
        else:
            if tag in ("HUSB", "WIFE"):
                cur[tag.lower()] = val
            elif tag == "CHIL":
                cur["chil"].append(val)
    return indi, fam


def descent(indi, fam, root: str, target: str) -> list[str]:
    """The path of xrefs from root down to the person whose name starts with
    `target`. Depth-first: the file is a spine with a few branches at the bottom,
    so the first path found is the only path."""
    stack = [(root, [root])]
    seen = set()
    while stack:
        person, path = stack.pop()
        if person in seen:
            continue
        seen.add(person)
        if indi[person]["name"].lstrip().startswith(target):
            return path
        for f in indi[person]["fams"]:
            for child in fam.get(f, {}).get("chil", []):
                if child in indi:
                    stack.append((child, path + [child]))
    raise SystemExit(f"no descent found from {root} to a name starting {target!r}")


def display(name: str) -> str:
    """`Itamar /ben Aaron/` → `Itamar ben Aaron`; `//` → empty."""
    return " ".join(name.replace("/", " ").split())


def render(indi, path: list[str]) -> str:
    people = [indi[x] for x in path]
    named = [p for p in people if display(p["name"])]
    blank = len(people) - len(named)

    rows = []
    for n, p in enumerate(people, start=1):
        label = display(p["name"])
        note = " ".join(" ".join(p["note"]).split())
        if label:
            body = (
                f'<div class="who">{html.escape(label)}</div>'
                + (f'<div class="occu">{html.escape(p["occu"])}</div>' if p["occu"] else "")
                + (f'<div class="note">{html.escape(note)}</div>' if note else "")
            )
            cls = "named"
        else:
            body = '<div class="who unnamed">unnamed placeholder</div>'
            cls = "placeholder"
        rows.append(
            f'<li class="{cls}"><span class="gen">{n}</span>'
            f'<div class="cell">{body}</div></li>'
        )

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aaron to 'Abed Ela</title>
<style>
  :root {{
    --bg: #fbfaf7; --fg: #1b1a17; --muted: #6b675e; --rule: #ded9cf;
    --card: #ffffff; --accent: #7a5c1e; --ghost: #f2efe8;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg: #16151a; --fg: #ecebe6; --muted: #9c968a; --rule: #2f2d35;
      --card: #1e1d23; --accent: #d8b45e; --ghost: #1a1920;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--fg);
    font: 16px/1.5 "Iowan Old Style", Georgia, "Times New Roman", serif; }}
  main {{ max-width: 46rem; margin: 0 auto; padding: 3rem 1.25rem 5rem; }}
  h1 {{ font-size: 1.9rem; line-height: 1.15; margin: 0 0 .4rem; letter-spacing: -.01em; }}
  .sub {{ color: var(--muted); margin: 0 0 2rem; }}
  .counts {{ display: flex; flex-wrap: wrap; gap: .75rem; margin: 0 0 2.5rem; padding: 0; list-style: none; }}
  .counts li {{ background: var(--card); border: 1px solid var(--rule); border-radius: .5rem;
    padding: .6rem .9rem; min-width: 7.5rem; }}
  .counts b {{ display: block; font-size: 1.5rem; font-variant-numeric: tabular-nums; }}
  .counts span {{ color: var(--muted); font-size: .82rem; text-transform: uppercase; letter-spacing: .06em; }}
  .warn {{ border-left: 3px solid var(--accent); background: var(--ghost);
    padding: .9rem 1.1rem; margin: 0 0 2.5rem; border-radius: 0 .4rem .4rem 0; }}
  .warn p {{ margin: 0 0 .6rem; }} .warn p:last-child {{ margin: 0; }}
  ol.chain {{ list-style: none; margin: 0; padding: 0; }}
  ol.chain li {{ display: flex; gap: 1rem; align-items: flex-start;
    padding: .35rem 0; position: relative; }}
  ol.chain li::before {{ content: ""; position: absolute; left: 1.1rem; top: 0; bottom: 0;
    width: 1px; background: var(--rule); }}
  ol.chain li:first-child::before {{ top: 1.1rem; }}
  ol.chain li:last-child::before {{ bottom: calc(100% - 1.1rem); }}
  .gen {{ position: relative; z-index: 1; flex: 0 0 2.2rem; text-align: center;
    font-variant-numeric: tabular-nums; font-size: .78rem; color: var(--muted);
    background: var(--bg); padding: .15rem 0; border-radius: 1rem; }}
  .cell {{ flex: 1 1 auto; min-width: 0; padding-bottom: .2rem; }}
  .named .cell {{ background: var(--card); border: 1px solid var(--rule);
    border-radius: .5rem; padding: .7rem .9rem; margin: .15rem 0 .55rem; }}
  .named .gen {{ color: var(--accent); font-weight: 700; }}
  .who {{ font-size: 1.05rem; }}
  .named .who {{ font-weight: 600; }}
  .unnamed {{ color: var(--muted); font-style: italic; font-size: .9rem; }}
  .occu {{ color: var(--accent); font-size: .82rem; text-transform: uppercase;
    letter-spacing: .06em; margin-top: .15rem; }}
  .note {{ color: var(--muted); font-size: .86rem; margin-top: .45rem; }}
  footer {{ margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid var(--rule);
    color: var(--muted); font-size: .88rem; }}
  code {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .85em; }}
</style></head><body><main>

<h1>Aaron ben Amram → 'Abed Ela ben Shalma</h1>
<p class="sub">The Israelite Samaritan priestly descent, generation by generation,
as <code>gedcom/samaritan-sources.ged</code> records it.</p>

<ul class="counts">
  <li><b>{len(people)}</b><span>generations</span></li>
  <li><b>{len(named)}</b><span>named</span></li>
  <li><b>{blank}</b><span>placeholders</span></li>
</ul>

<div class="warn">
  <p><strong>This is a placeholder skeleton, not a documented line.</strong>
  Only the top two and the bottom two people are named by any source. Everything
  between Itamar ben Aaron and Shalma is an unnamed placeholder record.</p>
  <p>The <em>length</em> of that stretch is borrowed from the parallel Phinhas
  line, which the source says ran <strong>112 generations father-to-son from
  Aaron</strong>. Nobody counted this line. Do not read the generation numbers
  below as a measurement of it.</p>
  <p>No name is invented anywhere here. A placeholder that acquires a name should
  get it from a source, not from the shape of the tree.</p>
</div>

<ol class="chain">
{chr(10).join(rows)}
</ol>

<footer>
<p>'Abed Ela ben Shalma is where the walk stops because the source calls him
“the forefather of the current priestly families” — born and active in Damascus,
titled <em>President of the House of 'Abtah</em>. Below him the file continues
through Yusef and Tabia ha'Abta'i to Tsedaka ben Tabia, first High Priest of the
Itamar line in 1624.</p>
<p>Source: <em>The High Priesthood and the Israelite Samaritan Priests</em>,
Benyamim Tsedaka, A.B. — The Samaritan News / The Samaritan Update,
March–April 2012. See <code>reports/samaritan-priesthood.md</code>.</p>
<p>Generated by <code>scripts/build-samaritan-spine-page.py</code>. Nothing on
this page has been sent anywhere; it is a local file.</p>
</footer>
</main></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="out/samaritan-spine.html")
    args = ap.parse_args()

    indi, fam = parse(GED)
    path = descent(indi, fam, ROOT, TARGET_NAME)
    out = REPO / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(indi, path), encoding="utf-8")
    print(f"{len(path)} generations, Aaron to 'Abed Ela -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
