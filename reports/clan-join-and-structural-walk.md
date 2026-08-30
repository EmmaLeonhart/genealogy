# The clan join, and the structural walk's verdict counts

Rescued from `queue.md` on 2026-08-30, where they were the orphaned tail of items already
finished and deleted. Neither number was recorded anywhere else, and the queue is for steps not
yet taken — `CLAUDE.md`: findings belong in `reports/`.

## The clan join agrees completely with the About Me extraction

Tanba **179/183 (97%)** and the sister repo's Izumo roster **120/202** joined — and **0 pairs
that the corpus-wide About Me extraction had not already found.**

That is not a null result. Two independent paths reach the same set, which is the strongest
thing a join of this kind can say about itself. Emma: *"it probably means we did good data
modelling early on."*

**The new fact is `Onakatomi` 0 of 97.** That clan has no About Me links written yet, so it
cannot join at all — nothing is wrong with the join. Writing them is hers.

## The structural walk

`scripts/walk-structural-merge.py`, verdicts over the pairs it considered:

| verdict | pairs |
| --- | ---: |
| AGREE | 89,486 |
| MERGE | 35,737 |
| GENI ONLY | 131,366 |
| WD ONLY | 12,512 |
| AMBIGUOUS | 237 |

`reports/structural-correspondence.csv` **7,841 rows** and
`reports/wikidata-structural-placeholders.json` **35,162 entries**. Against the stale version
those figures replaced: 34,943 entries identical, 218 gone, 219 new — it reads as a 12,321-line
diff only because the JSON is pretty-printed at ~28 lines an entry.
