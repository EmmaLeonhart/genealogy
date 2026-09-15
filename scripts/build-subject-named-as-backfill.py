"""Add `P1810` *subject named as* to `P2600` statements that already exist without it.

Ruled 2026-09-14: *"I'm asking you to add the subject named as to existing P2600 properties
within the universe and on adjacent items to the universe."*

**New statements have carried it since 2026-08-28** — `named_as()` in `build-garborg-day.py` is
on the `CREATE` line and on the add-to-an-existing-item line alike, and 148 of the 152 `P2600`
lines in today's batch have it. This is the other half: the statements written BEFORE that, which
have the identifier and no qualifier, and which no amount of correct behaviour going forward will
ever reach.

## ⛔ THE ADJACENT HALF IS THE POINT, NOT A TIDY-UP

Ruled 2026-09-14, emphatically: *"we are applying this to adjacent individuals to the universe.
And these adjacent individuals get added into the universe because of the fact that we just did
an edit on it. That's the entire point."*

The universe is **the account's own items** — `wikidata_subgraph` takes `reports/garborg-qids.tsv`
as `universe` and walks only edges with both ends inside it, which is what stops Bureus dragging
in Wikidata's 1,339,227-item genealogical component. And that ledger *is filled from the
account's contributions*. So:

    backfill P1810 on an adjacent item
      -> the item is now in the account's contributions
      -> the next ledger refresh puts it in garborg-qids.tsv
      -> wikidata_subgraph counts it as universe
      -> ITS neighbours become the new adjacent ring

**The edit is what makes the item ours.** That is the growth mechanism: the universe expands by
one ring per pass, and it expands by editing things we were already entitled to edit rather than
by widening a rule. Nothing here creates an individual — it annotates statements that already
exist.

## ⛔ LOCALITY: the universe and one step out, and nothing else

`CLAUDE.md` § *ONLY EVER EDIT THINGS IN THE UNIVERSE OR ONE STEP ADJACENT TO IT*, and the reason
it is a rule: *"the Scandinavian areas are places that we can really have a good idea of what
good data looks like and what the edge cases are, but having stuff that leaks out from the
universe and into just random areas is an intrinsic risk."* Wikidata holds **518,975** `P2600`
holders. Almost none of them are ours to annotate, and a backfill is exactly the shape of edit
that could quietly touch all of them.

So the scope is `reports/garborg-qids.tsv` — the account's own items, which is what
`wikidata_subgraph` means by *universe* — plus, for the adjacent step, the QIDs those items point
at through `P22`/`P25`/`P26`/`P40`/`P3373` in `reports/garborg-live-values.tsv`.

## The value is Geni's display name, never our label

Set 2026-08-28: `P1810` carries the specific name **Geni** gives a person, so it comes from
`display_name` in `reports/display-names.csv`. Our own label is the married form we chose since
2026-08-29 and is a different claim.

**Neither form of private gets a qualifier, and neither does an `NN`** — ruled 2026-08-30, after
`Q141223549` carried `P1810 "Private"` while Geni displayed `<private> Paulson`. There are two
backend kinds of private that render identically, so which one a profile exports as is an
artefact of the export rather than a fact about the person. The same test is applied here as in
`named_as()`, deliberately: one rule, two callers.

## Re-stating the statement is how a qualifier is added

QuickStatements V1 has no *add a qualifier to this existing statement* verb. Emitting
`Q123<TAB>P2600<TAB>"6000..."<TAB>P1810<TAB>"Name"` matches the existing statement on
property-and-value and attaches the qualifier to it; it does not create a second `P2600`.
`CLAUDE.md` § *A second Geni ID on one item is NOT a conflict* covers the case where it somehow
did.

    BOT_CONTACT=you@example.com PYTHONPATH=src python scripts/build-subject-named-as-backfill.py

Writes `reports/wikidata-subject-named-as.qs`.
"""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from live_name_items import _get as api_get  # noqa: E402

LEDGER = REPO / "reports" / "garborg-qids.tsv"
DISPLAY = REPO / "reports" / "display-names.csv"
LIVE = REPO / "reports" / "garborg-live-values.tsv"
OUT = REPO / "reports" / "wikidata-subject-named-as.qs"

AGENT = "geni-wikidata-backfill"

#: A newline, named so the writers below read cleanly.
NLJ = chr(10)

#: A tab, for splitting an emitted line back into its subject.
TAB = chr(9)

#: The relationship properties that make an item *adjacent* to the universe.
ADJACENT_VIA = ("P22", "P25", "P26", "P40", "P3373")

