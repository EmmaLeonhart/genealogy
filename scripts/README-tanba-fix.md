# Tanba day-batch gate (2026-09-23)

Emma: QuickStatements must not edit Tanba people. **Drop matching lines entirely** —
never leave them as `#`-prefixed CREATE/LAST/Q comments or annotate walls.

## On main now
- `scripts/tanba_batch_block.py` — roster-backed Tanba QID denylist
- `scripts/install_tanba_day_gate.py` — idempotent installer (correct behavior)
- `scripts/strip_tanba_from_day_batch.py` — one-shot cleaner
- `scripts/tanba-day-gate.patch` / `scripts/tanba_gate_replacements.json` — apply helpers
- `reports/wikidata-garborg-day.txt` — measured **zero** `tanba` (case-insensitive)
- `tests/test_tanba_day_gate_wired.py` — CI fails closed until the composer gate is present

## Required in `scripts/build-garborg-day.py` (CI test enforces)
- `from tanba_batch_block import tanba_blocked_qids` (prefer over inline)
- `excluded |= tanba_blocked_qids()`
- `names_excluded` drops **any** line with `tanba` / Tanba QIDs **including comments**
- `usable()` rejects relative names with NN as a token (`Margreta NN`)

If the composer gate is not yet present on tip, run locally on a clone with push auth:

```bash
python scripts/install_tanba_day_gate.py
python scripts/apply_tanba_gate_replacements.py  # if present; prefers import over inline
git add scripts/build-garborg-day.py scripts/README-tanba-fix.md
git commit -m "Wire Tanba day-batch gate: drop Tanba lines entirely; never comment them out"
git push origin main
```

Strip alone is not the end state: the composer gate must stay wired.
