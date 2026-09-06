# `final-wikidata-geni-scrape`

**The task, named by Emma 2026-09-06.** Walk the Geni profiles this project cares about, take from
each one the things the collector can take, and turn every one of them into a **tiny GEDCOM** that
merges into the synoptic tree on the Geni id.

**It cannot start until the extension and these deliverables are good** — her words: *"The scrape
is to be done with the extension we built yesterday and it can only be done after we have a
coherent idea of the deliverables."* § *NOT SETTLED* below is that gate, and it is not
decoration: nothing the extension writes can reach disk today.

## What it covers

| population | count | source |
| --- | ---: | --- |
| every member of every sibling pair | **2,527** unscraped of 2,528 | `reports/sibling-pair-worklist.tsv` |
| the isolate path pilot | 82 of 100 remaining | `reports/isolate-path-pilot.tsv` |
| legacy saved pages already on disk | **1,555** | `geni-scraping/` |
| the full isolate campaign the pilot decides | 185,327 | `reports/isolate-path-pilot-urls.txt` is the sample |

## Why it is called final

Because after it there is nothing further to take off a Geni page: the immediate family, the
relationship path, and the statistics block are the whole of what a profile exposes. What follows
is merging and then Wikidata authoring, not more collection.

---

**Emma, 2026-09-06:** *"The scrape is to be done with the extension we built yesterday and it can
only be done after we have a coherent idea of the deliverables."*

Written because the deliverable moved three times in one day — a TSV, then a tiny GEDCOM with `NN`
placeholder parents, then a tiny GEDCOM with absent slots — while collection carried on through
all three. Nothing more is scraped until this is right.

## SETTLED — her words, this session

**Two distinct operations.** *"There's two distinct operations. Paths and profiles. Both ought to
make tiny gedcoms for each path or individual. Both have similar information. Many saved pages
have the info to make both tiny gedcoms from them."*

| operation | unit | one file per |
| --- | --- | --- |
| **profiles** | a person's immediate family | person |
| **paths** | a relationship path | path |

**The output is thousands of tiny GEDCOMs, and that shape is the point.** *"you didn't understand
that thousands of tiny gedcom files was the signal."* Not two aggregate files. The granularity is
what distinguishes this from the earlier incomplete attempt.

**GEDCOM is the native format.** *"for all intents and purposes the native format of this project
is the gedcom now."* A `.ged` under `exports/` is read recursively by `genimerge.sources`, so it
reaches the synoptic tree with no wiring.

**Geni ids are the entity resolution.** *"with the geni ids set up so that they end up getting
merged in ... the entity resolution in them means they significantly link things together."* Every
`INDI` xref is a Geni id, so the merge is an exact join and these files fuse into the tree.

**An unknown parent is an ABSENT SLOT, not a person.** Her ruling, chosen between the two
readings. A sibling pair with no known parents is a `FAM` with two `CHIL` and no `HUSB`/`WIFE`.
This supersedes her 2026-08-29 *"Both parents are 'NN' placeholders"*.

**Every member of every sibling pair gets the profile scrape, and the redundancy is deliberate.**
*"every single sibling pair gets the small scrape done on it ... I know this is slightly
redundant, but I'm telling you to do it."* Because: *"it'll create a gedcom for each one of the
members of the sibling pair, and then this links them as siblings with their parents in this new
gedcom file, but they're also linked as siblings in the path gedcom files."* The path GEDCOM says
*siblings, parents unknown*; each member's profile GEDCOM carries the real parents; the merge
fuses all three on the Geni id.

**The extension does the scraping.** *"The scrape is to be done with the extension we built
yesterday."* Not agentically, and not by hand-carrying data through tool results — which
double-encoded 4 of 14 scrapes before it was caught.

## BUILT

`scripts/build-tiny-gedcoms.py` — both operations, absent slots, zero invented people. Currently
13 profile GEDCOMs from `geni-families/*.tsv` and 694 path GEDCOMs from `paths/*.tsv`, 28,648
`INDI` lines.

`scripts/sibling-pair-worklist.py` — 2,130 pairs, 2,528 distinct people, 2,527 with no scrape.

## NOT SETTLED — these gate the scrape

1. **How the extension writes the files.** It holds the TSV in the tab. `chrome.downloads` from
   the background is not subject to the content setting that blocks an `<a download>` click, so
   the collector can write to disk — but the background service worker has never updated and that
   needs a reload at `chrome://extensions`. Until then nothing the extension writes can land, and
   hand-transport is barred.

