"""Who the edit bot says it is.

Emma, 2026-08-18: *"User agent for my ci/cd bot should have email Email Address B."* Then: *"Ideally, the Benthic one should be a secret in the
repo."* And on what to do when it is not available: *"No email on the user agent is fine!
Although Benthic thoughts are best."*

So the address is **not in this file**. It comes from the `BOT_CONTACT` environment
variable, set from a GitHub Actions secret of the same name, alongside the `USERNAME`,
`BOT_NAME` and `BOT_PASSWORD` secrets the workflow already uses. Without it the agent
still names the tool and links the source and simply carries no contact, which she said is
acceptable.

**What must never come back is `Email Address T`.** That address belongs to
order.life, not here — her words, *"order.life should use Email Address T because
it is order.life; the geni one is supposed to use the Benthic one"* — and
`tests/test_bot_identity.py` asserts no agent in this repo carries it.

WHAT THIS REPLACED

`.github/workflows/wikidata-edits.yml` runs two scripts and each carried its own
hand-written agent, neither naming a contact at all:

    wikidata_lockout.py    "genimerge-bot/0.1 (wikidata lockout check)"
    wikidata-edit-run.py   "genimerge-bot/0.1 (https://github.com/EmmaLeonhart/geni)"

An anonymous agent that *writes* is the case Wikimedia's policy is written for and the one
it throttles hardest, and the two strings had already drifted apart from each other.

WHY A MODULE BESIDE THEM RATHER THAN A CONSTANT IN `genimerge`

`wikidata-edit-run.py` already imports `wikidata_lockout` as a sibling, and Python puts a
script's own directory on the path, so this import works however the step is invoked. The
workflow does set `PYTHONPATH: src` on the batch step — an earlier version of this
docstring claimed otherwise and was wrong — but the lockout step runs before it and does
not, so a `genimerge` import would work in one of the two places it is needed.
"""

from __future__ import annotations

import os

#: The contact, from the `BOT_CONTACT` secret. Empty when unset, and that is a supported
#: state rather than an error.
BOT_CONTACT = os.environ.get("BOT_CONTACT", "").strip()

#: Identifies the tool and links the source always; adds the contact when there is one.
BOT_USER_AGENT = (
    "genimerge-bot/0.1 (https://github.com/EmmaLeonhart/geni"
    + (f"; {BOT_CONTACT}" if BOT_CONTACT else "")
    + ")"
)
