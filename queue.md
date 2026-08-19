## THIS IS THE `name-development` BRANCH — Emma, 2026-08-18

**This checkout is not the one doing the Geni exports.** Emma split the work after the
export session spent a day doing two jobs badly at once:

> *"there was a bit of a conflict with that session going all ADHD with trying to perform
> two tasks at once. It was trying to do a combination of Geni exports that were occurring
> about every — and doing name work — and not being able to do either one."*

- **Directory:** `GitHub/name-development`, a fresh clone. **Branch:**
  `name-development`, off `main`. The original checkout at `GitHub/geni` belongs to the
  export session and is not touched from here.
- **NO exports and NO browser work of any kind.** *"you do not do any browser activity of
  running exports from individuals, because that's the job of the other session."*
- **NO Wikidata runs.** The standing 1 September rule holds; asked directly, Emma:
  *"Yes, of course it doesn't run!"*
- **The export-slowness item below does not apply to this branch.** Her words, asked
  directly: *"In this branch that you are making, it is resolved. There are no exports
  whatsoever. You are doing the name stuff and other things like that that it was getting
  distracted by."*
- **Commit and push to `name-development` constantly. NO pull request** until the export
  branch has finished what it is doing: *"There is a pull request once the other branch is
  done with all the shit it's doing with the Geni exporting."*

**Note for whoever reads this on `main` later:** the branch was cut at `7ad0596` and
`main` moves under it with every export round, so expect the eventual merge to be a
reconciliation, not a fast-forward.

*(`git push` over HTTPS returned HTTP 500 for this repo on 2026-08-18 and the branch ref
had to be created with `gh api ... git/refs` instead. If a push fails that way again, that
is the workaround, not a reason to stop committing.)*

## ⛔ TOP PRIORITY — the export slowness. NOTHING ELSE RUNS — Emma, 2026-08-18

*"figuring out this download stuff is the top priority of this entire thing. It is THE
top priority. You should not be doing any other work."*

**Exactly one thing may interrupt it**, in her words: *"downloading an exported GEDCOM,
then creating a new individual and exporting from there, because that is time-dependent."*
Everything else in this file waits behind this item, including the name work, the label
batches and the marker fixes.

### The measurement, and what it is made of

**The data is the session transcripts**, `~/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl`.
Every tool call and every result carries a UTC timestamp, so they *are* the log of when
each export was requested and when its page was next seen. `scripts/measure-export-build-times.py`
reads them; `reports/export-build-times.{csv,md}` is the output.

Two earlier attempts were worse and should not be revived: timing from **file mtimes**
(`measure-export-throughput.py`) is biased because a late download makes the next build
look short, and matching a page's text to **every** task id in the message attributes one
poll's state to other open tabs.

| day | exports | Geni build ≥ | cycle | latency here | exports/hour |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026-08-17 | 53 | 4.2 min | 8.0 min | 3.8 min | 7.5 |
| 2026-08-18 | 8 | 3.5 min | 12.3 min | 8.8 min | 4.9 |

**Geni is not slower. It is slightly faster.** Build times fell 4.2 → 3.5 min median and
the worst case fell 9.8 → 6.1 min. Size does not explain it either: `r = 0.13` against
megabytes, and today's files are *smaller*.

**The lost throughput is latency on this side** — 3.8 → 8.8 min per cycle, from running
multi-gigabyte scans and batch regenerations between polls. That is the whole difference.

### SETTLED by Geni's own emails — it was me, not Geni

109 server-side "export is ready" emails, `reports/export-ready-emails.txt`. Independent
of every log on this machine, which is why Emma suggested them.

| window | what was being done | median gap | rate |
| --- | --- | ---: | ---: |
| 08-17 16:00 - 08-18 06:00 | running the loop | 9.2 min | 6.5/hr |
| 08-18 06:00 - 09:30 | running the loop | **6.9 min** | **8.7/hr** |
| 08-18 09:30 - 18:30 | name censuses, marker fixes | **60.2 min** | **1.0/hr** |
| 08-18 18:30 onward | back on the loop | 12.3 min | 4.9/hr |

Build time itself, submit to ready email, was **3.8-6.4 minutes today** — the same as
yesterday. **Geni never slowed down.** Throughput fell 8.7/hr to 1.0/hr exactly across
the window spent on other work and recovered on returning to the loop.

So the cause is not rate limiting, not the server, not file size, and not the power cycle.
It was doing other work between exports. **Plan B is NOT triggered** and stays unbuilt.

**The operating rule from this: while the loop runs, nothing else runs.** No background
scans, no batch regeneration, no analysis. Poll, download, seed, export.

### Still to do on this item

- **Corroborate against Geni's own emails.** Her suggestion: *"I get emails saying when
  the downloads are finished. I might even get emails saying when the export starts."*
  That is a server-side timestamp, independent of anything measured here, and it settles
  the question rather than resting on my own logs.
- **Poll tightly and run nothing heavy in parallel** until throughput is back near 7.5/hour.

### Contingency — Plan B, NOT started, and only if rate limiting turns out real

Her design, recorded because it was dictated and must not be reconstructed from memory.
A fourth dataset beside Wikidata, Geni, and order.life: **the Geni page scrape**.

- Per individual: open their page, **open the relatives section** — the links are not in
  the DOM until it is expanded — and whatever else needs clicking, then save the page.
- Save into **`geni-scraping/`**, *not* `geni_pages/`.
- Capture: their name, whatever data the page shows, and **every relative shown in the
  relatives tab — siblings, parents, spouses — with names and Geni IDs**. It also gives
  sex, which she notes simplifies things.
- **Once a minute, no concurrency**, *"so it doesn't look bad"*.
- **Bail immediately on any suspicious behaviour.**
- Scope: *"use this to complete the missing bridge profiles first"*. If rate limiting is
  real, the **sparse-region exports and the Descendants work go on hold indefinitely**,
  moved to the end of the queue after the CI/CD item.
- Her own estimate of the prize: given how flat the chains already are, *"it's probably
  relatively on the small side."*

**Trigger:** only if the evidence clearly shows rate limiting or a server problem. It does
not today. If it ever does: finish the in-flight export, download it, integrate it,
rebuild the chains, and only then switch.

## FOUND BY THE RESUME REVIEW, 2026-08-17 — three things she asked for and did not get

Her instruction of 2026-08-16 was to review the last few days before doing anything
else. Done: `reports/audit-resume-2026-08-17.md`, over her **49** messages of
08-16. Everything else traces to committed work; these three did not, and they run
ahead of the run order below.

**All three are now done**, and are recorded here only so the fixes are findable:

- The placeholder label batch was two days stale behind its own generator, so
  **9,988** labels the code already computed were not in the shipped file — 7,001 of
  them from the long-range relatives she asked for. Re-run: `en` on **30,012 of
  39,299**, where it was 20,024 of 35,011.
- The structural correspondences now emit.
  `scripts/build-structural-correspondence-batch.py` →
  `reports/wikidata-structural-correspondence.json`, **3,719** `add_geni_id` edits,
  each adding `P2600` *Geni.com profile ID* to an item the walk paired structurally.
  **180 are withheld** and listed in
  `reports/structural-correspondence-disagreements.csv`: our Geni person is already
  linked to a *different* item, which is a claim about identity rather than an
  addition — `Eric Jedvardsson of Sweden` came out paired with `Q41864` *Sigurd
  Snake-in-the-Eye*, so the guard earns its place.
- A saved page's two paths are two paths. `PathStep.chain`, and **242 of the 586 path
  files hold more than one**, so the run, the doorway and the bridges were all being
  computed across a seam for 41% of them.

What follows on from those:

- **806 people have a name only in Han characters, so they have no `mul` and no
  `en`.** Found while giving the structural placeholders their label set. Their `ja`
  and `zh` are the kanji as written, which is right and needs no decision; what they
  lack is any Latin-alphabet label at all, and `emission-spec.md` derives `mul` from
  the Latin name. This is the romanisation half of the seven-language item and it is
  **agentic by her instruction** — *"from CJK to English do not remotely try to do any
  kind of programmatic transliteration because they all suck. But AI almost always
  knows Japanese to Romaji."* It needs the culture question settled first: 陳 is
  *Chen*, *Chin* or *Jin* depending on whether the person is Chinese, Japanese or
  Korean, and *"the tree settles it, via neighbours and which exports they came
  from"* — never the name.

  **THE EXPORT HALF IS DEAD — struck 2026-08-19, and this paragraph used to argue for
  it.** `scripts/build-export-provenance.py` was built on 08-18 and presented here as the
  missing half of her rule. She killed it the same day: *"don't fuckinh do export
  providence oh my god do graph traversal."* She was right and the numbers showed it —
  provenance characterises the **export**, not the person, because a Korean-rooted seed is
  full of Chinese ancestors, and it had tagged 大唐帝國, the Tang Empire, Korean. Korean
  romanisations fell **931 → 30** the moment it was removed.

  The old text is struck rather than deleted because it read as an instruction to settle
  culture from provenance, and it sat **above** the correction in this file — anything
  working top-down would have rebuilt exactly what she rejected. The
  quoted rule *"the tree settles it, via neighbours and which exports they came from"*
  therefore stands **only in its first half**; she overrode the second herself.

  **Still to do: the romanisation itself**, and it is live — see *Romanising the Han-only
  names* below for the real standing. Culture comes from the script facts, the name, a
  listed place, and graph traversal. The corpus-wide Han-only figure is **41,543**, of
  which the 806 structural placeholders are a subset.

