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

## 2026-07-31 — CI turned off: billable minutes on a private repo

The user asked why Actions was running on a private repo at all, given it
costs money. Fair, and my fault: I wired push-triggered CI during
bootstrap without flagging that Actions minutes are free on *public*
repos but billable on private ones once the monthly allowance is used.
Enabling a metered service on someone's account is not a detail to slip
into a commit.

**What it actually cost, as far as I can see: nothing.** GitHub's own
timing API reports **0 billable milliseconds across all 14 runs** — the
seven that ran used roughly 10 minutes of wall-clock, against the 2,000
minutes a month included with private repos on Free. The account-level
figure needs a `user` OAuth scope this token does not have, so that is
GitHub's accounting rather than the final invoice, and the user should
confirm in Billing & plans.

Which also reframes the earlier block. *"Recent account payments have
failed or your spending limit needs to be increased"* appeared while
usage was inside the free allowance, so it is an **account-level payment
problem, not a bill from this repo** — something else on the account
switched Actions off everywhere. Recording that because the previous
entry tagged it BLOCKED-ON-USER-ACTION on the assumption it was ours to
unblock.

Turned off structurally, not just switched off:

- the workflow is **disabled** at the GitHub end (`gh workflow disable`);
- `ci.yml` lost its `push:` and `pull_request:` triggers and is now
  `workflow_dispatch:` only, so re-enabling it does not silently resume
  per-push billing;
- `CLAUDE.md` says never to re-add a push trigger here, and why;
- `README.md` and `queue.md` now describe local `pytest` as the
  verification step.

**The cost of the decision is stated rather than hidden:** the Python
version matrix no longer runs, so 3.10 is covered only by the static
check in `tests/test_python_floor.py`, and nothing should be called
CI-verified. That is a real reduction in assurance, and the right trade
against an unexpected bill — but it is a trade, not a free win.

## 2026-07-31 — the merge report's failure branches, tested at last

`merge.render_report` has two halves that have never run. All three exports
agree with each other, so `report.conflicts` is empty every time, and the
dangling-pointer paragraph only fires through the CLI. `merge.py` was at 92%
coverage for that reason — not because the branches are trivial, but because
the data has never reached them. The first export that contradicts one already
merged would execute them for the first time inside the report a human is
reading to decide whether to trust the merge.

Eight tests, `merge.py` **92% -> 99%** (the one line left is a loop `continue`).
What they pin down:

- **Only structural pointers mean a broken tree.** A missing `HUSB` does; a
  missing `SUBM` does not, and the paragraph has to say so — 14 of the real
  merge's dangling pointers are the incidental kind, and calling them breakage
  would misreport a healthy tree.
- **`detail=True` lists every conflict; `detail=False` points at
  `out/merge-report.md`** rather than duplicating it into `reports/merge.md`.
- **A `|` in a disputed value is escaped.** GEDCOM does not reserve the pipe,
  Markdown does. An unescaped one shifts every later column of that row and
  nothing announces it — the assertion counts delimiters, not just the escape.
- **A long value truncates to 80 chars with an ellipsis, and an empty one
  renders `*(empty)*`** instead of an invisible cell.

Each of the four assertions was checked against a deliberately broken copy of
`merge.py` — pipe escaping removed, `HUSB` dropped from the structural set,
the ellipsis dropped, every pointer counted as structural. All four mutations
failed the suite, so the tests bite rather than merely pass.

`pytest`: **435 passed**, Python 3.13 only. Not CI-verified; CI does not run
on this repo.

One thing to avoid repeating: the mutation script wrote `merge.py` back with
`Path.write_text`, which on Windows translates every line feed into a
carriage-return/line-feed pair unless `newline=""` says otherwise. The content
compared equal and `git diff` showed nothing, but the file on disk had gone
CRLF throughout. Restored with `git checkout`. Same shape as the
`Get-Content -Raw` warning already in `CLAUDE.md`: on Windows, a round-trip
through a text-mode write is not a no-op.

## 2026-07-31 - todo.md item 6 was describing built work as open

Item 6 listed "P735/P734 name links" and "missing parent/spouse links on items
that already exist" as still to do. Both had shipped: `genimerge name-links`
writes `add-names.qs` (commit 51f1eec), and `genimerge crosscheck` writes
`add-claims.qs` (commit 21dd123), which carries P22 x1, P25 x4, P26 x18
alongside 42 dates. The text was written before those landed and never
revisited.

That stale paragraph is not cosmetic: a work-loop tick read it, took it at face
value, and went looking for work that was already done. Backlog text that lags
the code sends effort at solved problems.

Item 6 now lists the three built slices with the command and output file for
each, and states what is genuinely left - re-running reconciliation once a
batch has been accepted, tagged BLOCKED-ON-USER-ACTION, because accepting a
batch at QuickStatements is the user's action and nothing here should do it for
them. The progress note at the top of the file is redated and says the same.

Added a line the file did not have anywhere: every batch under items 4, 5 and 6
stops at a file in `out/wikidata/`, nothing in this repo writes to Wikidata,
and nothing should start without the user saying it may.

`pytest`: 435 passed, unchanged - this commit touches no code.

## 2026-07-31 - "Jenny" was never a data source

The user's stated direction, as recorded in CLAUDE.md, said the tree would
later be expanded "with more exports (from Geni, and from Jenny)". Jenny was
transcription noise - a speech-to-text mishearing of Geni, confirmed by the
user. There is no second genealogy site, no second export format, and nothing
to wait for.

Struck from `CLAUDE.md`, `todo.md` items 3, 3a and 7, and `queue.md`.

What that changes, which is more than wording:

- **A blocker dissolved.** Items 3b and 7 were tagged BLOCKED-ON-USER-ACTION
  with "a Jenny export appearing in `data_lake/`" as the unblock signal. That
  signal was never going to arrive. Item 3b is still the user's action, but the
  real one: take the next Geni export from the branch points ranked in
  `reports/frontier.md`.
- **Item 7 shrank to almost nothing.** It was "support additional sources ...
  without the merge logic having to care which source a record came from".
  `Merger.add_source` keys on the xref and never asks which file a record came
  from, and `genimerge merge` globs `data_lake/*.ged` by default, so a further
  Geni export is a file drop and a re-run. What remains is a non-GEDCOM input
  path, with no second format in hand to build one against. Recorded as
  abstract rather than left looking like pending work.

Worth noting for the next session that reads an old devlog entry: Jenny is also
a real given name in this genealogy - `Jenny Martinsdatter Stangaland`,
`Jenny Pedersdatter Ølberg`, `Jenny Joakimsdatter Lea` all appear in
`export-BloodTree.ged`. Those are people in the tree, unrelated to the
mistranscription.

No code touched; 435 passed locally on 3.13.

## 2026-07-31 - cleanvibe update check, run for the first time

CLAUDE.md had recorded the last check as `never` since the repo was cloned, so
the six vendored skills had been frozen at clone-time wording without anyone
confirming that was current - including the skills that govern how these
sessions run.

Fetched <https://cleanvibe.emmaleonhart.com/updates.md>. It lists exactly six
skills, all introduced at **v1.14.0 (2026-05-30)**: emergency-stop,
cron-is-local, autonomous-loop, queue-driven-workflow, writing-style,
cleanvibe-update-check. All six are present here and none is superseded. No
skill file was changed, and the page lists none this repo lacks.

**What this check cannot tell us.** The page's newest entry is **v1.15.0
(2026-06-05)**, but this repo was scaffolded from **v1.17.0** - the devlog's
first entry says so. So the page is two minor versions behind the release that
produced this clone. "Nothing listed is newer than what we have" is true;
"nothing has shipped since" does not follow, because v1.16.0 and v1.17.0 are
not described there at all. Recorded in CLAUDE.md next to the date so the next
check does not read a bare date as an all-clear.

Also replaced the work-loop cron's prompt this tick. The old one asserted that
item 6's parent/spouse-link slice was unblocked work and named a Jenny export
as an unblock signal - both wrong since e59ac1a and 3ee6555, and the first of
them had already sent one tick chasing shipped work. The new prompt tells the
tick to read `todo.md` and `queue.md` for status rather than trust the snapshot
written into it, states that reporting `nothing actionable` is a correct
outcome, and carries the warning about writing repo files from Python needing
an explicit newline argument as well as an explicit encoding. Crons are
session-local, so this is not a repo change: work-loop is now job 41b7519c.

