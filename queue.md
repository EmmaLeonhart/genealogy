# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active — merge the exports, then reconcile against Wikidata

Derived from `todo.md` items 1 (canonical merge), 2 (Wikidata reconciliation),
and a first slice of 3 (expansion frontier). Work top to bottom.

1. **Second-pass reconciliation on names and dates.** For people P2600 did not match, generate *candidate* QIDs from name + birth/death year, plus a structural signal (does the candidate's P22/P25 point at an already-matched item?). Output `out/wikidata/candidates.csv` with an explicit confidence column and NO automatic acceptance — this file is for human review.

2. **Write `reports/wikidata-coverage.md`.** How many of the 8766 merged individuals are matched by P2600, how many have review-grade candidates, how many are unmatched, broken down by era and by subtree. This is the answer to "configure out the Wikidata connections as much as possible".

3. **Frontier analysis → `reports/frontier.md`.** Individuals with missing parents, sparse subtrees, and high-connectivity hubs — ranked as candidate branch points for the next Geni/Jenny export. First slice of `todo.md` item 3.

4. **Create the private GitHub repo and wire CI.** `gh repo create --private --source=. --push`, plus `.github/workflows/ci.yml` running `pytest` on push and PR.

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
