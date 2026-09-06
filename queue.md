# Queue

Only work. An item is DELETED when done, never annotated. Bullets, never numbers —
`CLAUDE.md` § *Queue items are BULLET POINTS*.

**Read `docs/collector-run-loop.md` before touching the collector.** It is her dictation of the
whole run loop and it ends *"there's no discretion on your part at all"*, said three times.

---

- **⛔ RUN THE COLLECTOR OVER THE ISOLATE TARGETS. This is the work, and it is the only executable
  item here.** Emma, 2026-09-06: *"all the queue did was just ask the browser agent to navigate to
  each page and run the stuff would be decent."* That is the entire loop:

      1. navigate to  https://www.geni.com/people/x/<geni id>
      2. dispatch     {job:"individual", geni_id:"<geni id>"}
      3. read the result, write the files, move to the next target

  **The agent navigates and nothing else.** Every decision — whether the path resolved, whether
  the statistics justify an export, which ancestor to add — is inside
  `geni-extension/content/individual.js`. Do not re-derive any of it in prose; that reasoning is
  the discretion she removed.

  **Where the targets come from, in this order:**

      reports/isolate-path-pilot.tsv       100 targets, 19 touched, 81 to go
      reports/sibling-pair-worklist.tsv    2,526 people with no scrape yet

  `python scripts/pilot-progress.py` prints the first count; the second is any `geni_id` in the
  worklist with no `geni-families/<id>-family.tsv`.

  **After each scrape:** `PYTHONPATH=src python scripts/build-tiny-gedcoms.py` turns everything on
  disk into tiny GEDCOMs. It is idempotent and safe to run repeatedly.

  ⛔ **THE FOUR THINGS THAT WILL WASTE A SESSION IF YOU REDISCOVER THEM:**

  * **Nothing downloads.** Roughly two files land per browser session and Chrome blocks the rest —
    a per-origin permission needing an omnibox grant she cannot give from a phone. The job returns
    the TSV on the data attribute; a **file tool** writes it. `saveBlob` has been deleted twice
    and must not come back.
  * **Never retype a scrape through a shell heredoc.** It double-encodes UTF-8 — `Wenström`
    becomes `Wenstr\xc3\x83\xc2\xb6m` — and silently destroyed 4 of 14 scrapes. The tool result
    itself carries UTF-8 intact; only the shell breaks it. Base64 out of the browser is refused by
    the tool's content filter, and so is any line containing `key=value`.
  * **A pending path search is NOT a miss**, and a requested search **decays back to unrequested**
    within hours. Revisit and re-request; never write a blank over an observed verdict.
  * **The background service worker cannot be updated from here** and does not matter — it runs
    only the scheduler. `todo.md` § 3d has the measurement and five failed routes.

  **State right now:** pilot 19 of 100 · `reports/isolates.csv` 20 rows, 7 misses / 1 hit /
  12 pending · 1,569 tiny profile GEDCOMs · 1,151 tiny path GEDCOMs · **zero invented people** ·
  the merge reads 3,323 files.

  **The live-site writes sit behind `job.create`.** Setting it lets the loop create one ancestor
  and run a `Forest` export when the gate clears. It has not been exercised yet, so the first one
  is worth watching.

- **The parent-adding campaign.** GATED: it starts once the placeholder parents have been
  sufficiently gathered in the synoptic tree and a batch is on Wikidata. Emma, 2026-09-03: *"In
  the future after we've sufficiently gathered all the placeholder parents and added a bunch to
  wikidata we can do a parent-adding campaign, especially if we use forest exports in closely
  related eccentric graph points on geni."* Do not start it early and do not invent the gate's
  threshold — that is hers.

- **Experiment: generate the manual parental zipper correspondences into a gitignored GEDCOM that
  the synoptic tree merge consumes.** Emma, 2026-09-05: *"I actually think a good long term
  architectural smoothing would make it so that in the pipeline they are generated into a
  gitignored gedcom that is part of the synoptic tree merge, with qids in bios being a fundamental
  part of the pipeline. But for now pipeline works well and that will be a thing to experiment
  with at the end of the queue."* `docs/correspondence-merge-proposal.md` is the proposal, not a
  decision. **The pipeline works and must not be broken** — her words — so the GEDCOM is generated
  *in addition* first, and the direct CSV read goes only once the tree route carries the same
  pairs.

---

## What this session settled, so it is not relitigated

* **Tiny GEDCOMs are the native format.** One per person, one per path, in different directories
  even when both come off the same page. `exports/tiny-profiles/`, `exports/tiny-paths/`.
* **An unknown parent is an ABSENT SLOT, never an `NN` person.** A sibling pair with no known
  parents is a `FAM` with two `CHIL` and no partners. `exports/0-scraped/` and
  `build-scraped-gedcom.py` were deleted on her instruction for inventing 4,928 people.
* **The export gate is one floor of 300 on any statistics figure**, disjunctive, and it lives in
  the extension rather than in a script the agent applies.
* **No Playwright, no headless.** `CLAUDE.md` § *PLAYWRIGHT AND HEADLESS ARE A NO-GO* — the
  agentic navigation is overhead paid to keep the traffic acceptable, not a design to improve on.
* **The anchor is on Charlemagne**, set 2026-09-06 by protocol. `docs/anchor-protocol.md`.

## Pointers

`docs/collector-run-loop.md` — her dictation of the loop, and the no-discretion rule ·
`docs/final-wikidata-geni-scrape.md` — the campaign, its scale, and its settled deliverables ·
`docs/per-individual-loop.md` — the phase order and the statistics gate ·
`docs/anchor-protocol.md` — check, set, verify · `todo.md` § 3c and § 3d ·
`devlog.md` — what happened and why · `questions.md` — open questions for her.
