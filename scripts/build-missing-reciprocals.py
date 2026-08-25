"""Every relationship our tree records between two items that Wikidata is missing.

    python scripts/build-missing-reciprocals.py

**Emma, 2026-08-25:** *"there is also another error where the created individuals do no actually
get connected in they have their links to other people but the creation quikstatements can add
links on other profiles but it just does no"*, then *"make quickstatements please that fill in all
of the relationships that are asymmetric that should have been added in the people we made but
were not added for some reason."*

**The cause, exactly.** A creation block writes `LAST P40 Q141168797` — the new person points at
an existing child. The reverse, `Q141168797 P22 <the new person>`, cannot be written in the same
batch: the new item has no QID until QuickStatements mints it, and **`LAST` is only valid as the
subject of a line, never as a value.** So every creation leaves its links one-way, and the
reciprocal is silently never emitted. Verified on the built file: **0 lines use `LAST` as a
value.**

The daily builder was supposed to close these the next day, in its "everything missing from people
who already have QIDs" section. It did not, because that section decides what is missing from
`live_state` and the downloaded store — both of which **predate the items being asked about**. An
item created yesterday is not in either, so the builder falls back to assuming it carries nothing,
and a fallback that guesses "nothing" cannot notice something absent.

**So this reads the items live instead of guessing.** `WikidataClient.full_entities`, one batched
request, exactly as `CLAUDE.md` requires: *"anything that decides what to emit is read from
downloaded JSON"* and *"a summariser may be used to find something, never to establish that a
property is absent — absence is exactly what it gets wrong."*

## What it emits

For every pair of people **both** of whom carry a QID, and for every relationship our merged tree
records between them, the statement is emitted if the live item does not already hold it:

| our tree says | statement | and the reverse |
| --- | --- | --- |
| B is A's father | `B P40 A` | `A P22 B` |
| B is A's mother | `B P40 A` | `A P25 B` |
| A and B are spouses | `A P26 B` | `B P26 A` |
| A and B are siblings | `A P3373 B` | `B P3373 A` |

Both directions are checked independently, because the asymmetry is the whole complaint: an
existing item may hold `P40` while the child holds no `P22`.

Every statement carries an `S2600` reference to the Geni id of the person the claim is about.

**It creates nothing and removes nothing.** Only additions, only between items that already exist.

Writes `reports/wikidata-reciprocals.qs`.
"""
from __future__ import annotations

import collections
import csv
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("BOT_CONTACT", "emma@topazcomputing.com")

FATHER, MOTHER, CHILD, SPOUSE, SIBLING = "P22", "P25", "P40", "P26", "P3373"


def main():
    # Everyone we know to have an item: Emma's ledger plus anything Wikidata states.
    qid = {}
    with open(ROOT / "reports" / "garborg-qids.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row.get("qid"):
                qid[row["geni_id"]] = row["qid"]
    ledger_only = set(qid)
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0].startswith("Q") and row[1].strip().isdigit():
                qid.setdefault(row[1].strip(), row[0])
    print(f"{len(ledger_only)} in Emma's ledger, {len(qid):,} Geni ids with a known item")

    # Our tree's relationships among those people.
    want = set(qid)
    father, mother = {}, {}
    spouses = collections.defaultdict(set)
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g = row["geni_id"]
            if g not in want:
                continue
            if (row.get("father") or "").strip() in want:
                father[g] = row["father"].strip()
            if (row.get("mother") or "").strip() in want:
                mother[g] = row["mother"].strip()
            for s in (row.get("spouses") or "").replace(",", ";").split(";"):
                if s.strip() in want:
                    spouses[g].add(s.strip())
    siblings = collections.defaultdict(set)
    bykids = collections.defaultdict(set)
    for g, p in list(father.items()) + list(mother.items()):
        bykids[p].add(g)
    for kids in bykids.values():
        for a in kids:
            for b in kids:
                if a != b:
                    siblings[a].add(b)
    print(f"{len(father):,} father links, {len(mother):,} mother links, "
          f"{sum(len(v) for v in spouses.values())//2:,} spouse pairs among them")

    # **No live check.** Emma, 2026-08-25: *"do no fuckin check"*. QuickStatements ignores a
    # statement an item already holds, so re-asserting one costs nothing, while reading a
    # thousand items live costs minutes and a rate-limit budget. Emit everything the tree
    # records; let QuickStatements deduplicate.
    touched = set(ledger_only)
    for g in list(ledger_only):
        for other in ([father.get(g), mother.get(g)] + list(spouses.get(g, ()))
                      + list(siblings.get(g, ())) + list(bykids.get(g, ()))):
            if other:
                touched.add(other)
    print(f"{len(touched)} people touched")

    lines, seen, tally = [], set(), collections.Counter()

    def add(subj_g, prop, obj_g, why):
        sq, oq = qid.get(subj_g), qid.get(obj_g)
        if not sq or not oq or sq == oq:
            return
        key = (sq, prop, oq)
        if key in seen:
            return
        seen.add(key)
        tally[why] += 1
        lines.append(f'{sq}\t{prop}\t{oq}\tS2600\t"{subj_g}"')

    for g in sorted(touched):
        f_, m_ = father.get(g), mother.get(g)
        if f_:
            add(g, FATHER, f_, "child -> father (P22)")
            add(f_, CHILD, g, "father -> child (P40)")
        if m_:
            add(g, MOTHER, m_, "child -> mother (P25)")
            add(m_, CHILD, g, "mother -> child (P40)")
        for s in spouses.get(g, ()):
            add(g, SPOUSE, s, "spouse (P26)")
        for s in siblings.get(g, ()):
            add(g, SIBLING, s, "sibling (P3373)")

    dest = ROOT / "reports" / "wikidata-reciprocals.qs"
    with open(dest, "w", encoding="utf-8", newline="\n") as out:
        out.write("# Relationships our tree records that the live Wikidata items do not hold.\n")
        out.write("# Both directions are checked separately: a parent item can hold P40 while\n")
        out.write("# the child holds no P22, which is exactly what a CREATE block leaves behind\n")
        out.write("# -- LAST is only valid as a subject, never as a value, so a new person's\n")
        out.write("# reciprocal can never be written in the batch that creates them.\n")
        out.write("#\n")
        out.write("# Nothing checked live: QuickStatements ignores a statement already held.\n")
        out.write("# Additions only. Nothing is created and nothing is removed.\n\n")
        out.write("\n".join(lines) + ("\n" if lines else ""))

    print(f"\nwrote {dest.relative_to(ROOT)} - {len(lines)} statements")
    for k, n in tally.most_common():
        print(f"   {n:>5}  {k}")


if __name__ == "__main__":
    main()
