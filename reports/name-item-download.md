# Sizing the name-item download

Emma approved a `wikidownload` pass fetching the items `P735` and `P734` point
at. The store holds *people* — the download walked P22/P25/P26/P40/P3373 — so no
name string resolves to an item offline today.

**The figure on record was a sample**: 40 shards, 40,000 items, 13,683 distinct
name targets of which 55 were present, 0.4%. That is a 2.8% sample, and this
project has had to withdraw an extrapolation before. This is the full count.

Measured over **all 1,408 shards, 1,408,401 stored items**.
Offline; nothing was fetched.

## The answer

| | count |
| --- | ---: |
| distinct items referenced by `P735` | 31,023 |
| distinct items referenced by `P734` | 101,854 |
| referenced by both | 308 |
| **distinct name items in total** | **132,569** |
| …already in the store | 113 |
| **…to download** | **132,456** |

**0.09% are already present**, so the download is 132,456 items.

| | items |
| --- | ---: |
| stored items stating a given name (`P735`) | 1,015,504 |
| stored items stating a family name (`P734`) | 758,744 |

## How concentrated the references are

A name item referenced by thousands of people is worth more than one referenced
once, and it decides whether a partial download would be useful.

| | |
| --- | ---: |
| name items referenced at least 1 times | 132,569 |
| name items referenced at least 2 times | 76,184 |
| name items referenced at least 5 times | 33,593 |
| name items referenced at least 10 times | 17,936 |
| name items referenced at least 100 times | 2,420 |
| name items referenced at least 1,000 times | 225 |

The twenty most-referenced name items:

| item | references |
| --- | ---: |
| Q4925477 | 45,022 |
| Q12344159 | 32,428 |
| Q16428906 | 19,996 |
| Q385468 | 19,368 |
| Q734578 | 19,095 |
| Q2958359 | 18,248 |
| Q677191 | 18,032 |
| Q4927937 | 17,549 |
| Q15921732 | 16,216 |
| Q1158477 | 15,976 |
| Q1249148 | 13,147 |
| Q278835 | 12,019 |
| Q4963612 | 10,972 |
| Q564684 | 9,201 |
| Q666578 | 8,712 |
| Q18057751 | 7,956 |
| Q923 | 7,856 |
| Q686223 | 7,125 |
| Q471788 | 6,735 |
| Q18201513 | 6,719 |

Those twenty account for **312,372 of 2,016,016 references** (15.5%).

### A partial download is viable, and this is by how much

Downloading the most-referenced items first, what share of all references
would be resolvable:

| download the top | of 132,569 | references covered |
| ---: | ---: | ---: |
| 100 | 0.1% | **28.4%** |
| 500 | 0.4% | **46.5%** |
| 1,000 | 0.8% | **55.3%** |
| 2,420 | 1.8% | **66.3%** |
| 5,000 | 3.8% | **74.5%** |
| 10,000 | 7.5% | **81.4%** |
| 17,936 | 13.5% | **86.6%** |
| 33,593 | 25.3% | **91.6%** |
| 76,184 | 57.5% | **97.2%** |

Per-item counts for all 132,569 are in `reports/name-items.csv`, so any other
cut can be taken without re-reading the 2.7 GB store.

## What this does not do

**No download was run and none is scheduled.** `CLAUDE.md` says the one bulk job
permitted to talk to Wikidata *"is confirmed before a live run"*, and an
approval given in a rapid question round is not that confirmation. This is the
number that makes the confirmation an informed one.
