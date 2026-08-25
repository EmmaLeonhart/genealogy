"""Which of an item's several Geni ids is the WRONG one, decided by the parents.

    python scripts/resolve-multi-geni-by-parents.py

**Emma, 2026-08-25:** *"the easiest way to do this at scale would be to figure out consistency
of relatives on WikiData versus Geni. If one has two IDs and then they have a father and a
mother that both have one Geni ID and the Geni IDs match one but not the other, that zipper
join thing helps a lot with figuring out."*

That is the zipper join used on the half she called easy: *"parents are very easy to do a
zipper join on. Children, however, selecting between children and spouses... is a much, much
more difficult task."* This module does parents only, on purpose.

## The test

For a Wikidata item carrying two or more `P2600` *Geni.com profile ID* values:

1. read the item's `P22` *father* and `P25` *mother*;
2. those parent items must each carry **exactly one** `P2600` -- an anchor with two ids of its
   own decides nothing, so it is skipped rather than guessed at;
3. for each candidate Geni id, look up **our** tree's father and mother;
4. a candidate whose parent matches the anchor is `CONFIRMED`; one whose parent is recorded and
   is somebody else is `CONTRADICTED`.

**A verdict is only emitted when exactly one candidate is confirmed and every other candidate is
contradicted.** A candidate with no recorded parent on our side is `UNKNOWN` and blocks the whole
item, because "we have no evidence against it" is not evidence that it is wrong -- and the output
of this script deletes data.

## Why this is not the failing walk

`docs/structural-walk.md` records that the structural walk pairs on **position alone** and that
89% of the tangles in the correspondence are its own doing. This is the opposite direction and
does not have that failure mode: nothing here proposes a new pairing. Both candidate ids are
already asserted by Wikidata; the parents are used only to **choose between two claims Wikidata
itself makes**, and the anchor is a recorded `P2600`, never an inference.

## Removal versus deprecation, which are different cases

Emma has asked for both, for different things, and conflating them would destroy data:

* **Wrong id** -- the item is carrying a *relative's* profile, as with `Q102825194` holding both
  Gilbert Motier de La Fayette and his son Antoine. Nothing on Geni fixes this. The statement is
  **removed**, which is what she asked for here: *"Make edit JSONs that remove the property of
  the wrong one."*
* **Merged-away id** -- two Geni profiles for one person, one since merged into the other. Her
  rule, 2026-08-25: *"Once you've merged it, you would deprecate the one that redirects to the
  other one."* That is a rank change, not a removal, and this script does not emit it.

This script only ever emits the first, and only where the parents contradict the candidate.

## What it cannot tell you

The local store predates Emma's hand editing (`CLAUDE.md` -- *a downloaded item file is a
photograph, not a mirror*), so an item she has fixed since the download still reads as broken
here. Every emitted edit therefore names the store as its evidence and is **queued, never run**;
Wikidata editing in this repo starts 2026-09-01.

Writes `reports/multi-geni-parent-verdicts.tsv` and
`reports/wikidata-remove-wrong-p2600.json`.
Offline throughout.
"""
from __future__ import annotations

import collections
import csv
import gzip
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "wikidata" / "items"
INDEX = ROOT / "out" / "wikidata" / "store-index.sqlite3"

GENI_ID = "P2600"       # Geni.com profile ID
FATHER = "P22"          # father
MOTHER = "P25"          # mother
BIRTH = "P569"          # date of birth
DEATH = "P570"          # date of death

#: Tight on purpose. `validate-structural-walk.py` uses 15 years because it is judging whether a
#: pairing is *impossible*; this decides which of two people an item is *about*, and its output
#: deletes a statement, so a near miss must not count as a match.
YEAR_TOLERANCE = 3

#: The six pairs opened in the browser on 2026-08-25 and judged by eye, with the Geni id the
#: page evidence says does NOT belong on that item. The script is checked against these before
#: its output is trusted -- see `--validate`. `None` means the pair is a real duplicate or was
#: left unclear, so nothing should be removed.
HAND_CHECKED = {
    "Q101248370": None,                     # genuine duplicate, both are Edel Saltensee
    "Q102825194": "6000000003493396117",    # Antoine Motier, the SON
    # **Corrected 2026-08-25 by this script, against my own eyeball.** The artifact said the
    # daughter's id was the interloper. The item is labelled *Ermengarde of Provence* and its
    # `P22` anchor is the DAUGHTER's father, so the item is about the daughter and it is the
    # QUEEN's id that does not belong. Our tree agrees: it records the queen as the other
    # candidate's mother.
    "Q100327211": "348889594040013469",     # Ermengardis the QUEEN, the mother
    "Q101247043": None,                     # two different women; which id is wrong is unknown
    "Q103775136": None,                     # unclear
    "Q103568200": None,                     # unclear
}


