# Geni drift: the cases, in plain words (2026-10-08)

For the queue item on items whose Geni profile "turned into another person". Emma, 2026-10-05: a versioning problem,
and FamilySearch decides. The data behind each case: `reports/geni-drift-versions-2026-10-08.csv` (what the Geni id
named in each day's tree), `reports/geni-drift-familysearch-2026-10-08.csv` (the item's FamilySearch id and that person
in our downloads), `reports/geni-drift-walk-2026-10-08.csv` (the positional walk's pairing), and
`reports/geni-drift-history-2026-10-08.csv` (the item's live edit history). The verdicts are the session's.

## Part A: the 19 items that carry the positional walk's FamilySearch pick

For each of these the walk paired the item's Geni profile with a FamilySearch person, rendered that person onto the
Geni id, and our batches then wrote that person's FamilySearch id (`P2889`, on 2026-10-02, off the same day, back on
2026-10-04) and often their name pieces onto the item. So the "new person" came from the walk, not from Geni.

### Wrong: the walk put another person on the item (5)

- **`Q141532596` Berit Rasmusdatter Høyland.** Created 2026-09-22 as Berit. The walk paired her with FamilySearch
  `G2T9-19V` Elen Svensdatter Fosse (born 1660) in a spouse slot, on the birth year alone ("born 1660 vs 1660"). Since
  then the item gained Elen's name as an alias (09-24), Elen's patronymic Svensdatter (09-30), Elen's FamilySearch id
  and display name (10-04). Different given name, different patronymic, different farm: two women. Belongs off the item:
  `P2889` `G2T9-19V`, the `P5056` Svensdatter, the alias "Elen Svensdatter Fosse".
- **`Q141538482` Kierstin Slut.** The walk paired her, in a *mother* slot, with FamilySearch `L63V-WW2` Mårten
  Andersson (born 1570), a man, on shared name tokens. The item gained his FamilySearch id (10-02, 10-04) and the
  patronymic Andersson (10-02). Belongs off: `P2889` `L63V-WW2`, `P5056` Andersson.
- **`Q141422290` Nils, father of Per Nilsson.** The walk paired him with FamilySearch `L6RL-W5T` Isak Abrahamsson
  (1569-1598) in a father slot, on the birth year alone. The item gained Isak's FamilySearch id and Isak's patronymic
  Abrahamsson (10-02). A father named Nils is what "Per Nilsson" requires; Isak is someone else. Belongs off: `P2889`
  `L6RL-W5T`, `P5056` Abrahamsson.
- **`Q141217433` Per Persson Hagman.** Created 2026-08-29; his own FamilySearch id `PNMB-CPN` came on 09-22. The walk
  paired his Geni id with `LRP6-5H5` Daniel Pehrsson (born 1750), a child slot, on the names "daniel, pehrsson". Both
  are sons of Per (Pehr) Andersson Storskytt, so these are brothers. The item gained the alias "Daniel Pehrsson"
  (10-03). Also on 10-03 another editor, Anvilaquarius, merged `Q141584329` into this item: that was our own
  duplicate of the same man ("Pehr Pehrsson Hagman", born 24 Sep 1754 like Per, Geni `6000000227891680354`), so the merge
  is right, but it carried that item's FamilySearch id `LRP6-5H5`, which is the walk's pick, Daniel. The item now holds
  `P2889` `PNMB-CPN` (his) and `LRP6-5H5` (Daniel's). Belongs off: `P2889` `LRP6-5H5`, the alias "Daniel Pehrsson", and the
  `P1810` "Daniel Pehrsson" display name.
- **`Q141570661` Marit Svalesdatter Skas.** Created 2026-09-26 as Marit. The walk paired her in a spouse slot with
  FamilySearch `GXSB-Q57` Domild Svensdatter (1555-1670) on the birth year alone. Different given name (Marit,
  Domild) and different father (Svale, Sven). The item gained Domild's FamilySearch id (10-03). Belongs off: `P2889`
  `GXSB-Q57`.

### Right: the walk found the same person (12)

- **`Q141492819` Marite Bergesdatter Talgje** = FamilySearch `LHKZ-6D5` Marite Bergesdatter (1552). The Geni name only
  moved between Talgje and no farm name.
- **`Q141516727` Elen Salvesdotter Ims** = `L4B9-DGL` Eli Salvesdatter Frøyland (1568-1614), father Salve Hallvardsen
  Frøyland on both sides. Eli and Elen are one name; Ims and Frøyland are farms.
- **`Q141562986` Siur Torkelsen Berge** = `LH3T-ZCT` Sigvard, father Torkel on both sides. Sjur (Siur) and Sigvard are
  one name on Geni.
- **`Q141581295` Nils Fanuelsen Åreskjold** = `KLXW-RJC` Nils Fanuelsen Åreskjold (born 1714); the other Geni form,
  Njell Fanuelson Auglend, is the same man (Njell is a form of Nils, father Fanuel).
- **`Q141560301` Mrs Ole Jaatun** = `KJ5C-L8H`, a mother recorded on FamilySearch only by her husband's name, Ole
  Jåtun. Both sides name her only through him (the unnamed-against-named principle).
- **`Q141566137` Riskadatter** = `PSCX-B5N` Berthe Jacobsdr (born 1505). "Riskadatter" reads as "the daughter from
  Riska" (a farm), not a patronymic, so one side has her name and the other only an epithet.
- **The Güntersberg line, four items, renamed on one date (2026-09-24):** `Q141499675` Joachim = `G6HP-V83` Jakob,
  `Q141502702` Günther = `GBYR-856` Henning, `Q141510091` Heinrich = `GDBR-PKV` Voltekin Walter, `Q141511190`
  Burchard = `GBYR-F31` "von Güntersberg, Herr auf Grutkow …". The father links are unchanged and still match
  generation for generation (Henning's father is Voltekin Walter, whose father is the Herr auf Grutkow), so each item
  is still the same position in the line; Geni renamed the whole line and FamilySearch has the new names. The items'
  labels are the old names.
- **The Eickstedt pair, renamed 2026-09-24:** `Q141517168` Tidericus = `LVGN-3RW` Friedrich von Eickstedt V,
  `Q141523508` Theodericus II = `LVGN-3YS` Dietrich von Eickstedt III, the father link matching.

### Not settled (2)

- **`Q141562977` Siri Madland.** Paired in a mother slot with FamilySearch `PHY3-2V4` "Sigmund Madland" (born 1534) on
  the year. Sigmund is a man's name in a mother slot: probably the same woman under a garbled FamilySearch name, but
  not certain.
- **`Q141610297` Antoine de Constant.** Settled 2026-10-08: the item is Antoine (about 1500 Geneva - 1547 Lausanne), son
  of Antoine Constant (1475-1548); FamilySearch `K4YV-M5N` is his son Augustin Constant (1542-1593), a generation later,
  reached by the walk through a grandchild FamilySearch places under Augustin and Geni under Antoine. `K4YV-M5N` and the
  alias "Augustin Constant" were removed (checked live).

## Part B: the other 39

### Created from an earlier walk run, then given the Geni person on top (16)

These 16 Geni ids are not in the walk's current pairs, but every earlier run under its old name (the zipper,
`reports/familysearch-zipper-pairs.tsv`, 2026-09-24 to 2026-10-01) paired each with a FamilySearch person by slot
position alone ("solo, position"), and stopped on 2026-10-02. Those are exactly the dates the names flip in the tree's
history. The items were created during that window, so each was created AS the FamilySearch person, under the Geni id
of somebody else; once the pairing dropped, the Geni export's own person came back and our batches appended that
person's name as an alias and their patronymic as a second `P5056`. FamilySearch and the item's creation agree on who
the item is; the Geni id is the other person's.

- `Q141562866` Oleiv Samuelsen (FamilySearch `LDYY-JT9`); the Geni id is Mogens Olson Bjørgås: alias "Mogens Olson
  Bjørgås", "Mogens Bjørgås" and `P5056` Olson appended.
- `Q141559631` Halvor Oleivsen (`K84M-FXV`, father Oleiv Samuelsen, as on the item); Geni: Tormod Monsson Bjørgås
  (alias, `P5056` Monsson).
- `Q141558357` Barbro Olsdatter (`L4P9-YSY`, father Ole Eriksen, as on the item); Geni: Marita Larsdotter Bjørgås
  (alias, `P5056` Larsdotter).
- `Q141562856` Ole Eriksen (`L4P9-BXD`); Geni: Lars Larsson (alias, `P5056` Larsson).
- `Q141562358` Guri Vilhelmsdatter (`L6PH-S6D`); Geni: Kari Bjørgås (alias).
- `Q141562826` Ola Mekkelson (`MNC3-4CC`); Geni: Hallvard Gulleikson Bjørgås (aliases).
- `Q141565565` Jon Herbrandsen (`KCHF-HMZ`); Geni: Knut Sjurson Bjørgo (alias, `P5056` Sjurson).
- `Q141565713` Margit Larsdatter (`GMZM-RBY`); Geni: Elisabet Olsdatter Bjørgo (alias, `P5056` Olsdatter).
- `Q141564600` Andres Ottarsen (`L2H4-8S4`); Geni: Knut Knutsen Mestad (alias, `P5056` Knutsen; the item's father
  link is Knut Mestad, the Geni side's).
- `Q141565147` Gietrud Torstensdatter (`L7LN-RSZ`, father Torsten Tolleivsen, as on the item); Geni: Guri
  Knutsdatter Mestad (alias, `P5056` Knutsdatter).
- `Q141560557` Ole Tollefsen Storla (`LCRT-MN6`, father Tollef Olsen, as on the item); Geni: Berge Toresen Brunborg
  (aliases, `P5056` Toresen).
- `Q141569620` Giertrud Ivarsdatter; Geni: Ambjørg Johannesdatter (alias, `P5056` Johannesdatter). No FamilySearch id
  on the item.
- `Q141571165` Torsten Tolleivsen; Geni: Knut Toresson Hærum (alias, `P5056` Toresson). No FamilySearch id on the item.
- `Q141487959` Kari Oddsdatter Foss: Geni only moves her between the farms Foss and Hauge; the same woman. No harm.
- `Q141579565` Peder Bat (`9K6F-FYR`); Geni: Karl Bååt (alias). Different given name.
- `Q141611085` Roe (`9VM1-4Y9`, "Roe Bishop of Farogane"); Geni: Hroy. Roe and Hroy are one name; the same man.

### Walk-paired, the walk's FamilySearch id since removed or never applied (12)

On 2026-10-07 the FamilySearch-id review took several of these ids off. What the walk left behind:
- **Wrong, residue left:** `Q141532548` Barbro Hersesdotter (father Herse, so the item is right) still carries the
  walk's Malin Olofsdotter as alias and `P5056` Olofsdotter; `Q141533731` Nils Olofsson (father Olof Filipsson) still
  carries `P5056` Nilsson from the walk's Olof Nilsson Albrektsson; `Q141549731` Stefan Olofsson still carries `P5056`
  Nilsson (added 2026-10-06) from the walk's Anders Nilsson; `Q141528244` Elin Nilsdotter carries the alias "Anna
  Nilsdotter" from a mother-slot pairing on the birth year alone.
- **Wrong, nothing left behind:** `Q141538883` Olof Filipsson (the walk's Nils Albrektsson, on a birth year; id removed).
- **Settled 2026-10-08:** `Q141538789` Mariet Jönsdotter (wife of Herse Andersson Bure): her parents Nils Hansson and Kålug
  Larsdotter are Geni's own (our tree gives the same), so they stay; the walk's residue was the given names Sigrid and Sara
  and the patronymic Nilsdotter (added 2026-10-01), removed and checked live. Jönsdotter against a father Nils is a Geni-side
  mismatch for after 2026-10-21.
- **Not settled:** `Q141515038` Hallgrim
  Oxehode, whose father link is Bratt Oxehode, which fits the walk's Aslak Brattson better than Hallgrim.
  `Q141382445` / `Q141382447` Niklas Olsson and Stina Larsdotter, whose merge history (2026-09-09 and 09-23) has to be
  read first.
- **Same person or harmless:** `Q141515084` Heinrich = Jakub Kaszuba von Güntersberg (the renamed line);
  `Q141551485` Tjærand Olson Goa (id removed, aliases his own); `Q141574824` Marita Gunnarsdatter Nordland (id removed;
  `P5056` Gunnarsen fits her father Gunnar).

### Not walk-related (11)

The same person under another form of the name, so not drift: `Q135268178` Lars = Laurentius Lang; `Q141499439`
Álfheiði = Alvhild Tumesdatter; `Q141523034` Els Pfinzing = Elisabeth Isolt; `Q141529028` Markward = Merklin Pfinzing;
`Q141526129` Tollak Reiarson/Reiersen Kydland; `Q141571108` Soffi Massdatter = Sophie Madsdatter (father Mass/Mads);
`Q141583399` Ulrika Fredrika Braun = Fredrika Ulrika von Nolcken (married and birth name); `Q141584552` "Traung" =
Johanna Sandelin; `Q141585911` Ole Nag = Olav Persen Nag; `Q141498427` Signe Maria Wedberg/Gustavsson, whose live
label is the bare surname "Gustavsson" (a label error to fix). Not settled: `Q141517162` Elisabeth Margaretha Rahm /
Margareta Elisabet Brunlöf (no FamilySearch id, no parents on the item).

## The whole picture

47 of the 58 trace to the positional walk (31 in its current pairs, 16 in its earlier zipper runs); the Geni profiles
themselves did not change person in those. The two lines renamed on Geni (Güntersberg, Eickstedt) are the real Geni
changes, and FamilySearch agrees with Geni's new names there.

## Round 2 (2026-10-08, after Emma: "do more analysis for the three unsettled cases ... and fix these things")

**Correction to Part A.** The Güntersberg and Eickstedt items were listed above as "the same person, renamed on Geni".
That was wrong. On Geni the Güntersberg items are 15th-16th-century men (died about 1531, 1433, 1419), and the
FamilySearch people the walk gave them are 13th-century (Herr auf Grutkow about 1240, Voltekin Walter about 1260, Henning
about 1300): paired on "von Güntersberg" plus one shared given name, two centuries apart. The Eickstedt pair was paired
one generation down (our Theodericus II, 1185-1249, got FamilySearch's Dietrich III, the son of Theodoricus II; our
Tidericus got Dietrich III's son Friedrich V). Geni renamed nobody; the "new names" were the walk's renders. The old
labels are right. The walk's FamilySearch ids (5) and aliases (4) came off. Likely, not acted on: our Tidericus
(Dietrich, son of Theodericus II) is FamilySearch's Dietrich III `LVGN-3YS`.

- **`Q141562977` Siri Madland: the same woman.** Female in both our tree and FamilySearch `PHY3-2V4`, born about 1534, wife of
  Sigmund Madland I, mother of Ola Sigmundsen Madland. FamilySearch (and Geni's latest version) record her under her
  husband's name, "Sigmund Madland" (a "Mrs Sigmund" whose "Mrs" was lost); Siri is her own name from Geni's earlier
  versions. The FamilySearch id stays; the family name "Sigmund" (her husband's given name, added 2026-09-28) came off.
- **`Q141515038` Hallgrim Oxehode: the item is Hallgrim.** His son on the item is Torstein Halgrimsen ("son of Hallgrim");
  Geni's own versions name the profile Hallgrim Oxehode, then Hallgrim Grisen. "Aslak Brattson Oxehode" is the walk's
  FamilySearch `GSVR-494`, another son of Bratt (born about 1300, no children). The walk's given name Aslak (added
  2026-10-02) came off; its FamilySearch id had already gone on 2026-10-07.
- **`Q141382445` Niklas Olsson and `Q141382447` Stina Larsdotter: both right.** Two brothers, sons of Olof Svensson and Stina
  Nilsdotter: Niklas (1827-1909, wife Stina Larsdotter 1828-1910, son Anders Petter Nilsson) and Anders Gustaf
  (1824-1875, wife Anna Brita Andersdotter 1821-1914). The walk rendered Anders Gustaf's name and children onto Niklas's
  Geni profile, which is why our tree shows "Anders Gustaf Olsson" with Niklas's dates. The 2026-09-09 merge in their
  history was undone. The family name "Andersson" (added to both on 2026-10-06, the brother's family's) came off.
- **`Q141564600` Andres Ottarsen:** his father link to Knut Mestad (the Geni person Knut Knutsen Mestad's father) came off,
  and the reverse link on Knut Mestad.

All 12 statements (QuickStatements, new tab) and 4 aliases (`wbsetaliases`) checked live: gone. All in
`reports/removed-statements.tsv`.
