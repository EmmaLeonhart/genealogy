# geni — Long-horizon backlog

**This file is the project's *abstract destinations*, not its steps.** Items here
describe where the project is going. When work on one begins, it gets decomposed
into concrete, executable steps in `queue.md`, mirrored into the task tool,
executed, and deleted from both. Finished work is recorded in `devlog.md`.

See `CLAUDE.md` § "Queue and longer-horizon work".

---

**Progress note (2026-08-01).** Items 1 and 2 are built and running. Item 3 now
has **both** halves: the analysis in `reports/frontier.md` and `reports/seeds.md`,
and the ingest, exercised for real by a fourth export on 2026-08-01. Item 6 has
all three of its edit-generating slices — P2600, name links, and the
parent/spouse/date gaps — leaving only the post-acceptance re-run. Items 4, 5
and the non-GEDCOM half of 7 are untouched. What is done in detail lives in
`devlog.md`.

**Two claims below stopped being predictions on 2026-08-01.** The fourth export
tested them and both held; they are marked *Confirmed* where they appear. This
file is a list of intentions, so it is worth being explicit about which of them
have since been measured — item 3b's "the merge absorbs it without changes", and
item 7's "a file drop and a re-run, not a code change".

The tree is **89474 people in one connected component** (`reports/frontier.md`,
2026-08-04, over 45 exports). **Treat the numbers in this paragraph as a
timestamp, not a fact.** It has been wrong four times in five days: it read
"12422 people in one connected component" and was left alone when the fifth
export made it two; then 16266/12422/3844; then 27718/16217/11501; then 32393,
each for a matter of hours.
`reports/frontier.md` is the live count and this file is not regenerated.

The warning that used to follow it turned out to be a description rather than a
caution: an export seeded outside what we hold merges without a single conflict
and still leaves two trees. That is why `genimerge merge` reports connectivity
on every run — and it is also why "one component" is not a permanent state. The
next export to reach somewhere nothing else does will split it again, and that
is normal.

**The Japanese line was joined on 2026-08-04** by two `Forest` exports seeded in
the six-person gap that `reports/path-jimmu.md` had isolated. The path from the
account owner to Emperor Jimmu is now 83 of 83 steps held. The method — save a
Geni page for a target, extract the path, read off exactly who is missing —
generalises to every other line worth reaching, and is item 4 in `queue.md` for
the nine pages already saved.

Every batch under items 4, 5 and 6 stops at a file in `out/wikidata/`.
**Nothing in this repo writes to Wikidata**, and nothing should start doing so
without the user saying it may.

## 1. One canonical genealogy, not N exports

Collapse the Geni GEDCOM exports into a single canonical dataset keyed on the
**Geni profile ID**, which every export preserves both as the GEDCOM xref
(`@I6000000087535357291@`) and as `RFN geni:6000000087535357291`. The merged
form must be re-exportable as a valid GEDCOM *and* queryable as structured data.
Merging must be idempotent and re-runnable as new exports land, never a one-off
hand-edit.

`Forest`, `Ancestors`, `BloodTree` and `Descendants` are export **styles**, not
exports — the first three files are three styles of one seed, and a second
`Forest` from a different seed arrives with the filename already taken.
`CLAUDE.md` carries the naming scheme, which is `export-<style>-<seedID>.ged`:
the style has to be in the name because one seed can be exported in several.

## 2. Wikidata reconciliation

For every person in the canonical dataset, determine whether a Wikidata item
already exists. The primary key is **P2600 (Geni.com profile ID)**; where that
is absent — which it will be for most of the tree — fall back to progressively
weaker evidence (name + birth/death dates, parent/child links to already-matched
items, known-royalty name forms). Reconciliation output is a mapping table with
a confidence level per row, never a silent guess.

## 3. Expansion planning — where to export next

The current exports are bounded slices of Geni. Identify the **frontier** of the
merged tree: individuals with missing parents, sparse subtrees, and
high-connectivity hubs that would pull in the most new material per export. Use
this to decide what to export next from Geni.