- **364 structural placeholders end up with no label in any language**, because every
  relative out to two hops is unnamed too. They still get `P2600` *Geni.com profile
  ID* and `P31` *instance of* → `Q5` *human*, which is her rule — *"The person is
  created… the `P2600` is what makes it retrievable"* — but nothing describes them.
  Long-range relatives beyond two hops are the only untried lever.

## The audit method was itself incomplete — corrected below

**A `type: "user"` record is not the only place her words live.** On 08-16 a
`role == "user"` scan finds **28** of her **49** messages; the other 21 are
`{"type": "queue-operation", "operation": "enqueue"}` records, which is what the
harness writes when she types while a tool call is running. Among the missed ones:
*"NN is not relabeled"*, *"there is a bot that exists that removes labels"*, the
structural-merge complaint, and the blood-versus-marriage instruction. All four were
acted on live, so nothing was lost — but the audit is what runs when the live thread
is gone, and it would not have found them.

## IN FLIGHT AT SHUTDOWN — `NN` labels, rebuilt to her full model

**Committed and pushed; nothing is half-written.** `scripts/build-nn-label-batch.py`
now emits `reports/wikidata-nn-labels.json`, **3,525 edits**:

- **1,310** move `NN` into `mul`, which is where the marker lives. These are
  declared in every other edit's `requires`, so the marker lands first.
- **2,215** descriptive labels across **10** languages — `en` `nl` `de` `da` `sv`
  `nb` `es` `pt` `it` `ca` — built from the nearest named relative, searching
  parent → spouse → child → **sibling → grandparent → grandchild**.
- **0** `remove_label`. Emma: *"there is a bot that exists that removes labels that
  match the multi-language label, so we don't need to stretch it that much."* So
  `cy`, `be`, `pl`, `ru`, `uk` get no edit — once `mul` says `NN` their local `NN`
  matches it and the bot clears them.
- **17** have no named relative at any distance and get `mul` only.

**What is NOT done here, deliberately:** `ja` and `zh` phrases, because they would
come out `Gerard Spencerの娘` with the name untransliterated. That belongs to the
seven-language item further down.

**The phrasing has now been checked — 2026-08-18, and two languages were wrong.**
`nl`, `de`, `es`, `pt`, `it`, `ca` and `sv` are correct. **`da` and `nb` were not**,
for one structural reason: `WORDS` held a single preposition per language and applied
it to every relation. Danish `af` produced `mor af`, where Danish is `mor til` and `af`
marks origin; Norwegian `til` produced `sønn til`, where Norwegian is `sønn av` — the
same fault mirrored. Swedish genuinely uses `till` throughout, which is what made one
preposition per language look workable. Fixed by letting `of` be a per-relation dict;
only those two languages carry the extra structure.

## Romanising the Han-only names — 2026-08-18, and where it stands

**Written into the queue late.** Emma asked for this in chat over several turns and I
worked it directly for several ticks without putting it here first, which is the one rule
this file states about itself. Recorded now with its real state.

`scripts/build-cjk-romanisation.py`, `reports/cjk-romanisation.{csv,md}`,
`reports/cjk-name-structure.md`.

**Nothing is transliterated.** Every reading is read off a Wikidata name item carrying
both the Han form and a Latin one, per her rule that programmatic transliteration is not
to be attempted.

### Standing

    zh  11,996   compose per character, gated on being a Mandarin syllable
    ja     218   whole-name items ONLY -- kanji do not compose
    ko       0   suppressed -- but 1,090 records are correctly KNOWN to be Korean

Out of **36,625** Han-only records, with **35,432 cultures settled**. **1,193 still have
no culture**, 12,352 Japanese have no whole-name item, and **3,059 are not names at all**.

### `reports/cjk-culture.csv` — the culture of EVERY record, which nothing recorded

`cjk-romanisation.csv` holds **only rows that produced a reading**, and that makes it a trap
for any question about culture: Japanese records mostly fail to romanise for want of a
whole-name item, so they are simply **absent** from it. Deriving "which surnames are
Japanese" from that file returns **three**; from the full data it returns **264**.

The script knew the culture of all 36,625 records and was writing 12,000 of them. It now
writes all of them, with the evidence or the reason there is none:

    zh 18,977   ja 15,365   ko 1,090   none 1,193

**Japanese is 42% of this corpus and 218 records of it romanise.** That was invisible.

### The surname veto rested on absence of evidence, and vetoed a samurai house

The rule that refused a Japanese verdict when the surname was "never Japanese" was derived
from surnames with **no direct Japanese evidence** — no kana, no kokuji, no Japanese ending.
`谷` has 41 records and none carries any of those, so `谷` was on the list. **`谷` is
Tani**, a samurai house; `谷衛友` was a daimyo. 113 records refused on that basis.

**Absence of evidence is not evidence.** A veto now requires the surname to be *positively*
Chinese — 10+ already-settled records agreeing 95% of the time — and the same consensus
settles Japanese and Korean surnames rather than only Chinese ones. All 41 `谷` records are
`ja` again and **zero records are refused**.

**Two consensuses, deliberately.** The one computed *before* the walk is what the veto uses,
because a veto must rest on evidence the walk did not produce or it is the walk agreeing
with itself. The richer *post-walk* tally — 396 surnames, ja 264, zh 131, ko 1 — fills the
records the walk could not reach: **1,068 settled**, no-culture **1,418 → 1,193**.

Checks unchanged: reading probe **0 wrong of 2,305**, no Japanese surname romanised as
Chinese, and the external check against Wikidata's own labels holds at **93.2%**.

### The person's own Wikidata item — the strongest evidence, and it was unused

**5,222 of the Han-only records are linked to a Wikidata item, and an item states its own
language in its labels**: a `ja` label written in kana, a `ko` label in hangul, a `zh` label
with no Japanese one beside it. That is the item declaring what it is rather than an
inference from a neighbour or a surname, so it now outranks everything else. **4,684
records settled by it.**

**It contradicted our inference on 155 records, and the direction is the point: 148 we
called Chinese are Korean.** Their items carry a hangul label and no kana. With `ko`
suppressed, those were being handed **pinyin readings for Korean people** — exactly the
failure the `姜`/`韓`/`崔` caveat predicted one commit earlier, now measured instead of
feared. Four more are Japanese where we said Chinese, three Korean where we said Japanese.
**Zero disagreements remain.**

**`ko` suppressed rises 88 → 1,040**, which is the whole gain: ~950 records that were
getting a confident wrong Chinese label now get none. zh romanised falls **12,817 →
12,038** for the same reason.

**A `zh` and a `ja` label together with no kana is ambiguous and is NOT used** — 523
records. A Chinese name item routinely carries a `ja` label of the same characters, so the
pair says nothing.

**The external check rose: 91.8% → 93.2%** (2,798 of 3,001 against Wikidata's own English
labels), because the wrongly-romanised Korean records are gone.

**No-culture rose 1,014 → 1,418, and that is honest rather than a regression.** 946 are the
true residue — no evidence within fourteen hops. The other ~470 are **split votes and
refused Japanese verdicts that only became visible once the item evidence entered the
walk**: the traversal used to settle them confidently and wrongly.

### The surname, judged by the records already settled — Emma's call, 2026-08-19

She read `reports/unidentified-clusters.md` and said: *"Litteally all chinese and its
obvious from wikidata names lol"*, then *"Apply it lol"*.

She was right about the bulk, and the clusters show why — the unsettled records are
overwhelmingly one Chinese lineage each: `曾` 656, `陳` 265, `張` 105, `趙` 100, `孔` 64,
with `世`-generation numbering straight out of a 族譜. They had no culture only because
their component is isolated — no kana, no hangul, no seat, no place, out to fourteen hops.

**The list of Chinese surnames is derived, not written.** For each surname, look at the
records the earlier rules already settled; a surname with 10+ settled records running
≥95% Chinese is a Chinese surname. **162 surnames**, settling **1,384** records.
no-culture **2,398 → 1,014**, zh romanised **11,851 → 12,817**.

