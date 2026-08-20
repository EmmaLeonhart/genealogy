"""The unidentified CJK records, grouped into the families they actually form.

Emma, 2026-08-19: *"I'll just try to identify them especially if they cluster it well
likely help."* She is right, and the shape of the data says so: the **2,398** Han-only
records that no rule could give a culture are not scattered. They form **362 connected
clusters**, and **84% of them sit in the 68 clusters of five or more** — so identifying one
cluster settles dozens of records at once, and there are only a few dozen judgements to
make rather than 2,398.

**Why they have no culture is the same fact.** Almost none of these clusters touches a
Wikidata-linked person, or anyone carrying kana, hangul, a clan seat or a listed place —
which is exactly what the six-to-fourteen-hop walk was looking for and did not find. They
are not hard cases; they are *isolated* cases. Nothing inside the data will settle them.

So this report is built for reading, not for inference. Per cluster: how big it is, the
surnames it carries, the generations it spans where dates exist, and a sample of the names
as written — enough to recognise a lineage.

    py scripts/build-unidentified-clusters.py [--min 3]

Offline: `reports/cjk-no-culture.csv`, `reports/derived-family.csv`,
`reports/derived-labels.csv`, `reports/derived-facts.csv`. Changes nothing.
"""

from __future__ import annotations

import csv
import io
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NOCULT = REPO / "reports" / "cjk-no-culture.csv"
FAMILY = REPO / "reports" / "derived-family.csv"
LABELS = REPO / "reports" / "derived-labels.csv"
FACTS = REPO / "reports" / "derived-facts.csv"
OUT = REPO / "reports" / "unidentified-clusters.md"

csv.field_size_limit(10 ** 7)
HAN_TOKEN = re.compile(r"[\u3400-\u9fff]+")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    min_size = 3
    if "--min" in sys.argv:
        min_size = int(sys.argv[sys.argv.index("--min") + 1])

    name = {}
    with io.open(NOCULT, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            name[r["geni_id"]] = r["cjk"]
    need = set(name)

    adj = defaultdict(set)
    qid = {}
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            me = r["geni_id"]
            if r.get("qid"):
                qid[me] = r["qid"]
            for p in (r.get("father"), r.get("mother")):
                if p:
                    adj[me].add(p)
                    adj[p].add(me)
            for k in (r.get("children") or "").replace("|", " ").split():
                if k.isdigit():
                    adj[me].add(k)
                    adj[k].add(me)
            for s in (r.get("spouses") or "").replace("|", " ").split():
                if s.isdigit():
                    adj[me].add(s)
                    adj[s].add(me)

    born = {}
    with io.open(FACTS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            y = (r.get("birth_date_year") or "").strip()
            if y and r["geni_id"] in need:
                born[r["geni_id"]] = y

    seen, comps = set(), []
    for g in need:
        if g in seen:
            continue
        stack, comp = [g], []
        seen.add(g)
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in adj.get(x, ()):
                if y in need and y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(comp)
    comps.sort(key=len, reverse=True)

    big = [c for c in comps if len(c) >= min_size]
    covered = sum(len(c) for c in big)
    md = [
        "# The unidentified CJK records, as the families they form", "",
        "Built by `scripts/build-unidentified-clusters.py`. **Proposes nothing** — this is "
        "for reading.", "",
        "Emma, 2026-08-19: *\"I'll just try to identify them especially if they cluster it "
        "well likely help.\"*", "",
        f"- records with no culture: **{len(need):,}**",
        f"- connected clusters they form: **{len(comps):,}**",
        f"- clusters of {min_size}+: **{len(big):,}**, covering **{covered:,}** records "
        f"({100 * covered / max(len(need), 1):.0f}%)",
        f"- singleton records: **{sum(1 for c in comps if len(c) == 1):,}**", "",
        "**58 of them carry a Wikidata item of their own**, which names them "
        "outright — the 孔 cluster is the Confucius family and `Q7240164` is 孔鯉, his "
        "son. The rest are unlinked, and that is why the culture walk could not settle "
        "them: it searches out to fourteen hops for kana, hangul, a clan seat or a listed "
        "place and finds none. Those are isolated rather than subtle, and are laid out "
        "here to be recognised rather than inferred.", "",
    ]
    for n, comp in enumerate(big, 1):
        surn = Counter()
        for g in comp:
            toks = [t for t in name[g].split() if HAN_TOKEN.fullmatch(t)]
            if len(toks) > 1:
                surn[toks[-1]] += 1
        years = sorted(int(born[g]) for g in comp if g in born and born[g].lstrip("-").isdigit())
        # **Members first, and this was a real bug.** The first version looked only at
        # NEIGHBOURS of the cluster for a Wikidata item and reported "anchors: none" for
        # clusters whose own members are linked -- the 孔 cluster is the Confucius family
        # and `Q7240164` is 孔鯉, his son. 58 of the 2,398 carry an item themselves.
        own = sorted({qid[x] for x in comp if x in qid})
        near = sorted({qid[y] for x in comp for y in adj.get(x, ()) if y in qid} - set(own))
        md.append(f"## Cluster {n} — {len(comp)} records")
        md.append("")
        if surn:
            md.append("- surnames: " + ", ".join(f"`{k}` ({v})" for k, v in surn.most_common(8)))
        if years:
            md.append(f"- birth years present: {years[0]} to {years[-1]} ({len(years)} dated)")
        else:
            md.append("- birth years present: **none**")
        md.append("- **Wikidata items ON these records**: "
                  + (", ".join(f"`{a}`" for a in own[:8])
                     + (f" … +{len(own) - 8}" if len(own) > 8 else "") if own else "none"))
        md.append("- Wikidata-linked relative one hop out: "
                  + (", ".join(f"`{a}`" for a in near[:8]) if near else "none"))
        md.append("")
        md.append("- names: " + ", ".join(f"`{name[g]}`" for g in comp[:16])
                  + (f" … and {len(comp) - 16} more" if len(comp) > 16 else ""))
        md.append("")
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{len(need):,} records, {len(comps):,} clusters, {len(big):,} of size {min_size}+")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
