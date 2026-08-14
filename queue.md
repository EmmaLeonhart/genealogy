# geni — Work Queue


**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## THE PLAN — Emma, 2026-08-12. This supersedes the decision list below

**"When we are doing this we do not need to do everything all at once."** The
twelve-decision table below is no longer the state of the project; it is
background. Several of its rows are answered here, and the rest wait rather than
block.

**Progress — 2026-08-12.** Her ordered list below is left verbatim rather than
having items deleted from it, because it is her wording and the queue's
delete-when-done rule is about *my* steps. Status is tracked here instead:

| item | state |
| --- | --- |
| 1 · derive labels | **done** — `reports/derived-labels.csv`, 298,591 rows; `reports/labels.md` carries the catalogue. 49,184 people (16.5%) have no derivable English label; 47,125 gain a married-name alias |
| 2 · derive name items | **possible now, and measured — `reports/name-resolution.md`.** The 882,477-label fetch made the lookup exist. It resolves **30.7% of given-name occurrences and 27.3% of surname occurrences**, but only 9.0% and 14.6% of *distinct* strings. **The unresolved head is mostly not names** — `I`, `II`, `of`, `NN`, `/`, `Rd.` — so the true rate for real names is higher and is *not* measured. Separating names from non-names is the missing step, and it is `todo.md` § 4's trap seen from the other side |
| 3 · occupation | **done** — `reports/derived-facts.csv`; 31,401 people carry one |
| 4 · places and dates | **done** — same file. birth 150,203 dates / 58,562 places · death 118,918 / 38,990 · burial 11,907 / 16,360 |
| 5 · family links | **done** — `reports/derived-family.csv`; 231,472 fathers, 178,656 mothers, 125,890 spouses. The invent-two-parents case is **250 families** → `reports/invented-parents.csv`, 500 placeholders. **Only 17 of the 250 have a child carrying a QID**, so "geni linked if possible" rarely applies |
| 6 · marriage | **done** — `reports/derived-marriages.csv`, 36,314 families. **36,257 carry a date (99.8%)**, 10,779 a place. But only **1,251 have both spouses on Wikidata**, which is the emittable size. "End" is divorce and only divorce: **483 families**, and Geni has no way to express a marriage ending at a death, so this is the one field where Wikidata has more than Geni |
| 7 · everything else | *"cool but not necessary"* |

### Answered 2026-08-12, second round

- **`ADDR` is kept as text, not dropped.** *"Do addresses with the address
  property (multilingual text)."* → **`P6375` street address**, monolingual text,
  so an address never has to become a place item. **This supersedes the
  `PLAC`-only rule** and recovers the location for **101,579 events** that had an
  `ADDR` block and no `PLAC`. Applied in `derive-facts.py`; `reports/facts.md` has
  the counts. **Flagged, not decided:** `P6375` is documented as a *street*
  address explicitly excluding country, while these blocks are `CTRY` 147,173 /
  `STAE` 132,781 / `CITY` 107,734 with a street line only 2,738 times.
- **Invented parents: the no-parent case only.** The 40,884 single-parent
  families get nothing. As implemented — 250 families, 500 placeholders.
- **The married-name alias is substitution.** `Judith /de France/` + `_MARNM
  Flandre` → `Judith Flandre`. As implemented and pinned by test.
- **The name-item download** — she asked what it is rather than choosing a size.
  It is fetching the Wikidata items that *represent names*, so that `P735`/`P734`
  can point at them: the store holds people and **113 of the 132,569 name items**
  their name statements reference. Deriving a name item means looking one up, and
  that is impossible offline today. Still open.

**One number from item 5 that her rule does not reach.** A sibling group with no
parents is **250 families**. A family with **exactly one** recorded parent is
**40,884** — 36,097 father-only, 4,787 mother-only. Whether the missing one is
invented too is not stated, and the unaddressed population is **163×** the
addressed one. `reports/family.md` has it. **NEEDS-DECISION — Emma.**

**One number from item 4 that bears on a decision she already made.** She chose
*ignore `ADDR`, use `PLAC` only*. Applied, that costs **101,579 events their
place entirely** — they carry an `ADDR` block and no `PLAC` — against 113,912
events where `PLAC` supplied one. So the rule drops the location for **47% of
the events that have any**. The alternative she declined, *use `ADDR` only when
`PLAC` is absent*, is exactly that population and would never override a `PLAC`.
The rule stands; `reports/facts.md` records the size so it is re-openable on a
number rather than a recollection.

**Order, in her words:**

1. **Derive labels from GEDCOM.** *"First thing is deriving labels from gedcom.
   Something that's very easy."*
2. **Derive name items but never create them.** *"We derive name items but never
   create name items."*
3. **Occupation** — *"can be done with string stuff"*.
4. **Birthplace, birth date, death date, death place, burial date, burial
   place** — *"all can be done with string"*.
5. **Family links.** Mother, father, spouse and child are *"easier"*.
   **Siblings with no parents recorded need two parents invented** — *"sibling
   relationships without parents need to get two parents that are 'father of x
   and y' and 'mother of x and y' and geni linked if possible"*.
6. **Marriage date and place and end** — *"will be easy-ish"*.
7. **Everything else** — *"other things in really common stuff will be cool but
   not necessary"*.

**Two rules stated alongside the order:**

- **The married name becomes an alias.** *"Married name plugs into name to
  produce an alias."*
- **Every individual needs an English, a Japanese and a Chinese label** — and
  *"we gotta catalogue these things a bit better too as a bulk operation"*.

