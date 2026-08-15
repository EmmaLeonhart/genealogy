# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

**`provisional-queue.md` is where new work goes right now, not here.** Emma,
2026-08-15: this file *"is kind of messed up"* and is being audited, so anything
decided since goes to the provisional queue and folds back in when the audit
settles. Item 0 below is that audit.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03**, **auto-flush at :15**, **status-report at :42**. On a fresh session they are started as the opening step; on a mid-session large-scale re-fill of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the last two items are pinned at the tail.

---

**`provisional-queue.md` is gone**, folded in here on 2026-08-15. It existed
because this file was untrustworthy while the audit ran; the audit is done, the
items below all trace to a dated instruction in the transcripts, and a second
queue file is exactly the *"second store"* mistake `CLAUDE.md` warns about.

## 0 · STANDING PROCEDURE — audit this queue against the chat logs before running it

**Emma, 2026-08-14, and this item exists because she could not tell what was
going on:** *"I'm extremely confused about what's going on here."* When she asks
for the queue to be executed, **run this before anything else** — it rebuilds the
queue from the transcripts, and only then is the rest of the queue trustworthy
enough to run. This item is **not deleted when it completes**; it is a procedure,
not a step.

**Last run: 2026-08-15** → `reports/audit-transcripts-2026-08-15.md`
(24 transcripts, 311 user turns, 2026-08-01 → 2026-08-15). Items 1–9 below are
its output.

### What went wrong, the first time

**The queue stopped driving the work, and nothing announced it.** On 2026-08-14 a
full day of work happened entirely from chat: four Geni exports integrated, three
Wikidata batches built, five reports written, `CLAUDE.md` amended four times —
**none of it in this file**, before or after.

Four failures, all of which recur:

1. **Finished work sat here as live work**, so reading the queue gave a picture
   of the project days out of date.
2. **Instructions given in chat never landed here**, and were written in
   retrospectively at the end of the day.
3. **The queue's own pinned tail was ignored** — it says three crons run the work
   loop; none were running.
4. **`git log` and `devlog.md` held the truth and the queue did not.**

**The root cause is not laziness about a file.** Chat instructions arrive faster
than they are recorded, and a queue only written to at the end of a session is a
transcript, not a plan. The fix is the audit below, run at the START.

### The audit

The transcripts are on disk and they are the authority, because they hold what
Emma actually said, in order, including the corrections:

    C:/Users/Emma/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl

Each line is a JSON object; a user turn has `message.role == "user"` with the
text in `message.content`. Read **newest first by mtime**, a week or more back —
the older files are where standing decisions were made. Then:

1. **Extract every user turn** with its timestamp. Do not summarise while
   extracting — summarising is where instructions get lost. A context-compaction
   turn is not something Emma wrote; its quoted messages are evidence, its
   narration is not.
2. **Classify each one**: an instruction, a decision about how something should
   work, a correction, or conversation. Only the first three matter.
3. **For every instruction and decision, ask three questions.** Is it done? Is it
   in `queue.md`? Is it in `CLAUDE.md` or `devlog.md`? Done and recorded needs
   nothing. Done and unrecorded goes to `devlog.md`. **Not** done becomes a
   concrete step here. A decision about how the project works goes to
   `CLAUDE.md`, not here.
4. **Corrections outrank the thing they correct.** Emma reverses herself
   explicitly and often — *"I didn't tell you to do that"*, *"Q1 is not a third
   gender, it is an error"*. The **latest** statement on any point is the live
   one, and the superseded version must not survive anywhere as if it were
   current.
5. **Delete finished items** and append a dated `devlog.md` entry in the same
   commit. No checkmarks — if it is here, it is not done.
6. **Commit and push**, then report what moved.

### What to watch for

- **Instructions phrased as frustration are still instructions.** *"Just fucking
  run the census"* is a queue item.
- **A thing done in chat but never written down is invisible to the next
  session** — that is how the 2026-08-14 work nearly vanished.
