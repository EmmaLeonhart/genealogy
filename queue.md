# Queue

Only work. An item is DELETED when done, never annotated. Bullets, never numbers —
`CLAUDE.md` § *Queue items are BULLET POINTS*.

**Read `docs/collector-run-loop.md` before touching the collector.** It is your dictation of the
whole run loop and it ends *"there's no discretion on your part at all"*, said three times.

---

## ⛔ EMMA'S OWN ITEMS, AND THEY COME FIRST

### ⛔ THE PATH COLLECTION IS A BACKGROUND ASSUMPTION, NOT THE FIRST ITEM. Ruled 2026-09-14

*"I think the paths collection being the first item made it so that you had a tendency to not do
other stuff... change up the queue item to make it be a background assumption that we are running
the path collection."*

**It runs. It needs no attention. It is not the thing you work on.** The requester and the chain
fetcher live in the geni.com tab, read their target lists off disk in chunks, and resume
themselves. Checking on them is not work; the only queue item about them is the restart check
pinned at the very end of this file.

State as of 2026-09-14: 8,000+ people requested with 12 failures, 2,150 chains fetched, 2,807
tiny path GEDCOMs, 773 isolates reached.

⛔ **PACE IT.** 500+ back-to-back census reads got the account CAPTCHAd on 2026-09-12. The stagger
is the extension's, never a sleep in the agent.

### ⛔ WIKIDATA EDITING IS HELD. Ruled 2026-09-13, and it is a STOP ORDER, not a date.

*"you had no business having any submissions going through until everything was done. That's why
it was at the end of the queue. Really, the submission should even have a requirement that all of
the Wikidata people get connected. Get connected with the path thing. So disable any editing of
Wikidata by the runner right now ... because we aren't ready for it. And the queue structure was
supposed to make that be the case."*

`HELD = True` in `scripts/wikidata_lockout.py` and `EDITS_HELD: "yes"` in
`.github/workflows/wikidata-edits.yml`, checked by both `editing_allowed` and
`automation_allowed`, with no environment override — a date arrives on its own, a hold is lifted
by a person. `tests/test_wikidata_start_date.py` fails if the two halves disagree.

**The condition for lifting it is stated and is not a date either**: the Wikidata people are
connected through the path search first. That campaign is at the END of this file.

### ⛔ SKJALGSSON IS DROPPED. Ruled 2026-09-13: *"Drop skjalgsson please"*.

Not paused and not finished-by-measurement — dropped. Three balls are filed under
`exports/skjalgsson/` and they stay in the corpus; nothing further is seeded, sampled or
re-swept there, and its banked hit is spent. Do not re-derive it from `reports/density.md` or
from any roster.


They were sitting BELOW two sections headed *ALWAYS LAST* and *THE END OF THE
QUEUE*, which is how a list gets ordered by when a thing was appended instead of by
what it is. Ruled 2026-09-13: *"uhh why did you shit the bed so hard with queue
ordering lol"*. Anything typed here by hand outranks anything derived.

## Reference moved out of the queue, 2026-09-15

Three sections were **over half this file** and none of them were work. They are reference and
they now live in `docs/queue-archive/`:

    docs/queue-archive/always-last-the-tail.md       461 lines
    docs/queue-archive/the-algorithms.md             204 lines
    docs/queue-archive/the-end-of-the-queue.md       155 lines

Nothing was deleted. `queue.md` is work only — which is the whole reason § *Queue items are
BULLET POINTS* and the delete-on-done rule exist, and a file that is half reference defeats both.

## `emmas-files/` — HERS, AND NOT TO BE TOUCHED

She saves interesting paths by hand into `emmas-files/` and changes the anchor as she goes.
**Neither is to be reconciled, renamed or reorganised**, and an anchor change is not an event.
Explaining what is in there and how it relates to `geni-paths/` is still owed and is a long way
out; the prohibition holds until then.

This clause used to live inside the `/paths` harvest item. That item is finished, and the
prohibition is not, so it keeps its own place rather than leaving with it.

