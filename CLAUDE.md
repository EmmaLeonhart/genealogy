# geni

## Skills

Workflow behaviors live as skills in `.claude/skills/` (auto-discovered by Claude Code):
`emergency-stop`, `cron-is-local`, `autonomous-loop`, `queue-driven-workflow`,
`writing-style`, `cleanvibe-update-check`. They are vendored into this repo and kept
current by the `cleanvibe-update-check` skill.

- **Last cleanvibe update check:** `2026-07-31` — all six skills present, none
  superseded, nothing refreshed. Note the page's newest entry is **v1.15.0**
  while this repo was scaffolded from **v1.17.0**, so the check can only show
  that nothing *listed* is newer than what is vendored here; whether v1.16 or
  v1.17 changed a skill is not something the page currently answers.
- **Updates source:** <https://cleanvibe.emmaleonhart.com/updates.md>

## Project Description

Merge Geni.com GEDCOM exports into one canonical genealogy, then reconcile that
genealogy against Wikidata — and eventually generate the edits that would create
the missing people on Wikidata.

The user's stated direction, in their own framing:

1. Merge the exports into a single tree.
2. Work out the Wikidata connections as far as the data allows, using the Geni
   ID that every record preserves.
3. Later, expand the tree with more exports from Geni — which means finding
   good **branch points** in the genealogy to export from next.
4. Much later, queue up creation of the absent people *on* Wikidata, connected
   to their parents, carrying whatever the genealogy supports: multilingual
   label, English label, Geni ID, sex, and the relationship links. Harder
   pieces they named explicitly: the name/surname *properties*, creating
   Wikidata items for surnames that have none so people can be linked to them,
   and queued edits adding name links to people who already have items.

## Architecture and Conventions

**The Geni profile ID is the primary key for everything.** Geni's export writes
it as the GEDCOM xref (`0 @I6000000087535357291@ INDI`) and repeats it as
`1 RFN geni:6000000087535357291`. Merging is therefore an exact join, never
fuzzy name matching. `genimerge.identity` is the single place that knows this;
`tests/test_gedcom_real_exports.py` asserts it against the real files so a
change in Geni's format fails loudly.

Exactly **four xref prefixes** occur, each bound to one record type: `I` on
`INDI`, `F` on `FAM`, `N` on `NOTE`, `S` on `SUBM` — measured over all **291,439**
xrefs in the exports, re-measured on 2026-08-04 against each batch of new
ones rather than carried forward. Some exports carry no `NOTE` records at all, so
an export need not use every letter; the claim is that no *other* letter appears
and no letter spans two record types. `GENI_ID_RE` accepts only
those on purpose: when it accepted any letters, the foreign xref `@NI04461@`
parsed as Geni ID `04461` and would have produced a URL to a stranger's profile.
**`tests/test_gedcom_real_exports.py` asserts this on every run**, per export,
naming the offending prefix and record type if Geni ever adds a fifth — so it
needs no remembering, and a change breaks the suite instead of quietly changing
which profile an ID points at.

### Open the FAMILY TREE page for an export seed, not the profile page

**Emma, 2026-08-17, definitively:** *"rather definitively this kind of thing
https://www.geni.com/family-tree/index/6000000085113755501 is a better page to open up
for them rather than the pages you opened."*

So a batch of export seeds is opened as
`https://www.geni.com/family-tree/index/<geni id>`, **not**
`https://www.geni.com/people/x/<geni id>`. The profile page shows one person; the
family-tree index shows the neighbourhood around them, which is what she needs in
front of her to create the placeholder and run the export.

**`reports/midpoint-seeds-to-open.tsv` is overwritten every batch, and that is the
intended behaviour.** Emma, 2026-08-17: *"don't make it accumulate overwriting is the
intended functionality lol."* It is the handoff for the batch being opened now, not a
history of what has been opened.

**So there is no already-opened filter.** Each batch is simply the top of the current
ranking. She has said this twice — 2026-08-16, on a filter built for the same reason:
*"I don't know what the already open filter is for… I feel like it might be
overcomplicating things"*, and its bug had cut a candidate list from 778 to 7. Re-opening
a tab she has already dealt with costs her one glance; a filter costs correctness.

Keeping the picks on **disjoint chains** is a different thing and stays: without it fifty
tabs can all be standing on the same three chains, so they buy three exports rather than
fifty.

This applies to **seed batches** — the midpoint openings, the density and edge picks.
It does not change the *isolate* batches, where the thing being judged is whether one
person connects at all, nor the saved-page workflow below, which needs the profile
page because that is where the relationship panel and its `href`s live.

### `docs/export-seed-rules.md` is how an export individual gets made

**Emma dictated the whole method on 2026-08-17** and asked for it written down.
It covers where to put a placeholder profile, what to name it, and what to do when
a tree has no open slots left — a five-tier preference order with patronymics at
the top, because a patronymic names the father and so the created person is
attested rather than invented. It also fixes the export itself: **`Forest`, size
5000, strictly one at a time, and the zips are filed into `exports/` in bulk only
once every one of them is down.**

That file is the authority; do not re-derive any of it here.

**The whole loop runs under Chrome automation now**, proven end to end on
2026-08-17: create the profile in the tree view, Actions → Export GEDCOM, poll the
download page, click through. Emma's framing: *"we've managed to use Chrome
automation to actually completely run my old workflow… all of my human labor
involved with the exports."*

**Relationship paths: save the page, never the pasted text.** A Geni
relationship path — the chain of people between two profiles, which Geni shows
for any pair it can connect — is the only evidence in this repo that comes from
*outside* our own data: it names people whether or not any export has reached
them. Copying the panel as text keeps the names and loses the `href`s, and the
`href`s are where the profile IDs are. **Saving the page keeps them**, so the
workflow is: save the profile page from the browser into `geni_pages/`, then
`python -m genimerge path-from-html <page> -o paths/<name>.tsv`, then
`python -m genimerge path <file>` → `reports/path-*.md` and `path-*.json`.

`genimerge.genipage` does the extraction, and the difficulty is scoping: a Geni
profile page carries several hundred `data-profile-id` anchors — immediate
family, managers, followers — and only those inside `span.segment > span.name`
are on the path. Matching anchors directly yields a plausible-looking list that
is not a path.

**`reports/connectors.md` and `out/connectors.html` answer "who do we lack?"
across all the paths at once.** `python -m genimerge connectors` checks every
path file against one loaded tree — a second `genimerge path` run per file would
pay the whole cost of loading the merge each time, so `--write-paths` refreshes
every `reports/path-*.md` from the same pass. It groups absent steps into
**bridges** (a run of consecutive missing people, plus the doorway to seed on and
the resume point beyond) and merges bridges that share any person into one
cluster. **Rank by slots closed across every path a cluster blocks, never by gap
length**: ten people blocking five paths beat fifty private to one. The report
carries a separate **"one export?"** column because payoff and feasibility come
apart at the top of the table — nine people is the widest gap a targeted export
has closed here, and the highest-slot cluster is routinely wider than that.

**`ABSENT` on a path means "not in the tree" and nothing else.** A person walked
*twice* on one path is `REPEAT`, which counts as held. The two shared a branch
until 2026-08-06 and the cost was not cosmetic: `paths/nn-basse.tsv` holds two
relationship paths end to end, so its second chain re-walks steps 1–9, and the
tool reported **the account owner himself** as a missing person — which
`connectors` then offered as a nine-person bridge worth exporting for. The
`used` rule that caused it is still right for the *name* fallback, where a
second step landing on one profile is a matching error; an exact ID landing
twice is a file holding two paths. `tests/test_paths.py` pins both directions,
including that a repeat of someone genuinely absent stays absent.

`genimerge.paths` **falls back to name matching only for rows with no ID**, and
that fallback is a report for a human, never an input to a merge. Do not let it
become load-bearing: run against the Jimmu path it invented eleven holes in a
run of thirty and moved the headline finding from "stops at step 30" to "stops
at step 2". Its guards exist because of specific failures — a person settled by
one step is never offered to a later one (Jelena Urošević matched Elisabeth of
Hungary, the step before her, reporting the doorway as already held); a name
shared by more than `AMBIGUITY_LIMIT` people is `UNRESOLVED` rather than held,
because 73 profiles are called `n n`; and a row whose ID is simply absent from
the tree resolves to absent rather than falling back to its name.

**Later sources win value conflicts.** Changed 2026-08-04, having been
earlier-wins since the start. Geni is a live site, so two exports disagreeing on
a single-valued path means the profile was edited between them and the newer
export holds the correction. The first conflicts to appear in real data — at 45
exports; there were none at 10 — were all `INDI.CHAN.DATE`, the profile's own
last-edited stamp, where keeping the older value is not arbitrary but wrong.
Merge order is filename order, not export date: if "later" ever needs to mean
"more recently exported", sort the paths by their `HEAD` date before calling
`merge_files` and the rule follows without a code change.

**The xref is the merge key; `RFN` is corroboration checked elsewhere.**
`Merger.add_source` deliberately does not call `geni_id_of`, so a contradictory
`RFN` does not stop a merge. The cross-check runs in `inventory`, in `model`,
and over the merged output in `tests/test_merge_real_exports.py`.

**Exports are bounded, but no number here is the bound.** The first three
exports each hit 3836 individuals exactly while sharing only 354 people, so they
are overlapping slices rather than copies — and that identical count read as a
cap. Every export since has held more. Ordered by the timestamp in their own
`HEAD`, 28 exports read: 3836 ×3 (30 Jul), 3840 (01 Aug), 3844 (02 Aug), then on
04 Aug 3848, 3852, 3856 within twelve minutes — and **3860 for each of the
eleven exports taken between 15:21 and 16:22**. Exports holding less (876, 1073,
1192) exhausted their component before filling.

That flat run of eleven is the part that pays: those eleven came from eleven
different seeds in three different styles and all landed on 3860 exactly, so the
bound is **global, not per-seed and not per-style** — which also rules out the
walk overshooting a floor to finish the generation it is on. Why the ceiling
*moved* 3836 → 3860 over five days is still unestablished. **Do not encode the
arithmetic**: a run of eleven identical values is evidence the number sits
still, not evidence it steps by four on a schedule, and do not describe it as a
cap Geni enforces.

`genimerge.seeds.GENI_EXPORT_CAP` is **5000** as of 2026-08-17, meaning *largest
yet seen*; its docstring is the long form of this, and is where each reading is
recorded — do not update this number without adding the reading there. It was 3860 when the
paragraph above was written, and the sentence about the number sitting still
survived the move rather than being falsified by it — 4008 came from a pair of
exports taken seven minutes apart that held 3972 and 4008, which is a ceiling
that moved, not a step of four. The 99th export (2026-08-06) held 4004 and
changed nothing. The four exports of that evening went 4016, 4020, 4020, 4020
between 18:10 and 18:19, so the ceiling **rose inside a single nine-minute
sitting** and then held for three takes — see
`reports/audit-downloads-2026-08-06.md`. It is a modelling number for
`reports/seeds.md` only — nothing in the merge depends on it.
`tests/test_seeds.py` fails if an export in `exports/` exceeds it, so the next
one to do so is loud rather than silent — that is how 3840, 3844 and 3856 were
each caught. The constant tracks the largest export *seen*, which is not
necessarily one that has been ingested, so the test is a floor on it rather than
its source. Expect to merge many exports over time, and expect the merge to be
re-run rather than hand-edited. See `reports/inventory.md`.

**The merged tree is one connected tree — as of 2026-08-04, and not before.**
105349 people, 56455 families, **1 component**, over 54 exports. It was two
components for most of that day (16217 Norwegian and 11501 Japanese, sharing no
person and no family) and the whole of 08-02..08-04. `reports/frontier.md`
§ Components is the live count and the thing to check rather than this
paragraph: an export that reaches somewhere nothing else does will split it
again, and that is normal rather than wrong. Disjoint components do not
conflict — they just never meet.

### The question is whether OUR TREE MATCHES GENI — never whether Geni is right

**Emma, 2026-08-24, correcting the whole framing of the duplicate work:** *"I think that
you are doing some thinking that you shouldn't be doing about whether the merges should
have been done rather than whether the tree is in a good state... even if the merge isn't
fixed on Geni, I still want it there. I still want the wrong information from Geni there
because it is possible to correct it now."*

**Geni is the source. Our corpus is a stale photograph of it.** The only question a
duplicate, a conflict or an odd relationship raises is: *does our snapshot still match
what Geni says today?* If Geni holds one profile, we should hold one. If Geni holds two,
we should hold two — **even when two is wrong**, because a wrong fact that is present can
be corrected on Geni and flow through, and one we filtered out cannot.

**What this forbids.** Adjudicating whether a merge was justified. Grading a pair as "not
really a duplicate" and therefore skipping it. Deciding an export has "thin expected
value" because the pair looks like two different people. All three were done on
2026-08-24 and all three are the same mistake: answering *is Geni right* when the question
is *are we current*.

**What the evidence grading in `reports/geni-stale-duplicates.tsv` is actually for:**
ranking which snapshots are most stale, so the most valuable refresh runs first. It is not
a filter on which people deserve fixing.

**So a post-merge export is worth running even when the pair turns out not to be a
duplicate at all** — it refreshes our record of those people to Geni's current state, which
is the whole job.

### A small component is IGNORED. Do not report it, do not analyse it

**Emma, 2026-08-17:** *"if there's a cluster of 344 people you fucking ignore it and add
to claude.md"* — and, on being told the merge had split into 472,655 and 344: *"this
isolated group of 344 people, they aren't in the chains, are they? They're not in the
chains, and because they're not in the chains, it means you shouldn't even be analysing
them."*

**She is right and it is checkable: 0 of those 344 appear in any of the 586 relationship
paths.** Every path starts at her own profile, which is in the large component, so a
small component cannot be on a chain — that is what being a separate component means.
The work is clearing chains, so a group off the chains is not small-priority, it is **no
priority**.