- **Do not re-derive settled questions.** If the transcripts show a question was
  answered, the answer belongs in `CLAUDE.md` and the question does not belong
  here.
- **Unrequested normalisation is its own category.** Emma, 2026-08-14: *"I find
  it extremely weird how it is that you have a tendency to try to do exception
  handling for stuff that I do not consider to be even necessarily errors."*
  Anything of that shape goes on the list to be **removed**, not kept.

---

## Scheduled — live cron jobs, this session

Session-only: they die when the Claude session ends and are recreated at the
start of the next one.

| id | fires | what |
| --- | --- | --- |
| `d425c1f5` | :03 hourly | work-loop |
| `be98e574` | :15 hourly | auto-flush — commit and push anything pending |
| `f8b152ab` | :42 hourly | status-report — reporting only |
| `f3d681e4` | **19:07** | **re-merge** the 203-export corpus, refresh the derived reports |
| `43140a93` | **21:02** | **bloat review** — candidates only, nothing deleted without asking |
| `d62449e3` | **22:01** | ask about `reports/seeds.md`'s future |
| `9f41a7a4` | **23:03** | entity-resolution: is it still a real task, and what format now |
| `05926d1d` | **00:01** | **the structural Geni↔Wikidata merge** |

The ordering is deliberate. The midnight merge needs *"the proper synoptic tree
and the proper samaritans"*, so the re-merge runs at 19:07, five hours ahead of
it, rather than after midnight.

---

## 1 · The structural merge produced its two outputs — review them

`scripts/walk-structural-merge.py --all`, run 2026-08-16 over all **12,620
anchors** (people holding both a Geni ID and a QID with a recorded parent), ten
generations up.

| outcome | positions |
| --- | ---: |
| `AGREE` — same person, already the same item | 52,977 |
| `GENI ONLY` — we have a parent, Wikidata does not | 52,731 |
| `MERGE` — both sides, ours has no QID | 20,265 |
| `WD ONLY` — Wikidata has a parent, we do not | 8,064 |
| ambiguous — Wikidata names more than one at that position | 162 |

**Neither `WD ONLY` nor `GENI ONLY` was ever a decision**, and treating them as
blockers was wrong. Emma, 2026-08-16: *"if they are only on wikidata there is no
problem is there lol. But about only geni well same? Tehy are created lol."*

- **`reports/structural-correspondence.csv` — 3,206 distinct QID ↔ Geni ID
  pairs**, each found by position and recorded with both names so the pairing can
  be read.
- **`reports/wikidata-structural-placeholders.json` — 7,851 `create_individual`**
  for people on Geni and not on Wikidata.

The 162 ambiguous positions are left alone: Wikidata names more than one parent
there, so the position does not single anybody out.

## 7+8+9 · Labels in seven scripts — the last step before Wikidata editing

**Emma, 2026-08-16:** *"WE ARE NOT DOING THIS SHIT UNTIL WE HAVE JA and ZH LABELS
ON EVERYTHING THIS IS RIGHT BEFORE WIKIDATA EDITING."*

**The labels are MADE, not copied, and that is the part I had wrong.** Her
instruction: *"you're supposed to make Japanese labels and Chinese labels for
everything, really Japanese first and then Chinese, just because a large amount
of stuff has to be romanized… like the ancient Near East stuff, has to go into
katakana."* So this is transliteration work, not a lookup — which is why the 3%
copy ceiling measured below is beside the point rather than a blocker.

### The language set

`en` · **`ja`** · **`zh`** · `hi` · `ar` · `ru` · `el` · plus `mul`

Japanese first, then Chinese, then the rest. Her reason for the last four:
*"Hindi, Arabic, and Russian are all languages because this kind of gives a
general strong coverage of all the different scripts of the world"* — plus Greek,
added immediately after: *"And I guess also Greek, the Greek alphabet and also
Greek."* Devanagari, Arabic, Cyrillic, Greek: with Latin and CJK that is most of
the world's living scripts.

