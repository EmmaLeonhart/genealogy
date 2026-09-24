# Derived facts: occupation, dates, places

Plan items 3 and 4. Occupation is string work, and so are birthplace,
birth date, death date, death place, burial date and burial place.

One row per person in `reports/derived-facts.csv` — **2,198,766 people**, 
of whom 86,764 carry a Wikidata item.

## What is actually present

| field | people | share |
| --- | ---: | ---: |
| sex | 2,194,295 | 99.8% |
| occupation | 205,445 | 9.3% |
| birth date | 1,332,720 | 60.6% |
| birth place | 0 | 0.0% |
| death date | 1,080,386 | 49.1% |
| death place | 0 | 0.0% |
| burial date | 117,536 | 5.3% |
| burial place | 0 | 0.0% |

## Addresses, kept as text

An address goes on the address property as text. Wikidata's **`P6375`
street address** is monolingual text, so an
address never has to become a place item. **This supersedes the `PLAC`-only
rule of 2026-08-11**, which was chosen before its cost was known.

| | events |
| --- | ---: |
| birth address | 0 |
| death address | 0 |
| burial address | 0 |
| birth address, **no `PLAC` at all** | 0 |
| death address, **no `PLAC` at all** | 0 |
| burial address, **no `PLAC` at all** | 0 |

**0 events would have had no location under the old rule** and now keep one.

**One thing to flag rather than decide.** `P6375` is documented as a *street*
address — building number, locality, post code, and explicitly not country.
These blocks are the opposite shape: `CTRY` 147,173, `STAE` 132,781, `CITY`
107,734, and a street line (`ADR1`) only 2,738 times. A typical block is
`CITY Erie, STAE PA, CTRY United States` — a place hierarchy, not a street
address. The values are composed and carried as instructed; whether `P6375` is
the right destination for a country-level string is a conversion question, and
this is ingestion.

## Dates the grammar could not read

**10,368 date values**, 7,779 distinct, parsed to no year. They keep their raw
text in the CSV rather than being dropped — a date we cannot read must not
become a date we guessed.

| raw value | times |
| --- | ---: |
| `about 1670` | 40 |
| `about 1650` | 35 |
| `about 1660` | 30 |
| `about 1680` | 28 |
| `about 1700` | 27 |
| `about 1665` | 26 |
| `about 1250` | 24 |
| `about 1300` | 24 |
| `about 1630` | 23 |
| `about 1685` | 23 |
| `about 1280` | 21 |
| `about 1320` | 20 |
| `about 1690` | 20 |
| `about 1655` | 20 |
| `about 1640` | 20 |

`reports/impossible-years.md` has the full account of these: bare modifiers with
no operand, and cosmological years in the hundreds of millions belonging to
Shinto creation deities.

## Not done here

- **No place string is resolved to a Wikidata item.** Geni gives a comma-chain,
  Wikidata gives one item at one level of nesting, and which level a string
  resolves to is undecided — `PLAC Anda` against `P19 = Klepp Municipality`.
- **No occupation string is resolved to an item** either.
- **Nothing is emitted.** This is ingestion.
