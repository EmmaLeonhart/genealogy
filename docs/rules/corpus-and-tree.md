# The corpus, the merge, and the synoptic tree

**Moved out of `CLAUDE.md` on 2026-09-09, verbatim.** The ruling was to cut `CLAUDE.md`
to under 1,000 lines and put the evidence for each rule on a page that `CLAUDE.md`
cites. Nothing here was reworded, shortened or dropped in the move — this is the
reasoning, the measurements and the post-mortems behind the one-line rules.

---

### Open the FAMILY TREE page for an export seed, not the profile page

A batch of export seeds is opened as `https://www.geni.com/family-tree/index/<geni id>`,
**not** `https://www.geni.com/people/x/<geni id>`. The profile page shows one person; the
family-tree index shows the neighbourhood around them, which is what creating the
placeholder and running the export needs in front of it.

**`reports/midpoint-seeds-to-open.tsv` is overwritten every batch, and that is the
intended behaviour.** It is the handoff for the batch being opened now, not a history of
what has been opened.

**There is no already-opened filter.** Each batch is simply the top of the current
ranking. A filter built for that purpose had a bug that cut a candidate list from 778 to
7; re-opening a tab already dealt with costs one glance, and a filter costs correctness.

Keeping the picks on **disjoint chains** is a different thing and stays: without it fifty
tabs can all be standing on the same three chains, so they buy three exports rather than
fifty.

This applies to **seed batches** — the midpoint openings, the density and edge picks. It
does not change the *isolate* batches, where the thing being judged is whether one person
connects at all, nor the saved-page workflow below, which needs the profile page because
that is where the relationship panel and its `href`s live.

### `docs/export-seed-rules.md` is how an export individual gets made

That file covers where to put a placeholder profile, what to name it, and what to do when
a tree has no open slots left — a five-tier preference order with patronymics at the top,
because a patronymic names the father and so the created person is attested rather than
invented. It also fixes the export itself: **`Forest`, size 5000, strictly one at a time,
and the zips are filed into `exports/` in bulk only once every one of them is down.**

That file is the authority; do not re-derive any of it here.

**The whole loop runs under Chrome automation**, proven end to end on 2026-08-17: create
the profile in the tree view, Actions → Export GEDCOM, poll the download page, click
through.

**Relationship paths: save the page, never the pasted text.** A Geni relationship path —
the chain of people between two profiles, which Geni shows for any pair it can connect —
is the only evidence in this repo that comes from *outside* our own data: it names people
whether or not any export has reached them. Copying the panel as text keeps the names and
loses the `href`s, and the `href`s are where the profile IDs are. **Saving the page keeps
them**, so the workflow is: save the profile page from the browser into `geni_pages/`,
then `python -m genimerge path-from-html <page> -o paths/<name>.tsv`, then
`python -m genimerge path <file>` → `reports/path-*.md` and `path-*.json`.

`genimerge.genipage` does the extraction, and the difficulty is scoping: a Geni profile
page carries several hundred `data-profile-id` anchors — immediate family, managers,
followers — and only those inside `span.segment > span.name` are on the path. Matching
anchors directly yields a plausible-looking list that is not a path.

**`reports/connectors.md` and `out/connectors.html` answer "who do we lack?" across all
the paths at once.** `python -m genimerge connectors` checks every path file against one
loaded tree — a second `genimerge path` run per file would pay the whole cost of loading
the merge each time, so `--write-paths` refreshes every `reports/path-*.md` from the same
pass. It groups absent steps into **bridges** (a run of consecutive missing people, plus
the doorway to seed on and the resume point beyond) and merges bridges that share any
person into one cluster. **Rank by slots closed across every path a cluster blocks, never
by gap length**: ten people blocking five paths beat fifty private to one. The report
carries a separate **"one export?"** column because payoff and feasibility come apart at
the top of the table — nine people is the widest gap a targeted export has closed here,
and the highest-slot cluster is routinely wider than that.

**`ABSENT` on a path means "not in the tree" and nothing else.** A person walked *twice*
on one path is `REPEAT`, which counts as held. `paths/nn-basse.tsv` holds two relationship
paths end to end, so its second chain re-walks steps 1–9; conflating the two reported the
account owner as a missing person and offered him as a nine-person bridge worth exporting
for. The `used` rule that caused it is still right for the *name* fallback, where a second
step landing on one profile is a matching error; an exact ID landing twice is a file
holding two paths. `tests/test_paths.py` pins both directions, including that a repeat of
someone genuinely absent stays absent.

`genimerge.paths` **falls back to name matching only for rows with no ID**, and that
fallback is a report for a human, never an input to a merge. Do not let it become
load-bearing: run against the Jimmu path it invented eleven holes in a run of thirty and
moved the headline finding from "stops at step 30" to "stops at step 2". Its guards exist
because of specific failures — a person settled by one step is never offered to a later
one (Jelena Urošević matched Elisabeth of Hungary, the step before her, reporting the
doorway as already held); a name shared by more than `AMBIGUITY_LIMIT` people is
`UNRESOLVED` rather than held, because 73 profiles are called `n n`; and a row whose ID is
simply absent from the tree resolves to absent rather than falling back to its name.

**Later sources win value conflicts.** Geni is a live site, so two exports disagreeing on
a single-valued path means the profile was edited between them and the newer export holds
the correction. The first conflicts to appear in real data — at 45 exports; there were
none at 10 — were all `INDI.CHAN.DATE`, the profile's own last-edited stamp, where keeping
the older value is not arbitrary but wrong. Merge order is filename order, not export
date: if "later" ever needs to mean "more recently exported", sort the paths by their
`HEAD` date before calling `merge_files` and the rule follows without a code change.

**The xref is the merge key; `RFN` is corroboration checked elsewhere.**
`Merger.add_source` deliberately does not call `geni_id_of`, so a contradictory `RFN` does
not stop a merge. The cross-check runs in `inventory`, in `model`, and over the merged
output in `tests/test_merge_real_exports.py`.