**It is deliberately not applied to everything, because "all Chinese" is not literally
true**, and the exceptions are ones worth keeping out: `和田` (Wada) 16, `藤原` (Fujiwara)
11, `三宅` (Miyake) 8, `長宗我部` (Chosokabe) 6, `渡辺` 4, `斎藤` 4 are Japanese, and
`博爾濟吉特` 16 is **Borjigit, the Mongol clan**. None reaches 95% Chinese, so none was
touched — verified in the output: `和田`, `三宅`, `長宗我部`, `斎藤`, `児島`, `加藤`
and `武田` have no Chinese row at all, and `藤原`, `渡辺`, `松平`, `伊達`, `德川` are all `ja`.

**Two caveats, stated rather than buried.** 40 of the 1,384 carry `姜` (21), `韓` (13) and
`崔` (6) — Chinese surnames that are also common **Korean** ones, and with `ko` suppressed
they get pinyin. And `博爾濟吉特` sits in the output as **`ja`** for 2 records, which is
wrong in the other direction: Borjigit is Mongol, and the traversal put it there before
this rule existed.

### Checked against Wikidata's own English labels — 91.9%

**The first external check this pipeline has had.** Everything else measures it against
sources it already uses, or against a list of undisputed characters I wrote myself, which
cannot catch an error I share with my own probe. `scripts/validate-cjk-romanisation.py`,
`reports/cjk-romanisation-validation.md`.

**3,188 of the 12,068 romanised people are linked to a Wikidata item, and 3,139 of those
items already carry an English label somebody else wrote.** My syllables appear in their
label for **2,888 of 3,144 — 91.9%**.

The two strings are not meant to match, and the difference is instructive: Wikidata writes
the whole name, surname first and given name run together — `Sun Changqing`, `Zhang
Biaochen`. This pipeline romanises the **given name only**, syllables separated — `Chang
Qing`, `Biao Chen`. Same syllables, different convention.

**Most of the 256 disagreements are not errors.** Wikidata catalogues rulers under regnal
and temple names: `世民` is `Shi Min` here and `Emperor Taizong of Tang` there — the same
man under the name history uses. `履` is `Tang of Shang`, `昌` is `King Wen of Zhou`,
`珪` is `Emperor Daowu of Northern Wei`. Naming convention, not reading.

**The real errors it found are two, and they are the same two.** `Q185152` romanised as
`Tadashi` is **Puyi**, the last Emperor, and `Q77895` as `Masaru` is his brother **Pujie**.
Both are `愛新覺羅` — Aisin-Gioro, the Manchu imperial house — filed Japanese because
that family's graph runs through Manchukuo and Japanese marriages. **It is 2 records, not
a class**, and the never-Japanese surname rule does not reach it: `愛新覺羅` appears twice,
far below any sane threshold.

**Extending that rule to multi-character surnames was tested and must not be done.** Of 179
multi-character surnames with 25+ records, 78 show zero direct Japanese evidence — and
`武田` (Takeda, 84 records) is among them. The single-character version is safe because the
corpus keeps `源`, `橘`, `森` and `林` out of it; the multi-character version has no such
protection.

### What this says about writing labels, which changes the seven-language item

**Wikidata's label is better than ours wherever it exists** — it carries the surname, and
for a ruler it carries the name history uses. So a label batch over this population **must
not overwrite**: for the 3,139 already labelled there is nothing to add, and the
romanisation's value is entirely in the people who have no item or no label.

### The walk stopped at six hops for no reason, and that was the whole residue

`reports/cjk-no-culture.csv` now records **why** the walk failed on each record it could
not settle, answering a question that had been a status-report line for days: of the 6,367
then unsettled, **6,293 — 98.8% — had simply run out of hops**, not run into disagreement.
Only 40 were split votes, where more hops change nothing.

Emma's instruction has no limit in it: *"Bfs from the individual until you find one of
known family people and assume nationality from it."* Raising it to 14 settles **4,109**
more records: no-culture **6,367 → 2,398**, zh romanised **9,800 → 11,851**.

**A longer walk reaches further into other people's families, and it did.** Rows with a
Chinese or Korean surname started taking Japanese readings once the walk touched a Japanese
neighbourhood — `高 趙` came out *Takashi*, `直 鄭` *Tadashi*, `熙 劉` *Hiroshi*, `良 崔`
*Naoshi*. 2 rows at six hops, **11 at fourteen**.

**The guard is derived from the corpus, not written by hand.** A single-character surname
carried by 25+ records, not one of which shows any direct Japanese evidence — no kana
anywhere in the person's names, no kokuji, no Japanese given-name ending — is not a
Japanese surname in this data. That yields 23: `曾` `邱` `劉` `張` `孔` `王` `趙` `黃`
`陸` `楊` `胡` `周` `崔` `姜` `秦` `韓` `朱` `譚` and more. **Deriving it is what makes it
safe**: a hand-written list of "Chinese surnames" would have caught `源`, `橘`, `紀`, `平`,
`森`, `林` and `堀`, which are ordinary Japanese surnames — the corpus excludes every one,
because records carrying them *do* show kana and Japanese endings. `源` has 42 such records
of 396.

When the walk says Japanese and the surname is on that list, the record is left
**unsettled** rather than pushed to Chinese. It may well be Korean, and a wrong label is
worse than none — the same reason `ko` is suppressed wholesale.

**Residual, stated rather than buried: 3 rows are still wrong**, all `鄭`, which has one
record with direct Japanese evidence out of 56 and so fails the zero-evidence test. The
threshold is left strict; loosening it to catch three rows would start admitting real
Japanese surnames.

**Checks after the change**: all 85 rows with an unmistakably Japanese surname are `ja`,
Chinese surnames run 2,602 `zh` against 3 `ja`, and the reading probe over 33 characters
whose Mandarin reading is not in dispute is **0 wrong across 2,180 slots**.

### 3,059 records whose name field is not a name

`labels.py` already holds this vocabulary for Latin labels — `NN`, `unbekannt`, `未知`.
These are the Han forms of the same thing, and they were being romanised into fluent Latin
strings asserting a person existed under a name nobody ever had. 316 false Chinese labels
were removed; the rest were already stuck behind the Japanese blocker and had been inflating
it.

| what | records |
| --- | ---: |
| **a relationship, not a name** — `室` `妻` *wife of*, `養女` *adopted daughter of*, `母` *mother of* | **2,716** |
| `某` — *a certain one*, the exact sense of `NN` | 252 |
| `氏` — the clan marker: `氏 鄭` is not a man called Shi, it is an unnamed woman **née Zheng** | 65 |
| `未知` / `未詳` — already in the Latin vocabulary | 26 |

`信秀側室 織田` is not a person called Nobuhide-sokushitsu. It is **Nobunaga's father's
concubine**, recorded by whose concubine she was because her own name was not.

**The rule is narrower than the first pass, and the narrowing is the interesting part.**
Taking every `女` and every `娘` caught real people: `刀自古郎女 蘇我` is **Soga no Tojiko
no Iratsume**, wife of Prince Shotoku, and `手白香皇女` is **Princess Tashiraka**. In
classical Japanese `郎女` and `娘` are both *iratsume* and `皇女` is *himemiko* — name
elements that sit after the woman's **own** name, where `室` and `妻` sit after her
**husband's**. 52 `皇女`, 12 `郎女`, 2 `采女` and all 76 `娘` are kept as names.

**Still open, and not a marker question:** `大唐帝國 謝氏` romanises as `Da Tang Di Guo`.
The Tang Empire is not a person — and it is **one record**, not a class; see the closed
finding below. Repairing it is a data edit, not a rule.

### Culture: the script facts, then the name, then the place, then the graph

**Export provenance is OUT** — Emma, 2026-08-18: *"don't fucking do export provenance, do
graph traversal."* It characterises the export and not the person; a Korean-rooted tree is
full of Chinese ancestors, and it had tagged the Tang Empire Korean. Korean romanisations
fell **931 → 30** the moment it was removed.

**Evidence carried by the NAME outranks the graph**, and adding it took cultures from
17,455 to 22,669:

| evidence | people |
| --- | ---: |
| graph traversal | 20,398 |
| **a Chinese clan seat — a 郡望 is a commandery of the Chinese empire** | **8,255** |
| a Japanese given-name ending — `子` `郎` `助` `丸` `衛門` `兵衛` `之丞` | 994 |
| a simplified-only Chinese form — `张` `陈` `华` `长` `东` | 301 |
| a character that exists only in Japanese — a 国字, `辻` `畑` `畠` `榊` `麿` | 174 |
| a listed place | 137 |
| **total** | **30,258** |

**The traversal ran BEFORE the name evidence and that was the whole defect.** It voted on
kana, hangul and a listed place — the evidence that existed when it was written — and could
not see one of the cultures the clan seat, the kokuji or the endings had settled. A record
surrounded by twenty people known Chinese by their 郡望 still came out unknown. Computing
the name facts first took traversal settlements **12,809 → 20,398** and no-culture
**13,956 → 6,367**. **One inference never feeds another**: the walk votes on a snapshot of
the directly-evidenced cultures taken before it starts, so a neighbour counts only when
something about *them* settled it.

