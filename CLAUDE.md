# Synoptic

## What this project is

**A campaign to connect every `P2600` person on Wikidata into one comprehensive family tree,
using Geni exports as the material.** Wikidata is often the better genealogy source; Geni is the
better *reach*. Joined, one can connect people the other leaves stranded.

**The repo generates QuickStatements every day through CI/CD**, and those go to Wikidata, where
they are expanded. It is moving towards automated edits rather than pasted batches.

**The synoptic tree is the thing everything runs on.** It has two meanings and both are in use:

* **the Geni union** — every `.ged` under `exports/` merged into one tree, `out/merged.ged`.
  *"Rebuild the synoptic tree"* always means this.
* **the full union** — that tree joined to Wikidata, which is what the campaign actually needs
  and **does not exist yet**.

It is keyed on the Geni profile ID throughout, so merging is an exact join and never a name
match. It is **slimmed**: anything not feeding the pipeline that ends at Wikidata is dropped on
input, which is what made it buildable in Actions at all.

## Where the pipeline is pointed right now

**At the Bure kinship in Sweden and the surrounding Scandinavian genealogy.** That is deliberate
and narrow. **It broadened on 2026-09-01** (moved forward from 2027-01-01 by Emma on 2026-09-30),
driven by `exports/post-merge/wikidata-qid-links.ged` — the file of Wikidata identifications that
turned into entry points on that date — and the seven entry-point groups.

## What is left

* **The Geni exports are mostly done.** A few are still running. They are **commanded rather
  than routine and they are a bit iffy** — run because those individuals were judged important,
  not because a rule selected them.
* **The descendant-gathering campaign.** Comprehensively export the descendants of named
  individuals, because **the descendants of these people are poorly documented on Geni and other
  sites and tend to be removed abruptly** — so gathering them is time-sensitive, and
  representing them on Wikidata is the point. `queue.md` holds the roster and the order.
* **The `P2600` connection campaign** — every holder either connected to Charlemagne or confirmed
  impossible. 518,889 holders, 266,201 currently disconnected.

**The first descendants target is the Cyprus person — Abul Hamza `6000000227676734863`** — and
the specific interest is **finding descendants of hers living in Scandinavia**, because those
would link into the people the tree already revolves around. Her Ancestors, Descendants and
Forest exports are down; the descendants ball came back **at the cap**, so the gathering has
barely started. `queue.md` holds the rest of the roster and its order.

## Not yet — the Wikidata update

**Updating the Wikidata side properly is wanted, and it is not time.** It waits; the pipeline has
to get further first. Do not start it, and do not treat its absence as a gap to close.

## ⛔ The practical barrier: the zipper merge

**The zipper merge is supposed to do entity resolution between Wikidata and Geni at scale** —
assigning QIDs to people, so the synoptic tree knows who is who. **It is not doing that well, and
the pipeline is effectively manual as a result.** That is an error caused by other
complications, **not the intended long-term shape**. The intent is zipper merging doing the
resolution over very large amounts of both sides, which is also what makes the tree efficient:
the more people are identified with each other, the less duplication there is to carry.

Treat manual adjudication as a stopgap. → [corpus-and-tree](docs/rules/corpus-and-tree.md)

---

**Below this line is RULES ONLY.** Every rule links to the page carrying its evidence — the
measurement that established it, the failure that caused it, the counts it operates at. Cut from
5,548 lines on 2026-09-09; nothing was deleted, it was moved. If a rule looks arbitrary, the page
says why, and § *the stupider and more specific the instruction* applies.

| page | what it holds |
| --- | --- |
| [`docs/rules/names.md`](docs/rules/names.md) | names, labels, patronymics, CJK, transliteration |
| [`docs/rules/wikidata-editing.md`](docs/rules/wikidata-editing.md) | what goes out, caps, properties, entry points, decks |
| [`docs/rules/corpus-and-tree.md`](docs/rules/corpus-and-tree.md) | exports, the merge, the zipper, dates |
| [`docs/rules/working-here.md`](docs/rules/working-here.md) | process, asking, blockers, reporting |
| [`docs/rules/collector-and-browser.md`](docs/rules/collector-and-browser.md) | the collector, Geni, Chrome |
| [`docs/rules/ci-and-pipeline.md`](docs/rules/ci-and-pipeline.md) | CI, the pipeline, the published site |
| [`docs/algorithms.md`](docs/algorithms.md) | the daily / edit / tail algorithm specifications |
| [`docs/unconnected-worklist.md`](docs/unconnected-worklist.md) | the unconnected-`P2600` worklist spec |

`queue.md` is the work. `devlog.md` is what happened. `name modelling.txt` is the authority on
how a name is modelled and beats anything here.

---

## Skills

`.claude/skills/` — `emergency-stop`, `cron-is-local`, `autonomous-loop`,
`queue-driven-workflow`, `writing-style`, `cleanvibe-update-check`. Vendored, kept current by
the last of them. Last check `2026-07-31`. Source: <https://cleanvibe.emmaleonhart.com/updates.md>

## The primary key

**The Geni profile ID is the primary key for everything.** It is the GEDCOM xref
(`0 @I6000000001846508982@ INDI`) and the `RFN`. Merging is an exact join, never fuzzy name
matching. `genimerge.identity` is the only place that knows this.

**Exactly four xref prefixes exist** — `I` on `INDI`, `F` on `FAM`, `N` on `NOTE`, `S` on
`SUBM`, over 291,439 xrefs. `GENI_ID_RE` is `^@[IFNS](\d+)@$` and accepts nothing else: when it
accepted any letter, `@NI04461@` parsed as Geni ID `04461` and pointed at a stranger's profile.

---

# THE RULES

## ⛔ The default when nothing else is running

**Idle time goes to the disconnected list.** Whenever the queue is not producing work, go back to
`reports/unconnected-p2600.tsv` and run the Chrome extension over it, linking unconnected
Wikidata people in through Geni. That is the standing fallback, not something to be asked about.
**266,201 people, 266,100 eligible today** — `reports/unconnected-p2600.tsv`, built by
`scripts/build-unconnected-worklist.py` and regenerated by `tree.yml` after every rebuild.
The extension's attempts are stamped into the `last_attempted` column by
`scripts/attempt_ledger.py`, which `write-family-scrape.py` calls on every capture, and a
stamped person waits out a 30-day cooldown.

**The order everything runs in, ruled 2026-09-09:**

    1. the minor technical issues in flight
    2. the eleven commanded exports            DONE 2026-09-09
    3. digest `undigested.md`                  DONE 2026-09-09 -- 15 hinge people, now queued
    4. a couple of collector runs, to prove the pipeline works
    5. the mass descendants exports on those groups
    6. THEN the 266,201, as the default whenever the queue is empty

**⛔ THE 266,201 ARE NOT A LAST RESORT AND THE COLLECTOR RUNS HAVE NOT BEEN SYSTEMATIC ENOUGH.**
The extension exists to make each one **mindless** — navigate, dispatch, write the files, next —
and the failure has been doing them inconsistently or narrating them rather than running them.
Run a couple deliberately and check the pipeline end to end before treating the number as a
grind.

**⛔ A LONG-HORIZON INSTRUCTION IS NOT ANSWERED FROM THE FIRST SLICE.** The recurring failure here
is taking a task that runs for hours over many rounds, drawing a conclusion from the first
result, and reporting it as though the work were done — dressed up as caveats, which reads as
diligence. **A `Descendants` ball that came back at the cap is truncated by definition** and can
only say what is *in* it, never what is absent from the descent.

**⛔ THE STOPPING CONDITION IS DIMINISHING RETURNS, NOT A COUNT.** The descendants campaign runs
**Monte Carlo exports off the people already in the person's GEDCOM** — sample, check the census,
export from the saturated ones, merge, sample again — **until it is clearly hitting significant
diminishing returns.** Only then is it clear whether the thing works.

**An "export" here means: create an ANCESTOR of the saturated person per
`docs/export-seed-rules.md`, then run a `Descendants` export on that created ancestor.**
**⛔ `Descendants`, NOT `Forest`** — this overrides both that file's fixed style and
§ *anything odd about a person → `Forest` export*. `Forest` follows spouse links and spends the
5,000 slots sideways; this campaign needs the ball to go down.

**⛔ AND THE ROUND ITSELF HAS NO DISCRETION IN IT — `docs/monte-carlo-procedure.md`.** Ruled
2026-09-13: *"the failure mode of the Monte Carlo campaign was that you did too much of your own
judgment, because it was supposed to be strictly organized and scope limited."* The picker was
kept dumb by an explicit rule and **the judgment moved into the campaign around it**, where no
rule was watching. 40 candidates a round, the trunk cut as the frame, `--list-saturated` as the
denylist, every reading ≥ 5000 exported off a created ancestor, and **the root stops when a round
returns zero of them** — a given condition, not a read of the distribution. Seven properties were
invented here as yield predictors and all seven were refuted; they are listed on that page.
**Which root runs is `queue.md` top to bottom and never a choice.**

