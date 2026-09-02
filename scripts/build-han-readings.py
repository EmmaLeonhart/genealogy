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

* **`ko` is mechanical and right.** A Han character has a regular Sino-Korean reading;
  `CLAUDE.md` § *CJK INCLUDES KOREAN* already records this as the reason `ko` is engine work
  while kana is research. Spot-checked against names whose romanisation is independently known:
  金庾信 → 금유신, 陳恕 → 진서, 黃 → 황.
* **`ja` is a CANDIDATE and is never emitted unreviewed.** Measured on 2026-09-02, `pykakasi`
  resolves *surnames* out of its dictionary correctly — 青山 → あおやま, 酒井 → さかい,
  藤原 → ふじわら — and falls back to on'yomi on *given* names, where Japanese personal readings
  are irregular: 幸豊 → こうほう when the man was Yukitoyo, 忠貫 → ちゅうかん for Tadatsura.
  `CLAUDE.md` § *`P1814`* says a kana reading is not derivable by rule, and this measurement is
  what that sentence looks like in the data. `scripts/fetch-kana-readings.py` is the sourced
  answer; this column exists to be checked against it, never instead of it.
* **`zh` has no offline source yet** and is written blank rather than guessed. `pypinyin` is not
  installed and `CLAUDE.md` § *Stdlib only* means that is a decision rather than an oversight.
  The column exists so the shape is right the day a source lands.

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

#: CJK Unified Ideographs, Extension A, and the Compatibility block. Kana and Hangul are
#: deliberately excluded: they are already readings.
HAN = re.compile(r"[㐀-䶿一-鿿豈-﫿]")


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

    rows, blank_ko = [], 0
    for ch, n in count.most_common():
        ko = ""
        if ko_of:
            try:
                got = ko_of(ch)
                # `hanja` returns the character unchanged when it has no reading for it.
                # Passing that through would put a Han character in a Hangul column.
                ko = got if got and got != ch else ""
            except Exception:                                          # noqa: BLE001
                ko = ""
        if not ko:
            blank_ko += 1
        kana = romaji = ""
        if ja_of:
            try:
                kana, romaji = ja_of(ch)
                if kana == ch:
                    kana = romaji = ""
            except Exception:                                          # noqa: BLE001
                kana = romaji = ""
        rows.append([ch, n, ko, kana, romaji, ""])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["han", "corpus_count", "ko", "ja_kana_candidate",
                    "ja_romaji_candidate", "zh_pinyin"])
        w.writerows(rows)

    print("wrote %s - %s rows" % (OUT.relative_to(ROOT), format(len(rows), ",")))
    print("   ko  filled %s, blank %s" % (format(len(rows) - blank_ko, ","), format(blank_ko, ",")))
    print("   zh  blank on every row: no offline pinyin source (see the docstring)")
    print("\nthe twelve most common characters:")
    for r in rows[:12]:
        print("   %s  %-7s ko=%-3s ja=%s" % (r[0], format(r[1], ","), r[2], r[3]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
