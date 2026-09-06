# Immediate family scrapes

One TSV per person, `<geni id>-family.tsv`, produced by the collector at **step 1** of
`docs/per-individual-loop.md`.

**The collector RETURNS the file; it does not download it.** Emma, 2026-09-06: *"we are not
supposed to be saving pages lol ... Only the exports need downloading because you write stuff
into files in the repo you dummy."* So the TSV comes back in the job result on a data attribute
and is written straight into this directory. Nothing passes through `~/Downloads`, and
`saved: true` -- which used to mean *a click returned* rather than *a file exists* -- is gone.

Emma, 2026-09-06: *"on each individual we always grab the html family members and save them
first"*. It is the cheap, unconditional step -- no search requested, no export spent, nothing
created -- and it runs on everybody before the Charlemagne path is attempted.

Each file carries the subject, Geni's own prose line, the statistics block, and one row per
relative with the relationship it was listed under.
