"""Add an `S2600` source to relationship statements that already exist WITHOUT one.

Ruled 2026-09-14, as the second vehicle for growing the universe:

> *"adding sources on individuals for existing relationships for the people adjacent to the
> universe. That's another thing, because our universe doesn't really expand itself past the
> people we're creating and that's a bit of a problem."*

**Everything WE emit is already sourced** -- checked 2026-09-14 on the live batch: `P22` 48/48,
`P25` 48/48, `P40` 100/100, `P26` 52/52, `P3373` 6/6, every one carrying `S2600`. The gap runs
the other way: relationships already on Wikidata, put there by somebody else or by us before the
rule, carrying **no reference at all**. Adding one is the same true-and-missing edit as `P1810`.

## THE POINT IS THE UNIVERSE GROWING, NOT THE REFERENCES

Ruled 2026-09-14: *"we are applying this to adjacent individuals to the universe. And these
adjacent individuals get added into the universe because of the fact that we just did an edit on
it. That's the entire point."*

    source a relationship on an adjacent item
      -> the item is now in the account's contributions
      -> the next ledger refresh puts it in garborg-qids.tsv
      -> wikidata_subgraph counts it as universe
      -> ITS neighbours become the new adjacent ring

And the vehicle is chosen for being harmless: *"it isn't even that important as a qualifier. It's
just a thing that none of them have. And so it means we can add it to all of them and it's
useful."*

## A SOURCE IS A CLAIM ABOUT THE SOURCE, SO THE RELATIONSHIP MUST BE IN OUR TREE

**This is the one place this script is stricter than the `P1810` backfill, and it has to be.**
`S2600` says *Geni states this*. Attaching it to a relationship Geni does not state is not a
harmless missing statement, it is a false citation -- and unlike a wrong label nobody can tell by
looking, because the reference renders as a tidy Geni link either way.

So every line is checked against `reports/derived-family.csv` first: the father, mother, spouse
or child must actually be that person in **our** tree, joined on the Geni id per CLAUDE.md
section *The Geni profile ID is the primary key*. A relationship Wikidata holds and Geni does not
is left alone -- it may well be right, it is simply not something Geni can be cited for.

Siblings are computed rather than read: `derived-family.csv` has no sibling column, so a sibling
is somebody sharing a father or a mother. That is also what Geni means by one.

**Both ends must be resolvable to a Geni id.** The subject's comes from the ledger, or from the
item's own `P2600` when it is an adjacent item we have never edited; the value's the same way.
An item with no `P2600` cannot be cited to Geni at all and is skipped.

## LOCALITY AND PACE, both unchanged from the P1810 backfill

CLAUDE.md section *ONLY EVER EDIT THINGS IN THE UNIVERSE OR ONE STEP ADJACENT TO IT*. Wikidata
holds 518,975 `P2600` holders and a backfill is exactly the shape of edit that could quietly
touch all of them. Scope is `reports/garborg-qids.tsv` plus the QIDs those items point at
through `P22`/`P25`/`P26`/`P40`/`P3373` in `reports/garborg-live-values.tsv`.

And the pace is the ruled one -- *"it's not supposed to be by a ring. By a ring is fucking insane
... let's say 40 people in the quick statements batch and then 20 people in the CICD edits."*

## Re-stating the statement is how a reference is added

QuickStatements V1 has no *add a source to this existing statement* verb. Emitting
`Q123<TAB>P22<TAB>Q456<TAB>S2600<TAB>"6000..."` matches the existing statement on
property-and-value and attaches the reference to it; it does not create a second `P22`.

    BOT_CONTACT=you@example.com PYTHONPATH=src python scripts/build-relationship-sources-backfill.py

Writes `reports/wikidata-relationship-sources.qs` and `-auto.qs`.
"""

from __future__ import annotations

import csv
import gzip
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from live_name_items import _get as api_get  # noqa: E402

LEDGER = REPO / "reports" / "garborg-qids.tsv"
LIVE = REPO / "reports" / "garborg-live-values.tsv"
FAMILY = REPO / "reports" / "derived-family.csv"
OUT = REPO / "reports" / "wikidata-relationship-sources.qs"
AUTO_OUT = REPO / "reports" / "wikidata-relationship-sources-auto.qs"

