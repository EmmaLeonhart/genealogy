## THE ALGORITHMS, moved out of `queue.md` on 2026-09-01
The queue is for work; these are specifications and standing processes, so they live here
instead.

### STANDING PROCEDURE — audit this queue against the transcripts first

**Not deleted when it completes: it is a procedure, not a step.** Run it before
executing the rest of the queue, because otherwise the rest is not trustworthy.
**Last run 2026-08-30** → `reports/user-turns.tsv` and `reports/unrecorded-instructions.tsv`
(38 transcripts, **3,679 turns since 2026-08-15**, 1,577 distinct, **243 directive and written
down nowhere**). Steps 1 and 3 are scripts now — `scripts/extract-user-turns.py` extracts
verbatim, `scripts/audit-turns-recorded.py` screens for directive shape and then for whether any
six-word run of the turn appears in `CLAUDE.md`, `queue.md`, `devlog.md`, `name modelling.txt`
or `docs/`. The screen was checked against rulings known to be recorded and flagged none of
them. A miss is a **candidate to read**, never a finding — instructions repeat, and much of what
is said is answered in the moment and needs no record.

The previous run was 2026-08-15 → `reports/audit-transcripts-2026-08-15.md` (24 transcripts,
311 user turns).

Transcripts are the authority — they hold what was actually said, in order, including the
corrections:
`C:/Users/Emma/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl`.
Newest first by mtime. Each line is JSON.

**Read BOTH record types, or the scan misses half the input.** A turn typed while the model was
idle is `{"type": "user", "message": {"role": "user"}}`. A turn typed while a tool call was
running is
`{"type": "queue-operation", "operation": "enqueue", "content": "…"}`, and it is
**not** a user record. On 2026-08-16 the split was 28 user records against 21
queue-operations, so a `role == "user"` scan finds 57% of the input. Skip the
`enqueue` entries whose content is a cron prompt or a `<task-notification>`; those
are the harness talking, not input.

1. **Extract every user turn with its timestamp.** Do not summarise while
   extracting — that is where instructions get lost. A compaction turn is not
   input: its quoted messages are evidence, its narration is not.
2. **Classify:** instruction, decision, correction, or conversation. Only the
   first three matter. **Frustration is still an instruction** — *"just fucking
   run the census"* is a queue item.
3. **For each, ask: is it done? is it here? is it in `CLAUDE.md`/`devlog.md`?**
   Done and recorded → nothing. Done and unrecorded → `devlog.md`. Not done → a
   concrete step here. A decision about how the project works → `CLAUDE.md`.
4. **Corrections outrank what they correct.** The latest statement wins and the
   superseded one must not survive anywhere as if it were current.
5. **Unrequested normalisation is its own category** — exception handling built for things that
   are not considered errors. Those go on the list to be **removed**.

---


### Always last — pinned to the very end of the file

**Bullets, not letters.** These were `A.` and `B.`; `CLAUDE.md` § *Queue items are BULLET POINTS*
covers lettering for the same reason it covers numbering.

- **⛔ ENSURE THE TWO CRONS ARE RUNNING — work-loop `0,30 * * * *`, auto-flush `15 * * * *`.**
  `.claude/skills/autonomous-loop/SKILL.md` is the authority. The status-report and
  dead-queue-sweep crons are DELETED and not to be recreated. **NEVER KILL A CRON WITHOUT BEING
  TOLD TO** (ruled 2026-09-14). Session-only: they die with the session, so check `CronList`
  rather than trusting any line in this file.

  ⛔ **AND IT HAPPENED AGAIN ON 2026-09-12.** The session ran roughly nine hours with `CronList`
  reading *no scheduled jobs* — through the whole Alix, Seljuq, NN Näf, Dál Fiatach and no-name
  campaign — and **Emma noticed, not the session**: *"I think you kinda did nothing like the
  crons may have messed up."* The line above — *recreating them is the first thing a session
  does* — was already in this file and was not read. **Check `CronList` before the first export,
  not after the fortieth.**
  **A session once ran for hours with ZERO crons and nobody noticed.** Recreating them is the
  first thing a session does, not something to get to.

  **⛔ THE STATUS-REPORT AND DEAD-QUEUE-SWEEP CRONS ARE DELETED.** Ruled 2026-09-14:
  *"Work-loop and auto-flush only"*. The status report was reporting-only, so each tick was a tick
  not spent on the queue; the sweep nearly deleted two live items — d'Esneval and Bettencourt,
  whose balls then returned 1,111 and 3,130 people — because it tested *is this done* with
  `find exports -name "*<id>*"` and hit a tiny path GEDCOM. **Do not recreate either.** Deleting a
  finished item is the work-loop's own step (d).

