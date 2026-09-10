# Synoptic

## What this project is

**A campaign to connect every `P2600` person on Wikidata into one comprehensive family tree,
using Geni exports as the material.** Wikidata is often the better genealogy source; Geni is the
better *reach*. Joined, one can connect people the other leaves stranded.

**The repo generates QuickStatements every day through CI/CD**, and those go to Wikidata, where
they are expanded. It is moving towards automated edits rather than pasted batches.

**The synoptic tree is the thing everything runs on.** It has two meanings and both are in use:

* **the Geni union** — every `.ged` under `exports/` merged into one tree, `out/merged.ged`.
  *"Rebuild the synoptic tree"* always means this.
* **the full union** — that tree joined to Wikidata, which is what the campaign actually needs
  and **does not exist yet**.

It is keyed on the Geni profile ID throughout, so merging is an exact join and never a name
match. It is **slimmed**: anything not feeding the pipeline that ends at Wikidata is dropped on
input, which is what made it buildable in Actions at all.

## Where the pipeline is pointed right now

**At the Bure kinship in Sweden and the surrounding Scandinavian genealogy.** That is deliberate
and narrow. **On 2027-01-01 it broadens**, driven by
`exports/post-merge/wikidata-qid-links.ged` — the file of Wikidata identifications that turns
into entry points on that date.

## What is left

* **The Geni exports are mostly done.** A few are still running. They are **commanded rather
  than routine and they are a bit iffy** — run because those individuals were judged important,
  not because a rule selected them.
* **The descendant-gathering campaign.** Comprehensively export the descendants of named
  individuals, because **the descendants of these people are poorly documented on Geni and other
  sites and tend to be removed abruptly** — so gathering them is time-sensitive, and
  representing them on Wikidata is the point. `queue.md` holds the roster and the order.
* **The `P2600` connection campaign** — every holder either connected to Charlemagne or confirmed
  impossible. 518,889 holders, 266,201 currently disconnected.

**The first descendants target is the Cyprus person — Abul Hamza `6000000227676734863`** — and
the specific interest is **finding descendants of hers living in Scandinavia**, because those
would link into the people the tree already revolves around. Her Ancestors, Descendants and
Forest exports are down; the descendants ball came back **at the cap**, so the gathering has
barely started. `queue.md` holds the rest of the roster and its order.

## Not yet — the Wikidata update

**Updating the Wikidata side properly is wanted, and it is not time.** It waits; the pipeline has
to get further first. Do not start it, and do not treat its absence as a gap to close.

## ⛔ The practical barrier: the zipper merge

**The zipper merge is supposed to do entity resolution between Wikidata and Geni at scale** —
assigning QIDs to people, so the synoptic tree knows who is who. **It is not doing that well, and
the pipeline is effectively manual as a result.** That is an error caused by other
complications, **not the intended long-term shape**. The intent is zipper merging doing the
resolution over very large amounts of both sides, which is also what makes the tree efficient:
the more people are identified with each other, the less duplication there is to carry.

Treat manual adjudication as a stopgap. → [corpus-and-tree](docs/rules/corpus-and-tree.md)

---

**Below this line is RULES ONLY.** Every rule links to the page carrying its evidence — the
measurement that established it, the failure that caused it, the counts it operates at. Cut from
5,548 lines on 2026-09-09; nothing was deleted, it was moved. If a rule looks arbitrary, the page
says why, and § *the stupider and more specific the instruction* applies.

| page | what it holds |
| --- | --- |
| [`docs/rules/names.md`](docs/rules/names.md) | names, labels, patronymics, CJK, transliteration |
| [`docs/rules/wikidata-editing.md`](docs/rules/wikidata-editing.md) | what goes out, caps, properties, entry points, decks |
| [`docs/rules/corpus-and-tree.md`](docs/rules/corpus-and-tree.md) | exports, the merge, the zipper, dates |
| [`docs/rules/working-here.md`](docs/rules/working-here.md) | process, asking, blockers, reporting |
| [`docs/rules/collector-and-browser.md`](docs/rules/collector-and-browser.md) | the collector, Geni, Chrome |
| [`docs/rules/ci-and-pipeline.md`](docs/rules/ci-and-pipeline.md) | CI, the pipeline, the published site |
| [`docs/algorithms.md`](docs/algorithms.md) | the daily / edit / tail algorithm specifications |
| [`docs/unconnected-worklist.md`](docs/unconnected-worklist.md) | the unconnected-`P2600` worklist spec |

