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

## How to read this file

**Emma, 2026-08-27:** *"Organize the queue to make it usable again, currently it does no appear to
be usable."* It was not, and the reason was structural rather than volume: **five sections declared
themselves the front** — the mass export campaign, the algorithm review, `THE EXPORT LOOP` (*"it is
the top of this file"*), `THE AGENDA` (*"everything else is secondary"*) and `RUN ORDER` — while
**ten declared themselves the tail**. With both ends contested there was no order to work in.

**The order is now position, and nothing else.** Top to bottom. Two conventions, both hers:

- **Bullets, never numbers** — `CLAUDE.md` § *Queue items are BULLET POINTS*. A number is a promise
  the item will still be there.
- **An item is deleted when it is done**, in the same commit as its `devlog.md` entry. A section
  still here is a step not yet taken.

**Everything titled `LAST` / `THE LAST ITEM` / `THE TAIL` is now physically at the end**, in one
run, so "last" means last. Nothing was reworded and nothing was dropped — only moved.

**Some sections are SPECIFICATIONS, not steps**, and are worth knowing about before working the
ones above them: `THE EDIT ALGORITHM`, `THE DAILY ALGORITHM`, `THE TAIL ALGORITHM`,
`Link reliability order`, `The chain of provenance`, `How the synoptic tree is actually made`,
`PREREQUISITE ORDER`. They describe how a thing is done rather than asking for it to be done.

## 0. Aug 28, 2026 manual adds

These are supposed to be manually added to the queue and worked on, do no just paraphrase during the rebase keep this part entirely intact. We are approaching usage limit for now.

## The queued tasks, IN HER EXACT WORDS — the times are ORDERING, not schedule

Emma, 2026-08-27: *"just look over the chatlog and remake all of them as queue items over this
bullshit. The queue items all need my exact words the times were meant as ordering."*

**These were cron jobs. Cron text lives only in memory and three of them were destroyed by being
re-typed from memory, on the evening she said the exact wording is the most important thing.**
That is why they are here. **Do not paraphrase these. Do not summarise them. Do not append
"where to look" hints** — one of the destroyed prompts was her message alone, and the replacement
bolted on a hypothesis that would have biased the analysis before it looked at anything.

Work them **in this order**. The clock times are how she expressed the order and nothing more.

**Bullets, never numbers.** Emma, 2026-08-29: *"no numbering the queue isn't really what I want I
was just repeating your pattern"* — the numbering here was mine and she was echoing it back.
`CLAUDE.md` § *Queue items are BULLET POINTS* already said so and gives her reason: a number is a
promise the item will still be there, so deletion feels like renumbering everything else and items
accumulate instead of being blasted through. Order is position; nothing else is needed.

**Done and deleted so far:** the `Q141198538` `nn`-first-name item — fixed in `_carries_marker`,
pinned by `tests/test_garborg_day_batch.py::test_a_marker_beside_a_real_name_still_takes_the_nn_path`.

---







| ---: |
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
- **`P1449` *nickname* is modelled and no longer emitted** — `d97e92c2` dropped it from
  `build-garborg-day.py` (a Norwegian nickname tagged `en`), `model-vs-reality.py` still models
  it, so the diff reports **66 `missing`** that nothing will ever emit. Decide which side is
  right; do not silence it by filtering the column.
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

23 + Emma, who has `Q232803` and needs an id rather than a creation, is **24** — the spine
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

## What is actually left in `entity_resolution.md` — measured live 2026-08-29

Emma, shown a claim that the file was not to be acted on: *"Uhh I don't know if there's any useful
info in this lol."* Checked rather than guessed — one batched `full_entities` request over all
eight items the file names. **There is, and it is small.**

**One of her three label edits never landed:**

| item | she wrote | live 2026-08-29 |
| --- | --- | --- |
| `Q19657284` | `en` *Buyeo Deokjang* | done — `mul` *Buyeo Deokjang* |
| `Q12598947` | `en` *Buyeo Taebi* | done — `mul` *Buyeo Taebi* |
| `Q11443857` | *"change her name to Mononobe no Futohime"* | was **not** done; now in `CJK_CLAN_BLOCK`, so every batch carries it until it lands |

**Six of the eight items carry no `P2600` at all**, so the Geni pairings the file records exist
nowhere Wikidata can see: `Q11596350` *Prince Wakatakehiko*, `Q11078587` *Harima no Inabi no
Ooiratsume*, `Q24890131` *Mononobe no Ikofutsu*, and the two Kitajima items. Only the two Buyeo
items have one.

**Three of those six are out of scope and stay so.** The two Kitajima items are in
`NEVER_TOUCH_QID`, and her own `Q232803` entry is the one she said she will remove herself.

**So the residue is three edits**: `P2600` on `Q11596350`, `Q11078587` and `Q24890131`. The
Futohime label is handled — she asked for it in the clan block on 2026-08-29 and it is there.

The three `P2600` statements were **not** written, and that is deliberate rather than pending: the
nine pairs belong to her dictated item 11, whose method is to put the Wikidata link in each Geni
bio and then run a `Forest` export per person, not to write `P2600` from here.

## The eight Asian identities — bios get their QID links AT SYNOPTIC-MERGE TIME, not now

**Emma, 2026-08-29, correcting a recovered plan that a later discussion had already replaced:**
*"No fuck you you didn't get the later discussion. When the synoptic tree is merged we change all
of their bios to links to their qids so that the next step in with the wikidata union (which isn't
really implemented yet) they get joined with those wikidata items lol."*

**So there is no standalone Geni-editing task here, and no export campaign for these eight.** The
bio link is a *step inside the synoptic tree build*, and its purpose is to feed the **Wikidata
union**, which is not implemented yet. Nothing about these people is actionable until that build
runs.

**The eight** (everyone in `entity_resolution.md` but her): `Q11596350` Wakatakehiko · `Q11078587`
Harima no Inabi no Ōiratsume · `Q11443857` Futohime Mononobe · `Q24890131` Ikofutsu Mononobe ·
`Q19657284` Buyeo Deokjang · `Q12598947` Taebi Buyeo · `Q135579480` Yasutaka Kitajima ·
`Q135579474` Tokitaka Kitajima. Every one is an Asian identity she *"put a lot of effort into
creating identification with"*, for this purpose. That is why their `P2600` statements are not
loose ends to write by hand.

**What was actually lost in the crash, and it is worth keeping straight from what was superseded.**
A cron for 03:00 on 2026-08-29 held the *older* plan — edit the eight bios now, then a `Forest`
export each, file them for the post-merge stage. Crons are session-only, the session died at 18:52
on 08-28, and it never fired. Recovering it was right; presenting it as live work was not, because
§ *The Wikidata link goes in the bio during the SYNOPTIC TREE BUILD* already recorded the
replacement. **The transcript is not the authority when `CLAUDE.md` has a later ruling on the same
thing.**

**Her own entry leaving `entity_resolution.md` still stands and is still hers.** After it goes,
confirm `paths/bergitte-to-emma.tsv` step 1 does not become a `CREATE` — by running `--compose` and
reading the output, not by reasoning about `NEVER_TOUCH_*`.

## The nickname strip belongs in `derive-labels.py`, not only in the daily batch

`without_nickname` in `build-garborg-day.py` fixes the label the batch emits — Emma's
`Q141199868` case, `Ingvold (Pinkie) Remmie` → `Ingvold Remmie`. It is applied at the point of
emission, so `reports/derived-labels.csv` still holds the bracketed form and **every other reader
of that file still sees it**. 57 scripts read it; 48 read `label_en`/`label_mul`.

**The population is 22,707 nickname tokens inside `GIVN`** — 16,742 parenthesised, 5,965 quoted —
so this is the same shape as the married-name flip, which was fixed at source precisely because
fixing it there reached all 48 readers in one change.

**And `namemodel.QUOTED` treats an ASCII apostrophe as a quote delimiter.** On
`Jean d'O Seigneur d'O & de Maillebois` it matches `'O Seigneur d'`, so that name yields a
`P1449` *nickname* of `O Seigneur d`. `without_nickname` skips apostrophe matches for the label;
the name statements are **not** fixed. Narrowing `QUOTED` moves every `P1449` in the repo, so
measure the affected population before changing it.

---

# THE TAIL, PART TWO — the sections that each called themselves "last"

Her own dictated tail block is above, from `# THE TAIL OF THE QUEUE — Emma, 2026-08-18`. This
second block is the ten-odd sections that had each independently titled themselves `LAST`,
`THE LAST ITEM` or `THE VERY LAST ITEM` and were scattered through the file. They are collected
here so the word means something. Nothing was reworded; only moved.


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

## LAST — incidental findings from the review, to look at when it is over

- **Two tests fail after the ledger regeneration** (2026-08-27, 1,415 passed / 2 failed):
  `test_garborg_day_batch.py::test_the_ledger_and_the_batch_do_not_both_claim_a_person` and
  `test_generated_inventories.py::test_the_batch_inventory_names_exactly_the_batches_on_disk`.
  The ledger went 164 -> 130 -> 209 rows, so the batch and the ledger now overlap where they did
  not before, and a new `.qs` exists that the inventory does not list. Neither is urgent.
- **`labels.strip_markers()` was rewritten twice on 2026-08-27** — first to delete markers, then
  to preserve and normalise them to `NN`. The deleting version shipped and touched a batch. Check
  nothing carries a label it produced.
- **Uncommitted at the time of writing:** the `strip_markers` rewrite and the regenerated ledger.

## LAST — name items are being MERGED by other editors. Stop preferring creation over reuse

**Recovered from the same crashed session; she asked for it at the end of the queue.** Emma,
2026-08-29: *"I've noticed that certain names, for example Tunheim, I've noticed that some of these
names got merged in with an existing item. I'm extremely confused how this happened, and it seems
to me to indicate maybe you're not actually checking the existence of the names correctly in our
data. Having a strong preference for creating new name objects versus using the existing ones is a
very wrong move here. Creating the name objects and having them merged by somebody else (and this
is important) is a thing that gets attention in a bad way."*

Two things, in order:

- **Find out how the existence check missed them.** Start from the name items the batches have
  created, find which have since been merged away by another editor, and work back to what the
  lookup did at the time. A diacritic is *not* the first explanation to reach for — `CLAUDE.md`
  records that folding them invents ambiguity — so measure before theorising.
- **Then invert the default.** Reuse an existing name item unless there is positive evidence the
  usage differs. § *One name item per USAGE* still holds: a given name and a family name spelled
  alike are genuinely two items; two spellings of one family name are not.

## LAST — a comprehensive CJK fallback so nothing is ever emitted untransliterated

**Recovered from the crashed session; she put it at the very end.** Emma, 2026-08-29: *"setting up
a comprehensive fallback... probably using external libraries for doing katakana, so that it is
very consistent. If anything even remotely wants to generate without having katakana or Chinese
characters, it goes through this thing and then adds the token to the library, and then continues
on."*

So the shape is a **funnel, not a table lookup**: an unknown token is transliterated on the spot,
written into `reports/garborg-name-transliterations.tsv`, and the caller carries on — rather than
`label_in()` returning `(None, None)` and the whole label being dropped.

**Her standard, and it should not be softened:** *"Incorrect romanization or incorrect
representations in katakana are totally acceptable. An incorrect name is not, because half these
words, nobody knows how they're pronounced anyway."* That relaxes *partial is worse than absent*
for the **rendering** of a token and for nothing else — a wrong *name* stays forbidden.

**This is the one place an external dependency is sanctioned.** `CLAUDE.md` § *Stdlib only* allows
one where the stdlib genuinely cannot do the job, and she has named this as such a case.

## THE VERY LAST ITEM — review the algorithm once we are connected to the World Tree

**Emma, 2026-08-27:** *"eventually we will reach a point where we are actually connected to the
world tree. Once we are actually connected to the World Tree on Wikidata, this raises some more
concerns... the last queue item should be a sort of review. You should be putting it at the very
end of the queue once we connect to the World Tree."*

**Her proposal, in her words:** *"a sort of stateful feature ledger that expands by about one hop
each day, plus all the people that we create to the eligible people. It still very much focuses
its creation around this particular neighbourhood, but I'm not even sure whether that would be
needed because I don't know enough about what's going to happen once the World Tree is
connected. This might be assuming a scenario where once the World Tree is connected, the eligible
people explode, but that might not be the case."*

**Two things established 2026-08-27 that this review should start from rather than rediscover.**

- **The eligible set probably does NOT explode, and the reason is `universe`.**
  `wikidata_subgraph(universe=set(have.values()))` counts an edge only when **both ends are items
  we hold**. Connecting Arne to Charlemagne therefore cannot pull the world tree in; the walk
  still cannot leave the ledger. That restriction exists because without it, adding Bureus
  `Q633094` as a root took the group from 97 items to **1,339,336** in one step.
- **What she describes is close to what the code already does.** Creations land in her
  contributions, the refresh pulls them into `have`, and the subgraph grows to whatever they
  newly connect. The daily hop is the ring; the "plus all the people that we create" is the
  refresh. What is *not* there is any explicit statefulness — no history, no record of what was
  eligible yesterday.

**The world-tree-agnostic algorithm she half-remembers was never written.** Emma: *"We did have a
world tree-based, agnostic algorithm earlier, but that one's not the most clear about what it was
supposed to be doing. I don't know if the spatially agnostic algorithm is one that was actually
written."* Checked against the whole history: the only match is `a901fd59` (2026-08-12), *"Save
the world-tree route as an ordered priority chain: 17 edits"* — a route and a priority list, not
a selection algorithm. Nothing has ever selected people world-tree-agnostically.

**Trigger:** when a person in `have` is connected on Wikidata to the 1,339,227-item component
containing Charlemagne. That is checkable offline against `out/wikidata/relations.tsv` and should
be measured, not waited for by eye.

## NOTE from the review — what `universe` actually means, and the bridging risk it creates

**Her restatement, 2026-08-27, after the `universe` restriction was explained:** *"having
explained the universe thing to me better and how it needs to be a path between my items. As I
understand it, a path between my items can be filled in, or one hop off of any of my items, with
that thing in mind."*

That is exactly right, and it is worth keeping in her words because it is the clearest statement
of the design anywhere: **the subgraph is the set of paths between her own items**, and **the ring
is one hop off any of them**.

**The risk she then identified, which nothing currently checks.** *"it means that we could
potentially start to see some of the European-to-Asian street stuff behaving weird, because in my
items most of them are Scandinavian, but there are those Korean things and a couple more remote
answers and some more remote people."* Her items are overwhelmingly Norwegian and Swedish with a
few Korean, Japanese and Samaritan outliers. If a chain of edits ever connects those clusters
through her own items, the subgraph joins them and the ring starts growing at both ends of a
bridge nobody intended. Worth measuring before it happens: which of her items sit outside the
Scandinavian mass, and what would have to be linked for the walk to cross.

**And a caution against fixing it prematurely.** *"I don't want to over-engineer statefulness into
the system when it's not needed. A statefulness of one person, like a statefulness of 'every day
there's an additional hop', is something that would conceivably make it lighter. I'm also not even
100% sure, because that might make it explode quite fast too."* So: do not build daily-hop
statefulness on the strength of this note. It could bound the growth or accelerate it, and which
one is an empirical question.

## LAST — ingest the saved pages and paths into the tree

**Emma, 2026-08-28, and she guessed it before it was checked:** *"you never actually
bothered with any of the actual ingestion logic of the paths... The saved pages had their
names, plus all their immediate relatives, siblings, spouses, children, and those people's
names and display names, and Geni links."*

**Confirmed.** `genimerge.sources.find_exports()` globs `*.ged` and nothing else, so the
merged tree is built from GEDCOM exports alone. Everything below is read only by reports
and seed-picking scripts, never by the merge:

| source | count | holds |
| --- | ---: | --- |
| `geni-scraping/` | 1,556 pages | name, Geni id, immediate relatives with their names and ids |
| `paths/` | 697 TSVs | relationship chains, one person per step, with ids |
| `geni_pages/` | 28 saved pages | the same, plus the relationship panel |

**Why it matters:** these are the only evidence in the repo that comes from *outside* the
exports — they name people whether or not any export reached them. `CLAUDE.md` already
says so of relationship paths. Ingesting them would add people and edges the GEDCOMs do
not have.

**Not urgent, per her:** *"while it is important, it is not worth messing with stuff right
now."* Hence the tail of the queue.

## THE LAST ITEM — fix the pipeline so dates carry their proper qualifiers

**Emma, 2026-08-29:** *"Yes, we very much need to have those qualifiers, and I don't know why it
is that you don't. That was almost a prerequisite for putting any Geni information on
Wikidata."*

**Nothing in the pipeline emits one.** `reports/wikidata-garborg-day.qs` contains no `P1480`, no
`P1319` and no `P1326` — every `ABT`, `BEF`, `AFT` and `BET x AND y` in the corpus is being
flattened to a bare year at precision 9, which asserts a date Geni does not claim.
`reports/wikidata-spine-completion.qs` does the same, and did it deliberately to match the
pipeline; that was the wrong call and it is part of this fix.

The mapping is already in `CLAUDE.md` § *Date qualifiers* and needs no re-deriving:

| GEDCOM | Wikidata |
| --- | --- |
| `ABT` / `EST` / `CAL` | `P1480` *sourcing circumstances* = `Q5727902` *circa* |
| `BEF` | `P1326` *latest date* |
| `AFT` | `P1319` *earliest date* |
| `BET x AND y` | `P1319` *earliest date* + `P1326` *latest date* |

`reports/derived-facts.csv` already carries the modifier — `birth_date_modifier`,
`death_date_modifier`, values `about` / `before` / `after` — so the parse is done and only the
emission is missing. `genimerge.dates` is the authority on the grammar; do not re-parse the raw
string.

## THE LAST ITEM — the chains should be a SYSTEM, not four files that happen to exist

**Emma, 2026-08-29**, and she is explicit this is not a question about how full the chains are:
*"Oh my God, I'm not asking if it's close to filling in. I'm asking: I thought that we have a
system... I thought this existed, and it should exist if it doesn't exist. This is a problem, and
you should make it exist."* Filed at the tail by her own instruction — *"put all this chain stuff
at the end of the queue, and then move on... it's not worth messing with the workflow and making
it so that you get long-term distracted and don't do the queue work."*

**What exists today, and in which direction.** Measured 2026-08-29; pairs bonded is from
`reports/spine-bonds.tsv`.

| file | runs | steps | pairs bonded | in `SPINE_PATHS`? |
| --- | --- | ---: | ---: | --- |
| `paths/charlemagne-to-arne-garborg.tsv` | Arne → Charlemagne | 34 | 29 of 33 | yes |
| `paths/bergitte-to-emma.tsv` | Emma → Bergitte, walked reversed | 16 | 3 of 15 | yes |
| `paths/bureus-to-emma.tsv` | Bureus → Emma | 16 | 3 of 15 | yes |
| `paths/arne-to-bureus.tsv` | Arne → Johannes Jacobi Bureus | 19 | 5 of 18 | no |
| `paths/arne-to-bureus-q633094.tsv` | Arne → **Johannes Tomasson** | 21 | 4 of 20 | no |
| `paths/emma-to-bureus.tsv` | Emma → Bureus | 21 | 4 of 20 | no |

**The directions she named, which the files do not currently match:**

- **Arne ↔ Bureus goes BOTH ways.** Two files exist and neither is in `SPINE_PATHS`, so neither
  advances.
- **Emma ↔ Bureus goes from Bureus to her ONLY.** `paths/emma-to-bureus.tsv` runs the other way
  and is a duplicate of the same relationship; decide whether it is deleted or kept as evidence.
- **Bergitte → Emma goes that way only.** Already true, via `SPINE_REVERSED`.

**The "weird other version" is identified.** She said *"I do not know what that weird other
version is"* of `arne-to-bureus-q633094.tsv`. It is named for `Q633094` — Johannes Bureus — but
its last step is **Johannes Tomasson**, a different person. Both files were generated by
`scripts/path-between.py` breadth-first over `reports/derived-family.csv`. Work out which endpoint
was actually asked for and either rename the file or regenerate it.

**The new chain she wants, and the part that is NOT settled.** *"a various deferral domain that
also generates, starting at various and moving towards [garbled] and only... I don't think you
need to do it in Chrome, because I think you can use local information. You probably only go
towards certain specific modern people and not into mediaeval times."*

So: a chain generated **downward from Bureus toward modern descendants**, from local data, never
into the medieval end. `scripts/path-between.py` is the generator and needs no browser — every
person on these paths is already in the corpus. **Two phrases in that sentence did not transcribe
and must not be guessed at**: the destination (*"towards strongly and only"*) and what a *"deferral
domain"* is. Ask before building, per § *If you are not sure what she wants, ASK*.

**Once the set is settled, the ones that should advance go in `SPINE_PATHS`**, with any that are
stored the wrong way round listed in `SPINE_REVERSED` — that is the whole mechanism, and it is why
`bergitte-to-emma` had walked outward from her for weeks without moving.

## THE LAST ITEM — rebuild the synoptic tree, which is how the QID-link GEDCOM gets tested

**Emma, 2026-08-29:** *"don't test it now but make the last queue item rebuilding the synoptic
tree to test this thing so that we can quickly move onto other work."*

`exports/post-merge/wikidata-qid-links.ged` is **three individuals, three `NOTE` links, 358
bytes** — Wakatakehiko `Q11596350`, Harima no Inabi no Ōiratsume `Q11078587`, Mononobe no Ikofutsu
`Q24890131`. It has never been through a merge.

**Re-merge and confirm three things:**

- **The links arrive** — each of the three ends up holding
  `1 NOTE https://www.wikidata.org/wiki/Q…` beside their existing About Me, because `NOTE` is in
  `merge.ALWAYS_REPEATABLE` and repeatable-with-a-value matching keeps both.
- **Nobody is invented.** All three xrefs were checked against `reports/derived-labels.csv`, so the
  individual count must not rise. An `INDI` with an unseen xref is a *new person*.
- **It is idempotent** — regenerating and re-merging changes nothing.

`_post_merge_last` puts `exports/post-merge/` at the end of merge order, so this applies last.

**The merge is 837 seconds and 16.8 GB** — background it, per § *A ten-minute ceiling is not a
wall*. Keep the pre-merge tree.

**Widening this beyond the three is her call and is one constant.** The machinery handles any
number; the first version emitted 83,988 people off `reports/synoptic-correspondence.tsv` and that
was a generalisation she had not asked for.

## THE TAIL — two she moved here herself, 2026-08-29

*"Just add both of these to the end of the queue."* Both were cron jobs she scheduled by clock
time on 2026-08-27; every cron died in the 08-28 crash, so neither will fire on its own. Her words
are kept because these are unstarted.

- **`Sara /NN/`** — the case she set aside at the time: *"Ignore the fucking NN thing. 'Sara /NN/'
  can wait until a cron job at 9pm fires to analyze this problem then."* The name is
  `Sara` with `NN` in the surname slot, which is the inverse of the shape
  `_carries_marker` was fixed for — there the marker was the *given* token and the surname real.

- **Why a redacted profile came out labelled `Garborg`** — *"do a cron job at 10pm to analyze why
  https://www.geni.com/people/private/6000000021223635839 was added as "Garborg" instead of the
  current labels on wikidata that I manually added https://www.wikidata.org/wiki/Q141199845"*.
  Note this is a `<private>` profile, so § *The NN/Private label algorithm* governs what it should
  have been, and she had already hand-corrected the item — so the question is also why our label
  overrode hers.


## Did the Swentepolk export ever actually happen? Review it, and re-run if not

**Emma, 2026-08-29:** *"have, at the end of the queue, an item to review whether this thing
actually happened and was implemented, and to run the export again and stuff like that if it
didn't."*

She is right to want this written down rather than trusted to a cron: **cron text lives only in
memory and dies with the session**, which is exactly how every job was lost in the 08-28 crash and
why nothing ran between 00:03 and 06:00 on 08-29.

**The state at the time this was written:** submitted, `task_id 6000000227491938853`, seed
`6000000227491932881`, `Forest`/5000. Sat at about **8%** for hours, which is why she called it
blocked. Cron `9499a8c8` checks it hourly at `:30`.

**What "it happened" means, concretely — check all four:**

- A `.ged` exists under `exports/obotrite/` and is **committed**, with its zip gitignored on its own
  explicit line.
- **`grep '@I6000000007716541890@'`** finds Swentepolk in it. That is the success condition; a file
  that arrived without him did not do its job.
- `reports/mass-export-log.tsv` has an outcome line, not just the `submitted` row.
- `bure-coverage.py`-style check: his father `6000000007718311626` too, if the Forest reached him.

**If it did not happen**, resubmit from the same seed — it still exists and is hers, so no new
placeholder is needed. If Geni has lost the task, submit fresh from
`https://www.geni.com/gedcom/export/6000000227491932881`, `Forest`, size 5000, and record the new
`task_id`.

**Do not silently drop it.** `Q4411612` is identified and its `.qs` is written, but neither he nor
his father is in the tree, so the correspondence exists only in a file until an export lands.

## The algorithm review ended before six of its steps — what was never walked through

**Closed 2026-08-29 at her instruction** — *"consider the review over"* — after pinning the queue
since 2026-08-27. This records the unfinished half so closing it is not the same as pretending it
finished.

**She walked through, and ruled on:** step 1 the ledger refresh, 2 `have`, 4 the provisional ring,
5 the 1880 cutoff, 6 the subgraph, 7 `compose`, 9 the duplicate guard, 11 the fill-in pass.

**Never reached: steps 3 (`linked`), 8, 10, 12, 13, 14.** Nobody has told me what is wrong with
them, so nothing in them has her sign-off — treat any behaviour there as unreviewed rather than
approved.

**Her rulings on the covered steps, which stand:**

- The 34 unlabelled ledger rows dropped and regenerated from Wikidata.
- Her own `entity_resolution.md` entry to go **by her hand, not mine** — since overtaken: she had
  the whole file deleted on 2026-08-29, which removed her `Q232803` from `have` anyway.
- Bureätten people eligible for **both** fill-in and seeding.
- `MODERN_CUTOFF = 1880` *"totally undesired"* — removed, with nothing in its place.
- Steps 4–5 are dead code under `--compose`.
- Her duplicate items are **deliberate**: create the duplicates, then merge them, because that
  leaves the trail Wikidata's review machinery expects.
- The Wikidata link goes into bios **during the synoptic tree build**; Geni is never edited for it.

## How many Geni labels actually need changing? Count them

**Emma, 2026-08-29:** *"Put at the end of the queue: a specific thing, doing an analysis on the
amount of people whose Geni labels are made to be changed and stuff like that."*

**The number she wants first:** *"I don't know the degree of people that we have that only have CJK
labels, because that is an important thing for analysing with this."* So: how many people in the
corpus carry a name **only** in Han, kana or hangul, with no Latin form anywhere on the record?
Those are the ones who would need an English name written onto Geni.

`reports/derived-labels.csv` has `cjk_names`, `other_script_names` and `further_latin_names`, and
`display-names.csv` has the raw fields and a `scripts` column, so this is offline and cheap.

**Report the count before proposing any edit.** The campaign's value is whatever our pipeline puts
in `mul`, so the second number worth having is how many of those people our pipeline can currently
produce a `mul` for at all — a person we cannot label is not a person we can fix.

## "Synoptic tree" means two different things — resolve it usage by usage

**Emma, 2026-08-29, asked what it concretely is:** *"it is consistently conflated between the union
of all the geni gedcoms and the union of that tree with all data sources."*

So the term carries two meanings and the repo does not distinguish them:

- **the Geni union** — every `.ged` under `exports/` merged, i.e. `out/merged.ged`
- **the full union** — that tree joined to every other source, Wikidata above all

**Her instruction: `AskUserQuestion` on every specific usage** — *"Add to the end of the queue a
task to run AskUserQuestion on every specific usage as the full version geni union idk or custom"*.
So go through every place the phrase appears in `CLAUDE.md`, `queue.md`, `docs/` and the scripts,
and put each one to her as *Geni union / full union / something else*, rather than picking a
definition and applying it everywhere.

**She also considers the immediate question moot:** *"I'm pretty sure the gedcom we added as a
workaround makes this question obsolete"* — `exports/post-merge/wikidata-qid-links.ged` puts the
Wikidata links into the corpus, so they arrive in the merge either way and nothing waits on the
definition being settled.

## Census: how the four labels derive from each other, and how many people lack each

**Emma, 2026-08-29, on where each label comes from:** *"Mul is transcribed lol and Japanese and
Chinese are the characters and korean is a rendering derived from the Chinese ir Japanese and
English is from the mul lol, add a count cebsus thing to the end of the queue."*

The chain she describes:

- **`mul`** — transcribed; the base everything else derives from
- **`ja` / `zh`** — the characters themselves
- **`ko`** — a rendering derived from the Chinese or Japanese, not from `mul` directly
- **`en`** — from `mul`

**What to count**, one row per person per language as `CLAUDE.md` § *"Analyse this" means build a
CSV* requires: who has each label today, who could have one under this chain, and who could not and
why. The number that matters most is the people whose Geni name is CJK-only, since the emitter
currently gates `en` on a Latin character being present and so gives them none.

**No `ko` is emitted anywhere today.** Worth stating plainly rather than discovering: this is the
first mention of Korean in the label model, so the census should say how many people it would apply
to before anything emits it.

## CJK label conversion — fill in Korean and `P1814` *name in kana*, with research

**Emma, 2026-08-29:** *"do a cjk label conversion thing with research to fill in the korean and name
in kana properties using among other things stuff from the shintowiki-scripts repo"*.

**Two things are missing, and they are different in kind.**

- **`P1814` *name in kana*** — a real Wikidata property, confirmed offline in
  `reports/wikidata-labels.tsv`. **Nothing in this repo emits it.** The two scripts that mention a
  property in that family, `build-garborg-name-items.py` and `build-orderlife-identifiers.py`,
  reference it once each and neither writes one.
- **Korean** — the `ko` **label**, not a property. Her chain, 2026-08-29: *"korean is a rendering
  derived from the Chinese ir Japanese"*, so it comes off `ja`/`zh` rather than off `mul`. Nothing
  emits `ko` today either.

**"With research" is the load-bearing half.** Kana for a Han name is not derivable by rule — the
same characters take different readings per person, which is why `P1814` exists as a property at
all rather than being computed. This is the case `CLAUDE.md` § *The one hard problem: which culture
a CJK name is* already names. So the work is: find the readings, do not generate them.

**`shintowiki-scripts` is a SEPARATE repo and the coupling has burned this repo once.** `CLAUDE.md`
§ *WIKIDATA EDITING STARTS 2026-09-01* records that a previous session invented a shared lockout
between the two and it *"failed closed"*, blocking edits this repo was entitled to make. Emma:
*"Shintowiki scripts and this one are not the same and not really coordinated"* and *"I think you
hallucinated a coordination between them."*

**So: take material from it, do not couple to it.** Copy or vendor what is useful — reading tables,
transliteration data, whatever it holds — into this repo, and add no runtime dependency, no shared
state file, and no network call to it. It is not checked out beside `geni`, so the first step is
asking her where it is.

## Resolve names against the STORE'S name items, not against the ones our people already use

`measure-name-resolution.py` asks *which name items do people in our store already point at*
(132,569) and its answer is used as *which name items exist*. The store actually holds
**823,907** name items — `out/wikidata/name-items-in-store.tsv.gz`,
`scripts/extract-name-items.py`.

**5,212 of the 14,351 tokens `reports/name-item-plan.csv` would create already have an item of
the right kind on our own disk** — 36.3%, including `Thomas`, `Hans`, `Sarah`, `Henry`, `陳`,
`藤原`. Every one is a duplicate waiting to be made, and `Tunheim` is the one that already was.

Point the resolver at the new index, keeping `CLAUDE.md` § *One name item per USAGE* (kind is
never collapsed) and the diacritic rule (case folds, nothing else). Then re-run the plan and
report how `create` / `link` / ambiguous move.

## The NN path drops the birth-name alias the named path emits

Found while answering the `Q141205924` label question. The named branch of
`build-garborg-day.py` emits `Lmul <married>` **and** `Amul <birth>`; the redacted/NN branch
sets `birth = ""` and emits the `mul` alone. So a married NN woman keeps only one of her two
recorded surnames. `NN Gjøa` would be her alias under the current rule and is not emitted.

Analysis first: count the NN people carrying both a `SURN` and a different `_MARNM`.

## ABSOLUTE PREREQUISITE — no individual is created without their CJK labels

**Emma, 2026-08-29:** *"There should be an absolute prerequisite that nothing is created until you
add in the CJK labels... It should be an absolute prerequisite for the creation of any individual:
that we have their CJK labels."*

**Apply this at the END of the queue, not now** — her explicit instruction: *"Apply it at the end of
the queue because I don't want to interrupt whatever pipeline we're running right now."*

**The rule:** a `CREATE` is refused unless that person has `ja` and `zh`. Today the builder emits
them when every token resolves and creates the person anyway when they do not; under this rule the
person is carried forward instead. It currently bites rarely — 37 of 38 creations in the last batch
already carry both — but rarely is not never, and she wants it absolute rather than usual.

**The order she wants, and the reason:** *"All of the items that I have created, especially the ones
that I have edited, need the CJK stuff first on them."* So the shared 15-a-batch cap stays as built,
clan block last — she confirmed it: *"keep the shared 15 with the clan left. That is the best thing
to do because the most important thing is to fix up the CJK labels on our existing items first."*
Existing people drain first, then the 177 clan people. *"The clan people also extend the range of
the quick statement stuff by a lot, so this is worth leaving at the end."*

## Systematic review for legacy code — find it and delete it

**Emma, 2026-08-29, and it is the last item by her instruction:** *"That is the last item of the
queue to do a systematic review to find this kind of legacy code thing."* `CLAUDE.md` § *LEGACY CODE
IS DELETED* is the rule; this is the sweep.

**Three scripts are orphaned as of `12f3134a` and are the obvious start** — all three read
`entity_resolution.md`, which no longer exists:

- `scripts/build-entity-resolution-batch.py` — its entire purpose was that file
- `scripts/build-charlemagne-route.py`
- `scripts/build-edit-objects.py`

**218 scripts are in `scripts/`.** The test is *does the pipeline read this*, not *might it be
useful*. A defensible sweep: every script not referenced by another script, by a test, by
`CLAUDE.md`, or by a queue item, and whose outputs nothing reads. Report the list before deleting
in bulk — but do not preserve something merely because deleting feels irreversible, since git has
it and a stale file in the tree is the thing that actually costs.

## Always last — pinned to the very end of the file

**Bullets, not letters.** These were `A.` and `B.`; `CLAUDE.md` § *Queue items are BULLET POINTS*
covers lettering for the same reason it covers numbering, and she said so again on 2026-08-29.

- **Ensure the three crons are running** — work-loop `3 * * * *`, auto-flush `15 * * * *`,
  status-report `42 * * * *`. They are **session-only**: they die when the session ends and must be
  recreated at the start of the next one. This is not theoretical — every cron died in the
  2026-08-28 crash and none was recreated, which is why nothing ran between 00:03 and 06:00 on
  2026-08-29. Confirmed live this session as `82923e5b`, `0d208cfd`, `31df9ff8`.

- **The three crons, as durable queue items.** Her instruction, 2026-08-27: *"For all of the cron
  jobs that I set up in the session. They are good and continue on with them, but also add them
  into the queue as actual items with he specification they are the cron jobs so they cget crossed
  off if he cron job finishes, but are a bit more stable."* Cron text lives only in memory, so the
  queue is the durable copy:

  - **Work-loop, hourly at :03** — sync, take the top actionable item, do it, commit with a
    `devlog.md` entry, push, report one line. Rails: never loosen a test, never claim verified
    without running it, no live Wikidata beyond the ledger refresh and `full_entities` before a
    correction, never generalise a named instruction into a mechanism, never invent a `.qs` she did
    not ask for.
  - **Auto-flush, hourly at :15** — commit and push anything pending, or report nothing pending.
    Never an empty commit.
  - **Status-report, hourly at :42** — reporting only. What advanced, queue state, whether the
    rails held, blockers each under exactly one not-done tag, and real test numbers from a run.

- **Run the status-report action once more** — an end-of-session summary of everything that
  happened this session.

### `P2600` constraint violations report — analysis AT THAT TIME, no pre-analysis

<https://www.wikidata.org/wiki/Wikidata:Database_reports/Constraint_violations/P2600>

Emma, 2026-08-29: *"we are gonna do analysis at that time (no pre-analysis) of how to
potentially elp wih wikidata genealogy with this stuff, it overlaps with some of our
entity resolution stuff do no think on it"*

So: nothing is to be investigated, measured or fetched about this before the item is
reached. The analysis is of how the constraint-violations report could help Wikidata
genealogy, and it overlaps the entity-resolution work.

### The clan labels may be much worse than we think — `Q45449130`

<https://www.wikidata.org/wiki/Q45449130>

Emma, 2026-08-29: *"I think that our clan things are much worse than you think, which is why I
never acually ran them adn I think I am seein at least some evidence."*

An analysis. Nothing was investigated when this was written.

## ⛔ `exports/post-merge/` — MOVED TO THE TAIL, 2026-08-29, her call

**Emma, 2026-08-29**, shown that 408 of the 412 falsifiable drops are real deletions:
*"For now leave these things and still run them, but put them at the end of the queue, I lean on
the idea of saving them but do not have bandwidth to process this now."*

So: **leave them in the tree, keep running the measurement, decide later.** She leans toward
saving the 408 rather than dropping them. Nothing is applied and no override is written.

`scripts/grade-post-merge-drops.py` → `reports/post-merge-falsifiable.tsv` is the standing
measurement — 408 `link-gone`, 2 still linked, 2 with no shared family, over 159 parents,
159 children and 90 spouses.

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

**Why it matters right now.** `out/merged.ged` is **0 bytes** (two rebuilds were killed) and every
derived CSV is from **24 Aug 18:28**, while the Bure campaign landed **28 Aug**. So:

- **Israel Hwasser** `Q5818420` is in `exports/bure-campaign/export-Forest-6000000227475095829.ged`
  with a full record and has **0 rows** in `derived-family.csv`. The whole campaign is invisible to
  the batch generator.
- `Q141219067` carries `P1810 "Private"` where Geni shows `<private> Dokken`, because three older
  exports say `Private` and only the 28 Aug one says `<private> /Dokken/`.
- The compliance audit's 15 relationship-less roster people cannot be acted on, because their
  relatives are not in the derived tree.

**Run it alone.** Step 1 peaks near 17 GB and has been killed twice when something else was running.
