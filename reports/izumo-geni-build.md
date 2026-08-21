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

## THE MERGE THAT MATTERS — two Takatoki profiles

**`Takatoki Izumo-kokuso` `6000000019459698488` already existed**, from the older
additions, and it already carries the whole modern tree beneath it:

    Takatoki Izumo-kokuso [6000000019459698488]
      Takamune Senge [6000000019459773306]  -> Naokuni Senge [...924115]
      Sadataka Kitajima [6000000019459854230]
      Kiyotaka Izumo [6000000019460072018]
      Kojobo Izumo [...878161]
      Kagetaka Mukai [...756746]
      Wife of Munenao Nanjo Izumo [...756758]

The `Takatoki 53 Izumo` `6000000227334408837` created today under Yasutaka 52 is the
**same person**. So this is not merely a duplicate to tidy — **merging these two joins
the numbered kokuso chain to the entire existing Senge and Kitajima tree**, which is
the join the whole exercise is for. It is the highest-value item in this file and it
is Emma's to perform.

It also means **54 and 55 need no creating**: Kiyotaka 54, Senge Takamune 55 and
Kitajima Sadataka 55 are already there under the old Takatoki.

## Fourth block — the Hiraoka line, absent in full

The chart runs a Hiraoka column in parallel with the Izumo line from generation 53
down. **None of it existed.** Created as a chain off Yasutaka 52:

    Sadataka Hiraoka [6000000227334496889]
      Takataka Hiraoka [6000000227334666836]
        Tsunetaka Hiraoka [6000000227334638839]
          Kuninori Hiraoka [6000000227334708829]
            Naonori Hiraoka [6000000227334638877]
              Naotaka Hiraoka [6000000227334516908]
                Naokiyo Hiraoka [...]

Named given-first per Emma's rule, so `Hiraoka no Sadataka` becomes `Sadataka Hiraoka`.

**79 people created in total.**

## A silent failure mode, found late — saves that report success and do nothing

Geni's add dialog **rejects a save when Status is neither Living nor Deceased**, with
`Please select Living or Deceased for this person.` The status radio is only
pre-selected when the *parent* carries dates; on a profile created today it is blank.
Clicking Save then does nothing at all, and a script that only clicks the button
cannot tell the difference — `Kuninori Hiraoka` reported `OK` twice and did not exist
either time.

The helper now **sets Deceased explicitly** and, after saving, **looks for the error
text and reports `ERR` instead of `OK`**. Everything created before this fix was
verified by re-reading the parent's child list, which is the only trustworthy check:
the return value of the add is not evidence.

## Fifth block — the Kitajima line, 55 to 79, which did not exist at all

`Sadataka Kitajima` `6000000019459854230` had **no children on Geni**. The chart runs
a Kitajima column in parallel with Senge from generation 55 to 79 and then on to
Daikou, and none of it was there. Checked twice before creating: by walking the tree
from Takatoki 53 down, and by Geni name search for `Eitaka Kitajima` and
`Hisataka Kitajima`, which returned nothing. `Takatomi Senge` returned
`Takatomi 80 Senge`, so the search itself was working.

**The headship crosses houses, so column alignment is not enough.** Kitajima no
Masataka 60 descends from **Inaoka no Nobutaka** and Hidetaka 61 from **Takahama no
Tomotaka**, both cadet houses; the grid puts a Kitajima box directly above each of
them. `reports/izumo-chart-edges.md` carries the full edge list and how it was read.

## How the adds are driven now — an iframe, so the save's reload lands elsewhere

The 2026-08-19 method scripted the dialog on the profile page itself. That works, but
**saving reloads the page**, which wipes the helper, so the helper had to live in
`localStorage` and be `eval`-ed once per person - one tool call per person, and a
person takes about a minute.

The page now opens the parent's profile in a **hidden iframe** and drives the dialog
inside it. The reload happens in the iframe; the driving page keeps its state. That
makes the whole thing a background loop over a work list in `localStorage`, so a
33-person chain is one call to start and one call to check.

Two things this needed:

- **The queue is idempotent.** Before creating, it reads the parent's child list and
  returns the existing id if a child of that name is already there. This is not
  tidiness: a CDP call that times out at 45 seconds has usually *succeeded* on Geni,
  and the first attempt at Yukitaka 57 did exactly that - the timeout was reported as
  a failure, the queue retried, and **there are now two Yukitaka 57 Kitajima**.
- **The verification matches on first + last only.** Geni's profile slug drops the
  middle name, so `Yoshitaka-Kitajima` is what comes back for `Yoshitaka 56
  Kitajima`. Matching the full name reported a successful save as a failure.

## Duplicate created today, for Emma to merge

