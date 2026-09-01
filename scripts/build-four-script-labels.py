"""`hi`, `ar`, `ru` and `el` labels — the four scripts that had never been started.

    py scripts/build-four-script-labels.py

**Emma, 2026-09-01: "Wire hi/ar/ru/el now."** `queue.md` § *Labels in seven languages* has had
them listed since the beginning — *"Devanagari, Arabic, Cyrillic and Greek chosen for script
coverage"* — and nothing had ever emitted one.

## Why transcription is the method here, where `ja`/`zh`/`ko` withhold it

The CJK batches refuse to transcribe a Latin name, because a Chinese or Japanese or Korean name
may exist in its own script already and a transcription would be second-best. **These four have
no such alternative.** Her own description of the job is *"English → the four remaining
scripts"*: for a Norwegian farmer there is no Russian or Greek or Hindi or Arabic form of the
name waiting to be found, and writing one is the whole task rather than a fallback.

So the standard here is hers: *"incorrect romanization or incorrect representations in katakana
are totally acceptable. An incorrect name is not."* `Флйгаре` may not be how a Russian would
spell *Flygare*, but it is that person's name in Cyrillic letters, and nothing invents a
different name.

## Scope: people who already have an item

**43,680 people carry a QID.** Everyone else would need creating first, and their labels ride
along with the creation rather than being a separate batch — which is what the daily builder
already does for `en`/`mul`/`ja`/`zh`/`ko`. Emitting four more languages for 1.29 million people
who do not exist on Wikidata yet would be five million edits nobody can apply.

## What the engine does, and two things fixed on the way

`scripts/translit_scripts.py` holds the per-letter tables. Reading its output found two
systematic defects, neither of which a test would have caught:

* **Proper names are capitalised in Cyrillic and Greek.** Every label came out `арне гарборг`
  rather than `Арне Гарборг`. Devanagari and Arabic have no case, so they are untouched.
* **`chr` is a hard k, not the `ch` digraph** — `Christina` was `чристина` and `χριστινα`. The
  identical bug had just been found in `translit_ko_latin`, which is what made it worth looking
  for here.

Writes `reports/wikidata-four-script-labels.json` and `.md`.
"""

from __future__ import annotations

import collections
import csv
import io
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

from translit_scripts import render  # noqa: E402

LABELS = REPO / "reports" / "derived-labels.csv"
OUT = REPO / "reports" / "wikidata-four-script-labels.json"
OUT_MD = REPO / "reports" / "wikidata-four-script-labels.md"

CODES = ("ru", "el", "hi", "ar")

#: A label with no Latin letter has nothing for these tables to read.
LATIN = re.compile(r"[A-Za-zÀ-ÿ]")


def main() -> int:
    edits = []
    why = collections.Counter()
    per_lang = collections.Counter()
    with LABELS.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            qid = (r.get("qid") or "").strip()
            label = (r.get("label_en") or "").strip()
            if not qid:
                why["no Wikidata item -- their labels ride along with the creation"] += 1
                continue
            if not label:
                why["has an item but no label of ours to transcribe"] += 1
                continue
            if not LATIN.search(label):
                why["label has no Latin letters for these tables to read"] += 1
                continue
            got = 0
            for code in CODES:
                value = render(label, code)
                if not value:
                    continue
                got += 1
                per_lang[code] += 1
                edits.append({
                    "id": f"{code}_label:{r['geni_id']}",
                    "type": "set_label",
                    "source": "step 6 of Emma's label order -- hi/ar/ru/el",
                    "subject": {"qid": qid, "geni_id": r["geni_id"]},
                    "requires": [],
                    "label": {"language": code, "value": value},
                    "kind": "add",
                    "derived_from": "transcribed from the Latin label",
                })
            why["EMITTED for a person with an item" if got else
                "an item and a label, but nothing rendered"] += 1

    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    lines = ["# Steps 6-9 — `hi`, `ar`, `ru`, `el`", "",
             "Built by `scripts/build-four-script-labels.py`. **Emits nothing to Wikidata.**", "",
             "Emma, 2026-09-01: **\"Wire hi/ar/ru/el now.\"** These four have been listed in the "
             "seven-languages item since the beginning and nothing had ever emitted one.", "",
             f"- **{len(edits):,} labels** over {why['EMITTED for a person with an item']:,} "
             "people who already carry a Wikidata item.", "",
             "| language | labels |", "| --- | ---: |"]
    for code in CODES:
        lines.append(f"| `{code}` | {per_lang[code]:,} |")
    lines += ["", "## Scope, and why it is not everybody", "",
              "Only people who already have a QID. Everyone else needs creating first and their "
              "labels ride along with the creation, which is what the daily builder already does "
              "for `en`/`mul`/`ja`/`zh`/`ko`. Four more languages across 1.29 million people who "
              "are not on Wikidata yet would be five million edits nobody can apply.", "",
              "## Why transcription is right here and wrong for CJK", "",
              "The CJK batches refuse to transcribe a Latin name, because a Chinese, Japanese or "
              "Korean name may already exist in its own script. These four have no such "
              "alternative — for a Norwegian farmer there is no Russian or Greek form waiting to "
              "be found, so writing one is the task rather than a fallback.", "",
              "## Skipped", "", "| reason | people |", "| --- | ---: |"]
    for k, v in sorted(((k, v) for k, v in why.items() if not k.startswith("EMITTED")),
                       key=lambda x: -x[1]):
        lines.append(f"| {k} | {v:,} |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(f"wrote {OUT.relative_to(REPO)} - {len(edits):,} labels")
    for code in CODES:
        print(f"   {per_lang[code]:>8,}  {code}")
    print()
    for k, v in why.most_common():
        print(f"   {v:>9,}  {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
