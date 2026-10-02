"""One uncapped QuickStatements batch of every relationship our tree gives between our items.

    PYTHONPATH=src python scripts/build-uncapped-relationships.py

Ruled 2026-10-02 (Emma): *"after it is done we create an uncapped quickstatements thing on all
relationships between all individuals that we run. Which will ideally fix the problem we had
earlier where the universe does not properly expand"*.

Creation builds a new person's relationships, but the edit-universe gate drops every link to a
relative outside the universe, so those links were never sent and the universe never grew past
them. This batch sends them. No universe gate and no cap.

**Scope.** A statement is written when one end is one of our items (`reports/garborg-qids.tsv`,
everything the account created or edited) and the other end is any item our data identifies:
the ledger, the `P2600` roster (`out/wikidata/p2600-all.tsv`, Geni ids that point at exactly one
item) or the `P2889` roster through the person's FamilySearch id. Father, mother, spouse, child
and sibling, both directions. A sibling is anyone sharing a father or a mother (Emma,
2026-10-02, on the source backfill: *"I think the change is the problem"*).

**Skipped:** a statement Wikidata already holds (`out/wikidata/relations.tsv`, plus
`reports/garborg-live-values.tsv` for our own items, which is fresher), and any statement a
person removed (`suppressed-statements.tsv`, `removed-statements.tsv`,
`relationship-corrections.csv`), in both directions, so a removal is never re-asserted.

Every line carries its source: `S2600` when Geni gives the link, `S2889` when only FamilySearch
does, both when both do (`reports/derived-family-sources.csv`).

Writes `reports/wikidata-relationships-uncapped.txt`.
"""

from __future__ import annotations

import collections
import csv
import gzip
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LEDGER = REPO / "reports" / "garborg-qids.tsv"
LIVE = REPO / "reports" / "garborg-live-values.tsv"
FAMILY = REPO / "reports" / "derived-family.csv"
SOURCES = REPO / "reports" / "derived-family-sources.csv"
P2600_ALL = REPO / "out" / "wikidata" / "p2600-all.tsv"
P2889_ALL = REPO / "out" / "wikidata" / "p2889-all.tsv"
RELATIONS = REPO / "out" / "wikidata" / "relations.tsv"
SUPPRESSED = REPO / "reports" / "suppressed-statements.tsv"
REMOVED = REPO / "reports" / "removed-statements.tsv"
CORRECTIONS = REPO / "reports" / "relationship-corrections.csv"
OUT = REPO / "reports" / "wikidata-relationships-uncapped.txt"

TAB = "\t"
NL = "\n"
#: property -> the `derived-family-sources.csv` relation that states it, from the subject's side
RELATION_OF = {"P22": "father", "P25": "mother", "P26": "spouse", "P40": "child"}
#: The same link read from the other end: `a P22 b` is `b P40 a`.
INVERSE = {"P22": ("P40",), "P25": ("P40",), "P40": ("P22", "P25"), "P26": ("P26",),
           "P3373": ("P3373",)}


def qs(value: str) -> str:
    """A QuickStatements V1 string: it has no escape for a double quote, so the quote goes."""
    return (value or "").replace('"', "").strip()


def open_family():
    if FAMILY.exists():
        return FAMILY.open(encoding="utf-8", newline="")
    return io.TextIOWrapper(gzip.open(str(FAMILY) + ".gz"), encoding="utf-8")


def split_ids(cell):
    """`derived-family.csv` separates with ` | `, spaces included."""
    return [s for s in (cell or "").replace("|", " ").split() if s]


def read_tsv(path, delimiter=TAB):
    if not path.exists():
        print(f"WARNING: {path.relative_to(REPO)} missing")
        return []
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=delimiter))


def identities():
    """`(ours, geni_to_qid)`: our items as `{qid: geni}`, and every Geni id we can place."""
    ours = {}
    geni_to_qid = {}
    for row in read_tsv(LEDGER):
        q, g = (row.get("qid") or "").strip(), (row.get("geni_id") or "").strip()
        if q.startswith("Q") and g:
            ours[q] = g
            geni_to_qid.setdefault(g, set()).add(q)
    roster = collections.defaultdict(set)
    with open(P2600_ALL, encoding="utf-8", newline="") as fh:
        for line in fh:
            parts = line.rstrip("\n").split(TAB)
            if len(parts) >= 2 and parts[0].startswith("Q"):
                roster[parts[1]].add(parts[0])
    for g, qids in roster.items():
        geni_to_qid.setdefault(g, set()).update(qids)
    # A Geni id on two items is a duplicate on Wikidata; linking either would pick one at random.
    placed = {g: next(iter(q)) for g, q in geni_to_qid.items() if len(q) == 1}
    ambiguous = len(geni_to_qid) - len(placed)
    return ours, placed, ambiguous


