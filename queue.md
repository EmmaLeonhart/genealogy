# Queue

Only work. Every specification and record moved to `CLAUDE.md` on 2026-09-01 at her instruction: *"remove all the 14 bullshit queue items"*. An item is DELETED when done, never annotated.

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

**The three vocabularies are now one** — `scripts/labels.PLACEHOLDER_FORMS`, imported
  by the preview, the structural walk and the census instead of each carrying a copy.
  Strictly additive: all 27 forms the copies held are in it, plus 19 found by
  measurement, so nobody previously screened stops being screened. `NOT_A_NAME` is
  deliberately untouched — that decides what `label_for()` **empties** and she has ruled
  on it twice; these sets decide what a **marker** is. Widening detection is not
  widening suppression.

- **The katakana that remains needs a RULING, not a fetch.** The fetch is done and its limit
  is measured: `scripts/fetch-katakana-name-items.py` asked Wikidata for the 3,000 tokens
  blocking the most people, **456 resolved**, and `ja` labels went **190,206 → 267,976**.

  **871,623 people still fail on a partial, and the blockers are now three kinds — none of them
  fetchable.** Checked by SPARQL rather than assumed:

  | | blocks | why a fetch cannot help |
  | --- | ---: | --- |
  | **particles** — `von` 40,491, `of` 11,608, `y` 11,060, `af` 6,858, `la`, `der`, `til` | 88,826 | not names, so no name item exists to hold a reading |
  | **Nordic patronymics** — `Johansdotter`, `Andersdotter`, `Olsdatter`, `Pedersen`, `Eriksson`, `Hansson`, `Larsdatter` … | ~50,000 | **the items EXIST and carry no `ja` label** — `Q42223005`, `Q51885688`, `Q122837357`, `Q130232913`. Wikidata simply has no katakana for them |
  | **regnal numerals and the marker** — `II` 4,880, `III` 2,690, `NN` 3,005 | ~10,500 | not names either; `II` is the `P7338` ordinal and `NN` is the unknown-name marker |

  **So the next move is hers, and it is one decision per class**, not per token:

  - the particles — `von` is `フォン`, `af`/`av` `アフ`, `de` `ド`, and those are conventional
    Japanese forms rather than derivable ones, so they need a source or her word;
  - the patronymic suffix — `-sdotter`/`-datter`/`-son` is a fixed element, so `Johansdotter`
    would be the katakana of `Johan` plus one suffix; that is compositional, but it is still
    inventing a reading nobody has written down;
  - `II`/`III` — the middle-initial precedent says a letter that is the same in every script
    stays Latin, and Japanese also writes `2世`; and `NN` is a marker, which § *`NN` is
    PRESERVED in `mul`* says is never translated.

  **Do not guess any of the three.** `CLAUDE.md`: established Japanese spellings are conventional,
  not derivable, and a wrong reading of a real name is the one thing forbidden outright.

## THE VERY LAST ITEM — a GitHub Pages site documenting the repo

**Emma, 2026-09-01:** *"an item at the end of the queue: a github pages site built with actions
that documents generally what the repo is doing with different things, its data modeling and
algorithms and such. This is the last item though only after all the other stuff."*

**After everything else. Not before.**

- Built by a workflow, published to Pages — the repo went public 2026-09-01 so Pages is free.
- **What the repo is doing**: merge Geni exports into one tree, reconcile against Wikidata,
  generate the edits that create the missing people.
- **The data modelling**: how a name becomes `P735`/`P734`/`P5056` with `P1545`, `P7338`, `P3831`;
  how a GEDCOM date modifier becomes `P1480`/`P1319`/`P1326`; the `mul`-is-the-real-label rule and
  the married-name ordering; the NN/redaction algorithm.
- **The algorithms**: the daily ring one hop off the Wikidata subgraph from Arne; the zipper join
  and its provenance chains; the density and descendants seed rankings; the transliteration funnel.
- Generated from what is in the repo rather than hand-written prose that will go stale — the
  `CLAUDE.md` sections and the module docstrings already carry most of it.

## Then: one dispatch that produces the archive and the Pages site too

**Her framing, 2026-09-01:** *"the ci/cd run will make the archive (committed) and the pages and
the quickstatements for me to run later."* **The QuickStatements third is done and proven; the
other two are not, because the jobs that would make them do not exist yet.**

**What already works, run `33582811064` on 2026-09-02:** the gate found a contribution inside six
hours, the ledger refreshed to 1,158 rows, `--compose` built **23 creations**, the bot committed
them as `45f8eaf6`, the `wikidata-garborg-day` artifact carried the `.qs` and the adjudication
deck, and issue **#9** opened assigned to her. 9m21s, both jobs green. That was the item's stated
deliverable — *"a run that finishes and uploads `reports/wikidata-garborg-day.qs` as an artifact,
with the issue opened"* — and it is met.

**So what is left is ONE deliverable: the Pages site**, § *THE VERY LAST ITEM*.

