# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active — nothing checks the Python floor we advertise

`pyproject.toml` claims `requires-python = ">=3.10"`. CI was the only thing
testing that, and CI has stopped running; the only interpreter on this machine
is 3.13. So the floor is currently an unverified claim, and a 3.11-only
construct could land without anything noticing.

1. **Add `tests/test_python_floor.py`.** Read the floor out of `pyproject.toml` rather than hardcoding it, so raising the floor updates the check automatically. Then `ast.parse(..., feature_version=(3, N))` every file under `src/` — that rejects syntax the floor cannot parse — and grep the sources for a short denylist of stdlib names newer than the floor (`tomllib`, `datetime.UTC`, `typing.Self`, `assert_never`, `ExceptionGroup`, `enum.StrEnum`, `itertools.batched`, `hashlib.file_digest`, `pathlib.Path.walk`, `asyncio.TaskGroup`).

   **State plainly in the test and the devlog what this does not do.** It is a syntax and known-name check, not an execution of the suite on 3.10. Only CI does that, and only once billing is fixed. The point is to catch the cheap class of breakage while the expensive check is unavailable — not to let "3.10 supported" quietly become an assumption again.

---

**When that is done the queue is empty again.** What remains needs something
this repo does not have:

- **BLOCKED-ON-USER-ACTION — CI is not running.** Since 2026-07-30 06:29 UTC
  both matrix jobs refuse to start: *"The job was not started because recent
  account payments have failed or your spending limit needs to be increased."*
  A GitHub billing state, not a repo problem — the run 47 seconds earlier
  passed. The action is fixing billing or the spending limit in GitHub
  settings; the unblock signal is a run that starts. **Until then no commit can
  honestly be called CI-verified, and Python 3.10 is untested** — local runs are
  3.13 only.
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
