# Wikidata items with a Geni ID we have never exported

Generated offline from `out/wikidata/p2600-all.tsv` against the 275,437-person
merge. Full pair list: `reports/wikidata-unreached.tsv`. Browsable page:
`out/wikidata-unreached.html` (gitignored — regenerate rather than commit).

| | count |
| --- | ---: |
| P2600 pairs on Wikidata | 516,983 |
| **pairs whose Geni ID is not in our tree** | **504,123** |
| …distinct Geni IDs | 504,063 |
| …distinct Wikidata items | 502,165 |
| pairs we do hold | 12,860 |

**Every row is a person Wikidata already names a Geni profile for, and that no
export here has reached.** This is the direct answer to why the joined figure is
only ~12,850: not because the two sites disagree about who exists, but because
our 145 exports have touched 2.5% of the Geni population Wikidata points at.

The three counts differ on purpose. Distinct Geni IDs is smaller than pairs
because an item can carry two Geni IDs; distinct items is smaller again because
a Geni ID can sit on two items. Collapsing them would hide exactly the rows
worth looking at — see `reports/wikidata-doubles.md`.

**What this is not.** It is not a queue of people to create on Wikidata: these
already have items. It is a list of **export targets** — Geni profiles that
exist and that we have never pulled. It says nothing about where they sit in
the genealogy, so it does not rank; `reports/wikidata-ancestors.md` is the
ranked slice (the 1,821 sitting one hop above somebody we already hold).