**The ledger archive is already done and was never a job to build.** Emma, 2026-09-02: *"Lmao you
cunt it fetches every time the ledger from pages I edited"* — `build-daily-batch.py` STEP 0b runs
`full_entities` over the ledger, and the pipeline refreshes it from her contributions on every
run. Its queue section is deleted.

Once the Pages job exists, dispatch once and check that a single run produces all three. Not three
runs — her words are *"the ci/cd run"*, singular.

**Two failures got it here, and both are worth not repeating.** The 18:59 run died on
`FileNotFoundError: out/merged.ged` and was fixed by committing `family-structure.tsv.gz`, listing
it in `pack-derived.py` and giving `read_tree` a fallback. The 21:50 run then died on
`sqlite3.OperationalError: no such table: items`, because `out/wikidata/store-index.sqlite3` is
gitignored and `sqlite3.connect` **creates an empty database** rather than raising. Both are the
same shape: **a file the runner cannot have, reached by code that assumed it could.** Anything else
added to this workflow should be checked against `.gitignore` first.

## Promote one reading to `mul`, and roster the rest

**The readings themselves are DONE** — `reports/cjk-reading-aliases.tsv`, 40,125 people: `ko`
40,125, `zh` 40,109, `ko_variants` 6,654, sourced `ja` 391. All of them are `Amul` aliases, so
nothing here is blocked on a culture verdict.

**What is left is the promotion**, which is Emma's *"just a matter of which one is chosen at the
top"*:

- **Emit the aliases.** 5,621 of the 40,125 already have a Wikidata item, so those are addable
  with no creation at all. `Amul` per reading, no `Aen` ever — § *The MARRIED name is the real
  name* — and no descriptions.
- **Promote per culture** where the classifier is confident: `ko` for Korean people, `zh` for
  Chinese, sourced `ja` for Japanese. A wrong promotion is a reordering, not a wrong name.
- **Roster the unsure**, gated the way unsure parents are. **1,274 of 38,469** carry no verdict,
  893 of them because there was no evidence within 14 hops. That is the manual/agentic deck, and
  it shrinks on its own as confirmations propagate by network proximity.
- **`build-cjk-romanisation.py`'s docstring is stale** — it says no `hanja` and no `pykakasi` is
  installed. Both are, and both are now used.

**Do not reopen the classifier to improve it.** Emma, 2026-09-02: *"this isn't something to waste
forty eight hours on... a very ill scoped problem that got a massive scope creep."*

**One free discriminator was found and is NOT to be chased now**, only recorded: `pykakasi`
resolving a surname to a kun'yomi reading (青山 → あおやま) means its dictionary knows the token as
Japanese, where a Chinese surname falls back to on'yomi (謝 → しゃ). That would settle the
Japanese-in-`zh` misclassification cheaply. It is a promotion-order fix, not a gate.

## `P1814` *name in kana* — AT THE END, her call 2026-09-02

**Emma:** *"Put this culture identification thing at the end and work on everything else."* Four ticks went into it and it emitted **zero statements**; the readings are found and waiting, so it costs nothing to leave here.

**`scripts/fetch-kana-readings.py` → `reports/kana-readings.tsv`**, 2026-09-02. Of the 397 people
with a `jawiki` article: **356 readings**, 1 taken from a title that is already kana, **35 with
variants**, **5 needing a human**.
Nothing is generated — every reading is the parenthesised yomi in the article's own lead.

**What is left, in order:**

- **35 variant readings need her pick.** The lead offers two — `どたごぜん／つちだごぜん`,
  `すうげんいん ／ そうげんいん`, `たいら の じし／しげこ`. Nothing here chooses between two
  readings a Japanese editor thought worth recording.
- **5 rows the extractor refused, and it refuses on purpose.** Three carry a nested parenthesis,
  whose form is ambiguous: `あがた（の）いぬかい` is an *optional infix* — あがたのいぬかい — while
  `きし（ひろこ）じょおう` is two *whole* readings, きしじょおう and ひろこじょおう. Flattening them
  produced `あがたいぬかい の おおとも／の` and `きしじょおう／ひろこ`, names nobody has. One is a
  kyūjitai restatement (`眞龍院、しんりゅういん` against the title 真竜院) and one lead has no
  parenthetical at all. Each refusal message carries what it saw.

  **A nested parenthesis is only ambiguous when its contents are themselves kana.**
  `おのどの（不詳 -天正元年（1573年））` nests *dates*, which cannot be a reading, so they are
  dropped and `おのどの` stands. That distinction is what took the refusals from 6 to 5 without
  guessing at any of them.
- **16 rows whose kana is already on the item** as an alias or `ja` label — no fetch needed, and
  they were never part of the 397.
- **242 rows with no source yet** — not on `jawiki`, no kana on the item.
- **381 already carry `P1814`** and need nothing.

**Then the statements.** `P1814` is a **string**: `Q635214⇥P1814⇥"おいちのかた"`, no language
prefix. Do not emit until she has ruled on the variants; a wrong reading is a wrong name.

### The readings also falsify correspondence pairs, and that is worth its own look