#: ⛔ **THE PACE. A WHOLE RING A DAY IS NOT THE PLAN.** Ruled 2026-09-14, correcting exactly
#: that reading: *"it's not supposed to be by a ring. By a ring is fucking insane ... let's say
#: 40 people in the quick statements batch and then 20 people in the CICD edits."*
#:
#: The universe grows because each edit makes an item ours, so an unpaced pass would claim every
#: neighbour at once -- thousands of items annotated in a day by an account that had touched
#: none of them the day before. That is the shape of edit that gets an account noticed, and
#: *our algorithm is relatively resistant to editors fixing its mistakes and this is drawing
#: attention* is already a queue item about exactly that.
#:
#: 60 a day, split the way the daily batch is: the larger share for the file a person pastes,
#: the smaller for the run that goes out unattended.
MANUAL_CAP = 40
AUTO_CAP = 20

#: ⛔ **A FLOOR OF NEW BORDERING PEOPLE, EVERY RUN. Ruled 2026-09-14 and it is the POINT of the
#: pass, not a detail of it:** *"Every run 10 new bordering people not in the universe but
#: connected to it get that as it."*
#:
#: **Without it the ring is never reached and the universe never grows.** The caps are 40 + 20 and
#: the universe is queried first, so on any day with sixty spare rows among our own items the
#: quota fills before a single neighbour is looked at. Measured 2026-09-15 over all four emitted
#: files -- `subject-named-as` 39 people, `-auto` 20, `relationship-sources` 32, `-auto` 8 --
#: **adjacent people: 0, 0, 0 and 0.** The growth mechanism was doing nothing at all.
#:
#: Ordering our own items first is still right: they are the ones we are certainly entitled to
#: edit. The floor is what stops "first" meaning "only". Counted in PEOPLE, not statements,
#: because the ruling says people and one item can need several lines.
ADJACENT_FLOOR = 10


def qs(value: str) -> str:
    """A QuickStatements string literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def carries_marker(name: str) -> bool:
    """`NN`, `Private`, `<private>` and the rest — the same exclusion `named_as()` applies."""
    low = (name or "").casefold()
    if not low or "<private>" in low:
        return True
    words = {w.strip("().,[]") for w in low.split()}
    return bool(words & {"nn", "private", "unknown", "ukjent", "okänd", "n.n.", "n.n"})


def universe():
    """`{qid: geni_id}` for the account's own items."""
    out = {}
    with LEDGER.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
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
        for row in csv.DictReader(fh, delimiter="\t"):
            if (row.get("property") or "") not in ADJACENT_VIA:
                continue
            subj, val = (row.get("qid") or "").strip(), (row.get("value") or "").strip()
            if subj in core and val.startswith("Q"):
                out.add(val)
            elif val in core and subj.startswith("Q"):
                out.add(subj)
    return out - set(core)


def display_names():
    """`{geni_id: display_name}`."""
    csv.field_size_limit(10 ** 7)
    out = {}
    with DISPLAY.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g, d = (row.get("geni_id") or "").strip(), (row.get("display_name") or "").strip()
            if g and d and g not in out:
                out[g] = d
    return out


