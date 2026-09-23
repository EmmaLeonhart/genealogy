# Geni-blocked campaign laundry list — archived 2026-09-22

Moved out of `queue.md` because the front of the queue asked to fix the file becoming
garbage, and Emma clarified that this Geni export / Monte Carlo / Ingemund / Inal Kut Chor
/ Ursula / STEP Forest / Bagrationi laundry list is **not meant to be worked** under the
Geni moratorium (and was never the live plan). Nothing deleted — parked here the same way
`docs/queue-archive/` already holds reference that used to bloat the queue.

**Do not start these.** The Geni moratorium forbids contact until at least 2026-10-21.

---

<!-- archived-as: geni-exports-and-campaign-order -->

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

**Checked 2026-09-17 and it says exactly that**, so the created-ancestor route is the only one.
The ancestor exists now: **`6000000227804005917` NN von Pardubice**, created as the father of
`6000000176534654825` **Anna von Pardubice** (c.1359, born Pardubice, no parents on Geni) —
tier 4 of `docs/export-seed-rules.md`, no parents at all and a surname, so `NN` plus the child's
birth surname. Anna is five generations above Ursula: Anna → Barbara von Sternberg → Königin
Kunigunde von Kunstadt-Podiebrad → Viktorin Bocek von Münsterberg → Ursula. `Descendants` 5000
submitted off him as task `6000000227804000942`.


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

**Checked 2026-09-17: it says exactly that**, and redirects to `/error`. So this one needs the
same created-ancestor route Ursula needed — create a relative of `292373984150002914` this
account owns, then run `Forest` off the created person, because the walk has to cross the step
link rather than descend. Still to do; the commanded roster is ahead of it.


## THE ORDER, 2026-09-17. WORK IT TOP TO BOTTOM

Dictated in one go after a session that jumped between things. **None of these depend on an
earlier one finishing** -- the order is hers -- except that the archive is best delved into
before the connection investigations, because it may hold the answer.

The Geni exports below run alongside all of this and are **the least significant part**:
*"these actual Geni exports are kind of the least significant part of what we're doing here. It
just happens that I got a lot of them all at once."*

- **4. All the random CI/CD crap.** CI has been failing since before 2026-09-17, and the
  three-ledger refactor has never run green: every pipeline run since it landed was cancelled by
  the next push.

- **5. Investigate the Pomeranian-Cypriot connections.**

- **6. The ontology.** `P407` *language of work or name* is the piece left undone: which languages
  a name belongs to is not a fact about the string and needs a source.

- **7. An aggressive campaign to do the downloading properly.**

- **8. Then a Cypriot / Russian / Bagrationi investigation.**

- **9. Then whatever else.**

### Why the cluster campaign exists

*"we are trying to dig in on a specific cluster to make sure we have completely exhausted it."*
The bet: the Dutch-Pomeranian cluster has a relatively high likelihood of a descent from
antiquity -- the kings of Cyprus, or Russian nobility -- either of which reaches the **Georgian
royal family, which is the goal**. It is strange in that it moves very far geographically and
then fizzles out unexpectedly; the theory is that many people have investigated it a little and
nobody pushed far, because it tends to be the less noble ancestry on a lot of paths.

⛔ **THE POINT IS TO *ADD* BLOOD, NOT TO FIND IT IN THE GRAPH.** Ruled 2026-09-17 against exactly
that mistake: measuring existing connectivity treats the tree as fixed, and in a 1.4M-person tree
almost any two noble lines are reachable at some hop count, so a reachability number says nearly
nothing. The exports are what create the edges.

## ⛔ A FULL RING OF ANCESTRY ON TWO PEOPLE, EVERY RUN. Ruled 2026-09-18

*"for these two people I want you to go crazy with their ancestors. Every run should add a full
ring to their ancestry."*

    6000000000757999620  Q141493478  Inger Axelsdatter Güntersberg
    6000000002621242041  Q141450322  Olfvir / Ølver Rømer

`PRIORITY_ANCESTOR_SEEDS` and `priority_ancestor_ring` in `scripts/build-garborg-day.py`. The
walk goes up THROUGH people who already hold a QID and returns everybody standing on the first
boundary above -- the whole ring, unioned in after `compose` picks, uncapped, because a full ring
is not a shape `compose` can express and a slice of it advances the ancestry a fraction of a
generation a day.

**It advances itself and there is nothing to maintain**: what it returns gets created, enters the
ledger, and is walked THROUGH next run instead of returned again. No depth counter, no cursor, no
state, and no way for it to quietly stop.

⛔ **THE LEDGER'S GENI ID FOR `Q141450322` IS THE HUSK.** `garborg-qids.tsv` pairs it with
`6000000227289508960`, which redirects to `6000000002621242041` and has no `FAMC` of its own --
so seeding on the ledger alone would have grown nothing while printing a cheerful zero. Both ids
seed the walk. Correcting the ledger row is still owed.