**A recorded entity resolution, put in without analysis at her instruction**
(*"Do not analyze this just fucking put it in whatever data the discovered
correspondence goes into"*): geni `6000000087535357291` ↔ `Q140568870`, now in
`entity_resolution.md`, which is where hand-recognised Geni-to-Wikidata
identities live. `tests/test_entities.py` still passes, so the parser
understands the entry without the file being reformatted to suit it.

### What this changes about the twelve decisions

| # | status now |
| --- | --- |
| 5, 6 (`P734` bynames, patronymic `P735`) | **narrowed** — name items are *derived, never created*, so the open part is only which existing item a string resolves to |
| 4 (`P26` shape) | **in scope**, item 6 above |
| 11 (display-name rule) | **superseded in spirit** — she calls label derivation "very easy" and it is item 1 |
| 12 (name-item download scale) | **still open**, and now load-bearing: deriving a name item means resolving a string to an existing item, which nothing can do offline today |
| 1, 2, 3, 7, 8, 9, 10 | **not addressed** — they wait, they do not block items 1–7 |

**One reversal recorded so it is not lost.** On 2026-08-11 she said *"We create
new people and new name items. This is literally the fundamental purpose of this
entire project."* Today: *"We derive name items but never create name items."*
The later statement holds. Whether **people** are still created is not restated
either way and is not assumed here.

**One measurement that bears on item 1, offered and not argued.**
`reports/display-names.md` measured "the Latin display name becomes the English
label" against the 8,457 people where Wikidata already has a human-chosen English
label: **20.6% land exactly right**, and a perfect oracle picking the best of a
person's Latin names reaches only 26.8%. The failures concentrate in royalty,
where Geni holds the native birth name and Wikidata the English regnal form.
That does not make item 1 hard — deriving the label is easy — but the derived
label will disagree with Wikidata's four times in five where both exist.

---

## TWELVE DECISIONS WAITING — 2026-08-12 (background; see THE PLAN above)

**Everything in this queue is blocked on one of these.** They accumulated over
twelve autonomous ticks and are collected here because eleven decisions scattered
across eleven reports is not answerable, and one list is. Each has the measurement
already done and the cases already in front of you.

**One question unblocks three items.** Everything else is independent.

| # | the decision | what it blocks | where the evidence is |
| --- | --- | --- | --- |
| **1** | **Where does a correction to Geni data live?** Editing `exports/` in place, or a corrections file applied at merge. `CLAUDE.md` says every GEDCOM under `exports/` is committed and that tracking them is what this repo is *for* — so editing in place fixes the data and destroys the record of what Geni sent, across up to five files per person. | the BCE minus signs · the Ōjin/Wikramawardhana merges · the 442 encoding reconstructions | `reports/impossible-years.md`, `reports/encoding.md` |
| 2 | **Which date faults are in scope?** 6 missing BCE signs (recoverable, four self-proving), 3 digit typos in day-precision records (correcting = guessing), 24 modifiers with no operand (unrecoverable), 13 cosmological years (not errors — somebody recording a myth). | the BCE item | `reports/impossible-years.md` |
| 3 | **Does ingestion strip invisible characters?** 4,199 of them in `NAME`/`PLAC`: 1,409 LRM, 1,336 RLM, 1,281 NBSP, 132 soft hyphen, 26 ZWSP, 15 BOM — one BOM mid-word in `Willis Hil﻿l Cemetery`. ZWSP/BOM/soft-hyphen are clearly unwanted; the bidi marks may be doing real work in Arabic and Hebrew names. | any label emission | `reports/encoding.md` |
| 4 | **What shape does `P26` take?** And are the 30 "Wikidata names a different spouse" rows excluded outright — Christian IV's mistress is in that bucket, so Geni records a union where Wikidata records a marriage. | marriage conversion | `reports/marriages.md` |
| 5 | **`P734` for territorial bynames?** Wikidata gives one to *dynastic* names (Habsburg, Savoia) and not to individual bynames (de Provence, of Württemberg). And the largest self-evidencing group is Norwegian **farm names**, which are ordinary surnames. | surname conversion | `reports/toponym-surn.md` |
| 6 | **Does a patronymic ever become a `P735`?** 27,003 Latin multi-token `GIVN`s end in one — `Olsen`, `Olsdatter`. Arne Olson Anda is the ordinary case, not an edge case. | given-name conversion | `reports/givn.md` |
| 7 | **The `ABT` tolerance**, and whether `consistency.py` changes at all. At ±5 years 41% of the 6,734 "impossible" findings dissolve; 14% go at tolerance zero on `BEF`/`AFT`/`BET` alone. | the consistency report's standing as a verdict | `reports/consistency-analysis.md` |
| 8 | **Is the `Q1349864xx` batch investigated as a batch?** 26 of the 66 suspect links sit in one contiguous QID creation block holding 1.7% of linked people — a 23× enrichment. | link quality | `reports/link-suspects.md` |
| 9 | **The personal data.** 639 postal addresses of living people and 12,176 names of living Geni users, already committed inside the GEDCOMs and now trivially extractable. Does it matter given the repo is private; must anything public strip `SUBM`? | publication of anything derived | `reports/subm.md` |
| 10 | **Rip out `reconcile.py`'s fuzzy matcher now, or after modelling?** You ordered it removed. It touches `coverage`, `quickstatements`, `crosscheck` and five test modules. | nothing — but it is unremoved code that contradicts rule 1 | this file, § the queue wipe |
| 11 | **The display-name rule.** My proposal, for you to overrule: apply "Latin display name becomes the label" only where the name carries no title apparatus, and treat titled people as needing a name we do not have. 20.6% land exactly right; a perfect oracle reaches only 26.8%, so it is not a name-selection problem. | label emission | `reports/display-names.md` |
| **12** | **How much of the name-item download to run** — all 132,456, or the top 1,000 for **55.3%** of references, or 2,420 for 66.3%. A live run needs your **confirmation**, which `CLAUDE.md` requires separately from approval. Was BLOCKED-ON-EXTERNAL until sized on 2026-08-12; the external part is measured now and only the scale is open. | `names.py:240` · `reconcile.py:512` · **all `P734`/`P735` resolution**, which decisions 5 and 6 depend on | `reports/name-item-download.md`, `reports/name-items.csv` |

**What was measured while these waited**, all committed, all offline, nothing
altered in the corpus:

| report | the finding |
| --- | --- |
| `reports/consistency-analysis.md` | the "impossible" dates are 41% artefact — the check compares bare integers and discards every date modifier |
| `reports/subm.md` | `SUBM` is the Geni user managing the profile, and 657 of 12,176 are people in our own tree |
| `reports/link-suspects.md` | 66 suspect links, not 2; the worst was never named; 26 are one batch import |
| `reports/impossible-years.md` | the "five pharaohs" are nine people and three distinct faults |
| `reports/display-names.md` | display-name-as-English-label is 20.6% exact; failures are almost all royalty |
| `reports/givn.md` | the multi-token `GIVN` trap is real and `todo.md` locates it wrongly — 85% Latin, patronymics beat honorifics 4:1 |
| `reports/nsfx.md` | `NSFX` is an open field of 19,875 values and holds CJK numerals beside Latin ordinals |
| `reports/toponym-surn.md` | toponymic surnames are mostly Norwegian farm names, not nobility |
| `reports/marriages.md` | 240 marriages Wikidata has no `P26` for; marriage **place** is the biggest addable gap yet — 575 |
| `reports/encoding.md` | `Malm°` is Latin-1-read-as-CP437, 442 reversible lines; 4,199 invisible characters matter more |

**A note on how this went, because it is a finding about the process rather than
the data.** Six consecutive ticks produced an analysis each, every one defensible
on its own, while the decision list grew from eight to eleven. Producing more
measurement does not advance a project that is waiting on judgement. If the next
tick has nothing but analysis available, the honest report is `nothing
actionable` rather than a seventh census.

---

## 2026-08-11 — the queue wipe, and what the project actually is

**Emma emptied the blocked half of this queue by answering it.** Her framing:
*"so much stuff is blocked on user action, and half of this stuff probably is
stuff that I have no intention of ever actually doing. It's just clogging up the
queue."* Everything below that she killed is deleted rather than marked.

**Two rules now govern everything. Both are in `correspondence.md` in full.**

1. **Matching is genealogical only.** *"I only want us to be doing it based off
   of genealogical relationships and connections and stuff. That's all I want.
   That is the entirety of what I'm wanting to do."* The join is the **mother on
   both sides**: *"we merge them based off of whether something is the mother on
   both sides of an individual. We merge them together unless the mothers really
   conflict… might have it so they have a third mother or a second mother."*
   No fuzzy search, no label similarity, no long-distance search.
2. **We are doing ingestion, not conversion.** *"It takes a long-ass fucking time
   to get from a GEDCOM to a Wikidata item. These are very different data
   structures."* The Wikidata-emitting end is not being built yet.

**`reconcile.py`'s fuzzy matcher is to be removed.** Emma, on being shown it:
*"no fucking clue why there's a fuzzy matcher that sounds like something you made
with zero consent from me."* Correct — it entered on 2026-07-30 in commit
`8f60681`, whose message is entirely about `frontier.py`. Its docstring claims
nothing is auto-accepted; in fact `expand_from_matches` accepts every HIGH pair
into `matched_all.csv`, and `_cmd_quickstatements` reads **only** those rows to
build `add-p2600.qs`. Nothing has shipped from it. **Rip it out** — and no
matching method, threshold or score enters this repo again without being shown
to Emma first.

**Dropped permanently, by her decision:**

- **3.A's isolate exports** — the six seeds (Ovid, Avicenna, Khayyám, Aesop,
  Horace, Hobbes). The 183,681 isolate count stays as a measured fact.
- **2.A's export-target list** and the question of how out-of-tree seeds are
  found.
- **All three seed-research investigations** — smallest-ball ordering, whether
  the seed ranking predicts anything, and what bounds an export. The
  `GENI_EXPORT_CAP` test stays; the open questions do not.
- **The 10,000-individual entity-resolution backtest.** Emma: *"whatever this
  10,000 individual entity resolution backtest is, it is not something that I
  consent to."*

**No longer blocked on Emma — reassigned to analysis, which is my job:**

- **The five missing BCE minus signs** — *"Fix them in the fucking data."*
  **Censused, not fixed — `reports/impossible-years.md`.** The instruction covers
  six of nine people. There are **three faults, not one**: 6 missing minus signs
  (four self-proving, birth year later than death year), **3 digit typos in
  day-precision modern records** where correcting means guessing, and 38
  unreadable dates over 13 more people (24 modifiers with no operand, 13
  cosmological years for Shinto creation deities, 1 unseparated digit run).
  **NEEDS-DECISION — Emma, twice over:** where a correction lives, given every
  GEDCOM under `exports/` is committed and one person appears in up to five of
  them; and which faults are in scope.

The other three are **done**, and each replaced a verdict with a measurement:

- **The "impossible" dates — `reports/consistency-analysis.md`.** The check
  compares bare integers and discards every `ABT`/`BEF`/`AFT`/`BET` modifier, so
  a child `ABT 1500` against a parent `ABT 1512` was reported as impossible.
  Read as intervals, **41% of the 6,734 findings dissolve at ±5 years**; 14% go
  at tolerance zero, on `BEF`/`AFT`/`BET` handling alone. The `ABT` tolerance is
  **NEEDS-DECISION — Emma**, and `consistency.py` is deliberately unchanged.
- **`SUBM` — `reports/subm.md`.** The Geni user who manages the profile, and
  they are a profile themselves: `SUBM` ids share the `INDI` namespace and
  **657 of 12,176 submitters are people in our tree**. 99.6% of people carry
  one. Also surfaced 639 postal addresses of living people —
  **NEEDS-DECISION — Emma**.
- **The two suspect `P2600` links — `reports/link-suspects.md`.** Censused all
  70,785 comparisons instead of reading the two worst. The report's own
  criterion yields **66 suspect links, not 2**, and the worst was never named.
  Bengt Folkesson ranks 52nd — unremarkable. The real structure: **26 of the 66
  are one contiguous QID creation block** holding 1.7% of linked people, a 23×
  enrichment. **NEEDS-DECISION — Emma:** whether to investigate that batch as a
  batch.
- **Ōjin and Wikramawardhana** — *"Just merge the fucking Geni stuff within our
  data… I have merged them on Geni, but it's not going to appear for you because
  the export's already done. You've got to fucking merge them yourself."* The
  discriminator is the shared `FAMC`.
- **Which Geni field feeds `SURN` vs `_MARNM`** — answered by reading Geni's own
  documentation rather than by Emma opening an edit form. Geni has both a
  *Birth (maiden)* field and a *Last name* field; `SURN` is the maiden name and
  `_MARNM` the last name, which is why 43% of records carry only `_MARNM` and why
  the differing group is 53% male.

**Decided and now in scope:**

- **Creating new items is the point.** *"We create new people and new name items.
  This is literally the fundamental purpose of this entire project."*
- **Name items must be downloaded** — a `wikidownload` pass fetching `P31` =
  family name / given name. The store holds people; 0.4% of referenced name items
  are in it, so no name resolves offline today.
- **Names split by script, not by language.** *"We will sort by languages later.
  We are sorting by scripts right now."*
- **`ADDR` is ignored; `PLAC` only.**
- **Burial is two properties** — `P119` place, `P4602` date, no qualifiers.
- **Conflicts are added, referenced to `P2600`** — a reference, not a qualifier.

**Field-by-field modelling lives in `correspondence.md`** and is built one record
at a time. **No tooling is written from it until the modelling is finished** —
Emma: *"Tooling is something that is going to be done all at once, once all of
our modelling is finished."*

## STANDING ORDER LIFTED — 2026-08-09 16:50