def read_sources():
    links, fs_ids = {}, {}
    for row in read_tsv(SOURCES, delimiter=","):
        if row["relation"] == "fs_id":
            fs_ids.setdefault(row["geni_id"], row["relative"])
        else:
            links[(row["geni_id"], row["relation"], row["relative"])] = row["source"]
    return links, fs_ids


def fs_roster():
    """`{FamilySearch id: qid}` for ids on exactly one item."""
    seen = collections.defaultdict(set)
    if P2889_ALL.exists():
        with open(P2889_ALL, encoding="utf-8", newline="") as fh:
            for line in fh:
                parts = line.rstrip("\n").split(TAB)
                if len(parts) >= 2 and parts[0].startswith("Q"):
                    seen[parts[1]].add(parts[0])
    return {f: next(iter(q)) for f, q in seen.items() if len(q) == 1}


def existing():
    """`{(qid, property, value)}` Wikidata holds today."""
    have = set()
    if RELATIONS.exists():
        with open(RELATIONS, encoding="utf-8", newline="") as fh:
            header = fh.readline().rstrip("\n").split(TAB)
            props = [h.upper() for h in header]
            for line in fh:
                parts = line.rstrip("\n").split(TAB)
                q = parts[0]
                for i in range(1, min(len(parts), len(props))):
                    if props[i] in INVERSE:
                        for v in parts[i].split(";"):
                            if v:
                                have.add((q, props[i], v))
    for row in read_tsv(LIVE):
        if row.get("property") in INVERSE:
            have.add((row["qid"], row["property"], row["value"]))
    return have


def removed():
    """Statements a person took off, blocked in both directions."""
    out = set()
    for path, delim in ((SUPPRESSED, TAB), (REMOVED, TAB)):
        for row in read_tsv(path, delimiter=delim):
            out.add((row["qid"], row["property"], row["value"]))
    for row in read_tsv(CORRECTIONS, delimiter=","):
        out.add((row["qid"], row["property"], row["value_qid"]))
    for qid, prop, value in list(out):
        if value.startswith("Q"):
            for back in INVERSE.get(prop, ()):
                out.add((value, back, qid))
    return out


#: ⛔ **UNCAPPED FOR THE UNIVERSE AND ITS RING, NOT FOR EVERYTHING. Ruled 2026-10-02 (Emma):**
#: *"it was supposed to be an uncapped thing for relationships within our universe and from our
#: universe to other things. It was supposed to be uncapped for the ring, not just for
#: everything."* The first build (`d12c26ab2`) took any ledger row as an anchor and had no
#: universe gate; its run was stopped at 731 edits.
EDIT_UNIVERSE = REPO / "out" / "wikidata" / "edit-universe.json"


def scope(ours_rows):
    """`(members, ring)`.

    Members: the composer's universe, plus every item the account edited (the ledger, without
    its entry-point rows, which name items nobody edited). A statement needs one end a member;
    the other end is then one step beyond by the link itself. Ring (the composer's one-step set
    and what Wikidata already links to a member) is returned for reporting only.
    """
    import json
    d = json.loads(EDIT_UNIVERSE.read_text(encoding="utf-8"))
    # ⛔ The universe is the CONNECTED subgraph (Emma, 2026-10-02: "It has to be connected to our
    # universe lol not just we edited it"). An edited item that is not connected is not a member:
    # `Q272148` (Æthelbald of Mercia, carrying the Wessex Æthelbald's Geni id) was one.
    members = set(d.get("universe") or ())
    ring = set(d.get("one_step") or ())
    with open(RELATIONS, encoding="utf-8", newline="") as fh:
        fh.readline()
        for line in fh:
            parts = line.rstrip(NL).split(TAB)
            linked = {v for cell in parts[1:6] for v in cell.split(";") if v}
            if parts[0] in members:
                ring |= linked
            elif linked & members:
                ring.add(parts[0])
    return members, ring - members


