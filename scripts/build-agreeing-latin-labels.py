"""Where a person's Latin name records AGREE, that agreement is the `en` and the `mul` label.

    py scripts/build-agreeing-latin-labels.py

**Emma, 2026-09-01, giving the rule outright:** *"There's a simple solution to no English label:
if multiple Latin alphabet labels agree then it becomes the en label and the mul label."*

**The population is the 36,592 people who still have no `en` label** after the 2026-09-01 rebuild.
`build-en-label-batch.py` has three sources -- Wikidata's own English label, a romanised Han name,
and a relationship label -- and a person with none of those falls through with nothing. This is a
fourth source, and it needs no romanisation, no relative and no store lookup: it reads what the
corpus already says about the person in the Latin alphabet.

**Why agreement is the test, and why it is not a similarity heuristic.** A Geni profile carries
several `NAME` records, one per export that saw it, and they disagree when the profile was edited
between exports. `CLAUDE.md` section *Later sources win value conflicts* governs a single-valued
path; a *label* is different, because two independent records saying the same string is positive
evidence that the string is what the person is called. Nothing here compares two DIFFERENT strings
for resemblance -- they are equal after case folding or they are not, which is the same bar
`namemodel` uses and the same one `CLAUDE.md` section *A diacritic makes a different name* demands.

    Anna Martensdotter | Anna Martensdotter | Anna Martensdotter   -> agreed, 3 records
    Anna Martensdotter | Anna Mårtensdotter                        -> NOT agreed, a diacritic
    Private            | Private                                   -> a marker, never a label

**Markers are excluded before agreement is tested**, or every redacted person would come out
labelled `Private` -- which `CLAUDE.md` section *Redacted people go in* forbids in the strongest
terms it uses anywhere. `scripts/labels.label_for` is the single place that decides this and is
imported rather than restated.

**A single record is not agreement.** One record agrees with itself trivially, and that is the
`solo` failure `CLAUDE.md` section *The ONE place a name may choose* measures at 14.9% against
0.7%: *"Solo child says nothing unless there's some reason to match them lol."* Two independent
records are the minimum, and the count goes in the output so the weakest rows can be filtered.

Writes `reports/agreeing-latin-labels.tsv` and `reports/wikidata-agreeing-latin-labels.json`.
"""

from __future__ import annotations

import collections
import csv
import json
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

from labels import label_for  # noqa: E402

LABELS = REPO / "reports" / "derived-labels.csv"
NAMES = REPO / "reports" / "display-names.csv"
OUT_TSV = REPO / "reports" / "agreeing-latin-labels.tsv"
OUT_JSON = REPO / "reports" / "wikidata-agreeing-latin-labels.json"

#: Two records are the minimum. One record agreeing with itself is not evidence.
MIN_RECORDS = 2


def is_latin(text):
    """True when every letter in `text` is a Latin-script letter.

    Digits, spaces and punctuation are ignored -- they carry no script -- but a single Han or
    Cyrillic letter disqualifies the string, because this rule is explicitly about the *Latin
    alphabet* labels and a mixed string is not one.
    """
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    return all("LATIN" in unicodedata.name(c, "") for c in letters)


def main() -> int:
    print("reading derived-labels.csv for who still lacks an en label ...")
    need = set()
    with LABELS.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not (row["label_en"] or "").strip():
                need.add(row["geni_id"])
    print(f"  {len(need):,} people with no en label")

    print("reading display-names.csv ...")
    seen = collections.defaultdict(collections.Counter)
    for_geni = {}
    with NAMES.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g = row["geni_id"]
            if g not in need:
                continue
            raw = (row.get("display_name") or "").strip()
            if not raw or not is_latin(raw):
                continue
            # A marker is not a label. `label_for` empties `Private` and `<private>` and
            # nothing else, which is exactly the boundary wanted here.
            if not label_for(raw).strip():
                continue
            seen[g][raw] += 1
            for_geni[g] = row.get("qid") or ""
    print(f"  {len(seen):,} of them have at least one usable Latin name record")

    rows, agreed = [], {}
    for g, counter in seen.items():
        # Fold on case only. `CLAUDE.md`: case and whitespace fold; nothing else does, because
        # `María`, `Mária` and `Marià` are three different names with three different items.
        folded = collections.Counter()
        display = {}
        for value, n in counter.items():
            key = " ".join(value.split()).casefold()
            folded[key] += n
            display.setdefault(key, " ".join(value.split()))
        best, n = folded.most_common(1)[0]
        distinct = len(folded)
        if n < MIN_RECORDS:
            continue
        # Agreement means the records that carry a Latin name say ONE thing. If two different
        # Latin strings are each attested, the person does not have an agreed label and this
        # rule declines rather than picking the more frequent -- picking would be exactly the
        # coin-flip that `zipper-join`'s uniqueness rule refuses.
        if distinct != 1:
            rows.append({"geni_id": g, "qid": for_geni.get(g, ""), "label": "",
                         "records": n, "distinct_latin": distinct,
                         "verdict": "records disagree"})
            continue
        value = display[best]
        agreed[g] = value
        rows.append({"geni_id": g, "qid": for_geni.get(g, ""), "label": value,
                     "records": n, "distinct_latin": 1, "verdict": "agreed"})

    with OUT_TSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t",
                           fieldnames=["geni_id", "qid", "label", "records",
                                       "distinct_latin", "verdict"])
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (-r["records"], r["geni_id"])))

    # Two edits per person: `en` and `mul` carry the same agreed string. Her rule names both,
    # and `CLAUDE.md` section *The MARRIED name is the real name* makes `mul` the real label --
    # so this is not `en` with a copy, it is the label, written in both places.
    edits = []
    for g, value in sorted(agreed.items()):
        for lang in ("en", "mul"):
            edits.append({
                "id": f"{lang}_label_agreed:{g}",
                "type": "set_label",
                "source": "agreeing Latin name records (Emma, 2026-09-01)",
                "subject": {"qid": None, "geni_id": g},
                "requires": [],
                "label": {"language": lang, "value": value},
                "kind": "add",
                "derived_from": "two or more Latin NAME records that agree exactly",
            })
    OUT_JSON.write_text(json.dumps(edits, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")

    disagree = sum(1 for r in rows if r["verdict"] == "records disagree")
    print(f"\nwrote {OUT_TSV.relative_to(REPO)} and {OUT_JSON.relative_to(REPO)}")
    print(f"  {len(agreed):,} people gain an en AND a mul label from agreeing records")
    print(f"  {disagree:,} have several Latin names that disagree, so nothing is claimed")
    print(f"  {len(edits):,} edits")
    by = collections.Counter(r["records"] for r in rows if r["verdict"] == "agreed")
    for n in sorted(by)[:6]:
        print(f"    {by[n]:>7,} people agreed across {n} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
