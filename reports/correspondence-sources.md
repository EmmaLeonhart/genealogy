# The three Geni↔Wikidata correspondence sources, and how they differ

**Emma, 2026-09-05:** *"I'm not sure what the origin of this file is. And I'm concerned it might
be conflating two different entity resolution files with different functions — one gedcom and one
that operates within manual identifications I made using an html artifact."*

## ⛔ TWO CHANNELS. `bio-qids.tsv` is the READOUT of one of them, not a third

**Corrected 2026-09-05 after re-running the extractor**, which is what settled it. This page said
three sources, then said two by reclassifying one, and both were wrong. The measurement:

| | channel | how a pair gets in | readout |
| --- | --- | --- | --- |
| **1** | **the BIO channel** | she writes the QID into a Geni *About Me*; and `exports/post-merge/wikidata-qid-links.ged` **forces** pairs in as corpus regardless of any export | `reports/bio-qids.tsv` — **184 pairs** |
| **2** | **the MANUAL PARENTAL ZIPPER channel** | she adjudicates a parent in a **Claude artifact**; the deck writes the verdict | `reports/manual-identifications.csv` — **314 pairs** |

    overlap between the two channels: 0

**The GEDCOM is not a third source — it is the FORCING MECHANISM of channel 1.** Emma: *"there's
one special gedcom file that forces bio qids."* Proved by re-running the extractor: **29 of its
29 pairs are now in `bio-qids.tsv`, where 3 were before.** They were missing because the extract
was six days stale, not because they were separate.

**And it has a second job**: on **2027-01-01** everyone in it becomes an entry point and by
extension a ledger item — *"opening up the way for edits in certain eccentric clusters of the
tree."* Registered in `reports/entry-point-groups.tsv` as `special-geni-gedcom-recognition` with
`active_from = 2027-01-01`.

## ⛔ THE NAME OF CHANNEL 2, which is the thing she asked to have fixed

**It is the MANUAL PARENTAL ZIPPER MERGE CORRESPONDENCES.** Emma, 2026-09-05: *"Artifact entity
resolution is not 'manual entity resolution' and calling it as such is extremely misleading and
it's the reason for my fear. It should be called idk 'manual parental zipper merge
correspondences' since the extremely vague title is almost certainly gonna be fucking abused by
later agents for other purposes."*

- it is a **manual form of the zipper merge**, the job `zipper-join.py` does by position;
- **right now, only for parents**;
- she **hopes to phase it out**, so it is not a permanent channel;
- **artifact means a CLAUDE artifact**, never a GitHub Actions artifact, which is inaccessible
  to her and against policy.

The file is still `reports/manual-identifications.csv` and the pipeline reads it under that name.
**Renaming it is part of the queued architectural experiment, not something to do mid-pipeline** —
she said plainly that the pipeline works and must not be broken.

## ⛔ `bio-qids.tsv` GOES STALE SILENTLY

Nothing schedules `extract-bio-qids.py`. On 2026-09-05 the GEDCOM was updated and the extract was
last built 2026-08-30, so a file whose whole purpose is to **force** pairs into the corpus had 26
of its 29 invisible to the reader. Re-running took it 158 → 184. Re-run it before quoting a
bio-QID number.

`docs/correspondence-merge-proposal.md` proposes removing this failure mode by reading the bios
out of the merged tree rather than by scanning 600 exports.

