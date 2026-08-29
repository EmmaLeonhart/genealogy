# The three lines

**Emma, 2026-08-25:** *"Yes it should be three lines lol: Charlemagne to Bergitte, Bergitte to me,
Bergitte to Arne."* `CLAUDE.md` § *THE THREE LINES* is the rule; this file is the person-by-person
state.

**Bergitte Gunnbjørnsdatter Aukland** `6000000002481819312`, 1465–1522, is the hinge — an ancestor
of both Emma and Arne (Arne at depth 11), and the one on both lines who descends from Charlemagne.
She has **no Wikidata item**. `reports/wikidata-garborg-day.qs` creates her — the standalone `wikidata-bergitte.qs` was deleted on 2026-08-26 because both created her and running both would have duplicated the one person all three lines hinge on.

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

## Line 2 — Bergitte → Emma — CAPTURED 2026-08-26

**It exists now.** `paths/bergitte-to-emma.tsv`, 16 steps, read straight out of the live
relationship panel rather than from a saved page — three earlier attempts to expand it in a
browser had ended with the renderer timing out, and saving the page turned out to be unnecessary:
the panel's `span.segment > span.name` nodes carry the name and the sibling `a[href*="/people/"]`
carries the Geni id, which is the same scoping `genimerge.genipage` applies to a file.

**`python -m genimerge path` reports 16 of 16 steps held.** Every person on line 2 is already in
our corpus, so **line 2 needs no exports at all** — unlike lines 1 and 3, which took two.

| step | person | state |
| ---: | --- | --- |
| 1 | **Emma Leonhart** | `Q140568870` exists and carries **no** `P2600` — add the id, do not create |
| 2 | Richard Wade Borsheim, b.1963 | **her father — explicitly not to be created**, and past the cutoff besides |
| 3 | Randolph Paulus Borsheim, b.1926 | past the 1880 cutoff |
| 4 | Reinhert Borsheim, b.1891 | past the 1880 cutoff |
| 5 | Rakel Rasmusdottir Borsheim, b.1866 | create — the first creatable step |
| 6 | Anne Berta Osmundsdatter Nese | create — **adoptive** mother, the one non-blood link on the line |
| 7 | Osmund Larsson Nese | create |
| 8 | Lars Osmundsen Foss-Eikeland, d. y. | create |
| 9 | Osmund Larsen Raunes | create |
| 10 | Lars Nilsen Raunes | create |
| 11 | Nils Larsen Raunes | create |
| 12 | Guri Pedersdatter Foss | create |
| 13 | Cecilie Olsdatter Håland | create |
| 14 | Gudrun Sæbjørnsdatter Talgje | create |
| 15 | Sissel Jonsdatter Talje | create |
| 16 | **Bergitte Gunnbjørnsdatter Aukland** | create — the hinge, shared with lines 1 and 3 |

**Geni states "your 13th great grandmother"**, and 13 great-grandmother generations against 15
steps is consistent: two of the steps are the adoptive-mother link and Emma's own father.

**So line 2 is 12 creations, not 16**: Emma gets a `P2600` on an item that already exists, and
steps 2–4 are all born after the 1880 modern cutoff — her father b.1963, his father b.1926, and
Reinhert b.1891. The first creatable step is Rakel Rasmusdottir Borsheim, b.1866.

**Bergitte appears on all three lines**, so creating her once serves every one of them.

**The whole spine, now that all three lines exist:** 13 to create on lines 1 and 3, plus 12 on
line 2, minus Bergitte counted twice — **24 people**, of whom 7 are the already-existing items in
`reports/wikidata-spine-add-p2600.qs` and Emma is an eighth.

## The shape of the work

**19 of the 22 creations are consecutive** — steps 4–22, the entire Norwegian and Swedish middle:
Mele, Nedre Rossavik, Mjølhus, Tengs, Lejon, Algotsson, Svantepolksdotter, Guttormsdatter. The
royal end is already on Wikidata. **Create steps 4–22 and Arne is continuously linked to
Charlemagne.**

