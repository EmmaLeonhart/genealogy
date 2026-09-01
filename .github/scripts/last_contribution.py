"""How long ago Emma last edited Wikidata, so a workflow can decide whether to do real work.

    python .github/scripts/last_contribution.py            # prints hours, e.g. 2.4
    python .github/scripts/last_contribution.py --max 6    # also exits 0/1 on the threshold

**Emma's design, 2026-09-01:** *"Every six hours it checks the time of my last contribution. If it
is under six hours old then it does the full pipeline. Ledger refresh plus quickstatement rebuild.
So basically it is intended as facilitating potentially quite intensive work like this."*

**The gate is the point.** The pipeline it guards checks out ~5.7 GB and rebuilds the batch; run
unconditionally every six hours that is four expensive runs a day whether or not anything changed.
Her contributions are the signal that something *has* changed, because the ledger is built from
them — `scripts/refresh-garborg-ledger.py` reads the same `list=usercontribs` for the same account.

**One request, no authentication.** `usercontribs` with `uclimit=1` returns her most recent edit
and nothing else.

**It fails OPEN, and that is deliberate.** If Wikidata cannot be reached the age is unknown, and
the useful default is to run the pipeline rather than skip it: a wasted run costs minutes of free
Actions time, a skipped run means she wakes to a stale batch. The reason is printed either way.
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
import urllib.parse
import urllib.request

API = "https://www.wikidata.org/w/api.php"
ACCOUNT = "日巫女"
AGENT = "genimerge pipeline gate (emma@topazcomputing.com)"


def hours_since_last_edit():
    """`(hours, iso timestamp)`, or `(None, reason)` when it cannot be established."""
    q = urllib.parse.urlencode({
        "action": "query", "list": "usercontribs", "ucuser": ACCOUNT,
        "uclimit": "1", "ucprop": "timestamp", "format": "json"})
    try:
        req = urllib.request.Request(API + "?" + q, headers={"User-Agent": AGENT})
        with urllib.request.urlopen(req, timeout=60) as fh:
            data = json.loads(fh.read().decode("utf-8"))
    except Exception as exc:                                        # noqa: BLE001
        return None, f"could not reach Wikidata: {exc}"
    edits = (data.get("query") or {}).get("usercontribs") or []
    if not edits:
        return None, f"no contributions found for {ACCOUNT}"
    stamp = edits[0].get("timestamp")
    if not stamp:
        return None, "contribution carried no timestamp"
    when = datetime.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)
    return (now - when).total_seconds() / 3600.0, stamp


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--max", type=float,
                    help="exit 0 if the last edit is newer than this many hours, else 1")
    args = ap.parse_args()

    hours, detail = hours_since_last_edit()
    if hours is None:
        # Fail open: unknown is treated as recent, because a wasted run is cheaper than a
        # stale batch waiting for her in the morning.
        print(f"unknown ({detail}) -- treating as recent")
        print("hours=unknown")
        return 0
    print(f"last edit {detail}, {hours:.1f} hours ago")
    print(f"hours={hours:.1f}")
    if args.max is None:
        return 0
    if hours <= args.max:
        print(f"within {args.max}h -- run the pipeline")
        return 0
    print(f"older than {args.max}h -- nothing to do")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
