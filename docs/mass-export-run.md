# The mass export campaign — the run sheet

**Status, 2026-08-29: ALL FOUR GROUPS DONE.** Group 4 finished 2026-08-28 at about 14:00 Pacific
after 40 exports — **all 251 Bureätten people with a Geni id are in `exports/`, 0 absent**.

**A caution for whoever reads this next.** For a day afterwards `bure-coverage.py` reported *100
still absent*, and it was believed and repeated in two status reports. The script marked freshness
off `reports/derived-labels.csv` rather than `out/merged.ged`; the former is derived from the
latter, so regenerating it stamped it Aug 28 18:24 while the tree behind it was Aug 24 18:20, and
every campaign export fell in the gap. **Check what a coverage number is measured against before
trusting it** — Emma spotted this from memory alone, asking why a campaign she thought was finished
was being reported as outstanding.

---

**Status, 2026-08-28 (historical): group 1 DONE, group 2 RUNNING, group 3 dropped, group 4 AUTHORISED.**
The captcha that stopped the first attempt has not reappeared. Emma authorised the placeholder
seeds group 4 needs -- *"And yes I'm authorizing new seed people on all of these people lol"* --
so the campaign runs end to end from here.

Emma, 2026-08-28: *"Mass export these using our export protocol. Export from them and if their ids
were merged or moved record it each time and the other stuff. Do the earlier queued exports first
and then these — the big export thing is the current front queue task now, all of the other geni
exports in the queue first and then the bure people until we have all the ids."*

And, on the block: *"work on later queue items while I take the bus home."* So the rest of the
queue proceeds; this resumes when the captcha is cleared.

---

## The order

### 1. `6000000227464556886` — Eva Walaas — `Forest` **and** `Ancestors`

Her 1am item, in her words: *"do a forest export and ancestor export on
https://www.geni.com/profile/index/6000000227464556886 and incorporate them into the synoptic
tree and then rebuild the synoptic tree, and then generate the quickstatements with the
algorithm."*

- Ledger already pairs the profile with `Q109660986`.
- **Corpus check done 2026-08-28: 0 of 558 exports contain `@I6000000227464556886@`.** Worth
  running.
- Two styles, so two files: `export-Forest-6000000227464556886.ged` and
  `export-Ancestors-6000000227464556886.ged`.
- Afterwards: re-merge, rebuild the derived layer (**`build-display-names.py` first** — it is the
  only script that reads the merged tree, and `derive-labels.py` reads its output without
  building it), then `build-daily-batch.py`.

### 2. `Q10411463` Andreas Olai — `Forest` — **id found, export running**

**Geni `6000000040951562251`.** Emma supplied the profile URL after the search route dead-ended,
and it confirms structurally: the About text reads *"Andreas Olai, född 1521 i Örebro, död 1560,
var en svensk ämbetsman"*, matching the item's `P569` 1521, `P570` 1560 and its description
*Swedish civil servant*; *"Son of Olof, Brother of Kerstin Olofsdotter and Benedictus Olai"*
matches `P3373` *sibling* → `Q4355463`. The `P1889` *different from* separates him from the
better-known Andreas Olai, so the name alone could never have settled it.

**The trap worth writing down: the structured Birth field says "estimated between 1450 and
1570".** The real dates are only in the prose. Anything matching on the structured field
would have called this person unmatchable, which is exactly what happened.

The pairing is now in `build-garborg-day.py`'s hard-coded `P2600` block, on Emma's instruction:
*"we add this qid geni id add thing to the quickstatements block that always gets added in"*.

Neither he (0 exports) nor his brother `6000000040951399522` (0) is in the corpus, so
**Export GEDCOM is not offered** on either — Emma manages neither profile. Seeded instead, tier 3:
`NN` **`6000000227468650841`**, his mother, at the open *Add mother* slot beside his father Olof.

### 3. The eight `entity_resolution.md` people — `Forest` each

Everyone in that file **except Emma**. She withdrew the Geni-bio-editing half of this item on
2026-08-27 — *"we don't actually need to edit your geni at all for this"* — so only the exports
remain.

| Geni id | QID | who |
| --- | --- | --- |
| 6000000001835522164 | `Q11596350` | Wakatakehiko |
| 6000000001844033355 | `Q11078587` | Harima no Inabi no Ōiratsume |
| 6000000001902786893 | `Q11443857` | Futohime Mononobe |
| 6000000002039751362 | `Q24890131` | Ikofutsu Mononobe |
| 6000000186285688253 | `Q19657284` | Buyeo Deokjang |
| 6000000186285688286 | `Q12598947` | Taebi Buyeo |
| 6000000227335224861 | `Q135579480` | Yasutaka Kitajima |
| 6000000227335393824 | `Q135579474` | Tokitaka Kitajima |

`6000000001846508982` → `Q232803` is **Emma and is skipped**.

### 4. The Bureätten people — COVERAGE of 251, not an export each

**Emma, 2026-08-28:** *"the bure people here we don't need to export from all of them we just
need to get all of them in exports"*.

