# CI, the pipeline and the published site

**Moved out of `CLAUDE.md` on 2026-09-09, verbatim.** The ruling was to cut `CLAUDE.md`
to under 1,000 lines and put the evidence for each rule on a page that `CLAUDE.md`
cites. Nothing here was reworded, shortened or dropped in the move — this is the
reasoning, the measurements and the post-mortems behind the one-line rules.

---

### ⛔ TESTS RUN IN CI/CD OR NOT AT ALL. Never run the suite locally

**Tests are on CI/CD or not at all.**

**So do not run `pytest` here. Not the fast lane, not a single module, not in the background.**
`.github/workflows/ci.yml` runs on a schedule and on demand, and that is the only place the suite
executes. The green tick on a sha is the signal; there is no local equivalent to report.

**This is a standing rule, not a mood.** It has been drifted from repeatedly — the fast lane was
run six times in one evening on 2026-08-31, and again on 2026-09-02 in the background twice after
the point had already been made once. Backgrounding it is not a loophole: it still burns the
machine and still produces a number nobody wants.

**What this forbids in a status report:** a local pass count, "I'll run the lane on the next
tick", and any claim resting on a suite this session executed. § *Test-suite health* is answered
by **which sha CI last went green on**, and by nothing else — if that sha is older than the work,
say so plainly rather than filling the gap with a local run.

**What replaces it is unchanged** — § *"Analyse this" means
build a CSV*. A change is trustworthy because it was **measured over the real corpus**: how many
rows moved, which ones, and a sample read by eye. Every real defect this session came from that —
`スザンナ・h・ベイツ`, `土岐頼芸` emitting a bare surname, the Han range that swallowed Hangul —
and none came from the suite.

**The one thing tests are still good for is the platform this machine is not**, which is exactly
why they belong in CI: the Windows-path bug of 2026-09-01 was found by the first CI run and by
nothing else.

### The NO-NEW-TESTS moratorium ENDED on 2026-09-01, on its own terms

**The condition was: no more tests until CI/CD runs with GitHub Actions on a public repo**, the
existing suite being untrustworthy. That condition is now met
and was met by the thing itself rather than by anyone deciding it had been: the repo went public
on 2026-09-01, `.github/workflows/ci.yml` runs on a schedule and on demand, and the fast lane is
**green on 3.10 and 3.13**.

**So new tests are allowed again.** What does not come back is the habit the moratorium was
against — a test that asserts only the case its function already defaults to.
`tests/test_namemodel.py:620` is the worked example and it still stands as the warning: it passes
with the discriminator *deleted*, so it never observed the thing it appears to pin, and 62,637
tokens went out mis-modelled underneath it.

**And measurement stays the primary evidence.** Every real defect found on 2026-08-31 and
2026-09-01 came from reading output over the real corpus, not from the suite: `Bjørn` → `бйёрн`,
`strip_markers` not being idempotent, `<private> Garborg` emitted as a label for 14,449 people,
ㄹ named two different things in two slots, and a `csv.writer` path normaliser replacing two
backslashes where a path has one. The suite caught same-hour regressions, which is what a suite
is for and is a different job from establishing that new work is right.

**What CI actually changed** is that a defect can now be caught on a platform this machine is
not. The Windows-path bug was found by the first CI run and by nothing else.

### The repo is PUBLIC as of 2026-09-01. CI runs — and `pipeline.yml` DOES run on push

The repo went public so that CI could run without spending attention on the test question.
Actions minutes are free on public repos, so the cost argument that made CI manual-only is gone and `.github/workflows/ci.yml` now
carries `schedule:` (05:17 daily, off the hour) and `pull_request:` alongside `workflow_dispatch:`.

**`push:` was banned outright until it was reversed for ONE workflow:** a push should trigger
the pipeline to go all the way, up to a working `.qs` file and the daily batch on the site.

So `.github/workflows/pipeline.yml` carries `push: branches: [main]`, and **a push bypasses the
six-hour gate**. That is the point rather than a side effect: the gate asks whether *Wikidata*
has been edited, which cannot see that the *repo* changed. Gating pushes on those contributions
would
reproduce the failure this trigger exists to fix.

