# How to make an export individual

**Emma's rules, dictated 2026-08-17.** An *export individual* is a placeholder
profile created on Geni at an open slot in the tree, purely so a `Forest` export
can be run from it. This file is the whole method: where to put one, what to call
it, and what to do when a tree has no open slots left.

Her framing for why it is written down at all: *"This all occurs sequentially and
this is why it takes a bit of difficulty to do because it's sequential. It's a bit
time-consuming but I'm realizing I can just save all my time by having you do
it."*

The export itself is always **`Forest`, size 5000** — see § *Running the export*
at the bottom.

---

## The preference order

Five tiers, most preferred first. Take the highest tier the page offers.

### 1. Fatherless, has a surname, has a patronymic → create the father

The best case, and the reason patronymics rank above everything else: the
patronymic *names the father*, so the person being created is directly attested
rather than invented. Emma: *"patronymics allow us to create an individual that is
directly historically attested and doesn't involve the NN on them."*

- **Given name** — read it off the patronymic. `Anders Olsen` → the father is
  `Ole`.
- **Surname** — the child's surname, and **the patronymic must not survive into
  it**.

**The patronymic sits in either field and which one decides nothing.** Emma:
*"Sometimes the patronymic is part of the first name and sometimes it's in the
last name, so you want to make sure that just the surname comes in and the
patronymic is not present — the patronymic is removed if it was in the surname
thing."* So when the patronymic was occupying the surname field, the created
father gets **no** surname from it; strip it. This is the same both-fields rule
`CLAUDE.md` § *`name modelling.txt`* states for reading names generally.

### 2. Fatherless, has a patronymic, nothing else → create the father

Same father, but there is no surname to give him.

- **Given name** — from the patronymic, as above.
- **Surname** — `father of <the child's given name>`.

This is the form the existing seeds are in: `Anders father of Anna`,
`Karl father of Carl`, `Lewis father of Hugh`, `Øystein father of Berta`,
`Lars father of Sigrid`.

### 3. Has one parent, is missing the other → create the missing parent as `NN`

Almost always this is *father present, mother absent*, which is what Geni's tree
view offers as an **Add mother** box.

- **Given name** — `NN`.
- **Surname** — none. We do not know it, and Geni's *Suggest surnames* will offer
  the child's, which would be invented.

**Father-absent works identically.** Emma: *"For mother is present, father is
absent — we really will do the same thing. It's not a super preferable thing that
it has to be that the placeholder individual we're creating is for the mother. It
can be for the father. That's just really rare."*

**Why this is worth doing even with no name to give.** Emma: *"We don't really
know what their name is, but what we do know is that by creating this person we're
actually reducing ambiguity in the tree, because now there's an individual
representing their mother — which can be helpful for situations where somebody may
have had multiple marriages."* The value is the slot, not the label. This is the
same reasoning as `CLAUDE.md` § *Redacted people go in*: the structure is the
informative part.

### 4. No parents at all, has a surname → create the father as `NN`

- **Given name** — `NN`. No patronymic means no evidence of what he was called.
- **Surname** — the child's **birth** surname.

### 5. No parents at all, no surname → create the father as `NN father of …`

- **Given name** — `NN`.
- **Surname** — `father of <the child's given name>`.

---

## `-ez` IS a patronymic, and it is read as one

**Emma, 2026-08-18:** *"-ez is a real patronymic in some cases lol and we do treat it as
one in historical contexts."*

So `Juana Jiménez de Castro` is **tier 1**, not tier 4: the patronymic names her father
`Jimeno`, and the surname he takes is `de Castro` — the toponymic — because tier 1 is
explicit that *the patronymic must not survive into the surname*.

    Juana Jiménez de Castro   ->   Jimeno /de Castro/

**This was got wrong once**, on 2026-08-18, on that exact person. The reasoning was that
`-ez` had fossilised into an inherited surname by the 1400s and that reading it live would
invent a man. That is a real linguistic fact and it is **not** how this project reads
them; her ruling is that the historical context is where the patronymic is live. The
profile created under the wrong reading is `NN Jiménez de Castro`
(`6000000227314434935`) — it carries both faults, the `NN` and the patronymic left in the
surname. It is left as-is rather than edited: the export it seeded already ran and closed
its target, and re-editing a placeholder costs loop time for no gain.

