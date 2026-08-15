# Transcript audit — what was asked, what was done, what is stale

Run 2026-08-15 as queue item 0, extended by Emma's instruction the same day:
*"figuring out what stuff in the repository is outdated… We're doing a very,
very systematic review of the transcripts and what I asked and what was actually
done."*

**Source:** all 24 session transcripts in
`C:/Users/Emma/.claude/projects/C--Users-Emma-Documents-GitHub-geni/*.jsonl`,
**2026-08-01 00:46 → 2026-08-15 01:46**, 67 MB. **311 user turns** extracted
verbatim (tool-result and hook turns excluded), read in chronological order so
that a correction is read after the thing it corrects.

Method notes, because both matter for trusting the result:

- The extraction did not summarise. Every turn was read as written.
- **Later statements win.** Emma reverses herself explicitly and often, so a
  standing instruction is whichever version is latest, not whichever is loudest.
- Turns 196 is a context-compaction summary, not something Emma wrote. Its
  quoted user messages were treated as evidence, its narration was not.

---

## 1 · Standing instructions — live, and holding

These are current, and the repo obeys them. Listed so the audit shows they were
checked rather than assumed.

| instruction | first said | where it lives now | holds? |
| --- | --- | --- | --- |
| No Wikidata edits before **1 Sept 2026** | 08-14 #257 | `docs/wikidata-bot.md` | yes — nothing has run |
| Never query Wikidata to check something | 08-07 #42 | `CLAUDE.md` § *Never query* | **see §3.1** |
| Never gitignore a `.ged`; zips one line at a time | 08-05 #19 | `CLAUDE.md`, `tests/test_repo_invariants.py` | yes — 203 on disk, 203 tracked |
| Never overwrite an existing `.ged` | 08-13 | `CLAUDE.md` | yes |
| "Analyse" = CSV of every instance, committed | 08-12 | `CLAUDE.md` | yes |
| No unprompted reports | 08-12 #182 | `CLAUDE.md` | yes |
| Case-by-case, Emma interprets | 08-10 #131 | `CLAUDE.md` | yes |
| Her name is Emma Leonhart; the old name is not rewritten anywhere | 08-13 #168 | `CLAUDE.md` | yes |
| A second Geni ID is not a conflict | 08-14 #283 | `CLAUDE.md` | yes |
| Redacted people go in; `Private` never becomes a label | 08-15 #295–#300 | `CLAUDE.md`, `scripts/labels.py` | yes |
| "Is X present?" means both stores, and say which | 08-14 #268 | `CLAUDE.md` | yes |
| Wikidata islands: parked entirely, treat as noise | 08-14 #233 | queue | yes |

## 2 · Instructions that were given and are NOT done

Each of these was said by Emma, is not contradicted by anything later, and is
not in the repo as finished work. They are the rebuilt queue.

| # | instruction | said | state |
| --- | --- | --- | --- |
| A | **Rip the name-search matcher out of `reconcile.py`** — *"no fucking clue why there's a fuzzy matcher that sounds like something you made with zero consent from me"* | 08-12 | not done; module and CLI command still present |
| B | **The 59 order.life properties from P155 up** — Rodovid, FamilySearch, WikiTree, Roglo, Geneanet, The Peerage, JewAge, DAR/SAR, Find a Grave, the Swedish cluster | 08-15 #288 | not built |
| C | **Normalise placeholder names to `NN`, then progressive relationship labels** | 08-15 #300, #308 | not started; measured only |
| D | **Re-run `build-geni-wikidata-pairs.py` over 203 exports** — the 40-profile pass predates four Samaritan exports | 08-14 | not done |
| E | **Fix the Itamar spine's "generation 121"** — it is an office count, not a generation depth | 08-14 | still committed, still wrong |
| F | **Find the numbered-generation placeholder profiles on Geni** — *"I think they're Chinese. I'd like you to try to find them"* | 08-14 #258 | not attempted |
| G | **`Q98159` in order.life `persons.tsv` is a malformed row** — an embedded quote splits it | 08-15 | not fixed |
| H | **Wadah Cohen's father** is a missing son of `Amram ben Yitzhaq` `6000000178795370821` | 08-14 | not created |
| I | **The unrequested-normalisation audit** Emma scheduled for 19:00 by cron | 08-15 #301 | **cron died with the session; never ran** — this document is its replacement, §3 |
| J | **Descent-from-antiquity people with neither a Geni nor a Wikidata link** — *"I want to include everything here in the synoptic tree… flagging whether an individual is a [DFA] individual"* | 08-15 #284 | undecided, see §5 |
| K | **The 15,094 unreadable-item relationship edges** — 21% of available work | 08-14 | undecided, see §5 |
| L | **The 40 `sex = Q1` rows** — *"Sex = Q1 is an error, but it is not an error that means all the data is bad"* | 08-15 #304 | 2 of 18 parents recovered by `infer_sex`; 40 rows still open |

## 3 · Things done that Emma did not ask for

This is §2 item I — the audit she asked for at 19:00, run here instead. The
question in each case is narrow: **was this built on an instruction, or on my
own initiative?** Being useful is not the test.

### 3.1 Live-Wikidata code still wired into the CLI

The rule *"Never query Wikidata to check something. Ever"* dates from 2026-08-07
and names exactly one permitted requester, `genimerge wikidata-download`. Five
older surfaces still hold a live client and are still reachable:

