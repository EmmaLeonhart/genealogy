"""Every Han character in the corpus, with its Korean, Japanese and Mandarin readings.

    py scripts/build-han-readings.py

**Emma, 2026-09-02, and it dissolves the culture problem rather than solving it:** *"the kana
name plus the Korean name plus the Mandarin pronunciation of every single arbitrary character
thing is something that is actually produced... we'd even essentially have all of the labels
the thing would ever possibly have in the `mul` label. It's just a matter of which one is chosen
at the top."*

So the three readings are **produced for everybody** and go on as `Amul` aliases. The culture
classifier stops being a gate on whether a person gets a label at all, and becomes a much smaller
decision — **which of the three is promoted to `mul`** — that can be moved later, one person at a
time, agentically or by hand, without rebuilding anything.

That is why this file is characters rather than people. A character table is a few thousand rows,
it is reusable by every emitter, and it is the thing a per-person table is a join away from.

## The three columns are NOT of equal standing, and the file says so per row

* **`ko` is mechanical**, and a character may legitimately have MORE THAN ONE reading — the
  column is space-separated, most usual first. `CLAUDE.md` § *CJK INCLUDES KOREAN* records why
  `ko` is engine work while kana is research. Spot-checked against names whose romanisation is
  independently known: 陳恕 → 진서, 黃 → 황, and 金庾信 → 김유신 **only once both readings of
  金 are kept** — see the two-source section below, which is where that name was got wrong.
* **`ja` is a CANDIDATE and is never emitted unreviewed.** Measured on 2026-09-02, `pykakasi`
  resolves *surnames* out of its dictionary correctly — 青山 → あおやま, 酒井 → さかい,
  藤原 → ふじわら — and falls back to on'yomi on *given* names, where Japanese personal readings
  are irregular: 幸豊 → こうほう when the man was Yukitoyo, 忠貫 → ちゅうかん for Tadatsura.
  `CLAUDE.md` § *`P1814`* says a kana reading is not derivable by rule, and this measurement is
  what that sentence looks like in the data. `scripts/fetch-kana-readings.py` is the sourced
  answer; this column exists to be checked against it, never instead of it.
* **`zh` is mechanical**, from Unihan's `kMandarin`, once `scripts/import-unihan.py` has run.
  4,682 of the 4,688 characters carry one. Emma authorised the download on 2026-09-02, choosing
  a data file over a `pypinyin` dependency, so § *Stdlib only* is intact.

## `ko` merges TWO sources, and neither alone is right

Measured 2026-09-02 over all 4,688 characters:

* `hanja` covers 4,686 and Unihan's `kHangul` covers 3,645, so **each has ~1,000 the other
  lacks**. The union is complete.
* Where both speak they agree 3,543 times and differ 100. **Almost every difference is
  두음법칙**, the initial-sound rule: `hanja` returns the word-initial form (隴 농, 頼 뇌,
  礼 예) and Unihan the base reading (롱, 뢰, 례). Neither is wrong; they describe different
  positions in a word.
* **`hanja` alone misses the surname readings**, which is the one that produces wrong names:
  金 is `금 김` and `hanja` gives only 금, so 金庾信 came out 금유신 when the man is 김유신,
  Kim Yu-sin. 沈 is `심 침` and the surname is 심.

So every reading from either source is kept, and the caller emits the alternates as **aliases**
rather than choosing between them — `CLAUDE.md` § *One name item per USAGE*, where a token in
two roles is not an ambiguity to resolve.

**A blank is a blank, never a fallback to another language's reading.** That is the whole of
§ *partial is worse than absent* applied here: a Mandarin column quietly filled with Sino-Korean
would be undetectable downstream and wrong on every row.

Writes `reports/han-readings.tsv` — one row per distinct character, with a corpus count so the
common ones can be reviewed first.
"""
from __future__ import annotations

import collections
import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

TAB = chr(9)
LABELS = ROOT / "reports" / "derived-labels.csv"
OUT = ROOT / "reports" / "han-readings.tsv"
UNIHAN = ROOT / "reports" / "unihan-corpus-readings.tsv"