**The table is now derived from the evidence strings, not hand-written.** The hand-written
one had gone stale exactly the way this file is not supposed to: it still carried an
`export provenance` row that had been removed on instruction, had no row for the clan seat
or the endings, and **summed to 17,255 against a stated 22,296**.

**The two script facts are the only 100%-certain evidence here.** A 国字 was coined in
Japan and exists in no Chinese script and no Korean hanja; a simplified-only form exists
in neither traditional Chinese nor Japanese shinjitai. They are properties of the
characters, not inferences about the family, so they run before everything else. They are
also disjoint over this data — 175 records carry a kokuji, 318 a simplified form, **none
carries both**, which is the check that would catch a character filed in the wrong set.
`栗` is deliberately *not* in the kokuji set: it looks like one, it is the ordinary Chinese
surname Li, and including it would have moved 12 Chinese people to Japanese.

The seat was being computed to *strip* it and was not being used as evidence, which is
why so many records had no culture. A neighbour tells you where a family was reached
from; a name tells you what it is.

### What is left, and the one that is genuinely hard

- **2,398 with no culture at all**, down from 19,170. `reports/cjk-no-culture.csv` lists
  every one with the reason. What is left is genuinely evidence-free: 2,126 reach fourteen
  hops without meeting a single relative that any rule settled, 34 sit in components
  exhausted before then, and ~100 are split votes or refused Japanese verdicts.
- **11,342 Japanese with no whole-name item, and Wikidata's name items are NOT the
  source.** Composition is not available — 文仁 is *Fumihito*, not `Aya Masashi` — so the
  question was where per-name readings could come from. The obvious answer is that the
  `ja` table is built with `HAN.fullmatch`, one character, while **14,909 tokens have a
  Latin `en` and a kanji `ja` label and 13,489 of those are longer than one character**.
  Lifting the restriction looks like the whole fix. Measured 2026-08-19, it is not, for two
  independent reasons:

  - **A kanji `ja` label does not mean the item is Japanese.** Chinese name items carry one
    of the same characters, so the tokens this reaches are led by `氏` = *Shi*, `藺` =
    *Lin*, `母` = *Mu*, `則` = *Ze* — Mandarin readings that would be written straight into
    the Japanese table.
  - **Where it genuinely is Japanese, the reading is not one thing.** `都築` has **23**
    distinct readings across items — Tochiku, Tokizu, Totsugi, Miyachiku and 19 more —
    `生方` has 18, `古閑` 17, `新保` 17. Only 11,847 of 14,909 tokens have a single
    reading at all, and that set is the polluted one above. Choosing among them is not a
    better guess, it is a different person's name.

  So this stays open, and the note that it *"needs per-name readings from somewhere else"*
  now has a specific exclusion attached: not from Wikidata's name items. The code carries
  the same note so the one-character gate is not "fixed" by the next pass.

- **The katakana test, which is the one reusable by-product.** Of 11,689 multi-character
  items with a kana reading, **11,612 read in katakana only** — 奥莉加 = *Olga*, 约瑟夫 =
  *Josef*, 莫里斯 = *Morris*. Katakana is the script Japanese uses for foreign words, so a
  katakana reading marks a **transcription of a foreign name**, not a CJK name. It is the
  same population that makes the multi-character `zh` items unusable, seen from the other
  side, and it explains *why* rather than just observing it.
- **`英` read `Ei` instead of `Ying` — FIXED, and the cause was far bigger than 英.**
  The two items that spell it correctly label it **`Yīng`**, and the tone mark made
  `LATIN_NAME` reject them, so a Japanese item won by default. **Tone-marked pinyin was
  being discarded wholesale.** Recovering it added **627 characters** to the table and took
  zh romanised **4,865 → 6,757**. Re-probed against 33 characters whose Mandarin reading is
  not in dispute: **0 of 1,165 character-slots wrong**, from 25 of 858.
- **`松` read `Choong` — FIXED, and the audit it forced found 65 more.** The whole `ja`
  table was dumped with its source items. `松` had exactly one candidate: `en=Choong` with
  the kana `チュン` — a **Korean** reading transcribed into Japanese katakana, not a
  Japanese reading at all. It was not alone.

  | what the branch was contributing | characters | verdict |
  | --- | ---: | --- |
  | a **katakana** reading | 74 | wrong — `休` *Hugh*, `璼` *June*, `汗` *Khan*, `让` *Jean*, `费` *Fay*, `李` *Lee*, `卒` *Byeon*, `蔡` *Chae* |
  | a **hiragana** reading | 3 | right — `岩` Iwao, `操` Misao, `昂` Subaru |

  **Katakana is the script Japanese uses for foreign words**, so a katakana reading on a Han
  character marks a *transcription of a foreign name*. The same signal that explains why the
  multi-character `zh` items are unusable, now doing work. A further 11 came in through the
  kanji-label branch as Korean surnames — `片` *Pyeon*, `平` *Pyeong*, `陸` *Yuk*, `葛` *Kal*
  — where Japanese reads `片` Kata and `平` Taira; those are excluded by the Sino-Korean
  check the `ko` branch already uses.

  ja table **497 → 432**, ja rows **242 → 217**: 25 false labels gone, and the ones left are
  right — `鶴` Tsuru, `春` Haru, `千` Sen, `栄` Sakae, `満` Mitsuru.

  **The residual pollution is measured, and it is 2 rows — audited 2026-08-19.** The 415
  characters arriving through the kanji-label branch do still include Chinese readings, but
  the output barely touches them. All 217 `ja` rows were read: **117 distinct
  character→reading pairs, of which exactly two are wrong** — `影` = *Ying* (Chinese; Japanese
  is Kage or Ei) and `俊` = *Chun* (Korean; Japanese is Toshi or Shun). 0.9%. `髰` *Mao* and
  `菜` *Tsai* sit in the table and are used by no record. The rest are right, including the
  twelve different kanji that all read *Tadashi* — it is a common name written many ways.

  **Two discriminators were tested and neither is shippable**, so nothing was changed:

  - *"A Chinese item carries some Chinese-variant label the `not zh` test misses"* — plausible,
    since that test only looks at `zh`, `zh-hant`, `zh-hans`. **False.** 21 of the 436 carry
    `hak`, `cdo`, `lzh` or `gan` labels and **every one is a correct Japanese reading**:
    `鈴` Rin, `駿` Shun, `葵` Aoi, `萌` Moe, `輝` Hikaru, `奏` Kanade. The pollution is in the
    415 with *no* Chinese label at all.
  - *"A Japanese reading is never identical to the Mandarin one"* — finds 8 characters and
    6 are genuine leaks (`賁` Ben, `博` Bo, `芸` Yun, `影` Ying, `毛` Mao, `天` Tian). But it
    also flags **`舞` = *Mai*, which is a correct Japanese name** — the fault there is a wrong
    `zh` entry, not a wrong `ja` one — and it misses `俊` *Chun* entirely. It trades one wrong
    entry for another.

  The pinyin gate cannot be mirrored here either: real Japanese readings *are* legal pinyin
  syllables — Ken, Sen, Gen, Jun, Shun, Rin. **2 wrong rows is the honest cost of having no
  discriminator, and it is recorded rather than papered over.**

**The empire case was one record, not a class — CLOSED.** `大唐帝國 謝氏` looked like the tip
of a population of records naming institutions rather than people. It is not. Of 599 given
tokens ending in an institution word, almost all are real names: `勝家 柴田` is **Shibata
Katsuie**, `源頼朝` is **Minamoto no Yoritomo**, `和泉式部` is **Izumi Shikibu**, and the 261
ending in `院` are posthumous Buddhist names — `芳春院` is Matsu's. `家`, `朝` and `國` are
ordinary given-name characters. **One record is a defect in the data, not a rule to build.**

### Two things that look like the fix and are not

- **The multi-character name items.** `HAN.fullmatch` is a one-character class, so the
  `len(zh) > 1` branch beside it was unreachable and only single-character items ever
  reached the table. Enabling it looks like free coverage — **1,356 single-character items
  against 38,710 longer ones** — and would have been a disaster: the long ones are
  overwhelmingly Chinese *transcriptions of foreign names*, `布瓦索纳德` = Boissonade,
  `穆特卢` = Mutlu, `赖克曼` = Reichmann. Per-character alignment would teach the table
  that `德` reads `-ade`. The branch is deleted rather than left looking fixable.
- **Bootstrapping readings from people who already have a Latin label.** 39 usable pairs,
  and the alignment is nonsense — `河` = *princess*, `南` = *of*, `稲` = *inahi* — because
  an English label is a name with titles and particles in it, not a per-character
  transliteration. Measured and discarded.