### The three directions, and the one hard problem

**Emma, 2026-08-16, on what this actually is:** *"we have a large amount of
Japanese individuals that essentially have Japanese native names and most of them
have English language labels. Some of them don't… For the most part we're just
translating stuff from CJK into English, and from English into CJK, and then also
from English into the rest of these."*

So three directions, not one:

1. **CJK → English.** A person whose name is only in kanji and who has no English
   label. Romanisation.
2. **English → CJK.** The larger population: a Latin-script name needing `ja` and
   `zh`. Katakana for anything not already Japanese.
3. **English → `hi`/`ar`/`ru`/`el`.** Transliteration into the four remaining
   scripts.

**The hard part is not the scripts, it is knowing which culture a CJK name is.**
Her words: *"We have some CJK stuff that's confusing and needs work to figure out
what culture it is from."* Han characters do not say whether a name is Chinese,
Japanese or Korean, and the romanisation differs completely — 陳 is *Chen*,
*Chin* and *Jin* depending. `reports/name-classes.md` already measures the
population: **30,876 distinct Han tokens, 1,552 Hangul, 92 kana**, and kana or
Hangul are decisive while bare Han is not. `CLAUDE.md` records the same trap from
the other side: `SURN 秦州成紀` is a *place*, not a surname.

**Do not guess a culture from a name.** Where the script does not settle it, the
tree does — a person's neighbours, and which exports they came from.

### How the transliteration is done — Emma's ruling, 2026-08-16

**Hand-built tables, not a dependency.** `CLAUDE.md`'s stdlib-only rule stands.

**But CJK → English is NOT programmatic.** Her words: *"from CJK to English do not
remotely try to do any kind of programmatic transliteration because they all
suck. But AI almost always knows Japanese to Romaji."* So romanising a kanji name
is done **agentically, name by name**, and written into the repo as data. A
romanisation table produced by a library would be wrong often enough to poison
everything downstream.

**Name items first, and that is what makes it tractable.** *"the name objects can
actually be used in this because we can build the name objects first of all and
establish all the labels for them. We can do them probably kinda by hand,
agentically, and then put them here. We then only need to potentially not have
that many raw things that we need to do for the transliteration."*

The arithmetic is the point: `reports/name-classes.csv` holds **140,764 distinct
name tokens** across 396,163 people, and the CJK part is **30,876 Han tokens,
1,552 Hangul, 92 kana**. Transliterate the *tokens* once, in their name items,
and every person bearing them inherits it. Per-person transliteration would be
the same work multiplied by bearer count.

**So the order inside this item is:**

1. Build the name items and give **them** the seven labels — agentically for
   CJK → English, hand-built tables for English → the other scripts.
2. Compose each person's labels from the name items they already link to.
3. Only the residue — names that belong to no name item — needs raw work.

### How each is built

- **`ja`** — katakana for anything not already Japanese. Ancient Near Eastern
  names are the bulk of it. A name already in kanji keeps its kanji, and
  `CLAUDE.md` records her earlier rule that a kanji-only name gives the same
  string for `ja` and `zh`.
- **`zh`** — the phonetic rendering, after Japanese.
- **`hi`/`ar`/`ru`/`el`** — transliteration into Devanagari, Arabic, Cyrillic and
  Greek.
- **`mul`** — the `NN` / `NN <surname>` normalisation, already built.

### Order of work, and why

`reports/wikidata-placeholder-labels.json` holds **26,281 `set_labels` edits**
with `mul` on all and `en` on 14,351. It **must not run** in that state.

Emma: *"create the relatives first, then label."* The 8,018 relatives who name
these people are Geni-only; **7,851 of them are the `create_individual`
placeholders the structural walk produced**. Create them first and each carries
its full label set from the start rather than being revisited.

1. Create the 7,851 structural placeholders, **with the full label set**.
2. Then the other creations — the Samaritan line, the order.life tiers.
3. Then the 26,281 label edits, every one carrying all seven languages + `mul`.

