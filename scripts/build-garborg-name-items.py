"""The name items the Garborg batches need and Wikidata does not have.

    python scripts/build-garborg-name-items.py

Emma, 2026-08-24: *"we should be modelling the names properly, which he didn't
do."* `P735` given name, `P734` family name and `P5056` patronym all point at
**items**, and a link cannot be written before the item exists.

**A patronymic is its own item even when the spelling already exists.**
`CLAUDE.md` § *One name item per USAGE*: `Eivindsen` has a Wikidata item as a given
name, and the patronymic `Eivindsen` is *"a different object"*. Her own `Q141152710`
*Aadnesson* is the pattern — labels, `P31` → `Q110874` *patronymic*, and nothing else.
That minimalism is copied deliberately: the measurement in `CLAUDE.md` found `P1705`,
`P282` and `P407` on most existing patronymic items and **she does not add them**.

**Ambiguous tokens are never created.** Where `reports/name-item-plan.csv` says a
token already resolves to several items — `Marie`, `Olga`, `Anton` — creating one more
is the `Maria` failure that would have made a tenth. They are listed for Emma instead.

**It no longer runs first and on its own, because the limit it was built around is not
real.** This file said *"QuickStatements V1 cannot point at an item a `CREATE` in the same
batch has just minted"*, and that is the same false generalisation `CLAUDE.md` records for
relationship links: `LAST` **is** how you point at what was just created. What cannot be done
is having two items created in one run cite *each other*. A name item and a person who already
exists are not two new items.

**Emma, 2026-08-26:** *"For every missing name the daily quickstatements generation should
generate the ones for existing items and in the generation run add it to the existing ones too
lol. Just like with people being linked on their relatives through QID PID LAST inverted of the
creation property setting LAST PID QID."*

So each `CREATE` is followed immediately by the statements that use it:

    CREATE
    LAST    Len     "Mjolhus"          <- the name item
    LAST    P31     Q101352
    Q141152600  P734  LAST  S2600 "…"  <- every EXISTING bearer, in the same run

The bearers are the people in `reports/garborg-qids.tsv` who already hold a QID; a person the
day batch is *creating* still cannot be linked here, because `LAST` would then name the person
rather than the name item. Those wait for the next run, which is the ordinary carry-forward and
not a gate.

Writes `reports/wikidata-garborg-name-items.qs`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
csv.field_size_limit(1 << 30)
sys.stdout.reconfigure(encoding="utf-8")

from namemodel import (  # noqa: E402
    PATRONYMIC_CLASS, classify_fields, load_plan, statements_for)
from qscomment import annotate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

#: `CLAUDE.md` § Wikidata properties and items.
INSTANCE_OF = "P31"
FAMILY_NAME_CLASS = "Q101352"     # family name
GIVEN_NAME_CLASS = "Q202444"      # given name

#: **10 name items a run.** Emma, 2026-08-26: *"generating 10 name items based upon the
#: missing name items from the ideal state, with the links as a thing that specifically is
#: made."* The cap is hers; WHICH ten is not specified, so the most-borne tokens go first --
#: that maximises the links each created item earns in the same run. Rejected: taking them at
#: random, which would leave a nine-bearer surname waiting behind a one-bearer one for no
#: reason. Falsified if she says the choice should be random, as the parent pairs are.
NAME_ITEMS_PER_RUN = 10

CLASS_FOR = {
    "patronymic": PATRONYMIC_CLASS,
    "family": FAMILY_NAME_CLASS,
    "given": GIVEN_NAME_CLASS,
}

#: The live day batch. The earlier `wikidata-garborg.qs` and `-hop2.qs` were retired
#: on 2026-08-24: their creations are recorded in `reports/garborg-qids.tsv` and
#: re-running them would mint duplicates, which
#: `test_no_two_batches_create_the_same_person` caught.
BATCHES = ["reports/wikidata-garborg-day.qs"]


def people_in_batches():
    ids = set()
    for rel in BATCHES:
        path = ROOT / rel
        if path.exists():
            ids |= set(re.findall(r'P2600\t"(\d+)"',
                                  path.read_text(encoding="utf-8")))
    return ids


def ledger():
    """The people who ALREADY hold a QID -- the only ones a `LAST` statement can name."""
    out = {}
    path = ROOT / "reports" / "garborg-qids.tsv"
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="	"):
            if (row.get("qid") or "").startswith("Q") and (row.get("geni_id") or "").isdigit():
                out[row["geni_id"]] = row["qid"]
    return out


def main():
    ids = people_in_batches()
    have = ledger()
    print(f"{len(ids)} people across {len(BATCHES)} Garborg batches, "
          f"{len(have)} already holding a QID")
    # The token scan covers BOTH populations: the people being created (so the item
    # exists by the time they are linked on a later day) and the people who already
    # hold a QID (so they are linked in this very run).
    ids = ids | set(have)

    # **The GEDCOM name FIELDS, not the rendered label.** Emma, 2026-08-24, caught the
    # name model re-parsing a display string; this file was still doing it after the
    # model was fixed, which mattered more here than anywhere else. It gates every
    # other batch, so a wrong list means she creates items nobody needs and lacks ones
    # that are needed: nicknames stopped needing an item at all (`P1449` takes text)
    # and married surnames started needing one.
    fields = {}
    with open(ROOT / "reports" / "display-names.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids and row["geni_id"] not in fields:
                fields[row["geni_id"]] = {k: row.get(k, "") for k in
                                          ("givn", "surn", "nick", "marnm")}

    labels_of, father_of, sex_of = {}, {}, {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                labels_of[row["geni_id"]] = row.get("label_en") or row.get("label_mul") or ""
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                # ` | ` is the repo's multi-value separator and the strip is load-bearing.
                first = [x.strip() for x in (row.get("father") or "").split("|") if x.strip()]
                if first:
                    father_of[row["geni_id"]] = first[0]
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                sex_of[row["geni_id"]] = row.get("sex", "")

    plan = load_plan()
    need = collections.Counter()
    ambiguous = collections.Counter()
    linked = collections.Counter()
    for person in fields.values():
        for token, usage, _ordinal in classify_fields(**person):
            # A nickname is monolingual text on the person's own item, so it needs no
            # name item and must not be proposed as one.
            if usage == "nickname":
                continue
            # A married surname is a family name like any other -- same item kind, same
            # lookup -- it just reaches the person by a different field.
            usage = "family" if usage == "married" else usage
            qid, action = plan.get((token, usage), ("", "not in the plan"))
            if qid:
                linked[(token, usage)] += 1
            elif "AMBIG" in action.upper():
                ambiguous[(token, usage)] += 1
            else:
                need[(token, usage)] += 1

    print(f"{len(linked)} tokens already have an item and are linked, not created")
    print(f"{len(need)} need creating, {len(ambiguous)} are ambiguous and are not")

    lines = [
        "# Name items the Garborg batches need, AND the statements that use them.",
        "#",
        "# Each CREATE is followed by `Qperson  Pprop  LAST` for every bearer who",
        "# ALREADY holds a QID -- LAST is exactly how you point at what was just",
        "# created. A person this run is also CREATING cannot be linked here, because",
        "# LAST would then name the person; they wait for the next run.",
        "#",
        "# A patronymic is its own item even where the spelling exists as a given",
        "# name: CLAUDE.md, one name item per USAGE. Emma's Q141152710 Aadnesson is",
        "# the pattern -- labels, P31, nothing else.",
        "",
    ]
    ranked = sorted(need.items(), key=lambda kv: (-kv[1], kv[0]))
    held_back = ranked[NAME_ITEMS_PER_RUN:]
    linked_now = 0
    for (token, usage), bearers in ranked[:NAME_ITEMS_PER_RUN]:
        lines.append(f"# {token} -- {usage}, {bearers} bearer(s) in the batches")
        lines.append("CREATE")
        lines.append(f'LAST\tLen\t"{token}"')
        lines.append(f'LAST\tLmul\t"{token}"')
        lines.append(f"LAST\t{INSTANCE_OF}\t{CLASS_FOR[usage]}")
        # **The statements that use it, in the same run.** The name model is run with
        # this ONE token pointed at `LAST` and every other token left at its real QID,
        # so only the statement about the item just created comes back carrying `LAST`,
        # and it lands under that item's own `CREATE`.
        #
        # A person with several created names therefore gets one line in each of those
        # blocks, and those lines are TEXTUALLY IDENTICAL while meaning different things:
        # `Q141168787 P734 LAST` appears under *Tunheim*, *Bring* and *Iverson*. That is
        # correct and `tests/test_p2600_batches.py` had to learn it -- it already knew
        # `LAST` as a SUBJECT is scoped to its block and did not know the same of `LAST`
        # as a value.
        for geni_id, qid in sorted(have.items()):
            person = fields.get(geni_id)
            if not person:
                continue
            if not any(t == token and (u if u != "married" else "family") == usage
                       for t, u, _o in classify_fields(**person)):
                continue
            local = dict(plan)
            local[(token, usage)] = ("LAST", "created immediately above")
            if usage == "family":
                local[(token, "married")] = ("LAST", "created immediately above")
            dad = father_of.get(geni_id)
            try:
                sts, _notes = statements_for(
                    labels_of.get(geni_id, ""), local, geni_id,
                    father_qid=have.get(dad) if dad else None,
                    fields=person, sex=sex_of.get(geni_id, ""))
            except Exception as exc:                                   # noqa: BLE001
                lines.append(f"#   {qid}: the name model failed -- {exc}")
                continue
            for prop, value, quals in sts:
                if value != "LAST":
                    continue
                tail = "".join(f"\t{qp}\t{qv}" for qp, qv in quals)
                lines.append(f'{qid}\t{prop}\tLAST{tail}\tS2600\t"{geni_id}"')
                linked_now += 1
        lines.append("")

    if held_back:
        lines.append(f"# {len(held_back)} more name items are needed and wait for a later")
        lines.append(f"# run -- {NAME_ITEMS_PER_RUN} a day is her cap, not a limit of the data:")
        for (token, usage), n in held_back[:12]:
            lines.append(f"#   {token} ({usage}), {n} bearer(s)")
        if len(held_back) > 12:
            lines.append(f"#   ... and {len(held_back) - 12} more")
        lines.append("")

    if ambiguous:
        lines.append("# NOT created -- the plan says these already resolve to more than")
        lines.append("# one item, and creating another is the Maria failure that would")
        lines.append("# have made a tenth. Emma picks, the person's sex decides.")
        for (token, usage), bearers in sorted(ambiguous.items()):
            lines.append(f"#   {token} ({usage}), {bearers} bearer(s)")

    # A comment above every line, the same post-pass the day batch uses. Emma, 2026-08-26:
    # *"Every line has a comment the line above it saying what change is happening."*
    # `name_of` turns a QID back into the person it belongs to, so a link reads as a
    # sentence rather than as two numbers.
    qid_to_geni = {q: g for g, q in have.items()}
    lines = annotate(lines, lambda t: labels_of.get(qid_to_geni.get(t, t), ""))

    out = ROOT / "reports" / "wikidata-garborg-name-items.qs"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"\nwrote {out.relative_to(ROOT)}: {lines.count('CREATE')} name items "
          f"(cap {NAME_ITEMS_PER_RUN}, {len(held_back)} carried to a later run), "
          f"{linked_now} statements linking an EXISTING person to one, in the same run")
    for (token, usage), n in sorted(need.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  create  {token:<20} {usage:<12} {n}")
    for (token, usage), n in sorted(ambiguous.items()):
        print(f"  AMBIG   {token:<20} {usage:<12} {n}")


if __name__ == "__main__":
    main()
