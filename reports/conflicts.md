# Where Geni and Wikidata disagree — the 930 conflicts, characterised

Queue item 2.D, first half. Emma reframed 2.D from matching accuracy to **source
reliability**: measure Geni against Wikidata *per property*, assume no global
winner, and turn the result into a merge rule the code can apply. This is the
measurement step. **It does not adjudicate and names no winner.**

Full data: `reports/conflicts.tsv`, one row per disagreement, all 930 — the
crosscheck report lists only the worst 100, which is right for reading and
useless for measuring. Regenerate with `python scripts/build-conflicts.py`.
Offline: the store, the P2600 map and `out/merged.ged`.

Population: every `CONFLICT` over the **14,157** people linked by an exact
P2600. Both sides state the fact and the values differ.

## The shape

| property | conflicts | Wikidata's value is sourced | unsourced |
| --- | ---: | ---: | ---: |
| P569 date of birth | 321 | **223 (69%)** | 98 |
| P570 date of death | 317 | **220 (69%)** | 97 |
| P22 father | 134 | 64 (48%) | 70 |
| P25 mother | 90 | 41 (46%) | 49 |
| P26 spouse | 68 | 36 (53%) | 32 |
| **total** | **930** | 584 | 346 |

**The per-property asymmetry Emma asked to look for is present.** Where the two
sides disagree about a *date*, Wikidata's value carries a reference **69%** of
the time; where they disagree about a *relationship*, only **46–53%**. That is a
real difference and it runs in the direction the "Geni wins relationships,
Wikidata wins dates" prior would predict — which is a reason to test that prior,
not to adopt it.

**What this is evidence of, precisely.** Citation coverage, not correctness. A
sourced statement can be wrong and an unsourced one right, and **Geni has no
comparable field**, so this measures one side only. It cannot say who is right.
What it can do is say where adjudication effort is worth spending: the 346
conflicts where Wikidata's own value is unsourced are the cheapest place to look
for Wikidata errors, and the 584 sourced ones are where a Geni error is more
likely.

## The date conflicts are mostly near-misses

638 date conflicts, **median 13 years apart**, maximum 1,074.

| years apart | conflicts | |
| --- | ---: | ---: |
| 4–5 | 128 | 20% |
| 6–10 | 150 | 24% |
| 11–25 | 172 | 27% |
| 26–100 | 171 | 27% |
| 100+ | 17 | 3% |

Nearly half sit within a decade. The threshold is already 3 years and
deliberately tight — for medieval people a five-year difference between two
sources is ordinary rather than alarming. **A merge rule that picks a winner on
these is choosing between two plausible readings of a thin record**, which is a
different act from correcting an error, and the rule should say which of the two
it thinks it is doing. The 17 conflicts over a century apart are the ones that
are certainly somebody's mistake.

## Two smaller signals

**12 disputed statements carry `preferred` rank.** A Wikidata editor has already
chosen that value over a competing one on the same item, so a rule that
overrides it is overriding a human adjudication rather than filling a vacuum.

**54 conflicts are against an item that holds other values for the same
property too.** A person with three recorded fathers is a different problem from
one with a single wrong father, and "conflict" flattens them together.

## What is still open

**The adjudication itself.** Nothing here says who is right about any single
row. Doing that needs evidence neither side supplies — and the one case already
settled by hand, `reports/husb-conflicts.md`, was resolved by **structure**
(both records sharing a `FAMC`) rather than by any of the columns here. That is
the lead worth following: 292 of these are structural conflicts, and 0.00Z
showed a structural conflict can be a duplicate rather than a disagreement.

**The merge rule.** Emma chose a rule the code applies, which is the more
committal of the two outputs she was offered. It should be generated from an
adjudicated sample, not from the table above — citation coverage is not
correctness, and a rule built on it would encode "Wikidata cites more sources"
as "Wikidata is right", which this report does not show.