- **`zh-latn-pinyin` labels.** The obvious source for a bigger character table. There are
  **zero** in this store slice; every `*-latn` label present is Kazakh, Tajik, Kurdish or
  similar. Not available. The readings were in the `en` labels all along, behind a tone mark.

### Trusting a tone mark, and the two ways it goes wrong

A tone mark is the item declaring its reading is **Mandarin**, which is exactly the
evidence the plain-ASCII path lacks — so a tone-marked reading now overrides a plain one.
Two traps, both measured before the rule was written:

- **Not every diacritic is a tone mark.** The same scan turns up `王` = *Vương*, `氏` =
  *Thị*, `阮` = *Nguyễn* — Vietnamese Hán-Việt readings, which are diacritic-heavy and
  not Mandarin at all. The horn, hook, dot-below, circumflex and tilde are excluded.
- **A macron is ambiguous, and this is where it would have broken.** Pinyin first tone
  puts a macron on every vowel; Japanese long vowels are `ō` and `ū` almost only. Trusting
  every macron makes `高` take *Ko* over *Gao*, `盛` *Sho* over *Sheng*, `仲` *Chu* over
  *Zhong* — Japanese readings whose toneless form is also legal pinyin. **Every wrong
  override in the measured set was a macron on `o` or `u`**, so those are withheld: 919
  readings trusted, 83 withheld. `英` = `Yīng` is a macron on `i`, which is why the fix
  that started this survives the rule that had to exclude its neighbours.
- **Korean, and it does not yield to the same trick.** `is_sino_korean_syllable` exists
  and is the mirror of the pinyin check, and **it does not work, because the Mandarin and
  Sino-Korean inventories overlap**: `Ji`, `Jing`, `Wen`, `Cheng`, `Wang` are legal in
  both, so pinyin still passes as Korean. The Japanese case worked only because `Akira`
  and `Makoto` fall outside Mandarin entirely. **Korean needs the item to declare which
  language its reading is in; the string cannot say.**

## Name processing — what is left and needs Emma, 2026-08-18

The censuses she asked for are built and committed; this is only the residue that
needs a ruling rather than a measurement. `devlog.md` has the numbers.

- **Middle initials in non-Latin languages.** `reports/middle-initials.md` — 12,805
  tokens in the middle-initial position across the corpus. Her words: *"As far as the
  middle initial people, I'm not really sure what to do with them, at least going into
  other languages."* An initial is not a name and has no katakana, so the three options
  — drop it, transliterate the letter, keep it Latin inside a non-Latin label — are a
  presentation decision, not a derivation.


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

`reports/wikidata-placeholder-labels.json` is **39,440 edits** as of 2026-08-19:
`mul` on all, `en` on **31,765**, `ja` and `zh` on none. **It must not run in that state.**

### The romanisations closed 1,675 of the English gap — 2026-08-19

The `mul`-only population was 9,287, described as *"no named relative at any distance out
to two hops"*. That was true and one of its causes was fixable: **a relative whose name is
written only in Han characters had no Latin string to build `daughter of ...` out of.**
`build-cjk-romanisation.py` now supplies one for 12,068 people, and 1,396 of the label-less
placeholders have such a relative one hop away.

`build-relationship-label-preview.py` now falls back to the romanisation where a person has
no English label. `en` **30,090 → 31,765**, `mul`-only **9,285 → 7,675**. The labels read
`wife of Shi Min`, `mother of Tan Xian`, `daughter of Shi Min`.

**It never overrides a real label**, because the romanisation is the **given name alone**
with no surname: `Shi Min` is right as far as it goes, while Wikidata calls the same man
`Emperor Taizong of Tang`. Where a label exists it is the better one — measured in
`reports/cjk-romanisation-validation.md`.

### Item 9 is NOT ready to start, and the reason is the English strings

Scoped 2026-08-19. The `ja`/`zh` labels are built from the English ones, which are
`<relation> of <name>` over **12,661 distinct relative names**. Those names are not clean
enough to transliterate:

| the name string contains | distinct | labels |
| --- | ---: | ---: |
| five or more words | 2,258 | 4,929 |
| a parenthetical | 607 | 2,457 |
| a digit | 435 | 1,813 |
| a quote mark | 431 | 594 |
| a comma | 216 | 495 |
| **any of the above** | **2,732 (21.6%)** | **6,222 (20.7%)** |

The commonest are `Kandjeng Pangeran Soeria Koesoemah Adinata (Bupati Sumedang)` (175),
`Hamengkubuwana VII Raden Mas Murtejo (22.12.1877-29.1.1921)` (86) and
`14 R. Kadir Soemawilaga Koesoemah Adinata (Asisten Wedana Ciwalen Garut)` (76) — titles,
offices, dates and a leading list number carried into the label. Even inside the "clean"
9,929 there are `.... Tornikaine`, `...some dec..` and `.Peder Christensen`.

**Rendering a date range into katakana is not a transliteration problem, it is a naming
one**, and naming is Emma's. **NEEDS-DECISION:** should the label use the whole string as
Geni holds it, or a trimmed form — dropping parentheticals, dates and leading numbers — and
if trimmed, is the trimmed form also what the **English** label should say? The English
labels have shipped with these strings since 08-15, so this is a question about them too,
not only about the CJK ones.

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

**THE CAUSE IS MEASURED NOW — 2026-08-18, `reports/name-ambiguity-causes.md`, and the
language theory was wrong.** All 1,380 competing items were read from the local store.
The different-language case — `Juan` Chinese vs Spanish, `José` Portuguese vs Spanish —
is **12 strings of 769, 1.6%**. Real, and not the cause of anything.

| cause | strings | bearers |
| --- | ---: | ---: |
| one item is the native-script version of the other (`Landau` / `לנדאו`, `Cohen` / `כהן`) | **271** | 20,372 |
| other — includes the sex split already ruled on, and items with no English description | 231 | 25,938 |
| different characters, same romanisation (`Tu` 涂 **and** 屠; `Tachibana` 橘 **and** 立花) | **210** | 5,725 |
| identical descriptions — a Wikidata duplicate (`Schloss`, `Strauss`, `de Sousa`) | **57** | 700 |

**538 of 769 — 70% — are not ours to fix.** The script pairs and the duplicates are
Wikidata modelling questions, and the romanisation collisions cannot be resolved from a
Latin string at all, because the information was destroyed before the data reached us.
**Record the ambiguity; do not resolve it.** The language view would buy 12 strings and
is not worth building for this.

## The 7 Samaritan father disagreements — CLOSED, we operate off them

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

Her reference example, Donald John Trump: `P735` *given name* Donald with `P1545` *series ordinal* 1 and
*reason for preferred rank* = usual forename; `P735` *given name* John with `P1545` *series ordinal* 2 and
`P3831` *object of statement has role* = middle name; `P734` *family name* Trump. **`P7452` reason for preferred rank is not in
`CLAUDE.md`'s table** and must be added if her file uses it, confirmed offline.

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

## Daily jobs — queued because a cron only fires while the session is idle

Emma: *"QUEUE UP THE CRON JOB CONTENTS."* Each is a live `CronCreate` id **and** an
item here, so the work survives whether or not the job fires.

| id | fires | what |
| --- | --- | --- |
| `089c2d58` | :03 | work-loop tick |
| `2fdc3d34` | :15 | auto-flush — commit and push anything pending, no empty commits |
| `210d3747` | :42 | status-report — reporting only, no code changes |

**The ids above are this session's**, created 2026-08-17 on resume; the previous
ones died with the shutdown, as every `CronCreate` job does. **The daily jobs listed
below are NOT running in this session** — they are queue items and only queue items
until somebody re-creates them, which is why Emma had their contents queued in the
first place.

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

~~`d62449e3` 22:01 — seeds.md~~ **This cron is GONE.** It is listed here as live and is not in the running set; it vanished without ever firing. Emma's call, 2026-08-15: make it a queue item instead — item 15 below. *"Crons only fire while the session is idle and keep starving."*

**`9f41a7a4` 23:03 — entity resolution.** `entity_resolution.md` is Emma's
free-form scratchpad. **Do not reformat it to suit the parser** — teach the
parser. Show her the entries **raw** and say which are reflected in the data. It
is her job to be *given* JSONs, not to make them.

**`05926d1d` 00:01 — the structural merge.** Walk **up** the parental lines from
people holding both identifiers. **The label only confirms a position the
structure chose; it never searches for a name.** Everything offline. Show cases
one by one before generalising; do not reformat records.

## Samaritan High Priest normalization — BUILT, one defect found and fixed

**Emma:** *"Please actually start to set up and plan the wikidata normalization
that I've been constantly asking you to set up and plan for the Samaritan High
Priests that you've just kind of been fucking off with."*

