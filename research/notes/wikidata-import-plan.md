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

## Mechanics

`genealogy/make_ono_quickstatements.py` writes a **draft** in QuickStatements
v1 format, for review only. **Do not run it without reading it.** It has two
phases:

- **Phase 1** (`genealogy/ono_quickstatements_phase1.txt`): create the
  honkeichō item and the new people, with labels, descriptions, P31 and P1343.
- **Phase 2** (`genealogy/ono_quickstatements_phase2.txt`): the family
  statements. QuickStatements can only refer back to the *last* item it
  created, so phase 2 uses placeholders like `{ono:6}` that have to be filled
  with the QIDs phase 1 produced.

The draft follows option 1 above (no parent statements on Kobito or
Shikobuchi) until the user decides otherwise.

## Caution for phase 2

Some links between items that already exist are already on Wikidata from
other sources, for example Futodama P22 Takamimusubi and Futodama P40 Ame no
Kushimimi (see `wikidata-survey.md`). QuickStatements would add a **second,
"disputed" copy** next to the existing claim. For those, add only the
honkeichō as an extra *reference* on the existing claim, without the disputed
qualifier, or skip them. Lines where both sides already have QIDs are the
ones to check by hand before running.
