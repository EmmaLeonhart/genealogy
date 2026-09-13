# The relationship anchor

**Superseded at the top, 2026-09-13, and the rest of the page is kept for its measurements.**
This file used to open by saying the anchor *"decides what every path capture MEANS"* and that a
run against the wrong one *"produces a number that answers a different question and looks
identical"*. That is true of a REACH-RATE REPORT and false of a capture, and the two were
conflated here for a week.

**A capture is a chain of named people with Geni ids.** Those edges are worth the same whichever
end Geni started the chain from, and whether the person joins the world tree is decided by the
connectivity rebuild reading the merged corpus — later, elsewhere, and not by the pushpin. See
the ruling below.

The protocol further down is still the correct way to move the pin **when you have a reason to
move it**, and the 2026-09-06 measurement on Rudolf Beck is still the evidence that moving it
changes the question. What has changed is that moving it is no longer a precondition for doing
the work.

## ⛔ "SET EXACTLY ONCE" WAS A SHORTCUT, NOT A LAW. Recorded as a law, it cost a day

**A protocol can set the anchor on Charlemagne** — ruled 2026-09-06, correcting a rule invented
from a shortcut.

The 2026-09-03 wording — *do not pin Charlemagne, it needs to be done exactly once and it is
done* — was about a session that stalled on the page, and the pin was set by hand to unblock the
work. That got recorded in `CLAUDE.md` and `queue.md` as though the pin were untouchable, so when
the first real capture came back anchored on the viewer it was reported as **NEEDS-DECISION** and
left sitting. It was never a decision. It was a thing to check and set.

**The general fault, worth more than this instance: a shortcut taken by hand to unblock the work
became a constraint enforced against the person who took it.** When something is done by hand
because the automation is stuck, the lesson is *automate it*, not *this is sacred*.

## ⛔ THE ANCHOR IS NOT THE ROOT, AND IT DOES NOT DECIDE ANYTHING. Ruled 2026-09-13

*"Charlemagne is not the root, the root is just whoever geni wants to display. Could be
Charlemagne, could be me, could be some random king. Doesn't matter. The pipeline will
periodically update the linkedness of the people and figure out who is connected ... it will have
a path but it is not connected to the world tree and the synoptic tree rebuild pipeline stuff
will pick it up and consistently mark it as needing work."*

**So a capture cannot be invalidated by its anchor.** What a path capture produces is a CHAIN OF
NAMED PEOPLE WITH GENI IDS, and those edges are worth the same whichever end Geni started from.
Whether the person ends up joined to the world tree is decided **later and elsewhere**, by the
connectivity rebuild reading the merged corpus — not by which profile the pushpin was on when the
page rendered.

**This supersedes the framing of the rest of this page.** *Check, set, verify* is written as
though a viewer anchor were a fault to be corrected before real work could happen, and the
2026-09-06 entry treats a viewer-anchored capture as a run that "produces a number that answers a
different question". That is too strong. The reach-rate REPORT wants a consistent anchor; the
captures do not, and the two were conflated.

**What follows in practice:**

* **Do not spend page loads checking or setting the pin before a run.** Capture whatever Geni
  displays. The pin is worth moving when a run is being taken specifically to report a reach rate
  to one person, and not otherwise.
* **Record the anchor and move on.** `reports/isolates.csv` has the `anchor` column; it is
  provenance, not a gate. A row reading `viewer` is not a row to re-run.
* **A weird or failed capture is self-correcting.** The worklist is rebuilt from the corpus every
  run, so a person whose path did not join them to the tree simply keeps appearing as outstanding
  work. Nothing has to be detected or retried by hand.

## The protocol

1. **CHECK, on evidence rather than on the pin's appearance.** Load Charlemagne
   `6000000002457013227`. The banner reads either
   *"Charlemagne is your 35th great grandfather"* — anchored on the **viewer** — or
   *"View other profiles to see their relationship to Charlemagne"* — anchored on **him**.
   The pin's own CSS class is `pushpin-green` in both states and says nothing.
2. **SET only if it reads viewer-anchored.** Click the pin at the top-right of the relationship
   banner. **Never toggle blind**: the same control unsets it, and its tooltip says so —
   *"Click the push pin again to reset them to yourself."*
