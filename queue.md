# Queue

Work top to bottom. Delete an item when it is done (record it in
`research/SUMMARY.md` "What changed").

0. Wikidata import plan, `research/notes/wikidata-import-plan.md`: how to
   model the Ono pedigree on Wikidata. Cover an item for the 斎部宿禰本系帳
   itself (with its NDL identifier); P22/P25/P40/P26 statements referenced with
   P248 stated in = that item plus page/image; qualifiers marking the claim as
   disputed (P1310 statement disputed by, with Kosugi's 1876 note) and its
   nature (P5102 / P1480); instance-of for invented people (legendary figure
   vs human); and whether existing items (Kobito, Shikobuchi, Futodama) should
   get these parent claims at all. Verify every P/Q id against Wikidata before
   writing it down. Then a QuickStatements draft for review (do not run).

1. Continue transcribing 安房国忌部家系 (NDL 2538213) into
   `genealogy/awa_inbe_kakei.csv`: images 3–19 are done (gods to 1102; rows 34+ have
   dates but parent links not yet resolved from the bracket layout). Next:
   images 20–75 (lower priority than 1b/1c), plus a check of image 10 and the
   image 14→15 page break (who is 久米麻呂's father?). Verify 色洞子 =
   忌部色夫知.
1c. Find what Hōga Toshio's 古代氏族系譜集成 (1986) gives for the Inbe, and
   whether FamilySearch's line matches it.
2. Find the Hōraku-ji gravestone inscription text for Chikazane (Echizen
   town 2011) and what it says about his name/parentage.
2b. Search for any generational chain from Futodama or Ame no Tomi down to a
   historical Inbe (Kogo Shūi, Shinsen Shōjiroku, Awa Inbe / Miki family
   records, Awa Shrine priests). This is the user's core question.
3. Check the Kogo Shūi and Shinsen Shōjiroku notes against critical editions
   (Iwanami Bunko / Saeki); Kojiki / Nihon Shoki mentions of Futodama and Inbe
   ancestors.
4. Historical individuals: list every named Inbe person found in the
   chronicles (Nihon Shoki, Shoku Nihongi and later), with dates, rank and any
   stated parentage, `research/notes/individuals.md`.
5. Branches: one note per branch (Awa, Sanuki, Kii, Izumo, Tsukushi/Ise,
   Bōsō Awa), covering origin claims, shrines, surviving families (e.g. the Miki
   family of Tokushima), `research/notes/branches.md`.
5a. Origin theories: started in `research/notes/origin-theories.md`
   (be organisation, Soga link, kabane). Still: the hemp/Awa archaeology, the
   Miki family, kin-group counter-theories, craft-guild theories.
5b. Nakatomi comparison: check the eonet transcription against the 群書類従
   中臣氏系図 text (NDL Digital 1879557 vol. 16?); confirm the 失傳 note.
6. Build `genealogy/people.csv` and `genealogy/links.csv` (source and
   confidence on every row), plus a script that writes `genealogy/inbe.ged`.
   Check that the GEDCOM loads (parse it back).
7. Write `research/SUMMARY.md` answering: how far back can any real Inbe
   person honestly be traced, and does Wikidata or FamilySearch get closer to
   the gods?
