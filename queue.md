# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active — the identity guard has never been proven to fire

Found the same way as the CLI gap: by looking. `genimerge/identity.py` is the
one module the entire merge rests on, and it has **no test file**. Worse,
`IdentityMismatch` — the exception that stops a record whose xref and `RFN`
disagree from being treated as one person — is **never raised anywhere in the
suite**. Its only mention is a comment in
`test_merge_real_exports.py` saying it *would* raise, on data where it never
does. A guard that has never fired is a guard nobody has checked.

1. **Write `tests/test_identity.py`.** Cover `geni_id_from_xref` (valid, malformed, absent, non-numeric), `geni_id_of` (agreeing, **disagreeing so the exception actually fires**, `RFN` absent, xref absent so `RFN` is the fallback, and `strict=False`), `geni_id_from_pointer`, `xref_for`, and `profile_url`.

2. **Pin down what the merge actually keys on, in a test.** `Merger.add_source` keys on `record.xref` directly and never calls `geni_id_of`, so a record whose `RFN` contradicted its xref would merge on the xref without complaint. That is a defensible choice — the xref is the identifier and `RFN` is corroboration checked elsewhere — but right now it is implicit. Make it an asserted, documented decision rather than an accident, and say in `identity.py` where the cross-check does and does not run.

---

**When those are done the queue is empty again.** What remains needs something
this repo does not have:

- **NEEDS-DECISION** — `todo.md` items 4 and 5: creating Wikidata items, for
  people who have none and for the 1117 surnames and 1473 given names that have
  none. Sized in `reports/names.md`. The decision is the user's.
- **BLOCKED-ON-USER-ACTION** — `todo.md` items 3b and 7: ingesting Jenny
  exports. Unblock signal is a Jenny export appearing in `data_lake/`.

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
