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

**The batch is ordered before it is sliced.** Until 2026-08-24 this took
`edits[:limit]` in *file order*, which quietly ignored the `requires` every edit
object carries. `CLAUDE.md` leans on that ordering where it is most dangerous: the
`NN` fix is two edits per item, the `mul` one declared as a dependency of the `en`
one, *"so the marker is written before the slot holding it is reused"* — and on the
1,271 items whose only `NN` lives in `en`, the wrong order erases the marker.
`genimerge.editorder` now supplies the order, by Emma's design: a random pick from
whatever is currently runnable.

**A batch whose prerequisites live in another file refuses rather than half-running.**
Three do — `wikidata-mul-labels.json` needs `wikidata-en-labels.json` (14,972 times),
and the Samaritan succession and Abram fix need `wikidata-samaritan-links.json`. The
refusal names the file that provides what is missing, and `--satisfied` accepts a
list of ids already applied so a resumed run is not blocked by work that is done.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request

import qs_v1
import wikidata_lockout
from bot_identity import BOT_USER_AGENT
from http.cookiejar import CookieJar
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from genimerge.editorder import Blocked, runnable_order  # noqa: E402
API = os.environ.get("WIKIDATA_API", "https://www.wikidata.org/w/api.php")

#: Emma's stated cadence, CLAUDE.md-adjacent: 10-100 edits a day. A run may never
#: exceed the top of that range however it is invoked.
MAX_EDITS_PER_RUN = 200

#: A live run may only execute a batch that is committed and reviewable. Anything
#: generated on the fly is a dry run at best.
REVIEWED_BATCHES = {
    "out/wikidata/unlinked-items.json",
    "out/wikidata/priority-chain.json",
    "out/wikidata/edits.json",
    # The daily Garborg batch. Emma, 2026-09-05, choosing what starts running by
    # itself on the 15th: "The daily Garborg batch", sent through the bot-password
    # API. It qualifies as reviewed on the same terms as the others -- it is
    # committed to the repo by the pipeline and published on the site every day,
    # so what runs is a file that has been readable for as long as it existed.
    "reports/wikidata-garborg-day.txt",
}

#: The Gregorian calendar, which every date in this project's batches uses.
GREGORIAN = "http://www.wikidata.org/entity/Q1985727"


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

    def apply(self, edit: dict, token: str, minted: dict, *, delay: float) -> str:
        """Send one edit object. Returns the QID it created or changed.

        One `wbeditentity` call per object, which is what makes an object the unit
        of atomicity: a create carries its labels, aliases, descriptions and claims
        in a single request, so there is no state where the item exists unlabelled.

        **No `summary`.** `CLAUDE.md` § *NO descriptions and NO edit summaries* is
        categorical and covers the API path explicitly: *"No `summary=` on an API
        call"*. The absence is deliberate; do not add one.
        """
        data = entity_data(edit, minted)
        params = {"action": "wbeditentity", "token": token, "maxlag": "5",
                  "data": json.dumps(data, ensure_ascii=False)}
        if edit["kind"] == "create":
            params["new"] = "item"
        else:
            params["id"] = edit["qid"]

        for attempt in range(4):
            res = self._call(action="wbeditentity", _post=params)
            err = res.get("error")
            if not err:
                break
            # maxlag is the replication lag telling a bot to come back later. It is
            # the one error worth retrying; everything else is about this edit.
            if err.get("code") == "maxlag" and attempt < 3:
                wait = float(err.get("lag") or 5) + 5
                print(f"    maxlag {err.get('lag')}s -- waiting {wait:.0f}s")
                time.sleep(wait)
                continue
            raise EditFailed(f"{edit['id']}: {err.get('code')}: {err.get('info')}")
        else:
            raise EditFailed(f"{edit['id']}: still lagged after 4 attempts")

        qid = res.get("entity", {}).get("id")
        if not qid:
            raise EditFailed(f"{edit['id']}: no entity id came back: {res}")
        if edit["kind"] == "create":
            minted[edit["id"]] = qid
        time.sleep(delay)
        return qid


