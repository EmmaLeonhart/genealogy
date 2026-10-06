# Pipeline audit, 2026-10-06: are the errors of 2026-10-03 and 2026-10-04 solved?

Queue item (Emma, 2026-10-04: "a very important thing to do a thorough audit"). Every pipeline change made for an
error reported or found on those two days, each checked against what the pipeline produces now, never assumed from
the commit. Output audited: the batch `fb299cd39` (`reports/wikidata-garborg-day-manual.txt` / `-auto.txt`, rebuilt
2026-10-06 08:19 UTC), the synoptic tree `a984c3e10` (rebuilt 2026-10-04 18:36 UTC; `derived-*.csv` unpacked from the
committed gzips for this audit, the local copies were the 10-03 tree), and Wikidata read live on 2026-10-06.

Verdicts: **SOLVED** (checked in the output), **NOT SOLVED** (the error is still produced), **PARTLY** (say which part).

## 1. Impossible extra parents from spliced saved-path files (2026-10-03) — SOLVED

Error: 200 harvested path files hold a second chain after their target, and the first row of that chain was read
against the target (Ulla Celsing as Bogislaw II's mother, Immanuel Bang as Jelena of Hungary's father, four modern
men as Izyaslav II's spouses); 14 false statements reached Wikidata. Fixes: `build-tiny-gedcoms.py` ends a harvested
chain at its target (`:626-634`, present); the spliced links left the tree at the rebuild; the 14 were removed.
Checked:
- All 200 junction pairs (target, first row after it, `reports/spliced-path-files.csv`) against the current
  `derived-family.csv`: 197 have no link. The other 3 are linked the other way round from the splice and are real:
  Miguel Gallo Vergara is the father of Pedro León and Ángel Custodio Gallo Goyenechea, Mercedes Vergara Santelices
  the mother of Marcos Gallo Vergara (the splice would have made them the children).
- Jelena of Hungary `6000000006727871963`: father `6000000003858579100`, no Bang; Bogislaw II `6000000002188021178`:
  mother `6000000008248664316`, no Celsing.
- The 14 statements of `reports/wikidata-splice-removals.qs`: none in the current batch files, none live.

## 2. Tore of Steig as King Haakon's birth father; foster and adoptive parents (2026-10-03) — SOLVED

Error: the slim dropped `PEDI`, so a foster father went out as a birth father. Fix: `qualify_non_birth_parents`
(`build-garborg-day.py:2054`, called as the last pass at `:10643`) puts `P1039` foster/adoptive father/mother on every
`P22`/`P25` whose pair is foster or adoptive in `derived-pedigree.csv` (1,505 such rows in the current tree).
Checked:
- `Q1752172` Haakon live: `P22` `Q6149119` with `P1039` `Q20747105` (foster father), `P25` `Q141624579` with
  `Q20747106` (foster mother); his birth parents `Q343088`/`Q141624426` bare.
- Every `P22`/`P25` in the current batch files, mapped to Geni ids (`garborg-qids.tsv`, `p2600-all.tsv`): 39 between
  two existing items and 183 inside creations; none names a foster or adoptive pair without `P1039`. The batch uses the
  qualifier once (`Q141585487` `P25` `Q141654066` adoptive mother).

## 3. A private person linked to one person is not created, recursively (2026-10-03) — SOLVED

Fix: `lonely_private_people()` (`build-garborg-day.py:491`, applied at `:8047`). Checked: on the current tree it
removes 51,031 private people; none of the 180 Geni-id creations in the manual batch or the 30 in the auto batch is
one of them.

## 4. Puyi's ring starved by the cap's sort order (2026-10-03) — SOLVED, and the lines are now held elsewhere

Error: the 500-a-run cap kept the 500 lowest Geni ids as text, so Puyi's 13 frontier people never reached a batch.
Fix: `priority_ancestor_ring` (`:1256`) interleaves the seeds' frontiers. Checked on the current tree, ancestors without
an item: Puyi 598 -> 580, Naruhito 2,483 -> 2,280, Yi Ku 1,430 -> 1,290 since 2026-10-03, and each frontier (ancestors
without an item whose child has one) is now small: Puyi 16, Naruhito 18, Yi Ku 2. None of them is in the current
batch, for reasons that are not the cap: 11 are Han-only (no Latin label, so not created, the 2026-10-04 guard);
Yehe Nara, Uya and Alute are clan names alone (a surname-only person is not created from a romanisation, 2026-10-03);
and the rest checked live (10 of 19 before the API rate-limited) have no item carrying their Geni id but are famous
people with established items (the Qianlong Emperor, Prince Chun I huwan, Michiko Shōda, Empress Shōken), which must
be joined by identification, never created. **Unexpected:** so the three seed lines are
now waiting on identifying a handful of established items, which no part of the pipeline does by itself.

## 5. NN people created plain; relational labels a day later (2026-10-03) — PARTLY

Error: NN creations carried `ja`/`zh`/`ko` relationship phrases at creation. Fixes: creations plain; a day-after pass
(`build-garborg-day.py:~9120`, `LATER_RELATIONAL_CAP` 200) writes the relational label in en/ja/zh/ko.
- **Creation half: SOLVED.** The 11 NN creations in the manual batch and 1 in the auto batch are `NN …` in `mul` and
  `en` with no relational label in any language.
- **Day-after half: NOT SOLVED in what reaches Wikidata.** The pass runs (pipeline logs 2026-10-06 04:08 and 06:20 UTC:
  "relational labels a day after creation: 200 NN item(s)"), but none of its lines is in the current batch files (341
  label lines on existing items, none relational): `_cap_label_edits` drops every `(qid, slot, value)` already in
  `reports/label-edits-emitted.tsv`, and a value is recorded there when it is written into a batch, not when it lands.
  Of the 283 NN items of ours whose live `en` is still `NN …` or empty (`garborg-live-labels.tsv`, 2026-10-06 01:24
  PDT), 50 have an `en` relational label recorded as emitted and not live, so the pass will never send it again
  (e.g. `Q141632172` "wife of Öde stamfar Örnfot", `Q141628357` "daughter of Merfyn ap Rhodri Mawr"). One of the 50,
  `Q141523636`, is Emma's own removal (2026-10-04) and rightly stays. The same mechanism applies to every capped
  label edit, not only NN ones.

## 6. The CBDB id as an exact join; the zero-padding fix (2026-10-03) — SOLVED

Error: a ring creation could duplicate an established CBDB item that carries no Geni id. Fixes: `slim.harvest_cbdb`
writes `reports/derived-cbdb.csv` (8,605 Geni profiles with a CBDB id in the current tree); `--p497` writes
`out/wikidata/p497-all.tsv`; `cbdb_identifications()` joins them, leading zeros dropped. Checked: of the 180 Geni-id
creations in the manual batch and 30 in the auto batch, none has a CBDB id at all, so none can duplicate a CBDB item.

## 7. A surname links to an existing item only by its English label and "family name" (2026-10-03) — SOLVED

Error: `Tu`, a Norwegian farm name, matched `Q709747` 杜 through a label in another language. Fix:
`namemodel.family_item_fits`. Checked live: all 94 distinct `P734` targets in the current batch files (besides the
novalue placeholder) have the `en` description exactly "family name". Of the 71 `P734` links inside creations, 55
target an item whose `en` label is in the person's label; the other 16 are married names qualified `P3831`
`Q28418670` (the label carries the birth name, 2026-10-01) or, in one case, a second farm name from Geni's alias
(Gunnar Torsteinson Eia, alias "… Bjelland"). None is a cross-language match.

## 8. `P2976` on the given names, the reverse of each patronymic's `P144` (2026-10-03) — PARTLY

Fix: `build-garborg-name-items.py:1015-1022` writes `<given name> P2976 LAST` beside every `LAST P144 <given name>`, and
a backfill for existing pairs. Checked: the current batch files carry 90 `P2976` lines; of the 60 `P144` values on
patronymic items created there, 54 have the reverse and 6 do not, all pointing at two given names, `Q123820137` Jons
and `Q19869349` Pär (both live given-name items). The generator writes the reverse for every `P144`, so these were
dropped later in the batch assembly; the cause is not established here (NEEDS-INVESTIGATION: which gate refuses an
edit on those two items).

## 9. A given name with no surname is the name alone, not `Given NN` (NN ruling 2, 2026-10-03) — SOLVED

Fix: `labels.name_with_unknown_surname` no longer appends `NN`; the creation path drops a trailing `NN`; 379 items
backfilled. Checked: no creation in the current batch files is labelled `<given> NN`. 17 items of ours still have a
`Given NN` `mul` live (`garborg-live-labels.tsv`); the backfill's own record says 16 CJK slots and 5 names were left
because the labels there did not look like ours, so these are not a fresh output of the pipeline.

## 10. No family name = `Q108474139` for patronymic names (2026-10-04) — SOLVED, with one edge and a stale test

Fix: `NO_FAMILY_NAME` (`build-garborg-day.py:228`, emitted at `:9788`) when Geni's fields give a patronymic and no
family token. Checked on the current batch files: 79 creations have a patronymic; 7 carry `P734 Q108474139`, 39 a
real `P734`, 33 none. Of the 33, all but 4 have a family name in their label whose item does not exist yet (correct:
they have a family name). Of the 4: Bengt Jönsson Jönsson is the doubled-patronymic defect (queued); Benjamin
Svensson and Märta Gustafsdotter have married surnames in Geni's `marnm` (Humla, Kafle), so they do have a family
name and the placeholder rightly stays off; Markus Tomasson has no surname and the patronymic `Tomasson` in Geni's
married-name field, which counts as a family token (one edge case). CI: `test_the_no_family_name_placeholder_is_
the_item_emma_named` fails because it passes `Fernando Gundemárez` with no father, which the 2026-09-25 rule (a
patronymic requires the father) reads as a family name; the test is stale, not the output. `test_every_qid_the_
batch_points_at_already_exists` fails on `Q108474139` and `Q8201` (Chinese characters), both live items its vocabulary
does not list; also stale.

## 11. Error report `Q141633473` "Peder"; three hand fixes overwritten by a running batch (2026-10-04) — SOLVED

Fix: `namemodel.keep_own_surname` keeps a single-patronymic `_MARNM` tail when SURN is empty; Emma's values restored by
hand. Checked live: `Q141633473` "Peder Samuelsson" and `Q141560190` "Marit Rasmusdotter Tu" in `mul`/`en` (Emma's
values). The current batch files have no label line on either, or on `Q141628094`. The overwrite itself came from a
batch composed before her fix; the guard against that is the run-as-soon-as-it-lands rule and the pre-run live check
(`hold-live-creations.py` covers creations only, not label edits on existing items, so a stale batch can still carry a
label edit that a later hand fix supersedes; none does in this batch).

## 12. Error report `Q141610242`, Hebrew in the English label (2026-10-04) — SOLVED

Fix: a label correction never puts a non-Latin name over a Latin label (`is_latin_text`); `describe_all` no longer
leads a Latin phrase with a non-Latin given name. Checked live: `Q141610242` "Abigail Ogla Yaffe", `Q141585621`,
`Q141585629`, `Q141610308` Latin in `mul`/`en`; `Q141198548` `en` "wife of Buyeo Deokjang". The current batch files
carry no `mul`/`en` label in a script other than Latin or CJK.

## 13. Error report `Q141632229` "Luthard NN" (2026-10-04) — SOLVED (one item, handled as that item)

Checked live: `mul`/`en` "Luthard von Kleve". The current batch has a `P26` on him and no label line.

## 14. The particle "No" read as a given name; `no name` not seen as a marker (2026-10-04) — SOLVED in the generator

Fix: `namemodel.name_shape` reads lower-case `no` as a particle (and the 2026-10-06 decision models no Sinosphere
name at all). Checked: the current batch files have no `P735 Q21148356` ("No"), no `P735 Q116367185` ("Name") and no
label containing `no name`. The live statements were removed on 2026-10-06 (22-statement fix batch).

## 15. Guy I d'Aumelas: the ordinal lost in the `_MARNM` label rebuild (2026-10-04) — PARTLY

- **Generator: SOLVED.** No creation in the current batch files has a Roman numeral in Geni's `GIVN`
  (`display-names.csv`) that its label lacks.
- **The 8 relabels: NOT SOLVED.** All 8 queued in `label-applications.tsv` on 2026-10-04 (`Q141632439` Guy I
  d'Aumelas, `Q141634198`, `Q141636829`, `Q141621983`, `Q141624597`, `Q141633890`, `Q141632723`, `Q141583421`) are still
  live without the ordinal (read 2026-10-06), and none is in the current batch. `reports/label-edits-emitted.tsv`
  records their values as emitted on 2026-10-04: they went into a batch whose label lines did not run (the session's
  batch tab ended when Chrome was killed that day), and `_cap_label_edits` drops anything already recorded as emitted,
  so they will never be sent again while their rows sit in `label-applications.tsv` unretired. Same mechanism as
  error 5. **It also holds for the 1,160 Sinosphere label applications written 2026-10-06:** each gets one emission.

## 16. A created item turns into a different person when its Geni profile does (2026-10-04) — NOT SOLVED (no fix made)

No pipeline change was made: the 155 drift candidates (`reports/geni-identity-drift.csv`) were listed and queued, and
whether Geni renamed or merged cannot be read until Geni contact resumes (2026-10-21). The pipeline still follows the
Geni id, so an item whose profile now carries another person keeps receiving that person's statements. The queue
item "Items that turned into another person with their Geni profile" holds it.

## 17. Han-named creations duplicated 58 people; no Latin label, no creation; no creation without `en` (2026-10-04) — PARTLY

Error: Han-named people were created with `mul`/`ja`/`zh` and an `en` description only, so no language held both a
label and the description and Wikidata could not refuse the overlapping run's repeats (58 duplicate pairs).
Fixes: a Sinosphere person with no Latin record is not created; every person `CREATE` must reach `LAST Len`; `en`
readings for the 193 (and NN rows), 221 rows in `label-applications.tsv`.
- **Creation guard: SOLVED.** All 216 person creations in the current batch files have a Latin `Len` and a `Den`, so
  the label-plus-description refusal can fire again.
- **The `en` backfill: NOT SOLVED.** All 221 `en` rows of 2026-10-04 are recorded as emitted in
  `label-edits-emitted.tsv` and none is live (`garborg-live-labels.tsv`, 2026-10-06 01:24 PDT): the error-5 mechanism.
  The items created 2026-10-04 without `en` still have none, so their duplicate guard is still missing.
- Related, found today and queued as a generator defect: a lean rebuild snapshots while the previous batch is still
  creating, so already-live people come back in the next batch (64 held out of `fb299cd39` by hand,
  `hold-live-creations.py`). With every creation carrying `en` + description, Wikidata refuses them, but the guard
  is still Wikidata's refusal, not the pipeline's.

## 18. Men sent as mothers (Infovarius, 2026-10-04) — SOLVED in the composer

Error: a parent outside the batch's ids had sex "" and was filed as a mother (116 created items with a male `P25`);
separately, background QuickStatements runs chained `LAST` (a run rule, not the batch file). Fix: sex read for
everyone, then from the parent item's `P21`; unknown sex is neither. Checked: all 222 `P22`/`P25` lines in the current
batch files name a parent whose sex agrees (46 from `out/wikidata/sex.tsv`, the other 144 parents read live: every one
has a `P21` and none contradicts).

## 19. The automatic zipper taken out of the pipeline (2026-10-04) — SOLVED

Cuts, all present: `tree.yml` no longer runs `zipper-join.py`; `build-garborg-day.py:8094-8102` (and `:8010`) ignore a
correspondence row whose only sources are `zipper`/`structural`; `render-familysearch-gedcom.load_bridge` no longer
reads walked pairs unless an audit passes them; `build-id-backfill.py` and `build-familysearch-day.py` no longer read
them. Checked: 48,058 items are known only through inferred correspondence rows; none of the 489 items the current
batch files link creations to is one of them.

## 20. The bridge's feedback loop (2026-10-04) — SOLVED

Fix: `bridge-familysearch-qids.py:58` skips every id statement listed in `reports/id-claims-added-since-2026-09-28.tsv`
until reviewed. Checked: none of the 75,023 rows of the committed `familysearch-qid-bridge.tsv` rests on a listed
`P2889` claim.

## Entries of those two days with no pipeline change to audit

Decisions, investigations, hand fixes on Wikidata or principles; listed so none is skipped silently:
extra-parent drop (covered in 1); "pause FamilySearch importing" closed; the owner's ancestry GEDCOM script and its
re-emission (local reports); queue items gone back over; GZWDer's duplicate parent items (traced); Puyi/Naruhito/Yi Ku
as seeds (covered in 4); the ancestor deck counts, frontier and answers (decks retired 2026-10-04); label composition
item and "labels built from name objects" (live since 2026-10-02/03, not an error); CI fixes of 10-03 (see CI below);
Petrus Olai Gestricius merged; super entry points (separate queue item); Sinosphere creations under their Han name,
Han-surname-only carry, the held batches `b951ca695`/`295e94730`, the Sinosphere emergency fix and Emma's ten
screenshot items (all superseded by 17 and by the 2026-10-06 overrides); label fixes from the session's own
QuickStatements and Ryogu/Asukabe (hand data fixes); notable descents, Tang/Uyghur route, Helena (research); ancient
ring deck, FamilySearch-only ancient SAME, no Roman entry points (decisions); the NN interview and ruling (1)/(3)
(covered in 5); the -ez audit (no change); the 13 Spanish patronymics (hand fix, checked live that day); GEDCOMs of
09-30..10-03 (tidying); FamilySearch parent deck (nothing new); titles in `mul` aliases (analysis only); Emperor Ninken
merge; zipper-only links on Wikidata and the second cut (reports); patronymic audit and its fix batch (hand, checked
live 2026-10-04); identity-drift candidates (16); Sinosphere name statements sized (fixed 2026-10-06); Chrome killed;
the Kōkō duplicates and the 56 merges (hand); the Infovarius fix batch, its 227 wrongly removed links and their revert
(session errors on Wikidata, each checked live at the time); no decks, identities case by case, wrong ids removed as
judged, disputed parentage, Niklas Olsson (principles); scratch moved into the repo.

## Other findings of this audit

- **CI is red and has been since 2026-10-03 19:08 UTC** (last green `1020bf03c`, 2026-10-03 11:46 UTC). The latest
  run (2026-10-05, `303aaaf58`) has 7 failures: two are stale tests about the novalue placeholder (10 above), one
  expects a hand label row that has retired (`Q140568870` `ja`), one an inventory not regenerated
  (`built-batches.tsv`), one a repeated line in a hand fix batch, one a path file with a step lacking a Geni id
  (`emma-to-yuri-dolgorukiy.tsv`), and `test_the_father_name_reaches_statements_for_and_changes_the_property` (the
  patronymic-requires-father rule; not settled here). A fresh run on the current `main` was dispatched 2026-10-06
  (run 37437730721).
- **Decomposed Unicode in the batch.** 52 lines of the current batch files are not in NFC, 14 of them labels
  (`Märta`, `Bråstein`, `Ådnesdotter`): Wikidata stores NFC, so the live label is right, but every comparison the
  pipeline makes between its own text and live text fails on these, which can make it treat an existing name item as
  missing.
- **Pushes cancel pipeline runs.** Five pipeline runs were cancelled on 2026-10-06 by this session's pushes (a push
  supersedes the pending run), as CLAUDE.md warns.

## Summary

| # | error | verdict |
|---|---|---|
| 1 | spliced path files, impossible extra parents, 14 false statements | SOLVED |
| 2 | foster/adoptive parents as birth parents | SOLVED |
| 3 | lonely private people created | SOLVED |
| 4 | Puyi's ring starved by the cap's sort order | SOLVED (lines now wait on identifying established items) |
| 5 | NN relational labels at creation / a day later | PARTLY: creation solved; day-after labels never land |
| 6 | CBDB id join | SOLVED |
| 7 | surname linked through another language's label | SOLVED |
| 8 | `P2976` reverse links | PARTLY: 6 of 60 dropped in assembly |
| 9 | `Given NN` labels | SOLVED |
| 10 | novalue family name for patronymic names | SOLVED (one edge; stale CI test) |
| 11 | "Peder" / hand fixes overwritten | SOLVED |
| 12 | Hebrew in the English label | SOLVED |
| 13 | "Luthard NN" | SOLVED |
| 14 | particle "No", `no name` | SOLVED |
| 15 | lost regnal ordinal | PARTLY: generator solved; 8 relabels never land |
| 16 | created item drifts with its Geni profile | NOT SOLVED (no fix made; queued, waits on Geni) |
| 17 | Han-named duplicates / no creation without `en` | PARTLY: guard solved; 221 `en` rows never land |
| 18 | men as mothers | SOLVED |
| 19 | automatic zipper | SOLVED |
| 20 | bridge feedback loop | SOLVED |

**The one cause behind every PARTLY on labels (5, 15, 17):** `_cap_label_edits` records a label edit in
`reports/label-edits-emitted.tsv` when it is written into a batch, and drops it from every later batch; a batch
whose label lines never run (held, stopped, a tab closed) loses those edits for good, while their
`label-applications.tsv` rows stay unretired because they never went live. Measured now: 221 `en` rows of 2026-10-04,
the 8 ordinal relabels, and 50 NN relational labels. The 1,160 Sinosphere overrides of 2026-10-06 are exposed to the
same thing.
