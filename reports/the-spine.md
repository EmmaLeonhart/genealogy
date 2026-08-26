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

**Geni states it: "Bergitte Gunnbjørnsdatter Aukland is your 13th great grandmother."** Read from
<https://www.geni.com/people/Bergitte-Aukland/6000000002481819312?through=6000000087535357291> on
2026-08-25 — the `?through=` form pins the relationship to a chosen profile, which is how this
page is obtained without fighting the push-pin control.

**13 great-grandmother generations means roughly 15 steps**, against Arne's 11 (his 9th great
grandmother). So line 2 is the longer of the two.

**The step-by-step path is not yet captured.** Expanding the panel needs the page saved and run
through `python -m genimerge path-from-html <page> -o paths/bergitte-to-emma.tsv`; three attempts
to expand it in the browser ended with the renderer timing out.

## The absences were never established — and three more just fell

**Emma, 2026-08-25:** *"we didn't actually establish in any meaningful sense that the people are
absent in that chain... We might basically find that that one single daughter is the only person
absent in the line in Wikidata, but it's just that the Wikidata ones are not genealogically
linked."*

She was right twice over. Of the 34 chain steps: **14 hold a `P2600`, 7 are existing Wikidata
items we had called absent, and 13 remain to create.** The count of people to make has fallen from
22 to 13 without a single edit.

Four were found by the structural search. **Three more were found by name and then confirmed
structurally**, which is the order that matters — the name only produced the candidate:

| step | ours | item | what agrees |
| ---: | --- | --- | --- |
| 21 | Helena Guttormsdatter | `Q4953376` | identical label · father Guttorm · spouse **Esbern Snare** · children **Canute, Duke of Estonia** and **Ingeborg of Kalundborg** |
| 19 | Svantepolk Knutsson Viby | `Q6197518` *Svantepolk of Viby* | father **Canute, Duke of Estonia** · mother **Hedvig Svantepolksdotter** · spouse **Benedicta of Bjelbo** · four children match |
| 18 | Ingegerd Svantepolksdotter | `Q101247444` *…of Viby, lady of Händelöö* | **both** parents match |

**They chain, which is stronger than any of them alone.** Helena's son is Svantepolk's father is
Ingegerd's grandfather, and step 20 — Knut Valdemarsson — was already matched to `Q3743799`
*Canute, Duke of Estonia*. So **steps 18, 19, 20 and 21 are a contiguous run that exists on
Wikidata in full**, joined to each other there, and unlinked to Geni only because no `P2600` names
them.

`reports/wikidata-spine-add-p2600.qs` adds the identifier to all seven. Nobody is created.


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
