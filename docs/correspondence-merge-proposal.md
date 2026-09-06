# Proposal: fold the correspondences into the synoptic tree as a gitignored GEDCOM

**Emma's design, 2026-09-05, and this document is the proposal she asked for rather than a
decision:**

> *"I think the manual zipper parents are wired in correctly and well, and I do not want to break
> the pipeline, but I actually think a good long term architectural smoothing would make it so
> that in the pipeline they are generated into a gitignored gedcom that is part of the synoptic
> tree merge, with qids in bios being a fundamental part of the pipeline. But for now pipeline
> works well and that will be a thing to experiment with at the end of the queue."*

**Nothing here is implemented.** The queue item is at the tail. The pipeline is untouched.

## What exists today

| | file | rows | how it reaches anything |
| --- | --- | ---: | --- |
| 1 | `reports/manual-identifications.csv` | 314 | read directly by `build-garborg-day.py` as a CSV |
| 2 | `exports/post-merge/wikidata-qid-links.ged` | 29 | **corpus** — merged into the synoptic tree like any export |
| — | `reports/bio-qids.tsv` | 158 | an extract of what the corpus already carries, read by the roster scripts |

**Two shapes for one relationship.** File 2 says *this Geni profile is that Wikidata item* by
being part of the tree; file 1 says the same thing by being a table the batch builder opens. The
proposal is to make them the same shape.

## The proposal

Generate file 1 into a **gitignored GEDCOM** during the pipeline run, in the shape of file 2 —
ids plus a `NOTE` carrying the Wikidata URL — and let the synoptic tree merge consume it.

    reports/manual-identifications.csv          (stays: the deck writes here, she reads it)
              |
              v  generated in the pipeline, gitignored
    out/manual-parental-correspondences.ged     ids + NOTE https://www.wikidata.org/wiki/Q…
              |
              v
    the synoptic tree merge  ->  QIDs live in bios, uniformly, whatever their origin

### Why it is an improvement and not just a move

- **One consumer instead of two.** Anything wanting the correspondence reads the tree. Today a
  reader has to know that some pairs are in a CSV, some in a GEDCOM and some only in bios —
  which is exactly the confusion that produced three contradictory accounts of this in one
  evening.
- **It matches what the tree is for.** `CLAUDE.md` § *The Wikidata link goes in the bio during
  the SYNOPTIC TREE BUILD* already says the correspondence belongs in the tree: *"we put the
  Wikidata links into bios during the build process of the Synoptic tree… Forcing them into this
  Synoptic tree like this makes it so that the Synoptic tree, when it starts being used as an
  input, does use them properly, in the zipper merge thing."* This proposal is that instruction
  applied to the artifact-adjudicated pairs as well.
- **The zipper gets them for free.** They are *manual zipper merge* results; feeding them back
  into the tree the zipper reads closes the loop, and a manual verdict becomes an anchor for the
  automatic pass rather than a separate table it cannot see.
- **Gitignored is right.** It is derived from a tracked CSV every run, so tracking it would be a
  second copy that can disagree — the failure this evening kept turning up.

### What it must NOT break

- **The pipeline works now and she said so.** The GEDCOM is generated *in addition* first, with
  `build-garborg-day.py` still reading the CSV, until the tree route is shown to carry the same
  314 pairs. Only then does the direct read go.
- **`exports/` is the corpus and every `.ged` in it is committed.** This file is generated and
  gitignored, so it goes to `out/`, never `exports/` — putting it there would break
  `tests/test_repo_invariants.py`, which compares `git ls-files` against `find`.
- **The merge is 11.16 GB on the runner** (§ *the tree BUILDS in Actions*). 314 records is
  nothing, but the rebuild is not free and this must not add one.

### What has to be decided before it is built

- **Does the generated GEDCOM carry only the pair, or the verdict too?** The CSV has
  `verdict` and `batch`; a `NOTE` can carry them, and a tree consumer might want to know a pair
  came from the parent deck rather than from a bio.
- **`SAME` only, or the rest?** `manual-identifications.csv` holds rejections
  (`rejected-parents`, 24) and `blocked-creations` (12). A correspondence GEDCOM should probably
  carry only affirmed pairs, but a rejection is also a fact the zipper would benefit from.
- **Does `bio-qids.tsv` stay a separate extract?** Under this design the bios are already in the
  tree, so the extract becomes a *query* over the tree rather than a scan of 600 exports —
  which is faster and cannot go stale the way it just did.

## The staleness that motivates the last point

`bio-qids.tsv` was six days old on 2026-09-05: the special GEDCOM was updated that day and the
extract was last built 2026-08-30, so **3 of its 29 pairs** were visible in the extract. Nothing
schedules the extractor. A design where the bios are read out of the merged tree removes that
failure mode entirely, because the tree is rebuilt from the corpus rather than from a snapshot of
it.
