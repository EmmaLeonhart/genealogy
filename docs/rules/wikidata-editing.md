# Editing Wikidata: what goes out, and when

**Moved out of `CLAUDE.md` on 2026-09-09, verbatim.** The ruling was to cut `CLAUDE.md`
to under 1,000 lines and put the evidence for each rule on a page that `CLAUDE.md`
cites. Nothing here was reworded, shortened or dropped in the move — this is the
reasoning, the measurements and the post-mortems behind the one-line rules.

---

### Regenerating QuickStatements ALWAYS regenerates the ledger. It almost never rebuilds the tree

**Regenerating QuickStatements always regenerates the ledger, and almost never rebuilds the
synoptic tree.** Two separate inputs, and they are on opposite defaults:

- **The ledger, `reports/garborg-qids.tsv` — ALWAYS.** It is built from the account's Wikidata
  contributions, and those are edited by hand continuously, so a batch built on a stale ledger
  re-creates items that already exist. `--refresh-ledger` is not an option to weigh; it is what
  regenerating means. § *The ledger refresh is PART OF THE RUN* is the same rule from the other
  side — a batch at 17:33 on a ledger from hours earlier reported the Charlemagne spine stuck at
  step 8 when the person at step 13 had just been created.
- **The synoptic tree — almost never.** `scripts/rebuild-everything.py` merges the whole corpus:
  ~14 minutes, ~17 GB, and it has been killed mid-run more than once. It changes nothing unless
  `exports/` has changed, and asking for a batch is not asking for it.

**So the default command is `build-daily-batch.py --refresh-ledger`, and the check for the other
10% is one line:** is any `.ged` newer than `out/merged.ged`? If none is, the merge is redundant.
If one is, say so and ask before merging rather than doing it.

### The batches are a SEQUENCE. The algorithms are invariants, not walls

**The batches are generated in a specific order and run sequentially.** They are
invariance-based algorithms, and reading an invariant as a wall is the recurring failure here.

**Wikidata is faithful: what ran yesterday is there today.** That is the whole basis of the
daily cadence. A batch is not a self-contained unit that must do everything or fail — it is one
step of a sequence, and the next step gets to assume the previous one landed. *"What cannot run
today is tomorrow's batch, because tomorrow those items exist."*

**The rules are INVARIANTS that make the sequence converge.** *A statement goes in only if both
ends already have a QID* is not a limit on what can be built; it is the condition that makes
every batch runnable in full and lets the next one go further. Reading it as *"therefore this
cannot be done"* inverts it.

**The failure mode has a name and a track record: inventing a hard limit, then building around
it.** Three in this repo, all false:

| the "limit" | what is true | what it cost |
| --- | --- | --- |
| *`LAST` is only valid as a subject, never as a value* | `Q… P22 LAST` is ordinary | weeks of one-way links repaired by hand |
| *QuickStatements cannot point at an item a `CREATE` in the same batch just minted* | that is exactly what `LAST` is | 42 name items and every name statement gated behind a phantom, then reported as a blocker |
| *the merges and exports must wait on a person* | Chrome automation runs the loop end to end | an export tagged BLOCKED-ON-USER-ACTION that nothing was blocking |

**The one real limit: two things created in the same batch cannot point at each other.**
Everything else composes — an existing item can point at a new one, and a new one at an existing
one.

**And "relied on weird summaries" is literal.** `build-label-corrections.py` read
`out/garborg-new-items.json`, a summary with no `claims`, `labels` or `aliases`, and printed
*"0 items need correcting"* while 45 needed it. § *A SUMMARY of a Wikidata item is not the item*
already existed; the script predated nobody noticing.

**So, before writing that something is impossible:** try it, or find where this file already
says it works. The transcripts are the authority for these algorithms — not a reconstruction of
what seems plausible.

### A duplicate parent value is SELF-HEALING. Do not report it, do not fix it

**Duplicate parent pairs are self-healing: a bot clears them, and that is intentional.**

After a merge, an item can carry the same parent twice — the survivor and the redirect. On
`Q141180409` and `Q141199734` that reads as `P22 Q141199704, Q141199808` and
`P25 Q141199706, Q141199819`, where the second of each pair redirects to the first.

**This is intended and a bot clears it.** It is not a defect, not a conflict, and not something
to emit a correction for. Traversal is unaffected: both values resolve to the same person, so a
path through them is connected.

**What this forbids:** flagging it in a status report, adding a de-duplication pass, or reading
it as evidence that a spine is broken. It sits in the same family as § *A second Geni ID on one
Wikidata item is NOT a conflict* — an artefact of how Wikidata merges, which the ecosystem
resolves on its own.

### A second Geni ID on one Wikidata item is NOT a conflict

**It is impossible to merge two Geni profiles.** Two profiles for one person is a permanent,
structural feature of Geni, not an error to resolve, and a second `P2600` on a Wikidata item is the
correct representation of it.

**Why it happens:** Geni has rules against connecting biblical people to living
people. So users who want their line to reach antiquity keep **creating fresh
biblical profiles** and attaching to those instead. The duplicates accumulate and
cannot be merged. A second ID usually means the person just is not properly done that way.

Known pairs, both unmergeable:

| person | profiles |
| --- | --- |
| Aaron | `6000000000792907064` · `6000000227239142939` (`Aaron I /Samaritan High Priest/`) |
| Zerubbabel | `6000000000961704850` · `6000000206646432835` (`Zerubbabel-PLACEHOLDER`) |

**So: emit the second ID as an additional `P2600` statement. Never replace the
first, never hold it back as a conflict, never build machinery to adjudicate
it.** `P2600` is multi-valued and the local store already counts **2861 items
carrying more than one Geni ID** — this is ordinary. **751 of those second ids are already
DEPRECATED on Wikidata**, so the live count is **2,110**; `out/wikidata/relations.tsv` drops
deprecated statements and `out/wikidata/p2600-all.tsv` does not, which is the whole difference
between the two numbers and is worth knowing before quoting either.

**Of the 2,110, only 70 have both profiles in our corpus** — everything else we can say nothing
about. `scripts/classify-multi-p2600-by-tree.py` sorts those 70 by what our own tree records
between the pair, and it needs no browser: **41 have no relationship recorded** (the Zerubbabel
shape), **27 are siblings** (the Sapiega shape — Geni holds two people, Wikidata holds one, and
our snapshot matches Geni so there is nothing to do), and **2 are parent-child**, which is a
generation collapsed into one item and the only residue worth opening a page for. It is also the general rule
one section down: *prefer adding a second statement cited to Geni over editing
the existing one*.

`scripts/build-geni-wikidata-pairs.py` implements this; a run that reports these
as "conflicts" has regressed.

### NO descriptions and NO edit summaries. Categorical

**It is a hard rule that items are never created with descriptions**, and the same rule covers
edit summaries: **they are categorically never used.**

### ⛔ THE ONE EXCEPTION: a PATRONYMIC name item carries `Den "patronymic"`. Do not remove it

**All patronymics get the description `patronymic`, so that they are properly deduplicated.**
Without it, duplicate patronymics keep being created.

**The description IS the deduplication mechanism**, which is why it overrides the rule above rather
than breaking it. A label and description must be unique together per language, so two undescribed
`Olsdatter` items are both legal and Wikidata creates the duplicate; a second
`Olsdatter` + `patronymic` is REFUSED at creation. The uniqueness constraint the rule above warns
can BLOCK a creation is here turned round and pointed at the problem.

`DESCRIPTION_FOR` in `scripts/build-garborg-name-items.py` is the authority — `patronymic`,
`family name`, `matronymic`. **A `Den` line on a name-item `CREATE` is correct output. Never strip
it from a batch and never "fix" the generator to stop emitting it.**

**This section exists because the exception lived ONLY in a code comment.** On 2026-09-03 the
categorical rule was read out of this file, matched against three `Den` lines in a live batch, and
reported twice as a defect — with an offer to delete them, which would have reintroduced the
duplication the rule exists to stop. `CLAUDE.md` is loaded automatically; a code comment is not. **A
hard rule stated here whose exception is recorded only in the code will be enforced against the
exception.** So an exception to a rule in this file belongs in this file, beside the rule.

**Both, always, everywhere.** Not a default to override, not a per-batch decision:

* **No `D<lang>` line in any batch**, in any language, on a creation or on an existing item.
* **No edit summary.** No `summary=` on an API call, no custom summary in QuickStatements, no
  free text attached to an edit anywhere. Checked 2026-08-30: nothing in `scripts/`,
  `src/genimerge/` or the workflows sets one, and nothing may start.

**A `#` comment inside a `.qs` file is not an edit summary** -- it never reaches Wikidata -- and
those stay. The rule is about what is written to Wikidata, not about what the repo records.

A `CREATE` block carries labels and statements. It carries **no `D<lang>` line**, in any
language, ever. `queue.md` § *Wikidata person descriptions* is the longer statement of the
order: *"a person always gets labeled before they have a description added to them… We create
the individual with their multi-language label, their English language label, their Japanese
… but no descriptions are added to any of the people."*

**The reason is Wikidata's uniqueness rule, and it cuts both ways.** A label and description
pair must be unique per language, so:

* an existing item with a description **and no label** cannot be given the label if that pair is
  taken -- by far the worst trap;
* and two items sharing a label with **no** description are also the same pair, so the second
  `CREATE` is refused.

**Measured 2026-08-30 on a live batch: 3 of 22 creations would have been refused** --
`Anna Martens`, `Per Nilsson`, and a bare `NN`, each colliding with existing undescribed items.
`scripts/check-label-collisions.py` is the pre-flight check; it reads Wikidata and writes
nothing.

**So a collision is resolved by HOLDING the creation, never by adding a description.** The
carry-forward already exists for exactly this shape of "not today", and using it keeps the hard
rule intact.

### `P3373` sibling is capped at 40 PAIRS a day — doubled twice, 10 → 20 → 40

Sibling relationships are too numerous to send at once, so sibling adding is capped. The cap
started at 10 statements a day and has been doubled twice, along with every other per-run batch
size in the repo. The reasoning below is why there is a cap at all; only the number moved.

**The number that provoked it:** `reports/wikidata-reciprocals.qs` came out **257 statements, 160
of them `P3373`** — 62% of a batch, all siblings. Sibling links grow as the *square* of a family's
size, because every child is a sibling of every other: one family of nine children is 72 `P3373`
statements on its own. Parents grow linearly. So a batch that looks balanced by people is
overwhelmingly sibling links by statement.

**The cap is 40 `P3373` sibling PAIRS per day, across every batch**, not per file. Both
directions are emitted, so counting statements made a cap of 20 mean **10 pairs**; it counts the
unordered pair now. A full run comes out at about 79 lines. A builder emitting
siblings must count them and stop.

**It is a pacing rule, not a correctness one.** The links are right; there are simply too many of
them to send in one batch. The rest stay in the carry-forward and go out on later days, which is
the same mechanism the daily cadence already uses.