`pytest`: 435 passed, unchanged - no code touched.

## 2026-08-01 - export seeds: model the ball, not the subtree

The user pointed out what a Geni export actually is: a breadth-first walk from
one profile - ancestors, descendants, blood relatives, or everything - until it
hits the 3836 cap. What matters in a seed is therefore landing somewhere the
walk will cross into material we lack, and not landing in the middle of a
region already recorded several layers out. The seed itself does not need to be
well documented; the interconnectedness carries the export.

`frontier.py` answers a different question, and had been standing in for this
one. It ranks parentless people by descendant count - a measure of the tree we
already hold - and has no notion of two candidates sharing a neighbourhood, so
its top forty can all hang off one branch.

`genimerge/seeds.py`, and `genimerge seeds` writing `reports/seeds.md` and
`out/seeds.csv`:

- **Doorways** are people in a ball with no parents recorded. Parentless, not
  childless: a missing parent is evidence of missing data because everyone had
  two, while most people who look like leaves really were leaves. Counting
  childlessness would make every leaf an opportunity.
- **Openness** is the doorway share of a ball. Below 5% the ball is saturated
  and the seed is rejected outright.
- **Selection is greedy on newly-covered doorways**, not by rank, because
  neighbours share a ball.

Measured on the real 8766-person tree: 2336 candidates kept, **14 rejected as
saturated**, best openness 0.25. Ten greedy picks reach **173** distinct
doorways against **144** for the ten highest-ranked seeds - about 20% more for
the same ten exports.

Two things the numbers say that are worth not smoothing over:

**The saturation rejection barely fires.** Fourteen candidates out of 2350. The
threshold is a floor under the list, not the mechanism - ranking by doorway
count already keeps interior seeds away from the top. Left as measured rather
than tuned upward to look like it is doing more work than it is.

**A full export from the best seed reaches 3836 people we already have,
hitting the cap at hop 11.** That is not a prediction of a wasted export: Geni's
graph holds our people and the missing ones together, and its walk reaches both
at every hop. But it does mean the cap binds long before the walk runs out of
known territory, and the report says so instead of implying the ball is all new
material.

The report ends on what none of this can tell you. Doorways count what an
export can reach, never what is behind them - nobody knows how many people sit
above a parentless person, which is the whole reason to export from there. A
seed with 25 doorways is a better bet than one with 3; it is not a promise of
eight times the material.

18 module tests plus 3 CLI tests. `seeds.py` at 100% coverage. `pytest`: **462
passed**, Python 3.13 only. Not CI-verified; CI does not run here.

---

## 2026-08-01 — a fourth export lands, and it is not a fourth style

Commit `9046f73` dropped `export-geni/export-Forest.ged` into the repo root — a
Geni export dated 01 AUG 2026, 3840 individuals, 1806 families, 3840 `RFN`
lines. This is the unblock signal `todo.md` item 3b was waiting for.

Two things about it changed the conventions rather than just adding data.

**`Forest` is a style, not a person.** The three exports already in
`data_lake/` — `Forest`, `Ancestors`, `BloodTree` — are all rooted at the *same*
first `INDI` record, Eric Borsheim `6000000087535357291`, which is also their
`SUBM` xref. They are three shapes of one seed. So Geni's filename is
`export-<style>.ged` and carries nothing about who the export is *of*, and the
fourth export — rooted at Iver Mellegård `6000000226977233850`, who appears in
none of the three — arrived with a filename already taken. That collision is
structural and will happen again, so the fix is a scheme and not a rename:
`data_lake/export-Forest-6000000226977233850.ged`, style plus seed profile ID,
consistent with the profile ID being this repo's primary key. `git mv` kept the
history. Recorded in `CLAUDE.md`, not in `reports/inventory.md`, which is
generated and says not to hand-edit it.

Worth noting that `reports/seeds.md` could not have proposed this seed. That
report ranks parentless people *already in our tree*; Iver Mellegård is not one,
so this export came from somewhere the ranking cannot see. It is a good export
regardless — see below — but the ranking did not earn the credit.

**3836 is not the cap.** `CLAUDE.md` asserted exports are capped at 3836
individuals, on the evidence of three exports hitting it exactly.
The fourth has 3840. The claim was wrong, and it is not
inert prose: `genimerge/seeds.py` models an export ball as capped at 3836 and
`reports/seeds.md` reports the top seed "hitting the cap at hop 11", so the
number is wired into the ranking that decides what to export next. `CLAUDE.md`
now records 3836 as a lower bound observed three times rather than a constant.
It does **not** record 3840 as the new cap — that would be the same mistake
with a different number, from one observation and a four-person difference.
Establishing the real bound is queued as NEEDS-INVESTIGATION.

**What the export is worth**, measured before merging rather than predicted:

| | |
| --- | ---: |
| new export | 3840 |
| shared with `export-Ancestors` | 57 |
| shared with `export-BloodTree` | 140 |
| shared with `export-Forest` | 44 |
| shared with all three combined | 184 |
| **people it adds** | **3656** |
| merged tree 8766 → | **12422** |

95% new material, and a 42% larger tree.

**None of that has been merged, and no test was run.** There is no Python on
this machine. `python` and `python3` on PATH are the Microsoft Store stub
aliases — running one exits 49 with "Python was not found" — and there is no
real install anywhere: nothing under `%LOCALAPPDATA%\Programs` or
`C:\Program Files`, no `PythonCore` registry key under `HKCU` or `HKLM`, no
Store package. WSL is not a way around it; `wsl -l -v` fails with
`Wsl/CallMsi/Install/REGDB_E_CLASSNOTREG`. Python 3.13 did run here as recently
as 2026-08-01 02:23, going by the `cpython-313.pyc` timestamps in
`src/genimerge/__pycache__/`, so it was removed after that.

The counts in the table above were therefore computed in PowerShell by reading
`0 @…@ INDI` lines directly, not by `genimerge`. They stand as the numbers the
merge should be *checked against* when it can run — not as merge output. The
suite has not been run this session and nothing here is test-verified or
CI-verified.

Everything downstream — the merge itself, and the re-runs of `inventory`,
`frontier`, `seeds`, `reconcile`, `coverage`, `crosscheck`, `names`,
`namelinks` and `quickstatements` that a 42% larger tree forces — is
BLOCKED-ON-USER-ACTION behind a Python install. Unblock signal is a working
`python -VV` on PATH at 3.10 or newer.

---

## 2026-08-01 — the fourth export merged, and the cap claim retired

