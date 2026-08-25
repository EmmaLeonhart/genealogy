# The three lines

**Emma, 2026-08-25:** *"Yes it should be three lines lol: Charlemagne to Bergitte, Bergitte to me,
Bergitte to Arne."* `CLAUDE.md` § *THE THREE LINES* is the rule; this file is the person-by-person
state.

**Bergitte Gunnbjørnsdatter Aukland** `6000000002481819312`, 1465–1522, is the hinge — an ancestor
of both Emma and Arne (Arne at depth 11), and the one on both lines who descends from Charlemagne.
She has **no Wikidata item**; `reports/wikidata-bergitte.qs` creates her.

| line | people | have items | to create |
| --- | ---: | ---: | ---: |
| 1. Charlemagne → Bergitte | 23 | 9 | **14** |
| 2. Bergitte → Emma | **not captured** | — | — |
| 3. Bergitte → Arne | 12 | 3 | **9** |

Lines 1 and 3 are one saved path, `paths/charlemagne-to-arne-garborg.tsv`, 34 steps.

## Line 3 — Bergitte → Arne (steps 12 → 1)

| step | person | state |
| ---: | --- | --- |
| 12 | **Bergitte Gunnbjørnsdatter Aukland** | create |
| 11 | Gunnbjørn Jonson Mjølhus | create |
| 10 | Lars Gunnbjørnsen Mjølhus | create |
| 9 | Peder Larsen Mjølhus | create |
| 8 | Lars Person Nedre Rossavik | create |
| 7 | Berit Larsdatter Nedre Rossavik | create |
| 6 | Lars Tormodsen Mele | create |
| 5 | Jon Larson Mæle | create |
| 4 | Marta Jonsdatter Li | create |
| 3 | Jon Samuelsen Raustad | **`Q141168955`** |
| 2 | Ane Oline Jonsdatter Raugstad | **`Q141152523`** |
| 1 | **Arne Garborg** | **`Q467497`** |

## Line 1 — Charlemagne → Bergitte (steps 34 → 12)

| step | person | state |
| ---: | --- | --- |
| 34 | **Charlemagne** | **`Q3044`** |
| 33 | Louis I, The Pious | **`Q43974`** |
| 32 | Giséle of Cysoing | create |
| 31 | Berengar I, emperor of the Romans | create |
| 30 | Gisela of Friuli | **`Q3769073`** |
| 29 | Berengar II of Ivrea, king of Italy | **`Q314521`** |
| 28 | Rozala of Italy | create |
| 27 | Baldwin IV the Bearded, count of Flanders | **`Q378177`** |
| 26 | Judith of Flanders | **`Q273181`** |
| 25 | Skule Torstigson | **`Q6180419`** |
| 24 | Åsulv Skulesson | **`Q75291928`** |
| 23 | **Guttorm Àsulfsson à Rein** | **`Q19061035`** — the deepest existing item |
| 22 | Ingrid Guttormsdotter | create |
| 21 | Helena Guttormsdatter | create |
| 20 | Knut Valdemarsson, Duke of Estland, Blekinge and Lolland | create |
| 19 | Svantepolk Knutsson Viby, Skarsholmsätten | create |
| 18 | Ingegerd Svantepolksdotter | create |
| 17 | Algot Bryniolfsson | create |
| 16 | Knut Algotsson | create |
| 15 | Ramborg Knutsdotter Lejon | create |
| 14 | Knight Tore Gardsson | create |
| 13 | Lagmann Gunnbjørn Toresson Tengs | create |
| 12 | **Bergitte Gunnbjørnsdatter Aukland** | create |

## Line 2 — Bergitte → Emma

**Missing.** Emma descends from Bergitte by a different line from Arne's, and no saved page covers
it. Save the Geni relationship page, then
`python -m genimerge path-from-html <page> -o paths/bergitte-to-emma.tsv`.

## The shape of the work

**19 of the 22 creations are consecutive** — steps 4–22, the entire Norwegian and Swedish middle:
Mele, Nedre Rossavik, Mjølhus, Tengs, Lejon, Algotsson, Svantepolksdotter, Guttormsdatter. The
royal end is already on Wikidata. **Create steps 4–22 and Arne is continuously linked to
Charlemagne.**

**Two files per batch, always.** `LAST` is only valid as a QuickStatements subject, never as a
value, so people created in one run cannot cite each other. Creations first, then
`scripts/build-missing-reciprocals.py` for the relationships once the QIDs exist.

## Do not confuse this with `reports/charlemagne-route.csv`

That file is a **different** 399-step Emma→Charlemagne descent up another branch, and it does
**not** contain Bergitte. Treating the two as the same thing produced a wrong junction on
2026-08-25. `paths/charlemagne-to-arne-garborg.tsv` is the authority for the three lines.