### 3z. The three phases, in Emma's framing (recorded 2026-08-04)

This is the ordering the rest of item 3 sits inside. Written down because the
sub-items below were built during phase 1 and read as though it were the whole
job.

**Phase 1 — connect (now).** The point of an export right now is to *join*
things: reach a person, close a gap between components, make a path walkable.
`Forest` and `Ancestors` do this. The Jimmu bridge is the worked example.

**Phase 2 — bulk (in progress).** Emma is taking every export Geni will readily
give her, **up to about 50**. These are not aimed at anything; they are cheap
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

**Emma named the descendants of the Indian people as the clearest example of a
thin region.** That is the first thing to check when the measure exists.

`Descendants` exports belong to phase 3, not phase 1. They are not for
connecting people — they fan out to pull in everyone below one person, which is
a *breadth* instrument. Do not propose one to close a path.

**"Region" means a region of the graph, not a place.** Emma was explicit:
do not classify people geographically. Birthplace strings are dirty, most people
do not have one, and inferring a place from a name is exactly the fuzzy matching
this repo refuses everywhere else. A region here is a **neighbourhood in the
family graph** — people close to each other by parent/child/spouse edges,
regardless of where they lived.

**What is missing to do this.** `genimerge.inventory` computes pairwise overlap
and per-file uniqueness, but has no per-person presence count and no way to
aggregate it over the graph. The measure needs: (a) a count per Geni ID of how
many exports hold it, and (b) a way to find *contiguous stretches of graph*
where that count is low and the stretch is large. Neither exists.

**Not before the bulk downloads are done.** Emma is supportive of building this
and equally clear it is not wanted yet — with ~50 exports still arriving, any
density measured now describes the download queue rather than the tree.

### 3a. What the frontier analysis found

People with **no parents recorded** are the branch points, and
**`reports/frontier.md` is the live count** — how many there are, how they split
across components, and their ranking by descendant count. Re-run
`python -m genimerge frontier` rather than trusting a number written here.

This paragraph used to restate those numbers: "one connected component; 2350
people (26.8%)". By 2026-08-04 every part of that was false — two components,
16266 people, 3396 parentless, 20.9% — and nothing had flagged it, because a
sentence in a to-do file is not checked by anything. The count being wrong was
survivable; **the shape being wrong was not**, since a plan that assumes one
component has no way to describe the export that bridges two.

No test was added for this. The general case — prose in a tracked document
drifting from generated data — cannot be caught without a brittle assertion that
the first good reason to reword would delete. The durable fix is the one taken
here: stop restating generated numbers, and point at the generator.

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
Emma has since switched to exporting whatever Geni will readily give her — 17
takes in one afternoon — so the binding constraint is now ingest and download
time, not seed choice. Ranking still earns its place for the *targeted* exports
(the Jimmu gap was found and closed this way), but do not spend effort improving
it on the assumption it is on the critical path.

Still open: **taking the next export**, from the sequence in `reports/seeds.md`.
Only the user can do the export itself — **BLOCKED-ON-USER-ACTION**, unblock
signal is a new `.ged` under `exports/`.

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

## 4. Wikidata authoring pipeline — queue up the missing people

For people with no Wikidata item, generate a reviewable batch (QuickStatements
v1 to start) that creates them with everything the genealogy actually supports:

- multilingual label (the name, as a label in each applicable language)
- English label + description
- P2600 Geni.com profile ID
- P21 sex or gender
- P22 father / P25 mother / P26 spouse / P40 child — the link structure
- P569 date of birth / P570 date of death, P19 / P20 places, where present

Creation must be **ordered by dependency** so parents exist before children are
linked to them, and must be re-runnable without creating duplicates.

**What the profiles can actually feed this — `reports/profile-names.md`,
2026-08-07.** `genimerge profile-names` measures, per person over the whole
merge, how often each field a statement could carry is present. The pipeline's
shape follows from it: **sex (P21, 99.9%) and a given name (P735, 92.1%) are the
workhorses**, surname (P734) and dates land on ~half, and occupation (10.8%),
burial (7.9%) and title (2.9%) are a small minority — real where present, not
something to scope a batch around. Two consequences that are traps rather than
numbers:

