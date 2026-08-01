# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active

### 0. BLOCKED-ON-USER-ACTION — there is no Python on this machine

Everything below needs it, and nothing below can be verified without it.

`python` and `python3` on PATH are the **Microsoft Store stubs** (zero-byte app
execution aliases in `WindowsApps\`), not an interpreter — running one exits 49
with "Python was not found". No real install exists: nothing under
`%LOCALAPPDATA%\Programs`, nothing in `C:\Program Files`, no
`HKCU`/`HKLM` `PythonCore` registry key, no Store Python package. WSL is not a
fallback either — `wsl -l -v` fails with
`Wsl/CallMsi/Install/REGDB_E_CLASSNOTREG`.

Python **3.13 did run here**: `src/genimerge/__pycache__/` holds
`cpython-313.pyc` files, the newest stamped 2026-08-01 02:23. So the interpreter
was removed some time after that.

**Unblock signal:** a working `python -VV` on PATH (3.10+, per
`tests/test_python_floor.py`; 3.13 is what the caches were built with).
Installing it is the user's call — it is a change to their machine, not
this repo's to make.

### 1. Re-run the merge over four exports and refresh what it feeds

Measured already, in PowerShell, without the merge (so this is the number to
check the merge against, not a guess):

| | |
| --- | ---: |
| new export | 3840 |
| shared with `export-Ancestors` | 57 |
| shared with `export-BloodTree` | 140 |
| shared with `export-Forest` | 44 |
| shared with all three combined | 184 |
| **people it adds** | **3656** |
| merged tree 8766 → | **12422** |

95% of it is new. Then re-run what the merge feeds, since a 42% larger tree
moves every one of them: `genimerge inventory`, `merge`, `frontier`, `seeds`,
`reconcile`, `coverage`, `crosscheck`, `names`, `namelinks`, `quickstatements`.

### 2. Fix the "capped at 3836" claim, which the fourth export falsifies

`CLAUDE.md` is corrected already — it now records 3836 as a lower bound observed
three times rather than a constant. What is **not** fixed is the code: `genimerge
seeds` models an export as a ball capped at 3836 and `reports/seeds.md` reports
hitting that cap at hop 11, so the stale number is still wired into the ranking
that decides what to export next. Find where it is hard-coded in `seeds.py`,
correct it, and re-run `seeds`.

**NEEDS-INVESTIGATION** — 3840 vs 3836 is a 4-person difference and the cause is
not yet known. Do not guess a new cap from one observation; establish what the
number actually is (a floor of "at least 3840", a style-dependent cap, or a cap
on something other than individuals) before changing the model.

### Standing context

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
