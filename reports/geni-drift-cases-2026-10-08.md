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
- **`Q141610297` Antoine de Constant.** FamilySearch `K4YV-M5N` is Augustin Constant (1542-1593), whose father is
  Antoine Constant, and the item's own father link is Antoine Constant. Either the item is Augustin labelled with his
  father's name, or it is Antoine and the walk paired the son. Needs the item's other statements read.

## Part B: the 39 not covered by Part A

Not written yet: the 12 walk-paired items whose FamilySearch id is not the walk's, and the 27 the walk never touched
(the alternating Bjørgås, Bjørgo and Mestad groups among them).
