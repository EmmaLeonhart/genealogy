"""Every person in the corpus who gets NO label at all, and what each could get instead.

    py scripts/census-label-gap.py

**The population.** `reports/derived-labels.csv` holds 1,451,964 people; `label_en` and
`label_mul` are both non-empty on 1,389,442 of them and both empty on **62,522**. That 62,522 is
the whole of the outstanding `en`/`mul` job in `queue.md` § *Labels in seven languages* -- the
other 95% already have both, and the two columns agree row for row because they derive from the
same string.

An empty label is `scripts/labels.label_for()` returning `''`, which it does for `Private` and
`<private>` and nothing else. So this population is exactly the redacted one, plus whatever else
reduces to a marker.

**`CLAUDE.md` § *The NN/Private label algorithm applies to EVERY unnamed person* is not
optional**, so "no label" is never the answer. Each of these people gets one of three outcomes,
and the point of the census is to count them rather than assume the split:

| outcome | what goes in `mul` | needs |
| --- | --- | --- |
| **surname** | `NN Larsson` | a surname surviving redaction, from `SURN` or `_MARNM` |
| **relative** | `NN` + `son of <X>` in the locals | a NAMED relative within two hops |
| **bare** | `NN` | neither -- the marker alone |

**The surname is checked first because it is free and it is on the person.** `CLAUDE.md`
§ *Redacted people go in* measured 3,605 `<private> /Surname/` records against 16,402 bare
`Private` at an earlier corpus size and called the surname *"real data"* worth keeping; this
counts the same thing at 605 exports and per person rather than per record.

**Relatives are searched to two hops, not one**, and both are recorded separately so the cost of
the second hop is visible rather than assumed. Emma, 2026-08-16: *"It can work off of those
long-range things... grandparents or grandchildren or siblings."* Order within a hop is
father, mother, spouse, child, then sibling -- parents first because
`docs/export-seed-rules.md` puts patronymics at the top for the same reason, that a parent names
the person rather than merely relating to them.

**A relative whose own label is empty is not a relative for this purpose.** That is the
`UNUSABLE` guard `build-nn-label-batch.py` already applies to its own population: *"mother of
unknown"* names nobody. Here it falls out of the data instead of needing a regex, because an
unnamed relative is one of the 62,522 and so has no label to use.

Writes `reports/label-gap.csv` -- one row per unlabelled person, every one of them, per
`CLAUDE.md` section *"Analyse this" means build a CSV of every instance*.
"""

from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

LABELS = REPO / "reports" / "derived-labels.csv"
FAMILY = REPO / "reports" / "derived-family.csv"
NAMES = REPO / "reports" / "display-names.csv"
OUT = REPO / "reports" / "label-gap.csv"

#: A `SURN` that is punctuation or a marker is not a family name. Emma's boundary, 2026-08-17:
#: **words yes, punctuation no** -- and she confirmed a surname of `.` becomes nothing.
NOT_A_SURNAME = {"", ".", "?", "-", "--", "n", "nn", "n n", "private", "<private>",
                 "unknown", "ukjent", "okand", "ukendt"}

#: Where the relative search looks, in order. Parents first: a parent names the person.
SLOTS = ("father", "mother", "spouse", "child", "sibling")


def split_ids(cell):
    """`derived-family.csv` separates multi-valued cells with a pipe padded by spaces.

    `CLAUDE.md` section *Our side could never have two children* is the record of what
    splitting on the wrong character costs: 379,251 people arrived childless from a comma
    split, and the repair without `.strip()` moved the count by exactly zero.
    """
    return [t.strip() for t in (cell or "").split("|") if t.strip()]


