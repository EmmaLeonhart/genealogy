"""Which profiles to export from next, modelled on what a Geni export is.

A Geni GEDCOM export is a **breadth-first ball**: pick a profile, pick a style
— ancestors, descendants, blood relatives, everything — and Geni walks outward
from that profile until the export is full, at somewhere around 4000 people.
See :data:`GENI_EXPORT_CAP` for why that bound is written as "around" and not
as a number we know. So the question "who do I export from next?" is really
"whose ball would contain the most material we do not already have?".

:mod:`genimerge.frontier` answers a different question. It ranks parentless
people by the descendant count *already in our data*, which measures the known
tree rather than the unknown one, and it has no notion of two candidates
sharing a neighbourhood — its top forty can all hang off the same branch, which
would spend forty exports on one region.

What this module measures instead:

- **Openness.** Within a candidate's ball, how many people have no parents
  recorded. Each of those is a doorway: Geni knows who their parents are and we
  do not. A ball packed with doorways is worth walking through; a ball with
  almost none is a region already recorded several layers deep, and exporting
  from its middle re-fetches what we have.
- **Non-overlap.** Two candidates three hops apart have nearly the same ball,
  so ranking alone hands back one neighbourhood repeatedly.
  :func:`choose_export_set` picks greedily on *newly covered* doorways, which
  is what makes k picks into k useful exports.

**Openness counts doorways, not what is behind them.** We cannot know how many
people sit above a parentless person — not knowing is precisely why they are
worth exporting from. Nothing here predicts how many individuals an export
returns, and the report says so.

**Why doorways are parentless people and not childless ones.** A missing parent
is evidence of missing data: everyone had two. A missing child is not — most
people who appear as leaves really were leaves. Counting childlessness as a
doorway would rank every leaf in the tree as an opportunity.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from statistics import fmean, median

from .frontier import _child_map, _parent_map, family_graph
from .model import Tree

__all__ = [
    "EXPORT_FROM_THE_PARENT",
    "RANKING_IS_UNVALIDATED",
    "SIZE_BIAS_IS_MEASURED",
    "SIZE_BIAS_LIMIT",
    "THE_ONE_RESULT",
    "SMALL_BALL_IS_TESTABLE",
    "SMALL_BALL_IS_THE_OTHER_ARM",
    "SMALL_BALL",
    "SizeBias",
    "size_bias",
    "LARGE_BALL",
    "GENI_EXPORT_CAP",
    "STYLES",
    "Ball",
    "SeedProfile",
    "Pick",
    "edges_for_style",
    "export_ball",
    "profile_seed",
    "rank_seeds",
    "choose_export_set",
    "render_markdown",
]

#: Individuals to model one Geni export as holding: **the largest export we have
#: actually seen**, not a cap we know Geni enforces.
#:
#: **2026-08-06 — Emma states the mechanism, and it is not a Geni-side mystery:
#: the bound is four times the number of profiles she has added.** That explains
#: what the measurements below could not. Every observed value is a multiple of
#: four because the rule multiplies by four. It is not per-style and not
#: per-seed because it is a property of her account's contributions. It rises
#: across a session because she is adding profiles as she goes — which is also
#: why each batch of exports has a higher ceiling than the last, and why seeding
#: placeholders at the frontier raises it as a side effect.
#:
#: The long record below is kept because it is the evidence, and because the
#: readings it rules out are worth not re-proposing. But it is now subordinate
#: to a stated mechanism rather than being the best available guess, and no
#: future observation should be written up as though the cause were unknown.
#:
#: The distinction is not pedantry, because the obvious reading was wrong. The
#: first three exports each held exactly 3836, and since they are three
#: different styles of one seed that reach largely different people — they share
#: only 354 — three separate walks stopping on the same number read as a hard
#: cap. Every export since has held more, so it is not one.
#:
#: **What 90 exports say, ordered by the timestamp in their own `HEAD`:**
#: 3836 ×3 (30 Jul), 3840 (01 Aug), 3844 (02 Aug), then on 04 Aug 3848 at
#: 14:41, 3852 at 14:48, 3856 at 14:53, **3860 for every one of the eleven
#: exports from 15:21 to 16:22**, and that evening 3868, 3928, 3944, 3956,
#: 3972 between 19:15 and 19:55. Then **4008** for four exports from 04 Aug
#: 23:48 to 05 Aug 04:05, and **4004 for all twenty-six exports from 05 Aug
#: 04:17 to 14:57**. Exports holding less than the ceiling (455, 876, 1073,
#: 1192, 1619) each exhausted their component first.
#:
#: Two flat runs — eleven at 3860, twenty-six at 4004 — settle what the
#: three-observation version of this note could only list as possibilities:
#:
#: - **The bound is not per-seed and not per-style.** Those eleven exports were
#:   taken from eleven different seeds in three different styles — `Forest`,
#:   `Descendants`, `BloodTree` — and all landed on 3860 exactly. The
#:   twenty-six are twenty-six further seeds all landing on 4004.
#: - **It is therefore not a walk overshooting a floor** by however much it
#:   takes to finish the generation it is on. Walks through differently-shaped
#:   neighbourhoods would not all overshoot to the same number.
#: - **The ceiling does not only rise, and it never stepped by four.** The
#:   04 Aug evening run climbed 3868 → 3928 → 3944 → 3956 → 3972 in steps of
#:   60, 16, 12 and 16; then 4008 held for four exports and the number went
#:   *down* to 4004, where it stayed for ten and a half hours. An earlier
#:   version of this note called the movement "steps of four" and warned
#:   against encoding it. The warning was right and the description was wrong.
#:
#: **2026-08-05 — Geni states the number in its own UI, which is new evidence
#: and the first that does not come from measuring output.** The GEDCOM export
#: page carries a `Size` field reading "4004 Profiles to export (between 1 and
#: 4004 profiles)", seen at 15:05 on 05 Aug — the same 4004 that twenty-six
#: exports taken that day actually held. So the bound is a number Geni computes
#: per export and displays, not merely something inferable from file sizes.
#: That does **not** make it fixed: four exports hold 4008, above the 4004 the
#: page offered later the same day. What the displayed number tracks, and why
#: it fell by four, are both still unestablished. **Do not encode the
#: arithmetic** — a flat run is evidence the number sits still, not evidence it
#: moves on a schedule, and a movement that has now gone backwards is not one.
#:
#: **2026-08-06 evening — 4020, and the four exports that raised it were taken
#: over nine minutes.** Four `Forest` exports: 4016 at 18:10:37, then 4020 at
#: 18:13:25, 18:17:26 and 18:19:40. So the number rose by four *within a single
#: sitting* and then held for three consecutive exports, having last been
#: measured at 4004 and displayed by Geni's own UI as 4004 the day before.
#: Read against the note above this is one more movement of a ceiling that
#: moves — up this time, having previously gone down — and the flat run of
#: three is again evidence only that it sits still while it sits still.
#: Do not read 4016 → 4020 as a step of four; that reading has been made twice
#: here and falsified twice.
#:
#: **2026-08-06, 20:22-21:23 — twelve exports in one hour, and the number moves
#: both ways inside it.** Ordered by the timestamp in their own `HEAD`:
#: 4020 (`Ancestors`), 4024, 4028, 4032, 4032 (`BloodTree`), **4052**, 4040,
#: **4056**, 4048, 4048, 4052, 4056 (`Descendants`).
#:
#: This is the first batch dense enough in time to see the shape, and it
#: retires the reading that survived every earlier one. Up to here every
#: movement could be told as *a ceiling that changes now and then and holds
#: flat in between* — eleven exports at 3860, twenty-six at 4004, three at
#: 4020. Within this hour it went 4052 → 4040 → 4056 → 4048, so it is **not a
#: ceiling that holds between changes**. Consecutive exports minutes apart
#: differ, and differ downwards as often as upwards.
#:
#: What that rules out, and what it does not:
#:
#: - **Not a per-account or per-day quota being raised.** Those would not fall
#:   back within the hour.
#: - **Still not per-style.** The `Ancestors` take is the lowest of the twelve
#:   and the `Descendants` take ties the highest, with ten `Forest` exports
#:   spanning the whole range in between.
#: - **Not settled: what it actually tracks.** A per-export computed number
#:   varying with the neighbourhood is the obvious candidate — Geni's own UI
#:   displays a `Size` per export, which is how 4004 was seen directly — but
#:   twelve values in one hour cannot separate "depends on the seed's
#:   surroundings" from "depends on load" from "depends on something not
#:   visible here at all". Recorded rather than concluded.
#:
#: **Do not encode the arithmetic.** Read as steps of four this batch looks
#: tidy — every value is a multiple of four — and that reading has now been
#: made and falsified three separate times in this docstring. Multiples of four
#: with no consistent direction is a pattern in the *units*, not in the motion.
#:
#: Used only to bound the modelled ball in :func:`export_ball`, where being off
#: by a few people out of ~4000 does not move a ranking.
#: ``tests/test_seeds.py`` asserts this stays >= the largest export in the
#: corpus, so the next export to exceed it fails loudly instead of silently
#: modelling a ball that is too small. That is how 3840, 3844, 3856, 4008, 4020
#: and now 4068 were each caught.
#:
#: **2026-08-06, 21:23-21:53 — 4060, 4064, 4068 across three `Forest` exports.**
#: Taken minutes apart, and rising monotonically this time where the hour before
#: them did not. Alongside them a `Descendants`, an `Ancestors`, a `BloodTree`
#: and a `Bio` export all held 4056 exactly, and two `Ancestors` takes held 1073
#: and 663 — those two exhausted their component rather than filling.
#: Recorded because the mixed picture is the point: four different styles
#: landing on the same 4056 within twenty minutes, then three consecutive
#: `Forest` takes each four higher than the last. Neither "it sits still" nor
#: "it steps by four" survives both halves.
#:
#: **2026-08-09, 12:32 and 12:49 — 4080, from one seed in two styles.** A
#: `Forest` and a `Descendants` export of `6000000227143930843`, seventeen
#: minutes apart, both exactly 4080. Two things worth separating: the number
#: moved again, three days after the last reading, which is the fourth time;
#: and **two different styles from one seed returned the identical count**,
#: which is the same style-independence the eleven exports of 2026-08-04
#: showed at 3860 and is now seen at a second value. Their *contents* differ —
#: 2459 families against 2283 — so this is not one export downloaded twice.
#:
#: **2026-08-09, 14:26 and 15:03 — 4084 then 4088, two more seeds.** `Forest`
#: exports of `6000000227145420853` ("wife of Samuel Standen") and
#: `6000000227145774838` ("wife of Baruch Jafe"), taken about forty minutes
#: apart. Two readings, each four higher than the last, from *different* seeds —
#: so the step-by-four seen on 2026-08-04 is not an artefact of re-exporting one
#: person. Within a single afternoon the value went 4080 → 4084 → 4088, which is
#: the fastest it has been observed to move and the reason this constant is
#: documented as "the largest seen" rather than a known limit.
#: **2026-08-09, 16:57 and 17:10 - 4092 then 4096.** `Forest` exports of
#: `6000000227147210844` ("Niels NN") and `6000000227147141927` ("wife of
#: Ignazio Malerba"). Five consecutive readings now, each exactly four higher
#: than the last, across five different seeds within five hours: 4080, 4084,
#: 4088, 4092, 4096. At this point "it steps by four" describes the afternoon
#: better than any fixed limit does, and the spacing is roughly how long Emma
#: takes between exports - so this may be tracking Geni's own growth rather
#: than a cap at all. Not asserted, recorded: the next reading either continues
#: the run or breaks it, and both are informative.
#: **2026-08-12/13 — 4100, the run continues.** Two exports read exactly 4100:
#: a `Descendants` of `6000000227212960823` ("Erik", 12 Aug 23:52) and an
#: `Ancestors` of `6000000177921459056` ("Richard Wade Borsheim", 13 Aug 14:05),
#: from different seeds and different styles. 4096 → 4100 is the sixth reading in
#: the step-by-four run and the first across a style boundary, which strengthens
#: "tracking Geni's own growth" over "a per-export ceiling". Still recorded, not
#: asserted.
#: **2026-08-13 — 4104.** A large same-day batch (Descendants and BloodTree
#: seeds across the Borsheim/Norwegian mother's side, feeding the Charlemagne
#: route) topped out at 4104: seven exports read exactly 4104 across both
#: styles. Seventh reading in the step-by-four run. Still recorded, not asserted.
#: **2026-08-13, 16:45 and 16:53 — 4112, and the run skipped a value.** Two
#: `Forest` exports, of `6000000227225628908` ("Unknown Sorbian Prince") and
#: `6000000227225654852` ("Wife of Froyla Ferrández, Conde"), eight minutes
#: apart, both exactly 4112. 4104 → 4112 is a step of *eight*, the first reading
#: in the run that is not four higher than the last — either 4108 was never read
#: because no export was taken while it stood, or the step is not four. The two
#: readings agreeing with each other is the same style-and-seed independence
#: seen throughout. Recorded, not asserted, and the reason this stays "largest
#: seen". A third `Forest` take ten minutes later — `6000000227225487992`
#: ("NN"), 16:57 — held **4116**, so the same sitting read 4112, 4112, 4116.
#: **2026-08-13, 17:37 — 4120**, a `Forest` of `6000000227226600829` ("mother of
#: James Baskerville"). Fourth reading of the evening: 4112, 4112, 4116, 4120.
#: Then **4124** (`6000000227226552913`, "mother of Nicolaii Tregarthen", 17:43)
#: and **4128** (`6000000227226579873`, "mother of Robert Kemsley", 17:49). Six
#: readings in one evening, 4112 → 4128, and after the single step of eight the
#: rest went up by four apiece.
#: **2026-08-13, 18:19 to 19:32 — 4156, 4164, 4164, 4208**, four more `Forest`
#: takes the same evening: `6000000227226720863` ("mother of Sir John
#: Robertson") 4156, `6000000227226792872` ("mother of Isaac Dreyfus") 4164,
#: `6000000227226796847` ("mother of Michael Katzenellenbogen") 4164, and
#: `6000000227226850980` ("NN Chirino") **4208**. Ten readings in one evening,
#: 4112 → 4208. The steps here are 28, 8, 0 and 44 — so the run that "went up by
#: four apiece" earlier the same evening did not continue, which is the second
#: time a step description has been overtaken within hours of being written. The
#: pair at 4164 is two different seeds eight minutes apart, the usual
#: style-and-seed independence. Recorded, not asserted.
#: **2026-08-13, later the same evening — 4212**, a `Forest` of
#: `6000000227227104853` ("father of Marianos Argyros"). Eleventh reading of the
#: evening; the run reads 4112, 4112, 4116, 4120, 4124, 4128, 4156, 4164, 4164,
#: 4208, 4212, and **4216** (`6000000227227092862`, "father of Cian mac Mug
#: Nuadat"), twelve readings in one evening. Then **4220** ("mother of Kendel
#: Meyer Moch", `6000000227227238821`) and **4224** ("mother of Falk Jonas
#: Gamburg", `6000000227227141848`) — fourteen readings, 4112 to 4224. Then
#: **4228** ("mother of Dawid Halberstadt", `6000000227227142945`) and **4236**
#: ("mother of Samuel Abraham Sussman Ballin", `6000000227227132960`), and
#: **4240** ("mother of Rabbi Israel Henshel Isserles", `6000000227227041063`).
#: **Later the same evening the run continued to 4276**, over `Forest` and
#: `Descendants` seeds alike: 4244 ("mother of Rabbi Israel Henshel Isserles" and
#: "father of איציק עסלינגן"), 4264 ("mother of Elia Sussman Ballin"), 4268
#: ("mother of Fraidchen Scheuer von Deutz"), 4272 ("father of Uri" and "wife of
#: Simon Gunzburg") and **4276** ("mother of Bonna bat Kalonymos II",
#: `6000000227227190927`). Twenty-one readings in one sitting, 4112 → 4276, the
#: two styles interleaved throughout — the same style independence the earlier
#: flat runs showed.
#:
#: **2026-08-14 — 4868**, a `Forest` export seeded on **Alexandra Krasuk**
#: (`6000000227240691895`), a profile Emma created that day, taken at 16:08.
#: `exports/samaritans/export-Forest-6000000227240691895.ged`. That is a jump of
#: **592** over the previous reading, the largest single step recorded here, and
#: it is consistent with the stated mechanism rather than surprising under it:
#: the ceiling is four times the profiles she has added, and she had been adding
#: Samaritan profiles all day.
#: **2026-08-15 — 4940**, a `Forest` export seeded on **Abram ben Yitzhaq**
#: (`6000000178795709821`), taken at 02:30 and imported as export 204:
#: `exports/samaritans/export-Forest-6000000178795709821.ged`. A step of **72**
#: over the previous reading, and the seed is himself one of the 21 Samaritan
#: high priests Emma had been building that night. Emma re-exported because one
#: individual — `Yitzhaq I ben Tsedaka`, `6000000227245553985` — had been left
#: out of the earlier take; the ball came back 4940 rather than 4868 with him in
#: it. Consistent with the ceiling tracking the profiles she has added, and not
#: evidence of a rule about the number.
#: **2026-08-15, evening — 5000**, and it is a round number for the first time.
#: Eight `Forest` exports in Emma's edge batch came back at exactly 5000:
#: `6000000227254368832`, `…254335853`, `…254292863`, `…254162896`, `…254345871`,
#: `…254292875`, `…254550821`, `…254397877`, plus a `BloodTree` of
#: `6000000178918422849`. Nine readings on one flat number, from nine different
#: seeds and two styles, which is the same global-not-per-seed behaviour every
#: earlier flat run showed. **Do not read 5000 as a cap Geni enforces** — the
#: previous flat runs sat on 3860, 4020 and 4944, none of them round, and the
#: roundness here is not evidence of anything. The same batch also holds 4976,
#: 4952, 4948 and 4944, so the ceiling is not uniform across it.
#: **2026-08-15, later — 4944**, a `BloodTree` export seeded on **Jair IV**
#: (`6000000178918541826`), a Samaritan High Priest:
#: `exports/samaritans/export-BloodTree-6000000178918541826.ged`. A step of
#: **4** over the reading above. Four exports arrived in that sitting — a
#: `Forest` of Sanballat's daughter and a `BloodTree` of
#: `6000000178794141887` at **4940** each, an `Ancestors` of `NN /Cohen/` at
#: **348**, and this one — so three styles and four seeds sat on 4940/4944
#: within minutes, the same style-and-seed independence every earlier flat run
#: showed. The `Ancestors` take holding 348 exhausted its component rather than
#: reaching the ceiling, which is the ordinary reason a reading comes in low.
#: **2026-08-17 — 5000 again, four times, from a new kind of seed.** Emma's first
#: midpoint batch: `Forest` exports of `6000000227288930948` (`Wilchen /Tybekken/`),
#: `…289663852` (`Øystein /father of Berta/`), `…289604840` (`Michel /Jude/`) and
#: `…289792822` (`Björn /father of Prinsessan/`), all four at **exactly 5000**,
#: taken between 09:04 and 09:35 and filed in `exports/midpoints/`.
#:
#: What makes this reading worth adding rather than redundant: the seeds were chosen
#: by a *different method* from every earlier flat run — placeholders created at the
#: **midpoint of a relationship-path gap** rather than at a component edge or on a
#: Samaritan line — and the number did not move. Thirteen readings now sit on 5000
#: across two styles and thirteen seeds picked three different ways. That is more
#: evidence the ceiling is global rather than a property of how a seed is found, and
#: still not evidence of a rule about the number itself.
GENI_EXPORT_CAP = 5000

#: The step between reading this report and running an export.
#:
#: Load-bearing, and learned the hard way. The people listed below are
#: *doorways* — they are in our data and their parents are not. Exporting from a
#: doorway centres Geni's walk on somebody we already hold, so a large part of
#: the ball comes back as material we have. Centring it one step further out, on
#: the parent we do not hold, is what the one export with measured results
#: actually did, and it returned 95% new people.
#:
#: A constant for the same reason as
#: :data:`genimerge.crosscheck.SUSPECT_IS_NOT_WRONG`: a test asserts it
#: reaches the report, and a copy of the sentence in the test would break on any
#: rewording.
EXPORT_FROM_THE_PARENT = (
    "**Export from the parent, not from the person listed.** Every profile "
    "below is a *doorway*: we hold them, and we do not hold their parents. "
    "Open the profile on Geni, go **up** to the parent Geni knows and we do "
    "not, and export from there. Exporting from the doorway itself centres the "
    "walk on somebody already in our data, so much of the ball returns as "
    "material we hold; centring one step beyond the frontier is what made the "
    "2026-08-01 export 95% new. The listed person is the signpost, not the "
    "destination."
)

#: What the one measured export says about this ranking, which is not much and
#: not flattering. Kept in the report so the numbers above are not read as more
#: validated than they are.
RANKING_IS_UNVALIDATED = (
    "**No export has yet been taken from a seed this ranking chose, so none of "
    "it is validated.** The one export with measured results — 2026-08-01, 3656 "
    "new people — was seeded on the parent of Hågen Iversen "
    "`6000000019312592888`, who placed **2255 of 2336** here, on a ball of 5 "
    "with a single doorway. That is a reason for doubt rather than a verdict: "
    "the ranking never scored the actual seed, because he was not in our data "
    "to score, and no rival seed was tried against him. One data point is not "
    "enough to re-rank on, and it is not being re-ranked on; it is enough to "
    "say the list below is a hypothesis."
)

#: The part of the doubt that *is* measurable without another export, and the
#: part that is not.
#:
#: An earlier version of :data:`RANKING_IS_UNVALIDATED` asserted the mechanism
#: below as fact, on reasoning alone. It is now measured, and the numbers are
#: rendered beside it — three of its four claims held, and the fourth turned out
#: to be about Geni rather than about this data, which nothing here can check.
SIZE_BIAS_IS_MEASURED = (
    "The ranking sorts on **absolute** doorway count, and doorways are counted "
    "inside the ball, so a larger ball has more chances to hold one. That "
    "predicts a sort order tracking neighbourhood size rather than openness. "
    "Measured rather than assumed, on the candidates below:"
)

#: What the measurement does and does not settle.
SIZE_BIAS_LIMIT = (
    "**What this does not show is that the ranking is wrong.** It establishes "
    "how the sort behaves — it prefers large, proportionally less open "
    "neighbourhoods — and nothing more. Whether an open neighbourhood actually "
    "yields a richer export is a claim about Geni's data, not about ours, and "
    "no measurement here can reach it: we cannot see what sits behind a doorway "
    "without exporting through it. The one export taken so far is consistent "
    "with openness mattering and is a single observation. Taking the next "
    "export from a top-ranked pick, where this file has already committed its "
    "prediction, is what would settle it."
)

#: Ball size at or below which a candidate sits in a neighbourhood we barely
#: know. Reporting only — see :data:`THE_ONE_RESULT` for why this band is worth
#: counting and why nothing sorts on it.
SMALL_BALL = 5

#: What the single export with measured results says about every ordering we
#: could have used. Recorded rather than recomputed: the numbers are about the
#: pre-merge tree, reconstructed from the three original exports on 2026-08-02,
#: and that tree no longer exists in the workspace.
#:
#: This is the least flattering thing in the report and the most useful, so it
#: is stated before the table rather than after it.
THE_ONE_RESULT = (
    "**The one seed known to have worked ranks near the bottom of the ordering "
    "below.** The 2026-08-01 export was taken through Hågen Iversen "
    "`6000000019312592888` — ball of 5, one doorway, openness 20% — and "
    "returned 3656 new people. Against the 2336 candidates in the pre-merge "
    "tree he placed:\n"
    "\n"
    "| ordering | his rank |\n"
    "| --- | ---: |\n"
    "| doorway count — what this report sorts on | 2261 of 2336 |\n"
    "| openness | 1303 of 2336 |\n"
    "| ball size | 2293 of 2336 |\n"
    "| *smallest* ball first | 38 of 2336 |\n"
    "\n"
    "Openness is the obvious repair for the size bias described above, and it "
    "does not rescue him: 20% openness is exactly the pool median. The only "
    "ordering that surfaces him is the inverse of ball size, which has a "
    "plausible mechanism behind it — a tiny neighbourhood is one we know almost "
    "nothing about, so almost everything behind its doorway is new — and which "
    "is **not** adopted here. One observation cannot establish a ranking rule. "
    "The 3836 cap had three and was still wrong."
)

#: Heading note for the small-ball table. It exists so the experiment proposed
#: above can actually be run, and it is deliberately not a recommendation — the
#: sequence at the top of the report is still what the model says to do.
SMALL_BALL_IS_THE_OTHER_ARM = (
    "**This is the experiment's other arm, not a recommendation.** The sequence "
    "at the top of this report is still what the model proposes. These are here "
    "because the ordering that surfaces them is the only one that would have "
    "found the seed which worked, and a count on its own — *66 candidates* — is "
    "not something anyone can export from. Nothing about a short list of names "
    "makes the hypothesis behind it any better supported than it was: one "
    "observation. Take one export from the sequence above and one from here, "
    "and the comparison is worth more than either list."
)

#: Why the smallest-ball idea is worth stating rather than dismissing.
SMALL_BALL_IS_TESTABLE = (
    "That idea is cheap to test and the objection to it turned out to be "
    "wrong. A ranking on smallest ball sounds degenerate — as though it would "
    "return isolated fragments and broken records — but a doorway is in our "
    "tree, so it always has some recorded relative:"
)

#: Ball size above which a candidate counts as sitting in a large neighbourhood.
#: Arbitrary, and only used for reporting — it is a place to cut the pool so the
#: bias in the sort order can be quoted, not a threshold anything decides on.
LARGE_BALL = 100

#: Export shapes Geni offers, as edge sets over our data.
STYLES = ("blood", "all", "ancestors", "descendants")

#: Hops used when screening candidates. Deep enough to see whether a
#: neighbourhood is recorded "several layers" out, cheap enough to run over
#: every candidate.
SCREEN_RADIUS = 3

#: A ball with a smaller share of doorways than this is saturated — the region
#: is already recorded, and an export seeded in it would mostly return people
#: we hold. Deliberately low: the point is to reject the clearly-pointless, not
#: to fine-tune a ranking that is a proxy in the first place.
SATURATED_BELOW = 0.05


@dataclass(frozen=True)
class Ball:
    """The people a breadth-first export from ``seed`` would reach."""

    seed: str
    #: reached in breadth-first order, seed first
    reached: list[str]
    #: hop distance from the seed, per person
    hop: dict[str, int]
    #: True if the export cap stopped the walk before the ball was exhausted
    capped: bool
    #: the largest hop actually walked
    depth: int

    @property
    def size(self) -> int:
        return len(self.reached)


@dataclass(frozen=True)
class SeedProfile:
    """A candidate export seed, and what its ball is made of."""

    seed: str
    ball: Ball
    #: people in the ball with no parents recorded — the doorways
    doorways: frozenset[str]

    @property
    def size(self) -> int:
        return self.ball.size

    @property
    def open_count(self) -> int:
        return len(self.doorways)

    @property
    def openness(self) -> float:
        return self.open_count / self.size if self.size else 0.0

    @property
    def saturated(self) -> bool:
        """Everything around this seed is already recorded several layers out."""
        return self.openness < SATURATED_BELOW


@dataclass
class Pick:
    """One export in a planned sequence, and what it adds over its predecessors."""

    profile: SeedProfile
    #: doorways this pick covers that no earlier pick covered
    fresh: frozenset[str] = field(default_factory=frozenset)

    @property
    def fresh_count(self) -> int:
        return len(self.fresh)


def edges_for_style(tree: Tree, style: str, *, graph: dict[str, list[str]] | None = None):
    """The adjacency a given export style walks.

    ``blood`` and ``all`` are the undirected family graph — the distinction
    Geni draws between them is about *whose* profiles are included, not about
    which links are followed, and our data cannot tell the two apart.
    ``ancestors`` walks parent links only, ``descendants`` child links only.
    """
    if style not in STYLES:
        raise ValueError(f"unknown export style {style!r}; expected one of {STYLES}")
    if style in ("blood", "all"):
        return family_graph(tree) if graph is None else graph
    if style == "ancestors":
        return _parent_map(tree)
    return _child_map(tree)


def export_ball(
    edges: dict[str, list[str]],
    seed: str,
    *,
    cap: int | None = GENI_EXPORT_CAP,
    radius: int | None = None,
) -> Ball:
    """Breadth-first walk from ``seed``, stopped by ``cap`` or ``radius``.

    The cap is Geni's, and whether it bit matters: a ball that fills before it
    reaches a boundary is an export that never gets to the interesting part.
    """
    reached = [seed]
    hop = {seed: 0}
    queue = deque([seed])
    capped = False

    while queue:
        current = queue.popleft()
        next_hop = hop[current] + 1
        if radius is not None and next_hop > radius:
            continue
        for neighbour in edges.get(current, ()):
            if neighbour in hop:
                continue
            if cap is not None and len(reached) >= cap:
                capped = True
                queue.clear()
                break
            hop[neighbour] = next_hop
            reached.append(neighbour)
            queue.append(neighbour)

    return Ball(
        seed=seed,
        reached=reached,
        hop=hop,
        capped=capped,
        depth=max(hop.values()) if hop else 0,
    )


def profile_seed(
    tree: Tree,
    seed: str,
    edges: dict[str, list[str]],
    *,
    cap: int | None = GENI_EXPORT_CAP,
    radius: int | None = None,
) -> SeedProfile:
    """Walk one seed's ball and count the doorways in it."""
    ball = export_ball(edges, seed, cap=cap, radius=radius)
    doorways = frozenset(
        person_id
        for person_id in ball.reached
        if person_id in tree.people and not tree.people[person_id].has_known_parents
    )
    return SeedProfile(seed=seed, ball=ball, doorways=doorways)