**The RELATIONSHIP properties are not capped.** `P22` *father*, `P25` *mother*, `P40` *child*
and `P26` *spouse* stay uncapped — they are few per person and each one is structurally
load-bearing. This said *"nothing else is capped"* until 2026-09-09; the name statements and
the `P2600` lead are capped now, § *THE ADDITIONS PASS IS CAPPED TOO*.

### ⛔ THE ADDITIONS PASS IS CAPPED TOO. `NAME_ADD_CAP` and `P2600_LEAD_CAP`

**A 4,081-statement batch carried uncapped Geni ids and uncapped name statements. They are
capped now.**

**This supersedes the sentence in § *`P3373` sibling is capped at 40 PAIRS* that read "Nothing
else is capped."** That was true and safe only while another guard happened to be suppressing
the traffic.

**What was uncapped, measured:** the additions pass iterates the **whole ledger**, and on
2026-09-09 it emitted **2,033 name statements on 1,269 existing items in one batch** — 1,192
`P735`, 748 `P734`, 93 `P5056`, **62% of the file** — plus 47 `P2600` where the cap says 20.

**The cause was a fix made the same day, and that is the part worth knowing.** Removing
`_has_given_name` was right — it was withholding 6,978 statements from people who were owed
them — but the pass it unblocked had no pacing of its own, so a correct fix arrived as a flood.
**A guard that suppresses volume is not a cap**, and removing one exposes whatever it was
standing in for.

| | cap | unit |
| --- | ---: | --- |
| `NAME_ADD_CAP` | **60** | people per run gaining `P735`/`P734`/`P5056` on an EXISTING item |
| `P2600_LEAD_CAP` | **40** | the exempt `P2600` lead, on top of `MANUAL_P2600_PER_RUN` 20 |

**60 people, the same unit and number as `LABEL_EDIT_CAP`**, because it is the same shape of
work: a rolling window over the ledger that drains a little each run. Nothing is lost — what does
not go today goes tomorrow, § *The batches are a SEQUENCE*.

**⛔ THE CAP COUNTS PEOPLE WHO GAIN A STATEMENT, NEVER PEOPLE WHO REACH THE BLOCK.** Counted on
arrival it burnt 48 of the 60 slots on people whose tokens have no name item yet: **60 people
entered and 12 statements came out**, so the pass drained five times slower than the number says
while looking correct from the outside.

**The `P2600` lead stays exempt from `MANUAL_P2600_PER_RUN` and that is still right** — never
label an item whose id is being withheld, § *An item with no relationships is not a missing
item*. But exempt is not unbounded: the lead is *"every QID this run touches"*, so it grew as a
function of the flood. Capping the pass fixes it at the cause and `P2600_LEAD_CAP` is the
backstop.

**Result on the same run: 3,272 statements → 1,359**, existing items touched 1,269 → 202,
`P2600` on existing items 47 → 7. `P22`, `P25`, `P40` and `P26` stay uncapped — 149 statements
between them, few per person and structurally load-bearing, which is the reason § *`P3373`
sibling* gives and which still holds.

### A sibling step gets a PLACEHOLDER PARENT in our tree and NEVER on Wikidata

**The two stores get different answers, and that is the whole ruling:**

| store | a sibling step becomes |
| --- | --- |
| **Wikidata** | `P3373` *sibling*, directly between the two people. **No parent item is invented.** |
| **the synoptic tree** (the Geni union) | a **placeholder parent profile**, which is what makes the network position readable |

**Why the split is not an inconsistency.** Geni records no sibling edge — `CLAUDE.md` § *A
sibling step is the worked example* — so two siblings are joined only through a shared parent,
and GEDCOM has no way to say *sibling* without one. Our tree therefore needs the placeholder to
express the fact at all. Wikidata has `P3373` and needs no such prop, so inventing a parent item
there is a claim about a person nobody has evidence for, in the one store § *The purpose is to
ADD to Wikidata* makes hardest to undo.

**This is the same shape as § *Redacted people go in*:** the structure is what is informative,
and you assert only the part the data supports. A placeholder parent in our tree is scaffolding
we control and can re-derive from the exports; a placeholder parent item on Wikidata is a person
asserted to have existed.

**Scale, measured 2026-09-03: 2,125 sibling steps of 30,329, 7.0%, across 662 of 696 path
files.** So this governs nearly every path rather than an edge case. Note the interaction with
the section above: routing all of it through `P3373` puts it under the **20-a-day cap**, which
is a pacing limit and not a reason to reach for parents instead.

**The parent-adding campaign comes LATER and is not started here.** It runs once the placeholder
parents have been gathered and a batch of them is on Wikidata, using `Forest` exports at closely
related eccentric graph points. So the placeholders accumulate in our tree first; the campaign that turns them
into real people is gated on that, and on `Forest` exports seeded at eccentric points — the same
instrument § *"Not related to" does NOT mean not related* uses for eccentric targets.

### Always write the English label next to a property or item ID

**A bare property or item ID is unreadable.** Write **`P5056` *patronym or matronym***, **`Q110874` *patronymic***, **`P7338` *regnal ordinal***. This applies
in chat, in reports, in queue items and in commit messages — everywhere a bare ID
would otherwise appear.

`reports/wikidata-labels.tsv` has the label for almost every ID this project
touches, so there is no excuse for a bare one and no reason to guess: looking it up
is a grep. Guessing is also how `Q28513` got written down as *Empire of Japan* when
it is **Austria–Hungary**, which produced 1,406 fake Japanese isolates.

### Wikidata properties and items

All confirmed against live Wikidata via `wbgetentities` on 2026-07-30. On
2026-08-02, P1545 was added and P2600 / P734 / P735 plus **every item ID named
below** — `Q5`, `Q6581097`, `Q6581072`, `Q202444`, `Q12308941`, `Q11879590`,
`Q3409032`, `Q101352`, `Q5727902` — were re-confirmed the same way. Every label
matched. **Do not guess these** — several plausible-looking IDs are something
else entirely (P1288, for instance, is a German literature encyclopedia, not a
genealogy identifier).

**Anything the code can emit belongs in this table, and
`tests/test_wikidata_ids_documented.py` enforces it**: every `P…`/`Q…` string
literal in `src/genimerge/` must appear somewhere in this file, or the suite
fails naming the ID and the line it came from. P1545 was missing for a while
despite `genimerge.namelinks` emitting it, which was harmless only because it
happened to be right — a property outside this table is unguarded whether or not
it is correct.

That test checks an ID is **documented, never that it is correct**. Confirming
one means asking Wikidata, which is network and stays out of the suite, so a
typo added to code and table in the same change still passes. `wbgetentities`
remains the only thing that catches that, and the dates above say when it last
ran.

**Identity and structure**

| ID | label | datatype |
| --- | --- | --- |
| P2600 | Geni.com profile ID | external-id |
| P1810 | subject named as | string — **qualifier on `P2600`**, carrying the name *Geni* renders, from `display_name` in `reports/display-names.csv` and never our own label. Datatype and placement confirmed offline against `wikidata/items/`, where every `P1810` is a `string` qualifier on an external identifier (`P396`, `P1280`, `P8034`, `P12458`). **A REDACTED person gets no `P1810` at all.** There are two kinds of `private` on Geni — a backend difference that affects the GEDCOM export while displaying identically — so neither form belongs in the qualifier. Both forms are in the corpus — `<private> /Surname/` **19,945** and bare `Private` **99,645** — and Geni displays the same thing for both, so which one a profile exports as says nothing about the person. `Q141223549` is the case: `P1810 "Private"` where the site shows `<private> Paulson`, a surname that is in none of the five exports holding that profile. `tests/test_garborg_day_batch.py` pins that no marker reaches the qualifier. |
| P31 | instance of | item — value `Q5` human |
| P21 | sex or gender | item — `Q6581097` male, `Q6581072` female |
| P22 / P25 | father / mother | item |
| P26 | spouse | item |
| P40 | child | item |
| P3373 | sibling | item |

**Life events**

| ID | label | datatype |
| --- | --- | --- |
| P569 / P570 | date of birth / date of death | time |
| P19 / P20 | place of birth / place of death | item |
| P119 | place of burial | item |
| P2842 | place of marriage | item (qualifier on P26) |
| P106 | occupation | item |
| P97 | noble title | item |
| P535 | Find a Grave memorial ID | external-id |
| P4602 | date of burial or cremation | time — burial is **two** properties with P119, never a qualifier |
| P6375 | street address | monolingual text — where a GEDCOM `ADDR` block goes |

**Names** — the part of `todo.md` that needs new items created

| ID | label | datatype |
| --- | --- | --- |
| P735 | given name | item — name items are `Q202444` given name, or `Q12308941` male / `Q11879590` female / `Q3409032` unisex given name |
| P734 | family name | item — name items are `Q101352` family name |
| P1950 | second family name in Spanish name | item (not applicable here) |
| P1477 | birth name | monolingual text |
| P1559 | name in native language | monolingual text |
| P1545 | series ordinal | string — **qualifier**, ordering several given names, and ordering the links of a chained patronymic |
| P5056 | patronym or matronym | item — **the property a patronymic uses**, parallel to `P735`/`P734`, per `name modelling.txt`. Not a qualifier on `P735`. |
| P7452 | reason for preferred rank | **qualifier** — value `Q3409033` *usual forename* on the first given name |
| Q3409033 | usual forename | item — the `P7452` value. **Not** `Q3409032`, which is *unisex given name* |
| P7338 | regnal ordinal | **qualifier** on the given name — `Robert VII` is `P735` Robert + `P7338` VII. Every regnal order goes on the name as a qualifier, and **not only for the Samaritans** — anyone whose name carries an ordering. Confirmed offline against `reports/wikidata-labels.tsv`. Distinct from `P1545`, which orders a person's several given names rather than the person among namesakes. |
| P3831 | object of statement has role | item — **qualifier** saying *which kind* of name this `P735` is |
| P144 | based on | item — **qualifier on `P5056`, pointing at the PERSON that link names**: the father, then the grandfather for a chained patronymic. `name modelling.txt` supersedes the earlier reading of this as a name-item-to-name-item link. |
| P5278 | surname for other gender | item — pairs `Olsson` with `Olsdotter` |
| P460 | said to be the same as | item — between two SPELLINGS of one patronymic, both ways; `Olofsson` `Q141244186` and `Olai` `Q141313056` were linked by hand as the worked case. Emitted only where the two items share a `P144` source, a stem and a gendered suffix: a shared source alone matches `Jonsdatter` to `Johansdotter`, which are different names one father was recorded under. A gendered pair is `P5278`, not this. |
| P1814 | name in kana | **string, NOT monolingual text** — confirmed against `wbgetentities` on 2026-09-02, where `P1477` and `P1559` really are `monolingualtext` and this is not. The table said monolingual text and nothing had emitted it, so the error was harmless until a survey of 151 items reported **0 carrying it** when 45 do: the reader demanded a `{text, language}` dict and `P1814` stores `{"value": "おいちのかた", "type": "string"}`. A QuickStatements line therefore takes a bare quoted string with **no language prefix** — `Q635214	P1814	"おいちのかた"`, never `ja:"…"`. The Japanese reading of a name written in Han characters; **nothing emits it yet**, and a kana reading is not derivable by rule from the characters — it is found, not generated. |
| P1449 | nickname | monolingual text — **modelled but NEVER EMITTED**; see § *A nickname alias carries the SURNAME*. A quoted token inside `GIVN` is still read as a nickname — `Stine "Stena" Eivindsdatter` makes *Stena* a nickname, **not** a given name and **not** a middle name — and it becomes an `Amul` alias rather than a statement |
| Q2507958 | birth name | item — the `P3831` role on the `SURN` family name, when a married one sits beside it |
| Q28418670 | married name | item — the `P3831` role on the `_MARNM` family name |
| Q245025 | middle name | item — the `P3831` value for a middle given name |
| Q110874 | patronymic | item — the `P3831` value for a patronymic, which is also what the name item is an *instance of* |
| Q1076664 | matronymic | item — what a MATRONYMIC name item is an *instance of*, the sibling of `Q110874`. *"personal name component based on ones mother's given name."* Supplied by hand rather than guessed, since no offline source here holds it: § *A MATRONYMIC DERIVES FROM THE MOTHER* is the rule and this is its class. The person still carries `P5056` *patronym or matronym* — one property for both — so only the name item's `P31` and its `Den "matronymic"` description differ from a patronymic's |

