# `geni-extension/` — the Geni collector

**Emma's design, 2026-09-05:** *"I wish we could do this through playwright or some hybrid
thing. Lets say agentically opening up the tabs and then running an extension that we build
explicitly for this purpose. Can't be playwright proper but the extension can basically run
almost all our algorithms"*, and then *"And adding individuals to do a forest export"* /
*"All geni stuff for our repo"*.

Playwright proper is out for the reason she gave: Geni needs **her logged-in Chrome**, and the
pushpin anchor is a property of that account. An extension runs *inside* that session.

## Why it exists — it fixes the one thing that was actually broken

`geni-paths/README.md` names the problem exactly:

> A human reads the state at a glance; an agent gets one sampled snapshot per tool call at
> 10-20 seconds each, so it substitutes cheap DOM reads — which is exactly the channel that
> lies here. **So the design must minimise observations, not parallelise them.**

The extension does not sample at all. A `MutationObserver` fires on the mutation that resolves
the search, so the moment Geni writes the answer in is the moment it is read. And it reads
**rendered visibility** — `offsetParent` and a non-zero box — which is the question the saved
HTML cannot answer and the one the hidden `path_search_response` template defeats.

That template is worth restating because it has now cost this repo twice: it is on **every**
profile, `display:none`, before any search is requested. Matching `innerText` for it reported
22 untouched profiles as running. The same sentence as a substring test inside
`harvest-isolate-paths.pending()` put every genuine miss outside the reach-rate denominator, so
the rate could only come out 100%.

## Install

One-time, and it needs her:

1. `chrome://extensions` → **Developer mode** on.
2. **Load unpacked** → select `geni-extension/`.
3. The toolbar icon opens the panel.

## Use

Paste one Geni id per line. `export ` prefixes an export job; a bare id is a path job.

    6000000004051490175
    6000000174444394081 blood
    export 6000000227036288825

**Load queue** → **Start**. Then **Save results** for the run's TSV, and:

    python scripts/file-geni-downloads.py

which moves the captures into `geni-paths/`, the parsed chains into `paths/`, and the results
TSV into `reports/`. It never touches a `.ged` or a `.zip`.

## What it does per path target

The four states of `geni-paths/README.md`, driven rather than sampled:

| visible on the page | state | what happens |
| --- | --- | --- |
| **"How are they related?"** | not requested | click it, then wait |
| green **path search in progress** bar | running | wait, up to the budget |
| a chain naming the target | resolved | click "Show short path", capture, parse |
| *"No blood relationship was found."* | resolved, no path | recorded, nothing captured |
| no relationship box at all | isolate | recorded; **never** read as *unrelated* |

The capture is a Blob of `document.documentElement.outerHTML` clicked through an `<a download>`
— the method `geni-paths/README.md` § *THE CALL THAT WORKS* records, unchanged, because it is
the one that is known to work. The parse mirrors `genimerge.genipage`: the steps are the
anchors carrying `data-profile-id` **inside `span.segment > span.name`** and nothing else, and
the emitted TSV is byte-compatible with `to_tsv`.

**The guard is that the target's own id must be on the chain.** A miss page renders a full
chain — the viewer's own — so a step count alone scores every miss as a hit.

**Geni's prose summary is kept as a residual**, per `CLAUDE.md` § *Grab the RESIDUALS*: no step
word ever says *half* and the prose does.

## What it does per export

`docs/export-seed-rules.md` is the authority; `content/export.js` implements it. `Forest`,
size 5000, everything else default; submit; **poll the page, not a clock** — the flip to *Your
GEDCOM File is Ready to Download* is the trigger, and letting a clock notice instead dropped
the measured rate from 7.1 exports/hour to about 1.

**Two hard limits of Geni's, not settings.** Exports run **strictly one at a time** —
*"That isn't my decision thats geni"* — so `EXPORT_CONCURRENCY` is 1 and is not in the panel. A
submitted export **cannot be cancelled**; Stop only stops opening new tabs, and any control
implying otherwise would be fiction.

**The zips are not integrated as they land.** They stay in `~/Downloads` until a whole batch is
down, and filing them into `exports/` is hers.

## What it deliberately does NOT do

- **It never touches the pushpin.** *"You do not pin Charlemagne, it needs to be done exactly
  once and I did it."* Toggling it mid-run re-anchors every later search to *"You"*.
- **It does not create the placeholder individual.** `docs/export-seed-rules.md` is a five-tier
  preference order resting on whether a patronymic names a father and whether a Nordic farm
  name is a surname, with a *bail on anything weird* rule — because the wrong call creates a
  person on a live site with other people's trees on it. The mechanical half is automated; the
  naming stays a decision.
- **It decides no rates.** `harvest-isolate-paths.py` still computes the hit rate from the
  saved files, where the guards already live.

## Pacing

`searches at once` is how many may be in flight; a tab is held open **while its search runs**,
because closing it *"drops its promise to notify you"*. `seconds between opens` is the rate and
defaults to 60 — `geni-scraping/`'s one-a-minute rule. `wait minutes` is how long a single
target may run before it is left for the next pass; her measurement is that one *"might take 10
minutes"*.

Bail on anything odd. That rule is unchanged and is not automatable.
