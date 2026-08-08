# What eleven `Descendants` exports actually did

A backtest, not a proposal. `out/merged-134.ged` is the tree as it stood before
Emma's 2026-08-07 batch and `out/merged.ged` is the same tree with eleven
`Descendants` exports merged in, so for once there is a before and an after and
the question "was that a good seed?" has an answer rather than an argument.

Two methods for choosing seeds were tested against it. **Both failed**, and the
reason neither could have succeeded is the finding worth keeping.

## The batch

| | before | after | added |
| --- | ---: | ---: | ---: |
| people | 257,219 | 275,437 | **+18,218** |
| families | 129,348 | 137,764 | +8,416 |
| exports | 134 | 145 | +11 |

Eleven distinct seeds, all `Descendants` style, all exported 07 AUG 2026. Ten
came back holding 4,076 people and one holding 3,749.

## The campaign goal was not served

The `Descendants` campaign exists because **the tree is biased towards ancient
and medieval people and Emma is trying to reach modern times.** Against that
goal, this is what 18,218 new people bought:

| born | before | after | added |
| --- | ---: | ---: | ---: |
| 1000s | 4,787 | 4,825 | 38 |
| 1100s | 6,199 | 7,536 | 1,337 |
| 1200s | 6,824 | 7,364 | 540 |
| 1300s | 7,822 | 7,921 | 99 |
| 1400s | 7,262 | 8,177 | 915 |
| 1500s | 8,348 | 11,717 | **3,369** |
| 1600s | 17,746 | 20,791 | **3,045** |
| 1700s | 20,240 | 22,207 | 1,967 |
| 1800s | 21,702 | 21,803 | 101 |
| 1900s | 5,264 | 5,268 | **4** |
| 2000s | 13 | 13 | 0 |

**Four people born in the twentieth century.** The median new person was born in
**1582**; 105 of 18,218 were born in 1800 or later. The batch was a large and
successful piece of medieval genealogy and it moved the modern frontier by
essentially nothing.

## Why — and this is mechanical, not a matter of picking better seeds

A `Descendants` export is a **breadth-first ball with a budget of about 4,076
people.** Breadth-first means it fills generation *k* completely before starting
generation *k+1*, so the budget is spent on the generations nearest the seed. A
descent that branches even twice per couple reaches 4,096 people at generation
12 on its own — so a ball can carry roughly **a dozen generations, call it 350
years**, and no choice of seed changes that.

Every seed in this batch was ancient or undated. `Soeiro` was born 680. The rest
are medieval placeholders — `unknown grandfather`, `NN`, `wife of Guillaume,
Vicomte de Man`, `Wife of Tewdrig ap Teithfal`. From a seed in 1300, twelve
generations lands around 1660, which is exactly where the new people are.

The per-export ranges say the same thing. `new %` is how much of each 4,076-person
file was people we did not already hold:

| seed | new | new % | new people born | median |
| --- | ---: | ---: | --- | ---: |
| 6000000177955802827 | 4,055 | 99% | 1337–1748 | 1608 |
| 6000000227040553824 | 3,723 | 91% | 1470–1858 | 1675 |
| 6000000227086380915 | 3,621 | 89% | 1350–1676 | 1531 |
| 6000000227086506866 | 2,294 | 56% | 1027–1350 | 1175 |
| 6000000227039926826 | 2,119 | 52% | 1365–1927 | 1530 |
| 6000000227040338177 | 1,623 | 40% | 1679–1837 | 1734 |
| 6000000210457327856 | 486 | 12% | 1273–1390 | 1320 |
| 6000000210455376824 | 421 | 10% | 1273–1363 | 1316 |
| 6000000227040613855 | 272 | 7% | 1285–1940 | 1521 |
| 6000000210387665830 | 72 | 2% | 1280–1481 | 1405 |
| 6000000226989731860 | 3 | 0% | no dates | — |

