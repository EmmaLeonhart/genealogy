# Tanba day-batch gate (wired 2026-09-23)

Emma: QuickStatements must not edit Tanba people. **Drop matching lines entirely** —
never leave them as `#`-prefixed CREATE/LAST/Q comments or annotate walls.

## Live on main
- `scripts/tanba_batch_block.py` — roster-backed denylist
- `scripts/build-garborg-day.py` drops ANY line with `tanba` / Tanba QIDs **including comments**
- `usable()` rejects relative names with NN as a token (`Margreta NN`)
- `scripts/tanba-day-gate.patch` — the applied unified diff
- `scripts/install_tanba_day_gate.py` — prefers import of `tanba_blocked_qids`
