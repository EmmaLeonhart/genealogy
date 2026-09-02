# Queue

Only work. Every specification and record moved to `CLAUDE.md` on 2026-09-01 at her instruction: *"remove all the 14 bullshit queue items"*. An item is DELETED when done, never annotated.

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

**MEASURED 2026-09-02, and the campaign is two people from done.**
`scripts/post-merge-coverage.py` → `reports/post-merge-coverage.tsv` applies her stopping rule
directly: **25 of 27 survivors are covered**, and `exports/post-merge/` now carries **23,374
distinct people** from six `Forest` balls. Her clustering economy is exactly what happened.

**The two that remain are each missing ONE first-degree relative**, and both survivors are already
in the directory:

| survivor | missing |
| --- | --- |
| `6000000001893120054` Obito Haji-no-muraji (**strong**) | `6000000001893090174` 土師兎 |
| `6000000001846508982` Jingū-kōgō (weak) | `6000000179131744821` Ōjin Tennō |

So this needs **one or two exports**, seeded on those two relatives or on somebody who reaches
them — not an open-ended campaign. Re-run the script after each; it is the same shape as
`bure-coverage.py`, which ended that campaign at 251 of 251.

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

**412 drops are falsifiable** — both ends inside a post-merge ball, 160 parent / 160 child /
92 spouse. Those are the genuine *Geni deleted this link* candidates and the only population an
override should ever touch.

**GRADED, and the grading is `scripts/grade-post-merge-drops.py`** — which already existed and
which I failed to notice before writing a weaker analysis over the top of its output. A drop is
`link-gone` when both people are present in some `exports/post-merge/*.ged`, `out/merged.ged`
gives them a family in common, and **no post-merge record does**:

    link-gone                        408      parents 159 · children 159 · spouses 90
    link still present                 2
    no shared family in merged.ged     2

**So 408 of the 412 are real deletions**, and Emma has already ruled on what to do about it,
2026-08-29: *"For now leave these things and still run them, but put them at the end of the
queue, I lean on the idea of saving them but do not have bandwidth to process this now."*

**A reading-by-eye of the names contradicted this and was wrong.** On 2026-09-01 I read the 412
as *"real relationships, in reciprocal pairs"* and concluded the override still looked wrong. The
reciprocity is not evidence: the OLD exports carry both directions, and the question is whether
the POST-MERGE ones record a family at all. They do not, which is exactly what `link-gone` means
and what the structural grader measures rather than infers.

Depends on `reports/geni-stale-duplicates.tsv` (13 strong, 3 medium, 13 weak) and
`reports/geni-merges-performed.tsv` (180 survivors from her activity feed).

### English names ON GENI — MOVED TO THE TAIL, 2026-08-29, her call

**Emma, 2026-08-29**, asked whether her *"we don't actually need to edit your geni at all"* ruling kills this: *keep it but move it to the tail.* Still wanted, but it should stop being the first thing every work tick looks at and skips.

**The label half is NOT here and is not parked** — our `mul` and the CJK-only people are live work; see the analysis of 2026-08-29 (45 transliteration tokens block every remaining `ja`/`zh` label). What is at the tail is only the part that writes names **onto Geni**.

### English names ON GENI — the deferred half, and it is narrow

**Only the Geni-editing part was deferred**, not the English-label rule. Emma, 2026-08-29,
correcting my reading of her *"we just do not add a label"*: that sentence parked writing names
**onto Geni**, and nothing else.

**What the value is, when it happens:** *"the entire thing is whatever our pipeline puts as the
multilingual label on Wikidata. That is what our pipeline should be putting as the name, as in
Geni."* So the Geni name comes from our `mul`, not invented per-person and not taken from a
Wikipedia title.

**Her actual concern is CJK-only labels** — people whose Geni name exists only in Han/kana/hangul
and who therefore have no English form anywhere. Those are the ones this campaign is for.