**A diacritic makes a different name, and folding it away invents ambiguity.**
`Maria` matched nine Wikidata items, and almost all of them were diacritic variants rather than
the same name. `María` (Spanish), `Mária` (Hungarian) and `Marià` (Catalan) each
have their own Wikidata item on purpose. `measure-name-resolution` folded them
together, which manufactured ambiguity for **1,312** names and blocked them all
from being created or linked; keeping the diacritic cut that to **525** and moved
1,545 names from "create" to "link". Case and whitespace fold; nothing else does.

The genuine residue is `Q325872` and `Q25413386`, the **male**
and **female** given name `Maria`. That is settled by the *person's* sex, not by
the string, and neither item is in the local store yet.

**One name item per USAGE, not per string — "Jackson Jackson Jackson".** The worked example:
somebody whose given name is Jackson, whose surname
is Jackson, and who carries a patronymic Jackson **because their father is Jack
Jackson**. That is *"a different object for all three usages"* — a given-name
item, a family-name item and a patronymic item, three separate Wikidata items
that happen to share a spelling.

So a token appearing in more than one slot is **not an ambiguity to resolve**.
This was got wrong on 2026-08-15: the name census built a dominance ratio and a
bearer floor to decide which slot a token "really" belonged to. **If something is a surname and a
given name, it gets a surname object and a given name object** — two completely different things
with completely different objects. All the adjudication machinery was deleted.

**Where a real ambiguity does exist, ask** rather than figuring it out alone — whether Jackson is
ever a *middle* name is that kind of question.

**A middle name is a given name after the first that is NOT a patronymic.**

So position alone does not make a middle name — the second given token is a middle
name **only** if it is not patronymic. `Q245025` and `Q110874` are decided by what
the token *is*, and `P1545` numbers them either way.

### The Geni BIO carries hand-written QID claims. Read them before any download

**The bio QIDs are used.** `wikidata.org/wiki/Q…` written into a Geni profile's *About Me* comes
back inside the export as text on that person's record. `scripts/extract-bio-qids.py` → `reports/bio-qids.tsv`
attributes each link to the `INDI` that owns it: **158 pairs over 155 profiles, in 156 of the 600
exports**. That is a hand-written statement of identity, captured whenever an export next ran —
fresher than anything downloaded.

**Why it matters that this is read first.** Through the bio links the 204 Izumo roster QIDs
give **8** Geni ids; through `out/wikidata/p2600-all.tsv` they give **2**. The honest reading of
8 is that the bio-link campaign has barely reached that family.

**And the 2 is NOT staleness — that was assumed and then refuted.** The file was refreshed from
live Wikidata on 2026-08-30 and the Izumo answer did not move: only **2 of those 204 items carry
a `P2600` at all**. The stale-file reasoning was written down here and in the script before
anyone ran the refresh that would have tested it. § *CHECK before raising an alarm* is the rule it
broke; a cause is not established by being plausible.

**The refresh was worth doing for a different reason, and that one is measured.**
`reports/garborg-qids.tsv` went from **258 of 849** items resolving to **849 of 849** — 591
hand-made items were invisible to the forty scripts that read this file. The row count moved only
+1,124 (517,851 → 518,975), which is why the staleness never announced itself.
`scripts/refresh-p2600-all.py` does the fetch in sixteen partitions without the corpus merge
that `genimerge overlap` drags along, and refuses to write a short fetch.

**A profile may name more than one item** (3 do), and that is § *A second Geni ID on one Wikidata
item is NOT a conflict* seen from the other side. Emit both.

### The tree and the items are edited BY HAND, continuously. Snapshots go stale in minutes

A downloaded item file is a photograph, not a mirror. Labels are fixed, Geni profiles merged and
relationships added by hand while a batch is being built, so:

- **Re-download immediately before emitting a correction**, never from a file fetched earlier in
  the session. A correction computed against a stale snapshot re-writes work already done, which
  is worse than doing nothing.
- **Say when a hand-off was verified.** "Checked live at <time>" is the useful claim; "the item
  has X" without a time is not.
- **A hand-changed label is a decision, not drift.** `Q141168785` had `en` and `mul`
  hand-corrected to the married form while `ja` still read the birth form — the stale half was
  ours.
- The ledger `reports/garborg-qids.tsv` has the same problem and is refreshed from the account's
  Wikidata contributions; a stale ledger is what made a batch try to re-create 21 people that had
  just been made.

### A SUMMARY of a Wikidata item is not the item. Download the full item

**The modelling comes from downloading the full Wikidata items, never from reading an edit
history to see what is in them.**

Reading an item through a fetch-and-summarise channel produced **three false findings**
in one session, each published to a report, the artifact and a commit message:

- **`Q467497` Arne Garborg was reported as having no `P22`, no `P25` and no `P3373`** —
  answering `ABSENT` even to a question posed narrowly to be reliable. The full item has
  all three. It was written up as *"the single highest-value outstanding edit in the
  programme"*. There was no edit.
- **The citation split was reported as inconsistent.** Counted over all 14 full items,
  `P2600` is **never** a reference on `P31` or `P21`. The modelling note it "corrected"
  had been right.
- **Property labels were invented** — `P2600` as "Peruvian NLB", `P1411` as "Nobel Prize
  recipient" — and `Q467497`'s 126 properties arrived truncated and out of order, which
  was the visible tell.

**So: anything that decides what to emit is read from downloaded JSON.**
`genimerge.wikidata.full_entities` fetches whole items in one batched request;
`scripts/garborg-modelling.py` is the worked example, deriving the whole model offline
from `out/garborg-full-items.json`. A summariser may be used to *find* something, never
to establish that a property is absent — absence is exactly what it gets wrong.

**The local store is not a substitute either.** It was downloaded before most of these items
existed, so it agreed that Arne had no parents. An item edited since the download must be
re-fetched, not looked up.

### Querying Wikidata is ALLOWED. Be polite about the rate

**Wikidata may be accessed for basically any task, under reasonable API policies.** The one
thing that is not allowed is running millions of requests to finish faster.

**So: query it.** Resolving a redirect, checking whether an item really carries `P22`, reading a
label — all of that is ordinary work now, not a rule violation. The constraint that remains is
**rate**, and it is about courtesy to Wikidata rather than about permission: batch where an API
offers batching (`wbgetentities` takes 50 ids), do not fan out one request per item when one
request would do, and do not hammer to finish faster.

**⛔ AND WE WERE 429ed, MEASURED 2026-09-07 in pipeline run 246.** *"Your bot is making too many
requests"* — **every chunk of every live read in `build-garborg-name-items.py` failed**: all 137
chunks of the description check over 6,833 items, then both chunks of the `P144` check, which
inherited the throttled state. So the whole existing-item enrichment emitted nothing that run —
`0 P144 to add`, `0 P460`, and `0` of the `P144` removals — while printing it as *"held, the live
read failed"*, which reads as a soft note rather than as the feature being dead.

`live_name_items._get` was the hand-rolled client with no pacing and no retry, next to
`genimerge.wikidata`, which has had a delay, `Retry-After` and a back-off ladder all along. It now
has the same, in `_get` because that is the one place every caller goes through. And
`GIVE_UP_AFTER = 5` stops a pass that is plainly being refused, because retrying turns a fast
total failure into a two-hour one — the same shape as the edit runner stopping after five
refusals. **A hold that fires on every item every run is indistinguishable from the feature not
existing**, which is why the pacing and the give-up go in together.

**What survives from the old rule, because the reasoning was never wrong:** the offline store under
`wikidata/items/` with its index is still the right first place to look — it is faster, it costs
Wikidata nothing, and a question answerable there needs no request at all. Reach for the network
when the store cannot answer, not before.

### An item with no relationships is not a missing item. Geni ID first, then everything else

**The Samaritan high priests are on Geni AND on Wikidata.** What they lack on Wikidata is *genealogy*:
*"they aren't really genealogical entries. They are just individuals… They just
are individuals without any relationships and such."* Reporting them as absent
was the § *"Is X present?"* failure again, one section down, in a new costume —
present as items, absent as a family tree.

**`Q232803` *Empress Jingū* is the worked example.** 38 sitelinks, `神功皇后` in `ja`, and
**no `P2600`** — present as an item, absent as a family tree, which is the whole shape. It is
just a Wikidata object, linked the way any other Wikidata object is linked; there is nothing
special about it.

**So the order is fixed, and it generalises to every merge:**

1. **Add the `P2600`.** The Geni ID must be present before any property derived from Geni can be
   taken from it, and before any relationship is added.
2. **Then everything Geni supports**, each statement cited to that Geni ID.

The same order applies wherever the trees are merged further: the Geni ID first, everything
derived from Geni after.

### THE THREE LINES. This is what the Garborg programme is building

**Three lines: Charlemagne → Bergitte, Bergitte → the account owner, Bergitte → Arne.**

**Bergitte Gunnbjørnsdatter Aukland** `6000000002481819312`, 1465–1522, is the hinge. Confirmed by
walking our own tree, not assumed: **she is an ancestor of both the account owner and Arne**, Arne
at depth 11.
She is *not* their nearest common ancestor — that is **Rasmus Ingebretsen Grude**
`6000000003492045766` (owner +10, Arne +5), and they share **2,780** ancestors in all. Bergitte
matters because she is the one on both lines who is **herself descended from Charlemagne**, which
is what `queue.md` meant by *"Bergitte is the bigger target one"*.

| line | source | people | have items | **to create** |
| --- | --- | ---: | ---: | ---: |
| **1. Charlemagne → Bergitte** | `paths/charlemagne-to-arne-garborg.tsv` steps 12–34 | 23 | 9 | **14** |
| **2. Bergitte → the owner** | Geni: *13th great grandmother*; steps not yet captured | ~15 | ? | ? |
| **3. Bergitte → Arne** | `paths/charlemagne-to-arne-garborg.tsv` steps 1–12 | 12 | 3 | **9** |