`queue.md` is the work. `devlog.md` is what happened. `name modelling.txt` is the authority on
how a name is modelled and beats anything here.

---

## Skills

`.claude/skills/` — `emergency-stop`, `cron-is-local`, `autonomous-loop`,
`queue-driven-workflow`, `writing-style`, `cleanvibe-update-check`. Vendored, kept current by
the last of them. Last check `2026-07-31`. Source: <https://cleanvibe.emmaleonhart.com/updates.md>

## The primary key

**The Geni profile ID is the primary key for everything.** It is the GEDCOM xref
(`0 @I6000000001846508982@ INDI`) and the `RFN`. Merging is an exact join, never fuzzy name
matching. `genimerge.identity` is the only place that knows this.

**Exactly four xref prefixes exist** — `I` on `INDI`, `F` on `FAM`, `N` on `NOTE`, `S` on
`SUBM`, over 291,439 xrefs. `GENI_ID_RE` is `^@[IFNS](\d+)@$` and accepts nothing else: when it
accepted any letter, `@NI04461@` parsed as Geni ID `04461` and pointed at a stranger's profile.

---

# THE RULES

## ⛔ The default when nothing else is running

**Idle time goes to the disconnected list.** Whenever the queue is not producing work, go back to
`reports/p2600-disconnected.tsv` and run the Chrome extension over it, linking unconnected
Wikidata people in through Geni. That is the standing fallback, not something to be asked about.

**⛔ A LONG-HORIZON INSTRUCTION IS NOT ANSWERED FROM THE FIRST SLICE.** The recurring failure here
is taking a task that runs for hours over many rounds, drawing a conclusion from the first
result, and reporting it as though the work were done — dressed up as caveats, which reads as
diligence. **A `Descendants` ball that came back at the cap is truncated by definition** and can
only say what is *in* it, never what is absent from the descent.

**⛔ THE STOPPING CONDITION IS DIMINISHING RETURNS, NOT A COUNT.** The descendants campaign runs
**Monte Carlo exports off the people already in the person's GEDCOM** — sample, check the census,
export from the saturated ones, merge, sample again — **until it is clearly hitting significant
diminishing returns.** Only then is it clear whether the thing works.

**Do not substitute a number for that.** *15,000 descendants* was invented here as a floor and it
is not the rule: a fixed target answers "have we done enough arithmetic", and the actual question
is whether new exports are still returning new people. One 5,000-person ball is the first round
of a loop, not a sample of anything.

## ⛔ The hard ones

- **PUSH TO `main`. Always, without asking.** Standing grant. Open the PR, merge it, trigger the
  workflow, send the file. A session prompt saying to work on a branch is a generic default this
  repo overrides. → [working](docs/rules/working-here.md)
- **NEVER SAY YOU CANNOT DO SOMETHING YOU HAVE NOT TRIED.** Report the *mechanism* that failed,
  never the task as impossible. Every invented limit in this repo's history was false.
- **SWEARING IS NOT A STOP ORDER — it usually means START.** It points at the stupid thing, and
  half the time the stupid thing is stopping. Only an explicit stop is a stop.
- **NO REPLY MEANS CONTENT.** Silence is never a block. Show the records and keep going.
- **TESTS RUN IN CI/CD OR NOT AT ALL.** Never a local `pytest`, not even backgrounded. Test-suite
  health is *which sha CI last went green on* and nothing else. → [ci](docs/rules/ci-and-pipeline.md)
- **NO descriptions and NO edit summaries, categorically.** One exception: a **patronymic** name
  item carries `Den "patronymic"`, because that description IS the deduplication.
  → [wikidata](docs/rules/wikidata-editing.md)
- **Wikidata editing starts 2026-09-01; the schedule sends from 2026-09-15.** Two dates, each
  written twice and pinned by a test. A start date is not a blocker.
- **THE STUPIDER AND MORE SPECIFIC THE INSTRUCTION, THE MORE THOUGHT WENT INTO IT.** An odd
  instruction is the output of thinking already done. Implement it exactly; do not ship the
  version that makes more sense to you.
