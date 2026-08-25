# The spine: Charlemagne → Bergitte Aukland → Marta Jonsdatter Li → Arne, and → Emma

**This is the line the whole Garborg programme is building along.** Recorded 2026-08-25 on Emma's
instruction: *"record somewhere clearly that we have that path from Marta Jonsdatter Li up to that
common ancestor and then to charlemagne and to me."*

Everything below is **read off Geni's own relationship panel**, which Emma showed on
2026-08-25. It is not re-derived from our files, and it should not be: Geni traced it, she
captured it, and re-computing it has already produced a wrong answer once.

## Bergitte Aukland → Arne Garborg

Geni: **"Arne Garborg is Bergitte Gunnbjørnsdatter Aukland's 9th great grandson."**

| # | person | relation to previous |
| ---: | --- | --- |
| 1 | **Bergitte Gunnbjørnsdatter Aukland** `6000000002481819312` | — |
| 2 | Gunnbjørn Jonson Mjølhus | her son |
| 3 | Lars Gunnbjørnsen Mjølhus | his son |
| 4 | Peder Larsen Mjølhus | his son |
| 5 | Lars Person Nedre Rossavik | his son |
| 6 | Berit Larsdatter Nedre Rossavik | his daughter |
| 7 | Lars Tormodsen Mele | her son |
| 8 | Jon Larson Mæle | his son |
| 9 | **Marta Jonsdatter Li** `6000000003491988826` — **`Q141178381`** | his daughter |
| 10 | **Jon Samuelsen Raustad** `6000000003732742137` — **`Q141168955`** | her son |
| 11 | Ane Oline Jonsdatter Raugstad `6000000003491986946` | his daughter |
| 12 | **Arne Garborg** `6000000003492005116` — **`Q467497`** | her son |

**Three of the twelve are on Wikidata**: Marta (made 2026-08-25), Jon Samuelsen Raustad, and Arne.
The nine between them are not.

## Bergitte Aukland → Emma

Bergitte is on **both** lines between Emma and Arne, which is what makes her the target rather
than the nearest common ancestor. Geni's second reading on the same page: *"Arne Garborg is
Bergitte Gunnbjørnsdatter Aukland's third great granddaughter's husband's third great grandson."*

The nearest common ancestor of Emma and Arne is a different person and is **not** Bergitte —
`queue.md`: *"the first common ancestor of us is Rasmus Ingebretsen Grude
`6000000003492045766`, and Bergitte is the bigger target one."* Both matter; they do different
jobs.

## Bergitte Aukland → Charlemagne

The half that makes Bergitte worth reaching. `queue.md`: she is *"the common ancestor in the two
lines between me and Arne who is a descendant of Charlemagne."*

**Bergitte does not appear in `reports/charlemagne-route.csv`.** That file traces a 399-step
descent from Charlemagne to Emma up a different branch. So the Bergitte→Charlemagne descent is
**not yet in the repo** and is the outstanding half — Emma's saved page for it goes through
`python -m genimerge path-from-html` into `paths/` the moment it lands.

## Why the daily runs matter

The daily Garborg batches create people **adjacent to this spine**, so every run shortens the
distance between what Wikidata holds and this line. That is the point of them, and it is the
reason the queue's closing item is to build the thing that makes many of these at once rather
than a hop a day.

## Current state

| | |
| --- | --- |
| Bergitte Aukland | **no Wikidata item** — `reports/wikidata-bergitte.qs` creates her |
| Marta Jonsdatter Li | **`Q141178381`**, made 2026-08-25 |
| Marta's parents | `reports/wikidata-jon-parents.qs` — wait, that is *Jon's* parents |
| Jon Samuelsen Raustad | **`Q141168955`** |
| Jon's parents | Samuel Jonson Raustad + Marta Jonsdatter Li — the latter now exists |
| Ane Oline Jonsdatter Raugstad | no item |
| Arne Garborg | **`Q467497`** |
| steps 2–8 (Mjølhus / Rossavik / Mele) | none on Wikidata |
