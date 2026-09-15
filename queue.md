# Queue

Only work. An item is DELETED when done, never annotated. Bullets, never numbers —
`CLAUDE.md` § *Queue items are BULLET POINTS*.

**Read `docs/collector-run-loop.md` before touching the collector.** It is your dictation of the
whole run loop and it ends *"there's no discretion on your part at all"*, said three times.

---

## ⛔ EMMA'S OWN ITEMS, AND THEY COME FIRST

### ⛔ THE PATH COLLECTION IS A BACKGROUND ASSUMPTION, NOT THE FIRST ITEM. Ruled 2026-09-14

*"I think the paths collection being the first item made it so that you had a tendency to not do
other stuff... change up the queue item to make it be a background assumption that we are running
the path collection."*

**It runs. It needs no attention. It is not the thing you work on.** The requester and the chain
fetcher live in the geni.com tab, read their target lists off disk in chunks, and resume
themselves. Checking on them is not work; the only queue item about them is the restart check
pinned at the very end of this file.

State as of 2026-09-14: 8,000+ people requested with 12 failures, 2,150 chains fetched, 2,807
tiny path GEDCOMs, 773 isolates reached.

⛔ **PACE IT.** 500+ back-to-back census reads got the account CAPTCHAd on 2026-09-12. The stagger
is the extension's, never a sleep in the agent.

### ⛔ WIKIDATA EDITING IS HELD. Ruled 2026-09-13, and it is a STOP ORDER, not a date.

*"you had no business having any submissions going through until everything was done. That's why
it was at the end of the queue. Really, the submission should even have a requirement that all of
the Wikidata people get connected. Get connected with the path thing. So disable any editing of
Wikidata by the runner right now ... because we aren't ready for it. And the queue structure was
supposed to make that be the case."*

`HELD = True` in `scripts/wikidata_lockout.py` and `EDITS_HELD: "yes"` in
`.github/workflows/wikidata-edits.yml`, checked by both `editing_allowed` and
`automation_allowed`, with no environment override — a date arrives on its own, a hold is lifted
by a person. `tests/test_wikidata_start_date.py` fails if the two halves disagree.

**The condition for lifting it is stated and is not a date either**: the Wikidata people are
connected through the path search first. That campaign is at the END of this file.

### ⛔ SKJALGSSON IS DROPPED. Ruled 2026-09-13: *"Drop skjalgsson please"*.

Not paused and not finished-by-measurement — dropped. Three balls are filed under
`exports/skjalgsson/` and they stay in the corpus; nothing further is seeded, sampled or
re-swept there, and its banked hit is spent. Do not re-derive it from `reports/density.md` or
from any roster.


They were sitting BELOW two sections headed *ALWAYS LAST* and *THE END OF THE
QUEUE*, which is how a list gets ordered by when a thing was appended instead of by
what it is. Ruled 2026-09-13: *"uhh why did you shit the bed so hard with queue
ordering lol"*. Anything typed here by hand outranks anything derived.

## Final item

please just get the pipeline to run all of the quickstatements as wikidata edits directly. Or really generate the quickstatements file every day and an additional smaller amount of edits (about 50%) every day run autonomously connected to wikidata

**⛔ THE MECHANISM IS BUILT. WHAT REMAINS IS EMMA'S TO LIFT.** Checked 2026-09-14:
`.github/workflows/wikidata-edits.yml` is scheduled `7 8 * * *`, sends
`reports/wikidata-garborg-day.txt` at `limit=100`, and goes live from
`AUTOMATION_START_DATE 2026-09-15`. `pipeline.yml` regenerates the batch daily. The only thing
stopping it is `EDITS_HELD: "yes"`, and the condition for lifting that is stated in the hold
item above — the Wikidata people get connected through the path search first — which is a
campaign at the END of this file, not a date.

**So do not treat the go-live date as the trigger.** 2026-09-15 is when the SCHEDULE is allowed
to send; the hold is what decides whether it does, and a hold is lifted by a person.

**What was actually wrong, and is now fixed:** the batch as committed would have sent 63
creations for people already holding QIDs in `reports/garborg-qids.tsv` — the ledger was
refreshed by a tree rebuild after the batch was composed — plus two name items labelled `(Ulf`
and `Horsnäs)`. `wikidata-edit-run.load_batch` now refuses both, on every batch format, because
the runner is the last thing between a file on disk and Wikidata. 216 edits → 151, 75 creations
→ 10 on the file as it stands.

**The remaining question is the 50%**, which is the only part of this item nobody has settled:
*"an additional smaller amount of edits (about 50%) every day"*. The workflow sends `limit=100`
from one file. Fifty per cent OF WHAT is not written down anywhere — of the day's generated
statements, of the carry-forward, of the caps. ⛔ ASK before implementing a reading of it.

## Additional item

Given names and surnames should have our standardized cjk-izations attached to them. imo they should even be the source of it in the logic. update the old ones to this form and new ones are always gonna be created in this manner

## Another item

Export descendants of these people, idk their status, ancestor climb and then descendants export

Sayaluna ata 6000000008384075400, 
Hélène de Corday 6000000000746523797, 
Robert d'Esneval VI 6000000026257912323, 
Inês de Bettencourt I 6000000001435366077, 
Pietro Antonio di Capua 6000000015633226273, 
Jacques Grimaldi 6000000015647948256. 

## Another item

read this https://pastebin.com/npAiDNLg using the chrome extension. View all of the pages since this is not really optimally organized, but set these as qid identifications

Look over this guy's contributions https://www.wikidata.org/wiki/Special:Contributions/Marcus.linneberg I think we might be able to do a lot of geni identifications from them. That pastebin was my hasty ones. But we can do it systematically

## Patronymic matronymic stuff

We really should be always creating patronymics in pairs. Feminine and masculine version in a pair in the quickstatements

So for example

Bjornsdatter
Bjornsson

Would be made at the same time

Honestly I am not 100% sure about all of this stuff. But I think the spelling equivalents are just regional and there is a clear distinction there

### Other traditions

I still think we do not have support for other languages like Semitic languages and celtic languages and their patronymics

Romance languages should be there too but I think they are the hardest and the most dead

## another item

address the problem in "address the problem in this image.png"

## CICD

Make the CICD do about half the edits every day automatically. Produce disjoint quickstatements on the github page too. MAke them actually start running.

---

- **⛔ THE ALGORITHM IS STATELESS EXCEPT FOR TWO THINGS. Ruled 2026-09-10.**
  *"This entire algorithm is completely stateless except for the actual connectivity graph of
  which it is built off of, and the dates of attempts."*

      the connectivity graph   rebuilt from the GEDCOMs in `exports/` every CI run
      last_attempted           carried across the rebuild by `load_previous`, and NOTHING ELSE is
      everything else          recomputed, or a placeholder rewritten every build

  **An attempt produces exactly two things:** a GEDCOM file that exists or does not, and a date
  in `reports/unconnected-p2600.tsv`. So *has this person been exported* is answered by looking
  for the file, and *what are their statistics* by scraping them again. Membership needs no state
  either — a person who gets connected stops being generated into the file, and nothing marks
  them done.

  **Verified 2026-09-10:** `load_previous` carries **266,201 dates** into a rebuild; the six
  statistics/`exported` columns are rewritten as `200 200 200 200 200 no`.

  ⛔ **DO NOT ADD STATE TO THIS.** A `load_extras` carrying those six columns across a rebuild was
  written and removed the same day; it looked like protecting data from a from-scratch rewrite
  and was really the introduction of state. Sweep rules, flags and registers proposed on top of
  this are the same error — *"you don't need to come up with new ideas. In fact, you actively
  shouldn't."*

- **⛔ RUN THE COLLECTOR OVER THE ISOLATE TARGETS.**
  ⛔ **ITS POSITION IS THE END OF THE FILE, NOT HERE.** Ruled 2026-09-13 — see
  § *Wikidata isolate connection*, which is the gate: everything else, then every isolate
  attempted, then editing may be unheld. This section is the HOW and that one is the WHEN. The
  line that used to open it — *"This is the work, and it is the only executable item here"* —
  was true when it was the only executable item and is not true now; it is struck rather than
  deleted because the loop below it is still the procedure to follow when the gate is reached.

  You, 2026-09-06: *"all the queue did was just ask the browser agent to navigate to
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
  * ⛔⛔ **RETIRED 2026-09-10. THERE IS NO PIN.** *"We are not centering the paths on Charlemagne
    anymore ... We just request paths to whoever it defaults to."* So the per-capture anchor
    check below, the check-set-verify protocol in `docs/anchor-protocol.md`, and the two-click
    re-pin from a third person are all gone: the run asks for the default path and records what
    comes back. `write-family-scrape.py`'s `ANCHOR` is `default`, and rows already reading
    `charlemagne` or `viewer` keep their own value because the anchor belongs to the observation
    that made it.

    **The superseded rule, kept for its detail only:**

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

  ⛔ **RULED TRIVIAL, 2026-09-10. DO NOT SPEND TIME ON IT.** *"If I understand the error, the
  error is that it is treating the non-blood relationship as a blood relationship while storing
  the path, but it still stores the path correctly. This is a bothersome error, but it's also an
  error that I frankly don't care about if we actually get shit done."* **The path is the
  deliverable and the path is correct.** A wrong `via` on somebody who has no blood relationship
  at all costs nothing, and one recorded path per individual is enough — *"I'd be legitimately
  cool with making it so that only one relationship path was kept for every single individual,
  and we consistently get 5 people a minute."* Throughput beats this. The one case that would
  matter is a person with BOTH a blood and an in-law path, where the labels would then disagree
  about which was found; that is not what any of the five instances are.

  **The five instances, kept as a record and not as an open question:** Miroslava of Bulgaria,
  Elen ferch Eudaf Hen, Wen Jifu 文及甫, Bai Jian 白建, Bai Shitong 白士通. The last three share a
  24-step spine whose marriage crossing is at step 10, and the last two are father and son.

  **The superseded alarm, kept for its detail only:**

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

  ⛔ **RULED 2026-09-10: THE THIRD MISS SHAPE IS NOT A DEFECT AND NOT A BLOCKER.** *"They are
  supposed to go in the queue cycling forever."* A person Geni answers with *"No path found to
  <name>."* keeps a blank `via`, gets stamped, waits out the 30-day cooldown and comes round
  again. That is the design. Measured the same day: **20 of 43 misses, 47%**, take this shape,
  and it was written up as a blocker three times before being ruled on. It is not one.

  **AND STAYING FOREVER IS THE POINT, not a cost the design tolerates.** *"The ideal
  implementation of this is that things end up failing and going into the queue, and they just
  stay there forever ... because that establishes a clear base of people who are isolated and of
  which we have the ability to potentially try to connect through other ways, or I have the
  ability to connect it. And other people might connect them, say, on Wikidata. And the people
  disappear as we address it."* So the file is a **register of the isolated**, not a worklist
  that ought to drain: a person leaves it by being CONNECTED, by anyone and by any route, and
  membership is recomputed every build and never stored (§ 3) precisely so that leaving needs no
  bookkeeping. A change that let people "finish" without being connected would delete the
  register and answer a question nobody asked.

  ⛔ **AND THE CBDB CLUSTER IS THE SAME SHAPE OF NON-PROBLEM.** *"All they're supposed to be
  doing here is we just have set its dates ... we treat them as though we've done it. It's
  gonna be at least thirty days until they're addressed again. So that's it."* 224 people,
  managed by `CBDB (China Biographical Database)`, no `Add Family` link, not editable. They are
  visited, they fail, they are stamped, they come back in thirty days. No campaign is owed on
  them and none is to be started.

  ⛔ **SUPERSEDED THE SAME DAY — THEY ARE PARKED AT `2026-10-31` RATHER THAN CYCLING.** Emma,
  2026-09-10: *"As far as the cbdb people go I think the solution is creating someone and merging
  them in. But honestly cbdb people can all get their date last edited set to October 31, 2026 so
  that we don't need to deal with their bullshit. This means every wikidata item with 'cbdb' in
  its English description."*

  **DONE 2026-09-10 — 54,164 people parked.** `scripts/scan-cbdb-items.py` and
  `scripts/park-cbdb-attempts.py`; see `devlog.md`. **41,373 of them were already in the
  disconnected worklist, which is 15.5% of the 266,201.**

  **The real fix is named and NOT started:** *"creating someone and merging them in."* It is
  written down here and nothing about it is to be investigated — `CLAUDE.md` § *"Add it to the
  end of the queue" means WRITE IT DOWN AND STOP*.

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