**Everything else still fails the test if it gains `push:`.** The exemption is one trigger on one
named file — `RUNS_ON_PUSH` in `tests/test_repo_invariants.py` — plus a second test asserting that
file still exists and still uses it, so a stale exemption cannot quietly become a hole. The
original reasoning stands for every other workflow: this repo commits large generated files many
times a day, and a run per push queues behind itself for no signal.

**It cannot loop, and that is a documented GitHub rule rather than a hope.** A push made with the
repository's `GITHUB_TOKEN` does not create a new workflow run. The pipeline commits as
`github-actions[bot]` through the token `actions/checkout` persists, so its own push to `main` is
inert; only a push from a person or a Claude session starts a run.

**⛔ A BURST OF PUSHES DOES NOT QUEUE. GitHub keeps ONE pending run per group, and this
paragraph said the opposite until 2026-09-09.** `concurrency: pipeline` with
`cancel-in-progress: false` means a run that is **mid-push is never cancelled** — that half is
right and is the half that matters, since a run killed between its commit and its push is the
failure the setting exists to prevent. But the waiting run **is** cancelled when a newer push
arrives. Measured, three instances in seven minutes:

    run 471  created 20:23:16  cancelled 20:27:06   <- 472 created 20:27:04
    run 472  created 20:27:04  cancelled 20:30:18   <- 473 created 20:30:17
    run 473  created 20:30:17  cancelled 20:33:0x   <- 474 created 20:33:0x

Each cancellation lands within two seconds of the next run being created, which is the tell.

**It is benign, and arguably what you want** — the superseded run would have rebuilt from an
older sha, and the survivor's checkout contains its commits anyway. Three consequences, all of
which cost a turn here before they were understood:

* **A cancelled pending run is not a failure.** Do not investigate one, and do not report it as
  a broken pipeline.
* **Three pushes produce two runs.** Any count of runs against pushes will be short, by design.
* **Do not push again while waiting on a run you want to watch**, because the push cancels it.
  Land the work in one commit, or accept re-arming the watch on the new run.

If the queue ever becomes the problem, the lever is a `paths-ignore:` on the trigger — not
`cancel-in-progress`, which is the thing that would kill a run between its commit and its push.

**What "all the way" means, checked end to end:** push → gate forced → ledger refresh and
`--compose` → commit and push the batch → `site` job builds Pages **from the sha just pushed** →
the daily batch appears on the site. That last hop needed its own fix the same day; see
§ *The Pages site is built from the sha the pipeline PUSHED*.

### The Pages site is built from the sha the pipeline PUSHED, not the one that triggered it

