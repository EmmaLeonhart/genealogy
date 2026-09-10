# Queue

Only work. An item is DELETED when done, never annotated. Bullets, never numbers —
`CLAUDE.md` § *Queue items are BULLET POINTS*.

**Read `docs/collector-run-loop.md` before touching the collector.** It is your dictation of the
whole run loop and it ends *"there's no discretion on your part at all"*, said three times.

---

- **⛔ BUILD THE UNCONNECTED-`P2600` WORKLIST. `docs/unconnected-worklist.md` is the
  specification, dictated 2026-09-09 and written down in full because the first attempt was lost
  to a flat phone battery. Read it before touching this.**

  **The premise was checked and is TRUE: the Wikidata tree does NOT go into the synoptic tree.**
  `rebuild-everything.py` merges `exports/**/*.ged` plus one small correspondence GEDCOM;
  Wikidata's 5,041,567 relationship edges are nowhere in `out/merged.ged`.
  `scripts/p2600-connectivity.py` does the union in memory and writes no tree.

  Six pieces, none of which exists, in dependency order:

      1. Wikidata's tree AS A GEDCOM, merged into the synoptic tree. Natively a GEDCOM
         because that preserves the family ids; a union-find over edges destroys them.
      2. neighbourhood size -- ONE number, the combined Wikidata-and-Geni neighbourhood.
      3. the TSV: qid, geni_id, neighbourhood_size, last_attempted -- in that column order.
         Membership: not linked to Charlemagne. Recalculated every run, never stored.
      4. the date carry-forward: qid and geni id fixed, size and membership recalculated,
         the date read from the PREVIOUS VERSION OF THIS FILE. There is no second file.
      5. the ordering: eligible block on top, ineligible below it ordered by when they
         become eligible; within either, neighbourhood size DESC then qid ASC.
         Eligibility is a 30-day cooldown after an attempt.
      6. the extension writing `last_attempted` every time it runs on somebody.

  Then CI runs it after the tree build.

  **Seed dates are placeholders**: `2026-09-01` where a path capture has been attempted,
  `2026-01-01` everywhere else.

  **Nothing records success, deliberately** — a connected person simply stops being generated
  into the file, and the tree build is what says so.