**Exports are bounded, but no number here is the bound.** The first three exports each hit
3836 individuals exactly while sharing only 354 people, so they are overlapping slices
rather than copies — and that identical count read as a cap. Every export since has held
more. Ordered by the timestamp in their own `HEAD`, 28 exports read: 3836 ×3 (30 Jul),
3840 (01 Aug), 3844 (02 Aug), then on 04 Aug 3848, 3852, 3856 within twelve minutes — and
**3860 for each of the eleven exports taken between 15:21 and 16:22**. Exports holding
less (876, 1073, 1192) exhausted their component before filling.

That flat run of eleven is the part that pays: those eleven came from eleven different
seeds in three different styles and all landed on 3860 exactly, so the bound is **global,
not per-seed and not per-style** — which also rules out the walk overshooting a floor to
finish the generation it is on. Why the ceiling *moved* 3836 → 3860 over five days is
unestablished. **Do not encode the arithmetic**: a run of eleven identical values is
evidence the number sits still, not evidence it steps by four on a schedule, and it is not
a cap Geni enforces.

`genimerge.seeds.GENI_EXPORT_CAP` is **5000** as of 2026-08-17, meaning *largest yet
seen*; its docstring is the long form of this and is where each reading is recorded — do
not update the number without adding the reading there. It was 3860 when the paragraph
above was written, and the sentence about the number sitting still survived the move
rather than being falsified by it: 4008 came from a pair of exports taken seven minutes
apart that held 3972 and 4008, a ceiling that moved rather than a step of four. The 99th
export (2026-08-06) held 4004 and changed nothing. The four exports of that evening went
4016, 4020, 4020, 4020 between 18:10 and 18:19, so the ceiling **rose inside a single
nine-minute sitting** and then held for three takes — `reports/audit-downloads-2026-08-06.md`.
It is a modelling number for `reports/seeds.md` only; nothing in the merge depends on it.
`tests/test_seeds.py` fails if an export in `exports/` exceeds it, which is how 3840, 3844
and 3856 were each caught. The constant tracks the largest export *seen*, not necessarily
one that has been ingested, so the test is a floor on it rather than its source. Expect to
merge many exports over time, and expect the merge to be re-run rather than hand-edited.
See `reports/inventory.md`.

**The merged tree is one connected tree — as of 2026-08-04, and not before.** 105349
people, 56455 families, **1 component**, over 54 exports. It was two components for most
of that day (16217 Norwegian and 11501 Japanese, sharing no person and no family).
`reports/frontier.md` § Components is the live count and the thing to check rather than
this paragraph: an export that reaches somewhere nothing else does will split it again,
and that is normal rather than wrong. Disjoint components do not conflict — they just
never meet.

### The question is whether OUR TREE MATCHES GENI — never whether Geni is right

**Geni is the source. Our corpus is a stale photograph of it.** The only question a
duplicate, a conflict or an odd relationship raises is: *does our snapshot still match
what Geni says today?* If Geni holds one profile, we should hold one. If Geni holds two,
we should hold two — **even when two is wrong**, because a wrong fact that is present can
be corrected on Geni and flow through, and one we filtered out cannot.

**What this forbids.** Adjudicating whether a merge was justified. Grading a pair as "not
really a duplicate" and therefore skipping it. Deciding an export has "thin expected
value" because the pair looks like two different people. All three are the same mistake:
answering *is Geni right* when the question is *are we current*.

**What the evidence grading in `reports/geni-stale-duplicates.tsv` is for:** ranking which
snapshots are most stale, so the most valuable refresh runs first. It is not a filter on
which people deserve fixing.

**So a post-merge export is worth running even when the pair turns out not to be a
duplicate at all** — it refreshes our record of those people to Geni's current state,
which is the whole job.

### A small component is IGNORED. Do not report it, do not analyse it

A cluster of a few hundred people disconnected from the main tree is **no priority**, not
low priority. It is checkable: 0 of the 344 in one such split appear in any of the 586
relationship paths. Every path starts from the account owner's own profile, which is in
the large component, so a small component cannot be on a chain — that is what being a
separate component means. The work is clearing chains.

**The merge's component count is not a finding and does not go in a status report.** The
line the merge prints is fine where it is. Working out what is in a small component, or
which export brought it, is the unprompted analysis § *No unprompted reports* forbids.

`reports/frontier.md` § Components stays as the place the number lives.

### Path repair, export naming, and what a seed actually is

**`reports/path-jimmu.md` is the worked example of closing a path.** It checks an 83-step
Geni relationship path against the tree: 62/83 held (gap of 21) → 77/83 (gap of 6) →
**83/83**. Two `Forest` exports seeded inside the six-person window closed it. The style
mattered: that stretch crosses `her brother`, `his partner` and `her husband` links, so
`Ancestors` and `BloodTree` would have walked straight past Guarandukht Bagrationi and
Sultan Alp Arslan and never bridged. **When an export is meant to close a specific path,
read the relation column first and pick a style that follows those link types.**

**An export is named for its style, not its seed — so filenames collide.** Geni writes
`export-<style>.ged`, and **five** styles have been seen: `Forest`, `Ancestors`,
`BloodTree`, `Descendants` and `Bio`. Nothing enumerates the styles, so a sixth would land
silently. What `Bio` selects for is **not established** and should not be guessed; the one
export of it holds 4056 people, the same as the `Descendants`, `Ancestors` and `BloodTree`
takes minutes either side of it, so its size says nothing about its shape. Disambiguate a
collision by appending the seed's Geni profile ID —
`export-Forest-6000000226977233850.ged` — since the profile ID is this repo's primary key.
The `SUBM` xref is the *account owner*, not the seed, so it cannot be used for this.

