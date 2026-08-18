"""The edit bot must say who it is, and say it once.

Emma, 2026-08-18: *"User agent for my ci/cd bot should have email
benthicthoughts@gmail.com."*

Before this, `.github/workflows/wikidata-edits.yml` ran two scripts and each carried its
own hand-written User-Agent with **no contact at all** — an anonymous agent that writes,
which is the case Wikimedia's policy exists for and throttles hardest. The two strings had
also already drifted apart from each other.

What is pinned here is the rule, not the string's exact shape: the bot identifies itself
with Emma's bot contact, both entry points use the same constant rather than their own
copy, and the read-only agents keep their own separate addresses because she specified the
CI/CD bot and not everything.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"

sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(REPO / "src"))

import bot_identity  # noqa: E402
import wikidata_lockout  # noqa: E402
from genimerge import wikidata, wikilabels  # noqa: E402

BOT_SCRIPTS = ["wikidata-edit-run.py", "wikidata_lockout.py"]


def test_the_bot_agent_carries_emmas_bot_contact():
    assert bot_identity.BOT_CONTACT == "benthicthoughts@gmail.com"
    assert bot_identity.BOT_CONTACT in bot_identity.BOT_USER_AGENT


def test_the_bot_agent_identifies_the_tool_and_links_the_source():
    """Wikimedia asks for tool, source and contact. All three or it is not compliant."""
    agent = bot_identity.BOT_USER_AGENT
    assert "genimerge-bot" in agent
    assert "github.com/EmmaLeonhart/geni" in agent
    assert "@" in agent


def test_the_lockout_check_uses_the_same_constant_not_a_copy():
    assert wikidata_lockout.BOT_USER_AGENT is bot_identity.BOT_USER_AGENT


def test_no_bot_script_hand_writes_an_agent_string():
    """The defect was two hand-written strings, so this is what must not come back.

    A source check on purpose: `wikidata-edit-run.py` has a hyphen and is awkward to
    import, and the property worth asserting is that the literal is not there at all.
    """
    for name in BOT_SCRIPTS:
        text = (SCRIPTS / name).read_text(encoding="utf-8")
        assert "BOT_USER_AGENT" in text, f"{name} does not use the shared agent"
        assert '"genimerge-bot/0.1 (' not in text, (
            f"{name} hand-writes a User-Agent again; import BOT_USER_AGENT instead")


def test_every_agent_in_the_repo_uses_the_same_contact():
    """Emma, 2026-08-18: *"Just use the BenthicThoughts one, please!"*

    An earlier version of this test pinned `contact@emmaleonhart.com` and
    `emma@topazcomputing.com` onto the read-only agents, on my reasoning that she had
    named the CI/CD bot specifically. That was my judgement, not her instruction, and
    writing it into a test made it durable. She was explicit: *"No email is better than
    the Topaz computing one. Just use the BenthicThoughts one."* One address, everywhere.
    """
    for agent in (wikidata.USER_AGENT, wikilabels.USER_AGENT,
                  bot_identity.BOT_USER_AGENT):
        assert bot_identity.BOT_CONTACT in agent, agent
        assert "topazcomputing.com" not in agent, agent
