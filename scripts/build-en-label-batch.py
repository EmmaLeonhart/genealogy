"""Step 1 of Emma's label order: an `en` label for every individual who lacks one.

**Emma, 2026-08-17:** *"makes en labels for every individual (so Japanese gets
transcribed)... all of the en labels are done at the same time as one step, and then mul,
then ja, then zh, then others."*

**This is that step, and only that step.** `mul` follows from `en` and is the next batch;
nothing here emits `mul`, `ja` or `zh`.

**Her order is the one that works.** `emission-spec.md` had `mul` first with `en` derived
from it, which has no route at all for a person whose name is written only in Han
characters. Making `en` first, by transcribing, is what gives those people anything to
derive a `mul` from.

WHERE EACH LABEL COMES FROM, IN PRIORITY ORDER

1. **Wikidata's own English label**, for a linked person who has none of ours. It is a
   whole name -- `Emperor Taizong of Tang` -- where anything we derive is a fragment.
   5,208 people. (`reports/linked-english-labels.csv`)
2. **The romanisation**, for a Han-only name. Given name only, syllables separated, and
   checked against Wikidata's own labels at 91.8%. (`reports/cjk-romanisation.csv`)
3. **The relationship label**, for a placeholder-named person -- `daughter of Olof
   Larsson`. (`reports/wikidata-placeholder-labels.json`)

**A marker is not an `en` label and is not emitted here.** `NN` belongs in `mul`, which is
`build-marker-label-fixes.py`'s job and already built. A person whose name is only a marker
appears in this file's *shortfall* count, not in its edits.

    py scripts/build-en-label-batch.py

Offline. Writes `reports/wikidata-en-labels.json`. Emits nothing to Wikidata.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LABELS = REPO / "reports" / "derived-labels.csv"
LINKED = REPO / "reports" / "linked-english-labels.csv"
ROMAN = REPO / "reports" / "cjk-romanisation.csv"
PLACE = REPO / "reports" / "wikidata-placeholder-labels.json"
OUT = REPO / "reports" / "wikidata-en-labels.json"
MD = REPO / "reports" / "wikidata-en-labels.md"

csv.field_size_limit(10 ** 7)
SCRIPTED = re.compile(r"[\u3400-\u9fff\u3040-\u30ff\uac00-\ud7af]")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    need, has_cjk = [], set()
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if (r.get("label_en") or "").strip():
                continue
            need.append(r["geni_id"])
            if SCRIPTED.search(r.get("cjk_names") or ""):
                has_cjk.add(r["geni_id"])
    need = set(need)
    print("individuals with no English label: %d (%d of them written in CJK)"
          % (len(need), len(has_cjk)))

    src = {}
    with io.open(LINKED, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["geni_id"] in need and r["label_en"].strip():
                src[r["geni_id"]] = (r["label_en"].strip(), "wikidata's own English label")
    with io.open(ROMAN, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            v = (r.get("romanised") or "").strip()
            if v and r["geni_id"] in need and r["geni_id"] not in src:
                src[r["geni_id"]] = (v, "romanised from %s" % r["culture"])
    for e in json.loads(io.open(PLACE, encoding="utf-8").read()):
        g = (e.get("subject") or {}).get("geni_id")
        v = (e.get("labels") or {}).get("en")
        if g and v and g in need and g not in src:
            src[g] = (v, "relationship label")

    edits = [{
        "id": "en_label:%s" % g,
        "type": "set_label",
        "source": "step 1 of Emma's label order",
        "subject": {"qid": None, "geni_id": g},
        "requires": [],
        "label": {"language": "en", "value": v},
        "kind": "add",
        "derived_from": why,
    } for g, (v, why) in sorted(src.items())]
    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    by = Counter(why for _, why in src.values())
    short = len(need) - len(src)
    md = ["# Step 1 — an `en` label for every individual who lacks one", "",
          "Built by `scripts/build-en-label-batch.py`. **Emits nothing to Wikidata.**", "",
          "Emma, 2026-08-17: *\"makes en labels for every individual (so Japanese gets "
          "transcribed)... all of the en labels are done at the same time as one step, and "
          "then mul, then ja, then zh.\"* This is that step and only that step.", "",
          "- individuals with no English label: **%d**" % len(need),
          "- of those, an `en` is now available: **%d**" % len(src),
          "- still without one: **%d**" % short, "",
          "| where the label comes from | people |", "| --- | ---: |"]
    md += ["| %s | %d |" % (k, v) for k, v in by.most_common()]
    md += ["", "**A marker is not an `en` label.** `NN` belongs in `mul`, which "
           "`build-marker-label-fixes.py` already emits, so a person whose name is only a "
           "marker is counted in the shortfall above rather than given a false name here."]
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("  en now available for %d; still short %d" % (len(src), short))
    for k, v in by.most_common():
        print("    %-32s %d" % (k, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