**Measured for context, not as a blocker:** copying `ja` from a relative's
Wikidata item reaches 478 people and `zh` 439, against 14,351 for `en`, because
only 432 of the 8,018 relatives have a QID at all. Transliteration is what closes
that gap.

## 9b · The Samaritan source vs Geni — they do not conflict. 7 cases for Emma

`reports/samaritan-source-comparison.csv`, built 2026-08-16. Emma's question was
whether the hand-transcribed GEDCOMs need superseding now Geni has the same
people. **Measured, the answer is neither.**

| | |
| --- | ---: |
| present in both, **fathers agree** | **130** |
| **fathers disagree — for Emma to look at** | **7** |
| in the published source, not on Geni | 48 |
| Geni records a father, the source does not | 4 |
| ambiguous on name alone | 2 |

**The transcription is not superseded and does not contradict Geni.** 130 of 137
comparable people agree on the father; the 48 it holds alone are its value.

**The 7 to look at**, at least one of which is only a spelling difference
(`Phinhas` vs `Phinehas`):

- `Matzliach ben Phinhas` — source `Phinhas ben Yitzhaq`, Geni `Phinehas`
- `Yusef` and `Yusef ben Ab-Hisda` and `Yusef ben Yehoshua` — Geni gives a
  `119th generation Samaritan…` placeholder as the father
- `Shalom ben 'Amram` — source `'Amram ben Yitzhaq`, Geni `Shembet ben Bakhi`
- `Asher ben Shelach` — source `Shelach`, Geni `Matzliach ben Phinehas`
- `'Abed Hanuna ben Jacob Hadinfi` — source `Jacob Hadinfi`, Geni `Shalma`

**Matching took three passes and the first two were wrong in opposite
directions**, which is worth keeping because the shape recurs. Exact names were
too strict — the two sides decorate differently *both* ways, Geni writing
`Aaron I /Samaritan High Priest/` for the source's `Aaron /ben Amram/` and plain
`Ab-Hisda` for its `Ab-Hisda /ben Jacob/`. Dropping regnal numerals was too
loose — `Levi` then matched any Levi, pairing `Levi ben Abraham` with a man whose
father is Simeon. What works is the rule the rest of the repo already uses:
**the structure confirms and the name only locates** — same leading name *and*
same father's leading name.

## 10 · Name items — PLANNED, and the ambiguous ones need Emma

`reports/name-item-plan.csv` and `reports/wikidata-name-items.json`, built
2026-08-16. **This is the prerequisite for the labels**: transliterate a token
once in its name item and every bearer inherits it.

| | |
| --- | ---: |
| name items planned | **21,939** |
| link an item that already exists | **6,547** |
| create | **14,080** |
| **ambiguous — several items share the label, held** | **1,312** |
| below 5 bearers, not planned yet | 136,022 |
| excluded: particle, ordinal or placeholder | 123 |

**`ambiguous` counts as existing, and getting that wrong nearly created a tenth
`Maria`.** The first run treated only `resolved` as existing, so `Maria` (nine
items on Wikidata, 5,476 bearers here), `Anna`, `John`, `Anne` and 1,167 others
came out as creations. Duplicates are the failure `CLAUDE.md` says damages
Wikidata rather than wasting a run. They are now held: **choosing among nine
items is a judgement, and so is deciding there are none.**

**NEEDS-DECISION for Emma:** the 1,312 ambiguous names. Link the most-referenced
item, hold them all, or look at the top few by hand.

**The 116,583 below five bearers** are the long tail — 70% of distinct tokens are
used once. Not excluded on principle, just not worth an item before the ones that
matter exist.

## 11 · Small, named — three closed, one measured, one with Emma

**Closed 2026-08-16:**