3. **VERIFY on a real target, never on the pin.** Load a profile with a known viewer-anchored
   answer and confirm it changed. Rudolf Beck `6000000026849996554` is the worked case: he
   resolved to a **23-step chain to the viewer** at 14:xx, and after the anchor moved the same page read
   **"No blood relationship was found"** — the question demonstrably changed.

**Calling `toggleRelationshipAnchor(...)` from the page world is blocked by the permission
classifier**, so the click is the mechanism. That is fine and arguably better: it is the same
action a person takes, and it leaves the tooltip visible to read back.

## ⛔ THERE IS A THIRD STATE: ANCHORED ON SOMEBODY ELSE ENTIRELY

**Found 2026-09-09.** The protocol above names two states — viewer, or Charlemagne. A third
exists and it is what was actually found: the pin was on **Lǐ Shìmín 李世民, Emperor Taizong of
Tang**, so every page read *"… is connected to Lǐ Shìmín"* and Charlemagne's own page read
*"Charlemagne is Lǐ Shìmín's 8th great nephew's wife's mother's partner's wife's fiancé's 6th
great grandfather."*

**Step 1's test must therefore be positive, not a negation.** *"Not viewer-anchored"* does not
mean *anchored on Charlemagne* — it meant anchored on a Tang emperor. The check that works is
the one already used per-capture: does the banner name **Charlemagne** as the other end?

**AND IT TAKES TWO CLICKS FROM THAT STATE.** The pin is a toggle against the VIEWER, not a
three-way switch:

    on Lǐ Shìmín   --click-->  "Charlemagne is your 35th great grandfather"   (viewer)
    viewer         --click-->  "View other profiles to see their relationship to Charlemagne"

So a single click from the third state lands on the state being left. Read the
banner between the two clicks; do not fire them blind as a pair.

## ⛔ THE SCREENSHOT AND THE PAGE DISAGREE ON COORDINATES, AND THE FIRST CLICK MISSED

`getBoundingClientRect()` put the pin at **(1215, 256)**; it renders in the screenshot at
**(1240, 261)**. The `computer` tool takes SCREENSHOT coordinates, so the JS-derived pair missed
the element and the page did not change — which reads exactly like a click that was ignored, and
sent this session looking for a permission problem that was not there.

The ratio is about **1.021** here and it is a property of the display rather than of the page, so
it must not be hard-coded. **Take a screenshot and read the pin off it**, or click by element
`ref` from `find`/`read_page`. Do not compute a click target from `getBoundingClientRect`.

### It moved TWICE on 2026-09-09, and the second time onto a profile we had just created

**First to Lǐ Shìmín 李世民, Emperor Taizong of Tang**, found when Charlemagne's own page read
*"Charlemagne is Lǐ Shìmín's 8th great nephew's wife's mother's partner's wife's fiancé's 6th
great grandfather."*

**Then, hours later, onto `NN`** — one of the placeholder ancestors created that afternoon.
Anders Danielsson Falk's page read *"NN is connected to Anders Danielsson Falk"* and
Charlemagne's read *"NN is connected to Charlemagne"*.

**⛔ THAT WAS EMMA, AND IT IS NOT A HAZARD. I guessed at a cause and guessed wrong.** I wrote
that creating placeholders and running exports had dragged the anchor along, and called it a
per-run hazard. Her correction, same day: *"that is something I did and it is not likely to be
that much of a big issue moving forward … It is not some kind of run hazard lol I just assumed
the logic was good."*

So the anchor moved because **she moved it**, working on her own profiles. Nothing in the
collector does it, and no run needs to be treated as suspect for having created a person or run
an export. What survives is only what was actually measured: the anchor can be on a third party,
and the per-capture check catches it for free.

**And her expectation is that the EXTENSION sets it**: *"I am assuming the extension is good for
setting the anchor to charlemange lol."* It is not — nothing in `geni-extension/` touches the
pin, by deliberate rule (`test_the_pushpin_is_never_toggled`, which stops a *job* flipping it
mid-run). Setting it out of band, once, is a different operation from a job toggling it, and the
extension could own that. It does not today.

**It cost nothing, and that is the point of the per-capture check.** `anchorOk` is a single
regex on the banner and it caught the state before a single row was written. Nothing was filed
under the wrong question either time.

