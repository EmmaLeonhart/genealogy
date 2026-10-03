# Queue

Work top to bottom. Delete an item when it is done (record it in
`research/SUMMARY.md` "What changed").

1. Check the references on Wikidata's unusual Futodama parentage statements
   (Ame no Uzume and Kamo Taketsunumi as Futodama's children; Ame no Hiwashi
   as Tajikarao's son), add to `research/notes/wikidata-survey.md`.
2. Find the source behind FamilySearch's Inbe line (Hamanari → Chikazane):
   look for an Inbe/斎部 pedigree in Oda genealogies, Tsurugi Shrine records,
   Zoku Gunsho Ruijū / Keizu Sanyō. Check Hamanari–Hironari against the
   Shoku Nihongi / Nihon Kōki.
2b. Search for any generational chain from Futodama or Ame no Tomi down to a
   historical Inbe (Kogo Shūi, Shinsen Shōjiroku, Awa Inbe / Miki family
   records, Awa Shrine priests). This is the user's core question.
3. Primary-source notes: the Kogo Shūi (807) branch genealogy,
   `research/notes/kogo-shui.md`; Shinsen Shōjiroku (815) Inbe entries,
   `research/notes/shinsen-shojiroku.md`; Kojiki / Nihon Shoki mentions of
   Futodama and Inbe ancestors.
4. Historical individuals: list every named Inbe person found in the
   chronicles (Nihon Shoki, Shoku Nihongi and later), with dates, rank and any
   stated parentage, `research/notes/individuals.md`.
5. Branches: one note per branch (Awa, Sanuki, Kii, Izumo, Tsukushi/Ise,
   Bōsō Awa), covering origin claims, shrines, surviving families (e.g. the Miki
   family of Tokushima), `research/notes/branches.md`.
5a. Origin theories: what scholars propose the Inbe actually were
   (occupational be grouping vs kin group, immigrant/craft-guild theories,
   the Awa hemp connection, how the shared Futodama descent was assembled),
   `research/notes/origin-theories.md`.
5b. Nakatomi comparison: why the Nakatomi genealogy is so much better defined
   (Fujiwara-era lineage records such as the Ōnakatomi family register, the
   Sonpi Bunmyaku) and what that says about the Inbe gaps,
   `research/notes/nakatomi-comparison.md`.
6. Build `genealogy/people.csv` and `genealogy/links.csv` (source and
   confidence on every row), plus a script that writes `genealogy/inbe.ged`.
   Check that the GEDCOM loads (parse it back).
7. Write `research/SUMMARY.md` answering: how far back can any real Inbe
   person honestly be traced, and does Wikidata or FamilySearch get closer to
   the gods?
