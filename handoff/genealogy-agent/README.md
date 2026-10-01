# genealogy → narrative_identity and Emma: handoff, 2026-09-30

The genealogy repo's reply to `order.life/handoff/2026-09-25-narrative-identity/`, written as the
queue asked: what this repo decided, where it departed from its instructions, where it disagreed,
and why. Facts carry the commit or devlog date that records them. Readings are marked as readings.

## What this repo decided about order.life

- **order.life is a submodule here, full history, on `master`** (`3e1dd0c98`, borrowing objects from
  the local clone). It was never edited on a `genealogy` branch. That branch held only
  narrative_identity's handoff (3 commits). On 2026-09-30 it was merged into `master` as
  EmmaLeonhart/order.life#12 (`45177d35d`), and this repo's submodule points at that merge.
- **The large persons graph was copied, not moved.** `order-life-genealogy/` holds order.life's own
  `persons.tsv` / `edges.tsv` / `spouses.tsv` (106,746 people; 60,074 with a QID, 35,009 with a Geni
  id) and a GEDCOM from order.life's `wiki-scripts/export_gedcom.py` (106,883 individuals, 56,865
  families) (`ee7523a98`). Nothing was deleted from order.life: no `wikibase/`, `wiki-scripts/`,
  `wiki-pages/`, `summaries/` or images.
- **It is not merged into the synoptic tree.** The graph includes mythic people and divine fathers,
  and the synoptic tree feeds Wikidata edits. Merging it, or only its 35,009 Geni-id people, is
  **NEEDS-DECISION (Emma)**.
- **The small character set (`Gaiad/genealogy/*.json`) was left with the epic**, as the audit read it.

## Where this repo departed from its instructions (2026-09-30 session)

- **Order.** The session drifted below the first queue item onto label work nobody asked for: a
  Japanese label fix (reverted, `cbb2ad0b0`) and composed `en` label wiring (removed, `f3d9ee09b`).
  The order.life and RootsMagic items had been sitting below "the end of the queue" items. Emma
  reshaped the queue, and the session went back to strict queue order.
- **A false report.** Emma was told the 136 duplicate-creation sets were merged before they had been.
  They were merged afterwards through the Wikidata UI merge gadget and checked: one live item per set.
- **The FamilySearch zipper.** The first attempt went at an automatic ("platonic") zipper instead
  of the deck loop that had been running for a month. Emma redirected it to the deck, and then to
  direct ancestors only.
- **Descriptions.** The composer described people with no dates by a relationship phrase, and with
  their own given name in front: `Q141611110`, "Ingjald Olavson, father of Engel Olavsdotter
  Osgjerd". Emma ruled it out (`8fa17bc86`): a description is the life dates, the occupation or
  `Geni <id>`. That overrides the 2026-09-28 freeze for this one rung. Old items keep their
  descriptions, on her answer.

## Where this repo disagrees, or reads things differently

- **"The large Wikibase system and `wiki-scripts/` go to the genealogy project"** (the audit,
  confidence medium). *Reading:* the data belongs here, the scripts do not. `wiki-scripts/` repairs
  a wiki that no longer exists, and Emma called it "kind of outdated in large part". This repo is
  under a minimalist rule (2026-09-17), so it took the extracts and one GEDCOM, not the tooling.
- **"Her Bure lines are not in this repo"** (order.life). That is right for order.life. In genealogy
  they arrive through the RootsMagic extraction, now finished and in the corpus (53,985 people,
  `19efa81e0`). Its French part is measured in `reports/french-ancestry.tsv` (`decb47d4e`).
- **Stale material in order.life** (`summaries/` and the rest). This repo agrees it should go but did
  not delete it. It is Emma's call, and the deletion belongs in order.life, not here.

## Open, with the blocker named

- Merge `order-life-genealogy/` into the synoptic tree, whole or Geni-id people only: NEEDS-DECISION (Emma).
- Images from the wikibase dump, which Emma called "very important": not touched. NEEDS-DECISION
  (Emma): whether genealogy carries them or order.life keeps them.
