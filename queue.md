# Queue

Only work. An item is DELETED when done, never annotated. Bullets, never numbers —
`CLAUDE.md` § *Queue items are BULLET POINTS*.

**Read `docs/collector-run-loop.md` before touching the collector.** It is your dictation of the
whole run loop and it ends *"there's no discretion on your part at all"*, said three times.

---

- **⛔ DESCENDANTS EXPORTS ON THE 15 HINGE PEOPLE — digested out of `undigested.md`,
  2026-09-09.** A *hinge person* is defined there: *"people who seem to have clearly disjoint
  large numbers of descendants, and as such are good descendants export sources."*

  **EASTERN european tang — 9**

      6000000146583752828  Елбуздуко Битуев
      6000000008867333533  Князь Кабарды Камбулат Идарович Черкасский
      6000000028522915307  Zhelegot Mirza Cherkassy
      6000000191078589837  knyaz Kanshov of Cherkessia
      6000000220167394834  Джамурза Джиляхстанов
      6000000048540283061  Kamal Kara Musel Джилястханов, Shamkhal of Tarku
      6000000144779499889  Alkas Jamurzin Dzhilyakhstanov
      6000000146583752840  Князь Пшеапшоко Кайтукин Черкасский
      6000000220167401825  Шолох Акуджба

  **WESTERN european tang — 6**, the Cilician Armenian side

      6000000006101354712  Princess Alix de Lampron
      6000000006101354653  Constantine I, lord of Lampron
      6000000006101354662  Constantine, lord of Barbaron
      6000000006101430432  Leo I the Magnificent, king of Armenia
      6000000006101354628  Tolita Doleta of Armenia
      6000000007086662766  Ruben III Rouponi, King of Armenia

  **Per person: create an ANCESTOR of them per `docs/export-seed-rules.md`, then run a
  `Descendants` export on the created ancestor.** `Descendants`, **not** `Forest` — see the
  campaign item below for why. One at a time; Geni's limit.

  The OneTab page in `undigested.md` is **not** digested and stays there: still being worked on,
  *"better for my judgment on this one."*

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

  **`reports/cjk-culture-manual.tsv` is committed with its header and no rows**, and
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
  - **`6000000035218690155`** — <https://www.geni.com/people/n-n/6000000035218690155>. Added
    2026-09-10: *"Abul Hamza is top priority but descendants of
    https://www.geni.com/people/n-n/6000000035218690155 should be in there too"*.

    **Its position in this order was NOT stated**, only that it belongs in the campaign and that
    Abul Hamza outranks it. Recorded here rather than ranked, and nothing about the person is
    investigated, measured, seeded or grepped — `CLAUDE.md` § *"Add it to the end of the queue"
    means WRITE IT DOWN AND STOP*. The slug is `n-n`, so the profile is an `NN`.

  - **Bergitte Aukland** `6000000002481819312` — *"as far as export capture descendants people
    add https://www.geni.com/people/Bergitte-Aukland/6000000002481819312 to it as well she is
    kinda critical"*, 2026-09-09. **Her slot was settled the same day: `Replaces Tore`.** She
    takes Tore Underberge III's place in this order and **Tore Underberge III
    `6000000005607672589` comes OFF the list.**

    **⛔ AND THE EXPORT GOES FROM A DIFFERENT PERSON — `KNUT ALGOTSSON`, decided 2026-09-10:**
    *"for Bergitte, I decided on a slightly different person to go from: Knut Algotsson"*.

        geni  6000000002572699392      qid  Q5915800
        Knut Algotsson, Geni MASTER PROFILE, curated by 78 people
        b. circa 1330  Hammarö, Karlstad, Värmland, Sweden
        d. after 1393  Rogaland, Norway
        son of Algot Bryniolfsson (`Q19842232`) and Kristina Tolvesdotter Näs
        husband of Märta Ulfsdotter (Ulvåsa) · partner of NN (Frille)
        father of Ramborg Knutsdotter Lejon, Ingegerd Knutsdotter, Katarina, Ingrid Knutsdotter
        brother of Bengt Algotsson · CHARLEMAGNE IS CONNECTED TO HIM, stated on the page

    **He replaces Bergitte as the person to go from, not as the target** — the campaign is still
    her descendants, and he is where the export starts. Whether the seed rule still applies on
    top of him — create an ancestor of HIM and export `Descendants` from that ancestor — is
    **not decided here**, because the two readings differ and this was written down rather than
    interpreted.

    Nothing about either of them is investigated, measured, seeded or grepped yet.
  - **Gamle Olof** `5328189268700111491` — **BEFORE the Chinese clusters, ruled 2026-09-09.**
    The two readings differed by exactly one position — *"after you've comprehensively gotten the
    descendants of this particular individual"* put him straight after Abul Hamza, while the
    numbered list put the Chinese clusters second — and the first reading won. So the head of the
    order is settled end to end:

        1  Abul Hamza  6000000227676734863     in flight
        2  Bergitte Aukland  6000000002481819312   critical; took Tore Underberge III's slot
        3  Gamle Olof  5328189268700111491
        4  NN ben Ovadya  6000000227708968860   ruled 2026-09-11, "after gamle olof"
        5  the two most eccentric ancient Chinese clusters

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

## What this session settled, so it is not relitigated

* **Tiny GEDCOMs are the native format.** One per person, one per path, in different directories
  even when both come off the same page. `exports/tiny-profiles/`, `exports/tiny-paths/`.
* **An unknown parent is an ABSENT SLOT, never an `NN` person.** A sibling pair with no known
  parents is a `FAM` with two `CHIL` and no partners. `exports/0-scraped/` and
  `build-scraped-gedcom.py` were deleted on your instruction for inventing 4,928 people.
* **The export gate is one floor of 250 on any statistics figure**, disjunctive, and it lives in
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
  2026-08-29. Live in the 2026-09-09 session as `b6ad7ac1`, `2263d879`, `f09fcc7b`, `803b418d`, created at
  the top of it against a `CronList` that read *no scheduled jobs*; the 2026-09-05 ids
  (`7c8cc0c6`, `7fb9d24f`, `9f3125b0`, `caf417ce`) and everything before them are dead sessions',
  which is the reason to check `CronList` rather than trust this line.
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

**One thing is left of the three, and it does not touch a person's data either:**

- **Cut the strategy content.** Anything in `CLAUDE.md`, `queue.md`, `devlog.md` or the scripts
  about how that item gets linked or how the account's editing reads to others.

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
