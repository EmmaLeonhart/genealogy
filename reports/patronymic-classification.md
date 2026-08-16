# Which tokens are patronymics, decided from the father

**Emma, 2026-08-15:** *"Whether something is or is not a patronymic here is
determined by completely offline information related to the person's father's
name."* No Wikidata data is used here at all.

Every token of every person is a row in
`reports/patronymic-classification.csv`.

| verdict | tokens | share |
| --- | ---: | ---: |
| not patronymic | 386,476 | 65.1% |
| no father recorded | 105,978 | 17.9% |
| patronymic | 41,767 | 7.0% |
| AMBIGUOUS: form, father differs | 33,170 | 5.6% |
| patronymic (inferred, no father recorded) | 21,242 | 3.6% |
| father has no given name | 3,273 | 0.6% |
| surname: patronymic form conflicts with recorded sex | 1,449 | 0.2% |
| AMBIGUOUS: form, father unnamed | 156 | 0.0% |
| patronymic (chain link 2, names William) | 9 | 0.0% |
| patronymic (chain link 2, names Abaye haKohen Gaon) | 7 | 0.0% |
| patronymic (chain link 2, names Ya'ish) | 4 | 0.0% |
| patronymic (chain link 2, names Yahya Hazaken) | 4 | 0.0% |
| patronymic (chain link 2, names Musa Banu Qasi) | 2 | 0.0% |
| patronymic (chain link 2, names Adai) | 2 | 0.0% |
| patronymic (chain link 2, names Éireann) | 2 | 0.0% |
| patronymic (chain link 2, names Briain) | 2 | 0.0% |
| patronymic (chain link 2, names Ferruzi'el) | 2 | 0.0% |
| patronymic (chain link 2, names Mar Shealtiel) | 2 | 0.0% |
| patronymic (chain link 2, names Ezra) | 2 | 0.0% |
| patronymic (chain link 2, names Khamma) | 2 | 0.0% |
| patronymic (chain link 2, names Kaspi) | 2 | 0.0% |
| patronymic (chain link 2, names Asher ben Matzliach) | 2 | 0.0% |
| patronymic (chain link 3, names Matzliach) | 2 | 0.0% |
| patronymic (chain link 2, names Muhājir) | 1 | 0.0% |
| patronymic (chain link 2, names Meir) | 1 | 0.0% |
| patronymic (chain link 2, names Palṭoi Kohen Ṣedeq) | 1 | 0.0% |
| patronymic (chain link 2, names Nearya) | 1 | 0.0% |
| patronymic (chain link 2, names Tzadok) | 1 | 0.0% |
| patronymic (chain link 2, names ʿAwkal) | 1 | 0.0% |
| patronymic (chain link 2, names Obadya) | 1 | 0.0% |
| patronymic (chain link 2, names Petrwn) | 1 | 0.0% |
| patronymic (chain link 2, names 'Amr) | 1 | 0.0% |
| patronymic (chain link 2, names Abdullaah bin Muslim bin Aqeel) | 1 | 0.0% |
| patronymic (chain link 3, names Muslim bin Aqeel) | 1 | 0.0% |
| patronymic (chain link 4, names Aqeel) | 1 | 0.0% |
| patronymic (chain link 2, names Muslim bin Aqeel) | 1 | 0.0% |
| patronymic (chain link 3, names Aqeel) | 1 | 0.0% |
| patronymic (chain link 2, names Acha) | 1 | 0.0% |
| patronymic (chain link 2, names Lakhtush) | 1 | 0.0% |
| patronymic (chain link 2, names Avraham of Opatow) | 1 | 0.0% |
| patronymic (chain link 2, names Shaprut) | 1 | 0.0% |
| patronymic (chain link 2, names Samuel Gaon ha-Kohen) | 1 | 0.0% |
| patronymic (chain link 2, names Israel Gaon ha-Kohen) | 1 | 0.0% |
| patronymic (chain link 2, names Isaac of Narbonne) | 1 | 0.0% |
| patronymic (chain link 2, names Hasan) | 1 | 0.0% |
| patronymic (chain link 2, names Aqeel) | 1 | 0.0% |
| patronymic (chain link 2, names Muhammad) | 1 | 0.0% |
| patronymic (chain link 2, names Khalaf) | 1 | 0.0% |
| patronymic (chain link 2, names Zemah Kohen Ṣedeq) | 1 | 0.0% |
| patronymic (chain link 2, names Ghayyāth HaLevi) | 1 | 0.0% |
| patronymic (chain link 2, names Anan) | 1 | 0.0% |
| patronymic (chain link 2, names Tabin) | 1 | 0.0% |
| patronymic (chain link 2, names Sallah al-Kafri, resh metivta al-Kafri) | 1 | 0.0% |
| patronymic (chain link 2, names Albalia) | 1 | 0.0% |
| patronymic (chain link 2, names Dafydd) | 1 | 0.0% |
| patronymic (chain link 2, names Shmuel & Yocheved bat RASHI) | 1 | 0.0% |
| patronymic (chain link 3, names RASHI) | 1 | 0.0% |
| **total** | **593,591** | |

**33,326 tokens carry a patronymic FORM that the father does
not confirm.** Emma asked for these to be separated rather than silently
called non-patronymic: *"We probably should be doing some level of
classification for situations where it is ambiguous."* They are the
`AMBIGUOUS:` rows, split by why the father could not settle it.

Her prior on them, recorded and **not applied** — deciding on it would be
inference where this project uses evidence: *"most patronymics are not used
as surnames."*

**Of the 428,243 tokens where a verdict was possible, 41,767 are patronymic (9.8%).**

**A person with no recorded father gets no verdict**, not a `no` — absence of
a father in our data is absence of evidence, and a `no` there would be a
claim we cannot make.

## The tokens that go both ways — this is the point

**1,117 distinct tokens are built on one bearer's father and not on
another's.** Same string, different usage, and therefore **different Wikidata
items** — `CLAUDE.md` § *"Jackson Jackson Jackson"*. A suffix list alone would
have called every bearer of these a patronymic.

| token | father confirms | father differs |
| --- | ---: | ---: |
| Olsdatter | 1,256 | 50 |
| Olsen | 1,210 | 164 |
| Pedersdatter | 688 | 39 |
| Larsson | 637 | 114 |
| Pedersen | 633 | 77 |
| Larsdatter | 620 | 14 |
| Hansdatter | 618 | 3 |
| Andersson | 603 | 167 |
| Andersdatter | 577 | 8 |
| Andersdotter | 440 | 38 |
| Olson | 428 | 32 |
| Nilsson | 424 | 42 |
| Rasmusdatter | 404 | 5 |
| Jensdatter | 392 | 10 |
| Jonsdatter | 370 | 22 |
| Eriksdatter | 339 | 26 |
| Larsdotter | 336 | 14 |
| Nilsdatter | 311 | 22 |
| Rasmusson | 292 | 3 |
| Eriksen | 279 | 24 |
| Nilsdotter | 278 | 16 |
| Johannesdatter | 276 | 7 |
| Johansson | 271 | 84 |
| Johansdotter | 258 | 53 |
| Olofsson | 257 | 42 |

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