**Already done and not part of this:** the `P1810` qualifier. It carries **what Geni literally
says** — `<private> Garborg`, `Private`, `Unn (Bitten) Garborg` — while the label beside it is the
normalised `NN Garborg`. Her rule: *"we do it with whatever's on Geni, not whatever is all in
Wikidata. This is a qualifier thing."*

Her closing note on how I handled this, kept because it is the correction: *"This is a relatively
well-defined task that you decided to transform into something crazy."*

### Get the REAL parents behind the NN placeholders — and FIRST, cost it

**Emma, 2026-08-29.** Two rulings, and the second governs whether the first ever runs.

**The representation.** *"Both parents are 'NN' placeholders. Pipeline generates names for them.
However we may attempt to gain the information of the parents. Imo this is too large to do right
now, but at the end of the queue we will have a task that goes to one of the siblings and save
their page so the parent names and potentially other people are added. If half siblings we go to
both siblings to clarify."*

**Page-saving was ABANDONED once, and the reasons are hers.** *"I gave up on the page-saving system
for a reason, because it was taking far too long. Part of this was due to extreme inefficiency and
frustration about your behaviour with it. Part of it was due to extreme inefficiency in terms of
lack of compliance from you on doing it at a reasonable rate. Part of it was that the actual site
itself was way too slow."*

**What is different now is SELECTIVITY, and that is the whole bet.** *"we're only saving pages in a
very selective way... selective enough that it's not going to be harmful... only to ones that are
important at a significant level."* The old campaign saved everything; this one saves only the
sibling groups that matter.

**So the FIRST deliverable is a time estimate, not pages.** *"My expectation still is this is going
to occur within a reasonable time frame, or it's not going to occur. By extension, as an extension
of this thing, I want you to actually measure how long it takes. Make predictions about how long it
takes."* Measure the real per-page rate, predict the total, and put that to her before saving a
single page beyond the sample the measurement needs.

**The half-sibling question decides how big the job is, and it is OPEN.** *"I don't believe we have
half-sibling information. We might have it, or we might not... I'm not the most clear on whether
half-siblings versus full-siblings are properly recorded like this or are accessible within the
actual chain information itself. I don't think it is, but I think it might be. If it is, then we'd
be able to preemptively do the calculation. If it was not within it already, we'd have to do
something much more exploratory."*

- If the chain data marks half siblings, the count is computable up front and one page per group
  suffices for the rest.
- If it does not, every group is potentially a half-sibling group, which means **two** pages each
  and a much larger, exploratory job.

**4,924 placeholder parents exist today** — 2,284 from the saved pages, 2,640 from the paths, one
pair per sibling group. Half siblings found on saved pages are currently skipped entirely rather
than given placeholders, because they share one parent and giving them two would assert a marriage
that did not happen.

**NOT NOW.** Emma, same message: *"This is an edit to the cube item. Do not do any fucking
calculations right now!"*

### Anonymise, shrink the CI checkout, then go public

**Emma, 2026-08-29**, on `reports/public-repo-analysis.md`: *"we will optimize the cicd revisions to
be small and do other things to optimize filesizes for the runners but can 100% do all this stuff if
we anonymize it properly"*

Three pieces, in her order:

- **Shrink what CI checks out.** A run does not need the 12.2 GB working tree — `.css` and
  `.download` under `geni-scraping/` are 1.9 GB of page furniture, and the compose step reads only
  the derived CSVs.
- **Anonymise.** The gate on going public. ~96,000 rows concern people Geni treats as private.
- **Then public**, which makes Actions minutes free and lets the daily emailed batch run.

**The constraint the design must start from:** the Geni profile ID is both the identifier and this
repo's primary key, so it cannot be hashed or dropped without breaking every join, the `P2600`
statements and the spines. Redacting content while keeping structure is the likely shape.

**The memory ceiling is untouched by any of this** — the merge peaks at 16.8 GB against a 16 GB
runner, so the synoptic tree still cannot be rebuilt in Actions without a larger runner.

