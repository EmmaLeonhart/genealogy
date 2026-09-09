#!/usr/bin/env python3
"""QuickStatements for labels carrying Genealogics' `|`, the separator for two spellings of one name.

**You, 2026-09-09**, having relabelled `Q105815062` by hand: *"There's a bunch of people on
wikidata with pipe charters in their name. I relabelled this one but our archive should have the
character and I want to fix all labels with it."*

**Your fix IS the rule, and that is why this batch exists now and not on 2026-09-08.** Asked the
day before whether the first reading should become the label and the rest aliases, you said the
pipes were *"a bit more complicated, I am not 100% sure how to interpret it lol"* and they were
held. `Q105815062` settles it in your own edit:

    was   Gerard|Gerald de Furnival
    Lmul  Gerard de Furnival        <- the FIRST reading
    Amul  Gerald de Furnival        <- the second, kept as an alias

**The readings are the COLUMNS of the split, token by token.** `Anna Maria|Maija Husgavel` is
`Anna Maria Husgavel` and `Anna Maija Husgavel` -- the only reading that keeps `Anna` and
`Husgavel` in both. `Rossor|Roger ap John|Jenkin ap Hywel` carries the alternation on two tokens
and expands the same way; 4 people are shaped like that.

**⛔ THE BRACKETED SHAPE IS HELD, all 140 of them.** `Ann Bincks (Benckes|Bench)` puts the
alternation INSIDE a variant group rather than between two readings of the whole name, and the
minimal pipe fix there -- `Ann Bincks (Benckes)` plus `Ann Bincks (Bench)` -- is not obviously
what anyone wants, while removing the bracket is a convention you have not ruled on. What
`Q105815062` demonstrates is the plain shape; that is what ships.

**⛔ THE COMMA TAIL IS LEFT ALONE, and that is deliberate rather than an oversight.** 373 of these
labels also carry one -- `Gallehaut|Guillaume de Rougé, baron de Derval` -- and
`scripts/build-noble-label-batch.py` removes exactly that, under a scope you narrowed to `noble`.
This batch fixes the pipe and nothing else, so the label comes out
`Gallehaut de Rougé, baron de Derval`: better than it was, and no decision taken that was not
asked for.

**Every language carrying the string is corrected, measured rather than assumed** -- the same
rule as the `noble` batch and for the reason § *`NN` is PRESERVED in `mul`* records: emitting on
one language while another holds the same value leaves the defect live.

**The alias is `Amul` and never `Aen`** -- § *The MARRIED name is the real name*: *"No aen are
ever supposed to be added."* `mul` falls back into every language that has no alias of its own,
which is why `Q105815062` shows `Gerald de Furnival` on all six rows from one edit.
"""
import csv
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "reports" / "imported-title-labels.tsv"
DEST = ROOT / "reports" / "wikidata-pipe-labels.qs"
HELD = ROOT / "reports" / "pipe-labels-held.tsv"


def readings(label):
    """Every reading of a piped label, first one first. `(readings, ok)`.

    `ok` is false for a shape this batch does not ship: a bracketed variant group, or two piped
    tokens that disagree about how many readings they hold. Padding the shorter one would repeat
    a name into a position it never occupied.
    """
    toks = label.split()
    piped = [t for t in toks if "|" in t]
    if not piped:
        return [label], True
    if any(ch in t for t in piped for ch in "()[]"):
        return [label], False
    widths = {len(t.split("|")) for t in piped}
    if len(widths) != 1:
        return [label], False
    out, seen = [], set()
    for i in range(widths.pop()):
        r = " ".join((t.split("|")[i] if "|" in t else t) for t in toks)
        r = " ".join(r.split())
        if r and r not in seen:
            seen.add(r)
            out.append(r)
    return out, True


def main():
    if not SRC.exists():
        sys.exit(f"{SRC.relative_to(ROOT)} is missing -- run "
                 "scripts/census-imported-title-labels.py, the 20-minute store pass")

    lines = [
        "# Genealogics separates two spellings of ONE name with `|`, and GZWDer's semi-automatic",
        "# import of January 2022 carried the separator into the label. The first reading becomes",
        "# the label and every other becomes an `Amul` alias -- which is the fix you made by hand",
        "# on `Q105815062` (`Gerard|Gerald de Furnival` -> `Gerard de Furnival` + `Gerald de",
        "# Furnival`), applied to the rest.",
        "#",
        "# The comma tail is deliberately NOT touched here: 373 of these also carry one, and",
        "# removing it is `build-noble-label-batch.py`'s job under a scope you set to `noble`.",
        "# Bracketed variant groups -- `Ann Bincks (Benckes|Bench)`, 140 of them -- are held in",
        "# `reports/pipe-labels-held.tsv` because they are a different shape.",
        "",
    ]
    held, langs, people, aliases = [], Counter(), 0, 0

    with SRC.open(encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f, delimiter="\t")
                if "|" in (r["live_mul"] or r["live_en"])]

    for row in sorted(rows, key=lambda r: (int(r["qid"][1:]), r["qid"])):
        live = row["live_mul"] or row["live_en"]
        reads, ok = readings(live)
        if not ok:
            held.append({"qid": row["qid"], "live": live, "why": "bracketed-or-uneven"})
            continue
        if not row["langs_carrying_live"]:
            held.append({"qid": row["qid"], "live": live, "why": "no-language-carries-it"})
            continue
        label, rest = reads[0], reads[1:]
        if label == live:
            held.append({"qid": row["qid"], "live": live, "why": "no-change"})
            continue
        people += 1
        lines.append(f"# {row['qid']}  {live}  ->  {label}"
                     + (f"   + {' | '.join(rest)}" if rest else ""))
        for lang in row["langs_carrying_live"].split():
            langs[lang] += 1
            lines.append(f'{row["qid"]}\tL{lang}\t"{label}"')
        for alias in rest:
            aliases += 1
            lines.append(f'{row["qid"]}\tAmul\t"{alias}"')
        lines.append("")

    tmp = DEST.with_suffix(".tmp")
    tmp.write_text("\n".join(lines), encoding="utf-8")
    os.replace(tmp, DEST)

    held.sort(key=lambda r: (int(r["qid"][1:]), r["qid"]))
    tmp = HELD.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["qid", "live", "why"], delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(held)
    os.replace(tmp, HELD)

    print(f"wrote {DEST.relative_to(ROOT)}: {people} people, "
          f"{sum(langs.values())} label edits, {aliases} aliases")
    for lang, n in langs.most_common():
        print(f"    {n:5}  L{lang}")
    print(f"\nheld -> {HELD.relative_to(ROOT)}: {len(held)}")
    for why, n in Counter(h["why"] for h in held).most_common():
        print(f"    {n:5}  {why}")


if __name__ == "__main__":
    main()
