"""Which people on the spines ALREADY have a Wikidata item — derived, not hand-maintained.

    python scripts/refresh-spine-known.py

**The gap this closes, 2026-08-31.** `build-garborg-day.py --known <file>` folds that file's
`geni_id -> qid` pairs into `our_items`, and `our_items` is what the linking pass resolves every
relationship target through. A spine person absent from it cannot be linked to — the batch will
happily skip *creating* them, because `any_wikidata_item` catches the duplicate, and then emit no
`P22`/`P25` pointing at them either.

That is exactly what happened: `reports/spine-already-on-wikidata.tsv` was **9 rows, written by
hand on 2026-08-26**, and the Carolingian end of `paths/charlemagne-to-arne-garborg.tsv` is not in
it. So a spine run reported *0 creations, 69 links* and **not one of those links touched
`Q3044` Charlemagne, `Q43974` Louis the Pious, `Q314521` Berengar II, `Q378177` Baldwin IV or
`Q273181` Judith of Flanders**. The people exist on Wikidata, the tree knows who they are, and the
batch could not see the join.

**Why derive it rather than keep editing the file.** The hand-written rows carry something this
cannot reproduce — Emma's own adjudications, including the `Ingegerd Svantepolksdotter` case she
accepted on a closed-sibling-set argument. Those are kept verbatim. What is added is the
mechanical half: anybody on a spine whose Geni id already carries a `P2600` on Wikidata, which is
a lookup and never a judgement.

`out/wikidata/p2600-all.tsv` is the authority for that, refreshed from live Wikidata on
2026-08-30. A pairing there is Wikidata's own statement, not an inference of ours.

Writes `reports/spine-already-on-wikidata.tsv`, preserving every existing row.
"""

import csv
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
P2600 = ROOT / "out" / "wikidata" / "p2600-all.tsv"
OUT = ROOT / "reports" / "spine-already-on-wikidata.tsv"

#: The same four files `build-garborg-day.SPINE_PATHS` names. Kept here as paths rather than
#: imported, because that module is a 5,000-line script with a heavy import cost and this needs
#: four filenames.
#: The one live spine, matching `build-garborg-day.SPINE_PATHS`. The four it replaced are legacy
#: as of 2026-08-30.
SPINE_PATHS = ("paths/arne-garborg-to-johannes-bureus-geni.tsv",)

FIELDS = ["step", "geni_name", "geni_id", "candidate_qid", "candidate_label",
          "evidence", "confidence", "independent_anchors", "anchoring"]


def spine_people():
    """`{geni_id: (step, name)}` for every person on every spine."""
    out = {}
    for name in SPINE_PATHS:
        path = ROOT / name
        if not path.exists():
            sys.stderr.write(f"  missing, skipped: {name}\n")
            continue
        rows = [ln.rstrip("\n").split("\t")
                for ln in io.open(path, encoding="utf-8") if not ln.startswith("#")]
        if not rows:
            continue
        header = rows[0]
        try:
            i_step, i_name, i_note = (header.index("step"), header.index("name"),
                                      header.index("note"))
        except ValueError:
            continue
        for row in rows[1:]:
            if len(row) <= max(i_step, i_name, i_note):
                continue
            m = re.search(r"geni:(\d+)", row[i_note] or "")
            if m:
                out.setdefault(m.group(1), (row[i_step], row[i_name]))
    return out


def wikidata_pairs(wanted):
    """`{geni_id: qid}` from Wikidata's own `P2600` statements, for the ids we care about."""
    found = {}
    with io.open(P2600, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[1] in wanted:
                found.setdefault(parts[1], parts[0])
    return found


def main():
    people = spine_people()
    if not people:
        sys.exit("no spine people found -- are paths/*.tsv present?")
    pairs = wikidata_pairs(set(people))
    print(f"{len(people)} people across {len(SPINE_PATHS)} spines; "
          f"{len(pairs)} already carry a P2600 on Wikidata")

    # **Existing rows are kept verbatim.** They hold Emma's own adjudications -- the
    # Ingegerd Svantepolksdotter acceptance among them -- which no lookup reproduces.
    existing, seen = [], set()
    if OUT.exists():
        with io.open(OUT, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                existing.append(row)
                if row.get("geni_id"):
                    seen.add(row["geni_id"])
    print(f"{len(existing)} hand-written rows kept")

    added = 0
    for geni_id, qid in sorted(pairs.items(), key=lambda kv: int(kv[0])):
        if geni_id in seen:
            continue
        step, name = people[geni_id]
        existing.append({
            "step": step,
            "geni_name": name,
            "geni_id": geni_id,
            "candidate_qid": qid,
            "candidate_label": "",
            "evidence": "Wikidata states this P2600 itself (out/wikidata/p2600-all.tsv)",
            "confidence": "certain -- Wikidata's own statement, not an inference",
            "independent_anchors": "",
            "anchoring": "",
        })
        added += 1

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(existing)
    print(f"wrote {OUT}: {len(existing)} rows, {added} newly derived")


if __name__ == "__main__":
    main()