The same reading applies to the other Iberian patronymic endings — `-az`, `-iz`, `-oz`,
`-es` in Portuguese — and they will recur, since the remaining gap is thousands of people
wide and Iberian lines are well represented in it.

**Contrast with the Nordic farm name, which is the opposite call.** `Ingeborg Olsdotter
Gilja` and `Seri Mikkelsdatter Mjåland` take tier 2, not tier 1, because `Gilja` and
`Mjåland` are farm names both spouses carry rather than a patrilineal surname — there the
suffix is a live patronymic *and* the surname is not the father's. Two different traps
that look alike: read the suffix and the surname separately.

## Bail on anything weird. The loop is self-healing

**Emma, 2026-08-17, and this is the governing rule for the whole loop:** *"if you
run into any kind of weirdness on any specific individual that might make you do
weird stuff — like, say, running a search because you can't figure out how to
click through — bail on that one, and try the next thing."*

*"We do not need to get every single individual here. The operations here are
completely self-healing. If you miss an individual because of weird rendering
errors, then you move on to the next one, and there's a decent chance that you
won't even need to do that individual this next time."*

**A BAIL IS PER-ATTEMPT, NEVER PER-PERSON. There is no hold list.** Emma, 2026-08-18:
*"my guess with the bailed people is you can just go back to them… you can try different
people. You can try adding different individuals at other parts of their tree and then
running it… I feel like you've been too stateful with this."*

Her intent, in her words, is *"filling up the entire family tree around a certain person
with new individuals constantly trying to figure out one that actually works"*. So a
saturated rim is not a dead end — **expand a `+N` button and the frontier appears**, with
open parent slots on it. That is how `Ola R Sande` was retried after being wrongly written
off: one click on `Silla Torkelsdatter Ølberg`'s `+18` re-rooted the view and exposed
`Mareta Torkelsdatter` with both parent slots empty.

**`reports/chain-gaps-on-hold.csv` was a mistake twice over and is not to be relied on.**
It never persisted — `find-chain-gaps.py` rewrites it every run from an empty in-code
`ON_HOLD` dict, so the reasons written into it were destroyed on the next regeneration
(git shows it flipping 1 → 0 → 3 → 0 rows in one afternoon). Worse, the exclusion that
*did* persist was a hardcoded skip-list carried between target picks, which turned every
bail into a permanent one.

**The measurement that settles it: of seven people written off on 2026-08-18, three came
into the corpus on their own** — including *both* the locked master profiles, `Asma
Al-Kinani` and `Fredrik Gustaf Levan`. A later export simply reached them. Excluding them
would have been pure loss.

So: the ranking is the state. A person who is still missing is still a target, however
many times an attempt on them has failed.

**Why it is self-healing:** the ranking is recomputed from the corpus every round,
so a person skipped this round either gets covered by somebody else's export or
simply comes back at the top of the next list. Nothing is lost by skipping and
real time is lost by not skipping.

**Geni's own search is never used for anything, ever.** Emma, 2026-08-18:
*"Geni search should absolutely never be used whatsoever because it is actively
hostilely designed and built towards upselling you on a very expensive subscription.
It does not give any useful information whatsoever… you should absolutely never even
consider it."* That is a blanket ban, not advice about ID recovery — it applies
anywhere in this repo, and it is a stronger claim than "the index lags": the results
are engineered to sell a subscription rather than to answer the query.

**The substitute, where a lookup is genuinely needed, is `site:geni.com` on Google** —
and it does **not** help here, because *"new individuals take a while to be indexed"*
and every profile this loop creates is seconds old. For a freshly created placeholder
there is no search of any kind that works. The page is the only source.

**Never run a search to recover an ID. Bail.** Emma, 2026-08-18: *"bruh why did
you attempt a search?"* and *"you do not search you just bail if you run into
issues."* The ID comes off the page — click the newly created node in the tree and
it opens the profile in a new tab whose URL carries the ID. If it does not come off
the page, that individual is done: drop it and take the next one. Searching Geni for
the name you just typed is the second route to the same person that the paragraph
below forbids, and it is slow *and* unreliable — `NN Holst` was searched 37 times in
one session and 40 minutes later in the next, and never appeared, because Geni's
search index lags profile creation by an unbounded amount.

