# Izumo / Senge clan — building the Shinto-wiki chart onto Geni

Source chart: <https://shinto.miraheze.org/wiki/Izumo_clan> § Genealogy.
Geni entry point: <https://www.geni.com/people/Tsusa-no-mikoto-no-Mikoto/6000000012789160423>

**The chart has no machine-readable relationships** — it is a `{{familytree}}` ASCII
grid rendered as a table, and Emma ruled out parsing it (2026-08-19: *"you can only
look at it visually it's basically an image"*). Edges are read from screenshots of the
rendered chart. Existence on Geni is checked **by profile ID**, not by the tree canvas
— Emma, same day: *"you can just use the IDs and look through the list of children
and add"*. The canvas gave a stale render and cost a duplicate; the ID check did not.

**The regnal number is the join key.** Geni carries it inside the name —
`Tsusa-no-mikoto 4 no Mikoto`, `Kushini-no-mikoto 3 no Mikoto` — so the chart's
numbered kokuso match exactly despite romanisation differing between the 2008
Japanese, 2011 English and 2026 additions. Never match these people by name spelling.

## Rules for this job (Emma, 2026-08-19)

- **Only add individuals the chart has and Geni lacks entirely.**
- **Never merge.** *"just flag the duplicates so I can merge them later merges are not
  difficult"* — duplicates go in the table below and nowhere near a merge tool.
- **Leave `NN no Mikoto` placeholders alone.** They are hers; renaming them from the
  chart was offered and declined.
- Add the Wikidata link to a person's description where it is missing.

## Duplicates to merge — Emma's queue, not mine

| person | keep | duplicate | how it happened |
| --- | --- | --- | --- |
| Kamisahime no Mikoto, daughter of Isetsuhiko | `6000000227333087940` (has children) | `6000000227333445866` (empty) | Mine, 2026-08-19. The tree canvas rendered Isetsuhiko with only Mishirushi; the by-ID check afterwards showed Kamisahime already existed. Canvas render was stale. |

## Created

| person | Geni ID | parent |
| --- | --- | --- |
| Takeyamikiru no Mikoto | `6000000227333485851` | Kushini-no-mikoto 3 `6000000012789241315` |
| Samanahime no Mikoto | `6000000227333613846` | Kushimikasaki-no-mikoto 5 `6000000012789283534` |

## The Isetsuhiko line — state as of 2026-08-19

Emma asked for this branch first: *"it is a lot smaller but also big enough it needs to
be done"*. Measured by ID walk, its **named** spine is already complete to the chart's
end:

    Isetsuhiko [6000000227333117897]
    ├── Mishirushi no Mikoto [...082018]            no children
    └── Kamisahime no Mikoto [...087940]
        └── Misahimino no Mikoto [...488011]
            └── Ikokonehiko no Mikoto [...089032]
                ├── Morojinomi no Mikoto [...091907]
                │   └── Midorokimi no Mikoto [...488020]
                │       ├── Nintachikatahi no Mikoto [...084907]
                │       ├── Hinarajumi no Mikoto, Niihari no Kuni no Miyatsuko [...150827]
                │       └── Hikosonomigoromi no Mikoto [...231821]
                └── NN no Mikoto [...126860] → NN → Etarabihi no Mikoto,
                    Musashi no Kuni no Miyatsuko [...491049]

What is unfinished in it is **9 `NN no Mikoto` placeholders**, and those stay NN by
her instruction.

## Where the numbered succession actually stands on Geni

- **1–11 exist**, as the 2008 Japanese-added chain: Ameno-hohi 1 → Takehinatori 2 →
  Kushini 3 → Tsusa 4 → Kushimikasaki 5 → Kishitsuki 6 → Kushimikatomi 7 → Kushida 8
  → Chiri 9 → Morosu 10 → Ada no Mikoto → **Izumo-Furune 11**.
- **The chart breaks here and so does Geni.** Furune 11's only charted child is
  Miyoshiya no Mikoto, who has no children drawn — Emma: *"that person has no children
  just implied descendants"*. The succession resumes at **12 under Ibe no Mikoto**,
  Furune's brother, and Ibe → `Ukatsu Kunu 12 no Mikoto` `6000000227332010844`
  already exists.
- A separate descent from Ada no Mikoto runs into the **Haji clan** (土師) in
  Japanese — `Nomi-no-sukune 野見` and ~10 generations of 土師 profiles. That is the
  related clan the chart names, not the kokuso line.

## Wikidata

`reports/izumo-kokuso-roster.tsv` — 103 kokuso carrying both a regnal number and a
Wikidata item, extracted from the chart's `[Wikidata]` links. The regnal number joins
it to the Geni name. Emma: the numeric middle names *"are regnal numbers for the Izumo
no Kuni no Miyatsuko"*, not middle names.