**The seed is the file's first `INDI` record**, and this is checkable rather than assumed:
of the saved pages in `geni_pages/`, seven are the first `INDI` of some export and the
rest are pages saved for connections not yet exported from. **Do not expect the seed to be
the person the export is named after in conversation.** All three exports ingested on
2026-08-04 open on a profile created a minute or two before the export ran —
`export-Forest-6000000227036288825.ged` is "the Li Hong export" and its seed is an `NN`
wife of Li Yuanfeng created at 14:40:46 and exported at 14:41:36. Creating a placeholder
at the frontier and exporting from it is the technique; the filename records the seed, not
the intent.

### `reports/density.md` is where to look for the next export, not `reports/seeds.md`

`genimerge.density` counts how many exports contain each person — **presence** — and then
finds *connected runs* of people almost no export reached. One thin person is the rim of a
ball and means nothing; a run of thousands is a neighbourhood sampled once and never
returned to. `seeds.md` ranks by doorway count and has never been validated against an
outcome; density is measured from what the exports actually did.

### The `Descendants` campaign is about TIME, not thinness

`Descendants` exports are run because the tree is biased towards ancient and medieval
individuals, and the goal is to reach modern times. That is a different target from
`reports/density.md`, which ranks by how few exports touched a neighbourhood and knows
nothing about dates. The two can point the same way and often will, but do not present
density picks as serving this goal, and do not describe a `Descendants` take as
thin-region work. `Descendants` fans out downward, which is what makes it the instrument
for reaching later generations.

**A `Descendants` export reaches about twelve generations forward, and that outranks every
seed heuristic.** The export is a breadth-first ball of ~4076 people, so it fills the
generations *nearest* the seed; a descent branching twice per couple hits 4096 at
generation 12 unaided. A ball therefore carries roughly **350 years** and no choice of
seed changes it.

A batch of **eleven** `Descendants` exports, all seeded on ancient or undated people,
added **18,218 people** — median birth year **1582** — and **four** born after 1900. The
1500s gained 3,369, the 1600s 3,045, the 1800s 101, the 1900s 4. **No person born 1800 or
later gained a child, of 14,371.** The campaign is about reaching modern times and this
did not move it.

**So: seed where you want to arrive.** To deliver people born after 1900 an export must be
seeded after about 1750. `genimerge.descendants.REACH_GENERATIONS` and `REACH_TARGET`
encode the screen, and `reports/descendants.md` leads with § *Seeds that can reach 1900*.
Everything else in that report is background.

**The campaign's seeds are 1800s people, measured not argued.** Of the 7591 candidates a
ball can get to 1900 from: 1500s 605 (8%), 1600s 1426 (19%), 1700s 1777 (23%), **1800s
2980 (39%)**, 1900s 803 (11%). Two independent reasons put the answer there rather than
later — a seed born 1850 needs two or three generations to pass 1900 and has them to
spare, and **Geni redacts living people**, so a 1900s seed's descendants largely cannot be
exported at all. The 1800s are the last cohort whose full descent is retrievable, not a
compromise.

**One seed per couple — `drop_duplicate_balls`.** Two parents of the same children have
the same descendants, so a `Descendants` export from either returns the identical ball.
This is not an edge case: the ranking rewards a large recorded family and both parents of
one score alike, so **a quarter of the shortlist was the same export listed twice**
(10071 → 7591). Ranks 1 and 2 were Margaret Outlaw and Samuel D. Outlaw, a married couple
with the same 20 children, offered as two suggestions.

**`out/reach-1900-seeds.html` is the thing to actually use** — 600 candidates, filter by
decade, sort by any column, pick by eye. The ordering is untested and the page says so on
itself. Read `line reaches` against `ball reaches`: the gap is roughly what an export
would add.

**Two seed-choosing methods have been refuted by measurement. Do not propose a third on
reasoning alone.** `reports/descendants-backtest-2026-08-07.md` is the record, and it
exists because `out/merged-134.ged` was kept before the batch was merged — **keep the
pre-batch tree whenever a batch lands**, it is the only way this question is answerable.

- *"Small but nonzero descent"* — refuted. All ten seeds that already existed had
  **exactly one recorded child** and descent-path counts from 371 to **1.5 billion**,
  every one outside the 1–20 candidate band. The report would not have proposed any of
  them.
- *"The rim of a cut-off ball"* — refuted the same day. Childless people inside an export
  that came back at the size bound gained children at **0.71%**, *below* the 1.00% base
  rate and below the 1.05% of people on no rim. It anti-predicts.

### `reports/descendants.md` ranks the downward edge

`genimerge.descendants` ranks the **downward** edge the way `frontier` ranks the upward
one, and buckets it by period so the ranking can be read one century at a time.

- **The signal is a descent-path count that is small but nonzero**, and both halves carry
  weight. *Nonzero* means Geni recorded at least one child, so the line demonstrably
  continues and there is something below to follow. *Small* means it has barely been
  followed. A person with **zero** recorded descendants is deliberately excluded: nothing
  in our data separates childless from unexplored, which is the same discriminator
  `density` applies upward with its doorway column.
- **Count descent paths, not distinct people.** The measure is
  `paths(p) = Σ over each recorded child c of (1 + paths(c))`. Somebody reachable down two
  lines counts **twice**, and that is the point: the question is how many lines come down
  from a person, and a descendant reached twice is two lines. Distinct-person counting is
  not merely irrelevant here but plausibly worse — pedigree collapse is dense in this
  tree, and de-duplicating it makes the top of a wide, repeatedly-intermarried descent
  look narrow. `frontier.descendant_counts` still counts distinct people for callers that
  want that.
- **Rank on `generations followed` (`depth`), never on `stall`.** Stall — years between
  the line's last recorded birth and now — is a trap: a person's own birth year is a floor
  on how far their line reaches, so sorting a 100-year band by stall sorts it by birth
  year, and **every band's top pick came out born in the band's first year**. That is
  where the band edge fell, not a finding. Depth is available for dated and undated people
  alike and does not move with the band. Stall stays as a column worth reading.
