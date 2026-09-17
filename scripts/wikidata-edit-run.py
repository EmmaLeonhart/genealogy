"""Execute a reviewed batch of Wikidata edits through the bot-password account.

**Dry run is the default.** `--live` is required to send anything, and even then
the run is capped by `--limit` and refuses a batch that is not the reviewed file
committed to the repo.

Credentials come from the environment — `USERNAME`, `BOT_NAME` and
`BOT_PASSWORD`, all three GitHub Actions secrets, named for what exists in the
repo's secret store. A bot-password login name is
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
`genimerge.editorder` now supplies the order, as designed: a random pick from
whatever is currently runnable.

**A batch whose prerequisites live in another file refuses rather than half-running.**
Three do — `wikidata-mul-labels.json` needs `wikidata-en-labels.json` (14,972 times),
and the Samaritan succession and Abram fix need `wikidata-samaritan-links.json`. The
refusal names the file that provides what is missing, and `--satisfied` accepts a
list of ids already applied so a resumed run is not blocked by work that is done.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
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

#: The stated cadence was 10-100 edits a day; the ceiling has been doubled with every
#: other batch size in the repo -- 100 -> 200 on 2026-09-05, 200 -> 400 on 2026-09-07, the
#: daily batch being twice as large in everything it does. A run may never exceed
#: it however it is invoked, and it has to keep pace with the batch it sends or a doubled
#: batch simply arrives truncated.
MAX_EDITS_PER_RUN = 400

#: A live run may only execute a batch that is committed and reviewable. Anything
#: generated on the fly is a dry run at best.
REVIEWED_BATCHES = {
    "out/wikidata/unlinked-items.json",
    "out/wikidata/priority-chain.json",
    "out/wikidata/edits.json",
    # The daily Garborg batch: the thing that starts running by itself on the 15th,
    # sent through the bot-password API. It qualifies as reviewed on the same terms
    # as the others -- it is
    # committed to the repo by the pipeline and published on the site every day,
    # so what runs is a file that has been readable for as long as it existed.
    "reports/wikidata-garborg-day.txt",
    # ⛔ THE TWO HALVES OF THAT FILE, AND LEAVING THEM OUT COST EVERY EDIT THE PROJECT EVER SENT.
    # `scripts/split-daily-batch.py` cut the daily batch into an AUTO half the schedule sends and
    # a MANUAL half the Pages site publishes for a person to paste -- ruled 2026-09-14, "a third
    # of that to be run by cicd". The split updated `DAILY_BATCH` in wikidata-edits.yml and
    # neither of the two other places that name the batch: the workflow's sparse-checkout, and
    # this set. So the first live morning failed twice over, and 2026-09-16 08:23 still read
    # "refusing a live run on reports/wikidata-garborg-day-auto.txt: not one of the reviewed
    # batches" after the checkout half was fixed.
    #
    # They qualify on exactly the terms the whole file does, and no others: each is a SUBSET of
    # `wikidata-garborg-day.txt` cut by a committed script, committed by the pipeline, and
    # published on the site. Nothing is in a half that was not in the reviewed whole.
    "reports/wikidata-garborg-day-auto.txt",
    "reports/wikidata-garborg-day-manual.txt",
}

#: Printed when EVERY failure in a run is `permissiondenied`. That combination is diagnostic and
#: the old message was not: a run that logged in and took a CSRF token has good credentials and an
#: unblocked account, so what is missing is a GRANT -- and grants belong to the bot password, not
#: to the account, and are fixed at the moment the password is created.
#: ⛔ THE RUNNER'S IP IS THE PROBLEM, NOT THE CREDENTIAL. Measured 2026-09-17 off the
#: 2026-09-16 13:25 run: `whoami` reported the session BLOCKED with
#: *"Open proxy/Webhost ... <!-- Microsoft Azure -->"*, while `edit`, `createpage` and
#: `item-term` were all held. GitHub-hosted runners are Azure and Wikimedia blocks those ranges
#: on sight, so a scheduled run cannot write however the bot password is configured.
BLOCK_HINT = (
    "",
    "  THE SESSION IS BLOCKED. This is not the bot password and not the batch.",
    "",
    "  Wikimedia blocks open proxies and webhosts, and GitHub-hosted runners are Microsoft",
    "  Azure, so every scheduled run edits from a blocked address. Three ways out:",
    "",
    "    IP block exemption   ask on Wikidata for `ipblock-exempt` on the bot account;",
    "                         it is the normal remedy for a bot on cloud infrastructure",
    "    run it off Actions   a self-hosted runner, or send the batch from the machine that",
    "                         already edits Wikidata by hand",
    "    do nothing           the batch keeps composing and waits; nothing is lost, and the",
    "                         Pages site still publishes the half a person pastes",
    "",
)


PERMISSION_HINT = (
    "",
    "  Every failure is permissiondenied and the login succeeded, so this is the bot",
    "  password's GRANTS -- not the batch, and not the account. At Special:BotPasswords",
    "  the bot needs at minimum:",
    "      Edit existing pages           labels, descriptions, aliases, statements",
    "      Create, edit, and move pages  the CREATE lines that mint name items",
    "  Grants cannot be added to an existing bot password: it means generating a NEW one",
    "  and putting it in the BOT_PASSWORD secret. See docs/wikidata-bot.md.",
)

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

    def whoami(self) -> dict:
        """What this SESSION may actually do, which is not what the account may do.

        A bot-password session holds the INTERSECTION of the account's rights and the grants
        ticked on that password, so `meta=userinfo` is the only thing that settles an argument
        about whether a `permissiondenied` is the credential, the account or the grant. Asking
        costs one GET and it is the difference between a diagnosis and a guess.
        """
        return self._call(action="query", meta="userinfo",
                          uiprop="groups|rights|blockinfo")["query"]["userinfo"]

    def claims(self, qid: str) -> dict:
        """The item's existing statements, `{property: [claim, ...]}`. Empty on any failure.

        Read before every statement edit. See `plan_attachments`.
        """
        try:
            res = self._call(action="wbgetclaims", entity=qid)
        except Exception:
            return {}
        return res.get("claims") or {}

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
        plans = []
        if edit["kind"] == "create":
            params = {"action": "wbeditentity", "token": token, "maxlag": "5",
                      "new": "item",
                      "data": json.dumps(data, ensure_ascii=False)}
        else:
            # One extra GET per statement edit, and it is what stops a qualifier turning into
            # a duplicate statement. See `plan_attachments`.
            if data.get("claims"):
                plans = plan_attachments(data, self.claims(edit["qid"]))
            params = {"action": "wbeditentity", "token": token, "maxlag": "5",
                      "id": edit["qid"],
                      "data": json.dumps(data, ensure_ascii=False)}
            # EVERY CLAIM ALREADY HELD MEANS THERE IS NOTHING TO wbeditentity. Sending the
            # empty payload anyway is a null edit that still spends a write, and it would
            # report the object as changed when the change is entirely in the attachments.
            if not any(k in data for k in ("claims", "labels", "aliases",
                                           "descriptions", "sitelinks")):
                for plan in plans:
                    self.attach(plan, token, delay=delay)
                return edit["qid"]

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
        for plan in plans:
            self.attach(plan, token, delay=delay)
        time.sleep(delay)
        return qid

    def attach(self, plan: dict, token: str, *, delay: float) -> None:
        """Put one statement's qualifiers and references on it BY GUID.

        `wbsetqualifier` and `wbsetreference` add; they cannot replace the set, which is the
        whole reason the attachment does not ride along in the `wbeditentity` payload. See
        `plan_attachments`.

        **No `summary`.** `CLAUDE.md` § *NO descriptions and NO edit summaries* covers the API
        path explicitly, and it covers these two calls as much as the object write.
        """
        for qprop, snaks in (plan.get("qualifiers") or {}).items():
            for snak in snaks:
                post = {"claim": plan["guid"], "property": qprop,
                        "snaktype": snak.get("snaktype", "value"), "token": token}
                if post["snaktype"] == "value":
                    post["value"] = json.dumps((snak.get("datavalue") or {}).get("value"),
                                               ensure_ascii=False)
                self._attach_call("wbsetqualifier", post, delay)
        for ref in plan.get("references") or []:
            self._attach_call("wbsetreference", {
                "statement": plan["guid"],
                "snaks": json.dumps(ref.get("snaks") or {}, ensure_ascii=False),
                "token": token,
            }, delay)

    def _attach_call(self, action: str, post: dict, delay: float) -> None:
        res = self._call(action=action, _post={**post, "bot": "1"})
        err = res.get("error")
        if err and not is_already_present(err.get("info") or ""):
            raise EditFailed(f"{action}: {err.get('code')}: {err.get('info')}")
        time.sleep(delay)


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


def snak_key(snak: dict):
    """A comparable value for a mainsnak, or None when there is nothing to compare.

    `wikibase-entityid` is compared on the id and everything else on the datavalue, which is
    what makes `P2600 "6000000009968757483"` match whatever shape the item stores it in.
    """
    if snak.get("snaktype") != "value":
        return None
    dv = (snak.get("datavalue") or {}).get("value")
    if isinstance(dv, dict):
        return dv.get("id") or dv.get("time") or json.dumps(dv, sort_keys=True)
    return dv


#: Wikidata refuses a qualifier or a reference that the statement already carries, and the
#: refusal is a SUCCESS: the thing we wanted on the statement is on the statement. Vendored
#: from `shintowiki-scripts/modern-quickstatements/direct_daily_edits.py`, which measured it
#: on its 2026-09-12 run -- **23 of 26 reported failures were this** and only 3 were real.
#: A run that reports 26 failures when it has 3 trains everyone to ignore the number.
#:
#: Matched on the message rather than the code because `modification-failed` covers genuinely
#: different refusals too; this text is the specific one.
_ALREADY_PRESENT = ("already a qualifier with hash", "already a reference with hash")


def is_already_present(info: str) -> bool:
    """True when Wikidata's refusal means *this is already on the statement*."""
    text = (info or "").lower()
    return any(marker in text for marker in _ALREADY_PRESENT)