- **Do not split `GIVN` on spaces to make P1545 statements.** 36.9% of people
  have a multi-token given string, but most are romanised CJK/steppe names where
  the extra tokens are honorifics, particles and titles ("Lady", "no",
  "Chanyu"), not given names. The genuine P1545 case (European "Jean Paul" → two
  ordered given-name items) is the Latin-script subset. Splitting needs a step
  that can tell a name from an honorific; the naive split emits wrong P735s. This
  is the concrete failure mode behind `CLAUDE.md`'s "first multi-token batch
  needs reading closely".
- **A NAME is Geni's display *label*, not always a name.** Some values
  ("Unknown Wife", "NN", "daughter of …") are descriptions; on Wikidata they are
  a label or an alias, never a P735/P734 link. Emma's framing 2026-08-07: "the
  names aren't exactly the display names, and they aren't exactly the most
  natural" — the pipeline has to decide per string whether it is a name at all.

**The CJK names are present in native script, which was the open worry.** 16.6%
of the tree carries a CJK form; 56.3% of those are native-script only and 43.7%
also carry a romanisation (often in the `_MARNM` slot). So the hard-to-recover
native label is the *well*-covered one and matches Wikidata's native labels
directly; the gap is the *English* label, which Wikidata often supplies. Emma's
plan for the CJK cases (2026-08-07): translate to English where a romanisation
is missing, the harder part being to distinguish Japanese from Chinese first.

## 5. Name and surname items

Wikidata models names as items: P735 (given name) and P734 (family name) point
at dedicated name items. Many of the given names and surnames in this tree —
Norwegian patronymics especially (`Olavsdotter`, `Torsteinson`, …) — have no
Wikidata item yet. Detect which name strings lack items, and queue the creation
of the missing name items so people can then be linked to them.

## 6. Backfill existing Wikidata items

For people who *do* already have Wikidata items, generate edits that add what
the genealogy knows and Wikidata is missing: the P2600 Geni ID, P735/P734 name
links, and any missing parent/spouse links. These are edits to existing items,
so they need a higher review bar than new-item creation.

Three slices of this are built, each writing a reviewable batch to
`out/wikidata/` that nothing has sent anywhere:

- **P2600 backfill** — `genimerge quickstatements` → `add-p2600.qs`.
- **P735/P734 name links to name items that already exist** —
  `genimerge name-links` → `add-names.qs`. Only the *missing* name items
  depend on item 5; linking to extant ones never did.
- **Missing parent/spouse links, and dates** — `genimerge crosscheck` →
  `add-claims.qs`, 65 statements today (P22 x1, P25 x4, P26 x18, P569 x18,
  P570 x24). Only gaps are proposed, never conflicts, and a relationship needs
  both people linked by P2600 rather than by inference.

What is left under item 6 is **re-running reconciliation after a batch is
accepted**, since each new P2600 makes the exact join reach further. That is
**BLOCKED-ON-USER-ACTION**: no batch has been accepted, and running one at
QuickStatements is the user's call, not this repo's.

## 7. Ingest more sources

Absorb further exports — more Geni GEDCOMs, and possibly the Geni API direct —
into the same canonical store without the merge logic having to care which
source a record came from.

**Confirmed for GEDCOM on 2026-08-01.** `Merger.add_source` keys on the xref and
knows nothing about which file it came from, and `genimerge merge` defaults to
reading every `.ged` under `exports/` — so another Geni export is a file drop and a
re-run, not a code change. That was the claim; the fourth export tested it and
it held. Absorbing 3840 more people took **no change to the merge logic at all**.

The one thing it did require was a **rename**, because Geni names the file
`export-<style>.ged` and a second `Forest` export collided with the first. That
is not the merge caring where a record came from — it is two files wanting one
name — but it is the kind of detail a claim like "just a file drop" hides, so it
is worth recording that the claim survived with an asterisk rather than
untouched.

