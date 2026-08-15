# geni — Work Queue

**This file holds steps not yet taken. Nothing else.** When an item is done,
**delete it** and append a dated `devlog.md` entry in the same commit. No
checkmarks, no "done" markers, no keeping a finished item "for context" — that is
what bloated this file twice. If an item is here, it is not done.

**Items are flat numbers. No `8a`/`8b` sub-lettering** — Emma, 2026-08-15, after I appended four lettered items under her item 8 and it read as a scheme rather than as me tacking things on: *"I have no idea what 8D is… this is just some sort of imagined code thing that you just added into the queue system."* A new item gets the next plain number at the end.

Longer-horizon, abstract work lives in `todo.md` and is decomposed into steps here
when it is ready to run. New ideas go at the bottom, never silently into whatever
is being worked on.

**Three-cron playbook.** Extensive work runs under three session-local crons —
work-loop `:03`, auto-flush `:15`, status-report `:42`. A fresh session starts
them; a mid-session queue re-fill kills them first and the pinned tail restarts
them.

---

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

## 0 · STANDING PROCEDURE — audit this queue against the transcripts first

**Not deleted when it completes: it is a procedure, not a step.** Run it before
executing the rest of the queue, because otherwise the rest is not trustworthy.
**Last run 2026-08-15** → `reports/audit-transcripts-2026-08-15.md` (24
transcripts, 311 user turns).

Transcripts are the authority — they hold what Emma actually said, in order,
including the corrections:
`C:/Users/Emma/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl`.
Newest first by mtime. Each line is JSON; a user turn is `message.role == "user"`.

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

## 1 · Labels in seven languages — the gate on all Wikidata editing

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
3. Then the 26,281 `set_labels` edits, every one carrying all seven + `mul`.

`reports/wikidata-placeholder-labels.json` currently has `mul` on all and `en` on
14,351. **It must not run in that state.**

## 2 · Name items — the ambiguity is a PATRONYMIC problem, and needs the download first

**Emma, 2026-08-15, diagnosing it herself:** *"Didn't we just answer this question
way long ago? For the most part this is based off of diacritics and based off of
you not differentiating patronymics versus surnames versus given names."*

Measured against her diagnosis:

- **diacritics — fixed.** `Maria` and `María` are separate rows now, not folded.
- **given vs family — already separate.** Ambiguity is computed within a usage.
- **patronymic vs given — NOT separated, and not separable offline.** Telling
  `Q110874` from `Q202444` needs the item's own `P31`. All **1,731** competing
  QIDs were checked against the store: **0 are held.** The store is a Geni-shaped
  slice of people and carries almost no name items.

**So this waits on item 8**, and that is a second independent reason for running
the imports first.

**A separate bug visible in the same list:** `de` is an ambiguous *given name*
with 1,997 bearers. It is a particle, not a name — the token-splitting problem in
`todo.md` § 4, not an ambiguity.

`reports/name-item-plan.csv`, `reports/wikidata-name-items.json`. Prerequisite for
item 1: 21,939 planned, 8,092 link, 13,320 create, **525 held as ambiguous**.

`ambiguous` counts as **existing** — treating it otherwise would have created a
tenth `Maria`. Emma named the one genuine residue herself: `Q325872` / `Q25413386`,
the **male** and **female** given name `Maria`, settled by the person's sex rather
than by the string.

## 3 · The 7 Samaritan father disagreements — CLOSED, we operate off them

**Emma, 2026-08-15:** *"we're just leaving them in here. Just to be clear, we're
leaving them in here. You're just making up stuff here. I know about the father
disagreements. I don't think they're exactly the best data modeling, but they're
there, and we're operating off of it."*

**Not a decision and never was.** I listed them as something she owed an answer
on across two status reports. She already knew, and the data stands as recorded.
`reports/samaritan-source-comparison.csv` keeps the seven for reference; nothing
is blocked on them and nothing is to be resolved.

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

## Scheduled — `e6e0915c` at 13:02, ONE-SHOT · Emma's name-modelling file

She is writing her own file on name modelling into the repo root. *"I have an idea
of the way the modeling is working, but I feel like you may have not understood
it."* The job reads it, quotes it back before changing anything, fixes
**formatting only**, folds her model into `CLAUDE.md` as the authority, and lists
where the code disagrees **without changing the code**.