## Wikidata isolate connection — the standing background job

*"Actually connect the wikidata isolates I think we can just zoom through them by this point
with our pipeline we have"*

**It runs continuously.** `scripts/pathrun.js` in the geni.com tab, topped up every work-loop
tick; `CLAUDE.md` § *THE PATH CAMPAIGN RUNS IN EVERY SESSION, NO MATTER WHAT*. `attempt` is the
word, not `connect`: an isolate with no path is attempted and done.

⛔ **THE STAGE-3 GATE IS SUPERSEDED.** This section used to say Wikidata editing stayed held
until every isolate was attempted. Emma changed that 2026-09-14 — at ~900 requests an hour it is
months, and the isolate sweep needs a browser while the edits do not, so it made the slow half
the pacemaker for the fast one. The hold is lifted and CI/CD sends daily.

⛔ **AND THE "ATTEMPTED" COUNT WAS FICTION UNTIL 2026-09-15.** The roster read **262,908 of
262,908 attempted**; the real figure was **248**. `SEED_NEVER = 2026-01-01` marks *never
attempted* and fills the column, so a non-empty `last_attempted` never meant what it looked like.
Worse, 41,212 rows carried `2026-10-31` — which read as a date the script never writes, and the
30-day cooldown made every one ineligible until 2026-11-30.

⛔ **AND THE FIX FOR THAT HALF WAS WRONG AND IS REVERSED.** `2026-10-31` is
`park-cbdb-attempts.py` parking every CBDB person ON PURPOSE, because those profiles cannot be
edited — ruled 2026-09-15, *"If it's a stable two months into the future, for some reason, just
keep it."* `load_previous` reset them anyway, wiping all 41,212, and it incremented an undefined
name while doing it, so the first parked row it met raised `NameError` and took the whole rebuild
down. Parked dates are now carried through untouched and only an UNPARSEABLE value resets.
`attempt_ledger.stamp` still refuses to write a future date, which is the half that was right.

**Progress is measured by counting real dates, never by the column being filled.**

## ⛔ THE SIBLING SCRAPE CAMPAIGN — the next mass browser job. Ruled 2026-09-16

*"the list is something that we can do mass scraping on in the same way as the relationship
paths, although much more agentically due to dumb rules by the site."*

**What the list is.** `reports/sibling-pair-worklist.tsv`, now regenerated by `tree.yml` after
every rebuild. A path GEDCOM writes a sibling pair as a family with two `CHIL` and **no
partners** — Geni records no sibling edge, so a path can only ever say *these two are siblings* —
and the parents arrive from the members' own profile pages. The list is who still needs that.

**Why every member and not one of each pair.** Instructed, and it is not an oversight to optimise
away: scraping one side gets one side's account of the parents. Each member yields a GEDCOM
linking the pair as siblings *with* their parents, and the merge fuses the three on the Geni id
so the parentless family and the two parented ones become one family with real parents.

**⛔ AND IT IS NOT THE PATH CAMPAIGN'S SHAPE.** The path requester is one `fetch` per person
against a search endpoint, which is why 1,040 an hour is safe. This is a **real page load per
person** — `CLAUDE.md` § *a census read costs a real page load*, `fetch` returns zeros because
the stats block renders after load — and 500-odd back-to-back reads is what got the account
CAPTCHAd on 2026-09-12 and again on 2026-09-15. So it runs at the extension's pace, through the
extension, and the agent navigates and nothing else.

**What already exists to build on**: `scripts/write-family-scrape.py` writes the family file and
stamps `last_attempted` through `attempt_ledger`, and `build-tiny-gedcoms.py` turns
`geni-families/*-family.tsv` into `exports/tiny-profiles/*.ged`. The missing piece is the loop
that drives it over the worklist, which is the path campaign's `pathrun.js` equivalent.

⛔ **Do not start it while the path campaign is running.** Two browser loops against Geni is the
current load; a third doing full page loads is how the account gets CAPTCHAd.

