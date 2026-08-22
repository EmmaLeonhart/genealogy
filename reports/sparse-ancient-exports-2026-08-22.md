# Did the ancient sparse-region exports expand the tree?

Asked by Emma, 2026-08-22. Ten `Forest`/5000 exports ran that afternoon: five seeded
on the top sparse regions from `reports/density.md`, four on ancient seeds, one
`Descendants` that was hers and is excluded from the comparison.

**Baseline: 526 exports, 1,294,667 distinct people.** "New" means a Geni ID in none
of them.

| seed | born | new people | born <1100 | born <1600 | median birth of new |
| --- | ---: | ---: | ---: | ---: | ---: |
| Buhl region | 1847 | 3,873 | 1 | 15 | 1848 |
| Bates region | 1750 | 4,230 | 0 | 38 | 1792 |
| Andrews region | 1833 | 4,022 | 0 | 16 | 1821 |
| Lundgreen region | — | 2,862 | 0 | 0 | 1860 |
| Caracciolo region | — | 1,885 | 0 | 137 | 1651 |
| Fujiwara no Fuhito | 659 | 85 | 0 | 2 | 1162 |
| Magnus Maximus substitute | 340 | 222 | 119 | 133 | 1013 |
| Xue Jin 薛謹, Hedong | 401 | 761 | 68 | 68 | 729 |
| Ingina substitute (de Neustrie) | 680 | 237 | 127 | 129 | 965 |

**Five modern seeds: 16,872 new, one of them born before 1100.
Four ancient seeds: 1,305 new, 314 of them born before 1100.**

## The answer

**No, not in volume.** An ancient ball returns about a thirteenth of what a modern
one does — 326 new people on average against 3,374. Emma predicted this before the
run: *"the main spine is pretty much already there"*. A `Forest` ball seeded in
antiquity spends its 5000 slots re-walking people 526 previous exports already
reached.

**Yes, in reach, and nothing else gets there.** 314 people born before 1100 against
1 from the entire modern set. If the goal is stragglers of the ancient spine rather
than tree size, the ancient exports are the only instrument that works and the
volume comparison is measuring the wrong thing.

**File size is not yield.** The Ingina ball is 11.6 MB and holds 237 new people; the
Bates ball is 1.8 MB and holds 4,230. Ancient profiles carry long `about_me` text, so
size tracks how well-documented a neighbourhood is, not how much of it is new.

## Two things this run established about the loop

**Geni exports only from a profile the account manages.** `/gedcom/export/<id>` on
an existing profile Emma merely found redirects to `/error`. That is why the
placeholder technique in `docs/export-seed-rules.md` exists, and it means a density
seed can never be exported from directly — a placeholder at an open slot beside it
is mandatory, not a convenience.

**Ancient European seeds are frequently locked.** Magnus Maximus (340) and Ingina
(680) both render their parent slots grey rather than as *Add father* / *Add mother*,
which is the master-profile shape from a Basic account. Emma supplied a nearby
unlocked profile for each; both then worked. Expect this on curated World Tree
figures and expect to need a substitute one or two hops away.

## What is not established

Whether the 314 are worth the four exports is Emma's call, not a measurement. And
this compares four ancient seeds against five modern ones — enough to show the
direction, not enough to put a number on the ratio.
