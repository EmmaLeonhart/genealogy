# Do any close living relatives have a publication record?

**Emma's item, 2026-08-18:** *"Yeah can you actually search for this stuff?"*

**Answer: no. Not one of the 53.** OpenAlex, every living person inside eight hops.

## What was searched

The 53 people within eight hops born 1930 or later with no death year — the set from
`reports/eight-hop-search.md`, which is everyone in the corpus who could plausibly be
alive and is close enough to matter. Each name went to
`api.openalex.org/authors?search=`, and any author with **three or more works** was
inspected by hand.

**Four names returned an author. All four are other people.**

| name | hops | matched | why it is not them |
| --- | ---: | --- | --- |
| Karin Buchanan, b. 1982 | 8 | Karin M. Buchanan, Royal University Hospital, 3 works / 144 cites | **Published 1999–2000.** Our Karin was seventeen. Ruled out on dates, despite the institution sitting in Saskatchewan near the family's Birch Hills branch — which is exactly the coincidence that would have sold it |
| Robert Henry, b. 1934 | 8 | Robert R. Henry; Robert J Henry, Queensland | One of the commonest name pairs in English |
| Kirsten Judith, b. 1934 | 8 | Kirsten J. Koymans | Our record has **no surname**, so the search matched a given name |
| Bjørg, b. 1947 | 8 | Bjørg N. Cyvin; Bjørg Egelandsdal | Same — `Bjørg` alone is a given name |

**The other 49 returned nothing with three or more works**, including every one of the
nearest: Richard Wade Borsheim (1 hop), Jared Borsheim (2), Stephen and Heidi Joan
Borsheim (3), Ilene Hoknes, Barney Borsheim, Floyd Olaf Hoknes (4), Milton Francis Schwan
and Heather Heppner (5), Henry Stangeland and the three young Schwans (6), the nine
Stangelands and three Holbirds (7).

## Three reasons this no is weaker than it looks

**1 · OpenAlex indexes academic publishing and nothing else.** A relative notable as an
author of books, a journalist, a politician, an athlete or a musician would not appear
here at all. This search answers *is anyone an academic*, which is narrower than *is
anyone notable* — it was chosen because Emma's own framing is that **publications are the
cheapest route to Wikidata notability**, not because it is the only route.

**2 · Married names hide women.** Several of the 53 are recorded under a maiden name and
several under a married one. Anyone publishing under the other name is invisible to a
name search, and this family changes surnames on marriage as a rule.

**3 · The corpus is thinnest exactly where living people are, and that is the real
limit.** 1,015 people sit within eight hops; only **53** have a birth year of 1930 or
later and no death date. The rest are undated, unnamed, or `NN` — which is what a Geni
tree looks like near the living, because nobody exports them. **So no candidate is partly
no data.**

## What this means for the objective

Emma's goal is a relative close enough to be worth **creating** an item for. On this
evidence there is no such person inside eight hops, and the standing best remains
**Jonas Salte at 8 hops** — whose item already exists and who died in 1944, so he
shortens the measured chain without advancing the objective at all.

**What would change the answer, in order of cost:**

1. **Emma naming relatives she knows publish.** She knows her own family; this search
   knows 53 names and no context. One name from her beats another sweep.
2. **Exports seeded on the living generations**, which would populate the part of the
   tree this search found empty. That is the other session's job and not this branch's.
3. **A wider notability search** — books, news, public office — for the same 53, if
   academic publishing is not the only route she will accept.
