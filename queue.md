# geni — Work Queue

**This file holds steps not yet taken. Nothing else.** When an item is done, delete it
and append a dated `devlog.md` entry in the same commit. No checkmarks, no "done"
markers, no keeping a finished item for context.

**Do not preserve Emma's wording here.** Her instructions belong in `CLAUDE.md` (rules),
`devlog.md` (what happened) or `reports/` (findings). Emma, 2026-08-22: *"you are makign
the queue useless by presering my verbatim words."* A queue item is a step, in as few
lines as say what to do.

**Trimmed 2026-08-23** from 48 sections to these; what went was records of finished work,
audits, dead crons and superseded priorities. Recover any of it with
`git show 6edf302b:queue.md`.

<!-- HER OWN WORDS, RESTORED 2026-08-27. I had replaced this section with a
     paraphrase of it, on the same evening she said the exact wording is the most
     important thing. Recovered from `git show 07600faf:queue.md`. Do not rewrite
     her text; add underneath it. -->

## Stuff here (semi-confusing) 8-27

Okay so idk what is going on since a lot of contradictory thins are happening. idk if the section below is the next step and the queue is not in use or if it is awkwardly set up

Analyze https://www.wikidata.org/wiki/Q141180412 because it appears that it has Japanese and presumably Chinese label that are no derived from the mul label like we wanted. Remember that the mul lable takes priority

Also any abbreviations like -dtr (i.e. "Rasmusdtr." instead of "Rasmusdatter" should be fixd since wikidata mul labels ae supposed to have the full form. This is a part of the compliance stuff I mentioned earlier)

Organize the queue to make it usable again, currently it does no appear to be usable

For all of the cron jobs that I set up in the session. They are good and continue on with them, but also add them into the queue as actual items with he specification they are the cron jobs so they cget crossed off if he cron job finishes, but are a bit more stable.

Look over all of the items that I have edited but did no create. These are a bit of a weak point for me since they are potentially items that are no in my watchlist and might cause me issues. Create a batch of quickstatements that does some kind of minor edit on all of them if possible preferable settin their mul labels or something

Look over this item it just piques my curiosity whether we can identify it on geni and potentially add a mul label https://www.wikidata.org/wiki/Q4411612


## Tonight's cron jobs — SESSION-ONLY, so they are written here to survive

Emma, 2026-08-27: *"For all of the cron jobs that I set up in the session. They are good and
continue on with them, but also add them into the queue as actual items with the specification
they are the cron jobs so they get crossed off if the cron job finishes, but are a bit more
stable."*

**They die with the session.** If it ends before one fires, the item below is all that is left
and is the thing to work from. Delete an item when its job has finished the work.

- **20:50 `082e986a`** — `Q141198538` has `nn` as a first name though it was not produced as an
  NN person. Why, and stop it recurring.