**Emma: "you can barrel now, and you can also finally be loud and merge things
in and all of this stuff."** The quiet-until-18:30 CPU ban is void. `genimerge
merge`, `wikidata-index`, `wikidata-ancestors` and the full `pytest` run are all
allowed again.

**New standing order, same message:** *"Check every hour for new downloaded zip
files from geni that I am using for this and actively integrate them in and
update the page on which people are not in the tree."* That is a fourth local
cron at `33 * * * *`, alongside the three-cron playbook — sweep
`~/Downloads/export-geni*.zip`, drop content-identical repeats, import the rest,
re-merge, and rebuild `out/wikidata-unreached.html`.

## The re-clone of 2026-08-09 16:37 — what it cost

The repo was re-cloned into place, so **everything gitignored under `out/` was
lost**. `wikidata/` (2.7 GB) and `exports/` are tracked and survived.

- `out/wikidata-unreached.html` — **restored and now tracked** (`075c3fc`), with
  `scripts/build-unreached-page.py` to rebuild it from the tracked TSV. It had
  been generated straight into `out/` with "regenerate rather than commit"
  written in its report and no script that could regenerate it.
- `out/merged.ged` — regenerated by the 149-export merge below.
- **`out/merged-145.ged` can no longer be made.** Item 2 step 4 wanted the
  pre-batch 145-export tree kept so item 0.00A could measure a batch against it.
  That file never existed and the tree that would have produced it is gone.
  0.00A's before-measurement is **lost, not deferred** — the earliest baseline
  now obtainable is the 149-export tree.
- `out/wikidata/p2600-all.tsv` — gone, and it was *fetched from Wikidata*, which
  CLAUDE.md forbids re-querying. **Rebuilt offline** from `wikidata/items/` by
  `scripts/build-p2600-all.py`.

  **Two files, two formats, and crossing them fails silently.** `p2600-all.tsv`
  is `qid<TAB>geni_id` with **no header** — what `genimerge overlap` writes and
  what `_cmd_wikidata_ancestors`, `doubles` and the rest read *positionally*.
  `p2600-map.tsv` is `geni_id<TAB>qid` **with** a header, written by
  `wikistore.write_p2600_map` / `wikidata-index --map`. The first rebuild put
  map content at the all path; nothing raised, and `genimerge
  wikidata-ancestors` printed `0 of our people carry an item` while exiting 0.
  Anything reading this file should assert the first token starts with `Q`
  rather than trusting the path.

## Emma's decisions, 2026-08-09 — four answered

**3.A — export from the best-documented isolates.** Emma's pick. These six carry
a Geni profile ID and record no father, mother, spouse, child or sibling on
Wikidata, and none is in our tree. If Geni returns family for these, the
"export target list" reading holds for the tail; if it does not, the reading is
wrong and 183,681 items are not an export target at all.

| item | who | articles | Geni profile to export from |
| --- | --- | ---: | --- |
| [Q7198](https://www.wikidata.org/wiki/Q7198) | Ovid | 201 | [6000000015256128571](https://www.geni.com/people/x/6000000015256128571) |
| [Q8011](https://www.wikidata.org/wiki/Q8011) | Avicenna | 193 | [6000000010664917790](https://www.geni.com/people/x/6000000010664917790) |
| [Q35900](https://www.wikidata.org/wiki/Q35900) | Omar Khayyám | 166 | [6000000015297447236](https://www.geni.com/people/x/6000000015297447236) |
| [Q43423](https://www.wikidata.org/wiki/Q43423) | Aesop | 166 | [6000000073056397940](https://www.geni.com/people/x/6000000073056397940) |
| [Q6197](https://www.wikidata.org/wiki/Q6197) | Horace | 166 | [6000000015255871584](https://www.geni.com/people/x/6000000015255871584) |
| [Q37621](https://www.wikidata.org/wiki/Q37621) | Thomas Hobbes | 160 | [6000000010648830087](https://www.geni.com/people/x/6000000010648830087) |

**BLOCKED-ON-USER-ACTION** — only Emma can take a Geni export. The hourly sweep
imports them automatically once the zips land in Downloads.

**2.A — yes, seed from the dated 1500s+ targets. DONE —
`reports/ancestor-seeds.tsv`, 610 rows.** Built by
`scripts/build-ancestor-seeds.py`, ranked newest first, ties broken by how many
of our people the target is a parent of.

**The count Emma decided on was 829 and the real figure is 610, because the
report was counting rows.** `_century_rows` and the section heading both
counted *findings* — a parent Wikidata names for three of our children is three
findings and **one** export. Distinct people one hop above us is **1,482**, not
2,123; dated 1500s+ is **610**, not 829. The decision is unaffected — same cut,
same reasoning — but the seed list is a third shorter than the number it was
chosen from, and that is worth knowing before working down it. The heading now
states both figures and a test pins the distinction.

The split, distinct people: **610** dated 1500+, **361** dated pre-1500, **511**
undated. The 511 undated are still not in the list and still not discarded —
undated does not mean early, and they want their own question.

**2.D — measure Geni against Wikidata per property, assume nothing.** This is
not a matching-accuracy backtest; Emma reframed it as *source reliability*.

- **Population:** every CONFLICT `crosscheck` finds over the 14,177 held pairs.
  Not a sample — whatever the data actually disagrees about.
- **Measurement:** per property (P22 father, P25 mother, P26 spouse, P569 birth,
  P570 death) — how often Geni is right, how often Wikidata is, how often both
  are wrong. **No global winner is assumed**; Geni may be better at
  relationships and worse at dates, and that is the shape the table exists to
  reveal.
- **Output:** Emma chose **a merge rule the code can apply**, per-property
  precedence the union tree uses automatically. Worth stating plainly since it
  is the more committal of the two options offered: this turns the measured
  numbers into behaviour, so the adjudication has to be sound before the rule
  ships. Build the table first, show it, then generate the rule from it — not
  the rule directly.
- **Blocked on 2.B:** `crosscheck` still constructs a `WikidataClient`. Wiring
  it to the store reader is what makes this runnable offline.

**0.00Y — decided and done.** Floor plus seed-file check; see `devlog.md`.

## THE GOAL, restated 2026-08-10 — add to Wikidata

Emma: *"the entire purpose of this is to add it."* Correcting Wikidata is
*"almost effectively out of the question"*. **24,957 addable statements against
930 conflicts** over the 14,157 linked people. `CLAUDE.md` § *The purpose is to
ADD* has the rule; `reports/model.md` has the field-by-field table.

**Priority order, highest first:**

1. **Names — `reports/names-spec.md`.** The largest gap: 7,215 addable `P735`
   and 4,477 `P734`. Labels: English is 96.5% done (501 missing), **Japanese is
   the work at 10,161 missing**, and **4,500 of those already carry a CJK string
   in Geni with an empty `ja` slot** — addable with no language inference, only a
   codepoint range.
2. **Places.** 3,502 `P19` + 2,737 `P20` + 1,560 `P119` addable. Start from
   `ADDR/CTRY`+`STAE`+`CITY`, **not** from parsing `PLAC` — the structured block
   is twice as well filled. Blocked on place items being absent from the store;
   `scripts/fetch-labels.py` resolves them one batched query at a time.
3. **Dates and the rest.** 1,719 `P569`, 1,248 `P570`, 1,261 `P106`, 925 `P97`,
   312 `P1636`.
4. **Contradictions — explicitly low priority.** Emma: *"worth doing but
   genuinely not that important."* Note them, do not build for them.

**`_MARNM` is answered — Emma, 2026-08-11: it is the married name.** Right about
the tag, and the corpus uses the slot far more widely: of the 244,392 records
carrying it, 31% duplicate `SURN`, **43% are the only surname on the record**
(`SURN` empty), and the 25% that differ are **53% male** — spelling variants,
Norwegian farm names, and CJK records where `_MARNM` holds the clan surname
while `SURN` holds an ancestral *place* (`謝` against `陳郡陽夏`). So it can
neither be dropped nor read as marriage. `reports/names-spec.md` § `_MARNM` has
the table and the three consequences for P734.

Which Geni input field feeds which tag is inference, not fact —
**BLOCKED-ON-USER-ACTION**, one profile's edit form against its exported record.

**Open and needing Emma**, all from `reports/names-spec.md`:

- **Which `NAME` record becomes the label** when several share a script.
- **Whether `NSFX` belongs in a label** — Geni's `Henry III King of England`
  against Wikidata's own `Henry III of England`.
- **What "occasionally" means for `mul` labels.**

## THE WORK NOW: the ancestor walk, case by case — 2026-08-10

**Everything below this section is older and lower priority.** Emma redirected
the project on 2026-08-10 from corpus-wide reports to case-by-case review, with
her doing the interpretation. `CLAUDE.md` § *How this project works now* has the
rule; this is the state of the walk.

**Seed: Henry III of England** — geni `979118`, wikidata `Q160311`. Emma:
*"He is a really good starting point."* **34 generations and 717 distinct
ancestors above him.** (An earlier "13 generations" was a recursion cap reported
as a measurement.) Order is ahnentafel: self, father, mother, then the four
grandparents, and so on. `python scripts/show-case.py 979118 --up N`.

**Case 1 — Henry III. Reviewed. What it produced:**

- **The record is 2,686 lines**, of which 149 are `NOTE` and 367 are `OBJE`.
  Only 9 notes exceed 20 lines; those are pasted articles (English Wikipedia and
  a Norwegian one). The other 130 are short and real: Burke's Peerage, Scots
  Peerage, Dictionary of National Biography with volume and page, a `!RESEARCH
  NOTES:` block arguing a claimed daughter Mary "cannot be accepted", LDS sealing
  dates from 1933 and 1938.
- **No language marking exists anywhere.** Zero `LANG` subtags in the corpus. The
  only `NAME` subtags are `GIVN` (352,545), `_MARNM` (244,392), `SURN` (219,117),
  `NICK` (66,926), `NSFX` (36,072), `CONC` (6). Henry III has four `NAME` records,
  two English and two Spanish, and nothing distinguishes them. Emma: Geni drops
  the language on export, so this needs linguistic judgement — **parked, and she
  used the word deliberately**.
- **`FAM` objects carry marriage data**: `@F6000000009811238831@` has
  `1 MARR / 2 DATE 14 JAN 1236 / 2 PLAC Canterbury Cathedral`. His parents'
  family has `26 AUG 1200, Bordeaux`.
- **Wikidata has the same marriage, in qualifiers**, and disagrees:
  **P580 = 4 JAN 1236** against Geni's **14 JAN 1236**, plus P2842 place,
  P582 end, P1534 end cause, 4 references. Ten days apart.
- **A field-level source is plainly wrong**: Henry III's `First Name` and `Date
  of Death` both cite a Find A Grave memorial for **Edward I (1239–1307)**, his
  son.
- **Child counts differ**: Geni 8 in that family, Wikidata 9 under P40.

## Emma's decisions, 2026-08-10 (the walk)

- **Labels: only for the 14,177 people carrying both IDs.** Wikidata is the
  definitive source for a person's label. If an individual already has both an
  English and a Japanese label, **park it immediately** — move on to fields
  worth talking about.
- **Marriage mapping: not decided.** *"Show me marriage cases first."* Walk more
  `FAM` records before choosing any P26-qualifier shape.
- **Child-count disagreements: show the diff case by case.** Resolve both sides
  to names and dates, show what only one side has, Emma judges missing vs
  illegitimate vs different family vs duplicate.
- **Field-level sources: collect, do not trust.** Record what each `SOUR` claims
  to source; treat the citation as unverified. The Edward I case proves they can
  be simply wrong. Not usable as a Wikidata reference on that basis.
- **Notes: useful, but only where they disambiguate a data record.** Not the
  current job. Pasted articles are droppable; the short ones are not.
- **Ōjin: keep the detailed record** (`@I6000000001829492981@`).
  Wikramawardhana undecided — she said she does not know him. **This is a
  decision about two records, not a merge rule.**

### Case 1, continued — the marriage date, run to ground

Emma: *"agentic rag to figure this out it's probably a typo in geni"*. It is not.
**Geni's 14 JAN 1236 is right; Wikidata's `P580 = +1236-01-04` is wrong.**

Westminster Abbey — which is Wikidata's **own first reference on that statement**
— says *"in Canterbury cathedral on 14th January 1236"*. Britannica, Historic
Royal Palaces, English Monarchs and Wikipedia agree. Eleanor was crowned on 20
January, six days later; sixteen days would be odd. Almost certainly a dropped
`1`.

**Resolving the four references changes what "4 references" means:**

| | what it actually is |
| --- | --- |
| `Q5933` Westminster Abbey | authoritative, and **contradicts** the statement |
| `Q1465172` Lulu Press | a self-published book, page 155 |
| `Q75653886` | no English label; described only as "online genealogical network" — in context, very likely Geni |
| `Q21401824` The Peerage | hobbyist compilation site |

**This undercuts `reports/conflicts.md`.** That report measured that 69% of
disputed Wikidata dates carry a reference and offered it as evidence about where
errors are likelier. Reference *count* says nothing about reference *quality*,
and nothing in that pass looked at what a single reference was. Treat the 69% as
a coverage statistic and not as an argument.

### Places: Geni's string is Wikidata's hierarchy, flattened

`scripts/fetch-labels.py` — one batched SPARQL query, labels only. The store
holds people, so places and source items cannot be resolved offline at all.

| Geni string | Wikidata |
| --- | --- |
| `Winchester Castle, Winchester, Hampshire, England` | `Q1704670` Winchester Castle **and** `Q172157` Winchester |
| `Westminster Palace, Westminster, London, England` | `Q62408` Palace of Westminster |
| `Westminster Abbey, Westminster, Middlesex, England` | `Q5933` Westminster Abbey |
| `Canterbury Cathedral, Canterbury, Kent, England` | `Q29265` Canterbury Cathedral |

The two `P19` values are not a contradiction — they are the building and the
city. Wikidata states the birthplace twice at two levels of nesting; Geni states
it once as a comma-chain containing both. Emma: *"Wikidata stores data as QIDs
that are stored as strings on Jenny... if the strings show the same stuff,
Wikidata is basically always going to be good, just keep that in mind: difficult
conversion."* Note `Middlesex` — an administrative county abolished in 1965 — so
the chain can be historically stale.

### Cases 2-11 reviewed — what the walk has actually produced

**Three kinds of conflict, from three cases. This is the finding.**

| | case | who is wrong |
| --- | --- | --- |
| 1 | Henry III marriage, 14 vs 4 JAN 1236 | **Wikidata** — contradicts its own first reference |
| 2 | John marriage, 26 vs 24 AUG 1200 | **Geni** — 24 Aug confirmed by five sources |
| 3 | Eleanor of Aquitaine birth, 1122 vs 1124 | **neither** — a live scholarly dispute |

Type 3 is the one that matters for design. Alison Weir argues 1122 from Eleanor's
age at death and the 1136 fealty oath; Elizabeth Brown argues 1124 from a
13th-century genealogy giving her age as thirteen in 1137. **Any merge rule that
picks a winner fabricates certainty here.** Wikidata's own idiom for it — two
statements with ranks, or a sourcing-circumstances qualifier — is the shape that
survives, and neither side uses it: Wikidata states 1124 alone with **zero
references**, while its death date on the same item carries three.

**Dates otherwise agree almost perfectly.** Across cases 2-11, nine of ten match
exactly on both birth and death year. Eleanor is the only disagreement.

**Geni encodes uncertainty as prose, inside structured fields.** Eleanor's
birthplace:

    2 PLAC Nieul-sur-Autize, Vendée or Château de Belin, Guyenne or Palais d'Ombrière, Bordeaux

Three candidate birthplaces joined by "or" in a field that should hold one place.
Unparseable as a place, and unrepresentable on Wikidata without becoming three
ranked statements.

**Orphan marriage dates: counted, then dropped.** 16,229 of 36,257 dated `FAM`
records name no spouse (45%), and 22,513 families name one spouse with no
children and no marriage event. Emma: *"These aren't anything meaningful because
they can't be represented on wikidata"* — correct, and it closes the thread.
Marriage data hangs off `P26`; with no spouse there is no statement to qualify,
and expressing the one-spouse families would need an item for a partner Wikidata
does not have. Real counts, irrelevant to the conversion.

**Marriage ordinals: derive from dates.** Emma's call. `P1545` (Wikidata numbers
John's marriages 1 and 2) is a cross-check, not a source.

**The one-spouse families may be real.** Emma's reading: relationships Geni knows
about whose partner was not in the export's scope. Checking one against a live
Geni profile is **BLOCKED-ON-USER-ACTION**.

**Correction to an earlier note here:** I described six of John's families as
"empty shells". None are empty — John is `HUSB` on all six. The pattern is one
spouse named and nothing else, and it is corpus-wide, not a John quirk.

### Cases 2-11 are laid out and waiting — `out/cases/`

`python scripts/prepare-cases.py 979118 --count 10`. Regenerable in one command,
so not committed. Each file holds the person's structured GEDCOM record, **every
`FAM` record they appear in whole**, and **every Wikidata statement with its
qualifiers and references**. Long notes and image blocks are withheld and
counted. Nothing is compared and nothing is concluded.

| # | position | geni | source record |
| --- | --- | --- | ---: |
| 2 | father | `4924870419470035934` John, King of England | 7,358 lines |
| 3 | mother | `6000000007593862015` Isabelle of Angoulême | 959 |
| 4 | ff | `5597271884650100378` Henry II | 6,682 |
| 5 | fm | `6000000003582502504` Aliénor d'Aquitaine | 2,788 |
| 6 | mf | `6000000000134496318` Aymer d'Angoulême | 471 |
| 7 | mm | `6000000000134665152` Alice de Courtenay | 1,494 |
| 8 | fff | `4194887957440076070` | 1,732 |
| 9 | ffm | `6000000002106021492` | 1,245 |
| 10 | fmf | `6000000003523986134` | 1,163 |
| 11 | fmm | `6000000000701127473` | 342 |

**366 distinct QIDs** across the ten, all resolved in **one** SPARQL query →
`out/cases/labels.txt`.

**One thing already visible and not yet interpreted:** Geni places are *not*
only comma-strings. Isabelle's record carries both `2 PLAC Abbaye de Fontevraud`
and a structured `2 ADDR / 3 CITY Fontevraud-l'Abbaye / 3 STAE Pays de la Loire
/ 3 CTRY France`. The earlier note that "Geni's string is Wikidata's hierarchy
flattened" was drawn from Henry III alone and is incomplete — there is a
structured address block too, and how consistently it is filled is unknown. Her
call, not mine.

She also carries **six `NAME` records** across French, English and Lithuanian
(`Izabelė iš Angulemo`), with an empty `2 SURN` on one.

## Order of work — synthesized 2026-08-09

Three queues had accumulated: this machine's, the cloud session's (the import
item and 2.E's second half), and the older `0.*` items. **The IDs below are
unchanged on purpose** — `devlog.md` entries and commit messages already point
at them, so they are ordered here rather than renumbered.

| # | item | state |
| --- | --- | --- |
| 1 | **3.A singleton Wikidata items carrying Geni links** | counted in full; rest is BLOCKED-ON-USER-ACTION |
| 4 | **2.E** component walk as a command, isolates split out | overlaps 3.A — do 3.A first, it is the same discriminator |
| 5 | **2.B** port the `client.sparql` call sites offline | **done to the data's limit**: 6 ported, 2 blocked, 2 stay online |
| 6 | **2.C** build the union tree | shape settled by Emma; *edge* still undefined |
| 7 | **0.00Z** three `FAM.HUSB` conflicts | **answered**: both are one man twice; step 2 NEEDS-DECISION |
| 8 | **6** the stale Wikidata reports | rerun against the 151 merge |
| 10 | **2.D** source-reliability backtest | **decided 2026-08-09**, see below |
| — | 0.0, 0.00A, 1, 3, 4 | BLOCKED-ON-USER-ACTION, all needing Emma at Geni |

**Item 2 (the import) is done and deleted.** Merged at 149 exports, and the three
corpus tests that had never been run against the new files are green — `pytest
tests/test_seeds.py tests/test_repo_invariants.py tests/test_gedcom_real_exports.py`,
**1264 passed, 1 skipped, 4m17s** at 151 exports. The `GENI_EXPORT_CAP` 4080 → 4088 change is
therefore measured, not believed. Its one unrecoverable piece is recorded under
the re-clone above: the 145-export baseline item 0.00A wanted no longer exists.

**`## 8b-i **The century distribution** — DONE, `reports/centuries.md`

