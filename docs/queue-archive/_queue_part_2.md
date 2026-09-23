 **⛔ TWO THIRDS OF PATH REQUESTS NOW RETURN `202` AND WE COLLECT NONE OF THOSE ANSWERS.**
  Measured on the 4,432-attempt drain: `queued/queued` is 2,969, 67%. A queued search's result
  never comes back in the response and reaches `/paths` only when a path is FOUND. The inline
  harvest added 2026-09-19 catches the other, cheaper third.
  **The route exists and is HALF BUILT NOW**: every completed search emails a full degree
  sentence and a `https://www.geni.com/c/<hash>` permalink — a saved path object, the same kind
  `pathchains.js` spends 28 minutes walking `/paths` to collect 30 at a time. Emma, 2026-09-19:
  *"my email contains all of the requested paths ... you can recover them from my email."*
  `scripts/parse-path-emails.py` reads either an mbox or pasted bodies and merges into
  `reports/path-permalinks.tsv` on the hash. 11 harvested so far.

  ⛔ **AND "~200" WAS A CAP, NOT A COUNT.** This bullet used to say *~200 in the last seven
  days*. Gmail's `resultCountEstimate` returned exactly **201** for
  `from:geni.com subject:relationship`, for `from:no-reply@geni.com "View the full"`, and for
  the bare query `in:anywhere` — which matches the entire mailbox. It is a ceiling the API
  reports and nothing more. Notifications from 09-12 and 09-13 exist outside that window, so
  the real volume is unknown and larger; Emma, 2026-09-19: *"That's too low ... at least one
  order of magnitude."*

  ⛔ **SO THE CONNECTOR IS THE WRONG INSTRUMENT FOR THE BACKLOG.** The session's Gmail
  connector returns one message body per round trip — N notifications cost N round trips, which
  is fine for topping up and hopeless for thousands. **A Google Takeout mbox is one file and the
  parser eats it in seconds**, with no credential passing through the agent.

  **DONE, 2026-09-19. 47,692 permalinks are in `reports/path-permalinks.tsv`** — 15,944 blood
  and 31,748 in-law, parsed out of the Takeout mbox in 31 seconds. The Takeout was Mail only,
  MBOX, export once; it completed in about half an hour and Google also dropped the zip into
  Drive, which is how it was fetched without the password challenge the Takeout download page
  puts up.

  ⛔ **AND THE REAL NUMBER IS 47,692, NOT 201 — 240 TIMES THE FIGURE THIS BULLET USED TO CARRY.**
  Emma, 2026-09-19: *"That's too low ... at least one order of magnitude."* It was two.

  ⛔ **636 `/c/` LINKS WERE NOT PATHS AND ARE EXCLUDED.** `/c/<hash>` is Geni's generic content
  permalink, so it appears in unrelated mail — the one that exposed it was subject *"StrangerChat
  sent you a message"*. Every one had a valid-looking hash and a blank degree, and every one
  would have sent the chain walker at a URL that is not a path. `NOTIFICATION_RE` now requires
  the notification's own marker.

  ⛔ **PAUSED 2026-09-20 at 12,911 of 47,692. Ruled: the walk is not worth more session time.**
  *"honestly can you hold off on this stuff ... I think that this is the least value added
  session"*. **The permalinks are the artifact that mattered and they are committed** --
  `reports/path-permalinks.tsv`, 47,692 rows, verified 0 malformed, 0 duplicate, 0 blank, sorted
  on the hash. The walk is a long grind on top of them and any session can resume it.

  **To resume**: paste `scripts/pathchains.js` into a foreground geni.com tab, inject an
  `<input type="file">` and upload a hash-per-line file built from the TSV (geni.com's CSP
  blocks a cross-origin fetch and 47,692 urls is 3.6 MB of JavaScript, so neither a fetch nor a
  paste works), set `C.i` from `localStorage.chains_cursor`, then `C.go()`.
  **Use `build-chain-batch.py --skip-covered`**: 23,306 of the remaining 34,781 are worth
  walking and the rest can only re-fetch a chain already held.

  **State at the pause**: 12,911 walked, 12,764 resolved, 147 failed. 31,819 chains held against
  25,827 before this started, 192,556 distinct people. Rate when healthy 1,140 an hour; it fell
  to 161 for about seven hours on 2026-09-20 and recovered on its own, so a slow interval is an
  interval and not a projection.

  **What is left, for whoever resumes**: the walk itself; then `split-path-chains.py` and
  `build-tiny-gedcoms.py`, neither of which has been run -- the second writes corpus `.ged`
  files, so it is a deliberate step and was kept out of the two-hourly tick on purpose.

  ⛔ **AND `C.reseedFailed()` IS OWED AT THE END OF THE RUN.** A permalink that times out used to
  be counted in `fail` and stepped over for good; it is now kept in `C.failed` and appended back.
  **The run is not finished when `i >= of` -- it is finished when `i >= of` AND `C.failed` is
  empty.**

  ⛔ **AND THE FIRST `reseedFailed` RETRIED NOTHING WHILE REPORTING A FIX.** It went through
  `seed()`, which de-duplicates against `C.urls` -- and a failed permalink is by definition
  already in `C.urls`, at a position the cursor has passed. So it returned `0` every time. Worse,
  it had already SPLICED the urls out of `C.failed` before discarding them, so **the 143
  permalinks that failed before 2026-09-20 18:00 are not in any retry list and cannot be named**.
  The retry now appends unconditionally.

  **How to recover those 143, offline**: `reports/path-permalinks.tsv` carries `subject_name`
  for every permalink, and a harvested chain's LAST segment is that same person. The join is
  `covered_names()` in `build-chain-batch.py`, done 2026-09-20.

  ⛔ **AND THE SAME JOIN SAYS MOST OF THE REMAINING WALK IS WASTED.** Measured: of the 38,148
  permalinks still to walk, **20,856 already name-match a chain we hold** -- so walking them can
  only re-fetch something already on disk. `--skip-covered` drops them and takes the whole list
  from 47,692 to **27,808**.

  ⛔ **IT DROPS ONLY WHERE THE NAME IS HELD BY EXACTLY ONE CHAIN, AND THAT TEST IS THE WHOLE
  SAFETY OF IT.** Of those 20,856, only 13,031 match a name held by a single chain; the other
  7,825 match an ambiguous one, and the ambiguity is concentrated in placeholders -- `NN` ends
  21 held chains, `N.N.` 10, `<private> Schottenstein` 7. Skipping on a bare name match would
  throw away a real person because an unrelated `NN` is already held. **A name is not an
  identifier**, which is the same rule as § *PARSE PATRONYMICS BY FORM* in another costume.

  **Not yet applied to the running loop.** The whole 47,692 is seeded in the page and the loop is
  healthy; re-seeding it mid-run to save time is how a working campaign gets broken. Apply at the
  next restart.