What is genuinely unbuilt is a non-GEDCOM input path, and there is no second
format in hand to build one against — so this stays abstract until a source that
is not a GEDCOM turns up.

## 8. A parallel Wikidata tree, built by SPARQL, and provenance throughout

**Recorded 2026-08-05, in Emma's framing. Long-term — she is still doing a
comprehensive Geni export, and that comes first.**

The end goal is not only to reconcile our Geni tree against Wikidata one person
at a time, but to **build a parallel tree out of Wikidata itself** via SPARQL
and then piece the two together. Items 2 and 6 match individuals; this is the
larger move of treating Wikidata as a second genealogy with its own shape.

**Wikidata behaves differently, and the difference is the point.** It has
different notability standards, so its tree is not a subset or a superset of
Geni's — it is dense exactly where Geni is dense (heavily studied dynasties) and
absent for the ordinary people who make up most of a Geni export. Expect the two
trees to agree on structure and disagree on who exists at all.

**Emma's judgement on where exports pay, recorded because it changes the
ranking.** Hyper-dense regions are **low** return on an export: we can get that
material from Wikidata instead, and where Geni disagrees with Wikidata there it
will be over minor details rather than whole people. She also expects those
regions to be *hard* to export from at all — see the note on Geni entry points
below. So the small-world but non-dense regions are the ones worth exporting,
which cuts against ranking purely by doorway count.

**Why dense regions resist export, which no report here could have worked out.**
Emma gains access to a cluster through *nearby contributions* — that is how
every export so far was seeded. Once an area is too densely covered by other
contributors she cannot add an individual to it, and so cannot create the
foothold an export needs. A larger export size limit would penetrate these
areas; the current one does not. This is a constraint of Geni's editing model,
not of our data, and it explains the Carolingian hole in `reports/paths.md`
better than anything measured here.

**Provenance is a requirement, not a nicety.** Every fact will end up with more
than one possible origin — a Geni export, a Wikidata statement, or order.life —
and they will disagree. Each needs to carry where it came from. Nothing in the
merge records this today: `Merger` keeps the winning value and the conflict
list, not the source file per field.

**`order.life` is the last thing to touch, and not before everything else is
settled.** It is a separate repo on this machine holding similar material that
behaves differently again. **Another agent is editing it right now and it is in
flux**, so reading it for anything load-bearing would be reading a moving
target. BLOCKED-ON-EXTERNAL until Emma says it has settled.

**Emma's 2026-08-07 framing of order.life and the phase ordering.** order.life
is **a third source**, alongside Geni and Wikidata, feeding the Phase-4 queue of
things to add to Geni. It is **on Emma's PC** — local, not in this session's
reach — and she is **deferring it deliberately** ("we'll do it later"), until
the Wikidata side is built offline. Because it is not Geni-native it needs a
**different citation** from the Geni-ID-as-source used for the Geni-derived
claims. This does not change its BLOCKED status; it names why the block is
Emma's choice, not just the other agent's edits.

The ordering she stated, end to end: (1) descendant-distribution search to pick
where to export next — tomorrow's work, item 3/3z; (2) a very large export
campaign off those picks; (3) the Geni-side enrichment pipeline (items 4/6);
(4) build the Wikidata tree offline and superimpose it (this item); (5)
integrate, which is "for the most part a very large amount of merges". The whole
of 4–5 is done **offline** on purpose — it is how the entity resolution and the
merge decisions get made without hammering Geni with live operations, and only
the *final* confirmed merges go online where parents can be compared.