## More items at the end

Do not fucking do this until after everything else is done but I want to review middle initial items since there are roman numeral related confusions with it. Middle initials do actually deserve their own items, but we are only gonna analyze this after everything else is done, so we can focus solely on this. Losses are a bigger threat than the gains are positive here.


## ⛔ THE PATH TAIL — I DROPPED IT, AND IT HAS TO COME BACK. Ruled 2026-09-15

*"it's clear that the path stuff was dropped. It's clear that the path tail was just dropped by
you, and it needs to be brought back."*

**What the path tail IS.** Every relationship path Geni returns is a chain of steps, and each step
carries a relation word — *his father*, *her mother*, *his son*. Counted over
`reports/path-chains.tsv` there are **40 distinct relation strings**, and six of them are almost
all of the volume (`his father` 16,848, `his mother` 11,345, `her father` 10,704, `his son` 9,789,
`her mother` 7,275, `her daughter` 4,553). **The TAIL is everything below those six:**

    726  her adoptive mother       15  his child            4  her fiancé
     18  her ex-husband            14  his partner          3  her child
     15  your relative?            10  his/her parent       3  his ex-wife
     29  his adopted son            8  his adoptive father  2  her ex-partner

**Why the tail matters more than its size suggests.** A relation we have never seen written in a
real Geni export has **no attested representation**, and § *no guessing on the representations*
forbids composing one. So each tail relation has to be learned from a `Forest` export centred on
somebody who actually has it — that is the whole reason the export item exists.

**What I did to it, plainly.** Working `## Tiny GEDCOMs` I implemented the common cases, and then
for `step-parent`/`step-child` I searched the corpus for a `PEDI step` value, found none, and
**wrote them off as having no attested representation**. That was inventing a tag and treating its
absence as evidence. Corrected 2026-09-15 after Emma pointed at the family object: a step-parent is
the other spouse of a parent, in a separate `FAM`, with the child not a `CHIL` of it — read off
`exports/isolate-exports/export-Forest-6000000227738818838.ged` (Bach). Now emitted, and `P3448`
*stepparent* goes to Wikidata too.

**⛔ STILL DROPPED AND STILL OWED — and the counts below are the post-harvest ones, which are
much larger than the pre-harvest figures this item was written with.**

* **`fiancé` / `fiancée`, 57 rows over 11 people.** `ENGA` occurs **zero** times in the corpus.
  Currently emitted as a couple with no marriage event, which is a guess.

  ⛔ **AND THE EXPORT ROUTE IS CLOSED ON ALL ELEVEN. Checked 2026-09-16, every one of them.**
  `https://www.geni.com/gedcom/export/<id>` redirects to `/error` with *"You are not allowed to
  export that profile"* for the whole list -- none was created by this account. So *"needs a
  `Forest` on one of them"* cannot be done as written, and re-running the check is spending
  eleven page loads to learn this again.

      359282548040006278   Constantine Doukas        denied
      6000000000350860821  Napoléon I                denied
      6000000001723257706  James Hepburn             denied
      6000000005931058360  Margaret of Geneva        denied
      6000000007061365126  Beatriz de Castilla       denied
      6000000008579937191  Beatrice Komnene          denied
      6000000012442001730  Dante Alighieri           denied
      6000000014829030443  Richenza                  denied
      6000000023090769164  Mika Brzezinski           denied
      6000000031546887817  Mariam Bagrationi         denied
      6000000077426598714  <private> Holmgren        denied

  ⛔ **AND THE ROUTE IS THE CLIMB, COMMANDED 2026-09-17.** *"never ever even attempt to export
  these people directly. Jump straight to the climbing from one of the parties in the
  relationship, I command you to do this right now."* An ancestor is CREATED off one of the
  parties and the `Forest` runs off the created person, per `docs/export-seed-rules.md`. The
  agent never opens `/gedcom/export/<id>` on one of the eleven -- not to export, and not to check
  whether it could.

  ⛔ **AND THIS IS NOT AN END-OF-QUEUE ITEM.** Ruled the same day: *"These are not limited to
  the end, you just didnt explain what you were doing enough for me to make an informed
  decision."* It was being treated as parked behind § *GEDCOM EXPORTS -- MOVED TO THE VERY END*.

  **Emma creates the people; the agent pastes the links.** *"just paste into chat all of the
  links to each member of an unrepresentated relationship so I can make them"* -- the eleven
  above, as links, and nothing recomputed from `reports/path-chains.tsv`. That was done and it
  returned 223 people, which is not what was asked for: *"use the 11 in queue.md"*.

  **First one done, 2026-09-17.** `Nn от Осетия` `6000000227787716121`, created by Emma, `Forest`
  submitted as `task_id` `6000000227787758013` -- GEDCOM 5.5.1, 5,000, BOM on.

  ⛔ **THE FORM DEFAULTS TO `Family Tree Builder 8.0` AND THE CORPUS IS `5.5.1`.** Every
  `.ged` under `exports/` carries `1 GEDC` / `2 VERS 5.5.1`. A `Forest` can take days, so the
  Type has to be set before submitting or the wait is spent on the wrong format.
