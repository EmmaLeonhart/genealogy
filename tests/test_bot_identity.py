"""The User-Agent is an email address and nothing else.

Emma, 2026-08-18: *"This GitHub repo shouldn't be linked into the user agent. Really,
none of this should be in the user agent. You're leaking a massive amount of information
here. It's just an email address. That is the secret."*

Every earlier version of the agent named the tool, linked
her repository, and described what the project does. All three
told a reader where the code lives and what it is for, which is the leak. What is pinned
here is that none of them can come back.

The address itself is not asserted literally: it lives in the `BOT_CONTACT` secret, and a
test that hard-codes it puts it back into the source.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"

sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(REPO / "src"))

import bot_identity  # noqa: E402
import wikidata_lockout  # noqa: E402
from genimerge import wikidata, wikilabels  # noqa: E402

AGENTS = ("bot_identity", "genimerge.wikidata", "genimerge.wikilabels")
BOT_SCRIPTS = ["wikidata-edit-run.py", "wikidata_lockout.py"]


def _agents():
    return {
        "bot_identity": bot_identity.BOT_USER_AGENT,
        "genimerge.wikidata": wikidata.USER_AGENT,
        "genimerge.wikilabels": wikilabels.USER_AGENT,
    }


def test_no_agent_links_the_repository():
    """The instruction was absolute: never, in any user agent, link the repository."""
    for name, agent in _agents().items():
        assert "github.com" not in agent, name
        assert "EmmaLeonhart" not in agent, name
        assert "geni" not in agent.lower(), name


def test_no_agent_describes_the_project():
    """A purpose string is the same leak in prose form."""
    for name, agent in _agents().items():
        for word in ("GEDCOM", "Wikidata", "reconciliation", "label", "bot", "import"):
            assert word.lower() not in agent.lower(), f"{name} leaks {word!r}"


def test_the_agent_is_exactly_the_contact_from_the_secret():
    want = os.environ.get("BOT_CONTACT", "").strip()
    for name, agent in _agents().items():
        assert agent == want, name


def test_the_agent_is_empty_rather_than_a_fallback_when_the_secret_is_absent():
    """*"No email on the user agent is fine"* -- but nothing else may take its place."""
    if not os.environ.get("BOT_CONTACT", "").strip():
        for name, agent in _agents().items():
            assert agent == "", name


def test_no_address_is_written_into_the_source():
    for rel in ["scripts/bot_identity.py", "src/genimerge/wikidata.py",
                "src/genimerge/wikilabels.py", "tests/test_bot_identity.py"]:
        text = (REPO / rel).read_text(encoding="utf-8")
        # Built at runtime so this assertion does not itself put an address in the
        # source and fail against its own file.
        for needle in ("@" + "gmail.com", "@" + "topazcomputing.com"):
            assert needle not in text, f"{rel} contains {needle}"


def test_the_bot_scripts_do_not_hand_write_an_agent():
    for name in BOT_SCRIPTS:
        text = (SCRIPTS / name).read_text(encoding="utf-8")
        assert "BOT_USER_AGENT" in text, f"{name} does not use the shared agent"
        assert '"genimerge-bot/0.1 (' not in text, f"{name} hand-writes an agent again"


def test_the_lockout_check_uses_the_same_constant():
    assert wikidata_lockout.BOT_USER_AGENT == bot_identity.BOT_USER_AGENT


def test_no_source_file_links_a_repository():
    """Emma, 2026-08-18: *"no fucking github links in it either"*.

    Not only the agent. A URL in a constant names her repositories to anyone reading the
    code, which is the same disclosure by a different route -- so the lockout state file's
    location moved into the LOCKOUT_STATE_URL secret too, and the gate fails closed
    without it.

    `.github/workflows` is a path inside this repo, not a link out to one, so the check
    is for the host rather than the string "github".
    """
    host = "github" + ".com"
    raw = "raw." + "githubusercontent.com"
    for path in sorted((REPO / "scripts").glob("*.py")) +             sorted((REPO / "src" / "genimerge").glob("*.py")):
        text = path.read_text(encoding="utf-8")
        assert host not in text, f"{path.name} links {host}"
        assert raw not in text, f"{path.name} links {raw}"
