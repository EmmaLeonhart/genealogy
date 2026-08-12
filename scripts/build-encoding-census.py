"""How widespread is character mis-encoding in the corpus?

Raised by `reports/marriages.md`: one place string is `Malm°` — `U+00B0 DEGREE
SIGN` where `ö` belongs — while other rows carry `Malmø` correctly and `Malmohus`
unaccented. Three forms of one place name coexist. That the fault is real was
established; **how widespread it is was not**, and this measures it.

Two censuses, because the phenomenon has two shapes:

* **Every distinct non-ASCII character** in the fields that hold names and
  places, with counts and a sample line. This is the map: what is actually in
  there, before deciding what looks wrong.
* **Every line carrying a mojibake marker.** UTF-8 read as cp1252 produces
  recognisable sequences — `Ã` before a letter, `â€`, `Â` before punctuation.
  `LAKSHMAN KUMÄ€R` in `reports/impossible-years.csv` is one, already sitting in
  a committed report.

**No character is corrected and none is called wrong on sight.** A corpus this
multilingual holds Han, Cyrillic, Arabic, Devanagari and Ethiopic legitimately;
the point is to separate "unusual" from "broken", and only the mojibake markers
are evidence of breakage rather than of language.

Writes `reports/encoding-characters.csv` and `reports/encoding-mojibake.csv`.
Offline; reads the merged GEDCOM only.

    py scripts/build-encoding-census.py
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MERGED = REPO_ROOT / "out" / "merged.ged"
OUT_CHARS = REPO_ROOT / "reports" / "encoding-characters.csv"
OUT_MOJI = REPO_ROOT / "reports" / "encoding-mojibake.csv"

#: Tags whose values are human-readable text worth checking.
TEXT_TAGS = {"NAME", "GIVN", "SURN", "_MARNM", "NICK", "NSFX", "NPFX",
             "PLAC", "CITY", "STAE", "CTRY", "ADR1", "OCCU", "TITL"}

#: Sequences that UTF-8-read-as-cp1252 produces and that essentially never occur
#: in correctly-encoded text. `Ã` followed by a letter covers Ã¥ Ã¸ Ã¦ Ã© Ã¶;
#: `â€` covers the smart quotes and dashes; `Â` before punctuation or space is
#: the stray lead byte of a Latin-1 supplement character.
MOJIBAKE = re.compile(r"Ã[-ÿ\w]|â€|Â[\s -¿]|Ä€|Å¾|Ð[-¿]")

#: Characters that are not letters, digits, space or ordinary name punctuation.
#: Used only to *flag a row for reading*, never to judge it.
ORDINARY_PUNCT = set(" -'’.,/()[]\"&*?!:;+#%_|=<>@~^`{}\\\n\t")


def category(char: str) -> str:
    try:
        name = unicodedata.name(char)
    except ValueError:
        return "unnamed"
    return name.split()[0]


def main() -> int:
    chars: Counter[str] = Counter()
    char_tags: dict[str, Counter[str]] = defaultdict(Counter)
    samples: dict[str, str] = {}
    moji_rows: list[list] = []
    lines_read = 0
    text_lines = 0

    print(f"reading {MERGED}", flush=True)
    xref = ""
    with open(MERGED, encoding="utf-8", errors="replace") as handle:
        for number, line in enumerate(handle, 1):
            lines_read += 1
            if line.startswith("0 "):
                parts = line.split()
                xref = parts[1] if len(parts) >= 2 else ""
                continue
            parts = line.rstrip("\n").split(None, 2)
            if len(parts) < 3:
                continue
            tag, value = parts[1], parts[2]
            if tag not in TEXT_TAGS or not value:
                continue
            text_lines += 1

            for char in value:
                if ord(char) < 128:
                    continue
                chars[char] += 1
                char_tags[char][tag] += 1
                if char not in samples:
                    samples[char] = value[:120]

            if MOJIBAKE.search(value):
                moji_rows.append([xref, number, tag, value[:200],
                                  "; ".join(sorted(set(MOJIBAKE.findall(value))))])

    print(f"{lines_read:,} lines, {text_lines:,} in text fields", flush=True)
    print(f"{len(chars):,} distinct non-ASCII characters", flush=True)

    OUT_CHARS.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CHARS, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["char", "codepoint", "unicode_name", "script_word",
                         "occurrences", "top_tags", "sample"])
        for char, count in chars.most_common():
            try:
                name = unicodedata.name(char)
            except ValueError:
                name = "(unnamed)"
            writer.writerow([
                char, f"U+{ord(char):04X}", name, category(char), count,
                "; ".join(f"{t}:{n}" for t, n in char_tags[char].most_common(4)),
                samples.get(char, ""),
            ])

    with open(OUT_MOJI, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["record", "line_number", "tag", "value", "markers"])
        writer.writerows(moji_rows)

    print(f"wrote {OUT_CHARS} ({len(chars):,} rows)")
    print(f"wrote {OUT_MOJI} ({len(moji_rows):,} rows)")

    total_nonascii = sum(chars.values())
    print(f"\n{total_nonascii:,} non-ASCII character occurrences in text fields")
    print(f"{len(moji_rows):,} lines carry a mojibake marker "
          f"({100.0*len(moji_rows)/max(text_lines,1):.3f}% of text lines)")

    print("\nby script, occurrences:")
    by_script: Counter[str] = Counter()
    for char, count in chars.items():
        by_script[category(char)] += count
    for script, n in by_script.most_common(12):
        print(f"  {script:<16} {n:>10,}")

    print("\nsuspicious: non-letter, non-digit characters in name and place fields")
    odd = [
        (c, n) for c, n in chars.most_common()
        if not c.isalnum() and c not in ORDINARY_PUNCT and not unicodedata.combining(c)
    ]
    for char, n in odd[:25]:
        try:
            name = unicodedata.name(char)
        except ValueError:
            name = "(unnamed)"
        print(f"  {char!r:<8} U+{ord(char):04X} {name[:44]:<44} {n:>7,}  {samples[char][:44]!r}")
    print(f"\n  ({len(odd):,} such characters in total)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
