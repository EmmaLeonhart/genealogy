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

## Second block — the numbered line's collaterals, generations 11-21

The main kokuso line **12 to 22 already existed on Geni as a bare chain**: every
numbered person had exactly one child, the next kokuso, and no siblings at all. The
chart gives each of those generations several. That made this block large and
unambiguous — these people are plain siblings of a numbered kokuso, so no
Isetsuhiko-branch judgement was involved.

| parent | children added |
| --- | --- |
| Izumo-Furune 11 | Miyoshiya |
| Ibe no Mikoto | Hishirahime, Igasokumano |
| Ukatsu Kunu 12 | Iimochi, Otofukuno, Kisumino, Mikihime, Minibuno, Izumo Kasayano |
| Okimimi 13 | Kitashiko, Kutano, Mitamino, Uke, Nanashi, Koneno |
| Raihita no Wiho 14 | Otonakushihimeno, Kushimarozu Ashinazu, Hotsukono |
| Mishima 15 | Ami, Oshimakono, Fusu, Sahine, Kaguro |
| Ou 16 | Kiwamebi, Ayoutsunino, Kumamarono |
| Miyamukasu 17 | Ayu, Tomonoomi, Mananoomi, Kasa |
| Funin 18 | Tagiko, Shishikoomi, Tomu, Ibanushi |
| Funei 19 | Ishiazu, Makiyama, Kushi, Manbei |
| Ihohiku 20 | Chino, Ninikioomi, Omarono, Fushimaro |

**63 people created in total across both blocks.**

## How the adds are driven, because the UI fights back

Three mechanisms were tried and only the third is usable.

- **The tree canvas** re-renders and pans between one click and the next, so about two
  thirds of clicks land on empty space. It also served a **stale render** — showing
  Isetsuhiko with only one child when he already had two — which is what produced the
  duplicate Kamisahime. Abandoned on Emma's instruction.
- **Coordinate clicking on the profile dialog** works but the browser window keeps
  resizing between calls (1536x674, 1568x688, 1568x745 all seen in one session), so
  fixed coordinates drift and silently miss the name field. Several adds saved blank
  and had to be redone.
- **Scripting the dialog** is what works: click `Add Family`, set the relationship
  select to `child`, set the first-name input and fire `input`/`change`, pick the
  gender radio by its adjacent label text, click `Save`. No coordinates anywhere.

**Saving reloads the page**, which wipes any helper defined on `window` — including
when `Add another family member` is ticked, so that checkbox does not actually chain.
The helper is therefore kept in `localStorage.__ADD` and `eval`-ed at the start of
each call, which survives the reload and makes each person a single tool call.

## Naming artifact worth a look

Geni's `Suggest surnames` fills the surname from the parent, so children added under
`Mishima 15 Ashinazu-ni-Mikoto` came out as `Ami Ashinazu-ni-Mikoto`,
`Fusu Ashinazu-ni-Mikoto` and so on, and those under `Funei 19 Izumo` came out as
`Tagiko Izumo`, `Kushi Izumo`. The chart writes them as bare given names. This was
left as Geni generated it rather than corrected mid-run — flagging it rather than
deciding it.

## Emma's naming rule for the later generations, not yet reached

**`Higashianatsuu Senge` and its like are really `Anatsuu Higashi`** — Emma,
2026-08-19: *"they are all more like 'Anatsuu Higashi' and they should be changed
accordingly once you reach that point"*. So the chart's run-together forms in the
Senge/Kitajima/Higashi/Takaoka/Hiraoka/Akatsuka generations are surname+given
concatenated and must be split, given name first. This applies from roughly
generation 51 onward and has not been reached yet.

## Third block — gaps in the numbered line itself, 26 to 53

Walking the chain by ID showed the succession **skipping numbers**: Geni ran
25 → 27 → 30 → 33 and 42 → 44 → 45 → 47, so eight numbered kokuso simply did not
exist. These are not collaterals; they are holes in the spine.

| created | parent |
| --- | --- |
| Otoyama 26 | Ka'an 24 |
| Kunikami 28 | Otoyama 26 |
| Kuninari 29 | Otoyama 26 |
| Chikuni 31 | Kuninari 29 |
| Kanemutsu 32 | Masakata 27 |
| Munefusa 43 | Yukikane 42 |
| Kaneie | Munefusa 43 |
| Kanetsune 46 | Kaneie |
| Takatoki 53 | Yasutaka 52 |

The regnal number goes in the **middle-name** field, matching how the existing chain
is written (`Hiroshima 25 Izumo` = first `Hiroshima`, middle `25`, last `Izumo`).

**72 people created in total.**

## The name inversion, applied — Emma's rule

*"they are all more like 'Anatsuu Higashi' and they should be changed accordingly once
you reach that point"* — reached, and done. Ten profiles renamed:

| was | now |
| --- | --- |
| Higashitakakage Senge | Takakage Higashi |
| Higashitokitaka Senge | Tokitaka Higashi |
| Higashitakataka Senge | Takataka Higashi |
| Higashisadayori Senge | Sadayori Higashi |
| Higashitakanori Senge | Takanori Higashi |
| Higashiyasunori Senge | Yasunori Higashi |
| **Higashianatsuu Senge** | **Anatsuu Higashi** |
| Higashiyoshiakira Senge | Yoshiakira Higashi |
| Higashisadanobu Senge | Sadanobu Higashi |
| Higashinobutoshi Senge | Nobutoshi Higashi |

Two things this confirmed. The surname was **`Senge`, which was also wrong** — these
people are Higashi, not Senge; the concatenated form had buried the real surname
inside the given name and left a wrong one in the surname field. And the **Takaoka
profiles in the same branch were already correct** — `Sadashige Takaoka`,
`Shigeyori Takaoka`, `Shigeyasu Takaoka` — so the inversion is specific to the
run-together spellings, not to the branch.

Renames go through `https://www.geni.com/profile/edit_basics/<id>`, which is a plain
form: set `page_profile[names][en-US][first_name]` and `[last_name]`, then click
**`Save & Close`** — not `Save`, which is what the add dialog uses.
