"""The Izumo chart becomes THREE offices, not one succession.

    python scripts/build-izumo-succession.py

**Emma's model, 2026-08-24:** *"Izumo succession is based on surname so original Izumo would
be the Unified Izumo no Kuni no Miyatsuko and Senge and Kitajima are different ones all three
designated with a qualifier on according to which organization: izumo taisha for the unified,
izumokyo for kitajima and izumo taishakyo for senge. With the last unified one having both
successors."*

| holders | seats | organisation |
| --- | --- | --- |
| surname 出雲 *Izumo* | 1-54 | `Q696362` *Izumo Taisha* |
| surname 北島 *Kitajima* | 55-79 | `Q11395891` *Izumo-kyō* |
| surname 千家 *Senge* | 55-84 | `Q6102386` *Izumo-taishakyo* |

`Q135579414` *Izumo no Kiyotaka*, seat 54, is the last unified holder and carries **two**
`P1366` *replaced by* -- `Q135579415` *Senge no Takamune* and `Q135579416` *Kitajima no
Sadataka*, both seat 55. That fork is why one `P1365`/`P1366` chain through the roster would
be wrong.

## Every QID here was reached by walking links, never by searching

`CLAUDE.md` forbids querying Wikidata and equally forbids guessing an ID. None of the three
organisations is in the local store -- it is a Geni-shaped slice of **people** -- so each was
reached from an item already held, by `full_entities` on a known QID:

* `Q11395856` *Izumo no Kuni no Miyatsuko* is the `P53` *family* value on 95 of the 111
  fetched Izumo items and the `P39` *position held* value on 4. One item, both readings.
* Its `P2389` *organization directed by the office or position* is `Q696362` *Izumo Taisha*.
* Izumo Taisha's `P140` *religion or worldview* is `Q6102386` *Izumo-taishakyo*, whose
  `P1889` *different from* is `Q11395891` *Izumo-kyō*. The two sects name each other.

**An independent corroboration of the pairing Emma stated**: `Q6102386` *Izumo-taishakyo* has
`P112` *founded by* -> `Q11405449` *Senge Takatomi*, who is **seat 80 of the Senge line** on
this very roster.

## The organisation qualifier is `P2389`, and that is a reading

Her phrase is *"a qualifier on according to which organization"* and she did not name a
property. `P2389` *organization directed by the office or position* is used, because on a
`P39` statement it reads as exactly her sentence and because it is already the relation
between this office and Izumo Taisha. **Rejected: `P1416` *affiliation***, which describes a
person rather than a position. Falsified if she names a different property.

## Two defects in the roster, both found by NOT trusting the Latin name

**The surname screen is on the KANJI**, with the Latin name only as a fallback. Screening on
Latin alone put `Kitashima no Naotaka` (北島脩孝, seat 75) and a row whose `english` column is
literally `Q48763085` (北島斉孝, seat 76) into the *unified* line -- which then ran to seat 76
and would have chained two Kitajima heads onto the end of an office that ended at 54.
`CLAUDE.md` § *A clan name is not a clan* is the same lesson.

**Seat 36 has two holders and seat 37 has none.** `Q135579384` *Izumo no Tsunesuke* and
`Q135579385` *Izumo no Ujihiro*. Ujihiro is probably seat 37 and the chart's transcription is
off by one -- but *probably* is not enough to order an office, so both get `P39` with ordinal
36 and **no `P1365`/`P1366` is emitted across 35 -> 36 -> 38 for anybody**. Ordering is the
only part that is unresolvable; that they both held it is not in doubt.

**A seat whose person has no item breaks its neighbours' links, and they are dropped rather
than bridged.** Linking seat N-1 straight to N+1 would assert an adjacency the chart denies.

Writes `reports/wikidata-izumo-succession.json` (edit objects, the shape
`scripts/build-samaritan-succession.py` established and `genimerge.editorder` consumes).
Queued, never run.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
ROSTER = ROOT / "reports" / "izumo-chart-roster.tsv"
OUT = ROOT / "reports" / "wikidata-izumo-succession.json"

#: `Q11395856` *Izumo no Kuni no Miyatsuko* -- the office all three lines hold.
OFFICE = "Q11395856"
#: The organisation each line's holders direct, per Emma's model.
ORGANISATION = {
    "Izumo": ("Q696362", "Izumo Taisha"),
    "Kitajima": ("Q11395891", "Izumo-kyō"),
    "Senge": ("Q6102386", "Izumo-taishakyo"),
}
#: The page the succession is stated by. It is not a Geni fact, so it gets no `P2600`
#: reference -- citing the Geni profile for a chart's seat numbering would be a miscitation.
SOURCE_URL = "https://shinto.miraheze.org/wiki/Izumo_clan"

#: Seats whose ORDER cannot be resolved: two holders at 36 and none at 37. No `P1365`
#: *replaces* or `P1366` *replaced by* is emitted into or out of this run.
UNORDERED_SEATS = {36}


def line_of(row):
    """Which of the three lines a holder belongs to, decided on the KANJI surname."""
    ja, en = row["japanese"], row["english"]
    if ja.startswith("千家") or "Senge" in en:
        return "Senge"
    if ja.startswith("北島") or "Kitajima" in en or "Kitashima" in en:
        return "Kitajima"
    return "Izumo"


def main():
    rows = list(csv.DictReader(open(ROSTER, encoding="utf-8"), delimiter="\t"))
    seats = {}
    for r in rows:
        s = r["succession"].strip()
        if s.isdigit():
            seats.setdefault((line_of(r), int(s)), []).append(r)

    for name in ("Izumo", "Kitajima", "Senge"):
        got = sorted(s for (l, s) in seats if l == name)
        held = sum(1 for (l, s), v in seats.items()
                   if l == name and v[0]["qid"].strip().startswith("Q"))
        print(f"{name:<9} seats {min(got)}-{max(got)}  {len(got)} seats, {held} with an item")

    def qid_at(line, seat):
        """The single holder's QID at a seat, or None if unheld, unknown or ambiguous."""
        v = seats.get((line, seat))
        if not v or len(v) > 1 or seat in UNORDERED_SEATS:
            return None
        q = v[0]["qid"].strip()
        return q if q.startswith("Q") else None

    edits, notes = [], []
    for line, (org_qid, org_label) in ORGANISATION.items():
        present = sorted(s for (l, s) in seats if l == line)
        for seat in present:
            for row in seats[(line, seat)]:
                qid = row["qid"].strip()
                if not qid.startswith("Q"):
                    notes.append(f"{line} seat {seat}: {row['english'] or row['japanese']} "
                                 f"has no Wikidata item; nothing emitted, and its neighbours "
                                 f"lose that link")
                    continue
                quals = [{"property": "P2389", "value": org_qid},
                         {"property": "P1545", "value": str(seat)}]

                # `P1365` *replaces* -- the previous seat, unless this line begins here.
                # The fork: seat 55 of Senge and of Kitajima both replace the last
                # unified holder, seat 54 of Izumo, not a seat 54 of their own line.
                prev_line = "Izumo" if (line != "Izumo" and seat - 1 == 54) else line
                prev = qid_at(prev_line, seat - 1) if seat - 1 in (
                    [s for (l, s) in seats if l == prev_line]) else None
                if prev and seat not in UNORDERED_SEATS:
                    quals.append({"property": "P1365", "value": prev})

                # `P1366` *replaced by* -- the next seat. The last unified holder has TWO.
                if line == "Izumo" and seat == 54:
                    for fork in ("Senge", "Kitajima"):
                        nxt = qid_at(fork, 55)
                        if nxt:
                            quals.append({"property": "P1366", "value": nxt})
                else:
                    nxt = qid_at(line, seat + 1)
                    if nxt and seat not in UNORDERED_SEATS:
                        quals.append({"property": "P1366", "value": nxt})

                edits.append({
                    "id": f"izumo_succession:{qid}",
                    "type": "normalise_office",
                    "source": f"{ROSTER.name} + Emma's three-office model, 2026-08-24",
                    "subject": {"qid": qid, "geni_id": row["geni"].strip()},
                    "requires": [],
                    "add": [{
                        "property": "P39",
                        "value": OFFICE,
                        "qualifiers": quals,
                        "references": [{"property": "P854", "value": SOURCE_URL}],
                    }],
                    "remove": [],
                })

    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    forks = [e for e in edits
             if sum(1 for q in e["add"][0]["qualifiers"] if q["property"] == "P1366") > 1]
    chained = sum(1 for e in edits
                  if any(q["property"] in ("P1365", "P1366") for q in e["add"][0]["qualifiers"]))
    print(f"\n{len(edits)} P39 statements, {chained} carrying a P1365/P1366 link")
    print(f"{len(forks)} holder(s) with two successors: "
          f"{[e['subject']['qid'] for e in forks]}")
    for n in notes:
        print(f"   note: {n}")
    print(f"wrote {OUT.resolve().relative_to(ROOT)}")
    print("QUEUED, NEVER RUN. Wikidata editing in this repo starts 2026-09-01.")


if __name__ == "__main__":
    main()
