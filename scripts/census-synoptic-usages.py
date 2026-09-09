"""Every place the repo says "synoptic tree", and which of the two things it means.

    python scripts/census-synoptic-usages.py

**Emma, 2026-08-29:** *"it is consistently conflated between the union of all the geni gedcoms
and the union of that tree with all data sources."* Two meanings, one phrase:

* **geni** — every `.ged` under `exports/` merged, i.e. `out/merged.ged`.
* **full** — that tree joined to every other source, Wikidata above all. Does not exist yet.

Her instruction is to put **every specific usage** to her rather than pick a definition and
apply it everywhere. 181 occurrences across 26 files is too many questions to be answerable, so
this classifies each one first and leaves only the genuinely undecidable ones to ask about.

## How a usage is classified, and why it is keyword-based rather than clever

A line is `geni` when it sits beside something only the Geni union can mean — `merged.ged`,
`exports/`, `genimerge merge`, a people count, the rebuild chain. It is `full` when it sits
beside Wikidata, a QID, a union with another source, or a thing described as not existing yet.
It is `unclear` otherwise, and **unclear is the answer that matters** — those are the ones that
become questions.

No line is guessed into a bucket on tone. A keyword either appears in the line's own text or the
line is `unclear`; that is deliberately blunt, because the failure this exists against is
somebody deciding a usage means what would be convenient.

Writes `reports/synoptic-usages.tsv` — file, line, verdict, the line itself.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
OUT = ROOT / "reports" / "synoptic-usages.tsv"

SUFFIXES = (".md", ".py", ".txt", ".tsv")
SKIP_DIRS = {".git", "wikidata", "exports", "gedcom", "geni_pages", "geni-scraping"}

#: Words that can only belong to the Geni union.
GENI = re.compile(r"merged\.ged|exports/|genimerge merge|rebuild-everything|"
                  r"\bgedcoms?\b|\.ged\b|derived-|display-names|the merge\b", re.I)

#: Words that can only belong to the union with other sources.
FULL = re.compile(r"wikidata|\bQ\d{3,}|qid|union with|all data sources|zipper|"
                  r"\bp2600\b|other sources", re.I)


def main():
    rows = []
    for path in sorted(ROOT.rglob("*")):
        if path.suffix not in SUFFIXES or not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "synoptic" not in text.lower():
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if "synoptic" not in line.lower():
                continue
            geni, full = bool(GENI.search(line)), bool(FULL.search(line))
            verdict = ("both named" if geni and full else
                       "geni" if geni else "full" if full else "unclear")
            rows.append((str(path.relative_to(ROOT)).replace("\\", "/"), n, verdict,
                         " ".join(line.split())[:200]))

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        fh.write("file\tline\tverdict\ttext\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")

    counts = {}
    for _f, _n, verdict, _t in rows:
        counts[verdict] = counts.get(verdict, 0) + 1
    print(f"{len(rows)} usages of 'synoptic' across "
          f"{len({r[0] for r in rows})} files\n")
    for verdict in ("geni", "full", "both named", "unclear"):
        print(f"   {verdict:<12}{counts.get(verdict, 0):>5}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    print("\nthe UNCLEAR ones are what needs deciding:")
    for f, n, verdict, t in rows:
        if verdict == "unclear":
            print(f"   {f}:{n}  {t[:110]}")


if __name__ == "__main__":
    main()