### LAST ITEM — run `scripts/rebuild-everything.py`, then attach the batch

**Emma, 2026-08-29:** *"end of the queue is a rebuild of the tree and then after it is to build the
quickstatements and attach the file"*, and then, on being shown it was five scripts in a fixed
order: *"this explains why it's so hard: because it's not one script it's a bunch of scripts that
you need to remember to run in the right order. Nope make it one script that always ends by calling
the script that regenerates the quickstatements. This script is called as the last queue item."*

    python scripts/rebuild-everything.py

That is the whole item. It runs merge → display-names → derived family → derived facts → derived
labels → pack → `--compose`, stops at the first failure rather than continuing on stale inputs, and
ends with the batch. Then attach `reports/wikidata-garborg-day.qs`.

**Run it alone.** Step 1 peaks near 17 GB and has been killed twice when something else was running.
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

- **`en` for every individual, as one step.** Includes the transcription she names:
  a Han-only or Cyrillic-only or Hebrew-only person gets an `en` made for them.
  **CJK → English is agentic, never programmatic** — *"from CJK to English do not
  remotely try to do any kind of programmatic transliteration because they all suck.
  But AI almost always knows Japanese to Romaji."* The culture question comes first:
  陳 is *Chen*, *Chin* or *Jin*, and *"the tree settles it, via neighbours and which
  exports they came from"*, never the name. 806 Han-only among the structural
  placeholders alone; the corpus figure is larger and is what this step must count.

- **8 tokens the transliteration funnel still cannot read**, of 627 needed. The section that
  used to point at this said *"at the tail as § the tokens the transliteration funnel cannot
  read"* — a section that does not exist, so the pointer dangled and the work was invisible.
  Stated here instead. From the last full run they are `""Inge""`, `"Ingebret`, `Garborg"`, `I,`,
  `Talgje,`, `Törnstjerna,`, `Queen`, `Карлов` — six are **tokenisation debris** (a stray quote or
  a trailing comma carried into the token), one is a **title** rather than a name, and one is
  Cyrillic. So the fix is mostly in the tokeniser, not the engine, and a token it cannot read is
  correctly left out rather than guessed at.

- **The 1,539 with no label and a named relative are HERE, not in the placeholder work.**
  Traced 2026-09-01. They are in `reports/label-gap.csv` with outcome `relative`, they are in
  `reports/derived-family.csv`, and **none of them reaches
  `reports/relationship-label-preview.csv`** — correctly, because `is_placeholder()` returns
  False for them. They are not unnamed.

  **They have real names, in scripts nothing here transcribes.** Measured over their `NAME`
  records:

  | script | rows | |
  | --- | ---: | --- |
  | Han | 2,173 | `陳母`, `句芒` |
  | Cyrillic | 359 | `Иоанн Всеволодович` |
  | Han+Latin | 344 | `Jew Law Ying 趙羅英`, `Wo Deng 握登` |
  | Hebrew | 140 | `זלדה`, `חיים אהרון` |
  | Latin | 92 | `(Molher de Bernat Gòt)` — parenthesised descriptions |
  | Latin+Tibetan · Hangul · Arabic · Hiragana · Greek | 107 | the tail |

  So the work is the transcription this section already specifies — *"a Han-only or Cyrillic-only
  or Hebrew-only person gets an `en` made for them"* — and for the CJK majority it is **agentic,
  never programmatic**, with the culture question settled by the tree first.

  **The queue said "935 of them CJK-named" and that was wrong.** 107 is the count of those whose
  *relative* carries a CJK name; the number that matters is how many carry one **themselves**, and
  Han alone is 2,173 name rows. Both figures were in the file at once and neither was labelled.

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

**At the tail, her call 2026-08-31.** It is a mass operation over the whole population and the live work is hyperlocal, so it was being read and skipped every tick. Nothing about it changed except its position.

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

## A CI/CD job that archives the ledger's Wikidata items locally

