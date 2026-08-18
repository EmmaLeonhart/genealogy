"""Who the edit bot says it is.

Emma, 2026-08-18: *"User agent for my ci/cd bot should have email
benthicthoughts@gmail.com."* And, guessing at what it had: *"I bet it uses
emma@topazcomputing.com which is wrong."*

**It had no email at all.** `.github/workflows/wikidata-edits.yml` runs two scripts and
both carried their own hand-written agent, neither with a contact:

    wikidata_lockout.py    "genimerge-bot/0.1 (wikidata lockout check)"
    wikidata-edit-run.py   "genimerge-bot/0.1 (https://github.com/EmmaLeonhart/geni)"

That is the case Wikimedia's User-Agent policy is written for and the one it throttles
hardest — an anonymous agent that writes. `emma@topazcomputing.com` does exist in this
repo, on `genimerge.wikilabels`'s SPARQL lookup, but that is a read-only fetcher the
workflow never invokes, so her guess named a real string in the wrong place.

WHY THIS FILE EXISTS AT ALL, rather than a constant in `genimerge.wikidata`

Neither bot script imports the package. They are standalone, the workflow runs them as
`python scripts/...` from the repo root with no `PYTHONPATH`, and `wikidata-edit-run.py`
already imports `wikidata_lockout` as a sibling module. Reaching into `src/` would add a
path hack to the one code path that must not break at 03:00 on 1 September. A
dependency-free module beside them costs nothing and gives the two agents one definition
instead of two strings that had already drifted apart.

**The read-only agents are deliberately not changed.** `genimerge.wikidata.USER_AGENT`
carries `contact@emmaleonhart.com`, added 2026-08-07 with her say-so for the bulk
download, and `genimerge.wikilabels.USER_AGENT` carries `emma@topazcomputing.com`. She
specified the CI/CD bot; those are not it.
"""

from __future__ import annotations

#: Identifies the tool, links the source, and gives a contact — the three things
#: Wikimedia's policy asks for. Used by every request the edit pipeline makes,
#: including the lockout check it runs first.
BOT_USER_AGENT = (
    "genimerge-bot/0.1 (https://github.com/EmmaLeonhart/geni; benthicthoughts@gmail.com)"
)

#: The address, on its own, so a test can assert it without matching the whole string.
BOT_CONTACT = "benthicthoughts@gmail.com"
