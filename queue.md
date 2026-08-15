# geni — Work Queue

**This file holds steps not yet taken. Nothing else.** When an item is done,
**delete it** and append a dated `devlog.md` entry in the same commit. No
checkmarks, no "done" markers, no keeping a finished item "for context" — that is
what bloated this file twice. If an item is here, it is not done.

Longer-horizon, abstract work lives in `todo.md` and is decomposed into steps here
when it is ready to run. New ideas go at the bottom, never silently into whatever
is being worked on.

**Three-cron playbook.** Extensive work runs under three session-local crons —
work-loop `:03`, auto-flush `:15`, status-report `:42`. A fresh session starts
them; a mid-session queue re-fill kills them first and the pinned tail restarts
them.

---

## 0 · STANDING PROCEDURE — audit this queue against the transcripts first

**Not deleted when it completes: it is a procedure, not a step.** Run it before
executing the rest of the queue, because otherwise the rest is not trustworthy.
**Last run 2026-08-15** → `reports/audit-transcripts-2026-08-15.md` (24
transcripts, 311 user turns).

Transcripts are the authority — they hold what Emma actually said, in order,
including the corrections:
`C:/Users/Emma/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl`.
Newest first by mtime. Each line is JSON; a user turn is `message.role == "user"`.

1. **Extract every user turn with its timestamp.** Do not summarise while
   extracting — that is where instructions get lost. A compaction turn is not
   something Emma wrote: its quoted messages are evidence, its narration is not.
2. **Classify:** instruction, decision, correction, or conversation. Only the
   first three matter. **Frustration is still an instruction** — *"just fucking
   run the census"* is a queue item.
3. **For each, ask: is it done? is it here? is it in `CLAUDE.md`/`devlog.md`?**
   Done and recorded → nothing. Done and unrecorded → `devlog.md`. Not done → a
   concrete step here. A decision about how the project works → `CLAUDE.md`.
4. **Corrections outrank what they correct.** The latest statement wins and the
   superseded one must not survive anywhere as if it were current.
5. **Unrequested normalisation is its own category** — Emma: *"you have a
   tendency to try to do exception handling for stuff that I do not consider to
   be even necessarily errors."* Those go on the list to be **removed**.

---

## 1 · Labels in seven languages — the gate on all Wikidata editing

**Emma:** *"WE ARE NOT DOING THIS SHIT UNTIL WE HAVE JA and ZH LABELS ON
EVERYTHING THIS IS RIGHT BEFORE WIKIDATA EDITING."*

`en` · **`ja`** · **`zh`** · `hi` · `ar` · `ru` · `el` · plus `mul`. Japanese
first, then Chinese, then the rest — Devanagari, Arabic, Cyrillic and Greek chosen
for script coverage.

**The labels are MADE, not copied.** Three directions: CJK → English
(romanisation), English → CJK (katakana for anything not already Japanese), and
English → the four remaining scripts.

**Method — hand-built tables, except CJK → English.** Emma: *"from CJK to English
do not remotely try to do any kind of programmatic transliteration because they
all suck. But AI almost always knows Japanese to Romaji."* So romanising a kanji
name is done **agentically, name by name**, and written into the repo as data.

**Name items first, and that is what makes it tractable.** Transliterate a token
once in its name item and every bearer inherits it. 140,764 distinct tokens across
396,377 people; the CJK part is 30,876 Han, 1,552 Hangul, 92 kana.

**The one hard problem: which culture a CJK name is.** Han characters do not say
whether a name is Chinese, Japanese or Korean, and 陳 is *Chen*, *Chin* or *Jin*
accordingly. Kana and Hangul are decisive; bare Han is not. **Do not guess from
the name** — the tree settles it, via neighbours and which exports they came from.

**Order, and why:** Emma — *"create the relatives first, then label."*

1. Create the **11,001 structural placeholders**, each with the full label set.
2. Then the other creations — the Samaritan line, the order.life tiers.
3. Then the 26,281 `set_labels` edits, every one carrying all seven + `mul`.

`reports/wikidata-placeholder-labels.json` currently has `mul` on all and `en` on
14,351. **It must not run in that state.**

## 2 · Name items — 525 ambiguous ones need Emma

`reports/name-item-plan.csv`, `reports/wikidata-name-items.json`. Prerequisite for
item 1.

| | |
| --- | ---: |
| planned | 21,939 |
| link an existing item | 8,092 |
| create | 13,320 |
| **ambiguous — held** | **525** |

**NEEDS-DECISION:** link the most-referenced item, hold them all, or look at the
top few by hand. `ambiguous` counts as **existing** — treating it otherwise would
have created a tenth `Maria`. The genuine residue Emma named is `Q325872` /
`Q25413386`, the male and female given name `Maria`, settled by the person's sex.

## 3 · The 7 Samaritan father disagreements — for Emma to look at

`reports/samaritan-source-comparison.csv`. 130 of 137 comparable people agree; the
transcription is not superseded and does not contradict Geni.

- `Matzliach ben Phinhas` — source `Phinhas ben Yitzhaq`, Geni `Phinehas`
  (probably only a spelling)
- `Yusef`, `Yusef ben Ab-Hisda`, `Yusef ben Yehoshua` — Geni gives a
  `119th generation Samaritan…` placeholder as the father
- `Shalom ben 'Amram` — source `'Amram ben Yitzhaq`, Geni `Shembet ben Bakhi`
- `Asher ben Shelach` — source `Shelach`, Geni `Matzliach ben Phinehas`
- `'Abed Hanuna ben Jacob Hadinfi` — source `Jacob Hadinfi`, Geni `Shalma`