**So the merge's component count is not a finding and does not go in a report to her.**
The line the merge prints is fine where it is. Mentioning it in a status update, working
out what is in it, or wondering which export brought it — all of that is the unprompted
analysis § *No unprompted reports* forbids, and it cost her a turn to shut down.

`reports/frontier.md` § Components stays as the place the number lives for anyone who
ever needs it.

**How it was joined, because the method generalises.** `reports/path-jimmu.md`
checks an 83-step Geni relationship path against the tree. It went 62/83 held
(gap of 21 steps) → 77/83 (gap of 6) → **83/83, every step held**. Two `Forest`
exports seeded inside the six-person window closed it. Note the style mattered:
that stretch of path crosses `her brother`, `his partner` and `her husband`
links, so `Ancestors` and `BloodTree` would have walked straight past
Guarandukht Bagrationi and Sultan Alp Arslan and never bridged. **When an export
is meant to close a specific path, read the relation column first and pick a
style that follows those link types.**

**An export is named for its style, not its seed — so filenames collide.** Geni
writes `export-<style>.ged`, and **five** styles have now been seen: `Forest`,
`Ancestors`, `BloodTree`, `Descendants` and — first seen 2026-08-06 21:33 —
**`Bio`**. This paragraph said "four" until that file arrived, which is worth
noting as a caution rather than a correction: nothing enumerates the styles, so
a sixth would land silently. What `Bio` selects for is **not established** and
should not be guessed; the one export of it holds 4056 people, the same as the
`Descendants`, `Ancestors` and `BloodTree` takes minutes either side of it, so
its size says nothing about its shape. The first three exports are all three
styles of the *same* seed, Emma Leonhart `6000000087535357291`, which is also
their `SUBM` xref. A second `Forest` export from a different seed therefore
arrives with a filename already taken. Disambiguate by appending
the seed's Geni profile ID — `export-Forest-6000000226977233850.ged` — since the
profile ID is this repo's primary key. Note the `SUBM` xref is the *account
owner*, not the seed, so it cannot be used for this.

**The seed is the file's first `INDI` record**, and this is checkable rather
than assumed: of the saved pages in `geni_pages/`, seven are the first `INDI` of
some export and the rest are pages saved for connections not yet exported from.
**Do not expect the seed to be the person the export is named after in
conversation.** All three exports ingested on 2026-08-04 open on a profile
created a minute or two before the export ran — `export-Forest-6000000227036288825.ged`
is "the Li Hong export" and its seed is an `NN` wife of Li Yuanfeng created at
14:40:46 and exported at 14:41:36. Creating a placeholder at the frontier and
exporting from it is the technique; the filename records the seed, not the
intent.

**`reports/density.md` is where to look for the next export, not
`reports/seeds.md`.** `genimerge.density` counts how many exports contain each
person — **presence** — and then finds *connected runs* of people almost no
export reached. One thin person is the rim of a ball and means nothing; a run of
thousands is a neighbourhood sampled once and never returned to. `seeds.md`
ranks by doorway count and has never been validated against an outcome; density
is measured from what the exports actually did.

**The `Descendants` campaign is about time, not thinness — Emma's own framing,
2026-08-06.** She is running `Descendants` exports because **the tree is biased
towards ancient and medieval individuals and she is trying to reach modern
times**. That is a different target from `reports/density.md`, which ranks by
how few exports touched a neighbourhood and knows nothing about dates. The two
can point the same way and often will, but do not present density picks as
serving this goal, and do not describe her `Descendants` takes as thin-region
work. `Descendants` fans out downward, which is what makes it the instrument for
reaching later generations.

**A `Descendants` export reaches about twelve generations forward, and that
outranks every seed heuristic — measured 2026-08-07.** The export is a
breadth-first ball of ~4076 people, so it fills the generations *nearest* the
seed; a descent branching twice per couple hits 4096 at generation 12 unaided.
So a ball carries roughly **350 years** and no choice of seed changes it.

Emma's batch of **eleven** `Descendants` exports, all seeded on ancient or
undated people, added **18,218 people** — median birth year **1582** — and
**four** born after 1900. The 1500s gained 3,369, the 1600s 3,045, the 1800s
101, the 1900s 4. **No person born 1800 or later gained a child, of 14,371.**
The campaign is about reaching modern times and this did not move it.

**So: seed where you want to arrive.** To deliver people born after 1900 an
export must be seeded after about 1750. `genimerge.descendants.REACH_GENERATIONS`
and `REACH_TARGET` encode the screen, and `reports/descendants.md` leads with
§ *Seeds that can reach 1900*. Everything else in that report is background.

**The campaign's seeds are 1800s people, measured not argued.** Of the 7591
candidates a ball can get to 1900 from: 1500s 605 (8%), 1600s 1426 (19%), 1700s
1777 (23%), **1800s 2980 (39%)**, 1900s 803 (11%). Two independent reasons put
the answer there rather than later — a seed born 1850 needs two or three
generations to pass 1900 and has them to spare, and **Geni redacts living
people**, so a 1900s seed's descendants largely cannot be exported at all. The
1800s are the last cohort whose full descent is retrievable, not a compromise.

**One seed per couple — `drop_duplicate_balls`.** Two parents of the same
children have the same descendants, so a `Descendants` export from either
returns the identical ball. This is not an edge case: the ranking rewards a
large recorded family and both parents of one score alike, so **a quarter of the
shortlist was the same export listed twice** (10071 → 7591). Ranks 1 and 2 were
Margaret Outlaw and Samuel D. Outlaw, a married couple with the same 20
children, offered as two suggestions.

**`out/reach-1900-seeds.html` is the thing to actually use** — 600 candidates,
filter by decade, sort by any column, pick by eye. Emma asked to "arbitrarily
look over" them and that is the right instinct given the ordering is untested;
the page says so on itself. Read `line reaches` against `ball reaches`: the gap
is roughly what an export would add.

**Two seed-choosing methods have been refuted by measurement. Do not propose a
third on reasoning alone.** `reports/descendants-backtest-2026-08-07.md` is the
record, and it exists because `out/merged-134.ged` was kept before the batch was
merged — **keep the pre-batch tree whenever a batch lands**, it is the only way
this question is answerable.

- *"Small but nonzero descent"* — refuted. All ten seeds that already existed had
  **exactly one recorded child** and descent-path counts from 371 to **1.5
  billion**, every one outside the 1–20 candidate band. The report would not
  have proposed any of them.
- *"The rim of a cut-off ball"* — proposed and refuted the same day. Childless
  people inside an export that came back at the size bound gained children at
  **0.71%**, *below* the 1.00% base rate and below the 1.05% of people on no rim.
  It anti-predicts. The test is indirect, so it refutes the premise rather than
  the tactic — but the method was going to be presented as an improvement on
  reasoning alone, and that is exactly what is no longer allowed here.

**`reports/descendants.md` is the report built for that campaign** — added
2026-08-07 on the `geni-descendants` branch. `genimerge.descendants` ranks the
**downward** edge the way `frontier` ranks the upward one, and buckets it by
period so the ranking can be read one century at a time.

- **The signal is a descent-path count that is small but nonzero**, and both
  halves carry weight. *Nonzero* means Geni recorded at least one child, so the
  line demonstrably continues and there is something below to follow. *Small*
  means we have barely followed it. A person with **zero** recorded descendants
  is deliberately excluded: nothing in our data separates childless from
  unexplored, which is the same discriminator `density` applies upward with its
  doorway column.
- **Count descent paths, not distinct people — Emma's call, 2026-08-07.** The
  measure is her recursion, `paths(p) = Σ over each recorded child c of
  (1 + paths(c))`. Somebody reachable down two lines counts **twice**, and that
  is the point: the question is how many lines come down from a person, and a
  descendant reached twice is two lines. She ruled distinct-person counting out
  as not merely irrelevant but plausibly *worse* here — pedigree collapse is
  dense in this tree, and de-duplicating it makes the top of a wide,
  repeatedly-intermarried descent look narrow. `frontier.descendant_counts`
  still counts distinct people for callers that want that.
- **Rank on `generations followed` (`depth`), never on `stall`.** Stall — years
  between the line's last recorded birth and now — was the first ranking and is
  a trap: a person's own birth year is a floor on how far their line reaches, so
  sorting a 100-year band by stall sorts it by birth year, and **every band's
  top pick came out born in the band's first year**. That is where the band edge
  fell, not a finding. Depth is available for dated and undated people alike and
  does not move with the band. Stall stays as a column worth reading.
- **The path count is why this module is cheap, and it was not always.**
  Distinct-person counting needs a set union per person: `frontier` carries a
  bitmask, one bit per person per person, a kilobyte each at 8766 people and
  32 KB each at 257219 — tens of gigabytes. This module carried a capped walk
  and a `descendants_exact` flag to work around that. Emma's recursion is a
  plain post-order sum, O(V+E), exact at every size, and deleted all of it. The
  sums saturate at `PATH_CEILING` (1e12) because path counts compound through
  shared subtrees and a deep intermarried ancestor's true count runs to
  thousands of digits; that is a display bound thirteen orders of magnitude
  above any usable `small`, never a candidacy one.
- **A candidate whose parent is also a candidate is dropped, per band.** An
  export seeded on the ancestor covers the descendant's line plus branches off
  it we never saw, so the ancestor is strictly the better seed and a six-person
  line would otherwise be reported six times. Checking parents alone suffices,
  because path counts rise strictly upward — a parent's count is at least
  `1 + child's`. Per band rather than report-wide, so a band keeps its own best
  pick.
- **A depth of 0 must mean "no children", never "the child is in a cycle".**
  `_post_order` drops an edge back into a node still being expanded — right, a
  person is not their own descendant — and both depth functions then guarded
  with `if c in depth` and fell through to `0`, which reads as *childless*.
  Depth is `descendants`' primary ranking key **ascending**, so those people
  sorted above every genuine candidate: `Arne` (`6000000007351784249`), one
  descent path and no open ends, held the top of the `undated` band of 136953.
  **8** people of the 123256 with a recorded child were affected — a tiny
  population with an outsized effect, because being ranked first is a position
  of exactly one per band. `frontier.ancestor_depth` is the same eight lines
  with `parents` for `children` and had it identically (**5** of 208863),
  invisible only because nothing ranks on it. Both now contribute `0` for an
  unresolved neighbour rather than nothing, so a cycle *truncates* the measure
  instead of falsifying it. This is the same shape as the date parser's
  silently-dropped years: **a guard against a malformed case, paid for with real
  values that then vanish without trace.** The tree holds 15 ancestry cycles
  across 55 people — `frontier.ancestry_cycles` reports them.
- **The metric change moved the implementation, not the answer.** Candidates
  went 52196 → 52171 and the per-band picks barely shifted: path counts and
  distinct counts coincide almost exactly at the small end, because a line of
  twenty people rarely re-converges. They diverge in the tail, where this report
  does not look. Descent paths are right because they are the right *question*,
  not because they reranked anything — do not cite a numbers change as their
  justification.
- **Both axes are reported because neither covers everyone.** 53% of the tree
  carries no birth year, and those people are invisible to the period view.
  Generations-above ranks them — but it is **not a second clock**: it measures
  how far *we* have traced upward, so an untraced person looks shallow whenever
  they lived. No date is ever inferred.

### The NN/Private label algorithm applies to EVERY unnamed person. It is not optional

**Emma, 2026-08-24, when asked whether three redacted people should be created
unlabelled:** *"THERE IS LITERALLY A SUPER WELL DOCUMENTED ALGORITHM I TALKED ABOUT FOR
AGES AND ASSUMED THAT EXISTED INVOLVING NN AND FORMULAIC CONSTRUCTION IN MULTIPLE
LANGUAGES FOR PEOPLE WITH PRIVATE OR NN OR UKJENT OR WHATEVER."*

She is right, it is documented two sections down, and the question should never have been
asked. **"Create it with no label" is not one of the options.** The algorithm is:

    mul  NN Garborg                                  <- marker + the surname, which survives redaction
    en   son of Arne Olaus Fjørtoft Garborg          <- formulaic, from the nearest named relative
    nb   sønn av Arne Olaus Fjørtoft Garborg
    ja   アルネ・オーラウス・フョルトフト・ガルボルグの息子
    zh   阿尔内·奥劳斯·夫约托夫特·加尔博格之子

**`scripts/build-nn-label-batch.py` owns the language table** — ten languages with the
right relationship word per sex and the right preposition per direction (`datter af` but
`mor til`). Import it; do not restate it. It excludes Slavic and Welsh because they
inflect the name after the relationship word, and it excludes `ja`/`zh` **only** because
the relative's name is usually not transliterated — where it is, as in the Garborg family,
they are emitted.

**`PRIVATE`, `NN`, `UKJENT` and the rest are one population.** Emma: *"NN and private are
the same thing here, because if there's a private individual whose name is not exported,
it comes out as an NN."*

### Redacted people go in. `Private` never becomes a label

**Emma, 2026-08-14:** *"Even if the data is affected by redaction, I'm not really
that against the data getting onto Wikidata because it still is informative, like
the so-called private names."*

**Geni has TWO redaction markers and they withhold different amounts.** Of the
corpus's 390,560 profiles:

| form | count | what survives |
| --- | ---: | --- |
| `Private` | **16,402** | nothing; the whole name is gone |
| `<private> /Surname/` | **3,605** | **the surname is real data** |
| `NN` or blank | 772 | nothing |

`<private> /HUÁNG 黃/`, `<private> /Rådestad/`, `<private> /Larsson/` — the
**given name** is withheld and the family name is not. Treating those as fully
redacted throws away 3,605 surnames, which is the material Emma called valuable:
*"they still do flush out the wiki data, and they flush it out by a substantial
amount."* `surname_of()` exposes it; a bare surname is not a person's label, so it
feeds the `P734` family-name work rather than the label.

- **The person is created.** What is informative is the structure, and none of it
  is redacted: the Geni ID, the sex, the parents, the children, the dates.
- **The item gets no label.** "Private" is a redaction marker, not a name, and an
  item labelled that asserts something false while being impossible to find. The
  `P2600` is what makes it retrievable.