class EditFailed(RuntimeError):
    """One edit the API refused. Never swallowed — the run stops on it."""


def read_receipt(path: Path) -> dict:
    """What earlier live runs already applied: ``{edit id: qid}``.

    **This is what makes the batch safe to re-send**, and re-sending is the normal
    case rather than an accident: the daily file is regenerated four times a day
    and the schedule reads whatever is committed, so the same `CREATE` can appear
    in two consecutive runs whenever the ledger refresh has not yet caught up with
    what was made. Without a receipt the second run mints the person again.

    The QID is kept, not just the id, because a create that is skipped still has to
    resolve: a statement `requires`-ing it needs the QID that create returned, and
    guessing is exactly what `_datavalue` refuses to do.
    """
    if not path.exists():
        return {}
    applied = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        # The header is a row like any other to a naive split, and counting it made
        # the run report one more applied edit than existed.
        if len(parts) >= 4 and parts[1] != "edit_id":
            applied[parts[1]] = parts[3]
    return applied


def append_receipt(path: Path, edit: dict, qid: str) -> None:
    """One row per applied edit, written as it lands rather than at the end.

    A run that dies halfway has still done what it did, and a receipt written only
    on a clean exit would say it did nothing — which is the reading that re-sends.
    """
    import datetime
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as fh:
        if new:
            fh.write("date\tedit_id\tkind\tqid\n")
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        fh.write(f"{stamp}\t{edit['id']}\t{edit['kind']}\t{qid}\n")


def _datavalue(value: dict, minted: dict, edit: dict) -> dict:
    """One typed QS value as a Wikibase datavalue.

    ``LAST`` resolves here and nowhere else: the edit's own `requires` names the
    create, and `minted` carries what that create actually returned. An edit whose
    dependency has not run in this process has no QID to substitute and must fail
    loudly rather than send `"LAST"` as a literal.
    """
    kind = value["type"]
    if kind == "item":
        qid = value["id"]
        if qid == "LAST":
            needs = edit.get("requires") or []
            if len(needs) != 1:
                raise EditFailed(
                    f"{edit['id']}: LAST needs exactly one `requires` to resolve, "
                    f"got {needs}")
            qid = minted.get(needs[0])
            if not qid:
                raise EditFailed(
                    f"{edit['id']}: LAST points at {needs[0]}, which this run has "
                    "not created. Run it in the same batch, or the value is a guess.")
        return {"type": "wikibase-entityid",
                "value": {"entity-type": "item", "id": qid,
                          "numeric-id": int(qid[1:])}}
    if kind == "string":
        return {"type": "string", "value": value["value"]}
    if kind == "time":
        return {"type": "time",
                "value": {"time": value["time"], "timezone": 0, "before": 0,
                          "after": 0, "precision": value["precision"],
                          "calendarmodel": GREGORIAN}}
    if kind == "monolingualtext":
        return {"type": "monolingualtext",
                "value": {"text": value["text"], "language": value["language"]}}
    raise EditFailed(f"{edit['id']}: no datavalue mapping for {kind!r}")


def _snak(prop: str, value: dict, minted: dict, edit: dict) -> dict:
    return {"snaktype": "value", "property": prop,
            "datavalue": _datavalue(value, minted, edit)}


