"""Turn `order.life` into the third source of the synoptic tree, as edit objects.

**Everything goes in.** Emma, 2026-08-14: *"Something without a geni ID and
without a Wikidata ID can still be merged into the synoptic tree because we have
the order.life thing as a third data source… we are, in fact, trying to get all
this information, some of which was destroyed on geni."* So no person is dropped
for lacking an identifier.

**The Gaiad flag is recorded but does NOT tier, because it marks everything.**
`Q153802` "Gaiad character" is on **105,720 of 106,908** persons — and on
**400 of 400** sampled people who carry a Wikidata QID, i.e. definitely real
historical people. The epic runs through the whole genealogy, so the flag
separates nothing. An earlier version tiered on it and pushed 45,437 creations,
real people included, into "add last". Every entry still carries
`"gaiad": true`/`false` as data.

**Tiering is on identifiers instead**, which does discriminate: a person with no
Geni ID and no Wikidata QID is order.life-only, and that is where epic-only
material actually concentrates. Emma's intent — *"the Gaiad stuff would be added
only very, very, very, very late"* — is served by tier 3 being last, not by a
flag that is always true.

**No order.life citation is emitted, and that is the bug this fixes.** Emma:
*"These JSONs aren't gonna fire because they're trying to cite an order.life
citation that doesn't exist."* A reference to a source Wikidata does not have
makes the whole statement unusable. So: a Geni ID gives `S2600`, and a person
with no Geni ID gets **no reference at all** rather than a broken one.

**Relationships order.life has and Wikidata does not are added to the existing
items.** Emma, 2026-08-14: *"some of the wiki data stuff with wiki data IDs but
no geni IDs is literally stuff that I added… we are going to be adding all of the
relationships that are not present on wiki data that are present there in the
order.life stuff, because some of it is just work that I did that is not on
geni."* That is `add_relationship`, and it is why a person carrying a QID and no
Geni ID is **not** nothing to do — an earlier version of this script called them
that and buried 37,728 people.

Each candidate edge is checked against the local store first: if the existing
item already states that `P22`/`P25`/`P26` value, nothing is emitted.

**order.life is its own Wikibase, not a Wikidata mirror.** Emma: *"It isn't a
true wiki data export. It's its own wiki base, which is mostly structured very
commonly with wiki data but not entirely."* So its property numbers are its own —
`P47` father, `P48` mother, `P42` spouse, `P20` child — and must be translated
rather than passed through. The `analysis/*.tsv` tables are used instead of the
raw claims for exactly that reason.

**Emma's property decisions, 2026-08-14.** `P64 Multi language label` is
Wikidata's multilingual label and is emitted as `Lmul`. `P59 Cladoplast of` is
not mapped and not emitted — *"we don't do anything with it until there is a
Cladoplast object on Wikidata, which there currently is not."* `P12 Occupation`
and `P13 Residence` are **dropped**, not normalised: *"the only monolingual text
that we just don't do is the P12 and P13 occupation and residence."* Of the
monolingual-text properties, address is the one that is done, as `P6375`.

`Q2` is Emma and is skipped — her own item, not genealogy this should assert.

Inputs, all from `order.life/wikibase/`:
  `analysis/persons.tsv`  qid, label, sex, birth, death, gedcom, wikidata_qid, geni_id
  `analysis/edges.tsv`    parent -> child
  `analysis/spouses.tsv`  a <-> b
  `items/<qid>.json`      read only to test for the Gaiad flag

    py scripts/build-orderlife-batch.py
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))

from genimerge import sources  # noqa: E402
from labels import label_for  # noqa: E402

OL = Path("C:/Users/Emma/Documents/GitHub/order.life/wikibase")
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
INDI = re.compile(r"^0 @I(\d+)@ INDI")

GAIAD = "Q153802"          # order.life: "Gaiad character"
HUMAN = "Q5"
MALE, FEMALE = "Q6581097", "Q6581072"
OL_MALE, OL_FEMALE = "Q153718", "Q153719"

#: Lowest number is added first. Identified, real people lead; the epic trails.
TIERS = {
    "add_geni_id": 0,
    "add_relationship": 1,
    "create_geni_only": 2,
    "create_orderlife_only": 3,
}

#: **Never create an item for someone who already has one.** A person carrying a
#: `wikidata_qid` already exists on Wikidata; creating a second item is a
#: duplicate, and duplicates are the one failure mode here that damages Wikidata
#: rather than merely wasting a run. So a QID with nothing to add is
#: `nothing_to_do`, and a Geni ID the local store already maps to an item is too.
NOTHING = "nothing_to_do"


def corpus_geni_ids() -> set[str]:
    ids: set[str] = set()
    for path in sources.find_exports():
        with path.open(encoding="utf-8-sig", errors="replace") as fh:
            for raw in fh:
                m = INDI.match(raw)
                if m:
                    ids.add(m.group(1))
    return ids


def gaiad_qids(qids: list[str]) -> set[str]:
    """Which of these order.life items carry the Gaiad-character flag."""
    out = set()
    for n, q in enumerate(qids, 1):
        p = OL / "items" / f"{q}.json"
        if not p.exists():
            continue
        if GAIAD in p.read_text(encoding="utf-8", errors="replace"):
            out.add(q)
        if n % 20000 == 0:
            print(f"  scanned {n:,}/{len(qids):,} items for the Gaiad flag")
    return out


def read_existing_relations(qids: set[str]) -> dict[str, dict[str, set[str]]]:
    """qid -> {P22/P25/P26 -> the item ids already stated}, from the local store.

    A shard is opened once and every wanted item in it read, because the store is
    2.7 GB and per-item seeking over 37,000 items would read it many times over.
    An item absent from the store yields nothing and its edges are skipped: we
    cannot tell a missing statement from a missing item, and guessing that way
    round produces duplicate claims on live items.
    """
    import gzip
    if not INDEX.exists():
        return {}
    conn = sqlite3.connect(INDEX)
    by_shard: dict[int, set[str]] = {}
    for q in qids:
        row = conn.execute("select shard from items where qid=?", (q,)).fetchone()
        if row:
            by_shard.setdefault(row[0], set()).add(q)

    out: dict[str, dict[str, set[str]]] = {}
    for n, (shard, wants) in enumerate(sorted(by_shard.items()), 1):
        path = REPO / "wikidata" / "items" / f"items-{shard:05d}.jsonl.gz"
        if not path.exists():
            continue
        with gzip.open(path, "rb") as fh:
            for raw in fh:
                if not any(f'"{q}"'.encode() in raw for q in wants):
                    continue
                item = json.loads(raw)
                q = item.get("id")
                if q not in wants:
                    continue
                claims = item.get("claims") or {}
                out[q] = {
                    p: {s["mainsnak"]["datavalue"]["value"]["id"]
                        for s in claims.get(p, [])
                        if s.get("mainsnak", {}).get("datavalue")}
                    for p in ("P22", "P25", "P26")
                }
        if n % 100 == 0:
            print(f"  read {n:,}/{len(by_shard):,} shards")
    return out


#: **An order.life QID is never a Wikidata value.** Its Q-space is its own: `Q1`
#: is Aster, `Q153718/9` are Male/Female, `Q153801/2` are Person/Gaiad character.
#: A `wikibase-item` value carries no marker saying which wiki it came from, so
#: passing one through would write a real statement pointing at a wrong item.
#: Every emitted value is resolved through the target's own `P61` first, and a
#: target with no Wikidata item is simply not pointed at - which is also why
#: every edge into Aster falls out without needing a special case.
def read_tsv(path):
    """Read one of order.life's `analysis/*.tsv` tables.

    **`quoting=csv.QUOTE_NONE` is the whole point.** These are tab-separated
    files with no quoting convention, so a `"` in a label is literal data. With
    Python's default quoting it is an opening quote instead, and the field runs
    on until the next one — swallowing the tabs and newlines in between.

    Measured 2026-08-15: the default cost **128 rows** of `persons.tsv`, and
    corrupted the row before each loss. `Q98159` (*"Abu'l Hasan" Muhammad bin
    Yahya bin al-Husain*) was the one Emma reported. Its own line is well formed;
    the parser merged it with the next row, so its `geni_id` went missing and its
    `wikidata_qid` picked up `Q153719` — **order.life's "Female" item** — which
    is a syntactically valid QID and therefore sails past the validation below.
    That is the exact hazard `reports/orderlife-properties.md` warns about: an
    order.life QID appearing where a Wikidata QID is expected.
    """
    return csv.DictReader(path.open(encoding="utf-8", newline=""),
                          delimiter="\t", quoting=csv.QUOTE_NONE)


def _assert_wikidata_qid(value: str, where: str) -> str:
    if not re.fullmatch(r"Q\d+", value or ""):
        raise SystemExit(f"{where}: {value!r} is not a QID")
    return value

#: **Sex from the graph, when order.life's own column is unusable.**
#:
#: `Q1`/`Q153721` is "Aster, Goddess of Alpha" and appears in the sex column of
#: 40 people; 3,081 more are blank. Emma, 2026-08-14: *"Sex = Q1 is an error, but
#: it is not an error that means all the data is bad. I believe you can literally
#: just figure out the sex."*
#:
#: Two inferences, both from recorded relationships rather than from names:
#:
#:   * every co-parent of every child is female  -> this person is male
#:   * every recorded spouse is female           -> this person is male
#:
#: and the mirror of each. Unanimity is required: a mixed set resolves nothing.
#: This is evidence, not a heuristic about naming, which is the line this repo
#: draws everywhere else.
#:
#: It recovers 2 of the 18 Aster-sexed parents. The other 16 are a single-parent
#: Japanese descent chain with no co-parents and no spouses, so nothing in the
#: graph separates father from mother for them - their Wikidata items would, and
#: none of those items are in the local store.
def infer_sex(q, persons, kids, parents_of, spouses):
    known = {"Q153718": OL_MALE, "Q153719": OL_FEMALE}

    def sex_of(p):
        return known.get((persons.get(p, {}).get("sex") or "").strip())

    co = {sex_of(o) for c in kids.get(q, ()) for o in parents_of.get(c, ())
          if o != q}
    co.discard(None)
    if co == {OL_FEMALE}:
        return OL_MALE, "co-parent is female"
    if co == {OL_MALE}:
        return OL_FEMALE, "co-parent is male"
    sp = {sex_of(s) for s in spouses.get(q, ())}
    sp.discard(None)
    if sp == {OL_FEMALE}:
        return OL_MALE, "spouse is female"
    if sp == {OL_MALE}:
        return OL_FEMALE, "spouse is male"
    return None, ""

def _rel(q, wqid, prop, value, ref, other, persons, gaiad):
    return {
        "id": f"add_relationship:{wqid}:{prop}:{value}",
        "type": "add_relationship",
        "tier": TIERS["add_relationship"],
        "gaiad": q in gaiad or other in gaiad,
        "source": "order.life",
        "subject": {"qid": wqid, "geni_id": ref[0]["value"] if ref else None,
                    "orderlife_qid": q},
        "requires": [],
        "statement": {"property": prop,
                      "value": _assert_wikidata_qid(value, f"{q}->{other}"),
                      "references": ref},
        "note": (persons.get(q, {}).get("label", "")
                 + " -> " + persons.get(other, {}).get("label", "")),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="reports/wikidata-orderlife.json")
    ap.add_argument("--summary", default="reports/orderlife-batch-summary.csv")
    args = ap.parse_args()

    persons = {r["qid"]: r for r in
               read_tsv(OL / "analysis" / "persons.tsv")}
    persons.pop("Q2", None)
    print(f"{len(persons):,} order.life persons (Q2 dropped)")

    # **Validate the identifier columns on read.** One row - `Eurycratides` -
    # carries its own label in `wikidata_qid` instead of a QID, and it reached
    # the emit stage and tripped `_assert_wikidata_qid` there. Catching it here
    # keeps a malformed identifier from being treated as a real one at all: a
    # bad QID would otherwise have counted as "already exists on Wikidata" and
    # suppressed a creation. Geni IDs are all well-formed but are checked on the
    # same principle rather than trusted.
    bad_q = bad_g = 0
    for r in persons.values():
        if (r.get("wikidata_qid") or "").strip() and not re.fullmatch(
                r"Q\d+", r["wikidata_qid"].strip()):
            print(f"  dropping malformed wikidata_qid "
                  f"{r['wikidata_qid']!r} on {r.get('label','')!r}")
            r["wikidata_qid"] = ""
            bad_q += 1
        if (r.get("geni_id") or "").strip() and not re.fullmatch(
                r"\d+", r["geni_id"].strip()):
            r["geni_id"] = ""
            bad_g += 1
    if bad_q or bad_g:
        print(f"  {bad_q} malformed QIDs and {bad_g} malformed Geni IDs dropped")

    father: dict[str, list[str]] = {}
    for r in read_tsv(OL / "analysis" / "edges.tsv"):
        father.setdefault(r["child"], []).append(r["parent"])

    spouses: dict[str, list[str]] = {}
    for r in read_tsv(OL / "analysis" / "spouses.tsv"):
        spouses.setdefault(r["a"], []).append(r["b"])
        spouses.setdefault(r["b"], []).append(r["a"])

    ours = corpus_geni_ids()
    print(f"{len(ours):,} Geni profiles in this corpus")

    geni_to_qid: dict[str, str] = {}
    qid_to_geni: dict[str, set[str]] = {}
    if INDEX.exists():
        conn = sqlite3.connect(INDEX)
        for gid_, qid_ in conn.execute("select geni_id, qid from geni"):
            geni_to_qid[gid_] = qid_
            qid_to_geni.setdefault(qid_, set()).add(gid_)
    print(f"{len(geni_to_qid):,} Geni->item links in the local store")

    print("scanning items for the Gaiad flag...")
    gaiad = gaiad_qids(list(persons))
    print(f"{len(gaiad):,} of them are flagged Gaiad characters")

    batch, summary, skipped = [], {}, []
    unresolved: list[dict] = []
    inferred: list[dict] = []
    #: order.life qid -> (wikidata qid, geni id or "") for everyone who has an
    #: item on Wikidata. Their edges are the `add_relationship` source.
    rel_candidates: dict[str, tuple[str, str]] = {}
    for q, r in persons.items():
        gid = (r.get("geni_id") or "").strip()
        wqid = (r.get("wikidata_qid") or "").strip()
        # order.life carries Geni's redaction markers through into its own
        # label column - 278 "private", 47 "nn", 26 "unknown", 57 "?". Same
        # rule as everywhere else: the person is created, the label is not set.
        label = label_for((r.get("label") or "").strip()
                          or (r.get("gedcom") or "").strip())

        already = geni_to_qid.get(gid) if gid else None
        if wqid and gid:
            # The item exists. Add the Geni ID unless it is already on it.
            kind = NOTHING if gid in qid_to_geni.get(wqid, ()) else "add_geni_id"
        elif wqid:
            kind = NOTHING          # exists on Wikidata, nothing to add
        elif already:
            kind = NOTHING          # the Geni ID is already on an item
        elif gid:
            kind = "create_geni_only"
        else:
            kind = "create_orderlife_only"
        if kind == NOTHING:
            # The identifier work is done for this person, but their edges may
            # still be missing from Wikidata. Queue them for the relationship
            # pass rather than discarding them.
            summary[NOTHING] = summary.get(NOTHING, 0) + 1
            skipped.append({"orderlife_qid": q, "label": label,
                            "wikidata_qid": wqid, "geni_id": gid,
                            "already_on": already or wqid})
            if wqid or already:
                rel_candidates[q] = (wqid or already, gid)
            continue
        if wqid:
            rel_candidates[q] = (wqid, gid)

        # A Geni ID is the ONLY citation available. Never cite order.life.
        ref = [{"property": "P2600", "value": gid}] if gid else []

        statements = [{"property": "P31", "value": HUMAN, "references": ref}]
        if gid:
            statements.append({"property": "P2600", "value": gid, "references": []})
        sex = (r.get("sex") or "").strip()
        if sex in (OL_MALE, OL_FEMALE):
            statements.append({
                "property": "P21",
                "value": MALE if sex == OL_MALE else FEMALE,
                "references": ref,
            })

        batch.append({
            "id": f"{kind}:{q}",
            "type": "add_geni_id" if kind == "add_geni_id" else "create_individual",
            "tier": TIERS[kind],
            "gaiad": q in gaiad,
            "source": "order.life",
            "subject": {"qid": wqid or None, "geni_id": gid or None,
                        "orderlife_qid": q},
            "requires": [f"person:{p}" for p in father.get(q, [])],
            "labels": {"en": label, "mul": label},
            "statements": statements,
            "links": (
                [{"property": "P22_or_P25", "value": f"@person:{p}",
                  "references": ref} for p in father.get(q, [])]
                + [{"property": "P26", "value": f"@person:{s}", "references": ref}
                   for s in spouses.get(q, [])]
            ),
            "geni_id_in_our_corpus": bool(gid and gid in ours),
        })
        summary[kind] = summary.get(kind, 0) + 1

    # ---- relationships order.life has that Wikidata does not ---------------
    print(f"\n{len(rel_candidates):,} people have a Wikidata item; "
          f"checking their edges against it")
    wanted = {w for w, _ in rel_candidates.values()}
    existing = read_existing_relations(wanted)
    print(f"read {len(existing):,} of those items out of the local store")

    for q, (wqid, gid) in sorted(rel_candidates.items()):
        have = existing.get(wqid)
        if have is None:
            continue                      # item not in our slice; cannot compare
        ref = [{"property": "P2600", "value": gid}] if gid else []
        for parent in father.get(q, []):
            target = rel_candidates.get(parent)
            if not target:
                continue                  # parent has no item to point at
            psex = (persons.get(parent, {}).get("sex") or "").strip()
            prop = {OL_MALE: "P22", OL_FEMALE: "P25"}.get(psex)
            why = ""
            if not prop:
                guess, why = infer_sex(parent, persons, children_of, parents_of,
                                       spouses)
                prop = {OL_MALE: "P22", OL_FEMALE: "P25"}.get(guess)
                if prop:
                    inferred.append({
                        "parent_orderlife_qid": parent,
                        "parent": persons.get(parent, {}).get("label", ""),
                        "recorded_sex": psex or "(blank)",
                        "inferred": "male" if guess == OL_MALE else "female",
                        "property": prop, "because": why,
                    })
            if not prop:
                # **Do not drop the edge.** Wikidata has only P22 father and P25
                # mother, so an unresolved parent sex means the PROPERTY cannot
                # be chosen - it does not mean the RELATIONSHIP is absent. An
                # earlier version `continue`d here and silently deleted a
                # fourteen-generation Japanese descent chain, because
                # order.life records those parents' sex as `Q1` / `Q153721`,
                # which is "Aster, Goddess of Alpha" - a third value in its own
                # scheme, not a data error. Emitted unresolved and counted.
                unresolved.append({
                    "orderlife_qid": q, "wikidata_qid": wqid,
                    "parent_orderlife_qid": parent, "parent_wikidata_qid": target[0],
                    "parent_sex_value": psex or "(blank)",
                    "person": persons.get(q, {}).get("label", ""),
                    "parent": persons.get(parent, {}).get("label", ""),
                })
                e = _rel(q, wqid, "P22_or_P25", target[0], ref, parent,
                         persons, gaiad)
                e["needs"] = "parent sex unresolved - choose P22 or P25"
                batch.append(e)
                continue
            if target[0] in have.get(prop, set()):
                continue
            batch.append(_rel(q, wqid, prop, target[0], ref, parent,
                              persons, gaiad))
        for sp in spouses.get(q, []):
            target = rel_candidates.get(sp)
            if not target or target[0] in have.get("P26", set()):
                continue
            batch.append(_rel(q, wqid, "P26", target[0], ref, sp,
                              persons, gaiad))

    for e in batch:
        if e["type"] == "add_relationship":
            summary["add_relationship"] = summary.get("add_relationship", 0) + 1

    batch.sort(key=lambda e: (e["tier"], e["subject"]["orderlife_qid"]))

    out = REPO / args.out
    out.write_text(json.dumps(batch, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nwrote {out} ({len(batch):,} entries)")

    s = REPO / args.summary
    with s.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["kind", "tier", "count"])
        for k, n in sorted(summary.items(), key=lambda kv: TIERS.get(kv[0], -1)):
            w.writerow([k, TIERS.get(k, ""), n])
            print(f"  tier {TIERS.get(k, '-'):>2}  {n:>7,}  {k}")
    print(f"wrote {s}")

    if inferred:
        i = REPO / "reports" / "orderlife-sex-inferred.csv"
        with i.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(inferred[0]))
            w.writeheader()
            w.writerows(inferred)
        print(f"wrote {i} ({len(inferred):,} rows) - sex recovered from the graph")

    if unresolved:
        u = REPO / "reports" / "orderlife-parent-sex-unresolved.csv"
        with u.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(unresolved[0]))
            w.writeheader()
            w.writerows(unresolved)
        print(f"wrote {u} ({len(unresolved):,} rows) - emitted as P22_or_P25, "
              f"NOT dropped; the property needs choosing")

    sk = REPO / "reports" / "orderlife-nothing-to-do.csv"
    with sk.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["orderlife_qid", "label",
                                           "wikidata_qid", "geni_id", "already_on"])
        w.writeheader()
        w.writerows(skipped)
    print(f"wrote {sk} ({len(skipped):,} rows) - these already exist, "
          f"creating them would duplicate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