**`needs:` orders jobs. It does NOT move `github.sha`.** A reusable workflow called with `uses:`
runs at the *caller's* sha, and `actions/checkout` with no `ref` takes it — so `site: needs:
pipeline` sequenced the site after the rebuild while still building the tree as it stood *before*
it, because the pipeline pushes its commit after the sha is already fixed.

**Measured on run 33687514166 (2026-09-02):** the `pipeline` job pushed `4111f4d` at 22:02:19 and
`site / build` checked out `8dcf42f6` thirteen seconds later. Since `build-pages-site.py`
publishes `reports/wikidata-garborg-day.qs` on the page, **every site build served the previous
batch** — it had never once shown the batch from its own run. The symptom was that the pipeline
did not update GitHub Pages.

**The fix is an explicit hand-off:** the `pipeline` job outputs `git rev-parse HEAD` after its
rebase and push, `pages.yml` takes a `ref` input on `workflow_call`, and the `site` job passes it.
Empty falls back to `github.sha`, which is right for the schedule and for the nothing-changed path.

**The comment that used to sit in `pages.yml` claimed the opposite** — *"the site is rebuilt from
the same commit that just produced the batch"* — which is why it survived a day of runs. A comment
asserting a property nobody measured is worse than no comment: it answers the question for the
next reader, wrongly. It now carries the measurement instead.

**And the same fact about `github.sha` breaks the COMMIT step too, which is a second bug from one
cause.** The pipeline job checks out the triggering commit, so when two pushes land close together
the second run rebuilds from a base predating the first run's output commit, and rebasing its
regenerated files onto the first run's regenerated files conflicts every time. **Measured
2026-09-06: runs 199, 200, 202 and 205 all died at `Commit the rebuilt batch`**, and `site` is
`needs: pipeline`, so Pages stopped republishing with them — the exact symptom this section was
written about, arriving by a different route. The step now resolves such a conflict in favour of
the run's own rebuild (`--theirs` during a rebase) and retries the push up to five times. Every
conflicting path is a generated file by construction: the replayed commit holds only what the
rebuild changed, and a conflict needs both sides to have touched the path.

**The checkout has to be sparse or it does not fit.** Measured 2026-09-01: **13.3 GB tracked** —
`wikidata/` 4.3 GB, `exports/` 4.3 GB, `paths_for_wikidata_isolates/` 2.7 GB, `reports/` 1.1 GB —
against roughly 14 GB of runner disk. `filter: blob:none` plus a non-cone sparse checkout drops
what no test opens. **`exports/` and `out/` both stay in**: `test_repo_invariants` compares
`git ls-files` against `find` over the corpus, and `test_garborg_day_batch` resolves name items
against `out/wikidata/name-items-in-store.tsv.gz` — excluding either does not skip a test, it
fails one, and the failure is about the checkout rather than the repo.

**First run, 2026-09-01: 1,491 passed, 3 failed**, and one of the three was a real portability bug
nothing local would ever have caught — `build-repo-freshness.py` normalised Windows paths with
`.replace(chr(92)*2, '/')`, which replaces *two* backslashes where a path has one, so every
`generator` column stayed `scripts
ame.py` and resolved nowhere but Windows.

### A ten-minute ceiling is not a wall. Run it in the BACKGROUND, do not hand it back

This paragraph used to end *run it in your own terminal*, and that sentence was quoted in status
report after status report as though the slow lane needed somebody else. It does not. The
**foreground** tool call has a ten-minute ceiling; a **backgrounded** one does
not, and the slow modules run there perfectly well — sequentially in one command, so the
whole-corpus merges do not thrash each other.

**This is the same failure as every other invented limit in this file** — `LAST` as a value,
QuickStatements pointing at a fresh `CREATE`, the exports waiting on somebody. A real constraint
on one *mechanism* got written down as a constraint on the *task*, and then reported as
a blocker. § *The batches are a SEQUENCE* names the pattern: **learned helplessness about
something we can straightforwardly do.**

**So: run it, in the background, and report the numbers.** Never write "needs your terminal",
"run this yourself", or a slow-lane figure carried forward from a previous measurement, unless
the thing genuinely cannot execute here — and a long runtime is not that.

**Chunk the slow lane by COST, not by test count.** The unit of cost is the *fixture*: four
tests that only read the merged tree share one 837s merge and finish in 15m28; the two that
re-stream all 546 exports take 32m07; the three that re-merge or write the 409 MB file take
42m34. Splitting `-k` along those lines is what took `test_merge_real_exports` from "killed at
2 of 9, repeatedly" to **9 of 9 passed**.

**A whole-module run kept dying around 40-60 minutes and it was never hung** — CPU was
accumulating the whole time. The reading that each test took twenty minutes was wrong: it was
one 14-minute fixture followed by two heavy tests. Run `--durations=0` before concluding
anything about where a slow module spends itself.

**A second `pytestmark` assignment silently overwrites the first.** That is how the
marker looked applied and was not: `test_merge_real_exports.py` had
`pytestmark = pytest.mark.slow` on line 24 and
`pytestmark = pytest.mark.skipif(...)` on line 28, so the slow mark vanished and the
ten-minute merge kept running in the fast lane. Combine them into a **list**. The
symptom is a `-m "not slow"` run that still takes minutes while
`--collect-only` reports the tests as deselected.
The suite is fast, needs only pytest, and covers the real 24 MB exports. The one
thing local runs cannot do is the Python version matrix — `tests/test_python_floor.py`
is a partial stand-in for that, and says so.
