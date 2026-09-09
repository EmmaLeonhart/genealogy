"""How much corroboration does each zipper pair actually have? All of them, not a sample.

    python scripts/census-zipper-evidence.py

**Emma, 2026-08-25, after judging sixteen sampled merges:** *"All of these seemed like easy ones
lol I'm not sure if you're only choosing ones you consider 'ambiguous'... all of these look easy
and I'm confused what a hard one will even look like."*

The sample was drawn at random and then **sorted easiest-first**, because she had asked for that
ordering. So sixteen easy rows in a row says nothing about the population -- which is exactly the
thing this file measures instead of asserting.

For every pair in `reports/zipper-pairs.tsv`, count what a human would have to go on:

* how many parents our tree names,
* how many parents Wikidata names,
* and, of the slots where both sides name somebody, how many share a word.

The word check is **for banding only**. It never decides a pair and never feeds a merge -- it is
the same line `CLAUDE.md` draws for the name fallback in `genimerge.paths`: a report for a human,
never an input.

Bands, coarsest first:

| band | meaning |
| --- | --- |
| `BOTH-PARENTS-AGREE` | both sides name a father and a mother, and both slots share a word |
| `BOTH-PARENTS-PARTIAL` | both sides name two parents, one slot shares a word |
| `ONE-PARENT-AGREE` | one comparable slot, and it shares a word |
| `ONE-PARENT-DISAGREE` | one comparable slot, and it does not |
| `PARENTS-ONE-SIDE` | one side has parents, the other has none -- absence, not disagreement |
| `NO-PARENTS` | neither side names a parent; position is the whole evidence |
| `NAMES-CONFLICT` | every comparable slot disagrees |

Writes `reports/zipper-evidence.tsv`, one row per pair. Offline.
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

#: Tokens that carry no identifying force -- titles, particles, placeholders.
NOISE = {
    "of", "de", "von", "van", "der", "den", "di", "da", "du", "la", "le", "el",
    "af", "och", "the", "til", "till", "zu", "zur", "sir", "lord", "lady", "count",
    "countess", "graf", "grafin", "gräfin", "duke", "duchess", "king", "queen",
    "baron", "baroness", "earl", "prince", "princess", "herr", "fru", "nn",
    "unknown", "private", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii",
}


def words(name):
    """Lowercased identifying tokens. Diacritics are KEPT -- `CLAUDE.md` is explicit that
    folding them invents ambiguity; they are only stripped for the noise lookup."""
    out = set()
    for w in re.split(r"[^0-9A-Za-zÀ-ÿĀ-ſ]+", (name or "").lower()):
        if len(w) > 2 and w not in NOISE:
            out.add(w)
    return out


def main():
    labels = {}
    with open(ROOT / "out" / "wikidata" / "labels.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            labels[row["qid"]] = (row["en"] or row["mul"] or row["no"]
                                  or row["nb"] or row["sv"] or row["da"])
    print(f"{len(labels):,} Wikidata labels")

    ours_name = {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ours_name[row["geni_id"]] = row["label_en"] or row["label_mul"]
    print(f"{len(ours_name):,} of our labels")

    fam = {}
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fam[row["geni_id"]] = row
    print(f"{len(fam):,} of our people")

    theirs = {}
    with open(ROOT / "out" / "wikidata" / "relations.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            theirs[row["qid"]] = row
    print(f"{len(theirs):,} Wikidata items with relationships")

    bands = collections.Counter()
    by_round = collections.defaultdict(collections.Counter)
    rows = []
    with open(ROOT / "reports" / "zipper-pairs.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            g, q, rnd = row["geni_id"], row["qid"], row["round"]
            mine, their = fam.get(g), theirs.get(q)
            slots = []          # (ours_name, theirs_name) where BOTH sides name somebody
            n_ours = n_theirs = 0
            for col, prop in (("father", "p22"), ("mother", "p25")):
                a = (mine or {}).get(col, "").split(";")[0].strip()
                b = ((their or {}).get(prop, "") or "").split(";")[0].strip()
                an = ours_name.get(a, "") if a else ""
                bn = labels.get(b, "") if b else ""
                n_ours += bool(an)
                n_theirs += bool(bn)
                if an and bn:
                    slots.append((an, bn))
            hits = [bool(words(a) & words(b)) for a, b in slots]
            if not slots:
                band = "NO-PARENTS" if not (n_ours or n_theirs) else "PARENTS-ONE-SIDE"
            elif len(slots) == 2:
                band = ("BOTH-PARENTS-AGREE" if all(hits)
                        else "BOTH-PARENTS-PARTIAL" if any(hits) else "NAMES-CONFLICT")
            else:
                band = "ONE-PARENT-AGREE" if hits[0] else "ONE-PARENT-DISAGREE"
            bands[band] += 1
            by_round[rnd][band] += 1
            rows.append({
                "round": rnd, "geni_id": g, "qid": q, "band": band,
                "ours": ours_name.get(g, ""), "theirs": labels.get(q, ""),
                "our_parents": n_ours, "their_parents": n_theirs,
                "comparable_slots": len(slots), "slots_agreeing": sum(hits),
            })

    out = ROOT / "reports" / "zipper-evidence.tsv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    total = sum(bands.values())
    print(f"\n{total:,} zipper pairs\n")
    for band, n in bands.most_common():
        print(f"  {n:>7,}  {100 * n / total:5.1f}%  {band}")
    print("\nby round:")
    order = [b for b, _ in bands.most_common()]
    print("  round  " + "  ".join(f"{b[:12]:>12}" for b in order))
    for rnd in sorted(by_round, key=int):
        c = by_round[rnd]
        print(f"  {rnd:>5}  " + "  ".join(f"{c[b]:>12,}" for b in order))
    print(f"\nwrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