**Corrected 2026-08-10 after Emma asked to look over the future birth dates.**
The first run's `century_of` returned the century *ordinal* formatted as a year
range — 1950 came out as `2000s` — so every label was a hundred years late and
the headline conclusion was inverted. Fixed, re-run, and the report now carries
the corrected table.

| the claim | verdict |
| --- | --- |
| Wikidata skews to the 20th/21st | **wrong** — 1900s+2000s are 24.2% |
| …*much as Geni does* | **wrong** — Geni is 4.5% there |
| the 19th is where it gets interesting | **right** — the 1800s is the biggest bucket on both sides |

Wikidata's Geni-linked people peak in the **1800s (48.9%)**; ours are flatter and
older (1800s 21.4%, 1700s 18.6%, 1600s 15.2%, with a medieval tail Wikidata
barely has — 7,916 people born in the 1300s against their 1,523). Geni leads
every century through the 1700s, Wikidata from the 1800s on. The instinct
underneath the prediction survives — the Wikidata side *is* the more modern of
the two, 73.0% at 1800s-or-later against our 25.9% — but the centuries named
were a hundred years early.

## Emma's decisions, 2026-08-10 — four more

**BCE: the corpus already uses negative years.** Emma: *"it's negative years what
the fuck"* — and she was right; `out/merged.ged` carries **4,750** minus-sign
`DATE` lines and **2,256** BCE people. My earlier claim that BCE was
unrepresentable came from a hand-rolled parser using `str.isdigit()`, which is
`False` for `"-73"`. Both scripts now call `genimerge.dates.parse_date`.
`reports/bce.md` is rewritten; `reports/centuries.md` shows the 2,256.

