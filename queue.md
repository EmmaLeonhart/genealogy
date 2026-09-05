# Queue

Only work. Every specification and record moved to `CLAUDE.md` on 2026-09-01 at her instruction: *"remove all the 14 bullshit queue items"*. An item is DELETED when done, never annotated.

- **Fetch the 100-target isolate path pilot.** `reports/isolate-path-pilot-urls.txt`, 200 URLs,
  both `blood` and `inlaw` per target — her call, 2026-09-02. Blob-save each as
  `geni-paths/<geni id>-<kind>.html`, one a minute, no concurrency, bail on anything odd. Then
  `python scripts/harvest-isolate-paths.py --write-paths` for the hit rate.
  Anchored on **Charlemagne** (`6000000002457013227`, `Q3044`), her correction of 2026-09-03 —
  not on Emma, which is what the 663 existing paths use.
  **Needs her browser**: Geni is not reachable from the remote session, and the anchor is pinned
  by her logged-in account. The number it produces decides whether the 185,327-target campaign
  runs — her own batches were 34–39% for occupation-filtered academics and 92% for Nordic ones.
  A blank chain is `chain_found=0`, never *unrelated*. `geni-paths/README.md` is the method.

- **The parent-adding campaign.** GATED: it starts once the placeholder parents have been
  sufficiently gathered in the synoptic tree and a bunch are on Wikidata. Emma, 2026-09-03:
  *"In the future after we've sufficiently gathered all the placeholder parents and added a
  bunch to wikidata we can do a parent-adding campaign, especially if we use forest exports in
  closely related eccentric graph points on geni."* The instrument is `Forest` exports seeded at
  eccentric points, the same one § *"Not related to" does NOT mean not related* uses. Do not
  start it early and do not invent the gate's threshold — that is hers.

- **Pack `geni-extension` as a `.crx` and install it by policy.** Emma, 2026-09-05, choosing the
  relaunch now and this later: *"Relaunch and put at the end of the queue for it to be .crx and
  policy"*. An unpacked extension needs `chrome://extensions` and Developer mode, which the
  automation surface cannot reach, and a `--load-extension` relaunch has to be redone every time
  Chrome cold-starts without it. A packed `.crx` registered under an `ExtensionInstallForcelist`
  policy survives restarts, needs no Developer mode and no UI click. It wants admin rights on this
  machine. Nothing has been investigated or attempted — `CLAUDE.md` § *"Add it to the end of the
  queue" means WRITE IT DOWN AND STOP* governs.

## ⛔ AT THE TAIL — mass export work on the paths for disconnected Wikidata individuals

**Everything established on 2026-09-03, when Emma taught the task by hand after the automated
attempt failed. `geni-paths/README.md` holds the long form; this is the standing item.**

**The finding that reframes the whole campaign: SIX of six disconnected people returned
"no path found", and it means almost nothing.** `reports/isolates.csv` is the sample. Four of the
six carry **Blood Relatives at 15,000**, which is a *ceiling*, not a count --- Emma: *"15,000 on
any number there is a flag that the query number exceeded the maximum it can do. I do not believe
there is any section of 15,000 connected people on geni that is not connected to the world tree
either, or 5,000 for that matter."*

**And it was proved, not argued.** She ran a `Forest` export near George Drouillard, whose page
says *"No blood relationship was found. No in-law relationship was found."* The export holds 5,000
people; 7 are already in our tree; all 7 are in the main component (1,450,615 reachable from
Charlemagne); and **Drouillard reaches Charles Lespérance in 4 hops inside it.** Geni reported no
relationship for a man four steps from a family continuous with Charlemagne.

**Her precedence order for what to do with each person:**

1. **connected to Charlemagne, no relationship found after the query** --- run a full **Ancestors**
   export, which yields roughly 5,000 new individuals. This is the common case.
2. **connected to Charlemagne, relationship found** --- save the page, **once both blood AND
   in-law have loaded**.
3. **not connected to Charlemagne** --- *"we have not seen an example yet"*, across six.

**One failure mode she named:** Moshe Bar Nissim, the only non-saturated profile in the sample
(1,459 blood relatives), *"is failing because of large in-law chains typical of Jewish people to
get to Charlemagne. But is still almost certainly connected."*

**How the page is actually driven** --- the part the automated attempt got wrong:

- **The pushpin is HERS and is set exactly once.** *"You do not pin Charlemagne, it needs to be
  done exactly once and I did it."* Toggling it mid-run silently re-anchors searches to *"You"*.
- **Read the RENDERED page, never the DOM text.** A hidden `Path search in progress` element
  exists on every profile before any request. Reading `innerText` for it reported **22 untouched
  profiles as running when not one search had been requested.**
- Three visible states: a **"How are they related?"** button (not requested) → a green **progress
  bar** (running) → **"No blood relationship was found. No in-law relationship was found."**
  (resolved).
- **~10 seconds of attention per profile, but each tab stays open for minutes** --- up to ten.
  *"If you do not leave the tabs open then it actually messes a bit with the data that is
  given"*, and closing them *"drops its promise to notify you, or it only notifies you on the
  most recent one you requested."* RAM on our side is the limit on batch size.
- **The notifications are not the collector**: *"the notifications actively give a worse version
  of the data."*
- A **missing statistics row means zero**, not unknown --- Geni omits `Ancestors` rather than
  printing 0.

**Why this was slow, recorded so it is designed around rather than repeated.** A human reads the
state at a glance; an agent gets one sampled snapshot per tool call at 10-20 seconds each, so it
substitutes cheap DOM reads --- which is exactly the channel that lies here. Playwright does not
rescue it: the task needs her logged-in Chrome profile, and the search latency is server-side.
**So the design must minimise observations, not parallelise them**: read the statistics block
once, click once, and come back much later.

**The two shortcut columns.** `descendants` and `followers` in the first six rows are placeholder
zeros at her instruction, not readings --- at least two of those people visibly have children.
`family_tree`, `blood_relatives` and `ancestors` are measured.

**No `qid` column, ever:** *"the qid line is just completely prone to fabrication lol."*

