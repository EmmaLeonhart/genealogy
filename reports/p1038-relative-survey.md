# `P1038` *relative* in the local store — measured, not assumed

Emma, 2026-08-25, after ranking parents / spouses / children / siblings: *"there are other relationships there that are sometimes reported on Wikidata, like the relative role"*. The instruction attached to it was to **measure how much exists before building anything on it**. This is that measurement and nothing is built.

**The store is a Geni-shaped slice** — 2,247,041 lines read from the shards, seeded from `P2600` holders and their neighbours. Every number below is about that slice, never about Wikidata as a whole.

**Cross-checked against `out/wikidata/store-index.sqlite3`**, which holds 2,246,827 distinct QIDs against the 2,247,041 lines scanned — a difference of 214. The two agreeing to five significant figures is what makes the scan believable; one that had silently stopped early would not.

| | |
| --- | ---: |
| items scanned | 2,247,041 |
| items carrying `P1038` *relative* | **26,724** |
| of those, every statement DEPRECATED and so absent below | 15 |
| `P1038` statements, deprecated ones dropped | 49,974 |
| statements with no `P1039` *kinship to subject* | **3,651** |

## What the kinship qualifier says

| kinship | statements |
| --- | ---: |
| `Q76557` *uncle* | 2,803 |
| `Q9238344` *grandfather* | 2,603 |
| `Q15224724` *nephew* | 2,567 |
| `Q11921506` *grandson* | 2,151 |
| `Q3752578` *son-in-law* | 2,090 |
| `Q2914212` *brother-in-law* | 1,916 |
| `Q61740757` *adoptive father* | 1,716 |
| `Q20746725` *adopted son* | 1,590 |
| `Q31819505` *male first cousin* | 1,561 |
| `Q13204680` *father-in-law* | 1,320 |
| `Q23009870` *cousin* | 1,104 |
| `Q12158205` *father's brother* | 1,058 |
| `Q3403377` *niece* | 1,052 |
| `Q19756330` *granddaughter* | 1,019 |
| `Q76507` *aunt* | 842 |
| `Q2500621` *great-grandfather* | 807 |
| `Q19682162` *paternal grandfather* | 764 |
| `Q3238556` *sister-in-law* | 702 |
| `Q4346792` *stepson* | 692 |
| `Q4994791` *maternal grandfather* | 646 |
| `Q19822354` *stepdaughter* | 641 |
| `Q9235758` *grandmother* | 636 |
| `Q12160962` *wife's father* | 615 |
| `Q12051531` *female first cousin* | 610 |
| `Q23045211` *fraternal nephew* | 595 |
| `Q4120409` *mother's brother* | 590 |
| `Q19680017` *great-grandson* | 577 |
| `Q19595226` *paternal half-brother* | 564 |
| `Q19595228` *paternal half-sister* | 505 |
| `Q20746728` *adopted daughter* | 492 |
| … and 294 further values | |

## The part that is worth anything: what our own tree CANNOT derive

*uncle*, *grandfather*, *nephew*, *grandson* and *cousin* all follow from parent and child edges the merged tree already holds — recording them adds nothing a walk would not produce. The in-law, step-, adoptive, foster and godparent kinships do **not** follow from any edge in a GEDCOM, so they are the slice with information in it.

| | statements | share |
| --- | ---: | ---: |
| derivable from parent/child edges | 32,938 | 71% |
| **not derivable — in-law, step, adoptive, foster, godparent** | **13,708** | 29% |

The largest of the non-derivable kinds: `Q3752578` *son-in-law* 2,090, `Q2914212` *brother-in-law* 1,916, `Q61740757` *adoptive father* 1,716, `Q20746725` *adopted son* 1,590, `Q13204680` *father-in-law* 1,320.

**That split is a keyword rule over the English label**, not a claim about Wikidata's ontology — `in-law`, `step`, `adopt`, `foster`, `god…` against everything else, over 324 distinct kinship values. It is good enough to answer *is there anything here* and should not be relied on further.

`reports/p1038-relative.tsv` is every one of the 49,974 statements, one per row.