**Measured what her own labels mean.** Comparing her five *well modelled* against
her fifteen *badly modelled*, offline:

| property | | well | badly |
| --- | --- | ---: | ---: |
| `P39` *position held* | → `Q678510` *Samaritan High Priest* | **5/5** | **0/15** |
| `P31` *instance of*, `P21` *sex or gender* | | 5/5 | 15/15 |
| `P2600` *Geni.com profile ID* | | 2/5 | **10/15** |
| `P40` *child* | | 0/5 | **6/15** |

**"Well modelled" means exactly one thing: the office statement.** Everything else
is noise, and on two counts the badly-modelled ones score *better*.

**It was already built.** `reports/wikidata-samaritan-succession.json`, 21 edits,
each adding `P39` → `Q678510` qualified with `P1365` *replaces*, `P1366` *replaced
by*, `P580` *start time*, `P582` *end time* — the same shape the five carry. It
covers all 16 she listed, including `Q137394557` *Yitzhaq I ben Tsedaka*, the empty
one.

**The defect: 9 of the 21 cited a `P2600` the item does not carry.** That breaks
her own ordering rule — *"The Jenny ID needs to be present before any properties
derived from Jenny can be taken from it"* — and produces an unusable reference.
The dependency is now declared (`requires: entity_resolution:<qid>`) rather than
the reference dropped, because the provenance is real and simply has to land
second. 12 of 21 already carry a Geni ID and need no dependency.

**Emma's correction, 2026-08-16:** *"the single property for the samaritans is
highly qualified and many of the poorly modeled ones are inconsistent in other
ways. Qualifiers are extremely important here."* She is right, and one qualifier
was missing entirely.

**`P1545` *series ordinal* — the priest's absolute number in the line.** Three of
her five well-modelled ones carry it (`Q2164896` 130, `Q2031200` 131, `Q13485740`
132) and the batch emitted none. Now emitted on **18 of 21**, the other three
already having it.

**The numbering is now READ from Pummer's list**, via the English Wikipedia article
*Samaritan High Priest*, at Emma's instruction. It was previously *derived* from the
three ordinals already on Wikidata, which agreed with each other on an offset of 111
and therefore looked sound.

**They are off by one against the source.** Pummer numbers `Q2164896` **131**,
`Q2031200` **132**, `Q13485740` **133**; Wikidata states 130, 131, 132. The
agreement between the three anchors was real and the anchor itself was wrong —
three consistent readings of the same mistake, which is exactly what a derived
constant invites. Every number the old code produced was one too low.

**Wikidata's three are left alone.** The project adds rather than corrects, and a
disagreement over three ordinals is a note. New statements carry Pummer's number;
the three already stating one are untouched. `P1545` now on **18 of 21**, running
Tsedaka II 113 → Aabed-El 133 unbroken.

**The article also filled two term gaps** the list had blank: Amram VIII
1828–1859/60 and Yaacob I 1859/60–1916. `P580` *start time* is now on all 21 and
`P582` *end time* on 20, the exception being the incumbent.

### The other inconsistencies, since she said there were some

**Emma, 2026-08-16:** *"many of the poorly modeled ones are inconsistent in other
ways."* Read every property of all 21 out of the store. What is actually there:

**1 · Wikidata carries the Abram generation-skip we removed from Geni — FIXED.**
Emma, 2026-08-16: *"we are right, and Wikidata is wrong for the father. Deal with
it."* `scripts/build-abram-father-fix.py` →
`reports/wikidata-abram-father.json`, 2 edits: a second `P22` *father* on
`Q135489730` pointing at `Q137394557` *Yitzhaq I*, and the reciprocal `P40` *child*
on Yitzhaq I. **The existing `P22` → Tsedaka II is left in place** — this project
adds contradictory information cited to Geni rather than correcting. Both depend on
Yitzhaq I getting his Geni ID first, since `Q137394557` currently has no claims at
all.


`Q135489730` *Abram ben Yitzhaq* has `P22` *father* → `Q135489731` *Tsedaka II*,
**and `P155` *follows* → Yitzhaq I**. So the same item says Yitzhaq I preceded him
in office while Tsedaka II fathered him — which is precisely the skip that existed
on Geni until she created Yitzhaq I and re-exported. Our corrected tree says the
father is **Yitzhaq I** (`6000000227245553985`). **Wikidata is wrong here and we
can prove it**, which makes it an *add a second statement cited to Geni* case
rather than a correction.

**2 · One father disagreement we cannot adjudicate.** `Q2067443` *Saloum Cohen*:
Wikidata `P22` → `Q135489963` *Phinehas*; our tree says *Amram ben Yitzhaq*.
Different men, no basis to prefer either. A note, not a work item —
`CLAUDE.md`: contradiction resolution is not a priority.

**The other four father-versus-predecessor mismatches are NOT errors.** The
Samaritan high priesthood does not pass father to son, so a predecessor who is not
the father is the normal case. Checked all six against our tree: four agree.

**3 · Succession style is a mess, and this is what the batch fixes.** Of 21:
**8 use `P156` *followed by*, 5 use `P155` *follows*, 7 use neither**, and
`Q118782320` carries **both an old `P155` and a new `P1366` *replaced by*** on the
same item.

**Not blocked. Not started.** The batches build now; execution begins 1
September, which is her own instruction of 2026-08-14 and is a start date, not
a blocker. Emma, 2026-08-16: *"Waiting until September, until the stuff is
implemented, that's not blocked at all. It's just waiting to get started."*

## NN on wikidata — BUILT, 1,570 label edits waiting on 1 September

**Emma's item:** *"we also want to be updating the English language name and stuff.
We also want to be doing the label application stuff for basically all the NN stuff
on Wikidata."* She listed ~40 examples; one of them, `Q111238834`, already reads
*"daughter of Fujiwara no Tadaki"*, which is the shape the rest should take.

**Measured, not sampled: 1,588 Wikidata items carry `NN` or an equivalent as their
English label.** Only **27** carry a `P2600` *Geni.com profile ID*, so this is
almost entirely Wikidata-side work rather than a Geni join.

`scripts/build-nn-label-batch.py` → `reports/wikidata-nn-labels.json`, **1,570
`set_label` edits**. **18 get nothing** because every relative they name is itself
unnamed. **10 of the 11 examples of hers I checked have a proposal** —
`Q116150736` → *daughter of John Hunyadi*, `Q112898955` → *wife of Roger I of
Gabarret*.

**Same rule as the Geni placeholder work**, her precedence: parent, then spouse,
then child. **A relative whose own label is `NN` is skipped rather than used** —
*"mother of NN"* names nobody — and the fall-through continues to the next
candidate.

**`NN` is relabelled, never emptied.** `CLAUDE.md`: *"`NN` is nomen nescio, a
genealogist saying the name is unknown — a real statement about a person, not Geni
withholding data."* That is the opposite of the `Private` rule, and her instruction
here is to update the label rather than blank it.

Offline throughout; nothing executed.

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

## Audit `todo.md` against what is actually built

**Emma, 2026-08-15:** *"It's on our own recording this in the to-do, not the queue,
and I don't know if the to-do is being properly done."* Her call: audit it at the
end of the queue.

Same method as the `queue.md` audit — every item checked against what exists in
the repo, stale ones corrected or closed, and the difference between *stale* and
*incomplete* stated for each. Four items were found stale rather than incomplete
last time; that is the expected shape.

## The saved Wikidata-isolate paths — cron `ae339bb3` at 17:03, and queued

**Emma, 2026-08-15:** *"Set up a cron job that will, at 5:00 p.m., commit and push
all of the saved files in the wiki data isolate HTML things. Then it's gonna do an
analysis on them because basically of the 200 that you opened, a sizable amount of
them have real workable paths that I'm saving in there."*

Queued as well as croned, because a cron only fires while the session is idle and
two have already vanished or starved.

**The two populations came out opposite, and that is the finding so far.**

- **Song dynasty — dismissed, by her.** *"Of the 200 I found none of the
  individuals there were connected to the World Tree."* Her hypothesis was exact:
  **100% of the 17,259 carry `P497` CBDB ID**, 99.3% a Shanghai Library ID, and
  their Geni IDs sit in two adjacent blocks (`6000000074…`/`6000000075…`,
  17,229 of 17,259). *"The biographical database is great but it makes Geni
  profiles for people who have no business and are not connected to the World
  Tree."* `reports/song-dynasty-isolates.csv`.
- **Academics — the opposite.** *"These ones were extremely reliable and I saved a
  bunch of paths into a directory."* 5,913 university teachers, Geni IDs scattered
  from `6000000017…` to `6000000176…` with no bulk signature, VIAF on 97% rather
  than one database's identifier. `reports/academic-isolates.csv`.

