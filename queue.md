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

## ⛔ NO EDITS WHILE THE ADMINISTRATORS' NOTICEBOARD MENTIONS 日巫女; NO CRON JOBS TO 2026-10-01

Ruled 2026-09-24, replacing the two-week hold: *"as long as there is any mention of 日巫女 at
Wikidata:Administrators' noticeboard then there will be no edits ever ... No updating
quickstatements no editing at all."* Read live on every run and fails closed:
`wikidata-edits.yml` gate, `pipeline.yml` gate (every event), `daily-batch-email.yml`, and
the sender's live path (`scripts/wikidata_lockout.py` § NOTICEBOARD). **No cron job runs for a
week**: `wikidata-edits`, `pipeline`, `ci`, `daily-batch-email`, `pages`, `tree`, `review-decks`
stay DISABLED in GitHub until 2026-10-01; after that `gh workflow enable <file>` and the
noticeboard gate governs. **No exception, no one-off run**: ruled the same evening, *"no run at
all only runs of even generations of quickstatements happen only after the string is not present
on that page"* -- the gate in `pipeline.yml` stops every event, dispatch and `force` included.
*"This is indication I was editing too aggressively but it was mostly a quickstatements issue of
the tool not being throttled correctly."*

- **Re-enable the seven workflows on 2026-10-01** (`gh workflow enable <file>`).

## Now

- **The descendant reports are NOT yet a full family tree.** Closed too early on 2026-09-24,
  reopened. Done since: the exact-generation tie-break, the report subject at generation 1, and
  parents placed by ROW ORDER (8,446) -- couples with no parent resolved 74,440 -> 33,059.
  Left: those **33,059** (mostly `<private>` living people and spelling variants whose block sits
  between anchors with several candidates), **1,817 conflicting parent slots**, 1,605 parent
  strings with no split, and the `immediate_family` siblings/spouses, unused.
- **CI slow lane red: 11 failures, all `exports/sweep-parsed/`** (run `36011859223`).
  `test_gedcom_real_exports.py` does not know the `sweep-parsed` header or its `IL`/`FL` label
  prefixes. Fast lane green on 3.10 and 3.13.

- **Restore the open work the queue rewrite archived.** `docs/queue-archive/queue-before-2026-09-24-rewrite.md`
  holds real, unfinished items that left view on 2026-09-24. Re-read it end to end and bring back
  every open work item (not rulings, not history) into this list.
- **The FamilySearch zipper, done properly.** Checked on one family and a 16-pair Wikidata
  cross-check only. Measure it across all 4,863 pairs, work out what the 1,351 ambiguous slots
  need, and handle FamilySearch's own duplicate records (two ids, one person).
- **The name-model fixes, measured across the whole tree.** Latin patronymics
  (`LATIN_VERNACULAR`), `Jonæ` (`-ae`), the lone-letter surname rule (`N.`) and the marker rule
  were each checked on handfuls of examples. Census every one over `display-names.csv` before and
  after, and look at what each newly classifies.
- **The ration and the pacing, seen working end to end.** Edit run `36054472568` (dispatched
  2026-09-24, 500, live) is the first test: confirm names -> 30 people -> ring go out in order,
  20-50 s apart, and what stops it.
- **`Q660913` Kruto the Wend and FamilySearch `MBW7-P7H`** are Emma's own investigation. The job
  here is only to hold the identifiers and what the tree says (the archived queue has both).

