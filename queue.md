# geni — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03**, **auto-flush at :15**, **status-report at :42**. On a fresh session they are started as the opening step; on a mid-session large-scale re-fill of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the last two items are pinned at the tail.

---

## Wiped 2026-08-13 — 1,396 lines down to this

Emma: *"OH MY GOD THE QUEUE IS SO BLOATED I AM ALMOST CERTAIN NONE OF IT EVEN IS
RELEVANT ANYMORE AND IT IS JUST DECAYED COMPLETELY INTO BULLSHIT."*

What was removed was **decision history, not steps** — the twelve-decision table,
the case-by-case walk notes, the 2026-08-09/10/11/12 decision rounds, the
re-clone post-mortem, the standing-order records. The decisions that still govern
the project are in `CLAUDE.md`, which is where they belong; the rest is in
`git log` at `4127170^`. Nothing was lost, and nothing below it was a step
anybody was going to execute.

**Two live concerns, Emma's own numbering:**

---

## 1 · Missing ancestors — DONE 2026-08-13

`py scripts/check-missing-ancestors.py` → **absent: 0** over 186 GEDCOMs. All
337 ancestors enumerated on the 18 saved pages for Clara Amilia Hoknes and
Randolph Paulus Borsheim are in the corpus. Write-up:
`reports/missing-ancestors.md`.

It went 63 → 61 → 23 → 1 → 0 across 178, 182, 184, 185 and 186 exports, and four
exports did nearly all of it — every one seeded on somebody who was on the list.
The four before them were seeded on cluster-joining targets and closed 2 between
them. **Seed on the list or the number does not move.**

**Reopen this only when new ancestor pages are saved.** The result covers the 18
pages in `missing ancestors/` and says nothing about any root whose pages have
not been saved. If Emma saves more, drop them in that directory and re-run — the
script needs no other change.

---

## 2 · Wikidata isolates — PARKED ENTIRELY, Emma's decision 2026-08-13

**Do nothing with the Wikidata islands. Treat them as random noise.** Her words:
*"my opinion on it is they are useful data in the event something changes and
this is a more active project, but for now we are parking that line of inquiry
entirely."*

So: **no triage batches, no removal mechanism, no exports seeded on isolates.**
Do not open another 25. Do not build the clear-the-text-file path — it was
flagged as unbuilt and is now not to be built, because it is out of scope rather
than because it is hard.

The data stays where it is, unchanged, in case the decision reverses:
`out/_isolates.json` (183,681 items, `[qid, label, geni_id, dates, sitelinks,
flag]`), `out/wikidata-isolates.html`, `wikidata_isolates_to_clear/New Text
Document.txt` (19 triaged as genuine isolates), and
`paths_for_wikidata_isolates/` (6 triaged as connected — Dan Brown, Emma Watson,
George R. R. Martin, Benedict XV, Luka Modrić, Magnus Carlsen).

Her half-formed pattern is recorded here so it is not re-derived from scratch if
this reopens: modern celebrities are often connected, non-sports more than
sports, and **ancient people definitively are not**. It was never tested.

---

## 3 · The Baruch Jafe cluster — JOINED 2026-08-13

`py scripts/check-components.py`, 192 exports: **2 components**, 381,035 people.
Baruch Jafe, his wife, Samuell Standen and Emma are all in component #1 at
381,002. What is left is component #2 at **33 people — the Samaritan
high-priestly line**, which nothing has touched.

**The bridge was `export-Forest-6000000227227041063`, seeded on "mother of Rabbi
Israel Henshel Isserles".** Worth keeping because the shape of it generalises:

- **Six exports seeded inside the cluster moved nothing.** Component #1 held at
  exactly 350,777 across all of them while the cluster went 4,088 → 27,075. A
  ball seeded inside a component stays inside it.
- **Escaping through in-laws cannot work by construction** — Emma's own
  correction, 2026-08-13. A spouse edge joins two people already in the same
  component, or it would not be in it.
- **What worked was seeding at the top of the deepest line.**
  `scripts/cluster-upward-frontier.py` ranks parentless people in a component by
  how many generations of descent sit beneath them, which separates the head of
  a long line from the interior in-laws and leaves that a flat parentless list
  mixes together. The Isserles seed came out of that ranking.

---

## 4 · The 33 Samaritan high priests — JOINED 2026-08-14

**Steps 1-3 below are done.** Emma built the profiles on Geni herself and took
four exports (`exports/samaritans/`): a `Forest` seeded on **Alexandra Krasuk**
(4,868), an `Ancestors` and a `BloodTree` on **Eliazar Cohen** (348 / 4,868), and
a `Forest` on the current High Priest's daughter (4,820). The corpus is 203
GEDCOMs. The pre-1624 line turned out to be in the corpus all along — 78 people
from `Uzzi ben Bakhi` down through Baba Rabba — and the batch to create them on
Wikidata is `reports/wikidata-samaritan-priests.json`.

