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
`python -m genimerge path-from-html <page> -o data_lake/paths/<name>.tsv`, then
`python -m genimerge path <file>` → `reports/path-*.md` and `path-*.json`.

`genimerge.genipage` does the extraction, and the difficulty is scoping: a Geni
profile page carries several hundred `data-profile-id` anchors — immediate
family, managers, followers — and only those inside `span.segment > span.name`
are on the path. Matching anchors directly yields a plausible-looking list that
is not a path.

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

`genimerge.seeds.GENI_EXPORT_CAP` is **3860**, meaning *largest yet seen*; its
docstring is the long form of this. It is a modelling number for
`reports/seeds.md` only — nothing in the merge depends on it.
`tests/test_seeds.py` fails if an export in `data_lake/` exceeds it, so the next
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
writes `export-<style>.ged`, and `Forest`, `Ancestors`, `BloodTree` and
`Descendants` are the styles seen so far. The first three exports are all three
styles of the *same* seed, Eric Borsheim `6000000087535357291`, which is also
their `SUBM` xref. A second `Forest` export from a different seed therefore
arrives with a filename already taken. Disambiguate in `data_lake/` by appending
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

**Presence measures our sampling, never Geni's content.** A thin region is one
*we* barely covered. Whether Geni holds more there is precisely the unknown an
export resolves — reading it as "Geni has little here" is backwards. The doorway
column is the discriminator: many parentless people means under-sampled, few
means possibly just a small family that ended.

**"Region" is a neighbourhood in the family graph, never a place.** Emma was
explicit about this. Do not classify people geographically: birthplace strings
are mostly absent, and inferring a place from a name is the fuzzy matching this
repo refuses everywhere else.

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

**Layout.** `exports/` the download staging area, one directory per seed as
Geni's zips arrive (see below) · `data_lake/` raw inputs, the subset actually
merged (`*.ged` tracked) · `geni_pages/` saved Geni profile pages ·
`src/genimerge/` the package · `reports/` generated reports worth keeping in git
· `out/` generated data, gitignored · `tests/` pytest.

**`exports/` is Emma's staging area and `data_lake/` is what the merge reads.**
Geni's downloads land as `export-geni (N).zip`, extracted beside themselves,
grouped into a directory named for the person Emma exported from
(`exports/Li Hong/`, `exports/n n/`) or into `exports/archive/` and
`exports/fleshing-out/` for bulk takes. Inside a bulk directory the zip keeps
its download name and the GEDCOM it holds is extracted to
`export-geni/export-<style>-<N>.ged`, where `N` is the zip's download number —
that number is a local label for the batch, not a Geni identifier, and it means
nothing across directories. Ingesting one means **copying** it into `data_lake/`
under the `export-<style>-<seedID>.ged` name — not moving it, so the staging
area stays a record of what was downloaded. Not everything in `exports/` is
ingested; `data_lake/` holding fewer files than `exports/` is the normal state,
not drift.

**Two exports can share a style *and* a seed, and then the name collides.**
Seen on 2026-08-05: two `Forest` exports of `6000000227040338177` taken seven
minutes apart, 3972 people and 4008. Check containment before inventing a
disambiguator — the 3972 was a strict subset of the 4008, so ingesting only the
larger lost nothing and no new naming rule was needed. Both files stay in
`exports/`; only the ingested one is copied to `data_lake/`.

**Never delete a GEDCOM, and never add a zip.** The zips are gitignored **one
line at a time**, deliberately: Emma wants an unignored zip to show up in
`git status` so she can see a download has arrived. Do not replace those lines
with a `*.zip` pattern — it would look tidier and would destroy the signal.

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
