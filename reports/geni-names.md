# Geni name records: how many, which fields, which scripts

Asked for by Emma, 2026-08-12. Every `NAME` record is a row in
`reports/geni-name-records.csv`.

**298,591 people, 444,874 `NAME` records.**

**Nothing here is a label.** Geni names are language-agnostic strings. A Han
name is not Chinese, it is Han — and per Emma, if a name is written solely in
kanji the Japanese and Chinese labels are the *same string*, so there is nothing
to decide. Only kana and Hangul resolve to a language, because only they are
exclusive to one.

## How many names each person has

| names | people | share |
| ---: | ---: | ---: |
| 1 | 207,690 | 69.6% |
| 2 | 57,741 | 19.3% |
| 3 | 15,190 | 5.1% |
| 4 | 16,124 | 5.4% |
| 5 | 830 | 0.3% |
| 6 | 477 | 0.2% |
| 7 | 185 | 0.1% |
| 8 | 173 | 0.1% |
| 9 | 69 | 0.0% |
| 9 or more | 181 | 0.1% |

**207,690 people (69.6%) have exactly one name record**; 90,901 have several.

## Which fields are filled

| field | records | share of records | people | share of people |
| --- | ---: | ---: | ---: | ---: |
| GIVN given name | 342,340 | 77.0% | 276,279 | 92.5% |
| SURN surname | 211,584 | 47.6% | 177,545 | 59.5% |
| _MARNM married name | 244,392 | 54.9% | 223,298 | 74.8% |
| NSFX suffix | 36,072 | 8.1% | 32,597 | 10.9% |
| NPFX prefix | 0 | 0.0% | 0 | 0.0% |
| NICK nickname | 35,669 | 8.0% | 31,812 | 10.7% |
| SPFX surname prefix | 0 | 0.0% | 0 | 0.0% |

### `_MARNM` against `SURN`, per record

| | records | share |
| --- | ---: | ---: |
| neither | 127,072 | 28.6% |
| _MARNM only, SURN empty | 106,218 | 23.9% |
| identical | 75,953 | 17.1% |
| SURN only | 73,410 | 16.5% |
| differ | 62,221 | 14.0% |

## Scripts, per name record

| script class | records | share |
| --- | ---: | ---: |
| Latin | 297,861 | 66.95% |
| Han only (Chinese or Japanese kanji) | 94,702 | 21.29% |
| MIXED: Han+Latin | 23,381 | 5.26% |
| no letters | 7,963 | 1.79% |
| Cyrillic | 7,874 | 1.77% |
| Hangul (Korean) | 6,066 | 1.36% |
| Arabic | 3,921 | 0.88% |
| MIXED: Cyrillic+Latin | 1,024 | 0.23% |
| Han + kana (Japanese) | 566 | 0.13% |
| Hebrew | 471 | 0.11% |
| Greek | 404 | 0.09% |
| MIXED: Arabic+Latin | 167 | 0.04% |
| kana only (Japanese) | 119 | 0.03% |
| MIXED: Hebrew+Latin | 62 | 0.01% |
| MIXED: Greek+Latin | 46 | 0.01% |
| Armenian | 46 | 0.01% |
| MIXED: Hangul+Latin | 36 | 0.01% |
| MIXED: Latin+Tibetan | 34 | 0.01% |
| Mongolian | 21 | 0.00% |
| Han + Hangul (Korean) | 17 | 0.00% |
| Georgian | 16 | 0.00% |
| MIXED: Han+Hiragana+Katakana+Latin | 8 | 0.00% |
| Devanagari | 6 | 0.00% |
| Tibetan | 6 | 0.00% |

## The two mixed-script questions, which are different

Emma: *"A mixed script name often indicates some sort of attempt at a
commentary or disambiguation within the name, whereas … a name that suggests
multiple names and multiple scripts, just indicates multiple languages."*

### One record, two scripts inside it — 24,805 records

| scripts in one name | records |
| --- | ---: |
| Han+Latin | 23,381 |
| Cyrillic+Latin | 1,024 |
| Arabic+Latin | 167 |
| Hebrew+Latin | 62 |
| Greek+Latin | 46 |
| Hangul+Latin | 36 |
| Latin+Tibetan | 34 |
| Han+Hiragana+Katakana+Latin | 8 |
| Han+Hiragana+Latin | 6 |
| Latin+Mongolian | 5 |
| Katakana+Latin | 4 |
| Cyrillic+Han+Latin | 4 |
| Georgian+Latin | 4 |
| Egyptian+Han | 4 |
| Han+Katakana+Katakana-Hiragana | 3 |

Examples, which show the gloss-inside-the-name pattern:

