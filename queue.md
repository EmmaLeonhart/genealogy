## THIS IS THE `name-development` BRANCH — Emma, 2026-08-18

**This checkout is not the one doing the Geni exports.** Emma split the work after the
export session spent a day doing two jobs badly at once:

> *"there was a bit of a conflict with that session going all ADHD with trying to perform
> two tasks at once. It was trying to do a combination of Geni exports that were occurring
> about every — and doing name work — and not being able to do either one."*

- **Directory:** `GitHub/name-development`, a fresh clone. **Branch:**
  `name-development`, off `main`. The original checkout at `GitHub/geni` belongs to the
  export session and is not touched from here.
- **NO exports and NO browser work of any kind.** *"you do not do any browser activity of
  running exports from individuals, because that's the job of the other session."*
- **NO Wikidata runs.** The standing 1 September rule holds; asked directly, Emma:
  *"Yes, of course it doesn't run!"*
- **The export-slowness item below does not apply to this branch.** Her words, asked
  directly: *"In this branch that you are making, it is resolved. There are no exports
  whatsoever. You are doing the name stuff and other things like that that it was getting
  distracted by."*
- **Commit and push to `name-development` constantly. NO pull request** until the export
  branch has finished what it is doing: *"There is a pull request once the other branch is
  done with all the shit it's doing with the Geni exporting."*

**Note for whoever reads this on `main` later:** the branch was cut at `7ad0596` and
`main` moves under it with every export round, so expect the eventual merge to be a
reconciliation, not a fast-forward.

*(`git push` over HTTPS returned HTTP 500 for this repo on 2026-08-18 and the branch ref
had to be created with `gh api ... git/refs` instead. If a push fails that way again, that
is the workaround, not a reason to stop committing.)*

## ⛔ TOP PRIORITY — the export slowness. NOTHING ELSE RUNS — Emma, 2026-08-18

*"figuring out this download stuff is the top priority of this entire thing. It is THE
top priority. You should not be doing any other work."*

**Exactly one thing may interrupt it**, in her words: *"downloading an exported GEDCOM,
then creating a new individual and exporting from there, because that is time-dependent."*
Everything else in this file waits behind this item, including the name work, the label
batches and the marker fixes.

### The measurement, and what it is made of

**The data is the session transcripts**, `~/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl`.
Every tool call and every result carries a UTC timestamp, so they *are* the log of when
each export was requested and when its page was next seen. `scripts/measure-export-build-times.py`
reads them; `reports/export-build-times.{csv,md}` is the output.

Two earlier attempts were worse and should not be revived: timing from **file mtimes**
(`measure-export-throughput.py`) is biased because a late download makes the next build
look short, and matching a page's text to **every** task id in the message attributes one
poll's state to other open tabs.

| day | exports | Geni build ≥ | cycle | latency here | exports/hour |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026-08-17 | 53 | 4.2 min | 8.0 min | 3.8 min | 7.5 |
| 2026-08-18 | 8 | 3.5 min | 12.3 min | 8.8 min | 4.9 |

**Geni is not slower. It is slightly faster.** Build times fell 4.2 → 3.5 min median and
the worst case fell 9.8 → 6.1 min. Size does not explain it either: `r = 0.13` against
megabytes, and today's files are *smaller*.

**The lost throughput is latency on this side** — 3.8 → 8.8 min per cycle, from running
multi-gigabyte scans and batch regenerations between polls. That is the whole difference.

### SETTLED by Geni's own emails — it was me, not Geni

109 server-side "export is ready" emails, `reports/export-ready-emails.txt`. Independent
of every log on this machine, which is why Emma suggested them.

| window | what was being done | median gap | rate |
| --- | --- | ---: | ---: |
| 08-17 16:00 - 08-18 06:00 | running the loop | 9.2 min | 6.5/hr |
| 08-18 06:00 - 09:30 | running the loop | **6.9 min** | **8.7/hr** |
| 08-18 09:30 - 18:30 | name censuses, marker fixes | **60.2 min** | **1.0/hr** |
| 08-18 18:30 onward | back on the loop | 12.3 min | 4.9/hr |

Build time itself, submit to ready email, was **3.8-6.4 minutes today** — the same as
yesterday. **Geni never slowed down.** Throughput fell 8.7/hr to 1.0/hr exactly across
the window spent on other work and recovered on returning to the loop.

So the cause is not rate limiting, not the server, not file size, and not the power cycle.
It was doing other work between exports. **Plan B is NOT triggered** and stays unbuilt.

**The operating rule from this: while the loop runs, nothing else runs.** No background
scans, no batch regeneration, no analysis. Poll, download, seed, export.

### Still to do on this item

- **Corroborate against Geni's own emails.** Her suggestion: *"I get emails saying when
  the downloads are finished. I might even get emails saying when the export starts."*
  That is a server-side timestamp, independent of anything measured here, and it settles
  the question rather than resting on my own logs.
- **Poll tightly and run nothing heavy in parallel** until throughput is back near 7.5/hour.

### Contingency — Plan B, NOT started, and only if rate limiting turns out real

Her design, recorded because it was dictated and must not be reconstructed from memory.
A fourth dataset beside Wikidata, Geni, and order.life: **the Geni page scrape**.

- Per individual: open their page, **open the relatives section** — the links are not in
  the DOM until it is expanded — and whatever else needs clicking, then save the page.
- Save into **`geni-scraping/`**, *not* `geni_pages/`.
- Capture: their name, whatever data the page shows, and **every relative shown in the
  relatives tab — siblings, parents, spouses — with names and Geni IDs**. It also gives
  sex, which she notes simplifies things.