**Lines 1 and 3 are one saved Geni path**, `paths/charlemagne-to-arne-garborg.tsv` — 34 steps,
Arne up to Charlemagne, passing through Bergitte at step 12. It was generated by
`genimerge path-from-html` from a saved page and it is the authority. **Read it before
deriving anything**: `reports/charlemagne-route.csv` is a *different* 399-step owner→Charlemagne
descent up another branch that does **not** contain Bergitte, and treating the two as the same
thing has already produced wrong answers.

**Line 2 does not exist yet and is the missing piece.** The account owner descends from Bergitte by a
different line from Arne's, and no saved page covers it. It needs the standard handling: save the Geni
relationship page, then `python -m genimerge path-from-html <page> -o paths/<name>.tsv`.

**Where the gap actually is.** Of the 34 on lines 1 and 3, **22 need creating, and 19 of them are
consecutive** — steps 4 to 22, the whole Norwegian and Swedish middle: Mele, Nedre Rossavik,
Mjølhus, Tengs, Lejon, Algotsson, Svantepolksdotter, Guttormsdatter. **The medieval royal end is
already on Wikidata**: Guttorm Àsulfsson `Q19061035`, Judith of Flanders `Q273181`, Baldwin IV
`Q378177`, Berengar II `Q314521`, Louis the Pious `Q43974`, **Charlemagne `Q3044`**. Only three
gaps up there — Rozala of Italy, Berengar I, Giséle of Cysoing.

So the line closes at **step 23, Guttorm Àsulfsson à Rein**, the deepest person who already has an
item. Create steps 4–22 and Arne is continuously linked to Charlemagne.

**Nineteen consecutive creations cannot link TO EACH OTHER in one batch** — but each of them can
be linked to anybody who already has a QID, in both directions, in that same batch.
**`LAST` IS valid as a value; the limit is narrower than this repo long claimed.**
`Q141178381 P22 LAST` is ordinary QuickStatements — the subject already exists and `LAST`
resolves to the item created just above. What cannot be done is linking **two items created
in the same run** to each other, because `LAST` names only the most recent one.

Two-way relationship adding at creation time is entirely possible: it goes `QID PID LAST` rather
than `LAST PID QID`. Believing otherwise cost weeks of one-way links, repaired by hand.

So a spine batch needs a second file only for the links **between two people it is creating**.
`scripts/build-missing-reciprocals.py` is that second half, and it is much smaller than it was:
`scripts/build-garborg-day.py` now emits `Q… P… LAST` for every relationship to an existing item.

**All four of these lines are COMPLETE, and they are legacy.** The spines are all clear.
`reports/the-spine.md`, which carried the person-by-person state,
is deleted; the section above is kept as the record of what the three lines were and why Bergitte
is the hinge.

**One spine is live and it runs on a different rule** — `paths/arne-garborg-to-johannes-bureus-geni.tsv`,
Geni's own in-law route joining Arne Garborg and Johannes Bureus **to each other** rather than
through the account owner. **Any step is added whenever possible, from any side including the middle.** So
there is no front and no hop-a-day: every step that can be created is
created in the same run, and the only gate is being in the corpus. `SPINE_PATHS` in
`scripts/build-garborg-day.py` holds it, and `SPINE_REVERSED` is empty because that path is stored
Arne-first and grows from no particular end.

**No export is to be attempted on it.** Steps 9, 10 and 13 were tried as `Forest` seeds on
2026-08-30 and Geni refused all three — *"You are not allowed to export that profile."* The path
is the deliverable.

### The Wikidata link goes in the bio during the SYNOPTIC TREE BUILD. Geni is not edited

**Revising an earlier instruction to edit Geni profiles:**

> *"Actually, no, I realised we don't actually need to edit your geni at all for this. Editing
> geni is actually a step that makes stuff much more complicated than it actually should be. In
> the Synoptic tree, we put the Wikidata links into bios during the build process of the Synoptic
> tree. We put the Wikidata IDs in the bios of the final product, although I do want to check all
> the IDs to ensure that they haven't been merged or anything... Forcing them into this Synoptic
> tree like this makes it so that the Synoptic tree, when it starts being used as an input, does
> use them properly, in the zipper merge thing."*

**So the injection is into the merged output, not into Geni.** No browser, no bio edits, no
re-exports for this purpose. The QID is written into the person's bio field in the synoptic tree
as it is built, so that anything consuming the tree — the zipper merge above all — sees the
correspondence as ordinary tree content rather than needing a side file.

**The IDs are checked for merges first**, and offline: *"it really should be on our export of
Wikidata, because that's effectively what it works on."* Redirects resolve to their target.

**What the bio link is FOR:** when the synoptic tree is merged, the bios become links to the
QIDs, so that the next step — the Wikidata union, not yet implemented — joins those people to
those items. So it is a step
*inside* the build, feeding the **Wikidata union**, which does not exist yet. It is not a Geni
editing task that can be run early, and there is no export campaign attached to it.

**This supersedes an earlier plan that is still in the transcripts**, which had eight
hand-resolved people getting their bios edited immediately and a `Forest` export each. A
cron carrying that plan died in the 2026-08-28 crash; it was recovered on 08-29 and handed back to
back as live work, when a later ruling had already replaced it.
**A transcript is not the authority when this file holds a later ruling on the same thing** — the
replacement was already written down two paragraphs up, and reading it would have been enough.

**So the correspondence belongs in the TREE, not in a side file.** Do not act on it yet: the
entity-resolution work is important, and it has been presented as more important than it is.

### The seed set is the WIKIDATA SUBGRAPH from Arne. Not the ledger, and never a hop count

**The algorithm is based entirely on anyone on the continuous subgraph currently on Wikidata
from Arne.** No counting hops — it should do a billion hops under the constraints if possible.

**A person may seed a ring when Wikidata already connects them to Arne** by any chain of `P22`
*father*, `P25` *mother*, `P26` *spouse*, `P40` *child* or `P3373` *sibling*, however long.
`build-garborg-day.wikidata_subgraph()` walks it from `Q11959067` *Arne Olaus Fjørtoft
Garborg*. Measured 2026-08-28: **97 items, containing 96 of 171 ledger people.**

**The ledger is a different question and both are needed.** `reports/garborg-qids.tsv` answers
*does this person already have an item* — it must stay whole, or the batch re-creates things.
The subgraph answers *may the ring grow from them*. Conflating the two is what put a
7th-century Baekje royal, Carolingian Friuli, `Okoshi Mononobe` and `Saburou Kitashima` in a
Garborg batch of 36: the ledger is **every item ever made by hand**, including the Izumo and
Kitajima work, and the ring grew around all of it.

**This is what makes the spine self-limiting, with no special case.** Spine people play no role
because they are not part of the subgraph, which is stored and grown from the account's
contributions. A medieval couple the spine created yesterday
has no path to Arne on Wikidata yet, so it seeds nothing. It needs no exclusion, no flag and no
list.

**Exclusion lists are a smell here.** If the algorithm is followed, exclusions are not needed —
under the subgraph rule the account owner is not a seed and neither are the Kitajima people,
because nothing on Wikidata connects either to Arne.

**Two things that are NOT the algorithm and were invented here, both now deleted.** A
*distance-from-Arne radius*: it appears nowhere in the specification, and bounding the pool to
the immediate ring cut a batch from ~30 people to **7** because the caps stopped binding — 2 of
10 children, 0 of 10 parents. And *ordering the ring by closeness to Arne*, which `11295af7`
did over **our Geni tree**; that is the closest thing that ever existed, and it is not this.

### Entry points DRIP IN on a date. `reports/entry-points.tsv` is the timer

**Entry points drip in on a timer.** Robert Ettinger is an entry point now; George R.R. Martin
becomes one on October 1. Other people are probably worth dripping in, and which ones is an open
question.

**The timer is a DATE COLUMN, never a cron.** `reports/entry-points.tsv` carries
`qid, geni_id, label, active_from, note`, and `subgraph_roots()` includes a row once
`active_from <= today`. A cron here is session-local and dies with the session — § *A cron only
fires while the session is idle* records one starving for four hours, and every cron died in the
2026-08-28 crash. A date in a tracked file cannot be lost, needs nothing running on the day, and
makes switching someone on a property of the repo. Adding the next person is one line.

**Resolve an entry point's QID from OUR OWN DATA. Do not reach for Wikidata.**
`reports/derived-labels.csv` already
carries the qid beside the Geni id for everyone in the tree, so a `wbsearchentities` call for a
person we hold is a request that answers nothing a local join does not. § *Querying Wikidata is
ALLOWED* permits it and § *the offline store is the right first place to look* still decides
where to start; the network is for what the store cannot answer.

**The two named entry points, resolved that way** — § *Do not guess these*, joined on the label in
`reports/derived-labels.csv`:

| | QID | Geni | live from |
| --- | --- | --- | --- |
| **Robert Chester Wilson Ettinger** | `Q714044` | `6000000003022010249` | **now** |
| **George R.R. Martin** | `Q181677` | `6000000081001962237` | **2026-10-01** |

**Both are textbook service areas by the specification, measured.** Neither states a single
`P22`, `P25`, `P40` or `P26` on Wikidata, so each reaches exactly itself there — and § *THE EDIT
ALGORITHM* wants exactly that: *"something that has a GeniID but is otherwise isolated."* In our
Geni tree both are richly attached — Ettinger has parents, 2 spouses and 2 children, Martin has
parents and 2 spouses — and both sit in the main **1,446,089**-person component, so each has a
ring from its first day.

**The run prints LIVE and PENDING every time.** A timer nobody can see is a timer nobody can
check, so the day one switches on shows in the output rather than being inferred.

**Who else drips in is an OPEN QUESTION**, not a brief to go ranking candidates — § *No
unprompted reports* governs. Roots are cheap and reversible; the constraint is which people the
graph should be grown from, and that is decided rather than computed.

**And the roster stays at ABOUT 250.** Dripping in is a trickle, not a campaign — the count is a
property of the design, not a number to grow.

**The two are entry points for DIFFERENT reasons, and the `note` column records which.**
Ettinger is important enough to be an entry point in his own right; Martin is interesting for his
eccentricity, which is a position on the graph. So there is no single criterion to generalise
into a filter, and inventing one is what § *Do not grab the first artifact that vaguely matches*
warns against.

**Eccentricity is measured now: `reports/eccentricity.md` and `tree-eccentricity.csv`**, all
1,451,964 people. The headline matters for reading the word: **Martin is at the 80th percentile
of distance from Charlemagne, not the edge** — 40 hops against a median of 34 and a maximum of
183. His eccentricity is a property of **Geni's** World Tree, where the query has to cross the
sparse part and times out; our corpus is a sample of Geni, so someone we sampled well looks
central here. § *Presence measures our sampling, never Geni's content* is why the two cannot be
substituted. The far edge of our own tree is the Chinese legendary lineage (少昊 Shaohao at 183)
and, among people carrying a QID, the Samaritan high priests at 131–134.

