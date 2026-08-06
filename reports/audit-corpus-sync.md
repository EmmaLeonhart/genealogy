# Audit — why the cloud counts a different corpus from the PC

Settles queue item 0.0. **Verdict: REAL, with a DOC-FLAW rider.** The cloud is
not wrong and nothing is lost. 41 of the 98 GEDCOMs on the PC are gitignored by
full path, deliberately, so a fresh checkout anywhere — cloud, another machine,
CI — receives 57 and measures a smaller corpus than any report in `reports/`
describes. The flaw is that nothing said so.

Numbers below are from **Emma's PC, 2026-08-06**, and the cloud half is quoted
from the queue item that recorded it.

## PC ground truth

```
on disk:   98      find exports -name '*.ged' | wc -l
committed: 57      git ls-files 'exports/**/*.ged' | wc -l
gitignored: 41     git check-ignore over the 98 on-disk paths
.ged lines in .gitignore: 41
```

57 + 41 = 98, exactly. There is no third category: every GEDCOM on disk is
either tracked or named on its own line in `.gitignore`. Nothing was renamed,
lost, or merged from outside `exports/`.

## Cause, in one commit

`6eddadd` *"Undo cf45547's file additions: keep the exports on disk, out of
git"*, whose message states the decision outright:

> The 37 GEDCOMs in `exports/fleshing-out/export-geni/` stay on disk and are now
> untracked — `git rm --cached`, not a delete. They are gitignored by full path,
> one file per line, because a `*.ged` pattern would also hide the exports this
> repo does track.

The batch is ~200 MB and has grown to 41 files since. The one-line-per-file
style is the same deliberate choice made for the zips: a pattern would be tidier
and would destroy the signal that a new file has arrived.

So the ten basenames the cloud found missing — `export-Forest-0/1/3/4/7/8/20/33/38.ged`
and `export-BloodTree-16.ged` — were never removed. They are on the PC, they are
in the merge, and they are named in `.gitignore` lines 133 onward.

## What the docs got wrong

`CLAUDE.md` § Layout and § "`exports/` is the corpus" and `README.md` both say
every `.ged` beneath `exports/` is corpus the moment it is extracted. True of
the merge, and misleading about git: they never say that most of the corpus is
untracked. The commit message on `1de6d0c` — "corpus is 98" — is the same claim
without the qualifier. Anything that reads the repo rather than the disk gets
57 and has no way to notice.

**Consequence to keep in mind, not to fix by committing the files:** reports in
`reports/` are generated on the PC over 98 exports and cannot be reproduced from
a clean checkout. `reports/frontier.md`, `density.md`, `paths.md` and `merge.md`
are therefore *records of a measurement*, not artefacts a second machine can
re-derive. A cloud session must not "correct" them downward to what its 57
exports produce.

## Not done here

- **NEEDS-DECISION (Emma) — should the 41 be committed?** Committing them makes
  every checkout reproduce the reports and costs ~200 MB in git forever, on a
  private repo. Leaving them out keeps the repo small and keeps the cloud
  permanently unable to reproduce a report. `6eddadd` chose the second; the
  choice was never written down where a reader would find it, which is what
  produced this audit.
