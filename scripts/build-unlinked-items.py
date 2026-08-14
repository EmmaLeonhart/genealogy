"""Two Wikidata items to create standalone, on 2026-09-30.

Emma, 2026-08-13: *"create wikidata items for [Baruch Jafe] and [Samuell
Standen] on September 30 as independent unlinked items completely independently
of their links elsewhere... these appear to have gotten into the data somehow but
are apparently completely unlinked and I still want them to get in."*

**Unlinked is the starting point, not the goal.** Emma, 2026-08-13: *"I want
everything on geni naturally linked to wikidata but also ideally linked into both
of their world trees."* Both — Geni's tree and Wikidata's. These two items are
created standalone because *"this allows for the wikidata stuff to finally start
doing connections"*: an item has to exist before anything can point at it.

**Nothing to point at yet.** Neither man's father, mother, spouse or child
carries a Wikidata item — checked against `reports/derived-labels.csv`, all six
have no QID — so a `P22`/`P25`/`P26`/`P40` would have no target regardless of how
well connected the Geni side is. That, not the Geni component structure, is why
these are unlinked on the day.

**The Geni side is no longer symmetric between them**, which is worth stating
because it stops being a reason to treat them alike. Samuell Standen joined the
main tree on 2026-08-13 when Emma's `Forest` of `6000000227226600829` bridged the
Standen ball; Baruch Jafe is still inside the remaining cut-off component of
4,088. Each item carries only what stands on its own: label, `P31` human, `P2600`
Geni ID, `P21` sex, and the dates Geni records — every statement referenced to
the Geni ID. The links follow later, as their relatives get items.

**Places are absent too, for a different reason.** Geni gives Samuell Standen
"Sussex, England" as free text, and turning that into an item means asking
Wikidata which item it is — which this repo does not do (CLAUDE.md § *Never query
Wikidata to check something*). It stays out until the local Wikidata store can
answer it offline.

Same object shape as `build-priority-chain.py`, so whatever executes one can
execute the other. These carry `"priority": false` and a `"scheduled"` date —
they are queued to be written, not to be raced.

Writes `out/wikidata/unlinked-items.json` and `reports/unlinked-items.md`.

    py scripts/build-unlinked-items.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
FACTS = REPO_ROOT / "reports" / "derived-facts.csv"
FAMILY = REPO_ROOT / "reports" / "derived-family.csv"
OUT_JSON = REPO_ROOT / "out" / "wikidata" / "unlinked-items.json"
OUT_MD = REPO_ROOT / "reports" / "unlinked-items.md"

csv.field_size_limit(10_000_000)

SCHEDULED = "2026-09-30"
SEX = {"M": "Q6581097", "F": "Q6581072"}

#: Geni ID -> the URL Emma gave, kept so the report links where she linked.
SUBJECTS = {
    "6000000040078764766": "https://www.geni.com/people/Baruch-Jafe/6000000040078764766",
    "6000000107265740881": "https://www.geni.com/people/Samuell-Standen/6000000107265740881",
}

#: GEDCOM event -> (Wikidata property, which columns hold it). Burial date is
#: its own property rather than a qualifier on P119 — see CLAUDE.md's table.
DATES = [("birth", "P569"), ("death", "P570"), ("burial", "P4602")]


def geni_ref(*ids: str) -> list[dict]:
    return [{"property": "P2600", "value": i} for i in ids if i]


def date_statement(row: dict, kind: str, prop: str, geni_id: str) -> dict | None:
    iso = row.get(f"{kind}_date_iso")
    if not iso:
        return None
    return {
        "property": prop,
        "value": {
            "time": iso,
            "precision": int(row[f"{kind}_date_precision"]),
            "raw": row.get(f"{kind}_date_raw", ""),
        },
        "references": geni_ref(geni_id),
    }


def main() -> int:
    lab_all = {r["geni_id"]: r for r in csv.DictReader(open(LABELS, encoding="utf-8"))}
    lab = {g: r for g, r in lab_all.items() if g in SUBJECTS}
    fac = {r["geni_id"]: r for r in csv.DictReader(open(FACTS, encoding="utf-8"))
           if r["geni_id"] in SUBJECTS}
    fam = {r["geni_id"]: r for r in csv.DictReader(open(FAMILY, encoding="utf-8"))
           if r["geni_id"] in SUBJECTS}

    missing = [g for g in SUBJECTS if g not in lab]
    if missing:
        print(f"not in reports/derived-labels.csv: {missing}", file=sys.stderr)
        return 1

    objects: list[dict] = []
    for geni_id, url in SUBJECTS.items():
        label = lab[geni_id]["label_en"]
        facts = fac.get(geni_id, {})
        qid = lab[geni_id].get("qid") or None
        if qid:
            print(f"{label} already has {qid} — creation would duplicate it",
                  file=sys.stderr)
            return 1

        statements = [
            {"property": "P31", "value": "Q5", "references": geni_ref(geni_id)},
            {"property": "P2600", "value": geni_id, "references": []},
        ]
        sex = SEX.get(facts.get("sex", ""))
        if sex:
            statements.append({"property": "P21", "value": sex,
                               "references": geni_ref(geni_id)})
        for kind, prop in DATES:
            st = date_statement(facts, kind, prop, geni_id)
            if st:
                statements.append(st)

        objects.append({
            "id": f"create_individual:{geni_id}",
            "type": "create_individual",
            "priority": False,
            "scheduled": SCHEDULED,
            "subject": {"qid": None, "geni_id": geni_id},
            "requires": [],
            "anchor": None,
            "labels": {"en": label, "mul": label},
            "statements": statements,
            "links": [],
            "geni_url": url,
        })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(objects, ensure_ascii=False, indent=1),
                        encoding="utf-8")

    L: list[str] = []
    add = L.append
    add("# Two unlinked items, to create on 2026-09-30")
    add("")
    add("Emma, 2026-08-13: *\"create wikidata items for [these two] on September 30")
    add("as independent unlinked items completely independently of their links")
    add("elsewhere... these appear to have gotten into the data somehow but are")
    add("apparently completely unlinked and I still want them to get in.\"*")
    add("")
    add(f"**{len(objects)} creations, scheduled `{SCHEDULED}`.** Queued the way the")
    add("Charlemagne route is queued — written down as edit objects now, executed")
    add("later. `out/wikidata/unlinked-items.json` is the machine-readable half and")
    add("shares its shape with `out/wikidata/priority-chain.json`.")
    add("")
    add("| geni id | label | sex | born | died | buried | statements |")
    add("| --- | --- | --- | --- | --- | --- | ---: |")
    for o in objects:
        gid = o["subject"]["geni_id"]
        f = fac.get(gid, {})
        add(f"| [`{gid}`]({o['geni_url']}) | {o['labels']['en']} | {f.get('sex','') or '—'} "
            f"| {f.get('birth_date_raw','') or '—'} | {f.get('death_date_raw','') or '—'} "
            f"| {f.get('burial_date_raw','') or '—'} | {len(o['statements'])} |")
    add("")
    add("## What is deliberately not on them")
    add("")
    add("**No relationship statements — because there is nothing to point at.**")
    add("Every relative either man has is listed below, and **not one of them")
    add("carries a Wikidata item**. A `P22`/`P25`/`P26`/`P40` needs a target QID,")
    add("so the links wait until those relatives have items of their own.")
    add("")
    for gid in SUBJECTS:
        r = fam.get(gid, {})
        bits = []
        for k in ("father", "mother", "spouses", "children"):
            for other in (r.get(k) or "").split(";"):
                other = other.strip()
                if not other:
                    continue
                orow = lab_all.get(other, {})
                name = orow.get("label_en") or other
                q = orow.get("qid")
                bits.append(f"{k[:-1] if k.endswith('s') else k} {name} "
                            f"`{other}`{' ' + q if q else ' (no item)'}")
        add(f"- **{lab[gid]['label_en']}** `{gid}` — "
            + ("; ".join(bits) if bits else "no recorded relatives"))
    add("")
    add("**The Geni side differs between them, and that is not why.** Samuell")
    add("Standen joined the main tree on 2026-08-13, when a `Forest` of")
    add("`6000000227226600829` bridged the ball he sat in. Baruch Jafe is still")
    add("inside the remaining cut-off component of 4,088 people. Both are queued the")
    add("same way regardless: the goal is everything on Geni linked to Wikidata and")
    add("into both world trees, and an item has to exist before it can be connected.")
    add("")
    add("**No places.** Geni gives Samuell Standen \"Sussex, England\" as free text.")
    add("Resolving that to an item means asking Wikidata which item it is, and this")
    add("repo does not query Wikidata — it waits for the local store. `P19`/`P20`")
    add("stay off until that can be answered offline.")
    add("")
    add("## The properties used")
    add("")
    add("| property | what | reference |")
    add("| --- | --- | --- |")
    add("| P31 | instance of `Q5` human | P2600 |")
    add("| P2600 | Geni.com profile ID | — (it is the citation) |")
    add("| P21 | sex or gender | P2600 |")
    add("| P569 / P570 | date of birth / death | P2600 |")
    add("| P4602 | date of burial or cremation | P2600 |")
    add("")
    add("Dates carry the GEDCOM precision Geni stated — 9 year, 10 month, 11 day —")
    add("never widened or narrowed. The raw GEDCOM text rides along in the JSON so a")
    add("reviewer can see what was read.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_JSON} and {OUT_MD}")
    for o in objects:
        print(f"  {o['labels']['en']}: {len(o['statements'])} statements, "
              f"scheduled {o['scheduled']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