- **⛔ RUN THE COLLECTOR OVER THE ISOLATE TARGETS. This is the work, and it is the only executable
  item here.** You, 2026-09-06: *"all the queue did was just ask the browser agent to navigate to
  each page and run the stuff would be decent."* That is the entire loop:

      1. navigate to  https://www.geni.com/people/x/<geni id>
      2. dispatch     {job:"individual", geni_id:"<geni id>"}
      3. read the result, write the files, move to the next target

  **The agent navigates and nothing else.** Every decision — whether the path resolved, whether
  the statistics justify an export, which ancestor to add — is inside
  `geni-extension/content/individual.js`. Do not re-derive any of it in prose; that reasoning is
  the discretion you removed.

  **⛔ WHERE THE TARGETS COME FROM — AND THE TWO PILOT ROSTERS WERE NEVER THE POPULATION.**
  Emma, 2026-09-09, asked for the scope and gave it: *"Every p2600 holder who is disconnected from
  Charlemagne in the synoptic tree (combination of our geni exports and what exists on wikidata).
  The idea is that all p2600 people should either be confirmed impossible to connect, or
  connected. Connection to Charlemagne is our proxy for connection to the main graph as
  Charlemagne is one of the most central people."*

      reports/p2600-disconnected.tsv       THE POPULATION -- 266,201 people
      reports/sibling-pair-worklist.tsv    a pilot roster, 4,261 rows, kept
      reports/isolate-path-pilot.tsv       a pilot roster, COMPLETE 2026-09-06, 100 of 100

  `scripts/collector-worklist.py` drew its universe from the two pilot files alone until today
  — **4,360 people between them**, against **518,889** `P2600` holders — so the campaign ran over
  **0.8%** of the population, chosen by which roster happened to be on disk, and asked the wrong
  question about them: a person already connected needs no capture at all.
  `scripts/p2600-connectivity.py` computes the right one:

      P2600 holders            518,889
      connected to Charlemagne 252,688   48.7%   (208,985 of them via Wikidata alone)
      DISCONNECTED             266,201   51.3%   (266,195 never touched by any export)

  **The outstanding count is `wc -l reports/collector-worklist.tsv`** — 268,686 today, recomputed
  every run from what is on disk. The pilot rosters stay in `ROSTERS`: anyone in them who is
  genuinely disconnected is in the new file anyway, `scraped()` filters captured people either
  way, and dropping them would silently retire work in flight.

  **After each scrape:** `PYTHONPATH=src python scripts/build-tiny-gedcoms.py` turns everything on
  disk into tiny GEDCOMs. It is idempotent and safe to run repeatedly.

  ⛔ **THE EIGHT THINGS THAT WILL WASTE A SESSION IF YOU REDISCOVER THEM:**

  * **Nothing downloads.** Roughly two files land per browser session and Chrome blocks the rest —
    a per-origin permission needing an omnibox grant you cannot give from a phone. The job returns
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
  * ⛔ **IT WAS ON A THIRD PERSON ON 2026-09-09 — Lǐ Shìmín 李世民, Emperor Taizong of Tang — and
    was re-set by protocol that day.** *"Not viewer-anchored"* is not the same as *"on
    Charlemagne"*, and from a third-person state the pin takes **two** clicks: one back to the
    viewer, one onto Charlemagne. `docs/anchor-protocol.md` carries both that and the
    click-coordinate trap that made the first attempt look like a permission problem.
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
    verify on two real targets. Setting it is yours to do; you said so.
  * ⛔⛔ **BLOOD IS NOT THE QUESTION. IN-LAW COUNTS, AND THERE IS AT LEAST A THIRD SEARCH.**
    You, 2026-09-07: *"in-law connections are just as valid blood is no required lol"*. The loop
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

  **State right now, measured 2026-09-09 15:1x PST:** the isolate pilot is **100 of 100,
  COMPLETE** · `reports/isolates.csv` **131 rows, 131 family scrapes on disk**, of which **112
  were taken under the Charlemagne anchor: 25 hits, 87 misses** · **zero invented people** ·
  extension **1.6.8**, running and confirmed.

  **The in-law verdict is recorded for 25 of the 112** — `via` reads `neither` 12, `blood` 9,
  `inlaw` 4, and is **blank on 87**, which is every row taken before the in-law search existed.
  **75 of the 87 misses are blood-only**, so they re-enter the pool under rule 2 of § *BOTH TIES,
  ALWAYS* and are not final misses.

  ⛔ **CHECK THE RUNNING VERSION, AND KILL CHROME IF IT IS STALE.**
  `documentElement.dataset.geniCollector` reports it, and since 2026-09-09 it reads
  `chrome.runtime.getManifest().version` — it was a **hardcoded literal** until then, stuck at
  `1.6.4` through four releases and believed. An unpacked extension does not pick up file changes
  on its own and `chrome://extensions` is refused to the automation surface — **and that is not a
  blocker.** `CLAUDE.md` § *KILL CHROME WHENEVER YOU NEED TO*: `kill -9`, force-open on any page,
  the extension has reloaded. Standing authority. Never tag this BLOCKED-ON-USER-ACTION again.

  ⛔ **AN IN-LAW CHAIN COMES BACK AS `via=blood`. TWICE ON 2026-09-09, SO IT IS REPRODUCIBLE, AND
  THE CAUSE IS UNKNOWN.** Miroslava, Princess of Bulgaria `371367105380011098`, and Elen ferch
  Eudaf Hen `377649183480004232`. Both filed as `inlaw` by hand off the page banner.

  **The two differ in one way worth knowing:** Miroslava's page also said *"No blood relationship
  was found."*, Elen's did not — Geni simply returned the in-law chain as the SHORTEST. So the
  defect is not confined to the no-blood case.

  **Miroslava, the first instance:** Her page states BOTH *"Shortest in-law
  relationship"* and *"No blood relationship was found."*, and the job still returned
  `via: blood`, `state: path_found`, with a `path_tsv` header reading `(blood)`.

  **It was blamed on 1.6.7 not running. 1.6.7 WAS running** — that explanation rested on the
  hardcoded version literal above and collapsed with it. `6b2dee75` is the fix for this shape and
  it did not prevent this, so either it does not cover this case or something else does it.
  **Nothing explains it today.**

  ⛔ **THE MECHANISM, found by re-running her 2026-09-09: THE PAGE CHANGES UNDER THE JOB.**
  Sampled at three moments in one run, her page read:

      on load                  no verdict, no miss sentence
      after the blood search   "No blood relationship was found." appears
      after the in-law search  24 `span.segment`s, banner "Shortest in-law relationship"

  `runPath` reads **the chain that is on the page when it looks**, and by then that is the
  IN-LAW chain — not the one its own blood search produced. Nothing checks that the rendered
  chain belongs to the search that was dispatched. That fits both instances, and it explains why
  `6b2dee75` did not prevent them: it settles on *the segment count going up*, which is exactly
  what the in-law render does.

  It also explains the confusing detail from earlier — her page said *"No blood relationship was
  found"* in the morning, `false` when re-loaded, then `true` again mid-run. That sentence is not
  a property of the person; it is a **stage of the search**.

  **So `via` says WHICH SEARCH RAN and not what came back**, and
  every hit must be classified by hand from two things the result already carries: the relation
  words (hers crosses *"his wife"*, *"her brother"*, *"her ex-husband"*, *"his sister"*) and
  Geni's prose. Her file and ledger row were corrected to `inlaw` by hand.

  **The Chrome that is running is the `Default` profile**, and the Claude extension is
  `1.0.91` there — Profile 4 carries the same build, so the two-different-versions note this
  item used to carry is stale. Pairing is one click on **Connect** in that profile; on
  2026-09-09 the extension would not pair and `switch_browser` found nothing to prompt.

  ⛔ **`runInLaw` WAS THROWING AWAY THE IN-LAW VERDICT ON EVERY PERSON — fixed 2026-09-08 in
  1.6.6.** It looked for the *Show Me* button first and returned `not_offered` when it was
  absent; Geni states the miss in words and then removes the button, so a stated verdict read as
  *never asked*, `via` stayed blank, and `collector-worklist.py` re-queued that person forever.
  Nobody could ever be finished. It now reads the sentence before looking for a button.

  **AND THE SAME SHAPE FOR A HIT WAS MEANT TO BE CLOSED IN 1.6.7** — `6b2dee75`, *"the in-law chain was
  returned as the blood result, and scored via=both"*. `runInLaw` settled on *the segment count
  going up*, so an in-law chain Geni had already rendered before the click — Ellen
  Christensdatter Thrane `309763264470008240`, 29 segments, prose reading *"Charlemagne's third
  great granddaughter's 19th great niece"* — changed nothing and waited out the full 600000 ms.
  It compares against the chain already present now — **and 1.6.7 was running when Miroslava
  still came back mislabelled**, so this fix does not cover her case. See above.

  ⛔ **A HIT CAN COME BACK AS TWO CHAINS END TO END, numbered straight through.** Seen twice on
  2026-09-09 — Louis d'Anjou 37 rows over an 18-step and a 19-step chain, Margareta Sanseverino
  42 over 23 and 19, each second chain restarting on Charlemagne. **`path_steps` is a ROW COUNT
  and not a chain length**, so reading it as one roughly doubles the descent. The shape is safe
  — a person walked twice scores `REPEAT` — but it is new: all 11 path files the collector wrote
  before that day carry exactly one chain. Say which rows are which in the file's header.

  ⛔ **AND ONE OF THOSE SECOND CHAINS WAS THE MARRIAGE TIE, out of the BLOOD search.** Margareta's
  steps 24-42 are the descent to her HUSBAND and then one step, *"his wife"*, onto her — the ring
  § *BOTH TIES, ALWAYS* wants, with `inlaw_state` reading `not_offered` because rule 3 stops the
  second search once blood resolves. So rule 3 is cheaper than it looks: Geni sometimes
  volunteers the marriage route inside the blood answer. **This is an observation on two people,
  not a rate** — nobody has counted how often it happens.

  ⛔ **`write-family-scrape.py` WAS DOUBLE-ENCODING UTF-8 and it is the pipe this loop uses.**
  `sys.stdin.read()` decodes by locale on Windows (cp1252), so `Børge` came back `BÃ¸rge`. Fixed
  2026-09-09 with an explicit UTF-8 buffer read. **The heredoc warning above is right about the
  shape and wrong about the cause**: it is not the shell, it is anything that decodes by locale.

  **Poll in SHORT waits.** A `javascript_tool` call whose in-page `await` runs past ~45 s dies as
  *"CDP … timed out … the renderer may be frozen"*. It is not frozen and the job is not lost —
  check again in a separate call and the result is there.

  ⛔ **GENI HAS TWO MISS SHAPES AND ONLY ONE CAN BE ANSWERED.** Most profiles give the pair
  *"No blood relationship was found."* + *"No in-law relationship was found."* Katalin Varga
  `291026634180003195` gave the third form — *"No path found to Katalin Varga."* — with **no
  in-law sentence and no button at all**, so no in-law verdict is obtainable for her. Her `via`
  is blank rather than `neither`, which means she re-queues forever on the rule above. That
  population is not yet sized and nothing addresses it.

  ⛔ **THE ANCHOR COLUMN IS WHAT MAKES THAT RATE MEAN ANYTHING**, and it earned its keep on
  2026-09-06: the pin lapsed mid-run and four captures came back answering *related to you*.
  Two were **hits that became misses** once re-run under Charlemagne. Rows taken under the you
  anchor, and rows with no verdict yet, are excluded from the 92; a rate over all 111 answers a
  question nobody asked.

  **`job.create` WAS exercised on 2026-09-09 and both halves worked** — `NN`
  `6000000227675436876` created as Hans Jørgensen Hiuler's mother, Forest export back at 5,000
  people, filed to `exports/hiuler/`. What failed was the walk BETWEEN them, which had been
  handed out of the extension for the agent to hold; `content/walk.js` has the account.

  ⛔ **What is outstanding is the BACKGROUND DRIVER**: the queue, the tab loop, and the parallel
  waiting on path searches and exports. Until it exists the extension answers one person and
  nothing drives the traversal.