`scripts/labels.py` is the single place that decides this — `label_for()` returns
`''` for `Private` and `<private>` **and nothing else**. It briefly also emptied
`NN`, `unknown` and `?`; Emma, same day: *"I didn't tell you to do that. I didn't
tell you to avoid the NN people."* `NN` is *nomen nescio*, a genealogist saying
the name is unknown — a real statement about a person, not Geni withholding data,
and whether it becomes a label is a decision rather than a string to add to a set.
A caller that falls back to the raw
string when it gets `''` reintroduces the whole problem.

**This is the same rule as the Samaritan "wives" in `docs/future-modelling.md`,
with the opposite outcome, and the difference is what to check for.** `daughter
of Sanballat the Horonite` is also not a name — but she has no identifier and no
structure, so there is nothing to create. A `Private` profile has both. The test
is never "is the label bad", it is "is there anything real underneath it".

**Do not confuse redacted with unnamed.** The seed of
`exports/samaritans/export-Forest-6000000178794141887.ged` is
`NN /bint Aabed-El ben Asher ben Matzliach/` — that is how she is *recorded*, not
Geni withholding a name it holds. Her record comes through complete. Only 29 of
that export's 4,820 people are `Private` at all, so an export seeded on a living
person is **not** substantially redacted; assuming otherwise was wrong when it
was assumed here.

### `NN` is PRESERVED in `mul`. Descriptive labels are ADDED in other languages

**Emma, 2026-08-16:** *"NN is not relabeled. Why are you thinking that I'm saying
that it's relabeled? NN is always preserved in the multi-language label. It just
has more descriptive labels added in some languages for the relationships."*

So the shape on a Wikidata item for an unnamed person is **both**:

    mul  NN                              <- the marker, never removed
    en   daughter of Fujiwara no Tadaki   <- descriptive, added

**This nearly went wrong at scale.** `build-nn-label-batch.py` emitted
`set_label` on `en` with `"replaces": "NN"`, and NN lives in `en` on **1,549** of
the 1,588 such items and in `mul` on only **278** — so the batch would have erased
the only copy on 1,271 items. Measured over the store, not supposed:

    en 1549 · nl 671 · mul 278 · cy 25 · be 6 · pl 4 · ru 3 · da 3 · ca 3

The fix is two edits per item, the `mul` one declared as a dependency of the `en`
one, so the marker is written before the slot holding it is reused. An item whose
`en` already says something real is left alone (36 of them).

**`Private` and `NN` are the same population and get the same treatment.** Emma,
same message: *"NN and private are the same thing here, because if there's a
private individual whose name is not exported, it comes out as an NN."* The rule
one section down — *`Private` never becomes a label* — was right about what must
not be written and wrong to stop there: emptying it leaves an item with no way to
be read at all, which is the same objection. **Neither marker is a label; neither
person is left unlabelled.**

### Emma not replying means she is content. It is NEVER a block

**Emma, 2026-08-16:** *"Is there anything else that you treated me not responding
to as being a block? Because generally speaking, when I'm not responding to
anything, the assumption should be I'm happy with what you're doing."*

Showing her cases — which `CLAUDE.md` § *How this project works now* requires
before generalising a rule — is **not** a request for permission. Show the records,
then keep going. If she disagrees she says so, loudly and immediately; that is the
one thing this project can rely on.

**The failure this is written against.** `scripts/walk-structural-merge.py` ran and
wrote `reports/structural-correspondence.csv` (3,902 rows) and
`reports/wikidata-structural-placeholders.json` (12,260). Eight sample rows were
printed for her to eyeball. She did not reply, and **six consecutive status reports
carried "8 structural merge cases unanswered — 3,902 correspondences and 12,260
placeholders blocked behind it"** as the largest blocker in the repo. Nothing was
behind it. The files were on disk the entire time.

Related: a decision that is genuinely mine — the 207 name strings where one
candidate item is far better populated than the other — gets **taken and recorded**,
not parked on her. Asking is reserved for what § *One name item per USAGE* names:
a real ambiguity in what she wants, not a judgement call I would rather not own.

### A start date is not a blocker

*"no wikidata edits until September 1"* (2026-08-14) is a date on which execution
begins. Emma, 2026-08-16: *"Waiting until September, until the stuff is
implemented, that's not blocked on user action. That's literally not blocked at
all. It's just waiting to get started. Literally none of the entire fucking
programme waits until September to execute. Nothing is blocked."*

Every batch builds, is reviewed and is committed now. Do not tag the date
BLOCKED-ON-EXTERNAL, BLOCKED-ON-USER-ACTION, or anything else from the not-done
taxonomy — it is not a not-done item, and calling it one made a plan of hers look
like something outside anyone's control.

### A second Geni ID on one Wikidata item is NOT a conflict

**Emma, 2026-08-14: *"it is impossible to merge these geni profiles, simple as
that."*** Two Geni profiles for one person is a permanent, structural feature of
Geni, not an error to resolve, and a second `P2600` on a Wikidata item is the
correct representation of it.

**Why it happens:** Geni has rules against connecting biblical people to living
people. So users who want their line to reach antiquity keep **creating fresh
biblical profiles** and attaching to those instead. The duplicates accumulate and
cannot be merged. Emma's words for what a second ID means: *"it usually means
that the person just isn't properly done that way."*

Known pairs, both unmergeable:

| person | profiles |
| --- | --- |
| Aaron | `6000000000792907064` · `6000000227239142939` (`Aaron I /Samaritan High Priest/`) |
| Zerubbabel | `6000000000961704850` · `6000000206646432835` (`Zerubbabel-PLACEHOLDER`) |

**So: emit the second ID as an additional `P2600` statement. Never replace the
first, never hold it back as a conflict, never build machinery to adjudicate
it.** `P2600` is multi-valued and the local store already counts **2861 items
carrying more than one Geni ID** — this is ordinary. **751 of those second ids are already
DEPRECATED on Wikidata**, so the live count is **2,110**; `out/wikidata/relations.tsv` drops
deprecated statements and `out/wikidata/p2600-all.tsv` does not, which is the whole difference
between the two numbers and is worth knowing before quoting either.

**Of the 2,110, only 70 have both profiles in our corpus** — everything else we can say nothing
about. `scripts/classify-multi-p2600-by-tree.py` sorts those 70 by what our own tree records
between the pair, and it needs no browser: **41 have no relationship recorded** (the Zerubbabel
shape), **27 are siblings** (the Sapiega shape — Geni holds two people, Wikidata holds one, and
our snapshot matches Geni so there is nothing to do), and **2 are parent-child**, which is a
generation collapsed into one item and the only residue worth opening a page for. It is also the general rule
one section down: *prefer adding a second statement cited to Geni over editing
the existing one*.

`scripts/build-geni-wikidata-pairs.py` implements this; a run that reports these
as "conflicts" has regressed.

### "Is X present?" means BOTH stores. Answer for each, and name which

**Emma's rule, 2026-08-14, after a whole session was lost to the ambiguity.**
When she asks whether somebody or something is *present*, she is **completely
agnostic between Wikidata and Geni**. She is asking whether it exists in the
material this project works with, not which container it sits in. So:

- **Check both.** The corpus under `exports/` (plus `gedcom/`), and the local
  Wikidata store under `wikidata/items/` with its index in
  `out/wikidata/store-index.sqlite3`. Never one and report as if it were the
  question.
- **Say which store each answer is about, in the answer itself.** "Not present"
  with no store named is not an answer, it is a trap. "On Geni: 35 profiles, in
  `exports/gaps/export-Bio-…`. On Wikidata: none of the 35 carry an item."
- **Say when the absence is bounded.** Our exports are a sample of Geni, so
  absent-from-corpus never means absent-from-Geni. The Wikidata store is a
  *Geni-shaped slice* — 1,408,402 items seeded from P2600 holders and their
  neighbours — so absent-from-store never means absent-from-Wikidata. Both
  limits get stated, not implied.

**How it went wrong, because the shape recurs.** Asked whether the pre-1600s
Samaritan high priests existed, the answer given was scoped silently: first to
Wikidata (0 of 35 linked), then to `order.life` (0 of 35), each true, neither the
question. Emma had **built that tree on Geni herself** and heard "they are not
present". The 35 were in the corpus the whole time.

**Join on the Geni ID; do not search by name.** The same session grepped for
`Shalma|Tabia|Abta` — names from the *modern* end of the family — and missed 35
priests called Hezekiah, Akabon and Netaniel entirely, while matching
`Shalmaneser V`, an Assyrian king, across six exports. A later grep for `Abisha`
returned `Abishai` and `SHATABISHA Chandra`. The Geni profile ID is this repo's
primary key on **both** sides: `store-index.sqlite3` has a `geni` table keyed on
it, and `order.life`'s `wikibase/analysis/persons.tsv` carries a `geni_id`
column. Every one of those joins is exact and instant. Reach for the join first
and the name search never, except to pick candidates for a join.

**Presence measures our sampling, never Geni's content.** A thin region is one
*we* barely covered. Whether Geni holds more there is precisely the unknown an
export resolves — reading it as "Geni has little here" is backwards. The doorway
column is the discriminator: many parentless people means under-sampled, few
means possibly just a small family that ended.

**"Region" is a neighbourhood in the family graph, never a place.** Emma was
explicit about this. Do not classify people geographically: birthplace strings
are mostly absent, and inferring a place from a name is the fuzzy matching this
repo refuses everywhere else.

**A clan name is not a clan — measure the neighbourhood, not the surname.**
`reports/hata.md` is the worked example, 2026-08-06. "Do we have the Hata clan?"
was asked by counting people whose name carries 秦 or `Hata`, which over-counted
by 31 (秦州成紀 and 秦州清水 are a *Chinese place* in the surname field) and
implied a population Geni does not record. What answered it was walking one hop
out from those people along every parent, child and spouse edge **ignoring names
entirely**: the whole structure is 41 people, a father-to-son thread with two
clan exits and a single marriage. Reach for the neighbourhood walk first; the
name screen is at best a way to pick seeds for it.

**`SURN` is not reliably a surname, and `_MARNM` is not reliably a married
name.** `_MARNM` *is* the married name — Emma, 2026-08-11, and it is confirmed on
the female records checkable against history (Judith `/de France/` → `Flandre`).
But 244,392 of 444,874 `NAME` records carry the tag and most are not doing that:
31% duplicate `SURN`, **43% are the only surname on the record** because `SURN`
is empty, and the 25% that differ are **53% male**. So neither field can be read
alone. The trap for P734 is the CJK shape — `SURN 陳郡陽夏` (Chen commandery,
Yangxia, a *place*) against `_MARNM 謝` (the Xie clan surname), the same
inversion as the 秦州成紀 case above, and the wrong way round from what a
surname mapping assumes. `reports/names-spec.md` § `_MARNM` is the long form.
Which Geni input field feeds which tag is inference from the export, not
established.

**Zero recorded marriages after a `Forest` export is evidence, not a gap.**
`Forest` follows spouse links — that is why the style gets specified for
targeted exports — so a `Forest` ball that returns no marriages has found none
to follow. An `Ancestors` or `BloodTree` export can hide wives; a `Forest` one
cannot, and that asymmetry is what let the Hata question be settled rather than
left open.

**`entity_resolution.md` is Emma's scratchpad and must stay free-form.** It
holds Geni-to-Wikidata identities she recognised by hand plus label corrections
she wants — evidence no query in this repo can produce. `genimerge.entities`
parses it; `python -m genimerge entity-resolution` writes
`out/wikidata/entity-resolution.qs`. **Do not reformat the file to suit the
parser.** When an entry is not understood the parser reports it and the fix is
to teach the parser, which `tests/test_entities.py` pins by asserting the real
file parses with zero unparsed entries. Entries are grouped by "one Geni profile
and one Wikidata item, greedily" — *not* by blank lines, which was tried and
split one of Emma's entries into two unparsable halves.

**`reconcile` is deleted, and name matching does not come back.** Emma ordered
the name-search matcher removed on 2026-08-12 — *"no fucking clue why there's a
fuzzy matcher that sounds like something you made with zero consent from me"* —
and on 2026-08-15 chose to delete the whole module rather than strip it, along
with `genimerge reconcile` and `genimerge expand`. It held a live Wikidata
client, which is the other reason: a command that queries on a keystroke is how
the 2026-08-07 rate-limit incident happened. The four offline pieces that other
modules still need moved to `genimerge.matching` — two year tolerances,
`year_of` for **Wikidata** time literals, and `distance_from_matched`. Nothing
in `matching` makes a request and nothing in it compares names.

`out/wikidata/matched_p2600.csv`, `matched_all.csv` and `candidates.csv` were
its outputs and nothing writes them now; `coverage`, and the online branches of
`crosscheck`, `name-links` and `quickstatements`, read them and therefore have
no input. The offline replacement is the P2600 map, `out/wikidata/p2600-all.tsv`,
plus the downloaded item store — which is what `crosscheck --offline` already
uses.

**Stdlib only.** `urllib` covers the Wikidata SPARQL endpoint. Add a dependency
only when the stdlib genuinely cannot do the job.

**Layout.** `exports/` **the corpus** — every Geni export, one directory per
batch, read recursively · `paths/` relationship paths generated from saved pages
· `geni_pages/` saved Geni profile pages · `src/genimerge/` the package ·
`reports/` generated reports worth keeping in git · `out/` generated data, **tracked**
· `tests/` pytest.