- **21:20 `e01a1bff`** — two saved Geni pages, in
  `C:\Users\Emma\.claude\uploads\dbec586f-7705-4f0e-8652-03df7c6b73e5\`, named
  `a8b40e73-Geni__Caroline_Signe_Borsheim_Hoknes_19322007.mhtml` and
  `1ef99cd3-Geni__Randolph_Paulus_Borsheim_19262015_Penticton.mhtml`. Through
  `genimerge path-from-html`. The `?through=6000000177921459078` chain runs via Randolph Paulus
  Borsheim, and she notes the closest relationship is a **marriage** one, which decides the
  export style that would follow it.
- **21:55 `aea9cf19`** — the `Sara /NN/` census: every person whose name carries an NN marker in
  only ONE of the given/surname fields, as a CSV, then the decision stated explicitly.
- **22:00 `a5676be8`** — why `6000000021223635839` was emitted as bare `Garborg` rather than the
  labels she set by hand on `Q141199845`. Likely `labels.strip_markers()`, added the same day.
- **22:30 `5e093107`** — why `Q141199868` came out as brackets. `CLAUDE.md` § *A parenthesised
  token in `SURN`/`_MARNM` is THREE different things* already rules this; the label builder
  appears never to have applied it.
- **23:00 `0fbd27ed`** — script universality. Every individual gets a Latin `mul` label
  (`Q12598947` and `Q19657284` did not) and every script the tree records for them. Her rule:
  **if a script is the only script a name appears in anywhere in the tree, it belongs in the
  default label set on every item.**
- **23:30 `52d05831`** — whether to make the repo public and have Actions email her a batch every
  day. An analysis, not a decision; the decision is hers.
- **00:30 `0a2b3635`** — compliance audit of every individual created from this repo's batches
  against the original specifications, as a CSV with per-rule counts.
- **01:00 `18a633d0`** — `Forest` and `Ancestors` exports on `6000000227464556886`, integrate,
  re-merge, rebuild the derived layer, then run the daily batch and attach it.
- **02:00 `40c4c8e1`** — the ledger-with-history idea: resolve redirects, keep past Geni ids,
  compare both directions. **She asked for a question on every part, each carrying an "I do not
  know what this means contextually" option**, and no implementation until she answers.

## The spine's `P2600` statements were never written to Wikidata

`reports/wikidata-spine-add-p2600.qs` holds **16 `P2600` *Geni.com profile ID* statements** for
spine people whose items already existed — `Q5915800` Knut Algotsson, `Q101247444` Ingegerd
Svantepolksdotter, `Q6197518` Svantepolk Knutsson Viby, `Q3743799` Knut Valdemarsson, `Q4953376`
Helena Guttormsdatter, `Q274606` Berengar I and `Q284400` Gisele of Cysoing among them. Two were
**accepted by Emma on 2026-08-26**.

**Until it runs, those correspondences exist only in `reports/garborg-qids.tsv`**, written there
by hand. The contributions refresh cannot find them — it resolves an item by reading `P2600` off
it and there is none — but it also **never deletes rows**, so they survive every run. Nothing is
being lost today; the correspondence is simply local rather than on Wikidata, and only a rebuild
of the ledger from scratch would fail to recover it.

## Built and waiting on 2026-09-01 — nothing to do until then

- `reports/wikidata-geni-qid-p2600.qs` — **354** `P2600` *Geni.com profile ID* statements
  from the Wikidata links in the Geni About Me. Account in `reports/geni-qid-links.md`.
- `reports/wikidata-izumo-beyond-chart.json` — one `create_individual`, Takanori 81 Senge.
- `reports/wikidata-izumo-succession.json` — **105** `P39` *position held* statements,
  the three Izumo offices with `P2389` naming the organisation and `P1365`/`P1366`
  chaining each line. Built 2026-08-26 to Emma's three-office model.
- `reports/wikidata-nn-labels.json` — 3,525 `NN` label edits, built to her full model.
- Entity resolution — 10 edits, emitter correct.
- Samaritan High Priest normalization — built. `P39` *position held* → `Q678510`
  *Samaritan High Priest* is what separates her well-modelled five from the rest.
- `reports/wikidata-garborg.qs` — **rebuilt 2026-08-23** to the model in
  `docs/wikidata-item-template.md`: `S2600` references, no descriptions, `P3373` *sibling*
  both ways, and no `CREATE` for the four items Emma has already made. 6 creations, 84
  statements. Name properties are listed in its trailer rather than emitted — they need
  a QID per given-name item and a new `P5056` patronym item for *Jonsdatter*,
  *Eivindsdatter*, *Eivindsen*, *Eivindson*.

Emma runs these by hand — 2026-08-23: *"If it's geni id then I'll run manual
quickstatements."*

Every `.qs` in `reports/` is guarded by `tests/test_p2600_batches.py` — line shape,
quoting, `S2600` references, Geni ids, duplicate statements, one `P2600` per `CREATE`,
and no two batches creating the same person.

## The slow lane: every module has now been RUN and is GREEN

**4,467 slow tests, 0 failures.** The three that had never completed were run on 2026-08-27:

| module | tests | wall | where the time goes |
| --- | ---: | ---: | --- |
| `test_merge_real_exports` | 9 | 90m over 3 chunks | the merge, 837s per process; `is_idempotent` merges twice |
| `test_paths` | **24** | 16m52 | one 1,012s fixture; every test is under 5ms |
| `test_density` | 18 | 17m28 | `every_listed_region_gets_a_seed` 992s, `presence_never_exceeds` 57s |

`test_gedcom_real_exports` (4,427, in 4 chunks) and `test_wikidata_store_real` (5) were green on
2026-08-25 and have not been re-run since.

**The old figures in this section were wrong in both directions.** `test_paths` was recorded as
5 tests that "exceed 10 min even alone" — it is 24 tests and finishes in 17 minutes unchunked.
`test_density` was recorded as 17 passed with the 18th blocking; all 18 pass, and the slow one is
992 seconds rather than unbounded. Both readings came from watching a run get killed and
inferring, which is the same mistake as "twenty minutes per test".

**Only `test_merge_real_exports` actually needs chunking**, and the unit is the fixture: four
fixture-only tests share one merge (15m28), two corpus-streaming ones take 32m07, three that
re-merge or write the 409 MB file take 42m34. **16.8 GB for one merged tree, 23.6 GB while the
idempotence test holds two** — run nothing beside it.

## Decided 2026-08-25 — the multi-Geni-ID work

- **Borderline pairs: LEAN TWO PEOPLE.** Emma, 2026-08-25: *"Lean two people — never merge
  on a coin flip."* A wrong merge destroys a real person from the record; a wrong split
  only leaves work undone. The duplicate count staying understated is the accepted cost.

- **`Q122925764` is SETTLED, 2026-08-26, and needed no export.** The item is
  **Станіслаў Томаш Сапега** — *Stanisław Tomasz Sapieha*, one man whose name is **both**
  given names — carrying `P2600` for `6000000041241763571` *Tomas Stanislaus Sapiega* and
  `6000000041241858399` *Stanislovas Sapiega*. Its father `Q958111` is our Andrzej Sapieha
  for both. **Geni records the two as BROTHERS** (each other's siblings on the profile page,
  same father in our corpus). So Wikidata holds one man where Geni holds two, and one item
  carrying two Geni ids is the shape `CLAUDE.md` § *A second Geni ID on one Wikidata item is
  NOT a conflict* calls ordinary and correct. Nothing to remove, nothing to merge.

  **The export could not have been run anyway**: Geni offers *Export GEDCOM* only on
  profiles the account manages, and this one belongs to Algirdas Tamulis. `/gedcom/export`
  exports from Emma's own profile and rejects `?id=`. Reaching a stranger's family needs a
  placeholder created there first, per `docs/export-seed-rules.md` — which was not worth
  doing for a question already answered from data on disk plus one profile page.

- **The 70 targets are classified from our own tree, 2026-08-26 — 2 need a page opened, not 95.**
  `scripts/classify-multi-p2600-by-tree.py` asks what relationship our corpus already records
  between the two profiles one item claims. Of 2,110 items stating more than one Geni id, 1,831
  have neither profile in our corpus and 209 have only one, so nothing can be said about them.
  The **70** with both are:

  | our tree says | n | reading |
  | --- | ---: | --- |
  | no relationship recorded | 41 | the Zerubbabel shape — unmergeable duplicates. Ordinary. |
  | siblings, sharing a parent | 27 | the Sapiega shape — Geni holds two, Wikidata holds one. Our snapshot matches Geni, so nothing to do. |
  | **one is the other's PARENT** | **2** | a generation collapsed into one item. The residue. |

  **The two:** `Q104755784` *Ruben Wulff* claims Ruben Wulff **and** Wolf *Rubensson*, whose
  patronymic says he is Ruben's son. `Q96985053` *John Loomis* claims two John Loomises, one the
  parent of the other — father and son sharing a name.

  Those two are worth opening. The other 68 are shapes `CLAUDE.md` already calls ordinary.

- **The add gate is DECIDED, 2026-08-26: loosened.** Emma, shown that 5,540 of its 5,651
  rejects had no disagreement anywhere: *"Loosen it — emit the ~7,000."*
  `reports/wikidata-add-p2600.qs` is **7,168 additions**. It now refuses contradiction and
  not silence — 148 refused, each a case where a parent is recorded on both sides and the
  two are different people.

- **Classify the 70 multi-`P2600` targets by what our own tree says about the pair.**
  `Q122925764` was settled on 2026-08-26 with no browser at all: the item is one man whose
  name is both given names, and our corpus gives its two Geni ids **the same father** — so
  Geni holds two brothers where Wikidata holds one person, which `CLAUDE.md` calls ordinary
  rather than a conflict. That check generalises. For each of the 70, ask what relationship
  our tree records between the two profiles: same parents (siblings), one the parent of the
  other, spouses, or no relationship at all. Each answer means something different, and
  none of them needs a page opened. Whatever is left after that is the genuinely thorny
  residue and only that needs the browser.

## The bare day-build is now REFUSED — guard shipped 2026-08-27

`scripts/build-garborg-day.py` with no arguments exits non-zero, writes nothing, and names the
flag it wants. **Bare it emitted 272 creations; `--compose` emits 34** — that flag carries
`CHILDREN_PER_RUN`, `PARENTS_PER_RUN`, `FREE_PARENTS_FREE` and `SIBLING_CAP`, so the bare path
was not a smaller daily algorithm, it skipped the algorithm. Both wrote the same file, so a bare
run silently replaced a day Emma may already have run.

`--roster` stays a legitimate second mode; only the argument-free call is refused, because it has
no purpose except the mistake. `tests/test_join_sanity.py` asserts the exit code, the message and
that the batch file is byte-identical afterwards.

**`--compose` still ADVANCES the sequence and that is not guarded**, because it should not be:
it consumes and rewrites `reports/garborg-carry-forward.tsv`, so running it twice in a day gives
the next hop rather than today's. Run the daily batch through `build-daily-batch.py` and never to
"refresh" a committed day — a code change reaches the batch on the next legitimate run.

## Drift between stages — the recent tier is CLEAR; 69 deep-history rows stay flagged

`scripts/refresh-drift.py` walks the `generator -> input` graph the freshness census already
holds, orders the stale generators topologically, runs them, rebuilds the census and repeats.
It replaced a hand-typed chain that could not see its own cascade.

**Three rounds to converge: 9 scripts, then 2, then 3, then 0.** Refreshing a stage restales its
consumers, so a single pass was never going to be enough — the `--rounds` loop was written on
suspicion and the suspicion was right.

Guards that matter more than the sort: a script naming `WikidataClient`, `full_entities`,
`urllib.request` or `requests.` is **skipped and reported**, never ordered; a cycle is reported
rather than broken; `--max-age-hours` defaults to 72 so the deep-history rows stay out; and the
`generator` column is confirmed with `writes_in` before a script is run, because that column
names any script that *mentions* a file and a reader landing there would have re-run
`build-synoptic-correspondence.py` — a whole-corpus job — for a file it does not produce.

**69 rows remain, all 150-360h behind `out/merged.ged`, `derived-family.csv` or
`display-names.csv`.** They are one-off analyses the corpus grew under. Re-running them is a
choice about what to measure, not a fix, so they are not queued. `--max-age-hours 400` does it
if that choice is ever made.

## The derived CSVs are committed gzipped

Emma, 2026-08-24: *"Imo gzip because this is long term and we aren't adding any more data
into our tree. Just processing."* `scripts/pack-derived.py`, four `.csv.gz` in git
(26-43 MiB, 4.1-4.8x), four plain CSVs gitignored, `tests/test_derived_packing.py` pinning
the pair. `CLAUDE.md` § *The four big derived CSVs are committed GZIPPED*.

**After a clean clone: `python scripts/pack-derived.py --unpack` once.** Forty-four
scripts open the plain CSV by name.

## ⛔ `exports/post-merge/` — resolving stale duplicates without throwing exports away

**Emma's design, 2026-08-24.** The problem: Geni has merged people our corpus still holds
twice, and *"we can't just throw out the earlier exports that contain stale individuals"*
— they carry thousands of people the merge needs.

**Her method, in her order:**

- **Export from the merged individual directly** where she created them, since she can
  reach the profile.
- **Where that is impossible, fall back to the earlier add-an-ancestor-then-export-from-them
  algorithm**, in the browser. That is `docs/export-seed-rules.md`.
- **The new GEDCOMs go in `exports/post-merge/`**, a directory with special logic: **a
  Geni record in there overwrites the same Geni ID from any other export** in the synoptic
  tree. Post-merge is newest and therefore right.
- **Export until every first-degree relative of every merged individual is present** in
  that directory. That is the stopping rule, not a count of exports.

**The economy of it is hers and it is the important part:** *"merged individuals cluster
together so we will not need to run an export on every one of them"* — one ball covers
many. The 13 `strong` rows bear this out: seven are Haji-no-muraji and three are Sugawara,
two lineages rather than thirteen scattered people.

**MEASURED 2026-08-26, and the answer is: do not write the relationship override.**
`scripts/measure-post-merge-override.py` → `reports/post-merge-override.tsv`.

Half the design already works: `genimerge.sources._post_merge_last` sorts the directory last,
so post-merge has the final word on every **single-valued** path. The other half — overriding
**relationships**, which are unioned and never dropped — was measured before being written:

| | parents | spouses | children | total |
| --- | ---: | ---: | ---: | ---: |
| would be **dropped** | 1,701 | 1,126 | 2,710 | **5,537** |
| of those, pointing at somebody **no post-merge ball reached** | 1,541 | 1,034 | 2,550 | **5,125 (93%)** |
| **only in post-merge** — what the override would gain | 0 | 0 | 0 | **0** |

**It subtracts 5,537 and adds nothing.** A post-merge ball stops at 5,000 people, so a relative
outside it is absent because the ball ended, not because Geni deleted the link. Applying the
override literally would delete 5,125 real relationships to buy nothing.

**412 drops are falsifiable** — both ends inside a post-merge ball, 362 people, 160 parent /
160 child / 92 spouse. Those are the genuine *Geni deleted this link* candidates and the only
population an override should ever touch. Next step is to look at a handful of them as records,
not to write the override wholesale.

Depends on `reports/geni-stale-duplicates.tsv` (13 strong, 3 medium, 13 weak) and
`reports/geni-merges-performed.tsv` (180 survivors from her activity feed).

## Post-merge resolution is MEASURED — 20 of 29, and no export is outstanding

`scripts/check-post-merge-resolution.py` → `reports/post-merge-resolution.tsv`, over all
**seven** exports in `exports/post-merge/` (23,373 distinct people) and all 29 duplicate pairs,
not the one export and 13 strong rows the earlier note described.

| evidence | resolved | both still present |
| --- | ---: | ---: |
| strong (13) | **13** | 0 |
| medium (3) | **3** | 0 |
| weak (13) | 4 | 9 |

**Aaron III needed no export — two had already been run on his own survivor**,
`export-Forest-6000000178918141824.ged` and its `-refresh`. The refresh holds the survivor
without the twin, which is the resolution condition. The queue said one was outstanding because
the count was taken against a single file on the day it landed.

**The 9 open rows are all `weak`, and "both present" there is the expected outcome rather than a
failure.** `CLAUDE.md`: if Geni holds two, we should hold two. `weak` is the grade for pairs
least likely to be one person. Three of the nine are the same survivor,
`6000000227350557852` *Yorimoto Tanba*, who carries three stale twins — which is also why 29
pairs sit over 27 distinct survivors.

**Still to do here: re-merge and re-derive**, then the structural walk and the correspondence, in
the order § *PREREQUISITE ORDER* sets.

## ⛔ PREREQUISITE ORDER for the synoptic rebuild — merges first, then joins

**Emma, 2026-08-24:** *"you forgot about the geni merge stuff which is an even more
important prerequisite to the synoptic rebuild"*.

The order is:

1. **Resolve the Geni merges** — `reports/geni-stale-duplicates.tsv`, 13 strong. Our tree
   holds **two nodes for one person** where Geni holds one, so the structural walk and
   the correspondence are both computed over a tree that double-counts those people, and
   whole parallel lineages sit side by side. Rebuilding before this bakes the duplication
   in. Her `exports/post-merge/` design is how it gets fixed.
2. **The clan joins** — done 2026-08-24, `scripts/build-clan-p2600-pairs.py`.
3. **The structural walk and the correspondence — RE-RUN 2026-08-27.** Its input
   `reports/derived-family.csv` was rebuilt on 25 Aug at 18:10, three and a half hours *after*
   the walk last ran at 14:42, so the output had been stale against its own input.

   `python scripts/walk-structural-merge.py --all` — the bare invocation only prints sample
   lines, which is why an earlier attempt looked like it had run and changed nothing.

   | | |
   | --- | ---: |
   | AGREE | 89,486 |
   | MERGE | 35,737 |
   | GENI ONLY | 131,366 |
   | WD ONLY | 12,512 |
   | AMBIGUOUS | 237 |

   `structural-correspondence.csv` **7,841 rows**, `wikidata-structural-placeholders.json`
   **35,162**. The change from the stale version is small and real: 34,943 entries identical,
   218 gone, 219 new. It reads as a 12,321-line diff only because the JSON is pretty-printed at
   ~28 lines an entry.

**The clan-join result, stated correctly.** Tanba 179/183 (97%) and the sister Izumo
roster 120/202 joined — and **0 pairs that the About Me extraction had not already
found**. That is not a null result: two independent paths, the roster join and the
corpus-wide About Me pass, agree completely. Emma: *"it probably means we did good data
modelling early on"*. The new fact is **Onakatomi 0 of 97** — that clan has no About Me
links written yet, so it cannot join at all. Hers to write.

## The correspondence batch is current again — 3,719 → 7,535, 2026-08-27

`scripts/build-structural-correspondence-batch.py` was last built **2026-08-23** against a
correspondence file that has since doubled. Rebuilt against the current walk:

| | |
| --- | ---: |
| structural correspondences read | 7,841 |
| **emit** — the item states no Geni ID and our person is linked nowhere else | 7,134 |
| a **second** Geni ID on the item — emitted and flagged, never held back | 401 |
| our person is already linked elsewhere — **not emitted**, written to `structural-correspondence-disagreements.csv` | 302 |
| already stated on the item | 4 |

**7,535 `add_geni_id` edits over 7,514 items** — 21 items take a second `P2600`, which
`CLAUDE.md` calls the correct representation of two unmergeable Geni profiles rather than a
conflict. 1,371 share no name token with their Wikidata label and are **flagged for reading,
not filtered out**.

**`P813` *retrieved* was stamping a false date.** The flag defaulted to a literal
`2026-08-17`, so every rebuild after that day claimed the source was consulted on the 17th. It
now defaults to when `reports/structural-correspondence.csv` was written, which is both true
and deterministic for a given input.

## Model-vs-reality is BUILT — `scripts/model-vs-reality.py`

Emma, 2026-08-24: *"we are supposed to generate complete models of what the wikidata items should
be and compare with the reality for the quickstatements modelling stuff."*

Over the 71 ledger people, freshly fetched through `genimerge.wikidata.full_entities`:

| | |
| --- | ---: |
| **extra** — the item has it, the model does not. Her hand-work. Never touched. | 483 |
| **missing** — emittable, and the only column a batch may project from | 77 |
| **CONFLICT** — both hold it, values differ | **4** |

The four are genuine and **go out as second statements cited to Geni**, decided 2026-08-26:
Rozala d'Ivrea died 13 Dec or 7 Feb 1003; Knut Valdemarsson 15 or 5 Oct 1260; Arne Olaus
Fjørtoft Garborg 12 or 10 Oct 1968; Helena Guttormsdatter born 1167 or 1170. Nothing on
Wikidata is replaced; ours goes in beside it and the item records both.

**It found twelve more conflicts that were the comparator, not the model** — and that is worth
keeping in mind before trusting any diff's first output. Five `P1449` *nickname* rows compared
a bare string against the raw `{"language": ..., "text": ...}` blob. Seven date rows compared ISO
strings while ignoring Wikidata's precision field: `+0874-07-01` against `+0874-00-00` is not a
disagreement but a difference in what is known, and precision **7 is a CENTURY**, so `+0952/9`
against `+1000/7` is one century agreeing with itself.

**The projection is built too** — `scripts/build-from-diff.py` → `reports/wikidata-from-diff.qs`,
**74 statements over 42 items**, every one present because the diff says the item lacks it and for
no other reason. `extra` is never touched, `CONFLICT` is never emitted, labels and aliases are
never projected because they replace. The 8 missing `P2600` are skipped: the spine batch already
carries them, which the diff rediscovered independently.

**The Izumo diff is run** — `reports/model-vs-reality-izumo.tsv`, 111 people, and it inverts the
Garborg picture:

| | Garborg | Izumo |
| --- | ---: | ---: |
| missing | 77 | **351** |
| extra | 483 | 178 |
| CONFLICT | 4 | 8 |

**All 111 lack `P2600`**, which matches what was already known — 204 of the clan have items and
almost none carry a Geni id. 89 lack `P21` *sex or gender* and 80 lack `P22` *father*. The 95
`extra` `P53` *family* rows are the clan membership Wikidata records and our model does not.

**The conflicts said what they were built to say.** Two are `P31` *instance of*: our model asserts
`Q5` *human* where Wikidata says **`Q524158` *kami***. Kushiyatama `Q86734749` and Raihita
`Q123511663` are classified as Shinto deities there. The projection withheld both — a `CONFLICT`
is never emitted — so the design held, but **the model is asserting `Q5` for a divine-descent
lineage and that is a rule, not two rows.**

## Checked: succession-as-parentage on Wikidata is ONE case, not a pattern

`scripts/check-izumo-succession-as-parentage.py`, over every consecutive-seat sibling pair on the
chart:

| | |
| --- | ---: |
| no `P22` on the later brother at all | 7 |
| one of the pair has no item held | 2 |
| **brother recorded as father** | **1** |

The one is Hiroshima 25 → Otoyama 26, already known. **The error does not run wide**, and that
matters as much as finding it would have: Wikidata's Izumo parentage is thin rather than wrong —
seven of ten pairs simply have no father recorded.

**So the 80 missing `P22` rows in `reports/model-vs-reality-izumo.tsv` are the real story**, not
the four conflicts. There is little there to contradict.

**The count in this item said twenty and it was wrong.** 88 *ordered* sibling pairs contain **10**
unordered consecutive-seat pairs; twenty counted each from both ends. Corrected here rather than
left as a number somebody would later try to reconcile.

## A join that matches NOTHING must fail loudly — it has cost five findings this week

Every one of these produced a plausible number that was about the instrument rather than the data,
and each was caught by luck or by a second opinion rather than by anything structural:

| what | what it printed | what was true |
| --- | --- | --- |
| `split()` unaware of ` \| ` | 615 ambiguous slots, no `2×2` | 379,251 people arrived childless |
| `\|` split without `.strip()` | pair count moved by **exactly zero** | every token missed the index |
| `father[child] = husb` | census read **0** multi-parent people | 1,663 of them |
| sex rate over `zipper-pairs.tsv` | **0.0%** for all four shapes | measured the filter, not the join |
| `chart_name` column that does not exist | all 10 pairs *"no item held"* | 196 names carry a QID |

**The shape is always the same: an empty or narrowed join is indistinguishable from an absence of
data**, and absence is exactly what these reports are built to detect. `CLAUDE.md` already records
the same lesson for the date parser — *"a wrong date parser does not raise, it just quietly
narrows the data"* — and it has now recurred five times in a week outside dates.

**BUILT 2026-08-26** — `tests/test_join_sanity.py`, seven guards over the real files, each
verified to *fail* when its bug is reintroduced rather than merely to pass now.

**The first version did not guard.** It asserted that >50% of multi-value tokens in
`derived-family.csv` resolve to a person — and **both historical bugs passed it**, 58.5% for the
unstripped split and 86.3% for the pipe-blind one, because single-valued cells have no separator
and resolve either way while being the large majority. Restricted to cells that actually hold
several values the separation is total: **100.0% correct against 0.0% for both**.

That is the same mistake in miniature as the five it was written against — a plausible number
measured over the wrong population — and it was caught only by deliberately reintroducing the
bugs. **A guard that has not been seen to fail is not known to guard.**

## ⛔ Audit of Geni merges — her method, 2026-08-24

*"Find profiles that look similar like shared parents, plus look over basically all
Japanese items with higher scrutiny, and then use the browser extension to see if they
merge. Izumo ones are good to explore to see how redirects potentially work."*

Three steps, in her order:

**Steps 1 and 2 are built** — `scripts/find-geni-duplicates.py` →
`reports/geni-duplicate-candidates.tsv`, **9,744 same-parent-same-name groups** over 20,191
profiles, plus 367 unparented same-name-same-year ones. Nothing merged, nothing rewritten.

The Japanese pass exists now and did not before: the `script` column read `Latin` for all
1,329,328 people because the finder matched the romanised `label_en`, while the kanji sit in
`cjk_names`. It now classifies and matches on both, giving **119 CJK-scripted groups** where
there were 0, sorted first. `tests/test_join_sanity.py` fails if that returns to 0.

**Still to do: the browser extension on the candidates, Izumo first**, to see whether Geni
merges them and how redirects behave. **The merges are hers, never performed here.**

Read the top of the CJK section knowing what it holds: `Yasuji Tanba ×6` and the other Tanba
groups are the real signal; a residue of bare one-token surnames (`杨`, `黄`, `邱`) survives
because those people have a given name recorded somewhere but their `cjk_names` carries only
the surname.

## ⛔ THE DAILY ALGORITHM — her full spec, 2026-08-26. Supersedes the one-hop ring

`docs/dictation/2026-08-26-daily-algorithm.md` is her dictation verbatim;
`docs/daily-algorithm.md` is the reading. **The order is structurally rigid and the weirdness is
intentional** — *"the weirdness isn't something to be sanded off"*.

**Steps 1, 1b, 2 and 3 are BUILT into the existing scripts**, 2026-08-26 — she said the
existing generation should do this, not that a new script should:

- **Step 1, individuals** — `compose()` in `scripts/build-garborg-day.py`. 4 random parent
  pairs + 1 ancestral pair from the spine, **shuffled together** so the ancestral one is not
  always first; plus 4 people whose spouse and children are filled in. Run with `--compose`.
- **Step 1b** — `RANDOM_COUPLES` 1 → **5**, each filled with their **entire** uncreated children.
- **Step 2, names** — `NAME_ITEMS_PER_RUN = 10` in `scripts/build-garborg-name-items.py`, the
  rest carried and listed in the file's own trailer.
- **Step 3** — already right: `P3373` *sibling* capped at 10, every other relationship uncapped.
- **The section order is now hers** — individuals, then relationships, concatenated at write
  time. The file emitted relationships first until today.

**One command, 2026-08-26**: `python scripts/build-daily-batch.py [--refresh-ledger]`
runs step 0, then the three steps in her order, and prints the run order with each file's
position. Step 0 is off by default because it is the day's one network call.

**Still to do:**

- **BUILT 2026-08-26 — the parenthesised name tokens.** `scripts/namemodel.py` carries
  `PARTICLES`, `UNKNOWN_MARKERS` and `name_shape()`; `classify_fields` strips the brackets,
  `statements_for` skips particles and markers, `aliases_for` emits the bracketed form.
  Rulings in `CLAUDE.md`, census in `reports/paren-tokens.md`.

  **The particle rule reaches far beyond the brackets: 257,030 tokens** stop being `P734`
  *family name* lookups — `de` 125,425, `von` 60,959, `van` 13,836, `la` 7,481, `af` 7,189,
  `ap` 6,574. Every one of them was being proposed as a family-name item.
- **Diff the remainder against the ideal state as part of the run** — `model-vs-reality.py`
  is the diff and is not yet wired into the daily command.
- **The ideal state is still the Geni tree alone.** Her spec says the **union of the synoptic
  tree and the Geni tree**; the synoptic half does not exist yet, which is the § *PREREQUISITE
  ORDER* item.

**Do not "fix" the artefacts.** Spouses unlinked to their partner's children, and parents not
linked to each other as spouses, are intentional consequences of the order and are closed by later
days.

**Two readings taken rather than asked, both recorded where the code is:** which 10 name items —
most-borne first, so each earns the most links; and step 1b runs every time rather than behind a
gate for *"once we get to a certain point"*, because she said it *"could be in the same line as
the descendants one"* and a gate I invent that never opens is the failure mode § *The batches are
a SEQUENCE* is written against.

## `-sen`/`-son` is BUILT — both halves, 2026-08-27

**The plan emits a patronymic row for a `-sen`/`-son` token AS WELL AS its given/family rows**,
not instead of them. `CLAUDE.md` § *One name item per USAGE*: a token used two ways gets two
items and that is not an ambiguity to resolve. Patronymic rows 623 → **1,677**; the 18
patronymic tokens the daily batch needs moved from *"not in the plan"* to *"create"*.

**`classify_fields` takes an optional `father_name`** and `patronymic_or_surname()` applies her
test per person — same token as the father → inherited surname; stem matches the father's given
name → patronymic. Without a father it keeps the morphological answer, which all nine callers
rely on.

**The father reaches the emitter, 2026-08-27.** `statements_for` and `name_lines` take
`father_name` and both call sites in `build-garborg-day.py` pass the father's label. Worked
case, `Anna Gundersen`: no father → patronymic, item not minted, nothing emitted; father
`Gunder Olsen` → stem matches his given name, still a patronymic; father `Hans Gundersen` →
same token, so an inherited surname and **`P734` → `Q656767` goes out**. That third case used
to produce no name statement at all.

**Still to do:** the plan's patronymic rows are all `create`, so those items must be minted
before anybody links to them — 10 a run through `build-garborg-name-items.py`. That is cadence,
not work.

## The relationship section was 75% duplicates — fixed 2026-08-27

**Emma:** *"the relationship one is questionable that it's always gonna be so huge and
growing."* She was right and the cause was not workload. Measured: **229 of 306** statements on
existing items were **already on Wikidata**. The section was three-quarters noise.

Two causes:

- **`P40` *child*, `P26` *spouse* and `P3373` *sibling* consulted no check at all.** Only `P22`
  *father* and `P25` *mother* tested `absent()`, so every child, spouse and sibling link went
  out on every run.
- **`absent()` is property-level against a snapshot frozen at 2026-08-24.** It knows an item has
  *some* `P40`, not which children, and it could not know Emma had run yesterday's batch.

`scripts/refresh-live-values.py` reads whole items and writes
`reports/garborg-live-values.tsv` — 1,409 statements over 80 items, `qid`/`property`/`value`.
The builder drops any statement already present, as a **post-pass**: the check inside `add()`
caught 148 and missed 81, because the name-statement block appends to `lines` directly.

**Statement lines 895 → 666, links 164 → 16, duplicates remaining 0.**
`tests/test_p2600_batches.py` guards it, verified by disabling the filter.

**It is step 0b of the daily run, 2026-08-27** — `build-daily-batch.py --refresh-ledger` does
both halves: the ledger says WHO has an item, the live values say WHAT each already states.
Refreshing one and not the other is precisely how the batch became three-quarters duplicates.
A run without `--refresh-ledger` prints the age of both files and why it matters.

## The daily Garborg batch — one QuickStatements run per day

`scripts/build-garborg-day.py` → `reports/wikidata-garborg-day.qs`.
`reports/garborg-qids.tsv` is the ledger of who has a QID, filled from **Emma's Wikidata
contributions** (account 日巫女), never a bulk download — her instruction, 2026-08-24.

**The rule: a statement goes in only if BOTH ends already have a QID.** Emma, after
running the first file: *"I only ran some of the quick statements because many of them
required links that couldn't exist... this is going to be the practical limitation of
what our quick statements can do."* Nothing deferred, nothing commented out. What cannot
run today is tomorrow's batch, because tomorrow those items exist.

Each day: close the links yesterday's creations made possible, create the next ring, link
the new people only to what already exists.

**Outstanding on this item:**

- **NOT a blocker, and never was — `reports/wikidata-garborg-name-items.qs`.** It said it
  had to run first because *"QuickStatements cannot point at an item a `CREATE` in the same
  batch just minted"*, which is false: that is what `LAST` does. It now creates each name
  item and, in the same run, emits `Qperson Pprop LAST` for every bearer who already holds a
  QID — **112 name items and 106 statements**, where it was 42 items and nothing. Emma,
  2026-08-26: *"in the generation run add it to the existing ones too."* People this run is
  also creating still wait for the next one, which is the sequence working, not a gate.
- **`Olga` and the seven other ambiguous tokens are handled, not blocked.** A token the
  plan says resolves to several items is never created — that is the `Maria` rule — and is
  listed in the batch's own trailer for Emma. The batch runs without them, so nothing waits;
  the NEEDS-DECISION tag this carried was wrong.
- **CJK `SURN` is unproven and out of scope here.** `CLAUDE.md` records `SURN` holding a
  *place* while `_MARNM` held the real clan name, so reading `surn` as a surname is right
  for Norwegian material and not established corpus-wide. Belongs to the corpus-wide name
  work, not this batch.

## Ordering is now enforced — `genimerge.editorder`

Emma's design, verbatim: *"it randomly selects an edit object, sees if its requirements
are present, if they are then it runs, if no then randomly select and run another one."*
Implemented, 11 tests, and it orders all **284,146** edit objects in about a second with
**0 violations, 0 dangling, 0 cycles, 0 duplicate ids**.

**Wired into `scripts/wikidata-edit-run.py` on 2026-08-24.** The runner orders before it
slices — it used to take `edits[:limit]` in file order — and **refuses a batch whose
prerequisites live in another file**, naming the file that provides them. Three do:
`wikidata-mul-labels.json` needs `wikidata-en-labels.json` 14,972 times, and the Samaritan
succession and Abram fix need `wikidata-samaritan-links.json`. `--satisfied` takes a list
of ids already applied so a resumed run is not blocked by finished work.

## Izumo / Senge clan — measured 2026-08-23, `reports/izumo.md`

<https://shinto.miraheze.org/wiki/Izumo_clan>, and the Geni tree at
<https://www.geni.com/people/Tsusa-no-mikoto-no-Mikoto/6000000012789160423>.

**214 people rostered, 204 with a Wikidata item, and only 2 carry a Geni ID.** The
Wikidata side is nearly complete; the Geni side is joined to almost none of it.

Emma's constraints on this one:
- She trusts the tree-building from what the page shows, and the descriptions and Wikidata
  links. **The duplicate-profile merges are hers — flag, never perform.**
- The clan was added to Geni three separate times (2008 Japanese, 2011 English, her own in
  2026), so duplicates are expected and creating people blindly would make a fourth set.
- The numeric middle names are **regnal numbers** ordering the Izumo no Kuni no Miyatsuko,
  not names. The roster keeps them in their own column.

**76 of the 77 rostered lineage people are in the corpus with their Geni IDs**, measured
2026-08-23 with `python scripts/match-izumo-export.py --corpus` — 545 exports, joined on the
regnal number Geni writes inside the name. `reports/izumo-p2600-pairs.tsv` is the result:
76 rows, every one carrying a Wikidata item.

Two exports did it and they were complementary, not one right and one wrong: the founder-end
ball (Kushini 3) brought Izumo 18–40, the far-end ball (Naokuni Senge 56) brought Izumo 34–54
and the whole Senge/Kitajima 55–78. A third, seeded on Obitake 23, added nothing rostered and
should not have been run — it chased a gap that only existed in a single-file measurement.

**The Google route is dead for this clan.** `site:geni.com "Naokuni Senge"` and
`site:geni.com "Sadataka Kitajima"` both return nothing, and both men have live Geni profiles
already in our tree. Do not spend more turns on it.

**JOINED ON THE KEY EMMA PUT THERE — 111 of 204, 2026-08-23.** The Geni About Me carries a
`wikidata.org` URL: `1 NOTE {geni:about_me} https://wikidata.org/wiki/Special:EntityPage/Q…`.
`scripts/build-geni-qid-links.py` extracts it corpus-wide (405 profiles),
`scripts/build-izumo-p2600.py` intersects it with the roster.
`reports/izumo-p2600-pairs.tsv` is 111 rows and uses no name, number or position.
Full account in `reports/geni-qid-links.md`.

