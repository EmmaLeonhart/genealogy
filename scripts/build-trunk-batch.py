"""The bridge trunk: create the few people every saved path runs through.

**Agenda task A, Emma 2026-08-15:** *"Connecting myself with these other
researchers on Wikidata."* And on how the bridging should work: *"finding the
nearest person with a Wikidata ID to me, adding that, forming the bridge of that,
doing that for the next and so on."*

**The measurement says the nearest useful people are her own family, and they do
not exist on Wikidata.** Over the 560 saved paths:

| paths through | who | on Wikidata |
| ---: | --- | --- |
| 597 | Richard Wade Borsheim | no |
| 434 | Randolph Paulus Borsheim | no |
| 380 | Reinhert Borsheim | no |
| 204 | Helen Frisk / Hans Bertil Frisk | no |
| 194 | Beda Elvira Wedberg | no |

**8,987 of the 9,211 people named across those paths have no Wikidata item.** So
the first bridge is not a distant notable — it is the trunk of her own ancestry,
which every path already crosses. Creating it once means each isolate attached
afterwards reaches Wikidata *through* the trunk rather than needing its own chain.

**`P2600` first, then everything else.** `CLAUDE.md` § *An item with no
relationships is not a missing item*: *"The Jenny ID needs to be present before
any properties derived from Jenny can be taken from it, or before any
relationships can be added."* Every creation here leads with the Geni ID and every
subsequent statement is referenced to that profile.

**Relationships are emitted only where BOTH ends are in the batch or already have
a QID.** A `P22` pointing at a person who does not exist yet is unusable, and the
runner would reject it. The dependency order is recorded so a caller executes
parents before children.

**Nothing is executed.** This writes a reviewable batch;
`scripts/wikidata-edit-run.py` is the only thing that talks to Wikidata and it is
dry-run by default. Emma's standing rule: no Wikidata edits before 1 September.

Writes `reports/wikidata-trunk-batch.json` and `reports/trunk-batch.csv`.

    py scripts/build-trunk-batch.py --min-paths 20
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import labels as _labels  # noqa: E402  — the single marker vocabulary


def label_set(label: str) -> dict:
    """`mul` and `en` for a derived label, with markers kept out of `en`.

    This script copied the derived label straight into both slots, which shipped
    `Private` as a Wikidata label on one item and `ukjent Knutsdatter` on another.
    `CLAUDE.md` is explicit that `Private` must never be a label at all, and Emma
    2026-08-16: *"no local language should have"* `NN`.

    The same three cases the rest of the pipeline uses:

    * the whole label is a marker  -> `mul: NN`, no `en`
    * a marker leading a real surname -> `mul: NN <surname>`, no `en`; the surname
      is real data and discarding it loses the 3,605 surnames `CLAUDE.md` counts
    * anything else -> the label, unchanged, in both

    `en` is simply absent rather than guessed: this script has no relatives to
    build a description from, and inventing one is the failure being prevented.
    """
    text = (label or "").strip()
    if not text:
        return {}
    if _labels.is_redacted(text) or _labels.is_placeholder_form(text):
        return {"mul": _labels.UNNAMED_MARKER}
    if _labels.leads_with_a_marker(text):
        rest = " ".join(text.split()[1:]).strip()
        return {"mul": f"{_labels.UNNAMED_MARKER} {rest}".strip()}
    return {"en": text, "mul": text}

BRIDGE = REPO / "reports" / "path-bridge-targets.csv"
FAMILY = REPO / "reports" / "derived-family.csv"
#: **Labels come from `derived-labels.csv`, never from `display-names.csv`.**
#: The latter holds raw `NAME` records straight out of the GEDCOM, which for Emma
#: still contains the surname removed on 2026-08-12. `CLAUDE.md` § *Her name is
#: Emma Leonhart*: the removed name is never written down again, and
#: `derive-labels.py` is where the correction is applied. Reading the raw column
#: put the old name into a generated Wikidata label on the first run of this
#: script.
LABELS = REPO / "reports" / "derived-labels.csv"
FACTS = REPO / "reports" / "derived-facts.csv"
OUT_JSON = REPO / "reports" / "wikidata-trunk-batch.json"
OUT_CSV = REPO / "reports" / "trunk-batch.csv"

csv.field_size_limit(10_000_000)

HUMAN, GENI_ID = "Q5", "P2600"
FATHER, MOTHER, SEX = "P22", "P25", "P21"
INSTANCE_OF = "P31"
SEX_ITEM = {"M": "Q6581097", "F": "Q6581072"}


def geni_reference(geni_id: str) -> list[dict]:
    """Every Geni-derived statement cites the profile it came from."""
    return [{"property": "P854", "value": f"https://www.geni.com/people/x/{geni_id}"},
            {"property": "P813", "value": "2026-08-15"}]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-paths", type=int, default=20,
                    help="only people on at least this many of the 560 paths")
    args = ap.parse_args()

    trunk: dict[str, int] = {}
    with BRIDGE.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["qid"]:
                continue                      # already on Wikidata, nothing to create
            n = int(row["paths_through"])
            if n >= args.min_paths:
                trunk[row["geni_id"]] = n
    print(f"{len(trunk)} people on >= {args.min_paths} paths with no Wikidata item")

    fam: dict[str, dict] = {}
    with FAMILY.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            fam[row["geni_id"]] = row

    name_of: dict[str, str] = {}
    with LABELS.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            name_of[row["geni_id"]] = (row.get("label_en") or "").strip()

    sex_of: dict[str, str] = {}
    if FACTS.exists():
        with FACTS.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                sex_of[row["geni_id"]] = (row.get("sex") or "").strip()

    qid_of = {g: (r.get("qid") or "").strip() for g, r in fam.items() if (r.get("qid") or "").strip()}

    # **Anything Emma resolved by hand already exists and must not be created.**
    # `entity_resolution.md` is her scratchpad of Geni-to-Wikidata identities;
    # `Q232803` is her own item, which carries no `P2600` and is therefore
    # invisible to the `qid` column of `derived-family.csv`. The first run of this
    # script proposed creating her a second item.
    # **`entity_resolution.md` is gone and nothing may read it.** Emma, 2026-08-31: *"no
    # files should read it lol."* It was deleted in `12f3134a` and the readers were not;
    # every one of them either crashed or degraded silently, which `CLAUDE.md` § *Systematic
    # review for legacy code* names as the worse of the two.
    trunk = {g: n for g, n in trunk.items() if g not in qid_of}
    print(f"{len(trunk)} after removing people who already have an item")

    # Order parents before children so a caller can execute top-down and never
    # reference an item that does not exist yet.
    def depth(g: str, seen=None) -> int:
        seen = seen or set()
        if g in seen:
            return 0
        seen.add(g)
        row = fam.get(g) or {}
        ups = [x for x in ((row.get("father") or "").strip(),
                           (row.get("mother") or "").strip()) if x in trunk]
        return 1 + max([depth(u, seen) for u in ups], default=0)

    ordered = sorted(trunk, key=lambda g: (-depth(g), -trunk[g]))

    edits, rows = [], []
    for gid in ordered:
        row = fam.get(gid) or {}
        label = name_of.get(gid, "")
        statements = [
            {"property": GENI_ID, "value": gid,
             "references": geni_reference(gid)},
            {"property": INSTANCE_OF, "value": HUMAN,
             "references": geni_reference(gid)},
        ]
        sex = SEX_ITEM.get(sex_of.get(gid, ""))
        if sex:
            statements.append({"property": SEX, "value": sex,
                               "references": geni_reference(gid)})
        # A parent link only where the parent is creatable in this batch or
        # already has an item. Anything else would dangle.
        links = []
        for prop, key in ((FATHER, "father"), (MOTHER, "mother")):
            p = (row.get(key) or "").strip()
            if not p:
                continue
            if p in qid_of:
                links.append({"property": prop, "value": qid_of[p],
                              "references": geni_reference(gid)})
            elif p in trunk:
                links.append({"property": prop, "value": f"NEW:{p}",
                              "references": geni_reference(gid)})
        edits.append({
            "id": f"trunk:{gid}",
            "type": "create_individual",
            "source": "bridge trunk - agenda task A",
            "subject": {"qid": None, "geni_id": gid},
            "labels": label_set(label),
            "paths_through": trunk[gid],
            "statements": statements,
            "links": links,
        })
        rows.append([trunk[gid], gid, label, sex_of.get(gid, ""),
                     (row.get("father") or ""), (row.get("mother") or ""),
                     len(links)])

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(edits, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        w = csv.writer(handle)
        w.writerow(["paths_through", "geni_id", "label", "sex",
                    "father_geni_id", "mother_geni_id", "parent_links"])
        w.writerows(rows)

    total = sum(trunk.values())
    print(f"\nwrote {OUT_JSON} ({len(edits)} creations) and {OUT_CSV}")
    print(f"those {len(edits)} people carry {total:,} path-slots between them\n")
    for r in rows[:15]:
        print(f"  {r[0]:>4} paths  {r[2][:40]:<42} {r[6]} parent link(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
