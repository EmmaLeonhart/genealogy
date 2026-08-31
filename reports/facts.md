# Derived facts: occupation, dates, places

Plan items 3 and 4. Emma, 2026-08-12: *"Occupation can be done with string
stuff"* and *"Birthplace birth date death date death place burial date burial
place all can be done with string."*

One row per person in `reports/derived-facts.csv` — **1,451,964 people**, 
of whom 43,680 carry a Wikidata item.

## What is actually present

| field | people | share |
| --- | ---: | ---: |
| sex | 1,444,974 | 99.5% |
| occupation | 185,464 | 12.8% |
| birth date | 1,011,055 | 69.6% |
| birth place | 378,013 | 26.0% |
| death date | 809,089 | 55.7% |
| death place | 264,362 | 18.2% |
| burial date | 103,991 | 7.2% |
| burial place | 99,329 | 6.8% |

## Addresses, kept as text

Emma, 2026-08-12: *"Do addresses with the address property (multilingual
text)."* Wikidata's **`P6375` street address** is monolingual text, so an
address never has to become a place item. **This supersedes the `PLAC`-only
rule of 2026-08-11**, which was chosen before its cost was known.

| | events |
| --- | ---: |
| birth address | 605,378 |
| death address | 452,978 |
| burial address | 119,739 |
| birth address, **no `PLAC` at all** | 410,256 |
| death address, **no `PLAC` at all** | 318,875 |
| burial address, **no `PLAC` at all** | 58,766 |

**793,992 events would have had no location under the old rule** and now keep one.

**One thing to flag rather than decide.** `P6375` is documented as a *street*
address — building number, locality, post code, and explicitly not country.
These blocks are the opposite shape: `CTRY` 147,173, `STAE` 132,781, `CITY`
107,734, and a street line (`ADR1`) only 2,738 times. A typical block is
`CITY Erie, STAE PA, CTRY United States` — a place hierarchy, not a street
address. The values are composed and carried as instructed; whether `P6375` is
the right destination for a country-level string is a conversion question, and
this is ingestion.

## Dates the grammar could not read

**30 date values**, 16 distinct, parsed to no year. They keep their raw
text in the CSV rather than being dropped — a date we cannot read must not
become a date we guessed.

| raw value | times |
| --- | ---: |
| `ABT` | 15 |
| `BET 725 AND` | 1 |
| `-538000000` | 1 |
| `-1400000000` | 1 |
| `ABT -538000000` | 1 |
| `13011704` | 1 |
| `BET  AND` | 1 |
| `19981` | 1 |
| `265 APR 1843` | 1 |
| `SEP 41666` | 1 |
| `DEC 161728` | 1 |
| `105 NOV 1743` | 1 |
| `JUN 171862` | 1 |
| `AFT` | 1 |
| `BET 6 NOV 1432 AND` | 1 |

`reports/impossible-years.md` has the full account of these: bare modifiers with
no operand, and cosmological years in the hundreds of millions belonging to
Shinto creation deities.

## Not done here

- **No place string is resolved to a Wikidata item.** Geni gives a comma-chain,
  Wikidata gives one item at one level of nesting, and which level a string
  resolves to is undecided — `PLAC Anda` against `P19 = Klepp Municipality`.
- **No occupation string is resolved to an item** either.
- **Nothing is emitted.** This is ingestion.
