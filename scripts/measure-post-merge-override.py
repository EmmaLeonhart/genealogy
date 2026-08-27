"""What would `exports/post-merge/` actually overwrite? Measure before changing the merge.

    python scripts/measure-post-merge-override.py

**Emma's design, 2026-08-24:** `exports/post-merge/` is *"a directory with special logic: a
Geni record in there overwrites the same Geni ID from any other export"*, because post-merge is
newest and therefore right.

**Half of it exists.** `genimerge.sources._post_merge_last` sorts the directory to the end of
the merge order, so `CLAUDE.md` § *Later sources win value conflicts* already gives post-merge
the last word on any **single-valued** path — a birth date, a sex, a `CHAN` stamp.

**The other half does not, and cannot be got by ordering.** Relationships are *repeatable*:
`FAMC`, `FAMS` and `CHIL` are unioned and never dropped, which is the whole reason
`exports/excluded/` had to be invented for a parent link Geni deleted. So where an older export
says a person's father is X and post-merge says Y, the merged tree holds **both**.

**And she flagged the open question herself** — *"idk how we resolved geni conflicts in the
synoptic tree earlier either"* — with the queue noting that later-wins is not post-merge-wins
and would not do the job. So this measures the change before anything is written: **how many
people would lose a relationship, and which ones.**

## Method

Relationships cannot be compared through `FAMC`/`FAMS` xrefs, because `F…` xrefs are per-file
and mean nothing across exports. Each export is therefore reduced to, per person, the **Geni
ids** of their parents, spouses and children, resolved through that file's own `FAM` records.
Then for every person present in `exports/post-merge/`, the union of what the **other** exports
say is compared against what post-merge says.

* **would be dropped** — the other exports assert it, post-merge does not. This is exactly what
  the override removes, and the number that decides whether it is worth writing.
* **only in post-merge** — post-merge asserts it and nothing else does. Already gained by the
  ordinary union; the override changes nothing here.

**A dropped link is not necessarily wrong.** A post-merge ball is bounded at 5,000 people, so a
relative outside the ball is absent because the ball ended, not because Geni deleted the link.
That is the risk the override carries and it is reported separately: a link whose other end is
**absent from every post-merge export** is unfalsifiable, and dropping it would lose real data.

Writes `reports/post-merge-override.tsv` and prints the summary. Changes no code.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / "reports" / "post-merge-override.tsv"

INDI = re.compile(r"^0 @I(\d+)@ INDI", re.M)


def read_export(path):
    """`{geni_id: {"parents": set, "spouses": set, "children": set}}` for one GEDCOM.

    Families are resolved inside the file, because an `F…` xref means nothing outside it.
    """
    fam_husb = collections.defaultdict(set)
    fam_wife = collections.defaultdict(set)
    fam_chil = collections.defaultdict(set)
    person_fams = collections.defaultdict(set)
    person_famc = collections.defaultdict(set)
    cur = kind = None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("0 @"):
                parts = line.split()
                # `[1:-1]`, not `[2:-1]`: the slice must keep the RECORD LETTER. Stripping
                # `@I` left bare digits, every `startswith("I")` test failed, and the whole
                # scan returned zero people -- which the empty-join guard below caught and
                # reported as a broken join rather than as an absence of data.
                cur = parts[1][1:-1]
                kind = parts[2].strip() if len(parts) > 2 else ""
            elif cur and line.startswith("1 "):
                tag, _, val = line[2:].strip().partition(" ")
                ref = val[1:-1] if val.startswith("@") and val.endswith("@") else ""
                if kind == "FAM" and ref:
                    if tag == "HUSB":
                        fam_husb[cur].add(ref)
                    elif tag == "WIFE":
                        fam_wife[cur].add(ref)
                    elif tag == "CHIL":
                        fam_chil[cur].add(ref)
                elif kind == "INDI" and ref:
                    if tag == "FAMS":
                        person_fams[cur].add(ref)
                    elif tag == "FAMC":
                        person_famc[cur].add(ref)

    out = {}
    people = set(person_fams) | set(person_famc) | {
        m for fam in fam_chil.values() for m in fam}
    for p in people:
        if not p.startswith("I"):
            continue
        gid = p[1:]
        parents, spouses, children = set(), set(), set()
        for fam in person_famc.get(p, ()):
            for x in fam_husb[fam] | fam_wife[fam]:
                if x.startswith("I"):
                    parents.add(x[1:])
        for fam in person_fams.get(p, ()):
            for x in (fam_husb[fam] | fam_wife[fam]) - {p}:
                if x.startswith("I"):
                    spouses.add(x[1:])
            for x in fam_chil[fam]:
                if x.startswith("I"):
                    children.add(x[1:])
        out[gid] = {"parents": parents, "spouses": spouses, "children": children}
    return out


def merge_into(acc, one):
    for gid, rels in one.items():
        slot = acc.setdefault(gid, {"parents": set(), "spouses": set(), "children": set()})
        for k, v in rels.items():
            slot[k] |= v


def main():
    from genimerge.sources import find_exports
    post_dir = ROOT / "exports" / "post-merge"
    everything = find_exports(ROOT)
    post = [p for p in everything if p.parent == post_dir]
    others = [p for p in everything if p.parent != post_dir]
    if not post:
        sys.exit("no post-merge exports found -- nothing to measure")
    print(f"{len(post)} post-merge exports, {len(others)} others")

    pm = {}
    pm_people = set()
    for path in post:
        one = read_export(path)
        merge_into(pm, one)
        pm_people |= set(one)
    print(f"{len(pm_people):,} distinct people in post-merge/")

    rest = {}
    for n, path in enumerate(others, 1):
        one = {g: r for g, r in read_export(path).items() if g in pm_people}
        merge_into(rest, one)
        if n % 150 == 0 or n == len(others):
            print(f"  scanned {n}/{len(others)} other exports", flush=True)

    overlap = set(pm) & set(rest)
    if not overlap:
        sys.exit("NO person in post-merge/ was found in any other export -- that is an empty "
                 "join, not a finding. The id shapes on the two sides must differ.")
    print(f"{len(overlap):,} of them also appear in the older exports\n")

    rows = []
    tally = collections.Counter()
    for gid in sorted(overlap):
        for kind in ("parents", "spouses", "children"):
            dropped = rest[gid][kind] - pm[gid][kind]
            gained = pm[gid][kind] - rest[gid][kind]
            for other in sorted(dropped):
                # A relative outside every post-merge ball is absent because the ball ended
                # at 5,000 people, not because Geni deleted the link. Dropping those is the
                # risk this measurement exists to size.
                unfalsifiable = other not in pm_people
                tally[(kind, "dropped-unfalsifiable" if unfalsifiable else "dropped")] += 1
                rows.append({"geni_id": gid, "relation": kind, "other": other,
                             "verdict": "would be dropped",
                             "other_in_post_merge": "no" if unfalsifiable else "yes"})
            for other in sorted(gained):
                tally[(kind, "only in post-merge")] += 1

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["geni_id", "relation", "other", "verdict",
                                          "other_in_post_merge"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"{'relation':<10}{'dropped':>9}{'  of those unfalsifiable':>26}{'only in post-merge':>21}")
    for kind in ("parents", "spouses", "children"):
        print(f"{kind:<10}{tally[(kind,'dropped')] + tally[(kind,'dropped-unfalsifiable')]:>9,}"
              f"{tally[(kind,'dropped-unfalsifiable')]:>26,}"
              f"{tally[(kind,'only in post-merge')]:>21,}")
    total_drop = sum(v for (k, w), v in tally.items() if w.startswith("dropped"))
    unfals = sum(v for (k, w), v in tally.items() if w == "dropped-unfalsifiable")
    print(f"\n{total_drop:,} relationships would be dropped by the override, "
          f"{unfals:,} of them ({unfals / max(total_drop, 1):.0%}) to a person no post-merge "
          f"export reached -- those are the ones that would lose real data.")
    print(f"{len(rows):,} rows -> {OUT.resolve().relative_to(ROOT)}")
    print("NOTHING CHANGED. This measures the override; it does not apply it.")


if __name__ == "__main__":
    main()