**First measurement, 2026-09-18: 8 people on the frontier**, 7 walked through.

## ⛔ TOP PRIORITY EXPORTS, from 00:30 on 2026-09-18 — run top to bottom, one at a time

Ahead of the commanded roster below. Geni allows one export at a time, so this is a strict
sequence, not a set.

- **Bothilde Sigurdsdatter Onarheim** — `Forest`. *"for merge related stuff changing"*, so it is
  a **privileged** export and is filed into `exports/post-merge/`.

  ⛔ **`6000000227805045863` IS A HUSK AND THE EXPORT DOES NOT RUN ON IT.** It redirects to
  `6000000177261659865`, the real Bothilde (c.1275), which this account does not manage —
  `https://www.geni.com/gedcom/export/6000000177261659865` answers *"You are not allowed to
  export that profile"* and lands on `/error`. The husk's own export form still loads, titles
  itself **"(No Name)'s GEDCOM File is Being Created"** and accepts the submit; that is the trap
  § *`6000000227289508960` IS A MERGED-AWAY HUSK* describes, and one such submit was spent here
  on 2026-09-19 before the redirect was checked.

  **The seed is `6000000227811549827` Sigurd Onarheim**, her father, created by this account and
  directly attested by her patronymic — tier 1 of `docs/export-seed-rules.md`. `NN Onarheim`
  `6000000227816629854` is the mother placeholder and is the fallback. `Forest` 5000 submitted
  off Sigurd on 2026-09-19; the page confirmed **"Sigurd Onarheim's GEDCOM File is Being
  Created"**, a named profile rather than `(No Name)`. Delete this when the zip is filed.

⛔ **AND `6000000002621242041` OLFVIR IS NOT EXPORTED DIRECTLY. RULED 2026-09-18.** Forest,
Ancestors and Descendants were all queued on that id and **none of them can run**: the profile
is not this account's, and the `request_export` endpoint does not get round that — the form
page's refusal was the real answer after all. The two `NN` seeds above are the route to the same
ancestry, which is the shape the whole campaign already uses: **you do not export the person you
want, you export a placeholder this account owns next to them.**

### ⛔ `6000000227289508960` IS A MERGED-AWAY HUSK. DO NOT SEED OFF IT

The link originally given for Olfvir was `6000000227289508960`, and it **redirects** to
`6000000002621242041`. That merge is what connected the new ancestors — it is the event the
00:30 wait was for, not a problem to route around.

The husk is still half-alive and that is the trap: its export form loads, titled
**"GEDCOM Export for (No Name)"**, and it **accepts a submit**. The task it returns —
`6000000227805163844`, `Ancestors` — then errors on every single reload. So a submit that looks
like it worked produces nothing, and nothing says so.

**The submit is a plain GET**, which the button merely builds, and navigating to it directly
beats hunting the button —

    https://www.geni.com/gedcom/request_export?id=<geni id>&walk=Forest&max_profiles=5000
      &destination=Ftb80&name_format=0&locale=en-US&include_bom=1

`walk` is `Forest` / `Ancestors` / `Descendants` / `BloodTree`. It is a convenience, **not a way
past a permission**: on a profile this account does not manage the endpoint refuses exactly as
the form page does. That was argued the other way here on 2026-09-18, under § *NEVER SAY YOU
CANNOT DO SOMETHING YOU HAVE NOT TRIED*, and it was wrong — the form page's refusal WAS the
mechanism, and the rule does not make an access control disappear.

⛔ **AND DO NOT INVENT A DESCENDANT TO WALK UP FROM.** `docs/export-seed-rules.md` only ever
creates **parents**, because a parent is implied to have existed and a child is not. Creating a
child of a real historical person to seed an `Ancestors` walk asserts something false about the
tree, and it was offered here and refused.

**A clicked submit is confirmed by `location.href` carrying `request_export` or
`/gedcom/download?task_id=`, never by the page text** — `get_page_text` returns stale content on
this site throughout. And coordinate clicks were landing off-target all night because
`getBoundingClientRect` reports in a 1536-wide viewport while the click frame is 1568 wide; that
is what looked like "the first click is always swallowed".

## COMMANDED EXPORTS, 2026-09-17 — one cluster, exhausted
## COMMANDED EXPORTS, 2026-09-17 — ABANDONED

⛔ **STOPPED BY INSTRUCTION, 2026-09-17:** *"after downloading the finished gedcom abandon doing
the exports since your job is different stuff"*, and earlier: *"these actual Geni exports are kind
of the least significant part of what we're doing here."*

**15 Forest exports were taken**, the last being NN von Flemming at 22:54. 215 zips sit in
`~/Downloads`, unfiled — filing them into `exports/` is hers.

The roster below is left listed rather than deleted, so the cluster is recoverable if it is ever
picked up again. Nothing here is running and nothing should be dispatched from it.

---

*(continued in `geni-blocked-campaigns-2026-09-cont.md`)*
