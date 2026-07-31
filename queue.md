# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active

Corrected on 2026-07-30: this section briefly said nothing was startable without
a user decision. Measuring the name vocabulary showed that is not true — **874
surnames and 1950 given names already have Wikidata items**, so linking people
to *existing* items needs nothing created and no decision made. That is the same
category as the P2600 backfill already shipped: a reviewable batch annotating
items that exist.

1. **Propose P735/P734 links against name items that already exist.** Decomposed from `todo.md` item 6. For the people already linked to a Wikidata item, emit QuickStatements adding **P735 given name** and **P734 family name** pointing at existing name items. Hard constraint: **only names whose lookup returned exactly one item**. A name matching two or more is a choice between them, and choosing would be guessing — those go in a separate "ambiguous, needs a human" list, never into the batch. Reuse `genimerge/quickstatements.py`; check the item's current P735/P734 first and skip anything already stated, exactly as the P2600 batch checks before proposing. Output `out/wikidata/add-names.qs` and a readable `.md`.

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