* **`your relative?`, 105 rows over 102 people** — not the 15 recorded here. Geni itself is not
  naming the relation. Only a `Forest` on those people shows what the link is. They are
  overwhelmingly ancient or disputed: Constantine the Great, Peroz I of Persia, Balamber of the
  Huns, Mattathias Maccabeus, and four US presidents.

## ⛔ RULINGS FROM 2026-09-15 — read these before working anything above

**⛔ DO NOT MEASURE THE VOLUME BEFORE DOING A SMALL THING.** *"don't measure the volume. We don't
need to measure the volume, and you measuring the volume is just going to waste time and cause
stress."* A census is for a question somebody asked, not a warm-up before every change.

**⛔ STOP GUESSING CONSERVATIVELY.** *"generally speaking, for most of your guesses, you've tended
to always guess the more conservative thing that I don't really fucking care about."* The Dutch
patronymics are the worked example: 90 occurrences, refused as too small, and the ruling was
*"under 100 total, do it."* When the choice is do-it or leave-it, do it.

**⛔ PATRONYMICS ARE DECIDED FROM THE FAMILY TREE, NOT FROM THE FORM.** *"patronymics are actually
extremely difficult to get wrong if you actually audit them ... I've been constantly telling you
that we have to be doing modeling based upon the family tree ... you just kind of never did it."*
`Eric` is a patronymic only if the father is `Er`, and he never is; `Nemanjić` is one because the
father is `Nemanja`. Refusing a whole family because its FORM is ambiguous is the error — 160 real
Slavic patronymics were being thrown away that way.

**⛔ A FUTURE `last_attempted` IS A DELIBERATE PARK, NOT CORRUPTION.** `park-cbdb-attempts.py`
writes `2026-10-31` on every CBDB person on purpose, because those profiles cannot be edited.
A previous version of `build-unconnected-worklist.load_previous` reset every future date to
`SEED_NEVER` and wiped all 41,212. Restored and re-parked 2026-09-15. *"If it's a stable two
months into the future, for some reason, just keep it."*

**⛔ DO NOT PANIC ABOUT ITEMS WE GOT WRONG.** *"it kind of sucks that we got some stuff wrong. It
would be nice if we make stuff self-healing, but don't fucking panic about it. These things can be
healed by other people."*

**⛔ TESTS DO NOT COUNT UNTIL THE QUEUE IS FINISHED.** *"literally test passing doesn't count, that
doesn't matter."* Do not dispatch CI, do not wait on it, do not report on it.

**⛔ THE FIRST THING IN A SESSION IS TURNING ON THE RELATIONSHIP REQUESTING**, and every even hour
at :45 the requested paths become TSVs in the repo. Both are in `CLAUDE.md`.

