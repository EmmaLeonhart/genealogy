"""`_FSFTID` -> `P2889` -> QID -> `P2600` -> geni id. The exact join, no name matching.

**The FamilySearch GEDCOM carries no Geni id at all** — measured 2026-09-21 on
`MBW7-P7H-a12-d2.ged`: 3,103 individuals, every one with `_FSFTID`, and **zero `RFN`**. So the
corpus cannot be joined directly and something has to bridge the two identifier spaces.

`P2889` *FamilySearch person ID* is that bridge, and it is a property Wikidata already holds
values for. Two exact joins:

    _FSFTID  ->  P2889  ->  QID          this script, from Wikidata
    QID      ->  P2600  ->  geni id      out/wikidata/p2600-all.tsv, 518,975 rows

⛔ **NO NAME MATCHING ANYWHERE.** `CLAUDE.md` § *The primary key*: merging is an exact join,
never fuzzy name matching. A FamilySearch person who does not resolve through `P2889` stays
unjoined and that is the correct outcome — it is not a cue to try the name.

**Scoped to the ids in one file, deliberately.** Ruled 2026-09-21: *"Just these 3,103"* rather
than a bulk pull of every `P2889` on Wikidata. So this asks about the people in hand, in
batches, and writes what came back.

Writes `reports/familysearch-qid-bridge.tsv` — `fs_id`, `qid`, `geni_id`.

Usage:
    python scripts/bridge-familysearch-qids.py [<download.ged> ...]   default: every gedcom/familysearch/*.ged
"""
from __future__ import annotations

import csv
import json

import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
#: ⛔ **THE USER-AGENT IS AN EMAIL ADDRESS AND NOTHING ELSE.** `scripts/bot_identity.py` is the
#: one definition and its rule is categorical: *"Never, in any user agent or anywhere else, link
#: the repository."* This file built its own agent carrying
#: `genealogy-repo/1.0 (<a github url>)` -- a tool name, a version, the account and the repo
#: name, every one of which tells a reader where the code lives and what it is for. That is the
#: leak `bot_identity` exists to prevent, and `tests/test_bot_identity.py` fails on the host
#: string in any script, which is how this was caught.
from bot_identity import agent                                          # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "familysearch-qid-bridge.tsv"

#: `P2889` values are asked for in batches of this many. A `VALUES` block of a few hundred is
#: one cheap query; the whole 3,103 in one go is a query long enough to be refused.
BATCH = 250

#: Between batches. Politeness is a rule here, not a courtesy -- `CLAUDE.md` § *Querying
#: Wikidata is allowed -- be polite about the rate*.
PAUSE = 1.5

ENDPOINT = "https://query.wikidata.org/sparql"




def fs_ids(path: Path) -> list[str]:
    """Every `_FSFTID` in the file, in first-seen order and deduplicated.

    Read off `_FSFTID` rather than the `REFN fs:` line the renderer adds, so this works on a
    raw `getmyancestors` file as well as a namespaced one.
    """
    seen = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\d _FSFTID (\S+)\s*$", line)
        if m:
            seen.setdefault(m.group(1), None)
    return list(seen)


def query(ids: list[str]) -> dict[str, str]:
    """`{fs_id: qid}` for the ids Wikidata knows, from one `VALUES` query."""
    values = " ".join('"%s"' % i.replace('"', "") for i in ids)
    sparql = (
        "SELECT ?fs ?item WHERE { VALUES ?fs { %s } ?item wdt:P2889 ?fs . }" % values
    )
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": sparql, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": agent(),
                                               "Accept": "application/sparql-results+json"})
    with urllib.request.urlopen(req, timeout=120) as fh:
        data = json.load(fh)
    out = {}
    for row in data["results"]["bindings"]:
        out[row["fs"]["value"]] = row["item"]["value"].rsplit("/", 1)[-1]
    return out


def live_anchors() -> dict[str, tuple[str, str]]:
    """`{fs_id: (qid, geni_id)}` for every item on Wikidata carrying BOTH `P2889` and `P2600`.

    One query, ~13,000 rows in ~11 seconds, measured 2026-09-24. These are the zipper's anchors
    and the local store cannot supply them: it predates the items this campaign creates, which
    is how `Q141223907` Elly Olivia Frisk -- both ids stated -- bridged to nothing. Asking for
    every `P2889` holder instead (34,920) runs past the service's timeout and returns a
    silently TRUNCATED file, so the join is done on the server and only the pairs come back.
    """
    sparql = "SELECT ?item ?fs ?g WHERE { ?item wdt:P2889 ?fs ; wdt:P2600 ?g . }"
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": sparql, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": agent(),
                                               "Accept": "application/sparql-results+json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as fh:
            data = json.load(fh)
    except Exception as exc:                                            # noqa: BLE001
        print(f"  live anchors: FAILED {exc} -- carrying on with what is on disk")
        return {}
    out = {}
    for row in data["results"]["bindings"]:
        out.setdefault(row["fs"]["value"], (row["item"]["value"].rsplit("/", 1)[-1],
                                            row["g"]["value"]))
    print(f"  {len(out):,} items on Wikidata state both a FamilySearch and a Geni id")
    return out