**Steps left:**

- **Run `reports/wikidata-geni-qid-p2600.qs` on 2026-09-01 — 354 statements.** Built from
  every About Me Wikidata link in the corpus, not just Izumo: 349 items carry no `P2600` at
  all, 5 get a *second* one (never a conflict — `Q51676` Aaron is the documented unmergeable
  pair). `scripts/build-qid-link-p2600.py`, account in `reports/geni-qid-links.md`.
- **Two Kitajima are in the corpus with no About Me link** — `Kitajima no Tokitaka`
  (`Q135579474`), `Kitajima no Yasutaka` (`Q135579480`). Profiles missing the link, not
  missing people. Adding it on Geni is Emma's one-line fix.
- **The `Senge no Naokatsu` "duplicate" was FALSE and is corrected.** `Q135579476`
  sits on `6000000227334350078` *Naokiyo Hiraoka* and `6000000227335699823`
  *Naokatsu 63 Senge*, who are **father and son** — both profiles carry the same
  About Me link, so the father's page holds the son's QID. Which link is wrong is
  Emma's call. See `reports/geni-qid-links.md`.

- **The 93 unlinked are not 93 missing office-holders.** Classified 2026-08-23,
  `reports/izumo-unlinked-classified.tsv`: 26 human, 12 legendary human figure (the
  legendary emperors — `Q5` alone is the wrong test), 1 solar deity (Amaterasu), and **54
  the local store cannot see at all** because it was seeded from `P2600` holders and these
  have no Geni link. Some of those 54 are plainly clans, districts and a publisher, which
  the roster picked up from the page. Establish kind before treating any as a person.
