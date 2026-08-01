# geni — Long-horizon backlog

**This file is the project's *abstract destinations*, not its steps.** Items here
describe where the project is going. When work on one begins, it gets decomposed
into concrete, executable steps in `queue.md`, mirrored into the task tool,
executed, and deleted from both. Finished work is recorded in `devlog.md`.

See `CLAUDE.md` § "Queue and longer-horizon work".

---

**Progress note (2026-07-31).** Items 1 and 2 are built and running; item 3 has
its analysis half (`reports/frontier.md`) but not its ingest half; item 6 has
all three of its edit-generating slices — P2600, name links, and the
parent/spouse/date gaps — leaving only the post-acceptance re-run. Items 4, 5
and the rest of 3 and 7 are untouched. What is done in detail lives in
`devlog.md`.

Every batch under items 4, 5 and 6 stops at a file in `out/wikidata/`.
**Nothing in this repo writes to Wikidata**, and nothing should start doing so
without the user saying it may.

## 1. One canonical genealogy, not N exports

Collapse the Geni GEDCOM exports (`Forest`, `Ancestors`, `BloodTree`, and any
future export) into a single canonical dataset keyed on the **Geni profile ID**,
which every export preserves both as the GEDCOM xref (`@I6000000087535357291@`)
and as `RFN geni:6000000087535357291`. The merged form must be re-exportable as
a valid GEDCOM *and* queryable as structured data. Merging must be idempotent
and re-runnable as new exports land, never a one-off hand-edit.

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

### 3a. What the frontier analysis found

The tree is one connected component; 2350 people (26.8%) have no parents
recorded, and those are the branch points. `reports/frontier.md` ranks them by
descendant count. Still open: **taking the next export**, from the top of that
ranking, and deciding how many exports it is worth taking. Only the user can do
the export itself — **BLOCKED-ON-USER-ACTION**, unblock signal is a new `.ged`
in `data_lake/`, after which `genimerge merge` absorbs it without changes.

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

**Mostly already true for GEDCOM.** `Merger.add_source` keys on the xref and
knows nothing about which file it came from, and `genimerge merge` defaults to
globbing `data_lake/*.ged` — so another Geni export is a file drop and a re-run,
not a code change. What is genuinely unbuilt is a
non-GEDCOM input path, and there is no second format in hand to build one
against — so this stays abstract until a source that is not a GEDCOM turns up.