**`out/` is NOT gitignored, and that is deliberate.** This line said "gitignored" until
2026-08-25 and it was stale — Emma un-ignored it on 2026-08-15: *"Oh my god why the fuck is
it gitignored? Un gitignore"*. The old `out/*` rule cost real work: the Wikidata
download-state index lives there, a restart lost it, and the downloader believed all
514,876 seeds were unfetched while 1.4M items sat on disk. **Only the files GitHub
physically refuses are ignored, one explicit line each** — `out/merged.ged`,
`out/merged-*.ged`, `out/wikidata/download-state.sqlite3`,
`out/wikidata/store-index.sqlite3` and `out/wikidata/labels.tsv` (187 MB, rebuilt by
`scripts/extract-wikidata-labels.py` in ~10 min) — all rebuildable, so the cost is a rebuild and
never data. `out/wikidata/relations.tsv` (65 MB) and `dates.tsv` (18 MB) are under the limit and
stay tracked, so a clean clone can run the zipper after one labels rebuild.
`.gitignore` line 32 carries the reasoning.

The stale word was not harmless: it was quoted back at Emma as grounds for adding `out/`
to `.gitignore`, and she approved a change that would have undone her own instruction.
The `.gitignore` was right and the documentation was wrong.

**`exports/excluded/` is the one part of `exports/` that is NOT corpus.** Added
2026-08-15. An export lands there when Geni has since **changed a relationship it
records**: the merge unions `FAMC`/`CHIL` and never drops one, so a parent link
Geni has deleted survives forever once any export carries it, and no later export
can undo it. Excluding the file is the only mechanism that removes it.

**The files stay in git** — the never-delete-a-GEDCOM rule is untouched. They are
tracked, readable, and still the record of what Geni said that day; they are only
kept out of the merge. `genimerge.sources` skips them and `excluded_files()`
lists them.

**The condition is checked now, never predicted.** Emma, 2026-08-15, rejecting a
proposal to exclude them *once* a later export covered their people: *"That is
stupid. It's a prediction of something that may or may not happen. I want you to
move them into an excluded directory… and check to see if every single individual
there is present in at least one other export."*
`tests/test_repo_invariants.py::test_no_excluded_export_strands_a_person` is that
check, so an exclusion that would drop somebody from the tree fails the suite.

**The worked case, `excluded/samaritans/`** — four exports taken before
`Yitzhaq I ben Tsedaka` (`6000000227245553985`) existed on Geni. Geni had linked
**Tsedaka II → Abram** directly, skipping him; when Emma created him, Geni
rewrote family `F6000000178795360833` **in place**, swapping its child from Abram
to Yitzhaq I. Merging old and new gave that family both children and gave Abram
two fathers, one of them the other's father. They became excludable only when
`export-BloodTree-6000000178794141887.ged` arrived and covered the last **1,091**
people — before it, exclusion would have lost Zipporah, Gershom, Eliezer and the
Itamar-line placeholders. **Do not treat this as licence to exclude an export for
disagreeing with another.** Two exports differing on a *value* is the
later-wins rule; this is Geni having deleted a *relationship*, which nothing else
can express.

**`exports/` is the corpus and is read recursively — there is no ingest step.**
Geni's downloads land as `export-geni (N).zip`, extracted beside themselves,
grouped into a directory named for the person Emma exported from
(`exports/Li Hong/`, `exports/n n/`) or into `exports/archive/`,
`exports/fleshing-out/` and `exports/edges/` for bulk takes. **103 GEDCOMs as of
2026-08-06 evening.** In a bulk directory holding one style from several seeds,
name by seed ID rather than by download number — `exports/edges/` does this,
because `N` is a per-directory label and the seed ID is the repo's primary key. Those subdirectories are filing and mean
nothing to the merge: every `.ged` beneath `exports/` is corpus the moment it is
extracted. Inside a bulk directory the zip keeps its download name and the
GEDCOM goes to `export-geni/export-<style>-<N>.ged`, where `N` is the zip's
download number — a local label for that batch, not a Geni identifier, and
meaningless across directories.

**Correcting her own record in an export does nothing until the tree is
re-merged, and nothing after that until `build-display-names.py` re-runs.** Learnt
2026-08-16. The chain is long and every link caches: `exports/*.ged` →
`out/merged.ged` → `reports/display-names.csv` → `reports/derived-labels.csv` →
every label emitter. Fixing the exports and regenerating `derived-labels.csv`
left the old surname in place, because `derive-labels.py` reads
`display-names.csv` and **does not build it** — `build-display-names.py` does, and
that is the only script that reads the merged tree. Running the analysers is not
running the generator.

**Every GEDCOM is committed. Never gitignore a `.ged`.** Tracking the exports is
what this repo is *for*, and disk size is not a reason to lose that. This is
written down because it was got wrong: `6eddadd` moved 37 exports out of git on
a size argument (~200 MB), one `.gitignore` line per file, and the stragglers
batch added four more the same way. Nothing was deleted — all 98 stayed on disk
— but a clean checkout then received **57** and silently measured a smaller
corpus than every report in `reports/` describes, which is how a cloud session
came to report 57 against reports claiming 94. `91cf363` removed those 41 lines
and committed the files; `git ls-files 'exports/**/*.ged'` and
`find exports -name '*.ged'` now both give 98, and
`tests/test_repo_invariants.py` fails if they ever diverge again. The **zip**
lines stay, one per line, for the reason they always had — an unignored zip in
`git status` is the signal that a download has arrived. Working in
`reports/audit-corpus-sync.md`.

**`genimerge.sources` is the only place that answers "which GEDCOMs are the
corpus?"** It used to have six answers — `cli.Workspace` globbing `data_lake/`
and five test modules each rebuilding the same glob. It **drops byte-identical
repeats**, which matters because the same export arrives twice routinely: the
merge would not care, being keyed on the profile ID and idempotent, but
`inventory`'s overlap figures and `density`'s presence counts both divide by how
many exports contain a person. Order is by path, which is deterministic but is
**not** export order — the same caveat that has always applied to "later sources
win".

**There was a `data_lake/` and it is gone (2026-08-05).** It was scaffolding
from the first session for sorting a pile of dropped zips, and it accreted a
naming scheme, an ingest ritual and a rule that the merge read from it and
nowhere else — none of it ever decided, all of it meaning a freshly downloaded
export was invisible until copied to a second place under a third name. Its five
unique files are in `exports/originals/`; the other 49 were duplicates of files
already under `exports/`. Do not reintroduce a second store.

**Two exports can share a style *and* a seed, and then the name collides.**
Seen on 2026-08-05: two `Forest` exports of `6000000227040338177` taken seven
minutes apart, 3972 people and 4008. Check containment before inventing a
disambiguator — the 3972 was a strict subset of the 4008, so keeping only the
larger lost nothing.

**Never overwrite an existing `.ged`. A new export is always a NEW file.**
Emma's rule, stated 2026-08-13 after it was broken. `cp`-ing a freshly
downloaded export **on top of** an existing tracked `.ged` clobbers a committed
file, and that must never happen. When placing an export, if the destination
path **already exists**, STOP — do not overwrite it. The download goes somewhere
as its own new file (its own seed-named path, or the bulk directory Emma names,
e.g. `fleshing-out/`), and where it goes is **her call, not a default to guess**.
Ask. This was got wrong when a 13 AUG re-export of the Ogasawara Descendants
seed was `cp`'d over `exports/descendants/export-Descendants-6000000227040613855.ged`
— it belonged in `exports/fleshing-out/` as a new file, and the committed
descendants copy had to be restored from git. Two exports sharing a seed *and* a
style is a filing question to raise, never a licence to overwrite. **Before any
`cp`/`mv`/`>` onto a path under `exports/`, check it does not already exist.**

**The one exception, and it is narrow: a BYTE-IDENTICAL duplicate.** Emma
authorised this on 2026-08-16 — *"Yes delete it"* — for
`export-Descendants-6000000178898487831.ged`, which existed twice with the same
sha256 `2e2f87a6…`: the original in `exports/descendants/` from 13 AUG and a
re-download filed into `exports/edges/` on 15 AUG. The `edges/` copy went.

**What makes it safe is identity, not redundancy.** Byte-identical means no person,
no family and no value is lost — `genimerge.sources` was already dropping the repeat,
so the merge never saw it. **This is not licence to delete an export because another
one covers its people**: that is the case `exports/excluded/` exists for, where the
file stays in git and is merely kept out of the corpus. Two exports that differ at
all are never candidates, however much they overlap.

**Check before, not after:** `sha256sum` both paths, keep the earlier one, and keep
the copy whose directory matches its style. `tests/test_sources.py::test_the_real_corpus_has_no_byte_identical_duplicates`
is what surfaces these, and it went green on this deletion.

**Never delete a GEDCOM, and never add a zip.** The zips are gitignored **one
line at a time**, deliberately: Emma wants an unignored zip to show up in
`git status` so she can see a download has arrived. Do not replace those lines
with a `*.zip` pattern — it would look tidier and would destroy the signal.

**Never write a `*.ged` or `*.zip` pattern into `.gitignore`. Ever.** Emma's
rule, stated 2026-08-06 after both halves of it had already been broken. The two
file types are ignored in opposite ways and a pattern gets both wrong:

- **`.ged` is never ignored at all.** Every GEDCOM under `exports/` is committed.
- **`.zip` is ignored one explicit full path per line**, and every zip currently
  on disk must have such a line. **Manual gitignores help humans**: a line per
  file means an *unlisted* zip appears in `git status`, which is how a new
  download announces itself. A pattern makes every download silent.

Re-checked 2026-08-06 evening after the edge-people batch: **51 zips on disk,
all 51 resolving under `git check-ignore`**, against 99 zip lines — the surplus
being stale entries for zips since removed, left alone rather than pruned, since
a re-download to one of those names is a re-download of something already
ingested. The invariant is *every zip on disk has a line*, never equality of the
two counts.
`tests/test_repo_invariants.py` asserts both halves, including against paths that
do not exist yet, so a pattern broad enough to swallow the *next* batch fails now
rather than after it arrives.

### `P3373` sibling is capped at 10 a day. It reads as spam

**Emma, 2026-08-25:** *"siblin relationships are too numerous and imo come off as spammy. We limit
sibling relationship adding to 10 quickstatements a day."*

**The number that provoked it:** `reports/wikidata-reciprocals.qs` came out **257 statements, 160
of them `P3373`** — 62% of a batch, all siblings. Sibling links grow as the *square* of a family's
size, because every child is a sibling of every other: one family of nine children is 72 `P3373`
statements on its own. Parents grow linearly. So a batch that looks balanced by people is
overwhelmingly sibling links by statement.

**The cap is 10 `P3373` statements per day, across every batch**, not per file. A builder emitting
siblings must count them and stop.

**It is a presentation rule, not a correctness one.** The links are right; there are simply too
many of them arriving at once for a watchlist to read as anything but noise. The rest stay in the
carry-forward and go out on later days, which is the same mechanism the daily cadence already uses.

**Nothing else is capped.** `P22` *father*, `P25` *mother*, `P40` *child* and `P26` *spouse* are
uncapped — they are few per person and each one is structurally load-bearing.

### Always write the English label next to a property or item ID

**Emma, 2026-08-15:** *"I have no fucking clue what any property or Q ID property
name is or what Q ID is. So you need to actually provide the English labels with
them."*

So `P5056` alone is not a thing anyone can read. Write **`P5056` *patronym or
matronym***, **`Q110874` *patronymic***, **`P7338` *regnal ordinal***. This applies
in chat, in reports, in queue items and in commit messages — everywhere a bare ID
would otherwise appear.

`reports/wikidata-labels.tsv` has the label for almost every ID this project
touches, so there is no excuse for a bare one and no reason to guess: looking it up
is a grep. Guessing is also how `Q28513` got written down as *Empire of Japan* when
it is **Austria–Hungary**, which produced 1,406 fake Japanese isolates.

### Queue items are BULLET POINTS, never numbered or lettered

**Emma, 2026-08-15, and the reasoning is hers:** *"they should be bullet points
because you should be blasting through them. Having something like A, B, C, or
whatever kind of implies durability, because you can't easily just remove A, so
that is actually detrimental."*

A number is a promise that the item will still be there. It makes deletion feel
like renumbering everything else, so items accumulate instead of being blasted
through — which is exactly what happened to `queue.md` twice in one day. An
unnumbered item can be deleted the moment it is done and nothing else moves.

**This also killed the `8a`/`8b` sub-lettering** and the `Task A/B/C` labels I
invented for her three priorities, which she had never used.

### Wikidata properties and items

All confirmed against live Wikidata via `wbgetentities` on 2026-07-30. On
2026-08-02, P1545 was added and P2600 / P734 / P735 plus **every item ID named
below** — `Q5`, `Q6581097`, `Q6581072`, `Q202444`, `Q12308941`, `Q11879590`,
`Q3409032`, `Q101352`, `Q5727902` — were re-confirmed the same way. Every label
matched. **Do not guess these** — several plausible-looking IDs are something
else entirely (P1288, for instance, is a German literature encyclopedia, not a
genealogy identifier).

**Anything the code can emit belongs in this table, and
`tests/test_wikidata_ids_documented.py` enforces it**: every `P…`/`Q…` string
literal in `src/genimerge/` must appear somewhere in this file, or the suite
fails naming the ID and the line it came from. P1545 was missing for a while
despite `genimerge.namelinks` emitting it, which was harmless only because it
happened to be right — a property outside this table is unguarded whether or not
it is correct.

That test checks an ID is **documented, never that it is correct**. Confirming
one means asking Wikidata, which is network and stays out of the suite, so a
typo added to code and table in the same change still passes. `wbgetentities`
remains the only thing that catches that, and the dates above say when it last
ran.

**Identity and structure**

| ID | label | datatype |
| --- | --- | --- |
| P2600 | Geni.com profile ID | external-id |
| P31 | instance of | item — value `Q5` human |
| P21 | sex or gender | item — `Q6581097` male, `Q6581072` female |
| P22 / P25 | father / mother | item |
| P26 | spouse | item |
| P40 | child | item |
| P3373 | sibling | item |

**Life events**

| ID | label | datatype |
| --- | --- | --- |
| P569 / P570 | date of birth / date of death | time |
| P19 / P20 | place of birth / place of death | item |
| P119 | place of burial | item |
| P2842 | place of marriage | item (qualifier on P26) |
| P106 | occupation | item |
| P97 | noble title | item |
| P535 | Find a Grave memorial ID | external-id |
| P4602 | date of burial or cremation | time — burial is **two** properties with P119, never a qualifier |
| P6375 | street address | monolingual text — where a GEDCOM `ADDR` block goes |