**So the moment a page fights back — a frozen renderer, a node that will not open,
a dialog that will not close, an ID that will not come off the page — abandon that
individual and take the next one on the list.** Do not invent a second route to
the same person.

## Edge case seen in the wild: `father of NN`

Anna Jonsdotter's tree, 2026-08-17. `NN Persson` is fatherless and carries a
patronymic, which is tier 2 — but tier 2 names the father `father of <the child's
given name>`, and here the child's given name *is* the unknown-marker. The result
would be `Per /father of NN/`, which names nobody.

**What I did:** took the tier 3 slot in the same tree instead (`Ingrid Jönsdotter`,
father present, mother absent) and created a plain `NN`. Nothing degenerate, same
neighbourhood, one export either way.

**Not yet a rule.** The alternatives are to use the child's full display name
(`father of NN Persson`), to fall back a tier whenever the child's given name is a
marker, or to accept `father of NN`. Raise it with Emma when the loop is not
mid-flight.

## The ID can be lost AFTER the profile is created, and that is still a bail

Seen 2026-08-18 on `Margareta Eriksdotter`, four generations up `Gustaf Adolph Mattsson
Martin`'s tree. The father was created — her node went from no badge to `+1`, which is
Geni saying the parent exists — but the `+1` would not expand on two attempts, the
renderer stopped answering screenshots, and the profile's own page was never reached.
No ID, so no export.

**Bail on the individual, not on the placeholder.** The created person stays: it is a
legitimate insertion at a real open slot, it is attached to the tree, and a later round
or a later export may well pick it up. What is abandoned is *this round's* attempt at
that target, and the round takes the next disjoint candidate from the ranking instead of
running four seeds.

**Do not go looking for the ID.** Geni's search is banned outright (§ above), and the
only other route — hunting the person through a saved page or a relationship panel — is
exactly the "second route to the same person" this file forbids. Two tries at the same
route is the limit.

## A master profile is a skip

Sometimes a slot looks addable and is not — Geni's **master profiles** are locked
against edits from an account that does not curate them. Emma, 2026-08-17: *"if it
looks like you should be able to add an individual but you can't… just don't
bother that much and skip through it."*

So: move to the next slot. Do not work out why, do not report it, do not count
them.

## When the whole visible tree is saturated

If every slot on the page is filled, move to an ancestor's own tree rather than
giving up on the page.

**The tree icon carries a count.** Each person's node has a small tree icon
showing how many people are in that person's family tree. Click it to open that
person's tree, and pick where to work from that number.

**Prefer a small count, and prefer an odd one.**

- **Small**, because a small tree means more open slots.
- **Odd**, because an odd number of ancestors almost always means one couple is
  half-filled — a father present with the mother absent — which is a guaranteed
  legitimate insertion point. Emma: *"an odd number of ancestors guarantees a
  legitimate insertion point."*

An even count is not disqualifying; it just does not come with that guarantee.
Emma: *"even number of ancestors — you can have that same kind of insertion point
if there is, say, a single eternal lineage of four people or something like
that."*

**Zero is a special case.** It happens rarely and is in some ways the ideal, but
in the context of choosing which tree to move to, **1 beats 0**.

**Rough ranking, and it is explicitly rough:** `1, 3, 5, 0, 2, 4, 6, 7, 9, 11, …`
Emma: *"you can make your own ordering ranking for this, and don't put too much
stress on it… just don't overthink it."* So this ordering is a tiebreak heuristic,
not a rule to defend. The tier list above is the part that matters.

---

## Running the export

Once the individual exists, export from **their** profile:

1. Their profile → **Actions** → **Export GEDCOM**, which is
   `https://www.geni.com/gedcom/export/<geni id>`.
2. Walk: **`Forest`**. Size: **5000**. Everything else default.
3. Submit, leave the page open — it refreshes itself when the file is built — then
   click **Download My GEDCOM File**.

