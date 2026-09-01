# geni — Work Queue

**This file holds steps not yet taken. Nothing else.** When an item is done, delete it
and append a dated `devlog.md` entry in the same commit. No checkmarks, no "done"
markers, no keeping a finished item for context.

**Do not preserve Emma's wording here.** Her instructions belong in `CLAUDE.md` (rules),
`devlog.md` (what happened) or `reports/` (findings). Emma, 2026-08-22: *"you are makign
the queue useless by presering my verbatim words."* A queue item is a step, in as few
lines as say what to do.

**Trimmed 2026-08-23** from 48 sections to these; what went was records of finished work,
audits, dead crons and superseded priorities. Recover any of it with
`git show 6edf302b:queue.md`.

## ⛔ ITEM 1 — KOREAN. `ko` is CJK and ranks with `zh`. IN PROGRESS 2026-09-01

**At the top of the queue by her instruction, 2026-09-01:** *"put the korean stuff at the
beginning of the queue to make it clear that we're following the instructions properly and will
continue on through all of the queue after"*, after *"korean is extremely important on par with
Chinese and you really should prioritize getting korean labels all the time and this seems to not
get that cjk includes korean"*.

**Done so far.**

- `scripts/translit_ko.py` — a hanja-to-Hangul engine, **733 hand-read characters**: the top 400
  by corpus frequency, then the top 300 of what that pass missed, chosen by measuring the misses.
  Hangul passes through untouched; the initial-sound rule (두음법칙) is applied to the head of each
  name, so 李 is **이** and not 리.
- **61% of the 46,452 people with a CJK name get a COMPLETE Korean label**, up from 44% after the
  first 400. A partial rendering is never emitted — one unknown character blocks the label.
- Verified by eye: 李成桂 → 이성계 · 金正日 → 김정일 · 朴正熙 → 박정희 · 藤原道長 → 등원도장.

**All four follow-ups are DONE, 2026-09-01.**

- **Coverage raised 44% → 61% → 72%** over three tranches, each chosen by measuring what was still
  unread rather than guessing. The table is **1,033 characters**. 3,960 distinct characters remain
  over 28,703 occurrences, so the tail is long and each further tranche is worth less.
- **`scripts/translit_ko_latin.py`** — the other half, Latin → Hangul, which is what the creation
  gate actually needs because the Garborg ring is Latin-named. **97% of the 1.29 million
  Latin-labelled people render.** Four bugs found by reading the output, not by testing: ㄹ is
  named `r` in the initial slot and `l` in the final; `l` closes a syllable where `r` opens its
  own; the final was skipped whenever the vowel split; and a doubled stop collapses where a
  doubled liquid does not.
- **A `ko` column in the funnel table** — 18,535 of 18,536 tokens carry a Korean reading. The one
  that does not is `'....'`, which is punctuation.
- **The creation gate is `ja` + `zh` + `ko`**, and all 28 creations in today's batch carry `Lko`,
  including the NN/relationship people, who take the genitive: `아스트리 …의 아들`.
- **`scripts/build-ko-label-batch.py`** — 33,725 labels for the whole CJK population, the same
  scale as `ja`'s 41,952 and on the same standard.

**What is left is one decision, and it is shared with `ja`:** 1,278,536 Latin-named people can be
rendered into Hangul at 97%, and both batches withhold that population because transcription is
not reading. Whether that line moves is a decision for `ja` and `ko` together, not for Korean
alone.

**`P1814` *name in kana* is NOT part of this and stays agentic** — a Japanese name reading does not
follow from the characters, which is why queuing the two together was the mistake this item fixes.

## Korean through the ROMANISATION pipeline — her emphasis, 2026-09-01

*"So just more emphasis with the korean stuff there and changing some of the romanization pipeline
queued stuff"*, after *"korean is extremely important on par with Chinese... this seems to not get
that cjk includes korean"*.

The romanisation pipeline currently has **two** directions where it needs three:

- `cjk_romanisation` classifies a name's culture as `ja` or `zh` and romanises accordingly. The
  1,552 Hangul tokens settle culture decisively, and Korean romanisation (Revised Romanization)
  is regular — so `ko` is a third branch, not an exception.
- **The Han-to-Korean direction is the one that is missing entirely.** A Chinese or Japanese name
  written in Han characters has a regular hanja reading, so `ko` labels are generable for the
  whole Han population the way `zh` is — 30,876 Han tokens, not just the Hangul ones.
- `reports/garborg-name-transliterations.tsv` gains a `ko` column and the funnel mints all three.
- The creation gate becomes `ja` + `zh` + `ko`.

**`P1814` *name in kana* stays agentic and is a different job** — a Japanese name reading does not
follow from the characters, which is exactly why it should never have been queued alongside `ko`.

## How to read this file

