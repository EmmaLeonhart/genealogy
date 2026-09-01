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

## KOREAN — done, except one decision shared with `ja`

**Her instruction, 2026-09-01:** *"korean is extremely important on par with Chinese... cjk
includes korean"*, and *"put the korean stuff at the beginning of the queue"*. It was, and it is
built — `devlog.md` 2026-09-01 has the detail. 1,033 hanja at 72% of CJK names, Latin → Hangul at
97% of 1.29 M, a `ko` column at 18,535 of 18,536 tokens, the creation gate on all three languages,
and `build-ko-label-batch.py` at 33,725 labels.

**What remains is ONE decision and it is not Korean's alone.** 1,278,536 Latin-named people can be
rendered into Hangul at 97%, and `build-ko-label-batch.py` withholds them for the same reason
`build-ja-label-batch.py` does: transcription is not reading, and English → katakana is the
direction her method reserves for a hand-built table. Emitting it under `ko` while `ja` withholds
the identical thing would be the two batches disagreeing about what counts as honest.

So the question is for `ja` and `ko` together: **does a rule-based transcription of a Latin name
count as a label we are willing to publish?** If yes, both batches grow by over a million. If no,
both stay as they are. NEEDS-DECISION, hers.

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
| CJK | `ko` **DONE**. `P1814` kana has an **empty population** — no correctly-identified Japanese person has an item; see `reports/culture-classifier-check.md` |
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

**`reports/label-gap.csv` is the census of who is left**, from `scripts/census-label-gap.py`,
re-run 2026-09-01 **after** the redaction fix. Every one of the 156,738 people with no label, with
what each can actually receive:

| | count | |
| --- | ---: | --- |
| no surname, but a NAMED relative within two hops | **108,876** | 69.5% |
| a surname surviving redaction → `NN Larsson` | **37,226** | 23.8% |
| **neither — stays a bare `NN`** | **10,636** | **6.8%** |

**93% is reachable.** 85,906 at one hop and **38,545 only at two**, which is Emma's *"it can work
off of those long-range things"* paying for itself; 15,575 of the surname rows also have a named
relative and take both halves.

**The population grew 62,522 → 156,738 and that is the redaction fix, not a regression.** Those
94,216 were previously "labelled" `<private> Garborg` and so counted as done. They now reach the
NN algorithm, which is why the `en` batch went 25,930 → 104,856 edits in the same change.

**What is left in her order.** `hi`, `ar`, `ru` and `el` are **done** —
`scripts/build-four-script-labels.py`, 151,320 labels over the 37,830 people who carry a QID.

**The `en` shortfall is 57,179, and it is NOT arithmetic — measured 2026-09-01.** I framed it as a
gap between what the census says is reachable and what the placeholder batch emits, and closing it
as "the next concrete step rather than a new method". That was wrong. Broken down:

| | people | |
| --- | ---: | --- |
| census says **surname only** — no relative to describe them by | **35,565** | correctly get no `en` |
| census says **bare** — neither | 10,495 | correctly get no `en` |
| census finds a relative, batch emits nothing | **9,580** | the real discrepancy |
| not in the placeholder population at all (935 of them CJK-named) | 1,539 | a different job |

**No `en` for the 35,565 is CORRECT and not a gap.** Her model puts the marker in `mul` and a
*description* in the local languages; a description needs a named relative, and these people have
none. `NN Larsson` in `mul` with no `en` is the algorithm working.

**The 9,580 need relation words her table does not have.** The slot my census reached them by:

    8,129  spouse's father          799  spouse's mother       426  spouse's sibling
       55  child's spouse            51  sibling's spouse       36  spouse's spouse

**9,562 of 9,580 are at two hops, and 8,129 of them are a father-in-law.** They have a spouse, but
the spouse is *also* unnamed — so the preview cannot say *"wife of NN"* at one hop, and the only
named person within reach is the spouse's father. `scripts/build-nn-label-batch.py`'s language
table covers son/daughter/father/mother/husband/wife/sibling **of**; it has no in-law wording, in
any of its ten languages.

**So this is a decision, not an implementation.** Emma named the long-range relations she wanted —
*"grandparents or grandchildren or siblings"* — and did not name in-laws. Adding
*"daughter-in-law of X"* to ten languages is inventing vocabulary she has not asked for, which is
what § *One name item per USAGE* and the edge-case rule both say goes to her. **NEEDS-DECISION.**
The default in force meanwhile is what already happens: they get `mul` and no `en`.

## CI kills two slow jobs and the cause is NOT understood

**Four kills across two attempts, both modules, same message:** `The runner has received a
shutdown signal`, exit 143. `test_density.py` died 25m32 into its pytest step on the second
attempt; `test_paths.py` three minutes later.

