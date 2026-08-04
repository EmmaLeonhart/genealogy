# geni — Work Queue


**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Active

1. **BLOCKED-ON-USER-ACTION — take one export seeded in the six-person window
   that is now the whole gap between the two components.** Jimmu path steps
   **37–42**, with their IDs — note Constantine's is **not** the usual
   `6000000…` shape, so do not pattern-match it:

   | # | person | Geni profile ID |
   | ---: | --- | --- |
   | 37 | Constantine IX Monomachos, byzantine emperor | `385935664970005621` |
   | 38 | Guarandukht Bagrationi, of Georgia | `6000000024168588582` |
   | 39 | daughter of Smbat of Lori | `6000000032327207506` |
   | 40 | Sultan Alp Arslan | `6000000031528209013` |
   | 41 | Dawud Chaghri Bey, Lord of Khorasan | `6000000031528142916` |
   | 42 | n n | `6000000035218690155` |

   Step 36 (Helena Komitopulo `6000000002837351971`) is held in component 1 and
   step 43 (Inal Kut Chor `6000000035218736073`) in component 2, so a ball
   centred anywhere in the window has a real chance of touching both — this is the
   export that joins the two trees. Unblocks by Emma taking it on Geni; the
   check afterwards is `python -m genimerge path data_lake/paths/jimmu.tsv`
   plus the component count in `reports/frontier.md`.

2. **Ingest the rest of `exports/archive/` once the downloads finish.** ~17
   Forest/Ancestors/Descendants/BloodTree exports at 3860 apiece, none yet in
   `data_lake/`. Deliberately left out of the 2026-08-04 ingest because Emma
   scoped that session to Li Hong and `n n`; they are still arriving. Ingesting
   is a copy into `data_lake/` under `export-Forest-<seedID>.ged` and a re-run,
   with one wrinkle to settle first: several share a seed with a saved page in
   `geni_pages/`, and two archive exports could share a seed with each other
   across styles, which the current filename convention does not disambiguate.

3. **Re-measure the standing-context counts below against the eight-export
   merge.** The impossible/implausible date counts now read 178 and 173 against
   the 96 and 89 quoted in the note; `reports/consistency.md` is regenerated but
   the prose here is not.

4. **Turn the nine new saved pages into path reports — after the Jimmu gap, not
   before.** Emma saved these on 2026-08-04 as candidate connections and asked
   explicitly that the Japanese emperor line be finished first:
   `Gervasio of Toledo`, `Madgacen`, `Makeda Queen of Sheba`, `NN Basse`,
   `NN daughter of Berenice`, `NN of Malwa`, `NN`, `Princess NN`, `Psamtik II`,
   `daughter of the king of Assyria`, `Lady Palsu of the Jin clan`, `意美 Hata`.
   Each is `path-from-html` → `data_lake/paths/<name>.tsv` → `path` → a report
   saying how many steps are already held and where the gap is, which is what
   turned the Jimmu page from a guess into a six-person target. Cheap, no
   network, and it ranks the candidates against each other before any export is
   taken.

5. **The Wikidata reports are stale and nothing says so on their face.**
   `reports/wikidata-coverage.md`, `wikidata-crosscheck.md` and `names.md`
   describe the 16266-person tree; the tree is now 27718. Refreshing them means
   `reconcile` against the live SPARQL endpoint, which is the only part of this
   pipeline that needs network, so it is a deliberate run rather than part of
   the merge. **BLOCKED-ON-EXTERNAL** only in the weak sense that it needs the
   Wikidata endpoint to be up; unblock signal is simply choosing to run it.

### Standing context

- **BLOCKED-ON-USER-ACTION — 96 impossible dates in the tree, listed in
  `reports/consistency.md`.** Someone born before a parent, or after their
  mother died. Every one is an error in Geni's data rather than in the merge, so
  fixing them means editing profiles on Geni; this repo will not change them.
  A further 89 are implausible rather than impossible — a parent under 12, a
  lifespan over 120 — and some of those will turn out to be correct.
  (Counts re-measured 2026-08-02 over the five-export merge.)

  Worth doing before the QuickStatements batches rather than after:
  `add-claims.qs` carries 19 P569 and 24 P570 statements built from these same
  dates, so an uncorrected year here becomes a wrong year on Wikidata.