- **The parent-adding campaign.** GATED: it starts once the placeholder parents have been
  sufficiently gathered in the synoptic tree and a batch is on Wikidata. You, 2026-09-03: *"In
  the future after we've sufficiently gathered all the placeholder parents and added a bunch to
  wikidata we can do a parent-adding campaign, especially if we use forest exports in closely
  related eccentric graph points on geni."* Do not start it early and do not invent the gate's
  threshold — that is yours.

- **How to read a `|` in an imported label.** You, 2026-09-09, asked whether
  `noble Nike|Victoria Soutzaina` should become `Nike Soutzaina` with `Victoria Soutzaina` as an
  `Amul`: *"bruh no the pipes are a bit more complicated, I am not 100% sure how to interpret it
  lol."* **1,565 people carry one** and `reports/title-label-proposals.tsv` holds every one with
  a computed reading, unemitted. Three shapes are in there and they may not want the same answer
  — two given-name spellings (`Margaret|Margery Bulkeley`), two whole names
  (`Conrad Hofmeister|Kornmann`), and a bracketed variant group inside one
  (`Ann Bincks (Benckes|Bench)`, 136 of them, already held separately). NOT to be interpreted
  here; yours.

- **`undigested.md` — NEEDS-INVESTIGATION.** Raw text from you, verbatim and unprocessed.
  Investigating it is a real outstanding item and belongs in every status report under that tag,
  so it does not quietly disappear. **But not yet, and not unprompted** — you, 2026-09-09: *"I do
  not want you to investigate"*. It rests until you say go.

  Currently holding **two batches of hinge people** — *"people who seem to have clearly disjoint
  large numbers of descendants, and as such are good descendants export sources"* — for
  descendants exports later:

  * **eastern european tang**, nine profiles, 2026-09-09
  * **western european tang**, six profiles, 2026-09-09 — Cilician Armenia, Lampron and Barbaron

  Her distinction, not an inferred one: *"This is a new one old hinge was eastern european tang
  … thjis is western european tang"*.