2. **The 1,555 legacy saved pages in `geni-scraping/`.** She said the emitter should run on
   *"legacy scrapings and with the new scrapings by the extension"*. Nothing in
   `build-tiny-gedcoms.py` reads them. Only `build-scraped-gedcom.py` does, and its output uses
   the superseded `NN` placeholders.

3. **What happens to `scraped-pages.ged` and `scraped-paths.ged`.** Two aggregate files in the
   merge carrying 4,928 `NN` people, which the absent-slot ruling says should not exist. Removing
   them changes every merge.

4. **Whether path GEDCOMs should also come from saved pages.** *"Many saved pages have the info to
   make both tiny gedcoms from them."* Today paths come only from `paths/*.tsv`.


---

# Moved out of `queue.md`, 2026-09-06

**Emma:** *"The scrape does not belong in the queue and I think it's presence there causes
issues."* She is right about the mechanism: `queue.md` is what the hourly work loop takes its next
item from, so a gated collection task sitting in it was picked up and run repeatedly today before
any of these deliverables existed. The queue is for executable steps; this is a long-horizon task
with a gate, which is `todo.md`'s job.

Everything below is verbatim from the queue, moved rather than rewritten.

## The phase order

- **⛔ THE PHASE ORDER governs everything below — `docs/per-individual-loop.md`.** Emma,
  2026-09-06: phase 1 runs the isolate-connecting operation over **all** Wikidata isolates, which
  yields paths, immediate-family objects and occasional Forest exports; phase 2 **integrates all
  of it into the synoptic tree**; phase 3 then scrapes each member of the sibling pairs that are
  **still parentless in that tree**. Her words on my starting at phase 3: *"jumping to the mass
  action was really bad because you skipped over a lot."* The sibling batch's input is the
  INTEGRATED tree, never today's `paths/*.tsv` — phase 1 supplies parents for many of those pairs
  as a side effect, so the real list is much smaller than the 1,321 pairs currently there.


## The 100-target isolate path pilot

- **Fetch the 100-target isolate path pilot.** `reports/isolate-path-pilot-urls.txt` — **100
  profile URLs**, one per target, and `reports/isolate-path-pilot-queue.txt` is the same list in
  the collector's input format. Then `python scripts/harvest-isolate-paths.py --write-paths` for
  the hit rate.

  **Progress is MEASURED, never written here:** `python scripts/pilot-progress.py`. The count sat
  in this item as prose and went stale twice in one night — *5 of 100* while nine were on disk,
  then *9* an hour after it was corrected to nine. A number in a queue item is wrong from the
  moment the next target lands.

  **⛔ EACH TARGET GETS THE PER-INDIVIDUAL LOOP, and step 1 is the family scrape.**
  `docs/per-individual-loop.md`: scrape and save the immediate family first, unconditionally,
  then try the Charlemagne path, and only run step 3b where the path fails **and**
  `scripts/export_gate.py` clears the statistics. Ballin is the worked skip — Family Tree 11.

  **NOTHING IS SAVED AS A PAGE ANY MORE.** Emma, 2026-09-06: *"we are not supposed to be saving
  pages lol ... Only the exports need downloading because you write stuff into files in the repo
  you dummy."* The collector parses the chain in the tab and RETURNS the path TSV, which is
  written straight into `paths/`; the family scrape returns its TSV for `geni-families/`. The six
  `geni-paths/*.html` captures are what the earlier page-saving method left and stay as those, not
  as a destination. `geni-paths/README.md` § *THE CALL THAT WORKS* still describes the Blob save
  and is superseded on that point.

  **Both `blood` and `inlaw` are still wanted — her call, 2026-09-02** — and they are two captures
  from the one profile page, not two fetches: blood against in-law is a control on the page, not a
  URL parameter. One a minute, no concurrency, bail on anything odd.

  ⛔ **PASS TWO IS NOT "COME BACK AND READ". A REQUESTED SEARCH DECAYS BACK TO UNREQUESTED** —
  measured 2026-09-06. Rudolf Beck read *"Path search in progress"* and showed the **"How are you
  related?"** button again two hours later; Hilde Kann's 2026-09-03 miss reads as unrequested
  today. So pass two must **re-request wherever it has reverted**, and a revisit that only reads
  reports a target as untouched forever.

  **Two consequences, both already handled, both worth knowing before changing that code.**
  `path_state` must never infer a hit from the absence of a miss — Asser de Haan showed the
  not-requested button and was written down as `path_found=yes`, a connected hit on a search
  nobody ran, which inflates the one number this campaign produces. A **miss** is stated on the
  page in words; a **hit** needs a parsed chain with the target on it. And a revisit must never
  blank an observed verdict: `no`/`yes` are observations, blank means *not seen yet*, and only a
  stronger observation replaces one. Without that, every revisit across 185,327 targets silently
  reverts its verdict to pending and the reach rate drifts to zero for a reason nothing records.

  ⛔ **This item said "200 URLs, both `blood` and `inlaw` per target" until 2026-09-05 and that
  method is refuted.** The `/path/x?from=&path_type=&to=` form ignores `to=`: it redirects to
  Charlemagne's own profile, which renders a full chain — the *viewer's* — so a harvest keyed on
  step count scores every miss as a hit and returns a reach rate made of copies of one path.
  Re-measured 2026-09-05 from her own browser. `geni-paths/README.md` § *THE CALL THAT WORKS*
  has the working call verbatim; do not re-derive it.

  Anchored on **Charlemagne** (`6000000002457013227`, `Q3044`), her correction of 2026-09-03 —
  not on Emma, which is what the 663 existing paths use. The anchor is her account's pushpin,
  set once by her, and is never toggled.

  ⛔ **THE ANCHOR IS NOW SET ON CHARLEMAGNE — `docs/anchor-protocol.md`.** The first real capture
  came back anchored on the viewer (step 1 `You`), and that was reported to her as a decision she
  had to make. **It was not hers to decide.** Her *"it needs to be done exactly once and I did
  it"* was a shortcut she took to unblock a stalled session, not a rule; her words, 2026-09-06:
  *"You can set up a protocol to get it set on Charlemagne lol."*

  Check the banner on Charlemagne's profile, click the pin only if it reads *"is your 35th great
  grandfather"*, and verify on a target rather than on the pin. **Verified:** Rudolf Beck resolved
  to a 23-step chain to Emma before the change and reads *"No blood relationship was found"*
  after it — the question demonstrably moved.

  `reports/isolates.csv` carries an **`anchor`** column now, because a verdict means nothing
  without it. Every row taken before this is marked `emma`, including Beck's `yes`, which is an
  Emma-path and **not a pilot hit**.

  **Needs her browser, and now runs through `geni-extension`** rather than agentically. The
  number it produces decides whether the 185,327-target campaign runs — her own batches were
  34–39% for occupation-filtered academics and 92% for Nordic ones. A blank chain is
  `chain_found=0`, never *unrelated*.