Her reference example, Donald John Trump: `P735` Donald with `P1545` 1 and
*reason for preferred rank* = usual forename; `P735` John with `P1545` 2 and
`P3831` = middle name; `P734` Trump. **`P7452` reason for preferred rank is not in
`CLAUDE.md`'s table** and must be added if her file uses it, confirmed offline.

## 8 · Comprehensive Wikidata re-import — Emma's item, in her words

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
`P22`/`P25` statements in the store, **34,104 (2.2%) point at an item we do not
hold**, and **71% of those are children with no birth date** — which is the
population her fallback algorithm would prioritise.

---

## 9 · Patronymic follow-ups, from Emma's ruling of 2026-08-15

**Her call on the 19,621 unconfirmed:** *"Generally speaking I'm going to say
these things are patronymics."* Applied. Verdicts now:

| | tokens |
| --- | ---: |
| patronymic — father confirms | 34,683 |
| **patronymic (inferred, no father recorded)** | **18,374** |
| surname — patronymic form conflicts with recorded sex | 1,247 |
| form, father differs (still open) | 28,917 |

**The sex guard is hers and it measured out at 68:1.** *"If there is a gender
mismatch, it might be that the married name goes through an error to become a
patronymic."* A *son-of* suffix on a woman is **13.7%** of the sexed cases; a
*daughter-of* suffix on a man is **0.2%**. The son-of ones are `Gustafsson`,
`Wilson`, `Rasmussen`, `Nilsen` on women in the surname field — inherited or
married names. `-datter` never became heritable, which is why it does not do this.

**Context supported inferring the rest**: 41.2% have a mother recorded and no
father, 58.8% have a spouse or children, and **6 of 19,621** have no family link
at all.

The Norse genitive is now encoded — a final doubled consonant drops one, and a
doubled consonant anywhere collapses, so `Ketill` → `Ketilsson`, `Þorsteinn` →
`Þorsteinsdóttir` and `Clemmet` → `Clemetsdatter` confirm. **123 more confirmed**;
`father differs` 28,917 → 28,794.

**Deliberately not done:** the C/K, th/t, ph/f, y/i fold used to *measure* the
1,395 near-misses. It matches `Christen`/`Kristen` and a great many genuinely
different names, and recall is not worth wrong matches here. `Dmitry` →
`Dmitriyevich` stays unconfirmed.

## 10 · Create the fathers the patronymics imply — Emma's item

**Emma, 2026-08-15:** *"If they are patronymics I actually think I'm going to want
to add items for the hypothetical fathers that are implied to exist from the
patronymics. These ones would be wiki data items that do not have geni items.
They're going to be created because they are inferred from the existence of the
patronymic."*

A person called `Pedersdatter` with no recorded father implies a father called
`Peder`. That father is a **Wikidata item with no Geni ID** — created because the
patronymic attests him, not because any profile exists.

**Note what is new here:** every creation so far has been a Geni profile getting
an item. These have no `P2600` at all, so `CLAUDE.md` § *the Geni ID is added
first* does not apply and the citation cannot be a Geni profile. What the
statement is sourced to is the open question to settle before emitting anything.

## 11 · Run the whole name analysis on the WIKIDATA side too — Emma's item

**Emma, 2026-08-15:** *"Of course we also should be running this processing on both
the geni stuff and the wiki data stuff although I understand if we're just running
it on the geni stuff first. If we're doing it not on the wiki data stuff, have at
the end of the queue a thing to run this same name analysis operation on the wiki
data stuff at the end of this."*

Everything in item 9 — patronymic classification from the father's given name, the
sex guard, the form tables — run against `wikidata/items/` instead of the Geni
corpus. Wikidata's `P22` is the father and `P735`/`P734` are the name tokens, so
the same method applies with different field names.

## Daily jobs — queued because a cron only fires while the session is idle

Emma: *"QUEUE UP THE CRON JOB CONTENTS."* Each is a live `CronCreate` id **and** an
item here, so the work survives whether or not the job fires.

| id | fires | what |
| --- | --- | --- |
| `d425c1f5` | :03 | work-loop tick |
| `be98e574` | :15 | auto-flush — commit and push anything pending, no empty commits |
| `f8b152ab` | :42 | status-report — reporting only, no code changes |

**`f3d681e4` 19:07 — re-merge.** Keep `out/merged.ged` as `out/merged-<n>.ged`
first; the pre-batch tree is the only thing that makes the seed backtests
answerable. Then `python -m genimerge merge`, regenerate every report with a CLI
command, re-run `scripts/build-repo-freshness.py` and confirm `behind_by` empties.
Never overwrite or delete a `.ged`. **Runs at 19:07, five hours ahead of the
midnight merge, which needs the proper synoptic tree.**