**Both resets needed TWO clicks**, because the pin toggles against the viewer rather than being a
three-way switch: `NN` → viewer → Charlemagne, with the banner read in between so neither click
is blind.

## What the collector may and may not do

`tests/test_geni_extension.py::test_the_pushpin_is_never_toggled` **stays**, and it is not
weakened by this document. A *job* must never toggle the anchor: a `path` or `family` job that
flipped it mid-run would silently re-anchor every capture after it, which is the failure the
original instruction named. Setting the anchor is a deliberate, verified, out-of-band operation —
this protocol — and never a side effect of collecting.

## Bookkeeping this changes

`reports/isolates.csv`'s `path_found` column now means *a path to Charlemagne*. Rudolf Beck's
`yes` predates the anchor and is a **viewer-anchored** result; his Charlemagne answer is a blood
miss with in-law unchecked. His path file
`paths/isolate-geni-rudolf-beck-1919-c1941.tsv` stays — viewer-anchored paths are live work by
standing ruling — but it is not a pilot hit and must not be counted as one.

## ⛔ THE ANCHOR DECAYS. IT CAME OFF CHARLEMAGNE MID-RUN ON 2026-09-06

**It was set at the start of the evening, produced ten verified Charlemagne captures, and was
back on the viewer a few hours later without anyone touching it.** Caught on Sophia Elisabeth
Sahlin `2892509`, whose capture came back with **step 1 = `You`** and Geni's prose reading
*"is your 15th cousin 7 times removed"*. The two targets running beside it, Anna Throndsen
`296165995120003655` and Anna Hørlück `297536201290008921`, were the same.

**Nothing in the capture announces it.** A viewer-anchored hit is a hit: `resolved_path`,
`hasTarget` true, a full chain, a confident prose sentence. It parses, it writes, it counts —
and it answers *how is this person related to the viewer*. Had the three been filed by the ordinary
route they would have entered `reports/isolates.csv` stamped `charlemagne`, because
`write-family-scrape.py` carries `ANCHOR` as a module constant and cannot see the page.

**So the anchor is not something set once a session either.** *"Set exactly once"* was already
recorded above as a shortcut mistaken for a law; this is the same lesson one level down — set
once **per run** is also wrong, because the anchor expires on its own.

### The check that costs nothing and must be done

**Step 1 of every captured chain is the anchor.** If it is Charlemagne
`geni:6000000002457013227`, the capture answers the pilot's question. If it is `You`
`geni:6000000087535357291`, it does not. Geni's prose says the same thing in words —
*"is Charlemagne's Nth great grandson"* against *"is your ..."* — and both are already in the
result the collector hands back.

Read one of them before writing any path file. It is free, it is per-capture rather than
per-session, and it is the only thing that survives the anchor expiring at an unknown moment.

**A miss needs the same care and gives less warning**, because a miss has no chain to read step 1
from. The banner wording is identical under either anchor. The only protection there is that the
anchor was verified recently — which is why the check above is per-capture and why a run that
finds a viewer-anchored hit should treat every miss since the last verified capture as suspect.

### What was done

The three were **not** filed as Charlemagne results. The anchor was re-set by this protocol —
checked on Charlemagne's own page, clicked, and verified on two independent targets: Rudolf Beck
went from a viewer-anchored in-law chain to *"How are they related"*, and Sahlin's page went to
*"Charlemagne is connected to Sophia Elisabeth"*. Then all three were re-run.

### Re-set again 2026-09-09, from the Lǐ Shìmín state

Checked on Charlemagne's own page, clicked twice with the banner read in between, and verified on
two independent targets that had been captured earlier the same day: Ellen Margrethe Charlotte
Jessen `360492713900012510` read *"Charlemagne's 35th great granddaughter"* and Louis d'Anjou
`368713820640003185` read *"Charlemagne's 15th great grandson"* — both matching the chains
already on disk, which verifies the anchor and corroborates those captures at the same time.

**The ten captures taken earlier are unaffected and were checked rather than assumed** — every
one of them has Charlemagne as step 1 and *"is Charlemagne's Nth great grand-"* in its prose,
both recorded in the files.
