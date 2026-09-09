# The collector's run loop — her dictation, 2026-09-06

**This is the whole of what the extension does per individual.** Written down before any of it is
built, because the last day was spent building pieces of it in the wrong order.

> *"You just go on the page, the page loads, and it's like run the tiny gedcom scrape thing, makes
> a tiny file with the family... I think it probably should be automatically when you're on it and
> you call the get path thing, it'll write the tiny file from the script, and then it'll do the
> request, and then it'll wait until the file thing is done... or it'll wait until the export is
> done by doing a watcher thing on it, then expand it, then grab the path that's generated, add it
> to the TSV thing, and also make another tiny gedcom for the file, which goes into the different
> directory.*
>
> *And in the event of failure, the logic thing should then check the relatives numbers. And if the
> relatives numbers indicate that it would be worthwhile based off of our common threshold there,
> I believe three hundred, then it goes through the process of trying to iterate through the
> family tree in order to add the individual and run the forest export. It would of course be
> flagging the individual as being one that we're exporting, in some kind of a ledger.*
>
> *It's a relatively extensive, almost entirely automated process. And the only reason why it's not
> completely automated is because of CAPTCHAs. Because by agentically going to the page and then
> running the extension, you are considered to be proper traffic.*
>
> **"There's no discretion on your part at all."** *(said three times)*
>
> *The idea behind this is that by doing this stuff, we are going to be getting all these Wikidata
> people connected into the tree.*

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

## ⛔ NO DISCRETION ON THE AGENT'S PART. She said it three times

The agent navigates. Everything after that — whether the path resolved, whether the statistics
justify an export, which ancestor to add, whether to run the export at all — is the extension's,
decided by the same rule every time.

**This is the correction of what has been happening.** Today the gate lived in
`scripts/export_gate.py` and was applied by me, per person, in prose; the family scrape and the
path request were separate jobs I dispatched by hand and reasoned about between; the ledger row
was written by a script I sometimes remembered to run. Every one of those is a judgement call the
extension should be making identically 2,527 times.

## ⛔ WHY IT IS AGENTIC AT ALL: the CAPTCHA, and nothing else

*"The only reason why it's not completely automated is because of CAPTCHAs. Because by agentically
going to the page and then running the extension, you are considered to be proper traffic."*

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
| 5b. statistics gate at 300 | **built but in the WRONG PLACE** — `scripts/export_gate.py`, applied by me |
| 5b. walk the tree, add the individual | **built** — `GC.runSeed`, and the walk in `background.js` |
| 5b. run the Forest export | **built** — `GC.runExport`, never exercised this session |
| 5b. flag in a ledger | **not built** — no export-target ledger exists |
| the whole thing as ONE job | **not built** — it is five jobs I sequence by hand |

**The missing piece is the sequencing**, not the parts. Almost every step exists as a job the
agent has to call in the right order and reason about between calls; her design is one job that
runs the whole loop and makes every decision itself.

## The goal, in her words

*"By doing this stuff, we are going to be getting all these Wikidata people connected into the
tree."*