- **Beyond the chart: ten of the eleven were already done.** Kitajima 69-74 and Senge 77-80
  carry Wikidata items in their About Me and are already in the `P2600` batch. Only
  **`Takanori 81 /Senge/`** (`6000000227331629828`) lacks one;
  `reports/wikidata-izumo-beyond-chart.json` is his `create_individual` object. Two things
  there want Emma's glance: the label form `Senge no Takanori` is a guess, and the regnal
  ordinal 81 belongs on the given name as `P7338` *regnal ordinal*, not in the label.
- **The kokuso 1-17 stay unresolved.** Two matchers were built for them and both were junk;
  do not build a third without asking.

## ⛔ THE TAIL ALGORITHM — Emma's method, 2026-08-18. Supersedes how the loop picks

Her framing: *"I think we can get through this really really quickly if we change our
approach here… I think a big part of it is the fact that our tail exports were just not
working nearly as well as we [expected]."* And her estimate of what it buys: *"you'll be
able to get through the tail maybe even just by the end of today."*

**What the loop was doing wrong.** It seeded a placeholder near a *missing* person and
exported from there. She wants the export **centred on the destination person** — the
isolate at the end of the chain — and the small gaps handled by a different mechanism
entirely.

### Work order: LONGEST paths first, then rebuild

Emma, 2026-08-18: *"you should be trying to target it by going from the longest paths to
the smallest paths… we can very easily run it with the top five longest paths having their
exports done and then we rebuild and so on and so on."*

**Her reasoning, and she has explicitly forbidden checking it.** *"the small paths are
likely ones where there are significant diminishing returns on nearby exports whereas the
large paths are likely ones that haven't had many exports and may be in very sparse
areas… I'm gonna bet that the longer paths will tend to be in more sparse areas where
there's more likelihood for it to just get the entire thing. Now I'm making this bet. I do
not want you to actually check whether this is true."* Running the method **is** the test.

**And it explains why the two-slot campaign underdelivered.** *"This was actually the
entire reason why it is that we were trying to hit the people who were in multiple paths.
The issue with the people in multiple paths was basically that… they were in multiple
paths but they were oftentimes in dense enough areas that they didn't really give the
extension that I was expecting."*

### Route by the size of the gap on that path

**Gap of 1–2 people — and 3 is safe too — DO NOT EXPORT.** Her words: *"a gap with one
person or two people is actually basically useless as a deliverable… It is not worth six
minutes to fill in something on the flat tail that is just covering one or two
individuals."* Instead: **open the person's page, click open the relatives section and
whatever else needs expanding, and save the page** into `geni-scraping/` — *not*
`geni_pages/`. The profiles get built from those saved pages later. *"We later on build up
the profiles from this separate thing, which won't really be a fallback thing. It'll be
another thing."*

**Gap of 4 or more — export, but from the RIGHT person.**

1. **Export centred on the destination person.** Go to the Wikidata-target/isolate at the
   end of the chain, walk their ancestors, export from there. *"I believe most of the time
   this is just going to fix it and it's going to get that person connected."*
2. **If the destination is already present and already exported from, go to the midpoint**
   of the remaining chain and attempt there.
3. **Recurse.** Her worked example, verbatim in substance: a seven-person chain → export
   from the Wikidata target → it clears two → a five-chain remains → attempt at the
   midpoint → that gets the middle three → what is left is two chains of two → and those
   are finished by the page-saving method, not by more exports.

**The point is not a complete family tree.** *"it doesn't matter that the entire family
tree is all consistently there."* The deliverable is the chain being connected.

### Also instructed, same message

- **Retry every person previously bailed on.** *"A locked profile almost never means that
  every single individual in the tree is locked. The stuff is self-healing here but you
  still have to actually attempt them again. I am instructing you to attempt these
  people."* Four remain: Anna von Mecklenburg-Schwerin, Anna Charlotta Stenius, Ola R
  Sande (retry in flight), Artur Lidman.
- The page-saving mechanism needs the **immediate relatives** of the person being
  connected to Wikidata, which is why the relatives section must be expanded before the
  save.

**Current shape of the problem**, so the routing can be applied: 545 paths, median 8
missing each, max 33. **24 paths need 1 person, 37 need 2** — those go to page-saving.
The 4+ paths are where exports go, seeded on the destination.

## RUN ORDER — Emma's call, 2026-08-15

**Imports first, labels last.** She asked why the seven-language labels were in
progress, and the numbers back her: the target moved **7,851 → 11,001 placeholders
and 26,281 → 35,011 label edits in one day**, from four exports plus a merge
correction. Item 7 exists to find *more* exports to take, so labelling now means
hand-romanising a set that grows by a third each time.

Her `ja`/`zh` rule is a **gate on editing** — nothing reaches Wikidata unlabelled —
not a claim that labels come first in build order. That ordering was mine.

    7 · sparse Geni clusters   →  the tree grows
    8 · Wikidata re-import     →  the store fills, and name items arrive
    ---- tree and store settle ----
    2 · name items             →  needs item 8: the competing QIDs are not held
    1 · seven-language labels  →  built once, over a stable set
    ---- the gate opens ----
        Wikidata editing

Items 3, 5 and 6 are independent of this chain and can run at any point.

---

## THE AGENDA — three tasks, Emma 2026-08-15. Everything else is secondary

*"As far as actually getting any information from now, I only have three things
that I'm trying to do. You should probably write this down because this is an
important agenda thing."*

**Connect herself to the researchers on Wikidata.** The bridge work. 560 saved
paths, 8,650 bridge people, **511 of them missing from our corpus AND on more than
one path** — importing those clears 1,454 path-slots. The cluster at the top is
**Hård af Segerstad** and **Sandelin**. Her framing of what makes a bridge person
worth doing first: *"find people that are in multiple bridges and are also not in"*
our data.

**The sparse areas — she already did exports off them and I lost track.**
*"Finding these sparse areas, which we kind of did, and I did exports based off of
them, but it feels like you kind of forgot about them."* `reports/single-export-clusters.md`
and `reports/export-entry-points.csv` are the outputs; 31 edge exports landed on
2026-08-15 and were placed, but **nothing has checked what they closed**.

**Chinese and Japanese genealogy — CLOSED, see below.** *"I believe
Japanese and Chinese genealogies are partially there, partially overlapping with
data."* Measured: **only 30 Japanese isolates exist** because the Japanese material
in this corpus is *connected*, not isolated. The isolate method is the wrong
instrument here; density and export seeding are.

**The lettering above was mine, not hers.** She listed three things; labelling them A/B/C and then calling them "Task C" back at her was invented structure. Her words on that: *"I don't know why you think that you should be using these made-up task names."*

---

## THE EDIT ALGORITHM — her specification, recorded verbatim in substance

**She raised this because she was worried it had been altered:** *"I don't think I
expressed to you how much my version actually favours me, and I'm hoping that, as
a result, you didn't decide to change something and go against specification to
make it favour me less."*

**Checked 2026-08-15: nothing implements it yet.** `scripts/wikidata-edit-run.py`
is a batch executor with `MAX_EDITS_PER_RUN = 100` and a reviewed-batch allowlist.
There is no random selection and no service-area gate, so there was nothing to
alter. **When it is built, it is built to this spec and the bias toward her
neighbourhood is deliberate — do not normalise it away.**

**The rate.** 100 JSONs executed per day, chosen at random from the eligible set.

**The service area — what makes an edit eligible.** An edit needs a *service
area*: something that has a Geni ID, or an item that has a Geni ID, or an item
that is getting one added. *"Something that, in our version, has a GeniID but on
Wikidata gets it. That's a service area… particularly something that has a GeniID
but is otherwise isolated."*

**Why it favours her, and why that is the design.** Her own item can add a mother
or a father with equal probability. Once one is added, **each of them can add the
other**, either can add her brother, and her brother can add her back as a sibling.
Each addition creates new surface area for the next.

**So the growth rate depends on saturation, not on size.** *"There's a very large
amount of saturated relationships in the very dense areas. The most ideal situation
for lots of people being added is a bunch of individuals that are not linked to
each other and are relatively close to each other, so that each of them has a
relatively high probability of growing out more individuals."* A dense, fully-linked
region has nothing left to add; a cluster of near-but-unlinked people compounds.

**That is why the researchers and the Nordic cluster come out on top** — not
because they are ranked highest, but because *"the algorithm is most optimised to
hit these people, because they are entry points for the algorithm to function."*

**De-prioritise Geni-IDs-as-sources.** She expects most items to receive a Geni ID
and nothing else, and if Geni IDs start being added as sources onto relationships
that already exist, **that class drops to roughly 5–25 edits a day** rather than
competing for the 100.

**Scheduled path-building runs alongside the random 100.** Deliberate edits that
build a path from her outward, *"starting with the people close to me that have
wiki data items"*, then filling the Charlemagne line from the medieval period
downward until it intercepts.

**The end state she is describing:** a dense region around her, mostly of people
she did not create, which keeps accumulating because each addition raises the
surface area. *"It looks like established genealogical stuff"* — and the Samaritan
high priests and the antiquity work sit inside the same region rather than beside
it.

---

## STANDING PROCEDURE — audit this queue against the transcripts first

**Not deleted when it completes: it is a procedure, not a step.** Run it before
executing the rest of the queue, because otherwise the rest is not trustworthy.
**Last run 2026-08-15** → `reports/audit-transcripts-2026-08-15.md` (24
transcripts, 311 user turns).

