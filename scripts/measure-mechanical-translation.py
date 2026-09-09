"""How many of OUR people's names can be translated with no transliteration at all.

`scripts/measure-name-item-languages.py` answers "what languages do the 823,907
downloaded name items carry labels in?" and the raw answer for Japanese is bleak: **9.0%**.
That number is the wrong one to plan from, and this script computes the right one.

Emma, 2026-08-18: *"I think in Japanese there's a standard katakana rendering of the name
Jack. There's a standard katakana rendering of the name John."* She is right, and the raw
share hides it — because the 824,358 name items are dominated by long-tail surnames that
exist on Wikidata and are borne by nobody in this tree, while `John` and `Maria` are borne
by thousands. **The question is per-person, not per-item**, so every figure here is
weighted by `occurrences`: how many name-uses in the corpus can be rendered.

A "name-use" is one person carrying one token — somebody with a given name and a surname
is two uses. That is the right denominator because a label is assembled from all of them.

Reads `reports/name-resolution.csv` (our tokens, with the QIDs they resolve to) joined to
`reports/name-item-languages.csv` (what each item is labelled in). Both are on disk; this
makes no request and loads no merge.

    python scripts/measure-mechanical-translation.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LANGS_CSV = REPO / "reports" / "name-item-languages.csv"
RES_CSV = REPO / "reports" / "name-resolution.csv"
OUT_MD = REPO / "reports" / "mechanical-translation.md"

LANGS = ["mul", "en", "ja", "zh", "ko", "ar", "he", "ru",
         "de", "fr", "es", "pt", "it", "nl", "sv", "nb", "da", "fi", "pl"]

#: A verdict that names exactly one item. `ambiguous` is held out rather than
#: guessed at: picking the first QID of several is the diacritic-folding mistake
#: in a new place, and `CLAUDE.md` § *One name item per USAGE* says a real
#: ambiguity is Emma's call.
RESOLVED = {"resolved"}

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def main() -> None:
    have: dict[str, dict[str, bool]] = {}
    with LANGS_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            have[row["qid"]] = {l: bool(row.get(l)) for l in LANGS}

    uses = Counter()          # language -> name-uses renderable
    total = 0
    resolved = 0
    ambiguous = 0
    no_item = 0
    by_kind = Counter()
    kind_ja = Counter()

    with RES_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            occ = int(row["occurrences"] or 0)
            kind = row.get("kind", "")
            verdict = (row.get("verdict") or "").strip()
            total += occ
            by_kind[kind] += occ
            qids = [q for q in (row.get("qids") or "").replace(";", " ")
                    .replace(",", " ").split() if q.startswith("Q")]
            if not qids:
                no_item += occ
                continue
            if verdict not in RESOLVED or len(qids) != 1:
                ambiguous += occ
                continue
            resolved += occ
            h = have.get(qids[0])
            if not h:
                continue
            for l in LANGS:
                if h[l]:
                    uses[l] += occ
            if h["ja"]:
                kind_ja[kind] += occ

    pct = lambda n, d: f"{n / d:.1%}" if d else "—"
    lines = [
        "# How much of the naming can be done mechanically",
        "",
        f"**{total:,} name-uses** in the corpus — one person carrying one token, so "
        "somebody with a given name and a surname counts twice. Weighted by people "
        "throughout, which is the whole point: the raw per-item share in "
        "`name-item-languages.md` is dominated by long-tail surnames nobody here bears.",
        "",
        "| | name-uses | share |",
        "| --- | ---: | ---: |",
        f"| resolve to exactly one name item | {resolved:,} | {pct(resolved, total)} |",
        f"| resolve to several (held for Emma) | {ambiguous:,} | {pct(ambiguous, total)} |",
        f"| no name item on Wikidata at all | {no_item:,} | {pct(no_item, total)} |",
        "",
        "## Renderable without transliterating anything",
        "",
        "`of resolved` is the honest ceiling for the mechanical path; `of all` is what "
        "it delivers against the whole corpus as it stands today.",
        "",
        "| language | name-uses | of all | of resolved |",
        "| --- | ---: | ---: | ---: |",
    ]
    for l in LANGS:
        lines.append(f"| `{l}` | {uses[l]:,} | {pct(uses[l], total)} | "
                     f"{pct(uses[l], resolved)} |")
    lines += ["", "## Japanese, by what kind of name the token is", "",
              "| kind | name-uses | with a `ja` label | share |",
              "| --- | ---: | ---: | ---: |"]
    for kind, n in by_kind.most_common():
        lines.append(f"| {kind} | {n:,} | {kind_ja[kind]:,} | {pct(kind_ja[kind], n)} |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"{total:,} name-uses; {resolved:,} resolved ({pct(resolved, total)}), "
          f"{ambiguous:,} ambiguous, {no_item:,} no item")
    for l in LANGS:
        print(f"  {l:<4} {uses[l]:>9,}  of all {pct(uses[l], total):>6}  "
              f"of resolved {pct(uses[l], resolved):>6}")
    print(f"wrote {OUT_MD.relative_to(REPO)}")


if __name__ == "__main__":
    main()
