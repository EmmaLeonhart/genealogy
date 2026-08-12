# Derived facts: occupation, dates, places

Plan items 3 and 4. Emma, 2026-08-12: *"Occupation can be done with string
stuff"* and *"Birthplace birth date death date death place burial date burial
place all can be done with string."*

One row per person in `reports/derived-facts.csv` — **298,591 people**, 
of whom 14,157 carry a Wikidata item.

## What is actually present

| field | people | share |
| --- | ---: | ---: |
| sex | 298,130 | 99.8% |
| occupation | 31,401 | 10.5% |
| birth date | 150,203 | 50.3% |
| birth place | 58,562 | 19.6% |
| death date | 118,918 | 39.8% |
| death place | 38,990 | 13.1% |
| burial date | 11,907 | 4.0% |
| burial place | 16,360 | 5.5% |

## The cost of `PLAC` only

Emma chose *ignore `ADDR`, use `PLAC` only* on 2026-08-11. That is applied here,
and the loss is counted rather than left implicit:

**101,579 events carry an `ADDR` block and no `PLAC` at all**, against **113,912** events where `PLAC` supplied a place.

So the rule is not costing precision on those events — it is costing the place
entirely, and it applies to 47% of the events that have any location information at all.

**The rule stands; this is the size of it.** It was chosen over *"use `ADDR`
only when `PLAC` is absent"*, which is exactly the population counted here —
that alternative would roughly double the places available and never override a
`PLAC`. Recorded so the choice is re-openable on a number rather than on a
recollection.

## Dates the grammar could not read

**12 date values**, 9 distinct, parsed to no year. They keep their raw
text in the CSV rather than being dropped — a date we cannot read must not
become a date we guessed.

| raw value | times |
| --- | ---: |
| `ABT` | 4 |
| `BET 725 AND` | 1 |
| `-538000000` | 1 |
| `-1400000000` | 1 |
| `ABT -538000000` | 1 |
| `13011704` | 1 |
| `BET  AND` | 1 |
| `AFT` | 1 |
| `BET 25 JUN 1284 AND` | 1 |

`reports/impossible-years.md` has the full account of these: bare modifiers with
no operand, and cosmological years in the hundreds of millions belonging to
Shinto creation deities.

## Not done here

- **No place string is resolved to a Wikidata item.** Geni gives a comma-chain,
  Wikidata gives one item at one level of nesting, and which level a string
  resolves to is undecided — `PLAC Anda` against `P19 = Klepp Municipality`.
- **No occupation string is resolved to an item** either.
- **Nothing is emitted.** This is ingestion.
