# Putting the Ono pedigree on Wikidata: a plan

Written 2026-10-03 for the user's goal: "My end interest is potentially
importing this tree onto Wikidata, although I'm not really sure how to ...
present it properly with its records and such." Every P and Q id below was
checked against Wikidata on 2026-10-03.

## The principle

Wikidata records **what sources say**, not what is true, so a forged
pedigree can go on it as long as every statement says where it comes from
and that it is disputed. The pedigree itself becomes the source item.

## Step 1: an item for the document

Create an item for the 斎部宿禰本系帳 (there is none; searched in ja/en):

| Property | Value |
|---|---|
| label en / ja | Inbe no Sukune honkeichō / 斎部宿禰本系帳 |
| description en | 1870 genealogy of the Ono family, claimed descendants of the Inbe clan |
| P31 instance of | Q87167 manuscript (and/or Q189977 family tree) |
| P407 language of work | Japanese (classical Chinese style) |
| P9836 NDL Persistent ID | 2538213 (the bound volume; formatter `https://dl.ndl.go.jp/pid/$1`) |
| P1310 statement disputed by | Q6536257 Kosugi Sugimura, as a qualifier on a statement such as P50 author = Q6536470 Suzuki Matoshi (鈴木真年) with P1480 sourcing circumstances = Q32188232 allegedly |

Wikidata labels 鈴木真年 as "Suzuki Matoshi" (Q6536470). Same person as the
"Suzuki Masatoshi" in these notes.

## Step 2: items for the people

- **Gods already on Wikidata**: Takamimusubi Q125400, Futodama Q11059539,
  Ame no Hiritome Q85879124, Ame no Kushimimi Q110064736, Ame no Tomi
  Q24899653, Kamimusubi Q3275901, Ame no Hiwashi Q10939697, Ōasahiko
  Q134846383. Reuse them.
- **Already created by the user**: Tahiko no Sukune Q141627252.
- **About 36 new items** for the other pedigree people. Suggested shape:
  - P31 = **Q13002315 legendary figure**, not Q5 human. Q4271324 mythical
    character or Q524158 kami are the options for the gods (命) of the
    Iinagahime and Yufutsunushi generations.
  - Labels: English (the roster's reading) and Japanese (the kanji). Where the
    roster flags the reading as a guess, give only the Japanese label, or put
    the guess in the English *alias*, not the label.
  - Description: "figure in the 1870 Ono family Inbe pedigree".
  - P1343 described by source = the honkeichō item, with P958 section / P304
    page = the NDL image number.

## Step 3: the family links

On each link (P22 father, P25 mother, P40 child, P26 spouse):

- qualifier **P1480 sourcing circumstances = Q18912752 disputed**, or
  Q32188232 allegedly;
- reference **P248 stated in = the honkeichō item**, plus P304 page = NDL
  image number, plus P854 reference URL = the NDL page.

## The decision only the user can make

**NEEDS-DECISION (the user): should the forged chain touch the real people?**
Inbe no Kobito (Q11490720) and Inbe no Shikobuchi (Q11490725) are real
officials. Adding "father: Sagashi" to them, even marked disputed, puts the
forgery on real historical figures. Many editors would object. The options:

1. **Stop the chain one step short.** Give Sagashi no child statement, and add
   only P1343 described by source = the honkeichō to Kobito and Shikobuchi.
   The chain stays in the legendary items. This is the conservative option.
2. **Link them, disputed.** Add P22 on Kobito and Shikobuchi with P1480
   disputed and the honkeichō reference. This is the most complete and the
   most likely to be challenged.
3. Option 1, plus a talk-page note on Kobito explaining the pedigree.

## Mechanics: the three-batch pipeline (user's design, 2026-10-03)

`genealogy/ono_wikidata_pipeline.py` writes QuickStatements **3.0** batches
(V1 syntax) into `genealogy/wikidata/`. The user reviews and runs each one.
Before each later batch, a SPARQL lookup finds what the earlier batch created.

1. `batch1` creates **the source item** for the 斎部宿禰本系帳: labels en/ja,
   descriptions, P31 manuscript and family tree, P407 Japanese, P9836 NDL
   Persistent ID 2538213, P571 c. 1870, and P50 Suzuki Matoshi *allegedly*,
   disputed by Kosugi Sugimura.
2. `batch2` finds the source item by P9836 = 2538213, then **creates the
   people without linking them**:
   - labels: the characters as the **ja** and **zh** labels; the romanised
     name as the **en, mul, fr, id and es** labels (the same text in each),
     including the readings flagged as guesses; **no Korean label** (the
     user's instruction, 2026-10-03); plus a description;
   - P31 kami or legendary figure, and P21 sex, both cited to the source;
   - **P1343 described by source = the source item, with qualifier P1545
     series ordinal = the pedigree id** (e.g. "H11"), which batch 3 uses to
     find them;
   - **estimated P569 / P570**: decade precision (`/8`), qualifier P1480
     sourcing circumstances = Q5727902 circa, **deprecated rank (`R-`)**, and
     P2241 reason for deprecated rank = Q25895909 "cannot be confirmed by other
     sources". These carry **no reference**: they are estimates, not claims of
     the source (the user's instruction).
   - The 11 people already on Wikidata get only the P1343 statement.
3. `batch3` finds all 49 by their P1545 ordinal, then writes the **family
   links** (P22, P25, P40, P26). Each is qualified P1480 = disputed and cited
   with S248 stated in = the source, S958 section = "NDL frame N", and S854 =
   the direct frame URL `https://dl.ndl.go.jp/pid/2538213/1/N`. By default it
   skips parent links for the two real people. `--link-real` adds them.

Every citation goes to the source item, except the dates. Rank setting
(`R-`) needs **QuickStatements 3.0**: QuickStatements 2 cannot set ranks
(QS 3.0 user guide, meta.wikimedia.org).

How the date estimates are made: each person is placed at the reign the
pedigree assigns them, using the traditional Nihon Shoki reign dates.
Unplaced people are interpolated between anchors (`make_ono_gedcom.DATES`).
Decade precision is used so the dates don't look exact.

## Caution for batch 3

Some links between items that already exist are already on Wikidata from
other sources, for example Futodama P22 Takamimusubi and Futodama P40 Ame no
Kushimimi (see `wikidata-survey.md`). QuickStatements would add a **second,
"disputed" copy** next to the existing claim. For those, add only the
honkeichō as an extra *reference* on the existing claim, without the disputed
qualifier, or skip them. Lines where both sides already have QIDs are the
ones to check by hand before running.
