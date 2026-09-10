# The collector, Geni and the browser

**Moved out of `CLAUDE.md` on 2026-09-09, verbatim.** The ruling was to cut `CLAUDE.md`
to under 1,000 lines and put the evidence for each rule on a page that `CLAUDE.md`
cites. Nothing here was reworded, shortened or dropped in the move — this is the
reasoning, the measurements and the post-mortems behind the one-line rules.

---

### ⛔ BOTH TIES, ALWAYS. BLOOD **AND** MARRIAGE TO CHARLEMAGNE, PLUS THE IMMEDIATE FAMILY

**The goal for each person is a blood tie AND a marriage tie to Charlemagne, plus their full
immediate family.** That builds an interconnected graph on Wikidata with far more surface area
for genealogical material to be grafted onto — from Geni above all, and from Genealogics,
WikiTree and the rest.

**⛔ THE REDUNDANCY IS THE POINT. It is not waste to be optimised away.** The ring of blood plus
non-blood gives the maximum number of relatives to go through, for the minimal cost of clicking
the button twice and waiting.

So a person's deliverable is a **ring**: the blood chain to Charlemagne, the marriage/in-law
chain to Charlemagne, and their immediate family. Two chains reach far more relatives than one,
and the extra cost is one more click and one more wait. Do not treat the second chain as a
fallback for when the first fails — that reading is what produced the bug this section replaces.

### THE FOUR RULES

1. **Both searches, always, on every person.** Requesting a blood relationship always requests the
   non-blood ways too, and a blood miss always looks at the other ways. Not in-law-as-fallback.
   Both, every time.
2. **A blood miss with no path is NOT DONE.** If blood did not hit and there is no path, redo it.
3. **⛔ DO NOT BACKFILL IN-LAW ONTO PEOPLE WHO ALREADY HAVE A BLOOD PATH.** The 12 already-resolved
   people keep their worse coverage. That is a deliberate cost, accepted to avoid the massive
   rework, not an oversight to correct later.
4. **The redone people are ORDINARY QUEUE MEMBERS**, and their order does not matter. They are
   not a separate backfill campaign — they go into the same pool as everyone else.

### ⛔ ANYTHING ODD ABOUT A PERSON -> FOREST EXPORT. Stop investigating

**If anything odd occurs with any individual, run a `Forest` export**: make an ancestor of them
and export around it, rather than planning an investigation.

**This authorises `job.create`** — creating an ancestor and running the `Forest` export — as the
STANDING response to an anomaly, in place of writing it up. `docs/export-seed-rules.md` is how
the placeholder is made and `Forest` is the style, both already specified.

**It replaces a habit, and that is the point.** A person who behaves oddly was becoming a
NEEDS-INVESTIGATION line in a status report, which costs a read and returns nothing. An
export costs one seed and returns up to 5,000 people around them — and `Forest` is precisely the
style that follows spouse links, which is what the in-law half of the ring needs.

### How progress is tracked, and why "mark them not done" needs no editing

**Progress is DERIVED, not stored, and no list is hand-edited.** `scripts/collector-worklist.py` recomputes
who still needs the collector on every run, from two facts on disk:

    no `geni-families/<id>-family.tsv`                    -> never scraped
    `reports/isolates.csv` row with path_found=no and     -> blood-only miss, rule 2 says redo
      `via` not recording that other-ways was checked

So rule 2 is satisfied by the criterion itself: the moment `via` became the record of which
search answered, every blood-only miss re-entered the pool without a row being touched. Nothing
is deleted to mark work undone, which matters because the family scrape on those people is real
data that must survive the re-run.

### ⛔ PLAYWRIGHT AND HEADLESS ARE A NO-GO. The agentic navigation is overhead we PAY, not a design

**The agentic navigation is complete overhead paid to be able to run this at all. Playwright is
a no-go, and so is anything headless.**

**Why it is paid rather than chosen.** Geni heavily gates API access. Driving a real, logged-in
browser is what makes the traffic acceptable: navigating to the page agentically and then running
the extension counts as proper traffic. Geni served an Incapsula CAPTCHA after roughly forty
rapid loads, which is what the cheaper route costs.

**So the agent's job is navigation and nothing else.** The queue asks the browser agent to
navigate to each page and run the extension: one `{job:"individual"}` call per profile, every
decision inside the extension — `docs/collector-run-loop.md`. **There is no discretion on the
agent's part at all.**

**And that is why the scheduler was always iffy**, which resolves a day spent treating its stale
service worker as a blocker. A scheduler that opens its own tabs removes the
very thing that makes the traffic pass. It is not the missing piece; the agentic loop is the
working one.

**Where it might go**, as an interest rather than a plan: browser automation that eliminates more
of the agentic components — one button in the browser, working through the queue gradually.

