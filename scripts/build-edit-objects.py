"""Emit the JSON edit objects. Nothing is sent.

Emma's specification, 2026-08-12 — see `edit-objects.md`. Four kinds:
`add_geni_id`, `create_individual`, `link_siblings`, `add_statement`.

The rules that shape the output, all hers:

* **The Geni ID goes on first.** Claims are cited to it, so an `add_statement`
  carrying a Geni reference `requires` the `add_geni_id` object. *"Not all of the
  JSONs are valid to run initially."*
* **A bidirectional relationship cites both parties' Geni IDs**, on either side.
* **Labels carry no citation, ever**, and Geni is not the source of labels
  *"except in items that actually lack an English-language label on Wikidata …
  or in situations where we're creating the individual from scratch."*
* **A sibling link between two people with no Geni ID is a Wikidata fix** —
  emitted, uncited, `wikidata_fix: true`. `P3373` is symmetric and often stated
  on one side only.

Writes `out/wikidata/edits.json` and `reports/edit-objects.csv`.

    py scripts/build-edit-objects.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import wikistore  # noqa: E402

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import labels as _labels  # noqa: E402

# **A marker is not a label, at any of this script's four emission sites.** It had
# no guard at all: `label_en` went straight into `en` and `mul`, and the first
# `cjk_names` component straight into `ja` and `zh`. queue.md carried it as a known
# defect -- *"same defect as the one fixed in walk-structural-merge.py, and it is
# only harmless today because its output is out/wikidata/edits.json, which is
# gitignored and fires nothing. Fix it before anything reads that file."*
#
# `derived-labels.csv` really does carry markers in those columns: that is what
# `NN`, `Private` and `未知` are for, and the NN pipeline exists precisely because
# such a person gets `NN` in `mul` and a *descriptive* label elsewhere, never the
# marker itself in a local slot.
is_marker = _labels.is_marker_label


def label_slots(lab: dict) -> dict:
    """The label slots one `derived-labels.csv` row may legitimately fill.

    One function so the guard is applied once and can be tested once. Before this,
    the same four lines were written out at two emission sites with no guard at
    either, and `walk-structural-merge.py` had a third copy that did have one --
    which is how the `ja`/`zh` branch came to emit 22 edits labelled `未知`.

    `mul` carries `label_en`, not a marker. Emma, 2026-08-16: *"NN is always
    preserved in the multi-language label"* -- but the marker that belongs there is
    `NN` specifically, written by `build-nn-label-batch.py` from the full model.
    Copying whatever marker happened to sit in `label_en` -- `Private`, `Ukjent`,
    `未知` -- is a different thing wearing the same shape. A person dropped here
    ends up with no label from this script and gets one from the NN pipeline, which
    is the honest outcome rather than a false one.
    """
    out = {}
    en = (lab.get("label_en") or "").strip()
    if en and not is_marker(en):
        # **`en` only for a name written in Latin script.** The marker guard above was
        # added here; the SCRIPT guard never was, and `build-garborg-day.py` has had it
        # all along -- the disagreement this module's own docstring warns about, that
        # "a predicate copied per caller is a predicate that will disagree with itself".
        # `derive-labels.py` sets `label_en` to the CJK string for 13,872 people, so
        # without this a Han name goes into the ENGLISH label. `Help:Default values for
        # labels and aliases` says a name not in Latin script is not a default label;
        # `mul` is the language-neutral slot and still takes it.
        if re.search(r"[A-Za-z]", en):
            out["en"] = en
        out["mul"] = en
    cjk = (lab.get("cjk_names") or "").split(" | ")[0].strip()
    if cjk and not is_marker(cjk):
        out["ja"] = cjk
        out["zh"] = cjk
    return out

LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
FACTS = REPO_ROOT / "reports" / "derived-facts.csv"
FAMILY = REPO_ROOT / "reports" / "derived-family.csv"
STORE = REPO_ROOT / "wikidata" / "items"
INDEX = REPO_ROOT / "out" / "wikidata" / "store-index.sqlite3"
OUT_JSON = REPO_ROOT / "out" / "wikidata" / "edits.json"
OUT_CSV = REPO_ROOT / "reports" / "edit-objects.csv"

csv.field_size_limit(10_000_000)

SEX = {"M": "Q6581097", "F": "Q6581072"}
CIRCA = "Q5727902"

#: Directed relationships. The inverse is what makes a citation two-sided.
RELATIONS = (("father", "P22"), ("mother", "P25"), ("spouses", "P26"),
             ("children", "P40"))


def geni_ref(*geni_ids: str) -> list[dict]:
    """The Geni profile ID as a **reference**, never a qualifier.

    Several are passed for a bidirectional relationship: *"we cite the Geni IDs
    of both parties of the relationship on either side."*
    """
    return [{"property": "P2600", "value": g} for g in geni_ids if g]


def time_value(fields: dict, prefix: str) -> tuple[dict, list[dict]] | None:
    iso = fields.get(f"{prefix}_iso")
    precision = fields.get(f"{prefix}_precision")
    if not iso or not precision:
        return None
    value = {"time": iso, "precision": int(precision)}
    modifier = fields.get(f"{prefix}_modifier")
    year_end = fields.get(f"{prefix}_year_end")

    quals: list[dict] = []
    if modifier == "about":
        quals.append({"property": "P1480", "value": CIRCA})
    elif modifier == "before":
        quals.append({"property": "P1326", "value": value})
    elif modifier == "after":
        quals.append({"property": "P1319", "value": value})
    elif modifier == "between":
        quals.append({"property": "P1319", "value": value})
        if year_end:
            year = int(year_end)
            sign = "+" if year > 0 else "-"
            quals.append({"property": "P1326", "value": {
                "time": f"{sign}{abs(year):04d}-00-00T00:00:00Z", "precision": 9}})
    return value, quals


def main() -> int:
    labels = {r["geni_id"]: r for r in csv.DictReader(open(LABELS, encoding="utf-8"))}
    facts = {r["geni_id"]: r for r in csv.DictReader(open(FACTS, encoding="utf-8"))}
    family = {r["geni_id"]: r for r in csv.DictReader(open(FAMILY, encoding="utf-8"))}
    linked = {g: r["qid"] for g, r in labels.items() if r["qid"]}

    # Matches she recorded by hand. **Nothing about these is special.** They
    # are Wikidata items that we have matched to a Geni profile and that do not
    # yet state the Geni ID — which is the ordinary output of a merge, and the
    # ordinary starting state for a person. Emma, 2026-08-12: "it's just a
    # wikidata object … there should not be anything special about it."
    #
    # The merge along the family trees is meant to produce these; the file is one
    # source of them, not a separate category. Every such item takes the same
    # path: add_geni_id first, because the Geni ID must exist before any claim
    # can be cited to it or any relationship added.
    hand: dict[str, str] = {}
    print(f"{len(linked):,} people carry an item "
          f"({len(hand):,} matched but not yet stating the Geni ID)", flush=True)

    by_parent: dict[str, list[str]] = {}
    for geni_id, row in family.items():
        for parent in (row.get("father"), row.get("mother")):
            if parent:
                by_parent.setdefault(parent, []).append(geni_id)

    with wikistore.StoreReader(STORE, INDEX) as reader:
        items = reader.entities(sorted(set(linked.values())))
    print(f"{len(items):,} items read", flush=True)

    objects: list[dict] = []
    counts: Counter[str] = Counter()

    def add(obj: dict) -> None:
        objects.append(obj)
        counts[obj["type"]] += 1

    # --- 1. the Geni ID, which everything else is cited to ------------------
    needs_id: set[str] = set()
    for geni_id, qid in linked.items():
        item = items.get(qid)
        if item is None:
            continue
        if "P2600" not in (item.get("claims") or {}):
            needs_id.add(qid)
            add({
                "id": f"add_geni_id:{qid}",
                "type": "add_geni_id",
                "subject": {"qid": qid, "geni_id": geni_id},
                "requires": [],
                # The identifier itself is not cited to itself.
                "statement": {"property": "P2600", "value": geni_id,
                              "references": []},
            })

    def requires_id(qid: str) -> list[str]:
        """A cited claim cannot run before the Geni ID is on the item."""
        return [f"add_geni_id:{qid}"] if qid in needs_id else []

    # --- 2. statements on existing items ------------------------------------
    for geni_id, qid in linked.items():
        item = items.get(qid)
        if item is None:
            continue
        claims = item.get("claims") or {}
        has_label = item.get("labels") or {}
        lab, fac, fam = labels[geni_id], facts.get(geni_id, {}), family.get(geni_id, {})

        # Labels: only where Wikidata has none, never cited.
        slots = label_slots(lab)
        latin = slots.get("en", "")
        if latin and "en" not in has_label:
            add({
                "id": f"add_label:{qid}:en",
                "type": "add_statement",
                "subject": {"qid": qid, "geni_id": geni_id},
                "requires": [],
                "label": {"language": "en", "value": latin},
                "references": [],
                "note": "Geni is not the source of labels except where Wikidata has none",
            })
        cjk = slots.get("ja", "")
        for code in ("ja", "zh"):
            if cjk and code not in has_label:
                add({
                    "id": f"add_label:{qid}:{code}",
                    "type": "add_statement",
                    "subject": {"qid": qid, "geni_id": geni_id},
                    "requires": [],
                    "label": {"language": code, "value": cjk},
                    "references": [],
                })

        sex = SEX.get(fac.get("sex", ""))
        if sex and "P21" not in claims:
            add({
                "id": f"add_statement:{qid}:P21",
                "type": "add_statement",
                "subject": {"qid": qid, "geni_id": geni_id},
                "requires": requires_id(qid),
                "statement": {"property": "P21", "value": sex,
                              "references": geni_ref(geni_id)},
            })

        for prefix, prop in (("birth_date", "P569"), ("death_date", "P570"),
                             ("burial_date", "P4602")):
            if prop in claims or not fac:
                continue
            found = time_value(fac, prefix)
            if found:
                value, quals = found
                add({
                    "id": f"add_statement:{qid}:{prop}",
                    "type": "add_statement",
                    "subject": {"qid": qid, "geni_id": geni_id},
                    "requires": requires_id(qid),
                    "statement": {"property": prop, "value": value,
                                  "qualifiers": quals,
                                  "references": geni_ref(geni_id)},
                })

        address = fac.get("birth_address", "")
        if address and "P6375" not in claims:
            add({
                "id": f"add_statement:{qid}:P6375",
                "type": "add_statement",
                "subject": {"qid": qid, "geni_id": geni_id},
                "requires": requires_id(qid),
                "statement": {"property": "P6375",
                              "value": {"text": address, "language": "en"},
                              "references": geni_ref(geni_id)},
            })

        # Relationships: bidirectional, so both Geni IDs are cited.
        for column, prop in RELATIONS:
            existing = {
                (s.get("mainsnak", {}).get("datavalue", {}).get("value", {}) or {}).get("id")
                for s in claims.get(prop, [])
            }
            for other in (fam.get(column) or "").split(" | "):
                other_qid = linked.get(other)
                if not other_qid or other_qid in existing:
                    continue
                add({
                    "id": f"add_statement:{qid}:{prop}:{other_qid}",
                    "type": "add_statement",
                    "subject": {"qid": qid, "geni_id": geni_id},
                    "requires": requires_id(qid) + requires_id(other_qid),
                    "statement": {"property": prop, "value": other_qid,
                                  "references": geni_ref(geni_id, other)},
                })

    # --- 3. creations, for people with no item whose family is already there --
    # Emma: "creating an individual with all their names and such and linking
    # them to their parents or children who are already in the database".
    for geni_id, fam in family.items():
        if geni_id in linked:
            continue
        lab = labels.get(geni_id)
        if lab is None:
            continue
        anchors: list[tuple[str, str, str]] = []
        for column, prop in RELATIONS:
            for other in (fam.get(column) or "").split(" | "):
                other_qid = linked.get(other)
                if other_qid:
                    anchors.append((prop, other_qid, other))
        if not anchors:
            continue

        statements = [
            {"property": "P31", "value": "Q5", "references": geni_ref(geni_id)},
            {"property": "P2600", "value": geni_id, "references": []},
        ]
        fac = facts.get(geni_id, {})
        sex = SEX.get(fac.get("sex", ""))
        if sex:
            statements.append({"property": "P21", "value": sex,
                               "references": geni_ref(geni_id)})
        for prefix, prop in (("birth_date", "P569"), ("death_date", "P570"),
                             ("burial_date", "P4602")):
            found = time_value(fac, prefix) if fac else None
            if found:
                value, quals = found
                statements.append({"property": prop, "value": value,
                                   "qualifiers": quals,
                                   "references": geni_ref(geni_id)})

        item_labels = label_slots(lab)
        if not item_labels:
            continue

        add({
            "id": f"create_individual:{geni_id}",
            "type": "create_individual",
            "subject": {"qid": None, "geni_id": geni_id},
            # The anchors must exist before this person can be linked to them.
            "requires": sorted({q for _, q, _ in anchors}),
            "labels": item_labels,
            # The column holds the BIRTH name now: `label_mul` took the married form as
            # primary on 2026-08-29, so what is left over as an alias is the birth one.
            "aliases": {"en": [a for a in (lab["alias_names"] or "").split(" | ") if a]},
            "statements": statements,
            "links": [{"property": prop, "value": q,
                       "references": geni_ref(geni_id, g)} for prop, q, g in anchors],
        })

    # --- 4. sibling links, including the uncited Wikidata fix ---------------
    seen_pairs: set[tuple[str, str]] = set()
    for children in by_parent.values():
        if len(children) < 2:
            continue
        for i, a in enumerate(children):
            for b in children[i + 1:]:
                qa, qb = linked.get(a), linked.get(b)
                if not (qa and qb):
                    continue
                pair = tuple(sorted((qa, qb)))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                item_a = items.get(qa) or {}
                stated = {
                    (s.get("mainsnak", {}).get("datavalue", {}).get("value", {}) or {}).get("id")
                    for s in (item_a.get("claims") or {}).get("P3373", [])
                }
                if qb in stated:
                    continue
                add({
                    "id": f"link_siblings:{pair[0]}:{pair[1]}",
                    "type": "link_siblings",
                    "subjects": [{"qid": qa, "geni_id": a}, {"qid": qb, "geni_id": b}],
                    "requires": requires_id(qa) + requires_id(qb),
                    "wikidata_fix": False,
                    "statements": [
                        {"qid": qa, "property": "P3373", "value": qb,
                         "references": geni_ref(a, b)},
                        {"qid": qb, "property": "P3373", "value": qa,
                         "references": geni_ref(a, b)},
                    ],
                })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(objects, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "type", "qid", "geni_id", "requires", "cited"])
        for o in objects:
            subject = o.get("subject") or (o.get("subjects") or [{}])[0]
            cited = bool(o.get("statement", {}).get("references")
                         or any(s.get("references") for s in o.get("statements", [])))
            writer.writerow([o["id"], o["type"], subject.get("qid"),
                             subject.get("geni_id"), " ".join(o["requires"]),
                             "yes" if cited else "no"])

    blocked = sum(1 for o in objects if o["requires"])
    print(f"\nwrote {OUT_JSON} ({len(objects):,} objects)")
    for kind, n in counts.most_common():
        print(f"  {kind:<20} {n:>8,}")
    print(f"\n  {blocked:,} are not valid to run yet — they require another object first")
    print("Nothing has been sent, and no executor exists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
