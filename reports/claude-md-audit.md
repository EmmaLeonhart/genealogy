# `CLAUDE.md` audit — stale, contradictory, and misfiled

**2026-09-09. Step 1 of the three you ordered: audit, report, CUT NOTHING.** Your ordering, from
the annotated screenshot: **1** audit and fuse · **2** hard cut, rules only, evidence to
`devlog.md` · **3** move the specifications out to `docs/`.

**5,548 lines. 162 sections.** Nothing below has been deleted or reworded. Every finding names
lines so it can be checked.

---

## 1. ⛔ A LIVE CONTRADICTION GOVERNING 67% OF THE CAMPAIGN YOU DEFINED TODAY

**§ *The 183,674 isolated Geni-linked Wikidata items are LOW PRIORITY*, line 3426**, ends:

> **Do not spend effort connecting them.** This is recorded because the group is large enough
> (13% of stored humans) to look like a priority and is not.

**Today you said the opposite about the same people:** *"all p2600 people should either be
confirmed impossible to connect, or connected."*

**Measured, so this is not a reading:**

    P2600 holders with NO relationship stated on Wikidata      183,940   (the file says 183,674 --
                                                                         same group, slightly grown)
    ...of those, disconnected from Charlemagne                 178,542

    the 266,201-person campaign splits:
      no Wikidata relationships at all -- the "LOW PRIORITY" group  178,542   67%
      relationships that lead nowhere near Charlemagne               87,659   33%

**This is the one finding that changes what runs tomorrow**, and it is yours to settle. The two
statements are not obviously reconcilable by reading: the old one says these people are not worth
connecting, the new one says every one of them must end up connected or confirmed impossible.

The old section's own evidence may be what dissolves it — its argument is *"only 722 of them are
in our Geni corpus at all… they are outside it entirely"*, which is an argument about **our
exports**, and the collector asks **Geni's World Tree**, which does not have that limit. But that
is a reading, not a ruling.

---

## 2. ~500 lines of `queue.md` are living in `CLAUDE.md`