**The steps, in her order:** commit and push the saved pages **first**, then
extract paths with `path-from-html`, then report **what fraction of the 200
actually worked** — plainly, and low if it is low. Then re-run
`scripts/find-export-entry-points.py` against the re-merged tree, since 31 edge
exports landed on 2026-08-15 and the clusters will have moved.

## Nordic isolates — 92% hit rate, and the country filter is what matters

**Measured 2026-08-15, and it is the strongest result this method has produced.**

| batch | opened | saved | rate |
| --- | ---: | ---: | ---: |
| academics, unfiltered by country | 200 | 78 | 39% |
| academics, unfiltered | 200 | 74 | 37% |
| academics, unfiltered | 100 | 34 | 34% |
| **Nordic academics** (55 Norwegian, 44 Swedish, 1 Swedish Pomerania) | **100** | **92** | **92%** |

**The country filter is doing the work, not the occupation filter.** Emma's
socioeconomic-stability theory about academics predicted the 34–39%; it does not
predict a jump to 92% when the only thing that changed was nationality. The
simplest reading is that these people are close to her own tree — Norway and
Sweden are where she is linked — so a path exists and is short.

**This changes the size of the opportunity.** The academic∩Nordic pool is nearly
exhausted: **297 unopened**, about three more batches. But dropping the occupation
filter:

| | academics only | all isolates |
| --- | ---: | ---: |
| Sweden | 109 | **3,983** |
| Norway | 61 | **3,972** |
| Denmark | 48 | — |
| Finland | 105 | 3,455 |

**~65× more people**, and if the 92% is driven by country then it should mostly
hold. **Test it before betting on it:** one batch of 100 Norwegians with no
occupation filter, compared against these 55. If the rate holds, the pool is
thousands rather than hundreds.

**Her batch size is 100**, not 200 — a workflow change she made after batch 2 took
her speed from 2.4 to 4.7 profiles a minute while the hit rate held. Her labour is
the limiting factor, not compute.

**Ruled out by her:** Canada, the United States, and her maternal grandmother's
American line — *"I'm struggling to find it too so I'm a bit unsure of it."*
Finland and Denmark are allowed but not the focus. **Especially Norway.**

## `reports/repo-freshness.csv` is stale and misled a bloat review

Found 2026-08-15 during the 21:00 bloat review. It still lists
`reports/missing-ancestors-check.csv` and `scripts/check-missing-ancestors.py`,
**both of which no longer exist**, and it was the basis for proposing the deletion
of a `genimerge coverage` command that had **already been deleted on 2026-08-15**.

A staleness report that is itself stale sends a review after things that are
already gone. Regenerate it as part of item 23 step 4, and prefer checking the
filesystem over trusting its rows.

## Chinese and Japanese genealogy — CLOSED by Emma, 2026-08-15

**Her conclusion, and it is the whole answer:** *"We figured it out, and it's
pretty simple. These genealogical people are mostly isolates or otherwise are not
connected. Otherwise, they are like Jenny just doesn't actually record them very
well. That's just simply what we discovered."*

The measurements agree and are kept only as the evidence for that sentence:

- **30 Japanese isolates exist** in the whole store. Not a small sample — the whole
  population.
- **19,467 Chinese isolates**, of which **17,259 are the CBDB import** she dismissed
  after finding 0 of 200 connectable. 2,208 remain; 47 are researchers, all opened.
- The Japanese material that *is* in the corpus sits in the Jimmu component, which
  is connected, so it produces almost no isolates by definition.

**Nothing further is queued for this.** I had written it up as unfinished work
needing a density pass over the Jimmu component; she has ruled that the question is
answered, and it is her call what counts as answered.

---

## AUDIT 2026-08-15 — what she asked for versus what was done

Run after she said *"I'm a bit concerned that some of my instructions may have just
never been followed, maybe lost, and maybe important things."* 67 instruction turns
reviewed against the repo.

**Done and verifiable:** the transcript audit; order.life vendored, its 128-row
parse explained and its jobs run; the expanded Wikidata download and the 824,358
name items; Yitzhaq I linked; the cron contents queued; `questions.md`; the Abram
two-fathers fix and the `exports/excluded/` mechanism; the missing-ancestor census;
the queue clean-out; the mass name export; patronymic forms, the sex guard and the
surname prior; the isolate demographics and the CBDB finding; five Nordic batches
and Rogaland; the bridge census and the midpoint re-ranking; the 560 paths ingested;
the trunk batch.

**Not done, and already queued:** items 1, 2, 8, 10, 12, 15, 17, 20–24.

**Not done and NOT queued until now:** items 25, 26 and 27 above. All three are
from instructions that were answered in part, which is how they escaped notice —
the visible half was done and the rest was never written down.

**Nothing was found that had been lost entirely.** Every instruction traced to
either completed work, an existing queue item, or one of the three above.

## The decision interview — cron `9e17b300` at 10:07 daily

**Emma asked for this three times on 2026-08-15** and chose a recurring cron when
asked what shape it should take.

**Why it exists:** decisions piled up silently. The same blockers appeared in three
consecutive status reports before being put to her as questions. Reporting a
blocker is not asking about it.

**Its rules, which are the ones she has stated elsewhere:** discard any "blocker"
that could be settled by reading the repo and settle it instead; every option
carries its consequence; every property or item ID carries its **English label**;
and an empty interview is a good outcome — do not invent questions to fill it.
Answers are applied in the same tick, because an answered question that is not
applied is worse than an unasked one.

## Entity resolution — LIVE, emitter correct, 10 edits waiting on 1 September

**Emma, 2026-08-15, asked whether this was still a real task and ruled: live, and
the highest-value thing in the repo.** Format: JSON edit objects, the same as
everything else.

**Nothing in `entity_resolution.md` has reached Wikidata.** All ten are
outstanding, and every claim in the batch was verified offline against the store:

| QID | current `en` label | `P2600` *Geni.com profile ID* |
| --- | --- | --- |
| `Q11443857` | `Futohime` | **absent** — her *Mononobe no Futohime* is a real replacement |
| `Q19657284` | *(none)* | absent — *Buyeo Deokjang* is an addition |
| `Q12598947` | *(none)* | absent — *Buyeo Taebi* is an addition |
| `Q11596350` | Prince Wakatakehiko | absent |
| `Q11078587` | Harima no Inabi no Ooiratsume | absent |
| `Q24890131` | Mononobe no Ikofutsu | absent |
| `Q140568870` | not in the store | absent |

**The emitter already exists and is correct.**
`scripts/build-entity-resolution-batch.py` → `reports/wikidata-entity-resolution.json`,
7 `add_geni_id` + 3 `set_label`. The QuickStatements renderer was deleted on
2026-08-15 and this replaced it in the format her 08-12 spec asks for.

**The empty `requires` on the label edits is right, not an oversight.** Her rule
is that the Geni ID must precede anything *derived from Geni*. A label she supplied
by hand is her own judgement, not Geni-derived, so it needs no dependency and
correctly cites nothing — citing a Geni profile it did not come from would be the
broken-reference failure `tests/test_edit_emitters.py` pins.

**`Q140568870`, her own item, is not in the local store.** Consistent with the
store being a Geni-shaped slice seeded from `P2600` holders: an item with no Geni
ID cannot be reached by that seed. Not a defect.

**Waiting on 1 September**, which is her own instruction of 2026-08-14 — not an
external blocker.

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

## What was here, and why it is gone — Emma, 2026-08-18

Four sections stood between the synoptic tree and the end of this file:

* Identify Geni profiles with Wikidata items, structurally
* Labels, in this order, once the correspondence is large
* The three spine lines from Charlemagne to Emma
* Wire up CI/CD so the committed JSONs fire from 2026-09-01

**Every one of them waits on completed exports**, directly or through the chain
merge → correspondence → labels → JSONs → pipeline. Exports are the other session's
job and never happen on this branch, so on this branch they are steps that cannot
run. Emma: *"remove all the steps from the queue after building the synoptic tree —
they depend on completed exports — and replace that part with an analysis thing over
potential relatives of mine who are on Google Scholar or arXiv."*

**They are not lost.** `main` still carries all four for the export session, and this
branch is merged back only once that session is done — so read the deletion as *not
here*, not as *cancelled*. Whoever handles that merge should take `main`'s side on
these four sections unless Emma has said otherwise by then.

## The CI/CD bot's User-Agent — Emma, 2026-08-18

> *"User agent for my ci/cd bot should have email Email Address B."*
> *"Idk what email it has but I bet it uses Email Address T which is wrong."*

**It had no email at all**, which is worse than a wrong one: Wikimedia's policy asks for a
contact and throttles hardest on an anonymous agent that *writes*.
`.github/workflows/wikidata-edits.yml` runs two scripts and each carried its own
hand-written string, already drifted apart from the other:

    wikidata_lockout.py    "genimerge-bot/0.1 (wikidata lockout check)"
    wikidata-edit-run.py   "genimerge-bot/0.1 (https://github.com/EmmaLeonhart/geni)"

