"""Which of our people already have a `ja` or `zh` label on Wikidata?

Emma, 2026-08-12: **"What the fuck we def have Japanese names?"** — after I
reported zero `ja` labels derivable.

That report was wrong in a way worth writing down. I had bucketed Hiragana,
Katakana, Hangul and Han together as "CJK" on the reasoning that Han is shared
between Japanese and Chinese, and then concluded nothing could be assigned a
language. **Kana is not shared** — Hiragana and Katakana are Japanese-only and
Hangul is Korean-only — so I had discarded the one decisive codepoint signal. It
settles 291 people as Japanese and 5,350 as Korean, leaving 42,956 written in Han
alone.

And a second source was ignored entirely: **the store holds whole items, and
those carry every label Wikidata has**, including `ja` and `zh`. Only *English*
labels were ever fetched separately; the Japanese ones were already on disk. For
a linked person, Wikidata's own `ja` label is authoritative and needs no
inference at all.

This measures both. Offline; reads the store and the derived labels.

    py scripts/measure-cjk-labels.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import wikistore  # noqa: E402

LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
STORE = REPO_ROOT / "wikidata" / "items"
INDEX = REPO_ROOT / "out" / "wikidata" / "store-index.sqlite3"
OUT_CSV = REPO_ROOT / "reports" / "cjk-labels.csv"

csv.field_size_limit(10_000_000)

WANTED = ("en", "ja", "zh", "zh-hans", "zh-hant", "ko", "mul")


def main() -> int:
    rows = list(csv.DictReader(open(LABELS, encoding="utf-8")))
    linked = {r["geni_id"]: r["qid"] for r in rows if r["qid"]}
    by_id = {r["geni_id"]: r for r in rows}
    print(f"{len(rows):,} people, {len(linked):,} linked", flush=True)

    with wikistore.StoreReader(STORE, INDEX) as reader:
        items = reader.entities(sorted(set(linked.values())))
    print(f"{len(items):,} items read", flush=True)

    have: Counter[str] = Counter()
    have_cjk: Counter[str] = Counter()
    out = []
    for geni_id, qid in linked.items():
        entity = items.get(qid)
        if entity is None:
            have["not in store"] += 1
            continue
        labels = entity.get("labels") or {}
        cjk_named = bool(by_id[geni_id]["cjk_names"])
        present = [code for code in WANTED if code in labels]
        for code in present:
            have[code] += 1
            if cjk_named:
                have_cjk[code] += 1
        if cjk_named or "ja" in labels or "zh" in labels:
            out.append([
                geni_id, qid,
                by_id[geni_id]["cjk_names"],
                (labels.get("ja") or {}).get("value", ""),
                (labels.get("zh") or {}).get("value", ""),
                (labels.get("ko") or {}).get("value", ""),
                (labels.get("en") or {}).get("value", ""),
            ])

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["geni_id", "qid", "geni_cjk_name",
                         "wikidata_ja", "wikidata_zh", "wikidata_ko", "wikidata_en"])
        writer.writerows(out)

    print()
    print(f"  {'language':<12} {'linked people':>14} {'…with a CJK Geni name':>24}")
    for code in WANTED:
        print(f"  {code:<12} {have[code]:>14,} {have_cjk[code]:>24,}")
    print(f"  {'not in store':<12} {have['not in store']:>14,}")
    print(f"\nwrote {OUT_CSV} ({len(out):,} rows)")

    ja_and_cjk = sum(1 for r in out if r[3] and r[2])
    ja_no_cjk = sum(1 for r in out if r[3] and not r[2])
    cjk_no_ja = sum(1 for r in out if r[2] and not r[3])
    print(f"\n  Geni CJK name AND Wikidata ja label : {ja_and_cjk:,}")
    print(f"  Wikidata ja label, no Geni CJK name : {ja_no_cjk:,}")
    print(f"  Geni CJK name, no Wikidata ja label : {cjk_no_ja:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