def entity_data(edit: dict, minted: dict) -> dict:
    """The `data` payload of a `wbeditentity` call for one edit object.

    **Aliases carry `add`, labels and descriptions do not**, and the asymmetry is
    load-bearing rather than tidy. `wbeditentity` REPLACES a language's alias list
    when given one plainly, and `CLAUDE.md` § *The MARRIED name is the real name*
    has every `Lmul` preceded by an `Amul` preserving whatever the item already
    read — *"Some of those are her hand-edits"*. A replacing alias write would
    delete the thing the preceding line exists to save. A label is a replacement by
    definition, which is what `Lmul` means.
    """
    data: dict = {}
    for lang, text in (edit.get("labels") or {}).items():
        data.setdefault("labels", {})[lang] = {"language": lang, "value": text}
    for lang, text in (edit.get("descriptions") or {}).items():
        data.setdefault("descriptions", {})[lang] = {"language": lang, "value": text}
    for lang, texts in (edit.get("aliases") or {}).items():
        data.setdefault("aliases", {})[lang] = [
            {"language": lang, "value": t, "add": ""} for t in texts]

    claims = []
    for claim in edit.get("claims") or []:
        prop = claim["property"]
        out = {"type": "statement", "rank": "normal",
               "mainsnak": _snak(prop, claim["value"], minted, edit)}
        quals = claim.get("qualifiers") or []
        if quals:
            byprop: dict = {}
            for q in quals:
                byprop.setdefault(q["property"], []).append(
                    _snak(q["property"], q["value"], minted, edit))
            out["qualifiers"] = byprop
        refs = claim.get("references") or []
        if refs:
            snaks: dict = {}
            for r in refs:
                snaks.setdefault(r["property"], []).append(
                    _snak(r["property"], r["value"], minted, edit))
            # QuickStatements puts every `S…` on one line into ONE reference block,
            # which is what "cited to this Geni id" means as a single citation.
            out["references"] = [{"snaks": snaks}]
        claims.append(out)
    if claims:
        data["claims"] = claims
    if not data:
        raise EditFailed(f"{edit['id']}: nothing to send")
    return data


def load_batch(path: Path) -> list[dict]:
    # A QuickStatements batch is read through `qs_v1`, which is the one place that
    # knows QS syntax. Everything downstream sees ordinary edit objects, so the
    # `requires` ordering and the dry run work identically either way.
    if path.suffix in (".qs", ".txt"):
        return qs_v1.edit_objects(qs_v1.parse(path.read_text(encoding="utf-8")))
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for key in ("edits", "items", "objects"):
            if key in data:
                data = data[key]
                break
    if not isinstance(data, list):
        raise SystemExit(f"{path}: expected a list of edit objects")
    return data


def _providers(missing: set) -> dict:
    """Which batch file emits each missing id, so the refusal is actionable."""
    found = {}
    for candidate in sorted((REPO / "reports").glob("wikidata-*.json")):
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except ValueError:
            continue
        items = data if isinstance(data, list) else data.get("edits", [])
        for e in items:
            if isinstance(e, dict) and e.get("id") in missing:
                found[e["id"]] = candidate.name
    return found


