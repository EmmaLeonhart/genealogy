# Who the isolated Wikidata people are

**Emma, 2026-08-15:** *"I want to basically analyze them demographically."*

**Isolated = the item states no `P22`/`P25`/`P40`/`P3373`/`P26`.** Every one
is a row in `reports/wikidata-isolates.csv`.

| | items |
| --- | ---: |
| humans in the store | 1,417,100 |
| **stated-none — no relationship at all** | **185,422** |
| edge-of-slice — states relatives we do not hold | 131 |
| connected | 1,231,547 |

**`edge-of-slice` is NOT isolation.** Those items state relationships whose
targets were never downloaded — a fact about our slice, not about Wikidata.
Merging the two would measure our own sampling and report it as Wikidata's
content, which is the § *"Is X present?"* failure this repo keeps making.

## By century of birth

| century | isolated | share |
| --- | ---: | ---: |
| BCE | 35 | 0.0% |
| 1s | 4 | 0.0% |
| 101s | 5 | 0.0% |
| 201s | 7 | 0.0% |
| 301s | 4 | 0.0% |
| 401s | 5 | 0.0% |
| 501s | 3 | 0.0% |
| 601s | 18 | 0.0% |
| 701s | 10 | 0.0% |
| 801s | 37 | 0.0% |
| 901s | 184 | 0.1% |
| 1001s | 497 | 0.3% |
| 1101s | 450 | 0.2% |
| 1201s | 276 | 0.1% |
| 1301s | 76 | 0.0% |
| 1401s | 112 | 0.1% |
| 1501s | 668 | 0.4% |
| 1601s | 1,912 | 1.0% |
| 1701s | 8,020 | 4.3% |
| 1801s | 88,666 | 47.8% |
| 1901s | 52,039 | 28.1% |
| 2001s | 90 | 0.0% |
| no date | 32,304 | 17.4% |

**Only 153,118 of 185,422 carry a birth date at all** (82.6%).

## Sex, and what else they carry

| | items | share |
| --- | ---: | ---: |
| male | 142,750 | 77.0% |
| female | 42,550 | 22.9% |
| not stated | 122 | 0.1% |
| carries an occupation `P106` | 94,393 | 50.9% |
| carries a noble title `P97` | 1,501 | 0.8% |
| **carries a Geni ID `P2600`** | **183,674** | 99.1% |

A `P2600` on an isolated item is the case `CLAUDE.md` describes: the person
is on Geni **and** on Wikidata, and what is missing is the genealogy.
