# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03**, **auto-flush at :15**, **status-report at :42**. On a fresh session they are started as the opening step; on a mid-session large-scale re-fill of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the last two items are pinned at the tail.

---

## 0 · READ THIS FIRST — how the queue went wrong, and how to audit it from the chat logs

**Emma, 2026-08-14, and this item exists because she could not tell what was
going on:** *"I'm extremely confused about what's going on here."* When she next
asks for the queue to be executed, **work this item before anything else** — it
rebuilds the queue from the transcripts, and only then is the rest of the queue
trustworthy enough to run.

### What went wrong

**The queue stopped driving the work, and nothing announced it.** On 2026-08-14 a
full day of work happened entirely from chat: four Geni exports integrated, three
Wikidata batches built, five reports written, `CLAUDE.md` amended four times —
**none of it in this file**, before or after. The queue was not consulted at the
start of the session and not updated during it.

Four distinct failures, all of which recur:

1. **Finished work sat here as live work.** Items 1-4 described the missing-
   ancestor sweep (done 08-13), the isolates (parked 08-13), the Baruch Jafe
   cluster (joined 08-13) and the Samaritan high priests (joined 08-14, and its
   "steps" already carried out by Emma). Reading the queue gave a picture of the
   project that was days out of date.
2. **Instructions given in chat never landed here.** Every decision below in
   items 5 and 6 was spoken, acted on, and only written into the queue
   retrospectively at the end of the day, when Emma asked why the queue was not
   being used.
3. **The queue's own pinned tail was ignored.** It says three crons run the work
   loop; none were running. The only cron in this session was one created ad hoc.
4. **`git log` and `devlog.md` held the truth and the queue did not** — so the
   queue became the least reliable file in the repo while looking like the plan.

**The root cause is not laziness about a file.** It is that chat instructions
arrive faster than they are recorded, and a queue that is only written to at the
end of a session is a transcript, not a plan. The fix is the audit below, run at
the START of a session rather than the end.

### How to audit the queue from the chat logs

**The transcripts are on disk and they are the authority**, because they hold what
Emma actually said, in order, including the corrections:

    C:/Users/Emma/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl

**23 files, 67 MB, one per session, going back to at least 2026-08-11.** Each line
is a JSON object; a user turn has `message.role == "user"` and the text in
`message.content`. Read them **newest first by mtime** and stop when the material
stops being new — a week or more of history is in scope, and the older files are
where standing decisions were made.

Do this, in order:

1. **Extract every user turn** across the transcripts, newest first, with its
   timestamp. Do not summarise while extracting — the summarising step is where
   instructions get lost.
2. **Classify each one**: an instruction to do something, a decision about how
   something should work, a correction of something already done, or
   conversation. Only the first three matter.
3. **For every instruction and decision, ask three questions.** Is it done? Is it
   in `queue.md`? Is it in `CLAUDE.md` or `devlog.md`? An item that is done and
   recorded needs nothing. An item that is done and unrecorded goes to
   `devlog.md`. An item that is **not** done goes into this queue as a concrete
   step. A *decision about how the project works* goes to `CLAUDE.md`, not here.
4. **Corrections outrank the thing they correct.** Emma reverses herself
   explicitly and often — *"I didn't tell you to do that"*, *"Q1 is not a third
   gender, it is an error"*, *"the Cladoplast property is not the Cladoplast
   object"*. The **latest** statement on any point is the live one, and the
   superseded version must not survive anywhere as if it were current.
5. **Delete finished items from this file** and append a dated `devlog.md` entry
   in the same commit. No checkmarks, no "done" markers — if it is here, it is
   not done.
6. **Commit and push**, then report what moved.

### What to watch for specifically

- **Instructions phrased as frustration are still instructions.** *"Just fucking
  run the census"* is a queue item.
- **A thing done in chat but never written down is invisible to the next
  session** — that is exactly how the 2026-08-14 work nearly vanished.
- **Do not re-derive settled questions.** If the transcripts show a question was
  answered, the answer belongs in `CLAUDE.md` and the question does not belong
  here.
- **Unrequested normalisation is its own category.** Emma, 2026-08-14: *"I find
  it extremely weird how it is that you have a tendency to try to do exception
  handling for stuff that I do not consider to be even necessarily errors."*
  Anything the audit finds of that shape goes on the list to be removed, not
  kept.