**Do not substitute a number for that.** *15,000 descendants* was invented here as a floor and it
is not the rule: a fixed target answers "have we done enough arithmetic", and the actual question
is whether new exports are still returning new people. One 5,000-person ball is the first round
of a loop, not a sample of anything.

## ⛔ WHAT A SESSION IS FOR: THE BROWSER WORK. CI/CD DOES THE REST

**Ruled 2026-09-14, and it is the shape of the whole project now:**

> *"the condition has changed ... this is going to take a long time, the solution is that the
> agent is triggered to run this thing every single session, and all it does is it just runs
> this script and commits and pushes it, and the CI/CD is going to be able to deal with
> everything ... I'll just be running the agent periodically, but the CI/CD should be able to do
> all of the stuff."*

**The division is by what needs a logged-in browser, and nothing else.**

    THE AGENT, once a session      Geni needs a real logged-in browser and cannot be automated:
                                   → start scripts/pathrun.js, top it up, commit, push
                                   → run a commanded export if one is queued
                                   → that is the job. Not the batches, not the labels.

    CI/CD, continuously            everything that needs no browser:
                                   tree.yml       rebuild the tree, REFRESH THE P2600
                                                  POPULATION FROM LIVE WIKIDATA, rebuild the
                                                  unconnected worklist from it
                                   pipeline.yml   compose the batch, split it, regenerate the
                                                  inventories, publish Pages
                                   wikidata-edits.yml  7 8 * * *  SEND the automatic half

**⛔ AND THE LOOP FEEDS ITSELF NOW.** Ruled 2026-09-14: *"I also want the CI/CD to check wikidata
to see if there's any new IDs that have been added that are also disjoint or disconnected, and
these will then be added into the queue."* `out/wikidata/p2600-all.tsv` is the master
QID-to-Geni correspondence that forty scripts read, and **nothing regenerated it** — every
workflow consumed it, none refreshed it, so a person given a `P2600` yesterday never entered the
worklist and never appeared anywhere as missing. `tree.yml` now refreshes it before building the
worklist, so new holders arrive on their own.

**⛔ SO DO NOT DO CI/CD's WORK BY HAND.** Composing a batch, regenerating an inventory or
rebuilding the site in a session is duplicated effort at best and a merge conflict at worst —
`pipeline.yml` runs on push and does all three. The exception is a defect: fix the generator,
push, and let the pipeline run it.

**⛔ AND THE EDITS ARE LIVE.** `EDITS_HELD` was lifted the same evening. The schedule sends
`reports/wikidata-garborg-day-auto.txt` — a third of the day's batch — by itself, every day at
08:07. The Pages site publishes the disjoint remainder for a person to paste. Nobody has to
start it.

**The pasted half stays. Ruled 2026-09-25:** asked whether to stop publishing the batch for
pasting (the Pages page and the Daily batch issue), the answer was *keep both*. The sender sends
the rationed `-auto` share; the Pages page and the Daily batch issue keep handing over the whole
batch for QuickStatements. **The overlap is allowed on purpose, and descriptions are why** (Emma, same
day: *"the reason we are doing descriptions is to allow for overlap"*): a creation carries a
description, and Wikidata refuses a second item with the same label and description, so a
person both pasted and sent is created once.

## ⛔ THE WIKIDATA STRATEGY (Emma, 2026-09-30, by AskUserQuestion)

In this order: (1) the 136 duplicate sets are merged and `User:日巫女` declares the account (done 2026-09-30); (2) batches run continuously, each from a pipeline run that has finished and committed it; (3) every entry point starts now, plus `Q701641` Youlan, `Q144348` Zaifeng, Prince Chun and `Q185152` Puyi; (4) FamilySearch creations stay paused (`CREATIONS_PAUSED`) until the zipper work on her ancestors is further along; (5) after the current batch, a private person goes on Wikidata only when they link two or more families.

## ⛔ AT SESSION START: THE BROWSER QUICKSTATEMENTS LOOP

Ruled 2026-09-27 (Emma): editing runs from her own browser, not a GitHub runner, and it starts with the session. Immediately after a session opens: open a NEW QuickStatements tab, load the current `reports/wikidata-garborg-day-manual.txt` (fetch it from raw.githubusercontent into the batch textarea), Import, and press **Run** (never "Run in background" unless she asks).

**⛔ WHAT THE LOOP IS FOR: THE RING. Ruled 2026-09-27 (Emma).** There are two kinds of people in a batch. The **ring people** are made obligatorily in every batch, and they are the limiting factor of the whole campaign: they connect to each other, so the next ring can only grow from a ring that already exists. The **non-ring people** are not the intended thing; they run, but nothing waits on them. So a batch opens with its ring (shuffled), and **whether a batch finishes does not matter**: several QuickStatements runs go at once in the browser, each old tab finishing its tail on its own. A generation is done when the LAST ring person in its batch's order exists on Wikidata.

**⛔ AND CI CHAINS THE GENERATIONS, NOT THE SESSION.** Every day-batch commit in `pipeline.yml` dispatches `ring-watch.yml` with that batch's last ring person (`qs-loop-status.py --last-ring`); it checks every 15 minutes for an item carrying that `P2600` and then dispatches the next lean rebuild (`pipeline.yml -f batch_only=true -f force=true`, about an hour), which starts the next watcher. **The session's only job is to open each new batch in another NEW tab as soon as it lands** (a session cron runs `scripts/qs-loop-status.py` and watches main for a new `rebuild the batch` commit). The session never dispatches the rebuild itself. Overlap between runs is fine: QuickStatements rate-limits each run.

    ⛔ NEVER navigate, reload or close a tab that is running a batch. A QuickStatements run done in
    the browser lives in the page; closing the tab killed Emma's run on 2026-09-27. Only open new tabs.

The noticeboard rule below still applies before any run.

**⛔ WHEN SOMETHING ABOUT THE BATCH IS UNCLEAR, DON'T STOP TO ASK: IMPLEMENT, REGENERATE, RUN. Ruled 2026-09-27 (Emma).** Overlapping batches, a possible duplicate, which order is current: implement the batch-structure changes Emma has asked for, regenerate the batch, and when the regeneration finishes, open another tab and run it. The batch order is ten FamilySearch people first (a separate population, a test that they come out well formed; **paused 2026-09-30**, Emma: FamilySearch creations wait on the zipper merge, `CREATIONS_PAUSED` in `build-familysearch-day.py`, so the section is empty), then the ring (shuffled), then the name items, then the other people one at a time with a slice of the edits on existing items: `max(120, 180 - ring)` of them, so a batch aims at 180 people (Emma, 2026-09-27); the next lean rebuild starts (from `ring-watch.yml`) as soon as the batch's last ring person is created, not when the whole batch ends.

## ⛔ FIRST OF ALL, THE FAMILYSEARCH ZIPPER — ABOVE THE DECKS

Ruled 2026-09-24: *"We should be having the zipper do all of the familysearch stuff. I want
familysearch zippering to be a specific thing that we do start with every session. Since
familysearch zippering is a bit higher priority."* It needs no Geni, so the moratorium does not
stop it, and it comes **before** the three decks below.

**The bridge alone reached 11 people of 4,442.** An exact join through `P2889` and `P2600` needs
an item carrying both ids, and almost none of the owner's ancestors' items do. So
`Q141539855` Emma Olivia Andersdotter was in the FamilySearch tree and nowhere in ours, with her
daughter anchored on both sides, because nothing walked from the daughter to the mother.
`zipper-join.py --familysearch` walks it: 12 anchors, 25 rounds, **4,866 pairs**, and she is
round 3.

    CI, pipeline.yml daily:
      refresh-p2600-all.py [--p2889]     both rosters, out/wikidata/p2{600,889}-all.tsv
    CI, in tree.yml before the merge:
      bridge-familysearch-qids.py        anchors: _FSFTID -> P2889 roster -> QID -> P2600 roster
      zipper-join.py --familysearch      FamilySearch downloads against the synoptic tree
      render-familysearch-gedcom.py --all  every paired person written on their Geni id

    THE SESSION:
      1. git pull; read reports/familysearch-zipper-pairs.tsv against the last session's count
      2. work reports/familysearch-zipper-ambiguous.tsv -- the slots the zipper refuses to guess,
         as the FamilySearch deck (scripts/build-familysearch-deck.py, built by review-decks.yml;
         its verdicts go into emma-judgments.tsv with the fs_id in `qid` and come back as anchors)
      3. then the three decks below

