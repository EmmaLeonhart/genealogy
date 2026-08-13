# Connected components of the Wikidata family graph

Computed once over the whole store so that asking whether a given person is on
an island is a lookup rather than a walk. Connectivity is
`P22`/`P25`/`P26`/`P40`/`P3373`.

**1,408,353 stored items, 4,081,369 relation edges, 223,178 components** (including items referenced but not stored).

## How big is the component a stored person sits in

| component size | people | share |
| --- | ---: | ---: |
| 1 — isolate | 183,296 | 13.0% |
| 2–5 | 87,558 | 6.2% |
| 6–20 | 64,676 | 4.6% |
| 21–100 | 23,645 | 1.7% |
| 101–1,000 | 3,823 | 0.3% |
| over 1,000 | 1,045,355 | 74.2% |

## The largest components

| component root | people |
| --- | ---: |
| Q2469565 | 1,116,499 |
| Q69783208 | 2,202 |
| Q45693533 | 284 |
| Q1528 | 277 |
| Q106828555 | 250 |

**This is what decides whether a link is worth making.** An ancestor whose
component is three people connects to three people. The world tree is the
component at the top of this table.