def main() -> int:
    csv.field_size_limit(1 << 30)
    ours, placed, ambiguous = identities()
    members, ring = scope([(r["qid"].strip(), r.get("note") or "") for r in read_tsv(LEDGER)
                           if (r.get("qid") or "").startswith("Q")])
    print(f"scope: {len(members):,} members, {len(ring):,} in the ring")
    links, fs_ids = read_sources()
    by_fs = fs_roster()
    print(f"our items: {len(ours):,}; Geni ids placed on one item: {len(placed):,} "
          f"({ambiguous:,} on two or more items, skipped)")

    def qid_of(g):
        q = placed.get(g)
        if q:
            return q
        f = fs_ids.get(g)
        return by_fs.get(f) if f else None

    father, mother = {}, {}
    pairs = []  # (subject geni, property, value geni)
    with open_family() as fh:
        for row in csv.DictReader(fh):
            g = row["geni_id"]
            dad, mum = (row.get("father") or "").strip(), (row.get("mother") or "").strip()
            if dad:
                father[g] = dad
                pairs.append((g, "P22", dad))
                pairs.append((dad, "P40", g))
            if mum:
                mother[g] = mum
                pairs.append((g, "P25", mum))
                pairs.append((mum, "P40", g))
            for s in split_ids(row.get("spouses")):
                pairs.append((g, "P26", s))
                pairs.append((s, "P26", g))
            for c in split_ids(row.get("children")):
                pairs.append((g, "P40", c))
                # the child's own row carries the P22/P25 side; which parent it is is known there
    by_parent = collections.defaultdict(set)
    for kid, p in father.items():
        by_parent[("F", p)].add(kid)
    for kid, p in mother.items():
        by_parent[("M", p)].add(kid)
    sib_parents = collections.defaultdict(set)  # (a, b) -> {("F"|"M", parent)}
    for key, kids in by_parent.items():
        if len(kids) < 2:
            continue
        for a in kids:
            for b in kids:
                if a != b:
                    sib_parents[(a, b)].add(key)
    for (a, b) in sib_parents:
        pairs.append((a, "P3373", b))
    print(f"relationships in our tree, both directions: {len(pairs):,}")

    def source(a, prop, b):
        if prop == "P3373":
            kinds = set()
            for side, p in sib_parents[(a, b)]:
                rel = "father" if side == "F" else "mother"
                kinds.add(links.get((a, rel, p), "geni"))
                kinds.add(links.get((b, rel, p), "geni"))
            src = "fs" if kinds == {"fs"} else ("both" if "fs" in kinds or "both" in kinds else "geni")
        else:
            src = links.get((a, RELATION_OF[prop], b))
            if src is None and prop in ("P22", "P25"):
                src = links.get((b, "child", a))
            if src is None and prop == "P40":
                src = links.get((b, "father", a)) or links.get((b, "mother", a))
            src = src or "geni"
        ref = ""
        if src in ("geni", "both"):
            ref += f'{TAB}S2600{TAB}"{qs(a)}"'
        fs_id = fs_ids.get(a) or fs_ids.get(b, "")
        if src in ("fs", "both") and fs_id:
            ref += f'{TAB}S2889{TAB}"{qs(fs_id)}"'
        if src == "fs" and not fs_id:
            ref = f'{TAB}S2600{TAB}"{qs(a)}"'
        return ref

    have = existing()
    blocked = removed()
    counts = collections.Counter()
    lines, seen = [], set()
    for a, prop, b in pairs:
        qa, qb = qid_of(a), qid_of(b)
        if not qa or not qb:
            counts["an end has no item"] += 1
            continue
        if qa == qb:
            counts["both ends are one item"] += 1
            continue
        # The other end is a relative of a member, so one step beyond it by this very link.
        if qa not in members and qb not in members:
            counts["outside the universe and its ring"] += 1
            continue
        key = (qa, prop, qb)
        if key in seen:
            continue
        seen.add(key)
        if key in have:
            counts["Wikidata already holds it"] += 1
            continue
        if key in blocked:
            counts["a person removed it"] += 1
            continue
        counts[f"written {prop}"] += 1
        lines.append((qa, prop, qb, f"{qa}{TAB}{prop}{TAB}{qb}{source(a, prop, b)}"))

    lines.sort(key=lambda r: (r[0][0], int(r[0][1:]), r[1], int(r[2][1:])))
    header = [
        "# Every relationship our tree gives inside the universe and its ring, both directions,",
        "# uncapped inside that scope. Emma, 2026-10-02.",
        "# Skips what Wikidata already holds and anything a person removed.",
    ]
    OUT.write_text(NL.join(header + [r[3] for r in lines]) + NL, encoding="utf-8", newline=NL)
    for k, v in sorted(counts.items()):
        print(f"   {k}: {v:,}")
    print(f"{len(lines):,} statements on {len({r[0] for r in lines}):,} items -> "
          f"{OUT.relative_to(REPO)}")
    print(f"items outside our ledger touched: {len({r[0] for r in lines} - set(ours)):,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