**Eccentricity is PARTLY A RECENCY MEASURE.** Ettinger scores high largely because he was added
recently. Measured over the 602 exports: **Ettinger is in 4,
Shaohao in 1**. A person one export reached sits wherever that export left them, and expanding
around them pulls them inward — so a high score can mean *we have not sampled here yet* rather
than *this person is structurally peripheral*. Two people is not a correlation and is not offered
as one; the full version is a `genimerge.density` presence count against the file, unrun.

### ⛔ "MANUAL ENTITY RESOLUTION" IS A MISLEADING NAME AND IT IS THE ONE TO GET RIGHT

**The vague name is the risk.** *Artifact entity resolution* is not *manual entity resolution*,
and calling it that is extremely misleading: the right name is **manual parental zipper merge
correspondences**, because a vague title will be abused by later sessions for other purposes.

**So `reports/manual-identifications.csv` is the MANUAL PARENTAL ZIPPER MERGE CORRESPONDENCES.**
Not "manual identifications", not "manual entity resolution", not a general-purpose place to put a
Geni-to-Wikidata pair somebody is confident about. What it is:

- **a manual form of the ZIPPER MERGE** -- the same job `scripts/zipper-join.py` does by
  position, done by eye where position is not enough;
- **right now, only for PARENTS.** The parent deck is the instrument
  (§ *THE PARENT DECK*), and 46 of its rows carry `batch = parent-adjudication-gui` while 204
  are `emma-pasted-verdicts` out of the same artifact;
- **something to be phased out eventually**, not a permanent channel.

**The danger the vague name creates is specific.** A later agent reading *manual identifications*
will put anything hand-checked into it -- a Samaritan pair, a bio link, a spine anchor -- and the
file stops meaning *parents adjudicated in the deck*. That is not hypothetical: this file already
carries `charlemagne-spine-anchors`, `zipper-sample`, `zipper-hard` and `blocked-creations`
alongside the parent verdicts.

**ARTIFACT means a CLAUDE ARTIFACT.** Not a GitHub Actions artifact, which is *"effectively
inaccessible and against our policy to use"* -- § *A REVIEW PAGE GOES ON GITHUB PAGES*. The two
share a word and are opposite things.

### BIO QIDs ARE ACROSS MANY GEDCOMS, and one file FORCES them

**Bio QIDs are present across many GEDCOM files, and one special GEDCOM file forces them.** After
2027-01-01 that file turns everything in it into an entry point and by extension a ledger item,
opening the way for edits in certain eccentric clusters of the tree.

Two distinct things, and the second is not a copy of the first:

- **The bios themselves are ordinary corpus content.** `extract-bio-qids.py` reads the QID links
  written into Geni *About Me* fields, wherever they occur -- **156 of 600 exports carry at
  least one**. This is a reading of the corpus, not a curated list.
- **`exports/post-merge/wikidata-qid-links.ged` FORCES them.** It carries nothing but ids and a
  `NOTE` with a Wikidata URL, so the pair is in the corpus whether or not any export happened to
  capture that bio. And on **2027-01-01** every person in it becomes an entry point, and by
  extension a ledger item -- which is what *"opening up the way for edits in certain eccentric
  clusters"* means.

**⛔ `bio-qids.tsv` GOES STALE SILENTLY, and did.** Measured 2026-09-05: the GEDCOM was updated
that day and the extract was last built **2026-08-30**, so only **3 of the GEDCOM's 29 pairs**
appeared in it. Nothing schedules the extractor, so a file that *forces* pairs into the corpus can
grow without the extract that reads them ever noticing. Re-run `extract-bio-qids.py` before
trusting a bio-QID number, exactly as § *The ledger refresh is PART OF THE RUN* says for the
ledger.

### ⛔ WHAT `wikidata-qid-links.ged` IS FOR: people TOO FAR OUT to edit yet

**What the file is for, rather than how it works:**

> *"it was originally recording very obscure random people that were obscure enough that I made
> the judgment that actually doing the Wikidata edit would be perceived as too out of left field
> … this file includes a bunch of Japanese entities that essentially act as entry points,
> including being a place to start with adding the QID or adding the Geni ID … but I decided
> that now, on January first of 2027, they just become regular entry points."*

**So it is a HOLDING PLACE, and the holding is a judgement about perception, not about evidence.**
The identification is sound; making the edit *now* would read as arriving from nowhere, because
the person is nowhere near anything the account has been building. Recording the pair in the
GEDCOM keeps it without spending it.

**It is EXPANDING, and it now takes people who already have a proper QID** — items that do have
the proper QID but are in the same category. The original rows were people needing a Geni ID added; that is no
longer the qualification.

**⛔ THE CATEGORY is the thing to get right:** far-off genealogical people, too far away in the
regular clusters to be ones to start with. The programme restarted with two Scandinavian families
and expands roughly around everybody from there.

So a row qualifies on **distance from the current base cluster**, not on obscurity, not on script,
not on lacking an identifier. The 24 eccentric-cluster pairs added on 2026-09-05 — pre-dynastic
and Third Intermediate Period Egypt, the Sixth Dynasty, the Axumite rope, Makeda — are exactly
that population: 100–168 hops from Charlemagne, nothing near the Scandinavian ring.

**And it is why the file is not two mechanisms.** Holding a far-off identification and minting an
entry point on 2027-01-01 are the same act, because a person too far out to edit *today* is
precisely a person worth growing a graph from *later*. § *THE STUPIDER AND MORE SPECIFIC* — the
stupid-spaghetti-code-that-reduces-redundancy case is this one.

### The 1,800-statement runs were SURFACE AREA, and it is temporary

**The outlier batches, explained** — the same question as § *the range is the subject count
draining*, from the other side:

> *"normally, we're adding people together, and there's an actual ring expanding. But this
> particular group was defined by the fact they were all present, but weren't connected."*

**The Bure family is the case.** A large number of them had Wikidata items already, from Swedish
Wikipedia articles, and **nobody had done genealogical work on them** — so the items existed and
the edges did not. That is a population where every statement is addable at once, which is what
produced runs of a size the ordinary ring cannot reach. § *THE EDIT ALGORITHM* predicted it:
*"the most ideal situation for lots of people being added is a bunch of individuals that are not
linked to each other and are relatively close to each other."*

**It is a stock, not a rate, and the stock is being spent.** It is a temporary phenomenon, and
the two families are now connected to each other enough. So a
falling batch size in that region is the campaign working, never a regression — do not treat it
as one and do not go looking for a cause.

**A prediction rather than a plan:** introducing the Japanese blocs on Wikidata should produce
the same phenomenon, as should any mass introduction of entry points. The blocs dated 2027-01-01
are that introduction.

**⛔ ECCENTRICITY IS THE ISSUE. CENTRALITY IS GOOD.** A high-eccentricity person or cluster is a
problem to close, which is what § *THE EDIT ALGORITHM*'s
service areas are for. Do not record this as *"centrality is not a metric"*; it was written that
way once and is the opposite of the rule.

### ⛔ A BLOC IS A ROSTER REFERENCE. Six people off a report is not the ancient Chinese bloc

**A more intuitive version of the specification is not the specification.** Six hand-listed
Chinese individuals were put into the entry points file where a roster reference was specified.

**What was done.** The bloc list names *Ancient Chinese bloc* alongside the Samaritan
high priests, the Ethiopian and Japanese Emperors, Tanba and Izumo. Instead of a roster, **six
individuals were hand-listed in `reports/entry-points.tsv`** — 少昊 Shaohao, 顓頊 Zhuanxu, 女修
Nüxiu, 大業 Daye, 皋陶 Gaoyao, 伯益 Bo Yi — the six an eccentricity report happened to surface,
none of them carrying a QID in our data.

**Why that is a specification violation and not a shortcut.** § *Whole BLOCS become entry points*
says it in the file already: **a group is a REFERENCE TO A ROSTER, never pasted ids**, which is
the same rule that makes `subgraph_roots()` read `bureatten.csv` rather than inlining 251 QIDs.
Hand-listing is the *intuitive* move — it is shorter, it is visible, and it looks like progress —
and it produces a bloc defined by whatever report was open at the time rather than by what the
bloc is.

**The mechanism is the GEDCOM, and it already existed** — keyed on the entity-resolution GEDCOM
for the new ones. It looks like stupid spaghetti code at first glance and it reduces redundancy.
A new entry point is added
by putting its pair in `exports/post-merge/wikidata-qid-links.ged` — the `special-geni-gedcom-recognition`
group reads it and switches on **2027-01-01**, the same date the bloc wanted. **One mechanism, two
purposes**: the bio link does entity resolution inside the merged tree *and* makes the QID an entry
point. Hand-listing six people duplicated a mechanism that was already there, which is the exact
redundancy the design removes.

**So `entry-points.tsv` is only for a person who needs their OWN date** — Ettinger 2026-09-03,
Martin 2026-10-01. Anything landing on 2027-01-01 goes through the gedcom.

**They are removed.** `entry-points.tsv` is back to the two people named individually, with
individual reasons: Ettinger and Martin. The `ancient-chinese-bloc` row stays in
`entry-point-groups.tsv` and correctly reports **NO ROSTER**; building one to fill the gap would
be the same mistake a second time; the roster has to be specified rather than derived.

**The tell was visible for two days and read as a feature.** All six printed in the UNRESOLVED
list every run — the mechanism that exists so *"a roster row that does nothing and says nothing"*
cannot hide. Six permanent UNRESOLVED lines were treated as the timer working rather than as six
rows that should not have been there. `unresolved_entry_points()` is now empty, which is what it
should read when nothing is wrong.

### The entry points are the BURE CLAN, and Arne Garborg is the ONE exception

**Composition, checked 2026-09-03: 253 roots = 251 Bure + Arne + Ettinger.** Johannes Bureus is
himself in `reports/bureatten.csv`, so of the 252 that existed before the drip-in, **251 are
Bure and exactly one is not**: almost all of them are Bure people, and Arne Garborg is the one
exception.

**The reason for the asymmetry is SURFACE AREA rather than importance:**

> *"the family of Arne were precreated by me and are generally pretty well connected to each
> other. Whereas this other family is in the interesting situation where… a massive amount of
> them had Wikidata items because of having Swedish Wikipedia articles, but nobody actually did
> genealogical work on Wikidata. So them as entry points means they have a high level of
> activity in connecting to each other, whereas the [Arne] people have been in large part added
> exclusively by me, and there's about the same amount of them, probably a bit less surface
> area. And the [Arne] people primarily connect to other groups."*

| | how the items got there | what they connect to |
| --- | --- | --- |
| **Bure**, ~251 | sv.wikipedia articles, **no genealogical work** | **each other** — the whole point |
| **Arne's family**, about the same number | created by hand, already well linked | **other groups** |

So the two sides are doing different jobs, and the Bure count is not lopsidedness to correct.
An item that exists but states no relationships is the highest-yield entry point there is —
§ *THE EDIT ALGORITHM*: *"The most ideal situation for lots of people being added is a bunch of
individuals that are not linked to each other and are relatively close to each other."* The Bure
people are that population, and they are why the roots look the way they do.

