# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active

**Export seed discovery** — model a Geni export as what it actually is, a
breadth-first ball from one profile capped at 3836, and rank candidate seeds by
the *new* material that ball would reach rather than by the known tree hanging
off them. The user's constraint: never pick a seed sitting in the middle of a
region already recorded several layers deep, and do not require the seed itself
to be well documented — interconnectedness carries the export.

1. **`src/genimerge/seeds.py` — the ball.** `export_ball(graph, seed, *, style,
   cap=3836, radius=None)`, BFS in hop order, cap applied at Geni's export
   limit. Styles matching how Geni exports: `blood` / `all` (undirected family
   graph), `ancestors` (parent edges only), `descendants` (child edges only).
   Return the reached set plus the hop at which the cap bit, because a ball that
   fills before it reaches the boundary is exactly the wasted export.

2. **Openness, and the saturation rejection.** For a seed's ball: `open` =
   how many people in it have no parents recorded (each is a doorway Geni can
   walk through and we cannot), `openness` = `open / ball`. A ball whose
   openness is below a threshold is **saturated** — everything around it is
   already recorded to several layers — and is rejected outright rather than
   ranked low. Screen on a cheap radius-limited ball (default 3 hops); pay for
   the full capped ball only on the finalists.

3. **Greedy non-overlapping selection.** Two seeds three hops apart have nearly
   the same ball, so ranking alone would hand back forty candidates from one
   neighbourhood. `choose_export_set(profiles, k)` picks the best seed, marks
   the frontier people its ball covers, then repeatedly picks whichever
   remaining seed adds the most *uncovered* frontier people. That answers "what
   are my next k exports" instead of "here are k names near each other".

4. **`genimerge seeds` CLI** → `reports/seeds.md` and `out/seeds.csv`, carrying
   per seed: ball size, open count, openness, hops used, whether the cap bit,
   and what each successive pick adds over the ones before it.

5. **Tests.** Ball shape and hop order per style; the cap actually biting;
   saturated balls rejected rather than ranked; greedy selection preferring a
   smaller distant ball over a large overlapping one; determinism on ties.

**Named honestly: the yield of an export cannot be measured, only proxied.** We
do not know what is above a parentless person — that is the whole reason to
export from them. Openness counts doorways, not what is behind them. The report
must say that rather than present a score as a prediction of new people.

What remains after that needs something this repo does not have:

- **CI is off on purpose, and stays off.** Not a blocker — a decision. This is a
  private repo, where Actions minutes are billable rather than free, and
  push-triggered CI was never worth that risk. `ci.yml` is now
  `workflow_dispatch:` only and the workflow is disabled at the GitHub end.
  Verification is `python -m pytest` before pushing. The cost of that choice is
  named rather than hidden: **the Python version matrix does not run**, so 3.10
  is exercised only by the static check in `tests/test_python_floor.py`, and no
  commit should be described as CI-verified.
- **NEEDS-DECISION** — `todo.md` items 4 and 5: creating Wikidata items, for
  people who have none and for the 1117 surnames and 1473 given names that have
  none. Sized in `reports/names.md`. The decision is the user's.
- **BLOCKED-ON-USER-ACTION** — `todo.md` item 3b: taking the next Geni export,
  from the branch points ranked in `reports/frontier.md`. Only the user can run
  an export. Unblock signal is a new `.ged` in `data_lake/`.

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
