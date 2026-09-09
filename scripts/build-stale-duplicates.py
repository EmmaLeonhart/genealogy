"""People Geni has merged and our corpus has not: the survivor plus a twin we still hold.

    python scripts/build-stale-duplicates.py

**Emma's method, 2026-08-24:** *"just use my method"* — read the merges off her own Geni
activity feed rather than guessing at them. `reports/geni-merges-performed.tsv` is that
list: 180 distinct surviving profile ids over 13 pages, and the feed reached its end, so
it is complete rather than a sample.

**What a row means.** Geni now holds **one** profile for this person. Our merged tree
holds **two**, because the exports covering them were taken before she merged. So the
tree double-counts the person, and — since their parents are frequently duplicated too —
whole parallel lineages sit side by side. That is the clan-added-to-Geni-three-times
phenomenon showing up in our data.

**The evidence column is the point, and the first version got it wrong.** It compared the
two profiles' father *ids*, which are different whenever the father is himself duplicated
— so it read "not the same father" for Kuiko Haji-no-muraji, whose two profiles both
name a father called *Otori Haji-no-muraji*. Comparing ids is the wrong test exactly where
the evidence is strongest. This compares father and mother **names**, and grades:

* `strong`   — a parent name matches, or both sides are parentless and the dates agree
* `medium`   — no parent recorded on either side and no dates to disagree
* `weak`     — parent names differ, or the dates do

`weak` is kept in the file, not dropped. Amram V Samaritan High Priest is the worked
example: one profile's father is *Tsedaka I*, the other's is *Aaron III*, and only one
carries a death date. That is either one man with conflicting parentage from two creation
runs or two different men, and Emma is the one who can tell.

**The absorbed id is unknowable from the feed** — it shows only the survivor. So a twin
here is a *candidate* for the profile that was absorbed, never a certainty; `Yorimoto
Tanba` is the known false positive, four men across generations sharing a name.

**Flags, never merges.** `CLAUDE.md`: the duplicate merges are hers.

Writes `reports/geni-stale-duplicates.tsv`.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent

#: Placeholder names — two `NN no Mikoto` profiles are two unnamed people, not one
#: person twice. Same screen as `scripts/find-geni-duplicates.py`.
NOT_A_NAME = {"", "nn", "n n", "n.n.", "private", "unknown", "?", "??", "???",
              "ukjent", "okänd", "ukendt"}


def is_placeholder(name):
    low = " ".join((name or "").lower().split())
    if low in NOT_A_NAME or "<private>" in low:
        return True
    first = low.split()[0] if low.split() else ""
    return first in NOT_A_NAME | {"fnu", "lnu", "infant", "baby", "stillborn"}


def main():
    survivors = set()
    with open(ROOT / "reports" / "geni-merges-performed.tsv", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and line != "geni_id":
                survivors.add(line)
    print(f"{len(survivors)} merge survivors from Emma's activity feed")

    labels = {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            labels[row["geni_id"]] = (row["label_en"] or row["label_mul"] or "").strip()

    by_name = collections.defaultdict(list)
    for gid, label in labels.items():
        if label and not is_placeholder(label):
            by_name[label.lower()].append(gid)

    # Only the people we need the family and dates for.
    interesting = set()
    for survivor in survivors:
        label = labels.get(survivor, "")
        if label and not is_placeholder(label):
            twins = [g for g in by_name[label.lower()] if g != survivor]
            if twins:
                interesting.add(survivor)
                interesting.update(twins)

    family, facts = {}, {}
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in interesting:
                family[row["geni_id"]] = row
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in interesting:
                facts[row["geni_id"]] = row

    def parent_name(gid, which):
        return labels.get((family.get(gid, {}).get(which) or "").strip(), "").lower()

    def years(gid):
        f = facts.get(gid, {})
        return (f.get("birth_date_year") or "", f.get("death_date_year") or "")

    rows = []
    for survivor in sorted(interesting & survivors):
        label = labels[survivor]
        for twin in sorted(g for g in by_name[label.lower()] if g != survivor):
            sf, tf = parent_name(survivor, "father"), parent_name(twin, "father")
            sm, tm = parent_name(survivor, "mother"), parent_name(twin, "mother")
            sy, ty = years(survivor), years(twin)

            name_match = (sf and sf == tf) or (sm and sm == tm)
            parents_differ = (sf and tf and sf != tf) or (sm and tm and sm != tm)
            dates_differ = any(a and b and a != b for a, b in zip(sy, ty))

            if dates_differ or parents_differ:
                evidence = "weak"
            elif name_match:
                evidence = "strong"
            elif not (sf or tf or sm or tm):
                evidence = "medium"
            else:
                evidence = "medium"

            rows.append({
                "evidence": evidence,
                "name": label,
                "merged_survivor": survivor,
                "stale_twin": twin,
                "survivor_father": labels.get(
                    (family.get(survivor, {}).get("father") or "").strip(), ""),
                "twin_father": labels.get(
                    (family.get(twin, {}).get("father") or "").strip(), ""),
                "father_name_matches": "yes" if (sf and sf == tf) else "no",
                "survivor_years": "-".join(x or "?" for x in sy),
                "twin_years": "-".join(x or "?" for x in ty),
                "survivor_children": family.get(survivor, {}).get("child_count", ""),
                "twin_children": family.get(twin, {}).get("child_count", ""),
            })

    order = {"strong": 0, "medium": 1, "weak": 2}
    rows.sort(key=lambda r: (order[r["evidence"]], r["name"]))

    dest = ROOT / "reports" / "geni-stale-duplicates.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    counts = collections.Counter(r["evidence"] for r in rows)
    print(f"\nwrote {dest.relative_to(ROOT)}: {len(rows)} pairs")
    for kind in ("strong", "medium", "weak"):
        print(f"   {kind:<7} {counts[kind]}")
    print()
    for row in rows[:20]:
        print(f"  [{row['evidence']:<6}] {row['name'][:32]:<32} "
              f"father matches: {row['father_name_matches']}")


if __name__ == "__main__":
    main()