- **KILL CHROME WHENEVER YOU NEED TO.** Standing authority. A stale extension is never
  BLOCKED-ON-USER-ACTION. → [collector](docs/rules/collector-and-browser.md)
- **NO PLAYWRIGHT, NO HEADLESS.** The agentic navigation is overhead paid to keep Geni's traffic
  acceptable, not a design to improve on.
- **THE DOCUMENTATION DOES NOT REFER TO THE ACCOUNT OWNER** — not in the third person, not in the
  second. State rules impersonally. **A blind regex pass is banned**: it turned `Emma Watson`
  into `you Watson` and shipped. A woman in the tree is still `she`.

## Working

- **Only `AskUserQuestion` gets answered.** A question in prose was not asked. Every option must
  be one that can actually be picked, and **the axis is part of the question** — four options on
  one wrong premise is one option.
- **If the instruction is ambiguous, ASK.** But **while working the queue, GUESS and record it**:
  ambiguity *inside* a specified item is guessed, ambiguity about *which thing is meant* is asked.
- **"Add it to the end of the queue" means WRITE IT DOWN AND STOP.** No investigation, no
  questions, no gathering evidence first.
- **Every two hours, put the blockers up as an `AskUserQuestion`** — 10, 12, 14, 16, 18, 20, 22,
  00. Each must offer the non-blocker reading, because that is usually the true one.
- **Not-done taxonomy**, exactly one tag, blocker named specifically: NEEDS-DECISION,
  BLOCKED-ON-USER-ACTION, BLOCKED-ON-EXTERNAL, NEEDS-INVESTIGATION, UNSAFE-TO-GUESS,
  OUT-OF-SCOPE. **If it fits none with a named blocker, it is not deferred — DO IT NOW.**
- **A long series of commands runs in STRICT ORDER**, even where the order looks inefficient.
- **No unprompted reports.** Write the thing asked for and stop.
- **"Analyse this" means: build a CSV of every instance, commit it, then analyse that** — not a
  sample, not the top 100.
- **CHECK before raising an alarm.** Run the check that would falsify it first.
- **Queue items are BULLET POINTS, never numbered.** A number is a promise it will still be there.
- **A cron only fires while the session is idle.** Never schedule a long job into active work.
- **A ten-minute ceiling is not a wall — background it.** Never hand a long job back.
- **Code that is WRITTEN but never CALLED is not done.** Wire it, then measure from the wired path.
- **LEGACY CODE IS DELETED.** The test is *does the pipeline read this*, not *might this be useful*.
- **Do not grab the first artifact that vaguely matches.** Find the one that is meant.
- **Incomplete earlier work is not the thing being described.** Its errors describe where it
  stopped, not a defect in a finished mechanism.
- **A shortcut taken to unblock a session is not a law to enforce back.** Automate it instead.
- **Duplication is deliberate here.** Never "fix" it. The thing to control is repetition in front
  of one reader.
- **SORTING MUST BE DETERMINISTIC** — total key, same bytes out for the same inputs. `casefold`
  alone is not a total order.
- **Windows:** commit with `git commit -F <file>`; never round-trip UTF-8 through
  `Get-Content`/`Set-Content`.

## The corpus and the tree → [corpus-and-tree](docs/rules/corpus-and-tree.md)

- **`exports/` is the corpus, read recursively. There is no ingest step.** Every `.ged` is
  committed; **never gitignore a `.ged`**, and never write a `*.ged` or `*.zip` pattern.
- **Never overwrite an existing `.ged`.** A new export is always a new file. If the path exists,
  STOP. The one exception is a byte-identical duplicate.
- **`exports/excluded/` is the one part that is not corpus** — for when Geni has *deleted a
  relationship* a merged export still asserts. Checked now, never predicted.
- **Later sources win value conflicts.** Geni is live; the newer export holds the correction.
- **The seed is the file's first `INDI`**, and an export is named for its style, so disambiguate
  with the seed id.
- **`GENI_EXPORT_CAP` is 5000** — largest seen, not a cap Geni enforces. Do not encode arithmetic.
- **A small component is IGNORED.** Not reported, not analysed.
- **The question is whether OUR TREE MATCHES GENI, never whether Geni is right.** If Geni holds
  two profiles, we hold two — even when two is wrong.