What survives: **five records have the sign missing**, all pharaohs with positive
birth years above 2026. Correcting them is a Geni edit — **BLOCKED-ON-USER-ACTION**
— or the pipeline adds a guard refusing any birth year later than the current
year, which catches the class rather than the five. Emma has not chosen between
those.

**Ōjin: keep the detailed record.** Emma, on being shown the two:
*"keep the more detailed one for ojin and idk who the wikramawardhana guy is"*.
So `@I6000000001829492981@` (誉田別命 /応神天皇/ — death date, occupation, five
spouse families, four images) wins over `@I6000000179131744821@` (`Ōjin /Tenno/`,
a birth year and nothing else). **Wikramawardhana is not decided** and she said
so plainly; leave it.

This is a decision about *these records*, not yet a merge rule. Whether
`merge_files` should generally prefer the richer record is still open, and
inventing that rule from one case would be over-reading her.

**Item 6: build the smaller offline `reconcile` now** — seeds and relative
expansion from the store, no name-matched candidates, so `coverage.md` can
refresh against the 151-export tree. The name-match half waits on the download
pass.

**2.D: chase the structural lead first.** Test whether the 292 structural
conflicts are duplicates rather than disagreements, the way 0.00Z turned out,
before adjudicating any dates.

## Emma's brief — her words, the destinations these decompose from` below is Emma's own brief, not steps.** It is
the destination list these decompose from; leave its wording alone.

3.A **Singleton Wikidata items that carry a Geni link.** Emma, 2026-08-09:
*"first thing is investigate the singleton wikidata ones with geni links."*

`reports/wikidata-components.md` found **183,296 isolated single items** out of
1,408,401. The subset that matters here is those carrying a P2600: Wikidata
names a Geni profile for them and records **no family at all** on its side.

**Keep 2.E's distinction — it is the whole question.** A **true isolate** has
*zero* relation statements; an item only *appears* isolated when it carries
P22/P25/P26/P40/P3373 pointing at QIDs the download never fetched. The second
is closed by finishing the import and is not interesting; the first is a real
question about what Wikidata holds. **Both are per-item properties**, so a
sample answers the shape without the full pass the component walk needed.

**Counted in full 2026-08-09 — `scripts/count-isolates.py`, all 1,408 shards.**
**183,681 true isolates**, 35.7% of the 514,903 Geni-linked items; 331,220
connected; **2** that only look isolated; **330** of the isolates already in our
tree. `reports/wikidata-isolates.md` carries the full table and keeps the sample
beside it. The page is rebuilt and tracked: `out/wikidata-isolates.html`.

**What is left of 3.A is one thing, and only Emma can do it:**

- **Export from a handful of isolates and see whether Geni returns family.**
  BLOCKED-ON-USER-ACTION — only Emma can take a Geni export. Pick seeds from the
  330 isolates already in our tree, or from `reports/wikidata-unreached.tsv`,
  since an isolate is almost never someone we hold. This is the load-bearing
  unknown: the whole "export target list" reading assumes Geni *has* the family
  Wikidata lacks, and that assumption is untested.

Three results worth carrying forward, because they change what other items mean:

1. **The "relatives not downloaded" explanation is all but dead — 2 items in
   514,903, and both are now named: Q68188 and Q928741.** Each has one relation,
   to an item the download never fetched. Recency is ruled out by measurement
   (76% of the store has a higher QID than one of the two targets); the file
   that would say *why* — `download-state.sqlite3` — died in the re-clone, and
   `rebuild` cannot recover a `missing` row from shards that never held the item.
   **Answered as far as offline data allows**; the next download run settles it
   for free. The sample said 0 of 9,000 and this queue said *dead*; the full
   pass says vanishing, not absent. The conclusion survives: 183,681 is a real
   isolate count, not the upper bound `wikidata-components.md` had to call it,
   and **2.E's discriminator has already done its job** — implement it for
   re-runnability, not to settle the question.
2. **An isolate is ~20x less likely to be someone we hold** (0.18% against
   3.43%). The ~183,000 well-described items missing only their genealogy are
   therefore an *export target list*, not an authoring list — the opposite of
   how they first read.
3. **Isolates are confined to the seed phase.** The count reaches 183,681 by
   shard ~600 of 1,408 and never moves again: expansion items were fetched
   *because* they were somebody's relative, so they cannot be isolates. Nothing
   further to download will reduce this number.

## Emma's brief — her words, the destinations these decompose from

Once we are finished with the wikidata tree export, or have decided we are finished with it, we can then look to see how much of the tree is interconnected.

The geni tree export should be analyzed and merged into, but this involves a lot of AskUserQuestion

We have the large batch of shared individuals, we will need to reconcile the radically different formats, and do entity resolution piecemeal across the graph. So like if person has two fathers, analyze if they seem to fit

With entity resolution stuff, parents are easier to resolve, but we need to do a test of say 10,000 individuals for any entity resolution algorithm. It needs to be rigorous. 

Notably geni names are structured with the form of separate first names and last names. There is a display name but I do not think it commonly happens. Display names are complicated and we need an analysis, plus our name property adding things. 

We also need some other geni-wikidata entity resolutions manually or with searches. Well there are a couple ids I have to manually propose at least.

Adding the geni source properties


Also the wikidata items with two geni ids, we need to resolve this

imo we need to figure out how to reach all the wikidata items with geni ids, but we do not have the geni ids. These can be discovered with tree traversal planning. Mainly descendants of individuals we have. Extension of the other descendants thing we were doing. We do that thing first, and then the general geni export thing later. This might get most of the significant geni stuff here anyways, but we can get say clearly terminating clusters in the 1800s or 1700s later after the incorporation of the geni descendants and such


## Active — the numbered items (see the order table above)

The five items planned this morning are done and are in `devlog.md`.
`genimerge.wikistore` now reads the downloaded store, and
`wikidata-index` / `wikidata-ancestors` are the two new commands. What that
opened up, and what it did not:

2.A **Export targets, one hop above us — RUN 2026-08-09, `reports/wikidata-ancestors.md`.**
The century breakdown that was coded but never run is now in the report, against
the 151-export tree. **2,123 targets** (was 1,821 at 145 exports); 14,157 of our
people carry an item; 4,854 parents have no Geni ID at all; 12,367 we already
hold; 70 Geni IDs sit on more than one item and were skipped.

**The question it was run to answer — is the list worth anything for a campaign
aimed at modern times? — answers yes.** Of the 1,400 targets carrying a birth
date, **829 are 1500s or later**, and the single biggest bucket is the **1700s at
283**. 1600s 204, 1800s 192, 1500s 150. Only ~495 are pre-1500. **723 carry no
date at all** — a third of the list, and the one real gap in this reading.

What is left of 2.A is a decision, not a computation: **NEEDS-DECISION, Emma** —
whether these 2,123 feed the export campaign the way `reports/descendants.md`
does, and what to do with the 723 undated ones. The tension the item was written
around is now measured rather than argued: a parent is a step backwards, but a
`Descendants` export from one returns their whole descent, and 829 of them are
late enough for that descent to reach modern times.

2.E **Make the component walk a command, and separate the 183,296 isolates.**
`reports/wikidata-components.md` answers "how many trees is the Wikidata side"
— one of 1,042,423 (74%) plus 223,207 fragments — but it was produced by a
throwaway script, so it is not re-runnable as the store grows. Port it to a
module the way `wikistore` was, reusing `wikidownload.RELATION_PROPERTIES`
rather than restating the five properties.