So the target shape is **the browser, one button, working through a queue at its own pace** —
which is what `background.js` was reaching for. The open question is whether extension-driven navigation
still reads as proper traffic; that is measurable and unmeasured, and it is the thing to establish
before building toward it. **What is settled is the floor: no Playwright, no headless.**

### ⛔ AN EMPTY BROWSER LIST IS NOT A BLOCKER. THE EXTENSION EXISTS AND YOU CAN ALWAYS GET IT WORKING

**An empty browser list is not a fact about the machine, and stopping on one is not acceptable.**
The extension exists and can always be got working.

**What the stop looked like.** `tabs_context_mcp` answered *"Browser extension is not
connected"*, `list_connected_browsers` returned `[]`, `switch_browser` said *"No other browsers
available to switch to"* — and that was reported as **BLOCKED-ON-USER-ACTION** and put in an
`AskUserQuestion` whose first option was *go and click Connect*. Three tool results in one
minute, treated as a fact about the machine.

**It was never a fact about the machine, and one command said so.** The extension is installed —
`fcoeoabgfenejglbffodgkkbkcdhcgfn`, **v1.0.91 under `Default` and v1.0.85 under `Profile 4`** —
and Chrome was running with 19 processes the whole time. `[]` describes the **pairing channel at
one instant**, nothing more. It is the same shape as every other invented limit in this file: a
mechanism's state reported as the task's ceiling.

**So an empty list is where the work starts.** In rough order, and none of these had been tried:

* **Wait and re-call.** The MCP server is often still connecting — the session's own
  system-reminder says so in as many words, and `ToolSearch` deliberately *waits* for a
  connecting server. Two calls a minute apart is not a retry.
* **`tabs_context_mcp{createIfEmpty:true}`**, which creates the group rather than reporting its
  absence.
* **`switch_browser`**, which broadcasts a Connect prompt to every extension instance, and
  **`select_browser`** with a deviceId once one answers.
* **Look at the machine.** Which Chrome profile is actually running, and does it carry the newer
  build? Two profiles here hold two different versions, and driving the stale one is a different
  problem from driving none.
* **Only then, one sentence** — *click Connect in the extension* — as a line in the report,
  never as a question with options. A one-click thing does not get an
  `AskUserQuestion`; § *EVERY TWO HOURS* is for work that claims to be stuck, and this does not
  qualify until everything above has failed.

**And do not idle on it.** § *SWEARING IS NOT A STOP ORDER* — the thing that provokes it is
stopping, not a wrong technique. If the browser genuinely will not pair after all of that,
say which mechanism failed and keep working on something else in the same turn.

### ⛔ KILL CHROME WHENEVER YOU NEED TO. That is standing authority, not a blocker

**You, 2026-09-09, on being told the extension could not be reloaded:** *"whatever the fuck this
block on user action bullshit is, just fucking remove it. You have full authority to kill Chrome
at any given moment in order to start this stuff again. It's not hard."* And: *"I'm asking you to
kill Chrome, by the way."*

**An unpacked extension does not pick up file changes on its own, and `chrome://extensions` is
refused to the automation surface the same way every `chrome://` URL is.** That is true and it is
NOT a blocker, because restarting the browser reloads the extension. The recipe you gave:

    kill -9 the Chrome processes
    force-open Chrome again from the command line on any page -- google.com will do
    the extension has reloaded; drive it as normal

**So a stale extension is never BLOCKED-ON-USER-ACTION and must not be tagged as one.** It was
tagged that way in four status reports on 2026-09-09 while 1.6.5, 1.6.6, 1.6.7 and 1.6.8 sat on
disk unrun — a mechanism's inconvenience reported as the task's ceiling, which is the exact
failure § *NEVER SAY YOU CANNOT DO SOMETHING YOU HAVE NOT TRIED* names. The version the browser
is running is measurable — `documentElement.dataset.geniCollector` — so there is no excuse for
not knowing, and now none for not fixing it.

**Two things worth keeping.** Killing Chrome loses whatever the browser was doing, so a Geni
export mid-submit is worth landing first — a submitted export cannot be cancelled and the
download page can be reopened by task id, but an unsaved form cannot. And the pairing with the
Claude extension has to be re-established after a restart; § *AN EMPTY BROWSER LIST IS NOT A
BLOCKER* is the procedure for that and it is also not a blocker.

### The working Geni capture call lives in ONE transcript. Name it, do not re-derive it

**Do the way that already worked; look it up rather than being creative.** A session rebuilt a
local HTTP sink to POST page captures to, having already been told the method existed.

