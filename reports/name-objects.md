# Name objects: what exists, what does not, and what kind of names these are

> **STALE, 2026-08-18.** The "no item found" counts below are built from only the
> name items our own people already point at, and that was superseded three days after
> this report was written. `scripts/collect-name-item-qids.py` enumerated **824,358**
> name items by `P31` across the six name classes on 2026-08-15 and **823,907 of them
> (99.9%) are in the local store**. Quoting the figures below as current coverage is
> wrong; check the store. This warning exists because the report was quoted that way.


Scheduled by Emma for midnight. Every distinct name is a row in
`reports/name-objects.csv`, ranked by how many people carry it.

**Why the classification matters.** Her rule is that name items get created
*"for all of the names that fit sufficiently into Western name conventions"* —
so the question is not how many names lack an item, but **which ones are
candidates at all**.

## 1. How many name objects exist

| | given names | surnames |
| --- | ---: | ---: |
| exists | 9,345 | 6,488 |
| ambiguous | 2,107 | 560 |
| no item found | 92,228 | 37,435 |
| **distinct total** | **103,680** | **44,483** |

By people carrying the name, which is the number that matters for coverage:

| | given names | surnames |
| --- | ---: | ---: |
| exists | 163,675 | 57,466 |
| ambiguous | 91,450 | 5,198 |
| no item found | 277,695 | 148,920 |

## 2. "No item found" is not the same as "needs creating"

**This cannot be separated with the data we hold, and the report will not
pretend otherwise.** The lookup is built from the 132,569 name items that our
*own people's* `P735`/`P734` statements already point at. A name item that
exists on Wikidata but that nobody in our store references is invisible here
and reads as missing.

The evidence that this is a large effect is in the data itself: `Thomas`,
`Hans`, `Sarah`, `Henry` and `Marguerite` all read as *no item found*, and
Wikidata certainly has items for those. So the "no item" column is an **upper
bound on creations** and a mixture of two populations.

Separating them needs a download that fetches name items directly rather than
following the family walk — the same gap that limits `P735`/`P734` emission.

## 3. What kind of names these are

### Given names

| kind | distinct | people | of which an item exists |
| --- | ---: | ---: | ---: |
| ordinary Western given name | 64,080 | 378,406 | 9,242 |
| CJK clan name | 22,877 | 66,197 | 2 |
| place misfiled as a name | 5,960 | 11,378 | 0 |
| patronymic | 3,187 | 28,661 | 72 |
| non-Latin script (CYRILLIC) | 2,864 | 13,426 | 1 |
| non-Latin script (ARABIC) | 1,523 | 4,652 | 0 |
| non-Latin script (HANGUL) | 1,487 | 3,887 | 0 |
| not a name | 969 | 24,793 | 16 |
| non-Latin script (HEBREW) | 285 | 636 | 0 |
| non-Latin script (GREEK) | 246 | 477 | 12 |
| non-Latin script (HIRAGANA) | 47 | 92 | 0 |
| non-Latin script (KATAKANA) | 43 | 68 | 0 |
| non-Latin script (ARMENIAN) | 40 | 65 | 0 |
| non-Latin script (TIBETAN) | 19 | 19 | 0 |
| non-Latin script (GEORGIAN) | 14 | 19 | 0 |
| non-Latin script (MONGOLIAN) | 11 | 13 | 0 |
| non-Latin script (DEVANAGARI) | 7 | 7 | 0 |
| non-Latin script (MASCULINE) | 6 | 6 | 0 |
| non-Latin script (ETHIOPIC) | 5 | 7 | 0 |
| non-Latin script (KATAKANA/KATAKANA-HIRAGANA) | 2 | 2 | 0 |
| non-Latin script (GOTHIC) | 2 | 2 | 0 |
| non-Latin script (BENGALI) | 2 | 2 | 0 |
| non-Latin script (CYRILLIC/GREEK) | 1 | 1 | 0 |
| non-Latin script (MICRO) | 1 | 1 | 0 |
| non-Latin script (EGYPTIAN) | 1 | 2 | 0 |
| non-Latin script (TAMIL) | 1 | 1 | 0 |