def main() -> int:
    core = universe()
    near = adjacent(core)
    names = display_names()
    print(f"universe: {len(core):,} items; adjacent: {len(near):,}; "
          f"display names: {len(names):,}")

    # ⛔ **STOP AS SOON AS THE DAY'S QUOTA IS FULL.** The scope is 10,955 items and the pace is
    # 60 a day, so querying everything to then discard 99% of it costs twenty minutes of
    # Wikidata's time for nothing — measured at 5.4s per 50-id chunk, 220 chunks. The first run
    # was killed at its timeout mid-query and wrote nothing at all, which is how this was found.
    #
    # The universe is queried before the adjacent ring, so a short day still spends its budget
    # on our own items first.
    need = MANUAL_CAP + AUTO_CAP
    rows, already, no_name, no_p2600 = [], 0, 0, 0
    counters = {"already": 0, "no_name": 0, "no_p2600": 0}

    def sweep(ids, stop):
        """Query `ids` in chunks until `stop(rows)` says the pass is done."""
        for k in range(0, len(ids), 50):
            if stop(rows):
                print(f"      pass satisfied after {k:,} of {len(ids):,} items")
                return
            chunk = ids[k:k + 50]
            try:
                data = api_get({"action": "wbgetentities", "format": "json",
                                "props": "claims", "ids": "|".join(chunk)}, AGENT)
            except Exception as exc:                               # noqa: BLE001
                print(f"      chunk at {k} failed ({exc}); left alone")
                continue
            for qid, ent in (data.get("entities") or {}).items():
                claims = (ent.get("claims") or {}).get("P2600") or []
                if not claims:
                    counters["no_p2600"] += 1
                    continue
                for st in claims:
                    snak = st.get("mainsnak") or {}
                    gid = ((snak.get("datavalue") or {}).get("value") or "")
                    if not isinstance(gid, str) or not gid:
                        continue
                    if "P1810" in (st.get("qualifiers") or {}):
                        counters["already"] += 1
                        continue
                    name = names.get(gid, "")
                    if not name or carries_marker(name):
                        counters["no_name"] += 1
                        continue
                    rows.append(f'{qid}\tP2600\t"{gid}"\tP1810\t"{qs(name)}"')

    def adjacent_people():
        return len({r.split(TAB)[0] for r in rows} - set(core))

    # **Our own items first, but only up to `need - ADJACENT_FLOOR`.** They are the ones we are
    # certainly entitled to edit, so they get the bulk; the remainder is held open for the ring.
    print(f"   pass 1, the universe (up to {need - ADJACENT_FLOOR}):")
    sweep(sorted(core), lambda r: len(r) >= need - ADJACENT_FLOOR)
    # **Then the ring, until the floor of new bordering PEOPLE is met.** This is the growth
    # mechanism and it is the reason the pass exists at all.
    print(f"   pass 2, the adjacent ring (floor of {ADJACENT_FLOOR} people):")
    # ⛔ **The stop condition here is the FLOOR ALONE, never the total.** Written first as
    # `... or len(rows) >= need`, which defeated the whole thing: one 50-id chunk yields many
    # rows at once, so pass 1 overshoots its own limit -- 90 rows against a budget of 50 -- and
    # the total was already past `need` before pass 2 looked at anything. It reported
    # `pass satisfied after 0 items` and reached zero neighbours, exactly the state this floor
    # was added to fix.
    sweep(sorted(near), lambda r: adjacent_people() >= ADJACENT_FLOOR)
    print(f"   new bordering people reached: {adjacent_people()}")
    already, no_name, no_p2600 = (counters["already"], counters["no_name"],
                                  counters["no_p2600"])

    # The universe first, then the adjacent ring, so a short day spends its budget on our own
    # items before it spends it claiming new ones.
    tab = chr(9)
    core_rows = [r for r in rows if r.split(tab)[0] in core]
    near_rows = [r for r in rows if r.split(tab)[0] not in core]

    # ⛔ **COLLECTING THE NEIGHBOURS IS NOT ENOUGH; THE SLOTS HAVE TO BE RESERVED.** Ordering
    # `core_rows + near_rows` and slicing put our own items in every slot whenever there were
    # sixty of them, so the ring was gathered and then cut. The floor is taken out of the total
    # FIRST, and it is a floor of PEOPLE -- one neighbour can need several lines and still
    # counts once.
    reserved, seen_people = [], set()
    for r in near_rows:
        who = r.split(tab)[0]
        if who not in seen_people and len(seen_people) >= ADJACENT_FLOOR:
            continue
        seen_people.add(who)
        reserved.append(r)
    rest = [r for r in near_rows if r not in reserved]
    ordered = core_rows[:max(0, need - len(reserved))] + reserved + rest + core_rows[
        max(0, need - len(reserved)):]
    manual = ordered[:MANUAL_CAP]
    auto = ordered[MANUAL_CAP:MANUAL_CAP + AUTO_CAP]
    held = len(ordered) - len(manual) - len(auto)
    print(f"   reserved {len(seen_people)} new bordering people ({len(reserved)} line(s))")

    header = [
        "# P1810 subject named as, backfilled onto P2600 statements that already exist.",
        "# Ruled 2026-09-14. Scope is the universe and one step out -- never all 518,975",
        "# P2600 holders on Wikidata.",
        "# The value is Geni's display_name, never our own label. NN and private are skipped,",
        "# per the 2026-08-30 ruling that neither form of private gets a qualifier.",
        "# Re-stating property+value attaches the qualifier; it does not add a second P2600.",
        "",
    ]
    OUT.write_text(NLJ.join(header + manual) + NLJ, encoding="utf-8", newline=NLJ)
    auto_out = REPO / "reports" / "wikidata-subject-named-as-auto.qs"
    auto_out.write_text(NLJ.join(header + auto) + NLJ, encoding="utf-8", newline=NLJ)
    print(f"   {len(rows):,} statements need the qualifier")
    print(f"   {len(manual)} -> {OUT.name} (MANUAL_CAP {MANUAL_CAP})")
    print(f"   {len(auto)} -> {auto_out.name} (AUTO_CAP {AUTO_CAP})")
    print(f"   {held:,} held for later days -- the pace is the point, not the backlog")
    print(f"   {already:,} already have it")
    print(f"   {no_name:,} skipped: no display name, or NN/private")
    print(f"   {no_p2600:,} of the items checked carry no P2600 at all")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
