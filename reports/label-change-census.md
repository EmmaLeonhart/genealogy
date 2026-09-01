# How many Geni labels actually need changing?

Her queue item, answered 2026-09-01 over `reports/derived-labels.csv` (1,451,964 people).

| | people |
| --- | ---: |
| no Wikidata item — nothing to change | 1,408,284 |
| **has an item** | **43,680** |
|   · our `en` DIFFERS from theirs | 29,743 |
|   · our `en` already matches | 11,155 |
|   · **the item has NO label — ours is an ADDITION** | **1,590** |
|   · no `en` on the item but a `mul` | 682 |
|   · we have no label to offer | 510 |

## The number that matters is 1,590, not 29,743

`CLAUDE.md` § *The purpose is to ADD to Wikidata, not to correct it* governs, and it is emphatic:
*"Correcting stuff on Wikidata is actually such a pain that it's almost effectively out of the
question."* A differing label is a **note**, not a work item.

So the 29,743 differences are not a backlog. **1,590 items carry no label at all and we have one**
— that is the addable population, and it is 3.6% of the items we touch.

**A difference is also not evidence that ours is better.** These items were largely labelled by
other editors from other sources; `CLAUDE.md` § *Emma edits the tree and the items BY HAND* adds
that some of the differences are her own corrections, where the stale half is ours. Nothing here
should be read as 29,743 wrong labels on Wikidata.

## What this does not count

Labels in `ja`, `zh`, `ko` and `mul`, which are overwhelmingly **additions** rather than changes —
`reports/wikidata-placeholder-labels.json` alone is 158,618 `set_label` edits, and the CJK ones
land on items that have no CJK label at all.
