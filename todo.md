# geni — Long-horizon backlog

**This file is the project's *abstract destinations*, not its steps.** When work on one begins, it is broken into
concrete items in `queue.md`, done, and recorded in `devlog.md`.

**Audited 2026-10-08, every item (queue item "Go through the entire todo.md").** What was built is gone from here
(the merged tree, reconciliation, the authoring pipeline, name items, backfills, more sources, the Wikidata download,
the old batch inventory, the `gaiad` flag fix); `devlog.md` 2026-10-08 says what happened to each. What is left is
Geni-gated (no Geni work, Emma 2026-10-01), explicitly not now, or not ready.

---

## 3. Expansion planning — where to export next

The current exports are bounded slices of Geni. Identify the **frontier** of the
merged tree: individuals with missing parents, sparse subtrees, and
high-connectivity hubs that would pull in the most new material per export. Use
this to decide what to export next from Geni.

### 3z. The three phases (recorded 2026-08-04)

This is the ordering the rest of item 3 sits inside. Written down because the
sub-items below were built during phase 1 and read as though it were the whole
job.

**Phase 1 — connect (now).** The point of an export right now is to *join*
things: reach a person, close a gap between components, make a path walkable.
`Forest` and `Ancestors` do this. The Jimmu bridge is the worked example.

**Phase 2 — bulk (in progress).** Every export Geni will readily give is being taken,
**up to about 50**. These are not aimed at anything; they are cheap
coverage. `exports/archive/` is where they land. Do not analyse them one by one
or try to read intent into a seed — but do check them for people a path file is
waiting on, because `(22)` and `(23)` were bridging exports sitting in the bulk
pile.

**Phase 3 — synoptic density, then targeted breadth (after phase 2).** With ~50
exports merged there is enough overlap to ask a question none of the current
reports answer: **for each person, how many exports contain them?** A person in
many exports sits in a densely covered region. A person in one or two is on a
thin edge, and a *region* of such people is where the tree is least
comprehensive — which is where the next round of exports should aim, and which
matters because thin regions are exactly the ones that will reconcile badly
against Wikidata.

**The descendants of the Indian people are the clearest example of a thin region.**
That is the first thing to check when the measure exists.

`Descendants` exports belong to phase 3, not phase 1. They are not for
connecting people — they fan out to pull in everyone below one person, which is
a *breadth* instrument. Do not propose one to close a path.

**"Region" means a region of the graph, not a place.** Do not classify people
geographically. Birthplace strings are dirty, most people
do not have one, and inferring a place from a name is exactly the fuzzy matching
this repo refuses everywhere else. A region here is a **neighbourhood in the
family graph** — people close to each other by parent/child/spouse edges,
regardless of where they lived.

**What is missing to do this.** `genimerge.inventory` computes pairwise overlap
and per-file uniqueness, but has no per-person presence count and no way to
aggregate it over the graph. The measure needs: (a) a count per Geni ID of how
many exports hold it, and (b) a way to find *contiguous stretches of graph*
where that count is low and the stretch is large. Neither exists.

**Not before the bulk downloads are done.** Building this is wanted, and equally
clearly not yet — with ~50 exports still arriving, any
density measured now describes the download queue rather than the tree.

### 3b. Export seeds, modelled on how Geni exports

Ranking by descendant count measures the tree we already hold. `genimerge
seeds` (`reports/seeds.md`) instead models an export as what it is — a
breadth-first ball from one profile, of a few thousand people, in one of four
styles — and scores a candidate by the **doorways** in its ball: people with no
parents recorded, where Geni can walk further than we can. Seeds inside a region
recorded several layers deep are rejected as saturated. The picks are chosen
greedily on newly-covered doorways, so ten picks are ten *different*
neighbourhoods rather than ten names off one branch.