- **`Q98159`'s malformed row** — fixed by reading order.life's TSVs with
  `QUOTE_NONE`. Its `geni_id` is `6000000011399707950` again and its
  `wikidata_qid` is correctly empty. It was 128 rows, not one.
- **The Samaritan office** — done as `P39` → `Q678510` *Samaritan High Priest*
  on all 21, in `reports/wikidata-samaritan-succession.json`. It needed no
  Wikidata query; the label was confirmed offline.
- **The numbered-generation profiles on Geni** — found, and **Emma was right that
  they are Chinese.** The convention is a comma-separated list of generation
  counts in different lineage reckonings ending in `世`: `,106,94,41,37,2世`,
  `(毛灬),136,124,71,67,32世`. **6,368 name records** carry one. Separately, the
  115 `Nth generation Samaritan Itamar line` profiles are her own placeholders.

**Still open:**

- **Wadah Cohen's father** is a missing son of `Amram ben Yitzhaq`
  (`6000000178795370821`); Geni records only one child for him.

### The Itamar spine contradicts itself, 112 against 121

Measured 2026-08-16, and the file is **more careful than the queue gave it credit
for** — `@I3@`'s note already says *"The LENGTH of the unnamed stretch is borrowed
from the parallel Phinhas line… Nobody counted this line. Do not read the number
as measured."* That is exactly right.

**But its header and its contents disagree.** The `HEAD` says *"Generation numbers
count from Aaron ben Amram = 1, so Itamar is 2 and Tabia is 112."* Tabia's own
note says **"Generation 121"**. The file holds **120 people numbered 2 through
121** — so nine more than its own header states, and nine more than the 112
generations the source gives for the parallel Phinhas line.

**NEEDS-DECISION, in `questions.md`:** renumber to end at 112, or collapse the
invented stretch to a single *"distance not recorded"* link as Emma originally
suggested. **The GEDCOM is not touched either way until she says** — it is
hand-made, and `CLAUDE.md` § 9b's rule applies: do not supersede a
hand-transcribed source on inference.

## 13 · Multi-hop relationship labels

Emma, 2026-08-15: *"Put this at the end of the… queue, and we'll work on this
later. We'll immediately get working on this."* **This is an ordinary queued
task, not parked** — it sits at position 13 because that is where it goes in the
order, and the work loop reaches it in the normal way. ("Parked" in this repo
means abandoned, as the Wikidata isolates were; that is not this.)

Her sketch of the ordering, extending the one-hop precedence rather than
replacing it:

**child-of → spouse-of → parent-of → grandchild-of → sibling / nephew / uncle.**

**Measured, so the size is known before it is built:** of the **11,930** people
with no one-hop label, **3,604 (30%) have a named relative two hops out** — 2,020
via a grandfather, 1,449 a grandmother, 135 a grandchild. So it is present in the
data and worth about a third of what one hop leaves behind.

Sibling, uncle and nephew need the family graph rather than the derived CSVs, so
that part waits on the re-merge.
## 14 · Wikidata batches built and waiting — nothing runs before 1 Sept

Their `.qs` siblings were deleted with QuickStatements on 2026-08-15; the
JSON is the artifact.

Not work items; here so they are not rebuilt from scratch by a future session.

- `reports/wikidata-samaritan-priests.json` — 78 `create_individual` for the
  pre-1624 line, chained `P22`, kept separate from the post-1624 items.
- `reports/wikidata-add-geni-id.json` — 32 `add_geni_id` from the QIDs Emma put
  in Geni `about_me`, including 2 additional-`P2600` unmergeable duplicates.
- `reports/wikidata-orderlife.json` — 52,233 entries; needs ONE rerun to pick up
  the label rule.

---

## 14b · A long job scheduled by cron will starve. Run it, or schedule it idle

**Measured 2026-08-15/16.** Of seven crons, six fired and one never did: the
19:07 re-merge, starved four hours running because **a cron only fires while the
session is idle** and the session was busy on the hour, every hour. Emma caught
it — *"fucking do this shit right there fuck now or at least queue it up at the
end so it actually runs"* — and it ran by hand at 00:30.

