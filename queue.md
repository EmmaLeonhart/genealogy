# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active

**Empty.** `reports/consistency.md` now also lists profiles that look like one
person recorded twice.

### Standing context

- **BLOCKED-ON-USER-ACTION — 95 impossible dates in the tree, listed in
  `reports/consistency.md`.** Someone born before a parent, or after their
  mother died. Every one is an error in Geni's data rather than in the merge, so
  fixing them means editing profiles on Geni; this repo will not change them.
  A further 88 are implausible rather than impossible — a parent under 12, a
  lifespan over 120 — and some of those will turn out to be correct.

  Worth doing before the QuickStatements batches rather than after:
  `add-claims.qs` carries 18 P569 and 24 P570 statements built from these same
  dates, so an uncorrected year here becomes a wrong year on Wikidata.



- **A third export candidate, and the only one with a *known* payoff.** Asked
  which people in a Geni relationship chain to Emperor Jimmu were in our tree,
  the answer was: it stops at **Elisabeth Árpád dynasty
  `6000000003243185408`**. The 51 people after her are all absent — Jelena
  Urošević, the Nemanjić rulers, Constantine IX Monomachos, Alp Arslan, the
  Ashina khagans, the Tang and Kudara royal lines, the Fujiwara and Mononobe
  clans, and every legendary emperor down to Jimmu.

  She has no parents recorded, so she is a doorway, and a strong one: ranked
  **198 of 2932**, ball 22, 9 doorways, **41% openness** against a pool median
  of 20%. The seed to export from is her absent mother, **Jelena Urošević**, per
  the export-from-the-parent rule.

  What no report here can express is why she is the best of the three
  candidates: the payoff is *observed*, not inferred. Every seed in
  `reports/seeds.md` is a bet on unseen material behind a door; Geni has already
  shown what is behind this one. That evidence comes from outside our data,
  which is the same blind spot that hid Iver Mellegård.

  **The honest limit:** an export fills at ~3840 people and Jimmu is ~51 further
  steps down the chain, so one export very likely reaches the Serbian and
  Byzantine material and **not** Japan. Getting to Jimmu is a sequence of
  exports walking down the chain, not a single one.



- **Not doing: centralising the per-module property constants.**
  `crosscheck`, `reconcile`, `namelinks`, `names` and `quickstatements` each
  declare the property IDs they use at the top of the file. That is local and
  readable, and a shared registry would move them away from the code explaining
  why they are there; `CLAUDE.md` already serves as the cross-module reference.
  Recorded so a later sweep does not re-open it as though it were an oversight.



- **NEEDS-INVESTIGATION — smallest-ball is the only ordering that surfaces the
  known-good seed, and it rests on one observation.** Hågen Iversen placed 38 of
  2336 by smallest ball, against 2261 by the shipped doorway count and 1303 by
  openness. The mechanism is plausible — a tiny neighbourhood is one we know
  almost nothing about — and the obvious objection turned out to be wrong, since
  the shortlist is 66 candidates with none isolated. It is **not** adopted and
  must not be until there is more than one data point. Resolves by taking one
  export from a top-ranked pick and one from the small-ball shortlist and
  comparing new-people counts. Not blocking anything.

- **NEEDS-INVESTIGATION — the seed ranking has never been tested.** No export
  has been taken from a seed `reports/seeds.md` chose. The one export with
  measured results was seeded on the parent of Hågen Iversen, who placed 2255 of
  2336 (ball 5, one doorway), and returned 3656 new people. That is a reason to
  doubt ranking by absolute doorway count — a large ball is a densely recorded
  neighbourhood, which is the opposite of where Geni has most to add — but it is
  n=1 and the ranking never scored the actual seed, who was not in our data. It
  resolves by taking the next export from a top-ranked pick and comparing. The
  prediction is already committed in `reports/seeds.md`, so `git show` will
  supply it when the fifth export lands. Not blocking anything.

