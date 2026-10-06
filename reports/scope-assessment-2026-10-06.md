# Scope assessment, 2026-10-06

Queue item (Emma, 2026-10-04: "I think we've gone insanely fast, like way too fast compared to what we probably should
have gone on"). The current scale, measured, against a smaller one. Source: every mainspace edit of 日巫女 since
2026-09-01, read live (`reports/scope-edits-by-day-2026-10-06.json`, 228,881 edits).

## How fast it has gone

| period | edits a day | creations a day |
|---|---|---|
| 2026-09-01 .. 09-20 (first three weeks) | about 2,000 (116 – 3,947) | about 190 (10 – 697) |
| 2026-09-21 .. 09-28 (after the caps were raised) | about 12,500 (641 – 17,722) | about 1,400 (8 – 2,235) |
| 2026-10-01 .. 10-04 (every entry point started) | about 20,000 (12,206 – 25,859) | about 1,100 (836 – 1,460) |
| 2026-10-05 .. 10-06 | 4,723 and 9,015 (10-06 not over) | 264 and 692 |

By kind, over the whole period: 99,543 statements, 71,006 references and qualifiers, 21,258 label edits, 11,162
aliases, 20,633 items created, 2,588 removals.

The jump came in two steps: the week of 2026-09-21 (lean rebuilds chained by `ring-watch.yml`, several QuickStatements
tabs at once, about 6x the earlier rate) and 2026-09-28 (every cap raised 5x: `SIBLING_CAP` 300, `NAME_ADD_CAP` 250,
`P2600_LEAD_CAP` 300, `MANUAL_P2600_PER_RUN` 150, `LABEL_EDIT_CAP` 450). From 2026-10-01, 20,000 edits a day.

## What went wrong at that speed (from devlog)

The serious incidents all fall in the fast weeks: 136 duplicate creations from a description change (2026-09-27);
background batches chaining `LAST` into 736 false relationship claims, a man made his daughter's mother (2026-10-03);
14 false statements from spliced path files (2026-10-02); 116 men sent as mothers (to 2026-10-04); 58 duplicate pairs
from overlapping runs of Han-named creations (2026-10-04); 1,829 statements from zipper-only pairs (2026-09-28 on);
4,412 FamilySearch ids added in a week, still being reviewed one by one (174 + 100 done so far). Each was found days
later, by Emma or another editor (Infovarius), not by a check before the run, and each fix took a session or more. At
20,000 edits a day a defect that lives one day reaches thousands of items; the review backlog it leaves (the 4,412 ids,
the 155 drifted items, the 645 chained claims) is larger than what a session can check in a day.

## Campaigns running at once now

1. Batch rebuilds: `morning-batch.yml` daily plus a lean rebuild chained by `ring-watch.yml` after each batch's last
   ring person (about every 1–3 hours), each up to ~180 people and 450 labelled people.
2. The scheduled sender, `wikidata-edits.yml`, the `-auto` third of each batch.
3. The browser QuickStatements runs, often two or three tabs at once.
4. Hand fix batches from sessions (17 in `reports/` from 2026-10-04 to 10-06).
5. Label applications (now 1,560 rows, about 1,400 to go out).
6. Three Claude sessions on this repo's queue in the last day, plus the sessions this repo launches.

## A smaller scale, and what it costs

A scale like 2026-09-01..09-20 (about 2,000 edits and 150–200 creations a day):
- one batch a day: the morning rebuild only; `ring-watch.yml` no longer chains rebuilds;
- the caps back to their pre-2026-09-28 values (each a fifth);
- one QuickStatements tab at a time, the next batch only after the audit of the last one has been read;
- no scheduled `-auto` sender while the browser runs the same batch.

What it costs: the ring grows about a tenth as fast (a generation in days rather than hours), and the label backlog
(1,400 applications, 221 + 50 + 8 recovered by today's drain fix) takes about a week at 450 a run with one run a day.
What it buys: a day's output (about 2,000 edits) is small enough for the daily audit to sample meaningfully and for a
defect to be caught before it has touched thousands of items.

## Reading

The rate is about ten times what it was when the pipeline was last reliable, and nothing in the error record says
the checks scaled with it. The smaller scale above is the session's recommendation. Which scale to run at is Emma's
decision; nothing has been changed.

## Answer

Put to Emma by AskUserQuestion at 03:54 PDT on 2026-10-06 (session `fba99135`); she answered at 05:5x through the
queue: **"Scale back (Recommended)"**, the smaller scale above. Applying it is its own queue item ("Scale back: the
full context of the question").