**What is ruled out.** Not the job timeout — that is 180 minutes and these died at 25 to 91. Not
concurrency from a newer run — `gh run list` shows no `ci.yml` run after `33497581132`, and pushes
do not trigger this workflow (no `push:` trigger). Not a test failure: **both modules pass
locally, 23 passed in 35m44**, and `--durations=0` gives two hot spots —
`test_every_listed_region_gets_a_seed_and_it_is_inside_the_region` at **1,051s** and
`test_the_path_file_runs_from_the_account_owner_to_jimmu` at **1,018s of setup**.

**What is suspected and NOT established:** memory. A runner has ~16 GB against this machine's
31 GB, and `test_density` counts presence across all 600 exports. An OOM kill can present exactly
like this — but 25 minutes with 17 dots printed is not proof, and `CLAUDE.md`'s rail is explicit
that what is not understood gets a queue item rather than a change.

**Nothing is blocked by it.** The slow lane is `workflow_dispatch`-only, the fast lane is green on
both Python versions, and the modules pass locally. **Do not "fix" this by adding
`continue-on-error`** — that hides the signal rather than explaining it.

**The next step is one measurement:** print `free -m` and the peak RSS around the pytest step, or
run one module on a larger runner, and see whether memory is actually the wall.

## Pointers

- Abstract backlog: `todo.md` · Completed work: `devlog.md` · History: `git log`
- Open questions for Emma: `questions.md`
- The pre-wipe queue, 1,396 lines: `git show 4127170:queue.md`

## Add three SMTP secrets so the daily batch email can send

**Her ruling, 2026-08-31:** *"not wikidata editing but instead emailing me the daily
quickstatements file to me every day so I can run it."* It was gated on the repo going public;
that happened 2026-09-01, so it is built.

`.github/workflows/daily-batch-email.yml` runs at **06:05 UTC daily** and on demand. It checks
out only the batch file, counts what is in it, **always** uploads it as a downloadable artifact,
and emails it as an attachment when the credentials exist.
`.github/scripts/send_batch_email.py` does the sending — stdlib `smtplib`, no dependency.

**BLOCKED-ON-USER-ACTION, and this is a real one with a named action.** Three repository secrets,
which only she can add:

    SMTP_SERVER     e.g. smtp.fastmail.com
    SMTP_USERNAME   the sending account
    SMTP_PASSWORD   an app password, never the account password

Settings → Secrets and variables → Actions → New repository secret.

**Until they exist the job does not fail.** It runs, attaches the batch to the run, and says in
the log that it could not send — a red workflow every morning is worse than a quiet one, and a
missing secret is not an error in the pipeline.

**It sends the file, not a summary.** The batch is what she runs, and a description of it is not
something anyone can paste into QuickStatements.

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

## `P1814` *name in kana* — the research half, and it has nothing to attach to yet

**Emma, 2026-08-29:** *"do a cjk label conversion thing with research to fill in the korean and
name in kana properties"*. **The Korean half is done** — `scripts/translit_ko.py`,
`translit_ko_latin.py` and `build-ko-label-batch.py`, 33,725 labels. What is left is the kana.

**Its population is currently empty, measured 2026-09-01** —
`reports/culture-classifier-check.md`. `P1814` attaches to an item, and no correctly-identified
Japanese person in this corpus has one: 226 are classified Japanese, 2 of those have items, and
both of those are misclassified. So this is a sequencing fact rather than a difficulty — the
property becomes emittable when those 226 are created.

**"With research" is the load-bearing half and stands.** A kana reading is not derivable by rule:
the same characters take different readings per person, which is why `P1814` exists as a property
rather than being computed. `scripts/build-cjk-romanisation.py`'s docstring makes the same point,
and the `pykakasi` measurement now supports it with a number — **6 of 10** on names whose readings
are not in doubt, and every failure was a classical `の` name of exactly the kind this corpus holds.
So: find the readings, do not generate them.

**`shintowiki-scripts` is a SEPARATE repo and the coupling has burned this repo once.** Take
material from it — reading tables, transliteration data — and add no runtime dependency, no shared
state file and no network call. It is not checked out beside `geni`, so the first step is asking
her where it is.

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

**GRADED, and the grading is `scripts/grade-post-merge-drops.py`** — which already existed and
which I failed to notice before writing a weaker analysis over the top of its output. A drop is
`link-gone` when both people are present in some `exports/post-merge/*.ged`, `out/merged.ged`
gives them a family in common, and **no post-merge record does**:

    link-gone                        408      parents 159 · children 159 · spouses 90
    link still present                 2
    no shared family in merged.ged     2

**So 408 of the 412 are real deletions**, and Emma has already ruled on what to do about it,
2026-08-29: *"For now leave these things and still run them, but put them at the end of the
queue, I lean on the idea of saving them but do not have bandwidth to process this now."*

**A reading-by-eye of the names contradicted this and was wrong.** On 2026-09-01 I read the 412
as *"real relationships, in reciprocal pairs"* and concluded the override still looked wrong. The
reciprocity is not evidence: the OLD exports carry both directions, and the question is whether
the POST-MERGE ones record a family at all. They do not, which is exactly what `link-gone` means
and what the structural grader measures rather than infers.

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