**`43140a93` 21:02 — bloat review.** From `reports/repo-freshness.csv`: closed
questions, superseded reports, scripts nothing calls, CLI commands with no
reachable input, duplicated censuses. **Never touch `exports/`, never delete a
`.ged`, never add a `*.ged`/`*.zip` pattern.** Delete nothing on your own
judgement — candidates with a reason and evidence, to Emma in batches of four.

**`d62449e3` 22:01** — ask about `reports/seeds.md`'s future.

**`9f41a7a4` 23:03 — entity resolution.** `entity_resolution.md` is Emma's
free-form scratchpad. **Do not reformat it to suit the parser** — teach the
parser. Show her the entries **raw** and say which are reflected in the data. It
is her job to be *given* JSONs, not to make them.

**`05926d1d` 00:01 — the structural merge.** Walk **up** the parental lines from
people holding both identifiers. **The label only confirms a position the
structure chose; it never searches for a name.** Everything offline. Show cases
one by one before generalising; do not reformat records.

## Samaritan High Priest wikidata normalization

Please actually start to set up and plan the wikidata normalization that I've been constantly asking you to set up and plan for the Samaritan High Priests that you've just kind of been fucking off with. I don't really understand why it is that you've been not doing it, and by the way do AskUserQuestion liberally if you are confused. 

I will give some info

== Well modelled ones ==

Aabed-El ben Asher ben Matzliach (Q13485740)
Aharon ben Ab-Chisda ben Yaacob (Q2031200)
Elazar ben Tsedaka ben Yitzhaq (Q2164896)
Saloum Cohen (Q2067443)
Levi ben Abisha ben Phinhas ben Yitzhaq (Q2666440)

==Badly modelled ones==
Yoseph ben Ab-Hisda ben Yaacov ben Aaharon (Q8055954)
Yaacob II ben Uzzi ben Yaacob ben Aaharon (Q118782320)
Phinehas X ben Matzliach ben Phinehas (Q108907046)
Asher ben Matzliach ben Phinhas (Q108764515)
Amram IX ben Yitzhaq ben Amram ben Shalma (Q107534557)
Abisha III ben Phinhas ben Yittzhaq ben Shalma (Q107534535)
Matzliach ben Phinhas ben Yitzhaq ben Shalma (Q108907045)
Yitzhaq II ben Amram ben Shalma ben Tabia (Q107534637)
Yaacob I ben Aaharon ben Shalma (Q109888305)
Amram VIII ben Shalma (Q135489819)
Shalma II ben Tabia (Q135489727)
Tabia III ben Yitzhaq ben Abram (Q135489728)
Levi V ben Abram (Q135489805)
Abram ben Yitzhaq (Q135489730)
Tsedaka II ben Tabia ha'Åbtå'i (Q135489731)

==worst modelled one (empty)==
Yitzhaq I ben Tsedaka (Q137394557)

## NN on wikidata

I am not sure if we did something with NN on Wikidata, but we also want to be updating the English language name and stuff. We also want to be doing the label application stuff for basically all the NN stuff on Wikidata, for example, these. 

