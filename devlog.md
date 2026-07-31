# geni — Devlog

**This file is where "done" lives.** `queue.md` is delete-only: when a queue
item is finished, the item is **deleted from `queue.md`** and a dated entry
is **appended here**, in the same commit as the work, then pushed. Never
tick a box in place — a checked box left in `queue.md` is the failure mode
this file exists to prevent.

Also record releases (tag + a one-line note), notable milestones, and
anything else worth a chronological trail. Newest entries at the bottom.

This is the **same convention as the cleanvibe repo's own `devlog.md`** —
every cleanvibe-scaffolded project gets one for the same reason.

See `CLAUDE.md` § "Workflow Rules" and `queue.md`'s preamble.

---

## 2026-07-30 — cleanvibe onboarding started

Onboarded with `cleanvibe clone` (cleanvibe v1.17.0). This is an
**existing repository**, so the very first onboarding task is to **backfill
the rest of this devlog from `git log`** (tagged releases, milestone
commits, merged feature branches). After that, every finished queue item
appends a new dated entry here.

Backfill from `git log` is two commits long and holds no releases or
feature branches: `31e2b19` (the user's dropped Geni export archives) and
`eebb9c2` (the cleanvibe v1.17.0 scaffold). Nothing further to recover.

## 2026-07-30 — data lake triage, and the real plan

Five zip archives at the repo root turned out to be three distinct GEDCOM
exports plus two byte-identical duplicates (SHA-256 confirmed):
`export-geni.zip` == `export-geni (1).zip`, `export-geni2.zip` ==
`export-geni (2).zip`. Extracted the three distinct files into
`data_lake/`, moved all five archives in alongside them, and added `*.zip`
to `.gitignore` — the extracted GEDCOMs are what git tracks.

| file | size | INDI | FAM |
| --- | ---: | ---: | ---: |
| `export-Ancestors.ged` | 16.3 MB | 3836 | 2281 |
| `export-Forest.ged` | 4.2 MB | 3836 | 2020 |
| `export-BloodTree.ged` | 4.0 MB | 3836 | 1054 |

The load-bearing find: **Geni writes the profile ID as the GEDCOM xref
itself** — `0 @I6000000087535357291@ INDI` — and repeats it as `1 RFN
geni:6000000087535357291`. So the merge has a real primary key across all
three exports and does not need name/date fuzzy matching to unify them.
All three report exactly 3836 individuals, which the inventory step has to
confirm is the *same* 3836 rather than a coincidence of size.

Also confirmed the Wikidata property for the Geni profile ID: **P2600**.

Wrote `todo.md` (seven long-horizon items, from the canonical merge through
Wikidata authoring and name-item creation) and replaced the cleanvibe
bootstrap queue in `queue.md` with the real thirteen-item work queue,
mirrored into the task tool.

## 2026-07-30 — three-cron playbook running

Started the three session-local crons: work-loop `a58ec58b` at :03,
auto-flush `680ee058` at :15, status-report `9f6681e1` at :42. They are
`durable: false`, so they die with this session and are recreated at the
start of the next one; they also auto-expire after 7 days.

## 2026-07-30 — `genimerge` package skeleton

`src/genimerge/` behind a src-layout `pyproject.toml`, `tests/` on
`pytest` (`pythonpath = ["src"]`, so no install step is needed to run
them), and `.gitattributes` normalising line endings to LF while marking
`*.ged` binary so the exports we were given are never rewritten.

The package is **stdlib-only on purpose**. `urllib` is enough for the
Wikidata SPARQL endpoint, and a zero-dependency package keeps CI and cold
clones trivial. `pytest`: 1 passed.

## 2026-07-30 — GEDCOM reader/writer

`genimerge/gedcom.py`: a streaming GEDCOM 5.5.1 parser that folds `CONC`
and `CONT` away on read and re-creates them on write, so callers deal in
whole values and never in line wrapping. Malformed lines land on
`Gedcom.warnings` instead of raising, and a level that jumps past its
parent is clamped rather than dropped — a real export is not a
conformance test, and refusing to read a 16 MB file over one odd line
would be useless.

All three exports parse with **zero warnings**, which was not a given.
Record counts:

| file | INDI | FAM | NOTE | SUBM |
| --- | ---: | ---: | ---: | ---: |
| `export-Ancestors.ged` | 3836 | 2281 | 1026 | 578 |
| `export-Forest.ged` | 3836 | 2020 | 8 | 395 |
| `export-BloodTree.ged` | 3836 | 1054 | 6 | 398 |

**One real bug, found by the round trip and not by the unit tests.**
Round-tripping Ancestors was not a fixpoint: one `INDI` note came back
different. The cause was `parse()` splitting input with
`str.splitlines()`, which breaks on `\v`, `\f`, `\x1c`–`\x1e`, `\x85`,
`U+2028` and `U+2029` in addition to `\n` — while `parse_file()`, reading
with `newline=""`, breaks only on `\n`. The Ancestors export carries a
literal **U+2028 inside five note values**, so the two entry points
disagreed on exactly those records and the round trip silently rewrote
them. `parse()` now splits on `\n` alone. The regression test spells the
character as an escape rather than embedding it, because a bare U+2028 in
source is exactly the kind of thing an editor quietly normalises away.

`tests/test_gedcom.py` covers the parser on hand-written fixtures;
`tests/test_gedcom_real_exports.py` runs against the actual exports and
asserts the load-bearing invariant — every `INDI` xref is `@I<digits>@`
and `RFN` repeats the same ID — so if Geni ever changes that, the merge
fails loudly instead of quietly mis-keying. `pytest`: 35 passed.

Dropped the `[project.scripts]` entry point from `pyproject.toml`; it
pointed at a `genimerge.cli` that does not exist yet.

## 2026-07-30 — export inventory, and the finding that reframes the project

`genimerge/inventory.py` plus `python -m genimerge inventory` measure the
exports and write `reports/inventory.md`. Also added
`genimerge/identity.py`, the one place that knows a Geni profile ID comes
from the xref and is cross-checked against `RFN` — it raises
`IdentityMismatch` rather than picking a winner, because guessing there
would silently merge the wrong people.

**The exports are capped, and they barely overlap.** All three contain
exactly 3836 individuals, which is not a coincidence — it is Geni
truncating each export. What they contain is mostly *different* people:

| | individuals | families |
| --- | ---: | ---: |
| union of all three | **8766** | **4056** |
| largest single export | 3836 | 2281 |
| present in all three | 354 (4.0%) | 245 (6.0%) |

Pairwise, BloodTree∩Forest is 2300 individuals, Ancestors∩BloodTree is
442, and Ancestors∩Forest is 354. Every family in BloodTree is also in
Forest (1054 of 1054), so BloodTree's families add nothing that Forest
does not already have — its value is in its individuals.

This changes the shape of the work: merging is worth **4930 individuals**
over the best single export, and reaching the whole tree means many more
exports rather than a few. It makes the frontier analysis load-bearing
rather than a nicety. Recorded in `README.md` and `CLAUDE.md`.

The tag vocabulary in the report is the field list the canonical model
will be built from. Worth noting from it: `INDI.NAME` occurs 5498 times
across 3836 people in Ancestors, so **people carry multiple name
records** — directly useful for the multilingual labels the Wikidata work
wants. `_MARNM` (married name) is populated on roughly 80% of people,
`NICK` on 1837, and `OBJE` (photos) on 3520.

`pytest`: 42 passed.

## 2026-07-30 — the merge, and two bugs that only the real data found

`genimerge/merge.py` plus `python -m genimerge merge`. **8766 individuals,
4056 families, 1035 notes, 940 submitters** in `out/merged.ged`, with
**zero conflicts and zero lost lines**.

Identity is exact — same xref, same record — so there is no fuzzy matching
anywhere. The interesting question is when two *child lines* are the same
line, decided per structure path:

- **single-valued paths** (`INDI.BIRT.DATE`, `INDI.SEX`) collapse to one
  node; a disagreement is a recorded `Conflict`, never a silent drop;
- **repeatable paths with a value** (`INDI.NAME`, `FAM.CHIL`) match on
  that value;
- **repeatable paths without one** (`INDI.SOUR`, `INDI.OBJE`), whose
  content is entirely in their children, match on the whole subtree.

Which paths are single-valued is **measured from the inputs** rather than
hardcoded, so an unfamiliar structure is treated as repeatable — the
failure mode that keeps data. Measurement alone is not enough though:
`ALWAYS_REPEATABLE` overrides it for `CHIL`, `FAMS`, `FAMC`, `NAME`,
`NOTE`, `SOUR`, `OBJE`, `ALIA`, `ASSO`, because if some future export
happened to give every family one child, measurement would call `CHIL`
single-valued and start reporting siblings as conflicts.

What each source brought:

| source | new INDI | new FAM | records merged | lines added |
| --- | ---: | ---: | ---: | ---: |
| `export-Ancestors.ged` | 3836 | 2281 | 0 | 0 |
| `export-BloodTree.ged` | 3394 | 809 | 827 | 632 |
| `export-Forest.ged` | 1536 | 966 | 3650 | 333 |

**Bug one — spurious conflicts from collapsing twins.** The first run
reported 8 conflicts. They were not conflicts. Some people carry *two*
`NAME` lines with identical text and different `_MARNM` (married name) —
`@I4366030@` is "Ragnhild Rasmusdatter /Eikeland/" twice, married
Giljabrekken Rage and married Løland. Matching repeatable lines on their
value alone collapsed the pair into one slot, so the second line looked
like a contradiction of the first. Matching now keeps a *list* of
candidates per key and merges into the first compatible one, where
"compatible" means no single-valued descendant contradicts. All 8
conflicts disappeared, because none of them was ever real.

**Bug two — the fix broke idempotency.** First-compatible matching is
greedy, and greedy is unstable: given siblings `NAME{GIVN,_MARNM}` and
`NAME{GIVN,SURN}`, re-merging let the second one's `SURN` be absorbed by
the first, so merging the merged file again changed it.
`@I309752110320008250@` caught it. An identical twin now wins over a
merely compatible one, which makes self-merge a strict no-op: every
incoming child has an exact match in the base, so nothing moves.

Neither bug was reachable from hand-written fixtures. Both came out of
`tests/test_merge_real_exports.py`, which asserts the property that
actually matters — **every (path, value) line of every source survives in
the merged tree** — plus idempotency, referential integrity, and that the
merged file re-parses.

`out/merged.ged` is 20.9 MB and re-parses with zero warnings. The exports
turn out to be referentially closed on family structure: of 14 unresolved
pointers, **0** are `CHIL`/`HUSB`/`WIFE`/`FAMC`/`FAMS` (13 are `INDI.SUBM`,
1 is a note). So dangling pointers are *not* the tree's edge, and the
frontier analysis will have to work from people with no parent family
instead — the merge report says so rather than implying otherwise.

`pytest`: 70 passed.

## 2026-07-30 — the canonical dataset: the GEDCOM stops being the working format

`genimerge/model.py` and `genimerge/dates.py`, behind
`python -m genimerge export`, turn the merged tree into
`out/people.jsonl` (8766) and `out/families.jsonl` (4056). Everything
downstream reads these, not GEDCOM.

Two decisions worth recording:

**Relationships are resolved both ways.** GEDCOM routes every
relationship through a family record — a person points at a family, the
family points at the parents — while Wikidata wants P22/P25/P26/P40
directly between people. `Tree.resolve_relationships` derives the direct
links and keeps the family view too, because the family record is where
a marriage date lives.

**Parsed dates never replace the raw text.** `date_raw` sits next to
`year`/`month`/`day`/`modifier` in every event, so a future statement can
be traced back to what the export actually said. A date the parser cannot
read reports *nothing* structured rather than a guess.

The date parser is small because the corpus is: across 38,605 `DATE`
lines there are only **fifteen** distinct shapes, all standard GEDCOM —
`23 APR 2021`, a bare year, `SEP 1930`, the same three behind
`ABT`/`BEF`/`AFT`, and `BET x AND y`. Modifiers are kept rather than
flattened, since "about 1275" and "1275" are different claims and
Wikidata can express the difference. Two lines read `7  2011` — a day
with no month — and the day is dropped rather than attached to a guessed
month.

Coverage of the merged 8766: **6386** have a father, **5843** a mother,
**6920** a birth year, and all but 10 have a recorded sex (4663 M,
4093 F).

`pytest`: 104 passed.

## 2026-07-30 — Wikidata property set confirmed

Every property and item ID the project will use, checked against live
Wikidata with `wbgetentities` rather than recalled, and written into
`CLAUDE.md` so no later step guesses. Worth the trip: **P1288**, which
looks like it could be a genealogy identifier, is the *Kritisches Lexikon
der Gegenwartsliteratur* ID.

Confirmed: P2600 Geni.com profile ID · P31/Q5 · P21 with Q6581097 male
and Q6581072 female · P22/P25 parents · P26 spouse (P2842 place of
marriage as its qualifier) · P40 child · P3373 sibling · P569/P570 dates
· P19/P20/P119 places · P106 occupation · P97 noble title · P535 Find a
Grave · P735/P734 given and family name, whose values are items of type
Q202444 / Q12308941 / Q11879590 / Q3409032 and Q101352 · P1477 birth name
and P1559 name in native language, both monolingual text.

The GEDCOM date modifiers map cleanly onto qualifiers, which is why the
model kept them: `ABT` becomes P1480 sourcing circumstances = Q5727902
circa, `BEF` becomes P1326 latest date, `AFT` becomes P1319 earliest
date, and `BET x AND y` becomes both bounds.

## 2026-07-30 — reconciled by Geni ID: 209 of 8766

`genimerge/wikidata.py` and `python -m genimerge reconcile` produce
`out/wikidata/matched_p2600.csv`.

**514,567 Wikidata items carry a P2600**, so the join is worth doing —
but pulling all half a million would be rude and slow. The reconciler
instead asks about only the IDs we have, 400 at a time in a `VALUES`
clause: 8766 people became **22 queries**. Every response is cached on
disk keyed by a hash of the query, so re-running a report costs nothing;
deleting `out/wikidata/cache/` is how you force a refresh.

**209 people matched (2.4%)**, all one-to-one — no Geni ID is claimed by
two Wikidata items. The matches are exactly who you would expect: Sverker
I of Sweden, Eric IX, Valdemar I of Denmark, Magnus Barefoot, Bolesław
III Wrymouth, Judith of Flanders. The medieval Scandinavian royalty in
this tree is on Wikidata; the Norwegian farmers are not.

2.4% is the ceiling for *exact-identifier* matching, not for matching.
Plenty of people here plainly have Wikidata items that simply carry no
Geni ID — which is what the name-and-date second pass is for, and what
the "add P2600 to existing items" backlog item exists to fix.

The client takes its `fetch` as a parameter, so all 17 of its tests run
offline: batching, disk caching, cache survival across processes, retry
on 429/503, immediate failure on 4xx, and the deliberate choice to return
a *list* of matches rather than a dict so that one Geni ID claimed by two
items stays visible instead of being silently collapsed.

`pytest`: 121 passed.

## 2026-07-30 — the expansion frontier, and two bugs under it

`genimerge/frontier.py` and `python -m genimerge frontier` write
`reports/frontier.md`. Taken out of queue order deliberately: the
name-search reconciliation pass is a ~25-minute network run, and this
needs no network.

The tree is **one connected component of 8766**, and **2350 people
(26.8%) have no parents recorded**. That is the real edge — not dangling
pointers, since the merged file has none. Generational depth runs to 40,
with a pronounced bulge at 31–37 generations (the medieval royal lines)
and 2351 people at depth 0. The report ranks the parentless by how many
people descend from them, which is the answer to "where should the next
export be taken from": exporting a lone leaf adds a lone leaf.

**Bug one — a phantom component, twice over.** The report first claimed
two components while also claiming nobody was isolated, which cannot both
be true. `Tree.resolve_relationships` kept only the *first* parent family
of a child who is a child in more than one, so the second father listed
the child while the child did not list the father: an asymmetric edge, and
a one-person "component" containing a man named Olof who plainly had a
son. The model now carries `parent_ids` (every parent, for graph work)
alongside `father_id`/`mother_id` (the primary pair, for P22/P25). The
first fix was still wrong — building neighbours from each person's own
`FAMC`/`FAMS` pointers misses a family that lists a person without the
person listing it back — so `family_graph` now walks the *family* records,
which is symmetric by construction. A test covers each of the two ways it
was broken.

**Bug two — 10+ minutes to compute descendants.** Counting descendants by
walking each person's subtree is O(n·m), and descendant sets overlap far
too much to sum from children without double-counting. Each set is now a
bitmask in a Python int, unioned up a cycle-tolerant post-order: exact, no
double-counting, about a kilobyte per person. **2.4 seconds** instead of
never finishing.

Which turned up a genuine defect in the source data: **Halldor Arnesson
is recorded as his own grandfather** — he is Arne's parent and Arne is
his. One person existing under two Geni profiles that were then linked as
parent and child. It is in the report under "People recorded as their own
ancestor" rather than being quietly absorbed, because it is worth fixing
on Geni and it distorts every generational measure.

`pytest`: 167 passed.

## 2026-07-30 — private repo online, CI green

`.github/workflows/ci.yml` runs `pytest` on push and pull request against
Python 3.10 and 3.13. `data_lake/*.ged` is committed, so the integration
tests that read the real exports run in CI rather than skipping — which is
the point, since both merge bugs were found by exactly those tests.

`gh repo create` failed with "Name already exists": the repo had already
been created earlier in this session, at commit `74083e6`, before
`reports/` existed. Rather than assume it was ours, checked it —
**private**, and `origin/main` was a strict ancestor of local `main` with
no commits we did not have — so the push was a plain fast-forward with
nothing to clobber. `74083e6..34db20a`. First CI run: **success**, 47s.

<https://github.com/EmmaLeonhart/geni> (private).

## 2026-07-30 — second-pass reconciliation, and the answer to "as much as possible"

`genimerge/reconcile.py` and `genimerge/coverage.py`, behind
`python -m genimerge expand --search` and `coverage`. The answer, in
`reports/wikidata-coverage.md`:

| | people | share |
| --- | ---: | ---: |
| linked by P2600 (exact) | 209 | 2.4% |
| linked by expansion (structure + name + dates) | 36 | 0.4% |
| **linked, total** | **245** | **2.8%** |
| proposed, awaiting review | 87 | 1.0% |
| neither | 8434 | 96.2% |

The century breakdown is the real answer, and it says the reconciliation
is working rather than failing: **47.7% of people born in the 1000s and
42.7% of those born in the 1100s are linked**, falling to 3% by the
1400s and 0% through the 1600s–1700s. Wikidata's coverage of a family
tree is coverage of its notable members, and this tree's notable members
are medieval. 2.8% overall is not a shortfall — it is what a tree of
mostly Norwegian farmers should score.

**Structural expansion beats name search**, which is why it runs first.
Walking outward from a confirmed match along P22/P25/P26/P40 and
requiring name and date agreement added 36 links over three rings before
going dry. It stops early because most Wikidata relatives of a matched
person *already* carry a P2600 and were matched in pass one.

**The name-search pass was rewritten mid-flight.** The first version
asked the Wikidata search API once per person; the endpoint throttled it
to roughly one request every twenty seconds, so 1127 people would have
taken about five hours. It now matches exact labels and aliases through
the label index instead, hundreds of names per query: **29 requests,
about a minute**. The trade is real and worth stating — exact matching
only finds names written the same way on both sides, where full-text
search tolerated variation. The API path is still there behind
`--api-search` for anyone willing to wait.

**And the confidence scoring was wrong, in a way that mattered.** The
first run produced 92 "high confidence" name matches — including four
separate Wikidata items all offered as *the* match for "Peder Christensen
Trane". This tree is full of Scandinavian patronymics, and "Peder
Christensen" is several different people. Two changes: a name with no
relationship behind it now needs an agreeing date to reach high
confidence, and when one name matches several items that is treated as
evidence the name is not identifying, so all of them are downgraded and
labelled "N Wikidata people share this name". High name-matches fell from
92 to **12** — and those twelve are Faroese chieftains (Øssur
Havgrímsson, Leivur Øssurson), the archbishop Pål Bårdsson, Jon Smør,
and a few modern Norwegians. Nothing from this pass is ever
auto-accepted; it is a reviewable list, not an answer.

`pytest`: 190 passed.

## 2026-07-30 — a reviewable batch of Wikidata edits, and three duplicate profiles

`genimerge/quickstatements.py` and `python -m genimerge quickstatements`
write `out/wikidata/add-p2600.qs` — **33 statements** adding the Geni
profile ID to Wikidata items that describe someone with a Geni profile
and do not say so — plus `add-p2600.md` listing every edit with links to
both sides.

**Nothing is sent to Wikidata.** The batch is a file to read and, if the
user agrees with it, run themselves. Two rules are enforced rather than
assumed: only *structure-confirmed* links are eligible, so no
name-search proposal reaches a batch file however good its score looked;
and the current P2600 of every target item is fetched first.

That second check earned its keep immediately. **Three items already
carry a different Geni ID than the one we matched** — Q101248596 (Haakon
Jonsson Roos), Q3736064 (Sune), Q4988633 (Hafrid Sigtryggsdotter
Boberg). Each means either our match is wrong or **two Geni profiles
exist for one person** and Wikidata points at the other one. Neither is
safe to overwrite, so all three are excluded from the batch and listed
for a human, and they are arguably the most useful thing this run
produced: they are duplicate profiles to merge on Geni.

Adding these IDs pays forward. Once an item carries a P2600, the exact
join finds that person on every future run, so each edit makes the next
reconciliation cheaper than the last.

`pytest`: 199 passed.

## 2026-07-30 — the name vocabulary, measured

`genimerge/names.py` and `python -m genimerge names` write
`reports/names.md`. Promoted from `todo.md` item 5, but only its
**read-only half**: creating name items is a decision for the user, and
this is the measurement that makes that decision informed rather than
blind. Nothing is proposed and nothing is created.

| | distinct | already have a Wikidata name item | share |
| --- | ---: | ---: | ---: |
| surnames (P734) | 1991 | 874 | 43.9% |
| given-name tokens (P735) | 3423 | 1950 | 57.0% |
| whole `GIVN` strings | 6420 | 882 | 13.7% |

So the job, if it is worth doing, is **1117 surnames and 1473 given
names**. The report ranks the missing ones by how many people would gain
a link: `Borsheim` (80 people), `Eriksson` (45), `Orre` (44),
`Sør-Kolnes` (35). 340 people carry no usable name at all.

Two things the data forced:

**Geni's `GIVN` holds a whole given string** — "Ragnhild Rasmusdatter",
not "Ragnhild" — while P735 takes one item per given name. Both are
recorded: the full string, and its tokens. The 13.7% row for full strings
against 57.0% for tokens is exactly that mismatch, and it is why the
token row is the one that matters for P735.

**The lookup has to be restricted to name items.** Matching a bare label
makes "Eikeland" a village and "Ragnhild" a queen, neither of which P734
or P735 could point at. The query filters `P31` to the five name types
(Q101352, Q202444, Q12308941, Q11879590, Q3409032).

Patronymics are counted separately — 565 of the surnames and 1081 of the
given tokens look patronymic — by a suffix heuristic that is stated in
the report to be **grouping only**. It will call some frozen hereditary
surnames patronymic, because nothing in the text distinguishes the two.

104 batched queries, all cached. `pytest`: 234 passed.

## 2026-07-30 — name links, and a misdiagnosis I have to own

`genimerge/namelinks.py` and `python -m genimerge name-links` write
`out/wikidata/add-names.qs`: **29 statements covering 28 of the 245
linked people**, linking them to P735/P734 name items that already exist.
Creates nothing, so it needed no decision. `quickstatements.py` grew a
generic `Statement` type; the P2600 path is unchanged and its tests still
pass untouched.

413 names were set aside, and the breakdown is the interesting part: 184
items **already state a given name** and 36 already state a family name —
the people we have linked are mostly well-curated royalty items that
already carry their names. 124 names have no item at all, 30 are
patronymics sitting in Geni's given-name field, and 27 are ambiguous
between several items.

Conservatism, all enforced: only names resolving to exactly one item;
only the primary `NAME` record, since order across records is not
meaningful; only items stating no P735/P734 at all; patronymics in the
given-name field never proposed as given names; and a given string is
**all-or-nothing** — if one token cannot be resolved the whole name is
held back, because proposing the second given name without the first puts
a wrong `P1545` series ordinal on the item.

**The misdiagnosis.** Spot-checking the first batch, I saw
`Q103781693 "Eirik 'Galte'" → family name Galtung` and called it a false
positive from alias matching. It was not. I had read Wikidata's label for
the *person* as though it were our source text; our surname for him is
"Galtung", and the link is right. I had already rewritten
`find_name_items` to distinguish `rdfs:label` from `skos:altLabel` on the
strength of that wrong reading.

Kept the change, because an alias is a weaker assertion than a label and
this file proposes edits — but rewrote every comment, docstring and report
line that justified it with the invented Galtung example. A fabricated
rationale left in the repo would be worse than the original mistake.

One real defect did come out of it: the `UNION` form of the label/alias
query **times the public SPARQL endpoint out with a 504** at this batch
size. It is now two plain index lookups per batch, which is why the
request count per batch doubled.

`pytest`: 252 passed.

## 2026-07-30 — cross-check: 625 agreements, 40 conflicts

`genimerge/crosscheck.py` and `python -m genimerge crosscheck` compare
what this tree says about the 245 linked people against what Wikidata
says, writing `reports/wikidata-crosscheck.md` and a batch for the
eligible gaps.

| property | agrees | gap | conflict | not comparable |
| --- | ---: | ---: | ---: | ---: |
| P22 father | 139 | 1 | 2 | 103 |
| P25 mother | 81 | 7 | 4 | 153 |
| P26 spouse | 135 | 24 | 3 | 83 |
| P569 date of birth | 127 | 70 | 20 | 28 |
| P570 date of death | 143 | 63 | 11 | 28 |

**625 agreements against 40 conflicts is independent evidence the matches
are right.** Nothing in the reconciliation used parents, spouses or dates
as a *primary* key — P2600 is an exact identifier and the structural pass
only walked relationships — so this is a genuinely separate check, and it
mostly agrees.

**Nine of the conflicts are structural** and those are the ones worth a
look: a different father for Canute I Erikska (we say Eric IX Q310152,
Wikidata says Q41864), a different mother for the same man, a different
spouse for Harald IV "Gille", a different father for NN Filipsdotter.
Each is either our match being wrong or a real error on one of the two
sites.

**The date threshold is deliberately not widened.** A date counts as
conflicting when the years differ by more than 3, which for medieval
people makes ordinary source disagreement (1145 against 1150) look like a
conflict. Widening it to 5 or 10 would have shortened the table by making
the classification vaguer. Instead conflicts are **ranked** — structural
first, then by how many years apart — so the serious ones surface and the
small ones sink, and the report states the threshold so a reader can
calibrate. A date our export marked approximate is never called a
conflict at all.

The batch, `out/wikidata/add-claims.qs`: **65 statements, 100 gaps
withheld.** 85 were withheld because our date is approximate and there is
no exact value to state; 15 because one end of a relationship is linked
by inference rather than by its Geni ID. That last rule is the important
one — putting an inferred parent onto a real Wikidata item is the error
that would be hardest for anyone to notice afterwards. Conflicts are
never proposed.

`pytest`: 281 passed.

## 2026-07-30 — the CLI had no tests at all

Not promoted from `todo.md`. Found by actually looking, rather than
repeating the claim that the queue was blocked: **no test imported
`genimerge/cli.py`.** Eleven subcommands' worth of argument wiring, output
paths and error handling were exercised only by me typing them, so a
broken command would have shipped with CI green. Every one of the bugs
this project has caught came from a test; this was the layer with none.

`tests/test_cli.py` — **52 tests**, all offline. Every command is
registered, dispatches to a callable, has working `--help`, and accepts
the workspace options. Then the documented pipeline runs end to end in a
`tmp_path` workspace over two small hand-written exports:
`inventory → merge → export → frontier`, asserting each file exists,
that the merged GEDCOM re-parses with no warnings, and that the merge
really merged (Ada's birth comes from one export and her death from the
other, on one record). Five tests cover the "run the earlier step first"
refusals.

**The fix underneath was a real limitation, not a testing convenience.**
`DATA_LAKE`, `OUT` and `REPORTS` were module constants pinned to the
repo, so the pipeline could only ever process one dataset — a second run
would overwrite the first, and a test could not run it without writing
into the working tree. There is now a `Workspace` resolved per command,
with `--data-lake` / `--out` / `--reports` on every subcommand. They are
added in a **loop over `sub.choices`** rather than threaded through each
`add_parser` call, so a new command cannot be added without them by
forgetting a `parents=`. `export` gained the output option it never had;
`merge` stopped writing two of its three files to fixed paths.

One test earns its place specially: `test_nothing_is_written_outside_the
_workspace` walks `tmp_path` afterwards and asserts every file written
landed inside it. That is the property that was false before this change.

Regression check beyond the suite: regenerated the three committed
reports with the refactored CLI and `git diff reports/` came back
**empty** — byte-identical output.

`pytest`: 333 passed.

## 2026-07-30 — the identity guard had never fired, and the pattern was wrong

Found by looking again rather than declaring the queue blocked.
`genimerge/identity.py` — the module the entire merge rests on — had **no
test file**, and `IdentityMismatch`, the exception that stops a record
whose xref and `RFN` disagree from being treated as one person, was
**never raised anywhere in the suite**. Its only mention was a comment
claiming it would, on data where it never does. A guard nobody has seen
fire is a guard nobody has checked.

`tests/test_identity.py`, 22 tests. Three of them failed on the first
run, and they were right to.

**The defect.** `GENI_ID_RE` accepted any run of letters as the record-type
prefix, so the xref `@NI04461@` parsed as Geni ID **`04461`** — a
fabricated ID, and `profile_url` would have produced a link to a
stranger's Geni profile. Measured what the data actually uses before
changing anything: across all 19,274 xrefs in the three exports there are
exactly four prefixes, each bound to one record type — `I` on every
`INDI`, `F` on every `FAM`, `N` on every `NOTE`, `S` on every `SUBM`. The
pattern now accepts only those. And `@NI04461@` is real: it is the single
`NOTE`→`NOTE` dangling pointer the merge report has been counting all
along, so refusing to read it loses nothing.

That is a defect the tests found in code that had shipped six commits
earlier, and it existed precisely because the module had no tests.

**What the merge keys on is now an asserted decision, not an accident.**
`Merger.add_source` keys on `record.xref` and never calls `geni_id_of`, so
a record whose `RFN` contradicted its xref merges on the xref without
complaint. That is the right call — a merge that refused to run over one
odd record would be useless — but it means the cross-check is *not* a
merge-time guard. It runs in `inventory`, in `model`, and over the merged
output in `test_merge_real_exports.py`. A test now states this and proves
both halves: the merge does not raise, and `geni_id_of` on the same record
does.

Regression check beyond the suite: regenerated the committed reports and
`git diff reports/` came back empty; merge totals unchanged at 8766
individuals and 4056 families.

`pytest`: 355 passed.

## 2026-07-30 — the commands that write the deliverables had never run under test

Found by **measuring** rather than guessing where to look next. Branch
coverage put the package at 89% with one outlier: **`cli.py` at 57%**,
138 statements unexecuted. The gaps were exactly the bodies of
`reconcile`, `expand`, `coverage`, `quickstatements`, `crosscheck`,
`name-links` and `names` — the code that writes the CSV and
QuickStatements files a human then reviews and acts on. The 52 CLI tests
from the previous tick covered those commands' *refusal* paths and
nothing else.

They were untestable **by construction**: each of the six built its own
`WikidataClient` inline, so the injectable `fetch` the client had been
given for precisely this purpose could not be reached. `cli.make_client`
is now the single seam, replacing six identical constructions.

`tests/test_cli_wikidata.py`, 14 tests, all offline. Each asserts the
*contents* of what a command produces, not that a file appeared: that
`reconcile` writes both sides of a match, that `expand` walks to an
unlinked child and records the evidence, that `crosscheck` proposes the
death year Wikidata lacks **and does not re-propose the birth year both
sides already agree on**, that `name-links` links to existing name items
and sets aside names with none.

**One of these tests was nearly worthless and got fixed before it
shipped.** `test_no_command_reached_the_network` asserted only that the
fake had seen some queries — which a command reaching the real Wikidata
would not have contradicted. The guard now patches
`urllib.request.urlopen` to raise, and a companion test *proves the guard
fires* by building a client the ordinary way and asserting it explodes.
Patching `wikidata._http_fetch` would not have worked: `fetch` defaults to
the function object captured when the dataclass was defined, so rebinding
the module name leaves a default-built client using the original.

**Deleted `gedcom.write_records`** — defined, called nowhere, tested
nowhere. Speculative streaming for "outputs too big to buffer" that
nothing ever needed. Deleting it is honest where adding a test to prop it
up would not have been.

`cli.py` 57% → **94%**; the package 89% → **95%**. Also untracked
`.coverage`, a 192 KB binary my own `git add -A` had swept into the
previous commit, and gitignored it.

`pytest`: 369 passed. Merge totals unchanged.

**CI did not run for this commit, and it is not the code.** Both matrix
jobs refused to start in under 4 seconds with:

> The job was not started because recent account payments have failed or
> your spending limit needs to be increased.

That is a GitHub Actions billing state on the account. The previous
commit's run passed 47 seconds earlier, and nothing in this change
touches the workflow. **BLOCKED-ON-USER-ACTION** — the action is sorting
out billing or the spending limit in GitHub settings; the unblock signal
is a run that starts.

Until then the only verification available is local, so it is stated
exactly: `pytest` 369 passed on Python 3.13 only (CI is what covers 3.10),
and the real-data regression check — regenerate the committed reports,
`git diff reports/` empty, merge totals unchanged at 8766 individuals and
4056 families. **Not** a claim that CI is green.

## 2026-07-31 — a partial substitute for the CI matrix, labelled as partial

With CI still refusing to start and only Python 3.13 on this machine,
`requires-python = ">=3.10"` in `pyproject.toml` was a claim nothing
checked. A 3.11-only construct could have landed and nothing would have
noticed until somebody on 3.10 tried to install the package.

`tests/test_python_floor.py`, 20 tests. It reads the floor **out of
`pyproject.toml`** rather than hardcoding it, so raising the floor updates
the check; parses every file under `src/` *and* `tests/` with
`ast.parse(..., feature_version=floor)`, which rejects syntax the floor
cannot handle; and greps the sources for a short list of stdlib names
newer than the floor (`tomllib`, `datetime.UTC`, `typing.Self`,
`ExceptionGroup`, `itertools.batched`, and so on).

Three details that matter more than the check itself:

**It says what it is not.** This is a syntax and known-name check, not the
test suite running on 3.10. Behavioural differences between versions are
exactly what it misses. Only CI catches those, and only once billing is
fixed. The file and this entry both say so, because the failure mode here
is letting "3.10 supported" quietly become an assumption again — which is
how the CI block became worth recording in the first place.

**It proves it bites.** Two tests assert the checks would actually reject
something: a `match` statement parses at 3.10 and raises `SyntaxError` at
3.9, and the denylist does flag `import tomllib`. A check that has never
rejected anything is the same category of thing as the identity guard that
had never fired.

**The floor is parsed with a regex, not `tomllib`** — because `tomllib` is
itself 3.11+, and importing it would stop this test running on the very
floor it checks.

The sources pass: every file parses at 3.10, none reaches for a newer
name. `pytest`: **427 passed**, Python 3.13 only. Still not CI-verified.