AGENT = "geni-wikidata-relationship-sources"
NLJ = chr(10)
TAB = chr(9)

#: The relationship properties, and the English label beside each per CLAUDE.md section
#: *Always write the English label next to a property or item ID*.
RELATIONSHIPS = {
    "P22": "father",
    "P25": "mother",
    "P26": "spouse",
    "P40": "child",
    "P3373": "sibling",
}

#: The same properties make an item *adjacent* to the universe.
ADJACENT_VIA = tuple(RELATIONSHIPS)

#: **THE PACE, ruled 2026-09-14 and identical to the `P1810` backfill by design.** 60 a day,
#: the larger share for the file a person pastes and the smaller for the run that goes out
#: unattended. The universe grows because each edit makes an item ours, so an unpaced pass would
#: claim every neighbour at once -- thousands of items touched in a day by an account that had
#: touched none of them the day before.
MANUAL_CAP = 40
AUTO_CAP = 20

#: ⛔ **A FLOOR OF NEW BORDERING PEOPLE, EVERY RUN. Ruled 2026-09-14, and it is the POINT of the
#: pass rather than a detail of it:** *"Every run 10 new bordering people not in the universe but
#: connected to it get that as it."*
#:
#: **Without it the ring is never reached and the universe never grows.** The caps are 40 + 20
#: and the universe is queried first, so on any day with sixty spare rows among our own items the
#: quota fills before a single neighbour is looked at. Measured 2026-09-15 over all four emitted
#: files -- `subject-named-as` 39 people, `-auto` 20, `relationship-sources` 32, `-auto` 8 --
#: **adjacent people: 0, 0, 0 and 0.** The growth mechanism was doing nothing at all.
#:
#: Ordering our own items first is still right; the floor is what stops *first* meaning *only*.
#: Counted in PEOPLE, not statements, because the ruling says people and one item can need
#: several lines.
ADJACENT_FLOOR = 10


def qs(value: str) -> str:
    """A QuickStatements string literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def universe():
    """`{qid: geni_id}` for the account's own items."""
    out = {}
    with LEDGER.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=TAB):
            q, g = (row.get("qid") or "").strip(), (row.get("geni_id") or "").strip()
            if q.startswith("Q") and g:
                out[q] = g
    return out


def adjacent(core):
    """QIDs one relationship step from the universe, from the live-values file."""
    out = set()
    if not LIVE.exists():
        return out
    with LIVE.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=TAB):
            if (row.get("property") or "") not in ADJACENT_VIA:
                continue
            subj, val = (row.get("qid") or "").strip(), (row.get("value") or "").strip()
            if subj in core and val.startswith("Q"):
                out.add(val)
            elif val in core and subj.startswith("Q"):
                out.add(subj)
    return out - set(core)


def open_family():
    """`derived-family.csv`, gzipped or not.

    CLAUDE.md section *The four big derived CSVs are committed gzipped* -- a clean clone has
    only the `.gz` until `pack-derived.py --unpack` has run.
    """
    if FAMILY.exists():
        return FAMILY.open(encoding="utf-8", newline="")
    return io.TextIOWrapper(gzip.open(str(FAMILY) + ".gz"), encoding="utf-8")


def read_our_tree():
    """What GENI says, as `{geni_id: {property: {geni_id, ...}}}` plus the two parent maps.

    Only the relationships this script can cite are kept, and the parent maps come back
    separately because siblings are computed from them.

    **The separator is ` | `, spaces included** -- CLAUDE.md section *reports/derived-family.csv
    separates with ` | `*, where splitting it wrong made 379,251 people arrive childless. Split
    on whitespace after replacing the bar, so both the bar and the spaces are consumed.
    """
    csv.field_size_limit(1 << 30)
    father, mother = {}, {}
    tree = {}
    with open_family() as fh:
        for row in csv.DictReader(fh):
            g = row["geni_id"]
            dad = (row.get("father") or "").strip()
            mum = (row.get("mother") or "").strip()
            if dad:
                father[g] = dad
            if mum:
                mother[g] = mum
            spouses = {s for s in (row.get("spouses") or "").replace("|", " ").split() if s}
            children = {c for c in (row.get("children") or "").replace("|", " ").split() if c}
            entry = {}
            if dad:
                entry["P22"] = {dad}
            if mum:
                entry["P25"] = {mum}
            if spouses:
                entry["P26"] = spouses
            if children:
                entry["P40"] = children
            if entry:
                tree[g] = entry
    return tree, father, mother


