"""The eccentric TAIL of the tree, split into connected clusters.

**Emma, 2026-09-05:** *"A couple days ago in a different chat you did eccentricity analysis on
the synoptic tree. You found a bunch of Chinese ancient people were most eccentric. Think you can
run something like that again? I want to see other eccentric clusters"*.

`scripts/measure-eccentricity.py` ranks PEOPLE, and the top of that ranking is one descent — 少昊
Shaohao down to 伯益 Bo Yi, six people on a single chain, which `CLAUDE.md` § *The Chinese
legendary lineage* records her calling *"very clustered with each other"*. A ranked list of
individuals cannot show a second group: everything near the top is the same lineage, and the next
family starts wherever that one runs out.

**So this cuts the tail and then finds its CONNECTED COMPONENTS.** Take everyone at or beyond a
distance threshold from Charlemagne, keep only the edges between them, and each component is a
cluster — a family that is far from the centre *together*. The Chinese lineage becomes one row
instead of six, and whatever else is out there gets its own.

**The threshold is swept rather than chosen**, because one cut is a choice about the answer: a
high threshold shows a handful of the very furthest and a low one merges everything back into the
bulk. The report carries several so the shape can be read rather than asserted.

**A cluster is described by what it IS, not by its rank.** Size, the distance band it spans, how
many carry a QID, and named members — because § *Always write the English label next to a
property or item ID* applies to people too, and a cluster nobody can name is not a finding.

Reads `reports/tree-eccentricity.csv` (already measured) and the family graph. Writes
`reports/eccentric-clusters.tsv` and `reports/eccentric-clusters.md`.
"""
from __future__ import annotations

import collections
import csv
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
csv.field_size_limit(10_000_000)

ECC = ROOT / "reports" / "tree-eccentricity.csv"
OUT_TSV = ROOT / "reports" / "eccentric-clusters.tsv"
OUT_MD = ROOT / "reports" / "eccentric-clusters.md"

#: The cuts to sweep. Chosen to bracket the tail rather than to produce a number: the median
#: distance to Charlemagne is 34 and the maximum 183, so these run from "well outside the bulk"
#: to "the far edge".
THRESHOLDS = (60, 70, 80, 90, 100, 120, 140)

#: How many clusters to name per threshold in the markdown. The TSV carries every one.
SHOW = 12


LABELS = ROOT / "reports" / "derived-labels.csv"
P2600 = ROOT / "out" / "wikidata" / "p2600-all.tsv"
OUT_MEMBERS = ROOT / "reports" / "eccentric-cluster-members.tsv"


