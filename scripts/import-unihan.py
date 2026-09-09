"""Extract the per-character readings this corpus needs from Unicode's Unihan database.

    py scripts/import-unihan.py --zip <path to Unihan.zip>

**Emma authorised the download on 2026-09-02**, choosing it over `pip install pypinyin`: Unihan is
a **data file**, not a dependency, so `CLAUDE.md` § *Stdlib only* is untouched — it is the same
pattern as the Wikidata dumps already under `wikidata/`.

`Unihan.zip` is ~8.5 MB from <https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip>. The raw
archive is **not committed**; this writes a derived TSV restricted to the characters that actually
occur in the corpus, which is a few thousand rows and reviewable by eye.

## The fields taken, and why each

* **`kMandarin`** — the pinyin. This is the column that had no offline source at all, and the
  whole reason for the download.
* **`kHangul`** — the Korean reading, **with its variants**, which is the correction this file
  carries. See below.
* **`kJapaneseOn` / `kJapaneseKun`** — recorded but **not** emitted as readings. A Japanese
  personal name does not follow from its characters, which is `CLAUDE.md`'s standing reason
  `P1814` is research; these are here so a *sourced* reading can be sanity-checked against them,
  never so one can be generated.

## `kHangul` carries several readings and taking the first one is WRONG

金 is `금:0E 김:0N`. The `hanja` library returns 금, so the Korean alias this repo shipped for
金庾信 was **금유신** when the man is **김유신**, Kim Yu-sin — the commonest surname in Korea read
as the wrong word. Measured against Unihan rather than assumed.

Two distinct things produce the alternates, and neither is an error to resolve:

* **두음법칙, the initial-sound rule.** ㄹ and ㄴ shift word-initially in South Korean
  orthography, so 李 is `리` medially and `이` initially, 柳 `류`/`유`, 羅 `라`/`나`. Both are
  the same character read correctly in different positions.
* **surname exceptions**, of which 金 금/김 is the famous one.

`CLAUDE.md` § *One name item per USAGE* is the governing precedent: a token in two roles is not
an ambiguity to resolve. So **every reading is kept** and the caller emits the variants as
aliases, which is exactly what aliases are for.

Writes `reports/unihan-corpus-readings.tsv`.
"""
from __future__ import annotations

import argparse
import collections
import csv
import io
import os
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

TAB = chr(9)
LABELS = ROOT / "reports" / "derived-labels.csv"
OUT = ROOT / "reports" / "unihan-corpus-readings.tsv"

# See scripts/build-han-readings.py: never write these boundaries as literal characters.
HAN = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]")

WANTED = ("kMandarin", "kHangul", "kKorean", "kJapaneseOn", "kJapaneseKun", "kDefinition")


def corpus_characters():
    """Every Han character occurring in a `cjk_names` cell."""
    seen = collections.Counter()
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            seen.update(HAN.findall(row.get("cjk_names") or ""))
    return seen


def read_unihan(path, wanted_chars):
    """`{char: {field: value}}` for the characters we care about."""
    out = collections.defaultdict(dict)
    with zipfile.ZipFile(path) as z:
        with z.open("Unihan_Readings.txt") as fh:
            for raw in io.TextIOWrapper(fh, encoding="utf-8"):
                if raw.startswith("#"):
                    continue
                parts = raw.rstrip("\n").split(TAB)
                if len(parts) != 3 or parts[1] not in WANTED:
                    continue
                try:
                    ch = chr(int(parts[0][2:], 16))
                except ValueError:
                    continue
                if ch in wanted_chars:
                    out[ch][parts[1]] = parts[2]
    return out


def hangul_readings(value):
    """`['금', '김']` from `'금:0E 김:0N'`, order preserved, duplicates dropped.

    The `:0E` / `:0N` suffix is a source flag, not a sense. It does **not** say which reading is
    the surname one — 金 is `금:0E 김:0N` while 羅 is `나:0 라:0E`, opposite flags for the same
    kind of alternation — so nothing here tries to rank them.
    """
    out = []
    for tok in (value or "").split():
        r = tok.split(":", 1)[0].strip()
        if r and r not in out:
            out.append(r)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--zip", required=True, help="path to Unihan.zip")
    args = ap.parse_args()
    if not os.path.exists(args.zip):
        print("no such file: %s" % args.zip, file=sys.stderr)
        return 1

    counts = corpus_characters()
    print("%s distinct Han characters in the corpus" % format(len(counts), ","))
    data = read_unihan(args.zip, set(counts))
    print("%s of them are in Unihan_Readings" % format(len(data), ","))

    rows, have = [], collections.Counter()
    for ch, n in counts.most_common():
        d = data.get(ch, {})
        ko = hangul_readings(d.get("kHangul"))
        zh = (d.get("kMandarin") or "").split()
        if ko:
            have["kHangul"] += 1
        if zh:
            have["kMandarin"] += 1
        if len(ko) > 1:
            have["more than one Korean reading"] += 1
        if len(zh) > 1:
            have["more than one Mandarin reading"] += 1
        rows.append([ch, n, " ".join(ko), " ".join(zh),
                     d.get("kKorean", ""), d.get("kJapaneseOn", ""),
                     d.get("kJapaneseKun", ""), (d.get("kDefinition", "") or "")[:60]])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["han", "corpus_count", "ko_readings", "zh_pinyin", "kKorean",
                    "kJapaneseOn", "kJapaneseKun", "definition"])
        w.writerows(rows)

    print("\nwrote %s - %s rows" % (OUT.relative_to(ROOT), format(len(rows), ",")))
    for k, v in have.most_common():
        print("   %-34s %s" % (k, format(v, ",")))
    print("\nthe ten most common characters:")
    for r in rows[:10]:
        print("   %s  %-7s ko=%-10s zh=%s" % (r[0], format(r[1], ","), r[2], r[3]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
