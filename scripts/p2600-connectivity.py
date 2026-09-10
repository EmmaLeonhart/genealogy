"""Which `P2600` holders are DISCONNECTED from Charlemagne in the synoptic tree.

⛔ **THIS IS THE CAMPAIGN'S REAL POPULATION, and the file it replaces was never it.** Your
definition, 2026-09-09, asked for directly:

    "Every p2600 holder who is disconnected from Charlemagne in the synoptic tree (combination
    of our geni exports and what exists on wikidata). The idea is that all p2600 people should
    either be confirmed impossible to connect, or connected. Connection to Charlemagne is our
    proxy for connection to the main graph as Charlemagne is one of the most central people."

**What was being run instead.** `scripts/collector-worklist.py` draws its universe from a
hardcoded pair of files -- `reports/sibling-pair-worklist.tsv` and
`reports/isolate-path-pilot.tsv`, **4,360 people between them** -- and asks *"have we scraped
them?"*. There are **518,975** `P2600` rows. So the campaign was running over 0.8% of the
population, selected by which pilot roster happened to be on disk rather than by anything, and
it asked the wrong question about them: a person already connected to Charlemagne needs no
capture at all, and an unscraped person who is connected was being queued forever.

That is `CLAUDE.md` § *Do not grab the first artifact that vaguely matches* exactly. The commit
that introduced it, `491b487c`, implemented your *both ties, always* ruling correctly -- that
ruling is about **what to do per person**, and the **population** was never specified there.

**THE GRAPH IS THE UNION AND BOTH HALVES CARRY EDGES.** Not our tree, and not Wikidata: the two
fused on the Geni id, which is what "synoptic tree" means in your sentence. Three edge sources:

    reports/derived-family.csv    our Geni tree: father, mother, spouses, children
    out/wikidata/relations.tsv    Wikidata: P22 father, P25 mother, P40 child, P26 spouse,
                                  P3373 sibling
    out/wikidata/p2600-all.tsv    the FUSION: this QID is that Geni profile

**A QID WITH NO GENI ID IS STILL A NODE.** Two `P2600` people can be joined only through a
Wikidata item nobody has linked to Geni -- their shared father, say -- and dropping unlinked
QIDs would score both as disconnected. So the graph carries both node types and the fusion is an
edge rather than a merge.

**A SPOUSE EDGE COUNTS.** `CLAUDE.md` § *BOTH TIES, ALWAYS* -- "in-law connections are just as
valid blood is not required" -- so `P26` and our `spouses` column are edges like any other. This
measures connection to the main graph, which is what you said Charlemagne is a proxy for, not
descent from him.

⛔ **`derived-family.csv` SEPARATES WITH ` | `, SPACES INCLUDED, AND SPLITTING WRONG IS SILENT.**
`CLAUDE.md` § *Our side could never have two children*: a consumer that split on `,` or `;` made
379,251 people arrive childless and published a distribution that looked clean. Both halves are
needed -- splitting on `|` without stripping moved a pair count by exactly zero, which is how the
second half was found.
"""

from __future__ import annotations

import argparse
import collections
import csv
import gzip
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: Charlemagne, by id on both sides. `CLAUDE.md` § *Always write the English label next to a
#: property or item ID*, and the anchor protocol pins the Geni one: it is NOT the viewer's.
CHARLEMAGNE_GENI = "6000000002457013227"
CHARLEMAGNE_QID = "Q3044"


def split_cell(value):
    """` | ` with the spaces, per `derived-family.csv`. Strip as well -- both halves are the bug."""
    if not value:
        return ()
    return tuple(t.strip() for t in value.split("|") if t.strip())