---

## Audited 2026-08-14 — items 1-4 closed out to devlog

Four items were still sitting here describing finished or parked work: missing
ancestors (0 absent), the Wikidata isolates (parked entirely), the Baruch Jafe
cluster (joined), and the Samaritan high priests (joined, and its steps 1-3 done
by Emma today). Per this file's own rule they belong in `devlog.md`, and the
decisions that still govern the project are in `CLAUDE.md`.

## Wiped 2026-08-13 — 1,396 lines down to this

Emma: *"OH MY GOD THE QUEUE IS SO BLOATED I AM ALMOST CERTAIN NONE OF IT EVEN IS
RELEVANT ANYMORE AND IT IS JUST DECAYED COMPLETELY INTO BULLSHIT."*

What was removed was **decision history, not steps** — the twelve-decision table,
the case-by-case walk notes, the 2026-08-09/10/11/12 decision rounds, the
re-clone post-mortem, the standing-order records. The decisions that still govern
the project are in `CLAUDE.md`, which is where they belong; the rest is in
`git log` at `4127170^`. Nothing was lost, and nothing below it was a step
anybody was going to execute.

**Two live concerns, Emma's own numbering:**

---

## 5 · Normalise the placeholder names, then generate relationship labels

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
have a surname, or only for the bare-`NN` ones. Not decided.

---

## 6 · Everything else outstanding from the 2026-08-14 session

Swept out of the chat log because none of it was ever queued.

**Wikidata batches built today, none executed** (nothing runs before 1 Sept):

- `reports/wikidata-samaritan-priests.json` — 78 `create_individual` for the
  pre-1624 line, chained `P22`, kept separate from the post-1624 items.
- `reports/wikidata-add-geni-id.json` — 32 `add_geni_id` from the QIDs Emma put
  in Geni `about_me`, including 2 additional-`P2600` unmergeable duplicates.
- `reports/wikidata-orderlife.json` — 52,233 entries; needs ONE rerun to pick up
  the label rule.

**Decisions waiting on Emma:**

1. **The 15,094 unreadable-item relationship edges.** 21% of the available work.
   Expand the `wikidata-download` seed set and re-check, or emit unchecked and
   accept duplicate-claim risk. `docs/future-modelling.md`.
2. **The 40 people whose `sex` column points at `Q1`.** An error, fixable; 39 of
   40 have a Wikidata QID so their own item has the answer, but none are in the
   local store. `reports/orderlife-sex-q1.csv`.
3. **The Itamar spine's generation 121.** Still committed and still wrong — it is
   an office count, not a generation depth. A single "distance not recorded" link
   is the honest replacement.

**Unbuilt, and the easiest remaining win:** the **59 order.life properties from
P155 up** — Rodovid, FamilySearch, WikiTree, Roglo, Geneanet, The Peerage,
JewAge, DAR/SAR, Find a Grave, a large Swedish cluster. Same numbers and meanings
as Wikidata, values Wikidata often lacks, on items that already exist. No
creation, no normalisation.

**Blocked on one thing, which unblocks two:** expanding the Wikidata download
would resolve both the 15,094 edges AND the Samaritan high priests who have
Wikipedia articles and Wikidata items but no Geni ID on them (Yoseph II,
`Q2031200` Aharon ben Ab-Chisda, Levi ben Abisha, Aabed-El ben Asher).

**Smaller:**

- Re-run `scripts/build-geni-wikidata-pairs.py` over the enlarged 203-export
  corpus; the 40-profile pass predates the four Samaritan exports.
- `Q98159` in order.life's `persons.tsv` is a malformed row — an embedded quote
  splits it, so its identifiers land in the wrong columns.
- The Samaritan office (`Samaritan High Priest`) is still only a description; no
  `P106`, because choosing the item means asking Wikidata.
- Wadah Cohen's father is a missing son of `Amram ben Yitzhaq`
  (`6000000178795370821`) — Geni records only one child for him.

**Running:** one cron, `a1b6b180` at 19:03 daily — audits unrequested
normalisation and exception handling, writes `reports/unrequested-normalisation.md`,
fixes nothing.

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
