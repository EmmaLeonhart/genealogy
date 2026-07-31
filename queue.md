# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active

## Active — the CLI is nine commands with no tests

Not from `todo.md`; found by looking rather than by assuming the queue was
blocked. **No test touches `genimerge/cli.py`.** Nine subcommands' worth of
argument wiring, file paths and error handling are exercised only by me typing
them, so a broken command would ship green. Two of the three bugs this project
has found came from tests over real data; this is the layer with none.

The second half is a real limitation, not just a testing convenience: `DATA_LAKE`,
`OUT` and `REPORTS` are module constants pinned to the repo, so the pipeline
cannot be run against a second dataset without overwriting the first — and a
test cannot run it at all without writing into the working tree.

1. **Make the workspace overridable.** A global `--data-lake` / `--out` / `--reports` (defaulting to today's repo paths) threaded through every command, so `genimerge` can be pointed at another dataset. `export` currently has no output option at all; `merge` writes two of its three files to fixed paths. Fix both while making the change.

2. **Test the CLI (`tests/test_cli.py`).** Every subcommand is registered and dispatches; `--help` works for each. Then an **offline end-to-end run** in a `tmp_path` workspace over a small hand-written GEDCOM: `inventory` → `merge` → `export` → `frontier`, asserting each output file exists and holds what it should, and that the merge output re-parses. No network: the Wikidata commands are covered for argument wiring and for their "run the earlier step first" error paths, not by calling out.

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
