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

The tree is **32393 people in one connected component** (`reports/frontier.md`,
2026-08-04, over ten exports). **Treat the numbers in this paragraph as a
timestamp, not a fact.** It has been wrong three times: it read "12422 people in
one connected component" and was left alone when the fifth export made it two;
then 16266/12422/3844; then 27718/16217/11501, for about two hours.
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

`Forest`, `Ancestors` and `BloodTree` are export **styles**, not exports — the
first three files are those three styles of one seed, and a second `Forest` from
a different seed arrives with the filename already taken. `CLAUDE.md` carries
the naming scheme.

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

**What is missing to do this.** `genimerge.inventory` computes pairwise overlap
and per-file uniqueness, but has no per-person presence count and no way to
aggregate it into regions. The measure needs: (a) a count per Geni ID of how
many exports hold it, (b) a notion of region — connected neighbourhood, surname,
place, or branch under a common ancestor — and (c) a report ranking regions by
low mean presence and size. **NEEDS-DECISION** on (b): what counts as a region
is a judgement, and picking wrong makes the ranking meaningless. Emma decides,
and the descendants-of-Indian-people case is the test it has to pass.

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
signal is a new `.ged` in `data_lake/`.

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
globbing `data_lake/*.ged` — so another Geni export should be a file drop and a
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
