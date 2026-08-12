# Character encoding in the corpus: how bad is it

**The question.** `reports/marriages.md` found one place string reading `Malm°` —
`U+00B0 DEGREE SIGN` where `ö` belongs — and recorded that the fault was real but
its extent unmeasured. This measures it.

Censused over `out/merged.ged`: **2,070,716 text-field lines**, **2,621,934
non-ASCII character occurrences**, **6,507 distinct non-ASCII characters**.
Full character map in `reports/encoding-characters.csv`.

## Most of the non-ASCII is not a problem, it is the corpus

| script | occurrences |
| --- | ---: |
| Cyrillic | 1,071,512 |
| CJK | 949,925 |
| Latin (accented) | 370,861 |
| Arabic | 113,754 |
| Hangul | 47,944 |
| Hebrew | 15,548 |
| Greek | 14,389 |

Worth noting in passing: **Cyrillic is the largest single script by character
count**, ahead of CJK. Nothing in `CLAUDE.md` or `todo.md` mentions a Cyrillic
component; the tree is described as Norwegian, Japanese and medieval European.

## Fault 1 — Latin-1 read as CP437. **442 lines, and reversible**

The `Malm°` case is not generic corruption. It is one specific, identifiable
transform, and identifying it makes the strings recoverable.

The non-ordinal `°` cases were all Danish or Norwegian — `K°benhavn`,
`Ringk°bing`, `N°rre`, `Gr°nderup`, `B°rnekopper` — alongside `pσ` and `rigsrσd`
for `på` and `rigsråd`. In Latin-1, `ø` is byte `0xF8` and `å` is `0xE5`. In
CP437 those bytes are `°` and `σ`.

**That is a testable prediction rather than a story**: if the diagnosis is right,
`æ` (`0xE6`) must appear as `µ`, and the rarer letters must appear as
box-drawing characters that occur nowhere else. Tested:

| appears as | should be | occurrences |
| --- | --- | ---: |
| `µ` | `æ` | 90 |
| `÷` | `ö` | 44 |
| `╪` | `Ø` | 33 |
| `ⁿ` | `ü` | 16 |
| `┼` | `Å` | 8 |
| `╞` | `Æ` | 1 |

Every predicted glyph is present, including `╞` **once**. A box-drawing character
appearing exactly once, inside `1481 ╞rkedegn` (`Ærkedegn`, archdeacon), is
strong confirmation — that glyph has no other reason to be in a Danish word.

Reconstruction, verified:

    'K°benhavn, Danmark'   ->  'København, Danmark'
    'Ringk°bing'           ->  'Ringkøbing'
    'rigsrσd'              ->  'rigsråd'
    'Malm°hus Len'         ->  'Malmøhus Len'
    'Oversekretµr i Danske Kancelli'  ->  'Oversekretær i Danske Kancelli'

**442 text lines carry the signature**, listed with their reconstruction in
`reports/encoding-nordic.csv`: 158 with an unambiguous glyph, 308 with a degree
sign not following a digit.

Two things deliberately *not* counted as corruption:

- **`σ` and `Θ` are Greek.** 554 and 75 occurrences, and **zero** of them are in
  lines without other Greek letters. All genuine.
- **423 of the 752 degree signs follow a digit** — `1° Conde de Talmont`, an
  ordinary Spanish and Italian ordinal.

And one false positive left visible: `§3n°3` reconstructs to `§3nø3`, which is
nonsense. It is a reference number, not Danish, and the `°` in it is real.

## Fault 2 — UTF-8 read as CP1252. **93 lines, 0.004%**

The classic `Ã¥` / `â€™` / `Ä€` shapes — `LAKSHMAN KUMÄ€R` is one, already sitting
in `reports/impossible-years.csv`. Listed in `reports/encoding-mojibake.csv`.

**93 lines out of 2,070,716.** Real, and negligible.

## The finding that actually matters: 4,199 invisible characters

Neither fault above is large. This one is, and it is invisible on inspection:

| | occurrences | example |
| --- | ---: | --- |
| `U+200E` left-to-right mark | 1,409 | `دسپنه خاتون‎ //` |
| `U+200F` right-to-left mark | 1,336 | a name that is *only* direction marks and spaces |
| `U+00A0` no-break space | 1,281 | trailing, in source citations |
| `U+00AD` soft hyphen | 132 | mid-word, `Sjæl­` |
| `U+200B` zero-width space | 26 | `LHZ6-KQG ​` |
| `U+FEFF` byte-order mark | 15 | `Willis Hil﻿l Cemetery` — **mid-word** |

These are in `NAME` and `PLAC` fields. They render as nothing, compare as
unequal, and would go into a Wikidata label silently — a label carrying a BOM in
the middle of *Hill* is a label nobody can search for and nobody can see is
wrong.

The right-to-left marks are the awkward ones: in an Arabic or Hebrew name they
may be doing real work, and stripping them is not obviously safe. The
zero-width space, byte-order mark and soft hyphen are not.

**NEEDS-DECISION — Emma:** whether ingestion normalises any of this. The Nordic
442 are reversible and the reconstruction is verified; the invisible characters
are a policy question; the 93 mojibake lines are probably not worth machinery.
Nothing has been changed.