- **A third export candidate, and the only one with a *known* payoff.** Asked
  which people in a Geni relationship chain to Emperor Jimmu were in our tree,
  the answer was: it stops at **Elisabeth Árpád dynasty
  `6000000003243185408`**, step 30 of 83.

  **Measured 2026-08-04** — `data_lake/paths/jimmu.tsv`, extracted from the
  saved page by `python -m genimerge path-from-html` so every row carries its
  profile ID, then checked by `python -m genimerge path` into
  `reports/path-jimmu.md` and `reports/path-jimmu.json`. **62 of 83 steps
  held**, joined on the primary key, nothing advisory.

  **"It stops at Elisabeth" was exactly right.** Steps 1–30 are held without a
  single hole and step 31 is the first absence. What was wrong is the *size* of
  what follows: the absent block is **21 steps, not 51** — steps 31–51, Jelena
  Urošević through Li Hong 李宏, covering the Nemanjić rulers, Constantine IX
  Monomachos, Alp Arslan, the Ashina khagans and the Tang line. It does **not**
  run to Jimmu; steps 52–83 are held, in component 2.

  Worth keeping as a caution: checking this same path by *name*, before the IDs
  were extracted, put eleven false holes in steps 1–30 and reported the run as
  stopping at step 2. Every one was a spelling difference. Name matching did not
  merely add noise — it moved the headline finding.

  She has no parents recorded, so she is a doorway, and a strong one: ranked
  **198 of 2932**, ball 22, 9 doorways, **41% openness** against a pool median
  of 20%. The seed to export from is her absent mother, **Jelena Urošević**, per
  the export-from-the-parent rule.

  What no report here can express is why she is the best of the three
  candidates: the payoff is *observed*, not inferred. Every seed in
  `reports/seeds.md` is a bet on unseen material behind a door; Geni has already
  shown what is behind this one. That evidence comes from outside our data,
  which is the same blind spot that hid Iver Mellegård.

  **The limit, restated 2026-08-04 now that the path is measured.** The old
  version of this paragraph said Jimmu was ~51 steps further down the chain and
  concluded that reaching him needs a sequence of exports rather than one. The
  count was wrong and the conclusion no longer follows: the missing block is
  **21 steps**, and Jimmu is not at the end of it — steps 52–83 are already
  held. What one export from Jelena Urošević has to do is span 21 steps, not
  reach Japan.

  Whether one can is **NEEDS-INVESTIGATION** and not answerable from here. An
  export is a breadth-first ball of ~3844 people, so what matters is the radius
  that ball reaches along *this* line, and that depends on how densely recorded
  the Serbian and Byzantine neighbourhood is — bushy branching burns the budget
  sideways before it gets deep. Jelena is not in our data, so `seeds.py` cannot
  model her ball. It resolves by taking the export and re-running
  `python -m genimerge path data_lake/paths/jimmu.tsv`, which will say exactly
  how far down the chain it got.

  **Update 2026-08-02 — the far end arrived first, and it is an island.** The
  fifth export is the Japanese line itself (seed `6000000226989731860`, rooted
  at Kunino-tokotachi-no-mikoto): 3844 people sharing **zero** individuals and
  **zero** families with the other four exports, so the merged file is now two
  disconnected components. It brings none of the Serbian/Byzantine/Turkic middle
  of the chain, which is exactly why it does not attach. This does not retire
  the Jelena Urošević candidate — it makes it a *bridge* between two components
  we now hold rather than a reach into the unknown, which is a better bet than
  before, not a worse one. Both ends are anchored; the middle is what is missing.

  **Update 2026-08-04 — the gap can be attacked from both ends, and that halves
  it.** Measuring the path turned up a second doorway nobody had looked for. The
  known one is at the north end: step 30 Elisabeth is held and parentless, so
  the seed is step 31 Jelena Urošević. The south end is the same shape — step 52
  **Li Yong 李邕 `6000000075060923880`** is held, in component 2, and has **no
  parents recorded**, so the seed there is his absent father, step 51
  **Li Hong 李宏**. Two exports walking toward each other cover ~10 steps each
  instead of one export covering 21, and either one landing tells us how far a
  ball actually reaches along this line. Neither has been taken.

  **Update 2026-08-04, later — both were taken, and the pincer worked almost
  exactly as drawn.** Emma exported from both ends and the three files are now
  in `data_lake/`. The path went from **62 of 83 steps held to 77 of 83**, and
  the gap from 21 steps to **6**: steps 37–42, listed with their IDs as item 1
  of "Active" above.

  - The `n n` export (seed `6000000227036742846`) came in from the north and
    took steps **31–36**, Jelena Urošević through Helena Komitopulo — so the
    Nemanjić block that was the whole reason for the Jelena candidate is now
    held, and Jelena herself is in the tree rather than being a doorway.
  - The `Li Hong` forest export (seed `6000000227036288825`) came in from the
    south and took steps **43–51**, Inal Kut Chor through Li Hong 李宏 — the
    Ashina khagans and the Tang line.
  - The second `Li Hong` export (seed `6000000227036719829`) is on none of the
    path. It attaches to component 2 through two people and brings 3850 people
    anyway, which is the ordinary case: an export's value is not confined to the
    chain that motivated it.

  **What this measured that the ranking could not.** The open question was how
  far a ball reaches along *this* line, since bushy branching burns the budget
  sideways. Answer: **each export covered 6 and 9 steps of chain**, not the ~10
  hoped for and not 21. So one export does not span a gap of that size, and the
  remaining 6 steps are a plausible single export precisely because 6 is inside
  the range now observed rather than hoped for.

  **The two trees still do not touch.** Both new components attached to the side
  they came from — 61 shared people with component 1 for `n n`, 41 with
  component 2 for `Li Hong` — and none to each other. Predicted before running
  the merge and confirmed after; the component count is still 2, now 16217 and
  11501.



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
  cannot see or reproduce. **Seen twice now:** the 2026-08-02 seed
  `6000000226989731860` was likewise in none of the four earlier exports, and
  produced an export that overlaps them by zero people. Two of the five exports
  came from seeds this repo had no way to name. The question is with the user;
  the answer decides whether to build out-of-tree candidate ranking or something
  else. Not blocking anything currently queued.

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
  The code no longer claims to know: `GENI_EXPORT_CAP` is documented as the
  largest export observed (**3844** as of 2026-08-02) rather than a limit Geni
  enforces, and `tests/test_seeds.py` fails if a future export exceeds it —
  which is how both 3840 and 3844 were caught. What is unresolved is the
  underlying fact. Five exports — 3836, 3836, 3836, 3840, 3844 — still cannot
  separate a raised limit from a per-account limit from a limit on something
  other than head count from a walk that overshoots a floor. **The even spacing
  is a trap:** three numbers four apart, from three days and three seeds, are
  not a step of four, and nothing in the code encodes that arithmetic. This
  advances as data arrives rather than by being worked on; it is not blocking
  anything, because being off by a few people out of ~3840 does not move the
  seed ranking.