The ball size is deliberately vague here. Three exports held exactly 3836, which
read as a hard cap until a fourth held 3840, and the ceiling has since walked up
to 3860; what actually bounds an export is not established.
`genimerge.seeds.GENI_EXPORT_CAP` carries the detail, including what 28 exports
ruled out on 2026-08-04.

**This whole item is worth less than it was, and that is a change in the
project rather than a defect.** Seed ranking answers "which one profile should I
export from next?", which mattered while each export was a deliberate choice.
The project has since switched to exporting whatever Geni will readily give — 17
takes in one afternoon — so the binding constraint is now ingest and download
time, not seed choice. Ranking still earns its place for the *targeted* exports
(the Jimmu gap was found and closed this way), but do not spend effort improving
it on the assumption it is on the critical path.

Still open: **taking the next export**, from the sequence in `reports/seeds.md`.
**This is NOT blocked on anybody and the tag saying so was wrong.** `CLAUDE.md`
§ *The batches are a SEQUENCE* lists "the merges/exports must wait" as one
of three invented limits, refuted on 2026-08-17: Chrome automation runs the whole
loop end to end — create the placeholder in the tree view, Actions → Export
GEDCOM, poll the download page, click through, with no human labour in it at all.
An export tagged BLOCKED-ON-USER-ACTION here is a thing nothing is blocking.

**Confirmed 2026-08-01.** The rest of that sentence used to predict that
`genimerge merge` would absorb a new export without changes and that the seed
ranking could then be re-run. A fourth export tested it. The merge took it with
**zero code changes**, and `seeds` re-ran to a materially different plan — ten
picks reaching 193 doorways against 173 before, with picks 2, 3, 8 and 9 new.

**What the ranking could not do** is find that seed. `reports/seeds.md` ranks
only people already in the merged tree, and the fourth export was seeded on Iver
Mellegård, who appeared in none of the first three. So the best export so far
came from a route this repo cannot see or reproduce — an open question, recorded
in `queue.md`, and the thing most likely to change what is worth building next.

## 3c. `final-wikidata-geni-scrape` — GATED, and the gate is real

**`docs/final-wikidata-geni-scrape.md` is the specification.** Read it before touching this.

Take from every Geni profile the project cares about what the collector can take — immediate
family, relationship path, statistics — and emit each as a **tiny GEDCOM** that merges into the
synoptic tree on the Geni id. **Thousands of small files, not aggregates** — that is the
signal, and it was missed once already.

**⛔ IT CANNOT RUN YET, and this is not a formality.** The scrape is to be done with the
extension, and only once the deliverables are coherently settled. Two conditions, both
currently unmet:

- **The extension must be able to write files.** Its background service worker has never updated —
  measured 2026-09-06, it returns the nine-key `DEFAULTS` from before `28a9f05a` — so nothing it
  writes can land. Hand-carrying scrapes through tool results is barred: it double-encoded 4 of 14
  before it was caught.
- **The deliverables must be settled.** § *NOT SETTLED* in the spec names four: how the extension
  writes at all, the 1,555 legacy saved pages nothing now reads, the two aggregate files still in
  the merge carrying 4,928 `NN` people the absent-slot ruling forbids, and whether path GEDCOMs
  should also be built from saved pages.

**Scale:** 2,527 sibling-pair members, 82 of the 100-target pilot, 1,555 legacy pages, and behind
the pilot a 185,327-target isolate campaign the pilot exists to decide.

**Built already:** `scripts/build-tiny-gedcoms.py` (both operations, absent slots, zero invented
people) and `scripts/sibling-pair-worklist.py`. What is missing is the running of it.

## 3d. The collector's background service worker — NOT NEEDED, recorded so nobody chases it

**The scheduler belongs in the todo, not the queue, and strictly speaking is never needed.**
It sat in `queue.md` as a blocker for most of a day and blocked nothing.

**The scheduler is the only thing it runs.** Jobs go through the DOM trigger in
`content/router.js`, which calls `GC.runFamily` and `GC.runPath` directly in the content script —
and content scripts *do* reload on a browser restart. Collection is unaffected.