**Names** — the part of `todo.md` that needs new items created

| ID | label | datatype |
| --- | --- | --- |
| P735 | given name | item — name items are `Q202444` given name, or `Q12308941` male / `Q11879590` female / `Q3409032` unisex given name |
| P734 | family name | item — name items are `Q101352` family name |
| P1950 | second family name in Spanish name | item (not applicable here) |
| P1477 | birth name | monolingual text |
| P1559 | name in native language | monolingual text |
| P1545 | series ordinal | string — **qualifier**, ordering several given names, and ordering the links of a chained patronymic |
| P5056 | patronym or matronym | item — **the property a patronymic uses**, parallel to `P735`/`P734`, per `name modelling.txt`. Not a qualifier on `P735`. |
| P7452 | reason for preferred rank | **qualifier** — value `Q3409033` *usual forename* on the first given name |
| Q3409033 | usual forename | item — the `P7452` value. **Not** `Q3409032`, which is *unisex given name* |
| P7338 | regnal ordinal | **qualifier** on the given name — `Robert VII` is `P735` Robert + `P7338` VII. Emma, 2026-08-15: *"they should all have the regnal orders put on their names as qualifiers"*, and **not only the Samaritans** — anyone whose name carries an ordering. Confirmed offline against `reports/wikidata-labels.tsv`. Distinct from `P1545`, which orders a person's several given names rather than the person among namesakes. |
| P3831 | object of statement has role | item — **qualifier** saying *which kind* of name this `P735` is |
| P144 | based on | item — **qualifier on `P5056`, pointing at the PERSON that link names**: the father, then the grandfather for a chained patronymic. `name modelling.txt` supersedes the earlier reading of this as a name-item-to-name-item link. |
| P5278 | surname for other gender | item — pairs `Olsson` with `Olsdotter` |
| P1449 | nickname | monolingual text — **what a quoted token inside `GIVN` becomes.** Emma, 2026-08-24: `Stine "Stena" Eivindsdatter` makes *Stena* a nickname, **not** a given name and **not** a middle name |
| Q2507958 | birth name | item — the `P3831` role on the `SURN` family name, when a married one sits beside it |
| Q28418670 | married name | item — the `P3831` role on the `_MARNM` family name |
| Q245025 | middle name | item — the `P3831` value for a middle given name |
| Q110874 | patronymic | item — the `P3831` value for a patronymic, which is also what the name item is an *instance of* |

**A diacritic makes a different name, and folding it away invents ambiguity.**
Emma, 2026-08-16, asked why `Maria` matched nine Wikidata items: *"everything
appears to be diacritics or stuff that's not actually it… there's a male and a
female Maria."* `María` (Spanish), `Mária` (Hungarian) and `Marià` (Catalan) each
have their own Wikidata item on purpose. `measure-name-resolution` folded them
together, which manufactured ambiguity for **1,312** names and blocked them all
from being created or linked; keeping the diacritic cut that to **525** and moved
1,545 names from "create" to "link". Case and whitespace fold; nothing else does.

The genuine residue is the one she named — `Q325872` and `Q25413386`, the **male**
and **female** given name `Maria`. That is settled by the *person's* sex, not by
the string, and neither item is in the local store yet.

**One name item per USAGE, not per string — "Jackson Jackson Jackson".** Emma's
worked example, 2026-08-15: somebody whose given name is Jackson, whose surname
is Jackson, and who carries a patronymic Jackson **because their father is Jack
Jackson**. That is *"a different object for all three usages"* — a given-name
item, a family-name item and a patronymic item, three separate Wikidata items
that happen to share a spelling.

So a token appearing in more than one slot is **not an ambiguity to resolve**.
This was got wrong on 2026-08-15: the name census built a dominance ratio and a
bearer floor to decide which slot a token "really" belonged to, and Emma: *"If
something is a surname and a given name, then it gets a surname and a given name
object… They're two completely different things with completely different
objects. I feel like you jumped through a lot of hoops to try to introduce safety
stuff here that I did not want."* All of it was deleted.

**Where a real ambiguity does exist, ask.** Her rule in the same breath, on
whether Jackson is ever a middle name: *"if there is an ambiguity like that, you
ask me what the ambiguity is. You don't try to figure it out on your own."*

**A middle name is a given name after the first that is NOT a patronymic.** Emma's
definition, 2026-08-15, stated when asked about the ambiguous name items: *"The way
we define a middle name, to be clear, is that a middle name is like a given name
that comes after the first given name but it's not a patronymic."*

So position alone does not make a middle name — the second given token is a middle
name **only** if it is not patronymic. `Q245025` and `Q110874` are decided by what
the token *is*, and `P1545` numbers them either way.

### Working the queue: GUESS. Do not ask

**Emma, 2026-08-18:** *"as for everything in the queue, I'm gonna say don't do an
ask-user question because I have explained everything sufficiently… when going through
the queue right now, you just make a reasonable guess whenever you have some sort of an
ambiguity."*

So while the queue is being worked, an ambiguity is **resolved by making a reasonable
guess and recording it**, not by stopping. This suspends the *ask on ambiguity* habit
for queue execution specifically — it does not repeal § *One name item per USAGE* or
`name modelling.txt` § *edge cases*, which are about the name model and are decisions
she wants to make herself once she is back.

**What "recording it" means, because a guess that vanishes is just an unlogged
decision:** write the reading you took and the reading you rejected next to the work —
the queue item, the devlog entry, or the module docstring — plus what would falsify it.
`queue.md` § *Mass export from every profile Emma has added* is the worked example: two
readings of one dictated phrase, the one chosen, and the observation that would switch
it.

**She was asleep from roughly 2026-08-18 00:40 PST for twelve hours** and asked for no
`AskUserQuestion` in that window. The guess rule is what makes that workable rather
than a stall.

### `name modelling.txt` is the authority on how a name is modelled

**Emma wrote it by hand, 2026-08-15, in the repo root.** It supersedes what this
file previously said, and where the two disagree it wins. *"Please use
AskUserQuestion if anything here is unclear in the modeling. I tried to make it as
clear as possible."*

**The patronymic is `P5056` patronym or matronym — NOT `P735` with a qualifier.**
This is the correction. This file used to say the patronymic was a `P735` given
name carrying `P3831` → `Q110874`, with the name item an instance of `Q110874`.
Her model gives the patronymic **its own property**, parallel to `P735` and
`P734` rather than nested inside `P735`:

    Vladimir Putin (Q7747)
      P735 given name          Vladimir (Q2253934)
        P1545 series ordinal   1
        P7452 reason for preferred rank  usual forename (Q3409033)
      P5056 patronym or matronym  Vladimirovich (Q27670878)
        P144 based on          Vladimir Putin (Q19300851)  ← his father
      P734 family name         Putin (Q30524893)

**`P144` based on points at the FATHER, the person.** Not at a name item. Her
note in the file: *"(his father, has the same name)"*. That is a different claim
from what this file recorded before, which had `P144` on a patronymic *name item*
pointing at the name it derives from.

**The first given name carries `P7452` → `Q3409033` usual forename.** A middle
name instead carries `P3831` → `Q245025`, which is unchanged:

    Donald Trump (Q22686)
      P735 Donald (Q13422248)   P1545 1   P7452 usual forename (Q3409033)
      P735 John   (Q4925477)    P1545 2   P3831 middle name (Q245025)
      P734 Trump  (Q16944413)

**Chained patronymics get one `P5056` each, ordered by `P1545`.** Her worked
example, and she is explicit that this one is **not on Wikidata yet** — *"It is
what I am saying it should be on Wikidata"*:

    Abisha III ben Phinhas ben Yittzhaq ben Shalma (Q107534535)
      P735 Abisha    P1545 1   P7452 usual forename   P7338 regnal ordinal 3
      P5056 ben Phinhas    P144 Phinhas ben Yittzhaq ben Shalma   P1545 1
      P5056 ben Yittzhaq   P144 Yittzhaq ben Shalma               P1545 2
      P5056 ben Shalma     P144 Shalma                            P1545 3

So `P144` on each link points at **the person that link names** — the father, then
the grandfather, then the great-grandfather — and `P1545` numbers the links
outward from the bearer. The regnal ordinal sits on the **given name**, not on the
person.

**The data problem she states, and it governs how the tokens are read:** *"some
people have patronyms but no surnames. Some people have surnames but no patronyms.
Some people have middle names, have first name, middle name, patronym. Some people
have first name, patronym, given name."* And: *"The surname thing on geni is not
always something that clearly corresponds to a surname versus a patronym
particularly. We have to check in the given names and in the surname whether it is
a patronym or the regular name."*

**Both fields, always.** A patronym can be in `GIVN` or in `SURN`, and which field
it sits in decides nothing.

**Edge cases go to her, not to a rule.** *"There are probably going to be edge
cases and for the edge cases I am going to want you to tell me about the edge
cases. Do an ask-user question on the edge cases so that I can figure them out."*

**`Q3409032` and `Q3409033` are adjacent and are different things** — *unisex
given name* and *usual forename*. Confirmed offline against
`reports/wikidata-labels.tsv`, along with `P5056`, `P7452` and `P7338`.

**What survives from the old text:** Geni writes `Ole Olsen` into `GIVN`, so the
patronymic lands in the position a middle name occupies — `Olsen` is a *given*
token for 742 people and a surname for 266, measured in `reports/name-classes.md`.
*"The daughter and son would be the same thing"* — `-son` and `-datter` are one
category.

**How a patronymic item records what it derives from: `P144` based on.** Measured
on 2026-08-15 over the 633 items that are `instance of` `Q110874`: **`P144` on
119 of them**, plus `P5278` *surname for other gender* on 97 — which is the
`Olsson` ↔ `Olsdotter` pairing. `P1705` native label (513), `P282` writing system
(579) and `P407` language of work or name (370) are the near-universal ones.
Emma also wants the derivation stated in the item's **description text**, not
only as a claim.

**That measurement is the one live Wikidata query this project has made since the
rule, and Emma authorised it specifically.** *"You are going to look at Wikidata
live to see if there are objects for patronymics… this is a legitimate reason to
keep Wikidata. It's not a legitimate reason to query Wikidata because you just
want to figure out something about some random individual."* It was one aggregate
`SPARQL` query, no per-item lookups, run only after the local store was checked
and found not to hold `Q110874` — the store is a Geni-shaped slice of **people**
and carries almost no name items. **The rule is unchanged**: the exception was
for a question about Wikidata's own modelling conventions that the store cannot
answer, granted explicitly, once.

**`P3831`, `Q110874`, `Q245025` and `Q202444` were confirmed offline**, against
`reports/wikidata-labels.tsv` from the bulk download.

`P1545` is how a person with several given names keeps them in order: each P735
statement carries the ordinal of that name within the full given-name string.
`genimerge.namelinks` emits it (`SERIES_ORDINAL`), and it has not yet appeared
in a generated batch, because no matched person so far has more than one
given-name token. So it is correct-by-confirmation rather than
correct-by-observation — the first batch that includes one is worth reading
closely.

**Date qualifiers** — the GEDCOM modifiers map onto these

| GEDCOM | Wikidata |
| --- | --- |
| `ABT` / `EST` / `CAL` | P1480 sourcing circumstances = `Q5727902` circa |
| `BEF` | P1326 latest date |
| `AFT` | P1319 earliest date |
| `BET x AND y` | P1319 earliest date + P1326 latest date |

**References** — P248 stated in, P854 reference URL, P813 retrieved,
P143 imported from Wikimedia project.

### Emma edits the tree and the items BY HAND, continuously. Snapshots go stale in minutes

**Emma, 2026-08-24:** *"Remember that I've been actively fixing the tree manually."*

A downloaded item file is a photograph, not a mirror. She fixes labels, merges Geni
profiles and adds relationships while a batch is being built, so:

- **Re-download immediately before emitting a correction**, never from a file fetched
  earlier in the session. A correction computed against a stale snapshot re-writes work
  she has already done, which is worse than doing nothing.
- **Say when a hand-off was verified.** "Checked live at <time>" is the useful claim;
  "the item has X" without a time is not.
- **A label she has changed is a decision, not drift.** `Q141168785` had `en` and `mul`
  hand-corrected to the married form while `ja` still read the birth form — the stale
  half was ours, not hers.
- The ledger `reports/garborg-qids.tsv` has the same problem and is refreshed from her
  Wikidata contributions; a stale ledger is what made a batch try to re-create 21 people
  she had just made.

### A SUMMARY of a Wikidata item is not the item. Download the full item

**Emma, 2026-08-24:** *"you're supposed to download the full wikidata items for the
people I've edited to get the modelling not look at my edit history to see what's in
them."*

Reading an item through a fetch-and-summarise channel produced **three false findings**
in one session, each published to a report, the artifact and a commit message:

- **`Q467497` Arne Garborg was reported as having no `P22`, no `P25` and no `P3373`** —
  answering `ABSENT` even to a question posed narrowly to be reliable. The full item has
  all three. It was written up as *"the single highest-value outstanding edit in the
  programme"*. There was no edit.
- **The citation split was reported as inconsistent.** Counted over all 14 full items,
  `P2600` is **never** a reference on `P31` or `P21`. The modelling note it "corrected"
  had been right.
- **Property labels were invented** — `P2600` as "Peruvian NLB", `P1411` as "Nobel Prize
  recipient" — and `Q467497`'s 126 properties arrived truncated and out of order, which
  was the visible tell.

**So: anything that decides what to emit is read from downloaded JSON.**
`genimerge.wikidata.full_entities` fetches whole items in one batched request;
`scripts/garborg-modelling.py` is the worked example, deriving the whole model offline
from `out/garborg-full-items.json`. A summariser may be used to *find* something, never
to establish that a property is absent — absence is exactly what it gets wrong.