- **The two crons, as durable queue items.** The crons are good and continue, and they are also
  queue items specified as cron jobs, so they get crossed off when the job finishes but are more
  stable than the cron itself. Cron text lives only in memory, so the queue is the durable copy:

  - **Work-loop, hourly at :03** — sync, take the top actionable item, do it, commit with a
    `devlog.md` entry, push, report one line. Rails: never loosen a test, never claim verified
    without running it, no live Wikidata beyond the ledger refresh and `full_entities` before a
    correction, never generalise a named instruction into a mechanism, never invent a `.qs`
    nobody asked for.
  - **Auto-flush, hourly at :15** — commit and push anything pending, or report nothing pending.
    Never an empty commit.
  - **Status-report, hourly at :42** — reporting only. What advanced, queue state, whether the
    rails held, blockers each under exactly one not-done tag, and real test numbers from a run.

- **Run the status-report action once more** — an end-of-session summary of everything that
  happened this session.

### `P2600` constraint violations report — analysis AT THAT TIME, no pre-analysis

<https://www.wikidata.org/wiki/Wikidata:Database_reports/Constraint_violations/P2600>

The analysis happens **at that time**, with no pre-analysis: how this could help Wikidata
genealogy, and it overlaps the entity-resolution work.

So: nothing is to be investigated, measured or fetched about this before the item is
reached. The analysis is of how the constraint-violations report could help Wikidata
genealogy, and it overlaps the entity-resolution work.

### The clan labels may be much worse than we think — `Q45449130`

<https://www.wikidata.org/wiki/Q45449130>

The clan labels are likely much worse than they look, which is why they were never run, and there
is at least some evidence for it.

An analysis. Nothing was investigated when this was written.

**⛔ ALREADY RULED, ALREADY SOLVED, AND THE HOLE IS CLOSED.** The 2026-08-29 block was real
and was implemented in ONE emitter; a hand-committed batch went round it with 1,431 clan-seat
labels. The gate now lives in `scripts/wikidata_lockout.py` and applies to every batch
`wikidata-edit-run.load_batch` reads, keyed on provenance. Detail in `devlog.md` 2026-09-14.

**What is left is the original question, due 2026-10-01 when the gate opens:** what should a
`mul` label be for a person known only by clan and seat? 隆西狄道 is a commandery-and-county in
Gansu — real evidence, not a name. Three shapes are in the data and the batch mixes them:
`隆西狄道` bare (79 people), `公主 隆西狄道`, and `某 李`.

### 0. Aug 28, 2026 manual adds

These are supposed to be manually added to the queue and worked on, do no just paraphrase during the rebase keep this part entirely intact. We are approaching usage limit for now.

### ⛔ THE RULINGS OF 2026-09-01 — the interview. These OVERRIDE the sections below

Every item was ruled on. Where a section below disagrees with this table, this table wins; the
sections are kept for their detail, not their status.

**Deleted outright, already removed:** the eight Asian identities · Bure kinship random-walk ·
the World-Tree review and its `universe` note · the chains as a SYSTEM · the six unwalked
algorithm steps · the four-label census · resolving names against the store · the 46%/41%
transliteration measurement (*"accept it and move on"*).

