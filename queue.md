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

## 4 · The 33 Samaritan high priests — one door, and it may be shut

The remaining component is **33 people**, the Samaritan high-priestly line
(Abisha, Phinehas, Elazar, Tsedaka, Aabed-El ben Asher…).

**It is a single descent with exactly one attachment point.** Of the 33, only
**Tabia ha'Åbtå'i** `6000000220294810877` has no parent recorded, and all 32
others sit beneath him — 11 generations. So this is not 33 candidate doorways;
it is one.

**Emma's reading, 2026-08-13:** they are legitimately not connected, because of
the change in the priestly house, and no export will find an edge Geni does not
record. That is very likely right and it is also **one export away from being
measured**: a `Forest` seeded on Tabia ha'Åbtå'i either returns a parent or does
not, and a `Forest` ball that returns nothing has found nothing to follow — the
same asymmetry that settled the Hata question in `reports/hata.md`.

She also raised **agentic RAG** over outside sources for a link. Worth doing only
after the export, because the export says whether there is anything on the Geni
side to attach a found link to.

**Not-done tag:** NEEDS-DECISION — Emma, whether to spend one export on it or
close the component as genuinely separate.

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
