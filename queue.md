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
















- **CI: the universe walk has escaped (Emma, 2026-10-07 23:2x).** The CI test at `tests/test_garborg_day_batch.py:1166` fails on every run since 2026-10-06 01:40 (not in the 2026-10-05 05:19 run): "Q12598947 Buyeo Taebi is in the group and is recorded as outside it — the walk has escaped the account's own items, most likely through Bureus into the world tree". If the walk really escaped, the edit universe is wider than it should be and batches can edit items outside it. Find which link pulls Buyeo Taebi in (the commits between those two runs, `wikidata_subgraph`, `reports/account-edited-links.tsv`), say how big the escape is (how many items joined the group), fix the walk, and check the test passes in CI. The other long-red CI tests (`emma-to-yuri-dolgorukiy.tsv` step with no Geni ID, malformed or repeated hand `.qs` files, Q141656681's `mul` overwrite) are not this item.
- **Make Buyeo Taebi (`Q12598947`) an entry point (Emma, 2026-10-08 00:0x).** Emma thinks the entry points are what caused the CI walk escape in the item just above (the test says Buyeo Taebi is in the group though recorded as outside it). Add him as an entry point the way the others are added (the roster with its date column; CLAUDE.md § THE WIKIDATA STRATEGY lists the entry points started on 2026-09-30), and update what the test treats as outside the group to match. Record in the devlog whether the escape came from the entry points, as Emma suspects, once the item above has found the link.
- **Make Abul Hamza a super entry point if he is not one already (Emma, 2026-10-09).** Check `reports/super-entry-points.tsv` for him; if he is missing, add him the way the other 11 were added.
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
