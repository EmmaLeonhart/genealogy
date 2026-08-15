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

## 1 · Merge the two trees structurally — STARTED, showing cases

**Emma queued this for midnight and it is running as a walk, not a pipeline.**
`scripts/walk-structural-merge.py` prints lines and writes nothing;
`CLAUDE.md` § *How this project works now* says the rule comes out of the cases.

**First three lines shown 2026-08-16.** 12,620 people hold both a Geni ID and a
QID and have a recorded parent — those are the anchors. Six generations up the
Bonaparte line gave **10 AGREE then 2 MERGE**, the merges being people with no
QID on our side sitting in the identical family position on Wikidata:
`Maria da Bozzi` ↔ `Maria Colonna di Bozzi`, `Carlo Maria Buonaparte` ↔
`Carlo Maria Buonaparte`.

**The structure finds them, not the name.** `Maria Anna Tusilo` /
`Maria Anna Tusoli` differ by one letter and are already the same item; a name
matcher would have hesitated. `correspondence.md` still holds: no name
similarity, ever — the label only confirms a position the structure chose.

**Three questions put to Emma and not yet answered**, so nothing is written:

1. Is `MERGE` right as shown, when the two labels differ?
2. `WD ONLY` — Wikidata names a parent we lack. Import them, or ignore?
3. `GENI ONLY` — the placeholder population. Record now or later?

Then: build the QID ↔ Geni ID correspondence from the merges, and the
placeholder system for people on Geni and not on Wikidata.

## 2 · The Samaritan priests' Wikidata items — the half of the download still open

**The download ran on 2026-08-15** and closed the order.life half: 14,836 seeds,
14,832 stored, 7 minutes, nothing throttled. The store is **1,423,022 items**.
That resolved the uncheckable order.life identifiers (4,245 → 145) and recovered
**+2,001 `add_relationship` edges** (5,108 → 7,109).

**What it did not reach: the Samaritan priests who have a Wikidata item and no
Geni ID** — Yoseph II, `Q2031200` Aharon ben Ab-Chisda, Levi ben Abisha,
Aabed-El ben Asher. They were never in the P2600 closure and are not in
order.life, so no seed list built so far contains them. `Q2031200` was fetched by
hand and its relative-scan **discovered nothing new**, so walking outward from it
does not find the others either.

**The blocker is finding their QIDs, and it cannot be done offline**: they are
not in the store, so there is nothing local to search. Naming them means either
Emma supplying the QIDs, or a search against Wikidata — which is the thing
`CLAUDE.md` forbids without her say-so, exactly as the patronymic survey needed.

**NEEDS-DECISION:** supply the QIDs, or authorise one search.

## 4 · Re-merge over 203 exports and refresh the derived reports

**RUNNING as of 2026-08-16 00:30**, started by hand. The 19:07 cron never fired —
crons only fire while the session is idle and the session was busy continuously,
so it starved. Emma: *"fucking do this shit right there fuck now or at least
queue it up at the end so it actually runs."* Waiting on a cron for something
this load-bearing was the mistake.

`out/merged-176.ged` holds the pre-merge tree — `CLAUDE.md` says keep it whenever
a batch lands, because it is the only thing that makes the seed-method backtests
answerable.

When it finishes, regenerate the reports whose CLI command exists — inventory,
paths, connectors, density, frontier, descendants — plus
`reports/samaritan-component.md`, then re-run `scripts/build-repo-freshness.py`
and confirm `behind_by` has emptied. **`reports/seeds.md` is deleted and gets
regenerated here**, which is what Emma meant by "delete it so we could
regenerate it".

## 7 · Normalise the placeholder names to `NN`

**Emma, 2026-08-14.** All 55 discovered forms (`reports/given-name-forms.csv`,
35,414 records) collapse to one `mul` label: `NN`, or `NN <surname>` where a
surname is present. The **relationship** labels that go with this are item 8,
whose spec is settled.

**Guardrail, measured:** of the 33,564 profiles carrying a placeholder name,
**28,268 have ONLY placeholder names and are safe**, and **5,296 also carry a
real name** — `/Avitus/` on one record and `Avitus, Western Roman Emperor` on
another. Those 5,296 must keep the real name; `reports/name-alternatives.csv`
lists them individually.