def plan_attachments(data: dict, existing: dict) -> list:
    """Take every outgoing claim the item ALREADY holds out of the payload, and return the
    qualifiers and references to attach to those statements by GUID instead.

    WITHOUT THIS, A QUALIFIER MAKES A DUPLICATE STATEMENT. Reported 2026-09-16 from an item
    carrying `P2600 6000000009968757483` **twice** -- once bare and once qualified `subject
    named as "Heinrich VI von Plauen III"` -- both written by this pipeline. Emma: *"it didn't
    add a qualifier it just added a full duplicate property"*.

    The cause is `wbeditentity` semantics. A claim object with no `id` is a NEW statement,
    always; the API has no notion that a statement with the same mainsnak is "the same one".

    AND THE FIX IS NOT TO SET THE CLAIM ID AND SEND THE MERGED SET. That was written here on
    2026-09-16 and it is the wrong mechanism, which is the half Emma pointed at: *"there's logic
    in shintowiki-scripts that was intentionally added to implement this that you didn't do"*.
    `wbeditentity` on a claim carrying an `id` REPLACES that claim's whole qualifier and
    reference set. Reconstructing the set from a live read makes every write depend on that read
    being complete and current -- and a human qualifier added between the read and the write is
    silently deleted, against `CLAUDE.md` § *The purpose is to ADD, not to correct*.

    `wbsetqualifier` and `wbsetreference` cannot do that. They take a statement GUID and one
    thing to put on it, so the operation is additive BY CONSTRUCTION rather than by our
    arithmetic being right. That is the logic `direct_daily_edits.execute_line` uses, and its
    file register says so in as many words: *"A qualifier-bearing line makes execute_line find
    the existing claim and add to it rather than create a second one."*

    VENDORED, NOT COUPLED. `CLAUDE.md` records a session that invented a shared lockout between
    the two repos and would have blocked editing this repo is entitled to do -- *"I think you
    hallucinated a coordination between them"*. So the shape is copied and nothing is imported,
    fetched or shared: no runtime dependency, no shared state, no network call.

    Returns ``[{"guid", "qualifiers", "references"}, ...]``, carrying only what the live
    statement does not already hold. `data["claims"]` is left holding the genuinely new
    statements, and is removed entirely when none remain.
    """
    def ref_key(ref):
        return {pp: [snak_key(x) for x in sn]
                for pp, sn in (ref.get("snaks") or {}).items()}

    plans = []
    keep = []
    for claim in data.get("claims") or []:
        prop = claim.get("mainsnak", {}).get("property")
        want = snak_key(claim.get("mainsnak") or {})
        live = None
        if prop and want is not None:
            for candidate in existing.get(prop) or []:
                if snak_key(candidate.get("mainsnak") or {}) == want:
                    live = candidate
                    break
        if live is None:
            # A value the item does not hold is a NEW statement, qualifiers and all, and one
            # `wbeditentity` writes it whole. A DIFFERENT GENI ID IS A DIFFERENT STATEMENT --
            # `CLAUDE.md` § *A second Geni ID on one item is NOT a conflict*.
            keep.append(claim)
            continue

        held = {k: {snak_key(x) for x in v}
                for k, v in (live.get("qualifiers") or {}).items()}
        quals = {}
        for qprop, snaks in (claim.get("qualifiers") or {}).items():
            fresh = [x for x in snaks if snak_key(x) not in held.get(qprop, set())]
            if fresh:
                quals[qprop] = fresh

        held_refs = [ref_key(r) for r in (live.get("references") or [])]
        refs = [r for r in (claim.get("references") or []) if ref_key(r) not in held_refs]

        if quals or refs:
            plans.append({"guid": live["id"], "qualifiers": quals, "references": refs})

    if keep:
        data["claims"] = keep
    elif "claims" in data:
        del data["claims"]
    return plans