def rank_seeds(
    tree: Tree,
    *,
    style: str = "blood",
    radius: int = SCREEN_RADIUS,
    limit: int | None = None,
    edges: dict[str, list[str]] | None = None,
) -> tuple[list[SeedProfile], list[SeedProfile]]:
    """Score every parentless person as an export seed.

    Returns ``(kept, rejected)`` — rejected being the saturated ones, returned
    rather than dropped so the report can say how many candidates were
    discarded and why.

    Candidates are the parentless people only. A seed that is certainly not
    terminal sits inside what we already hold, and walking outward from it
    spends most of the cap before reaching an edge.
    """
    edges = edges_for_style(tree, style) if edges is None else edges

    kept: list[SeedProfile] = []
    rejected: list[SeedProfile] = []
    for geni_id, person in tree.people.items():
        if person.has_known_parents:
            continue
        profile = profile_seed(tree, geni_id, edges, cap=None, radius=radius)
        (rejected if profile.saturated else kept).append(profile)

    kept.sort(key=lambda p: (-p.open_count, -p.openness, p.seed))
    rejected.sort(key=lambda p: (-p.size, p.seed))
    return (kept if limit is None else kept[:limit]), rejected


def choose_export_set(profiles: list[SeedProfile], k: int) -> list[Pick]:
    """Pick ``k`` seeds whose balls overlap as little as possible.

    Greedy on newly-covered doorways. Ranking alone would return one
    neighbourhood over and over, because neighbours share a ball; what matters
    for a *sequence* of exports is what each one adds to the ones before it.

    Stops early when no remaining candidate adds a doorway — returning fewer
    picks than asked for is the correct answer when the candidates are
    exhausted, and padding the list with redundant seeds would not be.
    """
    covered: set[str] = set()
    picks: list[Pick] = []
    remaining = list(profiles)

    while remaining and len(picks) < k:
        best = max(
            remaining,
            key=lambda p: (len(p.doorways - covered), p.open_count, -_ordinal(p.seed)),
        )
        fresh = best.doorways - covered
        if not fresh:
            break
        picks.append(Pick(profile=best, fresh=frozenset(fresh)))
        covered |= fresh
        remaining.remove(best)

    return picks