**Emma, 2026-09-01:** *"a thing that downloads a local archive of the wikidata items in the ledger
in a ci/cd run. So the ci/cd run will make the archive (committed) and the pages and the
quickstatements for me to run later."*

**Every QID in `reports/garborg-qids.tsv`** — 1,089 rows and growing — fetched as **full items**
and committed. Not a summary: `CLAUDE.md` § *A SUMMARY of a Wikidata item is not the item* records
three false findings published from a summarising channel, including reporting that
`Q467497` *Arne Garborg* had no `P22`, `P25` or `P3373` when it has all three.

**Why a fresh archive rather than the store under `wikidata/items/`.** That store is a Geni-shaped
slice downloaded before she made most of these items, so it agrees that Arne has no parents. These
are *her* items, edited by hand continuously, and the ledger is exactly the set where our copy
goes stale fastest.

- `genimerge.wikidata.full_entities` already fetches whole items in one batched request —
  `wbgetentities` takes 50 ids — so ~22 requests for the whole ledger. Be polite about the rate.
- **Fail loud on a short fetch**, the way `scripts/refresh-p2600-all.py` refuses to write one. A
  partial archive that looks complete is the failure mode this repo keeps hitting.
- **Commit it gzipped** if it passes 100 MiB; ~1,089 full items is likely under it, but
  `scripts/pack-derived.py` is the existing pattern and `.gitignore` takes one explicit line per
  path, never a `*.json` pattern.
- It runs in the same workflow as the batch, so one dispatch produces archive, Pages and
  QuickStatements together.

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

**So what is left is only the other two deliverables**, and each waits on its own item above:

- **the ledger archive** — § *A CI/CD job that archives the ledger's Wikidata items locally*
- **the Pages site** — § *THE VERY LAST ITEM*

Once both jobs exist, dispatch once and check that a single run produces all three. Not three runs
— her words are *"the ci/cd run"*, singular.

**Two failures got it here, and both are worth not repeating.** The 18:59 run died on
`FileNotFoundError: out/merged.ged` and was fixed by committing `family-structure.tsv.gz`, listing
it in `pack-derived.py` and giving `read_tree` a fallback. The 21:50 run then died on
`sqlite3.OperationalError: no such table: items`, because `out/wikidata/store-index.sqlite3` is
gitignored and `sqlite3.connect` **creates an empty database** rather than raising. Both are the
same shape: **a file the runner cannot have, reached by code that assumed it could.** Anything else
added to this workflow should be checked against `.gitignore` first.

## The merges, with an HTML page to work them from

**Emma, 2026-09-01:** *"merges put them at the end of the queue with an html page for them"*.

Emma, 2026-08-31: *"Just make a 'merges to do' file that records these merges and the wikidata
duplicates and all the other things we went over that's a file I'll use tomorrow to do merges
manually on my own with the quickstatements session."*

`python scripts/build-merges-to-do.py` rebuilds it. Regenerate it when
`out/wikidata/p2600-all.tsv` or `reports/garborg-qids.tsv` is refreshed, so the duplicate
counts are not stale when she next sits down to it.

**The merges themselves are hers now, not mine** — that is what the file is for. The Izumo
three are cleared and the browser pass is closed.

**The page is the new half.** `reports/merges-to-do.md` is 8 sections of markdown and she works
through it by hand; the adjudication deck showed what a page buys instead — she cleared **207
pairs in one sitting** off a page and had answered none off the equivalent TSV.

- **Build it from `out/parent-review.template.html`'s design**, not from scratch. That template is
  hers, hand-approved, and rebuilding it from scratch on 2026-09-01 was a mistake she named:
  *"did you regenerate it from scratch instead of using the template you used yesterday lol"*.
  Same fonts, same keyboard flow, same `localStorage`.
- **One card per merge**, showing both items side by side with the evidence that decides it:
  label, sex, born–died, property count, sitelink count, and which sources found the pair. The
  deck's lesson applies exactly — *"the problem with that html is it didn't give that good
  feedback"* — so a card without sex and dates is not worth building.
