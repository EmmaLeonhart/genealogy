"""Step 3 of Emma's label order: the `ja` label, for everyone it can be had for honestly.

**Emma, 2026-08-17:** *"and then the Japanese gets made for all languages, and then the
Chinese gets made for all languages"* -- one batch per language over the whole population.

**This emits only the `ja` labels that require no invention**, and says plainly how many it
cannot reach. Two sources:

1. **Wikidata's own `ja` label**, for a linked person who has one -- `カール・マルテル`,
   `ロロ`. Somebody wrote it; it beats anything derived. 4,547 people.
2. **The name as written**, for a person whose name is in Han characters or kana. Japanese
   writes a Chinese or Japanese name in its own characters, so the `ja` label *is* the
   name. 38,322 people.

WHAT IT DOES NOT DO, AND WHY THAT IS THE WHOLE POINT

**Hangul is excluded.** 5,291 people have a name written only in hangul, and a `ja` label
must not be the hangul -- Japanese does not write Korean names that way. Their `ja` needs a
katakana reading, which is the same problem as the Latin names below.

**401,410 people need English -> katakana and get nothing here.** Emma's method for that
direction is a hand-built table -- *"hand-built tables, except CJK -> English"* -- and a
table that turns `Brodsky` into `ブロツキー` correctly is a real piece of work with real
failure modes: syllabification, long vowels, and the fact that established Japanese
spellings of European names are conventional rather than derivable. **Guessing at 401,410
names would be the single largest act of invention in this repo.** It is sized here and
left for a deliberate build.

    py scripts/build-ja-label-batch.py

Offline: `reports/derived-labels.csv`, `reports/derived-family.csv`, the local store.
Writes `reports/wikidata-ja-labels.json`. Emits nothing to Wikidata.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from genimerge import wikistore  # noqa: E402

LABELS = REPO / "reports" / "derived-labels.csv"
FAMILY = REPO / "reports" / "derived-family.csv"
STORE = REPO / "wikidata" / "items"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
OUT = REPO / "reports" / "wikidata-ja-labels.json"
MD = REPO / "reports" / "wikidata-ja-labels.md"

csv.field_size_limit(10 ** 7)
HAN = re.compile(r"[\u3400-\u9fff]")
KANA = re.compile(r"[\u3040-\u30ff]")
HANGUL = re.compile(r"[\uac00-\ud7af]")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    cjk, total = {}, 0
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            total += 1
            c = (r.get("cjk_names") or "").split(" | ")[0].strip()
            if c:
                cjk[r["geni_id"]] = c
    qid = {}
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("qid"):
                qid[r["geni_id"]] = r["qid"]

    ids = sorted(set(qid.values()))
    wd = {}
    with wikistore.StoreReader(STORE, INDEX) as rd:
        for i in range(0, len(ids), 5000):
            for q, e in rd.entities(ids[i:i + 5000]).items():
                v = ((e.get("labels") or {}).get("ja") or {}).get("value")
                if v:
                    wd[q] = v

    src, hangul_only = {}, 0
    for g, q in qid.items():
        if q in wd:
            src[g] = (wd[q], "wikidata's own ja label")
    for g, c in cjk.items():
        if g in src:
            continue
        if HANGUL.search(c) and not (HAN.search(c) or KANA.search(c)):
            hangul_only += 1
            continue
        if HAN.search(c) or KANA.search(c):
            src[g] = (c, "the name as written, which Japanese uses unchanged")

    edits = [{
        "id": "ja_label:%s" % g,
        "type": "set_label",
        "source": "step 3 of Emma's label order",
        "subject": {"qid": None, "geni_id": g},
        "requires": [],
        "label": {"language": "ja", "value": v},
        "kind": "add",
        "derived_from": why,
    } for g, (v, why) in sorted(src.items())]
    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    by = Counter(why for _, why in src.values())
    short = total - len(src)
    md = ["# Step 3 — the `ja` label", "",
          "Built by `scripts/build-ja-label-batch.py`. **Emits nothing to Wikidata**, and "
          "emits only labels that require no invention.", "",
          "- individuals: **%d**" % total,
          "- `ja` available honestly: **%d**" % len(src),
          "- not reached: **%d**" % short, "",
          "| where it comes from | people |", "| --- | ---: |"]
    md += ["| %s | %d |" % (k, v) for k, v in by.most_common()]
    md += ["", "## What is deliberately not emitted", "",
           "**Hangul-only names: %d.** A `ja` label must not be the hangul — Japanese does "
           "not write Korean names that way. They need a katakana reading, which is the "
           "same unsolved problem as the Latin names." % hangul_only, "",
           "**English → katakana: the rest.** Emma's method for this direction is a "
           "hand-built table (*\"hand-built tables, except CJK → English\"*). A table that "
           "turns `Brodsky` into `ブロツキー` correctly has real failure modes — "
           "syllabification, long vowels, and the fact that established Japanese spellings "
           "of European names are conventional rather than derivable. Guessing at that many "
           "names would be the largest act of invention in this repo, so it is sized here "
           "and left for a deliberate build."]
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("individuals %d; ja available %d; not reached %d" % (total, len(src), short))
    for k, v in by.most_common():
        print("    %-46s %d" % (k, v))
    print("    hangul-only, deliberately skipped              %d" % hangul_only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