def sibling_index(father, mother):
    """`{geni_id: {sibling geni_id, ...}}` -- somebody sharing a father or a mother.

    `derived-family.csv` carries no sibling column, and this is what Geni means by one. Built
    from the two parent maps rather than from the `children` column, so a half-sibling recorded
    on only one side is still found.
    """
    by_parent = {}
    for child, parent in list(father.items()) + list(mother.items()):
        by_parent.setdefault(parent, set()).add(child)
    out = {}
    for kids in by_parent.values():
        if len(kids) < 2:
            continue
        for kid in kids:
            out.setdefault(kid, set()).update(kids - {kid})
    return out


def main() -> int:
    core = universe()
    near = adjacent(core)
    print(f"universe: {len(core):,} items; adjacent: {len(near):,}")

    tree, father, mother = read_our_tree()
    siblings = sibling_index(father, mother)
    print(f"our tree: {len(tree):,} people with a relationship; "
          f"{len(siblings):,} with a sibling")

    # **STOP AS SOON AS THE DAY'S QUOTA IS FULL**, the same rule as the `P1810` backfill and for
    # the same reason: the scope is ten thousand items and the pace is 60 a day, so querying
    # everything to discard 99% of it spends twenty minutes of Wikidata's time for nothing.
    #
    # ⛔ **BUT IT RUNS AS TWO PASSES, AND THE SECOND ONE IS THE GROWTH MECHANISM.** Our own items
    # are queried first -- they are the ones we are certainly entitled to edit -- but only up to
    # `need - ADJACENT_FLOOR`, so the remainder is held open for the ring. A single pass over
    # `core + near` never reaches the ring at all: see `ADJACENT_FLOOR` for the measurement that
    # found all four emitted files at zero adjacent people.
    need = MANUAL_CAP + AUTO_CAP
    rows = []
    sourced = unattested = no_geni = no_value = 0

    def adjacent_people():
        return len({r[0] for r in rows} - set(core))

    plan = [("the universe", sorted(core),
             lambda: len(rows) >= need - ADJACENT_FLOOR),
            # ⛔ The ring's stop condition is the FLOOR ALONE, never the total. A 50-id chunk
            # yields many rows at once, so pass 1 overshoots its own limit and the total is
            # already past `need` before this pass looks at anything -- which made it stop after
            # 0 items and reach 0 neighbours, the exact state the floor exists to prevent.
            ("the adjacent ring", sorted(near),
             lambda: adjacent_people() >= ADJACENT_FLOOR)]

    for _label, _ids, _done in plan:
      print(f"   pass over {_label} ({len(_ids):,} items):")
      for k in range(0, len(_ids), 50):
        if _done():
            print(f"      pass satisfied after {k:,} of {len(_ids):,} items")
            break
        chunk = _ids[k:k + 50]
        try:
            data = api_get({"action": "wbgetentities", "format": "json",
                            "props": "claims", "ids": "|".join(chunk)}, AGENT)
        except Exception as exc:                                   # noqa: BLE001
            print(f"   chunk at {k} failed ({exc}); left alone")
            continue
        entities = data.get("entities") or {}

        def geni_of(qid):
            """The Geni id for an item: the ledger first, then the item's own `P2600`."""
            if qid in core:
                return core[qid]
            for st in ((entities.get(qid) or {}).get("claims") or {}).get("P2600", []):
                val = ((st.get("mainsnak") or {}).get("datavalue") or {}).get("value")
                if isinstance(val, str) and val:
                    return val
            return ""

        for qid, ent in entities.items():
            subject_geni = geni_of(qid)
            if not subject_geni:
                no_geni += 1
                continue
            claims = ent.get("claims") or {}
            for prop in RELATIONSHIPS:
                for st in claims.get(prop, []):
                    # A reference already there is the whole point of the check.
                    if st.get("references"):
                        sourced += 1
                        continue
                    snak = st.get("mainsnak") or {}
                    if snak.get("snaktype") != "value":
                        no_value += 1
                        continue
                    target = (snak.get("datavalue") or {}).get("value") or {}
                    other = target.get("id") if isinstance(target, dict) else None
                    if not other:
                        no_value += 1
                        continue
                    other_geni = geni_of(other)
                    if not other_geni:
                        no_geni += 1
                        continue
                    # Geni must actually state it -- see the module docstring.
                    if prop == "P3373":
                        attested = other_geni in siblings.get(subject_geni, ())
                    else:
                        attested = other_geni in (tree.get(subject_geni, {}).get(prop) or ())
                    if not attested:
                        unattested += 1
                        continue
                    line = (f"{qid}{TAB}{prop}{TAB}{other}{TAB}S2600{TAB}"
                            f'"{qs(subject_geni)}"')
                    rows.append((qid, prop, other, line))

    # The universe first, then the adjacent ring, so a short day spends its budget on our own
    # items before it spends it claiming new ones.
    core_rows = [r for r in rows if r[0] in core]
    near_rows = [r for r in rows if r[0] not in core]

    # ⛔ **COLLECTING THE NEIGHBOURS IS NOT ENOUGH; THE SLOTS HAVE TO BE RESERVED.** Ordering
    # `core_rows + near_rows` and slicing put our own items in every slot whenever there were
    # sixty of them, so the ring was gathered and then cut. The floor comes out of the total
    # FIRST, and it is a floor of PEOPLE -- one neighbour can need several lines and counts once.
    reserved, seen_people = [], set()
    for r in near_rows:
        if r[0] not in seen_people and len(seen_people) >= ADJACENT_FLOOR:
            continue
        seen_people.add(r[0])
        reserved.append(r)
    rest = [r for r in near_rows if r not in reserved]
    keep = max(0, need - len(reserved))
    ordered = [r[3] for r in core_rows[:keep] + reserved + rest + core_rows[keep:]]
    manual = ordered[:MANUAL_CAP]
    auto = ordered[MANUAL_CAP:MANUAL_CAP + AUTO_CAP]
    held = len(ordered) - len(manual) - len(auto)
    print(f"   reserved {len(seen_people)} new bordering people ({len(reserved)} line(s))")

    header = [
        "# S2600 sources, backfilled onto relationship statements that already exist without",
        "# one. Ruled 2026-09-14. Scope is the universe and one step out -- never all 518,975",
        "# P2600 holders on Wikidata.",
        "# EVERY LINE IS ATTESTED BY OUR TREE: a source is a claim about the source, so a",
        "# relationship Geni does not state is left alone rather than cited to Geni.",
        "# Re-stating property+value attaches the reference; it does not add a second statement.",
        "",
    ]
    OUT.write_text(NLJ.join(header + manual) + NLJ, encoding="utf-8", newline=NLJ)
    AUTO_OUT.write_text(NLJ.join(header + auto) + NLJ, encoding="utf-8", newline=NLJ)
    print(f"   {len(rows):,} unsourced relationship statements our tree attests")
    print(f"   {len(manual)} -> {OUT.name} (MANUAL_CAP {MANUAL_CAP})")
    print(f"   {len(auto)} -> {AUTO_OUT.name} (AUTO_CAP {AUTO_CAP})")
    print(f"   {held:,} held for later days -- the pace is the point, not the backlog")
    print(f"   {sourced:,} already carry a reference")
    print(f"   {unattested:,} skipped: Wikidata holds it and our tree does not")
    print(f"   {no_geni:,} skipped: no Geni id on one end, so nothing to cite")
    print(f"   {no_value:,} skipped: somevalue/novalue")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