**Kept below for the record of how it was reasoned about.**

## 4a · The original entry — the line is documented after all

**Superseded 2026-08-13, twice in one evening.** The first conclusion — that
nothing above the component was named and it could never be joined — was wrong,
and `reports/samaritan-priesthood.md` is the correction.

**Tabia ha'Åbtå'i's father is Yusef**, from the community's own record: *"they
asked the priest Tsedaka b. Tabia b. Yusef to be the first High Priest from the
family of Itamar."* Above him the family forefather is **'Abed Ela ben Shalma**,
born and active in Damascus, titled *President of the House of 'Abtah*. And
**'Abtah means Translator** (Arabic *Haftawi*) — an occupation, from the Itamar
priests' duty of rendering the High Priest's Hebrew into Aramaic. It is not a
place, and reading it as one would be `CLAUDE.md` § *A clan name is not a clan*
in reverse.

**The deliverable is `gedcom/samaritan-sources.ged`** — 176 individuals, 69 named
and 107 explicit placeholders, for Emma to open in a tree editor and enter into
Geni by hand. See `gedcom/README.md`; it is deliberately outside `exports/` so
the corpus tests never see it.

**Steps:**

1. **Emma enters the named people into Geni**, starting with Yusef as Tabia's
   father — that one edge is what joins the component.
2. Re-export and re-run `py scripts/check-components.py`.
3. **The eight people who would reach the world tree** are the four sons of
   Yisrael ben Gamliel Tsedaka (b. 1932) and their four Jewish wives, attested in
   his own words to Sean Ireton and named in no source found. `A.B. — The
   Samaritan News`, founded December 1969, is where a community of 751 records
   births and marriages. NEEDS-INVESTIGATION.

---

## 2026-09-30 — create the two unlinked items on Wikidata (Emma)

**Scheduled, not pending.** Emma, 2026-08-13: *"create wikidata items for
[Baruch Jafe] and [Samuell Standen] on September 30 as independent unlinked items
completely independently of their links elsewhere... these appear to have gotten
into the data somehow but are apparently completely unlinked and I still want
them to get in."* And on what it is for: *"this allows for the wikidata stuff to
finally start doing connections."*

- **Baruch Jafe** `6000000040078764766` —
  <https://www.geni.com/people/Baruch-Jafe/6000000040078764766>
- **Samuell Standen** `6000000107265740881` —
  <https://www.geni.com/people/Samuell-Standen/6000000107265740881>

The edits are already written: `reports/unlinked-items.md` and
`out/wikidata/unlinked-items.json`, built by `scripts/build-unlinked-items.py`,
in the same object shape as the Charlemagne priority chain so one executor serves
both. Four statements on Jafe, six on Standen — label, `P31` human, `P2600`,
`P21`, and the dates Geni records, each referenced to the Geni ID.

**No relationship statements, on purpose.** Both men are the husbands of the two
`wife of ...` profiles whose exports are the corpus's cut-off components, so
every relative they have is inside a ball that shares nobody with the rest.
Nothing to point a `P26` or `P40` at yet.

**On the day:** re-run `py scripts/build-unlinked-items.py` first — if either man
has acquired a `qid` in `reports/derived-labels.csv` by then, the script exits
non-zero rather than creating a duplicate. Then execute the two creations.

**Not-done tag:** BLOCKED-ON-USER-ACTION — this is a Wikidata write, dated
2026-09-30 by Emma's instruction.

---

## 5 · Normalise the placeholder names, then generate relationship labels

**Emma, 2026-08-14.** Two stages, the second explicitly at the END of the queue.

**Stage 1 — normalise every placeholder form to `NN`.** All 55 discovered forms
(`reports/given-name-forms.csv`, 35,414 records) collapse to one `mul` label:

- no surname -> `mul: "NN"`
- surname present -> `NN <surname>`

**Guardrail, measured:** of the 33,564 profiles carrying a placeholder name,
**28,268 have ONLY placeholder names and are safe**, and **5,296 also carry a
real name** — `/Avitus/` on one record and `Avitus, Western Roman Emperor` on
another. Those 5,296 must keep the real name;
`reports/name-alternatives.csv` lists them individually.

**Stage 2 — progressive relationship labels, per language.** Generate labels from
recorded relationships in this precedence:

1. parent  2. father  3. mother  4. spouse  5. child

producing `daughter of Joe`, `wife of Carl`, `mother of Joseph`.