**The limitation, measured three times and stated once:** a Chrome restart does **not** update the
background service worker. After a clean restart the content script reports the current version
while a `ping` handler added to `background.js` returns `null`. Five routes to force it all
failed — `chrome://` refused by the browser tool, a page-world reload refused by the permission
classifier, `--load-extension` ignored both at the original path and at a fresh copy whose
distinct marker never appeared, and deleting the SW cache refused by the classifier. Likely
Chrome 137 dropping `--load-extension` without a policy.

**What is actually stuck behind it:** the queue, the pacing, and `addAncestor`'s termination —
which is why that investigation could never have succeeded and should not be reattempted until the
worker updates. Unblock signal is a `ping` returning a `pong` instead of `null`.

**Do not put this back in `queue.md`.** The queue is what the work loop takes its next item from,
and a permanent limitation sitting there reads as work.

The item as it stood in the queue, moved verbatim:

- **⛔ THE BACKGROUND SERVICE WORKER CANNOT BE RELOADED FROM HERE. It gates the SCHEDULER only.**

  **Two corrections to what this item said, both measured 2026-09-06.**

  **It does NOT gate the scrape.** The service worker runs the scheduler — the queue, the pacing,
  and `addAncestor`'s termination. The DOM trigger in `content/router.js` calls `GC.runFamily` and
  `GC.runPath` **directly in the content script**, and content scripts *do* reload on a browser
  restart. Scraping needs none of it. This item claimed otherwise and that claim held up the whole
  campaign in the reporting.

  **And it is not simply somebody clicking a button.** A phone has no
  `chrome://extensions` to reload from, and five automated routes were tried
  and each failed with a named mechanism:

      chrome://extensions                       the browser tool refuses chrome:// URLs
      page-world JS reload call                 blocked by the permission classifier
      --load-extension, same path               silently ignored
      --load-extension, fresh copy, marker 9.9.9  marker never appeared -- ignored
      deleting the SW ScriptCache / Database    blocked by the permission classifier

  **The staleness itself is proven, not inferred:** the content script reports **1.4.2** while a
  `ping` message added to `background.js` two minutes earlier returns **null**.

  **The cause is almost certainly Chrome 137 removing `--load-extension`** unless re-enabled by
  policy, which is the most promising route. That is a registry change under
  `Software\Policies\Google\Chrome`, a security-relevant system setting, and is not one for
  this session to make.

  **What is actually blocked by it:** the scheduler, batch pacing, and the `addAncestor`
  termination — which is why that investigation could never have succeeded. Unblock signal is a
  `ping` returning `{pong: "1.4.2"}` instead of `null`.


## 8. A parallel Wikidata tree, built by SPARQL, and provenance throughout

**Provenance is a requirement, not a nicety.** Every fact can come from a Geni export, a Wikidata statement, a
FamilySearch download or order.life, and they disagree. **Links carry it now:** `reports/derived-family-sources.csv`
cites each parent, spouse and child link per source (`S2600`/`S2889`). **Names and dates still do not:** `Merger` keeps
the winning value and the conflict list, not the source file per field.