So the target is that all 251 sv.wikipedia Category:Bureätten people carrying a Geni id end up
**somewhere in `exports/`**, and the number of exports that takes is whatever it takes. A
`Forest` export returns up to 5000 people and the Bureätten are one kinship network, so one
export seeded inside it can sweep in many of them at once. Seeding all 100 absent people would
be mostly redundant.

**The loop, therefore:**

1. `python scripts/bure-coverage.py` — writes `reports/bure-coverage.tsv` (all 251, with where
   each was found) and rewrites `reports/bure-to-export.tsv` (the still-absent ones).
2. Take an absent person, seed per `docs/export-seed-rules.md`, export `Forest`/5000.
3. File the `.ged`, then **run the coverage script again**. Whoever the export swept in drops
   off the list without an export of their own.
4. Repeat until `bure-to-export.tsv` is empty.

**State as of 2026-08-28: 151 of 251 held, 100 absent** — which independently reproduces the
number the first derivation got, by a different route.

They are the reason this matters: the batch resolves names through `derived-labels.csv`, so a
Bureätten person we do not hold gets no label and cannot be linked.

---

## Protocol — `docs/export-seed-rules.md` and `CLAUDE.md`, not restated loosely

- **Size 5000. Strictly one export at a time.** Zips filed into `exports/` in bulk only once every
  one of them is down.
- **Grep the corpus before each export and put the number in the commit message.** Two exports
  were wasted on 2026-08-23 by skipping this. `grep -l '@I<id>@' exports/**/*.ged`.
- **Never overwrite an existing `.ged`.** An export is named for its *style*, so filenames
  collide: append the seed id. If the destination path exists, **STOP** — where it goes is Emma's
  call, not a default to guess.
- **Do not analyse or diff an export.** Place it, commit, move on.
- Every `.ged` is committed. Every zip gets its own explicit `.gitignore` line — never a pattern,
  because an unignored zip in `git status` is how a download announces itself.
- Where Geni will not export from a profile directly, create a placeholder seed per
  `docs/export-seed-rules.md` and export from there; success is the target person appearing in
  the result.

## The record — `reports/mass-export-log.tsv`

Emma asked for this specifically: *"if their ids were merged or moved record it each time and the
other stuff."*

`geni_id · qid · style · outcome · redirected_to · new_geni_id · ged_file · people · notes`

- A **Geni profile that redirects** means the profiles were merged — record the id landed on in
  `new_geni_id` rather than quietly following it.
- A **QID that redirects** means the items were merged — record it in `redirected_to`.
- `outcome` is one of `exported`, `no-export-offered`, `seed-created`, `redirect`, `failed`.

Both kinds of move are the "weird stuff" Emma expects to find, and the point of writing them down
is that a redirect silently followed looks exactly like a profile that was always there.


---

## What the first hour of running it established

**Group 1 is complete.** `export-Forest-6000000227464556886.ged` 5,000 people (the cap exactly)
and `export-Ancestors-6000000227464556886.ged` 4,309 (matching the profile's own "Ancestors
4,308"). Both in `exports/bure-campaign/`, seed present in each.

**Timing: Forest ~6 minutes, Ancestors ~9.** Geni's form says *"A Forest export may take several
days to complete."* It is not a useful estimate. Emma: *"Forests take on average 6 minutes lol."*

**Clicking the download link by accessibility ref silently fails.** It reports success and no file
lands. Click it by coordinate.

**Group 2 (Andreas Olai) is blocked and it is not a dates problem.** He was identified
structurally — a Geni profile reading *"Benedictus Olai, Son of Olof, Brother of Kerstin
Olofsdotter and Andreas Olai"* matches Wikidata's `P3373` sibling `Q4355463` exactly. But **every
search-result link on Geni is Pro-gated**: the name and "View Profile" both resolve to
`geni.com/pro/signup`, and the only ungated `/people/` href on a results page is Emma's own
profile. Emma: *"geni search is a trap designed to upsell."* So search can confirm a person
exists and can never yield their id.

**Group 3 is dropped.** All eight are already in the corpus **3 to 15 times over**, and the export
existed to capture a Wikidata link in their Geni bio — which she withdrew when she moved that
injection into the synoptic tree build. Both the novelty and the purpose are gone.

**Group 4 needs 100 placeholder seeds, and Emma authorised them.** A direct profile URL works
without Pro — `geni.com/people/x/<id>` opened Nils Adolf Erik Nordenskiöld fine. But **Export
GEDCOM is absent from the Actions menu on a profile Emma does not manage**; that menu offers
Ancestor Report, Descendant Report and Merge This Profile and no export. So each of the 100 needs
the placeholder-seed technique: create a profile she manages in the target's neighbourhood, export
from it, and count success when the target appears in the result. That is 100 new Geni profiles,
which is hers to authorise and she did: *"And yes I'm authorizing new seed people on all of these
people lol"*.

**The seed is made in the family-tree view, not on the profile page** — `geni.com/family-tree/
index/<id>` shows the open slots as *Add father* / *Add mother* boxes, which is the whole method.
Two quirks of that canvas, both cost minutes on the first one: a click **pans the tree** rather
than opening the box, so the same box has to be clicked twice at its new position; and clicking a
node opens the profile in a **new tab that reports an empty URL for several seconds** before the
id appears. Neither is an error. Wait, do not re-click, and never search for the person you just
created.
