# "Claude's inefficient wiki data querying" — 2026-08-07

Text extracted from `Claude's inefficient wiki data querying - Claude.html`
(Sonnet 5, claude.ai, four exchanges). Emma opened it out of irritation at
agentic querying of Wikidata and it turned into a review of the § 8a plan this
repo had just written down; she ended it with *"I'm going to send this to the
agent now."*

One thing the saved page does **not** contain: her second message carried a
**pasted attachment** ("part of the chat"), shown in the page only as the word
`pasted`. The reviewing model was reading a transcript that is not preserved
here. What survives is its response, below.

---

**Emma:** Why is it that Claude is just so aggressively cavalier with wiki data,
querying it in the most inefficient way possible and getting the most 429s
possible?

**Claude:** A common complaint about agentic LLM behaviour rather than anything
specific to wikis, with structural causes: no persistent sense of state across
calls, so nothing stops a re-query of the same page or one request per fact;
an implicit objective of "resolve the request" rather than "be a good API
citizen"; and mostly **missing infrastructure rather than missing judgement** —
no cache, no dedup, no batching (`titles=A|B|C` instead of three calls), no
backoff, no throttle. MediaWiki APIs are easy to misuse this way because the
naive shape mirrors how a human clicks through a wiki. The fix is external to
the model: caching/dedup layer, batching, respect `Retry-After`, and a tool
design that nudges toward batched queries.

---

**Emma:** *(with the pasted transcript)* Here is part of the chat, can you give
me advice?

**Claude:** The plan is basically sound on the parts that mattered — SPARQL for
cheap bulk structure, the JSON entity endpoint for per-item pulls, backoff from
the start, resumability. Three flags:

1. **"Commit and push per item" will hurt.** 500k items means 500k commits or
   500k tiny diffs; git gets slow and the repo unreasonable long before item
   100,000. Write JSON to disk continuously, commit in batches. *"The
   never-query-twice property doesn't require a commit per item, it requires a
   durable on-disk record — the commit cadence is a separate knob."*
2. **Don't resume from git history — track state explicitly.** A SQLite table
   or flat manifest of QID → done is instant; `ls`-ing 500k files or grepping
   `git log` is not. It is also where retry counts and last-error live.
3. **At 500k items, reconsider hitting the live API for the seed set at all.**
   Wikimedia steers bulk consumers to the **Wikidata JSON dump** — a weekly
   full/truthy dump streamed and filtered locally, zero rate-limit risk. SPARQL
   for the P2600 QID list, then pull those items out of the dump. The
   **expansion** phase genuinely needs live queries because the frontier is not
   known in advance — so seed and expansion should use *different* strategies,
   not one uniform "hit the API slowly" plan.

Plus a Wikimedia-specific gotcha: **`query.wikidata.org` has its own limits,
separate from the action/REST API** — a 60-second query timeout and its own
throttling — so SPARQL needs batching and pagination too.

---

**Emma:** Every hundred or every thousand individuals would be fine; per
individual would be a big problem. *"This is supposed to be hard committed as
part of the repo. That's just how I'm doing it."* **The JSON dump is probably
the biggest thing to note here.**

**Claude:** *(the § 8a-revised sketch — storage/commit cadence, the two-phase
sourcing split, and the SPARQL-limits note; reproduced in `todo.md` § 8a-revised
rather than duplicated here)*

---

**Emma:** I'm generally not really sure about the 500,000. We could probably get
the 500,000 relatively quickly through this thing and then operate on the
frontier with it — faster than the search thing. **A large amount of the 500,000
are going to reach each other.** Expanding the tree beyond the stuff that has
Geni IDs is likely not going to be people without Geni IDs; it's going to be
mostly specific holes and specific lines that are only on Wikidata.

**Claude:** *(the expansion-scope note — expect heavy interconnection inside the
seed set, expect a small patchy frontier, and treat a much-larger-than-expected
frontier as a signal that an edge type is fanning out wrong rather than as the
expected case. Also in `todo.md` § 8a-revised.)*
