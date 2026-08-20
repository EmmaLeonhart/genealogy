"""Wikidata's own English label for people who have none of ours.

**The label we would generate is worse than the one already published**, and that was
measured rather than assumed: `reports/cjk-romanisation-validation.md` compares this
repo's romanisations against Wikidata's English labels for the same people and finds ours
is the given name alone — `Shi Min` where Wikidata says `Emperor Taizong of Tang`, `Lu`
where it says `Tang of Shang`.

So wherever a person is linked to an item that carries an English label, that label is the
better name, and **17,721 of our people are linked**. 12,334 already have a local English
label and need nothing. **5,387 do not, and 5,208 of those have one on Wikidata** — Jacques
Offenbach, Tokugawa Hidetada, David HaLevi Segal, Shimazu Tadahisa.

This is not a CJK job. It fell out of the CJK work because that is where the comparison was
made, but the population is every linked person, and the beneficiary is the relationship
label: `daughter of <name>` needs a name for the *relative*, and 9,285 placeholder edits had
none because no relative had one.

**It writes a mapping, not an edit.** Nothing here proposes changing Wikidata; the direction
is the other way, taking a published label as the best available name for our own labelling.

    py scripts/build-linked-english-labels.py

Offline: `reports/derived-family.csv`, `reports/derived-labels.csv`, the local store.
Writes `reports/linked-english-labels.csv`.
"""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from genimerge import wikistore  # noqa: E402

FAMILY = REPO / "reports" / "derived-family.csv"
LABELS = REPO / "reports" / "derived-labels.csv"
STORE = REPO / "wikidata" / "items"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
OUT = REPO / "reports" / "linked-english-labels.csv"

csv.field_size_limit(10 ** 7)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    qid = {}
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r.get("qid"):
                qid[r["geni_id"]] = r["qid"]
    local = set()
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if (r.get("label_en") or "").strip():
                local.add(r["geni_id"])

    missing = {g: q for g, q in qid.items() if g not in local}
    print(f"linked people: {len(qid):,}; already labelled here: {len(qid) - len(missing):,}; "
          f"unlabelled: {len(missing):,}")

    ids = sorted(set(missing.values()))
    label = {}
    with wikistore.StoreReader(STORE, INDEX) as rd:
        for i in range(0, len(ids), 5000):
            for q, e in rd.entities(ids[i:i + 5000]).items():
                L = {k: v["value"] for k, v in (e.get("labels") or {}).items()}
                v = L.get("en") or L.get("mul")
                if v:
                    label[q] = v

    rows = [(g, q, label[q]) for g, q in sorted(missing.items()) if q in label]
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geni_id", "qid", "label_en"])
        w.writerows(rows)
    print(f"  of those, Wikidata has an English label for: {len(rows):,}")
    print(f"wrote {OUT}")
    for g, q, v in rows[:10]:
        print(f"    {q:11} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