def load_p2600():
    """`{geni_id: [qid, ...]}` from **Wikidata's own `P2600` statements**, not our derived column.

    **The two are the same join and that is worth knowing rather than assuming**: measured
    2026-09-05 over all 1,451,964 people, the `qid` column of `reports/tree-eccentricity.csv`
    holds 43,680 and this file holds 43,709 for the same population — 43,680 in both, **29 here
    only, 0 there only**. So the derived column was never a second opinion; reading this file is
    reading the source it came from, and it catches the 29.

    **What neither can say is whether WIKIDATA HOLDS AN ITEM.** This counts a `P2600` — somebody
    having linked a Geni profile to an item — and `CLAUDE.md` § *"Is X present?"* is the rule
    that got broken: absent-from-this-file never means absent-from-Wikidata. Scorpion I, Makeda
    and Scheschonq all have items; none has a `P2600`, and reporting the cluster as `0` read as
    *Wikidata does not have these people*.
    """
    out: dict[str, list[str]] = {}
    with open(P2600, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[1]:
                out.setdefault(parts[1], []).append(parts[0])
    return out


def load_names():
    """`{geni_id: name}` --- `label_en`, then `label_mul`, then the CJK or other-script name.

    **`label_en` is EMPTY for a CJK-only person and that is most of this tail.** The far edge of
    this tree is the Chinese legendary lineage and the Egyptian and Axumite kings; reading only
    `label_en` printed `(no label)` for the largest cluster in the report — 1,524 people, the one
    the whole question is about. `CLAUDE.md` § *THE PARENT DECK* records the same hole in the
    adjudication cards: *"A CJK-only person had no name on our side at all… the name lives in
    `cjk_names`"*, and its rule is that a card naming nobody is a broken card. A cluster naming
    nobody is a broken row for the same reason.

    A multi-valued cell takes its first value — `derived-labels.csv` separates with ` | `.
    """
    out = {}
    with open(LABELS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            for col in ("label_en", "label_mul", "cjk_names", "other_script_names"):
                value = (row.get(col) or "").split(" | ")[0].strip()
                if value:
                    out[row["geni_id"]] = value
                    break
    return out


def load_eccentricity(names):
    """`{geni_id: (dist, qid, label)}` for everyone with a distance to Charlemagne."""
    out = {}
    with open(ECC, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            d = row["dist_charlemagne"]
            if d == "" or d is None:
                continue
            g = row["geni_id"]
            out[g] = (int(d), row.get("qid", ""),
                      (row.get("label_en") or "").strip() or names.get(g, ""))
    return out


#: Words that say nothing about which family a cluster is. Deliberately short: a stop list long
#: enough to be opinionated starts deciding what the answer may be.
NOISE = frozenset("""
of the and n nn a i ii iii iv v jr sr private daughter son wife husband unknown
""".split())


def describe(labels) -> str:
    """The words shared across a WHOLE cluster, commonest first.

    **This exists because reading the five farthest labels is how a cluster gets mislabelled.**
    Emma, 2026-09-05, on the 222-person cluster this report called *"the Samaritan Itamar line"*:
    *"you said Samaritan itamar line but it's clearly everyone in the Samaritans cluster and you
    just bullshitted"*. She is right and it is countable — over all 222 labels, `Samaritan`
    occurs **145** times and `Itamar` **111**, alongside `High Priest` 38, `Cohen` 35 and
    `ben` 71. The Itamar line is the largest thread in a Samaritan cluster, not the cluster.

    The five farthest members happened to be consecutive generations of that one thread, so the
    name was true of the sample and false of the group. A cluster is now described from every
    member, and `reports/eccentric-cluster-members.tsv` carries the membership so the description
    is checkable rather than taken on trust.
    """
    counts = collections.Counter()
    total = 0
    for label in labels:
        total += 1
        seen = set()
        for word in label.split():
            word = word.strip("()[],.:;'\"").casefold()
            # A generation number is per-person, so it never describes the group.
            if not word or word in NOISE or word.isdigit() or word[:-2].isdigit():
                continue
            if word not in seen:
                seen.add(word)
                counts[word] += 1
    if not total:
        return ""
    # Ordered by share, then alphabetically, so the column is a pure function of its input.
    top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:6]
    return " ".join(f"{w} {n * 100 // total}%" for w, n in top if n * 100 // total >= 10)


def main() -> int:
    # `measure-eccentricity.py` has a hyphen, so `import` cannot reach it -- the same
    # importlib pattern `build-garborg-day._load_gaps` uses. Importing rather than
    # re-deriving matters here: that module already knows the ` | ` separator, and
    # `CLAUDE.md` § *Our side could never have two children* is what a second copy costs.
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "measure_eccentricity", ROOT / "scripts" / "measure-eccentricity.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    load_graph = module.load_graph

    print("loading the family graph", flush=True)
    index, neighbours = load_graph()
    rev = [""] * len(index)
    for g, i in index.items():
        rev[i] = g

    print("loading names (label_en falls back to mul and the CJK name)", flush=True)
    names = load_names()
    print("loading the measured distances", flush=True)
    ecc = load_eccentricity(names)
    print(f"{len(ecc):,} people carry a distance to Charlemagne", flush=True)
    print("loading Wikidata's own P2600 statements", flush=True)
    p2600 = load_p2600()
    print(f"{len(p2600):,} Geni ids carry a P2600 somewhere on Wikidata", flush=True)

    rows, members = [], []
    for cut in THRESHOLDS:
        keep = {index[g] for g, (d, _q, _l) in ecc.items() if d >= cut and g in index}
        # Components of the INDUCED subgraph: only edges with both ends in the tail.
        seen, clusters = set(), []
        for start in keep:
            if start in seen:
                continue
            stack, group = [start], []
            seen.add(start)
            while stack:
                n = stack.pop()
                group.append(n)
                for m in neighbours[n]:
                    if m in keep and m not in seen:
                        seen.add(m)
                        stack.append(m)
            clusters.append(group)
        clusters.sort(key=lambda c: (-len(c), -max(ecc[rev[n]][0] for n in c)))
        print(f"  cut {cut:>3}: {len(keep):>6,} people in {len(clusters):>5,} clusters",
              flush=True)
        for rank, group in enumerate(clusters, 1):
            dists = sorted(ecc[rev[n]][0] for n in group)
            named = [(ecc[rev[n]][0], ecc[rev[n]][2], ecc[rev[n]][1], rev[n]) for n in group]
            named.sort(key=lambda t: (-t[0], t[1]))
            rows.append({
                "cut": cut,
                "rank": rank,
                "people": len(group),
                "max_dist": dists[-1],
                "min_dist": dists[0],
                "median_dist": dists[len(dists) // 2],
                "p2600_linked": sum(1 for n in group if rev[n] in p2600),
                "common": describe(lab for _d, lab, _q, _g in named),
                "farthest": " | ".join(f"{lab or '(no label)'}" for _d, lab, _q, _g in named[:5]),
                "farthest_geni": " | ".join(g for _d, _l, _q, g in named[:5]),
            })
            for dist, lab, _q, gid in named:
                members.append((cut, rank, gid, dist, lab,
                                " ".join(p2600.get(gid, ()))))

    # **A blank name is TWO different things and the report must say which.** The 174-person
    # cluster at cut 100 came out `(no label)` for every member, and they are Geni's redacted
    # profiles: `CLAUDE.md` § *Redacted people go in* has `label_for()` return `''` for
    # `Private`, so the blank is correct rather than a lookup that failed. Leaving both as
    # `(no label)` reads as a broken report — the failure § *THE PARENT DECK* names — when one
    # of them is a finding about who lives out there.
    unnamed = {g for r in rows for g in r["farthest_geni"].split(" | ")
               if g and not ecc.get(g, (0, "", ""))[2]}
    if unnamed:
        import importlib.util as _il
        spec = _il.spec_from_file_location("labels", ROOT / "scripts" / "labels.py")
        labels_mod = _il.module_from_spec(spec)
        spec.loader.exec_module(labels_mod)
        private = set()
        with open(ROOT / "reports" / "display-names.csv", encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                g = row["geni_id"]
                if g in unnamed and labels_mod.is_redacted(row.get("name_raw", "")):
                    private.add(g)
        print(f"{len(unnamed):,} named members have no label; {len(private):,} are redacted")
        for r in rows:
            shown = []
            for g, lab in zip(r["farthest_geni"].split(" | "), r["farthest"].split(" | ")):
                if lab != "(no label)":
                    shown.append(lab)
                else:
                    shown.append("(private)" if g in private else "(no label)")
            r["farthest"] = " | ".join(shown)

    fields = ["cut", "rank", "people", "max_dist", "min_dist", "median_dist", "p2600_linked",
              "common", "farthest", "farthest_geni"]
    tmp = OUT_TSV.with_suffix(".tsv.tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        # Total sort key: (cut, rank) is unique per row.
        w.writerows(sorted(rows, key=lambda r: (r["cut"], r["rank"])))
    os.replace(tmp, OUT_TSV)
    print(f"wrote {OUT_TSV.relative_to(ROOT)}: {len(rows):,} cluster rows")

    # Every member of every cluster, so a description can be checked rather than believed.
    tmp = OUT_MEMBERS.with_suffix(".tsv.tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["cut", "rank", "geni_id", "dist_charlemagne", "label", "p2600_qids"])
        # Total sort key: (cut, rank, geni_id) is unique, and the Geni id is this repo's key.
        w.writerows(sorted(members, key=lambda m: (m[0], m[1], m[2])))
    os.replace(tmp, OUT_MEMBERS)
    print(f"wrote {OUT_MEMBERS.relative_to(ROOT)}: {len(members):,} membership rows")

    lines = [
        "# Eccentric CLUSTERS in the synoptic tree",
        "",
        "**Emma, 2026-09-05:** *\"You found a bunch of Chinese ancient people were most "
        "eccentric… I want to see other eccentric clusters\"*.",
        "",
        "`reports/eccentricity.md` ranks people, and the top of that ranking is one descent — "
        "six people on a single chain. A ranked list cannot show a second group, because "
        "everything near the top is the same lineage.",
        "",
        "**This cuts the tail at a distance from Charlemagne and finds the connected components "
        "of what is left.** Each component is a family that is far from the centre *together*. "
        "The threshold is swept rather than chosen — one cut is a choice about the answer.",
        "",
        "`reports/eccentric-clusters.tsv` carries every cluster at every cut; this names the "
        f"largest {SHOW} per cut. `reports/eccentric-cluster-members.tsv` carries every member "
        "of every cluster, so a description can be checked rather than believed.",
        "",
        "## ⛔ `P2600 linked` DOES NOT MEAN WIKIDATA HAS THEM",
        "",
        "**Emma, 2026-09-05, on the first version of this report:** *\"your measurement of there "
        "being qids is a bit flawed. Both Chinese lines likely have wiki data items even if no "
        "connection… Pre dynastic Egypt definitely does… Axum certainly have qids lol… Third "
        "intermediate period def has qids lol\"*.",
        "",
        "**She is right, and the column was mislabelled rather than miscounted.** It counts a "
        "`P2600` *Geni.com profile ID* — somebody having **linked** a Geni profile to a Wikidata "
        "item. Scorpion I, Makeda Queen of Sheba and Scheschonq all have items; not one has a "
        "`P2600`, so the cluster reads `0` and the first version of this report said *\"every "
        "other cluster is 0\"* as though that were a fact about Wikidata's content.",
        "",
        "**So a `0` here means UNLINKED, and nothing more.** `CLAUDE.md` § *\"Is X present?\"* is "
        "the standing rule: our Wikidata store is a Geni-shaped slice, so absent-from-it never "
        "means absent-from-Wikidata, and every absence has to carry the store it is about. The "
        "column is now named for what it measures.",
        "",
        "**What it is genuinely good for is the opposite reading.** An eccentric cluster with a "
        "high link count is one we have already reconciled; one at `0` is unreconciled, and "
        "whether that is because the items do not exist or because nobody joined them is the "
        "question a live check answers and this file cannot.",
        "",
    ]
    by_cut = collections.defaultdict(list)
    for r in rows:
        by_cut[r["cut"]].append(r)
    for cut in THRESHOLDS:
        got = sorted(by_cut[cut], key=lambda r: r["rank"])
        total = sum(r["people"] for r in got)
        lines += [
            f"## At least {cut} hops from Charlemagne",
            "",
            f"**{total:,} people in {len(got):,} clusters.**",
            "",
            "| # | people | dist (min–max) | P2600 linked | shared across the whole cluster "
            "| the farthest members |",
            "| ---: | ---: | --- | ---: | --- | --- |",
        ]
        for r in got[:SHOW]:
            lines.append(f"| {r['rank']} | {r['people']:,} | {r['min_dist']}–{r['max_dist']} "
                         f"| {r['p2600_linked']} | {r['common']} | {r['farthest']} |")
        if len(got) > SHOW:
            lines.append(f"| … | | | | | {len(got) - SHOW:,} more clusters in the TSV |")
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
