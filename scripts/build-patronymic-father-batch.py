"""Emit the creation batch for the fathers the patronymics imply.

**Emma's item.** Both blockers were settled on 2026-08-19. Sourcing: *"reference the
bearer's profile"* -- each father is attested by the child whose patronymic names him, so
every statement carries that child's `P2600` as its reference. Unit: *"If you don't know
the people are siblings you create one per individual"*, with her one exception -- a shared
mother plus the same implied name is one man.

**These are the first creations in this repo with no `P2600` of their own.** Every other
created item is a Geni profile getting a Wikidata item; these people have no Geni profile
at all. They exist because the patronymic attests them, so `subject.geni_id` is null and
the Geni ID appears only in the *references*, pointing at the child.

WHAT IS EMITTED PER FATHER

    create_individual   labels mul+en = his given name, P31 Q5 human, P21 male
    add_relationship    P22 on each bearer -> @patronymic_father:<group>

**The name is never derived from the string.** It is the modal given name of the CONFIRMED
fathers of that same token in `reports/patronymic-classification.csv` -- `Olsen` implies
*Ole* because 1,809 real `Olsen` fathers are called Ole. Bearers whose token has no
confirmed father anywhere get no item, because there would be nothing to call him.

**Nothing here runs.** The 1 September rule stands; this writes a JSON file.

    py scripts/build-patronymic-father-batch.py

Offline: reports/patronymic-fathers.csv. Writes reports/wikidata-patronymic-fathers.json.
"""

from __future__ import annotations

import csv
import io
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "reports" / "patronymic-fathers.csv"
OUT = REPO / "reports" / "wikidata-patronymic-fathers.json"
MD = REPO / "reports" / "wikidata-patronymic-fathers.md"

csv.field_size_limit(10 ** 7)
HUMAN, MALE = "Q5", "Q6581097"


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    groups = defaultdict(list)
    with io.open(SRC, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            key = r["father_group"] if r["father_group"] != "own" else "own:" + r["geni_id"]
            groups[key].append(r)

    edits = []
    for key in sorted(groups):
        rows = sorted(groups[key], key=lambda r: r["geni_id"])
        name = rows[0]["implied_father_given_name"]
        fid = "patronymic_father:" + key.replace(":", "_")
        # Every statement is attested by the child. For a shared father the first bearer
        # is the reference and the rest are recorded in `attested_by`, so the edit says
        # which profiles the claim rests on rather than silently picking one.
        ref = [{"property": "P2600", "value": rows[0]["geni_id"]}]
        edits.append({
            "id": fid,
            "type": "create_individual",
            "source": "patronymic",
            "subject": {"qid": None, "geni_id": None},
            "requires": [],
            "labels": {"mul": name, "en": name},
            "statements": [
                {"property": "P31", "value": HUMAN, "references": ref},
                {"property": "P21", "value": MALE, "references": ref},
            ],
            "links": [],
            "attested_by": [r["geni_id"] for r in rows],
            "note": ("inferred from the patronymic %s borne by %d child(ren); no Geni "
                     "profile exists for him" % (rows[0]["token"], len(rows))),
        })
        for r in rows:
            edits.append({
                "id": "patronymic_father_link:%s" % r["geni_id"],
                "type": "add_relationship",
                "source": "patronymic",
                "subject": {"qid": None, "geni_id": r["geni_id"]},
                "requires": [fid],
                "property": "P22",
                "value": "@" + fid,
                "references": [{"property": "P2600", "value": r["geni_id"]}],
                "note": "%s implies a father called %s" % (r["token"], name),
            })

    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    creates = sum(1 for e in edits if e["type"] == "create_individual")
    links = len(edits) - creates
    shared = sum(1 for e in edits if e["type"] == "create_individual" and len(e["attested_by"]) > 1)
    names = Counter(e["labels"]["en"] for e in edits if e["type"] == "create_individual")
    md = ["# Creating the fathers the patronymics imply", "",
          "Built by `scripts/build-patronymic-father-batch.py`. **Nothing runs before "
          "1 September.**", "",
          "- fathers created: **%d**  (%d of them shared by siblings)" % (creates, shared),
          "- `P22` links added to bearers: **%d**" % links,
          "- total edit objects: **%d**" % len(edits), "",
          "**No `P2600` on the subject.** These are the first creations here for people with "
          "no Geni profile at all. The Geni ID appears only as the *reference* on every "
          "statement, pointing at the child whose patronymic attests him — Emma's ruling of "
          "2026-08-19.", "",
          "**The name is never derived from the string**: it is the modal given name of the "
          "confirmed fathers of that token. `Olsen` implies *Ole* because 1,809 real "
          "`Olsen` fathers are called Ole.", "",
          "| father | items |", "| --- | ---: |"]
    md += ["| %s | %d |" % (k, v) for k, v in names.most_common(20)]
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("fathers created: %d (%d shared); P22 links: %d; total edits: %d"
          % (creates, shared, links, len(edits)))
    print("wrote %s" % OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
