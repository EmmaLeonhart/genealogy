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

## 9b · The old Samaritan GEDCOM against the new export — supersede or amend?

**Emma, 2026-08-16, and she is explicit that she does not know the answer:**
*"I don't really know what you're supposed to do with the old Samaritan stuff.
Now that we have this new Samaritan stuff, has that one changed relationship?
This relationship would kind of either have to be changed in them or they need to
be superseded… I think it's an easy thing to do but I don't know."*

`gedcom/samaritan-sources.ged` and `gedcom/samaritan-itamar-spine.ged` are
**hand-transcribed from published sources**, carry no Geni profile IDs, and
predate the four Samaritan exports and export 204. The question is whether their
relationships still hold now that Geni has the same people with real IDs.

**Show her the comparison before deciding anything** — which people appear in
both, and where the two disagree about a parent. Do not supersede a
hand-transcribed source on inference.

## 10 · Name items: link the 143 that exist, create the rest

**One item per USAGE, not per string** — `CLAUDE.md` § *"Jackson Jackson
Jackson"*. A token used as a given name, a surname and a patronymic is three
items. Nothing adjudicates between them.

**Already saved so nothing gets duplicated:** `reports/name-items.csv` (132,569
given- and family-name items our people reference) and
`reports/patronymic-items.csv` (**all 633** Wikidata items that are `instance of`
`Q110874`, fetched 2026-08-15).

- **143 of the 633 match a token in this corpus** — `Eriksson` (331 bearers),
  `Eriksdotter` (146). **Link these, never create them.**
- **4,143 patronymic-shaped tokens have no item.** Wikidata's patronymic coverage
  is Russian, Icelandic, Spanish and Ukrainian; Swedish has 13 items and
  Danish/Norwegian essentially none, which is most of this corpus.
- **A created patronymic item carries `P31` → `Q110874` and `P144` → the base
  name's item**, plus the derivation in the description text. 119 of the 633 do
  this already. `P5278` pairs `Eriksson` with `Eriksdotter`.
- **The suffix is evidence, not proof.** `-ovich`/`-ovna`/`-sdatter` are
  reliable; `-son`/`-sen` are not — `Jefferson` has 30 bearers in the given slot.
  `reports/name-classes.md` has the per-suffix reliability.

## 11 · Small, named, and unblocked

Each of these is one instruction with no decision attached.

- **`Q98159` in order.life's `persons.tsv` is a malformed row** — an embedded
  quote splits it, so its identifiers land in the wrong columns.
- **Wadah Cohen's father** is a missing son of `Amram ben Yitzhaq`
  (`6000000178795370821`); Geni records only one child for him.
- **The Itamar spine's generation 121** is still committed and still wrong — it
  is an office count, not a generation depth. A single *"distance not recorded"*
  link is the honest replacement.
- **Find the numbered-generation placeholder profiles on Geni.** Emma,
  2026-08-14 #258: *"There are numbered generation things… I think they're
  Chinese. I'd like you to try to find them."* Not attempted.
- **The Samaritan office** (`Samaritan High Priest`) is still only a description;
  no `P106`, because choosing the item means asking Wikidata.

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

## 14d · Test the three edit-object emitters

Emma, 2026-08-16: *"Don't just test them before September 1st. Put them at the
end of the queue."* `build-orderlife-identifiers`, `build-entity-resolution-batch`
and `build-samaritan-priest-links` have none. Every other `scripts/` file is the
same, but these three emit **edit objects meant to run against Wikidata**, which
is a different risk class from a report.

The rules worth pinning, each of which has already failed once here:

- **No creation for somebody who already has an item.** `build-samaritan-priest-batch`
  proposed creating `Jonathan I` and `Baba Rabba` because it only read links
  Wikidata already stated, ignoring the QIDs Emma wrote onto the Geni profiles.
- **No order.life QID as a Wikidata value.** `Q153719` is order.life's *Female*
  and would type-check as a person.
- **Citation shape** — `P2600` reference where a Geni ID exists, no reference at
  all where it does not, never a citation to a source Wikidata lacks.

## 15 · Audit `todo.md` the way `queue.md` was audited, then fold in the provisional to-do

**Emma, 2026-08-15:** *"I don't know if the to-do is being properly done."* This
is the last real item in the queue, and it is the same shape as § 0 was for this
file. In her order:

1. **Look over `todo.md` and see the degree to which it has actually been
   followed.** 595 lines, last touched 2026-08-14.
2. **Analyse it** — per `CLAUDE.md`, that means one row per item with its state,
   not an impression.
3. **Remove what is finished**, to `devlog.md` with a dated entry in the same
   commit, exactly as this file's own rule requires.
4. **Convert what is immediately actionable into queue items**, appended at the
   end of this queue.
5. **Move `provisional-todo.md` into `todo.md`.**
6. **Delete `provisional-todo.md`.**

`provisional-todo.md` holds three future-modelling items — Cladoplast's eventual
property plus `P3831` role qualifier, Gaiad characters eventually getting
individual citations, and `P999999` as a Gaiad reference that is **meant** to
fail so no Gaiad-derived statement can execute before the citation system exists.

**Do not let a second to-do file become permanent.** `provisional-queue.md`
lasted one day by design; `CLAUDE.md` records `data_lake/` as the cost of a
second store that outlived its reason.

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