- **UNSAFE-TO-GUESS — two links flagged as worth re-checking, both exact P2600.**
  `reports/wikidata-crosscheck.md` § "Links worth re-checking" names Canute I
  Erikska `Q442876` (0 agreements, 4 conflicts, birth 1145 against 857) and
  Bengt Folkesson `Q1621801` (1 agreement, 2 conflicts). Both are matched by the
  Geni ID on the item, not by inference, so the ID itself is under as much
  suspicion as the match. Two readings fit and nothing in this repo separates
  them: the link is wrong, or it is right and one side's data is badly wrong.
  Resolving one means a human comparing the Geni profile against the Wikidata
  item. Nothing should edit either side on a guess.

- **NEEDS-DECISION — how out-of-tree export seeds are found.** `reports/seeds.md`
  can only rank people already in the merged tree. Iver Mellegård, who seeded
  the best export so far, was in none of the three earlier exports, so the
  ranking could not have proposed him. Whatever route found him is one this repo
  cannot see or reproduce. The question is with the user; the answer decides
  whether to build out-of-tree candidate ranking or something else. Not blocking
  anything currently queued.

- **Take the pipeline order from `README.md`, not from a list written by hand.**
  The README's "before pushing" block already gives every command in dependency
  order, and it says `expand --search`, not bare `expand`. Both details matter.
  `expand` writes `matched_all.csv` and `candidates.csv`, which `coverage`,
  `crosscheck`, `name-links` and `quickstatements` all read, so omitting it
  leaves four reports generated from a previous tree. And bare `expand` skips
  the label-index lookup that produces the `name-match` proposals — running it
  without `--search` silently drops 100 of them and rewrites
  `reports/wikidata-coverage.md` with 30 proposals instead of 87. That is not
  hypothetical: it happened on 2026-08-01 and was caught only by diffing the
  regenerated report.

- **`python` on PATH is not the interpreter.** Python 3.13.14 is installed at
  `C:\Program Files\Python313\python.exe`, but the Microsoft Store stub aliases
  in `WindowsApps\` come first on PATH, so the bare `python -m pytest` written
  throughout `CLAUDE.md` exits 9009 with "Python was not found". Use `py -m
  pytest` or the full path. The package is not pip-installed either; the CLI
  needs `PYTHONPATH=src` (pytest gets this from `pythonpath = ["src"]` in
  `pyproject.toml`, which is why the suite runs but `python -m genimerge` does
  not). Not worth changing the user's PATH over, but worth not rediscovering.
- **NEEDS-INVESTIGATION — what actually bounds a Geni export is still unknown.**
  The code no longer claims to know: `GENI_EXPORT_CAP` is now documented as the
  largest export observed (3840) rather than a limit Geni enforces, and
  `tests/test_seeds.py` fails if a future export exceeds it. What is unresolved
  is the underlying fact. Four exports — 3836, 3836, 3836, 3840 — cannot
  separate a raised limit from a per-account limit from a limit on something
  other than head count from a walk that overshoots a floor. This needs a fifth
  export to move, so it advances as data arrives rather than by being worked on;
  it is not blocking anything, because being off by a few people out of ~3840
  does not move the seed ranking.

- **CI is off on purpose, and stays off.** Not a blocker — a decision. This is a
  private repo, where Actions minutes are billable rather than free, and
  push-triggered CI was never worth that risk. `ci.yml` is now
  `workflow_dispatch:` only and the workflow is disabled at the GitHub end.
  Verification is `python -m pytest` before pushing. The cost of that choice is
  named rather than hidden: **the Python version matrix does not run**, so 3.10
  is exercised only by the static check in `tests/test_python_floor.py`, and no
  commit should be described as CI-verified.
- **NEEDS-DECISION** — `todo.md` items 4 and 5: creating Wikidata items, for
  people who have none and for the **1343 surnames and 1626 given names** that
  have none. Sized in `reports/names.md`: 1008 of 2351 distinct surnames (42.9%)
  and 2076 of 3702 distinct given-name tokens (56.1%) have an item, so the rest
  do not. Whole given-name strings as Geni stores them are far worse — 929 of
  8168 (11.4%) — because Geni packs multiple names into one field. The decision
  is the user's.

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