- `Han+Latin` — Xie Lingyun 謝靈運
- `Han+Latin` — Xie Tiao 謝朓
- `Han+Latin` — 陳纪 Chan 1
- `Cyrillic+Latin` — María Josefa Carmela Бурбон Infanta de España
- `Cyrillic+Latin` — Вильгельм I
- `Cyrillic+Latin` — Михаил VII
- `Arabic+Latin` — Assona Íñiguez بن فورتون
- `Arabic+Latin` — Shushandukht بنت رأس الجالوت ناثان الثاني
- `Arabic+Latin` — Muhammad محمد بن عبد الرحمن الأوسط Emir de Córdova
- `Hebrew+Latin` — Yoshea מארץ ישראל
- `Hebrew+Latin` — Rabeinu Yosef Hanassi הלוי
- `Hebrew+Latin` — Efraim Naftali Hirsch אבד לודמיר A.B.D. Ludmir
- `Greek+Latin` — Constantine Δούκας
- `Greek+Latin` — Ioannes Κομνηνός
- `Greek+Latin` — Ἀριoβαρζάνης

### One person, several names in different scripts

| | people | share |
| --- | ---: | ---: |
| one name only | 207,690 | 69.6% |
| several names, all one script | 77,390 | 25.9% |
| has a mixed-script name | 18,560 | 6.2% |
| several names, several scripts | 8,997 | 3.0% |

| script combination across a person's names | people |
| --- | ---: |
| Arabic + Latin | 3,143 |
| Cyrillic + Latin | 2,882 |
| Han only (Chinese or Japanese kanji) + Latin | 1,528 |
| Hangul (Korean) + Latin | 387 |
| Greek + Latin | 315 |
| Hebrew + Latin | 307 |
| Arabic + Cyrillic + Latin | 55 |
| Han + kana (Japanese) + Latin | 50 |
| Han + kana (Japanese) + Han only (Chinese or Japanese kanji) | 41 |
| Han + kana (Japanese) + kana only (Japanese) | 41 |
| Han only (Chinese or Japanese kanji) + Hangul (Korean) + Latin | 31 |
| Armenian + Latin | 30 |
| Cyrillic + Han only (Chinese or Japanese kanji) + Latin | 25 |
| Arabic + Hebrew + Latin | 25 |
| Cyrillic + Han only (Chinese or Japanese kanji) | 20 |

## The first-listed name

Emma: *"I believe that the first listed name in the files is usually the one
that is treated as being in English and taking priority, but Geni is weird about
English names. A lot of stuff is recorded as being English when it's not."*

Whatever the first record means, this is what script it is in:

| script class of the first name | people | share |
| --- | ---: | ---: |
| Latin | 244,025 | 81.7% |
| Han only (Chinese or Japanese kanji) | 33,784 | 11.3% |
| MIXED: Han+Latin | 7,934 | 2.7% |
| Hangul (Korean) | 4,900 | 1.6% |
| no letters | 4,792 | 1.6% |
| Cyrillic | 1,848 | 0.6% |
| MIXED: Cyrillic+Latin | 706 | 0.2% |
| Han + kana (Japanese) | 189 | 0.1% |
| MIXED: Arabic+Latin | 156 | 0.1% |
| MIXED: Hebrew+Latin | 52 | 0.0% |
| Arabic | 41 | 0.0% |
| MIXED: Hangul+Latin | 34 | 0.0% |

**20,937 people (7.0%) have names in
more than one script class**, so for them the first record is a choice among
scripts rather than the only option.

### The first slot is privileged, and this is by how much

Over the people carrying **both** a pure-Latin and a pure non-Latin name — the
only ones where the ordering can mean anything:

| the first record is | people | share |
| --- | ---: | ---: |
| Latin first | 7,839 | 88.4% |
| non-Latin first | 524 | 5.9% |
| mixed first | 500 | 5.6% |

Against a null model — order random, weighted by how many Latin and non-Latin
names each person actually has:

    observed  P(first record is Latin) = 0.884
    random    expected                 = 0.531

So the first slot is **not** arbitrary. And a Latin name sits at position 0 or 1
for 99.3% of them.

**What leads when Latin does not** is the informative part: almost every such
case is a *mixed-script* record in front — `Constantine /Δούκας/` ahead of
`Constantine Doukas Byzantine Co-emperor`. So slot 0 holds the primary name, and
when that primary is itself a Latin-plus-native hybrid the pure Latin form is
pushed to second.

**This does not establish that slot 0 is English.** Temüjin's first record is
Cyrillic+Latin. The corpus carries **zero `LANG` subtags**, so what it
establishes is that the slot is privileged, not what language it claims.
