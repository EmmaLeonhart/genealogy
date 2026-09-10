"""The unconnected-`P2600` worklist: who to try next, in a deterministic order.

    PYTHONPATH=src python scripts/build-unconnected-worklist.py

`docs/unconnected-worklist.md` is the specification. This is pieces 2 through 5 of it —
neighbourhood size, the four columns, the date carry-forward, and the ordering.

## The columns, in this order, because the order is part of the spec

    qid                 Wikidata QID
    geni_id             Geni profile id
    neighbourhood_size  the person's component in the combined Wikidata-and-Geni graph
    last_attempted      written by the extension every time it runs on somebody

## Who is in it

**Every `P2600` holder is considered**; a person is in the file only if they are **not linked to
Charlemagne**. Membership is recomputed every run and never stored, so success needs no state: a
person who gets connected simply stops being generated into the file, and the tree build is what
reports that.

## Neighbourhood size is the ranking key, and the reason is leverage

*"something in a very large neighborhood, if it gets connected, it'll just connect the entire
neighborhood and that's very good."* One number, over the **combined** graph — some of these
people are truly alone and some sit in large clusters, and the number is what separates them.

## The order

    ELIGIBLE      at the top
    INELIGIBLE    below, ordered by WHEN THEY BECOME ELIGIBLE

    within either block:  neighbourhood size DESCENDING, then qid ASCENDING

Take from the top. Eligibility is a **30-day cooldown** after an attempt: a failure costs one
attempt and the person goes to the back while the graph keeps moving underneath them.

## ⛔ THE DATES ARE CARRIED FORWARD FROM THIS FILE. THERE IS NO SECOND FILE

*"Actually I don't think we even need a separate file."* On each run the QID and Geni id are
fixed, the neighbourhood size and the membership are **recalculated**, and `last_attempted` is
**read from the previous committed version of this same file**. Seeds, explicitly placeholders:
`2026-09-01` where a path capture has been attempted, `2026-01-01` everywhere else.

## ⛔ THE GRAPH HERE IS UNION-FIND, WHICH IS A STAND-IN AND IS NOT THE SPEC

The specification says the neighbourhood is measured **in the synoptic tree**, after Wikidata's
tree has been merged into it as a GEDCOM — *"the syntactic tree now has a canonical form that is
natively a Gedcom because that means that it preserves the family IDs."* That merge does not
exist yet (`scripts/build-wikidata-gedcom.py` renders the overlay; nothing wires it in).

So this computes the same connectivity with a union-find over the same three edge sources, which
gets the membership and the component size right and **destroys the family ids**, which is the
one thing the GEDCOM form is for. Swap `component_sizes` onto the merged tree the moment it
exists; nothing else here changes.
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

OUT = ROOT / "reports" / "unconnected-p2600.tsv"
ISOLATES = ROOT / "reports" / "isolates.csv"

#: A failure costs one attempt and 30 days. Not a guess: the graph shifts underneath these
#: people as tiny edges from other captures land, so a retry is worth something later and
#: nothing immediately.
COOLDOWN = datetime.timedelta(days=30)

#: Placeholder seeds, stated as placeholders in the spec.
SEED_ATTEMPTED = "2026-09-01"
SEED_NEVER = "2026-01-01"

NL = chr(10)
TAB = chr(9)


def load_previous(path):
    """`geni_id -> last_attempted` from the previous committed version of THIS file."""
    if not path.exists():
        return {}
    out = {}
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=TAB):
            g = (row.get("geni_id") or "").strip()
            d = (row.get("last_attempted") or "").strip()
            if g and d:
                out[g] = d
    return out


def attempted_geni_ids(path):
    """Anyone a path capture has already been run on, for the seed date."""
    if not path.exists():
        return set()
    out = set()
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            if g:
                out.add(g)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="the unconnected-P2600 worklist")
    ap.add_argument("-o", "--out", default=str(OUT))
    ap.add_argument("--today", default="", help="override today, for a reproducible run")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    today = (datetime.date.fromisoformat(args.today) if args.today
             else datetime.date.today())

    # the union graph, exactly as `p2600-connectivity.py` builds it
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "conn", str(ROOT / "scripts" / "p2600-connectivity.py"))
    conn = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conn)

    uf = conn.Union()
    print("p2600-all.tsv ...", flush=True)
    holders, _ = conn.load_p2600(uf, ROOT / "out/wikidata/p2600-all.tsv")
    print("relations.tsv ...", flush=True)
    conn.load_relations(uf, ROOT / "out/wikidata/relations.tsv")
    print("derived-family.csv ...", flush=True)
    conn.load_family(uf, ROOT / "reports/derived-family.csv", "geni")

    root_key = "g:" + conn.CHARLEMAGNE_GENI
    if root_key not in uf.id:
        print("⛔ Charlemagne is not in the graph -- refusing to write a worklist")
        return 1
    root = uf.find(uf.id[root_key])

    # ⛔ NEIGHBOURHOOD SIZE IS THE COMPONENT SIZE, and the union-find already carries it:
    # `size[root]` is maintained by union-by-size on every join, so no second pass is needed.
    sizes = {}
    for gid in holders:
        node = uf.id.get("g:" + gid)
        sizes[gid] = uf.size[uf.find(node)] if node is not None else 1

    previous = load_previous(pathlib.Path(args.out))
    attempted = attempted_geni_ids(ISOLATES)

    rows = []
    for gid, qids in holders.items():
        node = uf.id.get("g:" + gid)
        if node is not None and uf.find(node) == root:
            continue                      # connected -- not in the file, and never stored
        last = previous.get(gid) or (SEED_ATTEMPTED if gid in attempted else SEED_NEVER)
        rows.append((sorted(qids)[0], gid, sizes.get(gid, 1), last))

    def eligible_on(last):
        try:
            return datetime.date.fromisoformat(last) + COOLDOWN
        except ValueError:
            return datetime.date.min

    # ELIGIBLE block first; then the ineligible, ordered by when they become eligible.
    # Within either: neighbourhood size DESCENDING, then qid ASCENDING.
    def key(r):
        qid, gid, size, last = r
        when = eligible_on(last)
        ready = when <= today
        return (0 if ready else 1, datetime.date.min if ready else when, -size, qid)

    rows.sort(key=key)
    ready = sum(1 for r in rows if eligible_on(r[3]) <= today)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline=NL) as fh:
        fh.write(TAB.join(["qid", "geni_id", "neighbourhood_size", "last_attempted"]) + NL)
        for qid, gid, size, last in rows:
            fh.write(TAB.join([qid, gid, str(size), last]) + NL)

    print("%d P2600 holders; %d DISCONNECTED -> %s" % (len(holders), len(rows), out))
    print("  eligible now                 %7d" % ready)
    print("  waiting out the 30-day cooldown %4d" % (len(rows) - ready))
    print("  dates carried forward from the previous file: %d" % len(previous))
    if rows:
        print("  top of the file: %s  neighbourhood %d" % (rows[0][0], rows[0][2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