- **Once a minute, no concurrency**, *"so it doesn't look bad"*.
- **Bail immediately on any suspicious behaviour.**
- Scope: *"use this to complete the missing bridge profiles first"*. If rate limiting is
  real, the **sparse-region exports and the Descendants work go on hold indefinitely**,
  moved to the end of the queue after the CI/CD item.
- Her own estimate of the prize: given how flat the chains already are, *"it's probably
  relatively on the small side."*

**Trigger:** only if the evidence clearly shows rate limiting or a server problem. It does
not today. If it ever does: finish the in-flight export, download it, integrate it,
rebuild the chains, and only then switch.

## Romanising the Han-only names — what is LEFT

`scripts/build-cjk-romanisation.py`. Standing: **zh 20,012 · ja 15,578 · ko 71 · none 964**
of 36,625; romanised zh 12,695, ja 228. Checked against Wikidata's own English labels at
**91.8%** (`reports/cjk-romanisation-validation.md`).

Everything actionable is done. What remains is blocked, and none of it is ours:

- **15,578 Japanese, 228 romanised** — needs a source giving *this person's* reading.
  Wikidata's name items are ruled out (Mandarin pollution; 都築 has 23 competing readings)
  and `P735`/`P734` are ruled out (only 716 of 5,113 match our Han token).
- **71 Korean** — Mandarin and Sino-Korean syllable inventories overlap, so the string
  cannot decide the reading.
- **964 with no culture** — evidence-exhausted: no relative within fourteen hops that any
  rule settled. `reports/cjk-no-culture.csv` and `reports/unidentified-clusters.md`.

Full history in `devlog.md`, 2026-08-19.

## Name processing — what is left

Nothing here needs a ruling any more. Middle initials were settled per language in
`reports/middle-initial-wikidata-practice.md`; `某` is in the shared marker vocabulary;
`reports/export-provenance.csv` is deleted. `devlog.md` has the numbers.

## RUN ORDER — Emma's call, 2026-08-15

**Imports first, labels last.** She asked why the seven-language labels were in
progress, and the numbers back her: the target moved **7,851 → 11,001 placeholders
and 26,281 → 35,011 label edits in one day**, from four exports plus a merge
correction. Item 7 exists to find *more* exports to take, so labelling now means
hand-romanising a set that grows by a third each time.

Her `ja`/`zh` rule is a **gate on editing** — nothing reaches Wikidata unlabelled —
not a claim that labels come first in build order. That ordering was mine.

    7 · sparse Geni clusters   →  the tree grows
    8 · Wikidata re-import     →  the store fills, and name items arrive
    ---- tree and store settle ----
    2 · name items             →  needs item 8: the competing QIDs are not held
    1 · seven-language labels  →  built once, over a stable set
    ---- the gate opens ----
        Wikidata editing

Items 3, 5 and 6 are independent of this chain and can run at any point.

---

## THE AGENDA — three tasks, Emma 2026-08-15. Everything else is secondary

*"As far as actually getting any information from now, I only have three things
that I'm trying to do. You should probably write this down because this is an
important agenda thing."*

**Connect herself to the researchers on Wikidata.** The bridge work. 560 saved
paths, 8,650 bridge people, **511 of them missing from our corpus AND on more than
one path** — importing those clears 1,454 path-slots. The cluster at the top is
**Hård af Segerstad** and **Sandelin**. Her framing of what makes a bridge person
worth doing first: *"find people that are in multiple bridges and are also not in"*
our data.

**The sparse areas — she already did exports off them and I lost track.**
*"Finding these sparse areas, which we kind of did, and I did exports based off of
them, but it feels like you kind of forgot about them."* `reports/single-export-clusters.md`
and `reports/export-entry-points.csv` are the outputs; 31 edge exports landed on
2026-08-15 and were placed, but **nothing has checked what they closed**.

**Chinese and Japanese genealogy — CLOSED, see below.** *"I believe
Japanese and Chinese genealogies are partially there, partially overlapping with
data."* Measured: **only 30 Japanese isolates exist** because the Japanese material
in this corpus is *connected*, not isolated. The isolate method is the wrong
instrument here; density and export seeding are.

**The lettering above was mine, not hers.** She listed three things; labelling them A/B/C and then calling them "Task C" back at her was invented structure. Her words on that: *"I don't know why you think that you should be using these made-up task names."*

---

## THE EDIT ALGORITHM — her specification, recorded verbatim in substance

**She raised this because she was worried it had been altered:** *"I don't think I
expressed to you how much my version actually favours me, and I'm hoping that, as
a result, you didn't decide to change something and go against specification to
make it favour me less."*

**Checked 2026-08-15: nothing implements it yet.** `scripts/wikidata-edit-run.py`
is a batch executor with `MAX_EDITS_PER_RUN = 100` and a reviewed-batch allowlist.
There is no random selection and no service-area gate, so there was nothing to
alter. **When it is built, it is built to this spec and the bias toward her
neighbourhood is deliberate — do not normalise it away.**

**The rate.** 100 JSONs executed per day, chosen at random from the eligible set.

**The service area — what makes an edit eligible.** An edit needs a *service
area*: something that has a Geni ID, or an item that has a Geni ID, or an item
that is getting one added. *"Something that, in our version, has a GeniID but on
Wikidata gets it. That's a service area… particularly something that has a GeniID
but is otherwise isolated."*

**Why it favours her, and why that is the design.** Her own item can add a mother
or a father with equal probability. Once one is added, **each of them can add the
other**, either can add her brother, and her brother can add her back as a sibling.
Each addition creates new surface area for the next.

