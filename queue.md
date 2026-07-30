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

1. **Start the three-cron playbook.** `CronCreate` three local session crons (`durable: false`): **work-loop `3 * * * *`**, **auto-flush `15 * * * *`**, **status-report `42 * * * *`**.

2. **Stand up the Python package skeleton.** `src/genimerge/` with `pyproject.toml`, `tests/` using `pytest`, and an `out/` directory that is gitignored except for committed reports. Nothing clever — just an importable package with a working `pytest` run so later items have somewhere to land.

3. **Write the GEDCOM reader/writer (`genimerge/gedcom.py`) + tests.** Streaming line parser for GEDCOM 5.5.1 as emitted by Geni: `LEVEL [@XREF@] TAG [value]`, with `CONC`/`CONT` folding, UTF-8 with BOM tolerance, and tolerance for the malformed level-0 `NOTE` records these exports contain. Round-trip guarantee: parse → serialize must reproduce a semantically equivalent file. Unit tests over hand-written fixtures, not the 16 MB export.

4. **Profile the three exports → `reports/inventory.md`.** Per file: record counts by type, the full tag vocabulary with occurrence counts, and the Geni-ID overlap between the three files (all three report 3836 `INDI` — confirm whether the ID sets are actually identical or merely the same size). This is the evidence base for the merge rules, so it gets committed as a report.

5. **Write the merge (`genimerge/merge.py`) + tests.** Identity is the Geni profile ID, taken from the xref `@I<id>@` and cross-checked against `RFN geni:<id>`. Union of individuals; union of families keyed on their own Geni ID; per-field conflict resolution with every conflict recorded rather than silently dropped. Must be idempotent: merging a file with itself changes nothing.

6. **Produce the merged outputs.** `out/merged.ged` (valid GEDCOM, re-importable) plus `out/conflicts.md`. Commit a summary of what merged and what conflicted into `reports/`.

7. **Emit the canonical structured dataset.** `out/people.jsonl` and `out/families.jsonl`: one record per person keyed on Geni ID with parsed given/surname, sex, birth/death dates and places, parent/spouse/child Geni IDs. This is what every downstream Wikidata step reads — the GEDCOM stops being the working format here.

8. **Confirm the Wikidata property set.** P2600 (Geni.com profile ID) is confirmed. Verify and record the rest against live Wikidata before any query depends on them: P21 sex/gender, P22 father, P25 mother, P26 spouse, P40 child, P569/P570 dates, P19/P20 places, P734 family name, P735 given name, P1477 birth name. Write them into `CLAUDE.md` so no later step guesses.

9. **Reconcile by P2600 (`genimerge/wikidata.py`).** Query the Wikidata SPARQL endpoint for every `wdt:P2600` value in existence, intersect with our Geni IDs, and write `out/wikidata/matched_p2600.csv` (geni_id, qid, label). Batch politely, cache the response to disk so re-runs are free.

10. **Second-pass reconciliation on names and dates.** For people P2600 did not match, generate *candidate* QIDs from name + birth/death year, plus a structural signal (does the candidate's P22/P25 point at an already-matched item?). Output `out/wikidata/candidates.csv` with an explicit confidence column and NO automatic acceptance — this file is for human review.

11. **Write `reports/wikidata-coverage.md`.** How many of the 3836 are matched by P2600, how many have review-grade candidates, how many are unmatched, broken down by era and by subtree. This is the answer to "configure out the Wikidata connections as much as possible".

12. **Frontier analysis → `reports/frontier.md`.** Individuals with missing parents, sparse subtrees, and high-connectivity hubs — ranked as candidate branch points for the next Geni/Jenny export. First slice of `todo.md` item 3.

13. **Create the private GitHub repo and wire CI.** `gh repo create --private --source=. --push`, plus `.github/workflows/ci.yml` running `pytest` on push and PR.

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