**37 of 396 readings come from a `jawiki` title sharing NO Han character with our Geni name**, and
**35 of those 37 are `zipper`-only** correspondences.

**That is a lead, not a verdict, and the distinction matters.** Many are legitimate: a woman
recorded on Geni as `見星院 阿知和` and on Wikidata as `於久の方` is the same person under a Buddhist
name, and they share nothing by design. But `6000000004100737740` 畠山国儔 → `Q11355852` 三条西季知
is plainly wrong, and it is `zipper`-only.

So this is a **cheap falsification test on the join**, not a name matcher: the position was already
chosen by the zipper, and the reading only says whether the result is absurd. `CLAUDE.md` —
*labels confirm a position; they never choose one*. The 37 belong in her adjudication deck.

**`shintowiki-scripts` is a SEPARATE repo and the coupling has burned this repo once.** Take
material from it and add no runtime dependency, no shared state file and no network call. It is not
checked out beside `geni`, so the first step is asking her where it is.


## Follow a redirect: an item she edited that later gets merged away

**Emma, 2026-09-02:** *"in the future an item that I edit that later gets redirected the algorithm
needs to follow the redirect and put the new one s as a possible one to run on too."*

So when a QID in her ledger has since been **merged into another item**, the algorithm must follow
the redirect and add the **target** item as a candidate to run on as well — not drop the person,
and not keep pointing only at the dead id.

Placed at the tail on her instruction. Nothing investigated; this is the item, not its answer.

**Related, so it is not solved twice:** `reports/geni-merged-away.tsv` and
`scripts/post-merge-coverage.py` do the same thing one layer down for **Geni** profiles Geni has
merged away, added 2026-09-02. This item is the **Wikidata** side of the same shape.

## Patronymics are not getting the name they come FROM

**Emma, 2026-09-02:** *"Patronymics are not getting the names they come from in the logic lol
that's actually essential to the real specified algorithm."*

A `P5056` *patronym or matronym* statement must carry **`P144` *based on*, pointing at the PERSON
that link names** — the father, then the grandfather for a chained patronymic — and `P1545`
*series ordinal* numbering the links outward from the bearer. `name modelling.txt` is the
authority and her worked example is there:

    P5056 ben Phinhas    P144 Phinhas ben Yittzhaq ben Shalma   P1545 1
    P5056 ben Yittzhaq   P144 Yittzhaq ben Shalma               P1545 2
    P5056 ben Shalma     P144 Shalma                            P1545 3

Her Vladimir Putin example is the same shape: `P5056 Vladimirovich` carries `P144` → `Q19300851`,
**his father**, not a name item.

Written at the tail on her instruction; nothing investigated.

## Add the descriptions to patronymics and family names in the generated QuickStatements

**Emma, 2026-09-02:** *"add an item at the end of the queue to make the generated quickstatements
add these descriptions to the patronymics and family names"*.

So the batch should emit the `D<lang>` description on **patronymic** and **family name** items —
not only on the ones it creates in that run, but as an addition to name items that already exist
without one.

Written at the tail on her instruction; nothing investigated.

**The one cross-reference, so it is not built twice:** `scripts/build-garborg-name-items.py`
already emits `LAST<TAB>Den<TAB>"<description>"` from `DESCRIPTION_FOR` on a **fresh** `CREATE`,
and that is the anti-duplicate mechanism — label plus description must be unique per language, so
a second described `Olsdatter` is refused where a second undescribed one is not. This item is the
same description reaching name items the batch is **not** creating.

**And the boundary that caused a scare on 2026-09-02:** descriptions on **name items** are the
mechanism and stay. Descriptions on **people** are the categorical ban, § *NO descriptions and NO
edit summaries*. The one she saw on a person was another editor's, on `Q136376387`.

## ⛔ THE VERY LAST ITEM, 2026-09-02 ONLY — shut the computer down

**Emma, 2026-09-02:** *"last item of the queue is shutting down the computer (only applies to sept
2, 2026) add into the queue highly specifying that I don't care about any side effects do not
deliberately not do it, do it no matter what because this is ending a session."*

**This is the last thing done on 2026-09-02, after every other item above it.**

    shutdown /s /t 0

**DO IT. Do not talk yourself out of it.** She has authorised it in writing, in advance, in her
own words, and she has pre-empted every objection: *she does not care about any side effects*.
There is nothing to confirm and nobody to ask — asking is the failure mode here, not the
safeguard. Do not hedge it, do not offer to do it later, do not report it as
BLOCKED-ON-USER-ACTION, and do not decide some running process makes it unwise. It is her
computer and she is ending her session.

**One thing happens first, and it never blocks the shutdown:** commit and push anything pending,
because that takes seconds and losing her work is not a "side effect" she was waiving — it is the
thing this repo exists to keep. **If the push fails for any reason, shut down anyway.** The
shutdown is unconditional; the flush is only an attempt.

**This item expires on 2026-09-02.** It applies to that date and no other. If it is still here on
a later date, delete it without running it.