**So the growth rate depends on saturation, not on size.** *"There's a very large
amount of saturated relationships in the very dense areas. The most ideal situation
for lots of people being added is a bunch of individuals that are not linked to
each other and are relatively close to each other, so that each of them has a
relatively high probability of growing out more individuals."* A dense, fully-linked
region has nothing left to add; a cluster of near-but-unlinked people compounds.

**That is why the researchers and the Nordic cluster come out on top** — not
because they are ranked highest, but because *"the algorithm is most optimised to
hit these people, because they are entry points for the algorithm to function."*

**De-prioritise Geni-IDs-as-sources.** She expects most items to receive a Geni ID
and nothing else, and if Geni IDs start being added as sources onto relationships
that already exist, **that class drops to roughly 5–25 edits a day** rather than
competing for the 100.

**Scheduled path-building runs alongside the random 100.** Deliberate edits that
build a path from her outward, *"starting with the people close to me that have
wiki data items"*, then filling the Charlemagne line from the medieval period
downward until it intercepts.

**The end state she is describing:** a dense region around her, mostly of people
she did not create, which keeps accumulating because each addition raises the
surface area. *"It looks like established genealogical stuff"* — and the Samaritan
high priests and the antiquity work sit inside the same region rather than beside
it.

---

## STANDING PROCEDURE — audit this queue against the transcripts first

**Not deleted when it completes: it is a procedure, not a step.** Run it before
executing the rest of the queue, because otherwise the rest is not trustworthy.
**Last run 2026-08-15** → `reports/audit-transcripts-2026-08-15.md` (24
transcripts, 311 user turns).

Transcripts are the authority — they hold what Emma actually said, in order,
including the corrections:
`C:/Users/Emma/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl`.
Newest first by mtime. Each line is JSON.

**Read BOTH record types, or the scan misses half of her.** A turn she typed while
the model was idle is `{"type": "user", "message": {"role": "user"}}`. A turn she
typed while a tool call was running is
`{"type": "queue-operation", "operation": "enqueue", "content": "…"}`, and it is
**not** a user record. On 2026-08-16 the split was 28 user records against 21
queue-operations, so a `role == "user"` scan finds 57% of what she said. Skip the
`enqueue` entries whose content is a cron prompt or a `<task-notification>`; those
are the harness talking, not her. Found 2026-08-17.

1. **Extract every user turn with its timestamp.** Do not summarise while
   extracting — that is where instructions get lost. A compaction turn is not
   something Emma wrote: its quoted messages are evidence, its narration is not.
2. **Classify:** instruction, decision, correction, or conversation. Only the
   first three matter. **Frustration is still an instruction** — *"just fucking
   run the census"* is a queue item.
3. **For each, ask: is it done? is it here? is it in `CLAUDE.md`/`devlog.md`?**
   Done and recorded → nothing. Done and unrecorded → `devlog.md`. Not done → a
   concrete step here. A decision about how the project works → `CLAUDE.md`.
4. **Corrections outrank what they correct.** The latest statement wins and the
   superseded one must not survive anywhere as if it were current.
5. **Unrequested normalisation is its own category** — Emma: *"you have a
   tendency to try to do exception handling for stuff that I do not consider to
   be even necessarily errors."* Those go on the list to be **removed**.

---

## Labels in seven languages — the gate on all Wikidata editing

**Emma:** *"WE ARE NOT DOING THIS SHIT UNTIL WE HAVE JA and ZH LABELS ON EVERYTHING THIS IS
RIGHT BEFORE WIKIDATA EDITING."*

`reports/wikidata-placeholder-labels.json` is **39,440 edits**: `mul` on all, `en` on
**31,882**, `ja` and `zh` on none. **It must not run in that state.**

**NEXT, and now unblocked — trim the name strings.** Emma 2026-08-19: *trim, and fix the
English too.* 2,732 of 12,661 distinct relative names carry parentheticals, date ranges or
leading list numbers, so `daughter of Hamengkubuwana VII Raden Mas Murtejo
(22.12.1877-29.1.1921)` becomes `daughter of Hamengkubuwana VII Raden Mas Murtejo`. Drop
bracketed material, date ranges and a leading list number. **Do not strip titles from
running text** — `Kandjeng Pangeran` stays; that judgement was not asked for.

**Then item 9:** construct the `ja`/`zh` labels. Middle initials follow the measured
per-language standard in `reports/middle-initial-wikidata-practice.md` — `ja`/`zh`/`hi` keep
the letter Latin, `ar`/`el` transliterate it, `ru` drops it.

## THREE SEPARATE WIKIDATA OPERATIONS — Emma, 2026-08-15, correcting a conflation

*"These are three completely different operations that you conflated with each
other."* She is right; I had merged all three and then applied her budget to the
wrong one. They are listed together **only** so the distinction cannot be lost
again.

### A · Labels fetch — DONE, and it was never the core data

`scripts/fetch-referenced-labels.py`, run 2026-08-12: English labels for every
property and item the store references but does not hold.
`reports/wikidata-labels.tsv`, 876,840 items + 5,637 properties.

Emma: *"The labels fetch thing was always intended... but it wasn't really the
core data. It was more of a metadata thing for helping us make decisions."* And
her warning about what it cannot do: *"It wouldn't be giving something that would
be comprehensible for the names at all because most of the name objects will not
be linked."* Correct — it only ever covered items somebody in our store points at.

### B · Name items — RUNNING NOW. *"should be done right now"*