**`out/wikidata/relations.tsv` cannot test this claim and must not be quoted as if it does.**
It is a download snapshot: **767 of the 928 non-Bure ledger items are absent from it entirely**,
having been created after the download, so it says nothing about Arne's side. The Bure rows in it
are also post-campaign rather than pre-campaign, so a relationship count there may be measuring
hand work. § *The tree and the items are edited BY HAND, continuously* is the governing rule.

### Whole BLOCS become entry points on 2027-01-01 — and a root outside the ledger does nothing yet

**Whole blocs become entry points on 2027-01-01**: the Ancient Chinese bloc, all Samaritan high
priests, all Ethiopian Emperors, all Japanese Emperors, all Tanba people, all
Izumo/Senge/Kitajima people, and everyone with special Geni GEDCOM recognition.

**Why it is not reckless, as a prediction rather than a claim:** the invariant graph structure
will probably mean they are cumulatively at most a quarter of edits. 1 → 251 roots got 250 more
people, about 50%. The precedent is real — 2 roots to 252 took the subgraph 316 → 565, so 250
extra roots bought ~249 people, because a root only seeds what the subgraph already connects.

**`reports/entry-point-groups.tsv` holds a group as a REFERENCE TO A ROSTER**, never as pasted
ids — the same reason `subgraph_roots()` reads `bureatten.csv` rather than inlining 251 QIDs.
State as of 2026-09-03:

| group | QIDs | state |
| --- | ---: | --- |
| tanba | 179 | roster found |
| izumo-senge-kitajima | 111 | roster found |
| samaritan-high-priests | 25 | roster thin — 14 of 132 succession rows carry a QID, plus 21 pairs |
| ancient-chinese-bloc | 6 | held as individuals; **none carries a QID in our data** |
| ethiopian-emperors | 0 | **NO ROSTER EXISTS** |
| japanese-emperors | 0 | **NO ROSTER EXISTS** |
| special-geni-gedcom-recognition | 0 | **awaiting a definition** |

**⛔ MEASURED, AND IT IS THE THING TO KNOW: a root that is not in the ledger contributes
NOTHING as `compose()` is wired.** `ring_seeds = {g for g, q in our_items.items() if q in
our_wikidata_subgraph}` draws from `our_items`, which is the ledger. **All 251 Bure roots are in
the ledger; none of the 315 group QIDs is, and neither is Ettinger or Martin.** Adding the 315 as
roots grows the subgraph by exactly 315 — themselves — and pulls in **0** further ledger people
and **0** further ring seeds.

**The diagnosis was right before the code was checked:** the Bure people were manually added to
the ledger too, in an unscalable way. **Every entry point should be automatically in the ledger
once it is an established entry point.**

That is exactly what `refresh-garborg-ledger.py` does — the Bure people are a hand-wired
**second source**, and 113 ledger rows carry the note `Category:Bureätten (bureatten.csv)`. So an
entry point being in the ledger was never a property of the algorithm; it was a property of one
roster having been wired in by hand. **Entry points are now a third source**, active ones only,
so the roster feeds the ledger automatically and a root that is walked from also seeds.

**The Geni id comes from the group's OWN roster, not from a lookup.** The ledger is keyed on the
Geni id, so an entry point without one cannot become a row. Resolving the QIDs through
`derived-labels.csv` found **14 of 321**; reading `geni_ids` off the curated pair files
(`izumo-p2600-pairs.tsv`, `tanba-p2600-pairs.tsv`) gives **316 of 330**. Same rule as reading
`bureatten.csv` rather than re-deriving it.

**`special-geni-gedcom-recognition` is `exports/post-merge/wikidata-qid-links.ged`** — a specific
GEDCOM that just links Geni profiles to Wikidata, carrying no relationship data, only ids and
bios with Wikidata links. **29** `INDI` records, each an id and a `NOTE`
with a Wikidata URL, **28** distinct QIDs -- counted 2026-09-05. This said *five records, four
distinct QIDs* until then, and it was read out and repeated twice in one evening before anybody
counted the file. `reports/correspondence-sources.md` measures it against the other two
correspondence sources: **3** of its pairs are in `bio-qids.tsv`, **0** in
`manual-identifications.csv`, and **26 are in neither**. Its own docstring says *"Do not let it become an
architecture"*, which is worth knowing before it is grown. The other reading is
`reports/bio-qids.tsv` — 155 profiles whose Geni *About Me* carries a link, read back out of the
corpus — and it is recorded in the group's `note` rather than silently dropped, because the
instruction names a specific gedcom.

### The subgraph gates CREATIONS only. Filling in existing items is ledger-wide, and that is fine

**It is fine for the subgraph guard not to apply to additions.** Adding statements to people we
are not creating is acceptable; a bit of activity not centred on the subgraph is fine, especially
where it improves the state of items already created. `Q116150299` *Jon Reimatsen* and
`Q116150300` *Cecilie Ebbesdatter* are the worked case, both outside the contiguous group.

**Two passes, two populations, and the split was never designed** — it is where the filter
happened to go. `build-garborg-day.py` line ~1035 gates the **seed pool** by the subgraph, which
is what `compose()` grows the ring from. The additions pass 300 lines later iterates
`sorted(have.items())` — the whole ledger — and every inner test is `in have`, never `in seeds`.

**It is bounded, which is why it is cheap.** Additions can only touch items already in the
ledger; they cannot pull a new person in. Expansion is the ring's job and stays subgraph-gated.
The only thing that grows with the ledger is the count of fill-in statements — 178 on 2026-08-28
— and `P3373` *sibling* is capped at 40 pairs a day regardless.

**And it pre-builds bridges rather than wandering.** The six people it was knitting together are
Jon Reimatsen, Cecilie Ebbesdatter and their four children — six of the seven named as outside
the group. Cecilie's father in our tree is `6000000003166417414` **Ebbe Sunesen Hvide**,
who is **step 22 of `paths/charlemagne-to-arne-garborg.tsv`**. When the spine reaches him, one
`P40` joins that whole island to the contiguous group in a single edit.

**Why the exclusion list still exists — for the account owner's own item, and not for the
Kitajima family.** If the algorithm is followed, exclusions are not needed — true of
**creations**, since that item is not in the subgraph and is never a seed. Not true of
**additions**, which are ledger-wide: `Q232803` reaches `have` through the ledger, so without the
exclusion the fill-in pass would edit it.

**The Kitajima half of that was wrong and is corrected here.** Checked by id, 2026-08-28:
**none of the 24 Kitajima/Kitashima people is in the ledger**, so neither the fill-in pass nor
any batch scoped to the ledger could ever reach them. `Saburou Kitashima` was created by the
**ring** — one hop out from a ledger person in our Geni tree — before the subgraph gate existed,
and the subgraph gate is what stops that recurring. Their entry in `NEVER_TOUCH_*` is belt and
braces, not the thing holding the line.

### The ledger refresh is PART OF THE RUN. A separate step is a stale ledger

**The script goes through the account's contributions and updates the ledger every time.**
Building the ledger as a separate step from the script is the defect.

`build-garborg-day.py --compose` now runs `scripts/refresh-garborg-ledger.py` first and **exits
if it fails**. `--no-refresh` exists for offline work and is the wrong thing to reach for.

**The cost of it having been separate, measured the same day:** a batch built at 17:33 used a
ledger refreshed hours earlier, so `Q141198835` **Bergitte Gunnbjørnsdatter Aukland** — the
hinge of all three lines, created minutes earlier — read as missing, and the Charlemagne spine
reported itself stuck at step 8. With the refresh inside the run it went **step 8 → step
13 in one build**.

**A stale ledger does not look like an error. It looks like work to do** — and the work it
invents is re-creating items that already exist.

### The programme is HYPERLOCAL: one hop out from Arne Garborg, per day

**The only reason to run these batches is building up from the Garborg tree.** The editing is
hyperlocal on purpose, and the algorithm may change further to favour that. The daily Garborg
batch extends off Arne by one hop each time. Until there is confidence to run this at scale on
Wikidata, this is the thing to run — it is testing the waters for a later Geni bot automation.

**One step is one HOP of the tree**: each daily batch takes everybody at the next distance from
Arne — his siblings, then their spouses and
children, then the grandparents, and outward. Not one person a day, and not one
relationship type a day.

**So the deliverable is a small daily batch, not a large correct one.** The point is
confidence: a hop a day is reviewable by eye, and it is rehearsal for a later Geni bot.
`docs/wikidata-item-template.md` is the shape each item takes, read off the hand-built items.

**Do not invent a runnable edit batch nobody asked for.** Mass batches are harmful when
generated speculatively. Measurement, censuses and reports are fine unprompted — § *No unprompted reports* still applies to their volume — but
a `.qs` or a JSON edit batch is a thing someone can paste into QuickStatements, and
producing one uninvited presents work as ready that nobody sanctioned. Four `.qs` files were once
attached to a chat when one had been asked for; the largest,
`reports/wikidata-geni-qid-p2600.qs` (354 statements), was generated unprompted during a
work-loop tick.

**The existing mass batches are NOT shelved and are NOT a mistake.** The 284,000 edit objects
stay maintained and are going to be run; the programme is on, it simply does not run before the
start date. They stay live and stay consistent. The rule above is about **new** batches, not about unwinding
the programme.

### The manual approvals are TRAINING DATA. That is why they happen now, at this size

**The manual approvals happen now, at this size, because the network is still small enough to
cover all of it by hand — and doing it by hand at this size yields legitimate information.** It
is stored so that the auto-merge threshold can eventually be set from real data.

**So the verdicts are not a backlog being cleared. They are a sample being collected**, and the
sample is only worth collecting while the network is small enough to cover **all** of it rather
than a slice. Every `SAME`/`DIFFERENT` in `reports/emma-judgments.tsv` is a labelled
example of what a correct identification looks like, and the point is to learn the rule well
enough to auto-merge later.

**Three things follow, and they change how these tools are built:**

- **Scope the deck to what can be finished**, not to what exists. The parent deck was 60 slices
  of a 9,061-row corpus-wide file, when there are at most ~400 people in the network and the
  answerable set was 47. The 47 are the ledger ones — the population the pipeline is actually blocked on. Full
  coverage of a small set is the deliverable; a ranked slice of a large one is not.
- **Never auto-accept the easy cases to shrink the deck.** The obvious ones are the labelled
  positives the sample needs most. Deciding them automatically destroys exactly the data being
  collected.
- **Storage is the point, so the record must be complete.** `emma-judgments.tsv` keeps every
  verdict including `UNSURE`, and `ledger()` folds only `SAME`. An `UNSURE` is a data point about
  where the evidence runs out, which is what tells us the auto-merge threshold.

### THE PARENT DECK: `parent-review.html`. Regenerate it, never hand over the committed one

**The artifact.** <https://emmaleonhart.github.io/genealogy/parent-review.html> --- the deck of
parent identifications the duplicate guard is sitting on, one card per case, rendered for reading
by eye. It is published on GitHub Pages **unlinked**, per § *A REVIEW PAGE GOES ON GITHUB PAGES*.
The *artifact used for identifying parents* is that URL.

**A cloud session regenerated the page and published it in a state that made it useless.** The
documentation below exists so that future sessions regenerate it on demand, correctly.