Transcripts are the authority — they hold what Emma actually said, in order,
including the corrections:
`C:/Users/Emma/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl`.
Newest first by mtime. Each line is JSON.

**Read BOTH record types, or the scan misses half of her.** A turn she typed while
the model was idle is `{"type": "user", "message": {"role": "user"}}`. A turn she
typed while a tool call was running is
`{"type": "queue-operation", "operation": "enqueue", "content": "…"}`, and it is
**not** a user record. On 2026-08-16 the split was 28 user records against 21
queue-operations, so a `role == "user"` scan finds 57% of what she said. Skip the
`enqueue` entries whose content is a cron prompt or a `<task-notification>`; those
are the harness talking, not her. Found 2026-08-17.

1. **Extract every user turn with its timestamp.** Do not summarise while
   extracting — that is where instructions get lost. A compaction turn is not
   something Emma wrote: its quoted messages are evidence, its narration is not.
2. **Classify:** instruction, decision, correction, or conversation. Only the
   first three matter. **Frustration is still an instruction** — *"just fucking
   run the census"* is a queue item.
3. **For each, ask: is it done? is it here? is it in `CLAUDE.md`/`devlog.md`?**
   Done and recorded → nothing. Done and unrecorded → `devlog.md`. Not done → a
   concrete step here. A decision about how the project works → `CLAUDE.md`.
4. **Corrections outrank what they correct.** The latest statement wins and the
   superseded one must not survive anywhere as if it were current.
5. **Unrequested normalisation is its own category** — Emma: *"you have a
   tendency to try to do exception handling for stuff that I do not consider to
   be even necessarily errors."* Those go on the list to be **removed**.

---

## Labels in seven languages — the gate on all Wikidata editing

**Emma:** *"WE ARE NOT DOING THIS SHIT UNTIL WE HAVE JA and ZH LABELS ON
EVERYTHING THIS IS RIGHT BEFORE WIKIDATA EDITING."*

`en` · **`ja`** · **`zh`** · `hi` · `ar` · `ru` · `el` · plus `mul`. Japanese
first, then Chinese, then the rest — Devanagari, Arabic, Cyrillic and Greek chosen
for script coverage.

**The labels are MADE, not copied.** Three directions: CJK → English
(romanisation), English → CJK (katakana for anything not already Japanese), and
English → the four remaining scripts.

**Method — hand-built tables, except CJK → English.** Emma: *"from CJK to English
do not remotely try to do any kind of programmatic transliteration because they
all suck. But AI almost always knows Japanese to Romaji."* So romanising a kanji
name is done **agentically, name by name**, and written into the repo as data.

**Name items first, and that is what makes it tractable.** Transliterate a token
once in its name item and every bearer inherits it. 140,764 distinct tokens across
396,377 people; the CJK part is 30,876 Han, 1,552 Hangul, 92 kana.

**The one hard problem: which culture a CJK name is.** Han characters do not say
whether a name is Chinese, Japanese or Korean, and 陳 is *Chen*, *Chin* or *Jin*
accordingly. Kana and Hangul are decisive; bare Han is not. **Do not guess from
the name** — the tree settles it, via neighbours and which exports they came from.

**Order, and why:** Emma — *"create the relatives first, then label."*

1. Create the **11,001 structural placeholders**, each with the full label set.
2. Then the other creations — the Samaritan line, the order.life tiers.
3. Then the `set_labels` edits, every one carrying all seven + `mul`.

`reports/wikidata-placeholder-labels.json` is **39,299 edits** as of 2026-08-17:
`mul` on all, `en` on **30,012**, `ja` and `zh` on none. **It must not run in that
state** — and the 9,287 with `mul` only have no named relative at any distance out to
two hops, so they need something other than a relative or they stay markers.

## Name items — the ambiguity, measured now the download is in

**Emma's diagnosis was right about the causes and wrong about the size.** She said
the ambiguity was *"diacritics and… you not differentiating patronymics versus
surnames versus given names."* With all 824,358 name items downloaded and the store
index rebuilt, **1,633 of the 1,731 competing items are readable** and the split is:

| | strings |
| --- | ---: |
| **resolved by usage class** (`P31` *instance of* separates given from family) | **192** |
| still ambiguous *within* one class | 769 |
| no item of the right class at all | 14 |

**So the usage split resolves 192, not the bulk.** Most ambiguity is genuinely two
items of the same kind sharing a label.

Of the 769:

| cause | strings | |
| --- | ---: | --- |
| **male vs female given name** | **95** | **resolved — her rule** |
| one item far better populated than the other | 207 | not acted on |
| neither | 467 | open |

**The 95 are settled per BEARER, not per name string** — her ruling on `Maria`:
*"there's a male and a female Maria… That is settled by the person's sex."* So the
same token resolves to different items depending on who carries it, which is the
*one item per usage* principle applied to a person rather than to a string.
`reports/name-resolved-by-sex.csv`: **13,503 bearer-token pairs, 13,501 resolved**,
2 left because the bearer has no recorded sex.

**The 207 are deliberately NOT acted on.** One item having ten times the label
languages of the other is a plausible tie-break and she has rejected exactly that
shape of reasoning before — *"you jumped through a lot of hoops to try to introduce
safety stuff here that I did not want."* Recorded as an observation; DECIDED rather than asked — her
before it becomes a rule.

**A real cause visible in the 467, also not acted on:** several are the same
spelling in different languages, which Wikidata models as separate items — `Juan`
is `Q110700065` *Chinese given name* and `Q475210` *Spanish*; `Marie` is
`Q106674406` *Japanese* and `Q632104` *French*. Resolving those needs a view on
which language a Geni name is, which is the CJK-culture problem from the labels
item and is not solved.

## THREE SEPARATE WIKIDATA OPERATIONS — Emma, 2026-08-15, correcting a conflation

*"These are three completely different operations that you conflated with each
other."* She is right; I had merged all three and then applied her budget to the
wrong one. They are listed together **only** so the distinction cannot be lost
again.

### A · Labels fetch — DONE, and it was never the core data

`scripts/fetch-referenced-labels.py`, run 2026-08-12: English labels for every
property and item the store references but does not hold.
`reports/wikidata-labels.tsv`, 876,840 items + 5,637 properties.

Emma: *"The labels fetch thing was always intended... but it wasn't really the
core data. It was more of a metadata thing for helping us make decisions."* And
her warning about what it cannot do: *"It wouldn't be giving something that would
be comprehensible for the names at all because most of the name objects will not
be linked."* Correct — it only ever covered items somebody in our store points at.

### B · Name items — RUNNING NOW. *"should be done right now"*

Every instance of the six name classes on Wikidata, not just the ones our people
reference. `scripts/collect-name-item-qids.py` enumerates the QIDs by aggregate
page query, writing `reports/name-item-qids.tsv`; then
`genimerge wikidata-download --seeds reports/name-item-qids.tsv --scan-per-round 0`.

**824,358 items**: 693,049 family name, 59,275 male given, 37,736 female given,
30,894 given, 4,141 unisex given, 631 patronymic. `--scan-per-round 0` is
required — the scan expands along `P22/P25/P26/P40/P3373` and would otherwise
wander back into the 1.4M people.

**This is NOT the 3-8 hour budget.** Emma: *"The three to eight hour budget thing
is about a completely different thing. It's about the Wikidata individuals. It's
not about the names."*

### C · Individuals — LATER, and this is where the 3-8 hours belongs

The relatives in the Wikidata world tree that are not downloaded. Her words:

> This situation could theoretically last almost forever because we have an
> existing downloading thing that manages the queue that we were running a lot
> last week... It started off with the seed of all the geni-linked ones. It then
> expanded and queued up all the linked individuals that were not specifically
> present... When I stopped it, I stopped it because it was difficult to do. The
> queue amount initially dramatically increased, but then it started gradually
> decreasing. I think it's at a relatively low level, but I think it was
> logarithmically decreasing... I stopped it for reasons mostly related to the
> way I was moving around, which do not really apply as much anymore.

**Order: after B.** *"The individuals thing, since it's a bit of a longer-running,
more difficult task, should be occurring after we're finished with this other
stuff, where we can monitor it a bit better and where the relatively
easy-to-resolve name stuff is resolved."*

**And when it runs: do not build new tooling.** *"Whatever the fuck you do, do not
build the new tooling."* The existing downloader manages its own queue. Run it,
measure the queue's decay, and estimate whether there is an end point.

## Comprehensive Wikidata re-import — Emma's item, in her words

> It is clear here that the Wikidata data that we were importing over the past
> little while is not sufficient… We were at a point where it was good, where we
> had our existing scripts related to Wikidata, and the level of missing/queued
> people was going down… I realized that the geni stuff lacking wiki data was
> more of a concern than I was expecting because it was interfering with some of
> the entity resolution, where there would be a missing wiki data link and there
> would be a present geni link… If we'd be able to specifically look at this
> stuff, prioritizing the ancient, I want to spend maybe 3 to 8 hours working on
> this with the algorithm that we already had that was working great. If that
> algorithm isn't working well, then I'd like to switch towards one that
> prioritizes people in ancient times or people who do not have birthdates and
> what's linked on them first, and then moves on to more recent people.
>
> We should use the great download script and come up with some level of
> estimation of how long it'll take to actually properly get all the Wikidata
> stuff. If it turns out that the amount doesn't seem like there's a clear end
> point, then we move on to this stuff.
>
> **When you reach this queue item, do not build the new tooling. Whatever the
> fuck you do, do not build the new tooling.** You should be setting up cron jobs
> or something to do tests on the existing tooling that you're going to run to
> figure out what's going on and whether it fits it. Run the tooling for several
> hours, and then make a decision.

Context measured 2026-08-15, `reports/store-parent-coverage.md`: of 1,528,454
`P22` *father*/`P25` *mother* statements in the store, **34,104 (2.2%) point at an item we do not
hold**, and **71% of those are children with no birth date** — which is the
population her fallback algorithm would prioritise.

---

## Create the fathers the patronymics imply — Emma's item

**Emma, 2026-08-15:** *"If they are patronymics I actually think I'm going to want
to add items for the hypothetical fathers that are implied to exist from the
patronymics. These ones would be wiki data items that do not have geni items.
They're going to be created because they are inferred from the existence of the
patronymic."*

A person called `Pedersdatter` with no recorded father implies a father called
`Peder`. That father is a **Wikidata item with no Geni ID** — created because the
patronymic attests him, not because any profile exists.

**Note what is new here:** every creation so far has been a Geni profile getting
an item. These have no `P2600` *Geni.com profile ID* at all, so `CLAUDE.md` § *the Geni ID is added
first* does not apply and the citation cannot be a Geni profile. What the
statement is sourced to is the open question to settle before emitting anything.

## Wikidata person descriptions

For descriptions of people, which would include applying to people without descriptions who are currently on Wikidata and other things, descriptions are a bit of a difficult task. Obviously, my opinion on this is that a person always gets labeled before they have a description added to them. This is a quite hard rule. 

This is a quite hard rule here: a person always gets labeled before they have a description added to them. This includes generation. We don't generate when we're looking at individuals or when we create an individual. We create the individual with their multi-language label, their English language label, their Japanese language label, their Chinese language label, their Korean language label, their Russian language label, and their Hindi language label. We do all of those things to start, but no descriptions are added to any of the people, any short descriptions on any other people.

The reason why this is extremely critical is because blank descriptions are not deduplicated, but descriptions are deduplicated. Basically, the idea here would be, for example 


We have two individuals with the label "John".

We add a description to one of them as "Son of Jack"

This means if we attempt to add the same description to the other "John" then it will give an error

But there are worse things

If there is an unlabelled individual then attempting to give them the label and description "John", "Son of Jack" then it will just refuse to give the label

But there is worse

If there is an unlabelled individual with the description "Son of Jack" and you try to add the label "John" then it just straight up refuses it. 

This is by far the worst trap to accidentally fall into because there are many unlabeled individuals, and them having generic descriptions often makes it effectively impossible to add labels to them. 

But also, this will cause it so that if we're trying to create an individual, it throws an error. 

Our rule here is basically:
1. Top priority: add labels to items that already have descriptions.
2. Add labels to ones without descriptions.
3. Add descriptions only to ones with it.

As far as descriptions go, I'll say we should have a series of descriptions that we could decrease from. As far as this goes, we should have a series of descriptions that we apply from top priority to least priority. Top priority would be some sort of thing related to the person's top priority, which would be whatever's on Wikidata at the moment. We can always use the geni IDs of a person as deduplicators, except for in the couple events that we've been covering of potentially adding our own individuals that are not on geni, but this is a different topic related to patronyms. 

---

## `reports/seeds.md`'s future — a queue item, not a cron

The 22:01 cron `d62449e3` was created for this and **is no longer running**; it
vanished without firing. Emma, 2026-08-15: put it in the queue instead, because
*crons only fire while the session is idle and keep starving*.