def _ordinal(geni_id: str) -> int:
    """Tie-break key that is stable across runs and independent of dict order."""
    return int(geni_id) if geni_id.isdigit() else 0


def _pearson(xs: list[float], ys: list[float]) -> float:
    """Correlation coefficient, stdlib only. 0.0 when either side is constant."""
    if len(xs) < 2:
        return 0.0
    mx, my = fmean(xs), fmean(ys)
    cov = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    vx = sum((a - mx) ** 2 for a in xs)
    vy = sum((b - my) ** 2 for b in ys)
    if vx == 0 or vy == 0:
        return 0.0
    return cov / (vx * vy) ** 0.5


@dataclass(frozen=True)
class SizeBias:
    """How far the sort order prefers candidates in large neighbourhoods.

    The ranking sorts on *absolute* doorway count, and doorways are counted
    inside the ball, so a bigger ball has more chances to hold one. Whether that
    makes the ranking a proxy for ball size is a question about this data rather
    than a matter of opinion, so it is measured and reported instead of argued.
    """

    candidates: int
    large: int
    picked: int
    picked_large: int
    correlation: float
    median_ball_pool: float
    median_ball_picked: float
    median_openness_pool: float
    median_openness_picked: float
    #: 1-based rank of the most open candidate in the pool
    most_open_rank: int
    most_open_openness: float

    @property
    def large_share(self) -> float:
        return self.large / self.candidates if self.candidates else 0.0

    @property
    def picked_large_share(self) -> float:
        return self.picked_large / self.picked if self.picked else 0.0


