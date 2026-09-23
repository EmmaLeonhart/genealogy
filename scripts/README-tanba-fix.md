# Tanba day-batch gate (wired 2026-09-23)

Emma: QuickStatements must not edit Tanba people. **Drop matching lines entirely** —
never leave them as `#`-prefixed CREATE/LAST/Q comments or annotate walls.

## Live on main
- `scripts/tanba_batch_block.py` — roster-backed Tanba QID denylist (`reports/tanba-qids.json`, `reports/tanba-p2600-pairs.tsv`)
- `scripts/build-garborg-day.py` final gate:
  - `from tanba_batch_block import tanba_blocked_qids`
  - `excluded |= tanba_blocked_qids()`
  - `names_excluded` drops **any** line with `tanba` (case-insensitive) or a blocked QID, **including comments**
- `usable()` also rejects relative names with NN as a token anywhere (`Margreta NN`)
- `scripts/install_tanba_day_gate.py` — idempotent installer (prefers the import if already present)
- `scripts/strip_tanba_from_day_batch.py` — one-shot cleaner for an already-written day file

Strip alone is not the end state: the composer gate must stay wired so the next compose cannot bring Tanba back as comments.