**⛔ THE HAND WORK IS ON EMMA'S DIRECT ANCESTORS ONLY. Ruled 2026-09-30:** *"the zipping that I'm asking you to do is only on the ancestors ... I don't care about identifying siblings with each other."* A deck card or any manual zipper work needs one side to be her direct ancestor: Geni side in `reports/owner-ancestors.tsv`, FamilySearch side an ancestor of her own record `PFR5-LDS`. Siblings, children and spouses' relatives get no cards. A card that asks whether a FamilySearch person is her ancestor (Agnes Jonsdotter / Karin Jonsdotter) is ancestor matching and stays. **⛔ An ancestor card is a FATHER or MOTHER slot whose child is her or one of her ancestors. Ruled 2026-10-01** (*"An ancestor is an ancestor. Your thing compares siblings and spouses and they are not ancestors"*): the zipper's `child` and `spouse` slots never go in the deck, even when one side is on an ancestor list. The 2026-10-01 deck had 523 child and 33 spouse cards of 907.

**THE ROOTSMAGIC EXTRACTION IS FINISHED (Emma, 2026-09-30, confirmed by AskUserQuestion).** The gate is open. Every `.rmtree` and `.ged` of that day is archived read-only in `Documents\rootsmagic-archive\2026-09-30\`, and the sibling repo `rootsmagic-import` already turns `copy of second attempt.rmtree` into a cleaned GEDCOM. The FamilySearch creations pause (`CREATIONS_PAUSED`) stays; its wording about stopping RootsMagic/GEDCOM imports is lifted. The RootsMagic and order.life queue items keep their place after the Wikidata items.

**The FamilySearch side is keyed on `_FSFTID`, never on a file's own counter**, and it is read
from the raw downloads in `gedcom/familysearch/`, never from the renders.
**FamilySearch holds duplicates of its own** — two records, one person, the same parents
(`GDQB-KJQ` and `PNMB-9FS` are both Anna Danielsdotter). A pair whose Wikidata item states the
*other* FamilySearch id is that, not a zipper error: all 6 such disagreements on 2026-09-24 were.

## ⛔ AND EVERY SESSION STARTS WITH THE ZIPPER DECKS, THE SAME WAY

Ruled 2026-09-23: *"I want to do zipper merge resolution right now and make it a constant start
of session thing like the paths"*, and *"You make an artifact as per protocol and then you move
through the queue."* It runs **beside** the path runner, and it needs no Geni, so the moratorium
does not stop it.

    1. gh workflow run review-decks.yml                 -- CI builds the decks, never locally
    2. when it lands, git pull
    3. publish each out/*-review.html as a claude.ai artifact, the same three URLs every session
    4. move on to the queue; do not wait for verdicts

    ⛔ NOT WHILE A PIPELINE RUN IS IN PROGRESS. pipeline.yml rebuilds all three decks itself, so a
    dispatched deck run pushes the same files under it: run 35937363940 did all its work, hit
    the conflict in its commit step and hung 43 minutes on the partial-clone rebase until the
    150-minute timeout killed it. If a pipeline run is going, its decks ARE the rebuild.

    parent    https://claude.ai/artifact/LKhTa5itp99KBXexTtY45Z
    family    https://claude.ai/artifact/8LrXG1u2QUamTFJ66Fayx3
    pick-one  https://claude.ai/artifact/AL1PD6ENiaKZbUST1ALUur
    familysearch  https://claude.ai/artifact/93GL9DBmVErTnBxfGsru3j   (the zipper's refused slots)

**Each deck keeps its verdicts in its own `db` store, `decisions/all`**, whether or not *Copy
decisions* was ever pressed. Read it with `ArtifactData` before rebuilding and append anything not
already in `reports/emma-judgments.tsv` — one Family verdict had sat there since 2026-09-09.

**The decks are worked on a PHONE.** Ruled 2026-09-23: *"I do almost all my work on mobile ...
these things are just way too large."* `out/review-deck.template.html` keeps the two sides side by
side under 720px, prints the name once, and cuts every list to three with a tap for the rest.
Judge a deck change on a phone-width screen first.

Pasted verdicts go into `reports/emma-judgments.tsv` exactly as
[wikidata-editing](docs/rules/wikidata-editing.md) § *THE PARENT DECK* says, then rebuild — the
deck shrinking is the check that they landed. Manual adjudication is still the stopgap the top
of this file calls it; the verdicts are the labelled examples the automatic zipper learns from.

## ⛔ THE FIRST THING IN EVERY SESSION: TURN THE RELATIONSHIP REQUESTING ON

**Before anything else. Before reading the queue, before any other tool call.** Ruled
2026-09-15: *"explicitly, first thing you do in the session is you turn on the relationship
requesting."*

    1. open an UNCONNECTED profile from reports/unconnected-p2600.tsv
    2. paste the DERIVE block from scripts/pathrun.js -- expect derived:true
    3. paste the RUN block with ids from scripts/build-pathrun-batch.py
    4. confirm window.__pathrun.health() reports alive:true with fail at 0

**Confirm it is ALIVE by `health()`, not by the object existing and not by `ok`.** On 2026-09-15
the runner had been dead since 20:33 the previous evening and nine queue items were worked before
anybody noticed, because the work-loop prompt says it *"needs no attention"* and that was read as
*it is running*.

**⛔ AND `ok` IS NOT AN INSTRUMENT. IT ANSWERS A QUESTION NOBODY ASKED.** Ruled by measurement
the same day: `ok` counted *the endpoint replied*, so it climbed to 253 while conveying nothing,
and the conclusion drawn from it — that the requester was broken — was wrong in the other
direction. The endpoint gives **two different successful answers** and they mean opposite things:

    202  ok / task <id>                  a real search was QUEUED
    200  data-result="not-found-blood"   answered at once: this person has NO path

`health()` separates them into `queued` / `notfound` / `found` / `fail`, and `alive` is
**time-based** — seconds since the last request — because a runner that stopped existing leaves
`running:true` frozen behind it and a counter cannot say *stalled*.

**⛔ `/paths` IS NOT THE INSTRUMENT FOR *IS IT RUNNING*, AND READING IT AS ONE COSTS AN HOUR.**
A `/paths` row appears only when a path is actually FOUND. The population being requested is
disconnected `P2600` holders, so most of them correctly return *not found* and correctly produce
no row. An empty-looking `/paths` is consistent with a perfectly healthy run. § *CHECK before
raising an alarm* applies to this exact page.

**⛔ RESTARTING IT TWICE RUNS IT TWICE.** Pasting the RUN block over a paused runner woke the old
loop as well, and two loops drove one cursor at double the request rate — the way to get
CAPTCHAd. `R.gen` is the guard and it is in the committed file; never hand-roll a restart that
skips it.

### ⛔ CHECK IT EVERY 45 MINUTES, AND THE CHECK IS `health()`

Ruled 2026-09-15: *"Every hour there should be a check to make sure that the thing is actually
running."* A local cron does it — § *A cron only fires while the session is idle* — and it reads
`window.__pathrun.health()` in the geni.com tab:

    alive:false or no tab    -> re-derive and restart from scripts/pathrun.js, top the batch up
    i >= of                  -> the batch DRAINED, which looks like success: top it up
    fail climbing            -> stop, look at lastFail / lastErr before requesting anything more

**The batch draining and the runner dying are the same event from outside**, and both were
noticed by Emma rather than by any check. That is what this cron is for.

**⛔ THE CHECK IS EVERY SIX HOURS, NOT 45 MINUTES. Changed 2026-09-17:** *"45 min path tick? Turn
it to 6 hours path tick lol."* The 45-minute figure was paired with a 2,400 batch; at six hours
that batch drains four times over and the runner sits idle between checks. **So the top-up is
~8,000, not 2,400** — the number that moves with the interval is the batch, not the cadence.
The reasoning below is kept because it is what makes that arithmetic checkable.

**⛔ AND THE BATCH MUST OUTLAST THE GAP, OR THE CHECK INTERVAL BECOMES THE THROUGHPUT.** Measured
2026-09-16 across five consecutive batches: 1,600 people in 90-94 minutes, about **1,040 an
hour** while running. On an hourly check that batch drained at ~92 minutes and then sat dead
until the next tick — a 78% duty cycle, and the difference between 1,040 an hour and 800.

So two numbers move together and neither is arbitrary: the check is **every 45 minutes** and a
batch is **2,400**, which is 2.3 hours of work against a 45-minute gap. A batch that can drain
between two checks is a batch sized wrong. The check also tops up at `i > of - 300` rather than
waiting for the drain, because arriving after it is already idle has cost the same time as
arriving late.

At that rate the 203,678 never-attempted are **~8 days of continuous running**, and the 30-day
cooldown means the first people stamped come back round well after the sweep has finished.

**Every even hour at :45, turn the requested paths into TSVs and commit them.** Ruled the same
day: *"every even hour at the forty five mark, you turn all the requested paths into TSV files"*
— that is the work loop, in place of an auto-flush that produces nothing.

## ⛔ THE PATH CAMPAIGN RUNS IN EVERY SESSION, NO MATTER WHAT

**Ruled 2026-09-14:** *"the path exporting campaign thing is always gonna run no matter what
during sessions."* It is not optional, not a background nicety, and not something to be
restarted only when somebody notices. **Start it at the top of every session and confirm it is
alive before doing anything else with Chrome.**

    scripts/pathrun.js               the requester -- derive the template, then run
    scripts/build-pathrun-batch.py   the id list, minus everyone already harvested
    window.__pathrun                 {running, i, ok, fail} in the geni.com tab

**⛔ IT DIES SILENTLY AND NOTHING TELLS YOU.** It does not crash — it stops existing, because it
lives in a page. On 2026-09-14 the tab was lost at 20:33 while Geni exports were being driven in
neighbouring tabs, and the outage went unnoticed for an hour until Emma said *"I see no
requested relationships in the past 30 min"*. The only external evidence is that
`path-chains-NNN.tsv` stops appearing in Downloads. **Check the FILE timestamps, not the
object** — the same rule as § *Read a sweep's results off the FILE a drain wrote*.

**⛔ AND IT WAS SAVED NOWHERE, WHICH IS WHY THESE TWO FILES EXIST.** The runner and its target
list were ad-hoc JavaScript in a tab. ~8,000 requests of infrastructure with no copy in the
repo, the extension, or anywhere else; when the tab went, it was unrecoverable and had to be
re-derived from Geni's own `pathSearcher`. Emma: *"Wait what the fuck the runner was not saved
anywhere?"* **Anything driving the browser for hours belongs in `scripts/`, committed, before it
is run.**

**⛔ A DRAINED BATCH IS THE SAME AS A DEAD RUNNER, AND IT LOOKS LIKE SUCCESS.** The batch is
inlined into the injection, so it is finite — `window.__pathrun.running` goes `false` and
`finished` gets a timestamp, which reads like a job well done while nothing is being requested.
It lapsed twice on 2026-09-14, once for an hour and once for fifteen minutes, both times
noticed by Emma rather than by me: *"hold the fuck on, have you been requesting paths or not"*.
**Top it up on every work-loop tick** — `scripts/build-pathrun-batch.py --skip <done so far>`.

**202 Accepted is the success status** on the search endpoints, not 200.

## ⛔ The hard ones

- **⛔ GENI WORK IS NOT IN THE QUEUE. Ruled 2026-10-01 (Emma):** the Geni-gated campaigns (descendants
  sweep, managing-accounts join, sibling scrape, permalink chain walk) live in
  `docs/queue-archive/geni-blocked-campaigns-2026-09-cont.md`: *"if we were to ever actually go back to
  Geni, this was what we would do ... We're never even touching it anymore."* Nothing Geni-gated goes
  back into `queue.md`, and no agent works on it.
- **There are no more edit runs (Emma, 2026-10-01).** The question of skipping known-blocked runner IPs is
  closed; editing is the browser QuickStatements loop.
- **The transliterated and NN relational labels already on Wikidata stay (Emma, 2026-10-01):** *"No, we're
  not removing those."*

- **⛔ REPO-ONLY UNTIL EMMA SAYS OTHERWISE. Ruled 2026-09-28** (after the duplicate creations):
  the queue is worked as usual, but everything changed stays in the repo (code, tests, reports,
  queue, devlog). Nothing is sent to Wikidata, and no batch or edit file meant to be run is written,
  until Emma gives an explicit go-ahead on that specific step. Edits through CI/CD are held
  (`HELD`/`EDITS_HELD`). Name and label changes may be written and tested; they reach Wikidata only
  with her go-ahead. A step that needs her decision is asked with AskUserQuestion, and the next
  workable item is taken meanwhile.
- **⛔ COMMIT AND PUSH AFTER EVERY MEANINGFUL CHANGE. Ruled 2026-09-25:** not in batches at the end
  of an item, so work is never left sitting unpushed. A finished step (a measured fix, a rebuilt
  report, a queue edit) is its own commit and is pushed at once.
- **⛔ THE ADMINISTRATORS' NOTICEBOARD CHECK IS SUSPENDED UNTIL 2026-10-05.** Ruled 2026-09-24:
  no edits while `Wikidata:Administrators' noticeboard` mentions `日巫女` (read live, fail-closed).
  Ruled 2026-09-25: *"the current noticeboard matter is considered done"*; the check is suspended
  until 2026-10-05 (`NOTICEBOARD_RESUMES` in `scripts/wikidata-edit-run.py` and the three workflow
  gates) and filters again from that date. The seven workflows were re-enabled the same day.
