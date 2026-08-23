"""Execute a reviewed batch of Wikidata edits through the bot-password account.

**Dry run is the default.** `--live` is required to send anything, and even then
the run is capped by `--limit` and refuses a batch that is not the reviewed file
committed to the repo.

Credentials come from the environment — `USERNAME`, `BOT_NAME` and
`BOT_PASSWORD`, all three GitHub Actions secrets, named for what Emma actually
created in the repo's secret store. A bot-password login name is
`<account>@<botname>`, so the first two are joined with `@` to make `lgname`.
They are never read from a file, never logged, and never written anywhere. If
any is missing the run stops before touching the network.

Stdlib only, per CLAUDE.md: `urllib` covers the API.

    py scripts/wikidata-edit-run.py --batch out/wikidata/unlinked-items.json --limit 10
    py scripts/wikidata-edit-run.py --batch ... --limit 10 --live
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

import wikidata_lockout
from bot_identity import BOT_USER_AGENT
from http.cookiejar import CookieJar
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
API = os.environ.get("WIKIDATA_API", "https://www.wikidata.org/w/api.php")

#: Emma's stated cadence, CLAUDE.md-adjacent: 10-100 edits a day. A run may never
#: exceed the top of that range however it is invoked.
MAX_EDITS_PER_RUN = 100

#: A live run may only execute a batch that is committed and reviewable. Anything
#: generated on the fly is a dry run at best.
REVIEWED_BATCHES = {
    "out/wikidata/unlinked-items.json",
    "out/wikidata/priority-chain.json",
    "out/wikidata/edits.json",
}


class Session:
    """Just enough of the MediaWiki action API to log in and edit."""

    def __init__(self, api: str) -> None:
        self.api = api
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(CookieJar())
        )
        self.opener.addheaders = [
            ("User-Agent", BOT_USER_AGENT)
        ]

    def _call(self, **params) -> dict:
        params.setdefault("format", "json")
        post = params.pop("_post", None)
        if post is None:
            url = f"{self.api}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(url)
        else:
            body = urllib.parse.urlencode({**params, **post}).encode()
            req = urllib.request.Request(self.api, data=body)
        with self.opener.open(req, timeout=60) as fh:
            return json.load(fh)

    def login(self, user: str, password: str) -> None:
        tok = self._call(action="query", meta="tokens", type="login")
        token = tok["query"]["tokens"]["logintoken"]
        # The value never appears in output: only the outcome is reported.
        res = self._call(action="login", _post={
            "lgname": user, "lgpassword": password, "lgtoken": token,
        })
        result = res.get("login", {}).get("result")
        if result != "Success":
            raise SystemExit(f"login failed: {result!r} (credentials not shown)")
        print(f"logged in as {res['login'].get('lgusername', '<unknown>')}")

    def csrf(self) -> str:
        return self._call(action="query", meta="tokens")["query"]["tokens"]["csrftoken"]


def load_batch(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for key in ("edits", "items", "objects"):
            if key in data:
                data = data[key]
                break
    if not isinstance(data, list):
        raise SystemExit(f"{path}: expected a list of edit objects")
    return data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--limit", type=int, default=10)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True)
    mode.add_argument("--live", action="store_true")
    args = ap.parse_args()

    rel = Path(args.batch).as_posix()
    path = REPO / args.batch
    if not path.exists():
        raise SystemExit(f"no such batch: {path}")

    limit = max(0, min(args.limit, MAX_EDITS_PER_RUN))
    edits = load_batch(path)
    print(f"batch {rel}: {len(edits)} edit objects, limit {limit}")

    if not args.live:
        print("\nDRY RUN — nothing will be sent. First edits:\n")
        for e in edits[:limit]:
            print("  " + json.dumps(e, ensure_ascii=False)[:300])
        print(f"\n{min(limit, len(edits))} would be attempted. "
              f"Re-run with --live to execute.")
        return 0

    # THE START DATE. Emma, 2026-08-14: "no wikidata edits until September 1."
    # Checked only on the LIVE path — a dry run sends nothing, so it stays useful
    # before the date. FAILS CLOSED: an unreadable date == locked.
    #
    # This used to read a lockout state file in another repo. Emma, 2026-08-23:
    # "Shintowiki scripts and this one are not the same and not really
    # coordinated" — and she is right that the coordination was invented here
    # rather than observed. The date is this repo's own.
    allowed, why = wikidata_lockout.editing_allowed()
    if not allowed:
        print("")
        print(f"NOT YET — no live run. {why}")
        print(f"The date is scripts/wikidata_lockout.py START_DATE "
              f"({wikidata_lockout.START_DATE}).")
        return 0

    if rel not in REVIEWED_BATCHES:
        raise SystemExit(
            f"refusing a live run on {rel}: not one of the reviewed batches "
            f"({', '.join(sorted(REVIEWED_BATCHES))}). "
            "Review before execute is load-bearing — see docs/wikidata-bot.md."
        )

    account = os.environ.get("USERNAME")
    botname = os.environ.get("BOT_NAME")
    password = os.environ.get("BOT_PASSWORD")
    if not account or not botname or not password:
        raise SystemExit(
            "USERNAME / BOT_NAME / BOT_PASSWORD not in the environment. "
            "They are GitHub Actions secrets; nothing reads them from a file."
        )
    # Bot-password logins are `<account>@<botname>`. If the account secret was
    # given in that joined form already, leave it alone rather than doubling it.
    user = account if "@" in account else f"{account}@{botname}"

    session = Session(API)
    session.login(user, password)
    token = session.csrf()
    print(f"csrf token acquired; executing up to {limit} edits\n")

    done = 0
    for e in edits[:limit]:
        # The per-object shape is whatever the batch generator emits; this is the
        # single place that turns it into an API call, so it changes with the
        # generator rather than being guessed here.
        raise SystemExit(
            "the edit-object → API-call mapping is not written yet. "
            "The batch format is still NEEDS-DECISION (docs/wikidata-bot.md § "
            "Next steps); wiring it before Emma approves the sequence would be "
            "exactly the review step this script exists to enforce."
        )
    print(f"{done} edits executed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
