"""The shortest relationship path between two people, walked over OUR OWN tree.

    python scripts/path-between.py <geni_id_a> <geni_id_b> [-o paths/name.tsv]

**Emma, 2026-08-26:** *"I'd be interested in whether there is a link between Arne and Bureus
that we could potentially follow and add… You have the ability to go into the browser, find
these, save them, and figure it out."*

**The browser is not needed when both ends are already in the corpus.** `genimerge path-from-html`
exists because a Geni relationship path names people *no export has reached* — that is its whole
value, and `CLAUDE.md` says so. But when both endpoints and the people between them are already
here, the answer is a breadth-first walk over `reports/derived-family.csv` and costs nothing.
Save a page only if this returns no path.

**Edges are parent, child and spouse**, which is what a Geni relationship path traverses — its
relation column reads *"her brother"*, *"his partner"*, *"her husband"*, and `CLAUDE.md` records
an export style being chosen because a stretch of path crossed exactly those.

**Every step reports whether that person holds a Wikidata item**, from the same ledger the daily
batch uses — `reports/garborg-qids.tsv` plus her hand-asserted identifications — because
the question behind this is what would have to be *created* to make the line continuous.

Writes a TSV in the shape `genimerge path` consumes, so a found path joins the same machinery as
the saved ones.
"""
from __future__ import annotations

import argparse
import collections
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

FAMILY = ROOT / "reports" / "derived-family.csv"
LABELS = ROOT / "reports" / "derived-labels.csv"


def split(cell):
    """` | ` is the separator and the strip is load-bearing -- `CLAUDE.md`."""
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def ledger():
    out = {}
    with open(ROOT / "reports" / "garborg-qids.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row.get("qid"):
                out[row["geni_id"]] = row["qid"]
    return out


def p2600_map():
    """Geni ids that already carry a `P2600` on some Wikidata item."""
    out = {}
    path = ROOT / "out" / "wikidata" / "p2600-all.tsv"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 2 and parts[1].isdigit():
                    out.setdefault(parts[1], parts[0])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("-o", "--out", default="", metavar="TSV")
    ap.add_argument("--avoid", action="append", default=[], metavar="WORD",
                    help="skip anyone whose label contains WORD, case-insensitively; "
                         "repeatable. The endpoints are always kept.")
    args = ap.parse_args()

    # **`--avoid` is a routing constraint, not a filter on the answer.** Emma, 2026-08-29:
    # *"I want a path to be added from Arne to Signe (adding from Arne to Signe) that does not
    # go through any Borsheim"*. Breadth-first returns *a* shortest path and there is usually
    # more than one; excluding people up front makes the walk find a different route rather
    # than reporting failure on the route it happened to pick first.
    #
    # It matches on the LABEL, which is a name test — the one thing this repo refuses almost
    # everywhere. It is safe here for the same reason the zipper's name step is: nothing is
    # being *identified* by name. A name only decides which edges the walk may use, and the
    # result is then checked step by step against the tree. A wrong exclusion loses a route;
    # it can never merge two people.
    avoid_words = [w.casefold() for w in args.avoid]
    avoided = set()
    if avoid_words:
        with open(LABELS, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                lab = ((row.get("label_en") or "") + " "
                       + (row.get("label_mul") or "")).casefold()
                if any(w in lab for w in avoid_words):
                    avoided.add(row["geni_id"])
        avoided -= {args.a, args.b}
        print(f"avoiding {len(avoided):,} people whose label carries "
              f"{' or '.join(args.avoid)}")

    adj = collections.defaultdict(set)
    with open(FAMILY, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g = row["geni_id"]
            for col in ("father", "mother", "children", "spouses"):
                for other in split(row.get(col)):
                    adj[g].add(other)
                    adj[other].add(g)
    print(f"{len(adj):,} people in the graph")
    for who in (args.a, args.b):
        if who not in adj:
            sys.exit(f"{who} is not in reports/derived-family.csv at all -- "
                     f"that is an absent person, not an absent path")

    # Breadth-first, so the first path found is a shortest one.
    prev, seen = {}, {args.a} | avoided
    queue = collections.deque([args.a])
    while queue and args.b not in seen:
        cur = queue.popleft()
        for nxt in sorted(adj[cur]):
            if nxt not in seen:
                seen.add(nxt)
                prev[nxt] = cur
                queue.append(nxt)
    if args.b not in seen:
        sys.exit(f"no path between {args.a} and {args.b} over parent/child/spouse edges"
                 + (f" avoiding {' or '.join(args.avoid)}" if args.avoid else "")
                 + f". {len(seen):,} people were reachable from the first, so the walk ran -- "
                 f"they are in different components.")

    chain = [args.b]
    while chain[-1] != args.a:
        chain.append(prev[chain[-1]])
    chain.reverse()

    labels = {}
    with open(LABELS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in set(chain):
                labels[row["geni_id"]] = (row.get("label_en")
                                          or row.get("label_mul") or "")
    have, p2600 = ledger(), p2600_map()

    print(f"\n{len(chain)} steps, {len(chain) - 2} people between them\n")
    missing = 0
    rows = []
    for i, g in enumerate(chain, 1):
        qid = have.get(g) or p2600.get(g) or ""
        if not qid:
            missing += 1
        print(f"  {i:>3}  {labels.get(g, '')[:42]:<42} {g:<20} {qid or '— no item'}")
        rows.append({"step": i, "name": labels.get(g, ""), "relation": "",
                     "note": f"geni:{g}", "qid": qid})
    print(f"\n{missing} of {len(chain)} hold no Wikidata item -- those are the creations "
          f"that would make the line continuous.")

    if args.out:
        dest = ROOT / args.out
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="") as f:
            f.write(f"# Relationship path over OUR OWN tree: {labels.get(args.a, args.a)} "
                    f"-> {labels.get(args.b, args.b)}\n")
            f.write("# Generated by scripts/path-between.py, breadth-first over "
                    "reports/derived-family.csv. NOT a saved Geni page: every person on it\n"
                    "# is already in the corpus, which is why no browser was needed.\n")
            w = csv.DictWriter(f, fieldnames=["step", "name", "relation", "note", "qid"],
                               delimiter="\t")
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {dest.resolve().relative_to(ROOT)}")


if __name__ == "__main__":
    main()
