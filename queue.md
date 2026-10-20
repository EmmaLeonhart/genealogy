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
















- **Audit: script policing on every label, universally (Emma, 2026-10-08).** A label's script must fit its language slot everywhere, not in one emitter: `en` and `mul` take extended Latin only (the guard for these two was added 2026-10-08); `ja`/`zh`/`ko` take their scripts, with the one ruled exception that Latin letters may stand as initials. The earlier guard (no individual created with a CJK `mul`) was not applied universally, which is how Han reached `en` on name items (OBender12, "Strange family names"). Audit every path that writes a label or alias (creations, label corrections, `label-applications.tsv`, name items, side batches) and make each go through the one script check.
- **Audit pipeline consistency: everything done the same way every time (Emma, 2026-10-08).** The "Strange family names" report showed the pattern: the 2026-09-28 rule (a surname field is parsed whole, never word by word) reached `SURN` but not `_MARNM`, which kept splitting word by word until 2026-10-08, so `Sparre över Blad` became `Sparre`, `över`, `Blad`. In this repo the same kind of data must go through the same code path every time; no second, special-cased copy of a rule. Audit the pipeline for places where one kind of input has two handlings (fields, emitters, creation vs. existing items, the day batch vs. side batches) and list each with what diverges.
- **Copy the RootsMagic export that is still downloading, without disturbing it (Emma, 2026-10-09).** It is somewhere on this machine; find it and copy it while it runs. Read-only on the original: no move, no rename, no lock, no edit, nothing that could stop or damage the download.
- **See whether Roger.ec1 replies to OBender12 (Emma, 2026-10-08).** OBender12's only other talk-page note in two weeks is on `User talk:Roger.ec1` ("Footballer import", 2026-09-24): add gender, and some countries are not standard nationalities. Read that page and report whether and how Roger.ec1 answered; it shows how another importer handles the same kind of note. Read only: no post, no reply drafted.
- **Score the 2026-08-07 century prediction (from todo.md § 8b, moved 2026-10-08).** The guess: the Geni-linked items on Wikidata skew to the 20th and 21st centuries much as the Geni profiles do, with the 19th ambiguous. Compute the century distribution of `P569`/`P570` over the local store `wikidata/items/` (never by querying Wikidata) against the Geni side's date coverage (`reports/profile-names.md`), write the CSV of both distributions to `reports/`, and say in the devlog whether the prediction held.
- **Clean up this project, and the ontology-harness checkout of it.** Emma: "we should be putting at the end of the queue something about cleaning it up." Keep it at the end. From Emma's notes of 2026-09-30, `docs/queue-archive/emma-notes-2026-09-30.md`.
- **Audit existing items for script leaks (Emma, 2026-10-08; very end of the queue).** Every item the account created or labelled: any `en`/`mul` label or alias not in extended Latin (the guard of 2026-10-08 stops new ones; this finds the ones already live), listed per item with who wrote the label and when.
- **Rerun the statements, after everything else in the queue is done (Emma, 2026-10-08).** Her words: "after everything else is done rerun the statements". Keep this item last.
- **`P2600` single-value violations, held (Emma, 2026-10-19).** `Wikidata:Database reports/Constraint violations/P2600` lists 3,157 items with more than one Geni id; Emma: most are ours, many carry the SAME Geni id twice, once with the `P1810` subject-named-as qualifier and once without (e.g. `Q70899`). Her ruling: "hold on here". Nothing is changed and nothing is investigated until she picks it up. The super entry points are held the same way (their FamilySearch records carry no sources; several are legend or romance).
- **Link the regular entry points that are unlinked on Wikidata (Emma, 2026-10-19).** Many regular entry points were "for some reason or another just straight up not linked on Wikidata, and they probably should be linked".
- **Figure out what is actually going on with the genealogy (Emma, 2026-10-19).** Her words: "we're figuring out what's going on with the genealogy actually", raised beside the eccentric clusters (`reports/eccentric-clusters.md`: the ancient Chinese, Egyptian and Axum/Ethiopian groups farthest from Charlemagne). The project is "mostly complete"; every queue item is to be finished.
