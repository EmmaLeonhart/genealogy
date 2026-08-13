# Marriage: date, place and end, derived

Plan item 6. Emma, 2026-08-12: *"Marriage date and place and end and whatever
will be easy-ish."*

`reports/derived-marriages.csv` — **36,314 families** that say something
about a marriage, out of 149,613.

## "End" is divorce, and only divorce

The `FAM`-level tags in this corpus are exactly:

| tag | count |
| --- | ---: |
| `CHIL` | 267,517 |
| `HUSB` | 126,894 |
| `WIFE` | 89,543 |
| `MARR` | 36,314 |
| `DIV` | 483 |
| `NOTE` | 73 |

**No annulment, no engagement, no separation.** A Geni marriage ends only by
divorce, and it does so **483 times**.

**This is the one field where the direction reverses.** Everywhere else in this
project Geni has more than Wikidata; here Wikidata's `P582` end time was
recorded on **257 of the 981** comparable marriages
(`reports/marriages.md`), because a marriage ending at a death is an end
Wikidata states and Geni has no family-level way to express. Deriving "end"
from Geni therefore supplies almost nothing.

## What is present

| | families | share of rows |
| --- | ---: | ---: |
| marriage date | 36,257 | 99.8% |
| marriage place | 10,779 | 29.7% |
| divorce date | 323 | 0.9% |
| divorce place | 21 | 0.1% |
| both spouses named | 20,059 | 55.2% |
| both spouses carry a Wikidata item | 1,251 | 3.4% |

**A marriage is only emittable when both spouses exist on Wikidata**, since
`P26` needs something to point at. That is the last row, and it is the real
size of what item 6 can currently produce.

## Dates the grammar could not read

1 values, 1 distinct. Raw text
kept rather than dropped.

| raw | times |
| --- | ---: |
| `-200000000` | 1 |

## Not done here

- **No `P26` shape chosen.** Emma asked to see cases before deciding and
  `reports/marriages.md` holds them; this is the derivation, not the mapping.
- **No place resolved to an item.**
- **The 30 families where Wikidata names a different spouse are untouched** —
  Christian IV's mistress is among them, so they are not gaps.