**Moved to the tail:** link reliability / `P1038` — *"we have the established method of
identifying parents and that works, siblings are just freely made and merged lol we only need a
scalable zipper thing much later"* · the `synoptic tree` vocabulary split · **creating the
fathers patronymics imply — *"postpone for a month lol"***.

**To do — the table was 20 rows and 18 are finished.** Each one's evidence is in
`devlog.md` for 2026-09-01 and its artifact is on disk; they are removed here so the queue reads
as outstanding work rather than as a record of a night. What is left of it:

| item | ruling | where it stands |
| --- | --- | --- |
| seven languages | wire `hi`/`ar`/`ru`/`el` **now**, and close the `en` shortfall | `hi`/`ar`/`ru`/`el` **done**, 151,320 labels. The `en` shortfall turned out to need in-law relation words that have not been sanctioned — a decision, not arithmetic |
| `exports/post-merge/` | do the stale-duplicate resolution | graded: **408 of 412 are real deletions**. The standing ruling is to leave them and keep measuring |

**Removed as done**, all verified by artifact rather than by memory: the `en` agreement rule ·
labels in the specified order (`en`/`mul`/`ja`/`zh`/`ko`) · name items reused by default · `Sara /NN/` and
the `Garborg` override · the label-change census · `ko` · the NN birth-name alias · the unreadable
transliteration tokens · the 218-script sweep · one batch file, names first · the clan labels ·
the export loop · the 179 ambiguous patronymics · `P407` by suffix · the `Nils`/`Nicolaus` form
table · the succession CSV · `pykakasi`, `BET x AND y` and the 74 MB file · the final rebuild.

### Anonymisation is NOT redacting the tree. It is scrubbing the repo of strategy

**The criterion: we show no more information than Geni does, so it is anonymised.**

**So the tree is ALREADY anonymised, and it always was.** This repo republishes what Geni
publishes and nothing beyond it — no field is derived that Geni does not itself display, and no
profile is enriched from elsewhere. That is the whole test, and it is met by construction.

**NOBODY IS EXCLUDED. No row is dropped, redacted or held back**, and a summary that leaves this
ambiguous is wrong: a sweep report once said "your redefinition of anonymising", which reads as
implying the private people had been cut. They have not been. Checked the same day:
`reports/derived-labels.csv` carries **20,928 rows with a redaction marker** out of 1,451,964, and
the corpus keeps all **94,071 `Private`** and **17,548 `<private>`** markers. § *Redacted people
go in* is the governing rule and is untouched — the person is created, the marker never becomes a
label.

**This replaces the ~96,000-private-rows reading entirely**, and that reading was wrong in
substance rather than merely superseded: it treated the private profiles as a *gate* to be cleared
before going public, when they were never an obstacle at all.

Cut the content in this repo that discusses **strategy around the account owner's own item and
how the account's editing is perceived**, and remove **code that treats that item as special**. The spine is the Arne→Bureus one only, and a task for 2026-09-02 removes that and all
spine logic once it is complete.

**One thing is left of the three, and it does not touch a person's data either:**

- **Cut the strategy content.** Anything in `CLAUDE.md`, `queue.md`, `devlog.md` or the scripts
  about how that item gets linked or how the account's editing reads to others.

**The repo is public as of 2026-09-01** — *"The repo is public now lol"* — so Actions minutes are
free and `CLAUDE.md` § *Cost* no longer binds.

### ⛔ `exports/post-merge/` — MOVED TO THE TAIL, 2026-08-29

408 of the 412 falsifiable drops are real deletions. **Leave them in the tree, keep running the
measurement, decide later** — the lean is toward saving the 408 rather than dropping them, but
there is no bandwidth to process it now. Nothing is applied and no override is written.

`scripts/grade-post-merge-drops.py` → `reports/post-merge-falsifiable.tsv` is the standing
measurement — 408 `link-gone`, 2 still linked, 2 with no shared family, over 159 parents,
159 children and 90 spouses.

---
