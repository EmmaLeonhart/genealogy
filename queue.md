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

## RUN ORDER — Emma's call, 2026-08-15

**Imports first, labels last.** She asked why the seven-language labels were in
progress, and the numbers back her: the target moved **7,851 → 11,001 placeholders
and 26,281 → 35,011 label edits in one day**, from four exports plus a merge
correction. Item 7 exists to find *more* exports to take, so labelling now means
hand-romanising a set that grows by a third each time.

Her `ja`/`zh` rule is a **gate on editing** — nothing reaches Wikidata unlabelled —
not a claim that labels come first in build order. That ordering was mine.

    7 · sparse Geni clusters   →  the tree grows
    8 · Wikidata re-import     →  the store fills, and name items arrive
    ---- tree and store settle ----
    2 · name items             →  needs item 8: the competing QIDs are not held
    1 · seven-language labels  →  built once, over a stable set
    ---- the gate opens ----
        Wikidata editing

Items 3, 5 and 6 are independent of this chain and can run at any point.

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

## 2 · Name items — the ambiguity is a PATRONYMIC problem, and needs the download first

**Emma, 2026-08-15, diagnosing it herself:** *"Didn't we just answer this question
way long ago? For the most part this is based off of diacritics and based off of
you not differentiating patronymics versus surnames versus given names."*

Measured against her diagnosis:

- **diacritics — fixed.** `Maria` and `María` are separate rows now, not folded.
- **given vs family — already separate.** Ambiguity is computed within a usage.
- **patronymic vs given — NOT separated, and not separable offline.** Telling
  `Q110874` from `Q202444` needs the item's own `P31`. All **1,731** competing
  QIDs were checked against the store: **0 are held.** The store is a Geni-shaped
  slice of people and carries almost no name items.

**So this waits on item 8**, and that is a second independent reason for running
the imports first.

**A separate bug visible in the same list:** `de` is an ambiguous *given name*
with 1,997 bearers. It is a particle, not a name — the token-splitting problem in
`todo.md` § 4, not an ambiguity.

`reports/name-item-plan.csv`, `reports/wikidata-name-items.json`. Prerequisite for
item 1: 21,939 planned, 8,092 link, 13,320 create, **525 held as ambiguous**.

`ambiguous` counts as **existing** — treating it otherwise would have created a
tenth `Maria`. Emma named the one genuine residue herself: `Q325872` / `Q25413386`,
the **male** and **female** given name `Maria`, settled by the person's sex rather
than by the string.

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

## 5 · Wadah Cohen's father

A missing son of `Amram ben Yitzhaq` (`6000000178795370821`); Geni records only
one child for him.

## 6 · Multi-hop relationship labels

Ordering, extending the one-hop precedence rather than replacing it:
**child-of → spouse-of → parent-of → grandchild-of → sibling / nephew / uncle.**

Of the 11,930 people with no one-hop label, **3,604 (30%) have a named relative
two hops out** — 2,020 via a grandfather, 1,449 a grandmother, 135 a grandchild.
Sibling, uncle and nephew need the family graph rather than the derived CSVs.

## THREE SEPARATE WIKIDATA OPERATIONS — Emma, 2026-08-15, correcting a conflation

*"These are three completely different operations that you conflated with each
other."* She is right; I had merged all three and then applied her budget to the
wrong one. They are listed together **only** so the distinction cannot be lost
again.

### A · Labels fetch — DONE, and it was never the core data

`scripts/fetch-referenced-labels.py`, run 2026-08-12: English labels for every
property and item the store references but does not hold.
`reports/wikidata-labels.tsv`, 876,840 items + 5,637 properties.

Emma: *"The labels fetch thing was always intended... but it wasn't really the
core data. It was more of a metadata thing for helping us make decisions."* And
her warning about what it cannot do: *"It wouldn't be giving something that would
be comprehensible for the names at all because most of the name objects will not
be linked."* Correct — it only ever covered items somebody in our store points at.

### B · Name items — RUNNING NOW. *"should be done right now"*

Every instance of the six name classes on Wikidata, not just the ones our people
reference. `scripts/collect-name-item-qids.py` enumerates the QIDs by aggregate
page query, writing `reports/name-item-qids.tsv`; then
`genimerge wikidata-download --seeds reports/name-item-qids.tsv --scan-per-round 0`.

**824,358 items**: 693,049 family name, 59,275 male given, 37,736 female given,
30,894 given, 4,141 unisex given, 631 patronymic. `--scan-per-round 0` is
required — the scan expands along `P22/P25/P26/P40/P3373` and would otherwise
wander back into the 1.4M people.

**This is NOT the 3-8 hour budget.** Emma: *"The three to eight hour budget thing
is about a completely different thing. It's about the Wikidata individuals. It's
not about the names."*

### C · Individuals — LATER, and this is where the 3-8 hours belongs

The relatives in the Wikidata world tree that are not downloaded. Her words:

> This situation could theoretically last almost forever because we have an
> existing downloading thing that manages the queue that we were running a lot
> last week... It started off with the seed of all the geni-linked ones. It then
> expanded and queued up all the linked individuals that were not specifically
> present... When I stopped it, I stopped it because it was difficult to do. The
> queue amount initially dramatically increased, but then it started gradually
> decreasing. I think it's at a relatively low level, but I think it was
> logarithmically decreasing... I stopped it for reasons mostly related to the
> way I was moving around, which do not really apply as much anymore.

**Order: after B.** *"The individuals thing, since it's a bit of a longer-running,
more difficult task, should be occurring after we're finished with this other
stuff, where we can monitor it a bit better and where the relatively
easy-to-resolve name stuff is resolved."*

**And when it runs: do not build new tooling.** *"Whatever the fuck you do, do not
build the new tooling."* The existing downloader manages its own queue. Run it,
measure the queue's decay, and estimate whether there is an end point.

## 8b · The offline patronymic classifier — DONE

**Emma's correction:** *"Whether something is or is not a patronymic here is
determined by completely offline information related to the person's father's
name."* Built and run: `reports/patronymic-classification.csv`, 528,612 rows.
34,139 patronymic, 376,748 not, 114,644 with no verdict because no father is
recorded. **958 tokens go both ways** — `Olsen` is patronymic for 1,018 people
whose father is Ole and an inherited surname for 119 whose father is not.

## Scheduled — `e6e0915c` at 13:02, ONE-SHOT · Emma's name-modelling file

She is writing her own file on name modelling into the repo root. *"I have an idea
of the way the modeling is working, but I feel like you may have not understood
it."* The job reads it, quotes it back before changing anything, fixes
**formatting only**, folds her model into `CLAUDE.md` as the authority, and lists
where the code disagrees **without changing the code**.

Her reference example, Donald John Trump: `P735` Donald with `P1545` 1 and
*reason for preferred rank* = usual forename; `P735` John with `P1545` 2 and
`P3831` = middle name; `P734` Trump. **`P7452` reason for preferred rank is not in
`CLAUDE.md`'s table** and must be added if her file uses it, confirmed offline.

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

## Samaritan High Priest wikidata normalization

Please actually start to set up and plan the wikidata normalization that I've been constantly asking you to set up and plan for the Samaritan High Priests that you've just kind of been fucking off with. I don't really understand why it is that you've been not doing it, and by the way do AskUserQuestion liberally if you are confused. 

I will give some info



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