#: CJK Unified Ideographs, Extension A, and the Compatibility block. Kana and Hangul are
#: deliberately excluded: they are already readings.
#: **Never write these boundaries as literal characters.** U+F900 CJK COMPATIBILITY
#: IDEOGRAPH and U+8C48 render identically, and NFC normalisation maps the first to the
#: second -- so a literal range silently becomes U+8C48-U+FAFF, which swallows the whole
#: Hangul Syllables block. Measured 2026-09-02: 358 Hangul characters counted as Han and
#: 5,350 Korean people dropped as unreadable when their names needed no conversion at all.
#: The escapes cannot be normalised; the literal form did not survive one edit round-trip.
HAN = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]")


def readers():
    """`(ko, ja)` callables, or `None` where the library is absent.

    Imported here rather than at module scope so the script still runs — and still writes the
    columns it can — on a machine that has one library and not the other. A missing library
    leaves a blank column, which is the documented meaning of blank.
    """
    ko = ja = None
    try:
        import hanja
        ko = lambda ch: hanja.translate(ch, "substitution")          # noqa: E731
    except Exception as exc:                                          # noqa: BLE001
        print("no Korean readings: %s" % exc, file=sys.stderr)
    try:
        import pykakasi
        kks = pykakasi.kakasi()
        def ja(ch):                                                   # noqa: E306
            out = kks.convert(ch)
            return ("".join(x["hira"] for x in out),
                    " ".join(x["hepburn"] for x in out).strip())
    except Exception as exc:                                          # noqa: BLE001
        print("no Japanese readings: %s" % exc, file=sys.stderr)
    return ko, ja


def main() -> int:
    if not LABELS.exists():
        print("no %s" % LABELS.relative_to(ROOT), file=sys.stderr)
        return 1
    ko_of, ja_of = readers()

    count = collections.Counter()
    people = 0
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            han = HAN.findall(row.get("cjk_names") or "")
            if han:
                people += 1
                count.update(han)
    print("%s distinct Han characters over %s people"
          % (format(len(count), ","), format(people, ",")))

    # Unihan, if `scripts/import-unihan.py` has been run. Absent, `zh` stays blank and `ko`
    # falls back to `hanja` alone -- which is the state this file shipped in, and is degraded
    # rather than broken.
    unihan = {}
    if UNIHAN.exists():
        with io.open(UNIHAN, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh, delimiter=TAB):
                unihan[r["han"]] = (r["ko_readings"].split(), r["zh_pinyin"].split())
        print("%s characters from Unihan" % format(len(unihan), ","))
    else:
        print("no %s -- run scripts/import-unihan.py; zh will be blank"
              % UNIHAN.relative_to(ROOT), file=sys.stderr)

    rows, tally = [], collections.Counter()
    for ch, n in count.most_common():
        uni_ko, uni_zh = unihan.get(ch, ([], []))
        readings = list(uni_ko)
        if ko_of:
            try:
                got = ko_of(ch)
                # `hanja` returns the character unchanged when it has no reading for it.
                # Passing that through would put a Han character in a Hangul column.
                # It is put FIRST because it applies 두음법칙 for word-initial position,
                # which is the form a Korean label most often takes.
                if got and got != ch and got not in readings:
                    readings.insert(0, got)
                elif got in readings:
                    readings.remove(got)
                    readings.insert(0, got)
            except Exception:                                          # noqa: BLE001
                pass
        if readings:
            tally["ko"] += 1
        if len(readings) > 1:
            tally["ko has alternates"] += 1
        zh = " ".join(uni_zh)
        if zh:
            tally["zh"] += 1
        kana = romaji = ""
        if ja_of:
            try:
                kana, romaji = ja_of(ch)
                if kana == ch:
                    kana = romaji = ""
            except Exception:                                          # noqa: BLE001
                kana = romaji = ""
        rows.append([ch, n, " ".join(readings), kana, romaji, zh])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["han", "corpus_count", "ko", "ja_kana_candidate",
                    "ja_romaji_candidate", "zh_pinyin"])
        w.writerows(rows)

    print("wrote %s - %s rows" % (OUT.relative_to(ROOT), format(len(rows), ",")))
    for k, v in tally.most_common():
        print("   %-24s %s" % (k, format(v, ",")))
    print("\nthe twelve most common characters:")
    for r in rows[:12]:
        print("   %s  %-7s ko=%-3s ja=%s" % (r[0], format(r[1], ","), r[2], r[3]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
