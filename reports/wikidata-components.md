# How many trees the Wikidata side is

Measured 2026-08-09 over the whole downloaded store, offline. One streaming
pass building the relation graph from the five properties the download walk
itself used — `P22` father, `P25` mother, `P26` spouse, `P40` child, `P3373`
sibling — then union-find. 412 seconds, no second pass.

This had never been established. Our Geni side has had a component count in
`reports/frontier.md` since the beginning; the Wikidata side had none, so
"is it all one tree?" was open.

## The graph

| | count |
| --- | ---: |
| stored items | 1,408,401 |
| relation references | 4,081,369 |
| …pointing at an item we stored | 3,998,312 |
| …pointing at an item we did **not** store | 83,057 |

## The components

| | count |
| --- | ---: |
| connected components | 223,208 |
| **largest** | **1,042,423** (74.0%) |
| second largest | 2,168 |
| components of 1,000 or more | 2 |
| isolated single items | 183,296 (13.0%) |

**It is one tree plus dust.** 74% of everything stored sits in a single
component, and the drop from there to the second largest is three orders of
magnitude — 1,042,423 to 2,168. There is no second genealogy: there is one, and
then 223,206 fragments of which 183,296 are single items with no family link to
anything else we hold.

## The 83,057 dangling references are the important number

They are relation statements pointing at items the download never fetched, and
**a component boundary caused by one of those is not a real boundary** — it is
our copy being truncated at the edge, not Wikidata being disconnected there.
The download was stopped with 74,610 QIDs still queued, which is the same
population seen from the other side.

So 223,208 is an **upper bound** on the number of Wikidata genealogies, not a
measurement of them. Finishing the download would merge an unknown number of
those fragments into the giant component, and nothing here says how many.

This matters for the union tree (`queue.md` 2.C): a union built now would
inherit these boundaries, and some of them are artifacts of where the download
stopped rather than facts about the data.

## What the isolated 183,296 are

Not yet established, and worth not guessing. A seed was fetched because it
carried P2600, whether or not it had any family statement — so an isolated item
is either a person Wikidata records with no recorded relatives at all, or one
whose relatives simply were not downloaded. Those are very different, and the
dangling-reference count above cannot separate them because an item with *no*
relation statements produces no reference either way.