- **The prefilled `Special:MergeItems` link is the action**, in the direction `Help:Merge` wants,
  with a one-key way to mark a card done. It never performs a merge.
- **Section 8 is the one that needs eyes most**: those pairs come from the zipper, which carries a
  measured 2.8–4.8% error, and § 1's pairs are already spot-checked.
- Regenerate it with the file, in the same pipeline step, so the page is never staler than the
  markdown.

## THE TRUE LAST ITEM — remove the spine and every trace of it

**Emma, 2026-09-01:** *"put the removal of the spine [stuff] and all traces of it as the true last
item"* — after the Pages site, after the ledger archive, after the CI/CD dispatch. It was on
2026-09-02 and it is now the end of the queue instead.

**Its precondition is met and was checked rather than assumed.** The 2026-09-01 generation reports
`spine arne-garborg-to-johannes-bureus-geni: every step already has an item`. All 18 steps hold a
QID; the batch she ran that afternoon created **Sara Carlberg**, step 13, the last one missing, and
her `CREATE` carried the link in both directions plus the `P22` to the father Maria Carlberg
already shares. Re-check it at the time anyway — if a step has regressed, say so rather than
deleting a live mechanism.

**Every trace, which is more than two constants:**

- `SPINE_PATHS` and `SPINE_REVERSED` in `scripts/build-garborg-day.py`, and every block that reads
  them.
- The spine handling in `scripts/build-missing-reciprocals.py`.
- `scripts/check-spine-bonds.py`, and `reports/spine-already-on-wikidata.tsv` if nothing else reads
  it — `build-garborg-day.py --known` names that file explicitly, so check the flag's other callers
  before removing it.
- Anything else matching `spine`. Measured 2026-09-01, 14 files carry the word — grep again at
  the time rather than trusting this list:
    - `scripts/build-daily-batch.py`
    - `scripts/build-from-diff.py`
    - `scripts/build-garborg-day.py`
    - `scripts/build-missing-reciprocals.py`
    - `scripts/build-samaritan-spine-gedcom.py`
    - `scripts/build-samaritan-spine-page.py`
    - `scripts/check-spine-bonds.py`
    - `scripts/compare-samaritan-sources.py`
    - `scripts/measure-three-seed-eccentricity.py`
    - `scripts/refresh-garborg-ledger.py`
    - `scripts/refresh-spine-known.py`
    - `scripts/samaritan_spine.py`
    - `scripts/search-spine-names.py`
    - `scripts/verify-spine-candidates.py`
- The `CLAUDE.md` paragraphs describing the spine as live work. `§ THE THREE LINES` already records
  the first three as **legacy**; this makes the fourth legacy too, and the section becomes history
  rather than instruction.

**⛔ "spine" NAMES TWO DIFFERENT THINGS AND ONLY ONE OF THEM GOES.** Of the 14 files matching
the word, five are the **Samaritan high-priest succession** — `samaritan_spine.py`,
`build-samaritan-spine-gedcom.py`, `build-samaritan-spine-page.py`, `compare-samaritan-sources.py`,
`search-spine-names.py` — which has nothing to do with Arne→Bureus. Deleting those would destroy
work Emma built by hand and has ruled finished (`CLAUDE.md` § *The Samaritan family relationships
are DONE*).

This is precisely § *Do not grab the first artifact that vaguely matches*: a name that resembles the
thing being removed is not the thing being removed. **Read what each file's spine IS before
touching it.**

**`paths/arne-garborg-to-johannes-bureus-geni.tsv` STAYS.** It is a saved Geni relationship path —
evidence from outside our own data, in the class `CLAUDE.md` § *Relationship paths: save the page*
protects. The machinery that walked it goes; the record of what Geni said does not.

**And no export is ever attempted on it.** Steps 9, 10 and 13 were refused by Geni on 2026-08-30 —
*"You are not allowed to export that profile."* That stays true after the code is gone.