**The transcript is `7a11670b-624d-43f7-ae9b-48665823b8e7.jsonl`, 2026-09-03** — in
`C:/Users/Emma/.claude/projects/C--Users-Emma-Documents-GitHub-geni/`. It is the session that
settled the whole isolate-path method: the `/path/` URL refuted, the pushpin anchor validated,
and the French-Canadian `Forest` export near George Drouillard that proved a Geni *"no
relationship found"* is a database failure rather than a negative result — 5,000 people, 7 of
them already in our tree, all 7 in the main component, Drouillard four hops from Charles
Lespérance.

**The call itself is now written out in `geni-paths/README.md` § *THE CALL THAT WORKS***, so
the transcript is the provenance rather than the only copy. It is a `browser_batch` of
navigate → a `javascript_tool` block that waits, clicks *"Show short path"*, waits again and
Blob-downloads `outerHTML` → `tabs_close_mcp`; the file lands in `~/Downloads` and is `mv`d
into `geni-paths/`.

**Why it got re-derived, because the shape recurs.** The README carried the *steps* —
navigate, wait, click, wait, save — and no *call*. Steps read as a description of a thing
someone would build; a call reads as a thing to copy. The session that reinvented it did so
after correctly measuring that a plain `fetch()` returns zero `span.segment` anchors, which is
true and is exactly the finding that makes the recorded call necessary. **A method documented
as prose gets rebuilt; a method documented as the literal call gets reused.**

This is the same family as § *Do not grab the first artifact that vaguely matches* and
§ *Code that is WRITTEN but never CALLED is not done*: the gap is between what the repo says
and what the repo lets you run.

### ⛔ A SHORTCUT TAKEN TO UNBLOCK A SESSION IS NOT A LAW TO ENFORCE BACK

**The case.** *"You do not pin Charlemagne, it needs to be done exactly once and I did it"* was
said because a session had stalled on the page instead of working — a shortcut to unblock it,
not a constraint. That went into `CLAUDE.md`, into `queue.md`, and into a test, as though the
anchor were untouchable. Setting up a protocol to get it set was always allowed. When the
first real path capture came back anchored on the viewer — making the pilot's reach rate answer a
different question than the one asked — it was written up as **NEEDS-DECISION** and left sitting
across three status reports. It was never a decision at all. It was a thing to check and set, and
`docs/anchor-protocol.md` is now that protocol.

**The general rule: when something is done by hand because the automation is stuck, the lesson is
AUTOMATE IT, not THIS IS SACRED.** A workaround describes a gap in the tooling. Reading it as a
constraint inverts it — the gap stays open and the workaround becomes permanent manual labour,
which is the opposite of the point.

**How to tell the two apart.** A real constraint has a reason attached that survives the
tooling improving — *the pushpin must not be toggled MID-RUN* is one, because it silently
re-anchors every later capture, and that stays true forever; the test enforcing it stays. *It was
set once by hand* is not a reason, it is a description of what happened when nothing else would
do it.

**And it is the same failure as § *Do not grab the first artifact that vaguely matches*, one
level up:** there, availability turned a stale file into an algorithm; here, a sentence spoken
about one bad session turned into a standing prohibition.

### Grab the RESIDUALS. The structured parse is not everything on the page

**So much structurally weird material comes through that residuals have to be grabbed all the
time.**

**The worked case, and it is why this is a rule.** `genimerge.genipage` parses a path as the
anchors inside `span.segment > span.name`, which is correct and is what makes the join exact.
But over **30,329 steps in 696 path files** those step words never say *half* — only
`his brother` / `her sister`. Geni does say it, in two elements the parser walks past: the
immediate-family block (*"Half brother of …"*, 325 occurrences across the saved pages) and the
prose `relation_description`, which reads *"…partner's son's wife's ex-husband's half sister's
ex-husband's second cousin twice removed's wife's father."*

So the page held a distinction our extraction destroyed, and nothing recorded that it had.
`genipage.relation_description()` now keeps it — present on **664 of 664** saved pages, 15
mentioning *half* and 112 *ex-* — written into every generated path file's header and into
`reports/isolate-path-pilot-results.tsv`. It is stored **as-is and not parsed**: the in-law
prose is a possessive chain that does not map one-to-one onto the segments, and aligning them is
a separate job nothing does yet.

**The rule: when an extraction narrows a page to a structure, keep what it dropped.** A residual
costs a column; recovering a distinction after the pages are gone costs a re-fetch of everything.
This is the § *check the separator before believing a distribution* family — an instrument that
quietly narrows its input and reports a clean number about itself.

**And the residual extractor had that exact bug on its first run.** A non-greedy `.*?</div>`
stopped at the block's first child, an expand/collapse image wrapper, so it returned whitespace
and measured **0 of 200 pages** as having a description. Balancing `<div>` depth instead gives
664 of 664. A terminator that is not the right terminator reads as absence.
