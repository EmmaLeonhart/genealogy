# The Han-only names are not names — they are name + courtesy name + clan seat

**Queue work, 2026-08-18.** One of the two things that made the romanisation attempt
unusable: `陳郡陽夏` was being romanised as part of a personal name when it is a *place*.
Measured, and it resolves into a rule.

## The structure

    鯤  幼輿  陳郡陽夏
    名   字    郡望
    given  courtesy  ancestral seat

Classical Chinese biographical form. `鯤` is the given name, `幼輿` the courtesy name
(字), and `陳郡陽夏` the 郡望 — the commandery and county a clan claims as its seat. The
last is **not part of anybody's name** and repeats across everyone in the lineage.

## It separates by token length, and the frequencies prove it

**66 four-character trailing tokens appear 20 or more times, across 8,315 records.**

| trailing token | records | what it is |
| --- | ---: | --- |
| `隴西狄道` | 1,253 | Longxi commandery, Didao county — seat of the Li |
| `河南洛陽` | 747 | Henan, Luoyang |
| `京兆長安` | 599 | Jingzhao, Chang'an |
| `京兆杜陵` | 402 | Jingzhao, Duling |
| `琅邪臨沂` | 368 | Langya Linyi — seat of the Wang |
| `河東聞喜` | 362 | Hedong Wenxi |
| `弘農華陰` | 337 | Hongnong Huayin — seat of the Yang |
| `范陽涿縣` | 316 | Fanyang, Zhuo county |

**A personal name does not repeat 1,253 times as the last token of a lineage.** That is
the whole test, and it needs no gazetteer.

### What remains once the seat is removed

| name tokens left | records |
| ---: | ---: |
| 0 | **714** |
| 1 | **6,113** |
| 2 | **1,459** |
| 3 | 28 |

**6,113 resolve to a single given name** — the tractable case. **1,459 are given plus
courtesy name**, where only the first should become the label, since a courtesy name is
not what a person is called in a catalogue. And **714 have nothing left at all**: the
entire recorded name was a clan seat, so those people have no personal name in the
corpus and no romanisation can invent one.

## Two-character trailing tokens are NOT the same case

    藤原 1,199   松平 770   織田 274   前田 236   本多 171   池田 159
    姬姓   279   范陽 214   河南 145   彭城 132

**The first row is Japanese surnames** — Fujiwara, Matsudaira, Oda, Maeda, Honda, Ikeda —
which are real names and must be kept. **The second is Chinese clan and place markers** —
`姬姓` is of the Ji clan, and `范陽`, `河南`, `彭城` are commanderies appearing without
their county.

**So the length rule does not generalise downward**, and a blanket drop of repeated
trailing tokens would delete 3,000-odd Japanese surnames. Two-character tokens need the
culture settled first, which is what the traversal already does.

## What this changes for the romanisation

The reading tables were never the only problem. **8,315 records were being romanised with
a place attached**, and 714 of them have no name at all underneath it. Stripping seats
before romanising takes the tractable set to **6,113 single-token given names** — a far
better target than 1,934 mixed strings, and one where a wrong reading is a wrong *name*
rather than a wrong sentence.
