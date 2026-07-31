# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active — the read-only half of `todo.md` item 5

`todo.md` items 4 and 5 both end in **creating** Wikidata content, and that is
the user's decision to make, not ours: they stay **NEEDS-DECISION**. But item 5
has a reconnaissance half that presupposes nothing and is exactly what makes
that decision decidable — measuring which of this tree's names already have
Wikidata items. Read-only, local output, no edits proposed.

1. **Extract the tree's name vocabulary (`genimerge/names.py`) + tests.** From the canonical dataset, pull every distinct **surname** and every distinct **given name**, with frequencies and the people carrying them. Geni's `GIVN` holds a whole given string ("Ragnhild Rasmusdatter"), and Wikidata's P735 takes one item per given name, so record both the full string and its individual tokens. Patronymics (`-sson`, `-sdotter`, `-sen`, `-datter`) are a distinct category worth counting separately — they are the bulk of this tree and the least likely to have items.

2. **Check which names already exist on Wikidata.** Reuse the batched label-index lookup from `reconcile`: `VALUES ?label` against `rdfs:label`/`skos:altLabel`, restricted to name items by `P31` in {Q101352 family name, Q202444 given name, Q12308941 male given name, Q11879590 female given name, Q3409032 unisex given name}. Cache like every other Wikidata call. Do **not** propose creating anything.

3. **Write `reports/names.md`.** How many distinct surnames and given names the tree holds, how many already have Wikidata items, and the most common ones that do not — ranked by how many people would gain a P734/P735 link if the item existed. This is the evidence the user needs to decide whether item 5 is worth doing, and how big it is.

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