**THE RUNBOOK. A cloud session with no corpus on disk uses the FIRST of these; nothing else
is needed and nothing else should be improvised:**

    gh workflow run review-decks.yml           # builds BOTH, commits to `main`, republishes Pages
    gh run watch $(gh run list --workflow=review-decks.yml --limit 1 --json databaseId -q '.[0].databaseId')

`.github/workflows/review-decks.yml` is `workflow_dispatch` only and does the whole job on a
runner: sparse checkout, unpack the derived CSVs, build, copy onto the site, commit and push to
`main`. **It exists separately from `pipeline.yml` on purpose.** The pipeline rebuilds the deck
too, but only after a ledger refresh and a QuickStatements compose, and it commits the batch in
the same run --- so on 2026-09-04 the deck rebuilt perfectly, the *batch* commit hit a rebase
conflict, the `site` job was skipped, and Pages went on serving cards that named nobody. The deck
is what gets asked for and must not be downstream of anything.

**On a machine that has the tree, it is one command:**

    python scripts/pack-derived.py --unpack     # only on a clean clone; the CSVs are gitignored
    PYTHONPATH=src python scripts/build-parent-candidates.py
    PYTHONPATH=src python scripts/build-family-candidates.py

It writes three things and they are one artifact in three forms --- `reports/parent-candidates.tsv`
(the row per case), `out/gui-data.json` (the deck), `out/parent-review.html` (the deck rendered).
`scripts/build-pages-site.py` copies the HTML to the site; `pipeline.yml` runs the generator on
**every push to `main`**, so a push is a republish and there is no separate deploy step.

**HOW TO HAND IT OVER, and both channels are right for different reasons.** Pages ---
<https://emmaleonhart.github.io/genealogy/parent-review.html> --- needs no sign-in and survives
the session, and is what § *A REVIEW PAGE GOES ON GITHUB PAGES* is about. A **claude.ai artifact**
(`Artifact` on `out/parent-review.html`) is instant and does not wait on a workflow, and is
often what is actually wanted. The rule against artifacts is about **GitHub Actions artifacts**,
the zip downloads that need a sign-in and are therefore inaccessible. Those two things share a
word and are not the same thing. **Publish the artifact first and let the workflow catch Pages up**, because the
workflow takes minutes and somebody is waiting.

**⛔ A CJK CASE IS NOT IN THE DECK.** A CJK card is not adjudicable in practice — `宣度 崔`/`Cui
Xuandu`, `丹後内侍`/`藤原遠宗の娘` and `惟宗広言`/`Koremune no Tadayasu` all came back `UNSURE`.

A card is judged by reading two people's spouses and children, which is not doable for a Heian
courtier or a Northern Wei official. Holding them costs a turn each and settles nothing. `build-parent-candidates._has_cjk` tests **both** sides — the pair
`宣度 崔`/`Cui Xuandu` is caught on ours — and the range is written in ASCII escapes, per § *A Han
range written with LITERAL boundary characters*.

**The `universe` half of that is right about them and must NOT become the filter.** None
of these is in the ledger — but neither is any other case, and the ledger scope was tried on
2026-08-31 and selected **0 of 709**, which published an empty page while the work was still
there. The filter is the script.

They stay in `reports/parent-candidates.tsv`, which is the census; only the deck is filtered.

**REGENERATE BEFORE HANDING IT OVER. Always.** The committed HTML is a photograph of whenever it
was last built, and § *The tree and the items are edited BY HAND, continuously* is why that goes
stale in minutes: an already-answered card wastes a turn. The verdicts go
back to `reports/emma-judgments.tsv` --- `SAME`/`DIFFERENT` retires a case, `UNSURE` does not.

**Verdicts arrive as a pasted block and go in by hand.** The page's *Copy decisions* button
gives five tab-separated columns --- `geni_id, our_name, qid, their_name, verdict` --- and a row
is appended as `date, batch, n, round, geni_id, our_name, qid, their_name, verdict, her_words`
with `batch` = `parent-adjudication-gui` and the three middle columns empty. Then rebuild: the
deck shrinks by what was answered, which is the check that it landed. One batch of 15 took
the deck to **7** and the file to 328 decided pairs.

**Three things made the published page useless, all fixed 2026-09-04, all worth knowing because
each one produced a page that looked fine to whatever built it:**

- **`cell()` split `reports/derived-family.csv` on `;`.** That file separates with ` | ` and holds
  **zero** semicolons, so no multi-valued cell had ever been split. A person with three recorded
  fathers arrived as the single token `4259064 | 9995000000000000074 | 9995000000000102196`,
  which is not an id, resolves to no name, and reached the deck as a card naming nobody --- 4 of
  17. Worse, `our_children` and `our_spouses` came back **empty** for everyone with more than one,
  which is precisely what makes a card unanswerable: no relationships means no judgement. This is § *Our side could never have two children* recurring in a second
  script; the two files this generator reads use two different separators and one helper served
  both.
- **The Wikidata names came only from `out/wikidata/labels.tsv`, which is GITIGNORED.** So it is
  absent in Actions --- and Actions is what publishes. Every deck that ever reached the site
  showed a bare `Q5290415` where the name belongs, while a local run with the 187 MB file present
  looked perfect. **There are now three sources in order, and each covers a hole the one above it
  leaves:** the 187 MB file where it exists; `labels_from_store()`, which reads the local Wikidata
  store through `out/wikidata/store-index.sqlite3` --- 54 QIDs out of 40 shards in seconds, and
  offline; then `_fetch_labels()` against `wbgetentities`, 50 ids a request, which is the only one
  that works in a sparse Actions checkout, where the index and `wikidata/items/` are both absent.
  Measured with the file hidden: **0 of 48 names resolved before, 47 of 48 after**, and the file
  path and the API path produce a byte-identical TSV.
- **A CJK-only person had no name on our side at all.** `label_en` and `label_mul` are both empty
  for them and the name lives in `cjk_names` --- so `Koremune no Hirokoto` and `Tango no Naishi`
  faced an empty box. § *CJK INCLUDES KOREAN*: these are not an edge case to skip.

**The tell in all three was the same and is the thing to check next time: a card that names
nobody.** The generator reported `17 structural candidates` either way, and a count is what gets
read in a log. Open the page. `build-parent-candidates.py` now exits non-zero on any card with an
empty name or a bare QID, so a broken deck says so.

**Two sessions fixed this within the same hour and neither knew of the other** --- `5beafdcb` from
a cloud session and this one, on the same file, resolved by keeping both rather than picking. The
overlap is worth reading before assuming a fix is complete: the cloud session repaired the *name*
on the card by splitting the glued id at display time, which is a real guard and is kept, but it
left `cell()` alone --- so the spouse and child lists, which are the evidence half and the thing
the cards are actually judged on, stayed empty for everyone with more than one. A symptom can be
fixed where it shows rather than where it starts.

### THE FAMILY DECK: the CHILD and SIBLING slots, `family-review.html`

**The child and sibling slots get the same manual zipper treatment as the parents.**

<https://emmaleonhart.github.io/genealogy/family-review.html> --- same shape as the parent deck,
same Copy-decisions round trip, same `reports/emma-judgments.tsv`, `batch` =
`family-adjudication-gui`. `scripts/build-family-candidates.py` builds it and
`reports/family-candidates.tsv` is its census. Everything both decks use lives in
`genimerge.deck`, once, because the parent deck's three published-cards-name-nobody bugs were
each a helper right in one copy and wrong in another.

**Two arms, and the second is not the first in disguise:**

* **child** --- a parent of our person holds a QID whose `P40` names a child nothing accounts
  for. **This is the duplicate guard's own first arm**, § *THE DUPLICATE GUARD* --- the one that
  caught `Q2183430` being created twice. It has held people back ever since and nothing had put
  the question up.
* **sibling** --- a *sibling* of our person holds a QID whose `P3373` names a sibling nothing
  accounts for. It needs no item on the parent at all, which is coverage the child arm cannot
  reach, and it is evidence our tree structurally cannot produce: Geni records **no** sibling
  edge, so two of our siblings are joined only through a shared parent.

**`P3373` had no column in `out/wikidata/relations.tsv` until 2026-09-09**, which is why nothing
could use it --- `CLAUDE.md` § *Link reliability order* has siblings as the fourth slot and says
they are *"not a slot yet"*. The extractor now carries it: **155,456 items, 418,004 statements**,
and the table went 65 MB -> 77 MB, which is still under GitHub's 100 MB refusal but no longer
comfortably.

**⛔ A CARD IS ONLY OFFERED WHERE THE SLOT HAS ONE ANSWER.** The unit is the slot, as in
`zipper-join.py`: one parent, one sex, our unclaimed children of that sex against Wikidata's
unaccounted ones, and a card only where both sides hold **exactly one**.

**Sex splits the slot and it is not decoration.** `scripts/census-solo-children.py` measured
`P21` refuting **10.0%** of solo-child pairs against 0.0% for solo father and mother slots. It
takes the deck from 1,466 whole-slot 1x1s to **3,507** pairs, because a 2x2 of one son and one
daughter each is two answerable questions while a 2x2 of two sons is none.

**Measured 2026-09-09: 3,522 answerable child slots and 1,727 sibling ones; 8,207 and 3,918
ambiguous ones held back in the census.** An `N x 1` slot asks *which of our N is this item?*,
which a Same/Different card cannot express --- offering it as N yes/no cards invites N Sames.
That is the next card shape to build, not something to smuggle through this one.

**The card carries parents, siblings, spouses and children on BOTH sides.** For these two arms
the siblings are the discriminating list, because the slot *is* a sibship and whether the two
sides line up is what settles it. § *1600-1900 is the band where NAMES LIE and YEARS decide* is
why sex and years are chips and the shared words are only a highlight.

**A card with no name on OUR side is dropped and counted, not a failure.** Geni redacts, so
`Private` and the unnamed arrive with an empty label, and an empty box cannot be judged against a
name. A bare QID on the **Wikidata** side still fails the run --- that one is the label lookup
having failed, which is the instrument rather than the data.

**`genimerge.deck.store_scan` is the third offline label source and in this sandbox the only
one.** The cloud container answers `CONNECT www.wikidata.org:443` with 403 and has no
`out/wikidata/store-index.sqlite3`, so without it every card here would have named a bare QID.
One pass over the 2,427 shards, ~6 minutes, and it is cheaper than the API once a deck is large.
In Actions the store is excluded and `wbgetentities` is what runs, exactly as before.

### THE PICK-ONE DECK: the AMBIGUOUS family slots, `pick-one-review.html`

<https://emmaleonhart.github.io/genealogy/pick-one-review.html> --- the third deck, and the only
one whose card is not Same/Different. `scripts/build-pick-one-candidates.py` builds it,
`reports/pick-one-candidates.tsv` is its census, `batch` = `pick-one-adjudication-gui`.

