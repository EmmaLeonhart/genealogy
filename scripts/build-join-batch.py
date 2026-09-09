"""The thing that consumes the synoptic correspondence: Geni facts onto joined items.

    python scripts/build-join-batch.py --scope reports/izumo-roster.tsv

**Emma, 2026-08-24, asked whether this existed and it did not.**
`reports/synoptic-correspondence.tsv` holds 522,086 Geni ID ↔ QID pairs from five
sources and was read by nothing — the entry point of the whole programme, built and
inert. Her decision: *"A generic emitter but ... run scoped to Izumo first."*

**Both join directions count, jointly.** Emma, same day: *"geni description qid to
wikidata qid is also important and needs to be done jointly in the synoptic tree
building."* The correspondence already carries both — `wikidata-p2600` (517,823, the
`P2600` *Geni.com profile ID* statement on the Wikidata side) and `geni-about-me` (405,
the QID she wrote into the Geni description) — and this reads the joined file rather
than either source alone.

**The order is hers and it is not cosmetic.** `CLAUDE.md` § *An item with no
relationships is not a missing item*: *"The Jenny ID needs to be present before any
properties derived from Jenny can be taken from it."* So `P2600` is emitted first for
each person, and every derived statement carries `S2600` — that same Geni ID — as its
reference.

**Only what Wikidata lacks.** The purpose is to ADD, not to correct: a property the item
already states is skipped, never overwritten, and a disagreement is left alone. What the
item holds is read from the downloaded full items, never from a summary of them and never
from the local store, which predates Emma's edits.

**The single-run rule applies here too.** A relationship is emitted only when the target
already has a QID; nothing points at an item this batch is creating, because this batch
creates nothing at all. Everyone it touches exists on both sides already.

Writes `reports/wikidata-join-<scope>.qs` and a `.tsv` of what was skipped and why.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent

#: `CLAUDE.md` § Wikidata properties and items.
GENI_ID = "P2600"        # Geni.com profile ID
SEX = "P21"              # sex or gender
MALE, FEMALE = "Q6581097", "Q6581072"
BIRTH, DEATH = "P569", "P570"      # date of birth / date of death
FATHER, MOTHER = "P22", "P25"      # father / mother
SPOUSE, CHILD, SIBLING = "P26", "P40", "P3373"


def load_items(paths):
    """`{qid: item}` from the downloaded full items. Later files win."""
    out = {}
    for path in paths:
        p = ROOT / path
        if p.exists():
            out.update(json.loads(p.read_text(encoding="utf-8")))
    return out


def load_scope(path):
    """The QIDs to restrict to. Any file with a `qid` column, delimiter guessed."""
    text = (ROOT / path).read_text(encoding="utf-8")
    delim = "\t" if "\t" in text.splitlines()[0] else ","
    return {row["qid"].strip()
            for row in csv.DictReader(text.splitlines(), delimiter=delim)
            if (row.get("qid") or "").strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", required=True,
                    help="a file with a qid column; the batch is restricted to those")
    ap.add_argument("--name", help="output name (default: the scope file's stem)")
    args = ap.parse_args()

    scope = load_scope(args.scope)
    name = args.name or Path(args.scope).stem.replace("-roster", "")
    items = load_items(["out/clan-full-items.json", "out/izumo-full-items.json",
                        "out/garborg-full-items.json"])
    print(f"scope {len(scope)} QIDs; {len(items)} downloaded items available")

    # -- the join, both directions, from the one correspondence ---------------
    geni_of = collections.defaultdict(set)
    with open(ROOT / "reports" / "synoptic-correspondence.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["qid"] in scope:
                geni_of[row["qid"]].add(row["geni_id"])
    print(f"{len(geni_of)} of them are joined to a Geni profile")

    qid_of = {}
    for qid, gids in geni_of.items():
        for gid in gids:
            qid_of.setdefault(gid, qid)

    wanted = set(qid_of)
    facts, family = {}, {}
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in wanted:
                facts[row["geni_id"]] = row
    # The relatives' Geni ids are needed too, to look their QIDs up in the join.
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in wanted:
                family[row["geni_id"]] = row

    # Siblings: everyone sharing a father or a mother. Computed from the rows we
    # already hold rather than a second pass over 1.3M people.
    by_parent = collections.defaultdict(set)
    for gid, row in family.items():
        for parent in ((row.get("father") or "").strip(),
                       (row.get("mother") or "").strip()):
            if parent:
                by_parent[parent].add(gid)

    lines, skipped = [], []
    lines += [
        f"# Geni facts onto items that ALREADY exist and are ALREADY joined -- {name}.",
        "# Nothing is created. Every subject and every value has a QID already, so this",
        "# runs in one pass. P2600 goes first for each person: the Geni ID must be",
        "# present before anything derived from Geni is added.",
        "",
    ]

    counts = collections.Counter()
    for qid in sorted(geni_of, key=lambda q: int(q[1:])):
        item = items.get(qid)
        if not item:
            skipped.append((qid, "", "not downloaded, so what it holds is unknown"))
            continue
        claims = set(item.get("claims", {}))
        gids = sorted(geni_of[qid])
        gid = gids[0]
        fact, fam = facts.get(gid, {}), family.get(gid, {})

        block = []

        def ref():
            return f'\tS2600\t"{gid}"'

        # 1. The Geni ID first, and every id we hold -- P2600 is multi-valued and a
        #    second one is not a conflict (CLAUDE.md).
        present = {s.get("mainsnak", {}).get("datavalue", {}).get("value")
                   for s in item.get("claims", {}).get(GENI_ID, [])}
        for one in gids:
            if one not in present:
                block.append(f'{qid}\t{GENI_ID}\t"{one}"')
                counts[GENI_ID] += 1

        # 2. Sex and dates, only where absent.
        if SEX not in claims and fact.get("sex") in ("M", "F"):
            block.append(f"{qid}\t{SEX}\t{MALE if fact['sex'] == 'M' else FEMALE}{ref()}")
            counts[SEX] += 1
        for prop, iso, prec in ((BIRTH, fact.get("birth_date_iso"),
                                 fact.get("birth_date_precision")),
                                (DEATH, fact.get("death_date_iso"),
                                 fact.get("death_date_precision"))):
            if prop not in claims and iso and prec:
                block.append(f"{qid}\t{prop}\t{iso}/{prec}{ref()}")
                counts[prop] += 1

        # 3. Relationships, only where the other end already has a QID.
        for prop, column in ((FATHER, "father"), (MOTHER, "mother")):
            other = (fam.get(column) or "").strip()
            target = qid_of.get(other) or (fam.get(f"{column}_qid") or "").strip()
            if prop not in claims and target and target in items:
                block.append(f"{qid}\t{prop}\t{target}{ref()}")
                counts[prop] += 1

        stated = {p: {s.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
                      for s in item.get("claims", {}).get(p, [])}
                  for p in (SPOUSE, CHILD, SIBLING)}

        for other in sorted(x for x in (fam.get("spouses") or "").split() if x):
            target = qid_of.get(other)
            if target and target in items and target not in stated[SPOUSE]:
                block.append(f"{qid}\t{SPOUSE}\t{target}{ref()}")
                counts[SPOUSE] += 1
        for other in sorted(x for x in (fam.get("children") or "").split() if x):
            target = qid_of.get(other)
            if target and target in items and target not in stated[CHILD]:
                block.append(f"{qid}\t{CHILD}\t{target}{ref()}")
                counts[CHILD] += 1
        for parent in ((fam.get("father") or "").strip(),
                       (fam.get("mother") or "").strip()):
            for other in sorted(by_parent.get(parent, ())):
                if other == gid:
                    continue
                target = qid_of.get(other)
                if target and target in items and target not in stated[SIBLING]:
                    block.append(f"{qid}\t{SIBLING}\t{target}{ref()}")
                    stated[SIBLING].add(target)
                    counts[SIBLING] += 1

        if block:
            lines.extend(block + [""])
        else:
            skipped.append((qid, gid, "Wikidata already holds everything Geni supports"))

    out = ROOT / "reports" / f"wikidata-join-{name}.qs"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    tsv = ROOT / "reports" / f"wikidata-join-{name}-skipped.tsv"
    with open(tsv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["qid", "geni_id", "why"])
        w.writerows(skipped)

    total = sum(counts.values())
    print(f"\nwrote {out.relative_to(ROOT)}: {total} statements")
    for prop, n in counts.most_common():
        print(f"   {prop:<7} {n:>5}")
    print(f"\nwrote {tsv.relative_to(ROOT)}: {len(skipped)} people contributed nothing")


if __name__ == "__main__":
    main()