- **⛔ THE OneTab PAGE, DIGESTED 2026-09-09. 19 people off the Cilician Armenian side.**
  It was held on *"I do not want you to investigate"* and released the same day: digest it the
  way the 15 hinge people were digested, **without judging which are worth exporting**. So this
  is the roster and nothing about it is a recommendation.

  `https://www.one-tab.com/page/2msuxPNbTrOZicwGHbqiLQ` — **25 links, 19 distinct people.** Every
  one carries a `through=` parameter, and every one of those six is a WESTERN EUROPEAN TANG hinge
  person, so the page is the neighbourhood of the six already queued rather than a new group.

  **Through Constantine, lord of Barbaron `6000000006101354662`** — 9, the largest fan-out

      6000000024948782278  Constantine, Lord of Neghir and Partzerpert   b. - 1308
      6000000006101354658  Stephanie of Barbaron                         c.1200-1274   *
      6000000006101430421  Hetum I, king of Armenia                      1215-1270     *
      6000000008049080226  Stephanie of Barbaron, reine de Chypre        1217-1249     *
      6000000011635945929  Maria de Barbaron                                           *
      6000000006101354644  Auschin I                                     b. - 1265     *
      6000000127383032880  Smbat, lord of Barbaron                       b. - 1275     *
      6000000024948121730  Vacahk, Lord of Gantschi                      b. - 1285
      6000000024948571097  Yovhanes, Archbishop of Sis                   b. - 1289

  **Through Constantine I, lord of Lampron `6000000006101354653`** — 5

      6000000224176114841  Oshin of Lampron, lord of Asgouras and Marnick  b. - c.1294
      6000000006101354667  Hetum IV Lampron                                c.1220-1250
      6000000006101354678  Schahandoukht                                   b. - c.1274
      6000000006101354649  Alix
      6000000006101354683  Kyranna of Lampron                              b. - 1274

  **Through Ruben III Rouponi `6000000007086662766`** — 2

      6000000007086577488  Alice of Armenia                              1182-c.1234
      6000000006727876826  Philippa, princess of Armenia                 1183-c.1219

  **Through Leo I the Magnificent `6000000006101430432`** — 2

      6000000003146970482  Stephanie of Armenia (Rita)
      6000000006101430426  Isabella I, queen of Cilician Armenia

  **Through Tolita Doleta of Armenia `6000000006101354628`** — 1

      6000000006101354617  Hugues l'Embriaco de Gibelet

  **The six starred people are reached through BOTH Constantine of Barbaron and Princess Alix de
  Lampron `6000000006101354712`**, which is the whole of Alix's fan-out — she adds no seventh
  person of her own. That overlap is the reason 25 links are 19 people, and it is a fact about
  the page, not an inference about the family.

  **⛔ ALL NINETEEN ARE ALREADY IN THE CORPUS** — one pass of `grep -rhoE` over `exports/`,
  2026-09-09, and every id is present, between **29 and 95 xref occurrences** each: Isabella I
  95, Philippa 74, Alice of Armenia 67, Smbat 56, and no id below 29. So the page is a
  neighbourhood the corpus has already gathered, not new material to fetch.

  That is the grep § *GREP THE CORPUS BEFORE RUNNING AN EXPORT* asks for and it is stated as a
  count, not as a verdict: whether an export is warranted on any of them is untouched here, per
  *without judging which are worth exporting*.

- **The parent-adding campaign.** GATED: it starts once the placeholder parents have been
  sufficiently gathered in the synoptic tree and a batch is on Wikidata. You, 2026-09-03: *"In
  the future after we've sufficiently gathered all the placeholder parents and added a bunch to
  wikidata we can do a parent-adding campaign, especially if we use forest exports in closely
  related eccentric graph points on geni."*

  **⛔ THE GATE IS DIMINISHING RETURNS, NOT A COUNT — ruled 2026-09-09**, the same stopping
  condition as the descendants campaign: it opens when a run stops finding many new placeholder
  parents. **Do not invent a number**; a fixed target answers *have we done enough arithmetic*
  and the question is whether the gathering is still paying. `CLAUDE.md` § *THE STOPPING
  CONDITION IS DIMINISHING RETURNS, NOT A COUNT* is the same rule in the other campaign, and it
  is now this one's too.

  **Nothing measures it yet**, which is the outstanding piece: the rate of new placeholder
  parents per run has to be reported somewhere before anyone can see it flatten.

- **PULL THE CJK CULTURE VERDICTS INTO THE REPO.** The queue is live —
  <https://claude.ai/code/artifact/f6b7d351-e367-4237-9c16-c9e3457d5fee> — **137 people**, each
  shown with their romanised relatives and the classifier's refusal sentence. Verdicts persist in
  the artifact's own store as they are made.

  **`reports/cjk-culture-manual.tsv` holds 32 of the 137 verdicts as of 2026-09-12** — it was
  committed with its header and no rows and has been partly filled since — and
  `build-cjk-romanisation.py` reads it every run as evidence 5, applied after all five tiers so a
  character rule cannot silently overrule a person.

  **⛔ THE STORE IS NOT REACHABLE FROM A SCRIPT.** It is read with the Artifact tool from inside a
  session, so this is a step somebody takes and cannot be a cron:

      1. read the artifact's `cultures` collection
      2. write the rows into `reports/cjk-culture-manual.tsv` — geni_id, culture, cjk, decided_at
      3. commit, and the next rebuild picks them up

  **The number to watch on that rebuild is how many verdicts OVERRULED the classifier**, which
  the run prints. It is the error rate on exactly the people it found hardest, and it is the only
  measurement that says whether the classifier is worth keeping at all.

## ALWAYS LAST — the tail

- **⛔ RUN THE EXTENSION'S EXPORTS ON EVERY PENDING PERSON. THIS IS TAIL WORK, AFTER EVERYTHING
  ELSE.** Emma, 2026-09-09: *"you run browser extension exports on all the pending people you
  cunt at the end after other tasks are completed, this is an actual tail thing."*

  The extension already decides this itself: a person who misses both searches and clears the
  **250** floor on any statistic gets `state: miss_export_warranted`, and with `job.create` set
  it walks up, creates one ancestor and runs a `Forest` export from them. `individual.js` owns
  every part of that; there is no discretion here and none is wanted.

  ⛔ **AND THE POINT OF ALL OF IT IS THE WIKIDATA ISOLATES.** Emma, same message: *"The wikidata
  isolates the entire point of the extension with its workflow."* So the collector over
  `collector-worklist.tsv` is the WORK and these exports are what falls out of it — never the
  other way round. An export campaign that crowds out the isolate captures has inverted the
  thing.

  **Scale, so nobody starts it lightly:** 2,587 outstanding on the worklist today. Geni runs one
  export at a time and that is its limit, not a setting.

