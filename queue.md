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

- **Build the Ethiopian and Japanese emperor rosters from Wikidata.** Her call, 2026-09-03, asked
  how to source them: *"Build from Wikidata later."* Both are entry-point groups dated 2027-01-01
  in `reports/entry-point-groups.tsv` and both currently resolve to **0** people, because nothing
  in the repo enumerates either. Needs a session with network access — Wikidata is blocked from
  the remote one. Query the holders of each position, join to Geni ids through `P2600`, write
  `reports/ethiopian-emperors.tsv` and `reports/japanese-emperors.tsv` with `qid` and `geni_ids`
  columns, then point the two group rows at them. Do **not** pick either list out by label: the 52
  tree labels matching Ethiopia/Negus are the surname *Neguse*, which is what that would catch.