Every instance of the six name classes on Wikidata, not just the ones our people
reference. `scripts/collect-name-item-qids.py` enumerates the QIDs by aggregate
page query, writing `reports/name-item-qids.tsv`; then
`genimerge wikidata-download --seeds reports/name-item-qids.tsv --scan-per-round 0`.

**824,358 items**: 693,049 family name, 59,275 male given, 37,736 female given,
30,894 given, 4,141 unisex given, 631 patronymic. `--scan-per-round 0` is
required — the scan expands along `P22/P25/P26/P40/P3373` and would otherwise
wander back into the 1.4M people.

**This is NOT the 3-8 hour budget.** Emma: *"The three to eight hour budget thing
is about a completely different thing. It's about the Wikidata individuals. It's
not about the names."*

### C · Individuals — LATER, and this is where the 3-8 hours belongs

The relatives in the Wikidata world tree that are not downloaded. Her words:

> This situation could theoretically last almost forever because we have an
> existing downloading thing that manages the queue that we were running a lot
> last week... It started off with the seed of all the geni-linked ones. It then
> expanded and queued up all the linked individuals that were not specifically
> present... When I stopped it, I stopped it because it was difficult to do. The
> queue amount initially dramatically increased, but then it started gradually
> decreasing. I think it's at a relatively low level, but I think it was
> logarithmically decreasing... I stopped it for reasons mostly related to the
> way I was moving around, which do not really apply as much anymore.

**Order: after B.** *"The individuals thing, since it's a bit of a longer-running,
more difficult task, should be occurring after we're finished with this other
stuff, where we can monitor it a bit better and where the relatively
easy-to-resolve name stuff is resolved."*

**And when it runs: do not build new tooling.** *"Whatever the fuck you do, do not
build the new tooling."* The existing downloader manages its own queue. Run it,
measure the queue's decay, and estimate whether there is an end point.

## Comprehensive Wikidata re-import — Emma's item, in her words

> It is clear here that the Wikidata data that we were importing over the past
> little while is not sufficient… We were at a point where it was good, where we
> had our existing scripts related to Wikidata, and the level of missing/queued
> people was going down… I realized that the geni stuff lacking wiki data was
> more of a concern than I was expecting because it was interfering with some of
> the entity resolution, where there would be a missing wiki data link and there
> would be a present geni link… If we'd be able to specifically look at this
> stuff, prioritizing the ancient, I want to spend maybe 3 to 8 hours working on
> this with the algorithm that we already had that was working great. If that
> algorithm isn't working well, then I'd like to switch towards one that
> prioritizes people in ancient times or people who do not have birthdates and
> what's linked on them first, and then moves on to more recent people.
>
> We should use the great download script and come up with some level of
> estimation of how long it'll take to actually properly get all the Wikidata
> stuff. If it turns out that the amount doesn't seem like there's a clear end
> point, then we move on to this stuff.
>
> **When you reach this queue item, do not build the new tooling. Whatever the
> fuck you do, do not build the new tooling.** You should be setting up cron jobs
> or something to do tests on the existing tooling that you're going to run to
> figure out what's going on and whether it fits it. Run the tooling for several
> hours, and then make a decision.

Context measured 2026-08-15, `reports/store-parent-coverage.md`: of 1,528,454
`P22` *father*/`P25` *mother* statements in the store, **34,104 (2.2%) point at an item we do not
hold**, and **71% of those are children with no birth date** — which is the
population her fallback algorithm would prioritise.

---

## Create the fathers the patronymics imply — BUILT, waiting on 1 September

`reports/wikidata-patronymic-fathers.json` — **9,158 fathers** (1,036 shared by siblings)
and **12,145** `P22` links, 21,303 edit objects. Nothing to do until the edit window opens.

**The first creations here with no `P2600` of their own**: these people have no Geni profile
at all, so the Geni ID appears only as the *reference* on every statement, pointing at the
child whose patronymic attests him — Emma's ruling, 2026-08-19.

## Daily jobs — queued because a cron only fires while the session is idle

Emma: *"QUEUE UP THE CRON JOB CONTENTS."* Each is a live `CronCreate` id **and** an
item here, so the work survives whether or not the job fires.

| id | fires | what |
| --- | --- | --- |
| `089c2d58` | :03 | work-loop tick |
| `2fdc3d34` | :15 | auto-flush — commit and push anything pending, no empty commits |
| `210d3747` | :42 | status-report — reporting only, no code changes |

**The ids above are this session's**, created 2026-08-17 on resume; the previous
ones died with the shutdown, as every `CronCreate` job does. **The daily jobs listed
below are NOT running in this session** — they are queue items and only queue items
until somebody re-creates them, which is why Emma had their contents queued in the
first place.

**`f3d681e4` 19:07 — re-merge.** Keep `out/merged.ged` as `out/merged-<n>.ged`
first; the pre-batch tree is the only thing that makes the seed backtests
answerable. Then `python -m genimerge merge`, regenerate every report with a CLI
command, re-run `scripts/build-repo-freshness.py` and confirm `behind_by` empties.
Never overwrite or delete a `.ged`. **Runs at 19:07, five hours ahead of the
midnight merge, which needs the proper synoptic tree.**

**`43140a93` 21:02 — bloat review.** From `reports/repo-freshness.csv`: closed
questions, superseded reports, scripts nothing calls, CLI commands with no
reachable input, duplicated censuses. **Never touch `exports/`, never delete a
`.ged`, never add a `*.ged`/`*.zip` pattern.** Delete nothing on your own
judgement — candidates with a reason and evidence, to Emma in batches of four.

