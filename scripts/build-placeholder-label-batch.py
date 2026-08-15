"""Labels for every placeholder-named person, as JSON edit objects.

Queue items 7 and 8, which are one job: the `mul` label is the normalisation and
the per-language label is the generated relationship. Both were settled by Emma
on 2026-08-15 after she read the preview, so this generates rather than asks.

**`mul` — the normalisation.** Every placeholder given-name form collapses to
`NN`, or `NN <surname>` where a real surname exists. A surname that is *itself*
placeholder vocabulary — `NN ???`, `NN N.N.`, `NN Unknown` — collapses to bare
`NN`; her call, 351 people.

**`en` — the relationship label.** Precedence parent, spouse, child, giving
`daughter of Olof Larsson`, `wife of Rostaing Arbald`. Her rulings, both applied:

* **Everyone with a placeholder given name gets one**, including the 3,934 who
  already carry a surname, and including the 331 whose surname also appears
  inside the generated label. Shown the rows, she chose to generate: the label
  still carries a given name the `mul` label does not.
* **A redacted or placeholder relative is skipped** and the precedence falls
  through to the next one, trying every spouse and child. This is why no label
  reads *"husband of `<private>` Gaya Pereira"* — there were 2,730 of those.

**The surname is kept, and the reason is the measurement.** A relative has a real
name for 69% of bare-`NN` people but only 36% of `NN <surname>` ones. Emma read
that correctly where I had it backwards: *"the surname ones being badly connected
is kind of evidence in favour of the fact that we need to keep the surname."* For
that population the relationship label usually cannot be built at all, so the
surname is the only informative thing they have.

**No `ja` or `zh` is emitted here and that is queue item 9, not an oversight.**
Emma requires English, Japanese, Chinese and `mul` on everything. `en` comes free
because the relative's own label is English; `ja` and `zh` have to be
*constructed*, since Japanese is not in Wikidata's top 18 languages by coverage
and cannot be copied from a relative. Every edit records which languages it is
missing so item 9 can find them.

**Unknown sex takes the neutral form** — `child of`, `spouse of`. No gender is
inferred to make a label read better.

Writes `reports/wikidata-placeholder-labels.json`.

    py scripts/build-placeholder-label-batch.py
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PREVIEW = REPO / "reports" / "relationship-label-preview.csv"
PAIRS = REPO / "reports" / "geni-wikidata-pairs.csv"
OUT = REPO / "reports" / "wikidata-placeholder-labels.json"

csv.field_size_limit(10 ** 7)

#: Emma, 2026-08-15: English, Japanese and Chinese on everything, plus `mul`.
REQUIRED = ("en", "ja", "zh")


def main() -> int:
    if not PREVIEW.exists():
        print(f"no {PREVIEW}; run scripts/build-relationship-label-preview.py first",
              file=sys.stderr)
        return 1

    rows = list(csv.DictReader(PREVIEW.open(encoding="utf-8", newline="")))
    print(f"{len(rows):,} people carry a placeholder given name")

    edits, counts = [], Counter()
    for r in rows:
        gid = r["geni_id"]
        labels = {"mul": r["mul_label"]}
        if r.get("generated_en"):
            labels["en"] = r["generated_en"]
        missing = [l for l in REQUIRED if l not in labels]
        counts["with an en label" if "en" in labels else "mul only"] += 1
        counts[r["population"]] += 1
        edits.append({
            "id": f"placeholder_label:{gid}",
            "type": "set_labels",
            "source": "geni placeholder normalisation",
            # No QID: these people are overwhelmingly not on Wikidata yet, so the
            # labels attach to whatever creates them. An edit runner resolves it
            # by Geni ID, the same key everything else in this repo joins on.
            "subject": {"qid": None, "geni_id": gid},
            "requires": [],
            "labels": labels,
            "missing_languages": missing,
            "relation_used": r.get("relation_used") or None,
            "via_geni_id": r.get("via_geni_id") or None,
            "skipped_a_relative": r.get("skipped_a_relative") or None,
        })

    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT} ({len(edits):,} set_labels edits)\n")
    for k, v in counts.most_common():
        print(f"  {v:>7,}  {k}")
    print(f"\n  {sum(1 for e in edits if 'ja' in e['missing_languages']):>7,}  "
          "still need a ja label - queue item 9")
    print(f"  {sum(1 for e in edits if 'zh' in e['missing_languages']):>7,}  "
          "still need a zh label - queue item 9")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
