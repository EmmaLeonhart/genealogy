# Wikidata items with a Geni ID we have never exported

Generated offline from `out/wikidata/p2600-all.tsv` against the 275,437-person
merge. Full pair list: `reports/wikidata-unreached.tsv`. Browsable page:
`out/wikidata-unreached.html` — **tracked**, and rebuilt from the TSV by
`python scripts/build-unreached-page.py` in about a second, no store pass and no
network. It used to say "gitignored — regenerate rather than commit" here, with
no script that could regenerate it; a fresh clone then took the page with it.

**What it is for**, in Emma's words: *"a table that lets me click to the geni
ids and run exports that will contain them and resolve these things."* Each row
links to the Wikidata item and to the Geni profile to export from.

| | count | at 145 exports |
| --- | ---: | ---: |
| P2600 pairs | 517,878 | 516,983 |
| …numeric, i.e. joinable | 517,850 | 516,955 |
| …malformed, kept separately | 28 | 28 |
| **pairs whose Geni ID is not in our tree** | **504,480** | 504,095 |
| pairs we do hold | 13,370 | 12,860 |

**Why only ~13,000 join.** Not because the two sites disagree about who exists:
because 149 exports have reached about 2.6% of the Geni population Wikidata
already points at.

**Both columns went up, for different reasons.** We hold 510 more of them than
at 145 exports — that is what the two new Forest exports and the Wife of John
Harvey pair bought on this axis. The *unreached* count also rose, because the
pair list itself is 895 larger: the 145-export figure came from a live SPARQL
query and this one is counted from the downloaded store, which is a later
snapshot. The two numbers are not measuring the same instant of Wikidata and
the drift is ordinary.

**Where the pair list comes from now.** `out/wikidata/p2600-all.tsv`, written
from `wikidata/items/` by `genimerge wikidata-index --map`. It used to be a
cached SPARQL result; that cache was lost with `out/` on 2026-08-09 and was
rebuilt offline rather than re-queried. `scripts/build-unreached-tsv.py` does
the diff against `out/merged.ged`.

## Two things measured while building this, both worth knowing

**28 P2600 values are not IDs at all** — `reports/wikidata-p2600-malformed.tsv`.
They are URLs and URL fragments pasted into the field, e.g.
`https://www.geni.com/people/Abdul-MUTHALIB/4799832763350031690` and
`people/Josefina-Virginia-Alvear-…/6000000013301059830`. Each one *contains* a
usable ID, and none is extracted here: recovering an ID by parsing a URL out of
a field that should not hold one is the fuzzy matching this repo refuses
everywhere else. They are listed so they can be fixed **on Wikidata**, which is
where the defect is.

**Geni IDs are bimodal in length, and the short ones are real.** Of the numeric
values: 511,236 are 19 digits, 3,646 are 18, and **2,073 are 7 digits or
fewer** — down to a single digit. The short ones are old-style Geni IDs, not
corruption, and they are kept. This mattered: the first version of this table
sorted by ID length ascending, which put every oddity at the top and made the
page look like it held nothing but junk. It is now sorted by item (QID).

## What this is not

Not a queue of people to create on Wikidata — they already have items. Not
ranked, either: it says nothing about where a person sits in the genealogy, so
it cannot tell you which export would cover the most rows.
`reports/wikidata-ancestors.md` is the ranked slice — the 1,821 sitting one hop
above somebody we already hold.
