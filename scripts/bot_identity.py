"""The User-Agent, which is an email address and nothing else.

Emma, 2026-08-18: *"This GitHub repo shouldn't be linked into the user agent. Really,
none of this should be in the user agent. You're leaking a massive amount of information
here. It's just an email address. That is the secret."* And: *"you never, ever, in any
user agent or anything, link the repository."*

So the agent carries **no repository URL, no tool name and no description of what the
project does**. Every one of those told a reader where the code lives and what it is for,
which is the leak. The address comes from the ``BOT_CONTACT`` secret and is the only
content.

There is one address for this whole repo. It is not in the source; version history was
not rewritten, which she said is unnecessary.
"""

from __future__ import annotations

import os
from pathlib import Path

#: Where the address lives when it is not in the environment. Gitignored, so the
#: secret still is not in source -- but every script finds it without the caller
#: having to export anything, which is what kept the ledger refresh from running.
CONTACT_FILE = Path(__file__).resolve().parents[1] / ".bot-contact"


def agent() -> str:
    """The contact address, or empty when the secret is not set.

    Environment first, then ``.bot-contact`` at the repo root. Empty is still a
    supported state -- *"no email on the user agent is fine"* -- and it is better
    than an agent that advertises the repository.

    **The file fallback exists because the env-var-only version silently pushed
    callers onto ``--no-refresh``**, which skips reading Emma's contributions and
    yields a build off a stale ledger that looks exactly like a real one.
    """
    env = os.environ.get("BOT_CONTACT", "").strip()
    if env:
        return env
    try:
        return CONTACT_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


#: Evaluated at import, which is what every caller uses.
BOT_CONTACT = agent()
BOT_USER_AGENT = BOT_CONTACT
