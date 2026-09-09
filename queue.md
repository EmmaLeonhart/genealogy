# Queue

Only work. An item is DELETED when done, never annotated. Bullets, never numbers —
`CLAUDE.md` § *Queue items are BULLET POINTS*.

**Read `docs/collector-run-loop.md` before touching the collector.** It is your dictation of the
whole run loop and it ends *"there's no discretion on your part at all"*, said three times.

---

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

  ⛔ **AN IN-LAW CHAIN CAME BACK AS `via=blood`, AND THE CAUSE IS UNKNOWN. Miroslava, Princess of
  Bulgaria `371367105380011098`, 2026-09-09.** Her page states BOTH *"Shortest in-law
  relationship"* and *"No blood relationship was found."*, and the job still returned
  `via: blood`, `state: path_found`, with a `path_tsv` header reading `(blood)`.

  **It was blamed on 1.6.7 not running. 1.6.7 WAS running** — that explanation rested on the
  hardcoded version literal above and collapsed with it. `6b2dee75` is the fix for this shape and
  it did not prevent this, so either it does not cover this case or something else does it.
  **Nothing explains it today.**

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

  Currently holding: nine Geni profiles you called **hinge people** — *"people who seem to have
  clearly disjoint large numbers of descendants, and as such are good descendants export
  sources"* — for descendants exports later.

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