**⛔ `Q320139` ZERUBBABEL TAKES NO `mul` LABEL OR ALIAS** until 2027-09-15. `MUL_BLOCKED` in
`build-garborg-day.py`. The lapse is silent and that is intentional.

**⛔ `Q70899` ADAM HAS TWO GENI IDS ON PURPOSE.** `6000000201847373856` is qualified `P2868`
*subject has role* `Q2001710` **Adam in Islam**. Biblical figures accumulate profiles because Geni
disconnects them. We hold one profile; that one IS the profile and the other is never a conflict.

**CJK FROM THE PARTS OF A `mul` LABEL IS ON HOLD.** *"probably we put a lot of the CJK from parts
on hold generally. Because I don't think it's worth it."* The investigation is
`docs/cjk-from-name-parts.md`; do not build it.

## Owed explanations, 2026-09-15

Two answers Emma asked for and did not get:

* **Why the relationship-source backfill is stricter than the `P1810` one.** `S2600` means *Geni
  states this*. `P1810` copies a name Geni already gave, so it cannot be false. A source on a
  relationship Geni does not record WOULD be false, and it renders as a tidy Geni link either way,
  so nobody can see it is wrong. That is why every line is checked against `derived-family.csv`
  first.
* **What `ADJACENT_FLOOR` is.** The universe grows by editing its neighbours, and the pass queried
  our own 4,430 items before the neighbours — so the 60-a-day quota filled before a single
  neighbour was ever reached, and all four emitted files contained **zero**. The floor reserves 10
  neighbours per run so "our own items first" cannot mean "our own items only".

## Edit the abbreviations out of the GEDCOM data itself

Ruled 2026-09-15, and NOT what was done: *"you're supposed to fucking change the data so that it
doesn't do it ... you are literally supposed to edit the gedcom files to replace all instances of
the abbreviated form with the non-abbreviated forms."*

What was done instead was refusing `Olsdtr` as a name ITEM and expanding it at emission.
`reports/abbreviated-patronymics.csv` already holds the resolved form for 11,731 tokens, decided
per person from the mother and paternal grandmother. This item is applying that to the `.ged`
files.

⛔ `CLAUDE.md` § *Never overwrite an existing `.ged`* stands against this and has to be settled
first — the instruction is explicit, the rule is explicit, and they disagree.


## ⛔ GET CI GREEN — IMMEDIATELY BEFORE LIFTING THE HOLD, AND NOT BEFORE THEN

Ruled 2026-09-14: *"put it as the queue item before actually running the cicd proper"*. Not a
first item, not worked ahead of real work.

Last read: run `34922163324` on `07fdb97e`, **4 failures, down from 11**. Three were fixed after
that run (`built-batches.tsv`, the `das` and `von` tests); the fourth is the committed batch
offering to create 63 people who already hold QIDs, which `pipeline.yml` fixes when it
recomposes. `build-repo-freshness.py` exits 0 and writes nothing — that is a real defect and it
is this item's.

Dispatch `ci.yml`, read the conclusion, fix what it says. § *TESTS RUN IN CI/CD OR NOT AT ALL*.

## ⛔ GEDCOM EXPORTS — MOVED TO THE VERY END, 2026-09-14

Ruled: *"these gedcom descendant exports are best moved to the very end of the queue so we can
focus on other stuff since they can be done and integrated on a more long term basis while we
fix important stuff."*

They sit AFTER the hold lift on purpose, so a long-running export can never block it. Each one
is a submit, a wait of 6-15 minutes, and a file — cheap to pick up whenever the browser is
free, and they integrate on their own schedule.

### Ursula von Münsterberg — the German branch of Alix's descent, missing from the corpus

`6000000188494434823`. **Not in our tree**, and her mother `Sophie of Teschen`
`6000000006727858370` already is — so this is one export away from closing a branch we know is
there. Established 2026-09-15 from Emma's own lead: Geni computed her relationship through
`6000000003481830064` **Guy d'Ibelin, whose mother is Alix de Lampron**, and the route from the
German side runs Cieszyn → Bavaria-Landshut → Lusignan Cyprus → Guy → Alix, hinging on the
marriage of Agnes von Bayern-Landshut to a Lusignan king.