- **Export DESCENDANTS of these individuals I created.** Emma, 2026-09-09, adding them at the
  end of the queue and not parked: *"do not think about this at all just add it"*. Verbatim:

      https://www.geni.com/people/NN-%D0%90%D0%BA%D1%83%D0%B4%D0%B6%D0%B1%D0%B0/6000000227676582856
      https://www.geni.com/people/NN-%D0%A7%D0%B5%D1%80%D0%BA%D0%B0%D1%81%D1%81%D0%BA%D0%B8%D0%B9/6000000227676362934
      https://www.geni.com/people/NN-Dzhilyakhstanov/6000000227676617890
      https://www.geni.com/profile/index/6000000227676697827
      https://geni.com/profile/index/6000000227676392008
      https://www.geni.com/people/NN-%D0%A7%D0%B5%D1%80%D0%BA%D0%B0%D1%81%D1%81%D0%BA%D0%B0%D1%8F/6000000227676257067
      https://www.geni.com/people/NN-%D0%A7%D0%B5%D1%80%D0%BA%D0%B0%D1%81%D1%81%D0%BA%D0%B0%D1%8F/6000000227676704828
      https://www.geni.com/people/NN-Volynskaya/6000000227676384979
      geni.com/profile/index/6000000227676454008
      https://www.geni.com/profile/index/6000000227676658979
      https://www.geni.com/people/NN-Ardzrouni/6000000227676802897

  **State: 9 of 11 DONE.** Filed into `exports/circassian-hinge/`.

      DONE  6000000227676582856   2,304 people, 1,306 families
      DONE  6000000227676362934   4,239 people, 2,275 families
      DONE  6000000227676617890   5,000 people, 2,270 families  (capped)
      DONE  6000000227676697827   3,216 people, 1,678 families
      DONE  6000000227676392008   2,303 people, 1,305 families
      DONE  6000000227676257067     646 people,   338 families
      DONE  6000000227676704828      90 people,    48 families
      DONE  6000000227676384979   5,000 people, 2,807 families  (capped)
      DONE  6000000227676454008   2,632 people, 1,450 families
      NOW   6000000227676658979   task 6000000227677942052
      TODO  6000000227676802897

  A cron grinds the list one at a time; this is idle-time work and no idle report should say
  "nothing pending" while any of it is outstanding.

  One at a time — Geni's limit, not a preference. The download button gets swallowed; navigate
  `https://www.geni.com/gedcom/request_download?task_id=<task id>` instead, and `/gedcom` lists
  every task id in a `downloadGedcom('...')` attribute — **though that attribute is not always
  in the rendered DOM**: on 2026-09-09 the rows came back with `href="#"` and the handler bound in
  JS, so the id had to come from the `/gedcom/download?task_id=` URL the submit redirects to.
  Record it at submit time rather than expecting to recover it later.

  **Submitting is scripted**, and the default walk is `BloodTree`, not `Descendants`:

      form index 1 -> input[name=walk][value=Descendants].checked = true
                      input[name=max_profiles].value = 5000
                      verify walk/id/max off the DOM, then form.submit()

