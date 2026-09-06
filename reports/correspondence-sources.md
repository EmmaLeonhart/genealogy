# The three Geni↔Wikidata correspondence sources, and how they differ

**Emma, 2026-09-05:** *"I'm not sure what the origin of this file is. And I'm concerned it might
be conflating two different entity resolution files with different functions — one gedcom and one
that operates within manual identifications I made using an html artifact."*

Measured rather than reasoned about. They are **three** sources, not two, and they are **almost
entirely disjoint**.

| source | pairs | origin | read by the daily batch? |
| --- | ---: | --- | --- |
| `reports/manual-identifications.csv` | **314** | her hand verdicts — `build-manual-identifications.py` unions `emma-judgments.tsv` and `manual-identifications-extra.csv` | **yes**, it is what the `P2600` block reads |
| `reports/bio-qids.tsv` | **158** | machine-extracted by `extract-bio-qids.py` from the **Geni About Me text inside the exports** | **no** |
| `exports/post-merge/wikidata-qid-links.ged` | **29** | a hand-built GEDCOM carrying only ids and a `NOTE` with a Wikidata URL | no — it is corpus, so it reaches the *tree*, not the `P2600` block |

## The overlaps, which are what settles the question

    GEDCOM pairs also in bio-qids       3
    GEDCOM pairs also in manual         0
    GEDCOM pairs in NEITHER            26
    bio pairs also in manual            0

So each file carries a population the others do not. `manual-identifications.csv` is the
adjudicated one and the only one feeding the `P2600` block; the other **184** (158 + 26) are
wired to different jobs -- see the section below, which is the part that matters.

**The `batch` column in `manual-identifications.csv` is its own provenance**, per row:

    204  emma-pasted-verdicts        <- pasted out of the HTML artifact
     46  parent-adjudication-gui
     24  rejected-parents
     14  zipper-sample
     12  blocked-creations
      8  charlemagne-spine-anchors
      3  zipper-hard
      2  given in conversation
      1  hand

## ⛔ NONE OF THIS IS A GAP. Each is doing a documented job

**Emma's guess, 2026-09-05, and it is correct:** *"My personal guess here is that it's all done
correctly but badly documented."* The table above reads like three sources of which one is wired
and two are neglected. That is the wrong reading, and it is the one this file was written under.

- **The GEDCOM is a HOLDING PLACE and the holding is deliberate.** `CLAUDE.md` § *WHAT
  `wikidata-qid-links.ged` IS FOR: people TOO FAR OUT to edit yet* -- the identification is
  sound and the **edit** is withheld, because for somebody nowhere near what the account has
  been building it *"would be perceived as too out of left field"*. They become ordinary entry
  points on **2027-01-01**. So its 26 unique pairs are unemitted **on purpose**, and wiring them
  into the `P2600` block would spend exactly what the file exists to keep.
- **`bio-qids.tsv` is for ROSTER RESOLUTION, not for emission.** It is read by
  `build-emperor-rosters.py`, `build-succession-roster.py`, `build-merge-worklist.py` and
  `slim-corpus.py`. `CLAUDE.md` § *The Geni BIO carries her own QID claims* gives the measured
  reason: through the bio links the 204 Izumo roster QIDs give **8** Geni ids, where
  `p2600-all.tsv` gives **2**. That is what it is for, and it is wired for it.
- **The ledger is her CONTRIBUTIONS, and holds 0 bio pairs correctly.** 1,518 rows: 975 and 469
  from her Wikidata contributions, 41 from `bureatten.csv`. It records what she has actually
  made on Wikidata, so a correspondence she has not yet acted on does not belong in it.

**So the disjointness measured above is the design, not a symptom.** Three files, three
functions, one of them feeding the batch. What was missing was a page saying so -- which is what
she diagnosed: *"badly documented"*, not wrongly built.

## What is NOT established here

Whether the 184 should reach the batch at all. `bio-qids.tsv` is extracted text rather than an
adjudicated verdict, and of its 158, **81 are already stated on Wikidata, 7 sit on an item
carrying a different Geni id, and 70 are on items with no `P2600`** — measured against
`out/wikidata/p2600-all.tsv`. The GEDCOM's 26 include her own profile `Q232803`, which the
exclusion lists keep out of the batch deliberately.

**Nothing was wired, changed or emitted on the strength of this file.** Her instruction, same
message: *"do not mess with anything until I give clear instructions."*

## A caution about `p2600-all.tsv`, which bit while measuring this

It has **no header** — the first line is data (`Q1000005 \t 6000000173769890893`). Read with a
header-consuming reader it silently yields nothing, and the first run of the comparison above
reported **"0 already stated, 158 genuine additions"**: clean, plausible and entirely an
artifact. `CLAUDE.md` records this trap for this exact file and it caught somebody again.
