# geni — Long-horizon backlog

**This file is the project's *abstract destinations*, not its steps.** Items here
describe where the project is going. When work on one begins, it gets decomposed
into concrete, executable steps in `queue.md`, mirrored into the task tool,
executed, and deleted from both. Finished work is recorded in `devlog.md`.

See `CLAUDE.md` § "Queue and longer-horizon work".

---

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
this to decide what to export next from Geni, and what to pull from Jenny.
Ingesting Jenny exports means supporting whatever format Jenny emits alongside
GEDCOM.

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

## 7. Ingest beyond Geni

Support additional sources (Jenny exports, future Geni exports, possibly direct
Geni API) into the same canonical store without the merge logic having to care
which source a record came from.
