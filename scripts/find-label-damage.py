"""Which labels did this pipeline write over somebody else's?

    python scripts/find-label-damage.py

**Ruled 2026-09-13**, after a first attempt got this wrong at scale: *"The point of this was you
were supposed to just find that there may have been only a single label that we got wrong based
off of this criteria."* She was nearly exactly right — the answer is **two**.

## The three criteria, and why the first two are not it

`reports/label-edits-emitted.tsv` is every label this pipeline has emitted;
`reports/garborg-live-labels.tsv` is what each item held when it was last fetched.

1. **"we emitted a value that differs from what the item held"** — 1,955 labels on 763 items,
   and almost all of it is the pipeline correcting ITSELF. `Q1036858` went
   `カール・アウグスト・エーレンスヴァルド` -> `カルル・アウグスト・エレンスヴェルド` when the
   transliteration rules were fixed. That is the 2026-08-30 ruling working, not damage.
2. **"...and the value we replaced is not one we ever emitted"** — 860 labels on 526 items. Still
   wrong: the ledger does not reach back to the earliest emissions, so our own older labels look
   like other people's.
3. **"...and the old value is a NATIVE name while ours is a phonetic rendering of a Latin
   string"** — **24 labels on 18 items**, and every one of them is real. `朱操` ->
   `ズフ・カオ`, `藤原乙麻呂` -> `フイヴァラ・ノ・オトマロ`, `扶餘德璋` -> `デオヒャング・プヨ`.
   That is the damage, and the shape is always the same: a name that was already in the script it
   belongs to, replaced by a transcription of its own romanisation.

The test for *native* is per language: a `ja` label in kanji with no kana, or a short `zh`/`ko`
label in Han with no interpunct. The test for *ours* is the mirror: katakana with no kanji, or a
Han string carrying `·`, which is how a foreign name is written in Chinese.

## What it found

22 of the 24 had already been reverted by hand before this ran. The two that had not are in
`reports/wikidata-label-restore.txt`.

**This is a detector, not a fix that runs by itself.** It prints; it emits no batch. A repair
that writes labels is exactly the thing that caused this.
"""

from __future__ import annotations

import collections
import csv
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EMITTED = ROOT / "reports" / "label-edits-emitted.tsv"
SNAPSHOT = ROOT / "reports" / "garborg-live-labels.tsv"
UA = {"User-Agent": "geni-repo/1.0 (emma@topazcomputing.com)"}

HAN = re.compile(r"[㐀-䶿一-鿿豈-﫿]")
KANA = re.compile(r"[぀-ゟ゠-ヿ]")


def native(lang: str, value: str) -> bool:
    """Is this the person's name in the script that language writes it in?"""
    if lang == "ja":
        return bool(HAN.search(value)) and not KANA.search(value)
    return bool(HAN.search(value)) and "·" not in value and len(value) <= 4


def phonetic(lang: str, value: str) -> bool:
    """Is this a transcription of a Latin string rather than a name?"""
    if lang == "ja":
        return bool(KANA.search(value)) and not HAN.search(value)
    return "·" in value or (lang == "zh" and len(value) > 4)


def read(path, delim="\t"):
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter=delim))


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    rows = read(EMITTED)
    ours = collections.defaultdict(set)
    for row in rows:
        if row["slot"].startswith("L"):
            ours[(row["qid"], row["slot"][1:])].add(row["value"])

    held = collections.defaultdict(dict)
    for row in read(SNAPSHOT):
        held[row["qid"]][row["lang"]] = row["label"]

    damage = {}
    for row in rows:
        if not row["slot"].startswith("L"):
            continue
        qid, lang, value = row["qid"], row["slot"][1:], row["value"]
        if lang not in ("ja", "zh", "ko"):
            continue
        before = held.get(qid, {}).get(lang)
        if before is None or before == value or before in ours[(qid, lang)]:
            continue
        if native(lang, before) and phonetic(lang, value):
            damage[(qid, lang)] = (before, value, row["first_emitted"])

    print("labels written over a native name: %d on %d item(s)"
          % (len(damage), len({q for q, _ in damage})))
    if not damage:
        return 0

    qids = sorted({q for q, _ in damage})
    live = {}
    for i in range(0, len(qids), 50):
        url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&ids="
               + "|".join(qids[i:i + 50]) + "&props=labels&format=json")
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA)) as fh:
            data = json.load(fh)
        for qid, entity in data.get("entities", {}).items():
            live[qid] = {k: v["value"] for k, v in entity.get("labels", {}).items()}

    standing = []
    for (qid, lang), (before, value, when) in sorted(damage.items()):
        now = live.get(qid, {}).get(lang)
        state = "restored" if now == before else "STILL WRONG"
        print("  %-12s %-3s %-14s -> %-22s  now %-22s %s"
              % (qid, lang, before, value, now, state))
        if now != before:
            standing.append((qid, lang, before))
    print()
    print("still carrying our value: %d" % len(standing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
