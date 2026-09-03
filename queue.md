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

- **AskUserQuestion: placeholder relationships for the siblings in these chains.** The paths
  produce dummy placeholders for siblings on the path, and Emma's view, 2026-09-03, is that
  *"we still do this thing"* and it is *"mostly unchanged"* — annoying, and possibly workable
  around depending on the scale and difficulty of scraping the parents. Put the question to her
  with `AskUserQuestion`. **Do not pre-investigate it**; `CLAUDE.md` § *"Add it to the end of
  the queue" means WRITE IT DOWN AND STOP* governs.

  Carry the measured answer to her own question into the options, because it bounds what a
  placeholder can say: over 30,329 path steps in 696 files, **ex-spouses are discriminated**
  (`her ex-husband` 52, `his ex-wife` 42, `her ex-partner` 42, `his ex-partner` 28, against
  `her husband` 934 / `his wife` 908) and **half-siblings are not** — `his brother`/`her sister`
  and no `half` anywhere, though Geni writes *"Half brother of"* in the immediate-family panel
  and in the prose `relation_description` sentence on the same page.
