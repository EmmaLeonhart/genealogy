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

  **Where the targets come from:**

      reports/isolate-path-pilot.tsv       ⛔ COMPLETE 2026-09-06, 100 of 100
      reports/sibling-pair-worklist.tsv    the live list -- 2,526 people with no scrape yet

  The remaining count is any `geni_id` in the worklist with no `geni-families/<id>-family.tsv`:

      awk -F'	' 'NR>1{print $2}' reports/sibling-pair-worklist.tsv |
        while read -r id; do [ -f "geni-families/$id-family.tsv" ] || echo "$id"; done | wc -l

  `python scripts/pilot-progress.py` still prints the pilot's own count and should read 100/100.

  **After each scrape:** `PYTHONPATH=src python scripts/build-tiny-gedcoms.py` turns everything on
  disk into tiny GEDCOMs. It is idempotent and safe to run repeatedly.

  ⛔ **THE EIGHT THINGS THAT WILL WASTE A SESSION IF YOU REDISCOVER THEM:**

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
  * ⛔ **`no_panel` HAS NEVER ONCE MEANT "STILL RUNNING".** Every one seen on 2026-09-06 — and it
    was the state's whole population that day — turned out to be a page stating
    **`No path found to <name>.`**, a third miss sentence `pathState` could not read until 1.6.2.
    Until Chrome restarts and loads 1.6.2, read the banner off the page at harvest time rather
    than trusting `path_state`.
  * ⛔⛔ **CHECK THE ANCHOR ON EVERY CAPTURE, NOT ONCE A SESSION. IT EXPIRES ON ITS OWN.**
    It came off Charlemagne mid-run on 2026-09-06 after ten good captures, with nobody touching
    it, and **a viewer-anchored hit looks exactly like a real one** — `resolved_path`, a full
    chain, confident prose. The tell is free and already in the result:

        step 1 == geni:6000000002457013227   -> Charlemagne. the capture counts.
        step 1 == geni:6000000087535357291   -> "You". it answers a different question.

    Geni's prose says the same: *"is Charlemagne's Nth great grandson"* against *"is your ..."*.
    Read one before writing any path file. `write-family-scrape.py` stamps `ANCHOR` from a module
    constant and **cannot see the page**, so nothing downstream will catch it.
    A **miss** gives no warning at all — no chain, identical banner — so if a hit comes back
    viewer-anchored, treat every miss since the last verified capture as suspect.
    Re-set it with `docs/anchor-protocol.md`: check on Charlemagne's own page, click the pin,
    verify on two real targets. Setting it is yours to do; she said so.
  * ⛔⛔ **BLOOD IS NOT THE QUESTION. IN-LAW COUNTS, AND THERE IS AT LEAST A THIRD SEARCH.**
    Emma, 2026-09-07: *"in-law connections are just as valid blood is no required lol"*. The loop
    asked Geni only for the blood path until 1.6.3, so **every `no` in `reports/isolates.csv`
    predating that means *no BLOOD path* and nothing more.** `GC.runInLaw` now clicks *Show Me*
    after a blood miss — and **only** after one: *"do not waste time redoing it on ones that have
    blood paths already."*
    ⛔ **AND IT IS NOT DONE.** Measured on Anna Hørlück `297536201290008921`: after
    *"No in-law relationship was found."* the page **still** offers *"They might be connected in
    other ways"* with another **Show Me**. So Geni has a third search that nothing has run and
    nobody has named. Establish what it returns before calling any person a final miss.
  * ⛔ **A HIT CANNOT BE READ OFF THE PAGE.** `path_state` is asymmetric by design; only the job's
    `resolved_path` + `hasTarget` establishes one. Pass `@PATH yes` to `write-family-scrape.py`
    when it does, or a confirmed hit is filed as pending.
  * **Long results truncate mid-row.** A family of ~10+ overflows the tool result; fetch the rows
    in slices and check the count before writing. A truncated line is visibly truncated, which is
    why the transport is tab-separated rather than JSON.
  * **The background service worker cannot be updated from here** and does not matter — it runs
    only the scheduler. `todo.md` § 3d has the measurement and five failed routes.

  **State right now, 2026-09-08:** the isolate pilot is **100 of 100, COMPLETE** ·
  `reports/isolates.csv` 118 rows, of which **99 were taken under the Charlemagne anchor: 15 hits,
  84 misses** · `reports/collector-worklist.tsv` has **2,592 outstanding** (2,510 never scraped,
  82 blood-only misses) · **zero invented people** · extension **1.6.6 on disk**.

  ⛔ **THE RUNNING CHROME IS STILL ON 1.6.5 UNTIL SOMEBODY RELOADS THE EXTENSION.** An unpacked
  extension does not pick up file changes on its own, and `chrome://extensions` is refused by the
  automation surface the same way `chrome://` always is. One click in that page, or a Chrome
  restart, loads 1.6.6. Until then the loop still returns `not_offered` for an in-law verdict
  that is stated on the page, and the harvest has to apply the same rule by hand.

  ⛔ **`runInLaw` WAS THROWING AWAY THE IN-LAW VERDICT ON EVERY PERSON — fixed 2026-09-08 in
  1.6.6.** It looked for the *Show Me* button first and returned `not_offered` when it was
  absent; Geni states the miss in words and then removes the button, so a stated verdict read as
  *never asked*, `via` stayed blank, and `collector-worklist.py` re-queued that person forever.
  Nobody could ever be finished. It now reads the sentence before looking for a button.

  ⛔ **AND THE SAME SHAPE IS STILL OPEN FOR A HIT.** `runInLaw` settles on *the segment count
  going up*, so when Geni has already rendered the in-law chain before the click — Ellen
  Christensdatter Thrane `309763264470008240`, 29 segments on the page, prose reading
  *"Charlemagne's third great granddaughter's 19th great niece"* — nothing changes and it waits
  out the full 600000 ms. Not a miss and not lost, just slow. The asymmetry rule says a hit needs
  a parsed chain rather than prose, so the fix is to compare against the chain already present,
  not to trust the sentence.

  ⛔ **GENI HAS TWO MISS SHAPES AND ONLY ONE CAN BE ANSWERED.** Most profiles give the pair
  *"No blood relationship was found."* + *"No in-law relationship was found."* Katalin Varga
  `291026634180003195` gave the third form — *"No path found to Katalin Varga."* — with **no
  in-law sentence and no button at all**, so no in-law verdict is obtainable for her. Her `via`
  is blank rather than `neither`, which means she re-queues forever on the rule above. That
  population is not yet sized and nothing addresses it.

  ⛔ **THE ANCHOR COLUMN IS WHAT MAKES THAT RATE MEAN ANYTHING**, and it earned its keep on
  2026-09-06: the pin lapsed mid-run and four captures came back answering *related to Emma*.
  Two were **hits that became misses** once re-run under Charlemagne. Rows taken under the Emma
  anchor, and rows with no verdict yet, are excluded from the 92; a rate over all 111 answers a
  question nobody asked.

  **The live-site writes sit behind `job.create`.** Setting it lets the loop create one ancestor
  and run a `Forest` export when the gate clears. It has not been exercised yet, so the first one
  is worth watching.

- **A PICK-ONE card for the ambiguous family slots.** The child/sibling deck only offers a slot
  where both sides hold exactly one person of that sex; **12,125 slots hold more** — 8,207 child
  and 3,918 sibling, in `reports/family-candidates.tsv`'s own run output. The common shape is
  `N x 1`, which asks *which of our N is this item?*, and a Same/Different card cannot say that:
  offering it as N yes/no cards invites N Sames. It needs a card that shows the sibship on both
  sides and lets her pick one, or none. The export format must stay the five columns her *Copy
  decisions* button already produces, so the paste-back into `reports/emma-judgments.tsv` does
  not change.

- **The parent-adding campaign.** GATED: it starts once the placeholder parents have been
  sufficiently gathered in the synoptic tree and a batch is on Wikidata. Emma, 2026-09-03: *"In
  the future after we've sufficiently gathered all the placeholder parents and added a bunch to
  wikidata we can do a parent-adding campaign, especially if we use forest exports in closely
  related eccentric graph points on geni."* Do not start it early and do not invent the gate's
  threshold — that is hers.

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
