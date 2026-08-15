# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03**, **auto-flush at :15**, **status-report at :42**. On a fresh session they are started as the opening step; on a mid-session large-scale re-fill of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the last two items are pinned at the tail.

---

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

## 1 · Merge the two trees structurally — the midnight job

**Emma, 2026-08-15, and she says plainly it has not been done:** *"it is an idea
of a thing that we still haven't really done yet."* Queued by cron for **00:01**,
after the re-merge at 19:07, because it needs *"the proper synoptic tree and the
proper samaritans"* in place first.

Walk up the relationships from people holding **both** a Geni ID and a QID,
merging the parents where both sides have one. `CLAUDE.md` § *Merging the two
trees is a walk up the relationships* is the full rule, including the part that
is easy to get wrong: **labels confirm a position the structure already chose;
they never search for one.**

Produces two things: our own QID ↔ Geni ID correspondence built from the merges,
and a placeholder for everyone on Geni but not on Wikidata, to be created later.

**Show cases one by one before generalising.** `CLAUDE.md` § *How this project
works now* — do not build the pipeline first, and do not reformat the records.

## 2 · Bulk-download the Samaritan priests' Wikidata items and fold them in

They are on Geni **and** on Wikidata; what they lack on Wikidata is genealogy.
`CLAUDE.md` § *An item with no relationships is not a missing item* has the order
this follows: `P2600` first, then everything Geni supports, each cited to it.

Part of the same download run as the **15,094 unreadable-item relationship
edges** — Emma chose *expand the download, then re-check* over emitting
unchecked. `genimerge wikidata-download` is the only thing in this repo allowed
to talk to Wikidata, and it is confirmed before a live run.

## 3 · Include the descent-from-antiquity people in the JSON generation

Emma, 2026-08-15, asked whether to import them, leave them out, or see the
population first: *"No, I am going to say just include these with the generation
of the jsns and everything."* So people with neither a Geni ID nor a Wikidata
item go in alongside the rest, not behind a flag or a gate.

## 4 · Re-merge over 203 exports and refresh the derived reports

**`out/merged.ged` is from 2026-08-13 17:53 and `reports/merge.md` lists 176
sources.** 27 exports have landed since, including the four Samaritan ones.
Everything derived from the merge is therefore describing a tree that no longer
exists — `paths.md`, `density.md`, `connectors.md`, `frontier.md`,
`descendants.md`, `samaritan-component.md`, the ten path reports.

Steps, in order:

1. **Keep the pre-batch tree.** `CLAUDE.md`: *"keep the pre-batch tree whenever a
   batch lands, it is the only way this question is answerable."* Copy
   `out/merged.ged` to `out/merged-176.ged` before re-running.
2. `python -m genimerge merge` — CPU-heavy, so check Emma is not on a hot laptop
   in public first.
3. Regenerate the reports whose CLI command exists, then commit.
4. Re-run `scripts/build-repo-freshness.py` and confirm the `behind_by` column
   has emptied for the generated rows.

## 5 · Re-run `build-geni-wikidata-pairs.py` over the 203-export corpus

The 40-profile pass predates the four Samaritan exports. Cheap; no decision
needed. A run that reports the two unmergeable Aaron / Zerubbabel pairs as
"conflicts" has regressed — see `CLAUDE.md` § *A second Geni ID … is NOT a
conflict*.

## 6 · The 59 order.life properties from P155 up

Emma, 2026-08-15 #288: *"look over all the order.life properties that might be
novel."* Rodovid, FamilySearch, WikiTree, Roglo, Geneanet, The Peerage, JewAge,
DAR/SAR, Find a Grave, a large Swedish cluster. Same numbers and meanings as
Wikidata, values Wikidata often lacks, on items that already exist. **No
creation, no normalisation** — the easiest remaining win.

## 7 · Normalise the placeholder names, then generate relationship labels

**Emma, 2026-08-14.** Two stages, the second explicitly at the END of the queue.

**Stage 1 — normalise every placeholder form to `NN`.** All 55 discovered forms
(`reports/given-name-forms.csv`, 35,414 records) collapse to one `mul` label:

- no surname -> `mul: "NN"`
- surname present -> `NN <surname>`

**Guardrail, measured:** of the 33,564 profiles carrying a placeholder name,
**28,268 have ONLY placeholder names and are safe**, and **5,296 also carry a
real name** — `/Avitus/` on one record and `Avitus, Western Roman Emperor` on
another. Those 5,296 must keep the real name;
`reports/name-alternatives.csv` lists them individually.

**Stage 2 — progressive relationship labels, per language.** Generate labels from
recorded relationships in this precedence:

1. parent  2. father  3. mother  4. spouse  5. child

producing `daughter of Joe`, `wife of Carl`, `mother of Joseph`.

**A relationship label can only exist in a language the RELATIVE already has a
label in** — that is the binding constraint and it is measured before anything is
generated.

**Every item must carry English AND Japanese, plus the `mul` label.** Emma,
2026-08-14: *"English and Japanese have to be present on everything and then
there's the multi-language label."* Measured ceiling for relationship labels
(`reports/relationship-label-languages.md`): en 96.1%, nl 81.1%, de/es/fr ~32%,
`mul` 25.3%. Japanese is **not** in the top 18 by coverage, so `ja` will usually
have to be constructed rather than copied from a relative.

**The surname is usually informative, with two contaminations — measured
2026-08-14.** Of the 29,452 placeholder records on profiles with no real name,
**10,362 carry a surname**, over **4,003 distinct** values, **70% used once**.

- **The bulk is a large Korean population** — 이 319, 김 214, 권 142, 허 106,
  홍 89, 안 71, 윤 68, 박 61, 최 61, 노 61 — plus `HUÁNG 黃` 83. **485 distinct
  surnames contain CJK.** These are real family names and are exactly the P734
  material.
- **Contamination 1: placeholders inside the surname slot.** `NN` 158, `???` 119,
  `N.N.` 70, plus `?`, `??`, `**`, `'`. The surname field is not clean.
- **Contamination 2: a place in the surname slot.** `隴西狄道` (Longxi Didao)
  110 records — the `SURN 秦州成紀` trap from `CLAUDE.md` § *A clan name is not a
  clan*, recurring.

**Do not screen these by length.** 361 distinct surnames are <=2 characters, but
Korean and Chinese surnames are one character — 이 and 김 would both be discarded.
Screen on the placeholder vocabulary and on punctuation, never on length.

**Open, Emma's own uncertainty:** whether to run stage 2 for people who already
have a surname, or only for the bare-`NN` ones. Put to her in item 1.

## 8 · Small, named, and unblocked

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

## 9 · Wikidata batches built and waiting — nothing runs before 1 Sept

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