- **GREP THE CORPUS BEFORE RUNNING AN EXPORT**, every time, and put the number in the commit.
- **The job with an export is to integrate it, not to analyse it.**
- **"Is X present?" means BOTH stores.** Answer for each, name which, and say when the absence is
  bounded. Join on the Geni ID; never search by name.
- **`reports/derived-family.csv` separates with ` | `, spaces included.** Splitting it wrong made
  379,251 people arrive childless and published a distribution that looked clean.
- **GEDCOM dates have a specification** — `genimerge.dates`, never a regex. A hand-rolled parser
  drops what it does not understand silently.
- **`reports/density.md`, not `reports/seeds.md`**, is where the next export comes from.
- **The `Descendants` campaign is about TIME, not thinness** — a ball reaches ~12 generations, so
  seed where you want to arrive. Two seed-choosing methods are refuted; do not propose a third on
  reasoning alone.
- **The zipper's one name exception lives inside a slot**: solo, then date, then name — and
  **1600–1900 is the band where names lie and years decide** (71% of confirmed pairs spell the
  name differently).
- **The four big derived CSVs are committed gzipped.** `pack-derived.py --unpack` on a clean clone.

## Names → [names](docs/rules/names.md)

- **`name modelling.txt` is the authority and beats this file.** A patronymic is `P5056`, parallel
  to `P735`/`P734`, with `P144` pointing at the **father, the person**.
- **PARSE PATRONYMICS BY FORM. Never parse a name positionally.** Positional parsing is the
  ultimate cause of most name defects here. Both `GIVN` and `SURN` are checked.
- **A TITLE IS NOT A NAME** — Geni already said so in `NSFX`. Drop titles, keep ordinals.
- **A DESCRIPTION MARKER COMES OUT OF THE LABEL**; a title stays in it. A title is a thing the
  person was; a marker is an annotation about the record.
- **A NAME FIELD THAT NAMES A RELATIVE IS NOT A NAME** — Geni puts the husband in `GIVN`.
- **A GUARD IN ONE EMITTER IS NOT A GUARD.** There are two emitters; rules live in `namemodel`.
- **No given name is not no name** — a redacted person's surname is still a `P734`.
- **The MARRIED name is the real name.** `mul` carries it, birth name as `Amul`, **never an `Aen`**.
- **`NN` is PRESERVED in `mul`**; descriptive labels are ADDED in other languages. `Private` never
  becomes a label, and neither person is left unlabelled.
- **A bare given name is not a label** — the farm name is the surname; else `Given NN`.
- **Redacted people go in.** `<private> /Surname/` keeps a real surname.
- **The gate is `ja` + `zh` + `ko`. CJK INCLUDES KOREAN.** All three readings are produced for
  everyone; culture only picks which is promoted to `mul`.
- **A title inside a label takes the NATIVE form in CJK**, never a transliteration. An unknown
  place or title is DROPPED, never transliterated.
- **Transliterate the English reading.** Faithfulness to the source language destroys more than it
  saves. Every rule change is scored against the attested column.
- **One name item per USAGE, not per string.** A token that is both a surname and a given name
  gets both objects. A diacritic makes a different name.
- **Write a Han range as ASCII `\uXXXX` escapes** — the literal form ate the Hangul block and cost
  5,338 Korean people.
- **A generation suffix goes LAST; a regnal ordinal stays put.** It is a fact about the person,
  not about one name string, and it must not reach an item somebody else labelled.
- **Wikidata's label beats ours.** An existing `mul` is not ours to overwrite.
- **A middle initial keeps its Latin letter in every language.** A bare lowercase letter is a word.

## Editing Wikidata → [wikidata-editing](docs/rules/wikidata-editing.md)

- **The purpose is to ADD, not to correct.** 24,957 addable statements against 930 conflicts. A
  conflict is emitted beside what is there, cited to Geni, and never routed to anyone for a ruling.
- **A statement goes in only if BOTH ends already have a QID.** That is an invariant that makes
  the sequence converge, not a wall. **The batches are a SEQUENCE**: what cannot run today is
  tomorrow's batch. `LAST` IS valid as a value; only two items created in one batch cannot point
  at each other.