---

## ALWAYS LAST — the tail

- **⛔ RUN THE EXTENSION'S EXPORTS ON EVERY PENDING PERSON. THIS IS TAIL WORK, AFTER EVERYTHING
  ELSE.** Emma, 2026-09-09: *"you run browser extension exports on all the pending people you
  cunt at the end after other tasks are completed, this is an actual tail thing."*

  The extension already decides this itself: a person who misses both searches and clears the
  **300** floor on any statistic gets `state: miss_export_warranted`, and with `job.create` set
  it walks up, creates one ancestor and runs a `Forest` export from them. `individual.js` owns
  every part of that; there is no discretion here and none is wanted.

  ⛔ **AND THE POINT OF ALL OF IT IS THE WIKIDATA ISOLATES.** Emma, same message: *"The wikidata
  isolates the entire point of the extension with its workflow."* So the collector over
  `collector-worklist.tsv` is the WORK and these exports are what falls out of it — never the
  other way round. An export campaign that crowds out the isolate captures has inverted the
  thing.

  **Scale, so nobody starts it lightly:** 2,587 outstanding on the worklist today. Geni runs one
  export at a time and that is its limit, not a setting.

- **⛔ THE DISJOINTNESS CAMPAIGN — YOUR PRIORITY ORDERING, 2026-09-09. AFTER THE WIKIDATA PATHS.**
  You: *"Yeah listing people here in their priority ordering for after other stuff done"*, and on
  the two profiles below: *"they are long term priorities... running it on them comes after the...
  after we've done all the Wikidata people's paths"*.

  The method is `scripts/descendant-frontier.py` and it is built and measured — see `devlog.md`
  2026-09-09. Per target: create an ancestor of theirs (`docs/export-seed-rules.md`), export
  `Descendants` from the created ancestor, then rank the RIM of the returned ball one pick per
  largest family cluster, and repeat outward. Your correction, same day: *"Create an ancestor of
  theirs using our algorithm, and then export descendants of them."*

  **The order, verbatim:**

  - The person I made — **Abul Hamza** `6000000227676734863`. In flight: all three exports are
    down and `reports/descendant-frontier-abul-hamza.tsv` holds the first ten rim picks. Not
    comprehensive yet, and the rest of the list waits on it.
  - **Tore Underberge III** `6000000005607672589` and **Gamle Olof** `5328189268700111491` — the
    two you linked. You placed them *"after you've comprehensively gotten the descendants of this
    particular individual"*, i.e. straight after Abul Hamza; the numbered list you then gave puts
    the Chinese clusters second, so the two readings differ by one slot and are not resolved here.
  - The two most eccentric ancient **Chinese** clusters
  - **Adasi**
  - **Genghis Khan**
  - **Aztec Emperors**
  - **Inca Emperors**
  - **Confucius**
  - **Charlemagne**
  - **Hermenegildo Gutteres**
  - **Fihr**, ancestor of the Quraysh
  - **Emperor Jimmu**

  Nothing on this list is investigated, measured or seeded until the Wikidata paths are done —
  `CLAUDE.md` § *"Add it to the end of the queue" means WRITE IT DOWN AND STOP*.

---

## What this session settled, so it is not relitigated

* **Tiny GEDCOMs are the native format.** One per person, one per path, in different directories
  even when both come off the same page. `exports/tiny-profiles/`, `exports/tiny-paths/`.
