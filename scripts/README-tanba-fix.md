# Tanba day-batch fix (2026-09-22)

Emma: QuickStatements must not edit Tanba people.

## Already on this branch
- `scripts/tanba_batch_block.py` — roster-backed Tanba QID denylist

## Still needed (local on Emma laptop / next agent with git push auth)
1. Strip Tanba comments from `reports/wikidata-garborg-day.txt` (526 lines; statements already absent).
2. Patch `scripts/build-garborg-day.py`:
   - `from tanba_batch_block import tanba_blocked_qids`
   - final gate: `excluded |= tanba_blocked_qids()` and drop comment lines naming Tanba/QIDs
   - `usable()`: reject relative names with NN as a token anywhere (`Margreta NN`)

Local SHAs on box (unpushed): `62bdf1b03` Tanba strip+gate; `b8b66aaed` Given-NN.
