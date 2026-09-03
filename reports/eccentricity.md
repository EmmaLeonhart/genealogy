# The most eccentric people in the synoptic tree

**Emma, 2026-09-03:** *"George RR Martin is interesting due to his eccentricity… Might be worth
measuring the most eccentric people in the synoptic tree."*

`scripts/measure-eccentricity.py` → **`reports/tree-eccentricity.csv`**, one row per person, all
**1,451,964** of them. The graph is parent, child and spouse edges from
`reports/derived-family.csv`, undirected: **2,537,928 edges**. Geni records no sibling edge, so
none is added — siblings are two hops through a shared parent.

## Two different numbers have been called eccentricity here

| column | what it is |
| --- | --- |
| `dist_charlemagne` | hops to Charlemagne, **the centre** — his own centrality is why the path campaign anchors on him |
| `ecc_lower_bound` | graph eccentricity proper: the greatest distance to anyone. Exact needs a BFS per person (1.45M runs); this is an 8-landmark lower bound, chosen by double sweep, and never over-states |

**Diameter is at least 318 hops.** Eight landmarks all agree on 318, so the bound is tight.

## Shape of the tree

**547 components. The largest holds 1,450,615 — 99.91%.** The other 1,349 people are spread
across 546 components, largest 250. Per `CLAUDE.md` § *A small component is IGNORED*, they are
counted here and nothing else.

Charlemagne reaches **every one** of the 1,450,615.

| | hops to Charlemagne |
| --- | ---: |
| p1 | 13 |
| p25 | 30 |
| **median** | **34** |
| p75 | 38 |
| p90 | 44 |
| p99 | 63 |
| max | **183** |

Degree: median **2**, max 179 (Charlemagne is 31). **163,594 people — 11.3% — have exactly one
recorded relationship.**

## The far edge is the Chinese legendary lineage

The most distant people from Charlemagne are a consecutive descent, which is why their distances
run 177, 178, 179 …:

| hops | person |
| ---: | --- |
| 183 | 少昊 Shaohao |
| 182 | 顓頊 Zhuanxu |
| 181 | 女修 Nüxiu |
| 180 | 大業 Daye |
| 179 | 皋陶 Gaoyao |
| 178 | 伯益 Bo Yi |

This is a real structural fact rather than an artefact: it is the far end of the tree from
Europe. But note what it means — **distance from Charlemagne measures distance from the European
centre**, and its extreme is a different genealogical tradition that happens to be densely
recorded, not a thin or fragile connection.

**Among the 43,667 people who carry a QID, the most distant are the Samaritan high priests** —
`Q107534557`, `Q2164896`, `Q108907045` and their line, 131–134 hops out. That is Emma's own
hand-built tree sitting at the far edge.

## George R.R. Martin is NOT extreme on either measure here

| | hops to Charlemagne | percentile | ecc bound | percentile | degree |
| --- | ---: | ---: | ---: | ---: | ---: |
| **George R.R. Martin** | 40 | p80 | 208 | p83 | 6 |
| **Robert Ettinger** | 39 | p76 | 210 | p89 | 6 |
| Charlemagne | 0 | — | 183 | — | 31 |

Both sit modestly outside the middle and nowhere near the edge, where the numbers run to 183 and
318.

**That does not contradict her read of Martin — it locates it.** His eccentricity is a property
of **Geni's World Tree**, where a relationship query has to cross the sparse part of the graph
and can time out. Our corpus is a sample of Geni, and someone we happen to have sampled well
looks central here while being eccentric there. `CLAUDE.md` § *Presence measures our sampling,
never Geni's content* is the standing form of this, and it is the reason a Geni-side measure and
a tree-side measure cannot be substituted for each other.

**So this file does not answer "who will Geni time out on".** It answers who is far from the
centre of what we hold. The two questions coincide only where our sampling is even, and the
Samaritan and Chinese results above are exactly where it is not.

## Eccentricity is PARTLY A RECENCY MEASURE, and that qualifies everything above

**Emma, 2026-09-03, on Ettinger:** *"I think Ettinger is high in eccentricity because of the fact
that he… I only recently added him, basically."*

She is right that this is the mechanism, and it is checkable. Over the **602** exports in the
corpus:

| person | exports containing them | hops from Charlemagne |
| --- | ---: | ---: |
| Robert Ettinger | **4** | 39 |
| 少昊 Shaohao | **1** | 183 |

A person reached by one export sits wherever that single export left them. Expanding around them
pulls them inward, so a high score can mean *we have not sampled here yet* rather than *this
person is structurally peripheral*. Two people is not a measurement of the correlation, and it is
not offered as one — the full version is a presence count per person from `genimerge.density`
against this file, which has not been run.

**So the ranking answers "where has our sampling not reached", which is close to but not the same
as "who is on the edge of the graph".** For the campaign that distinction mostly does not matter,
since both point at the same next export. For calling someone eccentric it matters a lot.

## What is here to build on

`dist_charlemagne` combined with `degree` is the closest thing in our own data to thin
attachment: 163,594 people hold a single relationship, and the ones far from the centre are
where a `Forest` export at an eccentric point would land. Nothing is proposed on that here —
`CLAUDE.md` records two seed-choosing methods already refuted by measurement, and a third on
reasoning alone is what that section forbids.

## A defect caught in the first run, and how

`degree` came out doubled, because every relationship is listed on **both** people's rows — a
father on the child's `father`, the child on the father's `children`. BFS distances are
unaffected, since a repeated neighbour is revisited and skipped, which is what made it easy to
miss. The tell was **0 people with degree 1** in a tree of 1.45 million, which cannot be true.
Deduping gives 163,594. Same family as `CLAUDE.md` § *Our side could never have two children*: a
distribution that is too clean is about the instrument.