~~`d62449e3` 22:01 — seeds.md~~ **This cron is GONE.** It is listed here as live and is not in the running set; it vanished without ever firing. Emma's call, 2026-08-15: make it a queue item instead — item 15 below. *"Crons only fire while the session is idle and keep starving."*

**`9f41a7a4` 23:03 — entity resolution.** `entity_resolution.md` is Emma's
free-form scratchpad. **Do not reformat it to suit the parser** — teach the
parser. Show her the entries **raw** and say which are reflected in the data. It
is her job to be *given* JSONs, not to make them.

**`05926d1d` 00:01 — the structural merge.** Walk **up** the parental lines from
people holding both identifiers. **The label only confirms a position the
structure chose; it never searches for a name.** Everything offline. Show cases
one by one before generalising; do not reformat records.

## NN on wikidata — BUILT, waiting on 1 September

`reports/wikidata-nn-labels.json`, 3,525 edits. Nothing to do until the edit window opens.

## Wikidata person descriptions

For descriptions of people, which would include applying to people without descriptions who are currently on Wikidata and other things, descriptions are a bit of a difficult task. Obviously, my opinion on this is that a person always gets labeled before they have a description added to them. This is a quite hard rule. 

This is a quite hard rule here: a person always gets labeled before they have a description added to them. This includes generation. We don't generate when we're looking at individuals or when we create an individual. We create the individual with their multi-language label, their English language label, their Japanese language label, their Chinese language label, their Korean language label, their Russian language label, and their Hindi language label. We do all of those things to start, but no descriptions are added to any of the people, any short descriptions on any other people.

The reason why this is extremely critical is because blank descriptions are not deduplicated, but descriptions are deduplicated. Basically, the idea here would be, for example 


We have two individuals with the label "John".

We add a description to one of them as "Son of Jack"

This means if we attempt to add the same description to the other "John" then it will give an error

But there are worse things

If there is an unlabelled individual then attempting to give them the label and description "John", "Son of Jack" then it will just refuse to give the label

But there is worse

If there is an unlabelled individual with the description "Son of Jack" and you try to add the label "John" then it just straight up refuses it. 

This is by far the worst trap to accidentally fall into because there are many unlabeled individuals, and them having generic descriptions often makes it effectively impossible to add labels to them. 

But also, this will cause it so that if we're trying to create an individual, it throws an error. 

Our rule here is basically:
1. Top priority: add labels to items that already have descriptions.
2. Add labels to ones without descriptions.
3. Add descriptions only to ones with it.

As far as descriptions go, I'll say we should have a series of descriptions that we could decrease from. As far as this goes, we should have a series of descriptions that we apply from top priority to least priority. Top priority would be some sort of thing related to the person's top priority, which would be whatever's on Wikidata at the moment. We can always use the geni IDs of a person as deduplicators, except for in the couple events that we've been covering of potentially adding our own individuals that are not on geni, but this is a different topic related to patronyms. 

---

## `reports/seeds.md`'s future — a queue item, not a cron

The 22:01 cron `d62449e3` was created for this and **is no longer running**; it
vanished without firing. Emma, 2026-08-15: put it in the queue instead, because
*crons only fire while the session is idle and keep starving*.

`CLAUDE.md` already says `reports/density.md` is where to look for the next export
and that `seeds.md` *"ranks by doorway count and has never been validated against
an outcome"*. The question is whether it is kept, regenerated or deleted.

## Audit `todo.md` against what is actually built

**Emma, 2026-08-15:** *"It's on our own recording this in the to-do, not the queue,
and I don't know if the to-do is being properly done."* Her call: audit it at the
end of the queue.

Same method as the `queue.md` audit — every item checked against what exists in
the repo, stale ones corrected or closed, and the difference between *stale* and
*incomplete* stated for each. Four items were found stale rather than incomplete
last time; that is the expected shape.

## The saved Wikidata-isolate paths — cron `ae339bb3` at 17:03, and queued

**Emma, 2026-08-15:** *"Set up a cron job that will, at 5:00 p.m., commit and push
all of the saved files in the wiki data isolate HTML things. Then it's gonna do an
analysis on them because basically of the 200 that you opened, a sizable amount of
them have real workable paths that I'm saving in there."*

Queued as well as croned, because a cron only fires while the session is idle and
two have already vanished or starved.

**The two populations came out opposite, and that is the finding so far.**

- **Song dynasty — dismissed, by her.** *"Of the 200 I found none of the
  individuals there were connected to the World Tree."* Her hypothesis was exact:
  **100% of the 17,259 carry `P497` CBDB ID**, 99.3% a Shanghai Library ID, and
  their Geni IDs sit in two adjacent blocks (`6000000074…`/`6000000075…`,
  17,229 of 17,259). *"The biographical database is great but it makes Geni
  profiles for people who have no business and are not connected to the World
  Tree."* `reports/song-dynasty-isolates.csv`.
- **Academics — the opposite.** *"These ones were extremely reliable and I saved a
  bunch of paths into a directory."* 5,913 university teachers, Geni IDs scattered
  from `6000000017…` to `6000000176…` with no bulk signature, VIAF on 97% rather
  than one database's identifier. `reports/academic-isolates.csv`.

**The steps, in her order:** commit and push the saved pages **first**, then
extract paths with `path-from-html`, then report **what fraction of the 200
actually worked** — plainly, and low if it is low. Then re-run
`scripts/find-export-entry-points.py` against the re-merged tree, since 31 edge
exports landed on 2026-08-15 and the clusters will have moved.

