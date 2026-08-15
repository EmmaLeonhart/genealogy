# Patronymic items that already exist on Wikidata

Emma, 2026-08-15: *"for the 119 patronymic items, please save them… so that we can be a bit clear about this stuff. Because I don't want us to be creating duplicates of things."*

**Every item on Wikidata that is `instance of` patronymic (`Q110874`): 633.** One row each in `reports/patronymic-items.csv`. Given-name and family-name items are already covered by `reports/name-items.csv` (132,569 rows); patronymics were the gap, because the local store is a Geni-shaped slice of **people** and holds none of them.

**119 carry `P144` based on** — the structured link to the name they derive from, which is what Emma asked to find. **97 carry `P5278`**, pairing `Eriksson` with `Eriksdotter`.

## Languages

| language | items |
| --- | ---: |
| (none stated) | 263 |
| Russian | 90 |
| Icelandic | 73 |
| Spanish | 63 |
| Ukrainian | 56 |
| Swedish | 13 |
| Belarusian | 11 |
| Dutch | 7 |
| Catalan | 7 |
| Portuguese | 6 |

**Wikidata's patronymic coverage is Russian, Icelandic, Spanish and Ukrainian.** Swedish has 13 items and Danish/Norwegian essentially none — which matters here, because the Nordic `-sen`/`-datter` forms are the bulk of this corpus's patronymics.

## Ours that already have an item — LINK these, never create them

**143 of the 633 match a token in our corpus.**

| item | name | our bearers | based on |
| --- | --- | ---: | --- |
| `Q51885688` | Olsdatter | 924 | — |
| `Q130233025` | Pedersen | 745 | Q10622039 (Peder) |
| `Q130232913` | Eriksson | 331 | Q750186 (Erik) |
| `Q130233015` | Nilsson | 322 | Q16423038 (Nils) |
| `Q122837798` | Nilsdatter | 229 | — |
| `Q108828512` | Karlsson | 206 | — |
| `Q130232912` | Eriksdotter | 146 | Q750186 (Erik) |
| `Q28800799` | Velásquez | 129 | — |
| `Q109482873` | Jacobsdatter | 92 | — |
| `Q124311590` | Fedorovych | 70 | — |
| `Q113333366` | Petrovych | 62 | Q16085472 (Petro) |
| `Q21506668` | Nogueira | 62 | — |
| `Q130232998` | Pedersson | 55 | Q10622039 (Peder) |
| `Q56627728` | Ivanovich | 54 | Q21104340 (Ivan) |
| `Q55359323` | Iñigo | 45 | — |
| `Q113146085` | Semenovych | 43 | — |
| `Q29441579` | Menéndez | 42 | — |
| `Q110169158` | Romanovych | 40 | — |
| `Q118604086` | Danylovych | 35 | Q16275293 (Danylo) |
| `Q29471474` | Páez | 33 | — |
| `Q108320932` | Simonsen | 33 | — |
| `Q59939101` | Belchior | 31 | — |
| `Q140226461` | Q140226461 | 31 | — |
| `Q21506553` | Sigurdsson | 25 | — |
| `Q7916711` | Vasilyevich | 24 | Q27452576 (Vasily) |
| `Q100964961` | Andreyevich | 24 | — |
| `Q114834115` | Romanovich | 24 | — |
| `Q83359767` | Johannesdotter | 22 | — |
| `Q70252981` | Ordoño | 22 | — |
| `Q28136553` | Månsdotter | 21 | Q19799975 (Måns) |

## Ours with no item at all

**4,143 distinct patronymic-shaped tokens in this corpus have no Wikidata patronymic item**, borne by 38,129 people. That is the creation population, and it is almost entirely Nordic — the languages Wikidata has barely covered.

**The suffix is evidence, not proof.** `-sen` and `-son` also end ordinary inherited surnames and a few genuine given names (`Jefferson`, 30 bearers; `Boson`, 26). `-ovich`/`-ovna`/`-sdatter` are reliable; `-son`/`-sen` are not. See `reports/name-classes.md`.