def same_person_brakes(multi, names):
    """`{qid: reason}` for items where a removal must be WITHHELD.

    **Both brakes exist because of `Q101248370`, where this script condemned the right answer.**
    Its two candidates are one woman, Edel Pedersdatter Saltensee -- and their recorded fathers
    are two different Geni profiles, because the father is duplicated on Geni too. The parent
    test therefore reads a duplicate as a contradiction, which is the exact case it must not
    delete: **a duplicated person usually has a duplicated parent.**

    Two signals that the candidates may be one person, either of which blocks the item:

    * **their parents sit on one Wikidata item** -- the duplication is visible one generation up,
      which is positive evidence the pair is a genuine duplicate rather than two people;
    * **the candidates carry the same name** after case and whitespace folding.

    The name check is a **brake on deletion, never a matcher.** `CLAUDE.md` forbids name
    similarity for deciding a merge, and nothing here decides one: an equal name only withholds a
    destructive edit, which is the direction where being wrong costs nothing. Diacritics are kept,
    per the rule that a diacritic makes a different name.
    """
    geni_to_qids = collections.defaultdict(set)
    with open(ROOT / "reports" / "synoptic-correspondence.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="	"):
            geni_to_qids[r["geni_id"]].add(r["qid"])

    def fold(s):
        return " ".join((s or "").split()).casefold()

    blocked = {}
    for qid, geni_ids in multi.items():
        labels = {fold(names.get(g, "")) for g in geni_ids if names.get(g)}
        if len(geni_ids) > 1 and len(labels) == 1 and labels != {""}:
            blocked[qid] = "candidates share a name - may be one person"
    return blocked, geni_to_qids


def read_items(qids, props):
    """`{qid: {prop: [values]}}` for `props`, one pass per shard."""
    con = sqlite3.connect(str(INDEX))
    by_shard = collections.defaultdict(set)
    for qid in qids:
        hit = con.execute("SELECT shard FROM items WHERE qid=?", (qid,)).fetchone()
        if hit:
            by_shard[hit[0]].add(qid)

    out = {}
    for shard, wanted in by_shard.items():
        path = STORE / f"items-{shard:05d}.jsonl.gz"
        if not path.exists():
            continue
        with gzip.open(path, "rt", encoding="utf-8") as f:
            for line in f:
                if not wanted:
                    break
                for qid in list(wanted):
                    if f'"{qid}"' not in line:
                        continue
                    item = json.loads(line)
                    if item.get("id") != qid:
                        continue
                    wanted.discard(qid)
                    claims = item.get("claims", {})
                    got = {}
                    for prop in props:
                        vals = []
                        for st in claims.get(prop, []):
                            # A deprecated statement is Wikidata already saying "not this one".
                            if st.get("rank") == "deprecated":
                                continue
                            dv = st["mainsnak"].get("datavalue", {}).get("value")
                            if isinstance(dv, dict):
                                t = dv.get("time", "")
                                if t:
                                    # `+1527-00-00T...` / `-0801-...`; keep the sign.
                                    digits = t[1:5]
                                    dv = ((-1 if t.startswith("-") else 1) * int(digits)
                                          if digits.isdigit() else None)
                                else:
                                    dv = dv.get("id")
                            if dv is not None and dv != "":
                                vals.append(dv)
                        got[prop] = vals
                    got["label"] = (item.get("labels", {}).get("en", {}).get("value")
                                    or next((v["value"] for v in item.get("labels", {}).values()),
                                            ""))
                    out[qid] = got
                    break
    return out


def main():
    validate = "--validate" in sys.argv

    # --- items carrying several Geni ids ---------------------------------------------------
    multi = collections.defaultdict(set)
    with open(ROOT / "reports" / "correspondence-shapes.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["kind"].startswith("one item"):
                multi[r["qid"]].add(r["geni_id"])
    if validate:
        multi = {q: v for q, v in multi.items() if q in HAND_CHECKED}
    print(f"{len(multi):,} items carrying several Geni ids")

    # (names are loaded before the brakes, which need them)
    items = read_items(set(multi), [GENI_ID, FATHER, MOTHER, BIRTH, DEATH])
    print(f"{len(items):,} read from the local store")

    # --- their parents, which must each carry exactly one Geni id --------------------------
    parent_qids = {q for it in items.values() for p in (FATHER, MOTHER) for q in it[p]}
    parents = read_items(parent_qids, [GENI_ID])
    print(f"{len(parents):,} parent items read")

    # --- our tree --------------------------------------------------------------------------
    wanted_geni = {g for gs in multi.values() for g in gs}
    ours = {}
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in wanted_geni:
                ours[row["geni_id"]] = ((row.get("father") or "").strip(),
                                        (row.get("mother") or "").strip())
    our_years = {}
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in wanted_geni:
                def yr(k):
                    v = (row.get(k) or "").strip()
                    return int(v) if v.lstrip("-").isdigit() else None
                our_years[row["geni_id"]] = (yr("birth_date_year"), yr("death_date_year"))

    names = {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in wanted_geni:
                names[row["geni_id"]] = row.get("label_en") or row.get("label_mul") or ""

    blocked, geni_to_qids = same_person_brakes(multi, names)
    print(f"{len(blocked):,} items withheld on the shared-name brake alone")

    rows, edits = [], []
    tally = collections.Counter()
    for qid, geni_ids in sorted(multi.items()):
        item = items.get(qid)
        if not item:
            tally["item not in store"] += 1
            continue

        # **One candidate IS the other's parent -- proof they are two people, so no brake.**
        # This is the shape of `Q102825194` (Gilbert Motier and his son Antoine) and
        # `Q100327211` (Ermengardis and her daughter). It is computed BEFORE the anchor gate,
        # because such an item is decidable even with no usable parent anchor: we already know
        # one id is wrong, and the dates only have to say which. Both brakes fire spuriously on
        # this shape -- a parent-child pair trivially "shares a parent item" (the parent IS the
        # other candidate, carried by this very item), and a family that reuses a name gives
        # them the same label too -- so the kin test overrides them rather than joining them.
        kin = any((ours.get(a) or ("", ""))[slot] == b
                  for a in geni_ids for b in geni_ids if a != b for slot in (0, 1))

        # Do the parents themselves sit on one Wikidata item? Then the "contradiction" is the
        # duplication showing up one generation up, not two different people.
        parent_sets = [set(geni_to_qids.get((ours.get(g) or ("", ""))[slot], ()))
                       for g in sorted(geni_ids) for slot in (0, 1)
                       if (ours.get(g) or ("", ""))[slot]]
        shared_parent_item = any(a & b for i, a in enumerate(parent_sets)
                                 for b in parent_sets[i + 1:])
        block = "" if kin else (blocked.get(qid) or (
            "parents sit on one Wikidata item - the duplicate propagates upward"
            if shared_parent_item else ""))

        # An anchor is a parent item with EXACTLY ONE Geni id. Anything else decides nothing.
        anchors = {}
        for prop, slot in ((FATHER, 0), (MOTHER, 1)):
            ids = [parents.get(q, {}).get(GENI_ID, []) for q in item[prop]]
            single = [v[0] for v in ids if len(v) == 1]
            if len(single) == 1:
                anchors[slot] = single[0]
        if not anchors and not kin:
            tally["no usable parent anchor"] += 1
            continue

        # Do the parents themselves sit on one Wikidata item? Then the "contradiction" is the
        # duplication showing up one generation up, not two different people.
        parent_sets = [set(geni_to_qids.get((ours.get(g) or ("", ""))[slot], ()))
                       for g in sorted(geni_ids) for slot in (0, 1)
                       if (ours.get(g) or ("", ""))[slot]]
        shared_parent_item = any(a & b for i, a in enumerate(parent_sets)
                                 for b in parent_sets[i + 1:])
        verdicts = {}
        for g in sorted(geni_ids):
            mine = ours.get(g)
            if not mine:
                verdicts[g] = "UNKNOWN (not in our tree)"
                continue
            hits = [(slot, mine[slot], anchor) for slot, anchor in anchors.items()]
            agree = [s for s, got, want in hits if got == want]
            clash = [s for s, got, want in hits if got and got != want]
            if agree:
                verdicts[g] = "CONFIRMED"
            elif clash:
                verdicts[g] = "CONTRADICTED"
            else:
                verdicts[g] = "UNKNOWN (no parent recorded)"

        # **Dates decide only where the parents cannot AND one candidate is provably the other's
        # parent.** The kin test has already established that exactly one id is wrong; this
        # only picks which. It is never allowed to *create* a removal on its own, because a
        # date agreeing with one candidate is not evidence the other is a different person --
        # two Geni profiles for one man carry the same dates.
        decided_by = "parents"
        if kin and len([v for v in verdicts.values() if v == "CONFIRMED"]) != 1                 and not [v for v in verdicts.values() if v == "CONTRADICTED"]:
            theirs = [y for y in (item[BIRTH][:1] + item[DEATH][:1])]
            if theirs:
                scored = {}
                for g in geni_ids:
                    mine = [y for y in (our_years.get(g) or ()) if y is not None]
                    gaps = [abs(a - b) for a in mine for b in theirs]
                    scored[g] = min(gaps) if gaps else None
                near = [g for g, d in scored.items() if d is not None and d <= YEAR_TOLERANCE]
                far = [g for g, d in scored.items() if d is not None and d > YEAR_TOLERANCE]
                if len(near) == 1 and far and len(near) + len(far) == len(geni_ids):
                    decided_by = "dates (no parent anchor; kin proves one id is wrong)"
                    for g in near:
                        verdicts[g] = "CONFIRMED"
                    for g in far:
                        verdicts[g] = "CONTRADICTED"

        confirmed = [g for g, v in verdicts.items() if v == "CONFIRMED"]
        contradicted = [g for g, v in verdicts.items() if v == "CONTRADICTED"]
        unknown = [g for g, v in verdicts.items() if v.startswith("UNKNOWN")]

        # **One confirmed, the rest contradicted, and nothing unknown.** An UNKNOWN blocks the
        # item: absence of a recorded parent is not evidence the id is wrong, and this output
        # deletes data.
        decisive = len(confirmed) == 1 and contradicted and not unknown and not block
        if kin:
            tally["one candidate is the other's parent"] += 1
        tally["DECISIVE" if decisive else
              "WITHHELD - " + block if block else
              "blocked by unknown" if unknown else
              "no single confirmed"] += 1

        for g in sorted(geni_ids):
            rows.append({
                "qid": qid, "wikidata_label": item["label"], "geni_id": g,
                "geni_name": names.get(g, ""), "verdict": verdicts[g],
                "our_father": (ours.get(g) or ("", ""))[0],
                "our_mother": (ours.get(g) or ("", ""))[1],
                "anchor_father": anchors.get(0, ""), "anchor_mother": anchors.get(1, ""),
                "decisive": "yes" if decisive else "no",
                "withheld_because": block,
                "one_is_the_other_parent": "yes" if kin else "no",
                "decided_by": decided_by if decisive else "",
            })
        if decisive:
            for g in contradicted:
                edits.append({
                    # The repo's edit-object shape, which `tests/test_edit_graph.py` enforces:
                    # a unique `id`, a `type` in `KNOWN_TYPES`, and a `subject` naming the item
                    # to act on. The first cut of this batch had none of them and reddened five
                    # tests, which is exactly what that suite is for.
                    "id": f"remove-p2600-{qid}-{g}",
                    "type": "remove_statement",
                    "subject": {"qid": qid, "geni_id": g},
                    "requires": [],
                    "property": GENI_ID, "value": g,
                    "because": (f"our tree gives {g} the parent(s) "
                                f"{ours[g]}, and this item's P22/P25 carry "
                                f"{sorted(anchors.values())}; "
                                f"{confirmed[0]} matches and {g} does not"),
                    "keeps": confirmed[0],
                    "decided_by": decided_by,
                    "evidence": "local Wikidata store + reports/derived-family.csv",
                })

    dest = ROOT / "reports" / "multi-geni-parent-verdicts.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    edits_path = ROOT / "reports" / "wikidata-remove-wrong-p2600.json"
    edits_path.parent.mkdir(parents=True, exist_ok=True)
    edits_path.write_text(json.dumps(edits, indent=1, ensure_ascii=False), encoding="utf-8")

    print(f"\nwrote {dest.relative_to(ROOT)}")
    for k, v in tally.most_common():
        print(f"   {v:>6}  {k}")
    print(f"\n{len(edits)} removals queued -> {edits_path.relative_to(ROOT)}")
    print("QUEUED, NEVER RUN. Wikidata editing in this repo starts 2026-09-01.")

    if validate:
        print("\n--- against the six pairs opened in the browser ---")
        got = {}
        for e in edits:
            got.setdefault(e["item"], []).append(e["value"])
        ok = True
        for qid, expected in HAND_CHECKED.items():
            mine = got.get(qid, [])
            if expected is None:
                verdict = "ok (nothing emitted)" if not mine else f"WRONG - emitted {mine}"
            else:
                verdict = ("ok" if mine == [expected]
                           else f"WRONG - emitted {mine}, expected [{expected}]")
            ok &= verdict.startswith("ok")
            print(f"   {qid:<12} {verdict}")
        print("\n" + ("all six agree with the pages" if ok
                      else "DISAGREEMENT - do not trust the batch"))


if __name__ == "__main__":
    main()