**The local store is not a substitute either.** It was downloaded before Emma made most
of these items, so it agreed that Arne had no parents. An item she has edited since the
download must be re-fetched, not looked up.

### Never query Wikidata to check something. Ever.

**Emma's rule, 2026-08-07, stated as flatly as it reads:** *"do not, whatever the
fuck you do, check it, except with our Wikidata export, because checking it is
the way that you get a 429."* One bulk job — `genimerge wikidata-download` — is
the only thing in this repo permitted to talk to Wikidata, and even it is
confirmed before a live run. There is no such thing as a harmless one-off lookup:
the download needs the whole rate-limit budget, and a side-query that trips
throttling costs hours of a run that was going fine.

**Every question about Wikidata's contents is answered offline, against the local
store**, after the download. That includes the ones that feel too small to
matter — does this item really carry P22, is this QID a redirect, what does this
label say. Write the question down as a check to run over `wikidata/items/`
rather than answering it live.

**A worked example of the shape, deferred on purpose:** Emma's guess is that the
Geni-linked items on Wikidata skew to the 20th and 21st centuries much as the
Geni profiles do, with the 19th ambiguous. That is checkable — and is **not to be
checked until the 500,000 are downloaded**, at which point it is a local
computation over stored items and costs nothing. Recorded in `todo.md` § 8b.

### The four big derived CSVs are committed GZIPPED

**Emma, 2026-08-24:** *"Imo gzip because this is long term and we aren't adding any more
data into our tree. Just processing."*

`reports/display-names.csv`, `derived-facts.csv`, `derived-family.csv` and
`derived-labels.csv` regenerate from the merge at **108-184 MiB** each, and GitHub refuses
any file over 100 MiB. They were 37-68 MiB at ~250 exports; the corpus is 546.

**The `.csv` is gitignored one path per line; the `.csv.gz` is committed.** After a clean
clone run `python scripts/pack-derived.py --unpack` once. Forty-four scripts read these by
name, so the plain CSV stays what every reader opens rather than churning all of them.
`tests/test_derived_packing.py` fails if a `.gz` goes missing, if a plain CSV gets tracked,
or if a `.gz` ever creeps over the limit itself.

**This does not loosen the `.ged` rule.** Every GEDCOM under `exports/` is still committed
uncompressed, and no `*.csv` pattern was written into `.gitignore` -- four explicit paths,
the same way the zips are listed.

**The merged GEDCOM is the one `.ged` not in git**, and it is worth saying why
here because "never gitignore a `.ged`" is a rule two sections up. `out/merged.ged`
is 409 MB — generated, regenerable by `genimerge merge`, and over GitHub's file
limit. It is covered by the existing `out/` line, so **no `.ged` pattern exists
and none should be added**; the rule about the corpus under `exports/` is
untouched. Emma's call, 2026-08-07: ignore it by necessity.

### Cost: this repo is private, so CI is manual-only

**Never add a `push:` or `pull_request:` trigger to `.github/workflows/`.**
Actions minutes are free on public repos but billable on private ones once the
monthly allowance is used, and a surprise bill is not worth a green tick.
`ci.yml` is `workflow_dispatch:` only, and the workflow is disabled at the
GitHub end as well.

Verification therefore happens **locally, before pushing**: `python -m pytest`.

**The suite has a fast lane, and the full run now needs a real terminal.**
`pytest -m "not slow"` is **1,104 tests + 2 xfail in ~6m** (2026-08-23; it was 932 in ~115s
on 08-16, and it grows with the corpus). A bare `pytest` still runs everything —
`slow` deselects nothing by default, and a run that has not included the slow tests
is not a full verification.

**`BOT_CONTACT` must be set in the shell or one test fails.**
`test_cli_wikidata.py::test_the_offline_guard_actually_fires` builds a client, and
`genimerge.wikidata.require_agent` refuses an empty User-Agent by design — Wikimedia
answers one with a bare 403, so failing loudly here is the point. Export the contact
address and the fast lane is **0 failures**.

Six modules carry `slow`, each working over the whole corpus:
`test_merge_real_exports`, `test_gedcom_real_exports`, `test_density`, `test_paths`
(its real-merge tests only), `test_wikidata_store_real`, and the real-merge work in
`test_sources`. `test_merge_real_exports` alone merges the whole corpus (546 exports
on 2026-08-23, 245 when this was written) in one
module-scoped fixture and **exceeds ten minutes**, which is the agent tooling's
per-command ceiling — so the full suite became unrunnable from a tool call around
2026-08-16, purely because the corpus grew. Nothing is wrong with it; it is just
long. **Run it in your own terminal.**

**A second `pytestmark` assignment silently overwrites the first.** That is how the
marker looked applied and was not: `test_merge_real_exports.py` had
`pytestmark = pytest.mark.slow` on line 24 and
`pytestmark = pytest.mark.skipif(...)` on line 28, so the slow mark vanished and the
ten-minute merge kept running in the fast lane. Combine them into a **list**. The
symptom is a `-m "not slow"` run that still takes minutes while
`--collect-only` reports the tests as deselected.
The suite is fast, needs only pytest, and covers the real 24 MB exports. The one
thing local runs cannot do is the Python version matrix — `tests/test_python_floor.py`
is a partial stand-in for that, and says so.

### The 183,674 isolated Geni-linked Wikidata items are LOW PRIORITY

**Emma's ruling, 2026-08-15**, after the demographic analysis:
*"this group of people is a group that I probably would consider to be very low
priority, and I don't consider my relationship with them to be that important. I
don't think that they're that important to get into the World Tree."*

`reports/wikidata-isolates.md` is the analysis. The measurement that matters:
**only 722 of them — 0.4% — are in our Geni corpus at all.** The other 182,949
appear in none of the 203 exports, so they are not people the tree is missing a
link to; they are outside it entirely.

They are politicians, writers, lawyers and academics, mostly 19th–20th century,
and **54.7% have no Wikipedia article** — Emma guessed almost all would.

**Do not spend effort connecting them.** This is recorded because the group is
large enough (13% of stored humans) to look like a priority and is not.

### An item with no relationships is not a missing item. Geni ID first, then everything else

**Emma, 2026-08-15, correcting the framing of the Samaritan high priests.** They
are **on Geni and on Wikidata**. What they lack on Wikidata is *genealogy*:
*"they aren't really genealogical entries. They are just individuals… They just
are individuals without any relationships and such."* Reporting them as absent
was the § *"Is X present?"* failure again, one section down, in a new costume —
present as items, absent as a family tree.

**Her own item is the same shape and is the worked example.** `Q140568870`
exists, carries no Geni ID, and is attached to nothing. She has been explicit
that this is ordinary rather than special: *"it's just a wiki data object. It's
a wiki data object that should be linked in the way that any other wiki data
object should be linked. There should not be anything special about it"* —
after an earlier session turned it into a bespoke case.

**So the order is fixed, and it generalises to every merge:**

1. **Add the `P2600`.** *"The Jenny ID needs to be present before any properties
   derived from Jenny can be taken from it, or before any relationships can be
   added."*
2. **Then everything Geni supports**, each statement cited to that Geni ID.

*"It's the same logic that would be occurring in the future for when we are
merging the trees more for situations where the Jenny and the wiki data are not
there. The Jenny ID is added first, and then all the Jenny-derived stuff is
added after."*

### The ONE place a name may choose: inside a zipper slot, dates first

**Emma, 2026-08-25:** *"Dates first then names but also bruh providence of zipper merges should be
recorded."*

**The three-step cascade is NOT hers and must not be attributed to her.** Emma, same day:
*"solo -> date -> name isn't really a thing I asked for lol it's a hallucination on your part."*
She said *dates first then names* about the **2x2 sibling** case; it was generalised into an
architecture and handed back to her as her design. The name exception below is real and she
approved it for that case; the shape around it is a local decision and is on trial.

**And she rejected the first step outright:** *"Solo child says nothing unless there's some reason
to match them lol."* One unmatched person on each side is *trivially* unique, so uniqueness proves
nothing when the set has one element. **`reports/zipper-reliability.md` measures it and she is
right**: `child`+`solo` disagrees with independent sources **14.9%** of the time against **0.7%**
for `father`+`solo` — twenty times. Solo *parents* are fine; solo *children* are not, which is
exactly the distinction she drew.

**Solo child STAYS, flagged as the weakest thing in the join.** Her call, 2026-08-25, given the
14.9%: *keep them, flagged as weakest*. All 3,326 remain in `reports/zipper-pairs.tsv` carrying
`method=solo` and `slot=child`, so any consumer can exclude them in one filter — and the queued
solo-children analysis may yet rescue them, since sex agreement (`P21` against our `sex` column)
is free evidence the join ignores entirely. **Do not silently drop them and do not silently trust
them.**

**The standard for every rule here:** *"a lot of these rules are empirical and we need to
empirically study our data to figure out what to make of it. Don't jump to conclusions based on
what sounds like it might be true. Even parents isn't certain."* The slot ordering in
`zipper-join.py` is her spoken ranking and is a **hypothesis under test**, not a settled rule.

This is a narrow, deliberate exception to *no name similarity, ever*, and the boundary is what
makes it safe. `scripts/zipper-join.py` resolves a family slot in three steps:

1. **solo** — one unpaired person on each side. Position is the whole evidence.
2. **date** — birth years within `matching.YEAR_TOLERANCE`, unique from **both** directions.
3. **name** — a shared identifying word, unique from **both** directions.

**Why this is not the deleted `reconcile` matcher.** That searched Wikidata *for* a name. This
never leaves the slot: the parent is already an established correspondence, so the candidate set
is closed and usually two people. `CLAUDE.md`'s own wording is *"Labels confirm a position; they
never choose one"* — position has already chosen the set; the label only orders within it. An
assignment that is not unique both ways proposes nothing, which is the coin-flip rule holding.

**The inherited-name guard, and why it exists.** In a child slot, every word of the *parent's* own
name is discarded before matching. The first run without it proposed `Carl Edvard Hansson
Wachtmeister` → `Hans Wachtmeister` on the shared token *wachtmeister* — a child of a Wachtmeister
matched to a child of a Wachtmeister. It passed uniqueness only because the other siblings had no
surname recorded, so the evidence was an artefact of missing data on the candidates it beat.
Removing the surname made the step **more** productive, not less: 3,309 → 10,862 proposals, because
the shared family name had been blocking ties that a given name then settles.

**The name step is measurably no worse than the position-only step it supplements.** Of proposals
where both sides carry a birth year, those reached by name disagree by more than ten years **9.2%**
of the time, against **11.8%** for `solo` and **0.0%** for `date` (which selects on the year). So
adding names did not lower the join's standard.

**Provenance is mandatory, and it is a CHAIN.** Emma, 2026-08-25: *"ideally, a zipper merge will
almost always be done with there being a relatively large chain of providence, not just a simple
'this was the justification,' but a potentially very large series of justifications."*
`reports/zipper-pairs.tsv` carries one step —
`round, geni_id, qid, slot, method, from_geni, from_qid, evidence`; it previously carried round,
geni id and qid alone, because the slot was assigned into the tuple as `""` and never emitted, so
no pair could be audited at all. `scripts/zipper-provenance.py` walks the steps into chains (max
depth 8, mean 2.7) and checks each against every *independent* correspondence in the repo.

**Support and contradiction both propagate along the chain** — her words, *"it goes both ways"*.
An independent resolution agreeing with an inferred step corroborates everything above it; one
disagreeing poisons everything above it. **Her own hand verdicts in
`reports/emma-judgments.tsv` are nodes in that graph** — that is what she said they are for:
*"That is the actual reason why I asked you to record my manual decisions, because of the fact
that they entered into the province too."* 25,570 of 44,725 pairs are corroborated somewhere in
their chain; 187 are poisoned.

**Poisoned is a reading, never a deletion.** Her bar for stopping the join is high — *"we need a
pretty damn good reason to stop it... This reasoning requires something pretty good."*

### Our side could never have two children — check the separator before believing a distribution

**`reports/derived-family.csv` separates multi-valued cells with ` | `, spaces included.** Every
consumer must split on it. `zipper-join.py` handled `,` and `;` only, so a five-child cell parsed
as the single token `"1050090 | 1050271 | ..."`, matched nothing, and the person reached the join
**childless**. 379,251 people have two or more children and every one of them arrived with none.

**The tell was a distribution that was too clean.** `reports/zipper-ambiguous.tsv` held 615 rows
and not one was `2 × 2` — read at the time as "two-against-two is rare", when the truth was that
our side could not *have* two. Emma spotted it from the outside: *"I feel the zipper merge still
isn't hitting the hard points lol."*

**And there were two bugs stacked.** Splitting on `|` alone yields `"1050090 "` with whitespace,
which still missed the index — the first fix moved the pair count by **exactly zero**, which is how
the second was found. A fix that changes nothing is evidence, not reassurance.

This is the same shape as the date-parser failures recorded above: **a parser that silently narrows
its input instead of failing**, with downstream counts that stay plausible while the data shrinks.

### Merging the two trees is a walk up the relationships, not a name search

**Emma, 2026-08-15, and she is clear this has not actually been done yet:**
*"it is an idea of a thing that we still haven't really done yet. I think we may
have tried at some point to do it, but we haven't really done it."*

**The method is structural.** *"For the synoptic tree, we're supposed to be
specifically going up the parental lines and stuff like that and merging the
parents on Jenny and Wikidata if there are ones on both. Same with all the other
relationships. That is a critical part of building up this synoptic tree."* Start
from somebody holding **both** a Geni ID and a QID, walk `P22`/`P25` against our
father/mother, and where both sides have a person in the same position, that is
a merge — her 2026-08-12 rule: *"we merge them based off of whether something is
the mother on both sides of an individual. We merge them together unless the
mothers really conflict."*

**Labels confirm a position; they never choose one.** She said *"you basically
have to use text-based stuff with their labels matching them to the ones on
Jenny"*, and that is **not** a reversal of *no name similarity, ever*. The
structure picks the pair — Wikidata's `P22` of this item against our father of
this Geni ID — and the label is read to check the pair is not absurd. Searching
Wikidata for a name is the deleted `reconcile` matcher, and it stays deleted.