*"it may be the case for many others too"* — so the interest is the branch, not the individual.
`Descendants` off a created ancestor per `docs/export-seed-rules.md`, not `Forest`.

⛔ Check `https://www.geni.com/gedcom/export/6000000188494434823` for *"You are not allowed to
export that profile"* first; she was not created by this account.


### `Forest` export for a STEP relationship — the one representation the corpus does not attest

The profile scrape carries `step-parent` 12 and `step-child` 3, and **the corpus attests no way to
write one**: every `PEDI` value in `exports/` outside the tiny directories is `adopted` 2,473,
`foster` 805 or `birth` 555, and there is no `PEDI step`. So `build-tiny-gedcoms.py` drops those 15
edges rather than invent a shape for them.

Ruled 2026-09-13 for this exact case: *"we have to do a `Forest` export on that point in order to
get that relationship so we know how to represent it."*

A seed is in `geni-families/292373984150002914-family.tsv` — subject `292373984150002914`, whose
`step-parent` row is `Ratanbai Tata`. `Forest`, because the point of the export is to cross the
step link rather than descend.

⛔ Check `https://www.geni.com/gedcom/export/292373984150002914` for *"You are not allowed to export
that profile"* first.


## Forest exports

These are people I want exports on but they are not in the priority in the same way. Often cover possibly underserved people but their significance is unclear

Forest https://www.geni.com/people/NN-Fuca/6000000227739821875

Descendants https://www.geni.com/people/NN/6000000227739695943

## Ancestor Exports

At the end of the queue after all other things are done I want to do some specific ancestor export campaigns. 

Ancestor exports from certain specific people to get their ancestors

try this one https://www.geni.com/people/Reformatorin-Ursula-von-M%C3%BCnsterberg/6000000188494434823?through=6000000003481830064

## `Forest` exports centred on people carrying the TAIL relationships in the TSVs

Ruled 2026-09-13: *"put it at the end of the queue that... to do forest exports centred on people
with the tail relationships for the TSV files."* Written down and not started **yet**.

**Last in order, and it gets done.** Emma, immediately after: *"it's at the very terminal end of
it. And it's NOT parked. It's gonna be addressed later."*

**Why a `Forest` and not a lookup:** a relationship we have never seen in a real Geni export has
no attested representation, and § *no guessing on the representations* forbids composing one.
The export centred on a person who **has** that relationship is what shows how Geni writes it.

**The tail, counted off `paths/harvested-path-geni-*.tsv` on 2026-09-13.** The whole distribution
is 33 distinct strings; these are the ones below the common six and their gender variants:

    134  her adoptive mother        3  her child            2  his/her father
     18  her ex-husband             3  his ex-wife          2  his parent
     15  your relative?             3  his fiancée          2  her ex-partner
     11  his partner                1  his child            1  his adoptive mother
      5  his/her parent             1  her partner          1  his adoptive father
      4  her fiancé

**⛔ THE URGENT ONES ARE THE UNATTESTED ONES, and there are two kinds.**

* **fiancé / fiancée — 7 rows, and `ENGA` occurs ZERO times in this corpus.** There is no shape to
  copy, so they are currently emitted as a couple with no marriage event. This is the case Emma
  described exactly: *"if there's some relationship that is only present in one spot, we have to
  do a `Forest` export on that point in order to get that relationship so we know how to
  represent it."*
* **`your relative?` — 15 rows.** Geni itself is not naming the relationship, so a `Forest` on
  those people is the only way to find out what the link actually is.

**Already attested and needing no export** (`devlog.md` 2026-09-13 carries the measurements):
adoptive → `FAMC` + `2 PEDI adopted` + `1 ADOP` + `3 ADOP BOTH`; ex- → bare `1 MARR` with bare
`1 DIV`; partner → a `FAM` with no `MARR`. `foster` is attested 781 times in the corpus and
appears in **no** path string, so it needs nothing until one turns up.