- **⛔ EXPORT FROM THESE SIX FIRST — found in Abul Hamza's ball, 2026-09-10.** They cleared the
  descendants threshold on a random pick and each one is an individual export to run **before**
  the general descendants-of-Abul-Hamza process below.

      6000000008384075400  Sayaluna ata                15,000   (Geni's display ceiling)
      6000000000746523797  Hélène de Corday            15,000   (ceiling)
      6000000026257912323  Robert d'Esneval, VI        15,000   (ceiling)
      6000000001435366077  Inês de Bettencourt, I      15,000   (ceiling)
      6000000015633226273  Pietro Antonio di Capua     12,476
      6000000015647948256  Jacques Grimaldi            11,468

  **⛔ YOU CANNOT EXPORT DIRECTLY FROM THE PERSON.** Measured on Jacques Grimaldi the same day:
  `https://www.geni.com/gedcom/export/6000000015647948256` returns **"You are not allowed to
  export that profile."** The account may only export from a profile it owns, which is what the
  seed rule has always been for — *create an ANCESTOR of them per `docs/export-seed-rules.md`,
  then run a `Descendants` export on the created ancestor.* A bare export job on somebody else's
  profile is refused, and that refusal is the reason the ancestor step exists rather than a
  formality on top of it.

  **The threshold is 4,000**, ruled 2026-09-10: *"you choose a random person of the 5,000
  available candidates and check if they have 5,000 descendants or more. I'm thinking,
  realistically, 4,000."*

  **⛔ AND THERE IS NO QUEUE.** *"There isn't even supposed to be a queue — the queue is only a
  thing that exists because of the fact that you violated the principles."* Pick one person at
  random, read the number, and if it passes go **immediately** into the export on them, finish it,
  and only then look at anybody else. Do not sample ahead, do not tabulate, do not build a census.
  These six are written down because they were already found, not as a batch to work through.

- **⛔ THE DISJOINTNESS CAMPAIGN — YOUR PRIORITY ORDERING, 2026-09-09. AFTER THE WIKIDATA PATHS.**
  You: *"Yeah listing people here in their priority ordering for after other stuff done"*, and on
  the two profiles below: *"they are long term priorities... running it on them comes after the...
  after we've done all the Wikidata people's paths"*.

  **⛔ THE PICK RULE IS RANDOM SAMPLING + THE CENSUS NUMBER. The family-cluster rule is DEAD.**
  Ruled 2026-09-09, superseding the one-per-largest-cluster answer given earlier the same day:
  *"stop with the large family clusters. Just randomly pick people in the graph and find out if
  anybody has listed 5,000 descendants, and then you perform the operation on them."*

      1. pick people from the ball at RANDOM -- not by cluster, not by size, not by name
      2. read the Geni profile's `descendants` statistic on each
      3. for each SATURATED one (5,000):
           a. create an ANCESTOR of them, per `docs/export-seed-rules.md`
           b. run a `Descendants` export on that created ancestor

  **⛔ `Descendants`, NOT `Forest`. This overrides the style in `docs/export-seed-rules.md`.**
  Ruled 2026-09-09: *"if the person has 5000 descendants then you create an ancestor of them
  according to the existing algorithm and run a descendants export on them instead of the typical
  forest."* That file fixes the export at `Forest`, size 5000, and `CLAUDE.md` § *ANYTHING ODD
  ABOUT A PERSON -> FOREST EXPORT* reaches for `Forest` as the standing response — **neither
  applies here.** `Forest` follows spouse links and spends the 5,000 slots sideways; this campaign
  wants the ball to go **down**, so every slot spent on an in-law is a descendant not gathered.
  Everything else about seed creation — where the placeholder goes, what it is named, the
  five-tier preference order — is unchanged and that file is still the authority for it.

  A saturated census number means Geni knows there is more below that person than one export can
  hold, which is exactly the person worth exporting from. The cluster rule sorted the rim by
  family and so could never select a **single** person, which is what every royal doorway is --
  Henriette Marie de Bourbon, James VII Stewart, Jan Kasimir Vasa all sat at the rim and none
  could ever be picked.

  **⛔ RUN IT UNTIL DIMINISHING RETURNS. THERE IS NO TARGET COUNT.** Sample, census-check, export
  from the saturated ones, merge, sample again — and keep going **until new exports are clearly
  returning few new people**. That is when it becomes clear whether the approach works at all.

  *~15,000 descendants* was invented here as a floor and is **NOT** the rule. A fixed number
  answers *have we done enough arithmetic*; the question is whether the loop is still paying.
  One 5,000-person ball is round one, not a sample of anything —
  `CLAUDE.md` § *A LONG-HORIZON INSTRUCTION IS NOT ANSWERED FROM THE FIRST SLICE*.

  The method is `scripts/descendant-frontier.py` and it is built and measured — see `devlog.md`
  2026-09-09. Per target: create an ancestor of theirs (`docs/export-seed-rules.md`), export
  `Descendants` from the created ancestor, then rank the RIM of the returned ball one pick per
  largest family cluster, and repeat outward. Your correction, same day: *"Create an ancestor of
  theirs using our algorithm, and then export descendants of them."*

  **The order, verbatim:**

  - **⛔ WHY ALIX DE LAMPRON, AND WHAT THE CAMPAIGN IS ACTUALLY FOR. Stated 2026-09-11.**
    *"The reason behind this person is because I consider them to have a descent from antiquity
    that is pretty valuable for Europe. And particularly I am hoping that me and my cluster
    somehow connect in here. I'm not super optimistic, but I'm hoping so."*

    **⛔ THE DELIVERABLE IS NOT PEOPLE GATHERED. IT IS A CONNECTION THAT DOES NOT YET EXIST
    ANYWHERE.** *"This would involve comparatively novel genealogical research ... it would not
    simply be something that is just the case based upon what the tree actually says, because I
    know neither the Geni tree nor the Wikidata tree contain this information. But I am convinced
    that there is entity resolution to be done that could relatively easily lead to a Swedish or
    Norwegian line being discovered that links up to me through similarly named people at similar
    times."*

    So the exports are **material for entity resolution**, not an import. The thing being looked
    for is a Scandinavian line inside this descent that matches the account owner's cluster on
    **name and period** — which is the zipper's problem, and `CLAUDE.md` § *1600–1900 is the band
    where names lie and years decide* is the standing warning about exactly that kind of match.

    **⛔ AND THAT KILLS THE YIELD METRIC AS A STOPPING CONDITION.** *"I honestly don't even
    consider it to be diminishing returns at this point ... the returns that come from the
    original descendants of this one person are also relatively diminished. There are not five
    thousand new individuals in the descendants of this person."* The 44%-new figure measured on
    2026-09-11 was scored against a 5,000-new ball that does not exist; the denominator is what
    the seam actually holds. Diminishing returns is relative to the alternative use of an export
    slot, never to a full ball.

  - **⛔ PHASE TWO, AFTER THE BULK: `Forest` EXPORTS ON THE SCANDINAVIAN PLACES ONLY.**
    Stated 2026-09-11: *"my vision would be that once we do the Monte Carlo stuff to gather a
    large bulk of people, and once that large bulk exists, then basically in the Scandinavian
    places and only the Scandinavian places, we would be doing additional Forest export work on
    those areas to try to expand these areas and find relationships."*

    **⛔ `Forest`, NOT `Descendants` — AND THAT IS THE OPPOSITE OF PHASE ONE.** The campaign rule
    above is `Descendants` precisely because `Forest` spends slots sideways on spouse links. In
    phase two the sideways links are the point: the job is no longer to go DOWN a descent, it is
    to widen a region until relationships appear. Do not carry the phase-one rule into phase two,
    and do not carry this one back.

    **⛔ THE DETECTOR IS THE PATRONYMIC.** *"Scandinavian people are extremely obvious in the
    data. They are extremely obvious because of the patronymics. I would say Scandinavian people
    are the most telltale people out there."* So finding the Scandinavian pockets inside the
    gathered bulk needs no classifier and no judgement — `-sson`, `-sdotter`, `-sen`, `-datter`
    and the rest are the signal, and `namemodel` already parses patronymics by form.

    **The expectation, and it is stated as an expectation rather than a finding:** *"there's
    going to be relationships there. They're not going to be the most easy, but they're going to
    be there."* And on the goal: *"there's a reasonable chance of me being descended from
    Scandinavian people who are in this, if they are present like that."*

    ⛔ **NOT STARTED, AND NOT TO BE STARTED UNTIL THE BULK IS IN.** Phase one is the Monte Carlo
    gathering and it is still running. Nothing here is investigated, measured or seeded now.

  - **⛔ THE FOCUS INSIDE ABUL HAMZA IS ALIX DE LAMPRON `6000000006101354745`.** Ruled
    2026-09-10: *"for descendants of Abul Hamza, imo focus on descendants of
    https://www.geni.com/people/Alix-de-Lampron/6000000006101354745?through=6000000001500872848
    ... the people I actually want are going to be descended from this individual."*

    **⛔ DO NOT RUN A DESCENDANTS EXPORT ON HER.** Said twice: *"Do not try to run a descendant
    export on them yourself. Please don't do that."* That is a prohibition on the export, not a
    licence to do something else instead — anything beyond it is unruled.

    **She is NOT the `Princess Alix de Lampron` already in this file.** That one is
    `6000000006101354712`, in the WESTERN european tang list of fifteen hinge people. This is
    `6000000006101354745`, a different profile, and the two must not be conflated.

  - The person I made — **Abul Hamza** `6000000227676734863`. In flight: all three exports are
    down and `reports/descendant-frontier-abul-hamza.tsv` holds the first ten rim picks. Not
    comprehensive yet, and the rest of the list waits on it.
  - **⛔ `NN ben Ovadya` `6000000227708968860` — A NEW CAMPAIGN ROOT, ADDED 2026-09-11.**
    Emma, running the export herself: *"Im exporting this one
    https://www.geni.com/gedcom/download?task_id=6000000227709071839 ... And the descendants of
    this person will be subject to a similar export descendant campaign."*

    The ball she exported is filed at
    `exports/ben-ovadya-descendants/export-Descendants-6000000227708968860.ged` — 5,000 INDI,
    3,634 FAM, **1,340 new to the corpus** and sharing only **20 people** with the whole Alix
    campaign. A disjoint population, which is what the hinge-person rule is for.

    **⛔ ITS POSITION IS AFTER GAMLE OLOF. Ruled 2026-09-11:** *"Ben ovadaya goes after gamle
    olof"*. So it is fourth, ahead of the Chinese clusters.

    **Nothing here is investigated, measured, seeded or grepped** beyond filing the file she
    named and counting it — `CLAUDE.md` § *"Add it to the end of the queue" means WRITE IT DOWN
    AND STOP*.

  - **⛔ THE SEEDS FOR THE REST OF THE ROSTER, SUPPLIED 2026-09-12.** Every one is a profile to
    export FROM, so the create-an-ancestor step is already done and must not be repeated on them.

        6000000209721822822  Inca Emperors

    **⛔ THREE OF THEM ALREADY HAVE BALLS ON DISK** — checked before spending an export slot:

        6000000227039926826   exports/descendants/export-Descendants-…
        6000000209721868822   two balls, exports/8-19 exports/ and exports/edges/
        6000000209721822822   exports/edges/ — BOTH Descendants and Forest

    **⛔ ON THE TWO CHINESE SEEDS, AND THE CAVEAT IS HERS.** Supplied 2026-09-12:
    *"I think they are in the two most eccentric clusters possibly at least at one point were the
    most eccentric individuals (the descendant export style may have stretched eccentricity
    elsewhere though since descendant exports are more stringy)."*

    **Measured now: both sit in cluster rank 1 at every cut** in
    `reports/eccentric-cluster-members.tsv`, not one each in two clusters. That is consistent with
    what she says rather than against it — the clustering is recomputed from a corpus that has
    grown by many descendant balls since, and a stringy descent changes what the components are.
    **The ids are hers and stand; the cluster reading is stale, not the seeds.**

  - **⛔ WHY THE LOW-YIELD ROOTS ARE STILL WORTH RUNNING, AND WHAT CLUSTER 2 ACTUALLY IS.**
    Stated 2026-09-12, after cluster 2 returned 72 new people across two exports against cluster
    1's 1,439:

    *"the general problem here as I think you saw is basically oftentimes we are starting from the
    most densely documented clusters and moving down."* So a low yield is the **expected** shape
    at the start of a root, not a verdict on it — the campaign begins where the documentation is
    thickest and works outward into the thin parts.

    **⛔ CLUSTER 2'S IDENTITY IS UNKNOWN AND IS NOT TO BE LOOKED UP.** *"I don't even know what
    this second cluster is … I'm not actually asking you right now to tell me what it is, or at
    least in any way that would involve looking something up."* Her own reading, offered as a
    guess and recorded as one: *"some kind of legendary lineage that might even be something
    that's connected to the Yellow Emperor stuff later."* **Cluster 1 is the Yellow Emperor
    material**; cluster 2 may join it further down.

    *"The Chinese ones go really deep and they really go far down in a weird way."*

    ⛔ **SO DO NOT IDENTIFY IT, AND DO NOT USE ITS LOW YIELD AS A REASON TO DROP IT.** She was
    skeptical about including it and included it anyway, on the grounds that not knowing what it
    is makes it worth gathering rather than less so.

  - **⛔ ADASI'S FIRST SEED SAT ON THE WRONG SIDE OF A BOTTLENECK. Ruled 2026-09-12.**
    *"For Adasi I think I get what happened and imo solution is this individual
    …/6000000227723403845 … They have a particularly weird structure to them where the family
    kind of fans out a lot, but it basically has at least one really, really significant
    bottleneck."*

    So the 141 / 182 / 0 on `6000000227712700862` is **not** a measurement of Adasi's descent —
    both root-anchored exports stayed in the narrow part above the bottleneck, and 30 random
    picks over a 102,016-person enumeration topped out at 225 for the same reason.

    ⛔ **A BOTTLENECK IS A THIRD SHAPE, ALONGSIDE *saturated sideways* AND *saturated at the
    root*.** It is not visible in any of the three steps' numbers — the exports simply return
    what is above it — and nothing measured so far would have revealed it. **She read it off the
    tree; it was not derived here.**

  - **⛔ `L. Ron Hubbard` `6000000020167386805` — FOREST REFUSED, NEEDS AN ANCESTOR.**
    Asked 2026-09-12: *"because he somehow has 15,000 recorded ancestors please do a forest export
    on this profile lol"*. `https://www.geni.com/gedcom/export/6000000020167386805` returns
    **"You are not allowed to export that profile"** — the same refusal as Gamle Olof and the
    first NN Ulster, checked with one fetch and no slot spent.

    **So it needs an ancestor created above him**, which is what she did for NN Ulster
    (`6000000227715492839`). **Not created here** — every ancestor made on an unowned profile so
    far in this campaign has been hers, and whether to make one on a modern person with living
    descendants is not a call to take unasked.

    **His path is saved** — `geni-paths/6000000020167386805-blood-and-inlaw.html`, 140 segments,
    **no blood relationship at all**, in-law only, sharing its first nine hops with NN
    Mixcoamatzin's chain off Iry-Hor.

    ⛔ **AND HIS PROFILE FREEZES THE RENDERER.** The first tab went unresponsive to CDP for over
    two minutes on that page and had to be closed; a fresh tab loaded it. Worth knowing before
    anything else is driven against it.

  - **⛔ ONE BANKED MONTE CARLO HIT LEFT.** They live in
    `reports/descendants-export-targets.csv` and **were tracked nowhere in this file**, which is
    how Chinese 1 and Skjalgsson went missing from the roster earlier today.

        6000000021665410212   5,086   from Aztec's sweep

    Each is a person over the 4,000 threshold whose export costs a climb and one slot, with **no
    census loads at all** — the sweep that found them is already paid for. Spend order is not
    ruled; largest first is the obvious default and is not a rule.

    ⛔ **THE CLIMB CHECKS ITS OWN LANDING FROM 1.7.45.** Write the denylist with
    `python scripts/ball-collision-check.py --list <exports/root-dir> > reports/avoid/<root>.txt`
    and pass it as `avoidFile:"file:///C:/Users/Emma/Documents/GitHub/geni/reports/avoid/<root>.txt"`
    on the `seedwalk`. The worker answers the pre-write announcement with `{collision:true}` and
    the walk climbs past that subject instead of creating on it. **Verify it loaded** — `status`
    reports `avoidSubjects`, and a silent 0 means the file did not read.

    The offline form, `ball-collision-check.py <subject> <exports/root-dir>`, is now only a
    post-mortem: by the time it can see the subject the export is submitted and Geni does not
    cancel. Do not grep the export log for this. The log's first column is a task id; the subject is not a column at all, which is
    why the old guard read 0 rows and cleared the ninth collision straight through. The script
    asks the question that actually predicts the yield — *is the subject already inside a ball
    filed under this root* — and over 65 balls it fired 9 times, 8 of which returned exactly 1
    new person against a median of 1,626 for the rest. It exits 1 on a collision.

  - **⛔ THE WHOLE PROGRAM, RE-RULED ROOT BY ROOT ON 2026-09-13.** Asked because she said to:
    *"AskUserQuestion on every descendant's campaign on what to do with it lol"*. Fifteen
    questions, fifteen answers. **This supersedes the 2026-09-12 four-answer ruling entirely.**

    **⛔ AND THE REASON THE BIG ONES ARE WORTH IT IS HERS, NOT A YIELD NUMBER:**
    *"Charlemagne is a person who is very central and well documented. There is not a whole lot of
    new stuff to add around him. A lot of these people with very large numbers of descendants are
    not as well documented and often are sparse in some areas. So I place them as worth a shot."*
    So **a large descent already held is not evidence of saturation.**

    **⛔ THE ROUND IS `docs/monte-carlo-procedure.md` AND THERE IS NO DISCRETION IN IT.**
    Ruled 2026-09-13: *"the failure mode of the Monte Carlo campaign was that you did too much of
    your own judgment, because it was supposed to be strictly organized and scope limited."*
    40 candidates, trunk frame, `--list-saturated` denylist, every reading ≥ 5000 exported, and
    the root stops when a round returns zero of them. Seven invented yield predictors are listed
    there, all refuted. Which root runs is this list, top to bottom, and never a choice.

    ### ⛔ SLOT ORDER, RE-RULED 2026-09-13 (LATE)

    *"the Aztec and the Inca are probably highest value added. And then after those ones are
    complete, then the Jewish one, the ben Ovadya one."* And on the Chinese root, whose point has
    already been served: *"the important part of the Chinese stuff was just putting all this
    stuff into the privileged section... the Chinese stuff probably is not that valuable right
    now."* Both its `Forest` and its `Descendants` are in `exports/post-merge/` as of tonight, so
    that is done; its remaining Monte Carlo rounds drop below the others.

        1  Aztec           Forest, then Monte Carlo; and the 5,086 banked hit
        2  Inca            more Monte Carlo rounds -- moved up out of POSTPONED
        3  NN ben Ovadya   more rounds, pool 28,124
        4  Adasi           the 15,000 cap hit and the 6,975
        5  Abul Hamza      d'Esneval and Bettencourt, then a Monte Carlo on her
        6  Jimmu           its first Monte Carlo
        7  Chinese root    further Monte Carlo rounds only

    **⛔ AND THE EXPORTS ARE WORTH LESS THAN THE ATTENTION THEY HAVE BEEN GETTING.** *"the exports
    are good, but they're not... I feel like these exports are probably worth a bit less than you
    are putting attention onto them."* Do not let a ball's arrival become an event; file it,
    measure it, move to the next thing.

    **⛔ CONCURRENCY IS PART OF WHY THIS IS HARD.** *"if we got the GEDCOMs instantly and didn't
    do anything concurrently, it wouldn't take that long."* Geni builds one ball at a time and
    everything else — census sweeps, climbs, the path campaign — runs beside it, so the critical
    path is easy to lose. **What is running stays running; what is next is this list, top down.**

    ### LIVE — in slot order

    **⛔ 1. THE CHINESE ROOT, `NN Father of Huaxu` `6000000227036719829` — FULL THREE-STEP, AND
    IT IS THE MOST IMPORTANT ONE.** *"Full three-step lol this is the most important one, and all
    gedcoms from it are considered privileged due to the merge history."*

    **⛔ NEWNESS IS THE WRONG YARDSTICK ON THIS ROOT, AND "ALREADY ON DISK" IS NOT A REASON TO
    SKIP A STEP.** Ruled 2026-09-13, after I looked at what was filed and decided *full
    three-step* must mean *more Monte Carlo rounds*:

    *"The forest export and descendants exports are both probably going to be mostly the same and
    not introducing new people, but they are correcting errors in the people. So it is very
    important to keep them, it is very important to do these, even though it may seem like it is
    not useful, because the Chinese one is qualitatively different in its utility than the other
    ones."*

    **So all three steps run, on the root, every time this root comes up** — `Forest`,
    `Descendants`, Monte Carlo — and a 0%-new ball is a success here, not a wasted slot. The
    deliverable is the corrected structure, not the count.

    **⛔ AND A LOT OF EXPORTS WERE ALREADY TAKEN OFF THIS ROOT, AND SOME OF THEM ARE WRONG.**
    *"we did a large amount of exports off of this one person... and some of them are going to be
    wrong."* What is on disk under this root is therefore **not evidence that a step is done** —
    it is a mixture of correct and stale balls, and re-exporting is how the stale ones lose.
    `exports/post-merge/` wins by `sources._post_merge_last`, which is the mechanism that makes
    that work without anyone having to decide which id was absorbed.

    What is currently on disk, for the record and NOT as a reason to skip anything:

        pre-merge    exports/chinese-clusters/     Forest + Descendants, 2026-09-12
        post-merge   exports/post-merge/           Forest 6000000227732606834
                                                   Descendants 6000000227732913835
                                                   4 Monte Carlo hit balls

    **⛔ AND IT IS A DROP-EVERYTHING ITEM.** *"the Chinese one was specifically a drop everything
    and do this thing. This is the most important thing... this is a really important thing to
    make it clear that you have to obey my instructions when I give them."* It takes the serial
    slot ahead of everything, including anything already climbed and ready.

    ⛔ **SAMPLE PAST THE BOTTLENECK.** Huaxu's descent is 156 generations with 78.6% at
    generation ≤130, so a uniform sample reads *top 43, zero hits* while a trunk-restricted one
    reads **9,265 / 6,802 / 6,793** off the same person. Cut the frame with
    `scripts/trunk-roster.py` and pass the saturated denylist. This applies to every deep root.

    **2. ADASI reseed `6000000227723403845` — THE CAP HIT AND THE 6,975.** Forest (26 new) and
    Descendants filed; the Monte Carlo read all 40 on 2026-09-13.

        6000000008826548841   15,000 -- at the cap, truncated by definition
        6000000015507447504    6,975 -- well clear of the cliff at 1,417

    Both get exports. No further rounds were asked for.

    **3. THE AZTEC — FOREST FIRST, THEN MONTE CARLO.** *"Forest first, then Monte Carlo"* — the
    Forest is the sampling frame, so building it first is what makes the sweep mean anything.

        6000000209721868822  NN Mixcoamatzin   no Forest on disk   -> Forest, then Monte Carlo
        6000000021665410212  banked hit, 5,086, never spent        -> still owed, unordered

    **4. JIMMU — RUN THE MONTE CARLO.** `Forest` and `Descendants` are filed and it has never
    been sampled.

    **5. NN ben OVADYA — MORE ROUNDS.** Pool 28,124; its banked hit `6000000011196793448` is
    climbed and spent, so the next thing is another sweep.

    **6. THE ABUL HAMZA SIX — FINISH THE TWO, THEN A MONTE CARLO ON ABUL HAMZA HERSELF.**
    All six are climbed. Two created ancestors are banked and never exported:

        6000000227739018883   d'Esneval      -- both descent-verified at 0 held, which per
        6000000227738961944   Bettencourt       Sayaluna means we lack the STRUCTURE, not people

    Then sample **Abul Hamza `6000000227676734863`** again: the six were themselves hits off her
    ball, and **her ball came back at the cap**, so it is truncated by definition and the descent
    below it is not bounded by what is in it. She is `CLAUDE.md`'s first descendants target and
    the specific interest is **descendants of hers living in Scandinavia**.

    ### POSTPONED — live, but they never take the slot while anything above is owed

        Inca            Forest + 2 Descendants + 1 MC ball   more MC rounds
        Hermenegildo    1 Forest, 5 Descendants, 4 MC balls
        Narayana        1 Forest, 3 Descendants, 2 balls -- 33 consecutive width<=2 generations
        Fihr            1 Forest, 2 Descendants, 1 ball -- sparse, not bottlenecked

    ### DROPPED 2026-09-13 — do not re-derive these from any roster

        Genghis         Forest filed, Descendants already ruled out; the Monte Carlo goes too
        Confucius       closed at Forest + Descendants, never sampled
        NN Naf          closed at 6 balls; the rounds read 80.1% then 26.8%
        no-name         6000000000183188387, closed at 9 Descendants and 8 MC balls
        Dal Fiatach     closed at 16 balls, the most of any root

    **A dropped root is dropped, not paused.** Nothing further is seeded, sampled or swept on it
    and it is not to come back from `reports/density.md` or any other derived list.

---

- **⛔ `den yngre` NEEDS THE PROPER NAME-CHANGE TREATMENT, AND THIS ONE CORRECTS EXISTING
  WIKIDATA.** Enqueued 2026-09-09: *"this one and everything with den yngre needs the proper
  name change stuff. This is correcting existing wikidata stuff though"* — so it is named as a
  correction rather than an addition, against `CLAUDE.md` § *The purpose is to ADD, not to
  correct*.

  **The instance she sent** is `Q5797554` **Detlof Heijkenskjöld den yngre**. Off the screenshot,
  nothing looked up:

      mul                                  no label defined
      en / en-ca / ast / nl / sv           Detlof Heijkenskjöld den yngre
      en-us / fr                           no label defined
      ja                                   デトロフ・ヘイイケンショルド
      ko                                   데트로프 헤이즈켄쇨드
      zh                                   德特洛夫·赫伊伊肯肖尔德
      description                          none, in any language

  **THE ALGORITHM IS FIXED; THE SCOPE AND THE CORRECTION ARE NOT.** `b22afdf1`:
  `generation_suffix_key` reads Geni's `NSFX` field and matches the whole of it, and Geni files
  him `NAME Detlof /Heijkenskjöld/` with **no `NSFX` at all** — so the suffix existed only inside
  Wikidata's own label, our derived label came out bare, and the `ja`/`zh`/`ko` labels **this
  pipeline wrote onto the item** dropped it in all three.
  `namemodel.generation_suffix_in_label` searches the same table inside a string;
  `derive-labels.py` falls back to it on `wikidata_en`/`wikidata_mul`, with `NSFX` still winning
  where both exist. Nothing downstream needed changing — `mul` and `en` already normalise to
  `II` / `Jr.` and the CJK readings already carry the established `2世` / `二世` / `2세`.

  **What remains:**

      1. MEASURED 2026-09-10 -- `reports/generation-suffix-gap.csv`, 101 items where
         Wikidata's label carries the suffix and ours does not, all with a QID. A further
         685 are the reverse and are a different question. See `devlog.md`.
      2. the corrected labels reaching Wikidata, which needs a rebuild and then a batch
      3. whether the same hole exists for the other suffixes: `d.y.` 8 on Wikidata,
         `the younger` 5, `nuorempi` 11, and every senior form

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

- **⛔ ENSURE THE **TWO** CRONS ARE RUNNING — work-loop `0,30 * * * *` and auto-flush
  `15 * * * *`.** Ruled 2026-09-14: *"Work-loop and auto-flush only"*, and the work-loop fires
  **on the hour and the half hour** — *"`:00` and `:30` work loop prompts asking to work on the
  1st queue item will be good"*. `.claude/skills/autonomous-loop/SKILL.md` is the authority and
  says the same; this line said FOUR and `3 * * * *` until 2026-09-14, which is the stale copy
  that caused the disagreement.

  **The status-report `42 * * * *` and dead-queue-sweep `45 * * * *` crons are DELETED and are
  not to be recreated.** The sweep came within one step of deleting two LIVE queue items.

  **⛔ NEVER KILL A CRON WITHOUT BEING TOLD TO.** Ruled 2026-09-14: *"I am not authorizing you
  to kill any cron jobs. We need all of the fucking cron jobs to be running so we can properly
  barrel through the queue."*

  They are **session-only**: they die when the session ends and must be recreated at the start
  of the next one. Not theoretical — every cron died in the 2026-08-28 crash and none was
  recreated, which is why nothing ran between 00:03 and 06:00 on 2026-08-29. Old session ids are
  dead and are the reason to check `CronList` rather than trust any line in this file.

  ⛔ **AND IT HAPPENED AGAIN ON 2026-09-12.** The session ran roughly nine hours with `CronList`
  reading *no scheduled jobs* — through the whole Alix, Seljuq, NN Näf, Dál Fiatach and no-name
  campaign — and **Emma noticed, not the session**: *"I think you kinda did nothing like the
  crons may have messed up."* The line above — *recreating them is the first thing a session
  does* — was already in this file and was not read. **Check `CronList` before the first export,
  not after the fortieth.**
  **A session once ran for hours with ZERO crons and nobody noticed.** Recreating them is the
  first thing a session does, not something to get to.

  **⛔ THE STATUS-REPORT AND DEAD-QUEUE-SWEEP CRONS ARE DELETED.** Ruled 2026-09-14:
  *"Work-loop and auto-flush only"*. The status report was reporting-only, so each tick was a tick
  not spent on the queue; the sweep nearly deleted two live items — d'Esneval and Bettencourt,
  whose balls then returned 1,111 and 3,130 people — because it tested *is this done* with
  `find exports -name "*<id>*"` and hit a tiny path GEDCOM. **Do not recreate either.** Deleting a
  finished item is the work-loop's own step (d).

- **The two crons, as durable queue items.** The crons are good and continue, and they are also
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

**⛔ THIS WAS ALREADY RULED AND ALREADY SOLVED. THE SOLUTION WAS IMPLEMENTED IN ONE EMITTER.**

Corrected 2026-09-14. A measurement of 1,431 clan-seat labels was reported here as a new finding
about how bad the clan labels are. Emma: *"I'm pretty sure this is a thing that was resolved like
two weeks ago that you just are continuously bringing up ... we came up with a solution, and you
might have just not implemented it."* **Right on both halves.**

The ruling is 2026-08-29: *"we block the clan name application stuff for one month. In October,
once the October gate passes, then the quick statements generate with these clan names in them,
but otherwise they do not, because I'm just too sceptical of the clan names."* It was implemented
the same day and it works — `build-garborg-day.py` prints `CJK clan labels suppressed until
2026-10-01` on every run.

**It suppressed a hardcoded list of 163 QIDs.** Then `reports/wikidata-cjk-mul-labels.json` was
committed by hand on 2026-09-10, `22b82b05`, and `wikidata-edit-run.py` reads it directly:
**1,431 clan-seat labels, ZERO of them among the 163.** § *A GUARD IN ONE EMITTER IS NOT A GUARD*.

Closed 2026-09-14: the gate moved to `scripts/wikidata_lockout.py` as the single copy of the
date, `wikidata-edit-run.load_batch` applies it to every batch it reads, and the test is each
edit's own `derived_from` rather than a list of ids — a list only covers the ids somebody
remembered to add. Four tests in `tests/test_wikidata_start_date.py` pin it.

**What is left here is the ORIGINAL question, which the block was always a deferral of**, and it
comes up on 2026-10-01 when the gate opens: what should a `mul` label be for a person known only
by clan and seat? 隆西狄道 is Didao county, Longxi commandery, in Gansu — real evidence, and not a
name. Three shapes are already in the data and the batch mixes them without deciding: `隆西狄道`
bare (79 people), `公主 隆西狄道` (a title plus the seat), and `某 李` (a surname with the
unknown-marker 某). § *A title inside a label takes the NATIVE form in CJK* and § *`NN` is
PRESERVED in `mul`* both bear on it.

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

**One thing is left of the three, and it does not touch a person's data either:**

- **Cut the strategy content.** Anything in `CLAUDE.md`, `queue.md`, `devlog.md` or the scripts
  about how that item gets linked or how the account's editing reads to others.

**The repo is public as of 2026-09-01** — *"The repo is public now lol"* — so Actions minutes are
free and `CLAUDE.md` § *Cost* no longer binds.

### ⛔ `exports/post-merge/` — MOVED TO THE TAIL, 2026-08-29

408 of the 412 falsifiable drops are real deletions. **Leave them in the tree, keep running the
measurement, decide later** — the lean is toward saving the 408 rather than dropping them, but
there is no bandwidth to process it now. Nothing is applied and no override is written.

`scripts/grade-post-merge-drops.py` → `reports/post-merge-falsifiable.tsv` is the standing
measurement — 408 `link-gone`, 2 still linked, 2 with no shared family, over 159 parents,
159 children and 90 spouses.

---

## THE END OF THE QUEUE

- **⛔ AN ANALYSIS OF THE FIVE ARTEFACTS SENT 2026-09-10.** *"Things to think about. But put at the
  end of the queue an analysis of these"* — so this is the roster and **nothing here is
  investigated, measured, fetched or queried.** `CLAUDE.md` § *"Add it to the end of the queue"
  means WRITE IT DOWN AND STOP*. When it is reached, § *"Analyse this" means: build a CSV of every
  instance* governs the shape of the answer.

  **1. The `daughters` paste** — <https://pastebin.com/wP2dbrVf>, guest paste, **11.13 KB**,
  posted **2026-09-10**, **365-day retention** so it expires 2027-09-10. One Wikidata item URL per
  line. The fifteen legible on screen:

      Q108655747  Q106472244  Q106535162  Q106472816  Q106683636
      Q106540429  Q109927895  Q108779632  Q108655970  Q108891795
      Q22694450   Q106240452  Q107239466  Q110573431  Q106240606

  and two more partly visible below the fold, `Q106713074` and `Q75381643`. At ~46 bytes a line
  the file is on the order of **240 items**; that is arithmetic off the byte count, not a count.

  **2. `Q106583062` — "Daughter of Ito Nyudo"**, `mul` / `en` / `en-ca` / `en-us` / `fr` all
  carrying that same string, no description in any language, `instance of` human,
  `sex or gender` female with 1 reference.

  **3. `Q116054588` — "NN ferch Iorwerth ab Owain Brogyntyn"**, the same string in all five
  language slots, no description, human, female.

  **4. `Q76006546` — "unknown son (?)"**, and this one disagrees with itself:

      mul      NN                    en-ca   unknown son (?)
      en       unknown son (?)       en-us   NN
                                     fr      NN

  Its **English description is `Peerage person ID=462780`** — an identifier used as a description.

  **5. `Q141381269` — label `..`**, in every language slot, `instance of` **family name**, English
  description `family name`. **Created by `日巫女` via QuickStatements**, revision 04:27
  2026-09-09, edit summary `#quickstatements; #temporary_batch_1788927746966`.

  **What connects them is not stated and is not to be assumed here.** Four of the five are
  unnamed or relationally-named people — *Daughter of X*, *NN ferch Y*, *unknown son (?)* — and
  the fifth is a name item whose label is two full stops. Whether the paste is a list of the same
  shape is exactly the thing the analysis has to establish rather than take as read.

- **⛔ WELSH PATRONYMIC CHAINS TAKE `P1545` (series ordinal).** Ruled 2026-09-10: *"For people
  like this (mostly welsh on wikidata) we use series ordinal for patronymics."*

  **The instance sent** is `Q116812067` **Margred ferch Llywelyn Gôch ab Ieuan ap Dafydd of
  Rhydlafar** — one label carrying a chain of three generations, `ferch Llywelyn` / `ab Ieuan` /
  `ap Dafydd`. No description in any language; `instance of` human, 0 references. The other tabs
  open beside it were `Lewys ap Robert Raglan, of Vorc…`, `John Games, of Penfathrin`, so the
  shape is a population rather than one person.

  **Why the ordinal is the answer and not a second property:** a Welsh name names the father, the
  grandfather and the great-grandfather in one string, so `P5056` (patronymic) has **several
  values on one person** and nothing about the statement says which generation each belongs to.
  `P1545` (series ordinal) is the qualifier that orders them.

  `name modelling.txt` is the authority on how a name is modelled and beats `CLAUDE.md`, so this
  rule belongs there once it is worked — `CLAUDE.md` § *`name modelling.txt` is the authority*.
  It is recorded here first because that is where it was sent.

  **Nothing is investigated, measured or queried**: not how many Welsh-chain labels exist, not
  which already carry `P5056` (patronymic), not whether `P144` (based on) points anywhere.
  `CLAUDE.md` § *"Add it to the end of the queue" means WRITE IT DOWN AND STOP*.

- **⛔ ANALYSE THE NINE SCREENSHOTS SENT 2026-09-11 AND THE ISSUES IN THEM.**
  `docs/queued-analysis/wikidata-reverts-2026-09-11/` — nine images, saved as sent:

      01-pastebin-contributions.jpg          pastebin.com/uXm3P4yA, a contributions listing
      02-Q3656094-Sempronia.jpg
      03-Q176912-Philip.jpg
      04-Q359687-Antigonus-II-Mattathias.jpg
      05-Q313883-Alexandros-II-of-Macedon.jpg
      06-Q1427539-Flavius-Hannibalianus.jpg
      07-Q125542470-Joel-von-Brehmer.jpg
      08-Q113006331-Johan-Leijel.jpg
      09-Q64802-Engelbert-II-of-Berg.jpg

  **The task emerges from the images; read them and work it out there.** Emma: *"add to the very
  end of the queue a task to analyze these images and issues I have with them, just save into a
  directory for this the task emerges from the images when you look at them do not ask questions
  or think about them carry on with your work"*.

  **⛔ NOT INVESTIGATED, NOT DIAGNOSED, NOT ACTED ON — and deliberately not summarised here
  either.** The instruction was to save them and carry on, so no reading of what they show has
  been written down: no account of who reverted what, no cause, no count, and above all **no
  change to any batch or emitter on the strength of them.** `CLAUDE.md` § *"Add it to the end of
  the queue" means WRITE IT DOWN AND STOP* and § *A LONG-HORIZON INSTRUCTION IS NOT ANSWERED FROM
  THE FIRST SLICE*.

  When this is worked: the answer is a CSV of every instance, committed, and then the analysis of
  that CSV — `CLAUDE.md` § *"Analyse this" means: build a CSV of every instance, commit it, then
  analyse that* — not a reading of nine screenshots. The screenshots are where the question comes
  from, not the evidence base.

- **⛔ FIX THE GENI-ID APPLICATION: IT IS SUPPOSED TO FIRE ONLY ON THE BORDER, AND IT FIRES
  EVERYWHERE.** Emma, 2026-09-11: *"fix our geni id application stuff, because it is only
  supposed to add geni ids to people bordering the universe when a relationship is added to them,
  right now it kinda just does it everywhere not in accordance with the algorithm"*.

  So the rule it is meant to obey has two conditions and it is honouring neither:

      the person is BORDERING THE UNIVERSE
      a RELATIONSHIP IS BEING ADDED to them

  **Nothing is investigated, measured, grepped or diagnosed.** Which emitter does it, whether
  `docs/algorithms.md` states the border condition, how many statements went out that should not
  have — none of that is looked at here, and no batch or emitter is touched on the strength of
  it. `CLAUDE.md` § *"Add it to the end of the queue" means WRITE IT DOWN AND STOP*.

- **⛔ WHY ARE `|` NAME CORRECTIONS LANDING ON NON-ADJACENT ITEMS?** Emma, 2026-09-11: *"look
  over why name corrections with the | appear to be being done to non-adjacent items"*.

  **Not investigated, not diagnosed, not traced to an emitter.** Which script writes the `|`
  form, what "adjacent" is measured against, and how many such corrections went out are all
  unexamined here. `CLAUDE.md` § *"Add it to the end of the queue" means WRITE IT DOWN AND STOP*.

- **⛔ ONLY EVER EDIT THINGS IN THE UNIVERSE OR ONE STEP ADJACENT TO IT.** Emma, 2026-09-11:
  *"making it so that we only ever edit things in the universe or one adjacent to it. We are
  being way too non-local and it is drawing attention"*.

  So the edit surface is bounded to two rings and nothing further:

      in the universe
      one step adjacent to it

  **And the reason is OPSEC, not correctness** — *"it is drawing attention"* — which is the same
  concern behind the caps in § *Caps* and behind the QuickStatements batching generally.

  **⛔ AND THE FUXI CASE IS THIS RULE'S FIRST MEASURED COST, 2026-09-14.** A Chinese
  mythological figure, `Q236972`, nowhere near the universe, got a phonetic katakana label
  written over its correct 伏羲 — because a batch reached him at all. Emma: *"the core of this
  really is based upon something later in the queue related to how the quickstatements that are
  generated are supposed to be local, but they're not local... the Scandinavian areas are places
  where we really have a good idea of what good data looks like and what the edge cases are, but
  stuff that leaks out of the universe into just random areas is an intrinsic risk."*

  That is the diagnosis and it outranks the symptom. The transliteration bug is real — the guard
  for it went in the same day — but **a correct transliterator pointed at Chinese mythology is
  still the wrong pipeline aimed at the wrong people.** Locality is what would have prevented it,
  and it is a stronger fix than any amount of per-script special-casing.

  **Nothing is investigated, measured or changed.** No emitter is audited, no locality test is
  written, and no batch is altered on the strength of this. It is written down where it was sent.

- **⛔ `Q1934051` — THE ONE OTHER IDENTIFICATION SHAPED LIKE THE WRONG ONE.**
  `NN Sverkerska Kungaätten` `6000000031940461725` identified with **Helena of Sweden**.

  `Q22678387` `NN de Courtenay` -> `Hodierne of Courtenay` was ruled wrong by Emma on 2026-09-11
  and is retracted. `reports/nn-manual-identifications.csv` holds all 11 identifications with
  `NN` on our side; nine are `NN` ↔ `NN` matched on family, and this is the **only** other one
  where an unnamed person on our side was matched to a **named** individual on Wikidata.

  **It is hers to rule on and is NOT retracted on a resemblance.** Written down, not acted on.

## Names

Remember that this is not something to be done out of order, it is the second last item in the queue for a reason

We are still generating non-name items as names such as numbers, and I think https://www.wikidata.org/wiki/Special:Contributions/OBender12 is likely pretty pissed at this point, but no talk page messages yet. idk why you did not fix it and seem to have completely overlooked the error that he constantly corrects. There are plenty of non-name things that need to be parsed not as names.

Read "address_this.html"

### Examples

Even in the current batch one exists lol

# und -- family, 8 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "und"
LAST	Len	"und"
#   set the mul label to "und"
LAST	Lmul	"und"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q61139384 Mangold von Thurgau und Nellenburg III: P734 family name = the item just created
Q61139384	P734	LAST	S2600	"6000000004106003883"
#   Q81827036 Adalbert von Saffenberg und Norvenich: P734 family name = the item just created
Q81827036	P734	LAST	S2600	"6000000009305060696"
#   Q55068638 Friedrich zu Schwarzenberg und Hohenlandsberg: P734 family name = the item just created
Q55068638	P734	LAST	S2600	"6000000014784646061"
#   Q110261972 Johann I von Tengen und Nellenburg: P734 family name = the item just created
Q110261972	P734	LAST	S2600	"6000000017758205608"
#   Q110415677 Georg III von der Leyen zu Eltz und Leiningen: P734 family name = the item just created
Q110415677	P734	LAST	S2600	"6000000019797018175"
#   Q828346 Berthold Graf von Neuffen und Achalm: P734 family name = the item just created
Q828346	P734	LAST	S2600	"6000000082813823834"
#   Q110410743 Nicolaus* Andreas Graf von Maltzahn, Freiherr zu Wartenberg und Penzlin: P734 family name = the item just created
Q110410743	P734	LAST	S2600	"6000000105706792946"

## Usual forrname

Please stop adding this to the first name in the given names. I do not think it is actually accurate most of the time. Leave it lying around do not try to fix it do not assess anything related to the population affected just drop this item of the pipeline


## `emmas-files/` — HERS, AND NOT TO BE TOUCHED

She saves interesting paths by hand into `emmas-files/` and changes the anchor as she goes.
**Neither is to be reconciled, renamed or reorganised**, and an anchor change is not an event.
Explaining what is in there and how it relates to `geni-paths/` is still owed and is a long way
out; the prohibition holds until then.

This clause used to live inside the `/paths` harvest item. That item is finished, and the
prohibition is not, so it keeps its own place rather than leaving with it.

## Wikidata isolate connection

Actually connect the wikidata isolates I think we can just zoom through them by this point with our pipeline we have

⛔ **THIS IS THE GATE BETWEEN THE QUEUE AND WIKIDATA, AND BOTH HALVES ARE LOAD-BEARING.**
Ruled 2026-09-13: *"Make sure it's clear that between everything else in the queue and running
stuff on wikidata you must attempt all the wikidata isolates."*

So the order is three stages and nothing skips a stage:

    1. everything else in this file, top to bottom
    2. ATTEMPT EVERY WIKIDATA ISOLATE          <- this section
    3. only then may Wikidata editing be unheld

**`attempt` is the word and it is not `connect`.** An isolate that turns out to have no path is
attempted and done; the gate is that every one has been tried, not that every one succeeded.
`reports/unconnected-p2600.tsv` is the roster — **266,201 people, 266,100 eligible** — the
extension does the work, and `scripts/attempt_ledger.py` stamps `last_attempted` so *attempted*
is a fact in a file rather than a memory.

**Stage 3 does not arrive on a date.** `HELD = True` in `scripts/wikidata_lockout.py` is lifted by
hand, and the condition for lifting it is stage 2 being finished: *"the submission should even
have a requirement that all of the Wikidata people get connected. Get connected with the path
thing."* See § *WIKIDATA EDITING IS HELD* at the top of this file.

⛔ **AND THIS SECTION IS STILL LAST.** *"remember that the wikidata isolate path capturing
campaign comes after everything else in the queue, maybe write that explicitly at the end if it
is not clear enough"*. It is also `CLAUDE.md` § *The default when nothing else is running* — what
idle time goes to — so it runs whenever nothing above it is live, and finishing it is what opens
stage 3. **Nothing above it waits on it; it does not start while anything above it is live.**

- **DECIDE: what happens to `build-add-p2600-batch`.** <!-- requeued-add-p2600-2026-09-13 -->
  Deferred on 2026-09-06 for want of context to decide on, and re-queued on 2026-09-13 by
  `.github/workflows/requeue-add-p2600.yml`.

  It writes **7,166 `P2600` statements** inferred from parent-anchor proof into
  `reports/wikidata-add-p2600.qs`, and **nothing runs it**. The four options as they stood: fold
  it into the daily batch under a cap; give it its own scheduled workflow; delete it; or leave it
  as a hand-run tool. `reports/qs-batch-audit.md` carries the measurement.

  The other five generators in that audit were settled on 2026-09-06 —
  `build-missing-reciprocals`, `build-qid-link-p2600`, `build-label-corrections` and
  `build-sibling-batch` deleted by instruction, `build-from-diff` given its own review item.
  This is the last one open.


## More items at the end

Do not fucking do this until after everything else is done but I want to review middle initial items since there are roman numeral related confusions with it. Middle initials do actually deserve their own items, but we are only gonna analyze this after everything else is done, so we can focus solely on this. Losses are a bigger threat than the gains are positive here.


## Chinese gedcom identification/entry points

I earlier talked about the entry point GETCOM like it was a well-established thing, with the Chinese people having consistent identifications that were easy to do for it. I realize this is not the case, and I am going to write out a bunch of my identifications because I do not want to fucking put them on Wikidata. We are putting way too many random, unconnected P2 600 items here. I don't want to draw more attention than I've been getting from being non-local. 


https://www.geni.com/people/G%C5%8CNGS%C5%AAN-Sh%C7%8Eo-Di%C7%8En-%E5%B0%91%E5%85%B8-1%E4%B8%96/6000000026522778851 https://www.wikidata.org/wiki/Q4302144

https://www.geni.com/people/Sh%C3%A9n-N%C3%B3ng-%E7%A5%9E%E5%86%9C-Y%C3%A1n-D%C3%AC-%E7%82%8E%E5%B8%9D-Y%C3%BA-Qu%C4%81n-%E6%A6%86%E5%9C%88-%E4%B8%80%E4%BB%BB%E5%B8%9D-2%E4%B8%96/6000000130192002822 https://www.wikidata.org/wiki/Q313336

https://www.geni.com/people/Yellow-Emperor/6000000001381274001 https://www.wikidata.org/wiki/Q29201

https://www.geni.com/people/Ch%C4%81ng-Y%C3%AC-%E6%98%8C%E6%84%8F-2/6000000001381063554 https://www.wikidata.org/wiki/Q6377648

https://www.geni.com/people/L%C3%A9i-Z%C7%94-%E5%AB%98%E7%A5%96/6000000002048439278 https://www.wikidata.org/wiki/Q1441379

https://www.geni.com/people/Fuxi/6000000130191678854 https://www.wikidata.org/wiki/Q236972

https://www.geni.com/people/Ji%C3%A1o-J%C3%AD-%E8%9F%9C%E6%A5%B5-3/6000000007213183226 https://www.wikidata.org/wiki/Q10514592

https://www.geni.com/people/Xu%C3%A1n-Xi%C4%81o-%E7%8E%84%E5%9B%82-Sh%C7%8Eo-H%C3%A0o-%E5%B0%91%E6%98%8A-2/6000000002481254239 https://www.wikidata.org/wiki/Q1147250

https://www.geni.com/people/T%C3%B3ng-Y%C3%BA-Sh%C3%AC-Wife-3-%E5%BD%A4%E9%AD%9A%E6%B0%8F/6000000002848066261 https://www.wikidata.org/wiki/Q28409803

https://www.geni.com/people/M%C3%B3-M%C7%94-Wife-4-%E5%AB%AB%E6%AF%8D/6000000023167303575 https://www.wikidata.org/wiki/Q8262857

https://www.geni.com/people/Zhu%C4%81n-X%C5%AB-%E9%A1%93%E9%A0%8A-3%E4%B8%96-DO-NOT-MERGE-PARENTS/6000000001381123265 https://www.wikidata.org/wiki/Q198180

https://www.geni.com/people/Qi%C3%B3ng-Ch%C3%A1n-%E7%A9%B7%E8%9D%89-4/6000000001381046535 https://www.wikidata.org/wiki/Q10752092

https://www.geni.com/people/Jing-Kang-%E6%95%AC%E5%BA%B7-5/6000000001381114215 https://www.wikidata.org/wiki/Q10299225

https://www.geni.com/people/Ju-Mang-%E5%8F%A5%E8%8A%92-6/6000000001380828716 https://www.wikidata.org/wiki/Q9569181

https://www.geni.com/people/Jiao-Niu-%E8%9F%9C%E7%89%9B-7/6000000001380983518 https://www.wikidata.org/wiki/Q7664534

https://www.geni.com/people/Yu-Gu-Sou-%E7%9E%BD%E5%8F%9F-8/6000000001272831610 https://www.wikidata.org/wiki/Q10438384

https://www.geni.com/people/Gui-Xiang-%E5%AA%AF%E8%B1%A1-9/6000000001272854603 https://www.wikidata.org/wiki/Q4499078

https://www.geni.com/people/Emperor-Sh%C3%B9n-%E5%B8%9D%E8%88%9C-9-1G/6000000195149451825 https://www.wikidata.org/wiki/Q313342

https://www.geni.com/people/W%C3%B2-D%C4%93ng-%E6%8F%A1%E7%99%BB/6000000001272026560 https://www.wikidata.org/wiki/Q7878975

https://www.geni.com/people/Gui-Shang-Jun-%E5%AA%AF%E5%95%86%E5%9D%87-10-2G/6000000000657386629 

https://www.geni.com/people/N%C7%9A-Y%C4%ABng-%E5%A5%B3%E8%8B%B1/6000000189960169823 https://www.wikidata.org/wiki/Q7480137


https://www.geni.com/people/%C3%89-Hu%C3%A1ng-%E5%A8%A5%E7%9A%87/6000000189960074826 https://www.wikidata.org/wiki/Q7991612

https://www.geni.com/people/Emperor-Y%C3%A1o-%E5%B8%9D%E5%A0%AF-5/6000000003485847175 https://www.wikidata.org/wiki/Q819556

https://www.geni.com/people/Zhu%C4%81n-X%C5%AB-%E9%A1%93%E9%A0%8A-3%E4%B8%96-DO-NOT-MERGE-PARENTS/6000000001381123265 https://www.wikidata.org/wiki/Q198180

https://www.geni.com/people/D%C3%A0-Y%C3%A8-%E5%A4%A7%E4%B8%9A-5/6000000008004418918 https://www.wikidata.org/wiki/Q10933357

https://www.geni.com/people/B%C3%B3-Y%C3%AC-%E5%AD%97-%E4%BC%AF%E7%9B%8A-8/6000000008004518685 https://www.wikidata.org/wiki/Q4243879

https://www.geni.com/people/J%C4%AB-N%C7%9A-X%C4%ABu%E5%A7%AC%E5%A5%B3%E4%BF%AE-4/6000000020107122663 https://www.wikidata.org/wiki/Q4268330

https://www.geni.com/people/Huaxu/6000000195149174838?through=6000000227036719829 https://www.wikidata.org/wiki/Q9511624

https://www.geni.com/people/Emperor-K%C3%B9-%E5%B8%9D%E5%9A%B3-4/6000000002481253260 https://www.wikidata.org/wiki/Q721756

https://www.geni.com/people/Q%C3%AC-%E5%A5%91-5/6000000003474166572 https://www.wikidata.org/wiki/Q1045160 

https://www.geni.com/people/Reformatorin-Ursula-von-M%C3%BCnsterberg/6000000188494434823 https://www.wikidata.org/wiki/Q18028984

https://www.geni.com/people/Wu-Zhao-%E6%AD%A6%E6%9B%8C-Zetian-Emperor/6000000002188099903 https://www.wikidata.org/wiki/Q9738

https://www.geni.com/people/Scorpion-I/6000000209058145828 https://www.wikidata.org/wiki/Q318613

https://www.geni.com/people/Iry-Hor-Pharaoh-of-Egypt/6000000009562419205 https://www.wikidata.org/wiki/Q314809


https://www.geni.com/people/%EC%A1%B0%EC%84%A0-27%EB%8C%80-%EC%88%9C%EC%A2%85-%EC%B2%99/6000000028714712399 https://www.wikidata.org/wiki/Q334111

https://www.geni.com/people/Yi-Un-Crown-Prince-of-Korea/6000000028856413461 https://www.wikidata.org/wiki/Q484866

https://www.geni.com/people/%EC%88%9C%ED%97%8C%ED%99%A9%EA%B7%80%EB%B9%84-%EC%97%84%EC%94%A8/6000000028786845951 https://www.wikidata.org/wiki/Q7214248

https://www.geni.com/people/private/6000000028895625641 https://www.wikidata.org/wiki/Q496421

https://www.geni.com/people/Umayya-bin-Abd-Shams/5152366561060066977 https://www.wikidata.org/wiki/Q2746812

https://www.geni.com/people/Caliph-Marwan-II-bin-Muhammad/6000000008659107006 https://www.wikidata.org/wiki/Q128371

https://www.geni.com/people/Adam-the-First-Man/6000000201847373856 https://www.wikidata.org/wiki/Q70899


https://www.geni.com/profile/index/6000000004533522186 https://www.wikidata.org/wiki/Q7877879
https://www.geni.com/profile/index/6000000020533302781 https://www.wikidata.org/wiki/Q141455323
https://www.geni.com/profile/index/6000000009305030992 https://www.wikidata.org/wiki/Q141455107
https://www.geni.com/profile/index/6000000009305036314 https://www.wikidata.org/wiki/Q141455100

## Forest exports

These are people I want exports on but they are not in the priority in the same way. Often cover possibly underserved people but their significance is unclear

Forest https://www.geni.com/people/NN-Fuca/6000000227739821875

Descendants https://www.geni.com/people/NN/6000000227739695943

## Relational labels issue

Just like the other things this is at the end for a reason

I notice on this one https://www.wikidata.org/wiki/Q141447199 and many others that relational labels are using the geni labels and not the wikidata labels. This is a bit of a problem because well the geni labels are not always the best
this rep
### Update to this issue

I noticed a weird thing where the person does not have all of their relatives, and it defaults to their mother. New rule: NN people with a mother and a father always get it from their father

Father
Mother
Spouse
Child

Reason is that child and spouse both can mean multiple people. Parents are the most stable identifiers. Father is generally most stable

## Remove abbrviations

They have been in here way too long. Feminine patronymic abbreviations like "Olsdtr." really should at this point be only present at all in the "subject named as" in the geni id. Imo fix this in every single gedcom that it is present in and only have it.

Here is my proposed algorithm for resolving "Olsdtr" to "Olsdatter" or "Olsdotter": check the mother's patronymic. If the mother has one then great, if not then check paternal grandmother, if she does not have one then default to "-datter". 

These are actively destructive since a lot of the time our deleted or redirected names end up getting recreated due to the statelessness of the algorithm. This is a strength of the algorithm overall but the tendency to do unintentional edit wars is not good. End queue item will discuss this more

## subject named as in the geni id

In our adding of geni ids we are not even doing the "subject named as" thing which really sucks. This is self-healing right? Like we do apply the geni ids after right?

## Unintentional edit wars

I think I explained it decently but I want us to address how to solve this issue. It has been a consistent issue where our algorithm is relatively resistant to editors fixing its mistakes and this is drawing attention.

## Questionable cjk-izations

Fix these and establish general rules and corrections out of them as time goes on. This is the last item of the queue for a reason as this is a relatively long tail and not urgent. Do not dismiss these go over them in full with your full attention at the end of the queue after addressing the other things lol.

https://www.wikidata.org/wiki/Q141444659
https://www.wikidata.org/wiki/Q141444720
https://www.wikidata.org/wiki/Q141444564
https://www.wikidata.org/wiki/Q141444589 

I think the -datter words might be systematically messed up. Possibly the -sson -ssen and general patronymics

## Implementing non-Scandinavian Patronymics

I keep on telling you to do this and you keep on not doing it. To be clear this is at the end of the queue and is to be done after the more urgent stuff at the end, but I really do not want you to just fuckign ignore it, since it seems like you always just kinda forget about it and don't do it because it is not urgent but remove it from the queue and it never gets done

## CBDB people

This is the last queue item for a reason lol do not do it immediately

I think I figured some stuff out about the CBDB people who I am just straight up unable to edit. My current working hypothesis is that these people all have the geni tree 100% present on wikidata due to the mass export coming from some external gedcom. So for the people for which we are not able to add ancestors, do not be too concerned with it. I think this might be a better thing to investigate using other things like familysearch and geni is just kinda a dead end there and wikidata has all of the geni information already for it. But searching the web for these things may be helpful so do it. 

## Ancestor Exports

At the end of the queue after all other things are done I want to do some specific ancestor export campaigns. 

Ancestor exports from certain specific people to get their ancestors

try this one https://www.geni.com/people/Reformatorin-Ursula-von-M%C3%BCnsterberg/6000000188494434823?through=6000000003481830064

## Possible leads

I think connecting me to Alix via German people such as this person https://www.geni.com/people/Reformatorin-Ursula-von-M%C3%BCnsterberg/6000000188494434823?through=6000000003481830064 might be a good way to go about it. Since I do see a clear line of descent for this person and it may be the case for many others too


## Jan 1 correspondences research

Based on the fact you did not figure out that the Chinese tails were duplicates, I am convinced you do not in fact know at all anything on the Egyptian Pharaohs geni to wikidata correspondences and should probably figure them out

## Tiny GEDCOMs: model every relationship off ATTESTED representations, never invention

Ruled 2026-09-13, and **timeboxed to 20:45 the same evening, then sent here**: *"I would consider
doing this to be a waste of time because the critical path is actually fucking getting the data
we need... this task is over. Put it at the end of the queue."* *"Over"* was the timebox, not the
item: it is last in order and still to be done.

**The problem.** `scripts/build-tiny-gedcoms.py` turns a relation string into a GEDCOM edge by
taking **the last word** and looking it up in `PATH_REL`. Everything else in the string is
discarded. Two consequences found the same evening:

* `father` and `mother` both mapped to one `parent` kind and every parent was written `HUSB`, so
  **every mother in all 1,007 files was a husband**. Fixed 2026-09-13; `WIFE` went 0 → 16,906
  and 40,435 `SEX` records appeared where there had been none.
* **`adoptive` is still discarded.** 136 rows say *her/his adoptive mother* or *adoptive father*
  in `paths/*.tsv` and `reports/path-chains.tsv`, and **0** of the built GEDCOMs mention it. They
  assert an adoptive parent as a birth parent.

**⛔ THE REPRESENTATION IS READ OFF OUR OWN EXPORTS, NEVER INVENTED.** *"Don't make up some kind
of a way of implementing the relationships. Use the actual relationships that are present within
our data... No guessing on the representations."* And where a relationship is attested in only
one place and cannot be read: *"we have to do a `Forest` export on that point in order to get
that relationship so we know how to represent it."*

**Already measured, 2026-09-13 — the corpus's entire relationship vocabulary.** Every
qualifier tag present in `exports/` outside the tiny directories, and there are only four:

    1 MARR    514,136        1 DIV     10,071
    2 PEDI      2,966        1 ADOP     2,185 (and 3 ADOP 2,185)

    2 PEDI adopted   2,185          3 ADOP BOTH   2,185   -- the only value attested
    2 PEDI foster      781

**Adoption's exact attested shape**, from `exports/8-19 exports/export-Ancestors-6000000227331261851.ged`,
on the CHILD's `INDI`:

    1 FAMC @F6000000001902863980@
    2 PEDI adopted
    1 ADOP
    2 FAMC @F6000000001902863980@
    3 ADOP BOTH

**Divorce**, inside the `FAM`: `1 MARR` with its `DATE`/`ADDR`, then `1 DIV`.

**What is left to do.** The 33 distinct relation strings are in
`reports/path-chains.tsv` column 6, with counts. For each one, find the same pair in the real
corpus and record the structure Geni itself used; build the CSV of every instance, commit it,
then implement from it. `foster` is attested 781 times in the corpus and appears in **no** path
string yet, so it needs no path handling until one shows up.

**⛔ The capture is not the problem and must not be touched.** The relation string is
`span.subtext`'s `textContent` — whitespace collapsed, parens stripped, nothing parsed. `q` would
be stored as `q`. Every one of these is a re-run of the emitter, never a re-scrape.

## `Forest` exports centred on people carrying the TAIL relationships in the TSVs

Ruled 2026-09-13: *"put it at the end of the queue that... to do forest exports centred on people
with the tail relationships for the TSV files."* Written down and not started **yet**.

**Last in order, and it gets done.** Emma, immediately after: *"it's at the very terminal end of
it. And it's NOT parked. It's gonna be addressed later."*

**Why a `Forest` and not a lookup:** a relationship we have never seen in a real Geni export has
no attested representation, and § *no guessing on the representations* forbids composing one.
The export centred on a person who **has** that relationship is what shows how Geni writes it.

**The tail, counted off `paths/harvested-path-geni-*.tsv` on 2026-09-13.** The whole distribution
is 33 distinct strings; these are the ones below the common six and their gender variants:

    134  her adoptive mother        3  her child            2  his/her father
     18  her ex-husband             3  his ex-wife          2  his parent
     15  your relative?             3  his fiancée          2  her ex-partner
     11  his partner                1  his child            1  his adoptive mother
      5  his/her parent             1  her partner          1  his adoptive father
      4  her fiancé

**⛔ THE URGENT ONES ARE THE UNATTESTED ONES, and there are two kinds.**

* **fiancé / fiancée — 7 rows, and `ENGA` occurs ZERO times in this corpus.** There is no shape to
  copy, so they are currently emitted as a couple with no marriage event. This is the case Emma
  described exactly: *"if there's some relationship that is only present in one spot, we have to
  do a `Forest` export on that point in order to get that relationship so we know how to
  represent it."*
* **`your relative?` — 15 rows.** Geni itself is not naming the relationship, so a `Forest` on
  those people is the only way to find out what the link actually is.

**Already attested and needing no export** (`devlog.md` 2026-09-13 carries the measurements):
adoptive → `FAMC` + `2 PEDI adopted` + `1 ADOP` + `3 ADOP BOTH`; ex- → bare `1 MARR` with bare
`1 DIV`; partner → a `FAM` with no `MARR`. `foster` is attested 781 times in the corpus and
appears in **no** path string, so it needs nothing until one turns up.

Pairs with these relations are in `reports/path-chains.tsv`; the person to centre the export on
is the one the tail word describes.

## expanding the universe

I think especially with the locality restrictions a good way to expand the universe is for us to actively add the  subject named as (P1810) property to  Geni profile ID (P2600) properties on adjacent items to the ones in our universe. So I want this to happen. Every run 10 new bordering people not in the universe but connected to it get that as it. In addition we add geni as a source to existing relationships

## Roman given names

I would like us to just never actually apply names and given names to Roman people since they always get undone, I think due to the weird naming structure of then

## wrong name

This person https://www.geni.com/people/konenes-navn/6000000007645527815 had the wrong name applied

Oh my god his name is Peter why did you not fucking update the naming shit after I asked you about it a million times https://www.wikidata.org/wiki/Q141451100

## Generate CJK names from the CJK labels on PARTS of the `mul` label

Emma's own plan, recorded 2026-09-14 and **deliberately not started**: *"I had a plan to generate
cjk names from cjk labels on parts of the mul label. But don't bother with that now. Put at the
end of the queue to investigate this and possible implementation but don't actually do anything
on it now, it will be done at the end of the queue lol."*

**Investigate and propose an implementation. Do not build it before this item comes up.**

⛔ **AND THIS IS THE ONE WAY NOT CREATING A NAME OBJECT COULD HAVE BEEN COSTLY**, which is why it
is written down here rather than left as a feeling. Ruled in the same breath, about the
2026-09-14 punctuation work: *"there is a way not creating name objects could have been costly,
but the problem is that you might have internalized that it 'could' have been costly without
understanding why."*

The reason is this plan and nothing else. A name object is not only a `P735`/`P734` target --
under this plan the name items on the PARTS of a `mul` label are the input that CJK readings get
generated from, so a part with no name object is a part that generates nothing. That is a real
cost and it is specific.

**It does not reopen anything decided on 2026-09-14.** *"There's effectively zero cost for not
creating a name object"* stands as the rule for junk: `.`, `Rd.`, `(Wife`, `und`, `Count` are not
parts of anybody's `mul` label and generate no reading in any language. The two live together --
zero cost for a bad object, a real cost for a missing good one -- and the thing to carry forward
is *why*, so the next strictness decision is made on this ground instead of on a vague worry.

## PINNED LAST -- RESTART THE PATH COLLECTION IF IT HAS STOPPED

Ruled 2026-09-14: *"have the very last queue item be one that would be to restart the path
collection in the event that the path collection ended up stopping."*

**This is the only queue item about the path collection.** Everything else about it is a
background assumption, per the top of this file.

    check   window.__pathrun.running and window.__chains.running in the geni.com tab
    if the tab was lost, re-establish both from the scratchpad chunk files:
      scratchpad/path-chunks/chunk-NNNN.txt   the requester's 2,000-id target lists
      scratchpad/perma2/perma-NNNN.txt        the fetcher's permalink lists
    the runner resumes from a chunk, so nothing already requested is requested again

**Its stopping is not an emergency and not a reason to work on it.** Restart it, go back to the
first item.

