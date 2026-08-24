"""The daily Garborg batch: one hop further out from Arne, each time.

    python scripts/build-garborg-hop.py 2

**Emma's programme, 2026-08-23.** *"We were supposed to every day have our own
Garborg qs batch kind of extending off of him by 1 each time... We are testing the
waters for a later geni bot automation."* Asked what one step means, she chose **one
hop of the tree per day**: everybody at the next distance from Arne — his siblings,
then their spouses and children, then the grandparents, and outward.

**Hop 1** is `reports/wikidata-garborg.qs`: the parents and the nine siblings.
**Hop 2** is this: their spouses and children, and Arne's four grandparents.

The shape of each item is `docs/wikidata-item-template.md`, read off the items Emma
built by hand — `S2600` references on dates and relationships, nothing on identity,
no descriptions, `P3373` both ways.

**Nobody who already has an item is created.** That rule has caught a duplicate twice
in two days: the first Garborg batch would have re-created Eivind and Ane Oline, and
ten of the eleven Izumo office-holders past the chart already had items. Existing QIDs
come from the About Me links and from the local `P2600` snapshot, and both are checked
before a `CREATE` is written.

**A link is only emitted when its target already has a QID.** QuickStatements V1
cannot point at an item a `CREATE` in the same run has just minted, so a nephew whose
parent is still a hop-1 creation goes to the commented second pass rather than being
guessed at.

Offline. Reads `out/merged.ged`, `reports/derived-facts.csv`,
`reports/derived-labels.csv`, `reports/geni-qid-links.tsv` and
`out/wikidata/p2600-all.tsv`. Writes `reports/wikidata-garborg-hop<N>.qs`.
"""
from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

csv.field_size_limit(1 << 30)
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

ARNE = "6000000003492005116"

#: Hop 0 and hop 1: Arne, his parents, his nine siblings. Their QIDs where known —
#: the four Emma created by hand plus Arne's own.
CORE = {
    "6000000003492005116": "Q467497",       # Aadne (Arne) Eivindson Garborg
    "6000000003492005111": "Q141152512",    # Eivind, father
    "6000000003491986946": "Q141152523",    # Ane Oline, mother
    "6000000003492005121": "Q141152600",    # Stena
    "6000000003492005126": "Q141152614",    # Jon
    "6000000003492005131": None,            # Samuel      -- hop 1 CREATE
    "6000000003492005136": None,            # Even
    "6000000003492005141": None,            # Inger Marie
    "6000000003492005146": None,            # Abel
    "6000000003492005151": None,            # Ole
    "6000000003492005156": None,            # Ane Oline "Lena"
}
PARENTS = ["6000000003492005111", "6000000003491986946"]
SEX = {"M": "Q6581097", "F": "Q6581072"}
HUMAN = "Q5"


def qs_string(text):
    """QuickStatements V1 cannot escape a double quote inside a string."""
    return (text or "").replace('"', "").strip()


