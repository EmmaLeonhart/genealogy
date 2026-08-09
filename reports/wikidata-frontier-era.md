# Where the download's frontier is, in time — 2026-08-08

Measured offline over `wikidata/items/`, at 1,127 shards and ~1.12M items
stored. No Wikidata query was made; every number here comes from items already
downloaded.

Written to test Emma's hypothesis, in her words: *children naturally get really
big but fall off hard once you reach the 21st century, and we are at the point
where likely we have exhausted the first major children wave.*

Shards are appended in fetch order, so **shard index is walk order** — comparing
the oldest shards against the newest is comparing the start of the walk against
its current frontier.

## The walk has marched into modern times

Twelve shards sampled evenly across the store.

| shard | dated | median birth year | ≥1900 | ≥1950 |
| --- | --- | --- | --- | --- |
| 00000 | 87% | 1788 | 10% | 1% |
| 00205 | 99% | 1862 | 26% | 5% |
| 00512 | 87% | 1768 | 7% | 0% |
| 00717 | 73% | 1880 | 36% | 12% |
| 00921 | 65% | 1870 | 41% | 23% |
| 01024 | 53% | 1920 | 62% | 34% |
| 01126 | 46% | 1926 | 59% | 37% |

Not monotone — shard 00512 sits at 1768 — but the direction over the whole run
is not in doubt, and the last two shards are the only ones with a median in the
twentieth century.

## Child fan-out by birth era

Children (P40 statements) per item, by the person's own birth era, computed
separately for three positions in the walk. The point of splitting it is that a
single pooled table would confound "the walk reached later people" with "later
people have fewer recorded children".

| born | oldest 4 shards | middle 4 | newest 4 |
| --- | --- | --- | --- |
| pre-1500 | 2.40 | 2.18 | 1.56 |
| 1600–1649 | 2.80 | 1.29 | 1.42 |
| 1700–1749 | 1.38 | 1.52 | 0.94 |
| 1750–1799 | 1.43 | 1.64 | 1.83 |
| 1800–1849 | 1.12 | 1.17 | 1.12 |
| 1850–1899 | 0.56 | 0.68 | 0.88 |
| 1900–1949 | 0.41 | 0.46 | 1.15 |
| 1950–1999 | 0.27 | 0.44 | 0.51 |
| 2000–2049 | — | — | **0.00** (89 items) |

The era effect holds in all three groups and is large: roughly 2.2 for the
pre-1500 population against 0.3–0.5 for those born after 1950, and **zero** for
the 89 sampled people born after 2000, none of whom has a recorded child.

**Part of this is Wikidata's recording practice, not demography.** Living
people's children are recorded far less often, for notability and privacy
reasons both. That distinction matters for any later claim about the *content*
of the tree; it does not matter for the walk, whose fan-out is governed by what
is recorded either way.

## The part that does not yet support "exhausted"

The frontier is increasingly **undated**: 18% of the oldest shards carry no
P569, against **53% of the newest**. The era table above therefore governs less
than half of what the walk is currently fetching, and the undated half still
fans out:

| group | undated items | children/item | all relation edges/item | claims/item |
| --- | --- | --- | --- | --- |
| oldest 4 | 707 | 1.53 | 3.11 | 8.3 |
| middle 4 | 858 | 1.13 | 3.07 | 7.3 |
| newest 4 | 1,840 | **1.05** | 2.49 | 6.9 |

1.05 children per undated frontier item is twice the rate of the dated
1950–1999 population. Everything is thinning — relation edges per item down from
3.11 to 2.49, claims per item from 8.3 to 6.9 — but the undated half is thinning
much more slowly than the modern dated tail.

## The prediction this makes

If the hypothesis is right, discovery per fetched item keeps sliding from its
current 0.73 and the queue drain accelerates past 28,000/hour. If it flattens
instead, the undated frontier is why, and the question becomes what those
undated items are — which is answerable from the store and is not answered here.

## Which edge drives the frontier — P40, not P3373

Separate sample, 8 shards spread across the store, 7,050 items. A target counts
as frontier if it is outside the 514,822-QID P2600 seed set; "sole" counts
targets that no other relation property on the sampled items also names.

| prop | label | edges | per item | distinct off-seed | sole |
| --- | --- | --- | --- | --- | --- |
| P40 | child | 8,253 | 1.17 | 4,195 | **3,580** |
| P22 | father | 4,717 | 0.67 | 2,116 | 1,880 |
| P25 | mother | 3,571 | 0.51 | 1,797 | 1,576 |
| P26 | spouse | 2,194 | 0.31 | 1,452 | 1,211 |
| P3373 | sibling | 3,472 | 0.49 | 1,003 | **649** |

P3373 was the suspect when the frontier first looked larger than `todo.md`
§ 8a-revised expected, on the grounds that sibling edges fan sideways without
advancing a generation. **That was wrong and this measures it**: sibling
accounts for 649 of 9,717 distinct off-seed targets, 6.7%, and its 3,472 edges
collapse to only 1,003 distinct targets — a 3.5:1 redundancy, because siblings
name each other and are mostly reachable anyway as co-children through P22/P25.
It is as cheap as the comment above `RELATION_PROPERTIES` claims.

P40 is the fan-out: 37% of the frontier, more than father and mother combined,
and it compounds generationally. It is also the direction the exercise is aimed
at, since people Wikidata holds and Geni does not are disproportionately
descendants no export reached.

## Caveats

- All figures are samples of 1,000-item shards, not the whole store. Distinctness
  in the edge table is measured **within the sample**, so its 1.38 off-seed
  targets per item overstates what the live walk sees (0.88 at the time).
- Shard index is walk order, not time order in the genealogy, and the walk
  revisits eras — shard 00512's median of 1768 is the visible proof.
- Scripts for all three tables were run from the session scratchpad and are not
  committed. Each is a short read over `wikidata/items/` and the numbers above
  are what they printed.