**Two files per batch only for new-to-new links.** People created in one run cannot cite each
other, because `LAST` names only the most recent item.
**`LAST` IS valid as a value; the limit is narrower than this repo long claimed.**
`Q141178381 P22 LAST` is ordinary QuickStatements — the subject already exists and `LAST`
resolves to the item created just above. What cannot be done is linking **two items created
in the same run** to each other, because `LAST` names only the most recent one.

Emma, 2026-08-25: *"you never actually did the 2-way relationship addin qith the creation of
items that is completely possible but you just decide to fuck off and no do it because it goes
QID PID LAST instead of LAST PID QID."* The general claim was mine, not hers, and it cost her
weeks of one-way links to repair by hand.

So the second file carries only the links between two people the batch created. Everything joining
a new person to an item that already exists goes out both ways in the first file.

## Do not confuse this with `reports/charlemagne-route.csv`

That file is a **different** 399-step Emma→Charlemagne descent up another branch, and it does
**not** contain Bergitte. Treating the two as the same thing produced a wrong junction on
2026-08-25. `paths/charlemagne-to-arne-garborg.tsv` is the authority for the three lines.

## A fourth line — Arne → Signe, no Borsheim

**Emma, 2026-08-29:** *"your path gets added starting at Arne and moving to Signe. Record this as
another spine and wire it in."* And, when asked which of the two: *"Your path not genis"*.

`paths/arne-to-signe-no-borsheim.tsv`, **15 steps**, in `SPINE_PATHS` since 2026-08-29. Built by
`scripts/path-between.py 6000000003492005116 6000000177921459072 --avoid Borsheim` over our own
tree, not from a saved page.

**Why it excludes Borsheims.** Signe's own surname is Borsheim by marriage, so the family the
endpoint is named for is not a family the path may travel through — she asked for a route that
*"does not go through any Borsheim"*. 167 people carry the name in a label and were removed from
the graph before the walk, endpoints excepted.

| step | person | state |
| ---: | --- | --- |
| 1 | Aadne Eivindson Garborg | **`Q467497`** |
| 2 | Ane Oline Jonsdatter Raugstad | **`Q141152523`** |
| 3 | Jonas Jonson Heigre | **`Q141168957`** — her husband, the marriage the route turns on |
| 4 | Jon Olsen Heigre | **`Q141199892`** |
| 5 | Berte Karine Jonsdatter Stokka | create |
| 6 | Torger Torgerson Stokka | create |
| 7 | Berta Guria Davidsdatter Stokka | create |
| 8 | Kristine Sørensdatter Gjesdal | create |
| 9 | Søren Sørenson Gjesdal | create |
| 10 | Inger Sørensdatter Lima | create |
| 11 | Ola Helgeson Lima | create |
| 12 | Ådne Olsson Lima Kyllingstad. Lima | create |
| 13 | Inger Serine Lerma Gunderson | create |
| 14 | Sophia Borgit Hoknes | create |
| 15 | **Caroline Signe Borsheim** | create |

**Four of 15 held items when it went in**, so the walk starts at step 5 and eleven creations close
the line.

**It is two steps longer than the route on her saved page, deliberately.**
`paths/caroline-signe-borsheim-hoknes.tsv` reaches Signe in 13 by hopping `his sister` and
`her sister` directly. `path-between.py` walks parent, child and spouse edges only, so it routes
through the shared parent instead and names **Jon Olsen Heigre** and **Søren Sørenson Gjesdal** —
two real people who have to exist for the line to be continuous either way. She chose this one over
Geni's.

**That saved file holds TWO paths end to end**, steps 1–13 and 14–31, which is the `nn-basse.tsv`
shape `CLAUDE.md` warns about. Any measurement treating it as a single 31-step chain counts a
non-existent edge between step 13 and step 14.
