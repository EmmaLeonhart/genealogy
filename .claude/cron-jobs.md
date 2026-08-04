# The three crons, written down so a restart costs nothing

`CronCreate` jobs are **session-local and in-memory**. Nothing is on disk, so
they die when the session ends — a closed terminal, a crashed session, or a
machine restart takes all three with it, silently. The next session starts with
none and no error is raised anywhere.

That is the failure this file exists to prevent. It is not documentation of the
crons; it is the **source** for them. On any fresh session in this repo, read
this file and recreate all three with `CronCreate`, using the prompts verbatim.

Cadence, staggered so the ticks do not collide:

| job | cron | what it does |
| --- | --- | --- |
| work-loop | `3 * * * *` | drains `queue.md`, refills from `todo.md` |
| auto-flush | `15 * * * *` | commit/push backstop |
| status-report | `42 * * * *` | heartbeat, reporting only |

They also **auto-expire after 7 days** even in a session that stays alive, so
this file is the recovery path for that too.

See `.claude/skills/autonomous-loop/` for why the playbook is shaped this way,
and `queue.md` § "Always last" for the pinned tail items.

---

## 1. work-loop — `3 * * * *`

```
Work-loop tick for the geni repo (C:\Users\Emma\Documents\GitHub\geni). In order:

(a) SYNC — `git fetch origin`, then fast-forward or rebase main. Never force-push, never `reset --hard`, never discard another machine's work.

(b) WORK — take the top actionable item from `queue.md` and do it. If nothing there is actionable (all BLOCKED-ON-USER-ACTION / NEEDS-DECISION), promote the next genuinely-unblocked, bounded, verifiable item from `todo.md` — plan it into `queue.md` first, mirror to the task tool, then execute.

(c) HARD RAILS — never fake anything; never weaken, skip or delete a test to make it pass; never claim "works"/"verified"/"passes" without having actually run it and measured. A real defect gets a strict xfail or a precisely documented blocker, never a loosened assertion. Don't implement what you don't fully understand — write the queue item instead. Name unbuilt or hard things plainly.

(d) COMMIT — `python -m pytest` must pass locally first (CI here is `workflow_dispatch:` only and must stay that way — never add a push: or pull_request: trigger). Commit with the why, delete the completed item from `queue.md` and append a dated entry to `devlog.md` in the same commit, mark task-tool items done, push. Use `git commit -F <msgfile>`, not `-m` with a here-string.

(e) REPORT — one line: the commit shas advanced, or `nothing actionable; <reason>`.
```

## 2. auto-flush — `15 * * * *`

```
Auto-flush backstop for the geni repo (C:\Users\Emma\Documents\GitHub\geni). Check for uncommitted or unpushed work. If there is any, run `python -m pytest` first, then commit it with a message explaining why (using `git commit -F <msgfile>`, not `-m`) and push. If `queue.md` has an item that the pending work completes, delete it and append the dated `devlog.md` entry in the same commit. If nothing is pending, do nothing and say "nothing pending" — never create an empty commit.
```

## 3. status-report — `42 * * * *`

```
Status-report heartbeat for the geni repo (C:\Users\Emma\Documents\GitHub\geni). REPORTING ONLY — make no code changes, no commits, no pushes.

Cover:
- What advanced since the last report: commit shas with one line each.
- Current `queue.md` state.
- How the work held the hard rails, and any place it brushed one.
- Blockers, each tagged with exactly one of: NEEDS-DECISION / BLOCKED-ON-USER-ACTION / BLOCKED-ON-EXTERNAL / NEEDS-INVESTIGATION / UNSAFE-TO-GUESS / OUT-OF-SCOPE — naming the specific decision, user action, external signal, risk or owner. If a not-done item fits none of these with a specifically-named blocker, it is not deferred: say so plainly and flag it for the next work-loop tick.
- Test-suite health: the actual `python -m pytest` count, run rather than remembered.
```

---

## What a restart does and does not lose

- **Lost:** the three cron jobs, and any tick that was mid-flight. Recreate from
  this file — that is the whole cost, about a minute.
- **Not lost:** anything committed and pushed. The auto-flush cron exists so the
  window of uncommitted work stays under an hour; before a *planned* restart,
  commit and push rather than relying on it.
- **Worth checking after a restart:** `git status` and `git log origin/main..`
  for work a dying session never pushed.