* **An unknown parent is an ABSENT SLOT, never an `NN` person.** A sibling pair with no known
  parents is a `FAM` with two `CHIL` and no partners. `exports/0-scraped/` and
  `build-scraped-gedcom.py` were deleted on your instruction for inventing 4,928 people.
* **The export gate is one floor of 300 on any statistics figure**, disjunctive, and it lives in
  the extension rather than in a script the agent applies.
* **No Playwright, no headless.** `CLAUDE.md` § *PLAYWRIGHT AND HEADLESS ARE A NO-GO* — the
  agentic navigation is overhead paid to keep the traffic acceptable, not a design to improve on.
* **The anchor is on Charlemagne**, set 2026-09-06 by protocol. `docs/anchor-protocol.md`.

## Pointers

`docs/collector-run-loop.md` — your dictation of the loop, and the no-discretion rule ·
`docs/final-wikidata-geni-scrape.md` — the campaign, its scale, and its settled deliverables ·
`docs/per-individual-loop.md` — the phase order and the statistics gate ·
`docs/anchor-protocol.md` — check, set, verify · `todo.md` § 3c and § 3d ·
`devlog.md` — what happened and why · `questions.md` — open questions for you.

---

## Returned from `CLAUDE.md`, 2026-09-09

This material was moved into `CLAUDE.md` on 2026-09-01 and never re-homed. It still
speaks in queue coordinates — *pinned to the very end of the file*, *the sections
below* — which meant nothing where it was sitting. Verbatim, nothing reworded.

## THE ALGORITHMS, moved out of `queue.md` on 2026-09-01
The queue is for work; these are specifications and standing processes, so they live here
instead.

### STANDING PROCEDURE — audit this queue against the transcripts first

**Not deleted when it completes: it is a procedure, not a step.** Run it before
executing the rest of the queue, because otherwise the rest is not trustworthy.
**Last run 2026-08-30** → `reports/user-turns.tsv` and `reports/unrecorded-instructions.tsv`
(38 transcripts, **3,679 turns since 2026-08-15**, 1,577 distinct, **243 directive and written
down nowhere**). Steps 1 and 3 are scripts now — `scripts/extract-user-turns.py` extracts
verbatim, `scripts/audit-turns-recorded.py` screens for directive shape and then for whether any
six-word run of the turn appears in `CLAUDE.md`, `queue.md`, `devlog.md`, `name modelling.txt`
or `docs/`. The screen was checked against rulings known to be recorded and flagged none of
them. A miss is a **candidate to read**, never a finding — instructions repeat, and much of what
is said is answered in the moment and needs no record.

The previous run was 2026-08-15 → `reports/audit-transcripts-2026-08-15.md` (24 transcripts,
311 user turns).

Transcripts are the authority — they hold what was actually said, in order, including the
corrections:
`C:/Users/Emma/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl`.
Newest first by mtime. Each line is JSON.

**Read BOTH record types, or the scan misses half the input.** A turn typed while the model was
idle is `{"type": "user", "message": {"role": "user"}}`. A turn typed while a tool call was
running is
`{"type": "queue-operation", "operation": "enqueue", "content": "…"}`, and it is
**not** a user record. On 2026-08-16 the split was 28 user records against 21
queue-operations, so a `role == "user"` scan finds 57% of the input. Skip the
`enqueue` entries whose content is a cron prompt or a `<task-notification>`; those
are the harness talking, not input.

1. **Extract every user turn with its timestamp.** Do not summarise while
   extracting — that is where instructions get lost. A compaction turn is not
   input: its quoted messages are evidence, its narration is not.
2. **Classify:** instruction, decision, correction, or conversation. Only the
   first three matter. **Frustration is still an instruction** — *"just fucking
   run the census"* is a queue item.
3. **For each, ask: is it done? is it here? is it in `CLAUDE.md`/`devlog.md`?**
   Done and recorded → nothing. Done and unrecorded → `devlog.md`. Not done → a
   concrete step here. A decision about how the project works → `CLAUDE.md`.
4. **Corrections outrank what they correct.** The latest statement wins and the
   superseded one must not survive anywhere as if it were current.
5. **Unrequested normalisation is its own category** — exception handling built for things that
   are not considered errors. Those go on the list to be **removed**.

---


### Always last — pinned to the very end of the file

**Bullets, not letters.** These were `A.` and `B.`; `CLAUDE.md` § *Queue items are BULLET POINTS*
covers lettering for the same reason it covers numbering.