**Emma, 2026-08-27:** *"Organize the queue to make it usable again, currently it does no appear to
be usable."* It was not, and the reason was structural rather than volume: **five sections declared
themselves the front** — the mass export campaign, the algorithm review, `THE EXPORT LOOP` (*"it is
the top of this file"*), `THE AGENDA` (*"everything else is secondary"*) and `RUN ORDER` — while
**ten declared themselves the tail**. With both ends contested there was no order to work in.

**The order is now position, and nothing else.** Top to bottom. Two conventions, both hers:

- **Bullets, never numbers** — `CLAUDE.md` § *Queue items are BULLET POINTS*. A number is a promise
  the item will still be there.
- **An item is deleted when it is done**, in the same commit as its `devlog.md` entry. A section
  still here is a step not yet taken.

**Everything titled `LAST` / `THE LAST ITEM` / `THE TAIL` is now physically at the end**, in one
run, so "last" means last. Nothing was reworded and nothing was dropped — only moved.

**Some sections are SPECIFICATIONS, not steps**, and are worth knowing about before working the
ones above them: `THE EDIT ALGORITHM`, `THE DAILY ALGORITHM`, `THE TAIL ALGORITHM`,
`Link reliability order`, `The chain of provenance`, `How the synoptic tree is actually made`,
`PREREQUISITE ORDER`. They describe how a thing is done rather than asking for it to be done.

## 0. Aug 28, 2026 manual adds

These are supposed to be manually added to the queue and worked on, do no just paraphrase during the rebase keep this part entirely intact. We are approaching usage limit for now.

## ⛔ HER RULINGS, 2026-09-01 — the interview. These OVERRIDE the sections below

She went through every item and ruled on each. Where a section below disagrees with this table,
this table wins; the sections are kept for their detail, not their status.

**Deleted outright, already removed:** the eight Asian identities · Bure kinship random-walk ·
the World-Tree review and its `universe` note · the chains as a SYSTEM · the six unwalked
algorithm steps · the four-label census · resolving names against the store · the 46%/41%
transliteration measurement (*"accept it and move on"*).

**Moved to the tail:** link reliability / `P1038` — *"we have the established method of
identifying parents and that works, siblings are just freely made and merged lol we only need a
scalable zipper thing much later"* · the `synoptic tree` vocabulary split · **creating the
fathers patronymics imply — *"postpone for a month lol"***.

**To do, in her words:**

| item | her ruling |
| --- | --- |
| seven languages | wire `hi`/`ar`/`ru`/`el` **now**, and close the `en` shortfall |
| **the `en` rule she gave** | *"if multiple Latin alphabet labels agree then it becomes the en label and the mul label"* |
| labels in her order | **only the languages already wired** — `en`, `mul`, `ja`, `zh`, **`ko`** |
| name items | **invert the default now** — *"I thought we reused name objects by default lol. The only hard situation is patronymics"* |
| `Sara /NN/` and the `Garborg` override | do both; the override of her hand-edit is the serious one |
| how many Geni labels need changing | run the census |
| CJK | **`ko` is CJK and ranks with `zh`** — *"on par with Chinese... prioritize getting korean labels all the time"*. `ko` by rule, `P1814` kana agentically |
| NN birth-name alias | fix it |
| unreadable transliteration tokens | read them agentically |
| the 218 scripts | **sweep and delete** |
| one batch file | **merge into one, names first** — absorbs *One pipeline, one output file* |
| clan labels `Q45449130` | check them — *"I never actually ran them"* |
| `exports/post-merge/` | do the stale-duplicate resolution |
| the export loop | **the four retries are DONE and every path is connected** — see below |
| the 179 ambiguous patronymics | **DONE** — https://claude.ai/code/artifact/fb4829e3-df7b-4db3-9ed1-9649bb97a0f5 · 64 names, 2,581 people |
| `P407` on patronymic items | **add it by suffix convention** |
| `Nils`/`Nicolaus` | build the form table |
| succession CSV | model it |
| `pykakasi`, `BET x AND y`, the 74 MB file | all three |
| final act of the night | `scripts/rebuild-everything.py`, then attach the batch |

### The export loop: the four retries were already satisfied, and the chains are CLOSED

**Checked 2026-09-01 before touching the browser**, which is what § *GREP THE CORPUS BEFORE
RUNNING AN EXPORT* is for.

**The four people she instructed me to reattempt are all in the corpus and all in the merged
tree** — Anna Charlotta Stenius `6000000002400180669`, Artur Lidman `6000000082482425565`,
Ola R Sande `6000000079231324930`, Anna von Mecklenburg-Schwerin `6000000000598850973` (who also
carries `Q90441`). Later exports picked them up. There is nothing to retry.

**And `scripts/census-paths.py` now reports `every path is connected end to end`** — 699 path
files, and the missing-count distribution is a single row at **0 missing**. The campaign those
exports existed to serve is finished.

**So no export was run.** What is left in the export item is phase 4, the sparse regions from
`reports/density.md`, which is exploratory rather than gap-closing — it looks for people we have
never seen rather than closing a known hole. That is not something to run unattended on her Geni
account while she is asleep, and nothing is waiting on it.

### Anonymisation is NOT redacting the tree. It is scrubbing the repo of strategy

**Her definition, 2026-09-01, and it replaces the ~96,000-private-rows reading entirely:**

Her instruction, 2026-09-01: cut the content in this repo that discusses **strategy around her
own item and how the account's editing is perceived**, and remove **code that treats her item as
special**. The spine is the Arne→Bureus one only, and a task for 2026-09-02 removes that and all
spine logic once it is complete.

So three things, and none of them touches a person's data:

- **Cut the strategy content.** Anything in `CLAUDE.md`, `queue.md`, `devlog.md` or the scripts
  about how her item gets linked or how the account's editing reads to others.
- **Remove code that treats her item as special.** `NEVER_TOUCH_QID`, the exclusion entries, and
  anything else keyed on `Q232803` / `Q140568870` / `6000000087535357291`.
- **`SPINE_PATHS` keeps only Arne → Bureus**, which is already true.

**The repo is public as of 2026-09-01** — *"The repo is public now lol"* — so Actions minutes are
free and `CLAUDE.md` § *Cost* no longer binds.

## FOR 2026-09-02 — the two removals, and one question I would not answer alone

### The `NEVER_TOUCH` lists — NOT removed, and here is why

Her anonymisation instruction includes *removing code that treats my item as special*, and
`NEVER_TOUCH_GENI` / `NEVER_TOUCH_QID` in `scripts/build-garborg-day.py` are exactly that. **They
were not removed**, because removing them does not make the code neutral — it makes the batches
start editing her item, which is the opposite of *"I should not be in the traversable graph"*
(2026-08-27). Deleting a guard overnight, on a guess, in a way that produces live edits, is not a
call to make while she is asleep.

**What was done instead:** the narrative around those lists is gone — they now read as an
exclusion list and not as a discussion of her item. Behaviour is byte-identical and
`tests/test_p2600_batches.py::test_no_batch_names_an_excluded_id` still guards it.

**What she needs to decide:** whether the lists come out entirely (and her item becomes editable
like any other), or stay as the mechanism keeping her out of the graph.

### Remove the Arne→Bureus spine and ALL spine logic

**Her instruction, 2026-09-01:** *"we add a task for tomorrow sept 2 that removes that spine thing
and all spine logic as it presumably will be completed there"*.

So tomorrow: `SPINE_PATHS`, `SPINE_REVERSED`, the spine blocks in `build-garborg-day.py`,
`build-missing-reciprocals.py` and anything else that special-cases a spine, all come out. Check it
is actually complete first — if it is not, say so rather than deleting a live mechanism.

## Keep `reports/merges-to-do.md` current

Emma, 2026-08-31: *"Just make a 'merges to do' file that records these merges and the wikidata
duplicates and all the other things we went over that's a file I'll use tomorrow to do merges
manually on my own with the quickstatements session."*

`python scripts/build-merges-to-do.py` rebuilds it. Regenerate it when
`out/wikidata/p2600-all.tsv` or `reports/garborg-qids.tsv` is refreshed, so the duplicate
counts are not stale when she next sits down to it.

**The merges themselves are hers now, not mine** — that is what the file is for. The Izumo
three are cleared and the browser pass is closed.

## ⛔ THE DAILY ALGORITHM — her full spec, 2026-08-26. SPECIFICATION, not a step

`docs/dictation/2026-08-26-daily-algorithm.md` is her dictation verbatim;
`docs/daily-algorithm.md` is the reading. **The order is structurally rigid and the weirdness is
intentional** — *"the weirdness isn't something to be sanded off"*.

**One command**: `python scripts/build-daily-batch.py [--refresh-ledger]` runs step 0, then the
three steps in her order, and prints the run order with each file's position. Step 0 is off by
default because it is the day's one network call.

Steps 1, 1b, 2 and 3 live in `scripts/build-garborg-day.py` and
`scripts/build-garborg-name-items.py`; the caps are in those files and are the authority on
their own values, not this section. `devlog.md` 2026-08-26 has how they were built.

**The one thing still outstanding: the ideal state is the union of the synoptic tree and the
Geni tree**, and the synoptic half does not exist yet. That is the § *PREREQUISITE ORDER* item,
not this one.

**Do not "fix" the artefacts.** Spouses unlinked to their partner's children, and parents not
linked to each other as spouses, are intentional consequences of the order and are closed by later
days.

**Two readings taken rather than asked, both recorded where the code is:** which name items —
most-borne first, so each earns the most links; and step 1b runs every time rather than behind a
gate for *"once we get to a certain point"*, because she said it *"could be in the same line as
the descendants one"* and a gate I invent that never opens is the failure mode § *The batches are
a SEQUENCE* is written against.

## The daily Garborg batch — one QuickStatements run per day

`scripts/build-garborg-day.py` → `reports/wikidata-garborg-day.qs`.
`reports/garborg-qids.tsv` is the ledger of who has a QID, filled from **Emma's Wikidata
contributions** (account 日巫女), never a bulk download — her instruction, 2026-08-24.

**The rule: a statement goes in only if BOTH ends already have a QID.** Emma, after
running the first file: *"I only ran some of the quick statements because many of them
required links that couldn't exist... this is going to be the practical limitation of
what our quick statements can do."* Nothing deferred, nothing commented out. What cannot
run today is tomorrow's batch, because tomorrow those items exist.

Each day: close the links yesterday's creations made possible, create the next ring, link
the new people only to what already exists.

**Nothing is outstanding on this item.** Three bullets sat here reading *NOT a blocker*,
*handled, not blocked* and *out of scope* — the name-items file (`LAST` does point at a fresh
`CREATE`), the ambiguous tokens like `Olga` (listed in the batch's own trailer, so the batch
runs without them), and CJK `SURN` (which belongs to the corpus-wide name work). They were
resolved statements rather than steps, and are removed 2026-08-30.

This item is the **standing daily process**, not a step to finish: one batch a day, for as long
as the programme runs.

## THE EDIT ALGORITHM — her specification, recorded verbatim in substance

**She raised this because she was worried it had been altered:** *"I don't think I
expressed to you how much my version actually favours me, and I'm hoping that, as
a result, you didn't decide to change something and go against specification to
make it favour me less."*

**Checked 2026-08-15: nothing implements it yet.** `scripts/wikidata-edit-run.py`
is a batch executor with `MAX_EDITS_PER_RUN = 100` and a reviewed-batch allowlist.
There is no random selection and no service-area gate, so there was nothing to
alter. **When it is built, it is built to this spec and the bias toward her
neighbourhood is deliberate — do not normalise it away.**

**The rate.** 100 JSONs executed per day, chosen at random from the eligible set.

**The service area — what makes an edit eligible.** An edit needs a *service
area*: something that has a Geni ID, or an item that has a Geni ID, or an item
that is getting one added. *"Something that, in our version, has a GeniID but on
Wikidata gets it. That's a service area… particularly something that has a GeniID
but is otherwise isolated."*

**Why it favours her, and why that is the design.** Her own item can add a mother
or a father with equal probability. Once one is added, **each of them can add the
other**, either can add her brother, and her brother can add her back as a sibling.
Each addition creates new surface area for the next.

**So the growth rate depends on saturation, not on size.** *"There's a very large
amount of saturated relationships in the very dense areas. The most ideal situation
for lots of people being added is a bunch of individuals that are not linked to
each other and are relatively close to each other, so that each of them has a
relatively high probability of growing out more individuals."* A dense, fully-linked
region has nothing left to add; a cluster of near-but-unlinked people compounds.

**That is why the researchers and the Nordic cluster come out on top** — not
because they are ranked highest, but because *"the algorithm is most optimised to
hit these people, because they are entry points for the algorithm to function."*

**De-prioritise Geni-IDs-as-sources.** She expects most items to receive a Geni ID
and nothing else, and if Geni IDs start being added as sources onto relationships
that already exist, **that class drops to roughly 5–25 edits a day** rather than
competing for the 100.

**Scheduled path-building runs alongside the random 100.** Deliberate edits that
build a path from her outward, *"starting with the people close to me that have
wiki data items"*, then filling the Charlemagne line from the medieval period
downward until it intercepts.

**The end state she is describing:** a dense region around her, mostly of people
she did not create, which keeps accumulating because each addition raises the
surface area. *"It looks like established genealogical stuff"* — and the Samaritan
high priests and the antiquity work sit inside the same region rather than beside
it.

---

## STANDING PROCEDURE — audit this queue against the transcripts first

**Not deleted when it completes: it is a procedure, not a step.** Run it before
executing the rest of the queue, because otherwise the rest is not trustworthy.
**Last run 2026-08-30** → `reports/user-turns.tsv` and `reports/unrecorded-instructions.tsv`
(38 transcripts, **3,679 turns since 2026-08-15**, 1,577 distinct, **243 directive and written
down nowhere**). Steps 1 and 3 are scripts now — `scripts/extract-user-turns.py` extracts
verbatim, `scripts/audit-turns-recorded.py` screens for directive shape and then for whether any
six-word run of the turn appears in `CLAUDE.md`, `queue.md`, `devlog.md`, `name modelling.txt`
or `docs/`. The screen was checked against rulings known to be recorded and flagged none of
them. A miss is a **candidate to read**, never a finding — she repeats herself, and much of what
she says is answered in the moment and needs no record.

The previous run was 2026-08-15 → `reports/audit-transcripts-2026-08-15.md` (24 transcripts,
311 user turns).

Transcripts are the authority — they hold what Emma actually said, in order,
including the corrections:
`C:/Users/Emma/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl`.
Newest first by mtime. Each line is JSON.

**Read BOTH record types, or the scan misses half of her.** A turn she typed while
the model was idle is `{"type": "user", "message": {"role": "user"}}`. A turn she
typed while a tool call was running is
`{"type": "queue-operation", "operation": "enqueue", "content": "…"}`, and it is
**not** a user record. On 2026-08-16 the split was 28 user records against 21
queue-operations, so a `role == "user"` scan finds 57% of what she said. Skip the
`enqueue` entries whose content is a cron prompt or a `<task-notification>`; those
are the harness talking, not her. Found 2026-08-17.

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

## Labels in seven languages — the gate on all Wikidata editing

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
3. Then the `set_labels` edits, every one carrying all seven + `mul`.

**The placeholder half, rebuilt 2026-09-01 and four times the size it was.**
`reports/wikidata-placeholder-labels.json` is **158,618** edits — `mul` on all, `en` on
**137,528**, `ja`/`zh` on **44,130** — built as `<relative's name>の娘` once the token funnel was
pointed at that population. What is left of it is at the tail as § *the tokens the
transliteration funnel cannot read*.

**Those numbers were 39,691 / 32,129 / 22,614 the day before, and nothing about the method
changed.** `reports/relationship-label-preview.csv` — the sole source of the `relationship label`
rows — was dated **2026-08-19** against a tree rebuilt **08-31**. It held 39,691 people of whom
only **9,996** were still unlabelled, and missed **52,526 of the 62,522** people who currently
have no label at all. It was not a pipeline step, so nothing re-ran it. It is one now, along with
the three batches below it, and `derive-family.py` was moved after `derive-labels.py`, which it
reads. Emma, 2026-09-01: *"Just that it was so stale lol."*

**`reports/label-gap.csv` is the census of who is left**, from `scripts/census-label-gap.py` —
every one of the 62,522, with what each can actually receive:

| | count | |
| --- | ---: | --- |
| a surname surviving redaction → `NN Larsson` | **37,205** | 59.5% |
| no surname, but a NAMED relative within two hops | **23,466** | 37.5% |
| **neither — stays a bare `NN`** | **1,851** | **3.0%** |

So **97% is reachable**, and the second hop is not decoration: 29,707 are reached at one hop and
**9,569 only at two**, which is Emma's *"it can work off of those long-range things"* paying for
itself. 15,810 of the surname rows also have a named relative and get both halves.

**What stays here is everything else in her order**: `hi`, `ar`, `ru`, `el` have not been started
(the wiring is at the tail), and **36,592 people still have no `en` label** after the rebuild —
down from 35,083 measured against the stale preview, which was a smaller number of a smaller
population. That is the large outstanding job.

## Pointers

- Abstract backlog: `todo.md` · Completed work: `devlog.md` · History: `git log`
- Open questions for Emma: `questions.md`
- The pre-wipe queue, 1,396 lines: `git show 4127170:queue.md`

## EMAIL me the daily QuickStatements file, every day — from 2026-09-01

**Her ruling, 2026-08-31**, replacing the automated-edit reading of this item: *"not wikidata
editing but instead emailing me the daily quickstatements file to me every day so I can run it."*

So nothing edits Wikidata. The deliverable is **delivery**: the day's
`reports/wikidata-garborg-day.qs` (and the name-items file, until they become one file) arrives in
her inbox each day and she runs it by hand, which is what has actually been happening in chat all
along.

- **The date is tomorrow.** `scripts/wikidata_lockout.py` and `.github/workflows/wikidata-edits.yml`
  both carry `START_DATE = 2026-09-01`, pinned together by `tests/test_wikidata_start_date.py`.
  Those stay as the safety rail on the *edit* path, which remains unused.
- **`schedule:` plus `workflow_dispatch:` only.** `CLAUDE.md` § *Cost* forbids `push:` and
  `pull_request:` triggers and this needs neither.
- **It runs on GitHub Actions, and it is step 4 of § *THE VERY LAST ITEM***, which carries the
  whole chain: shrink the checkout, anonymise, go public, then this. Do not build it before
  then — until the repo is public there are no free minutes to run it on, and the date passing
  changes nothing on its own.
- **Send the file, not a summary.** The batch is what she runs.

## The chain of provenance — Emma, 2026-08-25

**Her words:** *"providence is important in this, and ideally, a zipper merge will almost always
be done with there being a relatively large chain of providence, not just a simple 'this was the
justification,' but a potentially very large series of justifications."* And why the manual
verdicts exist at all: *"That is the actual reason why I asked you to record my manual decisions,
because of the fact that they entered into the province too."*

**BUILT — `scripts/zipper-provenance.py`, re-run 2026-08-31.** `reports/zipper-pairs.tsv` records
one step; this walks them into the **transitive closure** she describes — a round-5 pair's
justification being its own step plus every step beneath it, down to an anchor or to one of her
own verdicts. Chain depth **max 8, mean 2.7** over 45,898 inferred pairs. Outputs
`reports/zipper-provenance.tsv` and `reports/zipper-provenance-chains.md`.

    25,723  CORROBORATED        7,306 pairs an independent source confirms
    20,008  INFERRED            88 an independent source contradicts
       167  POISONED

Her hand verdicts are first-class nodes, as she asked: **103 independent pairs** from
`reports/emma-judgments.tsv`, alongside the structural walk (7,841), her Geni bio links (405) and
the clan rosters.

**This section stays as the SPECIFICATION** — the two propagation rules below are how it must keep
behaving, and they are hers rather than derivable from the code.

Two things follow, and she stated both:

- **Support propagates upward.** *"If you have a group of 100 people in one generation, all of
  their ancestors are all consistent. It's a really good sign... suddenly you go into the ancestors
  and you notice that somebody connected one of the ancestors. There's an entity resolution on one
  of the ancestors from our side. This supports it extremely well, and it actually supports it
  down the entire chain."*
- **Contradiction propagates the same way.** *"if you end up in a situation where there's an entity
  resolution that clearly contradicts it, this indicates a clear contradiction... it goes both
  ways."*

So the artefact is a provenance **graph** that can be walked in both directions, with her manual
RIGHT/WRONG verdicts as first-class nodes, and a report of which inferred chains an independently
recorded `P2600` confirms or refutes.

## Link reliability order — parents, spouses, children, siblings

**Emma, 2026-08-25, ranking them least messy first:**

1. **parents** — *"parents are always most reliable"*
2. **spouses** — *"can be a bit messy because sometimes people have multiple spouses"*
3. **children** — *"there's a lot of comparison stuff"*
4. **siblings** — *"sibling links are not very common"* on Wikidata

`scripts/zipper-join.py` now runs its slots in this order, which matters because the first slot to
claim a person in a round wins. Siblings are **not** a slot yet and should be added last, if at
all. **The fifth kind is surveyed** — `P1038` *relative* with `P1039` *kinship to subject*,
`reports/p1038-relative-survey.md`, 2026-08-26. 26,724 of 2,246,827 stored items carry it,
49,974 statements, 93% qualified. **71% of the kinships are ones a walk over our own parent and
child edges already produces** (uncle, grandfather, nephew, cousin); the **29%** that are not —
in-law, step, adoptive, foster, godparent — are the only part worth building on. Nothing built.

**And the point that stops a whole category of wrong stopping:** *"no ancestors isn't a point to
stop... It doesn't mean that the ancestors aren't on Wikidata. That's not what it means... at this
point, you're not really doing the zipper anymore. We'll just be adding new individuals on
Wikidata."* A slot with nothing on their side is a **creation opportunity**, which
`reports/creation-opportunities.tsv` now counts, not a failure of the join.

---

## LAST — name items are being MERGED by other editors. Stop preferring creation over reuse

**Recovered from the same crashed session; she asked for it at the end of the queue.** Emma,
2026-08-29: *"I've noticed that certain names, for example Tunheim, I've noticed that some of these
names got merged in with an existing item. I'm extremely confused how this happened, and it seems
to me to indicate maybe you're not actually checking the existence of the names correctly in our
data. Having a strong preference for creating new name objects versus using the existing ones is a
very wrong move here. Creating the name objects and having them merged by somebody else (and this
is important) is a thing that gets attention in a bad way."*

Two things, in order:

- **Find out how the existence check missed them.** Start from the name items the batches have
  created, find which have since been merged away by another editor, and work back to what the
  lookup did at the time. A diacritic is *not* the first explanation to reach for — `CLAUDE.md`
  records that folding them invents ambiguity — so measure before theorising.
- **Then invert the default.** Reuse an existing name item unless there is positive evidence the
  usage differs. § *One name item per USAGE* still holds: a given name and a family name spelled
  alike are genuinely two items; two spellings of one family name are not.

## THE TAIL — two she moved here herself, 2026-08-29

*"Just add both of these to the end of the queue."* Both were cron jobs she scheduled by clock
time on 2026-08-27; every cron died in the 08-28 crash, so neither will fire on its own. Her words
are kept because these are unstarted.

- **`Sara /NN/`** — the case she set aside at the time: *"Ignore the fucking NN thing. 'Sara /NN/'
  can wait until a cron job at 9pm fires to analyze this problem then."* The name is
  `Sara` with `NN` in the surname slot, which is the inverse of the shape
  `_carries_marker` was fixed for — there the marker was the *given* token and the surname real.

- **Why a redacted profile came out labelled `Garborg`** — *"do a cron job at 10pm to analyze why
  https://www.geni.com/people/private/6000000021223635839 was added as "Garborg" instead of the
  current labels on wikidata that I manually added https://www.wikidata.org/wiki/Q141199845"*.
  Note this is a `<private>` profile, so § *The NN/Private label algorithm* governs what it should
  have been, and she had already hand-corrected the item — so the question is also why our label
  overrode hers.


## How many Geni labels actually need changing? Count them

**Emma, 2026-08-29:** *"Put at the end of the queue: a specific thing, doing an analysis on the
amount of people whose Geni labels are made to be changed and stuff like that."*

**The number she wants first:** *"I don't know the degree of people that we have that only have CJK
labels, because that is an important thing for analysing with this."* So: how many people in the
corpus carry a name **only** in Han, kana or hangul, with no Latin form anywhere on the record?
Those are the ones who would need an English name written onto Geni.

`reports/derived-labels.csv` has `cjk_names`, `other_script_names` and `further_latin_names`, and
`display-names.csv` has the raw fields and a `scripts` column, so this is offline and cheap.

**Report the count before proposing any edit.** The campaign's value is whatever our pipeline puts
in `mul`, so the second number worth having is how many of those people our pipeline can currently
produce a `mul` for at all — a person we cannot label is not a person we can fix.

## "Synoptic tree" means two different things — resolve it usage by usage

**Emma, 2026-08-29, asked what it concretely is:** *"it is consistently conflated between the union
of all the geni gedcoms and the union of that tree with all data sources."*

So the term carries two meanings and the repo does not distinguish them:

- **the Geni union** — every `.ged` under `exports/` merged, i.e. `out/merged.ged`
- **the full union** — that tree joined to every other source, Wikidata above all

**Her instruction: `AskUserQuestion` on every specific usage** — *"Add to the end of the queue a
task to run AskUserQuestion on every specific usage as the full version geni union idk or custom"*.
So go through every place the phrase appears in `CLAUDE.md`, `queue.md`, `docs/` and the scripts,
and put each one to her as *Geni union / full union / something else*, rather than picking a
definition and applying it everywhere.

**She also considers the immediate question moot:** *"I'm pretty sure the gedcom we added as a
workaround makes this question obsolete"* — `exports/post-merge/wikidata-qid-links.ged` puts the
Wikidata links into the corpus, so they arrive in the merge either way and nothing waits on the
definition being settled.

## CJK label conversion — fill in Korean and `P1814` *name in kana*, with research

**Emma, 2026-08-29:** *"do a cjk label conversion thing with research to fill in the korean and name
in kana properties using among other things stuff from the shintowiki-scripts repo"*.

**Two things are missing, and they are different in kind.**

- **`P1814` *name in kana*** — a real Wikidata property, confirmed offline in
  `reports/wikidata-labels.tsv`. **Nothing in this repo emits it.** The two scripts that mention a
  property in that family, `build-garborg-name-items.py` and `build-orderlife-identifiers.py`,
  reference it once each and neither writes one.
- **Korean** — the `ko` **label**, not a property. Her chain, 2026-08-29: *"korean is a rendering
  derived from the Chinese ir Japanese"*, so it comes off `ja`/`zh` rather than off `mul`. Nothing
  emits `ko` today either.

**"With research" is the load-bearing half.** Kana for a Han name is not derivable by rule — the
same characters take different readings per person, which is why `P1814` exists as a property at
all rather than being computed. This is the case `CLAUDE.md` § *The one hard problem: which culture
a CJK name is* already names. So the work is: find the readings, do not generate them.

**`shintowiki-scripts` is a SEPARATE repo and the coupling has burned this repo once.** `CLAUDE.md`
§ *WIKIDATA EDITING STARTS 2026-09-01* records that a previous session invented a shared lockout
between the two and it *"failed closed"*, blocking edits this repo was entitled to make. Emma:
*"Shintowiki scripts and this one are not the same and not really coordinated"* and *"I think you
hallucinated a coordination between them."*

**So: take material from it, do not couple to it.** Copy or vendor what is useful — reading tables,
transliteration data, whatever it holds — into this repo, and add no runtime dependency, no shared
state file, and no network call to it. It is not checked out beside `geni`, so the first step is
asking her where it is.

## The NN path drops the birth-name alias the named path emits

Found while answering the `Q141205924` label question. The named branch of
`build-garborg-day.py` emits `Lmul <married>` **and** `Amul <birth>`; the redacted/NN branch
sets `birth = ""` and emits the `mul` alone. So a married NN woman keeps only one of her two
recorded surnames. `NN Gjøa` would be her alias under the current rule and is not emitted.

Analysis first: count the NN people carrying both a `SURN` and a different `_MARNM`.

## ABSOLUTE PREREQUISITE — no individual is created without their CJK labels

**Emma, 2026-08-29:** *"There should be an absolute prerequisite that nothing is created until you
add in the CJK labels... It should be an absolute prerequisite for the creation of any individual:
that we have their CJK labels."*

**Apply this at the END of the queue, not now** — her explicit instruction: *"Apply it at the end of
the queue because I don't want to interrupt whatever pipeline we're running right now."*

**The rule:** a `CREATE` is refused unless that person has `ja` and `zh`. Today the builder emits
them when every token resolves and creates the person anyway when they do not; under this rule the
person is carried forward instead. It currently bites rarely — 37 of 38 creations in the last batch
already carry both — but rarely is not never, and she wants it absolute rather than usual.

**The order she wants, and the reason:** *"All of the items that I have created, especially the ones
that I have edited, need the CJK stuff first on them."* So the shared 15-a-batch cap stays as built,
clan block last — she confirmed it: *"keep the shared 15 with the clan left. That is the best thing
to do because the most important thing is to fix up the CJK labels on our existing items first."*
Existing people drain first, then the 177 clan people. *"The clan people also extend the range of
the quick statement stuff by a lot, so this is worth leaving at the end."*

## Systematic review for legacy code — the 218 scripts, now the readers are done

**The `entity_resolution.md` readers are cleared, 2026-08-31.** Emma: *"no files should read it
lol."* **0 code readers remain**, down from 22 files:

- **2 deleted outright** — `build-entity-resolution-batch.py`, whose entire purpose was that file,
  and `build-charlemagne-route.py`, for the spine she declared legacy.
- **7 had the read removed** — `build-garborg-day.py`, `derive-labels.py`,
  `refresh-live-values.py`, `path-between.py`, `build-trunk-batch.py`, `build-edit-objects.py`,
  `build-path-to-wikidata-report.py`. Each folded that file's pairs into a lookup and had been
  contributing nothing since 2026-08-29.
- **`genimerge.cli`'s `entity-resolution` command keeps working but has no default source.**
  `genimerge.entities` parses her free-form format and she may hand it another file; what went is
  the assumption that the retired one is still there.

**`build-edit-objects.py` was deleted and then restored**, because `tests/test_edit_object_labels.py`
loads it. Deleting a script a test imports is breaking a test to tidy up, which the rails forbid;
only the read came out.

**What remains is the wider sweep.** 218 scripts in `scripts/`, and the test is *does the pipeline
read this*, not *might this be useful*. A defensible pass: every script not referenced by another
script, by a test, by `CLAUDE.md`, or by a queue item, and whose outputs nothing reads. **Report
the list before deleting in bulk** — the `build-edit-objects.py` near-miss is why.

## One batch file, names first, and a created person is linked to their names

Emma, 2026-08-30. Two changes to how the QuickStatements are generated:

- **One file, not two.** Names first, then everything else. Today it is
  `wikidata-garborg-day.qs` plus `wikidata-garborg-name-items.qs` and a run order to remember.
- **A person created in the run gets linked to their name items in that same run.** Today the
  name statements only reach people who already held a QID, so a new person waits a day.

## Always last — pinned to the very end of the file

**Bullets, not letters.** These were `A.` and `B.`; `CLAUDE.md` § *Queue items are BULLET POINTS*
covers lettering for the same reason it covers numbering, and she said so again on 2026-08-29.

- **Ensure the FOUR crons are running** — work-loop `3 * * * *`, auto-flush `15 * * * *`,
  status-report `42 * * * *`, and the **dead-queue-item sweep `45 * * * *`**, which Emma added on
  2026-08-31: *"Set up an hourly cron at :45 that says to remove dead queue items… Like items that
  are simply completed."* They are **session-only**: they die when the session ends and must be
  recreated at the start of the next one. This is not theoretical — every cron died in the
  2026-08-28 crash and none was recreated, which is why nothing ran between 00:03 and 06:00 on
  2026-08-29. Live in the 2026-08-31 session as `76ec2c05`, `f4332b23`, `cedb7fc4`, `21245a1a`
  — the ids recorded before (`82923e5b`, `0d208cfd`, `31df9ff8`) were a dead session's and are
  the reason to check `CronList` rather than trust this line.

  **The status-report cron carries no `AskUserQuestion`.** She barred it for eight hours from
  ~01:00 on 2026-08-31 — *"just move through the work and select the option that is consistent
  with what I've said earlier"* — so the two-hourly blocker question in `CLAUDE.md` was taken out
  of the cron text rather than left to fire while she slept. Restore it deliberately, not by
  default.

- **The three crons, as durable queue items.** Her instruction, 2026-08-27: *"For all of the cron
  jobs that I set up in the session. They are good and continue on with them, but also add them
  into the queue as actual items with he specification they are the cron jobs so they cget crossed
  off if he cron job finishes, but are a bit more stable."* Cron text lives only in memory, so the
  queue is the durable copy:

  - **Work-loop, hourly at :03** — sync, take the top actionable item, do it, commit with a
    `devlog.md` entry, push, report one line. Rails: never loosen a test, never claim verified
    without running it, no live Wikidata beyond the ledger refresh and `full_entities` before a
    correction, never generalise a named instruction into a mechanism, never invent a `.qs` she did
    not ask for.
  - **Auto-flush, hourly at :15** — commit and push anything pending, or report nothing pending.
    Never an empty commit.
  - **Status-report, hourly at :42** — reporting only. What advanced, queue state, whether the
    rails held, blockers each under exactly one not-done tag, and real test numbers from a run.

- **Run the status-report action once more** — an end-of-session summary of everything that
  happened this session.

### `P2600` constraint violations report — analysis AT THAT TIME, no pre-analysis

<https://www.wikidata.org/wiki/Wikidata:Database_reports/Constraint_violations/P2600>

Emma, 2026-08-29: *"we are gonna do analysis at that time (no pre-analysis) of how to
potentially elp wih wikidata genealogy with this stuff, it overlaps with some of our
entity resolution stuff do no think on it"*

So: nothing is to be investigated, measured or fetched about this before the item is
reached. The analysis is of how the constraint-violations report could help Wikidata
genealogy, and it overlaps the entity-resolution work.

### The clan labels may be much worse than we think — `Q45449130`

<https://www.wikidata.org/wiki/Q45449130>

Emma, 2026-08-29: *"I think that our clan things are much worse than you think, which is why I
never acually ran them adn I think I am seein at least some evidence."*

An analysis. Nothing was investigated when this was written.

## ⛔ `exports/post-merge/` — MOVED TO THE TAIL, 2026-08-29, her call

**Emma, 2026-08-29**, shown that 408 of the 412 falsifiable drops are real deletions:
*"For now leave these things and still run them, but put them at the end of the queue, I lean on
the idea of saving them but do not have bandwidth to process this now."*

So: **leave them in the tree, keep running the measurement, decide later.** She leans toward
saving the 408 rather than dropping them. Nothing is applied and no override is written.

`scripts/grade-post-merge-drops.py` → `reports/post-merge-falsifiable.tsv` is the standing
measurement — 408 `link-gone`, 2 still linked, 2 with no shared family, over 159 parents,
159 children and 90 spouses.

## ⛔ `exports/post-merge/` — resolving stale duplicates without throwing exports away

**Emma's design, 2026-08-24.** The problem: Geni has merged people our corpus still holds
twice, and *"we can't just throw out the earlier exports that contain stale individuals"*
— they carry thousands of people the merge needs.

**Her method, in her order:**

- **Export from the merged individual directly** where she created them, since she can
  reach the profile.
- **Where that is impossible, fall back to the earlier add-an-ancestor-then-export-from-them
  algorithm**, in the browser. That is `docs/export-seed-rules.md`.
- **The new GEDCOMs go in `exports/post-merge/`**, a directory with special logic: **a
  Geni record in there overwrites the same Geni ID from any other export** in the synoptic
  tree. Post-merge is newest and therefore right.
- **Export until every first-degree relative of every merged individual is present** in
  that directory. That is the stopping rule, not a count of exports.

**The economy of it is hers and it is the important part:** *"merged individuals cluster
together so we will not need to run an export on every one of them"* — one ball covers
many. The 13 `strong` rows bear this out: seven are Haji-no-muraji and three are Sugawara,
two lineages rather than thirteen scattered people.

**MEASURED 2026-08-26, and the answer is: do not write the relationship override.**
`scripts/measure-post-merge-override.py` → `reports/post-merge-override.tsv`.

Half the design already works: `genimerge.sources._post_merge_last` sorts the directory last,
so post-merge has the final word on every **single-valued** path. The other half — overriding
**relationships**, which are unioned and never dropped — was measured before being written:

| | parents | spouses | children | total |
| --- | ---: | ---: | ---: | ---: |
| would be **dropped** | 1,701 | 1,126 | 2,710 | **5,537** |
| of those, pointing at somebody **no post-merge ball reached** | 1,541 | 1,034 | 2,550 | **5,125 (93%)** |
| **only in post-merge** — what the override would gain | 0 | 0 | 0 | **0** |

**It subtracts 5,537 and adds nothing.** A post-merge ball stops at 5,000 people, so a relative
outside it is absent because the ball ended, not because Geni deleted the link. Applying the
override literally would delete 5,125 real relationships to buy nothing.

**412 drops are falsifiable** — both ends inside a post-merge ball, 160 parent / 160 child /
92 spouse. Those are the genuine *Geni deleted this link* candidates and the only population an
override should ever touch.

**Looked at as records, 2026-09-01** — `reports/post-merge-falsifiable.tsv`, all 412 with both
names, and a sample read by eye:

    Rivka Sirkes                    parents    Avraham Chaim Schor
    Avraham Chaim Schor             children   Rivka Sirkes
    Rivka Sirkes                    spouses    David HaLevi Segal "Turei Zahav"
    Reitze Horowitz 1st wife        children   Mordechai Zvi Halevi Horowitz
    Rachel Katzenellenbogen         spouses    Shimon Katzenellenbogen

**Two things the sample shows, and neither supports writing the override.**

- **They are the same few families.** Sirkes, Horowitz, Katzenellenbogen, Schor, Frankel — one
  rabbinical lineage, not 412 scattered errors. That is her own *"merged individuals cluster
  together"* observation holding, and it means this is one neighbourhood's worth of evidence
  rather than a corpus-wide pattern.
- **They read as real relationships, in reciprocal pairs.** `Rivka Sirkes → parents → Avraham
  Chaim Schor` appears alongside `Avraham Chaim Schor → children → Rivka Sirkes`. A link Geni
  had *deleted* would not usually survive in both directions in the older exports and vanish in
  both in the newer one; a ball that simply ended somewhere else would look exactly like this.

**So the override still looks wrong, now on the population that was supposed to justify it.**
That is a reading and not a proof — what would settle it is opening two or three of these
profiles on Geni and seeing whether the relationship is there today. That is hers, and it is
cheap: five profiles, not 412.

Depends on `reports/geni-stale-duplicates.tsv` (13 strong, 3 medium, 13 weak) and
`reports/geni-merges-performed.tsv` (180 survivors from her activity feed).

### English names ON GENI — MOVED TO THE TAIL, 2026-08-29, her call

**Emma, 2026-08-29**, asked whether her *"we don't actually need to edit your geni at all"* ruling kills this: *keep it but move it to the tail.* Still wanted, but it should stop being the first thing every work tick looks at and skips.

**The label half is NOT here and is not parked** — our `mul` and the CJK-only people are live work; see the analysis of 2026-08-29 (45 transliteration tokens block every remaining `ja`/`zh` label). What is at the tail is only the part that writes names **onto Geni**.

### English names ON GENI — the deferred half, and it is narrow

**Only the Geni-editing part was deferred**, not the English-label rule. Emma, 2026-08-29,
correcting my reading of her *"we just do not add a label"*: that sentence parked writing names
**onto Geni**, and nothing else.

**What the value is, when it happens:** *"the entire thing is whatever our pipeline puts as the
multilingual label on Wikidata. That is what our pipeline should be putting as the name, as in
Geni."* So the Geni name comes from our `mul`, not invented per-person and not taken from a
Wikipedia title.

**Her actual concern is CJK-only labels** — people whose Geni name exists only in Han/kana/hangul
and who therefore have no English form anywhere. Those are the ones this campaign is for.

**Already done and not part of this:** the `P1810` qualifier. It carries **what Geni literally
says** — `<private> Garborg`, `Private`, `Unn (Bitten) Garborg` — while the label beside it is the
normalised `NN Garborg`. Her rule: *"we do it with whatever's on Geni, not whatever is all in
Wikidata. This is a qualifier thing."*

Her closing note on how I handled this, kept because it is the correction: *"This is a relatively
well-defined task that you decided to transform into something crazy."*

### Get the REAL parents behind the NN placeholders — and FIRST, cost it

**Emma, 2026-08-29.** Two rulings, and the second governs whether the first ever runs.

**The representation.** *"Both parents are 'NN' placeholders. Pipeline generates names for them.
However we may attempt to gain the information of the parents. Imo this is too large to do right
now, but at the end of the queue we will have a task that goes to one of the siblings and save
their page so the parent names and potentially other people are added. If half siblings we go to
both siblings to clarify."*

**Page-saving was ABANDONED once, and the reasons are hers.** *"I gave up on the page-saving system
for a reason, because it was taking far too long. Part of this was due to extreme inefficiency and
frustration about your behaviour with it. Part of it was due to extreme inefficiency in terms of
lack of compliance from you on doing it at a reasonable rate. Part of it was that the actual site
itself was way too slow."*

**What is different now is SELECTIVITY, and that is the whole bet.** *"we're only saving pages in a
very selective way... selective enough that it's not going to be harmful... only to ones that are
important at a significant level."* The old campaign saved everything; this one saves only the
sibling groups that matter.

**So the FIRST deliverable is a time estimate, not pages.** *"My expectation still is this is going
to occur within a reasonable time frame, or it's not going to occur. By extension, as an extension
of this thing, I want you to actually measure how long it takes. Make predictions about how long it
takes."* Measure the real per-page rate, predict the total, and put that to her before saving a
single page beyond the sample the measurement needs.

**The half-sibling question decides how big the job is, and it is OPEN.** *"I don't believe we have
half-sibling information. We might have it, or we might not... I'm not the most clear on whether
half-siblings versus full-siblings are properly recorded like this or are accessible within the
actual chain information itself. I don't think it is, but I think it might be. If it is, then we'd
be able to preemptively do the calculation. If it was not within it already, we'd have to do
something much more exploratory."*

- If the chain data marks half siblings, the count is computable up front and one page per group
  suffices for the rest.
- If it does not, every group is potentially a half-sibling group, which means **two** pages each
  and a much larger, exploratory job.

**4,924 placeholder parents exist today** — 2,284 from the saved pages, 2,640 from the paths, one
pair per sibling group. Half siblings found on saved pages are currently skipped entirely rather
than given placeholders, because they share one parent and giving them two would assert a marriage
that did not happen.

**NOT NOW.** Emma, same message: *"This is an edit to the cube item. Do not do any fucking
calculations right now!"*

### Anonymise, shrink the CI checkout, then go public

**Emma, 2026-08-29**, on `reports/public-repo-analysis.md`: *"we will optimize the cicd revisions to
be small and do other things to optimize filesizes for the runners but can 100% do all this stuff if
we anonymize it properly"*

Three pieces, in her order:

- **Shrink what CI checks out.** A run does not need the 12.2 GB working tree — `.css` and
  `.download` under `geni-scraping/` are 1.9 GB of page furniture, and the compose step reads only
  the derived CSVs.
- **Anonymise.** The gate on going public. ~96,000 rows concern people Geni treats as private.
- **Then public**, which makes Actions minutes free and lets the daily emailed batch run.

**The constraint the design must start from:** the Geni profile ID is both the identifier and this
repo's primary key, so it cannot be hashed or dropped without breaking every join, the `P2600`
statements and the spines. Redacting content while keeping structure is the likely shape.

**The memory ceiling is untouched by any of this** — the merge peaks at 16.8 GB against a 16 GB
runner, so the synoptic tree still cannot be rebuilt in Actions without a larger runner.

### LAST ITEM — run `scripts/rebuild-everything.py`, then attach the batch

**Emma, 2026-08-29:** *"end of the queue is a rebuild of the tree and then after it is to build the
quickstatements and attach the file"*, and then, on being shown it was five scripts in a fixed
order: *"this explains why it's so hard: because it's not one script it's a bunch of scripts that
you need to remember to run in the right order. Nope make it one script that always ends by calling
the script that regenerates the quickstatements. This script is called as the last queue item."*

    python scripts/rebuild-everything.py

That is the whole item. It runs merge → display-names → derived family → derived facts → derived
labels → pack → `--compose`, stops at the first failure rather than continuing on stale inputs, and
ends with the batch. Then attach `reports/wikidata-garborg-day.qs`.

**Run it alone.** Step 1 peaks near 17 GB and has been killed twice when something else was running.
## ⛔ THE TAIL ALGORITHM — at the TAIL since 2026-08-30, her call

*"put these at the end of the queue instead of dropping them and start on the first queue item."* **The gap-size routing below is written against a MISSING-PERSON count that now reads 0 on every path** — the scraped-page GEDCOMs were ingested, so every path member is present. Apply it to the broken-link count in `reports/broken-links.md` instead: 85 of 979 paths, 102 links.

### The original method — Emma, 2026-08-18. Supersedes how the loop picks

Her framing: *"I think we can get through this really really quickly if we change our
approach here… I think a big part of it is the fact that our tail exports were just not
working nearly as well as we [expected]."* And her estimate of what it buys: *"you'll be
able to get through the tail maybe even just by the end of today."*

**What the loop was doing wrong.** It seeded a placeholder near a *missing* person and
exported from there. She wants the export **centred on the destination person** — the
isolate at the end of the chain — and the small gaps handled by a different mechanism
entirely.

### Work order: LONGEST paths first, then rebuild

Emma, 2026-08-18: *"you should be trying to target it by going from the longest paths to
the smallest paths… we can very easily run it with the top five longest paths having their
exports done and then we rebuild and so on and so on."*

**Her reasoning, and she has explicitly forbidden checking it.** *"the small paths are
likely ones where there are significant diminishing returns on nearby exports whereas the
large paths are likely ones that haven't had many exports and may be in very sparse
areas… I'm gonna bet that the longer paths will tend to be in more sparse areas where
there's more likelihood for it to just get the entire thing. Now I'm making this bet. I do
not want you to actually check whether this is true."* Running the method **is** the test.

**And it explains why the two-slot campaign underdelivered.** *"This was actually the
entire reason why it is that we were trying to hit the people who were in multiple paths.
The issue with the people in multiple paths was basically that… they were in multiple
paths but they were oftentimes in dense enough areas that they didn't really give the
extension that I was expecting."*

### Route by the size of the gap on that path

**Gap of 1–2 people — and 3 is safe too — DO NOT EXPORT.** Her words: *"a gap with one
person or two people is actually basically useless as a deliverable… It is not worth six
minutes to fill in something on the flat tail that is just covering one or two
individuals."* Instead: **open the person's page, click open the relatives section and
whatever else needs expanding, and save the page** into `geni-scraping/` — *not*
`geni_pages/`. The profiles get built from those saved pages later. *"We later on build up
the profiles from this separate thing, which won't really be a fallback thing. It'll be
another thing."*

**Gap of 4 or more — export, but from the RIGHT person.**

1. **Export centred on the destination person.** Go to the Wikidata-target/isolate at the
   end of the chain, walk their ancestors, export from there. *"I believe most of the time
   this is just going to fix it and it's going to get that person connected."*
2. **If the destination is already present and already exported from, go to the midpoint**
   of the remaining chain and attempt there.
3. **Recurse.** Her worked example, verbatim in substance: a seven-person chain → export
   from the Wikidata target → it clears two → a five-chain remains → attempt at the
   midpoint → that gets the middle three → what is left is two chains of two → and those
   are finished by the page-saving method, not by more exports.

**The point is not a complete family tree.** *"it doesn't matter that the entire family
tree is all consistently there."* The deliverable is the chain being connected.

### Also instructed, same message

- **Retry every person previously bailed on.** *"A locked profile almost never means that
  every single individual in the tree is locked. The stuff is self-healing here but you
  still have to actually attempt them again. I am instructing you to attempt these
  people."* Four remain: Anna von Mecklenburg-Schwerin, Anna Charlotta Stenius, Ola R
  Sande (retry in flight), Artur Lidman.
- The page-saving mechanism needs the **immediate relatives** of the person being
  connected to Wikidata, which is why the relatives section must be expanded before the
  save.

**Current shape of the problem**, so the routing can be applied: 545 paths, median 8
missing each, max 33. **24 paths need 1 person, 37 need 2** — those go to page-saving.
The 4+ paths are where exports go, seeded on the destination.

## The midpoint export campaign — her batch of 2026-08-17

**Open the family-tree index page, never the profile page.** Emma, 2026-08-17:
*"rather definitively this kind of thing
https://www.geni.com/family-tree/index/6000000085113755501 is a better page to open up
for them rather than the pages you opened."* Recorded in `CLAUDE.md`; the first 50 were
opened as `/people/x/<id>` and should have been `/family-tree/index/<id>`.

**Four exports integrated**, `exports/midpoints/`, all `Forest`, all exactly 5000
people, seeded on placeholders she made at the midpoints of path gaps:
`6000000227288930948` `Wilchen /Tybekken/` · `…289663852` `Øystein /father of Berta/` ·
`…289604840` `Michel /Jude/` · `…289792822` `Björn /father of Prinsessan/`.

**Done for this batch:** re-merged to 472,999 people; measured — the four exports closed
**199 chain people**, held 3,337 → 3,536 and steps held 66.5% → **67.7%**; the next 50
midpoints picked off the regenerated ranking and opened as family-tree pages.

**No already-opened filter, and no accumulating handoff.** The regenerated ranking drops
a closed person by itself — eight of the first batch's fifty are gone from it — so the
filter I added excluded 42 people who are still gaps and pushed her down to weaker
candidates. Both corrections are in `CLAUDE.md`.

**The loop does NOT re-merge, and the ranking is slots.** Both her corrections of
2026-08-17. `scripts/find-chain-gaps.py` answers *do we hold this person* straight off
the export files — 18 seconds against five minutes and 4.5 GB, and it cannot go stale.
Ranking is by **path slots filled**, her call: *"the midpoints for path segments were
making some assumptions: an assumption of relative equality of presence in slots, but I
don't think this is true anymore."* Slot counts run 10 down to 1, so they are not equal.

**The loop, per new export:** place it in `exports/midpoints/`, run
`find-chain-gaps.py --open 10`, open the ten. Nothing else. Currently **held 3,655, gap
6,632, 7,174 unfilled slots** over 251 exports. Her framing: *"I think I can get those
paths cleared soon."*

## THE EXPORT LOOP — 2026-08-17. At the TAIL since 2026-08-30, her call

**Emma, 2026-08-17:** *"this thing here is currently essentially the absolute top
importance task to do. This full sequence and all this other stuff that we're
doing, we should be operating on sequentially through the queue, with this stuff
being the very first thing."*

**The job changed shape.** *"From now on it's your job to create the individual and
then do other stuff."* Creating the export seed on Geni was her manual labour; it
is now mine. `docs/export-seed-rules.md` is the method — five tiers, patronymics
first — and it is not repeated here.

**A master profile is a skip, not a problem.** *"Sometimes you'll just run into a
situation where it looks like you should be able to add an individual but you
can't. If you run into anything like that then just don't bother that much and
skip through it."* Move to the next slot; do not investigate, do not report it.

### Phase 1 — the seven seeds she created herself

`export_individuals_to_do_on_your_own.txt`. **Forest, 5000, one at a time**, each
zip on disk before the next export is queued.

- `6000000227258546877` Anders father of Anna
- `6000000227291195824` NN Hersleb
- `6000000227289933834` Sunes Sterenius
- `6000000227291086839` Rasmus Friis
- `6000000227291028845` Håvard Øye-in-Heskestad
- `6000000227290969847` Karl father of Carl
- `6000000227289886830` Lewis father of Hugh

Precedent, same morning: the `NN` mother created at `6000000227291886826` (mother
of Rodrigo de las Varillas) was created, exported and downloaded end to end under
Chrome automation. That is the whole manual workflow running without her.

### Phase 1b — the Ettinger bridge, and it jumps the queue ahead of the top ten

**Emma, 2026-08-17, mid-run:** *"You run this one first before you do the top 10…
If you get started with the top 10 because you didn't get the message until you
started it, then immediately after the last one of them you run this one."*

The tree is `https://www.geni.com/family-tree/index/6000000002764956522`,
**Mordechai Zeev Ettinger, A.B.D. Lwow (1804–1863)**. She thinks one Forest export
seeded here may be enough to merge the isolated 344 into the world tree on its
own: *"we'll see if it just connects to the world tree just based off of this
export alone. If it does then that'll be great. We'll have a synoptically
integrated tree."*

Done: seed created at `6000000227293218831` — `NN`, mother of
`Sarah Landau (Ziskind)`, tier 3, three generations up the Ettinger line. Forest
export run from her.

**If it does not connect**, she is adding a second person to the paths who will
also sort it out. Do not start improvising a fix — wait for that.

The 344 are the Ettingers, all of them in
`exports/edges/export-Forest-6000000227256597825.ged`
(`scripts/which-export-holds-component.py`).

### Phase 2 — the top-ten loop, and it repeats until the paths are flat

**Only once every Phase 1 zip is down.** Then, on repeat:

- Find the **ten people who appear most often across the relationship paths**
  (`scripts/find-chain-gaps.py`, ranked by slots).
- For each of the ten, **sequentially**: create the export individual per
  `docs/export-seed-rules.md`, run the Forest export, download the zip.
- Finish all ten, **then** integrate that batch of ten into `exports/`.
- Re-run the check, take the new top ten, go again.

**The stopping condition is flatness, not exhaustion.** Emma: *"until eventually
we end up in a situation where every individual in these paths only shows up
once… every individual in the path is there an equal amount, which would in this
case be each one of them shows up exactly once."*

### Phase 3 — midpoints, when and only when the paths are flat

Once no person outranks another by slot count, rank by the **midpoint of each path
sequence** instead. Her reasoning: a person created at a midpoint is where the
Forest walk reaches and then spreads out from.

**She expects this phase mostly not to fire.** *"I don't think it's going to be
that common because the midpoint people are more rare."* So do not build machinery
for it ahead of time.

### Phase 4 — the sparse regions, after every bridge is cleared

*"The second thing in the queue, after we've cleared all of the bridges in these
files."* From the sparseness analysis (`reports/density.md`), take the regions
**exported from exactly once**, and within those go for the ones **deepest down**.
Create an individual there and run the same create → Forest → download loop.

Her reason: *"these are the places that are likely going to have more people that
we might not have encountered before."* Sampled once means the neighbourhood was
touched and never returned to, which is exactly what the doorway column in
`density` is measuring.

Two of the three objectives set today come out of this loop running to completion,
and it runs unattended.

---


## One pipeline, one output file — a stale name file is dangerous

**Emma, 2026-08-31:** the name generation must always be the same run as the day file. Two files
built by two scripts means one can be from an earlier run, and nothing on the file says so — it
happened today, when the day file was 14:32 and the name file 12:16 and only the mtimes gave it
away.

- **One output**, produced by one pipeline, with the names **at the end of it**.
- The run order it encodes is unchanged: individuals, then names, then relationships. Her order
  is structurally rigid.

**Note the placement disagrees with § *One batch file, names first, and a created person is linked
to their names***, which says names come first. This item is the later statement and wins; the
older section is cross-referenced here so the two are not solved twice.

## Create the fathers the patronymics imply — AFTER the name work, her call

**Emma, 2026-08-15:** *"If they are patronymics I actually think I'm going to want to add items
for the hypothetical fathers that are implied to exist from the patronymics… They're going to be
created because they are inferred from the existence of the patronymic."*

**The population, measured 2026-08-31:** **75,903** people carry a patronymic and have no recorded
father, over 3,993 distinct implied father-names.

**Emma, 2026-08-31:** *"we only create the people after a lot of other stuff is resolved. I'll leave it for later."* So this sits at the tail by her placement, not by a blocker.

**The obstacle is that the stem is not the name.** Stripping
`-sen`/`-son`/`-datter` gives a string that matches the father's actual given name **42.1% of the
time** — measured against **272,617** bearers whose father *is* recorded, so this is checked
against reality rather than argued. Three distinct failure modes, all in the sample:

| patronymic | naive stem | the father actually is | why |
| --- | --- | --- | --- |
| `Olsen` | `Ol` | `Ole` | the stem is not a name at all — 4,349 of them |
| `Jakobsdotter` | `Jakobs` | `Jakob` | the genitive `s` is kept |
| `Jonsen` | `Jon` | `John` | spelling variance |
| `Slawson` | `Slaw` | **`James`** | not a patronymic — an English surname ending in `-son` |

Creating from the naive stem would mint on the order of **44,000 wrong items**, including 4,349
for a man called *Ol* who never existed. `Ol`, `Ander`, `Han`, `Lar`, `Nil`, `Jen` are the top six
implied names and **not one is a name**.

**What would make this safe, in order:** a rule that recovers `Ole` from `Olsen` and `Jakob` from
`Jakobs`, validated the same way — against the 272,617 known fathers, reporting the hit rate
before anything is emitted. `namemodel.patronymic_or_surname` already uses the father to decide
*whether* a token is patronymic; this needs the inverse and does not have it.

**Sourcing, settled so it is not the open question any more.** The child's patronymic is the
evidence and it is recorded on the child's Geni profile, so the reference is `S2600` on the
**child's** id — not the father's, who has none. `P887` *based on heuristic* is the property that
marks the value as inferred rather than recorded; **its value item is not chosen** and must not be
guessed. `pq:P887` is used only single-digit times across Wikidata, so there is no convention to
follow and the reference-position query times out; pick the item deliberately when this is built.

## LAST — `AskUserQuestion` on the two patronymic decisions that are hers

Her instruction, 2026-08-31: the standing NEEDS-DECISION pair goes to her as an
`AskUserQuestion`, **as the last item in the queue**. Not before then — everything else runs
without it, which is why it sits here rather than at the front.

Two questions, one tool call each, with real options:

- **The 179 patronymic tokens still genuinely ambiguous.** Down from 546 once sex and writing
  system were applied; what is left is several items that are all male, all Latin, and all
  plausibly the same name. This is § *One name item per USAGE* and hers. Default in force
  meanwhile: skip them, emit the other 4,747.
- **`P407` *language of work or name* on the patronymic items we create.** 59% of the 631
  existing ones carry it, and nothing in a token supplies it — `Andersson` reads Swedish and
  `Andersen` Danish-Norwegian by convention, not by rule. Default in force meanwhile: omit it,
  because taking it from the export or the region is the geography inference `CLAUDE.md` forbids.

**Both defaults are already live and neither blocks anything**, so this is a question about
whether to do *more*, never a stall. Show her the actual candidate items, not a summary — the
`Carl`/`Johan`/`Olof` lookup is what made the last one answerable in one line.

## Patronymic residue: `Nils`/`Nicolaus` needs a form table, not a letter rule

The letter-level folds are done and measured — `d`/`t` and the inner `h`, each sampled by hand
before it shipped. What is left cannot be reached by any spelling rule:

- **`Nilsson` with father `Nicolaus`.** `Nils` is a *form* of `Nicolaus`, not a spelling of it;
  the skeletons are `nls` and `nkls` and no fold that joins them leaves anything else apart.
  Same shape: `Lars`/`Laurentius`, `Ola`/`Olaus`, `Jon`/`Johannes` where the vowel run differs
  too much.
- **What would work is a short table** of Scandinavian given-name forms — the Latin church form
  against the vernacular. It is data, not an algorithm, and it should be built from the corpus:
  take fathers whose given name is Latinate and whose children carry a vernacular patronymic, and
  read off the pairs rather than inventing them.

Measure first and sample the rescues by hand. That is what showed `d`/`t` was safe, showed the
inner `h` was safe, and is the only reason either shipped.

**At the tail with the rest of the patronymic modelling.** Emma, 2026-08-31: *"all pstronymic modelling is at the end now"* — she is working down the queue and three consecutive items landing on patronymics was a placement mistake of mine, not her priority.

## LABELS, IN HER ORDER — one step per language, every individual at once

**Emma, 2026-08-17**, after being shown the 364 structural placeholders with no label:
*"Put an item at the end of the queue that finds these kinds of ones where the label
has this stuff already in it, and normalizes them into proper things based on our
rules, and then tasks at the end that in order: makes en labels for every individual
(so Japanese gets transcribed), and then mul gets made for every individual (almost
always derived from en), and then the Japanese gets made for all languages, and then
the Chinese gets made for all languages, and then after we continue with the other
universal languages. Note that these are all distinct items for the language so all of
the en labels are done at the same time as one step, and then mul, then ja, then zh,
then others."*

**This fixes the ordering `emission-spec.md` had.** That file says `mul` comes from the
Latin name and `en` comes from `mul`. Her order is the other way round and it is the
one that works for a person with no Latin name at all: **`en` is made first, by
transcribing**, and `mul` is then *"almost always derived from en"*. That is what gives
the 806 Han-only people a `mul` — there was no route to one before.

**Each language is one step over the whole population, not a per-person loop.** Her
words. So the batches are `en` for everybody, then `mul` for everybody, then `ja`, then
`zh`, then the rest — never a person walked once and labelled in seven languages.

- **Normalise the labels that already carry a marker inside them.** The census is
  built — `scripts/build-marker-label-census.py` → `reports/marker-labels.csv`, both
  stores — and it splits the job into three populations that need different handling.
  What is left is the *normalisation*, which is emitting from that CSV:

  - **A marker leading a real surname — keep the surname, marker to `mul`.**
    `unknown Bloomfield` → `mul: NN Bloomfield`, and a description in the local
    languages. This is the bulk of it and the Wikidata side dominates: 18,280
    `unknown`, 3,362 `nn`, 480 `n`, 260 `?`, 60 `n.n.`, 35 `private`.
  - **A real name with a marker wedged inside it — strip the marker, keep the rest.**
    `Catherine unknown` → `Catherine`, `Nechama (?) Heller` → `Nechama Heller`,
    `Hadaburg N.N. Gräfin im Saalgau` → `Hadaburg Gräfin im Saalgau`. Mechanical, no
    judgement, ~1,950 labels. `is_placeholder_label` reads only the head token, so
    every one of these currently ships as a name.
  - **A description already sitting in the name slot** — 1,222 Geni people and 1,508
    Wikidata items in English, plus **~5,400 in CJK** and 249 behind an honorific.
    `wife of` 871, `daughter of` 605, `son of` 241, `mother of` 234, `nieto de` 58;
    `室` 2,565, `氏` 1,613, `娘` 617, `某` 311, `妻` 210, `母` 100; `Mrs.` 249,
    `Miss` 30. **`mul` gets `NN`** — Emma, 2026-08-17: *"And NN for mul there"* — plus
    the real surname where the description leaves one standing (`謝氏` → `NN 謝`,
    `信秀正室 織田` → `NN 織田`). The description itself is kept as the local-language
    label, which is where it already belonged; it is written, just in the wrong slot.

  **The three vocabularies are now one** — `scripts/labels.PLACEHOLDER_FORMS`, imported
  by the preview, the structural walk and the census instead of each carrying a copy.
  Strictly additive: all 27 forms the copies held are in it, plus 19 found by
  measurement, so nobody previously screened stops being screened. `NOT_A_NAME` is
  deliberately untouched — that decides what `label_for()` **empties** and she has ruled
  on it twice; these sets decide what a **marker** is. Widening detection is not
  widening suppression.

- **`en` for every individual, as one step.** Includes the transcription she names:
  a Han-only or Cyrillic-only or Hebrew-only person gets an `en` made for them.
  **CJK → English is agentic, never programmatic** — *"from CJK to English do not
  remotely try to do any kind of programmatic transliteration because they all suck.
  But AI almost always knows Japanese to Romaji."* The culture question comes first:
  陳 is *Chen*, *Chin* or *Jin*, and *"the tree settles it, via neighbours and which
  exports they came from"*, never the name. 806 Han-only among the structural
  placeholders alone; the corpus figure is larger and is what this step must count.

- **`mul` for every individual, derived from `en`.** *"Almost always derived from en"* —
  so the exceptions are the thing to find and report, not to guess at.

- **`ja` for every individual — and the native construction is the template.**
  **Emma, 2026-08-17:** *"That relationship description should be the template for how
  we generate Chinese and Japanese nn suppleting labels."*

  This unblocks the thing `ja`/`zh` were deferred for. The recorded objection was that
  a generated Japanese description *"would come out `Gerard Spencerの娘` with the name
  untransliterated"*. The corpus already contains ~5,400 CJK relationship descriptions
  written the native way, with no `の` and no borrowed grammar, and those are the model:

      織田敏信娘        daughter of Oda Toshinobu   <name>娘
      信秀正室 織田      principal wife of Nobuhide  <name>正室
      古河某妻          wife of a certain Kogawa    <name>某妻
      謝氏             the Xie-clan woman          <surname>氏
      母 陳            mother, of the Chen         母 <surname>

  So an unnamed person whose relative is recorded in Han characters gets
  `ja` = `<relative's name><suffix>`, taking the suffix from the table the records
  themselves use. **It only works where the relative's name is already CJK** — which is
  exactly the population that has no `en` and is otherwise unreachable, so the two
  problems solve each other. Where the relative is Latin-only the `ja` label still
  waits on the transcription step.

  Han-only people already have a `ja` label, as the kanji written: *"If the name is
  solely in kanji, then the Chinese and Japanese labels are both the same for it."*
  The work is everybody else.

  **`室`/`正室`/`側室` are not interchangeable and must not be normalised to one.**
  Principal wife, concubine and consort are different statements about a person. Pick
  the suffix the source used; do not choose one when generating from scratch — for a
  generated label the plain relationship word is the safe form and the specific rank is
  something only the source can supply.

  **STEP 3 PART-BUILT — `ja` where it needs no invention.**
  `scripts/build-ja-label-batch.py` → `reports/wikidata-ja-labels.json`, **41,952 edits**:
  37,405 from the name as written (Japanese uses a Han name unchanged) and 4,547 from
  Wikidata's own `ja` label.

  **TO DO — the hard half, 406,713 people:** English→katakana, plus 5,293 hangul-only names
  deliberately skipped (a `ja` label must not be the hangul). Emma's method is a hand-built
  table — *"hand-built tables, except CJK → English"* — and turning `Brodsky` into
  `ブロツキー` has real failure modes: syllabification, long vowels, and the fact that
  established Japanese spellings of European names are conventional rather than derivable.
  Sized, not guessed at.

  **Then `zh`, then the rest.** Middle initials follow
  `reports/middle-initial-wikidata-practice.md`.

- **`zh` for every individual.** Same string as `ja` for a Han name; the 291 people
  whose name carries **kana** are the ones needing a real Chinese form.

- **Then the other universal languages** — `hi` · `ar` · `ru` · `el` from her earlier
  list, each its own step over the whole population.

### First, the bug underneath all of it — 646 labels deleted by an ordinal sign

Found 2026-08-17 while answering *"what the FUCK are these 364 placeholders"*.

`scripts_of` in `scripts/build-display-names.py` classifies each character by the first
word of its Unicode name. `º` is `MASCULINE ORDINAL INDICATOR` and `'º'.isalpha()` is
**True** in Python, so it becomes a script called `Masculine`. `derive-labels.py` then
reads `scripts = Latin+Masculine`, calls the name **mixed-script**, and refuses it as
an `en` or `mul` label.

**646 people lose their Latin label to this**, every one an Iberian noble whose title
carries an ordinal: `Afonso de Bragança 1º conde de Faro e 2º de Odemira`,
`Maria da Cunha 3ª senhora de Basto`, `Mª Manuela Fernández de Córdoba`,
`João Soares de Sousa 3.º Capitão donatário da ilha de Santa Maria`. The same fault
hits `Feminine` (86 records), `Modifier` (105), `Superscript`, `Micro` and `Unnamed`
(12) — **943 NAME records** carry one of these pseudo-scripts.

**A character that is not a writing system must contribute no script**, rather than
being called Latin: `º` says nothing about what script a name is in. Then
`1º senhor de Baião` is Latin and the label survives. Fixing this means re-running
`build-display-names.py` → `derive-labels.py` → every label emitter, which is the whole
cache chain `CLAUDE.md` warns about.

**At the tail, her call 2026-08-31.** It is a mass operation over the whole population and the live work is hyperlocal, so it was being read and skipped every tick. Nothing about it changed except its position.

## THE VERY LAST ITEM — the sequence that ends with the daily email

**Emma, 2026-08-31**, shown the chain and confirming it: *"yep that's correct so put that
sophisticated sequence as the last queue item."* Four steps, strictly in order, each one the
precondition for the next. It absorbs the two sections that used to state pieces of it
separately.

### 1. Shrink what CI checks out

The working tree is **12.2 GB**, of which **1.9 GB** is `.css` and `.download` page furniture
under `geni-scraping/` that no build step reads. The merge peaks at **16.8 GB against a 16 GB
runner**, so the synoptic tree cannot be rebuilt in Actions at all — but it does not need to be:
the compose step reads only the derived CSVs, so the runner never needs the tree. Establish what
a run actually opens, and check out that and nothing else.

### 2. Anonymise

The gate on going public. **~96,000 rows concern people Geni treats as private.**

**The constraint the design starts from:** the Geni profile id is both the identifier and this
repo's primary key, so it **cannot be hashed or dropped** — every join, every `P2600` statement
and every spine runs through it. Redacting content while keeping structure is the likely shape,
and § *Redacted people go in* is the precedent: what is informative is the structure, and none of
that is redacted.

### 3. Make the repo public

Her decision, 2026-08-31: *"the repo will be public lol."* Actions minutes become free, which is
what steps 1 and 2 exist to earn.

### 4. Then the two things that were waiting on it

- **The daily email.** `reports/wikidata-garborg-day.qs` reaches her inbox every day and she runs
  it by hand — *"not wikidata editing but instead emailing me the daily quickstatements file."*
  `schedule:` plus `workflow_dispatch:` only; `CLAUDE.md` § *Cost* forbids `push:` triggers.
- **New tests resume.** `CLAUDE.md` § *NO NEW TESTS* is scoped to exactly this — *"no more tests
  until we got the ci/cd with github actions as a public repo running"* — so the moratorium ends
  here rather than by anyone deciding it has.

**Nothing in this chain is blocked and none of it is urgent.** `2026-09-01` passing changes
nothing on its own: the edit path stays unused, its `START_DATE` constants stay as the rail, and
the batch keeps reaching her in chat exactly as it has been.

## Model the succession CSV into statements

`reports/succession-and-ordinals.csv` is built and comprehensive — 221 rows: Samaritan all 132
positions, Izumo 53, Senge 22, Kitajima 14. This item is turning it into Wikidata statements.

- **`P7338` *regnal ordinal*** — a qualifier on the `P735` *given name* statement, per
  `name modelling.txt`, for the 111 rows carrying one. Never as a middle name.
- **`P39` *position held* with `P1545` *series ordinal*** — the number in office, for all 221.
  `reports/wikidata-samaritan-succession.json` already models it this way for 18 priests, so the
  Japanese houses and the rest of the Samaritan line extend a built shape.
- **The office items differ per family** and only the Samaritan one is known: `Q678510`
  *Samaritan High Priest*. Izumo Kokusō, Senge and Kitajima need theirs identified or created.
- **A row with no `qid` cannot carry a statement yet** — 23 of 132 Samaritans have one, and the
  Japanese side is better at 51/22/14. That is the ordinary both-ends-need-a-QID rule, not a
  blocker: what cannot run today is a later day's batch.

**Two things the CSV records that must not be lost in emission:** `geni_status` says how each
Geni id was established — succession number confirmed, sole match, her bio link — and the 38
Samaritan positions absent from the corpus are a near-contiguous run (1, 2, 3, 31, 59, then 81
onward), which is one unexported neighbourhood rather than 38 misses.

## THE LAST ITEM — `pykakasi` is fine AS A FALLBACK; verify it because she has been burned

**Emma, 2026-08-31**, on finding it installed: *"I can say for a fact that that library sucks for
converting Kanji to Hiragana. So with that being said, I'm skeptical of it... I'm gonna guess it's
probably easier for it to do European words than Kanji to Hiragana... but I am going to want to do
a bit of due diligence on it to make sure that it's getting stuff right."*

**The two directions are different jobs, and the one she knows it fails at is not the one we
need.** Kanji → hiragana is a *reading* problem: the same characters take different readings per
person, which is why `P1814` *name in kana* exists as a property rather than being computed.
European → katakana is a *transcription* problem, and her guess is that it is the easier of the
two. That guess is plausible and is not evidence.

**Her position, clarified the same day: as a fallback it is fine.** *"I think probably as a
fallback, it's fine... It's only for edge cases. It's just... I have been burned by that library
in the past, so I wanna make this stuff clear."*

So this is **not a gate**. A fallback fires on the tokens nothing else renders, which is a small
tail by construction, and a wrong katakana rendering there is inside her standing rule that
*"incorrect representations in katakana are totally acceptable"*. What she is asking for is that
the scepticism be written down rather than discovered again by somebody who does not know she has
been burned.

**MEASURED, 2026-09-01. Her scepticism is correct and the number is 6 of 10.**

Ten Japanese names whose readings are not in doubt, kanji → hiragana:

| name | pykakasi | the reading |
| --- | --- | --- |
| 藤原道長 | ふじわらどうちょう | ふじわらのみちなが |
| 菅原道真 | すがわらどうしん | すがわらのみちざね |
| 源義経 | みなもとよしつね | みなもとのよしつね |
| 小野妹子 | おのいもこ | おののいもこ |

**All four failures are the same failure, and it is ours.** The classical `の` between clan and
given name is dropped, and where the given name has a Sino-Japanese and a native reading it takes
the wrong one — 道長 as *dōchō* rather than *Michinaga*. That is precisely the population this
corpus is full of: Fujiwara, Sugawara, Minamoto, Taira. The six it got right are Sengoku and Edo
names with regular readings.

**So it is worse than 60% for us, not better.** She said *"I can say for a fact that that library
sucks for converting Kanji to Hiragana"*, and on the names we actually hold it does.

**Nothing depends on it.** `pykakasi` is installed on the machine and is referenced in exactly one
place — a docstring in `scripts/build-cjk-romanisation.py` saying it is *not* used, because the
romanisations are read out of Wikidata's own name items instead. So this measurement changes no
behaviour; it records the scepticism so nobody reaches for the library without knowing.

**`P1814` *name in kana* therefore stays agentic**, which is what `CLAUDE.md` already says and
what this measurement now supports rather than merely asserts.

- Compare `pykakasi` against `scripts/translit_no.py` and against the **317 hand-written rows** of
  `reports/garborg-name-transliterations.tsv` that the engine did not itself write. That file is
  the only ground truth in the repo, and `translit_no` scores **46% (ja) / 41% (zh)** on it — so
  there is a number to beat rather than an impression to form.
- The known gap in `translit_no` is **gemination and vowel length** — `Anna` → `アナ` where the
  hand form is `アンナ`, `Aagot` → `オーゴト` against `オーゴット`. Whether `pykakasi` gets those
  right is the specific question worth answering first.
- **Do not test it on kanji.** She has already settled that direction and it is not what this
  would be used for.

**And look for something better.** Her words: *"I think that there might be some sort of better
system than that library. Not one hundred percent sure."*

**Nothing depends on this today.** `translit_no` is what runs, the funnel is wired, and the ja/zh
gate refuses nobody. This decides whether `pykakasi` becomes the fallback under it — not whether
labels get made, and not whether it may be used at all.

## THE LAST ITEM — the tokens the transliteration funnel cannot read

**Emma, 2026-08-31: *"put these tokens at the end of the queue."*** So they are here and nothing
was investigated further.

After the funnel ran over the placeholder population on 2026-08-31 — table **4,054 → 18,410**,
14,356 tokens added — **1,075 tokens were left out as unreadable**, and `ja`/`zh` is still missing
on **17,077** of the 39,691 placeholder edits.

**The two remainders are different problems and should not be treated as one:**

- **7,562 have no `en` label at all.** No named relative at any distance, so there is nothing to
  build `<name>の娘` from. A transliteration fix cannot reach them; they need something other
  than a relative or they stay bare `NN` in `mul`.
- **~9,500 have an `en` label and one unreadable token in it.** These are the ones this item is
  about.

**Most of the unreadable ones are not names.** The reported sample is `!\`, `"`, `"AMNY"`,
`"Abbahu"`, `"Abu`, `"Adak-Jarni"`, `"Alexios`, `"Alviðrukappi“`, `"André"`, `"Annie"` — quoting
artefacts where a nickname's opening quote has been glued to the token. `Карлов` is Cyrillic and
`<private>` is a redaction marker that should never have reached a name field at all.

**So the first question is how many are actually tokens.** Stripping stray quotes may close most
of it without touching the reader; a Cyrillic name is a different engine; and `<private>` is a bug
upstream in whatever built that label.

`python scripts/extend-transliterations.py --placeholders` prints the current list.

## THE LAST ITEM — wire `hi`, `ar`, `ru`, `el` into the label batches

`scripts/translit_scripts.py` renders all four and **nothing emits them yet**. Her call,
2026-08-31: at the tail.

- The four join `ja`/`zh` in the emitters that already build CJK labels —
  `build-garborg-day.py`, `build-placeholder-label-batch.py`, `build-nn-label-batch.py`.
- **Read a sample by eye before wiring, every time.** Four manglings were caught that way when
  the module was written — `Bjørn` → `бйёрн`, `Johannes` → `Ёханнес`, `Maria` → `مرا` and
  `मरिअ` — and none was visible in the tables.
- **`ar` is an abjad and loses short vowels.** `Arne` and `Aren` collide. Decide deliberately
  whether an Arabic label is worth having on that basis; the module does not decide it.
- Her standard governs what is acceptable: *"incorrect romanization or incorrect representations
  in katakana are totally acceptable. An incorrect name is not."*

## THE LAST ITEM — `BET x AND y` properly

**Emma, 2026-09-01: *"I'll do between more later."*** So what ships today is the simple reading and
this is the considered one.

**What ships now.** `scripts/datequals.py` emits `P1319` *earliest date* at the value's own
precision and `P1326` *latest date* at the end year, precision 9. **All 7,797 `between` dates in
`reports/derived-facts.csv` carry an end year** — measured, none is missing — so the
no-end-year fallback in that module never fires on current data and exists only against a future
parse gap.

**What is left to think about, and none of it is urgent:**

- **The end is stored as a YEAR only.** `BET 5 JUL 1735 AND 5 JUL 1737` keeps the start's day
  precision and loses the end's, because `derived-facts.csv` has `birth_date_year_end` and no
  month or day column. `genimerge.dates` parses the full end date; the derived CSV is where it
  narrows. Widening that is a schema change to a 200 MB file that 44 scripts read.
- **Which date should the statement's VALUE be?** It is currently the start. For a range the
  midpoint or the start are both defensible, and Wikidata practice varies — some items put the
  range only in qualifiers and give the value a low precision covering both ends.
- **A range spanning a century boundary** — `BET 1798 AND 1802` — arguably wants precision 8
  (decade) or 7 (century) on the value rather than a year it does not have.

**Nothing depends on this.** The current form asserts less than it knows rather than more, which
is the safe direction, and it is a strict improvement on the bare value it replaced.

## THE LAST ITEM — `wikidata-placeholder-labels.json` is 74 MB and just quadrupled

It went **18 MB → 74 MB** on 2026-09-01 when the stale relationship-label preview was rebuilt
(39,691 edits → 158,618). It is tracked, and GitHub refuses a file over **100 MiB**, so one more
growth of that shape breaks a push rather than warning about it.

`scripts/pack-derived.py` already solves this for the four big CSVs — gzip the file, commit the
`.gz`, gitignore the plain one, and `--unpack` after a clean clone. Only
`build-en-label-batch.py` reads this JSON, so unlike the CSVs there is no forty-reader problem to
work around.

**Do not act on the size alone until it is near the limit** — the point of writing it down now is
that the next rebuild is when it would surprise her.

## THE VERY LAST ITEM — a GitHub Pages site documenting the repo

**Emma, 2026-09-01:** *"an item at the end of the queue: a github pages site built with actions
that documents generally what the repo is doing with different things, its data modeling and
algorithms and such. This is the last item though only after all the other stuff."*

**After everything else. Not before.**

- Built by a workflow, published to Pages — the repo went public 2026-09-01 so Pages is free.
- **What the repo is doing**: merge Geni exports into one tree, reconcile against Wikidata,
  generate the edits that create the missing people.
- **The data modelling**: how a name becomes `P735`/`P734`/`P5056` with `P1545`, `P7338`, `P3831`;
  how a GEDCOM date modifier becomes `P1480`/`P1319`/`P1326`; the `mul`-is-the-real-label rule and
  the married-name ordering; the NN/redaction algorithm.
- **The algorithms**: the daily ring one hop off the Wikidata subgraph from Arne; the zipper join
  and its provenance chains; the density and descendants seed rankings; the transliteration funnel.
- Generated from what is in the repo rather than hand-written prose that will go stale — the
  `CLAUDE.md` sections and the module docstrings already carry most of it.
