"""Step 2 of Emma's label order: `mul` for every individual, derived from `en`.

**Emma, 2026-08-17:** *"then mul gets made for every individual (almost always derived
from en)"*. This mirrors `reports/wikidata-en-labels.json`, which is step 1.

**"Almost always" is doing real work in that sentence, and this is where it bites.** A
`mul` label is the name a person is known by across languages. Two of step 1's three
sources are names; the third is not.

* **Wikidata's own English label** -- a name. `mul` mirrors it.
* **A romanised Han name** -- a name. `mul` mirrors it.
* **A relationship label**, `husband of Lakech Gashawbeza` -- **not a name.** It describes
  somebody by who they are related to, and copying it into `mul` would assert across every
  language that this is what the person is called. Emma ruled on exactly this shape on
  2026-08-17: *"And NN for mul there"*. Those people already receive `mul: NN` from
  `build-placeholder-label-batch.py`, so this batch leaves them alone rather than
  overwriting a correct marker with a description.

So step 2 is not a blind mirror of step 1, and the difference is 7,401 people.

    py scripts/build-mul-label-batch.py

Offline. Writes `reports/wikidata-mul-labels.json`. Emits nothing to Wikidata.
"""

from __future__ import annotations

import io
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EN = REPO / "reports" / "wikidata-en-labels.json"
OUT = REPO / "reports" / "wikidata-mul-labels.json"
MD = REPO / "reports" / "wikidata-mul-labels.md"

#: The step-1 sources that are a NAME. A relationship label is deliberately absent.
NAME_SOURCES = ("wikidata's own English label", "romanised from")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    step1 = json.loads(io.open(EN, encoding="utf-8").read())
    print("step 1 edits: %d" % len(step1))

    edits, skipped = [], Counter()
    for e in step1:
        why = e.get("derived_from", "")
        if not any(why.startswith(p) for p in NAME_SOURCES):
            skipped[why] += 1
            continue
        g = e["subject"]["geni_id"]
        edits.append({
            "id": "mul_label:%s" % g,
            "type": "set_label",
            "source": "step 2 of Emma's label order",
            "subject": {"qid": None, "geni_id": g},
            "requires": ["en_label:%s" % g],
            "label": {"language": "mul", "value": e["label"]["value"]},
            "kind": "add",
            "derived_from": "en, which came from %s" % why,
        })
    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    by = Counter(e["derived_from"] for e in edits)
    md = ["# Step 2 — `mul` for every individual, derived from `en`", "",
          "Built by `scripts/build-mul-label-batch.py`. **Emits nothing to Wikidata.**", "",
          "Emma, 2026-08-17: *\"then mul gets made for every individual (almost always "
          "derived from en)\"*.", "",
          "- step 1 `en` edits: **%d**" % len(step1),
          "- `mul` mirrored from them: **%d**" % len(edits),
          "- deliberately not mirrored: **%d**" % sum(skipped.values()), "",
          "## Why %d are left alone" % sum(skipped.values()), "",
          "*\"Almost always\"* is doing the work in her sentence. A relationship label — "
          "`husband of Lakech Gashawbeza` — is **not a name**; copying it into `mul` would "
          "assert across every language that this is what the person is called. She ruled "
          "on this shape on 2026-08-17: *\"And NN for mul there\"*, and those people already "
          "get `mul: NN` from `build-placeholder-label-batch.py`. Overwriting a correct "
          "marker with a description would be a regression.", "",
          "| mirrored from | people |", "| --- | ---: |"]
    md += ["| %s | %d |" % (k, v) for k, v in by.most_common()]
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("  mul mirrored: %d; left alone: %d" % (len(edits), sum(skipped.values())))
    for k, v in skipped.most_common():
        print("    left alone: %-28s %d" % (k, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
