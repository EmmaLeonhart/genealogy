# Queue

Work only. Take the first item in the queue and do it. When it is done, delete it and append a
dated `devlog.md` entry in the same commit. Bullets, never numbers. Nothing here is marked
priority: the order IS the priority, and a new item goes where it belongs in the order, not on
top with a banner. Rulings go in `CLAUDE.md`; history goes in `devlog.md`; everything else that is
not an action goes in `docs/queue-archive/`. The file this replaced, verbatim, is
`docs/queue-archive/queue-before-2026-09-24-rewrite.md`.

**Standing, not items:** no contact with geni.com until at least 2026-10-21, and only Emma lifts
it. Each session starts with
`CLAUDE.md` § *FIRST OF ALL, THE FAMILYSEARCH POSITIONAL WALK*.
**The noticeboard matter is over (Emma, 2026-10-19): "noticeboard is over we're back".** CI/CD is re-enabled by a
cron at 18:00 PDT that day; Emma is giving further instructions for starting again, so no batch run before them.
















- **CI red on the 2026-10-09 batch (run `39351835766`, 2026-10-19): 2 of 2,529 fail, both on the batch built 2026-10-09 15:21 UTC (`16cc002e4`).** (a) `test_every_link_to_an_existing_item_is_emitted_in_BOTH_directions`: Maren Kirstine Nilsdatter Skei (Geni `6000000003491958558`, created) gets `LAST P40 Q141499809` Tollak Pederson Folkvår with no `Q141499809 P25 LAST`. Tollak has two mothers in our tree (`…947049` and Maren; a disputed parentage) and Wikidata holds `Q141493424` as his mother, so the reverse half is a second mother; something dropped it without recording it in `reports/single-value-drops.tsv` (which has no `LAST` rows). Not yet found which stage. (b) `test_every_married_surname_in_the_batch_can_be_linked_or_is_being_created`: Guldsmed (`6000000001198139262`), Billberg (`6000000018712633510`), Planström (`6000000050223263059`) married surnames with no item, none created, and not in the carry-forward. Pipeline run `39351821800` (started by a push 2026-10-20 01:09 UTC) is rebuilding the batch; dispatch CI on its commit, and fix whatever survives a fresh build.
- **Analyze Abul Hamza on FamilySearch (`GRWG-G82`) and his position in the tree against Geni (Emma, 2026-10-08 16:1x).** Emma found Abul Hamza on FamilySearch: `GRWG-G82`. On Geni this is the Cyprus person, Geni `6000000227676734863`, the first target of the descendants campaign (CLAUDE.md § What is left). Analyze: who `GRWG-G82` is on FamilySearch (dates, places, parents, spouses, children), whether it matches the Geni profile, where he sits in our tree and in the FamilySearch tree, and how the two disagree (parents, descendants, especially any descendants in Scandinavia, which is the specific interest). Emma: a RootsMagic import is running at the same time, covering 100 generations above him and 100 generations below him. Do not touch that import or its files while it runs; read its results only once it is done, and archive any RootsMagic file before anything touches it (CLAUDE.md). Report what you find; no Wikidata edits from this item.
- **Look at FamilySearch `PF5Q-L8W`, which Emma believes is Izanagi (Emma, 2026-10-08 17:1x).** Emma, right after the Abul Hamza item above: "PF5Q-L8W other one look here I believe this is Izanagi so we do have the Japanese emperor lineage stuff on geni", and then: "I mean familysearch", so the imperial lineage is on FamilySearch. Check who `PF5Q-L8W` is on FamilySearch, whether it is Izanagi, and how the Japanese imperial lineage it sits in lines up with what we hold from Geni and with the imperial items on Wikidata (the Momozono and Ōtomo items merged on 2026-10-08 are in that line). Say how much of the line is there and where FamilySearch, Geni and Wikidata disagree. The same RootsMagic import that is running for Abul Hamza may touch this; leave it alone while it runs. Report only; no Wikidata edits from this item.
- **Error report, from the daily audit of batch `f8abb96a1` (2026-10-08): `Q5040609` Carl Otto Mörner has the `ja` label "カール・オットー・メルネル中尉", the title 中尉 (lieutenant) inside a label.** Read the item's history (who wrote it), fix the label through QuickStatements if it is ours, find the rule that let a title into a `ja` label, and sweep.
- **Audit: script policing on every label, universally (Emma, 2026-10-08).** A label's script must fit its language slot everywhere, not in one emitter: `en` and `mul` take extended Latin only (the guard for these two was added 2026-10-08); `ja`/`zh`/`ko` take their scripts, with the one ruled exception that Latin letters may stand as initials. The earlier guard (no individual created with a CJK `mul`) was not applied universally, which is how Han reached `en` on name items (OBender12, "Strange family names"). Audit every path that writes a label or alias (creations, label corrections, `label-applications.tsv`, name items, side batches) and make each go through the one script check.
- **Audit pipeline consistency: everything done the same way every time (Emma, 2026-10-08).** The "Strange family names" report showed the pattern: the 2026-09-28 rule (a surname field is parsed whole, never word by word) reached `SURN` but not `_MARNM`, which kept splitting word by word until 2026-10-08, so `Sparre över Blad` became `Sparre`, `över`, `Blad`. In this repo the same kind of data must go through the same code path every time; no second, special-cased copy of a rule. Audit the pipeline for places where one kind of input has two handlings (fields, emitters, creation vs. existing items, the day batch vs. side batches) and list each with what diverges.
- **Copy the RootsMagic export that is still downloading, without disturbing it (Emma, 2026-10-09).** It is somewhere on this machine; find it and copy it while it runs. Read-only on the original: no move, no rename, no lock, no edit, nothing that could stop or damage the download.
- **See whether Roger.ec1 replies to OBender12 (Emma, 2026-10-08).** OBender12's only other talk-page note in two weeks is on `User talk:Roger.ec1` ("Footballer import", 2026-09-24): add gender, and some countries are not standard nationalities. Read that page and report whether and how Roger.ec1 answered; it shows how another importer handles the same kind of note. Read only: no post, no reply drafted.
- **Score the 2026-08-07 century prediction (from todo.md § 8b, moved 2026-10-08).** The guess: the Geni-linked items on Wikidata skew to the 20th and 21st centuries much as the Geni profiles do, with the 19th ambiguous. Compute the century distribution of `P569`/`P570` over the local store `wikidata/items/` (never by querying Wikidata) against the Geni side's date coverage (`reports/profile-names.md`), write the CSV of both distributions to `reports/`, and say in the devlog whether the prediction held.
- **Clean up this project, and the ontology-harness checkout of it.** Emma: "we should be putting at the end of the queue something about cleaning it up." Keep it at the end. From Emma's notes of 2026-09-30, `docs/queue-archive/emma-notes-2026-09-30.md`.
- **Audit existing items for script leaks (Emma, 2026-10-08; very end of the queue).** Every item the account created or labelled: any `en`/`mul` label or alias not in extended Latin (the guard of 2026-10-08 stops new ones; this finds the ones already live), listed per item with who wrote the label and when.
- **Rerun the statements, after everything else in the queue is done (Emma, 2026-10-08).** Her words: "after everything else is done rerun the statements". Keep this item last.
- **`P2600` single-value violations, held (Emma, 2026-10-19).** `Wikidata:Database reports/Constraint violations/P2600` lists 3,157 items with more than one Geni id; Emma: most are ours, many carry the SAME Geni id twice, once with the `P1810` subject-named-as qualifier and once without (e.g. `Q70899`). Her ruling: "hold on here". Nothing is changed and nothing is investigated until she picks it up. The super entry points are held the same way (their FamilySearch records carry no sources; several are legend or romance).
