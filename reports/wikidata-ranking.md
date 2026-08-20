# Every relative with a Wikidata item, ranked

**Emma, 2026-08-18:** *"Jonas Salte (Q138696805) is the best person to go to. Any other
people — do you have a ranking of all the ones we found?"*

**22 people within 14 hops carry an item.** Ranked below by hops, then by what the item is
actually worth — because those two orders disagree, and the disagreement matters.

| hops | qid | sitelinks | family links | who |
| ---: | --- | ---: | ---: | --- |
| **8** | `Q138696805` | **0** | **0** | Jonas Salte — killed during WWII (1920–1944) |
| 9 | `Q30019076` | 1 | 1 | Racin Kolnes — missionary |
| 10 | `Q19392422` | 2 | 0 | Thorvald Oftedal — musician (1878–1967) |
| **10** | **`Q467497`** | **44** | **2** | **Arne Garborg — writer (1851–1924)** |
| 11 | `Q11959067` | 2 | 2 | Arne Olaus Fjørtoft Garborg — librarian |
| 11 | `Q30019081` | 0 | 1 | Sigrid Zetlitz Kolnes — missionary (1902–1949) |
| 12 | `Q16164886` | 1 | 1 | Arne Anda — missionary |
| 12 | `Q275867` | 7 | 0 | Peter Hognestad — bishop and writer (1866–1931) |
| **12** | `Q3143008` | **23** | 2 | **Hulda Garborg — writer and politician (1862–1934)** |
| 12 | `Q4588795` | 6 | **4** | Karen Grude Koht — educator (1871–1960) |
| 13 | `Q11993404` | 4 | 0 | Olaus Olsen Eskeland — politician (1833–1903) |
| 13 | `Q30019061` | 0 | 1 | Michael Jaasund — missionary (1893–1969) |
| 13 | `Q3936948` | 2 | 1 | Carl Rønneberg — businessman |
| 14 | `Q108793090` | 1 | **6** | Christoffer Christoffersen (1784–1855) |
| 14 | `Q108791311` | 1 | **5** | Marta Maria Aasland I (1790–1874) |
| 14 | `Q60461846` | 1 | **5** | Rasmus Gerhard Rønneberg |
| 14 | `Q11852697` | 3 | 0 | Arne Rancken — Finnish architect |
| 14 | `Q11979685` | 3 | 0 | Jørgen Erikson |
| 14 | `Q15814770` | 3 | 0 | Ole Gabriel Kverneland — businessperson |
| 14 | `Q19385288` | 2 | 0 | Peter Hjalmar Finnestad |
| 14 | `Q6423949` | 2 | 1 | Knut Lier-Hansen — resistance member |
| 14 | `Q80094092` | 2 | 0 | Ingvald Enersen |

## Jonas Salte is the nearest and he is an island

**0 sitelinks. 0 family links.** No `P22`, `P25`, `P26`, `P40` or `P3373` — his item is
not attached to another person anywhere on Wikidata.

This repo already knows that trap. `build-path-to-wikidata-report.py`'s own docstring
says it: *"An item with no P22/P25/P26/P40/P3373 is an island. Linking to it joins
nothing, which is why the nearest is not automatically the best target."* Salte is the
nearest **and** the emptiest item in the whole table.

**He is still the right answer to the question that was asked** — fewest hops to somebody
with an item. He is the wrong answer to the question underneath it, which is connecting
this tree to Wikidata's.

## Arne Garborg is two hops further and worth incomparably more

**`Q467497`, 44 sitelinks** — one of the most important writers in Norwegian literature,
the man who made Nynorsk a literary language. Forty-four language versions against
Salte's zero.

**Two hops of extra distance buys a national figure instead of a stub.**

And he does not come alone. The table is not a random scatter of Norwegians — it is the
**Jæren and Nynorsk cultural circle**, which is exactly the region the surname census
placed this family in:

- **Arne Garborg** (10) and **Hulda Garborg** (12), husband and wife, 44 and 23 sitelinks
- **Peter Hognestad** (12), Bishop of Bjørgvin, a Nynorsk bible translator
- **Karen Grude Koht** (12), educator, **4 family links** — she married the historian and
  foreign minister Halvdan Koht
- **Ole Gabriel Kverneland** (14), who founded the farm-machinery firm still named for him
- and a cluster of Jæren missionaries — Racin Kolnes, Sigrid Zetlitz Kolnes, Arne Anda,
  Michael Jaasund

## If the goal is joining the world tree, rank by family links instead

The last column is the one that matters for connection, and it reorders things again:

    Christoffer Christoffersen  14 hops   6 family links
    Marta Maria Aasland I       14        5
    Rasmus Gerhard Rønneberg    14        5
    Karen Grude Koht            12        4
    Arne Garborg                10        2   <- best combination of near, famous, attached

**`Q467497` wins on every reading except raw distance.** Near enough at ten, attached to
other people, and famous enough that anything linked to him inherits an audience.

## What is not in this table

**Nobody living.** All 22 are dead, and 20 of the 22 were born before 1935. The living
relatives inside eight hops — 53 of them — hold no items and, per
`reports/publication-search.md`, no publication records either. So this table answers
*"who can I connect to"* and not *"who can I make notable"*, which remains open.