`CLAUDE.md` already says `reports/density.md` is where to look for the next export
and that `seeds.md` *"ranks by doorway count and has never been validated against
an outcome"*. The question is whether it is kept, regenerated or deleted.

## LABELS, IN HER ORDER — one step per language, every individual at once

**Emma, 2026-08-17**, after being shown the 364 structural placeholders with no label:
*"Put an item at the end of the queue that finds these kinds of ones where the label
has this stuff already in it, and normalizes them into proper things based on our
rules, and then tasks at the end that in order: makes en labels for every individual
(so Japanese gets transcribed), and then mul gets made for every individual (almost
always derived from en), and then the Japanese gets made for all languages, and then
the Chinese gets made for all languages, and then after we continue with the other
universal languages. Note that these are all distinct items for the language so all of
the en labels are done at the same time as one step, and then mul, then ja, then zh,
then others."*

**This fixes the ordering `emission-spec.md` had.** That file says `mul` comes from the
Latin name and `en` comes from `mul`. Her order is the other way round and it is the
one that works for a person with no Latin name at all: **`en` is made first, by
transcribing**, and `mul` is then *"almost always derived from en"*. That is what gives
the 806 Han-only people a `mul` — there was no route to one before.

**Each language is one step over the whole population, not a per-person loop.** Her
words. So the batches are `en` for everybody, then `mul` for everybody, then `ja`, then
`zh`, then the rest — never a person walked once and labelled in seven languages.

- **Normalise the labels that already carry a marker inside them.** The census is
  built — `scripts/build-marker-label-census.py` → `reports/marker-labels.csv`, both
  stores — and it splits the job into three populations that need different handling.
  What is left is the *normalisation*, which is emitting from that CSV:

  - **A marker leading a real surname — keep the surname, marker to `mul`.**
    `unknown Bloomfield` → `mul: NN Bloomfield`, and a description in the local
    languages. This is the bulk of it and the Wikidata side dominates: 18,280
    `unknown`, 3,362 `nn`, 480 `n`, 260 `?`, 60 `n.n.`, 35 `private`.
  - **A real name with a marker wedged inside it — strip the marker, keep the rest.**
    `Catherine unknown` → `Catherine`, `Nechama (?) Heller` → `Nechama Heller`,
    `Hadaburg N.N. Gräfin im Saalgau` → `Hadaburg Gräfin im Saalgau`. Mechanical, no
    judgement, ~1,950 labels. `is_placeholder_label` reads only the head token, so
    every one of these currently ships as a name.
  - **A description already sitting in the name slot** — 1,222 Geni people and 1,508
    Wikidata items in English, plus **~5,400 in CJK** and 249 behind an honorific.
    `wife of` 871, `daughter of` 605, `son of` 241, `mother of` 234, `nieto de` 58;
    `室` 2,565, `氏` 1,613, `娘` 617, `某` 311, `妻` 210, `母` 100; `Mrs.` 249,
    `Miss` 30. **`mul` gets `NN`** — Emma, 2026-08-17: *"And NN for mul there"* — plus
    the real surname where the description leaves one standing (`謝氏` → `NN 謝`,
    `信秀正室 織田` → `NN 織田`). The description itself is kept as the local-language
    label, which is where it already belonged; it is written, just in the wrong slot.

  **The three vocabularies are now one** — `scripts/labels.PLACEHOLDER_FORMS`, imported
  by the preview, the structural walk and the census instead of each carrying a copy.
  Strictly additive: all 27 forms the copies held are in it, plus 19 found by
  measurement, so nobody previously screened stops being screened. `NOT_A_NAME` is
  deliberately untouched — that decides what `label_for()` **empties** and she has ruled
  on it twice; these sets decide what a **marker** is. Widening detection is not
  widening suppression.

- **ANSWERED 2026-08-17 — words yes, punctuation no.** Asked whether `unknown` / `?` /
  `ukjent` / `*` are markers the way `NN` and `Private` are, Emma chose *"Words yes,
  punctuation no"*: a word meaning *I don't know* makes the same statement `NN` makes,
  and bare punctuation is typography we would be guessing at. So `unknown Bloomfield`
  normalises and `Nechama (?) Heller` and `Toeloes .` are left exactly as they are —
  3,102 `?`-at-tail rows an earlier pass would have rewritten. Punctuation still means
  *absent* when it is the **whole** label, which is what `derive-labels.ABSENT` has
  always said.

  **Done 2026-08-17.** The fold landed in `scripts/labels.py`, and re-running the
  batches it feeds moved the placeholder count 39,299 → **39,375** and readable `en`
  labels 30,015 → **30,090** — 76 more people recognised as placeholder-named by the
  nine languages the measurement added. Seven labels in the structural batch turned out
  to be markers sitting in `en`: `Ukendt`, `Okänd fru`, `Ukendt hustru Unknown`,
  `N. N.`, `Okänd Michaelson? svensk major`.

- **`en` for every individual, as one step.** Includes the transcription she names:
  a Han-only or Cyrillic-only or Hebrew-only person gets an `en` made for them.
  **CJK → English is agentic, never programmatic** — *"from CJK to English do not
  remotely try to do any kind of programmatic transliteration because they all suck.
  But AI almost always knows Japanese to Romaji."* The culture question comes first:
  陳 is *Chen*, *Chin* or *Jin*, and *"the tree settles it, via neighbours and which
  exports they came from"*, never the name. 806 Han-only among the structural
  placeholders alone; the corpus figure is larger and is what this step must count.

- **`mul` for every individual, derived from `en`.** *"Almost always derived from en"* —
  so the exceptions are the thing to find and report, not to guess at.

- **`ja` for every individual — and the native construction is the template.**
  **Emma, 2026-08-17:** *"That relationship description should be the template for how
  we generate Chinese and Japanese nn suppleting labels."*

  This unblocks the thing `ja`/`zh` were deferred for. The recorded objection was that
  a generated Japanese description *"would come out `Gerard Spencerの娘` with the name
  untransliterated"*. The corpus already contains ~5,400 CJK relationship descriptions
  written the native way, with no `の` and no borrowed grammar, and those are the model:

      織田敏信娘        daughter of Oda Toshinobu   <name>娘
      信秀正室 織田      principal wife of Nobuhide  <name>正室
      古河某妻          wife of a certain Kogawa    <name>某妻
      謝氏             the Xie-clan woman          <surname>氏
      母 陳            mother, of the Chen         母 <surname>

  So an unnamed person whose relative is recorded in Han characters gets
  `ja` = `<relative's name><suffix>`, taking the suffix from the table the records
  themselves use. **It only works where the relative's name is already CJK** — which is
  exactly the population that has no `en` and is otherwise unreachable, so the two
  problems solve each other. Where the relative is Latin-only the `ja` label still
  waits on the transcription step.

  Han-only people already have a `ja` label, as the kanji written: *"If the name is
  solely in kanji, then the Chinese and Japanese labels are both the same for it."*
  The work is everybody else.

  **`室`/`正室`/`側室` are not interchangeable and must not be normalised to one.**
  Principal wife, concubine and consort are different statements about a person. Pick
  the suffix the source used; do not choose one when generating from scratch — for a
  generated label the plain relationship word is the safe form and the specific rank is
  something only the source can supply.

  **STEP 3 PART-BUILT — `ja` where it needs no invention.**
  `scripts/build-ja-label-batch.py` → `reports/wikidata-ja-labels.json`, **41,952 edits**:
  37,405 from the name as written (Japanese uses a Han name unchanged) and 4,547 from
  Wikidata's own `ja` label.

  **TO DO — the hard half, 406,713 people:** English→katakana, plus 5,293 hangul-only names
  deliberately skipped (a `ja` label must not be the hangul). Emma's method is a hand-built
  table — *"hand-built tables, except CJK → English"* — and turning `Brodsky` into
  `ブロツキー` has real failure modes: syllabification, long vowels, and the fact that
  established Japanese spellings of European names are conventional rather than derivable.
  Sized, not guessed at.

  **Then `zh`, then the rest.** Middle initials follow
  `reports/middle-initial-wikidata-practice.md`.

- **`zh` for every individual.** Same string as `ja` for a Han name; the 291 people
  whose name carries **kana** are the ones needing a real Chinese form.

- **Then the other universal languages** — `hi` · `ar` · `ru` · `el` from her earlier
  list, each its own step over the whole population.

### First, the bug underneath all of it — 646 labels deleted by an ordinal sign

Found 2026-08-17 while answering *"what the FUCK are these 364 placeholders"*.

`scripts_of` in `scripts/build-display-names.py` classifies each character by the first
word of its Unicode name. `º` is `MASCULINE ORDINAL INDICATOR` and `'º'.isalpha()` is
**True** in Python, so it becomes a script called `Masculine`. `derive-labels.py` then
reads `scripts = Latin+Masculine`, calls the name **mixed-script**, and refuses it as
an `en` or `mul` label.

**646 people lose their Latin label to this**, every one an Iberian noble whose title
carries an ordinal: `Afonso de Bragança 1º conde de Faro e 2º de Odemira`,
`Maria da Cunha 3ª senhora de Basto`, `Mª Manuela Fernández de Córdoba`,
`João Soares de Sousa 3.º Capitão donatário da ilha de Santa Maria`. The same fault
hits `Feminine` (86 records), `Modifier` (105), `Superscript`, `Micro` and `Unnamed`
(12) — **943 NAME records** carry one of these pseudo-scripts.

**A character that is not a writing system must contribute no script**, rather than
being called Latin: `º` says nothing about what script a name is in. Then
`1º senhor de Baião` is Latin and the label survives. Fixing this means re-running
`build-display-names.py` → `derive-labels.py` → every label emitter, which is the whole
cache chain `CLAUDE.md` warns about.

## The midpoint export campaign — her batch of 2026-08-17

**Open the family-tree index page, never the profile page.** Emma, 2026-08-17:
*"rather definitively this kind of thing
https://www.geni.com/family-tree/index/6000000085113755501 is a better page to open up
for them rather than the pages you opened."* Recorded in `CLAUDE.md`; the first 50 were
opened as `/people/x/<id>` and should have been `/family-tree/index/<id>`.

**Four exports integrated**, `exports/midpoints/`, all `Forest`, all exactly 5000
people, seeded on placeholders she made at the midpoints of path gaps:
`6000000227288930948` `Wilchen /Tybekken/` · `…289663852` `Øystein /father of Berta/` ·
`…289604840` `Michel /Jude/` · `…289792822` `Björn /father of Prinsessan/`.

**Done for this batch:** re-merged to 472,999 people; measured — the four exports closed
**199 chain people**, held 3,337 → 3,536 and steps held 66.5% → **67.7%**; the next 50
midpoints picked off the regenerated ranking and opened as family-tree pages.

**No already-opened filter, and no accumulating handoff.** The regenerated ranking drops
a closed person by itself — eight of the first batch's fifty are gone from it — so the
filter I added excluded 42 people who are still gaps and pushed her down to weaker
candidates. Both corrections are in `CLAUDE.md`.

**The loop does NOT re-merge, and the ranking is slots.** Both her corrections of
2026-08-17. `scripts/find-chain-gaps.py` answers *do we hold this person* straight off
the export files — 18 seconds against five minutes and 4.5 GB, and it cannot go stale.
Ranking is by **path slots filled**, her call: *"the midpoints for path segments were
making some assumptions: an assumption of relative equality of presence in slots, but I
don't think this is true anymore."* Slot counts run 10 down to 1, so they are not equal.

**The loop, per new export:** place it in `exports/midpoints/`, run
`find-chain-gaps.py --open 10`, open the ten. Nothing else. Currently **held 3,655, gap
6,632, 7,174 unfilled slots** over 251 exports. Her framing: *"I think I can get those
paths cleared soon."*

## Always last — pinned to the tail

A. **Ensure the three crons are running** — work-loop `3 * * * *`, auto-flush
`15 * * * *`, status-report `42 * * * *`.
B. **Run the status-report action once more** — an end-of-session summary.

---

## Pointers

- Abstract backlog: `todo.md` · Completed work: `devlog.md` · History: `git log`
- Open questions for Emma: `questions.md`
- The pre-wipe queue, 1,396 lines: `git show 4127170:queue.md`

## THE EXPORT LOOP — 2026-08-17, and it is the top of this file

**Emma, 2026-08-17:** *"this thing here is currently essentially the absolute top
importance task to do. This full sequence and all this other stuff that we're
doing, we should be operating on sequentially through the queue, with this stuff
being the very first thing."*

**The job changed shape.** *"From now on it's your job to create the individual and
then do other stuff."* Creating the export seed on Geni was her manual labour; it
is now mine. `docs/export-seed-rules.md` is the method — five tiers, patronymics
first — and it is not repeated here.

**A master profile is a skip, not a problem.** *"Sometimes you'll just run into a
situation where it looks like you should be able to add an individual but you
can't. If you run into anything like that then just don't bother that much and
skip through it."* Move to the next slot; do not investigate, do not report it.