Note the spread in yield: the best export was 99% new material, three were under
10%, and one returned **three** people we did not have. Same style, same day,
same budget — so seed choice is worth a great deal, just not for reaching
forward in time.

## Method 1: "small but nonzero descent" — refuted

`reports/descendants.md` ranks people whose recorded descent is small but not
zero, on the argument that the line demonstrably continues and we have barely
followed it. Its candidate band is 1–20 descent paths.

**Every one of the ten seeds that already existed in the tree had exactly one
recorded child — and descent-path counts far outside that band:**

| seed | name | paths before |
| --- | --- | ---: |
| 6000000226989731860 | unknown grandfather | 1,509,799,971 |
| 6000000210387665830 | Soeiro | 83,236,169 |
| 6000000210455376824 | Chinu no Ōkimi | 350,365 |
| 6000000210457327856 | Agata no Inukai no Michiyo | 260,997 |
| 6000000227086506866 | Wife of Tewdrig ap Teithfal | 32,337 |
| 6000000227039926826 | NN | 11,063 |
| 6000000227040613855 | Nobutaka | 10,535 |
| 6000000227040338177 | RODRIGO | 3,471 |
| 6000000227086380915 | wife of Guillaume, Vicomte de Man | 472 |
| 6000000227040553824 | João | 371 |

The report would not have proposed a single one of them. They are people with
**one recorded child sitting on top of an enormous descent** — the opposite
shape to the one it looks for. Whatever produced 18,218 people, this method
cannot find it.

It also shows the path count is only meaningful near the leaves. A billion
descent paths is a real count of a real quantity and it is useless as a ranking
key.

## Method 2: "the rim of a cut-off ball" — also refuted

Proposed here and tested here. The argument: an export that came back at the
size bound was **cut off, not finished**, so a childless person inside it may be
childless only because the walk stopped. Nine of the 134 pre-batch exports were
at or within 8 of the largest, and 20,313 childless people sat in one.

If the argument held, those people should gain children faster than everyone
else when new exports land. They did not:

| group — all childless before the batch | people | gained a child | rate |
| --- | ---: | ---: | ---: |
| everyone childless | 133,963 | 1,338 | **1.00%** |
| on the rim of ≥1 cut-off export | 20,313 | 145 | **0.71%** |
| on exactly 2 cut-off exports | 482 | 0 | 0.00% |
| on no cut-off export's rim | 113,650 | 1,193 | **1.05%** |

Rim membership **anti-predicts**. The honest caveat is that this is an indirect
test — the batch was seeded on ancient people and had no particular reason to
land on other balls' rims — so it refutes "rim people are systematically
under-recorded" rather than "seeding at a rim would work". It is not evidence
for the method either way, and the method was going to be presented as an
improvement on the strength of its reasoning alone. It is not one.

## What did predict nothing at all

**No person born in 1800 or later gained a child from this batch. Not one, of
14,371.** Neither on a rim nor off it. That is the same mechanical fact from a
different angle: these exports never went near the modern part of the tree.

## What follows

**Seed where you want to arrive.** A ball reaches roughly a dozen generations
forward, so an export that is to deliver people born after 1900 has to be seeded
on somebody born after about 1550, and realistically after 1750 — a wide descent
exhausts the budget much sooner than a narrow one. No ranking heuristic applied
to medieval people can substitute for this, which is why both methods above
failed: they were choosing among seeds that could not reach the target whichever
one was picked.

That is a constraint rather than a method, and it is the part supported by
evidence. The candidate list built on it is in `reports/descendants.md`, whose
1750–1899 bands are the ones that matter for the campaign — and which remains
**unvalidated**, exactly like the two methods above were before this batch
tested them. The way to test it is the way this was tested: take an export, then
diff the tree.

## Reproducing

`out/merged-134.ged` is the pre-batch tree, kept out of git for its size; it is
regenerable by merging every export except `exports/descendants/`. The scripts
that produced these numbers are one-offs against those two files.
