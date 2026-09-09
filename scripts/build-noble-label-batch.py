#!/usr/bin/env python3
"""QuickStatements for the `noble` rank, removed from the labels it was never a name in.

**You, 2026-09-09**, on `Q110731142` — `noble Nike|Victoria Soutzaina`: *"there's a fuckton of
people with the prefix 'noble' on wikidata that comes from the same guy in 2022... all of them
have the title in their mul label which is more like an English label and I would like to use our
completely present wikidata export that should contain all of these people and redo their labels
agentically to be proper."*

**⛔ SCOPE IS `noble` AND ONLY `noble`, and you narrowed it yourself.** Offered every lowercase
rank — 1,029 people, the same artefact from the same imports, `knight`, `ridder`, `farmer`,
`esquire`, `skipper`, `mistress` — You chose **`noble` only**. `reports/title-label-proposals.tsv`
holds the rest, computed and waiting; they are not emitted.

**⛔ AND THE PIPES ARE HELD, BY YOUR RULING THE SAME DAY:** *"bruh no the pipes are a bit more
complicated, I am not 100% sure how to interpret it lol."* So a `noble` label that also carries a
`|` — 7 of the 464 — is **excluded**, even though the rank half of it is settled. Your uncertainty
is about how to read `Nike|Victoria` at all, and a batch that removed the rank and left the pipe
would commit to half an interpretation you have not made.

**Nothing goes in the rank's place** — your third ruling, and it is `CLAUDE.md`
§ *A TITLE IS NOT A NAME* and § *A DESCRIPTION MARKER COMES OUT OF THE LABEL* already: dropped
from the name, nothing put back. **No `Amul` carrying the old string either.** The `Amul`
preservation of § *The MARRIED name is the real name* exists to stop a HAND EDIT of yours being
overwritten by a label; these are `GZWDer`'s bot labels of January 2022, and preserving
`noble Nike Soutzaina` as a searchable alias is exactly the *"something in its place"* you
refused.

**No `D<lang>` line and no edit summary**, § *NO descriptions and NO edit summaries*, categorical.

**Every language carrying the bad string is corrected, not just `mul`.** Measured: `en` 454,
`mul` 240, `nl` 31 — so `mul` is a MINORITY of them, and a `mul`-only batch would leave the rank
live on `en` for 454 people. That is the same shape as § *`NN` is PRESERVED in `mul`*, where
emitting on one language nearly erased the marker from the 1,271 items holding it in another:
**which language a value sits in is measured, never assumed.**
"""
import csv
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "reports" / "title-label-proposals.tsv"
DEST = ROOT / "reports" / "wikidata-noble-labels.qs"

RANK = "noble"


def main():
    if not SRC.exists():
        sys.exit(f"{SRC.relative_to(ROOT)} is missing -- run "
                 "scripts/propose-title-label-fixes.py (and the census before it)")

    picked, langs = [], Counter()
    skipped = Counter()
    with SRC.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["hold"]:
                skipped[row["hold"]] += 1
                continue
            if row["leading_title"].split()[:1] != [RANK]:
                skipped["not-noble"] += 1
                continue
            if row["kind"] != "title":
                skipped["carries-a-pipe"] += 1
                continue
            if not row["langs_carrying_live"]:
                skipped["no-language-carries-it"] += 1
                continue
            picked.append(row)

    lines = [
        "# Every one of these labels reads `noble <name>` -- a RANK that Genealogics files in",
        "# its own column and GZWDer's semi-automatic import of January 2022 carried into the",
        "# name field verbatim. Kristbaumbot then copied `en` into `mul` in June 2025, so the",
        "# language-neutral label became an English sentence. Nothing here is a name change:",
        "# the rank comes off and the name that was already there is what remains.",
        "#",
        "# Scope is `noble` alone and pipe-free, both by Emma's ruling of 2026-09-09.",
        "# `reports/title-label-proposals.tsv` holds every other lowercase rank, computed and",
        "# deliberately not emitted.",
        "",
    ]
    for row in sorted(picked, key=lambda r: (int(r["qid"][1:]), r["qid"])):
        live = row["live_mul"] or row["live_en"]
        lines.append(f"# {row['qid']}  {live}  ->  {row['proposed_label']}")
        for lang in row["langs_carrying_live"].split():
            langs[lang] += 1
            lines.append(f'{row["qid"]}\tL{lang}\t"{row["proposed_label"]}"')
        lines.append("")

    tmp = DEST.with_suffix(".tmp")
    tmp.write_text("\n".join(lines), encoding="utf-8")
    os.replace(tmp, DEST)

    edits = sum(langs.values())
    print(f"wrote {DEST.relative_to(ROOT)}: {len(picked)} people, {edits} label edits")
    for lang, n in langs.most_common():
        print(f"    {n:5}  L{lang}")
    print("\nnot emitted:")
    for why, n in skipped.most_common():
        print(f"    {n:6}  {why}")


if __name__ == "__main__":
    main()