class Union:
    """Union-find over interned string nodes. Path-halving, union by size."""

    def __init__(self):
        self.id = {}
        self.parent = []
        self.size = []

    def node(self, key):
        got = self.id.get(key)
        if got is None:
            got = len(self.parent)
            self.id[key] = got
            self.parent.append(got)
            self.size.append(1)
        return got

    def find(self, x):
        p = self.parent
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def join(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


def load_family(uf, path, note):
    """Our Geni tree. Every relationship column is an undirected edge.

    Returns the set of Geni ids this file actually holds, which is NOT the same as the set of
    interned nodes -- see `main`.
    """
    n = 0
    seen = set()
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        cols = ("father", "mother", "spouses", "children", "fathers", "mothers")
        for row in reader:
            gid = (row.get("geni_id") or "").strip()
            if not gid:
                continue
            seen.add(gid)
            a = uf.node("g:" + gid)
            for col in cols:
                for other in split_cell(row.get(col)):
                    uf.join(a, uf.node("g:" + other))
                    n += 1
            qid = (row.get("qid") or "").strip()
            if qid:
                uf.join(a, uf.node("w:" + qid))
                n += 1
            if n and n % 2000000 == 0:
                print("  %s %d edges" % (note, n), flush=True)
    return n, seen


def load_relations(uf, path):
    """Wikidata. `;`-separated values; the `p2600` column is the fusion edge."""
    n = 0
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        cols = ("p22", "p25", "p40", "p26", "p3373")
        for row in reader:
            qid = (row.get("qid") or "").strip()
            if not qid:
                continue
            a = uf.node("w:" + qid)
            for col in cols:
                raw = (row.get(col) or "").strip()
                if not raw:
                    continue
                for other in raw.split(";"):
                    other = other.strip()
                    if other:
                        uf.join(a, uf.node("w:" + other))
                        n += 1
            for gid in (row.get("p2600") or "").replace(";", " ").split():
                uf.join(a, uf.node("g:" + gid.strip()))
                n += 1
    return n


def load_p2600(uf, path):
    """qid -> geni id, the fusion, and the population the answer is about."""
    holders = {}
    n = 0
    with open(path, encoding="utf-8", newline="") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            qid, gid = parts[0].strip(), parts[1].strip()
            if not qid or not gid:
                continue
            holders.setdefault(gid, set()).add(qid)
            uf.join(uf.node("w:" + qid), uf.node("g:" + gid))
            n += 1
    return holders, n


def main() -> int:
    ap = argparse.ArgumentParser(description="P2600 holders disconnected from Charlemagne")
    ap.add_argument("-o", "--out", default="reports/p2600-disconnected.tsv")
    ap.add_argument("--summary", default="reports/p2600-connectivity.md")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    uf = Union()
    print("p2600-all.tsv ...", flush=True)
    holders, n_fuse = load_p2600(uf, ROOT / "out/wikidata/p2600-all.tsv")
    print("  %d holders, %d fusion edges" % (len(holders), n_fuse), flush=True)

    print("relations.tsv ...", flush=True)
    n_wd = load_relations(uf, ROOT / "out/wikidata/relations.tsv")
    print("  %d wikidata edges" % n_wd, flush=True)

    print("derived-family.csv ...", flush=True)
    n_geni, in_corpus = load_family(uf, ROOT / "reports/derived-family.csv", "geni")
    print("  %d geni edges over %d people" % (n_geni, len(in_corpus)), flush=True)

    print("nodes: %d" % len(uf.parent), flush=True)

    root_keys = [k for k in ("g:" + CHARLEMAGNE_GENI, "w:" + CHARLEMAGNE_QID) if k in uf.id]
    if not root_keys:
        print("⛔ CHARLEMAGNE IS IN NEITHER STORE -- refusing to report a reach rate", flush=True)
        return 1
    root = uf.find(uf.id[root_keys[0]])
    for key in root_keys[1:]:
        if uf.find(uf.id[key]) != root:
            print("⛔ Charlemagne's Geni node and QID node are in DIFFERENT components",
                  flush=True)

    connected, disconnected = [], []
    for gid, qids in holders.items():
        node = uf.id.get("g:" + gid)
        if node is not None and uf.find(node) == root:
            connected.append(gid)
        else:
            disconnected.append((gid, sorted(qids)))
    disconnected.sort()

    out = ROOT / args.out
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("geni_id\tqids\tin_our_tree\n")
        for gid, qids in disconnected:
            fh.write("%s\t%s\t%s\n" % (gid, ";".join(qids),
                                       "yes" if ("g:" + gid) in uf.id else "no"))

    total = len(holders)
    n_dis = len(disconnected)
    # ⛔ NOT `("g:" + gid) in uf.id` -- `load_p2600` interns a node for EVERY holder, so that
    # test is vacuously true and reported 266,201 of 266,201 "in our tree" on the first run.
    # `CLAUDE.md` § *Our side could never have two children*: a number about the instrument
    # rather than about the data. The corpus is `derived-family.csv` and nothing else.
    in_tree = sum(1 for gid, _ in disconnected if gid in in_corpus)
    print("\nP2600 holders            %d" % total)
    print("connected to Charlemagne %d  (%.1f%%)" % (total - n_dis, 100.0 * (total - n_dis) / total))
    print("DISCONNECTED             %d  (%.1f%%)" % (n_dis, 100.0 * n_dis / total))
    print("  of those, in our Geni corpus already: %d  (a separate component -- a PATH job)"
          % in_tree)
    print("  and absent from the corpus entirely:  %d  (never exported -- an EXPORT job)"
          % (n_dis - in_tree))
    print("\n-> %s" % out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