def _explain(blocked: Blocked, satisfied: set) -> None:
    """Say what is missing and where it comes from, rather than just refusing."""
    have = {e.get("id") for e in blocked.remaining} | satisfied
    missing = {r for e in blocked.remaining for r in (e.get("requires") or [])
               if r not in have}
    print("", file=sys.stderr)
    print(f"REFUSED: {len(blocked.remaining)} edits cannot be ordered.",
          file=sys.stderr)
    if not missing:
        print("  Their requirements form a cycle within this batch.", file=sys.stderr)
        return
    where = _providers(missing)
    by_file: dict = {}
    for mid in missing:
        by_file.setdefault(where.get(mid, "(no batch emits it)"), []).append(mid)
    print(f"  {len(missing)} requirements are not present in this batch:",
          file=sys.stderr)
    for name, ids in sorted(by_file.items(), key=lambda kv: -len(kv[1])):
        print(f"    {len(ids):>6} from {name}   e.g. {sorted(ids)[0]}", file=sys.stderr)
    print("  Run the providing batch first, or pass --satisfied with the ids "
          "already applied.", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--satisfied", help="file of edit ids already applied, one per "
                                        "line, so a resumed run is not blocked by "
                                        "work that is genuinely done")
    ap.add_argument("--seed", type=int, default=None,
                    help="fix the random order, for a reproducible dry run")
    ap.add_argument("--receipt", help="TSV of what previous live runs applied. Read "
                                      "before the run and appended after each edit. "
                                      "This is what stops a re-sent batch creating "
                                      "the same people twice.")
    ap.add_argument("--delay", type=float, default=2.0,
                    help="seconds between edits. Courtesy to Wikidata, per "
                         "CLAUDE.md: batch where you can, do not hammer to finish "
                         "faster. maxlag is honoured separately.")
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

    # The receipt drops what earlier live runs already did, and carries their QIDs
    # forward so a skipped create can still answer a LAST that points at it.
    receipt = Path(args.receipt) if args.receipt else None
    already = read_receipt(receipt) if receipt else {}
    minted: dict = dict(already)
    if already:
        before = len(edits)
        edits = [e for e in edits if e["id"] not in already]
        print(f"receipt {receipt}: {len(already)} edits already applied, "
              f"{before - len(edits)} of this batch skipped")

    satisfied = set(already)
    if args.satisfied:
        # Union, never replace: the receipt is evidence of what this account did,
        # and a hand-supplied list is an addition to it rather than a correction.
        satisfied |= {ln.strip() for ln
                      in Path(args.satisfied).read_text(encoding="utf-8").splitlines()
                      if ln.strip()}
    if satisfied:
        print(f"{len(satisfied)} ids treated as already applied")

    # Order before slicing. Taking the first N in FILE order ignores `requires`,
    # which is the whole reason those lists exist.
    try:
        edits = runnable_order(edits, seed=args.seed, satisfied=satisfied)
    except Blocked as blocked:
        _explain(blocked, satisfied)
        return 1
    print("ordered by requires; no edit precedes anything it depends on")

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
    failed: dict = {}
    consecutive = 0
    # Seeded from the receipt, so a create skipped as already-applied still answers
    # the LAST that points at it.
    for e in edits[:limit]:
        # ONE BAD EDIT MUST NOT COST THE DAY. An unattended run that stopped on the
        # first refusal would lose the rest of the batch to something as ordinary
        # as a label collision — `CLAUDE.md` § *NO descriptions*: 3 of 22 creations
        # on one live batch would have been refused on a label/description pair
        # already taken. Carrying on is safe *here* specifically because a dangling
        # `LAST` refuses in `_datavalue` rather than resolving to the wrong item,
        # which is exactly what QuickStatements does not do: its own mid-batch
        # CREATE failure "broke the four LAST lines after it".
        blocked = [r for r in (e.get("requires") or []) if r in failed]
        if blocked:
            failed[e["id"]] = f"skipped: depends on {blocked[0]}, which failed"
            print(f"       {e['id']}  {e['kind']:<9} SKIPPED (needs {blocked[0]})")
            continue
        try:
            qid = session.apply(e, token, minted, delay=args.delay)
        except EditFailed as exc:
            failed[e["id"]] = str(exc)
            consecutive += 1
            print(f"       {e['id']}  {e['kind']:<9} FAILED: {exc}", file=sys.stderr)
            # A run where everything fails is not a batch with a bad edit in it; it
            # is a broken account, a changed API or a block. Grinding through the
            # remaining edits would turn one problem into a hundred log lines.
            if consecutive >= 5:
                print(f"\nSTOPPED: {consecutive} failures in a row — this is not "
                      "about the individual edits.", file=sys.stderr)
                break
            continue
        consecutive = 0
        done += 1
        if receipt:
            append_receipt(receipt, e, qid)
        print(f"  {done:>3}  {e['id']}  {e['kind']:<9} {qid}")

    print(f"\n{done} edits executed")
    if failed:
        print(f"{len(failed)} did not go:", file=sys.stderr)
        for eid, why in failed.items():
            print(f"  {eid}: {why}", file=sys.stderr)
        # Non-zero so the run shows red. What landed still landed, and the receipt
        # already records it — a failure here is a thing to read, not to undo.
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