**Two things come out of the walk:**

- **Our own `QID` ↔ Geni ID correspondence**, built from the merges rather than
  from `P2600` alone: *"we definitely need to… be essentially building up our own
  correspondence of the QIDs and Jenny IDs for these ones."*
- **A placeholder for anyone on Geni and not on Wikidata**, created later —
  *"because our entire thing is we're trying to expand. There's going to be a
  very large amount of individuals that are merged."*

### The practical goal is EMMA densely linked, not a comprehensive import

**Emma, 2026-08-15, stating the actual target:** *"while I want to build a
comprehensive family tree of everybody, while I want to get a full-on
exfiltration or a full-on import of basically all of the Geni data onto Wikidata
— that isn't really a feasible thing. But it is very feasible for me to make it
so that I am in a very good place myself. I make myself go from being completely
unlinked to being in an extremely dense neighborhood of Wikidata, which is kind
of like the practical goal for myself that I have here."*

**So proximity to her beats volume.** A thousand people on the far side of the
tree are worth less than fifty in her own neighbourhood, and any ranking that
optimises for total people added is optimising for the wrong thing.

**This is what the Nordic result was really telling us.** Norwegian and Swedish
academic isolates saved at **86–94%** against **34–39%** for academics with no
country filter — not because Nordic records are better, but because Norway and
Sweden are *where she is linked*, so a path exists and is short.

**It also sets the stopping rule.** Emma, same day, on the wider Nordic pool:
*"I feel like we're kind of hitting diminishing returns here… I'm not trying to
necessarily get all these people. I think I got a good amount."* 7,748 unopened
Norwegian and Swedish isolates is not a backlog to burn down. **Her labour is the
constraint** — measured at 4.7 profiles a minute, that pool is ~27 hours of it.

**Tightest first.** Her own instruction: *"find any specific people related to
Rogaland or Stavanger… these are going to be the closest people and the most
likely to find clear examples of people who are really close."* Rogaland is where
her line is from, so place beats nationality beats occupation as a filter.

### THE THREE LINES. This is what the Garborg programme is building

**Emma, 2026-08-25:** *"make it very clear in the claude.md referencing all of this stuff that
this is what we are doing... Yes it should be three lines lol: Charlemagne to Bergitte, Bergitte to
me, Bergitte to Arne."*

**Bergitte Gunnbjørnsdatter Aukland** `6000000002481819312`, 1465–1522, is the hinge. Confirmed by
walking our own tree, not assumed: **she is an ancestor of both Emma and Arne**, Arne at depth 11.
She is *not* their nearest common ancestor — that is **Rasmus Ingebretsen Grude**
`6000000003492045766` (Emma +10, Arne +5), and they share **2,780** ancestors in all. Bergitte
matters because she is the one on both lines who is **herself descended from Charlemagne**, which
is what `queue.md` meant by *"Bergitte is the bigger target one"*.

| line | source | people | have items | **to create** |
| --- | --- | ---: | ---: | ---: |
| **1. Charlemagne → Bergitte** | `paths/charlemagne-to-arne-garborg.tsv` steps 12–34 | 23 | 9 | **14** |
| **2. Bergitte → Emma** | Geni: *13th great grandmother*; steps not yet captured | ~15 | ? | ? |
| **3. Bergitte → Arne** | `paths/charlemagne-to-arne-garborg.tsv` steps 1–12 | 12 | 3 | **9** |

**Lines 1 and 3 are one saved Geni path**, `paths/charlemagne-to-arne-garborg.tsv` — 34 steps,
Arne up to Charlemagne, passing through Bergitte at step 12. It was generated by
`genimerge path-from-html` from a page Emma saved and it is the authority. **Read it before
deriving anything**: `reports/charlemagne-route.csv` is a *different* 399-step Emma→Charlemagne
descent up another branch that does **not** contain Bergitte, and treating the two as the same
thing has already produced wrong answers.

**Line 2 does not exist yet and is the missing piece.** Emma descends from Bergitte by a different
line from Arne's, and no saved page covers it. It needs the standard handling: save the Geni
relationship page, then `python -m genimerge path-from-html <page> -o paths/<name>.tsv`.

**Where the gap actually is.** Of the 34 on lines 1 and 3, **22 need creating, and 19 of them are
consecutive** — steps 4 to 22, the whole Norwegian and Swedish middle: Mele, Nedre Rossavik,
Mjølhus, Tengs, Lejon, Algotsson, Svantepolksdotter, Guttormsdatter. **The medieval royal end is
already on Wikidata**: Guttorm Àsulfsson `Q19061035`, Judith of Flanders `Q273181`, Baldwin IV
`Q378177`, Berengar II `Q314521`, Louis the Pious `Q43974`, **Charlemagne `Q3044`**. Only three
gaps up there — Rozala of Italy, Berengar I, Giséle of Cysoing.

So the line closes at **step 23, Guttorm Àsulfsson à Rein**, the deepest person who already has an
item. Create steps 4–22 and Arne is continuously linked to Charlemagne.

**Nineteen consecutive creations cannot link TO EACH OTHER in one batch** — but each of them can
be linked to anybody who already has a QID, in both directions, in that same batch.
**`LAST` IS valid as a value; the limit is narrower than this repo long claimed.**
`Q141178381 P22 LAST` is ordinary QuickStatements — the subject already exists and `LAST`
resolves to the item created just above. What cannot be done is linking **two items created
in the same run** to each other, because `LAST` names only the most recent one.

Emma, 2026-08-25: *"you never actually did the 2-way relationship addin qith the creation of
items that is completely possible but you just decide to fuck off and no do it because it goes
QID PID LAST instead of LAST PID QID."* The general claim was mine, not hers, and it cost her
weeks of one-way links to repair by hand.

So a spine batch needs a second file only for the links **between two people it is creating**.
`scripts/build-missing-reciprocals.py` is that second half, and it is much smaller than it was:
`scripts/build-garborg-day.py` now emits `Q… P… LAST` for every relationship to an existing item.

`reports/the-spine.md` carries the person-by-person state. The closing item of `queue.md` is to
build the batch builder that does all of this at once rather than a hop a day.

### The programme is HYPERLOCAL: one hop out from Arne Garborg, per day

**Emma, 2026-08-23, correcting an assumption that had been running for days:**
*"the only reason we ever should be doin these is specifically building up from the
Garborg tree. Remember we are only editing hyperlocal for a reason and may even
substantially change the algorithm of the Garborg tree stuff to favor it more. We were
supposed to every day have our own Garborg qs batch kind of extending off of him by 1
each time. Until we get the confidence to actually run this on wikidata, this is a good
thin to run. We are testing the waters for a later geni bot automation."*

**One step is one HOP of the tree**, her ruling when asked: each daily batch takes
everybody at the next distance from Arne — his siblings, then their spouses and
children, then the grandparents, and outward. Not one person a day, and not one
relationship type a day.

**So the deliverable is a small daily batch, not a large correct one.** The point is
confidence: a hop a day is reviewable by eye, and it is rehearsal for a later Geni bot.
`docs/wikidata-item-template.md` is the shape each item takes, read off the items she
built by hand.

**Do not invent a runnable edit batch she has not asked for.** Emma, same message:
mass batches are *"pretty harmful when generated"*. Measurement, censuses and reports
are fine unprompted — § *No unprompted reports* still applies to their volume — but
a `.qs` or a JSON edit batch is a thing someone can paste into QuickStatements, and
producing one uninvited presents work as ready that nobody sanctioned. On 2026-08-23
four `.qs` files were attached to the chat when she had asked for one; the largest,
`reports/wikidata-geni-qid-p2600.qs` (354 statements), was generated on my own
initiative during a work-loop tick. Her reply: *"What the fuck are those
quickstatements only the garborg ones are ones that I asked for."*

**The existing mass batches are NOT shelved and are NOT a mistake.** Same message,
asked whether the 284,000 edit objects should be parked: *"Keep maintaining them they
are gonna be run lol the program is on it will just not run until sept 1."* They stay
live and stay consistent. The rule above is about **new** batches, not about unwinding
the programme.

### The purpose is to ADD to Wikidata, not to correct it

**2026-08-10, Emma:** *"the entire purpose of this is to add it… Correcting
stuff on Wikidata is actually such a pain that it's almost effectively out of the
question. We will be more prone to adding in contradictory information cited to
Geni than we are to correcting information."*

This governs what is worth working on. Over the 14,157 people carrying both a
Geni ID and a Wikidata item:

| | count |
| --- | ---: |
| **addable statements** (Geni has a value, Wikidata is silent) | **24,957** |
| conflicts (both sides state it, values differ) | 930 |

**Twenty-seven to one.** Contradiction resolution is worth doing and is *not a
priority* — Emma, same day: *"remember contradiction resolution is not that high
priority here generally… it is worth doing but genuinely not that important."*

Practical consequences:

- A disagreement is a **note**, not a work item. Do not build machinery to
  adjudicate them.
- Where Geni contradicts Wikidata and Geni looks right, prefer **adding a second
  statement cited to Geni** over editing the existing one.
- The measurement that matters for any field is *how many people have it in Geni
  and lack it on Wikidata*, not *how often the two disagree*.
- **A conflict is never routed to Emma for a ruling.** The pipeline emits the Geni
  value beside the existing statement, cited `S2600`, and moves on;
  `scripts/build-from-diff.py` does this for every `CONFLICT` row of every diff.
  Twelve conflicts were put to her as decisions on 2026-08-26 and her answer was that
  the question should not have been asked: *"those seemed like simple data issues that
  by design were supposed to get pushed onto wikidata"*, *"it's not your job to make
  the tree correct it's your job to set up a pipeline that gets the exported geni data
  onto wikidata"*, and — the reason it can never be per-case — ***"we are doing over a
  million people here."***

`reports/model.md` holds the field-by-field version of that table;
`reports/names-spec.md` is the first spec written against it.

### How this project works now: case by case, Emma interprets

**2026-08-10. This supersedes the "build a report over the whole corpus" habit.**
Emma: *"we go through the merging on a case-by-case basis. I am going to say we
go through the merging, and I look over each case one by one. You display each
case to me one by one, and I look over it. We try to derive rules for that."*

The failure being corrected: *"you're just aggressively jumping into the database
modelling and skipping the interpretation... you've run this algorithm on a bunch
of stuff without telling me and not even looked at a single thing."*

So:

1. **Show records, not statistics.** A markdown file of counts is not a
   deliverable. `scripts/show-case.py` prints one person, both sides.
2. **Never reformat data you were asked to inspect.** Emma, on a display that
   collapsed a 2,686-line record to fifteen lines of my formatting: *"Your
   display of the GEDCOM data is 100% wrong... you made editorial decisions on
   the GEDCOM data. You actively obscured stuff from me."* Print raw lines. If
   something is withheld, say what and how much.
3. **Rules come out of cases, not before them.** Do not generalise a merge rule
   from one example; Emma explicitly refused that for the Ōjin conflict.
4. **Ask on ambiguity.** *"The whole thing is you're supposed to slow down and
   ask the user a question on ambiguities."*

### The Samaritan family relationships are DONE. Do not audit them

**Emma, 2026-08-15:** *"Oh my god are you trying to somehow, for some bullshit
reason, analyze whether the family relationships of the Samaritans are correct?
Cuz you shouldn't be doing that. I don't want you to be doing that. The family
relationships of the Samaritans are done."*

She built that tree on Geni by hand. **She also knows it contains errors, and has
decided they stay** — 2026-08-15: *"I know that the Samaritans have errors in
their relationships but my perspective here is it's good enough and we're moving
on."* So finding one is not a discovery and reporting one is not a service. This
is the export-analysis reflex one section down, wearing a different costume.

**What this does not forbid.** Work *about* those people that is not an audit of
their relationships: giving them Wikidata items, normalising their office and
succession, classifying their **names** — `ben Yitzhaq` is a patronymic and that
is name work, not a relationship check.

**Two name forms the Samaritans use that the classifier does not yet handle**,
raised by Emma 2026-08-15 and going into her own name-modelling document rather
than being guessed at here:

- **Ordinal patronymics** — `Yitzhaq I ben Tsedaka`, `Tabia III ben Yitzhaq ben
  Abram`. The ordinal sits between the given name and the patronymic, and it is
  part of how the person is named rather than decoration to strip.
- **Chained patronymics** — `Yaacob II ben Uzzi ben Yaacob ben Aaharon` is four
  generations in one string. `classify-patronymics.py` reads only the first
  `ben X`, so the grandfather and great-grandfather are invisible to it.

**How it went wrong:** a stale queue item said Wadah Cohen's father was missing.
The right move was to notice the item was stale and delete it. Instead the
relationships were walked and reported back to her. They were fine — she had
created the intervening `NN ben Amram ben Yitzhaq /Cohen/` the week before.

### GREP THE CORPUS BEFORE RUNNING AN EXPORT. Every time

**Two exports were wasted on 2026-08-23, hours apart, for the same reason:** a question
about *what we already hold* was answered by fetching more instead of by looking at the
files on disk.

- **Obitake 23** (`export-Forest-6000000227331852896.ged`) — run to fetch Izumo 18–33,
  reported absent. All sixteen were already in the corpus. **51 new people, 0 rostered.**
  "Absent" had been measured against **one export file** and reported as a corpus fact.
- **Yitzhaq I ben Tsedaka** (`export-Forest-6000000227245553985.ged`) — run to test whether
  Samaritan About Me Wikidata links post-dated our exports. **0 new people, 0 new links.**
  Fifteen linked Samaritan profiles were already in the corpus; the "0 of 85" that prompted
  it was about a different population.

**Both were answerable by a grep over `exports/`, in a second, for nothing.** An export
costs a Geni round trip, a download, a commit of ~90k lines, and — the part that actually
matters — one of Emma's export slots and her patience.