While there: **an isolated item and an item whose relatives were not downloaded
are different things and the current pass cannot tell them apart**, because an
item with no relation statements emits no dangling reference either. Splitting
them needs only a count of relation statements per item, which the same pass can
carry. Until it does, do not describe the 183,296 as "people with no family on
Wikidata" — that is one of the two readings and it is unverified.

**The HTML must split the two, and isolates need investigation — Emma,
2026-08-09.** The component output (HTML) has to separate genuine **isolates**
— items with *zero* relation statements, no family recorded on Wikidata at all
— from items that only look isolated because their **relatives were not
downloaded** — items carrying P22/P25/P26/P40 that point at QIDs not yet in the
store. Those two are different work: the not-downloaded ones **just need
import** (the expansion walk fetches the referenced items and they stop looking
isolated), while the true isolates are **NEEDS-INVESTIGATION** — nothing the
import closes, a standing question about why Wikidata records no family for
them. The relation-statement count this item already calls for is the
discriminator; surface it per item so the two groups are told apart in the page.

2.B **Port the remaining `client.sparql` call sites to the store, by question.**
`reconcile`, `crosscheck` and `namelinks` still import `genimerge.wikidata`, so
they still cannot run under the no-query rule. Ten call sites; each asks one
concrete thing and gets answered from the index. `crosscheck` is the valuable
one — it compares our parents, spouses and dates against Wikidata's, and the
4,854 parents with no Geni ID are exactly the population it would speak to.
Do **not** write a SPARQL emulator.

**`crosscheck` runs fully offline as of 2026-08-10 — `--offline`.** Both of its
network dependencies are gone: the claims come from the store, and the links
come from `p2600-all.tsv` instead of `reconcile`'s `matched_all.csv`. Measured
over the 151-export tree: **14,157 linked people, 30,303 agree, 4,700 gaps,
930 conflicts**, 3,238 QuickStatements written, nothing sent anywhere.

The offline path covers the **exact P2600 links only** — `reconcile`'s expansion
matches are not in the map, so this is a subset of what the online command sees,
and the flag's help says so. That is the population `build_claim_batch` emits
for anyway.

**This unblocks 2.D**, whose population is now identified and counted:

| property | conflicts |
| --- | ---: |
| P569 date of birth | 321 |
| P570 date of death | 317 |
| P22 father | 134 |
| P25 mother | 90 |
| P26 spouse | 68 |
| **total** | **930** |

**Characterised 2026-08-10 — `reports/conflicts.md`, data in
`reports/conflicts.tsv`** (all 930; the crosscheck report shows only the worst
100). `scripts/build-conflicts.py`, offline.

| property | conflicts | Wikidata sourced | unsourced |
| --- | ---: | ---: | ---: |
| P569 birth | 321 | **69%** | 98 |
| P570 death | 317 | **69%** | 97 |
| P22 father | 134 | 48% | 70 |
| P25 mother | 90 | 46% | 49 |
| P26 spouse | 68 | 53% | 32 |

**The per-property asymmetry Emma asked for is present**: Wikidata's disputed
*dates* carry a reference 69% of the time, its disputed *relationships* only
46–53%. That runs the way the "Geni wins relationships, Wikidata wins dates"
prior would predict, which is a reason to **test** that prior rather than adopt
it. It measures citation coverage, not correctness, and Geni has no comparable
field — so it says where to spend adjudication effort, not who is right.

Date conflicts are mostly near-misses: 638 of them, **median 13 years apart**,
44% within a decade, only 17 over a century. A rule that picks a winner on a
four-year gap in a medieval record is choosing between two plausible readings,
not correcting an error, and should say so.

Also: **12** disputed statements carry `preferred` rank — a Wikidata editor
already chose that value over a competitor — and **54** are against items
holding other values for the same property as well.

**Still open, and the lead worth following:** the adjudication itself. The one
case settled by hand (`reports/husb-conflicts.md`) was resolved by **structure**
— two records sharing a `FAMC` — not by any column in this table. 292 of the 930
are structural, and 0.00Z showed a structural conflict can be a *duplicate*
rather than a disagreement. The merge rule should come from an adjudicated
sample, not from citation coverage; building it on the table above would encode
"Wikidata cites more sources" as "Wikidata is right", which nothing here shows.

**3 of 10 ported, 2026-08-09/10.** `namelinks._existing_name_claims` →
`existing_name_claims_from_store`: which of P735/P734 an item already states.
The *values* are never read, only which properties exist, so it is answerable
from the store even though the name items are not in it. 4 tests, plus a
real-store check (Q42 and Hobbes state both, Avicenna P735 only, Ovid neither).

**`names.py:240` cannot be ported, and this is a measurement, not an opinion.**
It asks Wikidata for *items whose label or alias equals a given name string and
whose P31 is a name type* — a label-to-item lookup over all of Wikidata. The
store cannot answer it because it does not contain name items: the download
walked P22/P25/P26/P40/P3373, which reaches people, not the items their names
point at. Sampled 40 shards, 40,000 items, 2026-08-10: of **13,683** distinct
P735/P734 targets referenced, **55 are in the store — 0.4%**.

**That sample was wrong by 4.7×, and the download is now measured — 2026-08-12,
`reports/name-item-download.md`.** All 1,408 shards, 1,408,401 stored items:
**132,569 distinct name items referenced, 113 already present (0.09%), 132,456
to download.** `P734` references 101,854 of them against `P735`'s 31,023.

**This is no longer BLOCKED-ON-EXTERNAL. It is a NEEDS-DECISION about scale**,
because the distribution is steep enough that the download need not be
all-or-nothing:

| download the top | of 132,569 | references covered |
| ---: | ---: | ---: |
| 100 | 0.1% | 28.4% |
| 1,000 | 0.8% | **55.3%** |
| 2,420 | 1.8% | 66.3% |
| 17,936 | 13.5% | 86.6% |

**0.8% of the vocabulary resolves over half of all 2,016,016 references.**
Per-item counts for all 132,569 are in `reports/name-items.csv`, so any other cut
is answerable without re-reading the 2.7 GB store.

**A live run still needs Emma's confirmation separately from her approval** —
`CLAUDE.md`: the one bulk job permitted to talk to Wikidata *"is confirmed before
a live run"*. She approved fetching name items inside a rapid four-question
round; that is not the same thing, and the sizing above exists so the
confirmation can be informed rather than blind. **Do not** port `names.py` by widening it
to "any item we happen to hold" — that would silently return a fraction of the
matches and read as if the endpoint had answered.

**4 of 10 ported, 2026-08-10.** `reconcile.fetch_relatives` →
`relatives_from_store`. This is the call site the store suits best: the download
grew the set by walking P22/P25/P26/P40/P3373, so a matched item's relatives are
in the store *by construction* — they are why it was fetched. Two shapes
reproduced rather than approximated: the `en,no,nb,nn,sv,da,de,fr` label
priority (`LABEL_LANGUAGES`), so a candidate is scored on the same string either
way; and `wdt:` truthy ranks. A relative the download never reached is still
returned as an edge with no label — dropping it would hide a real edge from the
reconciler. 5 tests, plus a real-store check on Q42 (father, mother, spouse,
child, with dates).

**`reconcile.py:512` is blocked for the same reason `names.py` is.** It asks
`?item rdfs:label|skos:altLabel ?label` with `P31 wd:Q5` — a label-to-item search
over all of Wikidata, to find people we have *not* matched. The store contains
the P2600 set and their relatives, so searching it by name can only return
people we already hold, which is the opposite of what the call is for.
**BLOCKED-ON-EXTERNAL**, same unblock signal as `names.py`: a download pass that
fetches beyond the family walk. Porting it against the store would silently turn
a discovery step into a no-op.

`reconcile.py:600` hydrates QIDs with label/dates/P2600 and *is* portable — the
same shape as the relatives hydration above — but it consumes the output of the
blocked search, so porting it alone buys nothing.

**6 of 10 ported, 2026-08-10 — 2.B is done to the limit of the downloaded data.**

- `wikidata.find_matches` → `matches_from_store`. **The P2600 join itself**, and
  the index was built for exactly this — a table lookup, not a scan. One `Match`
  per (Geni ID, item) pair as online, because the mapping is not one-to-one and
  collapsing a double-match hides what `wikidata-doubles.md` exists to surface.
  Sort order kept (shortest Geni ID first) so the two forms are comparable.
- `quickstatements._existing_p2600` → `existing_p2600_from_store`. Keeps the
  online form's **lossy** `qid -> one geni_id` shape deliberately: fixing it here
  alone would make the offline path disagree with the online one about a
  population another report owns. Lowest ID chosen, so repeated runs agree.

5 tests, plus a real-store check: Ovid's Geni ID resolves to Q7198, Avicenna's to
Q8011, and the reverse lookup returns their P2600 values.

**The final triage of the ten:**

| | call site | |
| --- | --- | --- |
| **ported (6)** | `crosscheck:224`, `namelinks:101`, `reconcile:295`, `wikidata:309`, `quickstatements:151`, plus the `crosscheck` command | |
| **needs the name-item download (2)** | `names.py:240`, `reconcile.py:512` | label-to-item search; the store holds people we already have, so a port returns a well-formed nothing. **No longer BLOCKED-ON-EXTERNAL** — the pass is sized (132,456 items, or 1,000 for 55.3% coverage) and what remains is Emma's decision on scale plus confirmation for a live run |
| **stays online (2)** | `overlap.py:89`, `cli.py:264` | see below |