**One at a time is GENI's limit, not a preference.** Emma, 2026-08-18: *"There's no
way that you can do an export concurrently. That isn't my decision thats geni."* So
there is no throughput dial here and nothing to trade off — a second export cannot be
in flight, short of a second Geni account. When builds are slow the rate is slow, and
the only thing the loop controls is dead time between one zip landing and the next
export being submitted.

**Poll the page, not a clock.** Her instruction the same day: *"please don't use the
ticks as a clock. Please use the web page changing as a clock."* The download page
flips to *Your GEDCOM File is Ready to Download* the moment the build finishes; that
flip is the signal to act. Waiting for an hourly cron tick to notice instead can add
most of an hour per export — measured overnight 2026-08-18, where letting the ticks
drive dropped the rate from 7.1 exports/hour to about 1.

**Strictly one at a time.** Emma, 2026-08-17: the batch of seeds *"needs to be
exported after these people have the GEDCOMs exported and downloaded"*, and
sequence is the point. Queue the next export only once the previous zip is on
disk.

**Do not integrate as you go.** *"I don't actually want you to import or integrate
the GEDCOM zip files because we're not doing it all at once."* The zips
accumulate in `~/Downloads`, and only when every one of them is down does the
whole batch get filed into `exports/` together.

---

## Numbered decisions

Kept numbered so they can be referred to later without re-reading the whole file.

### Decision 1 — tier 4's given name is `NN`

**Emma, 2026-08-17, asked directly.** A tier 4 father is `NN` plus the child's
**birth surname**: child `Kari /Bergstrom/` gives father `NN /Bergstrom/`.

Tier 4 is *defined* by having no patronymic, so nothing attests his given name,
and `NN` is already this project's marker for a name genuinely not known — see
`CLAUDE.md` § *`NN` is PRESERVED in `mul`*. It also keeps tier 4 and tier 5
consistent, since tier 5 gives `NN /father of Kari/`.

The father does **not** inherit the child's given name.

### Decision 2 — the patronymic resolves to the proper nominative

**Emma, 2026-08-17, choosing against the option that matched her own past seeds.**
Strip the patronymic ending and write the **real given name it came from**, not
the bare stem:

| child | father |
| --- | --- |
| `Anders Olsen` | `Ole` |
| `Karen Olsdatter` | `Ole` |
| `Anna Andersdotter` | `Anders` |
| `Carl Karlsson` | `Karl` |
| `Hugh ben Lewis` | `Lewis` |

So `Ols father of Karen` — an existing seed of hers — would be made as `Ole`
today. Her earlier seeds are not the standard; this is.

**Every patronymic system counts, not just the Norse one.** Emma, 2026-08-17:
*"this happens in all patronymics so like ap X, fitz X, ferch X, X-ez, but Norse
is by far most common in this data."*

| system | form | child | father |
| --- | --- | --- | --- |
| Norse | `-sen` `-son` `-sson` `-datter` `-dotter` | `Anders Olsen` | `Ole` |
| Welsh | `ap` `ab` `ferch` `verch` | `Rhys ap Gruffudd` | `Gruffudd` |
| Anglo-Norman | `fitz` | `Robert fitz Walter` | `Walter` |
| Iberian | `-ez` `-es` `-iz` `-oz` | `Álvar Rodríguez` | `Rodrigo` |
| Hebrew / Arabic | `ben` `bat` `bin` `ibn` | `Hugh ben Lewis` | `Lewis` |
| Polish | `-ic` `-yc` `-owic` | `Sulisława Wojsławic` | `Wojsław` |
| East Slavic | `-ovich` `-evich` `-ovna` `-evna` | `Ivan Petrovich` | `Pyotr` |
| South Slavic | `-ović` `-ević` `-ić` | `Marko Petrović` | `Petar` |

The Iberian one is the least obvious and the most likely to be missed:
`Rodríguez` is *son of Rodrigo*, `Fernández` *son of Fernando*, `Sánchez` *son of
Sancho*, `Núñez` *son of Nuño*. That family is all over the Monrory and de las
Varillas material.

**Where the ending admits several nominatives, take the commonest and do not
agonise.** `Ols-` is Ole, Ola or Olav in Norwegian; write `Ole`. This is a
reconstruction and is allowed to be one — the patronymic is the attestation that
the father existed and was called something of that stem, which is what makes
tiers 1 and 2 worth more than an `NN`.
