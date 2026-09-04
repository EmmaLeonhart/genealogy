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

- **Study the behaviour of the Wikidata user `Anvilaquarius`.** Emma, 2026-09-03: *"Anvilaquarius
  is a user I want to study the behaviour of."* Then, pointing at a pastebin on her screen:
  *"Actually just this pastebin it"* — **<https://pastebin.com/v4UcMx36>**, which is the material
  to work from. Nothing has been fetched or looked at; `CLAUDE.md` § *"Add it to the end of the
  queue" means WRITE IT DOWN AND STOP* governs.
  **A second case, 2026-09-03:** *"a few ones like https://www.wikidata.org/wiki/Q29246906 and
  https://www.wikidata.org/wiki/Q138582215 appear to have not had geni ids added on wikidata
  despite having been edited and I am not sure what is going on with it"*. So it is a class
  rather than one item, and the question is what edited them without adding a `P2600`. Still
  not looked at.
  The URL is transcribed from a photo of her screen, so check it resolves before relying on it.

- **Investigate items edited but never given a Geni id — `Q138582215` and `Q29246906`.** Emma, 2026-09-03:
  *"https://www.wikidata.org/wiki/Q138582215 idk how this was edited but no geni link or mul
  label add investigation to queue at end do not focus on it now just put at the end"*.
  So the question is **how the item came to be edited in that state** — carrying neither a
  `P2600` *Geni.com profile ID* nor a `mul` label, both of which every batch this repo emits
  puts on. Nothing has been fetched or looked at; `CLAUDE.md` § *"Add it to the end of the
  queue" means WRITE IT DOWN AND STOP* governs.

- **A script that hands back one random unconnected Wikidata isolate.** Emma, 2026-09-03, after
  watching profile-picking take far too long: *"you probably should have a script that spits out
  a random one whenever you need one."*

  Her specification, in her words: *"my vision would be that you have some kind of a csv file
  storing all of the wikidata isolates, and the script randomly selects one, checks if it is
  connected into the synoptic tree (geni links in the big mass), and if it is not then it
  returns it, and if it does not then it randomly selects another one and does the same, with a
  later option to with the script to refresh things so that the isolates csv is updated in cases
  where it is stale and a large portion of the unconnected people are skipped over, maybe even
  actually just removing the one that was found to be connected as soon as it is skipped over,
  making the script automatically heal it"*.

  So: a roster CSV of every Wikidata isolate → pick at random → test membership of the big
  connected mass of the synoptic tree → **return it if absent, drop it from the roster and
  re-draw if present**. The dropping is the self-healing: the file gets more accurate every time
  it is used, with no separate maintenance pass. A `--refresh` rebuilds the roster wholesale for
  when staleness has made too many draws miss.

  Note the connectivity test already exists in miniature — a BFS from Charlemagne over
  `reports/derived-family.csv` reaches 1,450,615 of 1,451,964 people — so the script is that
  walk plus a roster and a random draw.

* fix the daily batch quickstatements page since the copy button does not work
* fix the branding of this project away from geni since although the main thing it does is geni derived exports to wikidata that is not the core of it and not what I want the branding to be

- **Two algorithmic deviations in the daily batch — the Geni id is not first, and `mul` is
  often never assigned.** Emma, 2026-09-04, verbatim:

  *"It seems it is still messing with people's names without doing geni identifications. Like the
  name objects are being linked on people without geni ids, this should be categorically not
  allowed as the geni id must be applied as the first edit on any individual. If linking another
  relative, well in the create statements for the relative the geni id gets added before the
  relationships lol. Idk why it thinks name objects are an exception when the name data even
  comes from geni"*

  *"Also I am noticing mul labels are not being assigned based on most commonly agrees upon Latin
  alphabet label as I wanted on wikidata but instead many people are just never given mul labels.
  So yeah some algorithmic deviations exist"*

  So two separate deviations from her specification: a `P735`/`P734`/`P5056` name link emitted on
  an individual carrying no `P2600`, when the Geni id is meant to be the **first** edit on anybody
  and a name item is not an exception to that; and `mul` being left unset instead of taking the
  most commonly agreed Latin-alphabet label.

  Nothing has been looked at, measured or fetched — `CLAUDE.md` § *"Add it to the end of the
  queue" means WRITE IT DOWN AND STOP* governs. Related and not to be solved twice: `CLAUDE.md`
  § *An item with no relationships is not a missing item* is where the Geni-id-first order is
  already written down in her words, and § *The MARRIED name is the real name* is where `mul`
  is specified.

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

