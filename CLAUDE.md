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

`genimerge.seeds.GENI_EXPORT_CAP` is **4020** as of 2026-08-06, meaning *largest
yet seen*; its docstring is the long form of this. It was 3860 when the
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
styles of the *same* seed, Eric Borsheim `6000000087535357291`, which is also
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
- **Both axes are reported because neither covers everyone.** 53% of the tree
  carries no birth year, and those people are invisible to the period view.
  Generations-above ranks them — but it is **not a second clock**: it measures
  how far *we* have traced upward, so an untraced person looks shallow whenever
  they lived. No date is ever inferred.

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

**Names** — the part of `todo.md` that needs new items created

| ID | label | datatype |
| --- | --- | --- |
| P735 | given name | item — name items are `Q202444` given name, or `Q12308941` male / `Q11879590` female / `Q3409032` unisex given name |
| P734 | family name | item — name items are `Q101352` family name |
| P1950 | second family name in Spanish name | item (not applicable here) |
| P1477 | birth name | monolingual text |
| P1559 | name in native language | monolingual text |
| P1545 | series ordinal | string — **qualifier**, not a claim |

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