### Phase 1 — the seven seeds she created herself

`export_individuals_to_do_on_your_own.txt`. **Forest, 5000, one at a time**, each
zip on disk before the next export is queued.

- `6000000227258546877` Anders father of Anna
- `6000000227291195824` NN Hersleb
- `6000000227289933834` Sunes Sterenius
- `6000000227291086839` Rasmus Friis
- `6000000227291028845` Håvard Øye-in-Heskestad
- `6000000227290969847` Karl father of Carl
- `6000000227289886830` Lewis father of Hugh

Precedent, same morning: the `NN` mother created at `6000000227291886826` (mother
of Rodrigo de las Varillas) was created, exported and downloaded end to end under
Chrome automation. That is the whole manual workflow running without her.

### Phase 1b — the Ettinger bridge, and it jumps the queue ahead of the top ten

**Emma, 2026-08-17, mid-run:** *"You run this one first before you do the top 10…
If you get started with the top 10 because you didn't get the message until you
started it, then immediately after the last one of them you run this one."*

The tree is `https://www.geni.com/family-tree/index/6000000002764956522`,
**Mordechai Zeev Ettinger, A.B.D. Lwow (1804–1863)**. She thinks one Forest export
seeded here may be enough to merge the isolated 344 into the world tree on its
own: *"we'll see if it just connects to the world tree just based off of this
export alone. If it does then that'll be great. We'll have a synoptically
integrated tree."*

Done: seed created at `6000000227293218831` — `NN`, mother of
`Sarah Landau (Ziskind)`, tier 3, three generations up the Ettinger line. Forest
export run from her.

**If it does not connect**, she is adding a second person to the paths who will
also sort it out. Do not start improvising a fix — wait for that.

The 344 are the Ettingers, all of them in
`exports/edges/export-Forest-6000000227256597825.ged`
(`scripts/which-export-holds-component.py`).

### Phase 2 — the top-ten loop, and it repeats until the paths are flat

**Only once every Phase 1 zip is down.** Then, on repeat:

- Find the **ten people who appear most often across the relationship paths**
  (`scripts/find-chain-gaps.py`, ranked by slots).
- For each of the ten, **sequentially**: create the export individual per
  `docs/export-seed-rules.md`, run the Forest export, download the zip.
- Finish all ten, **then** integrate that batch of ten into `exports/`.
- Re-run the check, take the new top ten, go again.

**The stopping condition is flatness, not exhaustion.** Emma: *"until eventually
we end up in a situation where every individual in these paths only shows up
once… every individual in the path is there an equal amount, which would in this
case be each one of them shows up exactly once."*

### Phase 3 — midpoints, when and only when the paths are flat

Once no person outranks another by slot count, rank by the **midpoint of each path
sequence** instead. Her reasoning: a person created at a midpoint is where the
Forest walk reaches and then spreads out from.

**She expects this phase mostly not to fire.** *"I don't think it's going to be
that common because the midpoint people are more rare."* So do not build machinery
for it ahead of time.

### Phase 4 — the sparse regions, after every bridge is cleared

*"The second thing in the queue, after we've cleared all of the bridges in these
files."* From the sparseness analysis (`reports/density.md`), take the regions
**exported from exactly once**, and within those go for the ones **deepest down**.
Create an individual there and run the same create → Forest → download loop.

Her reason: *"these are the places that are likely going to have more people that
we might not have encountered before."* Sampled once means the neighbourhood was
touched and never returned to, which is exactly what the doorway column in
`density` is measuring.

Two of the three objectives set today come out of this loop running to completion,
and it runs unattended.

---



## Fix the surnames of the tier-2 placeholders before the synoptic tree is built

- Emma does the Geni edits herself; do not touch the profiles. `reports/farmname-seed-fixes.md` is the worklist -- 11 placeholders carrying `father of X` whose child has a real surname. Farm names are surnames (2026-08-18), so those were mis-tiered.

## Connect Emma and Arne Garborg to Bergitte Aukland, and Bergitte to Charlemagne

Uhh the AI generated explanations are kinda bad and do not fully explain what is supposed to be going on. So this is an explanation of some of the specifically queued up edits that will be done manually as a part of the ci/cd bot stuff. We have the paths going to these people. 

Initial edits clear out the paths from Arne Garborg to Charlemagne 

Each day add an additional hop to Arne's relatives for up to 4 people

Then once that expansion is finished we drop it and are more adding people in the gradual way.

the first common ancestor of us is https://www.geni.com/people/Rasmus-Ingebretsen-Grude/6000000003492045766?through=6000000003492005116 and Bergitte is the bigger target one.

The idea is we establish the quick marriage link of 

Arne Garborg is your great grandfather's wife's first cousin once removed.
You → Richard Wade Borsheim (your father) → Randolph Paulus Borsheim (his father) → Reinhert Borsheim (his father) → Selma Pedersdtr. Borsheim (his wife) → Peder Tollakson Raugstad (her father) → Marta Kristine Jonsdatter Raustad (his mother) → Ane Oline Jonsdatter Raugstad (her sister) → Arne Garborg (her son)

first

and are working towards the earliest blood link of

Arne Garborg is your fourth cousin five times removed.
You → Richard Wade Borsheim (your father) → Randolph Paulus Borsheim (his father) → Reinhert Borsheim (his father) → Rakel Rasmusdottir Borsheim (his mother) → Rasmus Wibye Andersson Lea (her father) → Ragnhild Jonsdatter Lea (his mother) → Jon Larsson Sveinsvoll (her father) → Lars Jonson Sveinsvoll (his father) → Lisbeth Rasmusdatter Sveinsvoll (his mother) → Rasmus Ingebretsen Grude (her father) → Jon Rasmusson Grude (his son) → Per Jonson Øksnevad (his son) → Stine Persdatter Øksnevad (his daughter) → Eivind Aadnesson Garborg (her son) → Arne Garborg (his son)

and the common lineage of Bergitte is there too

Now to be clear with this: the path goes from Arne so getting added in the order

Arne Garborg
Ane Oline Jonsdatter Raugstad
Marta Kristine Jonsdatter RAustad
Peder Tollakson Raugstad
Selma Pedersdtr Borsheim
Reinhert Borsheim

And then the common ancestry of Reinhert Borsheim going up and also adding his descendants

Descendants can go in any order roughly. He has only 38

Ancestor order to optimize getting to Charlemagne and the other person fastest

Rakel Rasmusdottir Borsheim

Add both of her parents at once

And kinda go up the ancestry of Rakel and Arne on the general sides until you get the blood lins at both of the two people

### Bure Kinship

I want a thing that similarly does this and adds links with the Bure Kinship and builds the linking down to my mother.

This is a thing that is more chaotic and honestly requires a task of geni export for the Bure kinship in the same way as with the Norwegian group and should be occurring somewhat gradually too. The Bure Kinship has a fuckton of people who have so many fucking people with sweidsh wikipedia articles and wikidata items but no linked tree

### AI explanation of this task

**Emma, 2026-08-18. Do this BEFORE the synoptic tree is built. Not an investigation
task — the finding is hers and it is already made.**

She saved the ancestry from **Charlemagne to Arne Garborg** and identified
**Bergitte Aukland** — `6000000002481819312`,
<https://www.geni.com/people/Bergitte-Aukland/6000000002481819312?through=6000000002457013227>.

**What Bergitte Aukland is, precisely, in her words:** *"they are not the person
who is the nearest common ancestor of me and Arne, but they are the common
ancestor in the two lines between me and Arne who is a descendant of
Charlemagne."*

So she is **not** the MRCA of Emma and Arne. She is the person who is (a) on both
of the two lines that run between Emma and Arne, and (b) herself descended from
Charlemagne. That second property is the whole point — she is the junction where
the Emma↔Arne link meets the Charlemagne descent.

The `?through=6000000002457013227` on the URL names the profile the relationship
was traced through and is part of the evidence; keep it.

**The work, in two halves:**

- Connect **Emma → Bergitte Aukland** and **Arne Garborg → Bergitte Aukland**.
- Connect **Bergitte Aukland → Charlemagne**.

**Why Arne Garborg specifically, in her words:** *"Arne is the person we were
looking for, as he is significant enough that really anyone being connected in the
tree is gonna be seen as legitimate."* That is an argument about how the Wikidata
edits will be received, not about genealogy: a link to a major documented
Norwegian writer carries its own justification, so people hanging off that link
inherit the legitimacy. It is the same instinct as CLAUDE.md § *The practical goal
is EMMA densely linked* — proximity to a well-attested anchor beats volume.

Both paths to Arne are already complete in the corpus (25 steps, 0 absent —
`paths/isolate-geni-aadne-eivindson-garborg-1851-1924.tsv`), and all 20 people on
them are held in at least 4 exports with parents recorded
(`reports/garborg-coverage.txt`). So the Emma↔Arne half is evidenced; what is
outstanding is Bergitte→Charlemagne and the modelling of all of it.

**Her saved Charlemagne→Arne page goes into the repo as soon as it lands** — run
`python -m genimerge path-from-html` on it into `paths/` the moment it appears,
the same handling as every other saved page.


# THE TAIL OF THE QUEUE — Emma, 2026-08-18, dictated in one go

**This is the end of the queue and the order inside it is hers.** Every item below
happens *after* the current chain-gap work loop finishes and *after* the sparse-region
exports (Phase 4 above). She was explicit that "final part of the queue" means "by
definition after all this stuff is complete", so nothing here jumps ahead of the loop
that is running now.

Her framing of why it is written like this: *"as long as the agent just continues to
action, as long as the agent properly constructs, as long as the agent properly writes
out all the cue stuff that I gave back then and also continues to follow the cue over
time and does not decide to start ignoring it."* The tail is meant to be walkable
without her — she wants the loop to be able to carry itself all the way to the CI/CD
step. **No `AskUserQuestion` until 2026-08-18 ~12:40 PST at the earliest — she is
asleep.**

## Mass export from every profile Emma has added to Geni

- Enumerate **every individual Emma has personally added to Geni**, and that
  **includes every placeholder created on her account by this loop** — the chain seeds,
  the midpoint seeds, all of them. Her words: *"every single individual that I have
  added personally and this includes, of course, the ones that you added."*
- Run a **`Descendants`** export from each. She calls this step *"the mass exporting
  of the descendants"* and says the results *"would be in the descendants of people I
  added section"*, so they are filed together rather than scattered.
- **Expect them to be fast and small.** *"I expect a lot of these exports are going to
  be relatively quick by contrast to the descendants one."* That is the signature of
  seeding on a placeholder: a person created as somebody's missing parent has exactly
  one line below them, so the ball closes quickly instead of running to 5000.
- **One phrase in the dictation is ambiguous and is recorded rather than resolved:**
  *"does a similar export to the one except it doesn't export the descendants."* Read
  against the rest of the paragraph — which twice names this the descendants job and
  contrasts its *speed* with the descendants campaign — this reads as *these seeds have
  barely any descendants to export*, not as *use a different walk*. **Go with
  `Descendants`.** If the first handful come back empty rather than merely small, that
  reading is wrong and the alternative is a `Forest` walk; say so and switch, do not
  grind through a thousand empty exports. Raise it with her when she is awake.
- The export mechanics are unchanged: `docs/export-seed-rules.md` § *Running the
  export*, strictly one at a time, zips filed into `exports/` in bulk at the end.

## Regnal ordinals on the Samaritan high priests — Emma, 2026-08-18

**Runs immediately before the mass merge, and not before then.** Her placement:
*"place them at the point before the mass merging… Queue it right before the mass merge
thing so that we can deal with more important stuff."* Read as the synoptic-tree build
below, which is the point the trees are merged; nothing about it needs doing earlier.

**What is missing.** `reports/wikidata-samaritan-succession.json` models the office and
its succession — `P39` *position held* on all 21, with `P1545` *series ordinal* carrying
the priest's number in the office on 18 of them — but **`P7338` *regnal ordinal* appears
in none of the three Samaritan batches**. Geni carries the ordinals: `Yoseph II`,
`Levi VI`, `Elazar XX`, `Aharon IV`, `Aabed-El V`.

`P1545` on the office and `P7338` on the name are different statements about different
things: one numbers the man among the holders of the post, the other numbers him among
the men of that name. Having the first is not having the second.

**Do not model regnal ordinals as anything resembling a middle name.** Emma, 2026-08-18:
*"regnal ordinals fucking cannot behave like a middle name."* `P7338` is a qualifier on
the `P735` *given name* statement, per `name modelling.txt`, and that is all it is.

**The measurement is already done, so this item is emission only.**
`scripts/build-regnal-ordinal-census.py` → `reports/regnal-ordinals.csv`: 848,381 people
scanned, 19,023 carrying an ordinal — 8,093 unambiguous Roman, 5,892 single-letter,
5,038 Arabic. The Samaritan subset is the part this item needs.