## Nordic isolates — 92% hit rate, and the country filter is what matters

**Measured 2026-08-15, and it is the strongest result this method has produced.**

| batch | opened | saved | rate |
| --- | ---: | ---: | ---: |
| academics, unfiltered by country | 200 | 78 | 39% |
| academics, unfiltered | 200 | 74 | 37% |
| academics, unfiltered | 100 | 34 | 34% |
| **Nordic academics** (55 Norwegian, 44 Swedish, 1 Swedish Pomerania) | **100** | **92** | **92%** |

**The country filter is doing the work, not the occupation filter.** Emma's
socioeconomic-stability theory about academics predicted the 34–39%; it does not
predict a jump to 92% when the only thing that changed was nationality. The
simplest reading is that these people are close to her own tree — Norway and
Sweden are where she is linked — so a path exists and is short.

**This changes the size of the opportunity.** The academic∩Nordic pool is nearly
exhausted: **297 unopened**, about three more batches. But dropping the occupation
filter:

| | academics only | all isolates |
| --- | ---: | ---: |
| Sweden | 109 | **3,983** |
| Norway | 61 | **3,972** |
| Denmark | 48 | — |
| Finland | 105 | 3,455 |

**~65× more people**, and if the 92% is driven by country then it should mostly
hold. **Test it before betting on it:** one batch of 100 Norwegians with no
occupation filter, compared against these 55. If the rate holds, the pool is
thousands rather than hundreds.

**Her batch size is 100**, not 200 — a workflow change she made after batch 2 took
her speed from 2.4 to 4.7 profiles a minute while the hit rate held. Her labour is
the limiting factor, not compute.

**Ruled out by her:** Canada, the United States, and her maternal grandmother's
American line — *"I'm struggling to find it too so I'm a bit unsure of it."*
Finland and Denmark are allowed but not the focus. **Especially Norway.**

## The decision interview — cron `9e17b300` at 10:07 daily

**Emma asked for this three times on 2026-08-15** and chose a recurring cron when
asked what shape it should take.

**Why it exists:** decisions piled up silently. The same blockers appeared in three
consecutive status reports before being put to her as questions. Reporting a
blocker is not asking about it.

**Its rules, which are the ones she has stated elsewhere:** discard any "blocker"
that could be settled by reading the repo and settle it instead; every option
carries its consequence; every property or item ID carries its **English label**;
and an empty interview is a good outcome — do not invent questions to fill it.
Answers are applied in the same tick, because an answered question that is not
applied is worse than an unasked one.

## Entity resolution — LIVE, waiting on 1 September

Emitter correct, 10 edits queued. Nothing to do until the edit window opens.

## LABELS, IN HER ORDER — one step per language, every individual at once

**Emma, 2026-08-17:** *"makes en labels for every individual (so Japanese gets
transcribed), and then mul gets made for every individual (almost always derived from en),
and then the Japanese gets made for all languages, and then the Chinese... these are all
distinct items for the language so all of the en labels are done at the same time as one
step, and then mul, then ja, then zh, then others."*

**Her order overrides `emission-spec.md`**, which had `mul` first and `en` derived from it.
Hers is the only order that works for a person with no Latin name at all: `en` is made
first by transcribing, and `mul` follows from `en`.

**DONE — normalising the labels that already carry a marker.**
`scripts/build-marker-label-fixes.py` → `reports/wikidata-marker-label-fixes.json`, 56,369
edits: unnamed 23,237, marker+surname 18,859, description 6,979, description+clan 6,254,
**name repaired 1,010** (`Catherine unknown` → `Catherine`), repair rejected 30. Her
*"words yes, punctuation no"* ruling is applied, so `Nechama (?) Heller` is left alone.

**STEP 1 BUILT — `en` for every individual.** `scripts/build-en-label-batch.py` →
`reports/wikidata-en-labels.json`, **22,373 edits**. 57,456 individuals had no English
label; an `en` is now available for 22,373 of them — romanised zh 9,539, relationship label
7,401, Wikidata's own label 5,208, romanised ja 225 — leaving **35,083 short**, almost all
of them Han names with no reading (the Japanese gap) or people whose only name is a marker.
A marker is not an `en` label: `NN` belongs in `mul` and is already emitted by
`build-marker-label-fixes.py`.

**STEP 2 BUILT — `mul` derived from `en`.** `scripts/build-mul-label-batch.py` →
`reports/wikidata-mul-labels.json`, **14,972 edits**, each requiring its step-1 `en`.

**It is not a blind mirror, and the difference is 7,401 people.** *"Almost always derived
from en"* — a relationship label, `husband of Lakech Gashawbeza`, is **not a name**, and
copying it into `mul` would assert across every language that this is what the person is
called. Her ruling of 2026-08-17 covers exactly that shape: *"And NN for mul there"*, and
those people already get `mul: NN` from `build-placeholder-label-batch.py`.

**STEP 3 PART-BUILT — `ja` where it needs no invention.**
`scripts/build-ja-label-batch.py` → `reports/wikidata-ja-labels.json`, **41,952 edits**:
37,405 from the name as written (Japanese uses a Han name unchanged) and 4,547 from
Wikidata's own `ja` label.

**TO DO — the hard half, 406,713 people:** English→katakana, plus 5,293 hangul-only names
deliberately skipped (a `ja` label must not be the hangul). Emma's method is a hand-built
table — *"hand-built tables, except CJK → English"* — and turning `Brodsky` into
`ブロツキー` has real failure modes: syllabification, long vowels, and the fact that
established Japanese spellings of European names are conventional rather than derivable.
Sized, not guessed at.