**A postponed Geni-side merge queue — recorded, not started.** Emma, 2026-08-07:
**most of the cases where two Geni IDs sit on one Wikidata item are Geni
duplicates that should be merged, but cannot be merged on Geni yet** ("because
Geni's Geni"). `reports/wikidata-doubles.md` already surfaces these pairs side by
side; the eventual Phase-4 output is a *queue of Geni merges* to perform online,
one that only exists once the offline Wikidata tree and its entity resolution
are in place. She is explicitly **postponing this until the Wikidata side is
offline as well** — it is the last thing, not a current task.

### 8a. How the Wikidata download must be built — Emma's design constraints, 2026-08-07

**This is the part that has been got wrong before by ignoring how Wikidata
behaves. Read it before writing a line of the downloader.** The shape of the job:
take the **~500,000 Wikidata profiles that carry a Geni ID** (the P2600 side of
`reports/wikidata-overlap.md`, 516,885 IDs), download each item *completely*, and
then **grow the set by walking family relationships** — parent, child, spouse
(P22/P25/P26/P40) — to items that have no Geni ID, iterating outward. That is the
whole tree of Wikidata reachable from the Geni-linked seed.

**Treat it as a multi-day background operation, not a rush.** Emma's words: it
"should be treated as a couple-day-long operation that is run in the background",
**not** a "do it as fast as possible and don't even bother with rate-limit stuff"
job. Running in the background is what *makes it easy* — wall-clock length is not
a problem, so there is no reason to run hot. The number of items per hour is
unknown and is to be **found by serious experimentation up front**, not assumed.

**Wikidata is hostile and rate-limits readily — design for that from the first
line.** Expect HTTP 429s (Emma: "we're going to get fortune nines"). The rule is
to **back off the moment one arrives**, not to run flat out and then treat 429s
as a surprise to complain about. Non-negotiables:

- A real, descriptive **User-Agent** identifying the tool and a contact — the
  bare default is itself a reason Wikidata throttles.
- **Exponential backoff on 429/503**, and respect `Retry-After` when present.
- **Politeness by default:** a conservative request rate, tuned down further the
  instant throttling appears. Start slow, measure, only then consider faster.

**Two APIs with opposite cost profiles — this is the distinction that was being
ignored.** A **SPARQL** query gets *massive amounts of structural information for
cheap* in one round trip (all items with P2600; the P22/P25/P26/P40 QIDs of a
batch of items — i.e. the graph and the set-expansion). But asking SPARQL for
*large amounts of per-individual detail* is **expensive** and is where it fights
back. The **JSON entity-download API** (`Special:EntityData/Q….json`, or
`wbgetentities`) is a **different, somewhat less hostile** path and is how to pull
the *complete* item. So the division of labour is: **SPARQL for structure and for
deciding who to fetch next; the JSON download for the full content of each item.**
Both paced.

**Store everything locally, incrementally, resumably — no re-querying.** When an
item is looked at, store the **whole item** on disk (the complete JSON), then
**commit and push** as the run proceeds. The operation is idempotent and
resumable: a killed run picks up from what is already stored rather than
re-fetching, and progress survives because it is committed. No individual item is
queried twice. — **Corrected in § 8a-revised below: the commit cadence is
batched, and resumability comes from a state store rather than from git.**

**Why this differs from the Geni side, stated so the two are not modelled alike.**
Geni is **bulk-export-only**, seeded from specific spots — a whole ball arrives at
once and the cost is getting the export at all. ~~Wikidata has **no bulk export**
but is cheap to probe for small things one at a time.~~ **This half is wrong and
was the expensive error** — see § 8a-revised: Wikidata publishes a **weekly
full JSON dump of every item**, and Wikimedia points bulk consumers at it
precisely so they stop doing what the plan above described. What is true is the
*asymmetry*: Wikidata is also cheap to probe one item at a time, which Geni is
not. Different acquisition shapes, different time-to-get; a downloader written as
though Geni were probeable per-person still gets that side wrong.

**Stdlib only still holds** — `urllib` covers both the SPARQL endpoint and the
JSON entity API; no dependency is needed for this.

### 8a-revised. Dump-first, batched writes — 2026-08-07, same day, before any code

**Source: `chats/wikidata-querying-2026-08-07.md`.** Emma took § 8a above to a
second model and it found three things wrong with it. This section supersedes
§ 8a where they disagree; § 8a is kept because most of it stands and because the
corrections only read as corrections next to what they replace.

**Storage and commit cadence — the per-item commit is out.**

- Write each item's full JSON to disk **the moment it is fetched**, and never
  fetch it again once present. That is the property § 8a actually wanted.
- **Commit and push in batches** — every 500–1000 items, or every few minutes,
  whichever comes first. Emma's own number: "every hundred or every thousand
  individuals would be fine; per individual would be a big problem". Half a
  million commits is not a slow version of this plan, it is a repo that stops
  working somewhere in the low hundreds of thousands.
- **Resumability comes from an explicit state store, not from git and not from
  the filesystem.** A SQLite table or flat manifest of QID → done/pending/errored
  (plus retry count and last error) is an instant lookup; `ls`-ing 500k files or
  reading `git log` on every resume is not. § 8a's "picks up from what is already
  stored" is right about the *guarantee* and wrong about the *mechanism*.
- **Still hard-committed to the repo** — that part is Emma's decision and does
  not change. The cadence is the only thing being changed.

**Two-phase sourcing, because the seed set and the frontier are different jobs.**

*Seed phase (~500k items carrying P2600).* Use the **Wikidata JSON dump** as the
primary source, not 500k live fetches. Get the QID list from SPARQL (paginated),
then stream-filter the dump against it locally: no rate-limit exposure for the
bulk of the volume. The live entity API becomes the **fallback** for items
missing from the dump snapshot — created or edited since it was cut.

*Expansion phase (walking P22/P25/P26/P40 out to items with no Geni ID).* This is
frontier-driven and cannot be known in advance, so it stays on the live API with
the § 8a backoff discipline in full: descriptive User-Agent with contact,
exponential backoff, honour `Retry-After`, find the sustainable rate by
experiment, back off the instant throttling appears.

**SPARQL is not free.** `query.wikidata.org` has **its own limits, separate from
the action API** — a 60-second query timeout and its own throttling. "SPARQL is
cheap" in § 8a is true per query and false per campaign; the P2600 list needs
pagination and pacing like anything else.

**Expansion scope — Emma's prediction, recorded so it can be scored.** Expect
**heavy interconnection inside the seed set itself**: most P22/P25/P26/P40 edges
from a Geni-linked item will land on another Geni-linked item already in the set,
not on a new one. The frontier — items reached that lack a Geni ID — is therefore
expected to be **small and patchy relative to the 500k**, "specific holes and
specific lines that are only on Wikidata". Practical consequence: do not
over-provision for expansion, and **treat a much-larger-than-expected frontier as
a symptom** — most likely an edge type fanning out further than intended — rather
than as the expected case.

**Two things neither chat costed, to settle before choosing dump-vs-live.** Both
are measurements, not arguments, and each could flip the decision:

1. **`wbgetentities` takes up to 50 QIDs in one request.** That is the batching
   the first answer named in the abstract and neither answer applied to this job.
   500k items is then ~10,000 requests rather than 500,000 — at a deliberately
   slow one request per second, a few hours. Against that, the full JSON dump is
   a very large download (order of 100 GB compressed; **check the current figure,
   do not take this number on trust**) before a byte is filtered. The dump wins
   on politeness and loses on local cost, and which matters more here is not
   obvious. **Measure both**: time a 50-QID `wbgetentities` batch, and read the
   actual dump size off the Wikimedia downloads page.
2. **What 500k full items weigh on disk, and what that does to a repo that must
   hold them.** Unknown until sampled — take 1000 real items and multiply.
   Whatever the answer, it lands in a git repo that GitHub starts warning about
   in the low single-digit GB, so **sharded and compressed** (gzipped JSONL,
   fixed items per shard) is the shape to assume, and the pilot exists to say
   whether even that is viable. If it is not, the plan needs Emma's decision
   about what "hard committed as part of the repo" means at this scale — not a
   quiet switch to storing it somewhere else.

**Do a 1000-item pilot before building the real thing.** It answers the sustained
rate, the batch behaviour, the per-item byte size and the shard layout at once,
and every one of those is currently a guess. Nothing about the 500k run should be
designed on numbers nobody has measured — that is the failure § 8a was written
to prevent, repeated one level up.

### 8a-decided. Emma's calls, 2026-08-07 evening — this is the built design

Made after reading § 8a-revised, and they close most of what it left open.
`genimerge wikidata-download` implements them; `src/genimerge/wikidownload.py`
is the long form.

**Live API for the whole seed set. The dump is not needed.** Her reasoning:
*"because of how easy it is to get the 500,000, we can get the 500,000 with all
their data"* — 50 QIDs per `wbgetentities` request makes it ~10,300 requests, not
500,000, and the dump's cost was always the ~100 GB download the seed phase would
have to pay before filtering. The dump stays on the shelf as the fallback if the
live path turns out to throttle harder than it looks.

**Storage: many ordinary files, committed and pushed as the run proceeds.**
Emma, explicitly: *"I do not want the Wikidata to be all in one file that would
need LFS. I want the Wikidata to be kept in a common way so they can be committed
and pushed and actively done, building up the tree."* Gzipped JSONL shards of
1000 items under `wikidata/items/`, each a few megabytes — small enough that a
push is incremental and no single file approaches a limit. **No LFS.** The
resume index sits in `out/` and is derived, not committed.

**Two queues, and the walk between them is the point.** Her design, in her
terms:

1. **The take-from-Wikidata queue** — QIDs known to exist and not yet held. It
   starts as the whole P2600 seed set.
2. **The iteration queue** — held items waiting to be read for the relatives
   they name. Anything named and not already known joins queue 1; anything
   fetched joins **the end of** queue 2. *"Sort of a BFS thing."*

Implementation note that is not a detail: **the iteration queue is the shard
sequence plus a cursor**, not a second list. Items are appended in fetch order,
so "the end of the iteration queue" is "the end of the last shard" for free.

**Reaching people with no Geni ID is the objective, not a side effect.** *"We'd
be finding the individuals and adding them in… eventually we have a big, honking
family tree, including many of the individuals that do not have GEDCOM IDs.
These individuals without GEDCOM IDs are going to be the ones that we'd be doing
this for."* The two trees are then parallel and unequal by construction — the
Wikidata one accreted a person at a time, the Geni one arriving in bulk exports —
and each holds people the other does not.

**No ad-hoc queries. None.** *"Do not, whatever the fuck you do, check it, except
with our Wikidata export, because checking it is the way that you get a 429."*
The downloader is the only thing that talks to Wikidata. Every question about
Wikidata's contents waits for the local store. This is in `CLAUDE.md` as a
standing rule because it binds future sessions, not just this one.

**`out/merged.ged` is ignored by necessity** — 409 MB, generated, over GitHub's
file limit, and already covered by the existing `out/` line. No `.ged` pattern
was added and none should be; the corpus rule under `exports/` is untouched.

### 8b. Checks that wait for the store — offline, after the 500,000

**Nothing here may be answered by querying Wikidata.** Each is a computation over
`wikidata/items/` once the download has finished, and each is written down now
precisely so it does not get "just quickly checked" against the live endpoint.

**The century distribution, Wikidata against Geni.** Emma's guess, 2026-08-07:
the Geni-linked items on Wikidata skew heavily to the 20th and 21st centuries
much as the Geni profiles do, with the 19th ambiguous — *"I'm not really sure,
but that dynamic is something I could imagine would be happening"*. Recorded as a
prediction before the data exists so it can be scored rather than confirmed after
the fact. `reports/profile-names.md` already has the Geni side's date coverage;
the Wikidata side is P569/P570 over the stored items.

**Ancient and medieval people with many descendants — the export-picking use.**
The Geni-side version is the descendant-distribution search (item 3/3z): rank by
realized documented descendants to choose where the next `Descendants` exports
run, since the campaign is about **reaching modern times**, not thinness. The
Wikidata store makes the same measurement possible on the other tree, and then a
third thing that neither side can do alone: **where Wikidata holds ancestors of a
Geni person that our Geni tree lacks**, which is both a Geni-side target to
export toward and the input to entity resolution between the two trees.
