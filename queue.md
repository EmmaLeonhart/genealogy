# Queue

Only work. Every specification and record moved to `CLAUDE.md` on 2026-09-01 at her instruction: *"remove all the 14 bullshit queue items"*. An item is DELETED when done, never annotated.

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

**Both other deliverables now exist.** The ledger archive was never a job to build — Emma,
2026-09-02: *"Lmao you cunt it fetches every time the ledger from pages I edited"*;
`build-daily-batch.py` STEP 0b runs `full_entities` over the ledger every run. And the Pages job
was built on 2026-09-02 and **ran green** on `f9ffac09`.

**So what is left is exactly the thing the item is named for: ONE dispatch producing all three.**
They are three workflows today — `pipeline.yml` for the QuickStatements, `pages.yml` for the site,
and the archive inside the daily batch — and her words are *"the ci/cd run"*, singular. Wire them
into one dispatch, run it once, and check a single run yields all three.

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