def entity_data(edit: dict, minted: dict) -> dict:
    """The `data` payload of a `wbeditentity` call for one edit object.

    **Aliases carry `add`, labels and descriptions do not**, and the asymmetry is
    load-bearing rather than tidy. `wbeditentity` REPLACES a language's alias list
    when given one plainly, and `CLAUDE.md` § *The MARRIED name is the real name*
    has every `Lmul` preceded by an `Amul` preserving whatever the item already
    read, some of which are hand-edits. A replacing alias write would
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
        # ⛔ BOTH BRANCHES ARE GATED. This one returned early for a day, which meant the gates
        # below covered the `.json` batches and not the QuickStatements ones -- and the daily
        # batch, the only thing the schedule ever sends, is `.txt`. Written while fixing the
        # third *A GUARD IN ONE EMITTER IS NOT A GUARD* of 2026-09-14 and caught by running the
        # live batch through it instead of trusting the docstring that said it was covered.
        return _gate(qs_v1.edit_objects(qs_v1.parse(path.read_text(encoding="utf-8"))), path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for key in ("edits", "items", "objects"):
            if key in data:
                data = data[key]
                break
    if not isinstance(data, list):
        raise SystemExit(f"{path}: expected a list of edit objects")
    return _gate(data, path)


def _gate(edits, path):
    """⛔ The 2026-10-01 clan-label block, applied to EVERY batch this runner reads.

    **It was implemented once and routed around once.** `build-garborg-day.py` has suppressed
    clan labels since the day it was ruled, 2026-08-29 -- but by a hardcoded list of 163 QIDs,
    and only in the batch it composes. `reports/wikidata-cjk-mul-labels.json` was committed by
    hand on 2026-09-10 and comes straight here, carrying **1,431 clan-seat labels of which none
    are among the 163**. § *A GUARD IN ONE EMITTER IS NOT A GUARD*.

    So it is applied at `load_batch`, which is the single point every batch passes through --
    `.qs`, `.txt` and `.json` alike -- and keyed on each edit's own `derived_from` rather than on
    a list of ids, because a list only covers the ids somebody remembered to add.
    """
    kept, dropped = wikidata_lockout.drop_clan_labels(edits)
    if dropped:
        _allowed, why = wikidata_lockout.clan_labels_allowed()
        print(f"{path.name}: {len(dropped)} clan-seat labels withheld - {why}")
    kept = _refuse_duplicate_people(kept, path)
    kept = _refuse_unnameable_name_items(kept, path)
    return kept


#: The ledger of people who already have a Wikidata item.
LEDGER = REPO / "reports" / "garborg-qids.tsv"


def _geni_ids_claimed(edit) -> set:
    """Every `P2600` Geni profile id this edit asserts."""
    out = set()
    for claim in edit.get("claims") or ():
        if claim.get("property") != "P2600":
            continue
        value = claim.get("value")
        raw = value.get("value") if isinstance(value, dict) else value
        if isinstance(raw, str) and raw.isdigit():
            out.add(raw)
    return out


def _refuse_duplicate_people(edits, path):
    """⛔ **NEVER CREATE A PERSON WHO ALREADY HAS AN ITEM.** The one failure that cannot be
    undone by running it correctly next time.

    `tests/test_garborg_day_batch.py::test_the_ledger_and_the_batch_do_not_both_claim_a_person`
    went red on 2026-09-14 with **all 63 of the batch's `P2600` creations already in
    `reports/garborg-qids.tsv`**. Nothing was wrong with either file: the ledger was refreshed
    by a tree rebuild AFTER the batch was composed, so the batch is creating people it did not
    know existed when it was written. `CLAUDE.md` § *The ledger refresh is PART OF THE RUN*
    describes the intended coupling; this is what it looks like when the two come apart.

    The composer can be fixed and the batch recomposed, and both should happen. This is here
    anyway because **the runner is the last thing between a stale file and Wikidata**, and a
    guard that lives only in the generator is the failure this repo has hit three times in one
    day. A batch is read from disk by a scheduled job; whatever wrote it is long gone.
    """
    if not LEDGER.exists():
        return edits
    with LEDGER.open(encoding="utf-8", newline="") as fh:
        have = {row["geni_id"] for row in csv.DictReader(fh, delimiter="	")
                if row.get("geni_id")}
    kept, refused = [], []
    for e in edits:
        if e.get("kind") == "create" and (_geni_ids_claimed(e) & have):
            refused.append(e)
        else:
            kept.append(e)
    if refused:
        ids = sorted(next(iter(_geni_ids_claimed(e))) for e in refused)
        print(f"{path.name}: {len(refused)} creations REFUSED - already on Wikidata "
              f"per {LEDGER.name}: {', '.join(ids[:5])}"
              + (" ..." if len(ids) > 5 else ""))
    return kept


def _refuse_unnameable_name_items(edits, path):
    """⛔ **A NAME ITEM WHOSE LABEL IS NOT A NAME DOES NOT GET CREATED.**

    `namemodel` gained the punctuation rule on 2026-09-14 and it works at the source. It does
    not reach a batch that was composed before it: the daily file committed at that moment had
    `(Ulf` as its FIRST creation, with `Den "family name"` under it, ready to send.

    So the same test runs here, on the label of anything being created as a name item. It is
    `namemodel`'s own function, not a copy -- § *A GUARD IN ONE EMITTER IS NOT A GUARD* means
    one rule consulted from both places, never two implementations of it.
    """
    try:
        import namemodel
    except Exception:                                # namemodel is optional to this script
        return edits
    name_item = {"Q101352", "Q202444", "Q110874", "Q12308941", "Q11879590", "Q4116295"}
    kept, refused = [], []
    for e in edits:
        label = ((e.get("labels") or {}).get("mul")
                 or (e.get("labels") or {}).get("en") or "")
        is_name_item = any(
            c.get("property") == "P31"
            and isinstance(c.get("value"), dict)
            and c["value"].get("id") in name_item
            for c in (e.get("claims") or ()))
        if e.get("kind") == "create" and is_name_item and label                 and namemodel.not_a_name(label):
            refused.append(label)
        else:
            kept.append(e)
    if refused:
        print(f"{path.name}: {len(refused)} name items REFUSED - the label is not a name: "
              + ", ".join(repr(x) for x in refused[:5])
              + (" ..." if len(refused) > 5 else ""))
    return kept


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
    # ⛔ **A THIRD OF THE BATCH IS WHAT CI/CD RUNS BY ITSELF.** Ruled 2026-09-14: *"you are
    # specifically making 50% more quickstatements and then segregating out a third of that to
    # be run by cicd"*. The caps were raised 50% the same day, so `1.5 / 3 = 0.5` -- the third
    # CI/CD takes is exactly the increase, and the hand-run keeps the volume it always had.
    #
    # A FRACTION rather than a number because the batch size moves every day and a fixed
    # `--limit 100` is a third of nothing in particular. `--limit` still applies on top as the
    # hard ceiling, so the scheduled run sends `min(third of the batch, limit)`.
    ap.add_argument("--fraction", type=float, default=None,
                    help="send at most this fraction of the batch (0 < f <= 1)")
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
    if args.fraction is not None:
        if not 0 < args.fraction <= 1:
            sys.exit(f"--fraction must be in (0, 1], got {args.fraction}")
        share = math.ceil(len(edits) * args.fraction)
        if share < limit:
            print(f"--fraction {args.fraction:.4g} of {len(edits)} edits -> {share}")
            limit = share
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

    # THE START DATE: no Wikidata edits until September 1.
    # Checked only on the LIVE path — a dry run sends nothing, so it stays useful
    # before the date. FAILS CLOSED: an unreadable date == locked.
    #
    # This used to read a lockout state file in another repo. The shintowiki
    # scripts and this one are not the same and are not coordinated; that
    # coordination was invented here rather than observed. The date is this
    # repo's own.
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

    # ⛔ SAY WHAT THE SESSION MAY DO, BEFORE TRYING TO DO IT. On 2026-09-16 a run failed five
    # times with `permissiondenied` and the honest answer to "is the secret outdated or unused?"
    # was not in the log: a successful login proves the credential works, and nothing printed
    # said whether `edit` was among the rights this session actually holds.
    info = session.whoami()
    rights = set(info.get("rights") or ())
    print("session: %s | groups: %s" % (info.get("name", "?"),
                                        ",".join(info.get("groups") or ()) or "none"))
    # ⛔ WIKIBASE HAS ITS OWN RIGHTS AND THEY ARE THE ONES THAT BITE. `edit` and `createpage`
    # are MediaWiki's and they were BOTH present on the run that failed every write, which is
    # what refuted the first diagnosis here -- "the Edit existing pages grant is missing" was
    # wrong. Wikibase adds `item-term`, `item-create`, `item-merge`, `item-redirect` and the
    # property equivalents, and a term edit checks `item-term`, not `edit`. So print both sets,
    # and print the whole list when something is missing rather than guessing which.
    # ⛔ `item-create` IS NOT ON THIS LIST AND MUST NOT GO BACK ON IT. It was, and it reported
    # NO on every run -- including the 2026-09-16 08:34 run that MINTED SIX ITEMS in the same
    # minutes (`Q141474261`, `Q141474269`, `Q141474270`, `Q141474271`, `Q141474276`,
    # `Q141474278`). Wikidata does not grant a right by that name for ordinary creation: an item
    # is created with `createpage` + `edit`, both of which are held.
    #
    # So the line was a permanent false alarm sitting next to real ones, and it was read twice
    # as "creations cannot land" when creations were landing. A check that is always NO teaches
    # the reader to discount the whole list.
    for needed in ("edit", "createpage", "item-term",
                   "item-merge", "item-redirect", "property-term"):
        print("  right %-14s %s" % (needed, "yes" if needed in rights else "NO"))
    blocked = bool(info.get("blockid"))
    if blocked:
        print("  ACCOUNT IS BLOCKED: %s" % info.get("blockreason", ""))
    # Carried to the stop message so the diagnosis there is made of what was MEASURED here
    # rather than inferred from the shape of the failures.
    globals()["_SESSION_BLOCKED"] = blocked
    globals()["_SESSION_BLOCK_REASON"] = info.get("blockreason", "")
    globals()["_SESSION_MISSING"] = [r for r in ("edit", "createpage", "item-term",
                                                 "item-merge", "item-redirect",
                                                 "property-term") if r not in rights]
    print("  all rights: %s" % " ".join(sorted(rights)))

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
            # ⛔ **`maxlag` IS BACK-PRESSURE, NOT A FAILURE, AND COUNTING IT STRANDS
            # HALF-WRITTEN PEOPLE.** Measured 2026-09-17: a run of 100 objects hit five
            # consecutive `maxlag` refusals -- the query servers were 5-7 seconds behind and
            # asked the bot to wait -- the stop below fired, and **38 objects never ran**. The
            # creations among the first 57 had already landed, so `Q141488165 Kasbar L` went
            # live asserting `P40` a child while `Q141419525` never got the reciprocal `P22`
            # that anchors him. The item floats: from the child's page he does not exist.
            #
            # Wikidata asks every bot to back off when replication lags; it clears by itself
            # and says nothing about the account, the batch or the API. The stop exists for a
            # broken credential or a block, where every edit fails for the same permanent
            # reason. Counting lag toward it turns a thirty-second wobble into an abandoned
            # run.
            #
            # `apply()` already retries maxlag four times with its own backoff, so reaching
            # here means the wobble outlasted that -- still a reason to skip this edit and
            # carry on, never a reason to abandon the ones behind it.
            if "maxlag" not in str(exc):
                consecutive += 1
            print(f"       {e['id']}  {e['kind']:<9} FAILED: {exc}", file=sys.stderr)
            # A run where everything fails is not a batch with a bad edit in it; it
            # is a broken account, a changed API or a block. Grinding through the
            # remaining edits would turn one problem into a hundred log lines.
            if consecutive >= 5:
                print(f"\nSTOPPED: {consecutive} failures in a row — this is not "
                      "about the individual edits.", file=sys.stderr)
                # NAME THE CAUSE. "this is not about the individual edits" is true and tells
                # nobody what to do. `permissiondenied` from a run that logged in and took a
                # CSRF token is never the batch: the login worked, so it is the bot password's
                # GRANTS at Special:BotPasswords, which are ticked per bot password and are not
                # the account's own rights. Seen 2026-09-16 on the first run that got as far as
                # trying to edit: five `qs-terms-*` edits, all permissiondenied.
                if failed and all("permissiondenied" in m for m in failed.values()):
                    # ⛔ **A BLOCK IS NOT A GRANT PROBLEM, AND SAYING SO SENT US TO THE WRONG
                    # PLACE.** On 2026-09-16 every edit failed `permissiondenied`, this printed
                    # the bot-password hint, and the real cause was three lines further up in
                    # the same log: the session was BLOCKED as an open proxy/webhost, commented
                    # `<!-- Microsoft Azure -->`. GitHub Actions runners are Azure, and Wikimedia
                    # blocks webhost ranges. No bot password can edit through that.
                    #
                    # The block is measured at login by `whoami`, so lead with it and do not
                    # offer the grants hint underneath, which reads as a second opinion.
                    if globals().get("_SESSION_BLOCKED"):
                        for line in BLOCK_HINT:
                            print(line, file=sys.stderr)
                        print("  the block reason: %s"
                              % globals().get("_SESSION_BLOCK_REASON", ""), file=sys.stderr)
                    else:
                        for line in PERMISSION_HINT:
                            print(line, file=sys.stderr)
                    # Separate from the block and true either way: a right the session does not
                    # hold fails that KIND of edit even once the IP problem is gone.
                    missing = globals().get("_SESSION_MISSING") or []
                    if missing:
                        print("  and separately, rights this session does NOT hold: %s"
                              % ", ".join(missing), file=sys.stderr)
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