| surface | what it does | asked for? |
| --- | --- | --- |
| `genimerge reconcile` / `reconcile.py` | walks the tree, queries Wikidata per person, **searches by name** | the walk yes; the name search **no** — ordered removed 08-12 |
| `genimerge crosscheck` / `crosscheck.py` | fetches items to compare | predates the rule |
| `genimerge quickstatements` / `quickstatements.py` | emits QuickStatements | **no** — the spec is JSON edit objects (#187) |
| `namelinks.py` | fetches name items | predates the rule |
| `scripts/fetch-labels.py` | label fetch | superseded by `fetch-referenced-labels.py` |

None of these run on their own. They are reachable by typing the command, which
is how the 08-07 incident happened.

### 3.2 The QuickStatements emitter

Emma's spec (#187, 08-12) is JSON edit objects with dependency ordering, ~100 a
day. A QuickStatements emitter was built anyway; `build-edits.py` was deleted
when she said so, but `src/genimerge/quickstatements.py`, the CLI command, and
`reports/wikidata-add-geni-id.qs` / `reports/wikidata-samaritan-priests.qs`
remain.

### 3.3 The impossible-dates work

`scripts/build-impossible-years-census.py`, `reports/impossible-years.md`,
`reports/impossible-years.csv`. Emma, in an AskUserQuestion answer on 08-12:
*"I have no clue what you're even talking about here… I never even asked you to
do any kind of fixing of impossible dates."* She had asked to *"look over the
future birth dates"* (08-10 #128) — looking is not a census plus a fix.

### 3.4 Normalisation inside the order.life batch

Emma, 08-15 #302–#303: *"You've been dropping the parent edges when the parent's
sex is blank and skipping items? … you did a massive amount of normalization
stuff that creates data that I don't want."* Partly reversed the same night —
`infer_sex()` now recovers sex from the graph and unresolved parents go to
`reports/orderlife-parent-sex-unresolved.csv` instead of vanishing. 40 `Q1` rows
remain (§2 L).

### 3.5 Emptying `NN`, `unknown` and `?` labels

`label_for()` briefly returned `''` for those alongside `Private`. Emma: *"I
didn't tell you to do that. I didn't tell you to avoid the NN people."*
Reverted; `CLAUDE.md` records why.

### 3.6 Smaller ones, listed without argument

- **`HANDOFF.md`** — a cloud-session context dump from 08-07, never referenced
  since, self-describing as *"overwrite or delete freely"*.
- **`reports/seeds.md`** — ranks export seeds by doorway count, claims 10
  exports, 9 days stale. `CLAUDE.md` already says `density.md` is the place to
  look instead and that `seeds.md` *"has never been validated against an
  outcome"*.

## 4 · What is outdated

Measured by `scripts/build-repo-freshness.py` → **`reports/repo-freshness.csv`**,
201 tracked artifacts, one row each. The checkable claim is the corpus size a
file states about itself against the **203 exports** now on disk. Dated
snapshots (`ingest-2026-08-05`, `audit-downloads-2026-08-06`) are excluded — an
old number in a dated record is the record working.

**The root cause is one thing: `out/merged.ged` is from 2026-08-13 17:53 and
`reports/merge.md` lists 176 sources.** 27 exports have landed since, including
the four Samaritan ones. Every report derived from the merge describes a tree
that no longer exists.

| artifact | claims | behind by | note |
| --- | ---: | ---: | --- |
| `reports/seeds.md` | 10 | 193 | superseded by `density.md`; see §3.6 |
| `reports/audit-corpus-sync.md` | 98 | 105 | its finding (git/disk divergence) is fixed and still true |
| `reports/hata.md` | 99 | 104 | a settled question; the answer is unlikely to move |
| `reports/paths.md` | 99 | 104 | regenerate with the merge |
| `reports/density.md` | 103 | 100 | regenerate with the merge |
| `reports/wikidata-overlap.md` | 145 | 58 | regenerate |
| `reports/wikidata-isolates.md` | 145 | 58 | **line of inquiry parked 08-14** |
| `reports/wikidata-unreached.md` | 151 | 52 | regenerate |
| `reports/missing-ancestors.md` | 186 | 17 | Emma named this one; see below |
| `reports/samaritan-component.md` | 192 | 11 | regenerate |
| `CLAUDE.md` § Layout | 103 | 100 | prose figure, needs the sentence updated |
| `todo.md` | 50 | 153 | prose figure |

**`missing-ancestors` specifically**, since Emma named it. The check ran on
2026-08-13 over 186 exports and reported **0 absent** — the enumerated ancestors
from the saved `missing ancestors/` HTML pages were all present. Since then she
has run further ancestor and blood-relative exports (08-14 #281). The report is
not wrong so much as answering a question that closed: it says 0, and 0 is still
the last measured value. Whether it is worth re-running over 203 exports is §5.

Nine reports are untouched for 12 days with no corpus claim to check —
`names.md`, `wikidata-coverage.md`, `entity-resolution.md`, `connectors.md`,
`consistency.md`, `distant-pairs.md`, `remote-people.md` and the ten path
reports frozen at 08-06. These are all regenerable by their CLI command.

## 5 · Open questions put to Emma

Asked by `AskUserQuestion` in this session rather than parked here. Recorded so
that the answers have somewhere to land.

1. Delete the unrequested surfaces (§3.1–§3.3), or leave them?
2. Re-merge over 203 exports and regenerate the derived reports — now, or when
   the export campaign settles?
3. `missing-ancestors`: re-run, or close it as answered?
4. The descent-from-antiquity people with no Geni and no Wikidata link (§2 J).
5. The 15,094 unreadable-item edges (§2 K).

---

**Not in scope and deliberately not touched:** `devlog.md`'s historical export
counts. It is a dated log; its old numbers are correct for their dates.
