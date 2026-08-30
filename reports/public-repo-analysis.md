# Could this repo be public, with Actions emailing a QuickStatements file daily?

**Emma's question, queued 2026-08-27:** *"analysis of whether we could set this repo as public, and
use github actions to have it periodically email me a quickstatements file every day at 9am... I do
not think the security issue is that bad (people who are digging can find stuff), and... making this
100% programmatic i gonna allow for more reliability since I am no gonna need you to constantly
opaquely generate stuff for me where I do not know the degree that somethin is your discretion or
part of the algorithm. Biggest barrier imo is the synoptic tree file stuff."*

Measured 2026-08-29. **She named the barrier correctly, and it is worse than a file-size problem.**

## The size, and a correction

| | |
| --- | ---: |
| tracked files | 46,360 |
| working tree | 12.2 GB |
| packed history (`size-pack`) | **6.15 GB** |

By extension: `.gz` 4,448 MB, `.ged` 4,244 MB, `.download` 1,243 MB, `.css` 701 MB, `.csv` 539 MB.
The `.css` and `.download` are saved-page furniture under `geni-scraping/`, not genealogy.

**An earlier draft of this said the 5 GB figure blocked CI. It does not, and Emma caught it:**
*"the repo size can be larger as history isn't in it?"* — correct.

- GitHub's 5 GB is a **soft limit on the hosted git database**, i.e. the 6.15 GB pack. It produces a
  warning, not a refusal.
- **CI never downloads that.** `actions/checkout` defaults to `fetch-depth: 1`, so a run fetches one
  commit's tree. A hosted runner has ~75 GB free disk, so even the full 12.2 GB working tree fits.

So size costs **checkout time**, not feasibility. It is not a barrier to either going public or
running a scheduled job.

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

## Her direction, 2026-08-29

*"we will optimize the cicd revisions to be small and do other things to optimize filesizes for the
runners but can 100% do all this stuff if we anonymize it properly"*

So the plan is: **shrink what CI checks out, and gate going public on anonymisation.** Both are
sound — the memory ceiling is the only hard stop, and it is marginal (16.8 GB against 16 GB).

**One constraint worth knowing before designing the anonymisation, because it is not obvious.**
The Geni profile ID *is* the identifier, and it is also this repo's primary key — every join, the
`P2600` statements, the ledger, the spines. So anonymisation cannot simply hash or drop the IDs
without breaking the thing the repo exists to do. The likely shape is therefore **redacting the
private people's content while keeping the structure**, which is close to what Geni already does and
what `CLAUDE.md` § *Redacted people go in* already assumes for Wikidata.

Not designed here. Flagged so the design starts from the right constraint.
