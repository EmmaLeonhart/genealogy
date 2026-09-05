"""The chain of justifications behind every zipper pair, walked both ways.

    python scripts/zipper-provenance.py [GENI_ID ...]

**Emma, 2026-08-25:** *"providence is important in this, and ideally, a zipper merge will almost
always be done with there being a relatively large chain of providence, not just a simple 'this
was the justification,' but a potentially very large series of justifications."*

And the reason her own verdicts exist: *"That is the actual reason why I asked you to record my
manual decisions, because of the fact that they entered into the province too."*

`reports/zipper-pairs.tsv` records **one step** — the slot, the method, the pair it hung off, and
the evidence. That is a link. This walks the links into the chain: a round-6 pair's justification
is its own step plus every step beneath it, all the way down to a Wikidata-stated `P2600`
*Geni.com profile ID* or to a verdict Emma gave by hand.

## Both directions, which is the part she was explicit about

**Support propagates upward from an independent resolution.** *"suddenly you go into the ancestors
and you notice that somebody connected one of the ancestors. There's an entity resolution on one
of the ancestors from our side... This supports it extremely well, and it actually supports it
down the entire chain."*

**Contradiction propagates identically.** *"if you end up in a situation where there's an entity
resolution that clearly contradicts it, this indicates a clear contradiction... it goes both
ways."*

So every pair the zipper inferred is checked against every *independent* correspondence this repo
holds -- Emma's About Me links, her hand identifications, the structural walk, the Izumo and Tanba
rosters, and her hand verdicts. An independent source that **agrees** is corroboration; one that
**disagrees** is a contradiction. Neither is applied only to the pair itself: both are pushed
along the chain, because a chain is only as good as the step it rests on.

## What "poisoned" means, and why it is not "deleted"

A pair whose chain passes through a contradicted step is marked `POISONED`. That is a **reading**,
not a deletion: `CLAUDE.md` is emphatic that the question is whether our snapshot matches Geni,
never whether Geni is right, and Emma's own standard for stopping the join is high --
*"we need a pretty damn good reason to stop it... This reasoning requires something pretty good."*
So nothing is dropped here. The marking exists so that the reason is visible.

Writes `reports/zipper-provenance.tsv` (one row per pair, with chain depth, root, and status) and
`reports/zipper-provenance-chains.md` (the full chains for the contradicted ones, plus any Geni
ids named on the command line).
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "reports"

#: Correspondences that do NOT come from the zipper, so they can corroborate or refute it.
#: `wikidata-p2600` is deliberately absent: the join already refuses to contradict a recorded
#: identifier (those land in `zipper-conflicts.tsv`), so it can only ever agree here.
INDEPENDENT = (
    ("emma-hand-verdict", R / "emma-judgments.tsv", "qid", "geni_id", "\t"),
    ("geni-about-me", R / "geni-qid-links.tsv", "qids", "geni_id", "\t"),
    ("structural-walk", R / "structural-correspondence.csv", "qid", "geni_id", ","),
    ("geni-wikidata-pairs", R / "geni-wikidata-pairs.csv", "qid", "geni_id", ","),
    ("izumo-roster", R / "izumo-p2600-pairs.tsv", "qid", "geni_ids", "\t"),
    ("tanba-roster", R / "tanba-p2600-pairs.tsv", "qid", "geni_ids", "\t"),
)


def read_pairs(path, qcol, gcol, delim):
    if not path.exists():
        return
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=delim):
            q = (row.get(qcol) or "").strip()
            # Emma's own file carries a verdict column; a WRONG is not a correspondence.
            if row.get("verdict") in ("WRONG", "BROWSER"):
                continue
            for g in re.split(r"[;,|]", row.get(gcol) or ""):
                g = g.strip()
                if q.startswith("Q") and g.isdigit():
                    yield q, g


def main():
    pairs = {}
    with open(R / "zipper-pairs.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            pairs[row["geni_id"]] = row
    if not pairs:
        sys.exit("no zipper pairs - run scripts/zipper-join.py first")
    if "method" not in next(iter(pairs.values())):
        sys.exit("zipper-pairs.tsv has no provenance columns - re-run scripts/zipper-join.py")
    print(f"{len(pairs):,} inferred pairs")

    # --- the chain -------------------------------------------------------------------
    def chain(g, seen=None):
        """Steps from `g` down to a root. A root is a pair the zipper did not make."""
        seen = seen or set()
        out = []
        while g in pairs and g not in seen:
            seen.add(g)
            row = pairs[g]
            out.append(row)
            g = row["from_geni"]
            if not g:
                break
        return out

    depth = {g: len(chain(g)) for g in pairs}
    print(f"chain depth: max {max(depth.values())}, "
          f"mean {sum(depth.values()) / len(depth):.1f}")

    # --- independent corroboration and contradiction ---------------------------------
    verdicts = collections.defaultdict(dict)   # geni -> {source: qid}
    manual_wrong = set()
    for label, path, qcol, gcol, delim in INDEPENDENT:
        n = 0
        for q, g in read_pairs(path, qcol, gcol, delim):
            verdicts[g][label] = q
            n += 1
        print(f"  {label:<22} {n:>7,} independent pairs"
              + ("" if path.exists() else "   (missing)"))
    # Her explicit WRONGs are the strongest contradiction there is.
    if (R / "emma-judgments.tsv").exists():
        with open(R / "emma-judgments.tsv", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                if row.get("verdict") == "WRONG":
                    manual_wrong.add((row["geni_id"], row["qid"]))

    supported, contradicted = {}, {}
    for g, row in pairs.items():
        for label, q in verdicts.get(g, {}).items():
            if q == row["qid"]:
                supported.setdefault(g, label)
            else:
                contradicted.setdefault(g, f"{label} says {q}")
        if (g, row["qid"]) in manual_wrong:
            contradicted[g] = "Emma judged this pair WRONG by hand"
    print(f"\n{len(supported):,} inferred pairs an INDEPENDENT source corroborates")
    print(f"{len(contradicted):,} an independent source contradicts")

    # --- propagate along the chain, exactly as she described -------------------------
    status, reason = {}, {}
    for g in pairs:
        st, why = "INFERRED", ""
        for step in chain(g):
            sg = step["geni_id"]
            if sg in contradicted:
                st, why = "POISONED", f"via {sg}: {contradicted[sg]}"
                break
            if sg in supported and st == "INFERRED":
                st, why = "CORROBORATED", f"via {sg}: {supported[sg]}"
        status[g], reason[g] = st, why

    counts = collections.Counter(status.values())
    print("\nstatus after propagating BOTH ways along the chain:")
    for k, n in counts.most_common():
        print(f"   {n:>7,}  {k}")

    out = R / "zipper-provenance.tsv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["geni_id", "qid", "round", "slot", "method", "chain_depth",
                    "root_geni_id", "status", "reason"])
        for g, row in sorted(pairs.items(), key=lambda kv: -depth[kv[0]]):
            c = chain(g)
            w.writerow([g, row["qid"], row["round"], row["slot"], row["method"],
                        len(c), c[-1]["from_geni"] if c else "", status[g], reason[g]])
    print(f"\nwrote {out.relative_to(ROOT)}")

    # --- the readable chains ---------------------------------------------------------
    names = {}
    with open(R / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            names[row["geni_id"]] = row["label_en"] or row["label_mul"]

    def render(g):
        lines = []
        for i, step in enumerate(chain(g)):
            lines.append(
                f"{'  ' * i}{'└─ ' if i else ''}{names.get(step['geni_id'], '?')} "
                f"`{step['geni_id']}` = `{step['qid']}` — round {step['round']}, "
                f"{step['slot']} by {step['method']} ({step['evidence']}), "
                f"from `{step['from_geni']}`")
        return lines

    md = R / "zipper-provenance-chains.md"
    wanted = [a for a in sys.argv[1:] if a in pairs]
    with open(md, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Zipper provenance chains\n\n")
        f.write("Generated by `scripts/zipper-provenance.py`. Emma, 2026-08-25: *\"ideally, a "
                "zipper merge will almost always be done with there being a relatively large "
                "chain of providence, not just a simple 'this was the justification,' but a "
                "potentially very large series of justifications.\"*\n\n")
        f.write(f"{len(pairs):,} inferred pairs · max chain depth {max(depth.values())} · "
                f"{counts.get('CORROBORATED', 0):,} corroborated · "
                f"{counts.get('POISONED', 0):,} poisoned\n\n")
        f.write("## Contradicted chains\n\n")
        poisoned = [g for g in pairs if status[g] == "POISONED"]
        if not poisoned:
            f.write("None.\n\n")
        for g in sorted(poisoned, key=lambda x: -depth[x])[:60]:
            f.write(f"### {names.get(g, '?')} `{g}`\n\n{reason[g]}\n\n")
            f.write("\n".join(render(g)) + "\n\n")
        if wanted:
            f.write("## Requested\n\n")
            for g in wanted:
                f.write(f"### {names.get(g, '?')} `{g}` — {status[g]}\n\n")
                f.write("\n".join(render(g)) + "\n\n")
    print(f"wrote {md.relative_to(ROOT)}")

    deepest = max(pairs, key=lambda g: depth[g])
    print(f"\ndeepest chain ({depth[deepest]} steps) - "
          f"{names.get(deepest, '?')} {deepest}:")
    for line in render(deepest)[:8]:
        print("   " + line)


if __name__ == "__main__":
    main()