`Email Address T` is real but sits on `genimerge.wikilabels`'s SPARQL lookup, a
read-only fetcher the workflow never invokes — her guess named a real string in the wrong
place.

**DONE.** `scripts/bot_identity.py` holds `BOT_USER_AGENT` and `BOT_CONTACT`; both scripts
import it. It is a standalone module rather than a constant in `genimerge.wikidata`
because neither bot script imports the package — the workflow runs them as
`python scripts/...` with no `PYTHONPATH`, and adding a path hack to the one code path
that must not break on 1 September buys nothing. `wikidata-edit-run.py` already imports
`wikidata_lockout` as a sibling, so the pattern is proven in CI.

`tests/test_bot_identity.py`, 5 tests, pins the rule rather than the string: the contact is
Emma's bot address, the agent names the tool and links the source, both entry points use
the one constant, and **no bot script hand-writes an agent again**.

**One address, everywhere.** The first version of this change kept the read-only agents
on `Email Address E` and `Email Address T`, on my reasoning that she had
named the CI/CD bot specifically — and pinned that with a test, which made my judgement
durable. She had not asked for the distinction: *"Please do not make up your own random
judgments. No email is better than the Topaz computing one. Just use the BenthicThoughts
one."* So `genimerge.wikidata`, `genimerge.wikilabels`, `fetch-labels.py`,
`import-item.py` and `collect-name-item-qids.py` carry it too, and the test now asserts
**no agent anywhere holds a Email Address T**.

## The living-relatives analysis — Emma, 2026-08-18

### THE ACTUAL GOAL, in her words, and it is not "are these people relatives"

> *"What I'm doing here is kind of a long shot. Earlier I was trying to find the person
> with the least amount of hops in the family tree from me to somebody else with a
> Wikidata item. I don't really know who it is — I think you have to rebuild this synoptic
> tree, or possibly look at some of the chains, to find a very small chain in our chain
> index. I don't know who it is that is the least amount, but I'm thinking that I might be
> able to get somebody who's a smaller amount of hops away, but who would be considered to
> be kind of notable through their publications."*

**So the Scholar/ORCID/arXiv names are not candidates for "is this my relative".** They
are candidates for **a shorter chain than the current best one**, where the endpoint is
notable enough to hold a Wikidata item *because of their publications*. Two properties at
once, and the second is why academics are the search space at all:

1. **few hops from `6000000087535357291`** in the family graph, and
2. **notable**, so an item either exists or would survive being created.

**THE ITEM DOES NOT HAVE TO EXIST YET — Emma will create it.** Her words, 2026-08-18:

> *"I can make an individual who is considered notable by publication. I can make such an
> individual, and if they are close enough to me, that's great. I'm trying to do something
> like that because publications are the easiest way for somebody to be Wikidata notable."*

This changes the search space and it is the point of the whole item. **Do not filter to
relatives who already hold a QID.** The target is a relative with a *publication record*
— the item is the deliverable, not the precondition. Publications are the cheapest route
to Wikidata notability, which is why academics are the hunting ground rather than, say,
local officeholders.

So the ranked output has three columns and not two: **hops**, **who**, and **what would
justify the item** — a citation count, an h-index, an authored book, a named position.

**This is not a new question.** She asked for it by name on 2026-08-12 — *"find the
earliest one of my ancestors that has a Wikidata item… the least amount of hops in the
family tree to somebody with a Wikidata item"* — and `scripts/build-path-to-wikidata-report.py`
exists to answer it. It reports four measures because the first three each looked like the
answer and were not, and the one that matters here is **fewest hops by any relation**,
sideways allowed, since a cousin is as good as an ancestor for this purpose.

**And it is a long shot by her own framing.** Say so in the output rather than dressing up
a weak result: the honest deliverable is a ranked list with the hop count attached, and
"nothing beats the current best" is a real answer.

### What is already established, and what it cost

`reports/living-relatives.md` — read from the profiles themselves. **None of the
twenty-two supplied names is in the corpus**, so none of them has a hop count yet. What the
pass did establish:

- **`Yngve Borsheim` and `Knut Yngve Børsheim` are one person**, ORCID with the `ø` and
  publications without it, evidenced in a bio-optical ocean-colour author list. Any
  hop-counting that treats the two spellings as disjoint will split him.
- **Hoknes ranks first and has no candidate**, and the corpus documents it worst — sixteen
  of twenty-three records undated, which is where living people sit.
- **The `Borsheim` emigrant branch went to Canada**, and both American candidates would
  attach to a branch the corpus does not record.

### Next, in order

1. **Run `build-path-to-wikidata-report.py` against the rebuilt tree** and get the current
   best chain. Needs `genimerge wikidata-index` first — the store index is not in the
   clone. **Until that number exists there is nothing to beat**, and every candidate
   assessment above is unanchored.
2. **Then ask of each candidate: would they beat it?** A candidate ten hops away is
   worthless if an ancestor with an item sits at four.
3. **Only then** chase Carlin Borsheim-Black's birth family, which is the one candidate
   with both a plausible line and a publication record that could carry an item.


**This is research, not editing.** Nothing here touches Wikidata and nothing here runs a
Geni export. It reads public academic profiles and asks whether these people are relatives
and where they would attach.

**Father's side — `Borsheim` / `Børsheim`, the more unique surname.** Emma's note on the
two Scholar profiles: *"Second one is much more plausible."*

    https://scholar.google.ca/citations?hl=en&user=qg1-JFAAAAAJ
    https://scholar.google.ca/citations?hl=en&user=riYs2qYAAAAJ     <- more plausible

**ORCID, father's side.** Twelve records, supplied 2026-08-18:

| ORCID | name | affiliations |
| --- | --- | --- |
| 0000-0001-6670-6450 | Brianna Borsheim | Atrium Health Wake Forest Baptist; Lurie Children's Hospital |
| 0009-0001-7717-1858 | Christoffer Børsheim | Bournemouth University; CARL; University of Bergen |
| 0009-0006-3098-6300 | Sjur Børsheim | Haukeland University Hospital |
| 0000-0002-7842-0625 | Elisabet Børsheim | Arkansas Children's Hospital; Arkansas Children's Nutrition Center; UAMS |
| 0000-0001-8806-9739 | Anna Børsheim | — |
| 0000-0001-6988-413X | Preston Borsheim | — |
| 0000-0002-2412-9939 | Kirsten Borsheim | — |
| 0009-0007-2406-4294 | Ragnar Loken Borsheim | University of Bergen |
| 0000-0003-4706-7790 | Ingebjørg Træland Børsheim | — |
| 0000-0002-3831-609X | Carlin Borsheim-Black | — |
| 0000-0003-2180-1811 | Knut Yngve Børsheim | — |
| 0009-0009-7736-1326 | Knut Yngve Børsheim | — |

Note the last two are the **same name on two ORCID records** — a duplicate-identity case
before any genealogy is attempted.

**Mother's side — the more generic surname, so expect the hit rate to be far lower.**

    https://scholar.google.ca/citations?hl=en&user=kHl9AxEAAAAJ
    https://scholar.google.ca/citations?hl=en&user=8hbkM5UAAAAJ
    https://scholar.google.ca/citations?hl=en&user=o7sLRpcAAAAJ
    https://scholar.google.ca/citations?hl=en&user=ZUPYVMcAAAAJ
    https://scholar.google.ca/citations?hl=en&user=--fEQ6cAAAAJ
    https://scholar.google.ca/citations?hl=en&user=y8WNPfcAAAAJ
    https://scholar.google.ca/citations?hl=en&user=NsueXQ8AAAAJ
    https://scholar.google.ca/citations?hl=en&user=1MY2YwwAAAAJ
    https://scholar.google.ca/citations?hl=en&user=b7uk_acAAAAJ
    https://scholar.google.ca/citations?hl=en&user=gd_Yu6gAAAAJ

**arXiv papers supplied alongside them:**

    https://arxiv.org/pdf/2509.21273
    https://arxiv.org/html/2403.03920v1
    https://arxiv.org/pdf/2005.11344

### How to work it, and what NOT to conclude

**A shared surname is not a relationship.** `Børsheim` is a Norwegian farm name — a
toponym that many unrelated families took — so surname alone is the weakest possible
evidence and the mother's side is weaker still by her own framing. The corpus already
holds the Norwegian material; the question is whether a candidate joins it **through a
named ancestor**, not whether they reach it at all.

This is the same rule the order.life sibling repo learned the hard way and it applies
here unchanged: *"reaches the tree: True" is not a result.* Name the people the line
passes through, or say the line is not found.

**Two questions are for Emma and must not be guessed:** whether a candidate really is a
relative, and whether to record living people in the tree at all. Report the evidence and
let her rule.
