"""The unconnected-`P2600` worklist: who to try next, in a deterministic order.

    PYTHONPATH=src python scripts/build-unconnected-worklist.py

`docs/unconnected-worklist.md` is the specification. This is pieces 2 through 5 of it —
neighbourhood size, the four columns, the date carry-forward, and the ordering.

Piece 6 — the date being WRITTEN on every attempt — is `scripts/attempt_ledger.py`, called from
`scripts/write-family-scrape.py` once per person the collector runs on. It edits the one field in
place and leaves the ordering alone, because the ordering is this script's and CI runs it after
the tree build.

## ⛔ WHAT IS STATE AND WHAT IS NOT. THE WHOLE ALGORITHM IN FOUR LINES

Ruled 2026-09-10, verbatim: *"This entire algorithm is completely stateless except for the actual
connectivity graph of which it is built off of, and the dates of attempts."*

    the connectivity graph   built from the GEDCOMs in `exports/`, every run, from scratch
    last_attempted           carried from the previous file by `load_previous`. THE ONLY
                             THING CARRIED. It cannot be recovered from anything else.
    everything else          recomputed, or a placeholder rewritten on every build

**An attempt produces exactly two things**, and neither of them is a flag somebody sets:

    a GEDCOM file that exists in `exports/`, or does not
    a date in this file

So *"has this person been exported?"* is answered by looking for the file, and *"what are their
statistics?"* by scraping them again. Neither is stored, because storing them would make this
file authoritative for something it cannot verify.

**Membership needs no state either** (§ 3): a person who gets connected simply stops being
generated into the file. Nothing marks them done, and nothing has to.

A `load_extras` that carried the six placeholder columns across a rebuild was written and removed
on 2026-09-10. It looked like protecting data from a from-scratch rewrite and was really the
introduction of state.

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

## THE GRAPH: THE MERGED TREE IF YOU HAVE ONE, THE UNION-FIND STAND-IN OTHERWISE

    --tree out/union.ged     measure on the merged tree, which is what the spec asks for
    (default)                the union-find over the three edge sources

The specification says the neighbourhood is measured **in the synoptic tree**, after Wikidata's
tree has been merged into it as a GEDCOM — *"the syntactic tree now has a canonical form that is
natively a Gedcom because that means that it preserves the family ids."*

**That tree now exists and it BUILDS ON A RUNNER**, measured 2026-09-09 in
`.github/workflows/union-tree.yml`: 3,038,219 people, 1,961,091 families, 516 MB, peak RSS
**9.76 GB of 16**, 18m38s. `--tree` reads it and the family ids survive, which is the one thing
the GEDCOM form is for.

**The stand-in stays, and is still the default**, because the merged tree is not committed —
it is 516 MB — so a run without one has to answer the same question from the three tracked
sources. The two agree on membership and component size by construction: the same edges, counted
the same way. What the stand-in cannot do is keep a `FAM` id.

⛔ **A SPOUSE EDGE COUNTS IN BOTH.** Every member of a `FAM` — `HUSB`, `WIFE` and every `CHIL` —
lands in one component. `CLAUDE.md` § *BOTH TIES, ALWAYS*: in-law connections are just as valid,
blood is not required, and this measures connection to the main graph rather than descent.
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

#: Charlemagne, by Geni id. `CLAUDE.md` § *Always write the English label next to an ID*,
#: and the anchor protocol pins this one: it is NOT the viewer's profile.
CHARLEMAGNE_GENI = "6000000002457013227"

#: A failure costs one attempt and 30 days. Not a guess: the graph shifts underneath these
#: people as tiny edges from other captures land, so a retry is worth something later and
#: nothing immediately.
COOLDOWN = datetime.timedelta(days=30)

#: Placeholder seeds, stated as placeholders in the spec.
SEED_ATTEMPTED = "2026-09-01"
SEED_NEVER = "2026-01-01"

NL = chr(10)
TAB = chr(9)


def sizes_from_tree(path, uf):
    """Union every `FAM`'s members together, straight off a merged GEDCOM.

    ⛔ **ONE PASS, AND IT UNIONS ON THE XREF RATHER THAN THE PRIMARY KEY.** A `FAM` can name an
    `INDI` defined later in the file, so resolving members to Geni ids as they are read would
    need a second pass or a held map of three million people. Union-find does not care what the
    nodes are called: the component sizes are identical whatever the labels, and only the
    HOLDERS have to be findable afterwards — which is what `by_geni` is for.

    Returns `(by_geni, node_of_charlemagne)`: Geni id -> xref, and the xref Charlemagne sits on.

    **`RFN geni:<id>` is the primary key** — `CLAUDE.md` § *The Geni profile ID is the primary
    key for everything*. A Wikidata-only person carries `REFN Q<digits>` instead and is a
    routing node: it has no Geni id, it is never a worklist row, and it still carries edges,
    which is the entire reason the overlay exists.
    """
    by_geni = {}
    charlemagne = None
    current = None
    members = []
    kind = ""

    def flush():
        if kind == "FAM" and len(members) > 1:
            first = uf.node(members[0])
            for other in members[1:]:
                uf.join(first, uf.node(other))

    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("0 "):
                flush()
                members = []
                parts = line.split()
                current = parts[1].strip("@") if len(parts) > 2 else None
                kind = parts[2].strip() if len(parts) > 2 else ""
                if kind == "INDI" and current:
                    uf.node(current)          # a person with no family is a component of one
            elif kind == "INDI" and line.startswith("1 RFN geni:"):
                gid = line[len("1 RFN geni:"):].strip()
                if gid:
                    by_geni[gid] = current
                    if gid == CHARLEMAGNE_GENI:
                        charlemagne = current
            elif kind == "FAM" and line[:1] == "1" and line[2:6] in ("HUSB", "WIFE", "CHIL"):
                ref = line[6:].strip().strip("@")
                if ref:
                    members.append(ref)
    flush()
    return by_geni, charlemagne


def eligible_on(last):
    """The date a row becomes eligible again: its attempt plus the 30-day cooldown.

    An unparseable date sorts first rather than crashing the run: the column is written by the
    collector pipe and a malformed value must not be able to stop the whole file being built.
    """
    try:
        return datetime.date.fromisoformat(last) + COOLDOWN
    except ValueError:
        return datetime.date.min


def sort_key(row, today):
    """§ 7 of the spec, as one total key — `CLAUDE.md` § *SORTING MUST BE DETERMINISTIC*.

    ELIGIBLE block first; the ineligible below it ordered by WHEN THEY BECOME ELIGIBLE. Within
    either block, neighbourhood size DESCENDING then qid ASCENDING. Every component is a number,
    a date or a string, so the same rows produce the same bytes on any machine.
    """
    qid, _gid, size, last = row
    when = eligible_on(last)
    ready = when <= today
    return (0 if ready else 1, datetime.date.min if ready else when, -int(size), qid)


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


#: The five statistics figures plus the export flag, carried across a rebuild.
STATS_COLUMNS = ["family_tree", "blood_relatives", "ancestors", "descendants", "followers"]
EXTRA_COLUMNS = STATS_COLUMNS + ["exported"]
#: ⛔ 200, DELIBERATELY. The export gate fires at 250, so a placeholder of 200 flags NOBODY.
#: Ruled 2026-09-10: *"list the statistics of everyone in the tsv as 200 and not exported. That
#: way it will not flag anyone to be exported but we have placeholder data."*
#:
#: ⛔⛔ **AND THE REBUILD PRESERVES ONLY THE DATES.** *"The CI/CD thing that builds the
#: connectivity tree and as a result rebuilds a TSV file every single run, it only preserves the
#: dates ... This entire algorithm is completely stateless except for the actual connectivity
#: graph of which it is built off of, and the dates of attempts."*
#:
#: So these six are rewritten as placeholders on every build and are NOT carried forward. A
#: `load_extras` that carried them was written on 2026-09-10 and removed the same day: it made
#: the file hold state, and the state it held was answerable without it. Whether an export
#: exists is answered by whether the GEDCOM exists in `exports/`; what a person's statistics are
#: is answered by scraping them again. Only `last_attempted` is genuinely unrecoverable, which
#: is why it is the one thing `load_previous` carries.
PLACEHOLDER = ["200"] * len(STATS_COLUMNS) + ["no"]


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
    ap.add_argument("--tree", default="",
                    help="a merged GEDCOM to measure the neighbourhood ON, which is what the spec asks for. Without it the union-find stand-in over the three tracked sources is used and answers the same question.")
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

    if args.tree:
        # ⛔ THE SPEC'S OWN GRAPH. The holders still come from `p2600-all.tsv` -- that file is
        # the fusion, this QID is that Geni profile, and the tree carries the edges rather than
        # the identification.
        print("holders from p2600-all.tsv ...", flush=True)
        holders = {}
        with open(ROOT / "out/wikidata/p2600-all.tsv", encoding="utf-8") as fh:
            for line in fh:
                parts = line.rstrip(NL).split(TAB)
                if len(parts) >= 2 and parts[0].strip() and parts[1].strip():
                    holders.setdefault(parts[1].strip(), set()).add(parts[0].strip())
        print("%s ..." % args.tree, flush=True)
        by_geni, charlemagne = sizes_from_tree(args.tree, uf)
        print("%d people keyed on a Geni id in the tree" % len(by_geni), flush=True)
        if charlemagne is None:
            print("⛔ Charlemagne is not in %s -- refusing to write a worklist" % args.tree)
            return 1
        root = uf.find(uf.id[charlemagne])
        lookup = lambda gid: uf.id.get(by_geni.get(gid, ""))      # noqa: E731
    else:
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
        lookup = lambda gid: uf.id.get("g:" + gid)                # noqa: E731

    # ⛔ NEIGHBOURHOOD SIZE IS THE COMPONENT SIZE, and the union-find already carries it:
    # `size[root]` is maintained by union-by-size on every join, so no second pass is needed.
    sizes = {}
    for gid in holders:
        node = lookup(gid)
        sizes[gid] = uf.size[uf.find(node)] if node is not None else 1

    previous = load_previous(pathlib.Path(args.out))
    attempted = attempted_geni_ids(ISOLATES)

    rows = []
    for gid, qids in holders.items():
        node = lookup(gid)
        if node is not None and uf.find(node) == root:
            continue                      # connected -- not in the file, and never stored
        last = previous.get(gid) or (SEED_ATTEMPTED if gid in attempted else SEED_NEVER)
        rows.append((sorted(qids)[0], gid, sizes.get(gid, 1), last))

    # ELIGIBLE block first; then the ineligible, ordered by when they become eligible.
    # Within either: neighbourhood size DESCENDING, then qid ASCENDING. `sort_key` at module
    # level, so the test suite pins the order rather than a closure nothing can reach.
    rows.sort(key=lambda r: sort_key(r, today))
    ready = sum(1 for r in rows if eligible_on(r[3]) <= today)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline=NL) as fh:
        fh.write(TAB.join(["qid", "geni_id", "neighbourhood_size", "last_attempted"]
                          + EXTRA_COLUMNS) + NL)
        for qid, gid, size, last in rows:
            fh.write(TAB.join([qid, gid, str(size), last]
                              + PLACEHOLDER) + NL)

    print("%d P2600 holders; %d DISCONNECTED -> %s" % (len(holders), len(rows), out))
    print("  eligible now                 %7d" % ready)
    print("  waiting out the 30-day cooldown %4d" % (len(rows) - ready))
    print("  dates carried forward from the previous file: %d" % len(previous))
    if rows:
        print("  top of the file: %s  neighbourhood %d" % (rows[0][0], rows[0][2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