- **The ledger refresh is PART OF THE RUN.** Regenerating QuickStatements always regenerates the
  ledger; it almost never rebuilds the tree.
- **Caps:** `P3373` **40 pairs/day**, `NAME_ADD_CAP` **60 people**, `P2600_LEAD_CAP` **40**,
  `MANUAL_P2600_PER_RUN` **20**, `LABEL_EDIT_CAP` **60**. `P22`/`P25`/`P40`/`P26` are uncapped.
- **A sibling step gets a placeholder parent in OUR TREE and never on Wikidata** — Wikidata has
  `P3373` and needs no invented parent.
- **A second Geni ID on one item is NOT a conflict**, and a duplicate parent value is
  self-healing. Do not report or fix either.
- **The seed set is the Wikidata subgraph from Arne** — no hop counts, a billion hops if that is
  what it takes. The subgraph gates **creations** only; filling in existing items is ledger-wide.
- **A BLOC IS A ROSTER REFERENCE, never pasted ids.** Entry points drip in on a date column, not
  a cron; the roster stays at about 250.
- **A SUMMARY of a Wikidata item is not the item.** Download the full JSON; a summariser gets
  absence wrong. **Querying Wikidata is allowed** — be polite about the rate.
- **The tree and the items are edited BY HAND, continuously.** Re-download before any correction
  and say when it was verified.
- **Always write the English label next to a property or item ID.** Never guess an ID.
- **Regenerate a review deck before handing it over**, never the committed copy. A CJK card is not
  in the deck.

## The collector and Geni → [collector-and-browser](docs/rules/collector-and-browser.md)

- **⛔ BOTH TIES, ALWAYS** — a blood chain AND a marriage chain to Charlemagne, plus the immediate
  family. **The redundancy is the point.** Both searches on every person; a blood miss with no
  path is not done; **do not backfill in-law onto people who already have a blood path**.
- **Anything odd about a person → `Forest` export.** Stop investigating.
- **The agent navigates and nothing else.** Every decision is inside the extension.
- **Progress is DERIVED, never stored.** No list is hand-edited.
- **An empty browser list is not a blocker.**
- **Grab the RESIDUALS** — keep what an extraction drops.
- **One export at a time is Geni's limit**, and a submitted export cannot be cancelled.

## CI and the pipeline → [ci-and-pipeline](docs/rules/ci-and-pipeline.md)

- **The repo is public; CI runs on a schedule, on dispatch and on PRs.** Only `pipeline.yml` runs
  on push, and a burst of pushes does not queue — the pending run is cancelled.
- **Pages is built from the sha the pipeline PUSHED**, not the one that triggered it.
- **A page whose generator no workflow runs is published as a photograph.**
- **The synoptic tree BUILDS in Actions**, slimmed. ~6.07 GB per million people.

---

## Live corrections, 2026-09-09

- **The campaign is every `P2600` holder disconnected from Charlemagne** in the union of our
  exports and Wikidata — connected, or confirmed impossible. 518,889 holders, 266,201
  disconnected. → [unconnected-worklist](docs/unconnected-worklist.md)
- **The old *183,674 isolates are LOW PRIORITY* rule is DELETED**, and not only because it
  governed 67% of that population. **The operating conditions changed underneath it**: it was
  written when finding those people was manual labour, and browser automation has turned that
  into something routine. A rule whose whole argument was cost does not survive the cost changing.
- **The Geni trimming is not finished.** The slim keeps ~73% of corpus bytes; a
  connectivity-only tree — `RFN`, `SEX`, `FAMC`, `FAMS`, `HUSB`, `WIFE`, `CHIL` — is ~19%.
  Names, dates, places and titles are still carried and the Wikidata pipeline does not read them
  to answer *is this person connected*.
- **The Wikidata tree does NOT yet go into the synoptic tree.** `scripts/build-wikidata-gedcom.py`
  renders it as a mergeable GEDCOM; nothing wires it into CI yet, and it must not be wired in
  until it fits.
- **Nameless routing nodes are the design.** A QID-only person exists so a Geni person can reach
  Charlemagne through Wikidata's structure; a router does not need a name.