**`cli.py:264` stays online, and a previous session already wrote why.** It reads
`COUNT_QUERIES` — how many items Wikidata holds with P2600, globally. The store
could produce a number, and `_cmd_overlap`'s offline branch already refuses to:
*"No `reported`: those counts come from the endpoint. Passing the fetched totals
instead would print a number that looks like Wikidata answering and is really our
own file counting itself."* That reasoning is unchanged. `overlap.py:89` is the
seed fetch that fills the store; porting it to read the store is circular.

**What this means for item 6.** `crosscheck` is offline and runnable. `coverage`
still needs `reconcile`'s `matched_all.csv`, and `reconcile` can now do its
P2600 seeding and relative-walking offline but **not** its name search — so a
fully offline `reconcile` would produce seeds and expansion without the
name-matched candidates. That is a smaller `reconcile`, not a broken one, but it
is a **NEEDS-DECISION — Emma**: whether an offline `reconcile --offline` that
skips name-matching is worth having, or whether item 6 waits for the download
pass that would unblock both searches. `crosscheck.claims_from_store` answers
`fetch_claims`'s question — `qid -> {property -> [values]}` for P22/P25/P26/
P569/P570 — from `StoreReader.entities`. Same return shape, so callers do not
care which side produced it. 5 tests, plus a real-store spot check (Q42 returns
father/mother/spouse/dates; the isolates Q7198/Q8011/Q37621 return dates and no
relations, matching 3.A).

**Truthy semantics are the part worth not fumbling.** `wdt:` is not "every
statement": preferred-rank if any exist, else normal, never deprecated. Reading
every statement out of the JSON would quietly widen the comparison and turn
superseded values into fresh conflicts for a human to adjudicate. The port
reproduces this and has a test for each half.

Remaining 9: `cli.py:264`, `namelinks.py:101`, `names.py:240`, `overlap.py:89`,
`quickstatements.py:151`, `reconcile.py:295/512/600`, `wikidata.py:309`. The
`crosscheck` command itself still constructs a `WikidataClient` — wiring it to
the store reader is the next step and is what makes item 6 runnable.

2.C **Build the union tree — one genealogy holding both sources.**

**The shape, from Emma directly, 2026-08-09.** A union individual is a JSON
object with the two sides **nested whole and side by side**:

```json
{
  "geni_id":     "6000000087535357291",
  "geni":        { ...the full text of the Geni export for that person... },
  "wikidata_id": "Q12345",
  "wikidata":    { ...the nesting of the Wikidata content... }
}
```

**It is synoptic, and that word is doing real work.** This is a *duplicated*
tree, not a fused one: both sides are kept verbatim, nothing is reconciled at
build time, and *"this duplicated tree is intended to be later updated for a
later integration process."* Integration is a **later** pass over this
structure, not a condition of writing it.

So the three things that follow are decided, not open:

- **Do not merge fields.** No picking a birth date, no preferring a parent. When
  the two sides disagree the union simply holds both, tagged by which side they
  came from — Emma's call, and it falls straight out of the structure: the
  disagreement *is* `geni.birth` next to `wikidata.P569`.
- **Do not drop either side's content.** Both nests are full, not a projection.
  Same reasoning as `wikidownload` storing whole items: what a later phase wants
  is not yet known, and something stored lossily has to be fetched again.
- **Everything downloaded is in scope** — all 1,408,401 stored items, not just
  the 514,903 carrying a Geni ID. A node with an empty `geni` side is normal.

Either side may be absent, which gives four node kinds: both sides (12,860
pairs), Geni only (262,587), Wikidata-with-an-unreached-Geni-ID (504,123 pairs
— `reports/wikidata-unreached.tsv`), and Wikidata with no Geni ID at all
(893,498).

**What it is for**, all of which the structure has to survive: queueing Wikidata
edits that create the missing people, planning the next Geni exports, being one
complete genealogy to look at, and surfacing where the two sources disagree.
Emma also marked "something else" — **ask before assuming the four are the whole
list.**

**Still to settle before building:** what an *edge* is in the union. A Geni
parent link is a FAM record and a Wikidata one is P22/P25 on an item, and the
node shape above says nothing about how the graph is walked. Write that down
first.

**Corrected here after getting it wrong.** This item previously asked Emma to
decide whether the 4,491 Geni-ID-less parents were "an authoring batch or a
matching problem", as though admitting them required choosing. In a union tree
it does not: a person Wikidata records with no Geni ID is simply a node that
came from the other source. Whether one later proves to be a Geni profile under
a different ID is entity resolution **inside** the union, not a gate on entry.
The dichotomy was invented and the NEEDS-DECISION tag was wrong — by this repo's
own load-bearing default that made it undone work, not deferred work.

Concretely, the union holds:

- **12,850 in both** — joined on P2600, one node with two source IDs.
- **262,587 Geni-only** — our tree, no item.
- **504,035 Wikidata items carrying a Geni ID no export has reached** — known to
  both sites, held by neither of our datasets yet.
- **893,498 Wikidata items with no Geni ID** — the expansion walk's catch, of
  which the 4,491 parents are the part sitting directly above people we hold.

The node identity has to carry **which source each fact came from**, because
`todo.md` § 8's whole point is provenance and because a union that forgets
whether a parent link came from a GEDCOM or from P22 cannot later be turned into
Wikidata edits. Do not collapse the two IDs into one key: the Geni profile ID is
this repo's primary key for the Geni side and the QID is Wikidata's, and a node
can have either, both, or (after a merge) two of one.

Start by writing the shape down before building it — what a union node is, what
an edge is, and what happens when the two sources disagree about a parent. The
merge rule for the Geni side is later-sources-win on single-valued paths; the
union across *sites* is a different question and is not answered by that rule.

2.D **The 10,000-individual entity-resolution backtest.** § *Active after import
finished* asks for it and says "It needs to be rigorous". It still has no stated
success criterion, and inventing one is the failure mode — two seed-choosing
methods have already been refuted by measurement here, and both were proposed on
reasoning alone. **NEEDS-DECISION** — Emma; what counts as success.
The display-name and name-property analysis is likewise unstarted;
`genimerge profile-names` already measures the Geni side.

## Active Earlier

0.00Z **The three `FAM.HUSB` conflicts — step 1 answered, `reports/husb-conflicts.md`.**
**Both families are two records of one man.** Not a genealogical disagreement in
either case:

- `@F6000000179131721834@` — **Emperor Ōjin, twice.** `Ōjin /Tenno/` against
  `誉田別命 /応神天皇/`. Same birth year, and **the same `FAMC`**. This is the
  duplicate Emma predicted in 0.2. The merge currently keeps the **thin** record
  — filename order displaced the one carrying the death date, the occupation,
  five more spouse families and the images.
- `@F6000000195596077832@` — **Wikramawardhana, twice**, seventh ruler of
  Majapahit. Again **the same `FAMC`**. Here the richer record happened to win,
  by the same accident.

**The discriminator that settles both is the shared `FAMC`, not the names** —
names are where the two records differ most and parentage is where they agree
exactly. Worth carrying into whatever entity resolution gets built.

**And the conflict list is a duplicate detector Wikidata cannot provide.** None
of these four profiles appears in `reports/wikidata-doubles.md`, which finds
duplicates via one Wikidata item claiming two Geni IDs — Wikidata does not link
these, so that method is blind to them. Our own merge found them structurally.
Mine the conflict list rather than only resolving it.

**Step 2 is still open. NEEDS-DECISION — Emma:** whether `merge_files` should
sort sources by `HEAD` date. It would make the winner deterministic, but it
would not have produced a better answer here — the right resolution is "one
person, merge them on Geni", and date-sorting still picks one of two duplicates.

**The Geni-side merges: BLOCKED-ON-USER-ACTION** — only Emma can merge two
profiles on Geni. Belongs with the postponed Geni-side merge queue.

### Standing context

- **BLOCKED-ON-USER-ACTION — impossible dates in the tree, listed in
  `reports/consistency.md`.** Someone born before a parent, or after their
  mother died. Every one is an error in Geni's data rather than in the merge, so
  fixing them means editing profiles on Geni; this repo will not change them.
  A further set are implausible rather than impossible — a parent under 12, a
  lifespan over 120 — and some of those will turn out to be correct.

  **This entry said 96 impossible and 89 implausible, "re-measured 2026-08-02
  over the five-export merge", until 2026-08-06.** The report says **3,189** and
  **1,966** over 202,433 people. The number was not wrong when written; it was
  left behind by 94 exports, which is what a count copied into prose does. It is
  not restated here now — **read `reports/consistency.md`**, the same rule
  `todo.md` § 3a already applies to `reports/frontier.md`.

  Worth doing before the QuickStatements batches rather than after:
  `add-claims.qs` carries P569 and P570 statements built from these same dates,
  so an uncorrected year here becomes a wrong year on Wikidata.



- **The Jimmu chain, 62/83 → 77/83 → 83/83, is finished and its long note is
  deleted (2026-08-06).** The note ended by saying it could go once nobody
  thought it load-bearing; the 99-export re-run holds both jimmu path files at
  **83 of 83**, so the arc is closed. What it taught survives in `CLAUDE.md` —
  read the relation column before choosing an export style, because two of the
  six bridging steps are reachable only through a marriage — and the numbers are
  in `devlog.md` and `git log`. A 21-step gap took four exports, not the one
  originally planned; that is the part worth remembering.

- **Not doing: centralising the per-module property constants.**
  `crosscheck`, `reconcile`, `namelinks`, `names` and `quickstatements` each
  declare the property IDs they use at the top of the file. That is local and
  readable, and a shared registry would move them away from the code explaining
  why they are there; `CLAUDE.md` already serves as the cross-module reference.
  Recorded so a later sweep does not re-open it as though it were an oversight.