Python came back (3.13.14, `C:\Program Files\Python313\`), which unblocked
everything the previous entry left standing.

**The suite passed before anything was touched: 467, up from the 462 recorded at
`47d7a04`.** The five new cases are the per-file tests parametrised over
`data_lake/*.ged` picking up the fourth export. So the new file was already
exercised by `test_gedcom_real_exports.py` and passed without changes — the open
question from the last status report, answered.

**The merge.** 12422 individuals, 5794 families, **0 conflicts**. Then
`inventory`, `frontier`, `seeds`, `reconcile`, `coverage`, `crosscheck`,
`names`, `name-links` and `quickstatements` re-run against the larger tree.
Reconciliation now matches **209 of 12422 by P2600 (1.7%)**, crosscheck sees
245 people — 625 agreements, 165 gaps, 40 conflicts — and writes 65 statements
with 100 gaps withheld. Names: 1008 of 2351 surnames and 2076 of 3702 given-name
tokens have a Wikidata item. Nothing has been sent to Wikidata.

**The PowerShell numbers held exactly.** The previous entry recorded 3840 / 184
shared / 3656 added / 8766 → 12422, measured by reading raw `INDI` lines because
there was no interpreter to run the real parser. `genimerge inventory` agrees on
every one: 3840 individuals, 1806 families, 3656 unique to the new export, union
12422. That was the one thing flagged as unverified — an ad-hoc reimplementation
of something `genimerge.gedcom` does properly, with nothing checking it. It
checks out.

One thing the regenerated inventory shows that the estimate did not: people
present in *every* export fell from 354 to **9**. The fourth export overlaps the
other three so little that the four-way intersection nearly vanishes.

**3836 is no longer described as a cap anywhere.** `GENI_EXPORT_CAP` is now
3840, and — the actual point — it is documented as *the largest export observed*
rather than a limit Geni enforces. The old comment said "Measured, not guessed:
all three exports contain exactly this many", which was true and still produced
a false conclusion; three different-style walks sharing only 354 people all
stopping on 3836 looked like proof of a hard cap.

What actually bounds an export is **not established, and is not guessed at**. A
raised limit between 2026-07-30 and 2026-08-01, a per-account limit, a limit on
something other than head count, and a walk that overshoots a floor by however
much finishes the current generation all fit four exports equally well. The
constant's docstring lists them and encodes none. The stale prose in
`frontier.py`, `cli.py` and the seeds report is corrected the same way, and
`inventory.py` no longer converts equal counts into "a per-export cap, not a
coincidence" — that inference has now failed once, and the report says so.

The load-bearing part is a test, not a number. `test_seeds.py` asserts
`GENI_EXPORT_CAP >= max(INDI)` over `data_lake/`, so the next export to exceed
it fails loudly rather than silently modelling a ball smaller than a real
export. Verified non-vacuous rather than assumed: the guard currently sits
exactly on the boundary (largest observed 3840, constant 3840) and evaluates
false at the old 3836. A second test pins that the constant actually bounds
`export_ball` rather than only appearing in documentation.

Re-running `seeds` on the larger tree moved the plan: 2932 candidates kept, 38
rejected as saturated, and the ten picks now reach **193** doorways against 172
for the ten highest-ranked taken without regard to overlap. Pick 1 is unchanged;
pick 2 is new.

**469 passed**, Python 3.13.14, run before and after the changes. Not
CI-verified — CI is `workflow_dispatch:` only here on purpose, so no run
happened and none was implied.

One environment wrinkle worth recording rather than fixing silently: `python`
and `python3` on PATH still resolve to the Microsoft Store stub aliases ahead of
the real install, so the bare `python -m pytest` that `CLAUDE.md` prescribes
exits 9009. `py -m pytest` and the full path work. The package is not
pip-installed, so the CLI needs `PYTHONPATH=src`; pytest does not, because
`pyproject.toml` sets `pythonpath = ["src"]`. Left alone — changing a user's
PATH is not this repo's business — and noted in `queue.md`.

---

## 2026-08-01 — `expand` re-run: the fourth export reaches no new Wikidata items

`out/wikidata/candidates.csv` and `matched_all.csv` were stamped 2026-07-30
18:06 while every other artefact in that directory was from 2026-08-01. The
merge tick's re-run list named nine commands and omitted `expand`, so the
fallback-matching half of `todo.md` item 2 had not been run against the larger
tree — and `coverage`, `crosscheck`, `name-links` and `quickstatements` all read
what `expand` writes.

**Re-running it changed nothing at all.** `candidates.csv` came back at 24484
bytes and `matched_all.csv` at 14585 — byte-for-byte the sizes of the 07-30
files — and `reports/wikidata-coverage.md` regenerated identical to the
committed version, git reporting no diff. Still 245 of 12422 linked (209 by
P2600, 36 by expansion over 3 rings), still 171 proposals, still 87 people
awaiting review.

So the 3656 people the fourth export added reach **zero** new Wikidata items,
either by exact P2600 join or by walking three rings of family structure out
from the existing matches. That is a result rather than a non-event: it says the
new export lands in a part of the tree Wikidata does not cover. Consistent with
what it is — Norwegian farm families, where the P2600 matches sit in the royalty
and nobility branches the first three exports were rooted in. Coverage fell from
2.8% of 8766 to 2.0% of 12422 purely by growing the denominator.

**A wrong claim made and withdrawn in the same tick, recorded because the
sequence is the useful part.** Re-running bare `expand` produced a coverage
report with 30 proposals against the committed 87, which read as proof that the
merge tick had committed a report built on stale data. It was not. Bare `expand`
skips the label-index lookup, and the 100 `name-match` proposals come only from
`--search`. The regression was in the re-run, not in the commit; `expand
--search` restored byte-identical output. The diff was real and the diagnosis
was wrong, which is worth more than either alone: a changed report is evidence
that *something* differs, never on its own evidence of which side is stale.

The durable fix is not new documentation, because the documentation was already
correct. `README.md`'s "before pushing" block lists every command in dependency
order and already says `expand --search`. The failure was following a re-run
list written by hand in a cron prompt instead of the file that exists for this.
`queue.md` now says to take the order from the README, and says what omitting
`expand` and what dropping `--search` each cost.

Also corrected: the NEEDS-DECISION entry in `queue.md` still sized `todo.md`
items 4 and 5 with pre-merge figures, 1117 surnames and 1473 given names lacking
Wikidata items. Against the regenerated `reports/names.md` the real gaps are
**1343 surnames and 1626 given names** — 1008 of 2351 distinct surnames (42.9%)
and 2076 of 3702 given-name tokens (56.1%) have items. Whole given-name strings
as Geni stores them are far worse at 929 of 8168 (11.4%), because Geni packs
several names into one field.

**469 passed**, Python 3.13.14. No code changed this tick, so the suite is
unchanged from `601f840`; it was run to confirm that, not to claim it. Not
CI-verified — CI is `workflow_dispatch:` only here on purpose. Nothing has been
sent to Wikidata.

---

## 2026-08-01 — the contradiction count gets a denominator, and a health warning

`add-p2600.md` reported "3 contradicting an existing ID — for you to resolve"
and had done since the batch existed. Three against nothing. This tick worked
out what the three are three *of*.

**What they are.** All three are expansion-inferred matches — each appears in
`matched_all.csv` and not in `matched_p2600.csv` — and in all three the Geni ID
Wikidata already carries is absent from our tree entirely, so no local check can
adjudicate them.

Reading `_cmd_quickstatements` settled the denominator exactly rather than
approximately: it filters `source == "expansion"`, so the batch is built *only*
from inferred links. A person already matched by P2600 needs no edit and never
reaches the file. That makes 33 edits + 0 already-correct + 3 contradicting =
**36**, which is every expansion match in the tree. The two numbers were both
already in the module; nothing said what they meant together.

So `Batch.considered` now exists and the report prints "expansion-inferred links
examined | 36" above the contradiction row, making "3" a fraction of something.

**A claim corrected mid-task.** The queue item written at the start of this tick
called the three "measured false positives", on the reasoning that an explicit
P2600 beats an inference. That is wrong, and the report says so instead: a
contradiction is *either* a bad match *or* two Geni profiles for one person, and
with the other ID outside our tree nothing here decides which. Writing the plan
before doing the work is what exposed it — the sentence had to be defended
before it could be published.

**Why the number is weak, stated in the report rather than left to the reader.**
A wrong inference is only detectable when the item it landed on already carries
a P2600, and almost none do — that absence is the problem this project exists to
address. So the check sees a little and cannot see the larger part, and 3-of-36
is not an accuracy figure. Two tests pin that framing to the output: one asserts
the count appears against its denominator, and one asserts the report keeps both
caveats — that a contradiction may be a duplicate profile, and that the check
only fires where a P2600 already exists. Prose tests are unusual, but this prose
is the finding; without those two sentences the number reads as a measured error
rate, which is what the previous version of the queue item took it for.

The denominator is printed even when nothing contradicts, since 0-of-N is a
result and a silently absent section is not.

**474 passed** (was 469; 5 added), Python 3.13.14. `add-p2600.md` regenerated
and confirmed showing 36. Not CI-verified — CI is `workflow_dispatch:` only here
on purpose. Nothing has been sent to Wikidata.

---

## 2026-08-01 — `merge` now says whether the result is still one tree

The user stated the project's purpose plainly this tick: one growing **synoptic**
tree. What makes it synoptic is that the graph is connected, and the merge step
had nothing to say about that. `genimerge merge` printed record counts and a
conflict count and stopped. The component count lived only in
`reports/frontier.md` — a different command, run later, that nobody is obliged
to run.

The gap is not theoretical, and the fourth export is the reason to close it. It
shares **184 people** with the union of the other three, 4.8% of itself, and
those 184 are the whole reason its 3656 new people joined the tree rather than
sitting beside it. Seeded a little further out it would have landed as an
island — and `merge` would have printed `0 conflicts` exactly as it did. That is
the trap: components do not conflict. Nothing contradicts anything; the two
halves simply never meet, so every counter the merge already had would have
looked perfect.

`frontier.describe_connectivity` now renders one line and `_cmd_merge` prints
it. On the real data: `one connected tree, all 12422 people`. When it splits it
names the sizes rather than just the count, because a 3656-person island and a
2-person island are not the same event.

**It warns; it does not fail.** More than one component is a legitimate state —
`frontier` exists partly to say that a component nobody outside it is related to
needs its own export seed. Making the merge fail would have been a wrong
assertion in the opposite direction from the usual one: not too weak, but too
strong, and the kind that gets silenced later rather than fixed. A test pins the
wording against the words "error", "invalid", "failed" and "corrupt" so it
cannot drift into blaming a state that is allowed.

Reused `frontier.components` rather than writing a second graph walk; it already
returned components largest first.

Seven tests. Two of them are at CLI level rather than on the helper, because the
helper being right proves nothing about it being called — and the existing
`workspace` fixture turned out to be exactly the case worth catching: `two.ged`
adds Di Delta with no family links, so that merge already succeeded with zero
conflicts and two trees. The test asserts both facts on the same run.

**481 passed** (was 474), Python 3.13.14. `reports/frontier.md` regenerated and
unchanged, as expected — the new function is additive and the report's renderer
was not touched. Not CI-verified; CI is `workflow_dispatch:` only here on
purpose.

Also recorded in `queue.md` as a standing NEEDS-DECISION: `seeds.md` can only
rank people already in the tree, and the seed that produced the best export so
far was not one of them. How that seed was found is a channel this repo cannot
see, and the answer decides what to build next.

---

## 2026-08-01 — a conflict that is about the link, not the fact

`wikidata-crosscheck.md` listed 40 conflicts as 40 rows, ranked by how far apart
the two sides were, above a per-property summary. One property per row reads as
40 independent errors. Four of them were one person.

Canute I Erikska, `Q442876`: father disagrees, mother disagrees, birth 1145
against 857, death 1196 against 934. Nothing agrees — **0 agreements against 4
conflicts**. As four rows that is two bad parents and two bad dates; together it
is one observation, and what it is evidence about is the link.

The provenance sharpens it rather than explaining it away. `Q442876` is an
**exact P2600 match** — the Geni ID is on the Wikidata item — so this is not the
expansion-inference weakness already written up in `add-p2600.md`. The Geni ID
on that item is under the same suspicion as the match itself.

`link_balances` and `suspect_links` now tally agreements and conflicts per
`(geni_id, qid)`, and the report gained a "Links worth re-checking" section.
Gaps and *not comparable* are excluded from the tally on purpose: a gap is
Wikidata not stating something, which is evidence about coverage, and *not
comparable* is not evidence at all. The test is `conflicts > agrees` with at
least two conflicts — one conflict alone is ordinary, since two medieval sources
differing on a single date says nothing, and a person agreeing on more than they
conflict on is a sound link with a data disagreement inside it.

On the real data it finds **2**: Canute I Erikska (0/4) and Bengt Folkesson
(1/2), both exact P2600. Nine tests, including one asserting that four people
with one conflict each are *not* pooled into a false signal.

**The section does not say the links are wrong, and a test holds it to that.**
Conflicting on everything is equally what a correct link to bad data looks like;
for early-medieval people a birth year three centuries out is a copied error,
not proof of mistaken identity. What the report does instead is name the two
readings and print the one column that shifts the odds between them — whether
the link is exact or inferred. An inferred link failing this test is weak
evidence twice over; an exact one failing it implicates the ID.

This is the same shape as the `add-p2600.md` denominator two ticks ago: nothing
newly measured, something already computed that nothing said out loud. The
per-property summary and the per-conflict list were both there; the per-person
view was the one nobody had taken.

**490 passed** (was 481), Python 3.13.14. Report regenerated against live
Wikidata. Not CI-verified — CI is `workflow_dispatch:` only here on purpose.
Nothing has been sent to Wikidata.

---

## 2026-08-01 — paying a debt named three times and deferred three times

Three reports carry a caveat that is the finding rather than decoration — that
3-of-36 is not an error rate, that a split tree is not an error, that a suspect
link is not a wrong link — and each had a test asserting the caveat survives.
The reasoning was right: a number stripped of its caveat actively misleads. The
mechanism was not. Each test held a copy of the sentence, so rewording a caveat
broke a test while nothing behavioural changed, and the repair anyone reaches
for under time pressure is to loosen the assertion. That is the one repair this
repo does not make.

**The interesting part is why it took three ticks.** Every status report since
`acb25d2` named this, and every one deferred it on a threshold I had invented —
"if a fourth case arises, build a shared mechanism". Three is not four, so
nothing happened, three times. But "wait for a fourth" is not one of the six
not-done categories, and under the load-bearing default an item with no named
blocker is not deferred, it is due. The rule caught something a plausible-
sounding personal heuristic had been quietly overriding.

Each caveat is now a module-level constant — `NOT_AN_ERROR_RATE`,
`SPLIT_IS_NOT_AN_ERROR`, `SUSPECT_IS_NOT_WRONG`, `NO_SUSPECT_LINKS` — emitted by
the renderer and asserted by *identity* in the test. Rewording is now a one-line
edit that keeps the tests green, because the test references the same object.

Identity alone would have been weaker than what it replaced, and the reason is
worth stating because it is not obvious: **an emptied constant is a substring of
every string**, so `"" in markdown` passes and a caveat deleted to nothing would
sail through. Checked rather than assumed — `'' in '# some report'` is `True`.
So each caveat also gets a companion test pinning the ideas inside it, and that
is the assertion that fails on an emptied constant. Brittleness is not removed;
it is moved to one place per caveat and made deliberate.

Two things stayed as literals on purpose. Assertions about *data* — `|
expansion-inferred links examined | 3 |`, `all 6 people` — are about output, not
wording. And `test_frontier.py`'s check that the connectivity line contains none
of "error", "invalid", "failed" or "corrupt" never depended on the wording at
all, which makes it the strongest of the three caveat tests and the model for
what to write when a property can be stated negatively.

Verified behaviour-preserving rather than assumed: `crosscheck`,
`quickstatements` and `merge` re-run against the real data, `git diff reports/`
empty, and `merge` still printing `one connected tree, all 12422 people`.

**493 passed** (was 490), Python 3.13.14. Not CI-verified — CI is
`workflow_dispatch:` only here on purpose.

---

## 2026-08-01 — `todo.md` catches up, and two predictions become measurements

`todo.md` is where this project keeps its intentions, and `CLAUDE.md` makes it
the file every queue item is decomposed from. It still described a three-export
world: a progress note dated 2026-07-31 saying item 3 had "its analysis half but
not its ingest half", when the fourth export had supplied that ingest half a day
earlier.

The stale summary was the small part. The part worth the tick is that this file
states expectations, and **two of them stopped being expectations**:

- **Item 3b** predicted that a new `.ged` would be absorbed by `genimerge merge`
  "without changes" and that the seed ranking could then be re-run. Tested. The
  merge took 3840 more people with **zero code changes**, and `seeds` re-ran to
  a materially different plan — ten picks reaching 193 doorways against 173,
  with picks 2, 3, 8 and 9 new.
- **Item 7** predicted that another Geni export would be "a file drop and a
  re-run, not a code change". Also held — but recorded with its asterisk rather
  than as a clean win. The export did require one change: a **rename**, because
  Geni names files `export-<style>.ged` and a second `Forest` collided with the
  first. That is two files wanting one name rather than the merge caring where a
  record came from, so the claim survives; but "just a file drop" is exactly the
  kind of phrase that hides a detail like that, and a backlog is more useful when
  it says which of its promises have been kept and how exactly.

Both are now marked *Confirmed 2026-08-01* where they appear. A list of
intentions that never distinguishes the predicted from the measured slowly
becomes a list of beliefs.

Also corrected, both of them things this repo had already fixed everywhere else:

- Item 3b still described an export ball as "capped at 3836". `CLAUDE.md`,
  `seeds.py` and `reports/seeds.md` all stopped saying that two commits ago;
  `todo.md` was the last place carrying it. It now points at
  `GENI_EXPORT_CAP` for the four competing explanations instead of asserting a
  number.
- Item 1 listed `Forest`, `Ancestors` and `BloodTree` as though they were
  exports. They are *styles* — the first three files are three styles of one
  seed — which is why the fourth needed renaming.

And item 3b gained the thing the ranking cannot do: it ranks only people already
in the merged tree, so it could not have proposed Iver Mellegård, who was in
none of the first three exports. The best export so far came from a route this
repo cannot see.

**493 passed**, unchanged, Python 3.13.14. Stated for completeness rather than
as evidence: this commit is prose only, so a green suite says nothing about it
beyond that nothing was broken in passing.

---

## 2026-08-01 — the report was naming the signpost, not the destination

Asked how the fourth export was seeded, the user said they took a recommended
person and "went one person off" — to that person's parent on Geni. Checked
against the data, and it holds exactly:

- the export was seeded on **Iver Mellegård** `6000000226977233850`;
- his only child in the tree is **Hågen Iversen** `6000000019312592888`, present
  in `export-Ancestors.ged` and therefore in the pre-merge 8766-person tree;
- Hågen had no parents recorded before the merge — a *doorway*, by this repo's
  own definition.

So the seed was never a listed candidate. It was the person **behind** one: the
unknown parent whose absence is what made the child a doorway. That export came
back 95% new.

`reports/seeds.md` had never said to do this. It lists doorways with Geni
profile links under "The next 10 exports", which reads as *export from this
person* — and exporting from the doorway centres Geni's walk on somebody we
already hold, so a large part of the ball returns as material we have. Centring
one step beyond the frontier is the whole trick. `EXPORT_FROM_THE_PARENT` now
says so at the top of that section: open the profile, go **up**, export from
there. The listed person is the signpost, not the destination.

**The ranking comes out of this badly, and the report now says so rather than
quietly not mentioning it.** Reconstructing the pre-merge tree from the three
original exports and re-running `rank_seeds` puts Hågen at **2255 of 2336** —
ball of 5, one doorway. The only export with measured results came from the
bottom of the list. There is a plausible mechanism: ranking by *absolute*
doorway count favours large balls, and a large ball is a densely recorded
neighbourhood, which is the opposite of where Geni has most to add. A sparse
corner scores near zero precisely because we know little there.

**It was not re-ranked on.** n=1; the ranking never scored Iver at all, because
he was not in our data to score; and no rival seed was tried against him. That
is a hypothesis, not a result, and rebuilding a model on one observation is the
mistake this repo already made once with the 3836 cap. `RANKING_IS_UNVALIDATED`
states the evidence and its limit together, and a test asserts both halves
survive — drop the first and the list reads as tested, drop the second and one
data point reads as grounds to rebuild.

The archaeology did not fully resolve. Neither Hågen nor Iver has ever appeared
in a committed report — `git log -S` over `reports/` finds nothing before the
merge — so whatever was recommended came from somewhere outside these files.
Said plainly rather than smoothed over: the useful finding came out of chasing
it, but the original question is still open.

**498 passed** (was 493), Python 3.13.14. `reports/seeds.md` regenerated. Not
CI-verified — CI is `workflow_dispatch:` only here on purpose.

---

## 2026-08-02 — measuring a claim I had put in a report on reasoning alone

`e5a41b8` shipped `RANKING_IS_UNVALIDATED`, which told anyone choosing an export
seed that "ranking by absolute doorway count favours large balls, and a large
ball is a densely recorded neighbourhood — which is the opposite of where Geni
has most to add." Plausible, and reasoned rather than measured — which is
exactly what the 3836 cap was before a fourth export falsified it. It sat in the
report people pick seeds from, and it was checkable against 2932 candidates
without waiting for anything.

So it was checked. Three of its four parts held, one did not belong to this data
at all, and the sentence has been split accordingly.

**Held, and more sharply than the original wording managed.** Candidates with a
ball over 100 are **1.5% of the pool and 80% of the picks**. Median ball among
the picks is 114 against 20 for the pool. Median openness among the picks is
**17% against 20%** — the recommended seeds are *less* open than a typical
candidate, which is the opposite of what a report about openness implies it is
doing. The most open candidate in the entire pool, at 57%, ranks **1198 of
2932**.

**Too strong in one place.** Ball size and doorway count correlate at r = 0.77,
r² = 0.59 — most of the ordering, not all of it. At a given ball size the
doorway counts still spread, so the sort is not ball size wearing another name,
and the report now says that rather than implying the stronger version.

**Did not belong here at all.** "The opposite of where Geni has most to add" is
a claim about Geni's data, not ours, and nothing measurable on this side can
reach it — we cannot see what is behind a doorway without exporting through it.
That is now stated as the limit of the measurement instead of riding along with
it. `SIZE_BIAS_LIMIT` carries it, with a test on the sentence that refuses the
verdict, because without it a description of the sort reads as a judgement on it.

The measurement is in `reports/seeds.md` beside the claim it tests, not only in
this file. A correction that lives where nobody choosing a seed will see it is
not a correction.

Two test failures on the way, both mine and both in the tests: a `Ball`
constructed without its required `seed` and `depth`, and an assertion on a
substring that the sentence does not contain — `"does not show that the ranking
is wrong"` against the actual `"does not show is that the ranking is wrong"`.
Fixed by correcting the tests, not by loosening them; the `_pearson` test
dropped its `SeedProfile` scaffolding entirely and now checks the coefficient on
plain lists, which is what it was ever testing.

**506 passed** (was 498), Python 3.13.14. `reports/seeds.md` regenerated. Not
CI-verified — CI is `workflow_dispatch:` only here on purpose.

---

## 2026-08-02 — the ordering, checked against the only export that ever worked

`7b68c0e` established that the ranking prefers large, proportionally less open
neighbourhoods and that the pool's most open candidate ranks 1198 of 2932. The
natural next commit was to offer openness as an alternative view. It was checked
first, and it is a good thing it was.

Hågen Iversen — the doorway the 2026-08-01 export was taken through — had a ball
of 5 and one doorway, which is **20% openness against a pool median of 20%**.
Middling on the very metric about to be promoted as the repair. So the question
was not "is openness better" but **would any ordering available to us have
surfaced him**, and against the 2336 pre-merge candidates:

| ordering | his rank |
| --- | ---: |
| doorway count — what the report sorts on | 2261 of 2336 |
| openness | 1303 of 2336 |
| ball size | 2293 of 2336 |
| *smallest* ball first | 38 of 2336 |

The shipped ordering puts the one seed known to have worked in the bottom 3%.
Openness does not rescue it. The only ordering that surfaces it is the inverse
of ball size.

**And that is not being adopted.** One observation cannot establish a ranking
rule; the 3836 cap had three and was still wrong. It is in the report as a
hypothesis with its mechanism stated — a tiny neighbourhood is one we know
almost nothing about, so almost everything behind its doorway is new — and an
explicit refusal to sort on it.

**One objection of mine turned out to be wrong, which is worth recording because
it nearly killed the finding.** Smallest-ball sounds degenerate: rank by fewest
recorded relatives and surely you get isolated fragments and broken records
first. Measured, that is false. A doorway is *in* our tree, so it always has
some recorded relative — the shortlist is **66 candidates of 2932, none with a
ball of 2 or fewer**. Having assumed the objection, stating it as fact would
have buried a testable idea under a plausible-sounding dismissal. That is the
same failure as asserting a mechanism without measuring it, pointed the other
way.

So the report now proposes the experiment rather than a conclusion: one export
from a top-ranked pick, one from the small-ball shortlist, compared on new
people returned. Two observations instead of one.

**510 passed** (was 506), Python 3.13.14. `reports/seeds.md` regenerated. Not
CI-verified — CI is `workflow_dispatch:` only here on purpose.

---

## 2026-08-02 — an experiment with only one arm is not an experiment

`d59191f` closed by proposing the only thing that would produce a second data
point: take one export from a top-ranked pick, one from the small-ball
shortlist, compare how many new people each returns.

It named the first arm — profile, link, rank — and gave the second as a number.
"66 of 2932", and nothing else. Every table in that file is ordered by doorway
count, which by construction puts large balls first, so the smallest ball
appearing anywhere in the report was **13** while the shortlist is everyone at 5
or fewer. Not one of those 66 people was identifiable from the document that
asked you to export from one of them.

That is a defect in the deliverable, not a refinement of the model, and it is
the kind that is easy to miss from the inside: the reasoning was complete, so
the output felt complete. It was not runnable.

The report now carries a "small-ball shortlist" section — ten of the 66,
smallest ball first — with profile links and IDs. The current tree puts ten
candidates at ball 4 with a single doorway each, so the cut is arbitrary among
equals and the heading says ten *of* 66 rather than implying a top ten.

**Named people look endorsed, so the section says twice that they are not.**
`SMALL_BALL_IS_THE_OTHER_ARM` states that the sequence at the top is still what
the model proposes, and that a list of names adds exactly nothing to the
evidence behind it — still one observation. A test pins both halves, because the
risk here is specific: putting ten linked profiles under a heading is the most
recommendation-shaped thing a report can do, and the hypothesis has not earned
it.

`EXPORT_FROM_THE_PARENT` is repeated inside the section rather than left to the
top of the file, and a test asserts it appears twice. A reader who scrolls
straight to a shortlist and exports from the person named would undo the one
thing the fourth export actually taught us.

**516 passed** (was 510), Python 3.13.14. `reports/seeds.md` regenerated. Not
CI-verified — CI is `workflow_dispatch:` only here on purpose.

---

## 2026-08-02 — the README documented the safest batch and not the riskiest

`README.md` § "Editing Wikidata" is where this project explains what it produces
for review and what the reviewer is taking responsibility for. It described
`add-p2600.qs` and stopped. Counted across the whole file: `add-p2600` three
times, `add-names` once — in a command listing, not the review section — and
**`add-claims` not at all.**

All three batches exist, all three are approved to run, and the undocumented one
is the largest and by a distance the most consequential:

| batch | statements | changes |
| --- | ---: | --- |
| `add-p2600.qs` | 33 | one external ID per item |
| `add-names.qs` | 29 | P735/P734 links to existing name items |
| `add-claims.qs` | 65 | parents, spouses and dates |

Adding a Geni ID is a fact about a record. Asserting someone's mother is a claim
about a person, on a public site, that other projects copy. Documenting the
first and not the third is exactly backwards, and it mattered this week rather
than in principle: the batches were approved two days ago and the file explaining
what they do covers a third of them.

The section now lists all three **in ascending order of consequence**, with the
rule each one enforces to stay out of trouble — every one of which is a refusal
rather than a guess:

- `add-p2600` takes only structure-confirmed links, and reports an item already
  carrying a different Geni ID as a contradiction instead of overwriting it;
- `add-names` sets an ambiguous name aside rather than choosing — 413 of them —
  and only links to name items that already exist, never creating one;
- `add-claims` proposes only gaps, never conflicts, needs *both* people linked
  by Geni ID rather than by inference, and will not state an approximate date.
  On the current tree it withholds 100 gaps to propose 65 statements.

Every number quoted was read back out of the generated files rather than
remembered: 413 set aside in `add-names.md`, 65 proposed and 100 withheld in
`add-claims.md`.

Also added: a pointer to the "links worth re-checking" section of
`reports/wikidata-crosscheck.md`, and the fact that nothing in it reaches a
batch. A reader who knows the batches are conservative should also know where
the unresolved things went.

**516 passed**, unchanged, Python 3.13.14. Prose only — stated for completeness,
not as evidence, since a green suite says nothing about a README. Not
CI-verified.

---

## 2026-08-02 — the instructions file said a fixed bug was still open

`CLAUDE.md` is what a future session reads as current fact, which makes a stale
claim there worse than the same claim anywhere else. Two were stale.

**It said the 3836 fix was never finished.** Verbatim: "`genimerge/seeds.py`
still models the ball cap as 3836 and `reports/seeds.md` still reports hitting
it at hop 11 — both are wrong in the same way and are tracked in `queue.md`."
Checked, all three parts false: `GENI_EXPORT_CAP` is **3840** and documented as
largest-observed rather than a cap, `seeds.md` contains **zero** occurrences of
"hitting the cap", and `queue.md` tracks nothing of the sort because it was done
in `601f840` — twelve commits before this one. A session trusting that would go
hunting a bug that is not there, or "fix" what is already right. Written when it
was true, left behind by the commit that made it false.

**And the xref total was a three-export figure.** 19,274 then; **25,138** across
four.

The count was the smaller problem. The claim it supports is load-bearing —
*exactly four xref prefixes, `I`/`F`/`N`/`S`, each bound to one record type* —
and `GENI_ID_RE` accepts only those because when it accepted any letters the
foreign xref `@NI04461@` parsed as Geni ID `04461` and pointed at a stranger's
profile. So the claim was re-measured rather than the number patched, since a
fourth export had landed since anyone last looked and a fifth prefix would break
that regex silently:

| prefix | record | count |
| --- | --- | ---: |
| `I` | INDI | 15348 |
| `F` | FAM | 7161 |
| `S` | SUBM | 1589 |
| `N` | NOTE | 1040 |

Four prefixes, none bound to more than one record type. The claim survives the
fourth export, and `CLAUDE.md` now says it was re-checked on 2026-08-02 rather
than implying the original measurement still covers the current data. It also
now says to re-measure when an export lands, because that is the assumption
`GENI_ID_RE` rests on and the failure mode is silence.

This is the third documentation file this session found asserting something the
code had moved past — after `todo.md` and `README.md`. The pattern is the same
each time: a sentence that was true when written, invalidated by a later commit
that had no reason to look at it. Nothing tests prose against reality, and the
only defence is going and looking.

**516 passed**, unchanged, Python 3.13.14. Prose only — stated for completeness,
not as evidence. Not CI-verified.

---

## 2026-08-02 — the prefix claim stops depending on somebody remembering

`e2b3f05` put this in `CLAUDE.md`: "**Re-measure this when an export lands.** It
is the assumption `GENI_ID_RE` rests on, and a fifth prefix would break it
silently rather than loudly." Correct, and the weakest available form of it — a
note asking a person to remember something on an occasion that happens every few
days at most.

The repo already prefers the other answer twice over: `test_seeds.py` fails when
an export exceeds `GENI_EXPORT_CAP`, and `test_gedcom_real_exports.py` exists in
the first place because "the fixtures are what we *think* Geni emits, and these
files are what it *actually* emitted".

**Nothing asserted the premise against the real files.** `test_identity.py`
covers `GENI_ID_RE` well, including the `@NI04461@` case that motivated it, but
only on hand-written fixtures. That every xref prefix in an actual export is one
of `I`/`F`/`N`/`S`, each bound to a single record type, was measured by hand —
most recently an hour before this commit, by me.

Now asserted per export, every run: the prefix set is a subset of the four
known, and no prefix appears on two record types. The failure message names the
offending prefix and tag, because the reader of that failure needs to know what
Geni changed, not merely that something did.

**The guard is proved non-vacuous rather than assumed to work.** Every export in
`data_lake/` passes, so a broken check would look identical to a working one.
Two tests run the real logic over hand-built documents that must fail it — one
carrying `@NI04461@`, one putting `I` on both an `INDI` and a `FAM`. A third
pins the detail the whole thing turns on: `_prefix("@NI04461@")` is `"NI"`, not
`"N"`. Had it stopped at one letter, the foreign xref would have read as a
`NOTE`, landed inside the known set, and the suite would have stayed green while
`GENI_ID_RE` went on parsing `04461` out of it — the exact bug these tests exist
to catch.

One test written on the way was discarded rather than kept: it built a dict
inline and asserted the dict was what had just been written, testing nothing.
Replaced with the two that exercise the real helper. A test that cannot fail is
worse than no test, because it reads as coverage.

**The count is deliberately not asserted.** 25,138 is a fact about how many
exports happen to sit in `data_lake/` and *should* change; pinning it would
produce failures that mean nothing and teach whoever hits them to edit numbers
until the suite passes. Only the structural claim is worth a test.

`CLAUDE.md` now points at the test instead of instructing a re-measure. An
instruction and a test saying the same thing will drift, and the instruction is
the half that drifts — which is how the paragraph corrected in `e2b3f05` came to
describe a bug that had been fixed twelve commits earlier.

**531 passed** (was 516), Python 3.13.14. Not CI-verified — CI is
`workflow_dispatch:` only here on purpose.

---

## 2026-08-02 — a property outside the table that guards against guessing

`CLAUDE.md` § "Wikidata properties and items" exists for one stated reason: "**Do
not guess these** — several plausible-looking IDs are something else entirely
(P1288, for instance, is a German literature encyclopedia, not a genealogy
identifier)."

**`P1545` was not in it, and `genimerge.namelinks` emits it.**
`SERIES_ORDINAL = "P1545"` at line 47, used at line 226 as a qualifier on a P735
statement whenever a person has more than one given name — live code on the path
to `add-names.qs`, a file that gets run against Wikidata.

Confirmed against live Wikidata by `wbgetentities`, the same method the table's
header claims for the rest: **P1545 is *series ordinal*, datatype `string`**. So
the code was right and this is a documentation gap rather than a defect. P2600,
P734 and P735 were re-confirmed in the same call and are unchanged.

Being right is not the same as being guarded. The table is the control against
guessing, and a property outside it is unchecked whether or not it happens to be
correct — so `CLAUDE.md` now also says that anything the code can emit belongs
in the table, and to confirm and add it in the same change.

It has **never appeared in a generated batch**: zero `P1545` lines in the
current `add-names.qs`, because no matched person so far has more than one
given-name token. Correct-by-confirmation, not correct-by-observation, and the
table says so — the first batch that includes one is worth reading closely.

Also, found in the same sweep and much smaller: `cli.py` wrote `"P2600"` into
the `source` column of `matched_all.csv` in one function and tested for it as a
bare literal in two others. Now `SOURCE_EXACT` and `SOURCE_EXPANSION`. Named
because a writer and a reader in different functions should not agree by
coincidence of spelling — **not** because it was a Wikidata-safety problem. It
is a CSV token that happens to share a spelling with the property and never
reaches an edit, and the constant's docstring says exactly that so nobody
"fixes" it into the real property later.

**One thing deliberately not done**, recorded in `queue.md` so a later sweep
does not re-open it as an oversight: the property constants each module declares
for itself were left where they are. They sit next to the code that explains why
they are there, and a shared registry would trade that for uniformity while
`CLAUDE.md` already provides the cross-module view.

Verified behaviour-preserving rather than assumed: `expand --search`, `coverage`
and `quickstatements` re-run, identical output — 245 linked, 209 by P2600 plus
36 by expansion, 3 contradictions — and `git diff reports/` empty.

**531 passed**, unchanged, Python 3.13.14. Not CI-verified — CI is
`workflow_dispatch:` only here on purpose.

---

## 2026-08-02 — the table's rule stops depending on people remembering it

`1f14279` added "**Anything the code can emit belongs in this table** … confirm
it and add it here in the same change" to `CLAUDE.md`. The same weak form
replaced two ticks earlier for the four-prefix claim, and weak here for a reason
already demonstrated in the commit that wrote it: **P1545 sat outside the table
for its entire existence**, and turned up in a grep rather than in anyone's
memory.

`tests/test_wikidata_ids_documented.py` now enforces it. Every `P…`/`Q…` string
literal in `src/genimerge/` must appear somewhere in `CLAUDE.md`, and the
failure names the ID and the line it came from. Offline, no new dependency, and
it would have failed on P1545 the day it was written.

Everything passes today, so this locks in a true state rather than fixing a
break. The sweep behind it: **15 distinct IDs** across the package — ten
properties over six modules, five items all in `names.py` — every one
documented.

**And the item IDs were confirmed, not just counted.** All nine the table names
were checked against live Wikidata by `wbgetentities`: `Q101352` family name,
`Q202444` given name, `Q12308941` / `Q11879590` / `Q3409032` male / female /
unisex given name, `Q5` human, `Q6581097` / `Q6581072` male / female, `Q5727902`
circa. Every label matches. That is worth more than it sounds — `names.py` uses
five of them to decide what counts as a name item, which is what produces "1008
of 2351 surnames have one", the figure sizing a decision currently with the
user. It is right.

**The test is honest about its limit, in the file and in `CLAUDE.md`.** It
checks an ID is *documented*, never that it is *correct*. Confirming one means
asking Wikidata, which is network and stays out of an offline suite, so a typo
added to code and table in the same change passes. `wbgetentities` is still the
only thing that catches that, and the table now carries both dates saying when
it last ran.

Four supporting tests rather than one: the scanner finds real IDs (a broken
regex would make everything else vacuous), the pattern matches quoted values and
not prose mentions (`P1288` appears in `CLAUDE.md` as a counter-example and must
never be read as a value), and the comparison reports an undocumented ID with
its location.

**The same mistake as last time, caught before committing this time.** The
non-vacuity test was first written re-implementing the comparison inline, which
tests nothing — exactly the test discarded from `757da7c`. Extracted
`_undocumented` and pointed both the real check and the proof at it, so the
proof exercises the code that runs.

**537 passed** (was 531), Python 3.13.14. Not CI-verified — CI is
`workflow_dispatch:` only here on purpose.

---

## 2026-08-02 — a wrong report sat in git for twelve commits, and I put it there

Ran the full README pipeline end to end for the first time — twelve commands in
the documented order, all exit 0, everything served from cache. Then checked the
thing worth checking: whether re-running it on unchanged inputs is a no-op.

It was not. `reports/merge.md` changed, and the cause was not non-idempotence.
**The committed file was wrong.** It described an 8766-person, three-export
merge while `out/merged.ged` held 12422 across four. `601f840` wrote it
correctly; `e5a41b8` regressed it; this run restored it.

The regression is mine, and the mechanism is a genuine defect. In `e5a41b8` I
rebuilt the pre-merge tree to find where Hågen Iversen had ranked, with
`merge <three files> -o <scratch>/merged3.ged`. In `_cmd_merge`, `--output`
redirected the GEDCOM and nothing else:

```
output = args.output or ws.merged        # redirected
_write(ws.out / "merge-report.md", …)    # not redirected
_write(ws.reports / "merge.md", …)       # not redirected
```

So a throwaway experiment wrote its GEDCOM to a temp directory and its reports
over the repository's. I staged `M reports/merge.md` in that commit — a commit
about the seeds report — and did not ask why it was there.

**`merge` was also alone in what `--output` meant.** Every other command uses
`args.output or ws.reports / "<name>.md"`, where `-o` names the report. Only
`merge` used it for the data file while pinning the reports to the workspace,
which made the single command whose reports are tracked in git the one where
`-o` did not cover them.

Now the reports follow the file they describe: given `--output`, they are
written beside it; without it, nothing changes. Four tests, one asserting the
property that actually failed — a redirected merge leaves the workspace report
untouched — and one asserting the redirected report describes the *redirected*
merge, since placement alone was never the point.

**Proved non-vacuous rather than assumed.** Both reports had to genuinely differ
or the test would pass either way: the workspace report lists two sources, the
side report one, and the workspace file is byte-identical before and after the
side run.

A warning would have been the cheaper fix and the wrong one. A command that
silently corrupts a tracked file when used the way its own `--help` invites is
not improved by mentioning it.

**What this says about the process is worth more than the fix.** Seventeen
commits, a status report every two hours claiming clean state, and a wrong
report sat in `reports/` the whole time. Nothing caught it — not the suite, not
the sweeps of `todo.md`, `README.md` and `CLAUDE.md`, not `git status`, which
was clean because the wrong file was committed. It took running the documented
pipeline and asking whether the result changed. Idempotence is a property worth
checking directly, and it had never been checked.

**541 passed** (was 537), Python 3.13.14. Not CI-verified — CI is
`workflow_dispatch:` only here on purpose.

---

## 2026-08-02 — a guard for the bug that hid for twelve commits, and a seed with a known payoff

Two things, both following from the previous tick.

**`reports/merge.md` is now checked against `data_lake/` on every run.**
`e9f4cde` fixed the *cause* of that file going stale and added nothing that
would notice the next one. The file was wrong in git for twelve commits with a
passing suite, a clean `git status` — clean because the wrong file was
committed — and a status report every two hours calling the tree healthy.

`test_merge_real_exports.py` already merged the real exports in a module fixture
and already had `test_the_merge_is_idempotent`, so the merge *function* was
covered and the committed *artifact* was not. The new assertion compares the
file against `render_report(report, detail=False, doc=doc)` and costs nothing
measurable — it does not appear in the slowest three durations.

**Proved against the actual historical failure rather than a synthetic one.**
The guard passes on the current file and fails on `e5a41b8:reports/merge.md`,
the exact stale version, and the companion test names what was missing:
`export-Forest-6000000226977233850.ged`, absent from a report that claimed to
describe the data lake containing it.

Deliberately only `merge.md`, said in the test so the omission does not read as
an oversight. `inventory.md`, `frontier.md` and `seeds.md` are equally pure
functions of `data_lake/` but each needs its own regeneration and `seeds` alone
takes about a minute, which would several-fold a 30-second suite to guard
reports that have not gone wrong. `names.md`, `wikidata-coverage.md` and
`wikidata-crosscheck.md` cannot be checked offline at all.

**And the Emperor Jimmu finding is recorded rather than left in chat.** Asked
which people in a Geni relationship chain were in our tree, the answer was that
it stops at **Elisabeth Árpád dynasty `6000000003243185408`** — the following 51
are absent, from Jelena Urošević through the Nemanjić rulers, Constantine IX,
Alp Arslan, the Ashina khagans, the Tang and Kudara lines, the Fujiwara and
Mononobe clans, to Jimmu.

She has no parents recorded, so she is a doorway: ranked 198 of 2932, ball 22, 9
doorways, **41% openness** against a 20% median. The seed is her absent mother,
per the export-from-the-parent rule.

The reason she belongs in `queue.md` and not merely in the ranking is that **her
payoff is observed rather than inferred**. Every seed in `reports/seeds.md` is a
bet on unseen material; Geni has already shown what is behind this door. That
evidence comes from outside our data — the same blind spot that hid Iver
Mellegård, and one no metric here can represent.

Recorded with its limit: an export fills at ~3840 people and Jimmu is ~51 steps
further, so one export reaches the Serbian and Byzantine material and almost
certainly not Japan.

**543 passed** (was 541), Python 3.13.14. Not CI-verified — CI is
`workflow_dispatch:` only here on purpose.

---

## 2026-08-02 — the README's isolation promise, asserted

`README.md` promises that every command takes `--data-lake`, `--out` and
`--reports`, "so a second dataset can be processed without touching the first".
Nothing checked it, and a promise of that shape had already been broken once
this session.

Checked by hand first, against the real repository: `inventory`, `merge`,
`export`, `frontier` and `seeds` run against a temp workspace, then every file
under the repo's `reports/` and `out/` compared before and after. **372 files,
none changed, none added.** The promise holds, so this locks in a true state
rather than repairing one.

Guarded as a family rather than per command, because the failure mode is a *new
or edited* command writing to a workspace-independent path — a per-command test
only ever covers the commands someone remembered to write one for.

Snapshot by size and mtime rather than content hash. Any write updates mtime,
and hashing the tens of megabytes in `merged.ged` and `people.jsonl` on every
run buys nothing; the test says so instead of leaving it as an unexplained
choice. It costs 0.05 s.

**The correction worth recording: this test would not have caught the bug that
prompted it.** `reports/merge.md` went stale because `merge -o elsewhere` ran
*without* `--reports`, so the reports fell back to the repository default while
the GEDCOM went to the target. Every run in the new test passes all three
directories — which was always the safe case. The first version of the comment
claimed the credit anyway, and it was wrong; the shipped version says which test
actually covers that shape
(`test_merge_output_elsewhere_does_not_touch_the_workspace_reports`) and that
this one guards an adjacent property, not the same one.

That distinction is the whole value of the entry. A guard described as covering
a bug it does not cover is worse than no guard, because the next person reads
the failure mode as handled.

Also honest about reach: five of eleven commands. `reconcile`, `expand`,
`coverage`, `crosscheck`, `names` and `name-links` need Wikidata and this suite
is offline on purpose — and they are the likelier place for a stray path, since
they are the ones that also write cache files. Uncovered, and said so.

**545 passed** (was 543), Python 3.13.14. Not CI-verified — CI is
`workflow_dispatch:` only here on purpose.

---

## 2026-08-02 — the billing invariant gets a test, and the test catches itself

Swept the remaining checkable assertions in `CLAUDE.md`. All hold:
`Merger.add_source` does not call `geni_id_of`; the RFN cross-check is present
in `inventory`, `model` and `test_merge_real_exports`; `ci.yml` declares only
`workflow_dispatch`; every import in the package is standard library. Nothing to
fix — which is why the interesting part is what got guarded and what happened on
the way.

Two of those claims are worth a test not for symmetry but for consequence.

**The CI trigger is a money claim.** `CLAUDE.md` forbids `push:` and
`pull_request:` because Actions minutes are billable on a private repository,
and it was enforced by a sentence asking someone to remember. Its failure mode
is the nasty kind: adding `on: push` makes the repository start producing green
ticks, so the thing going wrong looks exactly like the thing going right, and
the first real signal is an invoice. Now asserted, and proved by adding a `push:`
trigger to a copy of the real file and watching the guard fire.

**Stdlib-only is a cold-clone claim.** `pyproject.toml` declares
`dependencies = []`; a stray third-party import keeps working for whoever
already installed it and fails for everyone else.

**Then the stdlib test failed, and it was right to.** It reported
`seeds.py:5` importing a module called `that`. The line is inside a docstring —
"…from that profile until the export is full" — and the reader was a regex
matching `^(import|from)\s+(\w+)`. Prose that looks like code, which is exactly
the trap the trigger reader strips comments for: `ci.yml` explains *why* it has
no `push:` trigger, and a naive search finds the explanation.

Fixed by making the reader correct rather than the assertion loose — `ast`,
which is standard library, so checking the no-dependencies rule adds no
dependency. Relative imports fall out for free: `node.level > 0` is `.model`,
not something to install.

That false positive is now a test of its own, with the actual docstring text
that produced it. It is the second time this session a guard has been caught
reading prose as code; the first was the `P1288` mention in `CLAUDE.md`, which is
why the ID scanner matches only *quoted* identifiers. Worth naming as a pattern:
a repository whose prose discusses its own configuration will fool any checker
that reads text instead of structure.

Both limits stated in the test rather than left to be discovered — it cannot see
whether the workflow is *also* disabled at the GitHub end, which is a remote
setting, nor dependencies introduced at runtime rather than by import.

**553 passed** (was 545), Python 3.13.14. Not CI-verified — CI is
`workflow_dispatch:` only here on purpose, which is now a tested statement
rather than a described one.

---

## 2026-08-03 — a docstring calling a decision a blockage

Went looking at `tests/test_python_floor.py` for a different reason — it is the
stand-in for the 3.10 coverage this session reports as missing every tick, and I
wanted to know whether it could be strengthened. It cannot, much: it already
parses every file with `ast.parse(..., feature_version=floor())`, which is
exactly the right check, keeps a denylist of post-3.10 stdlib names, reads the
floor out of `pyproject.toml` rather than hardcoding it, and carries two
non-vacuity proofs. Sound.

Its docstring was not. "Only CI does that, and CI has stopped running (a GitHub
billing block — see `queue.md`)."

Both halves false. `queue.md` contains no mention of a billing block — zero hits
— and both it and `CLAUDE.md` frame CI as off **by decision**: "CI is off on
purpose, and stays off. Not a blocker — a decision." The phrase survived nowhere
else in the working tree and traces to `3c82da8`, the commit that created the
file.

**The distinction is the whole point, and this was the worst file to get it
wrong in.** A *block* is imposed from outside and might lift; a *decision* is a
standing choice to keep. This is precisely the file somebody opens while
wondering whether CI ought to come back, because it exists to explain what goes
unchecked while CI does not run — so a reader arriving with that question found
an answer implying the obstacle was temporary and external.

Restoring push-triggered CI is the one thing `CLAUDE.md` forbids outright, and
`3474ba7` added a test enforcing it two commits ago. The docstring had come to
contradict a guard in its own suite.

Now it says manual-only by decision, names the reason, points at `CLAUDE.md`
§ "Cost: this repo is private, so CI is manual-only" — heading checked, not
recalled — and notes that `test_repo_invariants.py` makes restoring an automatic
trigger fail the suite on purpose. It also records the thing the old wording
obscured: real 3.10 coverage is available any time via `gh workflow run CI`, and
costs minutes. That is a choice with a price, not an impossibility.

Everything else in the file was left alone. The checks are good and were
reviewed this tick.

**553 passed**, unchanged, Python 3.13.14. Prose only — stated for completeness,
not as evidence. Not CI-verified, which is now a described-and-tested state
rather than a described one.