- **NEEDS-INVESTIGATION — the merged tree is two components and nothing in hand
  joins them.** 12422 people (Norwegian, branch point Tora Torsteinsdatter
  Galge) and 3844 (Japanese mythological, root Kunino-tokotachi-no-mikoto).
  `reports/frontier.md` § Components is the live count. Every aggregate figure
  this repo prints — coverage percentages, generational depth, the seed ranking
  — is now computed across two unrelated trees, which is not wrong but is easy
  to read as one. Resolves either by an export that bridges them (see the Jimmu
  chain note above) or by deciding the components are reported separately.
  Not blocking anything.

- **CI is off on purpose, and stays off.** Not a blocker — a decision. This is a
  private repo, where Actions minutes are billable rather than free, and
  push-triggered CI was never worth that risk. `ci.yml` is now
  `workflow_dispatch:` only and the workflow is disabled at the GitHub end.
  Verification is `python -m pytest` before pushing. The cost of that choice is
  named rather than hidden: **the Python version matrix does not run**, so 3.10
  is exercised only by the static check in `tests/test_python_floor.py`, and no
  commit should be described as CI-verified.
- **NEEDS-DECISION** — `todo.md` items 4 and 5: creating Wikidata items, for
  people who have none and for the **1540 surnames and 4986 given-name tokens**
  that have none. Sized in `reports/names.md` over the five-export merge: 1167
  of 2707 distinct surnames (43.1%) and 2419 of 7405 distinct given-name tokens
  (32.7%) have an item, so the rest do not. Whole given-name strings as Geni
  stores them are far worse — 1186 of 11772 (10.1%) — because Geni packs
  multiple names into one field. The fifth export roughly doubled the
  given-token pool and dropped coverage from 56.1% to 32.7%: the Japanese
  component's names are much less represented on Wikidata than the Norwegian
  ones. The decision is the user's.

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