**So: never schedule a long or load-bearing job by cron during active work.**
Either run it directly, or schedule it for a window when nothing else is running.
The three hourly ticks are fine because they are short and re-fire; a
twenty-minute merge is not.

**Check the crons when a session resumes.** They are session-only, so they die
with it and need recreating — and a job that quietly never fires looks identical
to one that had nothing to do.

## 14c · The recurring cron jobs, written out as queue items

**Emma, 2026-08-16: queue up the cron contents.** A cron only fires while the
session is idle, so its instruction can be lost without trace — item 14b. These
are the four daily jobs in full, so the work survives whether or not the job
fires. Each is a real `CronCreate` id **and** an item here.

### :03 hourly — `d425c1f5` · work-loop tick

In order. **(a) SYNC** — `git fetch origin`, fast-forward or rebase main; never
force-push, never `reset --hard`, never discard another machine's work.
**(b) WORK** — take the top actionable item from this file and do it; if nothing
here is actionable, promote the next genuinely unblocked, bounded, verifiable
`todo.md` item, **writing it into this file first**. **(c) HARD RAILS** — never
fake a result; never weaken, skip or delete a test to make it pass; never claim
"works" or "verified" without having run it and measured. A real defect becomes a
strict `xfail` or a named blocker, never a loosened assertion. Never query
Wikidata live. Never overwrite an existing `.ged`. No unprompted reports or
analysis. **(d) COMMIT** — delete the finished item from this file in the same
commit, append a dated `devlog.md` entry, push. **(e) REPORT** one line: the shas
advanced, or `nothing actionable; <reason>`.

### :15 hourly — `be98e574` · auto-flush tick

If and only if something is actually pending, commit all uncommitted work with a
message saying **why**, and push. **No empty commits.** Never add a `*.ged` or
`*.zip` pattern to `.gitignore` — the zips are ignored one explicit line per file
so an unlisted one shows up in `git status`, which is how a new download
announces itself. Never delete a GEDCOM. Report the shas pushed, or
`nothing pending`.

### :42 hourly — `f8b152ab` · status-report tick

**Reporting only. No code changes, no files written.** Cover: what advanced since
the last report, shas with one line each; the current state of this file; any
place the hard rails were brushed; blockers, each tagged with exactly one of
**NEEDS-DECISION / BLOCKED-ON-USER-ACTION / BLOCKED-ON-EXTERNAL /
NEEDS-INVESTIGATION / UNSAFE-TO-GUESS / OUT-OF-SCOPE**, naming the specific
decision, action, signal, risk or owner — and if a not-done item fits none of
them with a specifically-named blocker, it is **not deferred, do it now**; and
test-suite health.

### 19:07 — `f3d681e4` · re-merge the corpus

Keep `out/merged.ged` as `out/merged-<n>.ged` first — `CLAUDE.md` says keep the
pre-batch tree whenever a batch lands, it is the only thing that makes the
seed-method backtests answerable. Then `python -m genimerge merge` over every
`.ged` under `exports/`, recursively. Regenerate the reports whose CLI command
exists — inventory, paths, connectors, density, frontier, descendants, seeds —
plus `reports/samaritan-component.md`. Re-run `scripts/build-repo-freshness.py`
and confirm `behind_by` has emptied. Never overwrite or delete a `.ged`.
**Last run 2026-08-16 00:30, by hand: 203 exports, 396,163 people, one tree.**

### 21:02 — `43140a93` · bloat review

Start from `reports/repo-freshness.csv` and
`reports/audit-transcripts-2026-08-15.md`. Look for work whose question is
**closed**; reports superseded by a later one; scripts nothing calls; CLI
commands with no reachable input; duplicated censuses of one phenomenon. **Never
delete a `.ged`, never add a `*.ged` or `*.zip` pattern to `.gitignore`, never
touch `exports/`.** Delete nothing on your own judgement — produce the candidate
list with a one-line reason and evidence each, put it to Emma in batches of four,
delete only what she approves. **Last run 2026-08-15: four deletions approved.**