- **Ensure the FOUR crons are running** — work-loop `3 * * * *`, auto-flush `15 * * * *`,
  status-report `42 * * * *`, and the **dead-queue-item sweep `45 * * * *`**, which removes dead
  queue items — ones that are simply completed. They are **session-only**: they die when the session ends and must be
  recreated at the start of the next one. This is not theoretical — every cron died in the
  2026-08-28 crash and none was recreated, which is why nothing ran between 00:03 and 06:00 on
  2026-08-29. Live in the 2026-09-05 session as `7c8cc0c6`, `7fb9d24f`, `9f3125b0`, `caf417ce`; the
  2026-08-31 ids (`76ec2c05`, `f4332b23`, `cedb7fc4`, `21245a1a`) and the ones before them
  are dead sessions', which is the reason to check `CronList` rather than trust this line.
  **A session once ran for hours with ZERO crons and nobody noticed.** Recreating them is the
  first thing a session does, not something to get to.

  **The status-report cron carries no `AskUserQuestion`.** It was barred overnight — move through
  the work and pick the option consistent with what is already written — so the two-hourly blocker
  question was taken out of the cron text rather than left to fire unattended. Restore it
  deliberately, not by default.

- **The three crons, as durable queue items.** The crons are good and continue, and they are also
  queue items specified as cron jobs, so they get crossed off when the job finishes but are more
  stable than the cron itself. Cron text lives only in memory, so the queue is the durable copy:

  - **Work-loop, hourly at :03** — sync, take the top actionable item, do it, commit with a
    `devlog.md` entry, push, report one line. Rails: never loosen a test, never claim verified
    without running it, no live Wikidata beyond the ledger refresh and `full_entities` before a
    correction, never generalise a named instruction into a mechanism, never invent a `.qs`
    nobody asked for.
  - **Auto-flush, hourly at :15** — commit and push anything pending, or report nothing pending.
    Never an empty commit.
  - **Status-report, hourly at :42** — reporting only. What advanced, queue state, whether the
    rails held, blockers each under exactly one not-done tag, and real test numbers from a run.

- **Run the status-report action once more** — an end-of-session summary of everything that
  happened this session.

### `P2600` constraint violations report — analysis AT THAT TIME, no pre-analysis

<https://www.wikidata.org/wiki/Wikidata:Database_reports/Constraint_violations/P2600>

The analysis happens **at that time**, with no pre-analysis: how this could help Wikidata
genealogy, and it overlaps the entity-resolution work.

So: nothing is to be investigated, measured or fetched about this before the item is
reached. The analysis is of how the constraint-violations report could help Wikidata
genealogy, and it overlaps the entity-resolution work.

### The clan labels may be much worse than we think — `Q45449130`

<https://www.wikidata.org/wiki/Q45449130>

The clan labels are likely much worse than they look, which is why they were never run, and there
is at least some evidence for it.

An analysis. Nothing was investigated when this was written.

### How to read this file