| person | keep | duplicate | how it happened |
| --- | --- | --- | --- |
| Yukitaka 57 Kitajima, son of Yoshitaka 56 | `6000000227335131944` | `6000000227335334829` | Mine, 2026-08-20. A 45-second tool timeout on a save that had actually gone through, retried. The queue now checks the parent's children first, so this shape cannot repeat. |
| Sadakiyo En'ya, son of Yoriyasu En'ya | `6000000019402925048` (pre-existing) | `6000000227335445948` (empty) | Mine, 2026-08-20. The pre-check compares the name Geni puts in the profile slug; I passed a curly apostrophe and Geni's slug uses a straight one, so `Sadakiyo En’ya` did not match the `Sadakiyo En'ya` already sitting there. The comparison now ignores apostrophes entirely. |

### Created 2026-08-20 — 43 people

Kitajima line and its cadet houses, off `Sadataka Kitajima` `6000000019459854230`:

| person | Geni ID | parent |
| --- | --- | --- |
| Yoshitaka 56 Kitajima | `6000000227335094894` | Sadataka Kitajima 55 |
| Yukitaka 57 Kitajima | `6000000227335131944` | Yoshitaka 56 |
| Takataka 58 Kitajima | `6000000227335301867` | Yukitaka 57 |
| Yoshitaka 59 Kitajima | `6000000227335324856` | Takataka 58 |
| Nobutaka Inaoka | `6000000227335076025` | Takataka 58 |
| Yoshitaka Takahama | `6000000227335365827` | Takataka 58 |
| Saburou Kitashima | `6000000227335233864` | Yoshitaka 59 |
| Masataka 60 Kitajima | `6000000227335360837` | Nobutaka Inaoka |
| Tomotaka Takahama | `6000000227335310891` | Yoshitaka Takahama |
| Hidetaka 61 Kitajima | `6000000227335366839` | Tomotaka Takahama |
| Tokitaka Kitajima | `6000000227335393824` | Saburou Kitashima |
| Yasutaka Kitajima | `6000000227335224861` | Tokitaka |
| Hisataka 62 Kitajima | `6000000227335155963` | Yasutaka |
| Hirokatsu 63 Kitajima | `6000000227335430822` | Hisataka 62 |
| Harutaka 64 Kitajima | `6000000227335378827` | Hirokatsu 63 |
| Tsunetaka 65 Kitajima | `6000000227335430827` | Harutaka 64 |
| Kanetaka 66 Kitajima | `6000000227335397826` | Tsunetaka 65 |
| Michitaka 67 Kitajima | `6000000227335299879` | Tsunetaka 65 |
| Mototaka Hisayama | `6000000227335337871` | Tsunetaka 65 |
| Naotaka 68 Kitajima | `6000000227335344839` | Michitaka 67 |
| Yoritaka 69 Kitajima | `6000000227335339873` | Naotaka 68 |
| Akitaka 70 Kitajima | `6000000227335337887` | Yoritaka 69 |
| Okitaka 72 Kitajima | `6000000227335008051` | Yoritaka 69 |
| Yoritaka 73 Kitajima | `6000000227335376843` | Yoritaka 69 |
| Nobutaka 71 Kitajima | `6000000227335365856` | Akitaka 70 |
| Zentaka 74 Kitajima | `6000000227335365861` | Yoritaka 73 |
| Naotaka 75 Kitashima | `6000000227335402830` | Zentaka 74 |
| Naritaka 76 Kitajima | `6000000227335317853` | Naotaka 75 |
| Yoshinori 77 Kitajima | `6000000227335420843` | Naritaka 76 |
| Eitaka 78 Kitajima | `6000000227335288917` | Yoshinori 77 |
| Takataka 79 Kitajima | `6000000227335344862` | Eitaka 78 |
| Daikou Kitajima | `6000000227335337905` | Takataka 79 |
| Motonori Yakura | `6000000227335305897` | Mototaka Hisayama |
| Kazutaka Yakura | `6000000227335311870` | Motonori Yakura |

The Akatsuka branch and the four Senge kokuso that reach the headship through it,
off `Takakuni Senge` `6000000019459850459`:

| person | Geni ID | parent |
| --- | --- | --- |
| Masatoki Akatsuka | `6000000227335344886` | Takakuni Senge 57 |
| Masakuni Akatsuka | `6000000227335337914` | Masatoki |
| Tokinobu Akatsuka | `6000000227335416833` | Masakuni |
| Kazunobu Akatsuka | `6000000227335383864` | Tokinobu |
| Nagatoshi Akatsuka | `6000000227335344896` | Kazunobu |
| Motokatsu 66 Senge | `6000000227335415836` | Nagatoshi Akatsuka |
| Takanou 67 Senge | `6000000227335444826` | Motokatsu 66 |
| Takamitsu 68 Senge | `6000000227335353899` | Takanou 67 |
| Hiromitsu 72 Senge | `6000000227335472827` | Takamitsu 68 |
| Sadatsune Higashi | `6000000227335317878` | Naoharu 70 Senge |

**Which Senge generations already existed, and why the gap had that shape.** Emma
built the Senge upward from Kunimaro, so Geni already held 64, 65, 69, 70, 71, 73,
74, 75, 76, 78, 79, 80 and on to 84 — searched by name, one at a time. The four that
were missing are exactly the four the chart routes through the **Akatsuka** house
(66, 67, 68, and 72 below them), which an upward walk from Kunimaro would never
cross. Sakusa no Jisei was already there as `Sakusa no Jisei Senge`.

**`Sadatsune Higashi` is created but not yet joined to what comes below him.** The
chart makes him the father of `Toshikatsu 75 Senge` (`6000000227331729823`), who
already exists on Geni with a parent of his own. Adding a second father is not a
thing to do quietly, so he stands as a child of Naoharu 70 and the link to 75 is
Emma's.

## Wikidata links in the About field — all 100, done 2026-08-20

`reports/izumo-kokuso-geni.tsv` is the join that made this possible: regnal number,
house, chart name, Geni id, QID, for 100 of the roster's 103. It was built by walking
the Izumo line **by id** — 50 profiles from Yasutaka 52 up to Ameno-hohi 1 — plus one
hop down to the branch numbers the direct ancestral chain skips (26, 28, 29, 31, 32,
43, 46), and a walk down the Senge column for 76-80.

The link written is the form Emma already used, so it matches the profiles she did
herself: `https://wikidata.org/wiki/Special:EntityPage/<QID>#sitelinks-wikipedia`.

