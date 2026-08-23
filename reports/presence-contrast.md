# People imported far less than the people standing next to them

Emma's instrument, described 2026-08-22: *"this isn't to say people very central to
areas with only one export to them. It's just people central to areas with few exports
and, particularly, people who are starkly imported less than the people around them. If
there's a section in the medieval tree where there's a person born in the year 500 that
was imported exactly once and everybody around them was imported five times, they are an
example of this."*

Built by `scripts/build-presence-contrast.py` over 540 exports and 1,321,589 distinct
people. **Contrast** is the median presence of a person's graph neighbours minus their
own presence.

## Why this is a different question from density

`reports/density.md` ranks by *absolute* thinness and therefore cannot point at
antiquity — every export climbs into the shared ancient spine, so ancient people have
high presence and never look thin. Its seeds came out with a median birth year of 1805.

Contrast is *relative*. It finds people the balls stopped just short of: well-covered
neighbourhood, barely-covered person. **6,067 people born before 1600 sit two or more
exports below their own neighbourhood**, against three pre-1100 seeds that density
offered.

## What it found

| contrast | people |
| ---: | ---: |
| 2 | 15,967 |
| 3 | 4,619 |
| 4 | 2,532 |
| 5 | 1,147 |
| 6–9 | 1,332 |
| 10+ | 242 |

**25,839 people at contrast ≥ 2. 6,067 of them born before 1600, and 13,234 undated** —
and undated skews ancient in this corpus, so the ancient population is larger than the
dated count.

Pre-1600 by century, showing the instrument reaching where density could not:

    -200s 42 · -100s 56 · 0s 44 · 100s 43 · 200s 24 · 300s 34 · 400s 39
    500s 59 · 600s 53 · 700s 75 · 800s 210 · 900s 405 · 1000s 679
    1100s 917 · 1200s 834 · 1300s 786 · 1400s 775 · 1500s 950

## The head of the list is Roman

Of the top thirty pre-1600 by contrast, a clear plurality are Roman or late-antique —
`Rufius Festus` (260, seen 4 times among neighbours seen 21), `Anicius Acilius Glabrio
Faustus` (400, seen **once** among neighbours seen 16), `Tarrutenia` (405, once against
16), `Marcus Cocceius Nerva` (−5, once against 15), `Julia Caesaris` (−76, three against
16), `Juba` (−85, once against 16). Emma named the Roman neighbourhoods as one of the
three she thought had been missed; the instrument found them without being told to.

`reports/presence-contrast-ancient.tsv` is the 392 pre-1600 people at contrast ≥ 6, with
names, sorted by contrast then by how many neighbours the median rests on.

## The caveat that matters for picking seeds

**Most of the top rows have only two neighbours**, so their "median" is the midpoint of
two numbers and moves easily. A contrast of 17 computed over two neighbours is far weaker
evidence than a contrast of 13 over four. The TSV carries the neighbour count for exactly
this reason and the sort prefers more neighbours at equal contrast; the minimum is two,
because a single edge is not a neighbourhood.

## REFUTED, 2026-08-22, by the first probe

**Rufius Festus (260), contrast 17, returned 35 new people out of 5000 — 0.7%.**

That is an order of magnitude worse than the ancient *density* seeds in
`reports/sparse-ancient-exports-2026-08-22.md`, which ran 85–761, and those were
themselves thirteen times worse than the modern ones at 1,885–4,230.

**The premise was backwards.** This report argued that a well-covered neighbourhood
around a barely-covered person meant the balls had stopped just short and there was
structure behind them. The measurement says the opposite: the neighbourhood is
well-covered *because it has been exhausted*, and the low-presence person is a leaf
hanging off it rather than a doorway into anything.

**The instrument did do what it claimed** — all 7 dated new arrivals are ancient, median
birth −115, none after 100 AD, so contrast really does select ancient material. There is
simply none of it left in that region to collect.

Emma, on being shown it: *"Great I think this is settled. No more sparse area stuff."*

**This is the third seed-choosing method refuted by measurement**, after "small but
nonzero descent" and "the rim of a cut-off ball" in
`reports/descendants-backtest-2026-08-07.md`. It is also the second proposed on
reasoning alone, which is the thing `CLAUDE.md` warns against after the rim case. Do not
propose a fourth without a measurement behind it.

`scripts/build-presence-contrast.py` and the CSVs are kept because the measurement is
sound and the refutation is worth being able to reproduce. Do not seed exports from
them.