**Lines 5050–5548, 9% of the file.** Moved in on 2026-09-01 (*"remove all the 14 bullshit queue
items"*) and never re-homed. They still speak in queue coordinates, which mean nothing here:

| line | section | the problem |
| ---: | --- | --- |
| 5380 | *Always last — pinned to the very end of the file* | "last" of a file that is not the queue |
| 5438 | *How to read this file* | **describes `queue.md`** — "an item is deleted when it is done", "everything titled LAST is now physically at the end" |
| 5460 | *0. Aug 28, 2026 manual adds* | a numbered queue item, in a file whose own § at 2631 bans numbering |
| 5464 | *THE RULINGS OF 2026-09-01 — these OVERRIDE the sections below* | "below" = the rest of the queue, which is not below |
| 5538 | *`exports/post-merge/` — MOVED TO THE TAIL* | there is no tail here |
| 5532 | *Pointers* | a second pointers block; `queue.md` has its own |

A reader who takes § *How to read this file* at face value will believe `CLAUDE.md` is
delete-on-done. It is the opposite.

---

## 3. Two `Historical:` sections, each superseded by its own live neighbour

| historical | live replacement | lines |
| --- | --- | ---: |
| 3215 *Historical: NO NEW TESTS until CI/CD runs on a public repo* | 3163 *TESTS RUN IN CI/CD OR NOT AT ALL* + 3191 *The moratorium ENDED* | 36 |
| 3355 *Historical: this repo was private, and CI was manual-only* | 3251 *The repo is PUBLIC as of 2026-09-01* | 31 |

Both are correctly labelled and sit **after** their replacements, so the risk is low — but 3355
still says *"Never add a `push:` or `pull_request:` trigger"*, which 3251 reverses for
`pipeline.yml`, and a grep lands in either.

---

## 4. Ten referenced files do not exist

Each checked against `git log --diff-filter=D`; the commit that removed it is named.

| line(s) | path | removed by |
| ---: | --- | --- |
| 1570, 1672 | `scripts/build-label-corrections.py` | `6e86ef64` |
| 3712 | `scripts/build-missing-reciprocals.py` | `6e86ef64` |
| 3821 | `scripts/build-scraped-gedcom.py` | `f5b4ac97` |
| 500 | `scripts/fetch-kana-readings.py` | `3f271dc9` |
| 3716 | `reports/the-spine.md` | `ecd627db` |
| 3317, 5128 | `reports/wikidata-garborg-day.qs` | `d3fa86fa` — *"the batches are .txt, not .qs"* |
| 4969 | `reports/wikidata-garborg.qs` | `8e129808` |
| 2464 | `geni-extension/background.js` | `f9f7eb24` — renamed `service-worker.js` |
| 5021 | `reports/wikidata-edits-applied.tsv` | never existed (the receipt file, unwritten) |
| 312 | `out/merged-134.ged` | never in git (the pre-batch tree, local only) |

§ *LEGACY CODE IS DELETED* (3761) is the rule this breaks: *"stale prose about what a file is for
is read as current, and then acted on."* Two of these are cited as **where a rule lives**.

---

## 5. § *"Is X present?"* is a 284-line dumping ground under an unrelated title

**Lines 1938–2222, the longest section in the file, no subheadings.** Its title governs the first
~70 lines. The remaining ~215 hold at least eleven unrelated rules:

`reconcile` is deleted · Stdlib only · **the repo Layout** · `out/` is not gitignored ·
`exports/excluded/` · never overwrite a `.ged` · the byte-identical exception ·
never gitignore a `.ged` or `.zip` · `genimerge.sources` · one store only · two exports sharing
a seed · **the two hand-label files** · a derived edit for a hand-set slot is dropped

The Layout of the repository is findable only by reading a section called *"Is X present?"*.

---

## 6. A superseded sentence is still the first one a reader meets

**Line 2305**, in § *`P3373` sibling is capped at 40 PAIRS*: the text notes it *"said 'nothing
else is capped' until 2026-09-09"*. **Line 2313**, the next section, opens *"This supersedes the
sentence in § `P3373` sibling…"*. Correct, and it means the wrong claim is read first and the
correction second. Same shape at 3278 (`pipeline.yml` push trigger) and 2075 (`out/` gitignored).

---

## 7. Topic clusters that want fusing

Not stale — just told many times, in many places, each with its own worked example.

| theme | sections | lines |
| --- | ---: | ---: |
| **do not invent a limit / do not stop** | 1704, 1735, 1813, 1833, 1854, 2440, 2468, 2506, 2564, 3386 | ~330 |
| **names, labels, titles, patronymics** | 386–1546, ~30 sections | **~1,160** |
| **AskUserQuestion and when to ask** | 1681, 2806, 2819, 2841, 2858, 2878 | ~90 |
| **entry points, blocs, subgraph roots** | 3909, 3942, 4036, 4060, 4122, 4163, 4197, 4258 | ~350 |
| **the review decks** | 4365, 4474, 4532 | ~215 |

The name block is 21% of the file on its own.

---

## 8. A scope tension, flagged rather than called a contradiction

§ *The practical goal is ONE DENSE NEIGHBOURHOOD, not a comprehensive import* (3639) and
§ *The programme is HYPERLOCAL: one hop out from Arne Garborg, per day* (4311) both describe a
deliberately small programme. The campaign defined today is **266,201 people**. These may simply
be different layers — the daily Wikidata batch is still hyperlocal while the collector campaign
is not — but nothing in the file says which governs when they point different ways, and I read
them as a limit on scope earlier today.

---

## What this measures against the three steps

Step 2 (hard cut) and step 3 (move specs to `docs/`) are not started, per your ordering. For
sizing only:

    queue material misfiled here                   ~500 lines   9%
    the three algorithm specs (5096, 5150, 5314)   ~230 lines   4%
    Historical: sections                            ~67 lines   1%
