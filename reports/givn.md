# Multi-token `GIVN`: what the extra tokens actually are

`todo.md` § 4 records the trap — *"Do not split `GIVN` on spaces to make
P1545 statements… Splitting needs a step that can tell a name from an
honorific"* — and that step cannot be designed without knowing what the extra
tokens are. This counts them and decides nothing.

Over **342,340** `NAME` records carrying a `GIVN`, **130,712 (38.2%) hold more than one token**. Every one of them
is a row in `reports/givn-multitoken.csv`.

## The trap is real. `todo.md` puts it in the wrong population

`todo.md` § 4 says the multi-token strings are *"most … romanised CJK/steppe
names where the extra tokens are honorifics, particles and titles"*, and that
*"the genuine P1545 case … is the Latin-script subset"*. The count it cites,
36.9%, matches what is measured here. **The characterisation does not.**

- **111,610 of the 130,712 multi-token records are Latin-script — 85%.** They are not a subset to be carved out;
  they are nearly the whole population.
- **Han is 6,465 records, 10.3% of Han `GIVN`s** — the *least* multi-token script in the corpus, not the most.
- And within Latin, the commonest non-name last token is not an honorific:

| last token of a Latin multi-token `GIVN` | records | share |
| --- | ---: | ---: |
| wordlike | 76,069 | 68.2% |
| patronymic | 27,003 | 24.2% |
| honorific/particle/ordinal | 7,219 | 6.5% |
| no letters | 1,127 | 1.0% |
| digits | 192 | 0.2% |

**Patronymics outnumber honorifics roughly four to one**, and a patronymic is
neither a given name nor a title — it is a third category the trap as written
does not mention. `Olsen`, `Olsdatter`, `Pedersdatter`, `Pedersen` are all in
the top twenty non-first tokens.

The honorific-class tokens that *do* appear at the top are mostly **regnal
ordinals** — `i`, `ii`, `iii`, `iv` — which is a different problem again from
"Lady" and "Chanyu".

So the conclusion `todo.md` draws survives — a naive space split emits wrong
`P735`s — while its reason does not. Anything built on "handle the CJK
romanisations and the Latin subset is fine" would be built on a
misapprehension.

## How many tokens

| tokens | records |
| ---: | ---: |
| 1 | 211,628 |
| 2 | 96,610 |
| 3 | 21,790 |
| 4 | 6,702 |
| 5 | 2,527 |
| 6 | 1,356 |
| 7 | 734 |
| 8 | 376 |
| 9 | 241 |
| 10 | 125 |
| 11 | 77 |
| 12 | 49 |
| 13 | 25 |
| 14 | 23 |
| 15 | 16 |
| 16 | 22 |
| 17 | 10 |
| 18 | 7 |
| 19 | 7 |
| 20 | 1 |
| 21 | 6 |
| 22 | 1 |
| 23 | 1 |
| 24 | 1 |
| 25 | 2 |
| 26 | 1 |
| 28 | 1 |
| 36 | 1 |

## Which scripts the multi-token ones are in

This is the load-bearing table: `todo.md` says the genuine P1545 case is the
Latin-script subset and the rest are romanisation artefacts.

| script | with `GIVN` | multi-token | share of that script |
| --- | ---: | ---: | ---: |
| Latin | 252,937 | 111,610 | 44.1% |
| Han | 62,888 | 6,465 | 10.3% |
| Han+Latin | 9,091 | 5,053 | 55.6% |
| Cyrillic | 6,783 | 4,880 | 71.9% |
| Hangul | 3,541 | 315 | 8.9% |
| Arabic | 3,178 | 867 | 27.3% |
| Cyrillic+Latin | 939 | 769 | 81.9% |
| Latin+Masculine | 640 | 203 | 31.7% |
| (none) | 389 | 4 | 1.0% |
| Greek | 380 | 49 | 12.9% |
| Hebrew | 351 | 151 | 43.0% |
| Han+Hiragana | 310 | 38 | 12.3% |

## What the *last* token looks like, by script

The last token is where a patronymic lands in this tree — `Arne Olson`,
`GIVN` of Arne Olson Anda, whose Wikidata item holds `P735 = Arne` and nothing
for `Olson`. A patronymic is neither a given name nor an honorific; it is a
third category, and the one this corpus is full of.

| script | wordlike | patronymic | honorific/particle/ordinal | digits | no letters |
| --- | ---: | ---: | ---: | ---: | ---: |
| Latin | 76,069 | 27,003 | 7,219 | 192 | 1,127 |
| Han | 6,406 | 0 | 0 | 4 | 55 |
| Han+Latin | 4,942 | 9 | 12 | 34 | 56 |
| Cyrillic | 4,857 | 0 | 0 | 19 | 4 |
| Hangul | 314 | 0 | 0 | 0 | 1 |
| Arabic | 865 | 0 | 0 | 0 | 2 |
| Cyrillic+Latin | 720 | 2 | 44 | 0 | 3 |
| Latin+Masculine | 191 | 0 | 12 | 0 | 0 |

