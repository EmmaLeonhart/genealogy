# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active

## Active — cross-check our claims against Wikidata's

The last unblocked piece of `todo.md` item 6. For the 245 people already linked
to a Wikidata item, both sides state parents, spouses and dates. Comparing them
needs nothing created and no decision: it is read-only, and the *disagreements*
are the point. The three P2600 contradictions found the same way turned out to
be duplicate Geni profiles — the most useful thing that run produced.

1. **Write the cross-check (`genimerge/crosscheck.py`) + tests.** For every linked person, fetch their Wikidata P22 father, P25 mother, P26 spouse, P569 birth date and P570 death date, and compare against ours. Classify each claim into exactly one of: **agrees**, **gap** (we know, Wikidata does not), **conflict** (both know, they differ), or **not comparable** (neither knows, or the other endpoint of a relationship is not itself linked). Dates compare on year with the same tolerance the reconciler uses, and a date our export marked approximate is never called a conflict.

2. **Write `reports/wikidata-crosscheck.md`.** Counts per property, then every conflict listed individually with both values and links to both sides. Conflicts are the deliverable here, not the gaps — each one is either our match being wrong or a real error on one of the two sites.

3. **Emit `out/wikidata/add-claims.qs` for the gaps only.** Strict eligibility, enforced not assumed: a relationship is proposed only when **both** endpoints are linked **by P2600** — never by expansion, since an inferred match on either end would put a wrong parent on a real item. A date is proposed only when our date is **exact** (no `ABT`/`BEF`/`AFT`/`BET`) and the item states nothing for that property. Everything else goes in the report for a human. Companion `.md` as with the other batches. Nothing is written to Wikidata.

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