Pairs with these relations are in `reports/path-chains.tsv`; the person to centre the export on
is the one the tail word describes.

## Names

Remember that this is not something to be done out of order, it is the second last item in the queue for a reason

We are still generating non-name items as names such as numbers, and I think https://www.wikidata.org/wiki/Special:Contributions/OBender12 is likely pretty pissed at this point, but no talk page messages yet. idk why you did not fix it and seem to have completely overlooked the error that he constantly corrects. There are plenty of non-name things that need to be parsed not as names.

Read "address_this.html"

### Examples

Even in the current batch one exists lol

# und -- family, 8 bearer(s) in the batches
# create a new item
CREATE
#   the item just created: set the en label to "und"
LAST	Len	"und"
#   set the mul label to "und"
LAST	Lmul	"und"
#   set the en description to "family name"
LAST	Den	"family name"
#   P31 instance of = Q101352
LAST	P31	Q101352
#   Q61139384 Mangold von Thurgau und Nellenburg III: P734 family name = the item just created
Q61139384	P734	LAST	S2600	"6000000004106003883"
#   Q81827036 Adalbert von Saffenberg und Norvenich: P734 family name = the item just created
Q81827036	P734	LAST	S2600	"6000000009305060696"
#   Q55068638 Friedrich zu Schwarzenberg und Hohenlandsberg: P734 family name = the item just created
Q55068638	P734	LAST	S2600	"6000000014784646061"
#   Q110261972 Johann I von Tengen und Nellenburg: P734 family name = the item just created
Q110261972	P734	LAST	S2600	"6000000017758205608"
#   Q110415677 Georg III von der Leyen zu Eltz und Leiningen: P734 family name = the item just created
Q110415677	P734	LAST	S2600	"6000000019797018175"
#   Q828346 Berthold Graf von Neuffen und Achalm: P734 family name = the item just created
Q828346	P734	LAST	S2600	"6000000082813823834"
#   Q110410743 Nicolaus* Andreas Graf von Maltzahn, Freiherr zu Wartenberg und Penzlin: P734 family name = the item just created
Q110410743	P734	LAST	S2600	"6000000105706792946"

## PINNED LAST -- RESTART THE PATH COLLECTION IF IT HAS STOPPED

Ruled 2026-09-14: *"have the very last queue item be one that would be to restart the path
collection in the event that the path collection ended up stopping."* And the standing rule is
now in `CLAUDE.md` § *THE PATH CAMPAIGN RUNS IN EVERY SESSION, NO MATTER WHAT*.

    check    ls -lt ~/Downloads/path-chains-*.tsv  -- a gap means it is dead
             window.__pathrun in the geni.com tab: {running, i, ok, fail}
    restart  open an UNCONNECTED profile, paste the DERIVE block of scripts/pathrun.js,
             then the RUN block with ids from scripts/build-pathrun-batch.py
    stop     window.__pathrun.stop()

**Its stopping is not an emergency and not a reason to work on it.** Restart it, go back to the
first item.

- **DECIDE: what happens to `build-add-p2600-batch`.** <!-- requeued-add-p2600-2026-09-13 -->
  Deferred on 2026-09-06 for want of context to decide on, and re-queued on 2026-09-13 by
  `.github/workflows/requeue-add-p2600.yml`.

  It writes **7,166 `P2600` statements** inferred from parent-anchor proof into
  `reports/wikidata-add-p2600.qs`, and **nothing runs it**. The four options as they stood: fold
  it into the daily batch under a cap; give it its own scheduled workflow; delete it; or leave it
  as a hand-run tool. `reports/qs-batch-audit.md` carries the measurement.

  The other five generators in that audit were settled on 2026-09-06 —
  `build-missing-reciprocals`, `build-qid-link-p2600`, `build-label-corrections` and
  `build-sibling-batch` deleted by instruction, `build-from-diff` given its own review item.
  This is the last one open.