**The surname is usually informative, with two contaminations — measured
2026-08-14.** Of the 29,452 placeholder records on profiles with no real name,
**10,362 carry a surname**, over **4,003 distinct** values, **70% used once**.

- **The bulk is a large Korean population** — 이 319, 김 214, 권 142, 허 106,
  홍 89, 안 71, 윤 68, 박 61, 최 61, 노 61 — plus `HUÁNG 黃` 83. **485 distinct
  surnames contain CJK.** These are real family names and are exactly the P734
  material.
- **Contamination 1: placeholders inside the surname slot.** `NN` 158, `???` 119,
  `N.N.` 70, plus `?`, `??`, `**`, `'`. Emma's rule, 2026-08-15: these **collapse
  to bare `NN`**, since a surname of `???` carries no information.
- **Contamination 2: a place in the surname slot.** `隴西狄道` (Longxi Didao)
  110 records — the `SURN 秦州成紀` trap from `CLAUDE.md` § *A clan name is not a
  clan*, recurring.

**Do not screen these by length.** 361 distinct surnames are <=2 characters, but
Korean and Chinese surnames are one character — 이 and 김 would both be discarded.
Screen on the placeholder vocabulary and on punctuation, never on length.

## 8 · Relationship labels — SETTLED, ready to generate

`reports/relationship-label-preview.md` showed both populations and Emma decided
on the rows. **26,281 people carry a placeholder given name.**

**Who gets a generated label: everyone with a placeholder given name.** No
filter on whether they have a surname, and **no filter on whether the surname is
repeated inside the generated label** — the 331 cases where `NN Kalf` becomes
`son of Anders Kalf` are generated, because the label still carries a given name
the `mul` label does not. Her two earlier answers pointed opposite ways on this;
shown the actual rows, she chose to generate.

**The surname is preserved, and the 36% is the reason.** A relative has a real
name for **69%** of bare-`NN` people but only **36%** of `NN <surname>` people.
Emma read that correctly and I had it backwards: *"the surname ones being badly
connected is kind of evidence in favour of the fact that we need to keep the
surname."* For that population the relationship label usually **cannot** be
built, so the surname is the only informative thing they have. `mul` stays `NN`
or `NN <surname>`.

**Precedence, one hop:** parent (father, then mother), spouse, child →
`daughter of Joe`, `wife of Carl`, `mother of Joseph`.

**Two rules from the preview, both hers:**

- **A redacted or placeholder relative is skipped** and the precedence falls
  through to the next one, trying every spouse and child rather than only the
  first. This removed all 2,730 labels reading *"husband of `<private>` Gaya
  Pereira"*. Only 1,052 of the 7,654 affected people (13%) recover a label from a
  later relative — for the rest the skip costs the label outright.
- **A surname that is itself placeholder vocabulary collapses to bare `NN`** —
  `NN ???`, `NN NN`, `NN N.N.`, `NN Unknown`. 351 people.

**Unknown sex takes the neutral form** (`child of`, `spouse of`), 127 cases. No
gender is inferred to make a label read better.

**Yield:** 14,351 of the 26,281 get a one-hop label — 13,140 bare `NN` and 1,211
with a surname.

## 9 · Label languages: English, Japanese, Chinese, and `mul`

Emma, 2026-08-15, resolving the 08-12 / 08-14 conflict in favour of the longer
list: **English + Japanese + Chinese + `mul`**, with Korean in the covered set
too. Her reasoning, which is the part worth keeping:

- *"Japanese is the lostiest language"* — it is not in Wikidata's top 18 by
  coverage, so `ja` nearly always has to be constructed rather than copied.
- *"Chinese needs to be generated to differentiate stuff with Japanese and
  Korean."* A Han-only string does not say which language it is; having zh
  explicitly is what separates the three.
- English is standard.

*"We might extend this to other languages, but this is something I consider to be
up for debate right now."* So the set is not final — do not build it as if it
were closed.

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