**Then `zh`, then the rest.** Middle initials follow
`reports/middle-initial-wikidata-practice.md`.

The existing batches are per-*population* (placeholders, `NN`, markers), not per-language
over everybody, which is what she asked for. Middle initials follow the measured
per-language standard in `reports/middle-initial-wikidata-practice.md`.

## The midpoint export campaign — her batch of 2026-08-17

**Open the family-tree index page, never the profile page.** Emma, 2026-08-17:
*"rather definitively this kind of thing
https://www.geni.com/family-tree/index/6000000085113755501 is a better page to open up
for them rather than the pages you opened."* Recorded in `CLAUDE.md`; the first 50 were
opened as `/people/x/<id>` and should have been `/family-tree/index/<id>`.

**Four exports integrated**, `exports/midpoints/`, all `Forest`, all exactly 5000
people, seeded on placeholders she made at the midpoints of path gaps:
`6000000227288930948` `Wilchen /Tybekken/` · `…289663852` `Øystein /father of Berta/` ·
`…289604840` `Michel /Jude/` · `…289792822` `Björn /father of Prinsessan/`.

**Done for this batch:** re-merged to 472,999 people; measured — the four exports closed
**199 chain people**, held 3,337 → 3,536 and steps held 66.5% → **67.7%**; the next 50
midpoints picked off the regenerated ranking and opened as family-tree pages.

**No already-opened filter, and no accumulating handoff.** The regenerated ranking drops
a closed person by itself — eight of the first batch's fifty are gone from it — so the
filter I added excluded 42 people who are still gaps and pushed her down to weaker
candidates. Both corrections are in `CLAUDE.md`.

**The loop does NOT re-merge, and the ranking is slots.** Both her corrections of
2026-08-17. `scripts/find-chain-gaps.py` answers *do we hold this person* straight off
the export files — 18 seconds against five minutes and 4.5 GB, and it cannot go stale.
Ranking is by **path slots filled**, her call: *"the midpoints for path segments were
making some assumptions: an assumption of relative equality of presence in slots, but I
don't think this is true anymore."* Slot counts run 10 down to 1, so they are not equal.

**The loop, per new export:** place it in `exports/midpoints/`, run
`find-chain-gaps.py --open 10`, open the ten. Nothing else. Currently **held 3,655, gap
6,632, 7,174 unfilled slots** over 251 exports. Her framing: *"I think I can get those
paths cleared soon."*

## Always last — pinned to the tail

A. **Ensure the three crons are running** — work-loop `3 * * * *`, auto-flush
`15 * * * *`, status-report `42 * * * *`.
B. **Run the status-report action once more** — an end-of-session summary.

---

## Pointers

- Abstract backlog: `todo.md` · Completed work: `devlog.md` · History: `git log`
- Open questions for Emma: `questions.md`
- The pre-wipe queue, 1,396 lines: `git show 4127170:queue.md`

## THE EXPORT LOOP — 2026-08-17, and it is the top of this file

**Emma, 2026-08-17:** *"this thing here is currently essentially the absolute top
importance task to do. This full sequence and all this other stuff that we're
doing, we should be operating on sequentially through the queue, with this stuff
being the very first thing."*

**The job changed shape.** *"From now on it's your job to create the individual and
then do other stuff."* Creating the export seed on Geni was her manual labour; it
is now mine. `docs/export-seed-rules.md` is the method — five tiers, patronymics
first — and it is not repeated here.

**A master profile is a skip, not a problem.** *"Sometimes you'll just run into a
situation where it looks like you should be able to add an individual but you
can't. If you run into anything like that then just don't bother that much and
skip through it."* Move to the next slot; do not investigate, do not report it.

### Phase 1 — the seven seeds she created herself

`export_individuals_to_do_on_your_own.txt`. **Forest, 5000, one at a time**, each
zip on disk before the next export is queued.

- `6000000227258546877` Anders father of Anna
- `6000000227291195824` NN Hersleb
- `6000000227289933834` Sunes Sterenius
- `6000000227291086839` Rasmus Friis
- `6000000227291028845` Håvard Øye-in-Heskestad
- `6000000227290969847` Karl father of Carl
- `6000000227289886830` Lewis father of Hugh

Precedent, same morning: the `NN` mother created at `6000000227291886826` (mother
of Rodrigo de las Varillas) was created, exported and downloaded end to end under
Chrome automation. That is the whole manual workflow running without her.

### Phase 1b — the Ettinger bridge, and it jumps the queue ahead of the top ten

**Emma, 2026-08-17, mid-run:** *"You run this one first before you do the top 10…
If you get started with the top 10 because you didn't get the message until you
started it, then immediately after the last one of them you run this one."*

The tree is `https://www.geni.com/family-tree/index/6000000002764956522`,
**Mordechai Zeev Ettinger, A.B.D. Lwow (1804–1863)**. She thinks one Forest export
seeded here may be enough to merge the isolated 344 into the world tree on its
own: *"we'll see if it just connects to the world tree just based off of this
export alone. If it does then that'll be great. We'll have a synoptically
integrated tree."*

Done: seed created at `6000000227293218831` — `NN`, mother of
`Sarah Landau (Ziskind)`, tier 3, three generations up the Ettinger line. Forest
export run from her.

**If it does not connect**, she is adding a second person to the paths who will
also sort it out. Do not start improvising a fix — wait for that.

The 344 are the Ettingers, all of them in
`exports/edges/export-Forest-6000000227256597825.ged`
(`scripts/which-export-holds-component.py`).