def read_tree():
    fam_p = collections.defaultdict(list)
    fam_c = collections.defaultdict(list)
    fams = collections.defaultdict(list)
    famc = collections.defaultdict(list)
    name = {}
    cur = kind = None
    with open(ROOT / "out" / "merged.ged", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("0 @"):
                p = line.split()
                cur = p[1][2:-1]
                kind = p[2].strip() if len(p) > 2 else ""
            elif cur and line.startswith("1 "):
                tag, _, val = line[2:].strip().partition(" ")
                if kind == "FAM":
                    if tag in ("HUSB", "WIFE"):
                        fam_p[cur].append(val[2:-1])
                    elif tag == "CHIL":
                        fam_c[cur].append(val[2:-1])
                elif kind == "INDI":
                    if tag == "NAME" and cur not in name:
                        name[cur] = val.strip()
                    elif tag == "FAMS":
                        fams[cur].append(val[2:-1])
                    elif tag == "FAMC":
                        famc[cur].append(val[2:-1])
    return fam_p, fam_c, fams, famc, name


def known_qids():
    """geni id -> QID, from the About Me links and the local P2600 snapshot."""
    out = {}
    snap = ROOT / "out" / "wikidata" / "p2600-all.tsv"
    if snap.exists():
        with open(snap, encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="\t"):
                if len(row) >= 2 and row[0].startswith("Q"):
                    out.setdefault(row[1].strip(), row[0].strip())
    links = ROOT / "reports" / "geni-qid-links.tsv"
    if links.exists():
        with open(links, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                qids = [q for q in row["qids"].split(";") if q]
                if qids:
                    out.setdefault(row["geni_id"], qids[0])
    return out


def frontier(hop, fam_p, fam_c, fams, famc):
    """(geni id -> why) for everybody at distance `hop` from the core."""
    if hop != 2:
        raise SystemExit("only hop 2 is defined so far; hop 1 is "
                         "reports/wikidata-garborg.qs")
    out = {}
    for person in CORE:
        for fam in fams.get(person, []):
            for spouse in fam_p.get(fam, []):
                if spouse != person:
                    out.setdefault(spouse, ("P26", person))
            for child in fam_c.get(fam, []):
                out.setdefault(child, ("child", person))
    for parent in PARENTS:
        for fam in famc.get(parent, []):
            for gp in fam_p.get(fam, []):
                out.setdefault(gp, ("parent", parent))
    return {g: why for g, why in out.items() if g not in CORE}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hop", type=int, nargs="?", default=2)
    args = ap.parse_args()

    fam_p, fam_c, fams, famc, name = read_tree()
    people = frontier(args.hop, fam_p, fam_c, fams, famc)
    print(f"hop {args.hop}: {len(people)} people")

    facts = {r["geni_id"]: r for r in csv.DictReader(
        open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8"))
        if r["geni_id"] in people}
    labels = {r["geni_id"]: r for r in csv.DictReader(
        open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8"))
        if r["geni_id"] in people}
    have = known_qids()

    lines, second, skipped = [], [], []
    lines.append(f"# Garborg hop {args.hop}: the spouses and children of Arne's "
                 f"siblings, and his grandparents.")
    lines.append("# Shape from docs/wikidata-item-template.md. S2600 references on "
                 "dates and links,")
    lines.append("# nothing on identity, no descriptions.")
    lines.append("")

    for gid, (why, anchor) in sorted(people.items(),
                                     key=lambda kv: name.get(kv[0], "")):
        if gid in have:
            skipped.append((gid, have[gid], name.get(gid, "")))
            continue
        f, lab = facts.get(gid), labels.get(gid)
        if not f or not lab:
            skipped.append((gid, "no derived facts", name.get(gid, "")))
            continue
        label = qs_string(lab.get("label_en") or lab.get("label_mul"))
        if not label:
            skipped.append((gid, "no label", name.get(gid, "")))
            continue
        ref = f'\tS2600\t"{gid}"'
        lines.append("CREATE")
        lines.append(f'LAST\tLen\t"{label}"')
        lines.append(f'LAST\tLmul\t"{label}"')
        lines.append(f"LAST\tP31\t{HUMAN}")
        if f["sex"] in SEX:
            lines.append(f"LAST\tP21\t{SEX[f['sex']]}")
        lines.append(f'LAST\tP2600\t"{gid}"')
        for prop, iso, prec in (("P569", f["birth_date_iso"], f["birth_date_precision"]),
                                ("P570", f["death_date_iso"], f["death_date_precision"])):
            if iso and prec:
                lines.append(f"LAST\t{prop}\t{iso}/{prec}{ref}")

        anchor_qid = CORE.get(anchor) or have.get(anchor)
        rel = {"P26": "P26", "child": None, "parent": None}[why]
        if why == "child":
            rel = "P22" if (facts.get(anchor, {}).get("sex")
                            or _sex_of(anchor)) == "M" else "P25"
        elif why == "parent":
            rel = "P40"
        if anchor_qid:
            if why == "child":
                lines.append(f"LAST\t{_parent_prop(anchor)}\t{anchor_qid}{ref}")
            elif why == "parent":
                # the hop-2 person is the PARENT of the anchor: they get P40.
                lines.append(f"LAST\tP40\t{anchor_qid}{ref}")
            else:
                lines.append(f"LAST\tP26\t{anchor_qid}{ref}")
        else:
            second.append((label, why, anchor, name.get(anchor, "")))
        lines.append("")

    lines.append("# --- second pass: targets that have no QID until hop 1 runs ---")
    for label, why, anchor, anchor_name in second:
        lines.append(f"# <{label}>\t{why}\t<{anchor_name}>  ({anchor})")
    lines.append("#")
    lines.append("# Reciprocals (P40 back from each parent, P26 back from each spouse)")
    lines.append("# also need the QIDs these CREATEs return.")

    out = ROOT / "reports" / f"wikidata-garborg-hop{args.hop}.qs"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    creations = lines.count("CREATE")
    print(f"wrote {out.relative_to(ROOT)}: {creations} creations, "
          f"{len(second)} links deferred")
    for gid, why, nm in skipped:
        print(f"  skipped {gid} {nm}: {why}")


_SEXES: dict = {}


def _sex_of(gid):
    return _SEXES.get(gid, "")


def _parent_prop(anchor):
    """P22 if the anchor is the father, P25 if the mother."""
    return "P22" if _SEXES.get(anchor) == "M" else "P25"


if __name__ == "__main__":
    # Sexes of the core, so a child's link picks P22 or P25 correctly.
    for _r in csv.DictReader(open(ROOT / "reports" / "derived-facts.csv",
                                  encoding="utf-8")):
        if _r["geni_id"] in CORE:
            _SEXES[_r["geni_id"]] = _r["sex"]
    main()