def size_bias(kept: list[SeedProfile], picks: list[Pick]) -> SizeBias:
    """Measure how much the sort order tracks ball size rather than openness."""
    chosen = [p.profile for p in picks]
    most_open = max(range(len(kept)), key=lambda i: kept[i].openness) if kept else -1
    return SizeBias(
        candidates=len(kept),
        large=sum(1 for p in kept if p.size > LARGE_BALL),
        picked=len(chosen),
        picked_large=sum(1 for p in chosen if p.size > LARGE_BALL),
        correlation=_pearson([p.size for p in kept], [p.open_count for p in kept]),
        median_ball_pool=median([p.size for p in kept]) if kept else 0.0,
        median_ball_picked=median([p.size for p in chosen]) if chosen else 0.0,
        median_openness_pool=median([p.openness for p in kept]) if kept else 0.0,
        median_openness_picked=median([p.openness for p in chosen]) if chosen else 0.0,
        most_open_rank=most_open + 1,
        most_open_openness=kept[most_open].openness if kept else 0.0,
    )


def render_markdown(
    tree: Tree,
    *,
    style: str = "blood",
    radius: int = SCREEN_RADIUS,
    exports: int = 10,
    top: int = 40,
    small_top: int = 10,
) -> str:
    """The report: what to export next, in what order, and what it cannot tell you."""
    kept, rejected = rank_seeds(tree, style=style, radius=radius)
    picks = choose_export_set(kept, exports)
    edges = edges_for_style(tree, style)
    parentless = sum(1 for p in tree.people.values() if not p.has_known_parents)

    lines = [
        "# Export seeds",
        "",
        "Generated by `genimerge.seeds` — re-run `python -m genimerge seeds`.",
        "",
        "A Geni export is a **breadth-first ball**: one profile, one style, and "
        f"Geni walks outward until the export is full, modelled here at "
        f"{GENI_EXPORT_CAP} individuals. "
        "So the useful question is not who has the biggest subtree in our data — "
        "that is what we already hold — but whose ball would contain the most of "
        "what we do not.",
        "",
        "**Doorways** are people in a ball with no parents recorded. Each is a "
        "place Geni can walk further than we can. **Openness** is their share of "
        "the ball.",
        "",
        f"Screened over a {radius}-hop ball in the `{style}` style.",
        "",
        "## Candidates",
        "",
    ]
    lines += _table(
        ["", "count"],
        [
            ["people in the tree", str(len(tree.people))],
            ["with no parents recorded — the candidates", str(parentless)],
            ["kept", str(len(kept))],
            [f"rejected as saturated (openness < {SATURATED_BELOW:.0%})", str(len(rejected))],
        ],
    )

    lines += [
        "",
        "Saturation rejects the seeds sitting inside a region already recorded "
        "several layers out, where an export would mostly return people we hold. "
        "It fires rarely, and that is worth saying rather than tuning: ranking by "
        "doorway count already keeps interior candidates away from the top, so "
        "the rejection is a floor under the list, not the thing that shapes it.",
        "",
        f"## The next {len(picks)} exports",
        "",
        "Chosen greedily on **newly covered** doorways, not by rank. Neighbours "
        "share a ball, so a ranked list hands back one neighbourhood repeatedly; "
        "what matters across a sequence of exports is what each one adds to the "
        "ones before it. `adds` counts doorways no earlier pick had.",
        "",
        EXPORT_FROM_THE_PARENT,
        "",
    ]
    running = 0
    rows = []
    for i, pick in enumerate(picks, 1):
        person = tree.people[pick.profile.seed]
        running += pick.fresh_count
        rows.append(
            [
                str(i),
                f"[{person.display_name}]({person.url})",
                f"`{pick.profile.seed}`",
                str(pick.profile.size),
                str(pick.profile.open_count),
                f"{pick.profile.openness:.0%}",
                str(pick.fresh_count),
                str(running),
            ]
        )
    lines += _table(
        ["#", "profile", "geni id", "ball", "doorways", "openness", "adds", "running"],
        rows,
    )

    if picks:
        naive: set[str] = set()
        for profile in kept[: len(picks)]:
            naive |= profile.doorways
        lines += [
            "",
            f"Those {len(picks)} picks reach **{running}** distinct doorways. The "
            f"{len(picks)} highest-ranked seeds, taken without regard to overlap, "
            f"reach **{len(naive)}** between them.",
        ]

        full = export_ball(edges, picks[0].profile.seed, cap=GENI_EXPORT_CAP)
        lines += [
            "",
            "## What the size limit does",
            "",
            f"Walking the top seed as far as Geni would take it reaches "
            f"**{full.size}** people already in our data"
            + (
                f", filling the export at hop {full.depth}."
                if full.capped
                else f", exhausting its component at hop {full.depth} without filling the export."
            ),
            "",
            "That number is not a prediction of waste. Geni's graph holds our "
            "people *and* the ones we are missing, and its walk reaches both at "
            "each hop — so a full export is a mix, and the doorway density near "
            "the seed is the best available proxy for how rich that mix is.",
            "",
            f"The {GENI_EXPORT_CAP} used above is **the largest export we have "
            "seen, not a limit we know Geni enforces**. Three exports held "
            "exactly 3836, which read as a hard cap until later ones held "
            "3840, 3844, 3848, 3852, 3856 and then 3860 — the last of those "
            "for eleven consecutive exports taken within one hour from eleven "
            "different seeds in three different styles. A second flat run "
            "followed on 05 Aug: twenty-six exports all holding 4004. Those "
            "runs are worth more than the rises, because they show the bound "
            "is global rather than per-seed or per-style and rule out a walk "
            "that simply overshoots a floor to finish the generation it is on. "
            "The ceiling has since gone *down* — 4008 for four exports, then "
            "4004 for twenty-six — so it is not a limit that only rises, and "
            "the spacing is recorded rather than encoded. Geni's own export "
            "page displays the number (a `Size` field reading 4004 on 05 Aug), "
            "which is the first evidence about it that is not inferred from "
            "output. Being off by a few people out of ~4000 does not move this "
            "ranking.",
        ]

    lines += ["", "## How well this ranking has actually done", "", RANKING_IS_UNVALIDATED]

    bias = size_bias(kept, picks)
    lines += ["", SIZE_BIAS_IS_MEASURED, ""]
    lines += _table(
        ["", "the pool", "the picks"],
        [
            ["candidates", str(bias.candidates), str(bias.picked)],
            [
                f"ball over {LARGE_BALL}",
                f"{bias.large} ({bias.large_share:.1%})",
                f"{bias.picked_large} ({bias.picked_large_share:.0%})",
            ],
            ["median ball", f"{bias.median_ball_pool:.0f}", f"{bias.median_ball_picked:.0f}"],
            [
                "median openness",
                f"{bias.median_openness_pool:.0%}",
                f"{bias.median_openness_picked:.0%}",
            ],
        ],
    )
    lines += [
        "",
        f"Ball size and doorway count correlate at **r = {bias.correlation:.2f}** "
        f"(r² = {bias.correlation ** 2:.2f}), so neighbourhood size accounts for "
        f"most of the ordering but not all of it — at any given ball size the "
        f"doorway counts still spread. The sort is not simply ball size under "
        f"another name.",
        "",
        f"The selection effect is sharper than the correlation. Candidates with a "
        f"ball over {LARGE_BALL} are **{bias.large_share:.1%}** of the pool and "
        f"**{bias.picked_large_share:.0%}** of the picks, and the picks are "
        f"*less* open than a typical candidate "
        f"({bias.median_openness_picked:.0%} against "
        f"{bias.median_openness_pool:.0%}). The most open candidate in the whole "
        f"pool — {bias.most_open_openness:.0%} — ranks "
        f"**{bias.most_open_rank} of {bias.candidates}**.",
        "",
        SIZE_BIAS_LIMIT,
    ]

    small = [p for p in kept if p.size <= SMALL_BALL]
    tiny = [p for p in kept if p.size <= 2]
    lines += ["", THE_ONE_RESULT, "", SMALL_BALL_IS_TESTABLE, ""]
    lines += [
        f"- candidates with a ball of {SMALL_BALL} or fewer: "
        f"**{len(small)}** of {len(kept)} ({len(small) / len(kept):.0%} — a "
        f"shortlist, not a crowd)" if kept else "- no candidates",
        f"- of those, with a ball of 2 or fewer: **{len(tiny)}**",
        "",
        "So the shortlist is workable and holds no isolated records. That makes "
        "it worth *testing*, not worth adopting. The way to settle it is one "
        "export from a top-ranked pick and one from this shortlist, compared on "
        "how many new people each returns — at which point there are two "
        "observations instead of one.",
    ]

    if small:
        shown = sorted(small, key=lambda p: (p.size, -p.open_count, _ordinal(p.seed)))[:small_top]
        lines += [
            "",
            f"### The small-ball shortlist ({len(shown)} of {len(small)})",
            "",
            SMALL_BALL_IS_THE_OTHER_ARM,
            "",
            EXPORT_FROM_THE_PARENT,
            "",
        ]
        lines += _table(
            ["profile", "geni id", "ball", "doorways", "openness"],
            [
                [
                    f"[{tree.people[p.seed].display_name}]({tree.people[p.seed].url})",
                    f"`{p.seed}`",
                    str(p.size),
                    str(p.open_count),
                    f"{p.openness:.0%}",
                ]
                for p in shown
            ],
        )

    lines += [
        "",
        f"## Ranked candidates (top {top})",
        "",
        "By doorways in the screening ball. Useful for picking a seed by hand; "
        "the sequence above is what to actually export, because these overlap.",
        "",
    ]
    lines += _table(
        ["profile", "geni id", "ball", "doorways", "openness"],
        [
            [
                f"[{tree.people[p.seed].display_name}]({tree.people[p.seed].url})",
                f"`{p.seed}`",
                str(p.size),
                str(p.open_count),
                f"{p.openness:.0%}",
            ]
            for p in kept[:top]
        ],
    )

    lines += [
        "",
        "## What this cannot tell you",
        "",
        "Doorways count what an export can reach, never what is behind them. "
        "Nobody knows how many people sit above a parentless person — not knowing "
        "is the whole reason to export from them — so nothing here predicts how "
        "many new individuals an export returns. A seed with 25 doorways is a "
        "better bet than one with 3; it is not a promise of eight times the "
        "material.",
        "",
        "Openness is also measured over *our* graph. A region Geni records "
        "thinly looks identical to one it records richly, until the export lands.",
    ]

    return "\n".join(lines) + "\n"


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    sep = ["---", *["---:"] * (len(header) - 1)]
    return [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
        *["| " + " | ".join(row) + " |" for row in rows],
    ]