## The commonest non-first tokens, by script

Raw counts, top 20 each. This is the evidence for what a name-versus-honorific
step would have to handle.

### Latin

| token | times | shape |
| --- | ---: | --- |
| `of` | 2,768 | wordlike |
| `i` | 2,559 | honorific/particle/ordinal |
| `ii` | 2,496 | honorific/particle/ordinal |
| `de` | 2,168 | honorific/particle/ordinal |
| `maria` | 1,520 | wordlike |
| `/` | 1,284 | no letters |
| `iii` | 1,208 | honorific/particle/ordinal |
| `antonio` | 879 | wordlike |
| `rd.` | 844 | wordlike |
| `marie` | 831 | wordlike |
| `olsen` | 770 | patronymic |
| `josefa` | 731 | wordlike |
| `olsdatter` | 714 | patronymic |
| `iv` | 698 | honorific/particle/ordinal |
| `nr.` | 633 | wordlike |
| `maría` | 600 | wordlike |
| `bin` | 576 | wordlike |
| `pedersdatter` | 562 | patronymic |
| `pedersen` | 525 | patronymic |
| `.` | 471 | no letters |

### Han

| token | times | shape |
| --- | ---: | --- |
| `親王` | 48 | wordlike |
| `‎` | 47 | no letters |
| `某` | 22 | wordlike |
| `子敬` | 14 | wordlike |
| `子文` | 13 | wordlike |
| `殤` | 12 | wordlike |
| `清光院` | 11 | wordlike |
| `内親王` | 11 | wordlike |
| `子明` | 11 | wordlike |
| `長寿院` | 10 | wordlike |
| `道明` | 10 | wordlike |
| `文通` | 10 | wordlike |
| `八条院` | 9 | wordlike |
| `王` | 8 | wordlike |
| `左馬助` | 8 | wordlike |
| `子元` | 8 | wordlike |
| `子立` | 8 | wordlike |
| `安國` | 8 | wordlike |
| `季達` | 8 | wordlike |
| `子思` | 8 | wordlike |

### Han+Latin

| token | times | shape |
| --- | ---: | --- |
| `gōng` | 195 | wordlike |
| `(kāi` | 109 | wordlike |
| `(jié` | 70 | wordlike |
| `(yì` | 60 | wordlike |
| `of` | 54 | wordlike |
| `hào` | 54 | wordlike |
| `(wén` | 52 | wordlike |
| `for` | 49 | wordlike |
| `2:` | 48 | no letters |
| `wēng)` | 48 | wordlike |
| `1:` | 46 | no letters |
| `descendents` | 46 | wordlike |
| `(hóng` | 38 | wordlike |
| `(sì` | 36 | wordlike |
| `yì)` | 34 | wordlike |
| `1` | 32 | digits |
| `surname` | 29 | wordlike |
| `(wěi` | 28 | wordlike |
| `(guāng` | 28 | wordlike |
| `zì` | 25 | wordlike |

### Cyrillic

| token | times | shape |
| --- | ---: | --- |
| `иванович` | 631 | wordlike |
| `васильевич` | 323 | wordlike |
| `андреевич` | 241 | wordlike |
| `михайлович` | 209 | wordlike |
| `фёдорович` | 176 | wordlike |
| `александрович` | 156 | wordlike |
| `дмитриевич` | 150 | wordlike |
| `юрьевич` | 133 | wordlike |
| `федорович` | 122 | wordlike |
| `петрович` | 111 | wordlike |
| `григорьевич` | 105 | wordlike |
| `семёнович` | 91 | wordlike |
| `константинович` | 86 | wordlike |
| `семенович` | 77 | wordlike |
| `владимирович` | 72 | wordlike |
| `ивановна` | 66 | wordlike |
| `никитич` | 62 | wordlike |
| `святославич` | 57 | wordlike |
| `романович` | 52 | wordlike |
| `васильевна` | 50 | wordlike |

### Hangul

| token | times | shape |
| --- | ---: | --- |
| `아` | 9 | wordlike |
| `방` | 7 | wordlike |
| `처` | 7 | wordlike |
| `영` | 6 | wordlike |
| `의` | 6 | wordlike |
| `보` | 5 | wordlike |
| `문` | 5 | wordlike |
| `효` | 5 | wordlike |
| `구` | 5 | wordlike |
| `계` | 5 | wordlike |
| `위` | 5 | wordlike |
| `종` | 5 | wordlike |
| `대` | 5 | wordlike |
| `견` | 5 | wordlike |
| `오` | 5 | wordlike |
| `인` | 4 | wordlike |
| `동` | 4 | wordlike |
| `수` | 4 | wordlike |
| `천` | 4 | wordlike |
| `상` | 4 | wordlike |

## What this does not do

It strips nothing and proposes no rule. The honorific list is used only to
*count* a category — `todo.md` names honorifics as the problem, and a list
short enough to write by hand is not a classifier. Whether a patronymic should
become a `P735` at all is **NEEDS-DECISION — Emma**, and it is the question
Arne Olson Anda raised in `correspondence.md`.
