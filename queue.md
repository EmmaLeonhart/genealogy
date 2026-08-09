# geni — Work Queue


**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step; on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below).

---

## Import the two new exports in Downloads (2026-08-09)

**Two `export-geni*.zip` files are sitting in the Downloads folder and are not
yet in the corpus.** Import them the usual way, and **filter out repeats** —
the same export arrives twice routinely, so this batch may not be two new files.

Needs the machine that has the Downloads folder; the cloud session cannot reach
it, so this is the first thing for a PC session to run.

1. Extract each zip beside itself; move the `.ged` under `exports/` into a
   directory named for the seed (the file's first `INDI`), disambiguating by
   seed profile ID if a `export-<style>.ged` name is already taken.
2. **Drop any that is a byte-identical repeat of a file already committed under
   `exports/`** before committing — as the 2026-08-06 edges batch did with two
   of its six zips. Check containment too: a strict subset of a committed export
   adds nothing.
3. Add the one-line gitignore entry per zip (full path, never a `*.zip`
   pattern), so the unignored zip is the signal a download arrived.
4. **Keep the current `out/merged.ged` as `out/merged-<n>.ged` before merging**
   — item 0.00A relies on the pre-batch tree being kept to measure a batch.
5. `python -m genimerge merge`, then record the new-people count and update the
   corpus count in `reports/`.

## Active after import finished

Once we are finished with the wikidata tree export, or have decided we are finished with it, we can then look to see how much of the tree is interconnected.

The geni tree export should be analyzed and merged into, but this involves a lot of AskUserQuestion

We have the large batch of shared individuals, we will need to reconcile the radically different formats, and do entity resolution piecemeal across the graph. So like if person has two fathers, analyze if they seem to fit

With entity resolution stuff, parents are easier to resolve, but we need to do a test of say 10,000 individuals for any entity resolution algorithm. It needs to be rigorous. 

Notably geni names are structured with the form of separate first names and last names. There is a display name but I do not think it commonly happens. Display names are complicated and we need an analysis, plus our name property adding things. 

We also need some other geni-wikidata entity resolutions manually or with searches. Well there are a couple ids I have to manually propose at least.

Adding the geni source properties


Also the wikidata items with two geni ids, we need to resolve this

imo we need to figure out how to reach all the wikidata items with geni ids, but we do not have the geni ids. These can be discovered with tree traversal planning. Mainly descendants of individuals we have. Extension of the other descendants thing we were doing. We do that thing first, and then the general geni export thing later. This might get most of the significant geni stuff here anyways, but we can get say clearly terminating clusters in the 1800s or 1700s later after the incorporation of the geni descendants and such


## Active — after the offline join (2026-08-09)

The five items planned this morning are done and are in `devlog.md`.
`genimerge.wikistore` now reads the downloaded store, and
`wikidata-index` / `wikidata-ancestors` are the two new commands. What that
opened up, and what it did not:

2.A **1,821 export targets — the century breakdown is coded and not yet run.**
`wikiancestors.parent_birth_years` reads P569 for each target from the store and
`render_markdown` buckets them by century, with 21 tests green. The report on
disk does **not** have that section: the regeneration was killed part-way to
keep the laptop cool, so `reports/wikidata-ancestors.md` is still the
counts-only version. Re-run `python -m genimerge wikidata-ancestors --source
out/merged.ged` when heat allows — two store passes, a few minutes.

The question it answers, so the run is not mistaken for a formality: the
`Descendants` campaign is about reaching **modern times** and a parent is one
step backwards, so the list is only worth anything if enough of the targets are
late enough for their descent to arrive where the campaign is going. A
`Descendants` export seeded on a missing parent returns that parent's whole
descent — the siblings of somebody we hold, and their lines — which is why a
parent is not simply a backwards move.

**The older framing, kept because it is what the report currently supports:**
`reports/wikidata-ancestors.md` lists Geni profiles Wikidata names as a parent
of somebody we already hold, and that no export here has reached. These are
doorways `frontier` **cannot** see — it ranks our own parentless people and
knows nothing about what the other tree says is above them. Nothing has been
done with the list: it wants reading, and then a decision about whether these
feed the export campaign the way `reports/descendants.md` does. Note the
tension worth resolving before acting: the `Descendants` campaign is about
reaching *modern* times, and a parent is by construction a step **backwards**.

2.E **Make the component walk a command, and separate the 183,296 isolates.**
`reports/wikidata-components.md` answers "how many trees is the Wikidata side"
— one of 1,042,423 (74%) plus 223,207 fragments — but it was produced by a
throwaway script, so it is not re-runnable as the store grows. Port it to a
module the way `wikistore` was, reusing `wikidownload.RELATION_PROPERTIES`
rather than restating the five properties.

While there: **an isolated item and an item whose relatives were not downloaded
are different things and the current pass cannot tell them apart**, because an
item with no relation statements emits no dangling reference either. Splitting
them needs only a count of relation statements per item, which the same pass can
carry. Until it does, do not describe the 183,296 as "people with no family on
Wikidata" — that is one of the two readings and it is unverified.

**The HTML must split the two, and isolates need investigation — Emma,
2026-08-09.** The component output (HTML) has to separate genuine **isolates**
— items with *zero* relation statements, no family recorded on Wikidata at all
— from items that only look isolated because their **relatives were not
downloaded** — items carrying P22/P25/P26/P40 that point at QIDs not yet in the
store. Those two are different work: the not-downloaded ones **just need
import** (the expansion walk fetches the referenced items and they stop looking
isolated), while the true isolates are **NEEDS-INVESTIGATION** — nothing the
import closes, a standing question about why Wikidata records no family for
them. The relation-statement count this item already calls for is the
discriminator; surface it per item so the two groups are told apart in the page.

2.B **Port the remaining `client.sparql` call sites to the store, by question.**
`reconcile`, `crosscheck` and `namelinks` still import `genimerge.wikidata`, so
they still cannot run under the no-query rule. Ten call sites; each asks one
concrete thing and gets answered from the index. `crosscheck` is the valuable
one — it compares our parents, spouses and dates against Wikidata's, and the
4,491 parents with no Geni ID are exactly the population it would speak to.
Do **not** write a SPARQL emulator.

2.C **Build the union tree — one genealogy holding both sources.**

**The shape, from Emma directly, 2026-08-09.** A union individual is a JSON
object with the two sides **nested whole and side by side**:

```json
{
  "geni_id":     "6000000087535357291",
  "geni":        { ...the full text of the Geni export for that person... },
  "wikidata_id": "Q12345",
  "wikidata":    { ...the nesting of the Wikidata content... }
}
```

**It is synoptic, and that word is doing real work.** This is a *duplicated*
tree, not a fused one: both sides are kept verbatim, nothing is reconciled at
build time, and *"this duplicated tree is intended to be later updated for a
later integration process."* Integration is a **later** pass over this
structure, not a condition of writing it.

So the three things that follow are decided, not open:

- **Do not merge fields.** No picking a birth date, no preferring a parent. When
  the two sides disagree the union simply holds both, tagged by which side they
  came from — Emma's call, and it falls straight out of the structure: the
  disagreement *is* `geni.birth` next to `wikidata.P569`.
- **Do not drop either side's content.** Both nests are full, not a projection.
  Same reasoning as `wikidownload` storing whole items: what a later phase wants
  is not yet known, and something stored lossily has to be fetched again.
- **Everything downloaded is in scope** — all 1,408,401 stored items, not just
  the 514,903 carrying a Geni ID. A node with an empty `geni` side is normal.

Either side may be absent, which gives four node kinds: both sides (12,860
pairs), Geni only (262,587), Wikidata-with-an-unreached-Geni-ID (504,123 pairs
— `reports/wikidata-unreached.tsv`), and Wikidata with no Geni ID at all
(893,498).

**What it is for**, all of which the structure has to survive: queueing Wikidata
edits that create the missing people, planning the next Geni exports, being one
complete genealogy to look at, and surfacing where the two sources disagree.
Emma also marked "something else" — **ask before assuming the four are the whole
list.**

**Still to settle before building:** what an *edge* is in the union. A Geni
parent link is a FAM record and a Wikidata one is P22/P25 on an item, and the
node shape above says nothing about how the graph is walked. Write that down
first.

**Corrected here after getting it wrong.** This item previously asked Emma to
decide whether the 4,491 Geni-ID-less parents were "an authoring batch or a
matching problem", as though admitting them required choosing. In a union tree
it does not: a person Wikidata records with no Geni ID is simply a node that
came from the other source. Whether one later proves to be a Geni profile under
a different ID is entity resolution **inside** the union, not a gate on entry.
The dichotomy was invented and the NEEDS-DECISION tag was wrong — by this repo's
own load-bearing default that made it undone work, not deferred work.

Concretely, the union holds:

- **12,850 in both** — joined on P2600, one node with two source IDs.
- **262,587 Geni-only** — our tree, no item.
- **504,035 Wikidata items carrying a Geni ID no export has reached** — known to
  both sites, held by neither of our datasets yet.
- **893,498 Wikidata items with no Geni ID** — the expansion walk's catch, of
  which the 4,491 parents are the part sitting directly above people we hold.

The node identity has to carry **which source each fact came from**, because
`todo.md` § 8's whole point is provenance and because a union that forgets
whether a parent link came from a GEDCOM or from P22 cannot later be turned into
Wikidata edits. Do not collapse the two IDs into one key: the Geni profile ID is
this repo's primary key for the Geni side and the QID is Wikidata's, and a node
can have either, both, or (after a merge) two of one.

Start by writing the shape down before building it — what a union node is, what
an edge is, and what happens when the two sources disagree about a parent. The
merge rule for the Geni side is later-sources-win on single-valued paths; the
union across *sites* is a different question and is not answered by that rule.

2.D **The 10,000-individual entity-resolution backtest.** § *Active after import
finished* asks for it and says "It needs to be rigorous". It still has no stated
success criterion, and inventing one is the failure mode — two seed-choosing
methods have already been refuted by measurement here, and both were proposed on
reasoning alone. **NEEDS-DECISION** — Emma; what counts as success.
The display-name and name-property analysis is likewise unstarted;
`genimerge profile-names` already measures the Geni side.

## Active Earlier

0.00Y **`test_the_seed_items_carry_the_geni_id_they_were_selected_for` fails,
and the assertion is what expired, not the download.** It asserts that over half
of every stored item carries P2600. Measured 2026-08-09 over the whole store:
**514,903 of 1,408,401 — 36.6%**.

Nothing is wrong with the data. The seed set is ~516,983 QIDs
(`out/wikidata/p2600-all.tsv`; `wikidownload.py:354` calls it "the real
514,822") and **514,903 of them are stored**, so the seed phase is essentially
complete. The other 893,498 items are expansion relatives, which is exactly what
the walk exists to fetch. The floor held only while the store was
seed-dominated, i.e. during the pilot, and the test's own comment already
concedes "Expansion items legitimately have none, so this is a floor, not a
rule".

**The decision is what should be asserted instead**, and it is Emma's because
the test encodes her requirement. The obvious candidate — P2600 count against
the seed-file count, rather than against the store total — has a catch worth
knowing before choosing: `out/` is gitignored, so `p2600-all.tsv` is absent on a
fresh checkout and the test would have to skip there, which is a weaker guard
than it looks. A plain absolute floor (say 500,000) is self-contained but goes
stale in the other direction.

Do **not** just lower `0.5` to a number that passes today. That retires the
guard without replacing it, and the guard is the one that would catch the seed
map drifting.

**NEEDS-DECISION** — Emma; what the seed-coverage invariant should be.

0.00Z **Three `FAM.HUSB` conflicts in the 145-export merge — decide them on
evidence, not on filename order.** The first structural disagreements the merge
has had to resolve: two exports naming different husbands for one family, where
every prior conflict was a value like a date or a place.

`@F6000000179131721834@` is the sharp case. It appears **twice** in
`out/merge-report.md` with the winners reversed —
`export-Descendants-6000000226989731860.ged` beats `export-Forest-14.ged` in one
row, and `export-Forest-6000000226989731860.ged` beats that same Descendants
file in the other. Candidate husbands are `@I6000000001829492981@` and
`@I6000000179131744821@`. The third is `@F6000000195596077832@`
(`export-Bio-6000000212213649822.ged` vs `export-Forest-32.ged`), husbands
`@I6000000198604813825@` and `@I6000000195595965846@`.

Later-wins picked the survivor, and **merge order is path order, not export
date** — so filename sorting decided which husband is in the tree. That is
within the stated rule and is still the wrong instrument for this question.

Two things to do, in order: (1) look at the six people and the two families in
the merged tree and say whether these are two records of one man or two men —
this is the "person has two fathers" case § *Active after import finished*
names, and it is the first real test case for whatever entity-resolution method
gets built; (2) decide whether `merge_files` should sort sources by their `HEAD`
date before merging, which `CLAUDE.md` says follows without a code change.

Do **not** settle it by re-running the merge in a different order — that changes
the answer without producing evidence for it.

**NEEDS-INVESTIGATION.**

0.00A **Take one `Descendants` export seeded after 1750 and diff the tree.**
The 2026-08-07 batch settled the previous version of this item and produced
`reports/descendants-backtest-2026-08-07.md`: eleven exports, 18,218 new people,
median birth 1582, **four** born after 1900. Two seed-choosing methods were
refuted against it. What is left is the one claim that has not been tested —
that seeding *after 1750* is what makes a ball arrive in modern times.

The prediction is specific: an export seeded on a candidate from
`reports/descendants.md` § *Seeds that can reach 1900* should return people born
after 1900 in numbers, where the eleven ancient seeds returned four between them.
If it does not, the twelve-generation reach model is wrong and the campaign needs
a different instrument than `Descendants` entirely.

**Keep `out/merged.ged` as `out/merged-<n>.ged` before merging the next batch.**
That is the only reason this batch could be measured at all.

**BLOCKED-ON-USER-ACTION** — taking a Geni export is Emma's to do. Unblock
signal: a new `export-Descendants-*.ged` under `exports/` seeded on a post-1750
profile.

0.000 The "FIRST ITEM" is finished — all 19 path files re-checked against the
98-export merge, `reports/paths.md` rewritten, devlog entry dated 2026-08-06.
Emma's update to the agenda of this project:

Big priorities:

1. Algorithmically finding the most remote individuals and then connecting all of them. Earlier one was random individuals which is not helpful, but that did not disprove our hypothesis on shortest path discovering new communities, we just chose things that were pretty central
2. Import the Hata clan. Surprised it is not all there already.
3. Ideally we want to connect all wikidata items with geni into this for our world tree

   **Priority 2 is answered, and the answer is no — `reports/hata.md`,
   2026-08-06.** Emma took a `Forest` export seeded on a Hata person the same
   afternoon (`exports/Hata/export-Forest-6000000210475738822.ged`, 4004 people,
   seed 酒君/酒公 /Hata/) and it settled the question against this repo's own
   prediction. The clan went 27 → 37 people and **all ten new people are one
   unbroken descent**; siblings across the whole clan stayed at 9, marriages
   stayed at 0, branch points stayed at 1. A `Forest` export follows spouse
   links and found none to follow. The one-hop neighbourhood ignoring names
   entirely is **four people**. There is no more clan to import: Geni records
   秦氏 as a line. Emma's call — *"likely definitively showing it is just a
   line"* — was right.

   The export paid on the other target anyway: 惟宗 2 → 8, 島津 51 → 92, and
   `reports/path-hata.md` **29/55 → 39/55**, closing all eight of steps 33–40.

   **That path is now 55 of 55, closed 2026-08-06 night.** The last four --
   Stephen Merrill and three descendants, steps 17-20 -- came in on a
   `Descendants` export seeded on `6000000227087382828`. **The whole path corpus
   is 3 464 of 3 464 steps, 26 of 26 paths complete, zero bridges.**

   Emma's reading before that export was that the area was "an extremely dense
   modern group even more impenetrable than the ancient ones", and she was one
   export from giving up on it. It went through. Worth keeping as a caution in
   both directions: density is a real obstacle to *seeding* -- `todo.md` item 8
   explains why, she cannot add a profile where other contributors are thick on
   the ground -- but it did not stop this one, and neither of us predicted that.

   **Never call this "the Hata gap".** The path is named `hata` for its
   *endpoint*; every step on it named Hata was held throughout, as was the whole
   Japanese side from step 21 to 55. Reporting the gap by path name led Emma to
   believe her Hata export had failed when it had not. Name the people who are
   missing, never the path they sit on.

   Also worth recording as a method note rather than a task: **a clan name is
   not a clan.** Counting Hata-named people implied a population Geni does not
   record; the measurement that answered it used no names at all.

0.0 **BLOCKED-ON-USER-ACTION — save the path pages for the 18 people in
   `reports/remote-people.md`.** The list is ranked by eccentricity, each row is
   provably 77+ hops from every other row, and each carries a one-click Geni
   path URL in blood and in-law form. `out/remote-people.html` is the page to
   work through; re-open it with
   `powershell Start-Process out\remote-people.html`. Unblock signal is a new
   `.html` under `geni_pages/`, then for each one:

   ```
   python -m genimerge path-from-html "geni_pages/<saved>.html" -o paths/<name>.tsv
   python -m genimerge path paths/<name>.tsv --source out/merged.ged
   ```

   **"Read the first three before saving many" has now been answered, and the
   answer is stop.** Nine more pages were saved on 2026-08-06 evening and
   checked in `reports/path-gaps-2026-08-06.md`: across all 26 paths, **3 199 of
   3 464 steps held (92.3%) and 11 paths are complete end to end**, `gong-liu`
   at 249/249 among them. No path ends in a gap — every break is an interior
   bridge and the remote endpoint is already held. The stated fallback applies:
   **this instrument measures our tree's shape, not Geni's gaps**, and the
   effort belongs on `reports/density.md`.

   Emma's reading of *why* is supported by the concentration: 265 absent
   step-slots sit on 196 people, but 29 people carry 98 of them, and five
   separate paths break at the *same ten* Alemannians. Sparse ancient graph,
   connectivity through few individuals. **Saving more path pages is not the
   work; closing the shared bridges is.**

   **Superseded again, 2026-08-06 night, over the 115-export merge: the paths
   are essentially closed.** `reports/connectors.md` is the live answer.
   **3 447 of 3 464 steps held (99.5%), 23 of 26 paths complete, 3 bridges
   holding 17 people, none shared between paths.** Emma's twelve gap-aimed
   exports closed the Alemannian ten *and* all three Chinese runs
   (`zeng-yuan` 52, `hao-huang` 25, `hou-zhang` 10) in one batch. Every bridge
   this queue has ever named by profile ID is now held.

   What is left is three private gaps, and each is its own item rather than a
   shared bridge: 11 people on `hata` (item 0.000 below, seed Enok Danielson
   `6000000004104838733`), 3 on `makeda-to-marguerite` (seed Pierre Louis de
   l'Estandart `6000000196474936821`), 3 on `psamtik-ii` (seed Musa bin Musa
   Al-Qasi `6000000012263275369`). All three `Forest` — the first crosses a
   brother and two wives, the second a husband.

   **The concentration finding did not survive.** "29 people carry 98 slots,
   connectivity through a few critical individuals" described a tree missing
   190 people; at 17 there is no concentration left to measure. It was a true
   description of a state, not a property of the graph, and it is worth being
   explicit that it is spent rather than leaving it to read as a standing fact.

   **Older text below, kept because the predictions in it were scored.**

   **Re-measured 2026-08-06 late, over the 103-export merge, by
   `python -m genimerge connectors`:**
   `reports/connectors.md` and `out/connectors.html` are now the live answer;
   do not read the counts in this item as current. **3 274 of 3 464 steps held
   (94.5%), 13 of 26 paths complete, 16 bridges in 12 clusters.** Two things
   changed: the four `exports/edges/` takes closed the
   'A'idhullah al-'Ashiri `6000000226741965864` bridge **entirely**, and a
   defect in `genimerge.paths` was fixed that had been reporting people we
   hold as missing (see the devlog entry — a person walked twice on one path
   was reported `ABSENT` the second time, and `nn-basse` is 57/57, not 47/57).

0.05 **The P2600 overlap is measured — `reports/wikidata-overlap.md`,
   2026-08-06.** Emma's ask, answered: **9,026 in both — 4.44% of our tree,
   1.75% of Wikidata's 516,913 Geni-linked IDs.** 507,859 people have a Geni
   profile Wikidata names and no export here has reached. `genimerge overlap`
   pulls all of P2600 in sixteen MD5 partitions rather than asking about our own
   IDs, which is the only way to see that second number at all.

   **What came out of it that is work rather than a number: 44 Wikidata items
   carry two Geni IDs that are *both* people in our tree.** Our merge keys on
   the profile ID, so it cannot see this — two IDs are two people to it, by
   construction. Reviewing those 44 is a human job and is genuinely open:

   - It is **not** a duplicate list. `Брячислав Васильевич` against
     `Bracheslav Vasylkovich Polozki` is one person in two languages;
     `Scribonia` against `Clodia Pulchra` is two of Octavian's wives and one of
     those P2600 statements is just wrong. Both readings occur and nothing in
     this repo separates them.
   - **Answered 2026-08-06: Emma wants the list, and it exists.**
     `python -m genimerge doubles` writes `reports/wikidata-doubles.md` and
     `out/wikidata-doubles.html`, putting the two profiles side by side with
     dates, sex, parents, spouses and children so a human can judge. Offline:
     it reads the map `overlap` already fetched. Over the 253,788-person merge
     the 44 hold: **21 share a relative, 4 share a name, 0 have births more
     than 120 years apart.** What happens to a pair Emma confirms is still
     hers to decide, and nothing here edits Geni or Wikidata.
   - None of the 44 are Japanese emperors, so this instrument did **not** catch
     the Emperor Ojin duplicates in item 0.2 below. Worth knowing why: it can
     only see a duplicate that Wikidata has already noticed and linked twice.

   Smaller, and both are read-only findings rather than tasks: 67 Geni IDs sit
   on two Wikidata items (5 of them ours), and 28 P2600 values are not profile
   IDs at all — mostly pasted `geni.com/people/…` URLs. 24 have an ID inside,
   and recovering it is **UNSAFE-TO-GUESS** in one specific way the report
   names: a URL with `?through=` carries two IDs and the one after the `?` is a
   different person, so the obvious "take the last digit-run" links the wrong
   human.

0.1 I have done a large amount of exports that definitely fleshed out the trees based off of your suggestions, although geni seems to have crapped out a bit, so it's probably gonna be tomorrow. Integrate these things when they arrive. I feel like they're probably going to be the last because I don't know what's going on with geni right now, but it's a bit difficult to get things to run. 

   **Four of them arrived and are in, 2026-08-06 evening** — `exports/edges/`,
   seeds `…085797849`, `…085766947`, `…085871850`, `…085828865`, none of them in
   any earlier export. Two further zips in the same batch were byte-identical
   repeats of committed files. The *measuring* of what they added is item 0.001,
   which is waiting on a machine that can spin up. This item stays open because
   Emma's "probably the last" is a prediction about Geni, not a statement that
   the batch is closed.

0.2 As another thing, there were some profile merges and edits related to Japanese emperors, particularly Emperor Ojin, and I just want you to keep in mind that this is the case. You probably will be able to see it in the data somewhere. Not 100% sure you probably would, because there were duplicates of Emperor Ojin and some other people. 

1. **BLOCKED-ON-USER-ACTION — export from `NN 高円宮` `6000000209740059823`.**
   The one individual on `individuals I can easily export.txt` that is **not in
   the tree**, and it is not merely unmerged: grepping the whole repo finds that
   ID in no export, not even as somebody's relative. The other 17 are all held.
   That makes it the only entry on the list that is certain to bring material we
   have none of. Everything else there is a re-sample of a neighbourhood we
   already touched.

2. **Review and run `out/wikidata/entity-resolution.qs`.** Six P2600 statements
   and three English label edits from `entity_resolution.md`. All six Geni
   profiles are in the tree. **BLOCKED-ON-USER-ACTION** — nothing here sends
   anything to Wikidata, and label edits overwrite other editors' work.

3. **BLOCKED-ON-USER-ACTION — the next four exports, picked 2026-08-05 from
   `reports/density.md`.** Unblock signal is a new `.ged` under `exports/`. All
   four seeds were checked against `out/people.jsonl`: every one is in the tree
   and every one has empty `parent_ids`, so all four are doorways. **Take them
   as `Forest`.** These regions are runs of people linked by marriage as well as
   descent, and a doorway opens *upward*, so `Descendants` walks the wrong way
   and `Ancestors`/`BloodTree` walk past the spouse links — the same trap that
   nearly cost the Jimmu bridge.

   | order | region | people | doorways | density | ball fit | seed |
   | ---: | ---: | ---: | ---: | ---: | ---: | --- |
   | 1 | 6 | 2561 | 957 | 37.4% | 0.66× | [Christen Pedersen Thrane](https://www.geni.com/people/x/5132829956720138378) `5132829956720138378` |
   | 2 | 3 | 3588 | 977 | 27.2% | 0.93× | [William "Bill" Rankin Monk](https://www.geni.com/people/x/6000000005965721836) `6000000005965721836` |
   | 3 | 1 | 6475 | 1757 | 27.1% | 1.68× | [Juan Andrés](https://www.geni.com/people/x/6000000014746707044) `6000000014746707044` |
   | 4 | 2 | 3858 | 854 | 22.1% | 1.00× | [Mercy Swetland](https://www.geni.com/people/x/6000000014643729729) `6000000014643729729` |

   **Why this order and not simply largest-first.** An export is a ball of at
   most ~3860 people (`GENI_EXPORT_CAP`, largest yet seen), so a region bigger
   than that cannot be covered by one take — the "ball fit" column is
   people ÷ 3860. Region 6 is ranked first because the *whole* region fits
   inside one ball with room to spare and it has the highest doorway density in
   the report at 37.4%: the largest share of the budget converts into walking
   somewhere new rather than re-fetching people we hold. Region 3 is second on
   raw doorways (977, the most of any region that fits in a single ball).
   Region 1 has the most doorways of all, 1757, but at 1.68× it needs at least
   two exports and only one seed exists for it — take one now and **re-run
   `python -m genimerge density` before choosing the second**, so the second
   seed is picked knowing where the first ball landed.

   **What to skip, and why it is in the report at all.** Regions 35, 38, 40, 42
   and 47 have **zero** doorways — nothing there opens outward, so an export
   buys only people we already have. Region 8 (Fakhita القشيري, 2355 people) is
   the large low-density case at 9.8%: a whole ball spent to reach few new
   places. Region 4 (Jøran Svensdatter, 3563/612, 17.2%) is the weakest of the
   big four and is the one to drop if only three exports get taken.

   **This is the first pick density has ever made, and it is untested** — the
   same standing objection as `reports/seeds.md`, which has also never been
   scored against an outcome. It resolves by measuring: after the export lands,
   `python -m genimerge merge` gives the new-people count and re-running
   `density` should show region 6 shrink or split. Recording the prediction here
   so `git show` supplies it later — **region 6 is predicted to yield more new
   people than region 4 would have**, on the density argument alone.

   **Still unscored as of 2026-08-06 late, and the seeds and region numbers
   above are stale.** `density` was re-run over the 103-export merge
   (126 060 of 208 089 people in ≤1 export, 5 814 regions), but none of the
   four new exports was seeded on a pick from this table, so the prediction has
   not been tested — it needs an export *from one of these seeds*. Re-read
   `reports/density.md` for current seeds before acting: region numbering is
   positional and has already shifted twice under it.

4. **BLOCKED-ON-USER-ACTION — run the 1000-item Wikidata pilot.** The unblock
   signal is Emma saying go; the command exists and is offline-tested:

   ```
   python -m genimerge wikidata-download --limit 1000
   ```

   It prints the four numbers the 500k run should not be designed without: the
   sustained rate, whether 50-per-request behaves as documented, the mean
   full-item JSON size, and what those project to over the whole seed set. Read
   them before starting the long run. `todo.md` §§ 8a-revised and 8a-decided are
   the design; `chats/wikidata-querying-2026-08-07.md` is where it came from.

   **Nothing else may query Wikidata — not a spot check, not one QID.** Emma's
   rule, 2026-08-07: a stray request is how the run collects a 429. Questions
   about Wikidata's contents go to `todo.md` § 8b and wait for the store.

   After the pilot, the long run is the same command without `--limit`, and it
   is a multi-day background job. Commit and push the shards as it goes —
   every 500-1000 items, never per item.

6. **The Wikidata reports are stale.** `reports/wikidata-coverage.md`,
   `wikidata-crosscheck.md` and `names.md` describe the 16266-person tree; it is
   now 105349. Refreshing means `reconcile` against the live SPARQL endpoint,
   the only networked step here.

### Standing context

- **BLOCKED-ON-USER-ACTION — impossible dates in the tree, listed in
  `reports/consistency.md`.** Someone born before a parent, or after their
  mother died. Every one is an error in Geni's data rather than in the merge, so
  fixing them means editing profiles on Geni; this repo will not change them.
  A further set are implausible rather than impossible — a parent under 12, a
  lifespan over 120 — and some of those will turn out to be correct.

  **This entry said 96 impossible and 89 implausible, "re-measured 2026-08-02
  over the five-export merge", until 2026-08-06.** The report says **3,189** and
  **1,966** over 202,433 people. The number was not wrong when written; it was
  left behind by 94 exports, which is what a count copied into prose does. It is
  not restated here now — **read `reports/consistency.md`**, the same rule
  `todo.md` § 3a already applies to `reports/frontier.md`.

  Worth doing before the QuickStatements batches rather than after:
  `add-claims.qs` carries P569 and P570 statements built from these same dates,
  so an uncorrected year here becomes a wrong year on Wikidata.



- **The Jimmu chain, 62/83 → 77/83 → 83/83, is finished and its long note is
  deleted (2026-08-06).** The note ended by saying it could go once nobody
  thought it load-bearing; the 99-export re-run holds both jimmu path files at
  **83 of 83**, so the arc is closed. What it taught survives in `CLAUDE.md` —
  read the relation column before choosing an export style, because two of the
  six bridging steps are reachable only through a marriage — and the numbers are
  in `devlog.md` and `git log`. A 21-step gap took four exports, not the one
  originally planned; that is the part worth remembering.

- **Not doing: centralising the per-module property constants.**
  `crosscheck`, `reconcile`, `namelinks`, `names` and `quickstatements` each
  declare the property IDs they use at the top of the file. That is local and
  readable, and a shared registry would move them away from the code explaining
  why they are there; `CLAUDE.md` already serves as the cross-module reference.
  Recorded so a later sweep does not re-open it as though it were an oversight.



- **NEEDS-INVESTIGATION — smallest-ball is the only ordering that surfaces the
  known-good seed, and it rests on one observation.** Hågen Iversen placed 38 of
  2336 by smallest ball, against 2261 by the shipped doorway count and 1303 by
  openness. The mechanism is plausible — a tiny neighbourhood is one we know
  almost nothing about — and the obvious objection turned out to be wrong, since
  the shortlist is 66 candidates with none isolated. It is **not** adopted and
  must not be until there is more than one data point. Resolves by taking one
  export from a top-ranked pick and one from the small-ball shortlist and
  comparing new-people counts. Not blocking anything.

- **NEEDS-INVESTIGATION — the seed ranking has never been tested.** No export
  has been taken from a seed `reports/seeds.md` chose. The one export with
  measured results was seeded on the parent of Hågen Iversen, who placed 2255 of
  2336 (ball 5, one doorway), and returned 3656 new people. That is a reason to
  doubt ranking by absolute doorway count — a large ball is a densely recorded
  neighbourhood, which is the opposite of where Geni has most to add — but it is
  n=1 and the ranking never scored the actual seed, who was not in our data. It
  resolves by taking the next export from a top-ranked pick and comparing. The
  prediction is already committed in `reports/seeds.md`, so `git show` will
  supply it when the fifth export lands. Not blocking anything.

- **UNSAFE-TO-GUESS — two links flagged as worth re-checking, both exact P2600.**
  `reports/wikidata-crosscheck.md` § "Links worth re-checking" names Canute I
  Erikska `Q442876` (0 agreements, 4 conflicts, birth 1145 against 857) and
  Bengt Folkesson `Q1621801` (1 agreement, 2 conflicts). Both are matched by the
  Geni ID on the item, not by inference, so the ID itself is under as much
  suspicion as the match. Two readings fit and nothing in this repo separates
  them: the link is wrong, or it is right and one side's data is badly wrong.
  Resolving one means a human comparing the Geni profile against the Wikidata
  item. Nothing should edit either side on a guess.

- **NEEDS-DECISION — how out-of-tree export seeds are found.** `reports/seeds.md`
  can only rank people already in the merged tree. Iver Mellegård, who seeded
  the best export so far, was in none of the three earlier exports, so the
  ranking could not have proposed him. Whatever route found him is one this repo
  cannot see or reproduce. **Seen twice now:** the 2026-08-02 seed
  `6000000226989731860` was likewise in none of the four earlier exports, and
  produced an export that overlaps them by zero people. Two of the five exports
  came from seeds this repo had no way to name. The question is with the user;
  the answer decides whether to build out-of-tree candidate ranking or something
  else. Not blocking anything currently queued.

- **Take the pipeline order from `README.md`, not from a list written by hand.**
  The README's "before pushing" block already gives every command in dependency
  order, and it says `expand --search`, not bare `expand`. Both details matter.
  `expand` writes `matched_all.csv` and `candidates.csv`, which `coverage`,
  `crosscheck`, `name-links` and `quickstatements` all read, so omitting it
  leaves four reports generated from a previous tree. And bare `expand` skips
  the label-index lookup that produces the `name-match` proposals — running it
  without `--search` silently drops 100 of them and rewrites
  `reports/wikidata-coverage.md` with 30 proposals instead of 87. That is not
  hypothetical: it happened on 2026-08-01 and was caught only by diffing the
  regenerated report.

- **`python` on PATH is not the interpreter.** Python 3.13.14 is installed at
  `C:\Program Files\Python313\python.exe`, but the Microsoft Store stub aliases
  in `WindowsApps\` come first on PATH, so the bare `python -m pytest` written
  throughout `CLAUDE.md` exits 9009 with "Python was not found". Use `py -m
  pytest` or the full path. The package is not pip-installed either; the CLI
  needs `PYTHONPATH=src` (pytest gets this from `pythonpath = ["src"]` in
  `pyproject.toml`, which is why the suite runs but `python -m genimerge` does
  not). Not worth changing the user's PATH over, but worth not rediscovering.
- **NEEDS-INVESTIGATION — what actually bounds a Geni export is still unknown.**
  The code does not claim to know: `GENI_EXPORT_CAP` is documented as the largest
  export *observed* — **4008** since 2026-08-05 — rather than a limit Geni
  enforces, and `tests/test_seeds.py` fails if one exceeds it, which is how 3840,
  3844, 3856 and the 4008 were each caught. What is unresolved is the underlying
  fact. Ninety-nine exports still cannot separate a raised limit from a
  per-account limit from a limit on something other than head count from a walk
  that overshoots a floor. **The even spacing was a trap and the data has since
  said so**: three numbers four apart looked like a step of four, then eleven
  exports in a row held 3860 exactly, then a pair taken seven minutes apart held
  3972 and 4008. Nothing in the code encodes any arithmetic. This advances as
  data arrives rather than by being worked on, and is not blocking anything —
  being off by a few people out of ~4000 does not move the seed ranking.

- **CI is off on purpose, and stays off.** Not a blocker — a decision. This is a
  private repo, where Actions minutes are billable rather than free, and
  push-triggered CI was never worth that risk. `ci.yml` is now
  `workflow_dispatch:` only and the workflow is disabled at the GitHub end.
  Verification is `python -m pytest` before pushing. The cost of that choice is
  named rather than hidden: **the Python version matrix does not run**, so 3.10
  is exercised only by the static check in `tests/test_python_floor.py`, and no
  commit should be described as CI-verified.
- **NEEDS-DECISION** — `todo.md` items 4 and 5: creating Wikidata items, for
  people who have none and for the **1540 surnames and 4986 given-name tokens**
  that have none. Sized in `reports/names.md` over the five-export merge: 1167
  of 2707 distinct surnames (43.1%) and 2419 of 7405 distinct given-name tokens
  (32.7%) have an item, so the rest do not. Whole given-name strings as Geni
  stores them are far worse — 1186 of 11772 (10.1%) — because Geni packs
  multiple names into one field. The fifth export roughly doubled the
  given-token pool and dropped coverage from 56.1% to 32.7%: the Japanese
  component's names are much less represented on Wikidata than the Norwegian
  ones. The decision is the user's.

---

## Always last — restart the three crons and summarize

**These two items stay pinned to the tail of the queue at all times** — below every real work item:

A. **Ensure the three crons are running** — start them if this session never did, restart them if a planning burst / queue re-fill killed them: work-loop (`3 * * * *`), auto-flush (`15 * * * *`), status-report (`42 * * * *`).
B. **Run the status-report action once more, independently** — an end-of-session summary of everything that happened this session.

---

## Pointers

- Long-horizon backlog (abstract goals, source of future queue items): `todo.md`.
- Completed work (chronological, with releases): `devlog.md`.
- Narrative history: `git log`.
