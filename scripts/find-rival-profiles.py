"""Find people we created on Wikidata who are RIVALS of an item that already existed.

The duplicate guard in build-garborg-day.py keys on P2600 (Geni.com profile ID).
An item with no P2600 is therefore invisible to it, and that is how
Q110302791 and Q5588874 came to be duplicated by items of ours -- neither
carries a P2600 and neither Geni id appears anywhere in p2600-all.tsv.

This looks for the shape directly, entirely offline against out/wikidata/:
a ledger item of ours and some OTHER store item share a neighbour
(a parent, or a child) and carry the same label.  Those are the pairs Emma
would otherwise have to merge by hand.
"""
import collections
import csv
import io
import re
import sys

LEDGER = "reports/garborg-qids.tsv"
LIVE = "reports/garborg-live-values.tsv"
RELATIONS = "out/wikidata/relations.tsv"
LABELS = "out/wikidata/labels.tsv"
OUT = "reports/rival-profiles.tsv"


def rows(path):
    with io.open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            yield row


def norm(label):
    """Fold for comparison only.  Diacritics are NOT folded -- CLAUDE.md is
    explicit that a diacritic makes a different name."""
    return re.sub(r"\s+", " ", (label or "")).strip().casefold()


# labels.tsv is qid, en, mul, no, nb, sv, da, aliases, ids.  A person is the
# same person whichever of those a label happens to sit in, so every one of
# them is a candidate form and the comparison is set-against-set.  Taking the
# whole tail of the line instead is how the first run of this script reported
# zero pairs: it compared "NN			...	P1819=..." against "NN".
LABEL_COLS = 7


def main():
    ours, minted = {}, set()
    for r in rows(LEDGER):
        if not r.get("qid"):
            continue
        ours[r["qid"]] = r.get("label") or ""
        # An item Emma merely added a P2600 to was already on Wikidata, so it
        # cannot be a rival WE created.  The question is about the ones this
        # programme minted.  The store snapshot predates almost all of them,
        # so absence from relations.tsv is the offline discriminator; the
        # note column catches the rest.
        if "added to an existing item" not in (r.get("note") or ""):
            minted.add(r["qid"])

    # our side of the graph, from the values we already hold offline
    kin = collections.defaultdict(set)   # our qid -> neighbour qids
    for r in rows(LIVE):
        if r["property"] in ("P22", "P25", "P40") and r["value"].startswith("Q"):
            kin[r["qid"]].add(r["value"])

    watch = set(ours) | {n for v in kin.values() for n in v}

    # everything in the store adjacent to a watched item
    adj = collections.defaultdict(set)   # neighbour -> other items touching it
    has_p2600 = set()
    preexisting = set()                  # every qid in the store snapshot
    with io.open(RELATIONS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            q = r["qid"]
            near = set()
            for col in ("p22", "p25", "p40"):
                for v in (r.get(col) or "").split():
                    if v.startswith("Q"):
                        near.add(v)
            preexisting.add(q)
            hit = near & watch
            if q in watch or hit:
                if (r.get("p2600") or "").strip():
                    has_p2600.add(q)
            for n in hit:
                adj[n].add(q)
            if q in watch:
                for n in near:
                    adj[n].add(q)

    want = set()
    for q, neighbours in kin.items():
        for n in neighbours:
            want |= adj.get(n, set())
    want |= set(ours)

    label = {}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        next(fh, None)
        for line in fh:
            parts = line.rstrip(chr(10)).split(chr(9))
            if parts and parts[0] in want:
                label.setdefault(parts[0], [c for c in parts[1:LABEL_COLS] if c])

    # everything in the store existed before we minted anything
    minted -= {q for q in minted if q in preexisting}

    found = []
    for q, neighbours in sorted(kin.items()):
        if q not in minted:
            continue
        mine = {norm(f) for f in ([ours.get(q) or ""] + list(label.get(q, []))) if norm(f)}
        if not mine:
            continue
        for n in sorted(neighbours):
            for other in sorted(adj.get(n, set())):
                if other == q or other in ours:
                    continue
                theirs = {norm(f) for f in label.get(other, []) if norm(f)}
                shared = mine & theirs
                if not shared:
                    continue
                found.append({
                    "ours": q,
                    "label": ours.get(q) or (label.get(q) or [""])[0],
                    "rival": other,
                    "rival_label": " | ".join(label.get(other, [])),
                    "matched_on": sorted(shared)[0],
                    "shared_neighbour": n,
                    "rival_has_p2600": "yes" if other in has_p2600 else "no",
                })

    seen, uniq = set(), []
    for row in found:
        key = (row["ours"], row["rival"])
        if key not in seen:
            seen.add(key)
            uniq.append(row)

    cols = ["ours", "label", "rival", "rival_label", "matched_on",
            "shared_neighbour", "rival_has_p2600"]
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(uniq)

    blind = [r for r in uniq if r["rival_has_p2600"] == "no"]
    print("ledger items:", len(ours), " minted by us:", len(minted), " with kin:", len(kin))
    print("rival pairs:", len(uniq), " of which the guard was BLIND to:", len(blind))
    for r in blind[:15]:
        print("  {ours} == {rival}  {label!r}  via {shared_neighbour}".format(**r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