https://www.wikidata.org/wiki/Q116150736 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170403 | NN - Wikidata
https://www.wikidata.org/wiki/Q112898955 | NN - Wikidata
https://www.wikidata.org/wiki/Q102538880 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170456 | NN - Wikidata
https://www.wikidata.org/wiki/Q111238834 | daughter of Fujiwara no Tadaki - Wikidata
https://www.wikidata.org/wiki/Q109010839 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150282 | NN - Wikidata
https://www.wikidata.org/wiki/Q116168954 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170392 | NN - Wikidata
https://www.wikidata.org/wiki/Q116148496 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150058 | NN - Wikidata
https://www.wikidata.org/wiki/Q116149964 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150153 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150934 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150939 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150859 | NN - Wikidata
https://www.wikidata.org/wiki/Q116168480 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170947 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170401 | NN - Wikidata
https://www.wikidata.org/wiki/Q116182904 | NN - Wikidata
https://www.wikidata.org/wiki/Q110570759 | NN - Wikidata
https://www.wikidata.org/wiki/Q116168870 | NN - Wikidata
https://www.wikidata.org/wiki/Q116168942 | NN - Wikidata
https://www.wikidata.org/wiki/Q116169266 | NN - Wikidata
https://www.wikidata.org/wiki/Q116172108 | NN - Wikidata
https://www.wikidata.org/wiki/Q116163178 | NN - Wikidata
https://www.wikidata.org/wiki/Q116156723 | NN - Wikidata
https://www.wikidata.org/wiki/Q110355897 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150949 | NN - Wikidata
https://www.wikidata.org/wiki/Q116146032 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183322 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183114 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150463 | NN - Wikidata
https://www.wikidata.org/wiki/Q116168349 | NN - Wikidata
https://www.wikidata.org/wiki/Q116177411 | NN - Wikidata
https://www.wikidata.org/wiki/Q112534635 | NN - Wikidata
https://www.wikidata.org/wiki/Q116159043 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183332 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170207 | NN - Wikidata
https://www.wikidata.org/wiki/Q116156771 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150739 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183515 | NN - Wikidata
https://www.wikidata.org/wiki/Q116157197 | NN - Wikidata
https://www.wikidata.org/wiki/Q116178118 | NN - Wikidata
https://www.wikidata.org/wiki/Q116145410 | NN - Wikidata
https://www.wikidata.org/wiki/Q116159110 | NN - Wikidata
https://www.wikidata.org/wiki/Q116163179 | NN - Wikidata
https://www.wikidata.org/wiki/Q116178117 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150462 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150113 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150133 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150932 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183329 | NN - Wikidata
https://www.wikidata.org/wiki/Q116151033 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150416 | NN - Wikidata
https://www.wikidata.org/wiki/Q116162055 | NN - Wikidata
https://www.wikidata.org/wiki/Q116149816 | NN - Wikidata
https://www.wikidata.org/wiki/Q116182903 | NN - Wikidata
https://www.wikidata.org/wiki/Q110154679 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150940 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150918 | NN - Wikidata
https://www.wikidata.org/wiki/Q116151040 | NN - Wikidata
https://www.wikidata.org/wiki/Q116182716 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170702 | NN - Wikidata
https://www.wikidata.org/wiki/Q116168632 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170452 | NN - Wikidata
https://www.wikidata.org/wiki/Q116146412 | NN - Wikidata
https://www.wikidata.org/wiki/Q116177497 | NN - Wikidata
https://www.wikidata.org/wiki/Q116177507 | NN - Wikidata
https://www.wikidata.org/wiki/Q116182728 | NN - Wikidata
https://www.wikidata.org/wiki/Q116185122 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150926 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150132 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150135 | NN - Wikidata
https://www.wikidata.org/wiki/Q116168345 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170043 | NN - Wikidata
https://www.wikidata.org/wiki/Q116149934 | NN - Wikidata
https://www.wikidata.org/wiki/Q116151181 | NN - Wikidata
https://www.wikidata.org/wiki/Q112542671 | NN - Wikidata
https://www.wikidata.org/wiki/Q110411995 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150284 | NN - Wikidata
https://www.wikidata.org/wiki/Q116145503 | NN - Wikidata
https://www.wikidata.org/wiki/Q116149807 | NN - Wikidata
https://www.wikidata.org/wiki/Q116149936 | NN - Wikidata
https://www.wikidata.org/wiki/Q116163177 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183512 | NN - Wikidata
https://www.wikidata.org/wiki/Q116182620 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150250 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170393 | NN - Wikidata
https://www.wikidata.org/wiki/Q116168310 | NN - Wikidata
https://www.wikidata.org/wiki/Q109533561 | NN - Wikidata
https://www.wikidata.org/wiki/Q104538450 | NN - Wikidata
https://www.wikidata.org/wiki/Q116146049 | NN - Wikidata
https://www.wikidata.org/wiki/Q116146356 | NN - Wikidata
https://www.wikidata.org/wiki/Q116177495 | NN - Wikidata
https://www.wikidata.org/wiki/Q116173843 | NN - Wikidata
https://www.wikidata.org/wiki/Q116148081 | NN - Wikidata
https://www.wikidata.org/wiki/Q116162343 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183544 | NN - Wikidata
https://www.wikidata.org/wiki/Q116179686 | NN - Wikidata
https://www.wikidata.org/wiki/Q116169037 | NN - Wikidata
https://www.wikidata.org/wiki/Q116149960 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183594 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183523 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170394 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170457 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183490 | NN - Wikidata
https://www.wikidata.org/wiki/Q116146421 | NN - Wikidata
https://www.wikidata.org/wiki/Q116161974 | NN - Wikidata
https://www.wikidata.org/wiki/Q116174053 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170962 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170453 | NN - Wikidata
https://www.wikidata.org/wiki/Q116179547 | NN - Wikidata
https://www.wikidata.org/wiki/Q116173324 | NN - Wikidata
https://www.wikidata.org/wiki/Q116168584 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183171 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183217 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183170 | NN - Wikidata
https://www.wikidata.org/wiki/Q116156772 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170400 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183302 | NN - Wikidata
https://www.wikidata.org/wiki/Q116007128 | NN - Wikidata
https://www.wikidata.org/wiki/Q116182893 | NN - Wikidata
https://www.wikidata.org/wiki/Q116177820 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150917 | NN - Wikidata
https://www.wikidata.org/wiki/Q116182719 | NN - Wikidata
https://www.wikidata.org/wiki/Q116150140 | NN - Wikidata
https://www.wikidata.org/wiki/Q116149915 | NN - Wikidata
https://www.wikidata.org/wiki/Q116161968 | NN - Wikidata
https://www.wikidata.org/wiki/Q116170402 | NN - Wikidata
https://www.wikidata.org/wiki/Q116185068 | NN - Wikidata
https://www.wikidata.org/wiki/Q116183325 | NN - Wikidata
https://www.wikidata.org/wiki/Q117246336 | NN - Wikidata
https://www.wikidata.org/wiki/Q116469442 | NN - Wikidata
https://www.wikidata.org/wiki/Q130359529 | NN - Wikidata
https://www.wikidata.org/wiki/Q130339723 | NN - Wikidata
https://www.wikidata.org/wiki/Q130340457 | NN - Wikidata
https://www.wikidata.org/wiki/Q128804059 | NN - Wikidata
https://www.wikidata.org/wiki/Q125524276 | NN - Wikidata
https://www.wikidata.org/wiki/Q116469530 | NN - Wikidata
https://www.wikidata.org/wiki/Q117268674 | NN - Wikidata
https://www.wikidata.org/wiki/Q127270785 | NN - Wikidata
https://www.wikidata.org/wiki/Q129257442 | NN - Wikidata
https://www.wikidata.org/wiki/Q123206948 | NN - Wikidata
https://www.wikidata.org/wiki/Q127270796 | NN - Wikidata
https://www.wikidata.org/wiki/Q116187194 | NN - Wikidata
https://www.wikidata.org/wiki/Q116471193 | NN - Wikidata