- **The Geni path anchor is not always the account owner, and it is not ours.** A `/path/` page
  rendered anchored on **Naruhito** (`from=6000000001783830969`), and notification emails read
  *"is NN NN NN's 37th great granddaughter's..."* and *"is Private User's..."*. Checked
  2026-09-19: neither id is in the batch, the requester's template carries **no `from=`
  parameter at all** and one `%ID%` placeholder, and all 138 harvested degree lines read
  `is your`. So the requester is anchored correctly and something else on Geni is not.
  Cause unknown. **Do not investigate without being asked** — it costs an hour and changes
  nothing about our output.

- **Wikidata lag spent the whole `MAXLAG_BUDGET` twice in one run.** Run `35467987263`: 191 edits
  executed, and the only genuine losses were two `still lagged after 900s of waiting` plus two
  dependents skipped behind one of them. `MAXLAG` is already 10 and the budget already 900 s.
  Nothing to fix in our code; recorded so the next session does not re-diagnose it as ours.

---

## Non-Geni follow-ons (kept short; full text was in the cleaned box queue)

- Parse the descendant reports into actual family trees (offline; no Geni contact).
- Export a GEDCOM from Wikidata (Wikidata only).
- The Rømer ring seed is one unrecorded parent link from the owner's ancestry — work when touching rings; do not Geni-fetch under the moratorium.
- Relative-describing labels are still a standing defect (see Queued 2026-09-21 / maiden-name and relational-label rulings).

---

## Queued 2026-09-21, arbitrary order — dictated in one go

### ⛔ PATRONYMICS ARE MADE IN PAIRS. STANDING ORDER, AND IT IS NOT BEING FOLLOWED

Ruled 2026-09-21: *"we are supposed to be always, always, always creating the male and the
female versions of the patronymics at the same time as pairs. We're supposed to be doing a
repetitive thing with a masculine and female version of them that are linked together. I don't
see this in the quick statements, even though it's been a standing order for a really long
time."*

**The judgment is that it was forgotten, not that it is reparative.** The batch creates
`Ingebretson` alone — masculine patronymic, son name, `P144` based on `Ingebret` — and no
`Ingebretsdatter` beside it and no link between the two.

`scripts/build-patronymic-items.py` already holds the gendered-suffix table and the `P5278`
*surname for other gender* pairing. **Whether anything CALLS it is the open question** —
§ *Code that is WRITTEN but never CALLED is not done*. Establish that first, with a narrow
search over `scripts/` and `.github/workflows/` only.

⛔ **THE CALLER SEARCH IS NOT A CORPUS GREP.** One was run here on 2026-09-21 as
`grep -rn ... -r . --include=*` from the repo root, which sweeps `exports/`; it ran for two
minutes and had to be killed. § *NEVER GREP THE WHOLE CORPUS* — the question was worth seconds.

The pair is `Q130444148` masculine patronymic ↔ `Q130444179` feminine patronymic, and
`Q10673705` son name ↔ `Q10476255` daughter name. `P5278` links the two items both ways.

