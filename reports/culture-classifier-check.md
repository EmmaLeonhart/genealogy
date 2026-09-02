# The CJK culture classifier, checked against Wikidata

**Why this was run.** Her ruling of 2026-09-01 was *"Do both, kana agentically"* — `ko` by rule
and `P1814` *name in kana* read by hand. Scoping the kana half turned into a check of the thing
underneath it, because kana readings only make sense for people the classifier calls Japanese.

## `P1814` has nothing to emit today, and that is the finding

| | people |
| --- | ---: |
| carry kana in their Geni name | 294 |
| …and have a Wikidata item | **2** — and both are Japanese *labels of foreign people*, `Q134128` Cnut the Great and `Q720` Genghis Khan |
| classified Japanese by the tree | 226 |
| …and have a Wikidata item | **2**, and **both are misclassified** |

`P1814` attaches to an item. **No correctly-identified Japanese person in this corpus has one**,
so the property has an empty population until those 226 are created. That is a sequencing fact,
not a difficulty — `CLAUDE.md` § *The batches are a SEQUENCE*: what cannot run today is
tomorrow's batch.

## The two `ja` people with items are both Chinese

    Q77895       傑 愛新覺羅        ours: Masaru    — 愛新覺羅 is Aisin Gioro, the Manchu Qing house
    Q10511648    整 公齊 東海蘭陵    ours: Tadashi   — 東海蘭陵 蕭 is the Xiao of Lanling, Chinese

Both were reached by `graph traversal, 2 hop(s)`. The method is the right one — `CLAUDE.md`
§ *"Is X present?"* says **do not guess culture from the name; the tree settles it** — but the
propagation runs to **eight hops**, and two is already enough to cross from a Japanese
neighbourhood into a Manchu or Chinese one through a marriage.

## The `zh` side is 93%, and its errors have the same shape

120 romanised people with a QID, sampled at random, our romanisation checked against Wikidata's
own `en` label:

| | people |
| --- | ---: |
| our romanisation appears in their `en` label | **109** |
| differs | 8 |
| item has no `en` label to check against | 3 |

**Of the eight, at most three are our error, and they are all the same error:**

    Q45512272   榮 鄭州榮澤    ours: Ei        Wikidata: Zheng Rong
    Q11597736   榮定 扶風平陵   ours: Ei Ding   Wikidata: Dou Rongding

`Ei` is the **Japanese** reading of 榮; the Chinese is *Róng*. So a Japanese reading was applied
to a person the classifier itself calls Chinese — the leak running the other way.

**The rest are not our error.** `Q7488` and `Q698909` differ because Wikidata uses a *title* where
we use a name (*Emperor Qinzong of Song*, *King Wen of Zhou* — whose given name genuinely was 昌
Chang). `Q45600318` is *Jun* against *Xun* for 濬, both defensible readings.

## What to do about it is hers

Shortening the propagation would cut the 226 and the leak together, but the hop count is not
obviously the right dial — a long chain inside one genuinely Japanese family is exactly what the
traversal is for. **What is measurable is that the clan seat already contradicts it**: three of
the eight carry `鄭州榮澤`, `扶風平陵`, `京兆長安` — Chinese commanderies, recorded on the person,
and stronger evidence than a two-hop walk. Using the seat to *veto* a Japanese classification
costs nothing and needs no threshold.

## Correction, 2026-09-01 — the propagation conclusion rested on n=2

**What this report concluded** was that the walk *"runs to eight hops, and two is already enough to
cross from a Japanese neighbourhood into a Manchu or Chinese one through a marriage"* — inferred
from the **two** classified-Japanese people who have a Wikidata item, both misclassified.

**Two is not a basis for a claim about the walk.** Emma, 2026-09-01: *"please don't make
generalizations on the entire dataset with small test sections, because the dataset is extremely
heterogeneous."* Measured over the whole output of `reports/cjk-romanisation.csv` instead:

| | |
| --- | ---: |
| people the classifier covers | **13,638** — 13,416 `zh`, 222 `ja` |
| settled by graph traversal | **7,150** |
| settled by a clan seat, a place, a name form or a derived surname | 6,488 |

**Where the walk actually settles, and it is not near:**

| hops | settled | cumulative |
| ---: | ---: | ---: |
| 1 | 1,574 | 22.0% |
| 2 | 1,089 | 37.2% |
| 3 | 855 | 49.2% |
| 5 | 482 | 64.9% |
| 8 | 263 | 78.4% |
| 14 | 218 | 100.0% |

**So capping the walk at two hops would unsettle 63% of everyone it settles** — 4,487 people — to
answer a defect seen twice. `MAX_HOPS` is **14**, not the eight this report said, and a comment
beside it still says "six-hop"; both were stale.

**The real finding is scope, not hops.** The classifier covers **13,638** people while **47,296**
distinct people carry Han in a name — so **33,658 Han-named people are never classified at all**.
For `P1814` that matters more than the misclassification rate: the property's population is not
"the 226 once they are created", it is however many of those 47,296 turn out Japanese, and most of
them have never been put to the classifier.

**Nothing is changed in the classifier on this evidence.** A hop cap needs a measured error rate by
hop distance, which needs more than two checkable people; that is the experiment to run, not a
threshold to pick.