def main() -> int:
    print("reading derived-labels.csv ...")
    label = {}
    unlabelled = set()
    with LABELS.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g = row["geni_id"]
            en = row["label_en"].strip()
            label[g] = en
            if not en and not row["label_mul"].strip():
                unlabelled.add(g)
    print(f"  {len(label):,} people, {len(unlabelled):,} with no label at all")

    print("reading display-names.csv for surnames ...")
    surname = {}
    with NAMES.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g = row["geni_id"]
            if g not in unlabelled or g in surname:
                continue
            for cell in (row.get("surn"), row.get("marnm")):
                s = (cell or "").strip()
                if s and s.lower() not in NOT_A_SURNAME:
                    surname[g] = s
                    break
    print(f"  {len(surname):,} of the unlabelled carry a usable surname")

    print("reading derived-family.csv ...")
    kin = collections.defaultdict(lambda: collections.defaultdict(list))
    parents_of = {}
    with FAMILY.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g = row["geni_id"]
            fa = (row.get("father") or "").strip()
            mo = (row.get("mother") or "").strip()
            parents_of[g] = (fa, mo)
            if fa:
                kin[g]["father"].append(fa)
                kin[fa]["child"].append(g)
            if mo:
                kin[g]["mother"].append(mo)
                kin[mo]["child"].append(g)
            for s in split_ids(row.get("spouses")):
                kin[g]["spouse"].append(s)
                kin[s]["spouse"].append(g)

    # Siblings: everyone sharing a recorded parent. Geni records no sibling edge --
    # `CLAUDE.md` section *CHECK before you alarm her* measures 2,126 of 30,361 path steps as
    # sibling hops, so leaving them out would understate the reach by a real margin.
    bykid = collections.defaultdict(set)
    for g, (fa, mo) in parents_of.items():
        for p in (fa, mo):
            if p:
                bykid[p].add(g)
    for kids in bykid.values():
        if len(kids) > 1:
            for a in kids:
                kin[a]["sibling"].extend(k for k in kids if k != a)
    print(f"  {len(kin):,} people carry at least one relationship")

    def named_at(g):
        """The first NAMED relative of `g`, as a (slot, id, label) triple, or `None`."""
        rel = kin.get(g)
        if not rel:
            return None
        for slot in SLOTS:
            for other in rel.get(slot, ()):
                if label.get(other):
                    return slot, other, label[other]
        return None

    print("searching for a named relative, one hop then two ...")
    rows, tally = [], collections.Counter()
    for g in sorted(unlabelled):
        surn = surname.get(g, "")
        hit = named_at(g)
        hops, slot, via, via_label = "", "", "", ""
        if hit:
            hops, (slot, via, via_label) = "1", hit
        else:
            # Two hops. The intermediate is by construction unnamed, which is why its own
            # relatives are worth walking -- an unnamed father with a named father gives a
            # grandfather, and that is the long-range case Emma named.
            for mid_slot in SLOTS:
                for mid in kin.get(g, {}).get(mid_slot, ()):
                    if label.get(mid):
                        continue
                    hit2 = named_at(mid)
                    if hit2:
                        hops = "2"
                        slot = mid_slot + "'s " + hit2[0]
                        via, via_label = hit2[1], hit2[2]
                        break
                if hops:
                    break
        outcome = ("surname" if surn else "relative" if hops else "bare")
        tally[outcome] += 1
        tally["  reachable via a relative (hops=" + (hops or "none") + ")"] += 1
        rows.append({"geni_id": g, "outcome": outcome, "surname": surn,
                     "relative_hops": hops, "relative_slot": slot,
                     "relative_geni_id": via, "relative_label": via_label})

    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["geni_id", "outcome", "surname", "relative_hops",
                                          "relative_slot", "relative_geni_id",
                                          "relative_label"])
        w.writeheader()
        w.writerows(rows)

    print(f"\nwrote {OUT.relative_to(REPO)} - {len(rows):,} rows")
    total = len(rows) or 1
    for k in ("surname", "relative", "bare"):
        print(f"  {tally[k]:>7,}  {k:<9} {tally[k]*100/total:5.1f}%")
    print()
    for k, n in sorted(tally.items()):
        if k.startswith("  "):
            print(f"  {n:>7,}{k}")
    # A person with a surname may ALSO have a named relative, and both go on the label --
    # `NN Garborg` in `mul` and `son of Arne` in the locals. The outcome column records the
    # strongest available, so this is the count that matters for the descriptive half.
    both = sum(1 for r in rows if r["surname"] and r["relative_hops"])
    print(f"\n  {both:,} of the surname rows ALSO have a named relative, so they get both halves")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