- **NEEDS-INVESTIGATION — smallest-ball is the only ordering that surfaces the
  known-good seed, and it rests on one observation.** Hågen Iversen placed 38 of
  2336 by smallest ball, against 2261 by the shipped doorway count and 1303 by
  openness. The mechanism is plausible — a tiny neighbourhood is one we know
  almost nothing about — and the obvious objection turned out to be wrong, since
  the shortlist is 66 candidates with none isolated. It is **not** adopted and
  must not be until there is more than one data point. Resolves by taking one
  export from a top-ranked pick and one from the small-ball shortlist and
  comparing new-people counts. Not blocking anything.

- **NEEDS-INVESTIGATION — the seed ranking has never been tested.** No export
  has been taken from a seed `reports/seeds.md` chose. The one export with
  measured results was seeded on the parent of Hågen Iversen, who placed 2255 of
  2336 (ball 5, one doorway), and returned 3656 new people. That is a reason to
  doubt ranking by absolute doorway count — a large ball is a densely recorded
  neighbourhood, which is the opposite of where Geni has most to add — but it is
  n=1 and the ranking never scored the actual seed, who was not in our data. It
  resolves by taking the next export from a top-ranked pick and comparing. The
  prediction is already committed in `reports/seeds.md`, so `git show` will
  supply it when the fifth export lands. Not blocking anything.

- **UNSAFE-TO-GUESS — two links flagged as worth re-checking, both exact P2600.**
  `reports/wikidata-crosscheck.md` § "Links worth re-checking" names Canute I
  Erikska `Q442876` (0 agreements, 4 conflicts, birth 1145 against 857) and
  Bengt Folkesson `Q1621801` (1 agreement, 2 conflicts). Both are matched by the
  Geni ID on the item, not by inference, so the ID itself is under as much
  suspicion as the match. Two readings fit and nothing in this repo separates
  them: the link is wrong, or it is right and one side's data is badly wrong.
  Resolving one means a human comparing the Geni profile against the Wikidata
  item. Nothing should edit either side on a guess.

- **NEEDS-DECISION — how out-of-tree export seeds are found.** `reports/seeds.md`
  can only rank people already in the merged tree. Iver Mellegård, who seeded
  the best export so far, was in none of the three earlier exports, so the
  ranking could not have proposed him. Whatever route found him is one this repo
  cannot see or reproduce. **Seen twice now:** the 2026-08-02 seed
  `6000000226989731860` was likewise in none of the four earlier exports, and
  produced an export that overlaps them by zero people. Two of the five exports
  came from seeds this repo had no way to name. The question is with the user;
  the answer decides whether to build out-of-tree candidate ranking or something
  else. Not blocking anything currently queued.

- **Take the pipeline order from `README.md`, not from a list written by hand.**
  The README's "before pushing" block already gives every command in dependency
  order, and it says `expand --search`, not bare `expand`. Both details matter.
  `expand` writes `matched_all.csv` and `candidates.csv`, which `coverage`,
  `crosscheck`, `name-links` and `quickstatements` all read, so omitting it
  leaves four reports generated from a previous tree. And bare `expand` skips
  the label-index lookup that produces the `name-match` proposals — running it
  without `--search` silently drops 100 of them and rewrites
  `reports/wikidata-coverage.md` with 30 proposals instead of 87. That is not
  hypothetical: it happened on 2026-08-01 and was caught only by diffing the
  regenerated report.

- **`python` on PATH is not the interpreter.** Python 3.13.14 is installed at
  `C:\Program Files\Python313\python.exe`, but the Microsoft Store stub aliases
  in `WindowsApps\` come first on PATH, so the bare `python -m pytest` written
  throughout `CLAUDE.md` exits 9009 with "Python was not found". Use `py -m
  pytest` or the full path. The package is not pip-installed either; the CLI
  needs `PYTHONPATH=src` (pytest gets this from `pythonpath = ["src"]` in
  `pyproject.toml`, which is why the suite runs but `python -m genimerge` does
  not). Not worth changing the user's PATH over, but worth not rediscovering.
- **NEEDS-INVESTIGATION — what actually bounds a Geni export is still unknown.**
  The code does not claim to know: `GENI_EXPORT_CAP` is documented as the largest
  export *observed* — **4008** since 2026-08-05 — rather than a limit Geni
  enforces, and `tests/test_seeds.py` fails if one exceeds it, which is how 3840,
  3844, 3856 and the 4008 were each caught. What is unresolved is the underlying
  fact. Ninety-nine exports still cannot separate a raised limit from a
  per-account limit from a limit on something other than head count from a walk
  that overshoots a floor. **The even spacing was a trap and the data has since
  said so**: three numbers four apart looked like a step of four, then eleven
  exports in a row held 3860 exactly, then a pair taken seven minutes apart held
  3972 and 4008. Nothing in the code encodes any arithmetic. This advances as
  data arrives rather than by being worked on, and is not blocking anything —
  being off by a few people out of ~4000 does not move the seed ranking.

- **CI is off on purpose, and stays off.** Not a blocker — a decision. This is a
  private repo, where Actions minutes are billable rather than free, and
  push-triggered CI was never worth that risk. `ci.yml` is now
  `workflow_dispatch:` only and the workflow is disabled at the GitHub end.
  Verification is `python -m pytest` before pushing. The cost of that choice is
  named rather than hidden: **the Python version matrix does not run**, so 3.10
  is exercised only by the static check in `tests/test_python_floor.py`, and no
  commit should be described as CI-verified.
- **NEEDS-DECISION** — `todo.md` items 4 and 5: creating Wikidata items, for
  people who have none and for the **1540 surnames and 4986 given-name tokens**
  that have none. Sized in `reports/names.md` over the five-export merge: 1167
  of 2707 distinct surnames (43.1%) and 2419 of 7405 distinct given-name tokens
  (32.7%) have an item, so the rest do not. Whole given-name strings as Geni
  stores them are far worse — 1186 of 11772 (10.1%) — because Geni packs
  multiple names into one field. The fifth export roughly doubled the
  given-token pool and dropped coverage from 56.1% to 32.7%: the Japanese
  component's names are much less represented on Wikidata than the Norwegian
  ones. The decision is the user's.

---

## 2026-08-13 — restore the lost link to two disconnected clusters (Emma)

Emma sent herself two Geni profiles that sit in **large but currently
disconnected** components of the merged tree, and believes each was once linked
to her / the main tree — the connecting relationship existing in one of the
saved HTML files (a relationship-path page, an ancestor page, or a `geni_pages/`
save) before that edge was removed on Geni:

- **wife of Baruch Jafe** — `6000000227145774838`
  <https://www.geni.com/people/wife-of-Baruch-Jafe/6000000227145774838>
- **wife of Samuel Standen** — `6000000227145420853`
  <https://www.geni.com/people/wife-of-Samuel-Standen/6000000227145420853>

**Her framing (2026-08-13):** whatever relation was removed from Geni will, once
found, go **back into the synoptic tree** and then into the later Wikidata edits.
So the deliverable is the missing connecting edge(s), not an analysis.

**Steps:**

1. Confirm both IDs are in the corpus and identify the component each sits in
   over the merged tree (are these two big components, and are they distinct from
   the main one?).
2. Enumerate every profile ID in each of the two clusters.
3. Cross-check those IDs against **everything else in the repo** — all other
   exports, every saved page under `missing ancestors/` and `geni_pages/`, and
   `paths/` — looking for any person who appears both in a cluster and in a file
   that also reaches Emma / the main component. That shared person (or the edge a
   saved page records) is the lost link.
4. If a saved page holds the connecting relationship, extract it the repo's way
   (`path-from-html`) so the edge becomes data, and note what re-connects the
   component. Report the found link(s) to Emma before merging anything.

**Steps 1-3 ran 2026-08-13 17:20. The search space is empty — the connecting
edge is not in this repo.** Union-find over all 175 exports:

- Four components. Main 325,661 (Emma). `wife of Baruch Jafe` sits in one of
  **4,088**; `wife of Samuel Standen` in one of **4,084**. A fourth holds 33.
- Each cluster is **exactly its own Forest export and nothing else**: of those
  4,088 and 4,084 people, **zero appear in any other export**. Not one person
  overlaps the other 173 files.
- **No cluster ID occurs in any saved page or path** — `geni_pages/`,
  `missing ancestors/`, `paths/` all return nothing. The `reports/*.csv` hits
  are derived from the merge itself, not independent evidence.

So step 3's cross-check has no material to work on, and step 4 cannot run.

**What the sizes say.** 4,088 and 4,084 are the export-size readings recorded for
exactly those two seeds in `seeds.GENI_EXPORT_CAP`'s docstring, so both balls
**stopped at the size bound rather than exhausting the neighbourhood**. A
truncated `Forest` ball proves nothing about whether the neighbourhood connects —
it only shows our walk stopped ~4,000 people out without meeting anything we had.
"The edge was removed on Geni" is therefore neither supported nor refuted here.

**Not-done tag:** BLOCKED-ON-USER-ACTION — resolving this needs Geni asked
directly, which is a browser action. Open the relationship path between Emma and
each of `6000000227145774838` / `6000000227145420853` on Geni; if Geni draws one,
save the page into `geni_pages/` and run `path-from-html`, and the chain names the
people the exports never reached. If Geni draws no path, the two really are
disconnected on the live site and the question becomes which edge to add.

---

## Always last — restart the three crons and summarize

**These two items stay pinned to the tail of the queue at all times** — below every real work item:

A. **Ensure the three crons are running** — start them if this session never did, restart them if a planning burst / queue re-fill killed them: work-loop (`3 * * * *`), auto-flush (`15 * * * *`), status-report (`42 * * * *`).
B. **Run the status-report action once more, independently** — an end-of-session summary of everything that happened this session.

---

## Pointers

- Long-horizon backlog (abstract goals, source of future queue items): `todo.md`.
- Completed work (chronological, with releases): `devlog.md`.
- Narrative history: `git log`.