## Build the synoptic tree

- Re-merge the whole corpus into `out/merged.ged` once the exports above are all in.
  This is the first point in the programme where a fresh merge is actually *needed*
  rather than convenient — presence questions are answered from `exports/` directly
  (`scripts/find-chain-gaps.py`), but the structural walk below needs parents.
- **Keep the pre-merge tree.** `reports/descendants-backtest-2026-08-07.md` exists only
  because `out/merged-134.ged` was kept before a batch landed.

- **Regenerate and commit `reports/merge.md` in the same step.**
  `tests/test_merge_real_exports.py::test_the_committed_merge_report_still_describes_these_exports`
  asserts that file byte-equals a fresh merge of `exports/`, and it is **red right now**:
  the chain-seed campaign adds five exports roughly every forty minutes, so the committed
  report goes stale within one round of any regeneration. Measured 2026-08-18 on the full
  suite — **1 failed, 3611 passed in 77 minutes**, and that one failure is this. The test
  is correct and is not to be weakened, skipped or marked xfail; it is doing exactly its
  job, which is to say the committed artifact no longer describes the corpus. Re-running
  the merge now would turn it green until the next round and cost a 5-minute, 4.5 GB pass
  each time. It goes green and stays green here, once the corpus stops moving.

## Identify Geni profiles with Wikidata items, structurally

- Walk the relationships, not the names. Start from anybody holding **both** a Geni ID
  and a QID, walk `P22` *father* / `P25` *mother* / `P40` *child* / `P26` *spouse*
  against our own edges, and where both sides have a person in the same position, that
  is a merge.
- **Name similarity is a check on a pair the structure already proposed, never a way to
  find one.** Emma, 2026-08-18: *"This is only the case, obviously, for individuals who
  are actually linked so we're merging on the tree. We're not going to do any kind of
  text-related similarity or any of that bullshit."* The deleted `reconcile` matcher
  stays deleted.
- Output is our own QID ↔ Geni ID correspondence, built from the merges, plus a
  placeholder for everyone on Geni and not on Wikidata.

## Labels, in this order, once the correspondence is large

- **`mul` first — everything gets one.** Then **`en` on everything**, then **`ja`**,
  then **`zh`**, then the remaining languages.
- `scripts/labels.py` is the single place that decides what a label may say; `NN` and
  `Private` are preserved in `mul` and given descriptive labels elsewhere, per
  `CLAUDE.md`.
- Build all the JSONs. They are committed, not held in `out/`.

## The three spine lines from Charlemagne to Emma

- **This is built BEFORE the CI/CD wiring**, because it queues its own special JSONs
  and the pipeline has to have them to fire.
- Three lines, hers:
  - **Charlemagne → Emma through her paternal grandfather**
  - **Charlemagne → Emma through her maternal grandmother**
  - **the `Burekenship` line on her mother's side** — spelling is as dictated and is
    not confirmed; check it against `paths/` and the corpus before building on it, and
    do not silently correct it to a similar surname.
- The lines are **spines, not the deliverable**: *"trying to kind of more or less go
  through these lines as the spines but hit a sufficiently large amount of nearby
  people who have Wikidata so that it practically connects up a lot of people."*
- From 2026-09-01 there must be **at least one item that tries to connect these
  people**.

## Wire up CI/CD so the committed JSONs fire from 2026-09-01

- The JSONs are already in git; the pipeline reads them and starts executing edits on
  Wikidata on **1 September 2026**.
- **Never add a `push:` or `pull_request:` trigger** — `CLAUDE.md` § *Cost* forbids it
  and this does not need one. A `schedule:` cron plus `workflow_dispatch:` is what this
  wants, and it leaves that rule intact.
- She expects it to be **stateful about the repo**: *"something that would do some
  degree of stateful editing of the repo through GitHub Actions, including something
  that would take out this part of the repo once it's done."* So the workflow commits
  back — marking a batch executed, and removing the spine-line queue once it has run.
- The edit algorithm it executes is already specified above in § *THE EDIT ALGORITHM*:
  100 edits a day chosen at random from the eligible set, service-area gate,
  Geni-IDs-as-sources de-prioritised to 5–25 a day. **Do not normalise away the bias
  toward her neighbourhood** — it is deliberate.
---

## How the synoptic tree is actually made — Emma, 2026-08-25

**Her words:** *"Put into the queue also an analysis of how the synoptic tree is actually made."*
And the framing that makes this a survey rather than a blocker: *"I feel like we may not have gone
over the synoptic tree stuff sufficiently, but I'm going to treat it as though it's all good. I'm
going to treat the synoptic tree as though it is perfect, and we are going to address whether the
synoptic tree is well functioning later."*

So **nothing waits on this.** Write down what `scripts/build-synoptic-correspondence.py` actually
does: the eight sources it unions, what each one's evidence is worth, the `date_refuted` filter,
the `ROUND_CAP = 3` cut on the zipper, which multiplicities it tolerates and which it calls
conflicts. Then say where it is doing something nobody chose.

## The chain of provenance — Emma, 2026-08-25

**Her words:** *"providence is important in this, and ideally, a zipper merge will almost always
be done with there being a relatively large chain of providence, not just a simple 'this was the
justification,' but a potentially very large series of justifications."* And why the manual
verdicts exist at all: *"That is the actual reason why I asked you to record my manual decisions,
because of the fact that they entered into the province too."*

`reports/zipper-pairs.tsv` now records one step — slot, method, the pair it came from, and the
evidence. That is a link, not a chain. What she is describing is the **transitive closure**: a
round-5 pair's justification is its own step *plus* every step beneath it, down to an anchor or to
one of her own verdicts in `reports/emma-judgments.tsv`.

Two things follow, and she stated both:

- **Support propagates upward.** *"If you have a group of 100 people in one generation, all of
  their ancestors are all consistent. It's a really good sign... suddenly you go into the ancestors
  and you notice that somebody connected one of the ancestors. There's an entity resolution on one
  of the ancestors from our side. This supports it extremely well, and it actually supports it
  down the entire chain."*
- **Contradiction propagates the same way.** *"if you end up in a situation where there's an entity
  resolution that clearly contradicts it, this indicates a clear contradiction... it goes both
  ways."*

So the artefact is a provenance **graph** that can be walked in both directions, with her manual
RIGHT/WRONG verdicts as first-class nodes, and a report of which inferred chains an independently
recorded `P2600` confirms or refutes.

## Link reliability order — parents, spouses, children, siblings

**Emma, 2026-08-25, ranking them least messy first:**

1. **parents** — *"parents are always most reliable"*
2. **spouses** — *"can be a bit messy because sometimes people have multiple spouses"*
3. **children** — *"there's a lot of comparison stuff"*
4. **siblings** — *"sibling links are not very common"* on Wikidata

`scripts/zipper-join.py` now runs its slots in this order, which matters because the first slot to
claim a person in a round wins. Siblings are **not** a slot yet and should be added last, if at
all. **The fifth kind is surveyed** — `P1038` *relative* with `P1039` *kinship to subject*,
`reports/p1038-relative-survey.md`, 2026-08-26. 26,724 of 2,246,827 stored items carry it,
49,974 statements, 93% qualified. **71% of the kinships are ones a walk over our own parent and
child edges already produces** (uncle, grandfather, nephew, cousin); the **29%** that are not —
in-law, step, adoptive, foster, godparent — are the only part worth building on. Nothing built.

**And the point that stops a whole category of wrong stopping:** *"no ancestors isn't a point to
stop... It doesn't mean that the ancestors aren't on Wikidata. That's not what it means... at this
point, you're not really doing the zipper anymore. We'll just be adding new individuals on
Wikidata."* A slot with nothing on their side is a **creation opportunity**, which
`reports/creation-opportunities.tsv` now counts, not a failure of the join.

---

# THE LAST ITEM — BUILT 2026-08-26. `reports/wikidata-garborg-day.qs`

**There is exactly ONE live batch file and that is deliberate.** A second copy under a spine-y
name was made and immediately deleted: `tests/test_p2600_batches.py` failed on it, correctly,
because two files creating the same people is precisely how somebody runs both and duplicates
everybody. `reports/wikidata-garborg-day.qs` is the batch; what it contains depends on the flags
it was built with.

**Emma, 2026-08-25:** *"make it 100% clear in our queue at the end and no other crap no excuses
queue says to build the thing that makes a lot of them."*

**It exists.** `scripts/build-garborg-day.py --roster out/roster-spine.txt --roster-is-frontier
--known reports/spine-already-on-wikidata.tsv` → **21 creations, 148 links**, the whole spine in
one file instead of a hop a day.

`--roster-is-frontier` is what was missing. `--roster` *filters* the one-edge ring, and the spine's
middle sits many edges from anybody holding a QID — which is the entire reason it needs building —
so filtering a ring they are not in returned nothing and read as "no work to do".

**Every guard still applies**, and each one bit:

| | |
| --- | ---: |
| people across all three lines | 49 |
| already in the ledger | 5 |
| already judged to have an item (`--known`) | 8 |
| born 1880 or later | 4 |
| already carry a `P2600` elsewhere | 9 |
| held by the duplicate guard | 0 |
| **created** | **23** |

23 + Emma, who has `Q140568870` and needs an id rather than a creation, is **24** — the spine
count in `reports/the-spine.md`, arrived at independently.

**The two the guard held were false positives and Emma released them, 2026-08-26.** The unmatched
item is a *named other person* in both cases, which the guard cannot see because it compares QIDs
and not labels: Ramborg Knutsdotter Lejon's parent `Q5915800` has `Q4955715` *Ingegerd
Knutsdotter* and `Q16595443` *Katarina Knutsdotter* — her sisters — and Algot Bryniolfsson's
`Q101247444` has `Q101247439` *NN Brynolvsdotter*, a **-dotter** where Algot is a **-son**.
`RELEASED_FROM_DUPLICATE_GUARD` in `scripts/build-garborg-day.py` carries both with their reason.
Releasing Ramborg pulled her married surname *Lejon* into `wikidata-garborg-name-items.qs`, which
went 41 → 42 creations; `tests/test_garborg_day_batch.py` caught that before the run did.

**Still needed, and it is not optional:** the 23 cannot link to *each other* in one run, because
`LAST` names only the most recent item. Everything joining them to an item that already exists is
emitted both ways in this file; the new-to-new links wait for
`scripts/build-missing-reciprocals.py` once the QIDs exist. That is the one place the two-file
shape genuinely applies.

---

## Bure kinship as random-walk start points — LAST. Postponed by Emma 2026-08-25

**She moved this to the tail herself:** *"Postpone the bure stuff to the end of the queue."* It sits
after the spine item deliberately. Do not promote it.

**Her open question, for whenever it is picked up:** *"What is the topology of them? Like of the
bure people what percentage of the wikidata linked ones are just directly connected through geni
even though they are absent on wikidata?"* That is the first measurement to run — take the
Wikidata-linked Bure people, walk our Geni tree between them, and report what fraction are joined
by a path whose intermediate people have no Wikidata item. It says how much of the cluster could be
connected by creating the people in between.

**Emma, 2026-08-25:** *"put at the end of the queue a thing that adds bure kinship people (all of
them) as random walk add start points and points where things can come off from."*

**It is not a bigger `n` on the Garborg batch and must not be built as one.** Her reason:
*"bure is a bunch of unlinked people with entity resolutions to geni, so it isn't dense it's a
different kind of area though which needs its own algorithm"*, and *"as so many people there have
wikidata items already the types of quickstatements will be different and potentially more
challenging."*

**The difference that drives the algorithm.** The Garborg ball is items we are *creating*: almost
every statement is part of a `CREATE`, and the constraint is that `LAST` cannot be a value. The
Bure region is the opposite — the items exist and already carry `P2600` *Geni.com profile ID*,
so nearly nothing needs creating and nearly everything needs **linking**: `P22`, `P25`, `P26`,
`P40` between two QIDs that both already exist. Those have no `LAST` problem at all and can be
emitted in any order, which means the one-hop-a-day pacing that exists to work around `LAST` does
not apply for the same reason.

What to build:

- **Roster every Bure-kinship person**, all of them, with their QID and Geni id. Start from the
  existing Bure work in the repo and from `P2600` holders in that region.
- **Use them as random-walk start points**, and as points work can come off from — so the walk
  is seeded from many places at once rather than expanding one ball from Arne.
- **Johannes Bureus as a second anchor.** Her proposal in the same breath: the neighbourhood
  becomes "within n steps of Arne **or** within n steps of Johannes Bureus". That is a
  modification to the composition and belongs here, not in the Garborg batch.
- **Different statement mix, so measure it before assuming.** Count how many of the roster
  already have each of `P22`/`P25`/`P26`/`P40` before deciding what a day's batch looks like.

**Bureätten the export campaign stays closed** — 7 resolved, 76 dropped, 0 exports. This is a
different thing: linking people already on both sides, not finding new ones.