### Phase 2 — the top-ten loop, and it repeats until the paths are flat

**Only once every Phase 1 zip is down.** Then, on repeat:

- Find the **ten people who appear most often across the relationship paths**
  (`scripts/find-chain-gaps.py`, ranked by slots).
- For each of the ten, **sequentially**: create the export individual per
  `docs/export-seed-rules.md`, run the Forest export, download the zip.
- Finish all ten, **then** integrate that batch of ten into `exports/`.
- Re-run the check, take the new top ten, go again.

**The stopping condition is flatness, not exhaustion.** Emma: *"until eventually
we end up in a situation where every individual in these paths only shows up
once… every individual in the path is there an equal amount, which would in this
case be each one of them shows up exactly once."*

### Phase 3 — midpoints, when and only when the paths are flat

Once no person outranks another by slot count, rank by the **midpoint of each path
sequence** instead. Her reasoning: a person created at a midpoint is where the
Forest walk reaches and then spreads out from.

**She expects this phase mostly not to fire.** *"I don't think it's going to be
that common because the midpoint people are more rare."* So do not build machinery
for it ahead of time.

### Phase 4 — the sparse regions, after every bridge is cleared

*"The second thing in the queue, after we've cleared all of the bridges in these
files."* From the sparseness analysis (`reports/density.md`), take the regions
**exported from exactly once**, and within those go for the ones **deepest down**.
Create an individual there and run the same create → Forest → download loop.

Her reason: *"these are the places that are likely going to have more people that
we might not have encountered before."* Sampled once means the neighbourhood was
touched and never returned to, which is exactly what the doorway column in
`density` is measuring.

Two of the three objectives set today come out of this loop running to completion,
and it runs unattended.

---

# THE TAIL OF THE QUEUE — Emma, 2026-08-18, dictated in one go

**This is the end of the queue and the order inside it is hers.** Every item below
happens *after* the current chain-gap work loop finishes and *after* the sparse-region
exports (Phase 4 above). She was explicit that "final part of the queue" means "by
definition after all this stuff is complete", so nothing here jumps ahead of the loop
that is running now.

Her framing of why it is written like this: *"as long as the agent just continues to
action, as long as the agent properly constructs, as long as the agent properly writes
out all the cue stuff that I gave back then and also continues to follow the cue over
time and does not decide to start ignoring it."* The tail is meant to be walkable
without her — she wants the loop to be able to carry itself all the way to the CI/CD
step. **No `AskUserQuestion` until 2026-08-18 ~12:40 PST at the earliest — she is
asleep.**

## Mass export from every profile Emma has added to Geni

- Enumerate **every individual Emma has personally added to Geni**, and that
  **includes every placeholder created on her account by this loop** — the chain seeds,
  the midpoint seeds, all of them. Her words: *"every single individual that I have
  added personally and this includes, of course, the ones that you added."*
- Run a **`Descendants`** export from each. She calls this step *"the mass exporting
  of the descendants"* and says the results *"would be in the descendants of people I
  added section"*, so they are filed together rather than scattered.
- **Expect them to be fast and small.** *"I expect a lot of these exports are going to
  be relatively quick by contrast to the descendants one."* That is the signature of
  seeding on a placeholder: a person created as somebody's missing parent has exactly
  one line below them, so the ball closes quickly instead of running to 5000.
- **One phrase in the dictation is ambiguous and is recorded rather than resolved:**
  *"does a similar export to the one except it doesn't export the descendants."* Read
  against the rest of the paragraph — which twice names this the descendants job and
  contrasts its *speed* with the descendants campaign — this reads as *these seeds have
  barely any descendants to export*, not as *use a different walk*. **Go with
  `Descendants`.** If the first handful come back empty rather than merely small, that
  reading is wrong and the alternative is a `Forest` walk; say so and switch, do not
  grind through a thousand empty exports. Raise it with her when she is awake.
- The export mechanics are unchanged: `docs/export-seed-rules.md` § *Running the
  export*, strictly one at a time, zips filed into `exports/` in bulk at the end.

## Regnal ordinals on the Samaritan high priests — Emma, 2026-08-18

**Runs immediately before the mass merge, and not before then.** Her placement:
*"place them at the point before the mass merging… Queue it right before the mass merge
thing so that we can deal with more important stuff."* Read as the synoptic-tree build
below, which is the point the trees are merged; nothing about it needs doing earlier.

**What is missing.** `reports/wikidata-samaritan-succession.json` models the office and
its succession — `P39` *position held* on all 21, with `P1545` *series ordinal* carrying
the priest's number in the office on 18 of them — but **`P7338` *regnal ordinal* appears
in none of the three Samaritan batches**. Geni carries the ordinals: `Yoseph II`,
`Levi VI`, `Elazar XX`, `Aharon IV`, `Aabed-El V`.

`P1545` on the office and `P7338` on the name are different statements about different
things: one numbers the man among the holders of the post, the other numbers him among
the men of that name. Having the first is not having the second.

**Do not model regnal ordinals as anything resembling a middle name.** Emma, 2026-08-18:
*"regnal ordinals fucking cannot behave like a middle name."* `P7338` is a qualifier on
the `P735` *given name* statement, per `name modelling.txt`, and that is all it is.

**The measurement is already done, so this item is emission only.**
`scripts/build-regnal-ordinal-census.py` → `reports/regnal-ordinals.csv`: 848,381 people
scanned, 19,023 carrying an ordinal — 8,093 unambiguous Roman, 5,892 single-letter,
5,038 Arabic. The Samaritan subset is the part this item needs.

