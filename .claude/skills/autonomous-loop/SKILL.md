---
name: autonomous-loop
description: Use when starting any session of relatively extensive or large-scale autonomous work — above all any large-scale population of queue.md with created tasks — to run the two local-cron productivity playbook (work-loop, auto-flush).
---

# Autonomous productivity loop — the two-cron playbook

**For any session involving relatively extensive work — above all, any large-scale population of `queue.md` with created tasks — this is the default way of working.** It is **two** local `CronCreate` jobs that turn "barrel through `queue.md`, and when it's empty atomise the next `todo.md` item into it" into a self-sustaining hourly cadence with a commit/push backstop. The crons are **session-local** (`durable: false` — they die when the session ends), so they are recreated at the start of every session.

## ⛔ TWO CRONS, NOT FOUR. Ruled 2026-09-14: *"Work-loop and auto-flush only"*

**The status-report and dead-queue-sweep crons are DELETED and are not to be recreated.** Both were
running hourly through 2026-09-13/14 and both earned their removal:

* **The status report cost turns and produced nothing that moved work.** It is reporting-only by
  design, so every tick spent gathering CI state, corpus counts and queue tallies was a tick not
  spent on the queue.
* **The dead-queue sweep came within one step of deleting two LIVE queue items** — d'Esneval and
  Bettencourt, each of which then returned 1,111 and 3,130 new people. It had tested "is this
  done" with `find exports -name "*<id>*"`, which hit a tiny *path* GEDCOM and read as a filed
  ball. A sweep that can delete live work on a bad test is worse than no sweep.

Finishing an item still means deleting it from `queue.md` and appending to `devlog.md` in the same
commit — that is the work-loop's job, step (d), and it does not need its own cron.

**And a general-purpose cron is the wrong instrument for a long single task.** Ruled 2026-09-13,
after the descendants campaign kept losing its thread: *"for the more agentic tasks, the general
purpose cron jobs just kinda fail... the cron job tells you to look at the queue, and then you
look at the queue and you find something unrelated, and it distracts you from it."* For a task
that will run for hours, **replace both crons with one that names that task and says continue
it**, and restore these two when it is done. `docs/descendants-campaign-loop.md` is the worked
example.

Twice an hour for the engine, once for the backstop, staggered so the ticks don't collide:

1. **Work-loop cron — `0,30 * * * *` (on the hour and the half hour).** The engine. Each tick does, in order:
   - **(a) SYNC** — `git fetch origin`; fast-forward or rebase the working branch (never force-push, never `reset --hard`, never discard a sibling machine's work).
   - **(b) WORK THE FIRST ITEM** — **⛔ the FIRST item in `queue.md`, by position, and it is named in the cron text.** Ruled 2026-09-14: *"`:00` and `:30` work loop prompts asking to work on the 1st queue item will be good."* Not *the top actionable item* — that phrasing is what sends the reader scanning a 1,600-line file and coming out on something unrelated, which is the failure that cost the descendants campaign its thread on 2026-09-13. Only a genuine BLOCKED-ON-USER-ACTION moves you down, and then you say which item you moved to and why. **Name the current first item inside the cron prompt** so a tick does not have to go looking for it. If nothing in `queue.md` is actionable (all blocked / needs user / a product decision), promote the next *genuinely-unblocked, bounded, verifiable* `todo.md` item — **plan it into `queue.md` first**, mirror to the task tool, then execute.
   - **(c) HARD RAILS** — never fake; never weaken / skip / delete a test to make it pass; never claim "works" / "verified" / "passes" without having actually RUN it and measured. A real defect → strict `xfail` or a precise documented blocker, never a loosened assertion. Don't implement what you don't 100% understand — write the spec / queue item instead. Name unbuilt or hard things plainly; don't paper over difficulty. Verify CI green, not just local — local-green does not imply CI-green.
   - **(d) COMMIT** — commit early/often with *why*; update `queue.md` in the same commit (delete completed items); append the dated entry to `devlog.md`; mark task-tool items done; push.
   - **(e) REPORT** — one line: the commit shas advanced, or `nothing actionable; <reason>`.

2. **Auto-flush cron — `15 * * * *` (hourly at :15).** The backstop. Commit + push all pending work so nothing sits uncommitted between manual pushes; report shas or "nothing pending". Only commit / push when something is actually pending — no empty commits.

**Why this exists:** the most common autonomous-agent failure is doing a large amount of work and silently losing the thread of what it is doing. The work-loop forces steady, verifiable, committed progress and the auto-flush guarantees nothing is lost between ticks.

**Lifecycle around a large-scale queue fill:**

- **(a) START both crons at the beginning of any extensive work session.** A fresh session has none of them running, so the opening move — the first queue item — is to *create them*.
- **(b) On a mid-session large-scale queue RE-FILL** (a planning burst that repopulates the queue), the FIRST item of that fill **kills the running crons**, then the work items follow top to bottom, and the pinned tail restarts them.
- **(c) Entering planning mode DISABLES the crons.** Their restart therefore lives at the **end** of the queue, not the beginning of the next burst.
- **(d) The LAST TWO queue items, always kept pinned at the tail, are:**
  1. **Ensure both crons are running** — start them if this session never did, restart them if a planning burst / queue re-fill killed them.
  2. **Summarise the session once, in the reply** — what advanced, what is blocked and on what. Once, at the end, not hourly.

In short: a fresh session **starts** the crons up front and the tail **ensures they are still running** + summarizes; a mid-session re-fill **kills** them up front and the tail **restarts** them + summarizes. Either way the queue both opens and closes on the cron set.

**Replication projects are exempt.** This is for `new` / general extensive work only — a bounded paper replication does not get the hourly loop.