def store_p2889() -> dict[str, str]:
    """`{fs_id: qid}` for every item in the local store (`wikidata/items/`) carrying `P2889`.

    The items this campaign already touched are in the store, and they are exactly the ones
    most likely to carry an id we or someone before us published. One pass, no network.
    """
    import gzip
    out = {}
    for shard in sorted((ROOT / "wikidata" / "items").glob("items-*.jsonl.gz")):
        with gzip.open(shard, "rt", encoding="utf-8") as fh:
            for line in fh:
                if '"P2889"' not in line:
                    continue
                e = json.loads(line)
                for st in (e.get("claims") or {}).get("P2889", ()):
                    v = (st.get("mainsnak") or {}).get("datavalue", {}).get("value")
                    if isinstance(v, str):
                        out.setdefault(v, e.get("id", ""))
    return out


def geni_by_qid() -> dict[str, str]:
    """QID -> geni id, from BOTH stores, the way `build-garborg-day.ledger` does.

    ⛔ **`p2600-all.tsv` ALONE IS NOT THE LEDGER.** The first version of this read only the
    master correspondence and reported `Q141493478` -- Inger Axelsdatter Güntersberg, the
    person this export is rooted on and the first of the two `PRIORITY_ANCESTOR_SEEDS` -- as
    reaching no geni id, while `reports/garborg-qids.tsv` pairs her with
    `6000000000757999620` perfectly well. `ledger()` in `build-garborg-day.py` folds the two
    together for exactly this reason: the ledger knows about items carrying no `P2600` on
    Wikidata yet, which is the shape of everything this campaign has created.

    The master wins where both hold a value, because it is what Wikidata actually states.
    """
    out = {}
    ledger = ROOT / "reports" / "garborg-qids.tsv"
    if ledger.exists():
        with open(ledger, encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                q = (row.get("qid") or "").strip()
                g = (row.get("geni_id") or "").strip()
                if q.startswith("Q") and g:
                    out.setdefault(q, g)
    path = ROOT / "out" / "wikidata" / "p2600-all.tsv"
    if not path.exists():
        sys.exit(f"{path.relative_to(ROOT)} is missing; it is the second hop of the join.")
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[0].startswith("Q"):
                out[parts[0]] = parts[1]
    return out


def main() -> int:
    # ⛔ **EVERY DOWNLOAD, INTO ONE BRIDGE.** It took one file and rewrote the bridge from it,
    # so bridging the owner's tree would have erased Inger's eleven. With no argument it reads
    # every raw download in `gedcom/familysearch/`, which is what `tree.yml` runs.
    srcs = [Path(a) for a in sys.argv[1:]] or sorted(
        p for p in (ROOT / "gedcom" / "familysearch").glob("*.ged") if "-test" not in p.stem)
    dst = OUT

    ids = list(dict.fromkeys(i for src in srcs for i in fs_ids(src)))
    print(f"{len(ids):,} distinct FamilySearch ids in {', '.join(s.name for s in srcs)}")

    # ⛔ **A FAILED QUERY MUST NOT ERASE A KNOWN ANSWER.** On 2026-09-24 the query service
    # answered every batch 429 (*"1 req / min ... during active wdqs outage"*) and the rewrite
    # replaced a bridge of 11 with one of 0. What was resolved before is kept.
    found = {}
    if dst.exists():
        with open(dst, encoding="utf-8", newline="") as fh:
            found = {r["fs_id"]: r["qid"] for r in csv.DictReader(fh, delimiter="\t")
                     if r.get("qid")}
    # The local store first: every item we hold that carries `P2889`, offline, no rate limit.
    idset = set(ids)
    found.update({fs: q for fs, q in store_p2889().items() if fs in idset})
    live = {fs: qg for fs, qg in live_anchors().items() if fs in idset}
    found.update({fs: q for fs, (q, _g) in live.items()})
    print(f"  {len(found):,} resolved from the previous bridge, the local store and the live anchors")

    todo = [i for i in ids if i not in found]
    for i in range(0, len(todo), BATCH):
        chunk = todo[i:i + BATCH]
        try:
            got = query(chunk)
        except Exception as exc:                                        # noqa: BLE001
            # Reported and the rest skipped: a rate-limited service is not asked 100 more
            # times, and the unasked ids are simply unresolved, the state they were in.
            print(f"  batch {i // BATCH + 1}: FAILED {exc} -- stopping the live queries")
            break
        found.update(got)
        print(f"  {min(i + BATCH, len(todo))}/{len(todo)} asked live, {len(found)} matched",
              flush=True)
        if i + BATCH < len(todo):
            time.sleep(PAUSE)

    geni = geni_by_qid()
    for q, g in live.values():
        geni.setdefault(q, g)
    rows = []
    for fs in ids:
        qid = found.get(fs, "")
        rows.append({"fs_id": fs, "qid": qid, "geni_id": geni.get(qid, "") if qid else ""})

    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["fs_id", "qid", "geni_id"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    with_qid = sum(1 for r in rows if r["qid"])
    with_geni = sum(1 for r in rows if r["geni_id"])
    print(f"\n  {len(rows):,} FamilySearch people")
    print(f"  {with_qid:,} resolve to a QID via P2889")
    print(f"  {with_geni:,} reach a geni id, and those are the ones that FUSE with the corpus")
    print(f"  -> {dst.relative_to(ROOT) if dst.is_relative_to(ROOT) else dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
