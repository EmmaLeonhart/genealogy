# Which tokens are patronymics, decided from the father

**Emma, 2026-08-15:** *"Whether something is or is not a patronymic here is
determined by completely offline information related to the person's father's
name."* No Wikidata data is used here at all.

Every token of every person is a row in
`reports/patronymic-classification.csv`.

| verdict | tokens | share |
| --- | ---: | ---: |
| patronymic | 34,139 | 6.5% |
| not patronymic | 376,748 | 71.3% |
| no father recorded | 114,644 | 21.7% |
| father has no given name | 3,081 | 0.6% |
| **total** | **528,612** | |

**Of the 410,887 tokens where a verdict was possible, 34,139 are patronymic (8.3%).**

**A person with no recorded father gets no verdict**, not a `no` — absence of
a father in our data is absence of evidence, and a `no` there would be a
claim we cannot make.

## The tokens that go both ways — this is the point

**958 distinct tokens are a patronymic for some bearers and not for
others.** Same string, different usage, and therefore **different Wikidata
items** — `CLAUDE.md` § *"Jackson Jackson Jackson"*. A suffix list alone would
have called every bearer of these a patronymic.

| token | patronymic | not | 
| --- | ---: | ---: |
| Olsdatter | 1,058 | 44 |
| Olsen | 1,018 | 119 |
| Pedersdatter | 626 | 36 |
| Larsdatter | 578 | 14 |
| Hansdatter | 573 | 3 |
| Pedersen | 570 | 58 |
| Larsson | 533 | 112 |
| Andersdatter | 497 | 5 |
| Olson | 386 | 26 |
| Rasmusdatter | 366 | 5 |
| Andersson | 365 | 117 |
| Jensdatter | 364 | 10 |
| Jonsdatter | 324 | 17 |
| Eriksdatter | 318 | 26 |
| Nilsdatter | 288 | 15 |
| Nilsson | 271 | 26 |
| Eriksen | 256 | 19 |
| Johannesdatter | 245 | 6 |
| Rasmusson | 238 | 3 |
| Larsdotter | 223 | 11 |
| Rasmussen | 221 | 12 |
| Jørgensdatter | 210 | 6 |
| Nielsdatter | 207 | 39 |
| Pederson | 203 | 13 |
| Jonson | 193 | 6 |

## Method

Two forms, both requiring the father:

- **suffixed** — `<father's stem><suffix>`, allowing a dropped final vowel
  (`Ole` → `Ols-`) and one linking `s`. 26 endings, Scandinavian, Dutch,
  Slavic and Polish.
- **particle** — `ben`/`bin`/`ibn`/`bint`/`bat`/`ap`/`mac` followed by the
  father's own name, which is how the Samaritan records are written.

Diacritics are folded **for the stem comparison only** — `Åke` → `Akesson` is
spelling drift inside one derivation, not two different names. The fold never
reaches an emitted value; `CLAUDE.md`'s rule about diacritics is unchanged.