- **PUSH TO `main`. Always, without asking.** Standing grant. Open the PR, merge it, trigger the
  workflow, send the file. A session prompt saying to work on a branch is a generic default this
  repo overrides. → [working](docs/rules/working-here.md)
- **NEVER SAY YOU CANNOT DO SOMETHING YOU HAVE NOT TRIED.** Report the *mechanism* that failed,
  never the task as impossible. Every invented limit in this repo's history was false.
- **SWEARING IS NOT A STOP ORDER — it usually means START.** It points at the stupid thing, and
  half the time the stupid thing is stopping. Only an explicit stop is a stop.
- **NO REPLY MEANS CONTENT.** Silence is never a block. Show the records and keep going.
- **TESTS RUN IN CI/CD OR NOT AT ALL.** Never a local `pytest`, not even backgrounded. Test-suite
  health is *which sha CI last went green on* and nothing else. → [ci](docs/rules/ci-and-pipeline.md)
- **NO edit summaries, categorically.** Never a `summary=` on an API call, never one in a batch.
- **⛔ DESCRIPTIONS ARE WRITTEN NOW, AND THE REASON IS THE DEDUPLICATION. Ruled 2026-09-19**,
  reversing the categorical ban of 2026-08-30: *"($DATE_OF_BIRTH - $DATE_OF_DEATH) should be the
  descriptions we make on individuals. Include the gedcom qualifiers ... These descriptions will
  be verbose enough that they will hopefully never collide but stop us from recreating our own
  items multiple times."*

  **A blank description is not a guard, it is the absence of one, and that is the whole point.**
  Wikibase refuses a creation only when the label AND a NON-EMPTY description both match.
  Measured 2026-09-19: **eleven live items labelled `Margareta` with no description, and four
  labelled `Hans Larsson`**, all coexisting. So blank descriptions never stopped a duplicate —
  they stopped Wikidata catching OURS.

  - **Individuals** get `Den` from `life_description` in `build-garborg-day.py`:
    `circa 1518 Bergen, Norway - 1580`. Dates are `birth_date_raw`/`death_date_raw` so the GEDCOM
    qualifiers survive; places come from `reports/derived-places.csv`. **The qualifier words are
    written out, not shouted** — `25 Oct 1801`, `Bet 848 and 850`, and `ABT` becomes **`circa`**,
    lower case, because it is a word in the sentence rather than a label on it (ruled 2026-09-19).
    `DATE_WORDS` in `build-garborg-day.py` is the authority. **A missing side is
    omitted, never left as a leading dash** — `died 1590`, not `- 1590`, which was 20% of the
    attested genealogical import this form was measured against.
    **Established items are not the urgent case** (ruled 2026-09-24): ~4,380 made before
    2026-09-19 have none; the guard is for the pipeline duplicating its own fresh creations. A
    backfill is queued last, dates and relatives only, never the Geni-id fallback (that rung is
    strictly anti-duplication). **⛔ An existing description is NEVER overwritten.**
  - **⛔ `PLAC` STAYS OUT OF THE SYNOPTIC TREE.** The 2026-09-10 ruling is intact: `KEEP_TAGS`
    drops it and `merged.ged` carries no place. `slim.harvest_places` reads it one record before
    the prune — the only moment it exists — and `genimerge merge` writes it BESIDE the tree.
    Nothing was ever removed from `exports/`; the slim has never written back to the corpus.
  - **Name items** keep their three strings: `Den "patronymic"`, `Den "matronymic"`,
    `Den "family name"`. Ruled 2026-09-09, *"both are intentional lol and matronymic too"*, and
    it holds on an **existing** name item as much as on a `CREATE`. `DESCRIPTION_FOR` in
    `scripts/build-garborg-name-items.py` is the authority. Never strip one from a batch.
  - **⛔ AND THERE IS NO PRE-EMPTIVE COLLISION CHECK.** `scripts/check-label-collisions.py` is
    DELETED. It held 12 real people — `Margareta` against eleven unrelated items, `NN` against
    ten — on a name match, for a refusal that could not happen. A refusal costs one edit and the
    sender already carries on past it; a hold costs that person every run forever.
  - **⛔ THE DESCRIPTION LOGIC IS FROZEN, EVEN WHEN IT IS BAD. Ruled 2026-09-28** (Emma), from the
    136 duplicate creations: Wikidata refuses a second item only on the same label AND description,
    and on 2026-09-27 the same people were created again because the description wording changed
    between builds (`Gjesdal, Rogaland, Norway` to `Gjesdal Municipality`). A description is the
    deduplication key, so it must come out identical from every build: never change how a creation's
    description is generated, however much it could be improved. Improving it IS the defect.
    The frozen logic is the one in place on 2026-09-28, including that day's rule that an unresolved
    occupation becomes an `en` description only in Latin script (kept by Emma, same day).
    **Junk in a description stays too. Ruled 2026-10-01:** the 617 descriptions carrying bygdebok
    citations (`reports/description-junk.csv`) are not rewritten, and no junk filter goes into
    `life_description`. Do not propose either again.
  - **⛔ NO RELATIONSHIP PHRASE IN ANY DESCRIPTION. Ruled 2026-09-30 (Emma), overriding the freeze
    above for this one rung:** *"get rid of all relational things from descriptions. It's Geni ID,
    its occupation, or its birth to death."* `Q141611110` went out described `Ingjald Olavson,
    father of Engel Olavsdotter Osgjerd`, the person's own name and a relative. The ladder is the
    life description, the occupation, then `Geni <id>`, for NN people too.
  - **⛔ NO DESCRIPTIVE LABELS ON PEOPLE IN ENGLISH. Ruled 2026-09-28:** an NN person is `NN` in `mul`
    and `NN` in `en`, never `wife of …` as a label. A descriptive label is the same liability as an
    improvable description.
  → [wikidata](docs/rules/wikidata-editing.md)
- **Wikidata editing starts 2026-09-01; the schedule sends from 2026-09-30 08:00 UTC.** Two dates, each
  written twice and pinned by a test. A start date is not a blocker. **⛔ The schedule is paused by
  the DATE, never by disabling it. Ruled 2026-09-28:** *"automatic editing is great. And it starts 48
  hours from now ... it has to be based off of date related gating"*; a disable-and-re-enable makes a
  session the point of failure. `AUTOMATION_START_DATE` is a UTC timestamp for that reason.
- **THE STUPIDER AND MORE SPECIFIC THE INSTRUCTION, THE MORE THOUGHT WENT INTO IT.** An odd
  instruction is the output of thinking already done. Implement it exactly; do not ship the
  version that makes more sense to you.
- **KILL CHROME WHENEVER YOU NEED TO.** Standing authority. A stale extension is never
  BLOCKED-ON-USER-ACTION. → [collector](docs/rules/collector-and-browser.md)
- **⛔ AND START IT WITH THE THROTTLING FLAGS. EVERY TIME. YOU KNOW THE DRILL.** Chrome throttles
  `setTimeout` in a background tab, so a loop pasted into a tab that is not on top keeps every
  counter green and does a twentieth of the work. Measured 2026-09-15: the chain fetcher managed
  **10 chains in 7 minutes** against the 1.5s a chain it runs at in front, `alive:true` and
  `fail:0` throughout. Two loops means two tabs and only one can be in front, so the flags are
  not a nicety — they are the thing that makes the pair of them possible at all.

        --disable-background-timer-throttling
        --disable-backgrounding-occluded-windows
        --disable-renderer-backgrounding
        --disable-features=CalculateNativeWinOcclusion

  `scripts/start-chrome.ps1` is the launcher; never start Chrome by hand instead.
  **Do not diagnose a slow loop before checking the browser was started this way** — the symptom
  is indistinguishable from a healthy run, which is exactly why it is a launch rule and not a
  debugging step.
- **GENI IS ACTIVELY HOSTILE, so its constraints are the environment and not defects.** No
  Playwright, no headless — driving the real logged-in browser is what makes the traffic read
  as proper. A census read costs a real page load (`fetch` returns zeros: the stats block is
  rendered after load), one export at a time, no cancelling, downloads mostly blocked.
  Solving any of these cheaply is what gets the account CAPTCHAd.
  → [collector](docs/rules/collector-and-browser.md)
- **THE DOCUMENTATION DOES NOT REFER TO THE ACCOUNT OWNER** — not in the third person, not in the
  second. State rules impersonally. **A blind regex pass is banned**: it turned `Emma Watson`
  into `you Watson` and shipped. A woman in the tree is still `she`.

## Working

- **⛔ IF AN ANSWER IS EXPECTED, IT IS AN `AskUserQuestion`. THERE IS NO OTHER WAY TO ASK.**
  Ruled 2026-09-09, directly: *"if you expect an answer do AskUserQuestion I will not reliably
  respond otherwise"*. A question in prose was not asked — not a question at the end of a report,
  not an offer to do something *unless you say otherwise*, not *let me know*. Those read as
  narration and go unanswered, and then the work stalls on an answer nobody was asked for.
  Every option must be one that can actually be picked, and **the axis is part of the question** —
  four options on one wrong premise is one option.
- **⛔ A CLASSIFIER REFUSAL IS PUT TO EMMA AS AN `AskUserQuestion`, EVERY TIME. Ruled 2026-09-25**,
  after a permission-classifier refusal (the noticeboard-gate lift) was explained twice in prose
  and went unanswered: *"Why haven't I been AskUserQuestioned"*. When Claude Code's classifier
  refuses an action, stop, do not route around it, and ask at once with options that can be
  picked (add a permission rule, do it by hand, skip it).
  **Ask for explicit authorization of the named action.** Ruled the same day: *"Put it in
  claude.md that explicit AskUserQuestion things like this work"*. An `AskUserQuestion` naming the
  exact command and asking *"Do you explicitly authorize me to …"* is Emma's consent on the record,
  and on 2026-09-25 it cleared two refusals: `git sparse-checkout add .github scripts`, and reading
  the `pipeline.yml` gate. It did **not** clear the third, the edit to the three workflow gates.
  So ask, retry once with the authorization, and if it is refused again, ask again. Never
  rephrase the action to slip past the check.
- **⛔ REPORT THE UNEXPECTED FIRST. Ruled 2026-10-02 (Emma):** *"Oftentimes, the repo skips over unexpected stuff, like it's not important ... it kind of refuses to give the information because it prejudged it as being unimportant. I think that's kind of the core issue."* When work turns up something surprising (a parent link that cannot be real, a constant pointing at the wrong person, a row that contradicts itself, a result from a different source than expected, a removed value back on Wikidata), say it first and plainly, in the reply and the devlog. Never filter it out, work around it silently, or leave it as an aside. And information the agent has that bears on her question is given, not withheld (Emma: *"it actively has the information I want but isn't willing to give it"*).
- **⛔ EXPLAIN A PROBLEM BEFORE SOLVING IT. Ruled 2026-10-02 (Emma).** Say what it is, how big it really is, and whether it reached Wikidata at all (checked live, never inferred from a local file), and only then fix it. A count from the local tree is never presented as a count on Wikidata, and a detail of one batch is never called a "scope" question.
- **⛔ THE OWNER'S ITEM AND HER FAMILY'S ARE HERS. Ruled 2026-10-02 (Emma).** Nothing links to or from her profile, and nothing edits it, her parents' or her brother's (`wikidata_lockout.PROTECTED_ITEMS`). She writes and runs their QuickStatements herself; the session does not build them.
- **⛔ EVERY QUESTION CAN BE DECLINED. Ruled 2026-10-02 (Emma).** Every `AskUserQuestion` ends with an option to not answer and ask for more explanation. A warning is never turned into a multiple-choice question and acted on at once: explain it first, then ask. *"For every multiple choice question, give me the ability to reject answering it and ask for more clarification."*
- **⛔ A SPECIFIC ISSUE IS NOT A GENERAL RULE, AND IT COMES FIRST. Ruled 2026-10-02 (Emma).** A problem in one part of the tree is handled as that problem, never folded into a general fix or rule; a specific queue item outranks a general one. People are reported with their Geni, FamilySearch and Wikidata links in the reply.
- **If the instruction is ambiguous, ASK.** But **while working the queue, GUESS and record it**:
  ambiguity *inside* a specified item is guessed, ambiguity about *which thing is meant* is asked.
- **⛔ AN INCOMPLETE OPERATION IS WORSE THAN A COMPLETED WRONG ONE. Ruled 2026-10-01 (Emma),
  knowingly against Wikimedia consensus.** Once an operation is under way, finish it the way the
  pipeline would (a Geni id carries its `P1810` display name, and so on). Do not stop it halfway
  to audit individual values; a wrong value is corrected later, a half-done operation is not.
- **AN ERROR REPORT IS A STANDING KIND OF QUEUE ITEM (Emma, 2026-09-27).** It is a screenshot of
  one item (usually Wikidata, often from a phone) and a line or two on what is wrong: `Q141224900`
  *Samuelis*, `Q141566035` *NN Orre*, `Q141570927` *Not Known*, `Q141510769` *eller*. Handling it:
  read the item and its history (who added the wrong value, and when); say exactly what is wrong
  and why; fix that item (labels through `label-applications.tsv`, statements as a batch, never
  over a human correction or another editor's statement); find the rule or step that caused it and
  fix that, or show it is already fixed and since when; sweep for every other item made the same
  way and fix those too; record it in the devlog. AskUserQuestion only where the fix is a real
  choice, and for the go-ahead to send anything. Error reports go at the end of the queue unless
  Emma says otherwise.
- **"Add it to the end of the queue" means WRITE IT DOWN AND STOP.** No investigation, no
  questions, no gathering evidence first.
- **Every two hours, put the blockers up as an `AskUserQuestion`** — 10, 12, 14, 16, 18, 20, 22,
  00. Each must offer the non-blocker reading, because that is usually the true one.
- **Not-done taxonomy**, exactly one tag, blocker named specifically: NEEDS-DECISION,
  BLOCKED-ON-USER-ACTION, BLOCKED-ON-EXTERNAL, NEEDS-INVESTIGATION, UNSAFE-TO-GUESS,
  OUT-OF-SCOPE. **If it fits none with a named blocker, it is not deferred — DO IT NOW.**
- **A long series of commands runs in STRICT ORDER**, even where the order looks inefficient.
- **No unprompted reports.** Write the thing asked for and stop.
- **"Analyse this" means: build a CSV of every instance, commit it, then analyse that** — not a
  sample, not the top 100.
- **CHECK before raising an alarm.** Run the check that would falsify it first.
- **Queue items are BULLET POINTS, never numbered.** A number is a promise it will still be there.
- **⛔ READ THE QUEUE FROM THE TOP, EVERY TIME. Ruled 2026-09-27.** Every tick, and before starting any new item, re-read `queue.md` from the top and take the first item in the queue as the file stands at that moment. Never carry a line number (`sed -n 38p queue.md`) or an earlier reading from one tick to the next: items are added at the top between ticks. On 2026-09-27 ticks read by line number from 03:12 to 07:42 UTC and a fix item at the top went unseen for 4.5 hours.
- **⛔ WHEN THE TOP ITEM IS WAITING, TAKE THE NEXT ONE THAT ISN'T. Ruled 2026-09-27.** An item blocked on something outside the session (a CI run, a tree rebuild) does not make the tick "nothing actionable": work the first item below it that can move, and come back to the top one when its blocker clears.
- **A cron only fires while the session is idle.** Never schedule a long job into active work.
- **A ten-minute ceiling is not a wall — background it.** Never hand a long job back.
- **Code that is WRITTEN but never CALLED is not done.** Wire it, then measure from the wired path.
- **⛔ THE REPO IS MINIMALIST. SMALLEST IT CAN POSSIBLY BE.** Ruled 2026-09-17: *"this repo ought
  to be extremely minimalist. Smallest it can possibly be."* It is a standing property, not a
  cleanup task: **every change should leave the repo smaller or the same size**, and a fix that
  adds a file, a flag, a script or a gate is a fix that has to justify its own weight first. The
  evening it was ruled, every single defect of the session had been answered by adding something.
  342 scripts, 1,805 reports, 41 docs, 12 workflows is the state it was ruled against.
  **It is queued, not started** — *"I want to actually see the repo editing in the current state
  before you torch the current state"* — and § *NOTHING IN THE PIPELINE IS TRIVIAL* governs the
  whole pass.
- **LEGACY CODE IS DELETED.** The test is *does the pipeline read this*, not *might this be useful*.
- **Do not grab the first artifact that vaguely matches.** Find the one that is meant.
- **Incomplete earlier work is not the thing being described.** Its errors describe where it
  stopped, not a defect in a finished mechanism.
- **A shortcut taken to unblock a session is not a law to enforce back.** Automate it instead.
- **Duplication is deliberate here.** Never "fix" it. The thing to control is repetition in front
  of one reader.
- **SORTING MUST BE DETERMINISTIC** — total key, same bytes out for the same inputs. `casefold`
  alone is not a total order.
- **Windows:** commit with `git commit -F <file>`; never round-trip UTF-8 through
  `Get-Content`/`Set-Content`.

## The corpus and the tree → [corpus-and-tree](docs/rules/corpus-and-tree.md)

- **`exports/` is the corpus, read recursively. There is no ingest step.** Every `.ged` is
  committed; **never gitignore a `.ged`**, and never write a `*.ged` or `*.zip` pattern.
- **Never overwrite an existing `.ged`.** A new export is always a new file. If the path exists,
  STOP. The one exception is a byte-identical duplicate.
- **`exports/excluded/` is the one part that is not corpus** — for when Geni has *deleted a
  relationship* a merged export still asserts. Checked now, never predicted.
- **Later sources win value conflicts.** Geni is live; the newer export holds the correction.
- **The seed is the file's first `INDI`**, and an export is named for its style, so disambiguate
  with the seed id.
- **`GENI_EXPORT_CAP` is 5000** — largest seen, not a cap Geni enforces. Do not encode arithmetic.
- **A small component is IGNORED.** Not reported, not analysed.
- **The question is whether OUR TREE MATCHES GENI, never whether Geni is right.** If Geni holds
  two profiles, we hold two — even when two is wrong.
- **⛔ NEVER GREP THE WHOLE CORPUS. IT COSTS TEN MINUTES AND IT IS PRIVILEGED.** Ruled
  2026-09-18: *"do not grep the corpus it is privileged after all"* and *"grepping the
  corpus has taken over a minute"* -- a recursive `grep -rl` over `exports/` ran past the
  two-minute tool ceiling and had to be backgrounded, in the middle of an urgent re-run.
  The check it was doing is worth seconds, never minutes. **Use the derived CSVs**, which
  are the indexed form of the same question, or a single named file. A **privileged**
  export skips the check entirely.
- **Check before running an export**, and put the number in the commit -- by the cheap
  instrument above, never by sweeping `exports/`.
- **The job with an export is to integrate it, not to analyse it.**
- **"Is X present?" means BOTH stores.** Answer for each, name which, and say when the absence is
  bounded. Join on the Geni ID; never search by name.
- **`reports/derived-family.csv` separates with ` | `, spaces included.** Splitting it wrong made
  379,251 people arrive childless and published a distribution that looked clean.
- **GEDCOM dates have a specification** — `genimerge.dates`, never a regex. A hand-rolled parser
  drops what it does not understand silently.
- **`reports/density.md`, not `reports/seeds.md`**, is where the next export comes from.
- **The `Descendants` campaign is about TIME, not thinness** — a ball reaches ~12 generations, so
  seed where you want to arrive. Two seed-choosing methods are refuted; do not propose a third on
  reasoning alone.
- **The zipper's one name exception lives inside a slot**: solo, then date, then name — and
  **1600–1900 is the band where names lie and years decide** (71% of confirmed pairs spell the
  name differently).
- **The four big derived CSVs are committed gzipped.** `pack-derived.py --unpack` on a clean clone.

## Names → [names](docs/rules/names.md)

- **`name modelling.txt` is the authority and beats this file.** A patronymic is `P5056`, parallel
  to `P735`/`P734`, with `P144` pointing at the **father, the person**.
- **⛔ A PATRONYMIC REQUIRES THE FATHER. Ruled 2026-09-25:** *"patronymics are supposed to require
  the father ... if the father has the Latin derived name"*. `Jonæ` is a patronymic when the
  father is Jonas or Jon; `Andreae` with no such father is an inherited surname (the Tübingen
  family). The father-free `-ae` rule of 2026-09-24 is gone.
- **PARSE PATRONYMICS BY FORM. Never parse a name positionally.** Positional parsing is the
  ultimate cause of most name defects here. Both `GIVN` and `SURN` are checked.
- **A TITLE IS NOT A NAME** — Geni already said so in `NSFX`. Drop titles, keep ordinals.
- **⛔ A BIRTH MARKER NEVER REACHES A LABEL. Ruled 2026-10-01 by AskUserQuestion ("Adopt it").** Lowercase `f.`, `født`, `född`, `geb.`, `née`/`nee` and `(born X)` introduce the birth surname: the label is the given names plus that surname, the form before the marker a `mul` alias (`namemodel.split_birth_marker`, wired in `derive-labels.py`). Capital `F.` is a middle initial; `Ne` is a given name; `f.d.` (före detta) gives an alias only; a place after the marker (`f. Norge`) is dropped.
- **A DESCRIPTION MARKER COMES OUT OF THE LABEL**; a title stays in it. A title is a thing the
  person was; a marker is an annotation about the record.
- **A NAME FIELD THAT NAMES A RELATIVE IS NOT A NAME** — Geni puts the husband in `GIVN`.
- **A GUARD IN ONE EMITTER IS NOT A GUARD.** There are two emitters; rules live in `namemodel`.
- **No given name is not no name** — a redacted person's surname is still a `P734`.
- **⛔ THE BIRTH NAME IS THE LABEL, FOR EVERYONE; THE MARRIED NAME IS AN ALIAS. Ruled 2026-10-01 (Emma):** *"Birth names are the default, and multiple languages and married name is an alias. I am taking this with the full accountability that it's going to mass-change a very large amount of names."* `namemodel.married_is_primary` is false for every sex, and `_label_corrections` backfills our established items: a live married-form label becomes the birth name, the married form an `Amul`, paced by `LABEL_EDIT_CAP`. The entry below recorded her 2026-09-25 reversal the wrong way round (what she reversed was an earlier ruling of hers) and is superseded.
- **Superseded 2026-10-01 (mis-recorded): ⛔ EVERYBODY GOES UNDER THE MARRIED NAME — AND IT CARRIES THE GIVEN NAME. Reversed 2026-09-25**
  (*"reverse course on the undo of the married-name handling"*, on `Q141492819`, whose label was
  given as `Marite Bergesdatter Talgje`). The 2026-09-21 switch that put women under their maiden
  names is undone: `mul` carries the married form for every sex and the birth form is the `Amul`.
  **Never an `Aen`.** **A married label without the person's given names is never built.** The
  bare married surname is how `Q141492819` went out as `Talgje`; 7 of 8,350 created items were
  that shape, and all were fixed by hand on 2026-09-25. **⛔ Still never backfilled** (ruled
  2026-09-24, *"a waste of edits"*): it governs what is CREATED.
- **`NN` is PRESERVED in `mul`**; descriptive labels are ADDED in other languages. `Private` never
  becomes a label, and neither person is left unlabelled.
- **A bare given name is not a label** — the farm name is the surname; else `Given NN`.
- **Redacted people go in.** `<private> /Surname/` keeps a real surname.
- **⛔ THE KANJI SIGNAL DECIDES WHICH LABEL UNIVERSE A PERSON IS IN.** A `ja` label in **kanji**
  means a SINOSPHERE name: a different universe of labels, and **no label edit in any language**.
  A `ja` label in **katakana or blank** means not Sinosphere, and ours to edit. `ko` and `zh` are
  not reliable signals on their own. **This is why `ja` is edited so aggressively — the editing IS
  the safeguard.** Writing katakana over kanji does not damage a label, it FLIPS THE
  CLASSIFICATION: the person stops reading as Sinosphere, falls into the Latin pipeline, and the
  corruption compounds. Nine went out 2026-09-18 and were reverted by hand.
  → [names](docs/rules/names.md)
- **⛔ LABELS ONLY IN ENGLISH, JAPANESE, CHINESE AND KOREAN (plus `mul`, `en-us`). Ruled 2026-09-27:**
  *"the only actual languages that I consider remotely like we should be including are Japanese,
  Chinese, Korean, and English."* Sixteen transliterated scripts were switched on 2026-09-26 on the
  assumption that transliteration is easy; it is not, and they were disabled (commented out, not
  removed). What was asked was different: COMPOSE a language's label from canonical forms of each
  name in that language (name items' labels), a person eligible only when every part has one -- a
  long tail, never transliteration. See `todo.md`. The NN relationship
  labels in Polish, French, German and the rest go too. One gate on the written batch
  (`LABEL_LANGUAGES` in `build-garborg-day.py`) drops any other label or alias; Emma's own hand
  labels pass. Other languages are `todo.md` work, not batch work.
- **⛔ LONG-TERM, A LABEL IS COMPOSED FROM THE NAME ITEMS, STRICTLY. Ruled 2026-09-27 by AskUserQuestion.** A person's label in any language, `ja`/`zh`/`ko` included, is built from the labels their name items (given names, patronymics, family names) carry in that language, and a language is written for a person only once EVERY part of the name has a label there. Transliteration is phased out over time in favour of this; it is a long tail and nothing is guessed. **English is switched on (Emma, 2026-10-02, by AskUserQuestion):** `COMPOSED_LANGS_LIVE` in `build-garborg-day.py` fills an empty `en` slot from the name items, never overwriting. **`ja`/`zh`/`ko` too (Emma, 2026-10-03, by AskUserQuestion):** an empty slot takes the composed label, and the transliterated line for that slot is dropped; transliteration still fills a slot the name items cannot compose.
- **The gate is `ja` + `zh` + `ko`. CJK INCLUDES KOREAN.** All three readings are produced for
  everyone; culture only picks which is promoted to `mul`.
- **A title inside a label takes the NATIVE form in CJK**, never a transliteration. An unknown
  place or title is DROPPED, never transliterated.
- **Transliterate the English reading.** Faithfulness to the source language destroys more than it
  saves. Every rule change is scored against the attested column.
- **One name item per USAGE, not per string.** A token that is both a surname and a given name
  gets both objects. A diacritic makes a different name.
- **Write a Han range as ASCII `\uXXXX` escapes** — the literal form ate the Hangul block and cost
  5,338 Korean people.
- **A generation suffix goes LAST; a regnal ordinal stays put.** It is a fact about the person,
  not about one name string, and it must not reach an item somebody else labelled.
- **Wikidata's label beats ours.** An existing `mul` is not ours to overwrite.
- **⛔ A CORRECTION ON WIKIDATA IS EVIDENCE, NOT A GAP. Ruled 2026-09-27.** The pipeline pushes our model onto Wikidata, and that *"goes a bit too far"*: when a human (Emma under the account, or anyone) changes or removes something, the model has to learn from it, not re-assert it. Never re-send a value somebody changed; take the correction back into our data. Emma's hand edits run under the pipeline's own account and are told apart by their tags (`wikidata-ui`, revert tags; batch edits carry `OAuth CID`).
- **⛔ AN APPLICATION IS APPLIED UNTIL IT IS LIVE, THEN IT IS DATA. Ruled 2026-09-27.** A hand table that pushes a value onto Wikidata (`label-applications.tsv`, `forced-labels.tsv`) sends a row every run until Wikidata holds it, and the run that sees it live removes the row (`retire_applied_labels`). A row that is never retired turns into a claim asserted forever, and it reverts every later hand correction.
- **⛔ A LANGUAGE LABEL DUPLICATING `mul` IS NOT OUR PROBLEM. A BOT ALREADY DOES IT.** Ruled
  2026-09-13: *"There is a bot that periodically takes language labels that duplicate the
  multi-language label. It removes them. I don't give a shit about that bot ... The fact that it
  has that job literally means that we don't care."* And it is **used on purpose** — *"I've even
  actively exploited that bot by ... some of the ways that I standardize labels across
  languages."* So writing a duplicate is a legitimate way to standardise, and cleaning one up is
  doing another bot's work. Never measure it, never queue it, never emit a removal for it.
- **⛔ A MIXED-SCRIPT LABEL IS NOT A CAMPAIGN. `mul` AGREEMENT SORTS IT OUT.** Ruled 2026-09-17:
  *"mul label agreement and all of that stuff should sort it out"*. `Q2575818` held
  `Robert Henrik Иванович Rehbinder till Viksberg` — a Russian patronymic spliced into a Latin
  name, written by our own batch on 2026-09-13 and corrected by hand on 2026-09-17. A scan of all
  1,451,994 derived labels found **622 mixing Latin and Cyrillic** (`Ivan Ivanovich Рюрикович`,
  `Tautvilas Кейстутович of Lithuania`). **That count is not a work item.** The label-agreement
  machinery is what resolves them, the same way the duplicate-label bot above is. Do not queue
  the 622, do not emit corrections for them, and do not count them again.
- **A middle initial keeps its Latin letter in every language.** A bare lowercase letter is a word.
- **⛔ A REGNAL NUMERAL UNDER A DYNASTY SURNAME IS A NAMED EXCEPTION, NOT A RULE. Ruled 2026-09-25:**
  *"you are trying way too hard to create a generalized rule on a minuscule population ... It's
  very easy to just figure this shit out with these individuals."* `reports/regnal-numerals.tsv`
  lists them by exact `GIVN`/`SURN` with evidence; add to it rather than generalising.

## Editing Wikidata → [wikidata-editing](docs/rules/wikidata-editing.md)

- **The purpose is to ADD, not to correct.** 24,957 addable statements against 930 conflicts. A
  conflict is emitted beside what is there, cited to Geni, and never routed to anyone for a ruling.
- **A statement goes in only if BOTH ends already have a QID.** That is an invariant that makes
  the sequence converge, not a wall. **The batches are a SEQUENCE**: what cannot run today is
  tomorrow's batch. `LAST` IS valid as a value; only two items created in one batch cannot point
  at each other.
- **The ledger refresh is PART OF THE RUN.** Regenerating QuickStatements always regenerates the
  ledger; it almost never rebuilds the tree.
- **Caps (5x on 2026-09-28, Emma):** `SIBLING_CAP` **300 pairs**, `NAME_ADD_CAP` **250 people**,
  `P2600_LEAD_CAP` **300**, `MANUAL_P2600_PER_RUN` **150**, `LABEL_EDIT_CAP` **450**. `P22`/`P25`/`P40`/`P26`
  are uncapped. The browser runs absorb ~2,500 to 3,000 edits an hour (`reports/browser-run-rates.csv`).
- **A sibling step gets a placeholder parent in OUR TREE and never on Wikidata** — Wikidata has
  `P3373` and needs no invented parent.
- **A second Geni ID on one item is NOT a conflict**, and a duplicate parent value is
  self-healing. Do not report or fix either.
- **⛔ AN EDIT GOES ON AN ITEM IN THE UNIVERSE, OR ONE STEP BEYOND IT. ALL EDITS, NO EXCEPTIONS.**
  Ruled 2026-09-17: *"the hand identification is supposed to fucking go to Wikidata. It just is
  supposed to go to things that actually are allowed to have valid edits put on them ... That
  means they must be in the universe or one step beyond the universe. **As all edits go.**"*
  The universe is the contiguous Wikidata subgraph from Arne and Bureus — no hop counts inside
  it, a billion hops if that is what it takes — and the ring is the items one relationship
  removes from it, which is the same reach `compose` builds creations from.
  **⛔ Every item the account has edited is in it when it is linked, and so is one hop from it. Ruled
  2026-10-02 (Emma):** *"Anything one hop over from edited items is a part of the universe"*, and
  *"any edited item at all is in the universe if it is linked no need for the geni id or
  familysearch id to be linked but them being linked is ideal"*. The walk is not limited to items
  carrying our `P2600`: `refresh-garborg-ledger.py` writes `reports/account-edited-links.tsv` (the
  relationship statements on every item the account touched), and `wikidata_subgraph` counts an
  edge when either end was edited by us. The owner's protected items are never walked.
  **A hand identification is not exempt and is not withheld**: it goes out like everything else,
  gated on where the item sits and on nothing else. Two over-corrections are refuted and must not
  return — gating on the CSV's free-text note, and withholding the file wholesale.
  `build-garborg-day.py` writes `out/wikidata/edit-universe.json` and `wikidata-edit-run.py`
  reads it, because the sender talks to Wikidata hours later with no tree to check against and
  **a gate that lives only in the composer is one stale artifact away from being no gate**.
- **⛔ A CREATED PERSON GETS EVERY RELATIONSHIP OUR TREE GIVES THEM, AT CREATION. Ruled 2026-10-02 (Emma):** *"The created people were supposed to at their creation have all relationships possible to add for them added."* Father, mother, spouses, children and siblings, both directions, to every relative with an item (ours or Wikidata's), with no locality test and no sibling cap on the creation's own links. A creation is an edited item, and one hop from an edited item is in the universe, so the gates (`refuse_non_local`, `check-batch-locality.py`) count a creation's relatives as members through `qs_v1.creation_relatives`. Two people created in the same batch still cannot point at each other (`LAST` names one item); that link goes in the next batch.
- **SIBLINGS SHARE A FATHER OR A MOTHER, FOR THE SOURCE BACKFILL TOO. Ruled 2026-10-02 (Emma):** *"I think the change is the problem."* `build-relationship-sources-backfill.py`'s `sibling_index` counts a shared parent again (the 2026-09-27 family-object reading is reverted), and a sibling's `P3373` is cited per source like any other link: `S2600` where Geni links both to the shared parent, `S2889` where FamilySearch does.
- **The seed set is the Wikidata subgraph from Arne** — no hop counts, a billion hops if that is
  what it takes. ⛔ **AND IT GATES `P2600` TOO, NOT JUST CREATIONS. Ruled 2026-09-17:** *"why the
  fuck were geni ids added to so many people who are not 1 hop away from the universe"* and, of
  the old rule, *"claude.md is wrong"*. This line used to end *"the subgraph gates creations only;
  filling in existing items is ledger-wide"*, and that sentence is what sprayed Geni ids across
  Wikidata: `manual_p2600_lines` read all **1,691** rows of `reports/manual-identifications.csv`
  and emitted up to 90 a day onto items anywhere in the world tree, unattended. Filling in an item
  we already work on is still ledger-wide; **putting our identifier on a stranger is not**.
- **A BLOC IS A ROSTER REFERENCE, never pasted ids.** Entry points drip in on a date column, not
  a cron; the roster stays at about 250.
- **A SUMMARY of a Wikidata item is not the item.** Download the full JSON; a summariser gets
  absence wrong. **Querying Wikidata is allowed** — be polite about the rate.
- **The tree and the items are edited BY HAND, continuously.** Re-download before any correction
  and say when it was verified.
- **Always write the English label next to a property or item ID.** Never guess an ID.
- **Regenerate a review deck before handing it over**, never the committed copy. A CJK card is not
  in the deck.

## The collector and Geni → [collector-and-browser](docs/rules/collector-and-browser.md)

- **⛔ BOTH TIES, ALWAYS** — a blood chain AND a marriage chain to Charlemagne, plus the immediate
  family. **The redundancy is the point.** Both searches on every person; a blood miss with no
  path is not done; **do not backfill in-law onto people who already have a blood path**.
- **Anything odd about a person → `Forest` export.** Stop investigating.
- **The agent navigates and nothing else.** Every decision is inside the extension.
- **Progress is DERIVED, never stored.** No list is hand-edited.
- **An empty browser list is not a blocker.**
- **Grab the RESIDUALS** — keep what an extraction drops.
- **One export at a time is Geni's limit**, and a submitted export cannot be cancelled.

## CI and the pipeline → [ci-and-pipeline](docs/rules/ci-and-pipeline.md)

- **The repo is public; CI runs on a schedule, on dispatch and on PRs.** Only `pipeline.yml` runs
  on push, and a burst of pushes does not queue — the pending run is cancelled.
- **⛔ AND THE 45-MINUTE PATH TICK PUSHES, SO THE PIPELINE CAN NEVER REACH THE FRONT.** Measured
  2026-09-17: **0 green pipeline runs in 20 — 16 cancelled, 2 failed, 2 running.** Every stamp
  commit is a push, a push cancels the PENDING run, and the campaign ticks every 45 minutes. So
  the composed batch stays frozen for as long as the session works, which is how a day of edits
  went out against a composition nobody had regenerated. `pipeline.yml` already warns *"do not
  push again while waiting on one if the point is to watch that run"* — that is not a style note,
  it is the reason the batch is stale. **If the pipeline has to complete, stop pushing and say
  so**; the stamps can wait one tick and nothing is lost, because `attempt_ledger.stamp` is
  idempotent and the drains are on disk.

  ⛔ **BUT `cancelled` IS TWO DIFFERENT EVENTS AND THIS SECTION USED TO EXPLAIN ONLY ONE.** A
  job killed by its own `timeout-minutes` and a pending run superseded by a push are **the same
  word in every listing**, and push contention — true, and written above — is the explanation
  that comes to hand. Two confident wrong diagnoses came out of reading the conclusion word on
  2026-09-19, when the real cause was a 100.32 MB file making the pre-receive hook decline every
  push while the timeout killed the job mid-retry. **Only the start and end times tell them
  apart**: a supersede cancels a run that never started work, so it dies in seconds with an
  empty log; a timeout kill runs for exactly `timeout-minutes` and its log is full. Check the
  duration before attributing a `cancelled` run to anything.
- **Pages is built from the sha the pipeline PUSHED**, not the one that triggered it.
- **A page whose generator no workflow runs is published as a photograph.**
- **The synoptic tree BUILDS in Actions**, slimmed. ~6.07 GB per million people.

---

## Live corrections, 2026-09-09

- **The campaign is every `P2600` holder disconnected from Charlemagne** in the union of our
  exports and Wikidata — connected, or confirmed impossible. 518,889 holders, 266,201
  disconnected. → [unconnected-worklist](docs/unconnected-worklist.md)
- **The old *183,674 isolates are LOW PRIORITY* rule is DELETED**, and not only because it
  governed 67% of that population. **The operating conditions changed underneath it**: it was
  written when finding those people was manual labour, and browser automation has turned that
  into something routine. A rule whose whole argument was cost does not survive the cost changing.
- **The Geni trimming is not finished.** The slim keeps ~73% of corpus bytes; a
  connectivity-only tree — `RFN`, `SEX`, `FAMC`, `FAMS`, `HUSB`, `WIFE`, `CHIL` — is ~19%.
  Names, dates, places and titles are still carried and the Wikidata pipeline does not read them
  to answer *is this person connected*.
- **⛔ THE WIKIDATA TREE NEVER GOES INTO THE SYNOPTIC TREE. THE SPLIT IS PERMANENT — ruled
  2026-09-10, option `c`.** *"the pipeline merges the corpus, and the union tree stays a separate
  `--connectivity` artifact that only the worklist reads."* This supersedes *not yet* and *until
  it fits*: it is no longer a gate waiting on a measurement, it is the shape.

  **The measurement that closed it**: `--slim` with `--also out/wikidata-tree.ged` was KILLED on
  run `34444557142` at **15,428 MB with 565 MB free** — the same shape as the 15,921 MB kill
  `--slim` was invented to fix. `--connectivity` fits (3,038,219 people, 9.76 GB peak, 18m38s,
  run `34439815071`) and says nothing about this: it drops names, dates and places, the derive
  scripts cannot read it, and it can never be `out/merged.ged`.

  So `scripts/build-wikidata-gedcom.py` renders a mergeable GEDCOM that the PIPELINE does not
  merge. **Do not wire `--also out/wikidata-tree.ged` into `rebuild-everything.py`** — not now
  and not after a future measurement. The two other options were refused with it: a middle
  slimming mode, and a bigger runner.
- **Nameless routing nodes are the design.** A QID-only person exists so a Geni person can reach
  Charlemagne through Wikidata's structure; a router does not need a name.