**So, before every export, run the check and put the number in the commit message:**

- *Are these people already here?* — `grep -l '@I<id>@' exports/**/*.ged`, or
  `scripts/measure-export-newness.py` for the general question.
- *Is this property already here?* — `grep -c 'wikidata.org' exports/**/*.ged` and its like.
- **Never let a single-file measurement stand in for a corpus one.** That is what
  `match-izumo-export.py --corpus` exists for, and its docstring says why.

An export that turns out redundant is still committed and never deleted — the
never-delete-a-GEDCOM rule is untouched. The point is not to run it.

### The job with an export is to integrate it, not to analyse it

**Emma, 2026-08-13, stated flatly after repeated violations.** *"This is not a
data analysis project, it is a project for editing Wikidata to add more stuff."*
When a new export lands, the task is to **integrate it into the tree** — place
the `.ged`, commit, re-merge if needed — and nothing else. Do **not** compare it
to an existing export, diff it, characterise what changed, count what it adds,
or narrate any of that. She is not paying for unsolicited analysis, and every
comparison of that kind cost her a turn to shut down (the 07-vs-13 AUG Ogasawara
diff being the case that named this rule). The one exception is what integration
mechanically forces — checking a destination path does not already exist before
placing (see *Never overwrite an existing `.ged`*) — which is a safety check,
not analysis. The tree is the substrate; the deliverable is Wikidata edits.

### No unprompted reports

**Emma, 2026-08-12.** Do not produce a report, an analysis or a measurement that
was not asked for. Write the thing that was requested and stop.

This is not a rule against measuring — § *"Analyse this" means build a CSV* still
stands, and when she asks for an analysis it should be exhaustive. It is a rule
against **answering an unasked question**, which in this session repeatedly cost
her a turn to redirect: a name-item census produced straight after a charged
exchange, a report on a fix written *instead of committing the fix*, three
consecutive tables about Geni name scripts for a question about Wikidata labels.

Two specific habits it forbids:

- **Narrating instead of finishing.** If the work is done, commit it. A report
  describing a completed fix is not accountability, it is the fix not landing.
- **Answering with whatever was most recently built.** Match on the *question*,
  not on vocabulary the question happens to share with the last thing measured.

**She will ask when she wants a report, and those are worth doing properly.**
`reports/geni-names.md` is one she asked for by name.

### "Analyse this" means: build a CSV of every instance, then analyse that

**Emma's rule, 2026-08-11, and she stated it as a correction of what I am and am
not good at:** *"When I ask you to analyse a problem, it generally means you run a
script to build a CSV of every single instance of the phenomenon that I'm asking
you about, and then do an analysis on it, and then make a decision explicitly.
I'm realising this is a thing you're good at, and you're absolutely not good at
analysing individual components."*

So the shape of every analysis task is three steps, in this order:

1. **Build the CSV.** Every single instance of the phenomenon, one row each — not
   a sample, not the top 100, not a summary table. A person with four `NAME`
   records is four rows.
2. **Commit and push it.** *"We're not trying to make the repo small. We don't
   care about repo size. We care about actually getting results."* These go in
   `reports/`, which is tracked; `out/` is gitignored and is the wrong place.
   `reports/display-names.csv` is 48 MB and that is fine.
3. **Analyse the CSV, and state the decision explicitly.**

**This supersedes reaching for a hand-picked example.** Looking at one record and
generalising is the failure this rule exists to stop — and note it does *not*
contradict § *How this project works now*, which is about Emma interpreting
**records** she has been shown. Showing her a record is how a rule gets decided;
building the CSV is how the phenomenon gets measured. Do both, in that order:
records first so she can see what the thing is, then the full census.

### Emma's own profile: the middle name is intended on Geni and stays off Wikidata

**Emma, 2026-08-15:** *"There was a middle name added to me, by the way, that is
intended. It is not something to be added to a wikidata."*

Two separate facts, and the second is the rule. The middle name on her Geni
profile is **deliberate** — not a data error, nothing to correct, nothing to ask
about. And it is **not to be emitted**: no `P735` with `P3831` → `Q245025`, no
appearance in a label, in any language.

**It is in the corpus now.** When she first mentioned it no export held it; a
later one did. `out/merged.ged` carries `1 NAME Emma Himiko /Leonhart/` as a second
`NAME` record, and `reports/derived-labels.csv` shows it under
`further_latin_names`.

**Checked 2026-08-16: nothing emits it.** No batch contains the string, and the
only edit referencing `6000000087535357291` anywhere is the `P2600` *Geni.com
profile ID* from her own `entity_resolution.md` entry — no label, no name, no sex.
The rule holds because the label emitters use `label_en`, which is the corrected
single name, and never `further_latin_names`. It is written here rather than in the queue because
it governs how the project works and has no step attached.

This is the same shape as § *Her name is Emma Leonhart*: what her profile says
and what gets emitted are separate questions, and the emitter is where the
answer lives.

### A cron only fires while the session is idle — never schedule a long job into active work

**Measured 2026-08-15/16.** Of seven crons, six fired and one never did: the
19:07 re-merge starved for four hours because the session was busy on the hour,
every hour. Emma: *"fucking do this shit right there fuck now or at least queue
it up at the end so it actually runs."* It ran by hand at 00:30.

**So: run a long or load-bearing job directly, or schedule it for a window when
nothing else is running.** The short hourly ticks are fine because they re-fire;
a twenty-minute merge is not. And **check the crons when a session resumes** —
they are session-only, so they die with it, and a job that quietly never fires
looks exactly like one that had nothing to do.

### Her name is Emma Leonhart

**Profile `6000000087535357291` is Emma Leonhart** — the account owner, and the
seed of the first exports. Geni was renamed; the exports taken before that were
not, so the old name was in every GEDCOM, every derived report, and the prose
that quoted them. It was removed from all 223 of them on 2026-08-12.

**The name that is gone does not get written down again** — not in a comment, not
in a report, not as a "superseded name" column, not in a script that exists to
remove it. `entity_resolution.md` records the correction in her words and
`derive-labels.py` applies it at derivation; that is the whole mechanism.

If a future export reintroduces it, correct the record and regenerate — do not
add a note explaining what it used to say. An earlier commit kept it in a
`further_latin_names` column and called that preservation rather than erasure.
That was wrong.

**Other people named Borsheim exist in this tree** — 391 lines carry that
surname legitimately. Never substitute on a bare surname; it rewrites strangers.

### Reading a Wikidata statement: the value is not the statement

**Qualifiers and references carry the genealogy.** Reading only `mainsnak` and
reporting what you found is how this project twice told Emma that Wikidata held
nothing when it held the answer.

Henry III (`Q160311`), 2026-08-10. The `P26` spouse statement's mainsnak is just
`Q228885`. Everything that matters is beside it:

    P26 -> Q228885
      P580  start time        +1236-01-04
      P582  end time          +1272-11-16
      P1534 end cause         Q99521170
      P2842 place of marriage Q29265
      4 references

Marriage date, marriage place, when and why it ended, all sourced. A display that
read mainsnak only reported "Wikidata has the spouse link but no date and no
place", and Emma corrected it: *"No wikidata often has it, but not in the same
place and it's relatively rare."* Both halves of that are true and the second is
the trap — it is rare enough that a sample can miss it and confident enough to
mislead when it is there.

**Geni says 14 JAN 1236; Wikidata says 4 JAN 1236.** Ten days apart. That
disagreement only exists to be found if qualifiers are read.

### GEDCOM dates have a specification. Use `genimerge.dates`, never a regex

**Do not parse a GEDCOM date by hand.** Not with a regex, not with
`str.isdigit()`, not by taking the last integer token. Call
`genimerge.dates.parse_date`.

GEDCOM 5.5.1 specifies the date grammar precisely — exact dates, bare years,
month-and-year, the `ABT`/`BEF`/`AFT`/`EST`/`CAL` modifiers, and `BET x AND y`
ranges. Geni emits that grammar with **one documented deviation**: BC years are
written as a **minus** (`-73`, `ABT -95`, `BEF -1310`) rather than 5.5.1's
`73 B.C.`. `dates.py` implements the grammar and that deviation, and reports no
structured value for anything it does not recognise — a date we cannot read must
not become a date we guessed.

**This has now cost the project twice, the same way both times.** A hand-rolled
parser drops what it does not understand *silently*, because an unreadable date
is discarded by design:

- 2026-08-05 — negative years were unhandled and **4,459 events**, every date
  before year 1 in the corpus including Emperor Jimmu and Makeda, parsed to
  `year=None`. Nothing downstream complained.
- 2026-08-10 — `scripts/build-centuries.py` and `scripts/find-bce.py` each took
  the last integer token. `"-73".isdigit()` is `False`, so **all 4,750
  negative-year `DATE` lines** vanished, a report concluded the corpus "cannot
  express BCE", and the century histogram was published with a `BCE: 0` row.

Both times the output looked entirely reasonable. That is the hazard: a wrong
date parser does not raise, it just quietly narrows the data.

**If a date genuinely does not fit the grammar**, that is a finding about the
corpus — record the raw text and say how many, rather than widening a pattern
until it swallows the value. Reaching for a regex here is how the specification
gets re-implemented badly.

### Working on Windows here

- Commit with `git commit -F <msgfile>`, not `-m` with a here-string: PowerShell
  5.1 mangles `<` and `>` in native-command arguments even inside quotes.
- Never edit UTF-8 text files with `Get-Content -Raw` + `Set-Content` — it
  double-encodes non-ASCII. Use the editing tools, or Python with an explicit
  `encoding="utf-8"`.

## ⛔ WIKIDATA EDITING STARTS 2026-09-01 IN THIS REPO

**Emma, 2026-08-23:** *"Shintowiki scripts uses a different lockdown period lol. This repo
starts at sept 1."* Then, on being shown the coupling: *"Shintowiki scripts and this one are
not the same and not really coordinated"*, and *"I think you hallucinated a coordination
between them."*

**She is right, and the coupling is gone.** `scripts/wikidata_lockout.py` used to fetch a
lockout state file belonging to `shintowiki-scripts` over HTTPS, and this file used to
assert there was *"exactly one lockout state file for all of Emma's repos"*. Nothing in
this repo ever evidenced that. An earlier session inferred it from her 2026-08-18 *"no
wikidata editing for a month"* instruction and wrote the inference down as fact.

**Why it mattered rather than being merely untidy: the check failed closed.** An unset
secret, a 404 or a network blip all reported LOCKED. From 2026-09-01 that would have
silently blocked editing this repo is entitled to do — and a blocked run looks exactly like
a run with nothing to do.

**What governs now is this repo's own date, written twice and pinned together.**
`scripts/wikidata_lockout.py` carries `START_DATE = "2026-09-01"`;
`.github/workflows/wikidata-edits.yml` carries the same in `START_DATE:`. They are two
copies because the workflow gates before it checks the repo out and cannot import the
module, so `tests/test_wikidata_start_date.py` fails if they ever disagree. It still fails
closed on an unreadable date, and it makes **no network request at all** — which is a
stronger guarantee than the agent-sharing it used to be tested for.

**`P2600` is *Geni.com profile ID*** — Emma asked directly on 2026-08-23, so it is worth
writing plainly next to the date: every batch this gate guards is of the form *this Wikidata
item is that Geni profile*.

**Nothing is blocked meanwhile, and she may not use the gate at all.** Emma, 2026-08-23:
*"If it's geni id then I'll run manual quickstatements."* Batches are written to files for
her — `reports/wikidata-geni-qid-p2600.qs`, `reports/wikidata-garborg.qs` — and no edit has
ever been attempted through the automated path. § *A start date is not a blocker* still
governs: build, review and commit now.

## Long command series run in strict order
When the user gives a long series of commands, treat it as a long series of commands to be
executed in relatively STRICT ORDER, one after another, EVEN IF the order seems not to make
sense or seems inefficient. The sequencing is intentional — the user organizes the steps so
states change in the order they want. Do not reorder, merge, or skip steps.

## Not-done taxonomy (never "deliberately deferred")
When work is NOT done, tag it with exactly ONE of: **NEEDS-DECISION** (name the decision +
who decides), **BLOCKED-ON-USER-ACTION** (a real-world action only the user can take — name
it), **BLOCKED-ON-EXTERNAL** (CI / a remote / a third party / another session's unpushed
commit — name it + the unblock signal), **NEEDS-INVESTIGATION** (not understood yet — a
to-do for the next tick, never a resting place), **UNSAFE-TO-GUESS** (could cause damage —
name the risk + what makes it safe), or **OUT-OF-SCOPE** (another repo's job — name it).
LOAD-BEARING DEFAULT: if it fits none of these with a specifically-named blocker, it is NOT
deferred — DO IT NOW. Bare "deliberately not done" / "blocked on <person>" is banned.

# currentDate
Today's date is 2026-07-30.

### Finish all 39 exports BEFORE saving any stragglers, then restart the work loop

**Emma, 2026-08-18.** The closing plan has two phases and they do not interleave:

1. **The 39 exports in `reports/export-worth.md`.** Each qualifying path gets the
   bounded treatment — an export seeded on an ancestor of the **endpoint**, then one
   seeded at the **midpoint** of whatever is still missing. Two exports, never more.
2. **Only once all 39 are complete**, save the straggler pages. That is every person
   left over on those 39 paths *plus* the 412 paths that never qualified — into
   `geni-scraping/`, one a minute, no concurrency, every path member getting their own
   page.
3. **Then restart the work loop.**

**The ordering is the instruction, not an optimisation.** Do not start page-saving
because an export is slow, and do not interleave the two to "make progress" while
waiting — the exports are the phase with a deadline attached (Emma's own hours), and
page-saving is the cheap fallback that will still be there afterwards. Her framing all
day has been that she is *"actively trying to close this thing off"*, and closing it
means the export phase ends before the scraping phase begins.

`scripts/classify-export-worth.py` decides which 39, `scripts/path-gap.py` names the
seed for each step, and `scripts/census-paths.py` is the current-state snapshot.