**A postponed Geni-side merge queue — recorded, not started.** As of 2026-08-07:
**most of the cases where two Geni IDs sit on one Wikidata item are Geni
duplicates that should be merged, but cannot be merged on Geni yet** ("because
Geni's Geni"). `reports/wikidata-doubles.md` already surfaces these pairs side by
side; the eventual Phase-4 output is a *queue of Geni merges* to perform online,
one that only exists once the offline Wikidata tree and its entity resolution
are in place. It is explicitly **postponed until the Wikidata side is offline as
well** — the last thing, not a current task.

### 8b. Checks that wait for the store — offline, after the 500,000

**Nothing here may be answered by querying Wikidata.** Each is a computation over
`wikidata/items/` once the download has finished, and each is written down now
precisely so it does not get "just quickly checked" against the live endpoint.

**Ancient and medieval people with many descendants — the export-picking use.**
The Geni-side version is the descendant-distribution search (item 3/3z): rank by
realized documented descendants to choose where the next `Descendants` exports
run, since the campaign is about **reaching modern times**, not thinness. The
Wikidata store makes the same measurement possible on the other tree, and then a
third thing that neither side can do alone: **where Wikidata holds ancestors of a
Geni person that our Geni tree lacks**, which is both a Geni-side target to
export toward and the input to entity resolution between the two trees.

## order.life: the descent-from-antiquity material

**Recorded 2026-08-14.** `order.life` is chaotic but is expected to **get the link
right** for the cases Geni cannot express — Zerubbabel especially, where
`6000000000961704850` and `6000000206646432835` are the same person and Geni
cannot merge them. It is expected to hold the correct father for him.

It is **not** a source to make our real-life tree from. It carries descent-from-
antiquity material that belongs **in the synoptic tree**, and its content is to be
gone over **later**.

Wikidata should also be getting this right, which is the check to run against the
local store once the pairs are in.

## 9. Future modelling, folded in from `provisional-todo.md` (2026-08-16)

That file was made on 2026-08-15 because `todo.md` was untrusted; this audit is
what it was waiting for, so it comes here and the file goes.

### 9a · Cladoplast — a property plus a role qualifier, once the item exists

The Gaiad's `P59 Cladoplast of` has no Wikidata equivalent
(`reports/orderlife-properties.md` § *Genuinely novel*). The model for it, when
the time comes:

> some sort of other Wikidata property, with a qualifier of *object of statement
> has role* → **Cladoplast**, for when a Cladoplast item exists on Wikidata

So the shape is `<some property>` + **`P3831`** → *Cladoplast*, exactly the
pattern already used for patronymics (`P3831` → `Q110874`). The base property is
**not chosen** and must not be guessed.

**The estimate of when: not soon.** The Cladoplast item will take a long time to be
made, so this is not currently relevant. Nothing is blocked on it.

**Note the distinction that has already been got wrong once:** the Cladoplast
*property* is not the Cladoplast *object*. `queue.md` § 0 lists that among the
corrections a transcript audit has to respect.

### 9b · Gaiad characters — individual citations, eventually

*"Gaiad characters, I don't know what's going to happen with them. My thought is,
eventually, once the Gaiad stuff is better sorted out, the Gaiad stuff is going to
have individual citations."*

**They are not a separate class of person** — everybody here is a human. So `P31` →
`Q5` stays, and no Gaiad-specific typing is emitted.

### 9c · `T999999` — a Gaiad reference that is MEANT to fail

The interim mechanism, and the deliberate part is the point:

> Right now, I am going to say that the best way to do it would be that
> `T999999` is going to be the property for a Gaiad reference. It's going to be
> the thing that's given as a reference for anything that specifically comes out
> of the Gaiad in the JSON files. **This one's going to throw an error, and it's
> intentionally throwing an error.** Because they would be intentionally throwing
> an error, as I understand it, the JSON editor is just going to not be able to
> add it.

So: anything sourced from the Gaiad carries a reference on `T999999`, which does
not exist on Wikidata, so the edit **cannot execute**. That is a fence, not a bug
— it keeps Gaiad-derived statements in the batch, visible and countable, while
making it impossible for one to reach Wikidata before the citation system is
designed. **Do not "fix" it, do not substitute a real property, and do not filter
these entries out of the batch to make it run clean.**

**It is `T`, not `P`, and that was checked.** Written as `P999999` at first on
the reasoning that properties are `P`, and corrected on 2026-08-15: it is not `P`. So the
`T` is deliberate and is part of why the reference cannot resolve. Do not
"correct" it back.

*"We'll figure out the Gaiad citation system at a later point."*

## Research `6000000000757999620`

<https://www.geni.com/people/index/6000000000757999620>

Added 2026-09-17 by instruction. Written down and not investigated — § *"Add it to the end of
the queue" means WRITE IT DOWN AND STOP*.

## Context for later, not work now (filed 2026-09-26)

Filed from the queue as context, on Emma's instruction; none of this is to be started yet.

- **Chinese surnames and their bottlenecks**, for the Gaiad writing.
- **shrines.order.life** for the Shinto wiki scripts, with **temples.order.life** redirecting there.
- **A religious-buildings database beyond Wikidata.**
- **Every deity treated as having a genealogy.**

## QuickStatements ideas Emma is considering (filed 2026-09-27, not work now)

- **Daily QuickStatements that create every individual they are allowed to, in priority order,
  running on indefinitely.** On a good maxlag day that could get a very large number of creations
  done. The cost: a long batch builds a fatter tree inside the pool of eligible individuals.
- **A small second QuickStatements generation started as soon as a ring is fully built**, in
  automatic running. Emma thinks this is probably a bad idea but wants it recorded.

Context: completing the mandatory rings is expected to take about 100 runs (possibly more with
timeouts), and there can be several runs a day.

## Labels in languages beyond English, Japanese, Chinese and Korean (filed 2026-09-27)

Not batch work now: the batches write labels only in `mul`, `en`/`en-us`, `ja`, `zh` and `ko`
(Emma, 2026-09-27). CJK is in by necessity, because a universe of people enforces it; nothing
enforces the rest.

**What was asked, and what was built instead.** The request (2026-09-25, the sixteen-language item)
was never transliteration. It was to set up the pipeline equipment so that, **once each name has an
established canonical representation in a language, the label in that language is COMPOSED from
those representations**, the way the Chinese labels partly use name items' own labels. What was
built on 2026-09-26 was letter-for-letter transliteration engines. That misread the request, and
they are now disabled (commented out in `scripts/translit_scripts.py` and `build-garborg-day.py`,
not removed).

**Transliteration is not easy.** Korean alone took many rounds of fixes to get right. So a letter
table cannot be trusted for Arabic, Inuktitut or Armenian, and the names have to be right.

**The design, for when it is done:**
- a language's label for a person is composed only from canonical forms of each of their names
  in that language, which in practice means the name items' labels in it;
- a person is eligible only when EVERY part of their name has one;
- so it is a long tail: labels appear as names gain canonical forms, possibly over years
  (Inuktitut perhaps a ten-year tail). There is no rush.

**Measured 2026-09-26:** of 8,006 name items, how many already carry a label in each language:
Russian 4,537, Arabic 3,238, Hebrew 2,247, Ukrainian 1,882, Greek 871, Bengali 547, Georgian 255,
Persian 255, Armenian 213, Hindi 165, Tamil 104, Cherokee 38, Inuktitut 37, Amharic 24, Dhivehi 16,
Tamazight 12.

Also deferred: the NN relationship labels in other languages (ca, da, de, es, fr, it, nb, nl, pl,
pt, sv and the rest), and the native generation-suffix labels (`d.y.`/`d.e.`).

**Ruled 2026-09-27 (AskUserQuestion): yes, strictly.** Labels are composed from the name items' labels in every language, CJK included, a language written only when every name part has a label in it; transliteration is phased out over time. The build is a queue item.

- The saved QuickStatements page in "Use this to do a new programmatic daily quickstatements cicd/" (saved 2026-10-03 19:38: the user page with the token-management section and the api.php import instructions) is for later CI/CD: submitting the daily batches programmatically instead of by hand. Not now: it requires us to be better than we are first (Emma, 2026-10-03). The page holds the account's live QuickStatements token, so the folder must never be committed or pushed: (gitignored at `.gitignore:666`, checked 2026-10-05; never committed), and never copy the token into a tracked file, a log or a queue item.
