# The collector's run loop — dictated 2026-09-06

**This is the whole of what the extension does per individual.** Written down before any of it is
built, because the last day was spent building pieces of it in the wrong order.

**The specified loop, per individual.** The page loads; the tiny-GEDCOM family scrape runs and
writes the family file; the path request goes out on the same call; a watcher waits until the
path resolves or the export finishes; the path is expanded, grabbed, appended to the TSV, and
written out as a second tiny GEDCOM into its own directory.

**On failure it checks the relatives numbers.** If they clear the common threshold — about
**300** — it iterates through the family tree to add the individual and runs the `Forest` export,
flagging that individual in a ledger as one being exported from.

**⛔ THERE IS NO DISCRETION ON THE AGENT'S PART AT ALL** — stated three times in the dictation,
which is the measure of how load-bearing it is. The process is extensive and almost entirely
automated; the only reason it is not completely automated is **CAPTCHAs**, because navigating to
the page agentically and then running the extension is what counts as proper traffic.

**The purpose is connecting the Wikidata people into the tree**, which is what all of it is for.

## The sequence, per individual

    1.  land on the profile                        <- the agent's ONLY job
    2.  scrape the immediate family                -> tiny profile GEDCOM, written immediately
    3.  request the Charlemagne path
    4.  WAIT on a watcher until it resolves        <- not a timer, not a fixed sleep
    5a. path found  -> expand it ("Show short path")
                    -> grab the chain
                    -> append to the path TSV
                    -> tiny path GEDCOM, into the OTHER directory
    5b. no path     -> read the statistics block
                    -> below the threshold: stop, nothing more is worth spending
                    -> at or above it: walk up the family tree, add the individual,
                       run the Forest export, and flag them in a ledger as an export target

## ⛔ NO DISCRETION ON THE AGENT'S PART. Stated three times

The agent navigates. Everything after that — whether the path resolved, whether the statistics
justify an export, which ancestor to add, whether to run the export at all — is the extension's,
decided by the same rule every time.

**This is the correction of what has been happening.** The gate lived in
`scripts/export_gate.py` and was applied per person, in prose, by whoever was at the session; the
family scrape and the path request were separate jobs dispatched by hand and reasoned about in
between; the ledger row was written by a script that was run when somebody remembered. Every one
of those is a judgement call the extension should be making identically 2,527 times.

## ⛔ WHY IT IS AGENTIC AT ALL: the CAPTCHA, and nothing else

**The only reason it is not completely automated is CAPTCHAs**: navigating to the page
agentically and then running the extension is what counts as proper traffic.

So the browser-driven navigation is not a limitation to engineer away — it is the mechanism that
keeps the traffic acceptable. A background fetch loop would be the thing that gets blocked. Geni
served an Incapsula CAPTCHA earlier today after roughly forty rapid loads, which is the cost of
getting this wrong.

## What exists already, and what does not

| step | state |
| --- | --- |
| 2. family scrape → tiny profile GEDCOM | **built** — `GC.runFamily`, `build-tiny-gedcoms.py` |
| 3. request the path | **built** — `GC.runPath` |
| 4. watcher until resolved | **partly** — `GC.until` waits, but the job is dispatched and polled by hand |
| 5a. expand, grab, TSV, tiny path GEDCOM | **built** — `GC.parsePath`, `GC.toTsv`, the path emitter |
| 5b. statistics gate at 300 | **built but in the WRONG PLACE** — `scripts/export_gate.py`, applied by hand |
| 5b. walk the tree, add the individual | **built** — `GC.runSeed`, and the walk in `background.js` |
| 5b. run the Forest export | **built** — `GC.runExport`, never exercised this session |
| 5b. flag in a ledger | **not built** — no export-target ledger exists |
| the whole thing as ONE job | **not built** — it is five jobs sequenced by hand |

**The missing piece is the sequencing**, not the parts. Almost every step exists as a job the
agent has to call in the right order and reason about between calls; the design is one job that
runs the whole loop and makes every decision itself.

## The goal

Getting all these Wikidata people connected into the tree.