### 23:03 — `9f41a7a4` · entity resolution

`entity_resolution.md` is Emma's free-form scratchpad of Geni-to-Wikidata
identities she recognised by hand. **Do not reformat it to suit the parser** —
teach the parser instead; `tests/test_entities.py` asserts the real file parses
with zero unparsed entries. Show her what is in it **raw**, entry by entry, and
say which entries are reflected in the data. It is **her job to be given JSONs,
not to make them**: `scripts/build-entity-resolution-batch.py` emits them.
**Last run 2026-08-16: 7 `add_geni_id` + 3 `set_label`.**

### 00:01 — `05926d1d` · the structural Geni↔Wikidata merge

Walk **up** the parental lines from people holding both a Geni ID and a QID,
merging the parents where both sides have one. **The label only confirms a
position the structure already chose; it never searches for a name** — that is
the matcher deleted on 2026-08-15, and `correspondence.md` forbids it. Everything
offline against `wikidata/items/`. Show cases one by one before generalising, and
do not reformat the records. Produces our own QID ↔ Geni ID correspondence and a
placeholder system for people on Geni and not on Wikidata.
**Last run 2026-08-16: `scripts/walk-structural-merge.py`, three lines shown,
three questions outstanding.**

## 14d · The emitter tests — WRITTEN, and they found a live bug immediately

`tests/test_edit_emitters.py`, **8 tests**, written 2026-08-16. Emma: *"Don't
just test them before September 1st. Put them at the end of the queue."*

**They caught a real defect on the first run.** order.life's **class items** are
rows in `persons.tsv` alongside real people — `Q153718` Male, `Q153719` Female,
`Q153800` Non Gaiad Character, `Q153801` Person, `Q153802` Gaiad character,
`Q153806`, plus `Q1` Aster and `Q5`. The batch was emitting all eight as
`create_individual` with `P31` = `Q5` **human**, so it would have created
Wikidata items asserting that "Male" and "Person" are people. Creations
19,234 → **19,226**.

**Found structurally, not by a list.** Anything another row names as its `sex`,
plus **every value anything declares itself an instance of** — collected in the
same shard pass that reads the Gaiad flag. A sex-only screen caught 4 of the 8;
`Person` and `Non Gaiad Character` never appear in that column.

**What the tests pin** — the shape of the failures, not the numbers, which move
whenever the corpus grows:

- a name whose label is **ambiguous** is never created, per `(token, usage)`
- a name item that exists is **linked**, never created
- the Samaritan batch creates nobody who already has a QID
- **no order.life QID reaches a Wikidata value**, and no class item is created
- a Geni-sourced statement cites the profile; nothing cites a source Wikidata
  lacks
- the succession never **removes** `P155`/`P156` without restating it

**Two of the eight were wrong when first written**, both too broad: comparing
bare tokens rather than `(token, usage)` flagged `Maria`, which is legitimately
ambiguous as a given name and created as a family name; and scanning the whole
JSON blob flagged `subject.orderlife_qid`, which is provenance and is *supposed*
to hold a local QID.

## Always last — restart the three crons and summarize

**These two items stay pinned to the tail of the queue at all times** — below every real work item:

A. **Ensure the three crons are running** — start them if this session never did, restart them if a planning burst / queue re-fill killed them: work-loop (`3 * * * *`), auto-flush (`15 * * * *`), status-report (`42 * * * *`).
B. **Run the status-report action once more, independently** — an end-of-session summary of everything that happened this session.

---

## Pointers

- Long-horizon backlog (abstract goals, source of future queue items): `todo.md`.
- Completed work (chronological, with releases): `devlog.md`.
- Narrative history: `git log`.
- The pre-wipe queue, 1,396 lines: `git show 4127170:queue.md`.
