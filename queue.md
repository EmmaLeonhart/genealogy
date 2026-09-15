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
Worse, 41,212 rows carried `2026-10-31` — a date the script never writes, six weeks in the
future — and the 30-day cooldown made every one ineligible until 2026-11-30. Both fixed:
`load_previous` resets a future date to `SEED_NEVER`, and `attempt_ledger.stamp` refuses to
write one.

**Progress is measured by counting real dates, never by the column being filled.**

## More items at the end

Do not fucking do this until after everything else is done but I want to review middle initial items since there are roman numeral related confusions with it. Middle initials do actually deserve their own items, but we are only gonna analyze this after everything else is done, so we can focus solely on this. Losses are a bigger threat than the gains are positive here.


## expanding the universe

I think especially with the locality restrictions a good way to expand the universe is for us to actively add the  subject named as (P1810) property to  Geni profile ID (P2600) properties on adjacent items to the ones in our universe. So I want this to happen. Every run 10 new bordering people not in the universe but connected to it get that as it. In addition we add geni as a source to existing relationships

## Generate CJK names from the CJK labels on PARTS of the `mul` label

Emma's own plan, recorded 2026-09-14 and **deliberately not started**: *"I had a plan to generate
cjk names from cjk labels on parts of the mul label. But don't bother with that now. Put at the
end of the queue to investigate this and possible implementation but don't actually do anything
on it now, it will be done at the end of the queue lol."*

**Investigate and propose an implementation. Do not build it before this item comes up.**

⛔ **AND THIS IS THE ONE WAY NOT CREATING A NAME OBJECT COULD HAVE BEEN COSTLY**, which is why it
is written down here rather than left as a feeling. Ruled in the same breath, about the
2026-09-14 punctuation work: *"there is a way not creating name objects could have been costly,
but the problem is that you might have internalized that it 'could' have been costly without
understanding why."*

The reason is this plan and nothing else. A name object is not only a `P735`/`P734` target --
under this plan the name items on the PARTS of a `mul` label are the input that CJK readings get
generated from, so a part with no name object is a part that generates nothing. That is a real
cost and it is specific.

**It does not reopen anything decided on 2026-09-14.** *"There's effectively zero cost for not
creating a name object"* stands as the rule for junk: `.`, `Rd.`, `(Wife`, `und`, `Count` are not
parts of anybody's `mul` label and generate no reading in any language. The two live together --
zero cost for a bad object, a real cost for a missing good one -- and the thing to carry forward
is *why*, so the next strictness decision is made on this ground instead of on a vague worry.

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


## Descendants export: Hélène de Corday

Export descendants of Hélène de Corday `6000000000746523797` — running off
`NN des Rotours` `6000000227695388934`, `task_id 6000000227757652945`. Download, file as
`exports/emma-requested/export-Descendants-6000000227695388934.ged`, done.

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
