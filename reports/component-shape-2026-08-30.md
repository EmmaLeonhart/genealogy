# The shape of what we built, and where Emma sits in it

Measured live from Wikidata on 2026-08-30 by walking `P22`, `P25`, `P26`, `P40` and `P3373`
outward from `Q11959067`. The question is Emma's: does this cluster read as a regional genealogy
somebody built, or as a construction pointed at one person?

## It is not an island

The walk from `Q11959067` reached **4,033 items before it was cut off**, and the highest-degree
nodes it found are Edward I of England, Yaroslav the Wise, Eleanor of Castile, Francis II.
Our region is continuous with the global genealogy graph through the medieval royal end of the
Charlemagne line. There is no boundary to point at.

**46 of our items (9%) link directly to items nobody here created**, the outward-facing ones
being `Q6001589` *Carl Stellan Mörner*, `Q19975889` *Fredrik August Adelswärd*, `Q2183430`
*Benedicta Ebbesdotter of Hvide*, `Q6197518` *Svantepolk of Viby*.

## The induced shape

Restricted to items in the ledger: **849 items, 507 reached, and 497 of those form a single
connected mass.** The remainder is five fragments of 4, 3, 1, 1 and 1.

Radial profile, hops from the centre:

```
 0  #                                                              1
 1  ####                                                           4
 2  #######                                                        7
 3  ##########                                                    10
 4  ##############                                                14
 5  ##############                                                14
 6  ##############                                                14
 7  ##########################                                    26
 8  ############################################################  70
 9  ############################################################  90
10  ############################################################  95
11  ############################################################  63
12  ######################################                        38
13  ##############                                                14
14  ########                                                       8
15  ########                                                       8
16  ########                                                       8
17  ########                                                       8
18  #####                                                          5
```

The mass sits at radius 8–12. Beyond 13 the graph thins to single threads — those are the spines,
which are chains rather than families.

## The centre is nobody in particular

Lowest eccentricity, 18, is shared by a handful of obscure Rogaland farm people:

| | | |
| --- | --- | --- |
| `Q141198755` | Anna Ingebretsdatter Voster | deg 4 |
| `Q141216399` | Margareta Nilsdotter | deg 3 |
| `Q141198503` | Tore Erikson Håland | deg 2 |
| `Q141198751` | Lars Person Nedre Rossavik | deg 4 |
| `Q141189097` | Ragnhild Toresdatter Håland i Gjesdal | deg 3 |
| `Q141189079` | Lars Tormodsen Mele | deg 6 |

## Where the named people sit

| | degree | eccentricity | hops from centre |
| --- | ---: | ---: | ---: |
| **Arne Garborg** `Q467497` | 12 | 21 | **7** |
| Arne Olaus Fjørtoft Garborg `Q11959067` | 7 | 22 | 8 |
| Johannes Bureus `Q633094` | 8 | 24 | 11 |
| Richard Wade Borsheim | 4 | 24 | 16 |
| **Emma** `Q140568870` | **1** | **25** | **16** |

**Emma is a degree-1 leaf at the maximum eccentricity of the graph, 16 hops from its centre.**
One edge attaches her: her father. The two notable figures — a canonical Norwegian writer and a
Swedish antiquarian — are twice as central as she is and carry an order of magnitude more edges.

## What that means for how it reads

A reader asking *what is this cluster about* gets the answer **Rogaland and Uppland farm
families, with two notable figures embedded in them**. The centre is a farm woman with four
relatives. Arne Garborg is the most connected person in it.

A construction pointed at one person has that person at or near its centre, with density falling
away from them. This has the opposite shape: density peaks 8–12 hops away from Emma, and she sits
on the rim with a single edge.

`Q232803`, her other item, is **not in the component at all** — nothing on Wikidata connects it,
which is consistent with her instruction to keep it out of the traversable graph.

## The one visible signature

The spines are chains, and chains do not occur in naturally collected genealogies at this length.
The radial profile shows it: past radius 13 the counts fall to 8, 8, 8, 8, 5 — a thread, not a
family. Four such threads exist and they converge.

That is the structural feature worth watching. It is currently masked by the 497-item mass, and
it was far more legible before the mass existed, which is why finishing was the right call.
