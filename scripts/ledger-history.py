"""Keep a dated history of the ledger, and explain every disagreement it reports.

    BOT_CONTACT=you@example.com python scripts/ledger-history.py

**Emma's queued item, in her words:** *"I think you should keep an active ledger, like a ledger
from a few times ago, with some level of history. It is going to check each QID that I have
edited: It's going to check whether this QID is a redirect... It should check the Genny IDs of
the QIDs that I've edited. It should compare the Genny IDs with the QIDs. The Genny IDs should
be saved. If anything occurs, it will run a query to find the wiki data mapping of the Genny IDs
of the QIDs and figure things out."* She also called it *"a potential concern"* and *"too much of
a tangent"* at the time, and asked for it to be queued.

**Most of it already exists and this only adds what does not.** `refresh-garborg-ledger.py`
rebuilds `reports/garborg-qids.tsv` from her contributions and calls `resolve-merged-qids.py`
in-process, so redirects are already resolved every run. What it does *not* do is keep history, or
say **why** a row disagrees — it prints `ledger=Q… live=Q…` and moves on.

**So this does two things:**

* **History.** Appends a dated snapshot of every `geni_id → qid` pair to
  `reports/ledger-history.tsv`, so a pairing that changes can be traced rather than inferred.
* **Explains disagreements.** For each Geni id where the ledger and her contributions differ, asks
  Wikidata **who currently holds that `P2600`** and whether either QID is a redirect. That is the
  *"run a query to find the wiki data mapping"* half.

**Querying is allowed now** — Emma lifted the ban on 2026-08-29: *"You are completely 100% allowed
to access wiki data to do basically any task... Just don't decide to run 5 million requests in a
minute."* This asks for at most a handful of items, batched, through the throttled client.
"""
import collections
import csv
import datetime
import io
import os
import sys
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from genimerge import wikidata                                       # noqa: E402

LEDGER = os.path.join(ROOT, "reports", "garborg-qids.tsv")
HISTORY = os.path.join(ROOT, "reports", "ledger-history.tsv")
COLS = ["seen", "geni_id", "qid", "label", "note"]


def rows():
    with io.open(LEDGER, encoding="utf-8", newline="") as fh:
        return [r for r in csv.DictReader(fh, delimiter="\t") if r.get("qid")]


def previous():
    """`{geni_id: qid}` as of the most recent snapshot, or empty on the first run."""
    if not os.path.exists(HISTORY):
        return {}, None
    seen = collections.defaultdict(dict)
    with io.open(HISTORY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            seen[r["seen"]][r["geni_id"]] = r["qid"]
    if not seen:
        return {}, None
    latest = max(seen)
    return seen[latest], latest


def main():
    today = datetime.date.today().isoformat()
    current = rows()
    before, when = previous()

    changed = [(r["geni_id"], before[r["geni_id"]], r["qid"]) for r in current
               if r["geni_id"] in before and before[r["geni_id"]] != r["qid"]]
    added = [r for r in current if r["geni_id"] not in before]

    fresh = not os.path.exists(HISTORY)
    with io.open(HISTORY, "a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", fieldnames=COLS)
        if fresh:
            w.writeheader()
        for r in current:
            w.writerow({"seen": today, "geni_id": r["geni_id"], "qid": r["qid"],
                        "label": r.get("label", ""), "note": r.get("note", "")})

    print(f"snapshot {today}: {len(current)} pairs written to {HISTORY}")
    if when:
        print(f"  against {when}: {len(added)} new, {len(changed)} changed")
    else:
        print("  first snapshot -- nothing to compare against yet")

    if not changed:
        return 0

    # **The query half.** Ask who actually holds each disputed P2600 now, and whether either
    # QID redirects. Batched into one request; the client throttles.
    ids = sorted({q for _, a, b in changed for q in (a, b)})
    print(f"\n{len(changed)} pairing(s) changed -- asking Wikidata about {len(ids)} items")
    # 1s between requests is the client's default and is the 'reasonable API
    # policies' half of her ruling; the cache lives beside the other Wikidata data.
    client = wikidata.WikidataClient(
        cache_dir=Path(ROOT) / 'out' / 'wikidata' / 'cache')
    ents = client.full_entities(ids)
    for geni_id, old, new in changed:
        def state(q):
            e = ents.get(q)
            if e is None:
                return "not returned"
            if "redirects" in e or e.get("id") not in (None, q):
                return f"REDIRECT -> {e.get('id', '?')}"
            held = [s["mainsnak"]["datavalue"]["value"]
                    for s in e.get("claims", {}).get("P2600", [])
                    if s.get("mainsnak", {}).get("datavalue")]
            return f"P2600={';'.join(held) or 'none'}"
        print(f"  {geni_id}")
        print(f"     was {old:<12} {state(old)}")
        print(f"     now {new:<12} {state(new)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
