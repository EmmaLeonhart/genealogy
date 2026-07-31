# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active — the commands that write the deliverables are untested

Found by measuring rather than guessing: `python -m coverage run --branch` puts
the package at **89%**, with one outlier — **`cli.py` at 57%**, 138 statements
unexecuted. The missing ranges are exactly the bodies of `reconcile`, `expand`,
`coverage`, `quickstatements`, `crosscheck`, `name-links` and `names`. The 52
CLI tests cover those commands' *refusal* paths and nothing else, so the code
that actually writes the CSV and QuickStatements files a human then reviews has
never run under test.

They are untestable by construction, not by oversight: each of the six builds
its own `WikidataClient` inline, so there is no seam for a fake — even though
the client was deliberately given an injectable `fetch` for exactly this reason.

1. **Give the CLI one client seam.** Replace the six identical `wikidata.WikidataClient(cache_dir=ws.cache, delay=args.delay)` lines with a single module-level helper a test can substitute. Duplicated six times is also just duplication.

2. **Test each network command's happy path offline.** With a fake client: `reconcile` writes `matched_p2600.csv`; `expand` writes `candidates.csv` and `matched_all.csv`; `coverage`, `crosscheck`, `names` write their reports; `quickstatements` and `name-links` write their `.qs` and `.md`. Assert the *contents*, not just that a file appeared — these files are the deliverable.

3. **Delete `gedcom.write_records`.** Defined, called nowhere, tested nowhere: speculative streaming that was never needed. Dead code that has never run is a liability, and deleting it is honest where adding a test to prop it up would not be.

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
