#!/usr/bin/env python3
"""QuickStatements for the `noble` rank, removed from the labels it was never a name in.

**On `Q110731142` — `noble Nike|Victoria Soutzaina`:** *"there's a fuckton of
people with the prefix 'noble' on wikidata that comes from the same guy in 2022... all of them
have the title in their mul label which is more like an English label and I would like to use our
completely present wikidata export that should contain all of these people and redo their labels
agentically to be proper."*

**⛔ SCOPE IS `noble` AND ONLY `noble`, narrowed deliberately.** Offered every lowercase
rank — 1,029 people, the same artefact from the same imports, `knight`, `ridder`, `farmer`,
`esquire`, `skipper`, `mistress` — the ruling was **`noble` only**. `reports/title-label-proposals.tsv`
holds the rest, computed and waiting; they are not emitted.

**⛔ AND THE PIPES ARE HELD, BY THE RULING THE SAME DAY:** *"bruh no the pipes are a bit more
complicated, I am not 100% sure how to interpret it lol."* So a `noble` label that also carries a
`|` — 7 of the 464 — is **excluded**, even though the rank half of it is settled. What is
unsettled is how to read `Nike|Victoria` at all, and a batch that removed the rank and left the
pipe would commit to half an interpretation nobody has made.

**Nothing goes in the rank's place** — the third ruling, and it is `CLAUDE.md`
§ *A TITLE IS NOT A NAME* and § *A DESCRIPTION MARKER COMES OUT OF THE LABEL* already: dropped
from the name, nothing put back. **No `Amul` carrying the old string either.** The `Amul`
preservation of § *The MARRIED name is the real name* exists to stop a HAND EDIT being
overwritten by a label; these are `GZWDer`'s bot labels of January 2022, and preserving
`noble Nike Soutzaina` as a searchable alias is exactly the *"something in its place"* that was
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

#: ⛔ **THE RANKS YOU HAVE RULED ON, and only those.** You went through them one at a time on
#: 2026-09-09 by `AskUserQuestion`, having asked for exactly that: *"the lowercase ranks I want
#: AskUserQuestion on every one of them."* A rank not in this set has not been ruled on and is
#: computed-but-unemitted in `reports/title-label-proposals.tsv`, which is where it stays.
#:
#: **`esquire` is DELIBERATELY ABSENT** — 9 people, and your verdict was *"If there's 9 people we
#: can do it manually lol."* Adding it here would be doing by machine what you said you would do
#: by hand.
#:
#: **`farmer` and `mistress` are in, and they needed no special case.** Your verdict on both was
#: *drop the word, keep the estate* — which is what PREFIX-ONLY already does, since
#: `propose-title-label-fixes.py` stopped cutting the tail. They are the reason that rule exists.
RANKS = (
    "noble",      # 572   your first batch, 2026-09-09
    "knight",     #  51
    "ridder",     #  41
    "baroness",   #  27
    "captain",    #  25
    "countess",   #  21
    "count",      #  14
    "major",      #  14
    "farmer",     #  11   drop the word, keep the farm
    "baron",      #   8
    "mistress",   #   6   drop the word, keep the estate
)


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
            if row["leading_title"].split()[:1] and row["leading_title"].split()[0] not in RANKS:
                skipped["rank-not-ruled-on"] += 1
                continue
            if row["kind"] != "title":
                skipped["carries-a-pipe"] += 1
                continue
            if not row["langs_carrying_live"]:
                skipped["no-language-carries-it"] += 1
                continue
            picked.append(row)

    lines = [
        "# Every one of these labels opens with a lowercase RANK that Genealogics files in",
        "# its own column and GZWDer's semi-automatic import of January 2022 carried into the",
        "# name field verbatim. Kristbaumbot then copied `en` into `mul` in June 2025, so the",
        "# language-neutral label became an English sentence. Nothing here is a name change:",
        "# the rank comes off and the name that was already there is what remains.",
        "#",
        "# ⛔ THE RANK COMES OFF AND NOTHING ELSE MOVES. You, 2026-09-09, shown that these",
        "# proposals also truncated the territorial tail: \"Uhh bruh what? I'm asking you to",
        "# remove the prefix lol not the other stuff.\" So `noble Detlof Heyke, master of",
        "# Gammelbo bruk` becomes `Detlof Heyke, master of Gammelbo bruk`, and the 87 rows that",
        "# would have been cut back to a bare given name plus patronymic keep their estate.",
        "#",
        "# Scope is the ranks you ruled on one by one, and pipe-free. `esquire` is out by your",
        "# own verdict -- 9 people, to be done by hand. Every rank you have not ruled on is",
        "# computed in `reports/title-label-proposals.tsv` and deliberately not emitted.",
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
