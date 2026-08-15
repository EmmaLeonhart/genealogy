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


## Who they actually are — Emma's questions, 2026-08-15

She asked for this and named what she wanted: *"the degree that these people have,
Anglophone names, their nationalities, maybe some level of categorization... Do
they tend to be celebrities? Do they tend to be athletes? Do they tend to be
academics?"* The first version of this report answered with centuries and with the
tautology that 99.1% carry a `P2600` — which is the definition of the group, not a
finding.

### Her guess about Wikipedia — WRONG

*"My guess is, out of these people, almost all of them have Wikipedia articles. Is
that true?"* No.

| | of 183,674 |
| --- | ---: |
| any Wikipedia article | 83,226 (**45.3%**) |
| English Wikipedia | 46,237 (25.2%) |
| **none at all** | **100,448 (54.7%)** |

### Her guess about Geni connectedness — untestable for 99.6%, and false for the rest

*"They tend to be people who are relatively not that well-connected on Jenny."*

**Only 722 of the 183,671 are in our Geni corpus at all — 0.4%.** The other
**182,949 appear in none of our 203 exports**, so their Geni connectivity is not
something this data can speak to.

For the 722 we do hold: median 2 relatives, mean 3.28 — against a whole-corpus
median of 2 and mean 3.20. **Indistinguishable from everybody else.**

**Her conclusion still holds, for a different reason.** Not that they are poorly
connected, but that they are *outside the tree entirely*. Her ruling, same day:
*"this group of people is a group that I probably would consider to be very low
priority... I don't think that they're that important to get into the World Tree."*

### Not celebrities, not athletes — officials, writers and academics

| occupation | | country | |
| --- | ---: | --- | ---: |
| politician | 20,273 | United States | 21,543 |
| writer | 9,157 | **Song dynasty** | **17,259** |
| lawyer | 5,918 | Kingdom of Italy | 6,400 |
| university teacher | 5,917 | Germany | 5,232 |
| journalist | 4,600 | Italy | 4,934 |
| painter | 4,500 | Sweden | 3,983 |
| actor | 4,332 | Norway | 3,972 |
| military personnel | 3,945 | Finland | 3,455 |
| physician | 3,495 | Netherlands | 3,251 |

`actor` at 4,332 and `film actor` at 2,307 are the only celebrity-shaped entries
and together are under 4%. **No athlete occupation reaches the top 18.**

**The Song dynasty at 17,259 is the anomaly** — a large Chinese cohort inside a
group that is otherwise American and European, and it is second only to the United
States. Not explained here.
