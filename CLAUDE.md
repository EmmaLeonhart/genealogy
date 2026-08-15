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

`genimerge.seeds.GENI_EXPORT_CAP` is **4940** as of 2026-08-15, meaning *largest
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
carrying more than one Geni ID** — this is ordinary. It is also the general rule
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
`reports/` generated reports worth keeping in git · `out/` generated data,
gitignored · `tests/` pytest.

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
| P1545 | series ordinal | string — **qualifier**, not a claim |
| P3831 | object of statement has role | item — **qualifier** saying *which kind* of name this `P735` is |
| P144 | based on | item — on a **patronymic name item**, points at the name it derives from |
| P5278 | surname for other gender | item — pairs `Olsson` with `Olsdotter` |
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

**A patronymic is not a middle name, and that distinction is Emma's**
(2026-08-15). Geni writes `Ole Olsen` into `GIVN`, so the patronymic lands in the
position a middle name occupies — `Olsen` is a *given* token for 742 people and a
surname for 266, measured in `reports/name-classes.md`. Her model separates them:
the name item is an **instance of `Q110874`**, and the `P735` statement carries
`P3831` → `Q110874` where an ordinary middle name would carry `Q245025` and a
first given name `Q202444`. `P1545` still numbers them in order. *"The daughter
and son would be the same thing"* — `-son` and `-datter` are one category.

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
The suite is fast, needs only pytest, and covers the real 24 MB exports. The one
thing local runs cannot do is the Python version matrix — `tests/test_python_floor.py`
is a partial stand-in for that, and says so.

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