### Surnames

| kind | distinct | people | of which an item exists |
| --- | ---: | ---: | ---: |
| ordinary Western surname | 28,991 | 103,608 | 5,059 |
| toponymic or territorial byname | 9,517 | 29,719 | 887 |
| patronymic | 2,075 | 12,570 | 530 |
| CJK clan name | 1,310 | 24,923 | 1 |
| non-Latin script (CYRILLIC) | 1,056 | 4,913 | 0 |
| place misfiled as a name | 830 | 24,941 | 0 |
| non-Latin script (ARABIC) | 314 | 3,284 | 0 |
| non-Latin script (HEBREW) | 138 | 268 | 0 |
| non-Latin script (HANGUL) | 121 | 5,272 | 0 |
| not a name | 69 | 1,949 | 11 |
| non-Latin script (GREEK) | 46 | 101 | 0 |
| non-Latin script (MONGOLIAN) | 6 | 22 | 0 |
| non-Latin script (ARMENIAN) | 3 | 3 | 0 |
| non-Latin script (GEORGIAN) | 3 | 5 | 0 |
| non-Latin script (ARABIC/GEORGIAN) | 1 | 1 | 0 |
| non-Latin script (BENGALI) | 1 | 1 | 0 |
| non-Latin script (ETHIOPIC) | 1 | 3 | 0 |
| non-Latin script (TAMIL) | 1 | 1 | 0 |

## Which names are creation candidates

Applying her rule — Western conventions — the candidates are the *ordinary*
rows with no item found. Everything else is excluded for a stated reason:

| excluded | why |
| --- | --- |
| patronymic | `Olsdatter` is not a family name; it says whose child someone is |
| place misfiled as a name | `隴西狄道` is a commandery and county, not a surname |
| CJK clan name | a real name, but not a Western convention |
| non-Latin script | same |
| toponymic byname | `of Châtellerault` is a place; Wikidata gives these no `P734` at a rate 33 points above base |
| not a name | `NN`, regnal ordinals, `Rd.`, punctuation |

**52,758 given names** with no item found, carried by 128,153 people.

The twenty most-carried:

| name | people |
| --- | ---: |
| of | 2,418 |
| Thomas | 1,113 |
| Hans | 1,098 |
| Sarah | 1,035 |
| Raden | 1,005 |
| Henry | 790 |
| Pangeran | 597 |
| Marguerite | 590 |
| Mas | 527 |
| R | 517 |
| Ratu | 477 |
| Wife | 455 |
| Of | 407 |
| Brita | 396 |
| Ayu | 365 |
| N | 335 |
| bint | 332 |
| Wilhelm | 307 |
| Jakob | 294 |
| (Wife | 287 |

**23,466 surnames** with no item found, carried by 57,930 people.

The twenty most-carried:

| name | people |
| --- | ---: |
| Al-Husayni | 471 |
| Bille | 172 |
| Al-Umawi | 153 |
| Spivey | 145 |
| Al-Hashemi | 139 |
| Welf | 133 |
| Al-Hasani | 124 |
| Espedal | 122 |
| Askanier | 121 |
| Tjørhom | 116 |
| Kaas | 112 |
| Chan | 108 |
| McKnight | 100 |
| Hurd | 95 |
| Håland | 90 |
| Laland | 85 |
| Sapieha h. Lis | 84 |
| Fidjeland | 82 |
| Borsheim | 81 |
| Erga | 80 |

## Where this classification is weak

- **CJK length is a proxy.** A one- or two-character Han string is treated as a
  clan name and anything longer as a place. `司馬` and `藤原` are two
  characters and are surnames; `隴西狄道` is four and is a place. It will
  misclassify a genuine three-character name.
- **Patronymic matching is by suffix.** `Jensen` as an inherited Danish family
  name and `Jensen` as "Jens's child" are the same string, and this counts
  both as patronymic. In this corpus that is usually right and sometimes not.
- **Nothing is fuzzy-matched.** A name matches a name item's label exactly,
  folded for case and diacritics, or it does not. A near miss is a miss.