- **The path count is why this module is cheap.** Distinct-person counting needs a set
  union per person: `frontier` carries a bitmask, one bit per person per person, a
  kilobyte each at 8766 people and 32 KB each at 257219 — tens of gigabytes. The
  post-order sum is O(V+E) and exact at every size. The sums saturate at `PATH_CEILING`
  (1e12) because path counts compound through shared subtrees and a deep intermarried
  ancestor's true count runs to thousands of digits; that is a display bound thirteen
  orders of magnitude above any usable `small`, never a candidacy one.
- **A candidate whose parent is also a candidate is dropped, per band.** An export seeded
  on the ancestor covers the descendant's line plus branches off it we never saw, so the
  ancestor is strictly the better seed and a six-person line would otherwise be reported
  six times. Checking parents alone suffices, because path counts rise strictly upward — a
  parent's count is at least `1 + child's`. Per band rather than report-wide, so a band
  keeps its own best pick.
- **A depth of 0 must mean "no children", never "the child is in a cycle".** `_post_order`
  drops an edge back into a node still being expanded — right, a person is not their own
  descendant — and both depth functions then guarded with `if c in depth` and fell through
  to `0`, which reads as *childless*. Depth is the primary ranking key **ascending**, so
  those people sorted above every genuine candidate: `Arne` (`6000000007351784249`), one
  descent path and no open ends, held the top of the `undated` band of 136953. **8** of
  the 123256 people with a recorded child were affected — a tiny population with an
  outsized effect, because being ranked first is a position of exactly one per band.
  `frontier.ancestor_depth` had it identically (**5** of 208863), invisible only because
  nothing ranks on it. Both now contribute `0` for an unresolved neighbour, so a cycle
  *truncates* the measure instead of falsifying it. This is the same shape as the date
  parser's silently-dropped years: **a guard against a malformed case, paid for with real
  values that then vanish without trace.** The tree holds 15 ancestry cycles across 55
  people — `frontier.ancestry_cycles` reports them.
- **The metric change moved the implementation, not the answer.** Candidates went
  52196 → 52171 and the per-band picks barely shifted: path counts and distinct counts
  coincide almost exactly at the small end, because a line of twenty people rarely
  re-converges. They diverge in the tail, where this report does not look. Descent paths
  are right because they are the right *question*, not because they reranked anything — do
  not cite a numbers change as their justification.
- **Both axes are reported because neither covers everyone.** 53% of the tree carries no
  birth year, and those people are invisible to the period view. Generations-above ranks
  them — but it is **not a second clock**: it measures how far *we* have traced upward, so
  an untraced person looks shallow whenever they lived. No date is ever inferred.

### "Is X present?" means BOTH stores. Answer for each, and name which

**"Is X present?" is completely agnostic between Wikidata and Geni.** It asks whether something
exists in the material this project works with, not which container it sits in. So:

- **Check both.** The corpus under `exports/` (plus `gedcom/`), and the local
  Wikidata store under `wikidata/items/` with its index in
  `out/wikidata/store-index.sqlite3`. Never one and report as if it were the
  question.
- **Say which store each answer is about, in the answer itself.** "Not present"
  with no store named is not an answer, it is a trap. "On Geni: 35 profiles, in
  `exports/gaps/export-Bio-…`. On Wikidata: none of the 35 carry an item."
- **Say when the absence is bounded.** Our exports are a sample of Geni, so
  absent-from-corpus never means absent-from-Geni. The Wikidata store is a
  *Geni-shaped slice* — **2,246,827** items as of 2026-08-26, seeded from P2600
  holders and their neighbours — so absent-from-store never means absent-from-Wikidata. Both
  limits get stated, not implied.

**How it went wrong, because the shape recurs.** Asked whether the pre-1600s Samaritan high
priests existed, the answer given was scoped silently: first to Wikidata (0 of 35 linked), then
to `order.life` (0 of 35), each true, neither the question. That tree had been built on Geni by
hand, and the answer came back "they are not present". The 35 were in the corpus the whole time.

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

**"Region" is a neighbourhood in the family graph, never a place.** Do not classify people
geographically: birthplace strings
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
name.** `_MARNM` *is* the married name, confirmed on the female records checkable against
history (Judith `/de France/` → `Flandre`). But 244,392 of 444,874 `NAME` records carry the tag and most are not doing that:
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

**A hand-recorded identity or label correction goes in a TRACKED TSV.** Hand-made
Geni-to-Wikidata identities live in `reports/manual-identifications.csv`, and a label that can
only be supplied by hand — *Name should be Jacobus Bothniensis* — in
`reports/label-corrections.tsv`, which `derive-labels.py` applies at derivation so the exports
stay the record of what Geni actually said.

**⛔ THERE ARE TWO HAND-LABEL FILES AND THEY ARE NOT INTERCHANGEABLE.** The one above is keyed
on the **Geni id**, carries **one Latin label**, and is read at DERIVATION — it corrects what our
tree thinks somebody is called. `reports/label-applications.tsv` is keyed on the **QID** and
carries `qid, kind, lang, value` — *this item, this language, this exact string* — and goes
**straight into the QuickStatements batch, verbatim**. The first four rows:

    Q140568870|Lzh|"李命玥"        Q140568870|Aja|"閻魔獅心"
    Q140568870|Lja|"エマ・レオンハート"  Q140568870|Lko|"엠마 레온하트"

Neither existing file could express this: the derivation one has no language and no alias, and
`_label_corrections` is every ground we DERIVE — an abbreviation we expanded, the birth-name
flip, a description marker, a generation suffix — each computed from our own data by
construction. `kind` is `L` or `A` only; a `D` row is **refused by name**, § *NO descriptions*
being categorical.

**Nothing thinks about the value.** No transliteration, no `label_in`, no consensus vote, no
title rule. § *WIKIDATA'S LABEL BEATS OURS* protects an item somebody else labelled from OUR
derived proposal; a hand-typed string is not that.

**⛔ AND A DERIVED EDIT FOR A HAND-SET SLOT IS DROPPED.** Those first four are corrections of
ours — the rule gave `Q140568870` `エマ・レオンハルト`, `艾玛·莱翁哈尔特` and `엠마 레온하르트`
— so both lines would be emitted, land adjacent under `_cap_label_edits`'s per-person ordering,
and **a label REPLACES: the last one written wins**, which is the derived one. The batch would
read as though the hand correction had gone out. `_without_hand_covered` removes them. An **alias is not covered**, because an alias adds rather than replacing.

**IT QUEUES LIKE ANY OTHER LABEL EDIT** — a stronger level of the regular label application, not
a higher priority. Giving these QIDs `_cap_label_edits(priority=…)` was wrong. **Stronger means
it wins its SLOT, not its place in the queue.**

**`reconcile` is deleted, and name matching does not come back.** The name-search matcher was
removed outright, and the whole module deleted rather than stripped, along with
`genimerge reconcile` and `genimerge expand`. It held a live Wikidata client, which is the other
reason: a command that queries on a keystroke is how
the 2026-08-07 rate-limit incident happened. The four offline pieces that other
modules still need moved to `genimerge.matching` — two year tolerances,
`year_of` for **Wikidata** time literals, and `distance_from_matched`. Nothing
in `matching` makes a request and nothing in it compares names.

**Stdlib only.** `urllib` covers the Wikidata SPARQL endpoint. Add a dependency
only when the stdlib genuinely cannot do the job.

**Layout.** `exports/` **the corpus** — every Geni export, one directory per
batch, read recursively · `paths/` relationship paths generated from saved pages
· `geni_pages/` saved Geni profile pages · `src/genimerge/` the package ·
`reports/` generated reports worth keeping in git · `out/` generated data, **tracked**
· `tests/` pytest.

**`out/` is NOT gitignored, and that is deliberate.** The old `out/*` rule cost real work: the Wikidata
download-state index lives there, a restart lost it, and the downloader believed all
514,876 seeds were unfetched while 1.4M items sat on disk. **Only the files GitHub
physically refuses are ignored, one explicit line each** — `out/merged.ged`,
`out/merged-*.ged`, `out/wikidata/download-state.sqlite3`,
`out/wikidata/store-index.sqlite3` and `out/wikidata/labels.tsv` (187 MB, rebuilt by
`scripts/extract-wikidata-labels.py` in ~10 min) — all rebuildable, so the cost is a rebuild and
never data. `out/wikidata/relations.tsv` (65 MB) and `dates.tsv` (18 MB) are under the limit and
stay tracked, so a clean clone can run the zipper after one labels rebuild.
`.gitignore` line 32 carries the reasoning.

This paragraph said "gitignored" for ten days after the rule changed, and the stale word was not
harmless: it was cited as grounds for adding `out/` back to `.gitignore`, and the change was
approved on the strength of it. The `.gitignore` was right and the documentation was wrong.

**`exports/excluded/` is the one part of `exports/` that is NOT corpus.** Added
2026-08-15. An export lands there when Geni has since **changed a relationship it
records**: the merge unions `FAMC`/`CHIL` and never drops one, so a parent link
Geni has deleted survives forever once any export carries it, and no later export
can undo it. Excluding the file is the only mechanism that removes it.

**The files stay in git** — the never-delete-a-GEDCOM rule is untouched. They are
tracked, readable, and still the record of what Geni said that day; they are only
kept out of the merge. `genimerge.sources` skips them and `excluded_files()`
lists them.

**The condition is checked now, never predicted.** Excluding an export *once* a later one covers
its people is a prediction of something that may or may not happen; the rule is to move the file
into the excluded directory and check that every individual in it is present in at least one
other export. `tests/test_repo_invariants.py::test_no_excluded_export_strands_a_person` is that
check, so an exclusion that would drop somebody from the tree fails the suite.

**The worked case, `excluded/samaritans/`** — four exports taken before
`Yitzhaq I ben Tsedaka` (`6000000227245553985`) existed on Geni. Geni had linked
**Tsedaka II → Abram** directly, skipping him; when he was created, Geni rewrote family
`F6000000178795360833` **in place**, swapping its child from Abram
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
grouped into a directory named for the person exported from
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

**Correcting a record in an export does nothing until the tree is
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

**There is ONE store and it is `exports/`. Do not reintroduce a second.** `data_lake/`
was that second store and was deleted 2026-08-05; its unique files are in
`exports/originals/`.

**Two exports can share a style *and* a seed, and then the name collides.**
Seen on 2026-08-05: two `Forest` exports of `6000000227040338177` taken seven
minutes apart, 3972 people and 4008. Check containment before inventing a
disambiguator — the 3972 was a strict subset of the 4008, so keeping only the
larger lost nothing.

**Never overwrite an existing `.ged`. A new export is always a NEW file.**
Stated after it was broken. `cp`-ing a freshly
downloaded export **on top of** an existing tracked `.ged` clobbers a committed
file, and that must never happen. When placing an export, if the destination
path **already exists**, STOP — do not overwrite it. The download goes somewhere
as its own new file (its own seed-named path, or a named bulk directory such as
`fleshing-out/`), and where it goes is **a decision, not a default to guess**. Ask. This was got wrong when a 13 AUG re-export of the Ogasawara Descendants
seed was `cp`'d over `exports/descendants/export-Descendants-6000000227040613855.ged`
— it belonged in `exports/fleshing-out/` as a new file, and the committed
descendants copy had to be restored from git. Two exports sharing a seed *and* a
style is a filing question to raise, never a licence to overwrite. **Before any
`cp`/`mv`/`>` onto a path under `exports/`, check it does not already exist.**

**The one exception, and it is narrow: a BYTE-IDENTICAL duplicate.** Authorised for
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
line at a time**, deliberately: an unignored zip shows up in `git status`, which is how a
download announces itself. Do not replace those lines
with a `*.zip` pattern — it would look tidier and would destroy the signal.

**Never write a `*.ged` or `*.zip` pattern into `.gitignore`. Ever.** Stated after both halves
of it had already been broken. The two
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

### "SYNOPTIC TREE" — the two things it means, and which one each usage is

The term is consistently conflated between the union of all the Geni GEDCOMs and the union of
that tree with all data sources. Both meanings are in use and both are legitimate;
what is not legitimate is a sentence where the reader cannot tell which.

- **the Geni union** — every `.ged` under `exports/` merged, i.e. `out/merged.ged`. This is what
  `scripts/rebuild-everything.py` builds, what a new export is *merged into*, and what
  *"rebuild the synoptic tree"* always means.
- **the full union** — that tree joined to every other source, Wikidata above all. This is what
  the structural walk *builds up*, what `reports/synoptic-correspondence.tsv` is a correspondence
  **for**, and what the zipper join feeds.

**Measured 2026-09-01: 975 usages across 61 files**, of which 81 are live prose rather than
transcript or devlog history. `scripts/census-synoptic-usages.py` → `reports/synoptic-usages.tsv`
is the census and re-runs.

**And the phrase *"the union of the synoptic tree and the Geni tree"* meant neither.** It is
**Wikidata's state ∪ Geni's state** — what the item already holds plus what Geni
supports. Under either definition above the sentence was a tautology or a redundancy, which is how
it was spotted. `docs/daily-algorithm.md` and this file now say the thing that was meant.

### The four big derived CSVs are committed GZIPPED

Gzipped because this is long term and no more data is being added to the tree — only processing.

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
untouched. It is ignored by necessity.

### The ONE place a name may choose: inside a zipper slot, dates first

**Dates first, then names**, and the provenance of a zipper merge is recorded.

**⛔ THE THREE-STEP CASCADE IS A LOCAL DECISION, NOT A SPECIFICATION.** *Dates first then names*
was said about the **2x2 sibling** case; `solo -> date -> name` was generalised out of it into an
architecture and then presented as though it had been specified. The name exception below is
sanctioned for that case; the shape around it is on trial.

**Solo child says nothing on its own.** One unmatched person on each side is *trivially* unique,
so uniqueness proves nothing when the set has one element. **`reports/zipper-reliability.md`
measures it**: `child`+`solo` disagrees with independent sources **14.9%** of the time against
**0.7%** for `father`+`solo` — twenty times. Solo *parents* are fine; solo *children* are not.

**Solo child STAYS, flagged as the weakest thing in the join**, given that 14.9%. All 3,326 remain in `reports/zipper-pairs.tsv` carrying
`method=solo` and `slot=child`, so any consumer can exclude them in one filter — and the queued
solo-children analysis may yet rescue them, since sex agreement (`P21` against our `sex` column)
is free evidence the join ignores entirely. **Do not silently drop them and do not silently trust
them.**

**The standard for every rule here:** *"a lot of these rules are empirical and we need to
empirically study our data to figure out what to make of it. Don't jump to conclusions based on
what sounds like it might be true. Even parents isn't certain."* The slot ordering in
`zipper-join.py` is a **hypothesis under test**, not a settled rule.

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

**Provenance is mandatory, and it is a CHAIN.** A zipper merge should almost always carry a
relatively large chain of provenance — not a single justification, but a potentially very long
series of them. `reports/zipper-pairs.tsv` carries one step —
`round, geni_id, qid, slot, method, from_geni, from_qid, evidence`; it previously carried round,
geni id and qid alone, because the slot was assigned into the tuple as `""` and never emitted, so
no pair could be audited at all. `scripts/zipper-provenance.py` walks the steps into chains (max
depth 8, mean 2.7) and checks each against every *independent* correspondence in the repo.

**Support and contradiction both propagate along the chain; it goes both ways.** An independent
resolution agreeing with an inferred step corroborates everything above it; one disagreeing
poisons everything above it. **The hand verdicts in `reports/emma-judgments.tsv` are nodes in
that graph** — recording manual decisions is what makes them enter the provenance. 25,570 of
44,725 pairs are corroborated somewhere in
their chain; 187 are poisoned.

**Poisoned is a reading, never a deletion.** The bar for stopping the join is high: it needs a
pretty good reason.

### 1600-1900 is the band where NAMES LIE and YEARS decide

**In this band the same person genuinely has several names, each of them correct.** People
of the 1700s, 1800s and early 1900s — modern but not contemporary — are frequently bilingual
in the records, so their names are represented in many different ways and formed from
different places.

**Measured over 207 hand verdicts, and it is not a small effect: 147 of them — 71% — spell the
name differently on the two sides** after folding case and diacritics. In the 1600-1900 band it
is 138 of 196, **70%**. A string comparison would have rejected seven of every ten pairs
confirmed by hand.

**Three mechanisms, none of them a spelling mistake:**

| | our side | Wikidata |
| --- | --- | --- |
| **language of the record** | `Gustav Adolf Järnefelt` | `Kustaa Adolf Järnefelt` (sv/fi) |
| | `Johan Jöransson` | `Johann Goransson` (sv/de) |
| | `Odert Reinhold von Essen d.y.` | `Odert Reinhold von Essen nuorempi` |
| **birth against married name** | `Lovisa Christina Herman` | `Lovisa Christina Schönherr` |
| | `Amalia Eleonora von Lepel` | `Gräfin Amalia-Eleonore Henckel von Donnersmarck` |
| **a title inside the label** | `Charlotta Lovisa Gyllenkrok` | `Baroness Charlotta Lovisa Gyllenkrok` |

**Why this band and not others.** These people are documented in two languages at once - Swedish
and Finnish, Swedish and German, vernacular and Latin - and the archive a given record came from
decides which form is written down. Earlier people are recorded once, in Latin, by one authority.
Later people are recorded in a settled national orthography. The 1600-1900 stretch is where one
person genuinely has several names, each of them correct.

**So the ordering in `zipper-join.py` - solo, then date, then name - is confirmed rather than
merely assumed, and the reason is now known.** The date step is not just "more precise than
names"; in this band the names are describing something other than identity. Do not promote the
name step, do not add a similarity threshold to rescue the 71%, and do not read a name mismatch as
evidence against a pair.

**And it says where a discriminator is worth building.** Birth year is on both sides for almost
every one of these people. `reports/zipper-reliability.md` already measures `date` at **0.0%**
disagreement against `solo`'s 11.8% and `name`'s 9.2% - the same conclusion from the other
direction, arrived at before anybody had the reason.

### Our side could never have two children — check the separator before believing a distribution

**`reports/derived-family.csv` separates multi-valued cells with ` | `, spaces included.** Every
consumer must split on it. `zipper-join.py` handled `,` and `;` only, so a five-child cell parsed
as the single token `"1050090 | 1050271 | ..."`, matched nothing, and the person reached the join
**childless**. 379,251 people have two or more children and every one of them arrived with none.

**The tell was a distribution that was too clean.** `reports/zipper-ambiguous.tsv` held 615 rows
and not one was `2 × 2` — read at the time as "two-against-two is rare", when the truth was that
our side could not *have* two. It was spotted from the outside, as the join not hitting the hard
points.

**And there were two bugs stacked.** Splitting on `|` alone yields `"1050090 "` with whitespace,
which still missed the index — the first fix moved the pair count by **exactly zero**, which is how
the second was found. A fix that changes nothing is evidence, not reassurance.

This is the same shape as the date-parser failures recorded above: **a parser that silently narrows
its input instead of failing**, with downstream counts that stay plausible while the data shrinks.

**It has now happened five times outside dates, in one week**, and every one printed a plausible
number that was about the instrument rather than the data:

| what | what it printed | what was true |
| --- | --- | --- |
| `split()` unaware of ` \| ` | 615 ambiguous slots, no `2x2` | 379,251 people arrived childless |
| `\|` split without `.strip()` | pair count moved by **exactly zero** | every token missed the index |
| `father[child] = husb` | census read **0** multi-parent people | 1,663 of them |
| sex rate over `zipper-pairs.tsv` | **0.0%** for all four shapes | measured the filter, not the join |
| `chart_name` column that does not exist | all 10 pairs *"no item held"* | 196 names carry a QID |

**An empty or narrowed join is indistinguishable from an absence of data**, and absence is exactly
what these reports are built to detect. So a join that matches nothing must fail loudly.
`tests/test_join_sanity.py` is the guard — 26 checks over the real files.

**A guard that has not been seen to FAIL is not known to guard.** Its first version asserted that
>50% of multi-value tokens in `derived-family.csv` resolve to a person, and **both historical bugs
passed it** — 58.5% and 86.3% — because single-valued cells have no separator and resolve either
way while being the large majority. Restricted to cells that actually hold several values the
separation is total: **100.0% against 0.0% for both**. That is the same mistake in miniature as
the five it was written against, and it was caught only by deliberately reintroducing the bugs.

### Merging the two trees is a walk up the relationships, not a name search

**This has not actually been done yet.** It has been attempted, not completed.

**The method is structural: walk up the parental lines and merge the parents where Geni and
Wikidata both hold one.** The same applies to every other relationship, and it is a critical part
of building up the synoptic tree. Start from somebody holding **both** a Geni ID and a QID, walk
`P22`/`P25` against our father/mother, and where both sides have a person in the same position,
that is a merge — **merged on whether something is the mother on both sides, unless the mothers
really conflict.**

**Labels confirm a position; they never choose one**, and that is **not** a reversal of *no name
similarity, ever*. The structure picks the pair — Wikidata's `P22` of this item against our father of
this Geni ID — and the label is read to check the pair is not absurd. Searching
Wikidata for a name is the deleted `reconcile` matcher, and it stays deleted.

**Two things come out of the walk:**

- **Our own `QID` ↔ Geni ID correspondence**, built from the merges rather than from `P2600`
  alone.
- **A placeholder for anyone on Geni and not on Wikidata**, created later, because the whole
  point is expansion and a very large number of individuals will be merged.

### The practical goal is ONE DENSE NEIGHBOURHOOD, not a comprehensive import

A full import of all the Geni data onto Wikidata is not feasible. What is feasible is taking the
account owner's own position from completely unlinked to an extremely dense neighbourhood of
Wikidata, and that is the practical goal.

**So proximity to that position beats volume.** A thousand people on the far side of the tree are
worth less than fifty in the home neighbourhood, and any ranking that optimises for total people
added is optimising for the wrong thing.

**This is what the Nordic result was really telling us.** Norwegian and Swedish
academic isolates saved at **86–94%** against **34–39%** for academics with no country filter —
not because Nordic records are better, but because Norway and Sweden are *where the home
neighbourhood is linked*, so a path exists and is short.

**It also sets the stopping rule.** The wider Nordic pool hits diminishing returns; 7,748
unopened Norwegian and Swedish isolates is not a backlog to burn down. **Manual labour is the
constraint** — measured at 4.7 profiles a minute, that pool is ~27 hours of it.

**Tightest first: Rogaland and Stavanger.** Those are the closest people and the most likely to
yield clear examples, since the line comes from there — so place beats nationality beats
occupation as a filter.

### The Samaritan family relationships are DONE. Do not audit them

**The family relationships of the Samaritans are done.** That tree was built on Geni by hand.
**It contains errors, and they stay** — it is good enough and the work has moved on. So finding
one is not a discovery and reporting one is not a service. This
is the export-analysis reflex one section down, wearing a different costume.

**What this does not forbid.** Work *about* those people that is not an audit of
their relationships: giving them Wikidata items, normalising their office and
succession, classifying their **names** — `ben Yitzhaq` is a patronymic and that
is name work, not a relationship check.

**Two name forms the Samaritans use that the classifier does not yet handle**, which belong in
the name-modelling document rather than being guessed at here:

- **Ordinal patronymics** — `Yitzhaq I ben Tsedaka`, `Tabia III ben Yitzhaq ben
  Abram`. The ordinal sits between the given name and the patronymic, and it is
  part of how the person is named rather than decoration to strip.
- **Chained patronymics** — `Yaacob II ben Uzzi ben Yaacob ben Aaharon` is four
  generations in one string. `classify-patronymics.py` reads only the first
  `ben X`, so the grandfather and great-grandfather are invisible to it.

**How it went wrong:** a stale queue item said Wadah Cohen's father was missing. The right move
was to notice the item was stale and delete it. Instead the relationships were walked and
reported back. They were fine — the intervening `NN ben Amram ben Yitzhaq /Cohen/` had been
created the week before.

### The Bureätten campaign ends on COVERAGE. Re-measure after every export

**Not every Bure person needs an export of their own; they all need to be IN some export.** The
campaign is over once everyone is covered, because these people are a family and therefore
heavily linked to each other.

**The target is that all 251 sv.wikipedia Category:Bureätten people carrying a Geni id are
somewhere in `exports/`.** Not one export each — the number of exports it takes is whatever it
takes, and the campaign is over the moment the absent list is empty.

**The reason it converges: they are a family.** A `Forest` export returns up
to 5000 people, so one seeded anywhere inside the network sweeps in many of them at once. Seeding
each absent person in turn would be mostly redundant work.

**The campaign is COMPLETE as of 2026-08-31: 251 of 251 covered**, and
`reports/bure-to-export.tsv` is down to its header row. So the re-measure below is no longer
a standing obligation after every export — run it only if the roster itself changes.

`scripts/bure-coverage.py` is the re-measure and **ran after every export**. It writes
`reports/bure-coverage.tsv` (all 251, with where each was found) and rewrites
`reports/bure-to-export.tsv` to the still-absent ones, which is what the loop consumes. It reads
`reports/derived-labels.csv` for the merged tree plus a raw scan of every `.ged` **modified more
recently than that file** — exactly the set the merge has not seen, wherever it was filed. Naming
directories instead was the first version and it silently under-reported coverage for anything
filed elsewhere, which looks identical to somebody still needing an export.

**It worked on its first run and from an export not aimed at the network at all**: the Andreas
Olai `Forest` swept in Pehr Kalling and Johan Otto Nauckhoff, taking the list 100 → 98, and
neither Andreas nor his brother is in `bureatten.csv`.

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
matters — an export slot, and the patience to sit through it.

**So, before every export, run the check and put the number in the commit message:**

- *Are these people already here?* — `grep -l '@I<id>@' exports/**/*.ged`, or
  `scripts/measure-export-newness.py` for the general question.
- *Is this property already here?* — `grep -c 'wikidata.org' exports/**/*.ged` and its like.
- **Never let a single-file measurement stand in for a corpus one.** That is what
  `match-izumo-export.py --corpus` exists for, and its docstring says why.

An export that turns out redundant is still committed and never deleted — the
never-delete-a-GEDCOM rule is untouched. The point is not to run it.

### The job with an export is to integrate it, not to analyse it

**This is not a data analysis project. It is a project for editing Wikidata to add more stuff.**
When a new export lands, the task is to **integrate it into the tree** — place
the `.ged`, commit, re-merge if needed — and nothing else. Do **not** compare it
to an existing export, diff it, characterise what changed, count what it adds,
or narrate any of that. Unsolicited analysis is not wanted, and every comparison of that kind
costs a turn to shut down (the 07-vs-13 AUG Ogasawara diff being the case that named this rule). The one exception is what integration
mechanically forces — checking a destination path does not already exist before
placing (see *Never overwrite an existing `.ged`*) — which is a safety check,
not analysis. The tree is the substrate; the deliverable is Wikidata edits.

### The account owner's own profile: the middle name is intended on Geni and stays off Wikidata

Two separate facts, and the second is the rule. The middle name on that Geni profile is
**deliberate** — not a data error, nothing to correct, nothing to ask about. And it is **not to
be emitted**: no `P735` with `P3831` → `Q245025`, no
appearance in a label, in any language.

**It is in the corpus now.** No export held it when the rule was written; a later one did. `out/merged.ged` carries `1 NAME Emma Himiko /Leonhart/` as a second
`NAME` record, and `reports/derived-labels.csv` shows it under
`further_latin_names`.

**Checked: nothing emits it.** No batch contains the string, and the only edit referencing
`6000000001846508982` anywhere is the `P2600` *Geni.com profile ID* from a hand-recorded
identification — no label, no name, no sex.
The rule holds because the label emitters use `label_en`, which is the corrected
single name, and never `further_latin_names`. It is written here rather than in the queue because
it governs how the project works and has no step attached.

This is the same shape as § *The account owner's name is Empress Jingū*: what a profile says and
what gets emitted are separate questions, and the emitter is where the answer lives.

### The account owner's name is Empress Jingū

**Profile `6000000001846508982` is Empress Jingū** — the account owner, and the seed of the first
exports. Geni was renamed; the exports taken before that were
not, so the old name was in every GEDCOM, every derived report, and the prose
that quoted them. It was removed from all 223 of them on 2026-08-12.

**The name that is gone does not get written down again** — not in a comment, not
in a report, not as a "superseded name" column, not in a script that exists to
remove it. The exports themselves carry the corrected name, so nothing has to
re-assert it; where a correction cannot come from an export,
`reports/label-corrections.tsv` records it and `derive-labels.py` applies it at
derivation.

If a future export reintroduces it, correct the record and regenerate — do not
add a note explaining what it used to say. An earlier commit kept it in a
`further_latin_names` column and called that preservation rather than erasure.
That was wrong.

**Other people named Borsheim exist in this tree** — 391 lines carry that
surname legitimately. Never substitute on a bare surname; it rewrites strangers.

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