## 4 · The Itamar spine numbering — NEEDS-DECISION

The `HEAD` now says 121 and the file holds 120 people numbered 2–121, but the
source's figure for the **parallel Phinhas line** is 112. Renumber to end at 112,
or collapse the invented stretch to a single *"distance not recorded"* link as
Emma originally suggested. **The GEDCOM is not touched until she says** — it is
hand-made, and a hand-transcribed source is not superseded on inference.

## 5 · Wadah Cohen's father

A missing son of `Amram ben Yitzhaq` (`6000000178795370821`); Geni records only
one child for him.

## 6 · Multi-hop relationship labels

Ordering, extending the one-hop precedence rather than replacing it:
**child-of → spouse-of → parent-of → grandchild-of → sibling / nephew / uncle.**

Of the 11,930 people with no one-hop label, **3,604 (30%) have a named relative
two hops out** — 2,020 via a grandfather, 1,449 a grandmother, 135 a grandchild.
Sibling, uncle and nephew need the family graph rather than the derived CSVs.

## 7 · Single-export clusters — Emma's item, in her words

> Add to the queue that we are going to look over the geni exports to try to find
> large clusters like the Javanese ones that have only one geni export covering
> them. My perception here is that such areas are more likely to have important
> links that were not covered and that with a different entry point and a larger
> export window thing, particularly looking at the deepest members of such
> clusters of people only in one export.

The Javanese case that prompted it: the excluded `BloodTree` held **1,091** people
no other export had, all Mataram and Demak royalty.

## 8 · Comprehensive Wikidata re-import — Emma's item, in her words

> It is clear here that the Wikidata data that we were importing over the past
> little while is not sufficient… We were at a point where it was good, where we
> had our existing scripts related to Wikidata, and the level of missing/queued
> people was going down… I realized that the geni stuff lacking wiki data was
> more of a concern than I was expecting because it was interfering with some of
> the entity resolution, where there would be a missing wiki data link and there
> would be a present geni link… If we'd be able to specifically look at this
> stuff, prioritizing the ancient, I want to spend maybe 3 to 8 hours working on
> this with the algorithm that we already had that was working great. If that
> algorithm isn't working well, then I'd like to switch towards one that
> prioritizes people in ancient times or people who do not have birthdates and
> what's linked on them first, and then moves on to more recent people.
>
> We should use the great download script and come up with some level of
> estimation of how long it'll take to actually properly get all the Wikidata
> stuff. If it turns out that the amount doesn't seem like there's a clear end
> point, then we move on to this stuff.
>
> **When you reach this queue item, do not build the new tooling. Whatever the
> fuck you do, do not build the new tooling.** You should be setting up cron jobs
> or something to do tests on the existing tooling that you're going to run to
> figure out what's going on and whether it fits it. Run the tooling for several
> hours, and then make a decision.

Context measured 2026-08-15, `reports/store-parent-coverage.md`: of 1,528,454
`P22`/`P25` statements in the store, **34,104 (2.2%) point at an item we do not
hold**, and **71% of those are children with no birth date** — which is the
population her fallback algorithm would prioritise.

---

## Daily jobs — queued because a cron only fires while the session is idle

Emma: *"QUEUE UP THE CRON JOB CONTENTS."* Each is a live `CronCreate` id **and** an
item here, so the work survives whether or not the job fires.

| id | fires | what |
| --- | --- | --- |
| `d425c1f5` | :03 | work-loop tick |
| `be98e574` | :15 | auto-flush — commit and push anything pending, no empty commits |
| `f8b152ab` | :42 | status-report — reporting only, no code changes |

**`f3d681e4` 19:07 — re-merge.** Keep `out/merged.ged` as `out/merged-<n>.ged`
first; the pre-batch tree is the only thing that makes the seed backtests
answerable. Then `python -m genimerge merge`, regenerate every report with a CLI
command, re-run `scripts/build-repo-freshness.py` and confirm `behind_by` empties.
Never overwrite or delete a `.ged`. **Runs at 19:07, five hours ahead of the
midnight merge, which needs the proper synoptic tree.**

**`43140a93` 21:02 — bloat review.** From `reports/repo-freshness.csv`: closed
questions, superseded reports, scripts nothing calls, CLI commands with no
reachable input, duplicated censuses. **Never touch `exports/`, never delete a
`.ged`, never add a `*.ged`/`*.zip` pattern.** Delete nothing on your own
judgement — candidates with a reason and evidence, to Emma in batches of four.

**`d62449e3` 22:01** — ask about `reports/seeds.md`'s future.

**`9f41a7a4` 23:03 — entity resolution.** `entity_resolution.md` is Emma's
free-form scratchpad. **Do not reformat it to suit the parser** — teach the
parser. Show her the entries **raw** and say which are reflected in the data. It
is her job to be *given* JSONs, not to make them.

**`05926d1d` 00:01 — the structural merge.** Walk **up** the parental lines from
people holding both identifiers. **The label only confirms a position the
structure chose; it never searches for a name.** Everything offline. Show cases
one by one before generalising; do not reformat records.

---

## Always last — pinned to the tail

A. **Ensure the three crons are running** — work-loop `3 * * * *`, auto-flush
`15 * * * *`, status-report `42 * * * *`.
B. **Run the status-report action once more** — an end-of-session summary.

---

## Pointers

- Abstract backlog: `todo.md` · Completed work: `devlog.md` · History: `git log`
- Open questions for Emma: `questions.md`
- The pre-wipe queue, 1,396 lines: `git show 4127170:queue.md`