## The sibling-pair scrape

- **Scrape the immediate family of EVERY member of EVERY sibling pair -- 2,527 people.** Emma,
  2026-09-06, said it twice because it looks redundant and is not: *"every single sibling pair
  gets the small scrape done on it ... needs to be done on every single person, every single
  person in sibling pairs. And, yes, I know this is slightly redundant, but I'm telling you to do
  it. I'm telling you to do it."*

  **Why both members.** A path can only say *these two are siblings* -- Geni records no sibling
  edge -- so under her ruling the path GEDCOM writes them as a family with two `CHIL` and no
  partners. The parents arrive from the members' own profile pages. Her words: *"it'll create a
  gedcom for each one of the members of the sibling pair, and then this links them as siblings
  with their parents in this new gedcom file, but they're also linked as siblings in the path
  gedcom files."* The merge fuses all three on the Geni id.

  `scripts/sibling-pair-worklist.py` writes `reports/sibling-pair-worklist.tsv`. **2,130 pairs,
  2,528 distinct people, 2,527 without a scrape.**

  The pace is the real constraint and is not a reason to skip it: Geni served an Incapsula CAPTCHA
  after roughly forty profile loads earlier today, it cannot be solved here, so this runs in
  stretches at the pilot's one-a-minute with her clearing them.


## Decision: retire `build-scraped-gedcom.py`

- **DECIDE: retire `build-scraped-gedcom.py`, whose output now contradicts her ruling.** Her
  2026-09-06 ruling is that an unknown parent is an **absent slot, no person**. That script
  implements her earlier 2026-08-29 instruction instead -- two `NN` placeholder parents per
  sibling group -- and its two files in the merge carry **4,928 such people**.

  `scripts/build-tiny-gedcoms.py` now covers **both** of its operations under the new ruling:
  profiles from `geni-families/*.tsv`, paths from `paths/*.tsv`, **zero invented people across
  28,648 `INDI` lines**. What it does not read is `geni-scraping/`'s 1,555 saved pages, which is
  the one thing only the old script does.

  **Not deleted on my own judgement this time.** I deleted it once today on a framing I supplied,
  having called her deliberate mechanism corruption, and restored it. Removing its two files
  changes every merge; that is hers.

