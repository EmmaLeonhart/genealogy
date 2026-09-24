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

- **The descendant reports are NOT yet a full family tree.** Closed too early on 2026-09-24. What
  the parse has: 208,385 people, 1,404,409 parent slots on a Geni id. What it lacks: **41,505
  couples with no parent resolved** (mostly `<private>` living people and spelling variants,
  which no name match can reach), **1,744 conflicting parent slots** dropped, 1,605 parent
  strings with no split, and the `immediate_family` siblings/spouses are not used at all. The
  structural route found in the 2026-09-24 morning session is untried in code: a report is
  breadth-first by generation, with sibling blocks in the same order as their parents in the
  generation before, so a parent follows from ROW ORDER -- id to id, no name.
- **CI slow lane red: 11 failures, all `exports/sweep-parsed/`** (run `36011859223`).
  `test_gedcom_real_exports.py` does not know the `sweep-parsed` header or its `IL`/`FL` label
  prefixes. Fast lane green on 3.10 and 3.13.

- **`Q660913` Kruto the Wend and FamilySearch `MBW7-P7H`** are Emma's own investigation. The job
  here is only to hold the identifiers and what the tree says (the archived queue has both).