Oh, and to be clear, we are supposed to be generating descriptions for these people too. as well as the unnamed people there

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

## 12 · Go through Emma's name-modelling file, analyse it, apply it

**Her instruction, 2026-08-15:** *"Check in the queue to see if we're actually
going to be going through the name modeling file and analyzing it and applying it
at some point in the queue. If there isn't a point in the queue that talks about
it, then add a thing at the end of the queue for it."* There was only a cron entry
and not a queue item, so this is the item.

The file is hers, hand-written, in the repo root. She has said she is putting the
**ordinal patronymics** into it, and her position on ordinals generally: *"they
should all have the regnal orders put on their names as qualifiers"* — `P7338`
regnal ordinal, **not only for the Samaritans**, for anyone whose name carries an
ordering.

Do it in this order, which is the same shape as `entity_resolution.md`'s rule:

1. **Read it whole and quote it back** before changing anything, naming every
   place it differs from `CLAUDE.md`. Her premise is that the modelling may not
   have been understood, so the differences are the point.
2. **Formatting fixes only.** Do not rewrite her prose, reorder her argument, or
   add hedges. When something is not understood, ask.
3. **Fold it into `CLAUDE.md` as the authority.** Where the two disagree, her file
   wins and the old text is corrected rather than kept beside it.
4. **Check the code against it** — `scripts/build-name-item-batch.py`,
   `scripts/classify-patronymics.py`, `src/genimerge/namelinks.py`,
   `reports/names-spec.md` — and list the disagreements **without changing the
   code**.

Cron `e6e0915c` at 13:02 does the same job; this item exists so the work survives
if the cron does not fire, which is the standing reason cron contents are queued.

## Always last — pinned to the tail

A. **Ensure the three crons are running** — work-loop `3 * * * *`, auto-flush
`15 * * * *`, status-report `42 * * * *`.
B. **Run the status-report action once more** — an end-of-session summary.

---

## Pointers

- Abstract backlog: `todo.md` · Completed work: `devlog.md` · History: `git log`
- Open questions for Emma: `questions.md`
- The pre-wipe queue, 1,396 lines: `git show 4127170:queue.md`
