# Queue

Only work. Every specification and record moved to `CLAUDE.md` on 2026-09-01 at her instruction: *"remove all the 14 bullshit queue items"*. An item is DELETED when done, never annotated.

- **BLOCKED-ON-EXTERNAL — the full synoptic rebuild.** Started 2026-09-05 at her instruction,
  because three `.ged` files are newer than `out/merged.ged` (Sep 1): two `post-merge` Forest
  exports and `wikidata-qid-links.ged`. **Run WITHOUT `--slim`** — slim drops `NOTE`, which is
  where the bios and their QIDs live, so the slim tree is the wrong tree for this. Unblock signal
  is the process finishing. It has been OOM-killed on this shape of machine at 13.3 min / 13.3 GB;
  if that happens, report it rather than falling back to `--slim`.
  **Then commit and push the regenerated artifacts** — her sequence: rebuild, regenerate, commit,
  push, confirm good, and only then the retarget below.

- **Retarget `bio-qids.tsv` to a gitignored path — AFTER the rebuild is confirmed good.** Emma,
  2026-09-05: *"it also shouldn't exist lol because it's just garbage for agents to get confused
  about"*, and on the two ways of doing it she chose **retarget**, not deletion of the script.
  So: `extract-bio-qids.py` writes `out/bio-qids.tsv`; the three readers follow
  (`build-emperor-rosters.py:77`, `build-merge-worklist.py:98`, `build-succession-roster.py:119`);
  **one explicit `.gitignore` line** for it, per § *`out/` is NOT gitignored* — named files only;
  `reports/bio-qids.tsv` deleted from tracking. **A separate commit and push from the rebuild**,
  which is how she asked for it. `slim-corpus.py` and `src/genimerge/slim.py` mention the path only
  in prose and need no change.

- **NEEDS-INVESTIGATION — `addAncestor`'s termination has never been exercised.** `background.js`
  drops the remaining seed queue when a result comes back `added`, which is her rule
  (*"it adds an ancestor of `start_id` and returns the id of it as `end_id`"*), but no walk has run
  through to a creation since that was written. It is code that has been read, not behaviour that
  has been measured, and the last real creation predates the change. Unblock signal is one walk
  from a real seed through to a single creation, with the queue observed to stop.

- **NEEDS-DECISION — the six unruled `.qs` generators. PUT THIS TO HER AS AN `AskUserQuestion`.**
  `reports/qs-batch-audit.md` measured **0 of 27** `.qs` files as produced by anything the pipeline
  runs. Nine have generators; three are settled. These six are not, and each wants one ruling
  — fold into the daily batch / give its own schedule / delete:

  - `build-add-p2600-batch` — 7,166 `P2600` from parent-anchor proof
  - `build-missing-reciprocals` — 6,770 statements, **no live check** by design; was folded in on a
    wrong claim and taken back out
  - `build-qid-link-p2600` — 354 statements; `CLAUDE.md` records her objecting to this file by name
  - `build-label-corrections` — 148; **measured superseded** by `_label_corrections` +
    `_cjk_follows_mul` in the daily batch
  - `build-sibling-batch` — 420; its own docstring calls it a one-off that ignores `SIBLING_CAP`
  - `build-from-diff` — 78 + 8; wired into `pipeline.yml` on a claim rather than a measurement,
    which is why its review is also queued at the tail

- **NEEDS-DECISION — the `.crx` + `ExtensionInstallForcelist` install. PUT THIS TO HER AS AN
  `AskUserQuestion`.** The `.crx` is packed and `update.xml` staged in `%LOCALAPPDATA%\geni-collector`;
  extension id `khcdcngbbjcdelkccmokkkbimjikfahl`. `HKCU\Software\Policies` is ACL-denied and the
  harness blocks the non-policy registry write, so the remaining route needs an **elevated shell**
  for `HKLM`. **Convenience only** — the extension is loaded and working via Load unpacked, and
  survives restarts; this only removes Developer mode and the folder-must-not-move condition.

- **Fetch the 100-target isolate path pilot.** `reports/isolate-path-pilot-urls.txt` — **100
  profile URLs**, one per target, and `reports/isolate-path-pilot-queue.txt` is the same list in
  the collector's input format. Then `python scripts/harvest-isolate-paths.py --write-paths` for
  the hit rate. **5 of 100 captured so far.**

  **Both `blood` and `inlaw` are still wanted — her call, 2026-09-02** — but they are two
  captures from the one profile page, not two fetches: blood against in-law is a control on the
  page, not a URL parameter. They file as `geni-paths/<geni id>-<kind>.html`, which is what the
  harvester looks for. One a minute, no concurrency, bail on anything odd.

  ⛔ **This item said "200 URLs, both `blood` and `inlaw` per target" until 2026-09-05 and that
  method is refuted.** The `/path/x?from=&path_type=&to=` form ignores `to=`: it redirects to
  Charlemagne's own profile, which renders a full chain — the *viewer's* — so a harvest keyed on
  step count scores every miss as a hit and returns a reach rate made of copies of one path.
  Re-measured 2026-09-05 from her own browser. `geni-paths/README.md` § *THE CALL THAT WORKS*
  has the working call verbatim; do not re-derive it.

  Anchored on **Charlemagne** (`6000000002457013227`, `Q3044`), her correction of 2026-09-03 —
  not on Emma, which is what the 663 existing paths use. The anchor is her account's pushpin,
  set once by her, and is never toggled.

  **Needs her browser, and now runs through `geni-extension`** rather than agentically. The
  number it produces decides whether the 185,327-target campaign runs — her own batches were
  34–39% for occupation-filtered academics and 92% for Nordic ones. A blank chain is
  `chain_found=0`, never *unrelated*.

- **The parent-adding campaign.** GATED: it starts once the placeholder parents have been
  sufficiently gathered in the synoptic tree and a bunch are on Wikidata. Emma, 2026-09-03:
  *"In the future after we've sufficiently gathered all the placeholder parents and added a
  bunch to wikidata we can do a parent-adding campaign, especially if we use forest exports in
  closely related eccentric graph points on geni."* The instrument is `Forest` exports seeded at
  eccentric points, the same one § *"Not related to" does NOT mean not related* uses. Do not
  start it early and do not invent the gate's threshold — that is hers.

- **Review `build-from-diff`.** Emma, 2026-09-05, on it being wired into `pipeline.yml`
  *"tolerantly, since it needs a diff to read and may have nothing to do"*: *"Put a review of
  this at the end of the queue"*. It is now the only unscheduled generator that was folded into
  the pipeline on a claim rather than on a measurement — `build-missing-reciprocals` was put in
  beside it and taken straight back out, because the justification given for both turned out to
  describe the wrong thing. Nothing has been investigated; `CLAUDE.md` § *"Add it to the end of
  the queue" means WRITE IT DOWN AND STOP* governs.

- **Experiment: generate the manual parental zipper correspondences into a gitignored GEDCOM that
  the synoptic tree merge consumes.** Emma, 2026-09-05: *"I actually think a good long term
  architectural smoothing would make it so that in the pipeline they are generated into a
  gitignored gedcom that is part of the synoptic tree merge, with qids in bios being a fundamental
  part of the pipeline. But for now pipeline works well and that will be a thing to experiment
  with at the end of the queue."* `docs/correspondence-merge-proposal.md` is the proposal, written
  2026-09-05 at her request; it is not a decision. **The pipeline works and must not be broken** —
  her words — so the GEDCOM is generated *in addition* first and the direct CSV read goes only
  once the tree route is shown to carry the same pairs.

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