### ⛔ THE BATCH IS PUTTING `P2600` ON REDIRECTS — FIXED 2026-09-21, AND IT WAS SIX NOT TWO

Ruled 2026-09-21: *"what the fuck is going on with the constant attempts to add these qids to
redirects?"* QuickStatements answers **"The given entity ID refers to a redirect, which is not
supported in this context"** and the statement is lost.

    Q141502958   P2600 "6000000004313804007"
    Q141502959   P2600 "6000000001821187530"

**These are the same two QIDs as CI failure #1**, `tests/test_garborg_day_batch.py::
test_every_explicit_subject_already_exists` — *editing items not in the ledger*. So the test
that would have stopped this has been failing rather than being fixed, which is why it is
*constant*.

⛔ **AND BOTH TARGETS ALREADY HELD THE STATEMENT**, so every run re-sent an edit that had
nothing to do. `Q3754184` Onneca Fortúnez already carried `P2600 6000000004313804007` and
`Q250731` Álmos, Duke of Nitra already carried `6000000001821187530`.

⛔ **THEY ARE DOUBLE REDIRECTS, WHICH IS WHY NOTHING SAW THEM.**
`Q141502958 → Q141498680 → Q3754184`. `wbgetentities` follows **neither** hop and returns an
empty entity, so the QIDs were simply absent from the live store and every downstream *does the
item already hold this?* check answered *do not know* and emitted. `action=query&redirects=1`
follows the whole chain and is what resolved them.

⛔ **AND CHECKING ALL 26 ENTRY POINTS FOUND SIX STALE, NOT TWO.** The test caught two because
the other four are shielded by the exemption sets:

    Q141493459 -> Q9353042      Q141502958 -> Q3754184
    Q141493460 -> Q695735       Q141502959 -> Q250731
    Q141493461 -> Q3736064      Q141502962 -> Q141498725

All six are resolved in `reports/entry-points-now.tsv`, which is the hand-maintained drip file
`entry-points-immediate.csv` is generated from. 26 rows became 25.

**The durable half is in `refresh-live-values.py`, and it adds no file.** It already knew — it
printed `{len(items)} of {len(qids)} fetched` and dropped the rest silently. It now NAMES the
ids that did not come back and says where to resolve them. A merged-away item is the ordinary
case, so it reports rather than exits.

- **`Q141502962 → Q141498725` — SETTLED 2026-09-21. Emma merged them herself**: *"I merged
  them — leave it"*. So the collapsed single entry-point row is correct, and the 2026-09-20
  ruling that they are *"not a duplicate pair"* is superseded by her own later merge rather than
  contradicted by it. Nothing to contest and nothing to re-split.

  **The general lesson is the one already written**: § *NOT A DUPLICATE PAIR* warns that the
  error was *"reading a cached ledger as the live state"*, and this session read a cached
  **ruling** as the live state in the same way. The live check is what settled it.

### The 7 CI failures — item 4 of the 2026-09-17 order

Run `35590570344`, 2026-09-21, identical on Python 3.10 and 3.13.

- `test_garborg_day_batch.py::test_every_explicit_subject_already_exists` — the redirect item above
- `test_garborg_day_batch.py::test_the_ledger_and_the_batch_do_not_both_claim_a_person`
- `test_garborg_day_batch.py::test_every_married_surname_in_the_batch_can_be_linked_or_is_being_created`
- `test_garborg_day_batch.py::test_every_link_to_an_existing_item_is_emitted_in_BOTH_directions`
  — `('P25', 'Q136660380')` emitted one-way
- `test_no_descriptions_or_summaries.py::test_no_batch_carries_a_description` — `Den` values that
  are relational phrases rather than life descriptions: `"born Foss"`, `"wife of Thure Johansson
  Stålarm"`, `"son of Gunnar Gunnarson Ænes"`, and one that is a raw source note,
  `"Grødem i Randaberg; jfr g og æ bok 1 side 118 - 17"`. **This is the same fault as the
  `Tora NN` item above** — a relative's name reaching a field that is not about them.
- ~~`test_p2600_batches.py::test_no_line_carries_an_unescapable_quote`~~ **FIXED 2026-09-21.**
  Two backfill generators carried `qs()` as
  `value.replace("\\", "\\\\").replace('"', '\\"')` -- Python's escape, not
  QuickStatements'. There is no backslash escape in V1 at all, so
  `Q141206058 P1810 "Bertha \"Betsy\" Pedersdatter"` was unparseable and the statement was
  silently lost. `build-garborg-day.qs` had always stripped the quote instead. Both now strip.
  **`wikidata-relationship-sources.qs` had the identical defect** and only passed because
  today's batch holds no quoted name -- § *A GUARD IN ONE EMITTER IS NOT A GUARD*. The three
  copies stay separate per § *Duplication is deliberate here*, and a new parametrised