**A relationship label can only exist in a language the RELATIVE already has a
label in** — that is the binding constraint and it is measured before anything is
generated.

**Every item must carry English AND Japanese, plus the `mul` label.** Emma,
2026-08-14: *"English and Japanese have to be present on everything and then
there's the multi-language label."* Measured ceiling for relationship labels
(`reports/relationship-label-languages.md`): en 96.1%, nl 81.1%, de/es/fr ~32%,
`mul` 25.3%. Japanese is **not** in the top 18 by coverage, so `ja` will usually
have to be constructed rather than copied from a relative.

**The surname is usually informative, with two contaminations — measured
2026-08-14.** Of the 29,452 placeholder records on profiles with no real name,
**10,362 carry a surname**, over **4,003 distinct** values, **70% used once**.

- **The bulk is a large Korean population** — 이 319, 김 214, 권 142, 허 106,
  홍 89, 안 71, 윤 68, 박 61, 최 61, 노 61 — plus `HUÁNG 黃` 83. **485 distinct
  surnames contain CJK.** These are real family names and are exactly the P734
  material.
- **Contamination 1: placeholders inside the surname slot.** `NN` 158, `???` 119,
  `N.N.` 70, plus `?`, `??`, `**`, `'`. The surname field is not clean.
- **Contamination 2: a place in the surname slot.** `隴西狄道` (Longxi Didao)
  110 records — the `SURN 秦州成紀` trap from `CLAUDE.md` § *A clan name is not a
  clan*, recurring.

**Do not screen these by length.** 361 distinct surnames are <=2 characters, but
Korean and Chinese surnames are one character — 이 and 김 would both be discarded.
Screen on the placeholder vocabulary and on punctuation, never on length.

**Open, Emma's own uncertainty:** whether to run stage 2 for people who already
have a surname, or only for the bare-`NN` ones. Not decided.

---

## 6 · Everything else outstanding from the 2026-08-14 session

Swept out of the chat log because none of it was ever queued.

**Wikidata batches built today, none executed** (nothing runs before 1 Sept):

- `reports/wikidata-samaritan-priests.json` — 78 `create_individual` for the
  pre-1624 line, chained `P22`, kept separate from the post-1624 items.
- `reports/wikidata-add-geni-id.json` — 32 `add_geni_id` from the QIDs Emma put
  in Geni `about_me`, including 2 additional-`P2600` unmergeable duplicates.
- `reports/wikidata-orderlife.json` — 52,233 entries; needs ONE rerun to pick up
  the label rule.

**Decisions waiting on Emma:**

1. **The 15,094 unreadable-item relationship edges.** 21% of the available work.
   Expand the `wikidata-download` seed set and re-check, or emit unchecked and
   accept duplicate-claim risk. `docs/future-modelling.md`.
2. **The 40 people whose `sex` column points at `Q1`.** An error, fixable; 39 of
   40 have a Wikidata QID so their own item has the answer, but none are in the
   local store. `reports/orderlife-sex-q1.csv`.
3. **The Itamar spine's generation 121.** Still committed and still wrong — it is
   an office count, not a generation depth. A single "distance not recorded" link
   is the honest replacement.

**Unbuilt, and the easiest remaining win:** the **59 order.life properties from
P155 up** — Rodovid, FamilySearch, WikiTree, Roglo, Geneanet, The Peerage,
JewAge, DAR/SAR, Find a Grave, a large Swedish cluster. Same numbers and meanings
as Wikidata, values Wikidata often lacks, on items that already exist. No
creation, no normalisation.

**Blocked on one thing, which unblocks two:** expanding the Wikidata download
would resolve both the 15,094 edges AND the Samaritan high priests who have
Wikipedia articles and Wikidata items but no Geni ID on them (Yoseph II,
`Q2031200` Aharon ben Ab-Chisda, Levi ben Abisha, Aabed-El ben Asher).

**Smaller:**

- Re-run `scripts/build-geni-wikidata-pairs.py` over the enlarged 203-export
  corpus; the 40-profile pass predates the four Samaritan exports.
- `Q98159` in order.life's `persons.tsv` is a malformed row — an embedded quote
  splits it, so its identifiers land in the wrong columns.
- The Samaritan office (`Samaritan High Priest`) is still only a description; no
  `P106`, because choosing the item means asking Wikidata.
- Wadah Cohen's father is a missing son of `Amram ben Yitzhaq`
  (`6000000178795370821`) — Geni records only one child for him.

**Running:** one cron, `a1b6b180` at 19:03 daily — audits unrequested
normalisation and exception handling, writes `reports/unrequested-normalisation.md`,
fixes nothing.

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
- The pre-wipe queue, 1,396 lines: `git show 4127170:queue.md`.
