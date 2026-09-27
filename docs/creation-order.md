# Who is created, and in what order (as the code stands, 2026-09-26)

Read from `scripts/build-garborg-day.py` (who) and `scripts/split-daily-batch.py` (order and share).

## Who is picked

Each composition (`pipeline.yml` recomposes several times a day) picks a fresh set:

1. **The spine, always, outside every cap.** The ancestral couples on the saved paths, from Arne to
   Bergitte to Charlemagne and down to the owner.
2. **The regular pick**, `compose()`, drawn at random (seeded) from people one family link away from
   the universe:
   - up to 200 **children**: a random person with an uncreated child gets one child. A childless
     marriage gives the spouse instead;
   - up to 200 **parents**: a random person missing a parent gets one;
   - **free parents**, uncounted: a child who seems to have a single mother or father gets the other.
3. **The priority ancestor ring, uncapped** (`priority_ancestor_ring`). From the hand-picked seeds
   in `PRIORITY_ANCESTOR_SEEDS` (Inger Axelsdatter Guntersberg, Olver Rømer and others), the walk
   goes up through everyone who already has an item and returns the whole next generation above
   them. It advances by itself, since the people it returns are walked through on the next run.
4. **Names**, from the name-item generator: the given, patronymic and family-name items the people
   need.

`DAILY_CREATION_CAP` (500) is reported against the pick, not enforced.

Then the gates drop people, and each is recorded in `reports/garborg-carry-forward.tsv`, not
lost:
- no `ja`/`zh`/`ko` label, which is the creation gate;
- no link to anybody already on Wikidata;
- outside the universe or its one-step ring;
- a description that repeats.

## In what order, and what goes out

`split-daily-batch.py` writes two files from the composed batch, both in this order (since
2026-09-26):

1. **Statements on existing items**: relationships, labels and the rest, because a batch can
   spend all day creating.
2. **The random individuals**: the first people of the regular pick, not ring and not names. 30 in
   the automatic share, 20 on the page.
3. **The ring**: every priority-ring person, in the automatic share as well as the page.
4. **The names**, each with the links to the people who carry it.
5. **Everyone else**, on the page only.

- **The automatic share** (`-auto.txt`) is sent by `wikidata-edits.yml`, up to 500 edits a run.
- **The page** (`-manual.txt`, the Pages site and the daily issue) carries the whole batch, for
  QuickStatements to run in full.

Unique English label and description pairs let both paths run at once without duplicates.

## Against Emma's understanding

- **"The ring pool is created unconditionally."** Right. The priority ring is uncapped, outside
  the regular pick, and always in the automatic share.
- **"From the non-ring pool, ~20 are created at the start of the QuickStatements (or should
  be)."** It *should be*, and it is as of `efa65d434e` (2026-09-26): 20 on the page, 30 in the
  automatic share. Before that, names led both files and no twenty were set apart.
- **"A further set is created at the end."** Yes. The rest of the regular pick comes last on the
  page, after the names. Only the page carries it, so it is created only when the pasted batch
  runs that far.
- **Not in the understanding:** statements on existing items now come first; the spine is created
  outside every cap; and the 500-a-day figure is a reported ceiling, not a limit anything enforces.