The queue was not usable, and the reason was structural rather than volume: **five sections declared
themselves the front** — the mass export campaign, the algorithm review, `THE EXPORT LOOP` (*"it is
the top of this file"*), `THE AGENDA` (*"everything else is secondary"*) and `RUN ORDER` — while
**ten declared themselves the tail**. With both ends contested there was no order to work in.

**The order is now position, and nothing else.** Top to bottom. Two conventions:

- **Bullets, never numbers** — `CLAUDE.md` § *Queue items are BULLET POINTS*. A number is a promise
  the item will still be there.
- **An item is deleted when it is done**, in the same commit as its `devlog.md` entry. A section
  still here is a step not yet taken.

**Everything titled `LAST` / `THE LAST ITEM` / `THE TAIL` is now physically at the end**, in one
run, so "last" means last. Nothing was reworded and nothing was dropped — only moved.

**Some sections are SPECIFICATIONS, not steps**, and are worth knowing about before working the
ones above them: `THE EDIT ALGORITHM`, `THE DAILY ALGORITHM`, `THE TAIL ALGORITHM`,
`Link reliability order`, `The chain of provenance`, `How the synoptic tree is actually made`,
`PREREQUISITE ORDER`. They describe how a thing is done rather than asking for it to be done.

### 0. Aug 28, 2026 manual adds

These are supposed to be manually added to the queue and worked on, do no just paraphrase during the rebase keep this part entirely intact. We are approaching usage limit for now.

### ⛔ THE RULINGS OF 2026-09-01 — the interview. These OVERRIDE the sections below

Every item was ruled on. Where a section below disagrees with this table, this table wins; the
sections are kept for their detail, not their status.

**Deleted outright, already removed:** the eight Asian identities · Bure kinship random-walk ·
the World-Tree review and its `universe` note · the chains as a SYSTEM · the six unwalked
algorithm steps · the four-label census · resolving names against the store · the 46%/41%
transliteration measurement (*"accept it and move on"*).

**Moved to the tail:** link reliability / `P1038` — *"we have the established method of
identifying parents and that works, siblings are just freely made and merged lol we only need a
scalable zipper thing much later"* · the `synoptic tree` vocabulary split · **creating the
fathers patronymics imply — *"postpone for a month lol"***.

**To do — the table was 20 rows and 18 are finished.** Each one's evidence is in
`devlog.md` for 2026-09-01 and its artifact is on disk; they are removed here so the queue reads
as outstanding work rather than as a record of a night. What is left of it:

| item | ruling | where it stands |
| --- | --- | --- |
| seven languages | wire `hi`/`ar`/`ru`/`el` **now**, and close the `en` shortfall | `hi`/`ar`/`ru`/`el` **done**, 151,320 labels. The `en` shortfall turned out to need in-law relation words that have not been sanctioned — a decision, not arithmetic |
| `exports/post-merge/` | do the stale-duplicate resolution | graded: **408 of 412 are real deletions**. The standing ruling is to leave them and keep measuring |

**Removed as done**, all verified by artifact rather than by memory: the `en` agreement rule ·
labels in the specified order (`en`/`mul`/`ja`/`zh`/`ko`) · name items reused by default · `Sara /NN/` and
the `Garborg` override · the label-change census · `ko` · the NN birth-name alias · the unreadable
transliteration tokens · the 218-script sweep · one batch file, names first · the clan labels ·
the export loop · the 179 ambiguous patronymics · `P407` by suffix · the `Nils`/`Nicolaus` form
table · the succession CSV · `pykakasi`, `BET x AND y` and the 74 MB file · the final rebuild.

### Anonymisation is NOT redacting the tree. It is scrubbing the repo of strategy

**The criterion: we show no more information than Geni does, so it is anonymised.**

**So the tree is ALREADY anonymised, and it always was.** This repo republishes what Geni
publishes and nothing beyond it — no field is derived that Geni does not itself display, and no
profile is enriched from elsewhere. That is the whole test, and it is met by construction.

**NOBODY IS EXCLUDED. No row is dropped, redacted or held back**, and a summary that leaves this
ambiguous is wrong: a sweep report once said "your redefinition of anonymising", which reads as
implying the private people had been cut. They have not been. Checked the same day:
`reports/derived-labels.csv` carries **20,928 rows with a redaction marker** out of 1,451,964, and
the corpus keeps all **94,071 `Private`** and **17,548 `<private>`** markers. § *Redacted people
go in* is the governing rule and is untouched — the person is created, the marker never becomes a
label.

**This replaces the ~96,000-private-rows reading entirely**, and that reading was wrong in
substance rather than merely superseded: it treated the private profiles as a *gate* to be cleared
before going public, when they were never an obstacle at all.

Cut the content in this repo that discusses **strategy around the account owner's own item and
how the account's editing is perceived**, and remove **code that treats that item as special**. The spine is the Arne→Bureus one only, and a task for 2026-09-02 removes that and all
spine logic once it is complete.

So three things, and none of them touches a person's data:

- **Cut the strategy content.** Anything in `CLAUDE.md`, `queue.md`, `devlog.md` or the scripts
  about how that item gets linked or how the account's editing reads to others.
- **Remove code that treats that item as special.** `NEVER_TOUCH_QID`, the exclusion entries, and
  anything else keyed on a specific person's ids. **Done 2026-09-01** — no exclusion set, banned
  list or test names an individual any more; the only hold left is the Kitajima one and it expires
  2026-10-01.
- **`SPINE_PATHS` keeps only Arne → Bureus**, which is already true.

**The repo is public as of 2026-09-01** — *"The repo is public now lol"* — so Actions minutes are
free and `CLAUDE.md` § *Cost* no longer binds.

### Pointers

- Abstract backlog: `todo.md` · Completed work: `devlog.md` · History: `git log`
- Open questions: `questions.md`
- The pre-wipe queue, 1,396 lines: `git show 4127170:queue.md`

### ⛔ `exports/post-merge/` — MOVED TO THE TAIL, 2026-08-29

408 of the 412 falsifiable drops are real deletions. **Leave them in the tree, keep running the
measurement, decide later** — the lean is toward saving the 408 rather than dropping them, but
there is no bandwidth to process it now. Nothing is applied and no override is written.

`scripts/grade-post-merge-drops.py` → `reports/post-merge-falsifiable.tsv` is the standing
measurement — 408 `link-gone`, 2 still linked, 2 with no shared family, over 159 parents,
159 children and 90 spouses.
