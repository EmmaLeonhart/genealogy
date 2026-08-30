# Could this repo be public, with Actions emailing a QuickStatements file daily?

**Emma's question, queued 2026-08-27:** *"analysis of whether we could set this repo as public, and
use github actions to have it periodically email me a quickstatements file every day at 9am... I do
not think the security issue is that bad (people who are digging can find stuff), and... making this
100% programmatic i gonna allow for more reliability since I am no gonna need you to constantly
opaquely generate stuff for me where I do not know the degree that somethin is your discretion or
part of the algorithm. Biggest barrier imo is the synoptic tree file stuff."*

Measured 2026-08-29. **She named the barrier correctly, and it is worse than a file-size problem.**

## The size, first

| | |
| --- | ---: |
| tracked files | 46,360 |
| tracked content | **12.2 GB** |
| `.git` on disk | 6.3 GB |

By extension: `.gz` 4,448 MB, `.ged` 4,244 MB, `.download` 1,243 MB, `.css` 701 MB, `.csv` 539 MB,
`.html` 372 MB.

**GitHub's soft limit for a repository is 5 GB and it warns above 1 GB.** This is over that whether
it is public or private, so "make it public" and "keep pushing this repo" are already in tension.
The `.css` and `.download` figures are saved Geni pages under `geni-scraping/`, which are page
furniture rather than genealogy.

## The barrier she named: the synoptic tree cannot be built in Actions

`genimerge merge` over the corpus is **~14 minutes and peaks near 17 GB of RAM** (`CLAUDE.md`
records 16.8 GB, and 23.6 GB for the idempotence test). GitHub-hosted runners give **16 GB on the
standard `ubuntu-latest`**. So the merge does not fit, and a daily job that rebuilds the tree before
generating the batch cannot run on a hosted runner. On *this* machine it has now been killed twice.

That is not a size problem to be solved by pruning — it is the job itself.

**What CAN run in Actions:** the batch generator, `build-garborg-day.py --compose`, reads the
derived CSVs rather than the merge. Those are committed (gzipped). So a daily emailed batch is
feasible **as long as the derived CSVs are refreshed by hand elsewhere** — which reintroduces
exactly the manual step she wants removed, just at a lower frequency.

## The privacy question, which is not the barrier she assumed

Of 1,697,887 name rows in `reports/display-names.csv`:

| | rows |
| --- | ---: |
| `Private` — Geni withheld the whole name | **79,795** |
| `<private> Surname` — given name withheld, surname real | **16,190** |

So ~96,000 rows concern people Geni considers private, most of them living. `CLAUDE.md` records her
position that redacted people still go on Wikidata because the structure is informative — but that
is a decision about *Wikidata*, where the identifiers are already public. Publishing the corpus is a
different act: it republishes Geni's private-profile structure in bulk, outside Geni's access
control, for people who never chose it. That is worth deciding deliberately rather than inheriting
from *"people who are digging can find stuff"*.

**This is hers to decide and is not a technical blocker.** It is recorded here because the question
as asked was about security, and the exposure is bulk rather than the "digging" kind.

## The billing point runs the other way

`ci.yml` is `workflow_dispatch:` only, and `CLAUDE.md` gives the reason: **Actions minutes are free
on public repos but billable on private ones.** So going public *removes* the constraint that made
CI manual, and a daily scheduled job becomes free. That is a real argument in favour, and it is the
one thing the change straightforwardly improves.

## Summary

- **Public repo: possible, with two decisions first** — 12.2 GB against GitHub's 5 GB soft limit,
  and the bulk republication of ~96,000 private-profile rows.
- **Daily emailed batch: possible, but not end-to-end.** The compose step fits a runner; the merge
  it depends on does not.
- **Her stated motive is sound.** A scheduled job would remove the *"I do not know the degree that
  somethin is your discretion or part of the algorithm"* problem, because the run would be a log
  rather than a conversation.