**`CLAUDE.md` § *LEGACY CODE IS DELETED* is the standard here:** the test is *does the pipeline read
this*, not *might this be useful*. Everything is in git, so a deletion is recoverable and a stale
special case is not recoverable from the confusion it causes.

## The 7 tokens the transliteration funnel cannot read

**Her instruction, 2026-09-01**, on being shown this: *"Also add this to the end"*.

**7 of 627 needed tokens have no reading.** It was 8 until 2026-09-01, and the one that left is
the reason to look at a list like this rather than trust it: **`Ånon` was never debris.** It
transliterates perfectly — `オーノン` — and the corpus token was `A` + a combining ring rather than
the precomposed `Å`. One `unicodedata.normalize("NFC", …)` fixed it and **3,377 other tokens** that
were failing the same way without ever appearing here.

The item went unnoticed for so long because § *Labels in seven languages* pointed at *"the tail as
§ the tokens the transliteration funnel cannot read"* — **a section that never existed**.

    ""Inge""   "Ingebret   Garborg"   Talgje,   Törnstjerna,   Queen   Карлов

**Five are tokenisation debris, not names.** A stray quote or a trailing comma has been carried into
the token: `Garborg"` is `Garborg`, `Talgje,` is `Talgje`, `""Inge""` is `Inge`. The engine is
being handed punctuation and correctly refuses it — **so the fix is in the tokeniser, not in
`translit_no.py`**, and fixing it there would be widening a reading rule to swallow junk.

**The other two are not that and must not be swept in with them.** `Queen` is a **title**, which
belongs with `NN`, `of`, `son` in `SKIP` rather than being transliterated — a katakana rendering of
the English word *Queen* is the exact failure that list exists to prevent. `Карлов` is **Cyrillic**,
which the Norwegian orthography reader cannot read by design; it needs `translit_scripts`, not this
engine.

**A token it cannot read is left out and reported, and that stays true.** The module says so
itself: *"a missing row means no `ja`/`zh` for that name, which is the current behaviour and is
honest; a guessed row would put a wrong name on a person in two languages at once."* This item
removes the debris so the count reflects real gaps, and does not lower the bar for what gets a
reading.

## How to handle the saved pages and path files, which all begin with her

**Her instruction, 2026-09-01:** *"put that as the last queue item to figure out how to deal with
the paths page files"*.

**The anonymisation pass could not touch these and stopped at the boundary.** Every file under
`paths/` and `geni_pages/` starts at the account owner, because that is what Geni renders: a
relationship path is *from the viewer to X*, so step 1 is always her and her profile id is in the
data itself. `reports/display-names.csv`, `derived-labels.csv` and the corpus under `exports/`
carry her the same way — as a person in the tree.

**One test asserts it and must keep asserting it.**
`tests/test_genipage.py::test_the_real_saved_page_yields_the_whole_jimmu_path` checks
`links[0].geni_id` against the real saved page. The 2026-09-01 pass renamed it, the test went red,
and it was changed back with a comment: renaming it would make the test assert something the file
does not contain, which is falsifying evidence rather than anonymising a docstring.

**So the question is what "anonymised" means for evidence, and it is hers to answer.** Four
readings, none obviously right:

- **Nothing to do** — these are data about a real tree, not documentation about her, and the
  documentation is what she asked to be cut. The 599 files carrying her name are almost all
  `exports/*.ged`, which are never edited.
- **Regenerate the paths from a different viewer**, so step 1 is somebody else. Costs re-saving
  every page from Geni and loses the provenance of what was saved when.
- **Keep the files, scrub the reports** — leave `paths/` and `geni_pages/` alone and make the
  derived layer not name her.
- **Rewrite step 1 in `paths/*.tsv` to a placeholder**, which breaks the join back to the page it
  came from.

**Do not guess between these.** The pass that prompted this already made one wrong call by
renaming an assertion about a real file; the cost of the same mistake across 586 path files is
much larger.

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