**It exists because the family deck cannot ask this question.** That deck offers a slot only
where both sides hold exactly one person of that sex; **12,125 slots hold more**. The common
shape is `N x 1` --- Wikidata names somebody nothing accounts for and we hold several people it
could be --- and its own docstring says why a yes/no card is wrong there: *"offering it as three
yes/no cards invites three Sames."* So the card shows the sibship on both sides and one is picked,
or none.

    N x 1   the anchor is the ITEM.        "which of our N is this item?"
    1 x N   the anchor is OUR PERSON.      "which of these items is our person?"

**A slot where BOTH sides hold several is not offered.** That is a matching problem across two
sets rather than a single pick, and forcing it into this card invites the same over-assertion.
**4,447 of them** stay in the census, counted in the run's output.

**⛔ A PICK ALSO SAYS *NOT THOSE*, and that is what lets the deck shrink.** The slot has one
answer by construction, so picking X writes `SAME` for X and `DIFFERENT` for every other option
in that slot; *None of these* writes `DIFFERENT` for all of them; *Skip* writes nothing and the
slot comes back. Without the losers' rows `deck.answered_pairs()` would re-offer the same N-1
people against the same item on every rebuild, forever. This is the reading taken rather than
asked --- § *Working the queue: GUESS. Do not ask* --- and what would falsify it is a ruling that a
pick means only *this one is right*.

**The export format does not change.** The *Copy decisions* button still gives the same five
columns --- `geni_id, our_name, qid, their_name, verdict` --- so the paste-back into
`reports/emma-judgments.tsv` is unchanged. One pick card simply emits N rows instead of one.

**`DECK_CAP` is 1,000 and the census is whole.** Measured 2026-09-09: all 6,762 cards render to a
**16.9 MB** page against the family deck's 819 KB, because a pick card carries an anchor plus up
to eight option blocks with four relative lists each. It is a rolling window of the same shape as
`LABEL_EDIT_CAP` --- what does not fit today goes out tomorrow, since the deck retires what has
been answered on every rebuild. **The ordering is most-evidence-first**, so the window holds the
cards that can actually be settled. `MAX_OPTIONS` is 8; **110 wider slots** stay in the census.

**A CJK card is held out here too**, § *A CJK CASE IS NOT IN THE DECK* --- and the holdout has to
read the card's **options**, not an `our`/`cand` pair, because a pick card has neither.
`deck.card_names()` is that reading and every deck goes through it. It runs **before** the window,
or the window spends slots on cards that are then dropped.

**Regenerate it before handing it over**, exactly as for the other two ---
`gh workflow run review-decks.yml` builds all three and republishes Pages, or
`PYTHONPATH=src python scripts/build-pick-one-candidates.py` on a machine that has the tree.


### The purpose is to ADD to Wikidata, not to correct it

**The entire purpose is to ADD.** Correcting existing material on Wikidata is such a pain that it
is almost out of the question; adding contradictory information cited to Geni is far more likely
than correcting anything.

This governs what is worth working on. Over the 14,157 people carrying both a
Geni ID and a Wikidata item:

| | count |
| --- | ---: |
| **addable statements** (Geni has a value, Wikidata is silent) | **24,957** |
| conflicts (both sides state it, values differ) | 930 |

**Twenty-seven to one.** Contradiction resolution is worth doing and is *not a
priority* — worth doing, genuinely not important.

Practical consequences:

- A disagreement is a **note**, not a work item. Do not build machinery to
  adjudicate them.
- Where Geni contradicts Wikidata and Geni looks right, prefer **adding a second
  statement cited to Geni** over editing the existing one.
- The measurement that matters for any field is *how many people have it in Geni
  and lack it on Wikidata*, not *how often the two disagree*.
- **A conflict is never routed to anybody for a ruling.** The pipeline emits the Geni value
  beside the existing statement, cited `S2600`, and moves on; `scripts/build-from-diff.py` does
  this for every `CONFLICT` row of every diff. Conflicts are simple data issues that by design
  get pushed onto Wikidata: the job is not making the tree correct, it is setting up a pipeline
  that gets the exported Geni data onto Wikidata — and, the reason it can never be per-case,
  **over a million people.**

`reports/model.md` holds the field-by-field version of that table;
`reports/names-spec.md` is the first spec written against it.

### Reading a Wikidata statement: the value is not the statement

**Qualifiers and references carry the genealogy.** Reading only `mainsnak` and
reporting what you found is how this project twice reported that Wikidata held nothing when it
held the answer.

Henry III (`Q160311`), 2026-08-10. The `P26` spouse statement's mainsnak is just
`Q228885`. Everything that matters is beside it:

    P26 -> Q228885
      P580  start time        +1236-01-04
      P582  end time          +1272-11-16
      P1534 end cause         Q99521170
      P2842 place of marriage Q29265
      4 references

Marriage date, marriage place, when and why it ended, all sourced. A display that
read mainsnak only reported "Wikidata has the spouse link but no date and no
place". **Wikidata often has it, but not in the same place, and it is relatively rare.** Both
halves of that are true and the second is
the trap — it is rare enough that a sample can miss it and confident enough to
mislead when it is there.

**Geni says 14 JAN 1236; Wikidata says 4 JAN 1236.** Ten days apart. That
disagreement only exists to be found if qualifiers are read.

## ⛔ WIKIDATA EDITING STARTS 2026-09-01 IN THIS REPO

**`shintowiki-scripts` uses a different lockdown period. This repo starts at 2026-09-01.** The
two are not the same repo and are not coordinated; a coupling between them was invented.

**There is no coupling to `shintowiki-scripts`** and nothing here may reintroduce one.

**What governs is this repo's own date, written twice and pinned together.**
`scripts/wikidata_lockout.py` carries `START_DATE = "2026-09-01"`;
`.github/workflows/wikidata-edits.yml` carries the same in `START_DATE:`. They are two
copies because the workflow gates before it checks the repo out and cannot import the
module, so `tests/test_wikidata_start_date.py` fails if they ever disagree. It still fails
closed on an unreadable date, and it makes **no network request at all** — which is a
stronger guarantee than the agent-sharing it used to be tested for.

**`P2600` is *Geni.com profile ID***, worth writing plainly next to the date: every batch this gate guards is of the form *this Wikidata
item is that Geni profile*.

**Nothing is blocked meanwhile, and the gate may not be used at all** — a Geni-ID batch gets run
as manual QuickStatements instead. Batches are written to files —
`reports/wikidata-geni-qid-p2600.qs`, `reports/wikidata-garborg.qs` — and no edit has ever been
attempted through the automated path. § *A start date is not a blocker* still
governs: build, review and commit now.

### ⛔ ON 2026-09-15 THE DAILY BATCH RUNS ITSELF. Two dates, not one

**On the 15th all of this starts automatically**: the daily Garborg batch, sent through the
bot-password API.

**There are TWO dates and both stay true.** They gate different things, so collapsing them would
either back-date the automation or re-lock the manual path:

| | date | gates |
| --- | --- | --- |
| `START_DATE` | **2026-09-01** | whether this repo may edit Wikidata **at all**. A dispatched live run has been allowed since. |
| `AUTOMATION_START_DATE` | **2026-09-15** | whether the **schedule** sends anything. Before it the scheduled run is a dry run. |

Each is written twice — `scripts/wikidata_lockout.py` and
`.github/workflows/wikidata-edits.yml` — because the workflow compares dates in bash before the
module could be imported. `tests/test_wikidata_start_date.py` fails if either pair drifts, which
is the whole reason to write them twice.

**The schedule runs BEFORE the 15th anyway, as a dry run.** A gate nobody has exercised is a gate
whose state nobody knows; running it daily means a break shows up on an ordinary morning rather
than on the day. It is at **08:07 UTC**, chosen rather than arbitrary: `pipeline.yml` runs at
01:23/07:23/13:23/19:23, so this lands after the 07:23 rebuild has refreshed the ledger and pushed
the batch. An earlier slot sends a batch built on a ledger seven hours stale — § *The ledger
refresh is PART OF THE RUN*.

**`scripts/qs_v1.py` is the join, and `LAST` is the whole difficulty.** The batch is
QuickStatements V1; the runner takes edit objects with `requires`. `LAST` is **positional** — it
means the item the `CREATE` above minted — and `genimerge.editorder` picks at random from whatever
is ready, which is right for independent edits and fatal for `LAST`. So the dependency is made
explicit instead of the order preserved:

- a `CREATE` and every `LAST`-**subject** line under it fuse into **one** edit object, sent as one
  `wbeditentity new=item`. They cannot be reordered because they are no longer separate things.
- a line whose subject is a QID and whose **value** is `LAST` becomes its own object carrying
  `requires`, and the QID is substituted at send time. § *THE THREE LINES*: `Q… P22 LAST` is
  ordinary, and calling it impossible cost weeks of one-way links.

**The file INTERLEAVES, so a one-pass reader is wrong.** Measured 2026-09-05 on one day's batch:
`LAST`-subject lines resume after a `Q… P… LAST` line **15 times**. A reader that closed the create
on the first such line would reject the batch it was written for. `qs_v1` is two passes — group,
then identify.

**Aliases carry `add`; labels and descriptions do not.** `wbeditentity` REPLACES a language's alias
list when given one plainly, and § *The MARRIED name is the real name* has every `Lmul` preceded by
an `Amul` preserving whatever the item already read, some of which are hand edits. A
replacing alias write deletes the thing the preceding line exists to save.

**⛔ THE RECEIPT IS WHAT MAKES A RE-SEND SAFE, and re-sending is the NORMAL case.**
`reports/wikidata-edits-applied.tsv` carries `date, edit_id, kind, qid`, written as each edit lands
and committed after the run. The daily file is regenerated four times a day and the schedule reads
whatever is committed, so the same `CREATE` appears in two runs whenever the ledger refresh has not
caught up with what was made. **Without the receipt the second run mints the person again**, and
that is the one failure here that running correctly next time does not undo.

Edit ids are a **hash of what the edit says**, never the line number, so an id survives the batch
regenerating with its lines somewhere else. The receipt keeps the QID as well as the id, because a
create that is skipped still has to answer the `LAST` pointing at it — and an unresolvable `LAST`
**refuses** rather than sending the literal string.

**`reports/wikidata-garborg-day.txt` is now in `REVIEWED_BATCHES`**, on the same terms as the
others: the pipeline commits it and publishes it on the site every day, so what runs is a file that
has been readable for as long as it existed.

**ONE BAD EDIT MUST NOT COST THE DAY.** The run records a refusal, skips whatever depended on it,
and carries on; five failures in a row stop it, because that is a broken account or a changed API
rather than a bad edit. Simulated against the real batch, one refused `CREATE` costs **2 edits of
85** instead of all of them — and a label collision is the ordinary case, § *NO descriptions* having
measured **3 of 22 creations** refused on a pair already taken.

**Carrying on is safe HERE and is not safe in QuickStatements**, which is the whole difference: a
dangling `LAST` refuses in `_datavalue` rather than resolving to the wrong item. QuickStatements'
own mid-batch `CREATE` failure *"broke the four `LAST` lines after it"*. The run still exits
non-zero, so it shows red and the failures are read rather than undone.

**No `summary`, on this path as on every other** — § *NO descriptions and NO edit summaries* says
*"No `summary=` on an API call"* in as many words. The absence in `Session.apply` is deliberate.
