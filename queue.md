# Queue

Only work. Every specification and record moved to `CLAUDE.md` on 2026-09-01 at her instruction: *"remove all the 14 bullshit queue items"*. An item is DELETED when done, never annotated.

## Patronymics are not getting the name they come FROM

**Emma, 2026-09-02:** *"Patronymics are not getting the names they come from in the logic lol
that's actually essential to the real specified algorithm."*

A `P5056` *patronym or matronym* statement must carry **`P144` *based on*, pointing at the PERSON
that link names** — the father, then the grandfather for a chained patronymic — and `P1545`
*series ordinal* numbering the links outward from the bearer. `name modelling.txt` is the
authority and her worked example is there:

    P5056 ben Phinhas    P144 Phinhas ben Yittzhaq ben Shalma   P1545 1
    P5056 ben Yittzhaq   P144 Yittzhaq ben Shalma               P1545 2
    P5056 ben Shalma     P144 Shalma                            P1545 3

Her Vladimir Putin example is the same shape: `P5056 Vladimirovich` carries `P144` → `Q19300851`,
**his father**, not a name item.

Written at the tail on her instruction; nothing investigated.

## Add the descriptions to patronymics and family names in the generated QuickStatements

**Emma, 2026-09-02:** *"add an item at the end of the queue to make the generated quickstatements
add these descriptions to the patronymics and family names"*.

So the batch should emit the `D<lang>` description on **patronymic** and **family name** items —
not only on the ones it creates in that run, but as an addition to name items that already exist
without one.

Written at the tail on her instruction; nothing investigated.

**The one cross-reference, so it is not built twice:** `scripts/build-garborg-name-items.py`
already emits `LAST<TAB>Den<TAB>"<description>"` from `DESCRIPTION_FOR` on a **fresh** `CREATE`,
and that is the anti-duplicate mechanism — label plus description must be unique per language, so
a second described `Olsdatter` is refused where a second undescribed one is not. This item is the
same description reaching name items the batch is **not** creating.

**And the boundary that caused a scare on 2026-09-02:** descriptions on **name items** are the
mechanism and stay. Descriptions on **people** are the categorical ban, § *NO descriptions and NO
edit summaries*. The one she saw on a person was another editor's, on `Q136376387`.

## Then: one dispatch that produces the archive and the Pages site too

**Her framing, 2026-09-01:** *"the ci/cd run will make the archive (committed) and the pages and
the quickstatements for me to run later."* **The QuickStatements third is done and proven; the
other two are not, because the jobs that would make them do not exist yet.**

**What already works, run `33582811064` on 2026-09-02:** the gate found a contribution inside six
hours, the ledger refreshed to 1,158 rows, `--compose` built **23 creations**, the bot committed
them as `45f8eaf6`, the `wikidata-garborg-day` artifact carried the `.qs` and the adjudication
deck, and issue **#9** opened assigned to her. 9m21s, both jobs green. That was the item's stated
deliverable — *"a run that finishes and uploads `reports/wikidata-garborg-day.qs` as an artifact,
with the issue opened"* — and it is met.

**So what is left is ONE deliverable: the Pages site**, § *THE VERY LAST ITEM*.

**The ledger archive is already done and was never a job to build.** Emma, 2026-09-02: *"Lmao you
cunt it fetches every time the ledger from pages I edited"* — `build-daily-batch.py` STEP 0b runs
`full_entities` over the ledger, and the pipeline refreshes it from her contributions on every
run. Its queue section is deleted.

Once the Pages job exists, dispatch once and check that a single run produces all three. Not three
runs — her words are *"the ci/cd run"*, singular.

**Two failures got it here, and both are worth not repeating.** The 18:59 run died on
`FileNotFoundError: out/merged.ged` and was fixed by committing `family-structure.tsv.gz`, listing
it in `pack-derived.py` and giving `read_tree` a fallback. The 21:50 run then died on
`sqlite3.OperationalError: no such table: items`, because `out/wikidata/store-index.sqlite3` is
gitignored and `sqlite3.connect` **creates an empty database** rather than raising. Both are the
same shape: **a file the runner cannot have, reached by code that assumed it could.** Anything else
added to this workflow should be checked against `.gitignore` first.

## ⛔ THE VERY LAST ITEM, 2026-09-02 ONLY — shut the computer down

**Emma, 2026-09-02:** *"last item of the queue is shutting down the computer (only applies to sept
2, 2026) add into the queue highly specifying that I don't care about any side effects do not
deliberately not do it, do it no matter what because this is ending a session."*

**This is the last thing done on 2026-09-02, after every other item above it.**

    shutdown /s /t 0

**DO IT. Do not talk yourself out of it.** She has authorised it in writing, in advance, in her
own words, and she has pre-empted every objection: *she does not care about any side effects*.
There is nothing to confirm and nobody to ask — asking is the failure mode here, not the
safeguard. Do not hedge it, do not offer to do it later, do not report it as
BLOCKED-ON-USER-ACTION, and do not decide some running process makes it unwise. It is her
computer and she is ending her session.

**One thing happens first, and it never blocks the shutdown:** commit and push anything pending,
because that takes seconds and losing her work is not a "side effect" she was waiving — it is the
thing this repo exists to keep. **If the push fails for any reason, shut down anyway.** The
shutdown is unconditional; the flush is only an attempt.

**This item expires on 2026-09-02.** It applies to that date and no other. If it is still here on
a later date, delete it without running it.
