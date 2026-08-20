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

Method: the person's **profile page** → `Add Family` → Relationship `child`. Not the tree
canvas — Emma, 2026-08-19: *"do not fucking use the graphical tree shit just use the
fucking regular individual page"*. The canvas re-renders and pans between clicks, so
roughly two thirds of clicks landed on empty space; the profile-page dialog is stable and
its `Add another family member` checkbox chains several children of one parent.

| person | Geni ID | parent |
| --- | --- | --- |
| Takeyamikiru no Mikoto | `6000000227333485851` | Kushini-no-mikoto 3 |
| Samanahime no Mikoto | `6000000227333613846` | Kushimikasaki-no-mikoto 5 |
| Kaburakono no Mikoto | `6000000227333652921` | Midorokimi no Mikoto |
| Shinono no Mikoto | `6000000227333709850` | Midorokimi no Mikoto |
| Aogatsuhikono no Mikoto | `6000000227333570970` | Nintachikatahi no Mikoto |
| Isumino no Mikoto | `6000000227333741822` | Nintachikatahi no Mikoto |
| Sugase no Mikoto | `6000000227333734826` | Nintachikatahi no Mikoto |
| Otomuhikono no Mikoto | `6000000227333770822` | Nintachikatahi no Mikoto |
| Takemisasuhino no Mikoto | `6000000227333652972` | Nintachikatahi no Mikoto |
| Ikinagano no Mikoto | `6000000227333783821` | Nintachikatahi no Mikoto |
| Kotatemi no Mikoto | — | Aogatsuhikono no Mikoto |
| Aratahishi Sukune | — | Isumino no Mikoto |
| Oshikunishikun no Mikoto | — | Sugase no Mikoto |
| Oyakinotomino no Mikoto | — | Otomuhikono no Mikoto |
| Anawaihikono no Mikoto | — | Etarabihi no Mikoto, Musashi no Kuni no Miyatsuko |
| Ikijirodome no Mikoto | — | Takemisasuhino no Mikoto |
| Otakino no Mikoto | — | Takemisasuhino no Mikoto |
| Kyosahino no Mikoto | — | Ikinagano no Mikoto |

**18 people, all collaterals of the Isetsuhiko branch.**

## How the collaterals were placed, and the guess it rests on

The chart hangs the "Ancestor of *X* no Kuni no Miyatsuko" collaterals off the **main
kokuso line** — its generation rows put them beside Chiri 9, Yomorosu 10 and Ada. Geni
does not: Emma had already built them descending through **Midorokimi**, Kushida 8's
brother, and had `Etarabihi no Mikoto, Musashi no Kuni no Miyatsuko` as a *child* of
Nintachikatahi. Both readings are coherent — the collaterals form their own line through
the non-kokuso brother.

**The additions follow her Geni structure, not the chart's row placement**, because
extending what is already there is what she asked for and because restructuring existing
relationships is merge-shaped work that is hers. Within that, each person's parent comes
from **column alignment in the chart**: the row-11 collaterals sit directly beneath their
row-10 counterparts, so Kotatemi(521)→under Aogatsuhikono(521), Aratahishi(652)→under
Isumino(652), Oshikunishikun(763)→under Sugase(763), Anawaihikono(862)→under
Etarabihi(862), Oyakinotomi(963)→under Otomuhikono(963), Ikijirodome and Otakino→under
Takemisasuhino, Kyosahino(1445)→under Ikinagano(1445).

**What would falsify it:** if Emma says the collaterals belong on the main line as the
chart draws them, every one of these 18 moves up a branch. Nothing else about them
changes — the people are right, only the attachment point is the guess.

## Still missing from this region

- `Isonokaya Sukunenomikoto` — chart column 1072, aligned under `Nintachikatapinomikoto`,
  which is probably the same person as Geni's `Nintachikatahi` under a different
  romanisation. Held because that identity is exactly the kind of call Emma makes.
- `Izumokusunemino Mikoto` — chart row 8, brother of Kushida 8 and Midorokimi.
- `Inakubinomikoto`, Ancestor of Tsushima no Miyatsuko — chart column 652, directly under
  `Takeyamikiru no Mikoto`, who did not exist until today.


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
