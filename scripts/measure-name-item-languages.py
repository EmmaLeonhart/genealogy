"""Which languages do the downloaded name items actually carry labels in?

**This is the ceiling on mechanical name translation.** Emma, 2026-08-18: *"there should
be a sizable amount of individuals for whom we're effectively able to just translate the
names, really, based off of the existing labels… I think in Japanese there's a standard
katakana rendering of the name Jack. There's a standard katakana rendering of the name
John."* If `John` (`Q4925477`) carries `ja` = ジョン, then a person called John gets a
Japanese label without anybody transliterating anything. If it does not, no amount of
assembling helps and the gap has to be filled by adding labels **to the name item**,
which is her second point: *"we're going to be… having to add labels in other languages
to the name objects."*

So the question this answers is not "how many name items do we hold" — that is settled,
`scripts/collect-name-item-qids.py` enumerated 824,358 by `P31` and 99.9% are in the
store. It is **how many of them are usable in each target language**.

**Reads the local store only.** No Wikidata request is made or possible here; the shards
under `wikidata/items/` are the whole input. `CLAUDE.md` § *Never query Wikidata*.

Writes `reports/name-item-languages.csv` — one row per name item, its classes, and a
column per target language holding the label if present. The per-language totals go to
`reports/name-item-languages.md`.

    python scripts/measure-name-item-languages.py
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEEDS = REPO / "reports" / "name-item-qids.tsv"
SHARDS = sorted((REPO / "wikidata" / "items").glob("items-*.jsonl.gz"))
OUT_CSV = REPO / "reports" / "name-item-languages.csv"
OUT_MD = REPO / "reports" / "name-item-languages.md"

#: The seven-language target from `emission-spec.md`, plus the Nordic and Iberian
#: languages the tree is actually full of, plus `mul`.
LANGS = ["mul", "en", "ja", "zh", "ko", "ar", "he", "ru",
         "de", "fr", "es", "pt", "it", "nl", "sv", "nb", "da", "fi", "pl"]

CLASS_NAMES = {
    "Q101352": "family name",
    "Q12308941": "male given name",
    "Q11879590": "female given name",
    "Q202444": "given name",
    "Q3409032": "unisex given name",
    "Q110874": "patronymic",
}


def load_seeds() -> dict[str, str]:
    seeds: dict[str, str] = {}
    with SEEDS.open(encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            parts = line.rstrip("\n").split("\t")
            if not parts or not parts[0].startswith("Q"):
                continue
            seeds[parts[0]] = parts[1] if len(parts) > 1 else ""
    return seeds


def main() -> None:
    seeds = load_seeds()
    print(f"{len(seeds):,} name-item QIDs to look for", flush=True)

    have = Counter()
    per_class_have: dict[str, Counter] = {c: Counter() for c in CLASS_NAMES}
    seen = 0
    rows_written = 0

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["qid", "classes"] + LANGS)
        for n, shard in enumerate(SHARDS, 1):
            with gzip.open(shard, "rt", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if '"Q' not in line:
                        continue
                    try:
                        item = json.loads(line)
                    except Exception:
                        continue
                    qid = item.get("id") or item.get("qid")
                    if qid not in seeds:
                        continue
                    seen += 1
                    labels = item.get("labels") or {}
                    cells = []
                    for lang in LANGS:
                        v = labels.get(lang)
                        if isinstance(v, dict):
                            v = v.get("value", "")
                        cells.append(v or "")
                        if v:
                            have[lang] += 1
                    classes = seeds.get(qid, "")
                    for cls in classes.split(","):
                        if cls in per_class_have:
                            for lang, cell in zip(LANGS, cells):
                                if cell:
                                    per_class_have[cls][lang] += 1
                    writer.writerow([qid, classes] + cells)
                    rows_written += 1
            if n % 200 == 0:
                print(f"  shard {n}/{len(SHARDS)}  matched {seen:,}", flush=True)

    lines = ["# What languages the name items carry labels in", "",
             f"**{seen:,} of {len(seeds):,} enumerated name items were found in the "
             f"local store** and are the basis of every figure here.", "",
             "This is the ceiling on mechanical translation: a person's label in a "
             "language can only be assembled from name items that have a label in "
             "that language.", "",
             "| language | items with a label | share |", "| --- | ---: | ---: |"]
    for lang in LANGS:
        n = have[lang]
        lines.append(f"| `{lang}` | {n:,} | {n / seen:.1%} |" if seen else f"| `{lang}` | 0 | |")
    lines += ["", "## By name class", "",
              "| class | " + " | ".join(f"`{l}`" for l in LANGS[:8]) + " |",
              "| --- | " + " | ".join("---:" for _ in LANGS[:8]) + " |"]
    for cls, name in CLASS_NAMES.items():
        c = per_class_have[cls]
        lines.append(f"| {name} | " + " | ".join(f"{c[l]:,}" for l in LANGS[:8]) + " |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"matched {seen:,} items; wrote {OUT_CSV.name} and {OUT_MD.name}")
    for lang in LANGS:
        print(f"  {lang:<4} {have[lang]:>8,}  {have[lang]/seen:.1%}" if seen else lang)


if __name__ == "__main__":
    main()
