# Queue

Work only. Take the first item under **Now** and do it. When it is done, delete it and append a
dated `devlog.md` entry in the same commit. Bullets, never numbers. Nothing here is marked
priority: the order IS the priority, and a new item goes where it belongs in the order, not on
top with a banner. Rulings go in `CLAUDE.md`; history goes in `devlog.md`; everything else that is
not an action goes in `docs/queue-archive/`. The file this replaced, verbatim, is
`docs/queue-archive/queue-before-2026-09-24-rewrite.md`.

**Standing, not items:** no contact with geni.com until at least 2026-10-21, and only Emma lifts
it. Each session re-creates the hourly `exports/2026-09-19` merge cron and starts with
`CLAUDE.md` § *FIRST OF ALL, THE FAMILYSEARCH ZIPPER*.

## Now

- **`Q660913` Kruto the Wend and FamilySearch `MBW7-P7H`** are Emma's own investigation. The job
  here is only to hold the identifiers and what the tree says (the archived queue has both).
- **Backfill descriptions on established items, dates and relatives only.** ~4,380 of our items
  made before 2026-09-19 have none. Use life dates, else the relationship phrase; never the
  Geni-id fallback -- it is strictly the anti-duplication rung, and an item with neither is left
  without one. ⛔ **Never overwrite an existing description**, in any language: only add where
  there is none.

## Blocked on the Geni moratorium

- **The research, manager half.** The ancestors report off Geni supplies `managed_by` for the
  owner's ~8,254 ancestors; then join managers in `match-descendants-to-ancestry.py`.
- **The path requester.** 140,692 never attempted at the last count; `scripts/pathrun.js`,
  `CLAUDE.md` § *THE PATH CAMPAIGN*.
- **The chain walk.** 12,911 of 47,692 permalinks walked. Resume with
  `build-chain-batch.py --skip-covered`, finish with `C.reseedFailed()`, then run
  `split-path-chains.py` and `build-tiny-gedcoms.py`.
- **The sibling scrape.** A loop over `reports/sibling-pair-worklist.tsv` at the extension's
  pace, never alongside the path campaign.
- **The descendants sweep.** Cursor 8,993 in `reports/sweep-queue-6000000227822546944.txt`; the
  209 people in `reports/sweep-partial-incapsula-2026-09-21.txt` are the WAF's output and are
  redone.
- **`Slavina` / `Slawina von Rügen`**, Kruto's mother and spouse, one letter apart: checked
  against Geni, not reasoned about.
- **The Rømer ring seed** is one unrecorded parent link from the owner's ancestry.
