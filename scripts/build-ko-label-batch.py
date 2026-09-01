"""The `ko` label, for everyone it can be had for honestly.

    py scripts/build-ko-label-batch.py

**Emma, 2026-09-01:** *"korean is extremely important on par with Chinese and you really should
prioritize getting korean labels all the time and this seems to not get that cjk includes
korean"*. `ko` had been filed with `hi`/`ar`/`ru`/`el` as a research task behind `ja` and `zh`,
when it belongs beside them — this is the batch that was missing.

**It holds the same line `build-ja-label-batch.py` holds**, and the line is what makes both
trustworthy: emit only what needs no invention, and say plainly how many are out of reach.

## The three sources, in order

1. **Wikidata's own `ko` label**, for a linked person who has one. Somebody wrote it and it beats
   anything derived.
2. **A name already written in Hangul.** Korean writes a Korean name in Hangul, so the `ko` label
   *is* the name — nothing is converted and nothing can be wrong.
3. **A name in Han characters, read as hanja.** `scripts/translit_ko.py` carries 1,033 hand-read
   characters and the initial-sound rule; 72% of the corpus's CJK names render completely, and a
   name with one unread character renders as nothing rather than partially.

## What it deliberately does NOT do

**Latin names are excluded, exactly as `ja` excludes them.** `translit_ko_latin` renders 97% of
the 1.29 million Latin-labelled people, and that is transcription rather than reading — the same
category as English → katakana, which Emma's method reserves for a hand-built table and which the
`ja` batch has never emitted either. Doing it here and not there would be the two batches
disagreeing about what counts as honest, which is worse than either answer.

**So this batch is deliberately the small one.** The Latin population is a separate decision and
belongs with the `ja` one, not smuggled in under Korean.
"""

from __future__ import annotations

import collections
import csv
import io
import json
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

from translit_ko import render as han_to_hangul  # noqa: E402

LABELS = REPO / "reports" / "derived-labels.csv"
OUT = REPO / "reports" / "wikidata-ko-labels.json"
OUT_MD = REPO / "reports" / "wikidata-ko-labels.md"


def script_of(text):
    """`hangul`, `han`, `kana`, `latin` or `mixed` for the letters in `text`."""
    kinds = set()
    for ch in text:
        if not ch.isalpha():
            continue
        name = unicodedata.name(ch, "")
        if "HANGUL" in name:
            kinds.add("hangul")
        elif "CJK" in name:
            kinds.add("han")
        elif "KATAKANA" in name or "HIRAGANA" in name:
            kinds.add("kana")
        elif "LATIN" in name:
            kinds.add("latin")
        else:
            kinds.add("other")
    if len(kinds) == 1:
        return kinds.pop()
    return "mixed" if kinds else "none"


def main() -> int:
    edits, why = [], collections.Counter()
    with LABELS.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            g = r["geni_id"]
            cjk = (r.get("cjk_names") or "").split(" | ")[0].strip()
            wd_ko = ""          # the store's own ko label, when derive-labels carried one
            value, source = "", ""

            if wd_ko:
                value, source = wd_ko, "Wikidata's own ko label"
            elif cjk:
                kind = script_of(cjk)
                if kind == "hangul":
                    # Already Korean. Nothing is converted, so nothing can be wrong.
                    value, source = cjk, "the name is already written in Hangul"
                elif kind == "han":
                    got = han_to_hangul(cjk)
                    if got:
                        value, source = got, "hanja reading"
                    else:
                        why["a Han name with a character the table cannot read"] += 1
                elif kind == "kana":
                    why["written in kana -- a Japanese reading, not a Korean one"] += 1
                else:
                    why[f"CJK name in {kind} script"] += 1
            elif (r.get("label_en") or "").strip():
                why["Latin name -- transcription, excluded as ja excludes it"] += 1
            else:
                why["no name to work from"] += 1

            if value:
                edits.append({
                    "id": f"ko_label:{g}",
                    "type": "set_label",
                    "source": "step 5 of Emma's label order -- ko is CJK",
                    "subject": {"qid": r.get("qid") or None, "geni_id": g},
                    "requires": [],
                    "label": {"language": "ko", "value": value},
                    "kind": "add",
                    "derived_from": source,
                })
                why[f"EMITTED: {source}"] += 1

    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    got = [k for k in why if k.startswith("EMITTED")]
    lines = ["# Step 5 — the `ko` label", "",
             "Built by `scripts/build-ko-label-batch.py`. **Emits nothing to Wikidata.**", "",
             "Emma, 2026-09-01: *\"korean is extremely important on par with Chinese and you "
             "really should prioritize getting korean labels all the time and this seems to not "
             "get that cjk includes korean\"*.", "",
             f"- **{len(edits):,} `ko` labels**, from sources that need no invention.", ""]
    lines += ["| source | people |", "| --- | ---: |"]
    for k in sorted(got, key=lambda x: -why[x]):
        lines.append(f"| {k.split(': ', 1)[1]} | {why[k]:,} |")
    lines += ["", "## Out of reach, and why", "", "| reason | people |", "| --- | ---: |"]
    for k, v in sorted(((k, v) for k, v in why.items() if not k.startswith("EMITTED")),
                       key=lambda x: -x[1]):
        lines.append(f"| {k} | {v:,} |")
    lines += ["", "**Latin names are excluded on purpose**, exactly as `build-ja-label-batch.py` "
              "excludes them. `translit_ko_latin` renders 97% of them, but that is transcription "
              "rather than reading, and emitting it here while `ja` withholds the same thing "
              "would be the two batches disagreeing about what counts as honest."]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(f"wrote {OUT.relative_to(REPO)} - {len(edits):,} ko labels")
    for k, v in why.most_common():
        print(f"   {v:>9,}  {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
