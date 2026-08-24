# The edit graph the batches declare

284125 edit objects, 284092 distinct ids.

## Duplicate ids

Two edits claiming one name. A `requires` pointing at it is ambiguous, and a run that skips ids it has already done may skip the wrong one.

| id | extra copies | file |
| --- | ---: | --- |
| `add_geni_id:Q694696` | 1 | `wikidata-add-geni-id.json` |
| `add_relationship:Q96124:P22:Q161419` | 1 | `wikidata-orderlife.json` |
| `add_relationship:Q40730:P26:Q161419` | 1 | `wikidata-orderlife.json` |
| `add_relationship:Q179844:P26:Q161419` | 1 | `wikidata-orderlife.json` |
| `add_relationship:Q886894:P22:Q39952` | 1 | `wikidata-orderlife.json` |
| `add_relationship:Q93172:P26:Q161419` | 1 | `wikidata-orderlife.json` |
| `add_relationship:Q785598:P22:Q161419` | 1 | `wikidata-orderlife.json` |
| `add_relationship:Q40003:P22:Q3350` | 1 | `wikidata-orderlife.json` |
| `add_relationship:Q161419:P26:Q40730` | 1 | `wikidata-orderlife.json` |
| `add_relationship:Q161419:P26:Q179844` | 1 | `wikidata-orderlife.json` |
| `add_relationship:Q161419:P26:Q93172` | 1 | `wikidata-orderlife.json` |
| `add_relationship:Q120197205:P22:Q161419` | 1 | `wikidata-orderlife.json` |
| `add_relationship:Q207715:P25:Q120197205` | 1 | `wikidata-orderlife.json` |
| `structural_correspondence:Q2001541` | 1 | `wikidata-structural-correspondence.json` |
| `structural_correspondence:Q712113` | 1 | `wikidata-structural-correspondence.json` |
| `structural_correspondence:Q110578320` | 1 | `wikidata-structural-correspondence.json` |
| `structural_correspondence:Q102825194` | 1 | `wikidata-structural-correspondence.json` |
| `structural_correspondence:Q238609` | 1 | `wikidata-structural-correspondence.json` |
| `structural_correspondence:Q2583477` | 1 | `wikidata-structural-correspondence.json` |
| `structural_correspondence:Q3120397` | 1 | `wikidata-structural-correspondence.json` |
| … | | 13 more |

## Dependencies nothing emits

A `requires` naming an id no batch produces. Nothing in this repo can ever satisfy it.

| batch | missing prefix | count | example |
| --- | --- | ---: | --- |
| `wikidata-orderlife.json` | `person:` | 55765 | `person:Q100068` |
| `wikidata-samaritan-succession.json` | `entity_resolution:` | 9 | `entity_resolution:Q107534535` |
| `wikidata-abram-father.json` | `entity_resolution:` | 2 | `entity_resolution:Q137394557` |

## Cycles

None among the edges that resolve.

