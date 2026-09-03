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

