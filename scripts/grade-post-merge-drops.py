"""Which of the 412 falsifiable post-merge drops really are *Geni deleted this link*?

`reports/post-merge-override.tsv` measured that applying the post-merge relationship override
literally would drop **5,537** relationships and gain nothing. **5,125 of those (93%) point at
somebody no post-merge ball reached**, so they are absent because the ball ended at 5,000 people,
not because Geni removed the link. Those are not evidence of anything.

The remaining **412 are falsifiable**: both ends sit inside a post-merge ball, so the export had
the chance to record the link and did not.

This grades those 412 structurally. A drop is `link-gone` when

* both people are present in some `exports/post-merge/*.ged`, **and**
* `out/merged.ged` gives them a family in common, **and**
* no post-merge record gives them a family in common.

Writes `reports/post-merge-falsifiable.tsv`. **It writes no override and changes no tree** --
queue.md is explicit that the next step is to look at these as records, not to apply anything.
"""
import collections
import csv
import glob
import io
import re
import sys

SRC = "reports/post-merge-override.tsv"
MERGED = "out/merged.ged"
OUT = "reports/post-merge-falsifiable.tsv"


def families(path, want):
    """`{geni_id: {family xref}}` plus the set of people the file actually holds."""
    fam, present, cur = collections.defaultdict(set), set(), None
    for line in io.open(path, encoding="utf-8", errors="replace"):
        if line.startswith("0 "):
            m = re.match(r"^0 @I(\d+)@ INDI", line)
            cur = m.group(1) if m and m.group(1) in want else None
            if cur:
                present.add(cur)
        elif cur:
            m = re.match(r"^1 (FAMC|FAMS) @([^@]+)@", line)
            if m:
                fam[cur].add(m.group(2))
    return fam, present


def main():
    rows = [r for r in csv.DictReader(io.open(SRC, encoding="utf-8"), delimiter="\t")
            if r["other_in_post_merge"] == "yes"]
    want = {g for r in rows for g in (r["geni_id"], r["other"])}

    merged_fam, _ = families(MERGED, want)
    pm_fam, present = collections.defaultdict(set), set()
    for f in sorted(glob.glob("exports/post-merge/*.ged")):
        fam, seen = families(f, want)
        for g, v in fam.items():
            pm_fam[g] |= v
        present |= seen

    out, tally = [], collections.Counter()
    for r in rows:
        a, b = r["geni_id"], r["other"]
        shared_before = merged_fam[a] & merged_fam[b]
        shared_after = pm_fam[a] & pm_fam[b]
        if a not in present or b not in present:
            verdict = "cannot-judge: not both in a post-merge ball"
        elif not shared_before:
            verdict = "no shared family in merged.ged"
        elif shared_after:
            verdict = "link still present"
        else:
            verdict = "link-gone"
        tally[verdict] += 1
        out.append({"geni_id": a, "relation": r["relation"], "other": b,
                    "verdict": verdict,
                    "family_in_merged": ";".join(sorted(shared_before)),
                    "family_in_post_merge": ";".join(sorted(shared_after))})

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    print(f"falsifiable drops graded: {len(out)}")
    for v, n in tally.most_common():
        print(f"  {v:<44} {n}")
    by_rel = collections.Counter(r["relation"] for r in out if r["verdict"] == "link-gone")
    print(f"  link-gone by relation: {dict(by_rel)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
