"""One day's Garborg batch: everything that can run in a SINGLE QuickStatements run.

    python scripts/build-garborg-day.py

**Emma, 2026-08-24, after running yesterday's file:** *"I only ran some of the quick
statements because many of them required links that couldn't exist... The siblings all
being connected to each other: they should be connected to each other, but they
couldn't be connected to each other without things that required their QIDs, which we
had just created. This means this is going to be the practical limitation of what our
quick statements can do. With every day, we are kind of going through a full run of
what we can do on the frontier like this."*

So the rule is: **a statement goes in only if both ends already have a QID.** Nothing
deferred, nothing commented out, nothing that fails. What could not run today becomes
tomorrow's batch, because tomorrow those items exist.

`reports/garborg-qids.tsv` is the ledger of who has one. It is filled from **Emma's
Wikidata contributions**, not from a bulk download — her instruction: *"You should be
looking at my contributions to see the new ones I've created."* Her account is 日巫女.

Each day therefore does three things, all runnable:

1. **Close the links that yesterday's creations made possible** — the reciprocal `P40`
   from the parents, and `P3373` among siblings who all have QIDs now.
2. **Create the next ring**, everyone one edge away from someone who has a QID.
3. **Link the new people to anything that already exists** — parents, spouses,
   siblings — but never to each other, because they are being minted right now.

Labels come with `ja` and `zh` from `reports/garborg-name-transliterations.tsv`, per
Emma 2026-08-24: *"we should also be adding their names in languages that are not
English, or at least in Japanese... and Chinese."*

Writes `reports/wikidata-garborg-day.qs` and `reports/garborg-carry-forward.tsv`.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
csv.field_size_limit(1 << 30)
sys.stdout.reconfigure(encoding="utf-8")

from namemodel import classify, load_plan, statements_for  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SEX = {"M": "Q6581097", "F": "Q6581072"}
HUMAN = "Q5"


def qs(text):
    """QuickStatements V1 cannot escape a double quote inside a string."""
    return (text or "").replace('"', "").strip()


def ledger():
    out = {}
    with open(ROOT / "reports" / "garborg-qids.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[row["geni_id"]] = row["qid"]
    return out


def translit():
    out = {}
    with open(ROOT / "reports" / "garborg-name-transliterations.tsv",
              encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[row["token"]] = (row["ja"], row["zh"])
    return out


def read_tree():
    fam_p = collections.defaultdict(list)
    fam_c = collections.defaultdict(list)
    fams = collections.defaultdict(list)
    famc = collections.defaultdict(list)
    cur = kind = None
    with open(ROOT / "out" / "merged.ged", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("0 @"):
                p = line.split()
                cur, kind = p[1][2:-1], (p[2].strip() if len(p) > 2 else "")
            elif cur and line.startswith("1 "):
                tag, _, val = line[2:].strip().partition(" ")
                if kind == "FAM":
                    if tag in ("HUSB", "WIFE"):
                        fam_p[cur].append(val[2:-1])
                    elif tag == "CHIL":
                        fam_c[cur].append(val[2:-1])
                elif kind == "INDI":
                    if tag == "FAMS":
                        fams[cur].append(val[2:-1])
                    elif tag == "FAMC":
                        famc[cur].append(val[2:-1])
    return fam_p, fam_c, fams, famc


def label_in(label, table):
    """(ja, zh) for a whole name, or (None, None) if any token is unknown.

    Partial is worse than absent: half a name in katakana and half in Latin is not a
    Japanese label, it is a broken one.
    """
    ja, zh = [], []
    for token, _usage, _o in classify(label):
        pair = table.get(token)
        if not pair:
            return None, None
        ja.append(pair[0])
        zh.append(pair[1])
    return "・".join(ja), "·".join(zh)


def name_lines(label, plan, geni_id, father_qid):
    """`P735`/`P734`/`P5056` lines for one person, and what could not be emitted.

    **Only tokens whose item already exists.** A name item this run is creating
    cannot be pointed at, same single-run rule as everybody else, so the rest waits
    for `reports/wikidata-garborg-name-items.qs` to have been run.

    QuickStatements takes qualifiers exactly like references, property then value on
    the same line: `LAST<TAB>P735<TAB>Q629347<TAB>P1545<TAB>"1"<TAB>P7452<TAB>Q3409033`.
    """
    out, notes = [], []
    lines, why = statements_for(label, plan, geni_id, father_qid=father_qid)
    for prop, value, quals in lines:
        parts = [f"LAST	{prop}	{value}"]
        for qprop, qvalue in quals:
            # A series ordinal is a string; everything else here is an item.
            qv = f'"{qvalue}"' if qprop == "P1545" else qvalue
            parts.append(f"{qprop}	{qv}")
        out.append("	".join(parts))
    notes.extend(why)
    return out, notes


def main():
    have = ledger()
    table = translit()
    plan = load_plan()
    fam_p, fam_c, fams, famc = read_tree()
    print(f"{len(have)} people already carry a QID; {len(table)} tokens transliterated")

    # Everyone one edge away from somebody who has a QID.
    frontier = {}
    for person in have:
        for fam in fams.get(person, []) + famc.get(person, []):
            for other in set(fam_p.get(fam, [])) | set(fam_c.get(fam, [])):
                if other not in have:
                    frontier.setdefault(other, fam)
    print(f"{len(frontier)} people one edge away and not yet on Wikidata")

    ids = set(frontier) | set(have)
    facts, labels = {}, {}
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                facts[row["geni_id"]] = row
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                labels[row["geni_id"]] = row["label_en"] or row["label_mul"]

    # Relationships, from the tree, in both directions.
    father, mother = {}, {}
    children = collections.defaultdict(set)
    spouses = collections.defaultdict(set)
    siblings = collections.defaultdict(set)
    for fam, parents in fam_p.items():
        kids = fam_c.get(fam, [])
        for p in parents:
            for k in kids:
                children[p].add(k)
                sex = (facts.get(p, {}).get("sex") or "")
                (father if sex == "M" else mother)[k] = p
        for a in parents:
            for b in parents:
                if a != b:
                    spouses[a].add(b)
        for a in kids:
            for b in kids:
                if a != b:
                    siblings[a].add(b)

    lines, carried = [], []

    def ref(g):
        return f'\tS2600\t"{g}"'

    # ---- 1. links between people who ALL already have QIDs ------------------
    lines += [
        "# 1. Links that only became possible once yesterday's items existed.",
        "#    Every subject and every value already has a QID.",
        "",
    ]
    seen = set()
    for g, q in sorted(have.items()):
        for kid in sorted(children.get(g, ())):
            if kid in have and (q, "P40", have[kid]) not in seen:
                seen.add((q, "P40", have[kid]))
                lines.append(f"{q}\tP40\t{have[kid]}{ref(g)}")
        for sib in sorted(siblings.get(g, ())):
            if sib in have and (q, "P3373", have[sib]) not in seen:
                seen.add((q, "P3373", have[sib]))
                lines.append(f"{q}\tP3373\t{have[sib]}{ref(g)}")
        for sp in sorted(spouses.get(g, ())):
            if sp in have and (q, "P26", have[sp]) not in seen:
                seen.add((q, "P26", have[sp]))
                lines.append(f"{q}\tP26\t{have[sp]}{ref(g)}")
    print(f"{len(seen)} links between existing items")
    lines.append("")

    # ---- 2. the next ring ---------------------------------------------------
    lines += ["# 2. The next ring. Each is linked only to items that already exist;",
              "#    links between two of these wait for tomorrow, when they have QIDs.",
              ""]
    created = 0
    for g in sorted(frontier, key=lambda x: labels.get(x, "")):
        f, label = facts.get(g), qs(labels.get(g, ""))
        if not f:
            carried.append((g, label, "no derived facts"))
            continue

        # A redacted profile is created and gets NO label. `CLAUDE.md`: *"Private is
        # a redaction marker, not a name, and an item labelled that asserts something
        # false while being impossible to find. The P2600 is what makes it
        # retrievable."* The person is real and none of the structure is redacted —
        # the Geni id, the sex, the parents, the dates all come through.
        low = label.lower()
        redacted = "<private>" in low or low.startswith("private")

        lines.append("CREATE")
        if redacted or not label:
            carried.append((g, label, "redacted: created, deliberately unlabelled"))
        else:
            lines.append(f'LAST\tLen\t"{label}"')
            lines.append(f'LAST\tLmul\t"{label}"')
            ja, zh = label_in(labels[g], table)
            if ja:
                lines.append(f'LAST\tLja\t"{ja}"')
                lines.append(f'LAST\tLzh\t"{zh}"')
            else:
                carried.append((g, label, "no transliteration for every token"))
        lines.append(f"LAST\tP31\t{HUMAN}")
        if f["sex"] in SEX:
            lines.append(f"LAST\tP21\t{SEX[f['sex']]}")
        lines.append(f'LAST\tP2600\t"{g}"')
        for prop, iso, prec in (("P569", f["birth_date_iso"], f["birth_date_precision"]),
                                ("P570", f["death_date_iso"], f["death_date_precision"])):
            if iso and prec:
                lines.append(f"LAST\t{prop}\t{iso}/{prec}{ref(g)}")
        for prop, target in (("P22", father.get(g)), ("P25", mother.get(g))):
            if target and target in have:
                lines.append(f"LAST\t{prop}\t{have[target]}{ref(g)}")
        for sp in sorted(spouses.get(g, ())):
            if sp in have:
                lines.append(f"LAST\tP26\t{have[sp]}{ref(g)}")
        for sib in sorted(siblings.get(g, ())):
            if sib in have:
                lines.append(f"LAST\tP3373\t{have[sib]}{ref(g)}")
        for kid in sorted(children.get(g, ())):
            if kid in have:
                lines.append(f"LAST\tP40\t{have[kid]}{ref(g)}")

        # The name model. Emma, 2026-08-24: *"we should be modelling the names
        # properly, which he didn't do."* Only tokens whose item ALREADY exists --
        # the ones still to be made are in reports/wikidata-garborg-name-items.qs and
        # join the batch the day after that runs, same single-run rule as everyone.
        dad = father.get(g)
        name_statements, unresolved = name_lines(
            labels[g], plan, g, have.get(dad) if dad else None)
        lines.extend(name_statements)
        for note in unresolved:
            carried.append((g, label, f"name item missing: {note}"))

        lines.append("")
        created += 1

    out = ROOT / "reports" / "wikidata-garborg-day.qs"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out.relative_to(ROOT)}: {created} creations, {len(seen)} links")

    cf = ROOT / "reports" / "garborg-carry-forward.tsv"
    with open(cf, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["geni_id", "label", "why"])
        w.writerows(carried)
    print(f"wrote {cf.relative_to(ROOT)}: {len(carried)} carried to a later day")
    for g, label, why in carried[:10]:
        print(f"  {g}  {label[:40]:<40} {why}")


if __name__ == "__main__":
    main()