**About a third already had it** and were skipped rather than rewritten. Generations
40-52 were hers to a person; the early Izumo line and the whole Senge/Kitajima columns
were empty. **Nothing carried a different QID** — the check is `OTHER`, and it never
fired, so no adjudication was needed anywhere.

Three still have no Geni id and so no link: `Senge no Munetoshi 71`,
`Senge no Toyomasa 73`, `Senge no Toyomi 74`. The chart routes those three through
`Sakusa no Jisei`, which is why a walk down the Senge headship misses them.

**How the write is driven.** Geni's About Me is a lightbox at
`/profile/edit_about_me_lb/<id>`; the form posts to `/profile/edit_about_me/<id>` with
`authenticity_token` and `page_profile[detail_strings][en-US][about_me]`. Existing text
is preserved and the link appended after a blank line.

**Hand-clicking that dialog is not reliable and the failure is silent** — of five done
by real clicks, 5, 6 and 7 saved and 8 and 9 did not, with no error either time. The
dialog's coordinates move between profiles, and a click landing on the toolbar instead
of the textarea types into nothing. Every save here was verified by re-reading the
field, which is the only trustworthy check.

## Created 2026-08-20 — the three people the chart had and Geni lacked

Emma settled the identity question that had held the first one: *"Same person"* —
the chart's `Nintachikatapinomikoto` is Geni's `Nintachikatahi`.

| person | parent | why there |
| --- | --- | --- |
| Izumokusunemino no Mikoto | Kushimikatomi 7 `6000000012789429513` | the chart draws him as Kushida 8's brother, and Geni gives Kushida 8 that father |
| Inakubinomikoto no Mikoto | Takeyamikiru no Mikoto `6000000227333485851` | chart column 652 |
| Isonokaya Sukune no Mikoto | Nintachikatahi `6000000227333084907` | chart column 1072 |

## Two more merges for Emma, both mine

| person | keep | duplicate |
| --- | --- | --- |
| Sadatsune Higashi, son of Naoharu 70 | `Higashisadatsune Senge` — already had Toshikatsu 75 under him | `6000000227335317878`, created by me 2026-08-20, empty |
| Shikatahime no Mikoto, sibling of Kushimikasaki 5 | `6000000227336200852` | `6000000227337123821` |

**`Sadatsune Higashi` is why the "second father" worry was wrong.** This file previously
recorded that joining him to `Toshikatsu 75 Senge` would give Toshikatsu two fathers and
was therefore Emma's call. It would not: Toshikatsu 75's father on Geni *is* that man,
written `Higashisadatsune Senge`, and the profile I created is a duplicate of him
standing beside him as his own brother. The chart edge was already there.


## Two junk profiles I created 2026-08-20, both duplicates of people already there

| mine, empty | the real one | parent |
| --- | --- | --- |
| `6000000227350446840` Munetoshi 71 Senge | `6000000227331623899` — has Toyomasa 73 and Toyomi 74 under him | Sakusa no Jisei Senge |
| `6000000227349108826` Inakubinomikoto no Mikoto | `6000000227333964856` Inakubino no Mikoto | Takeyamikiru no Mikoto |

**Same failure as the one already written into `devlog.md` today, hours later.** The
Senge-column walk did not reach Munetoshi 71, and this file recorded that as *"three
still have no Geni id"*. It was never a fact about Geni — all three were there, with
their children, the whole time. `Isonokaya Sukune` `6000000227333988831` was likewise
listed as *still missing from this region* and already existed under Nintachikatahi.

**The guard is one fetch and it was skipped:** read the intended parent's child list
immediately before creating, and compare on the given name alone. The earlier Kitajima
run had exactly that check built into its queue; the three creations today were driven
by hand and did not.

Of the three people created today, **one was genuinely new** — `Izumokusunemino no
Mikoto` under Kushimikatomi 7.
