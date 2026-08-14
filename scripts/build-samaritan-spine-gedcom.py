"""Write the Itamar → Tabia spine as a GEDCOM built for entering into Geni.

**Itamar ben Aaron is the first record and Tabia ha'Abta'i is the last**, with
every generation between them in descent order, one per record. Emma's
instruction, 2026-08-14: that ordering is what makes the file straightforward to
add to Geni, and Geni is the only one of these sites that will take a run of
numbered generations at all.

**Aaron is deliberately absent.** He is generation 1 and the count starts at him,
but he is already on Geni; emitting him here invites a duplicate. Itamar's NOTE
names his father instead, so the attachment point is stated without a record.

**The unnamed generations get a descriptive label, not a blank.** Each is
`<n>th generation Samaritan Itamar line`. That is a position in a named lineage,
which is what these records actually assert — the earlier file left the NAME
empty, and an empty name is not something Geni can hold or a person can read.
The label is still not a personal name and the NOTE on every one says so.

    py scripts/build-samaritan-spine-gedcom.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from samaritan_spine import (  # noqa: E402
    REPO, display, generation_label, is_placeholder, spine,
)

SOURCE = ("A.B. - The Samaritan News / The Samaritan Update, March-April 2012, "
          "'The High Priesthood and the Israelite Samaritan Priests', "
          "by Benyamim Tsedaka")

HEAD = """0 HEAD
1 SOUR genimerge
2 NAME genimerge samaritan-itamar-spine
2 CORP Emma Leonhart
1 GEDC
2 VERS 5.5.1
2 FORM LINEAGE-LINKED
1 CHAR UTF-8
1 NOTE The Israelite Samaritan 'Abtah (Itamar-line) priestly descent, ordered
2 CONT for entry into Geni: Itamar ben Aaron first, Tabia ha'Abta'i last.
2 CONT NOT a Geni export. No profile IDs except the one named in Tabia's NOTE.
2 CONT Generation numbers count from Aaron ben Amram = 1, so Itamar is 2 and
2 CONT Tabia is 112. Generations with no personal name carry a descriptive
2 CONT label instead - read their NOTE before treating one as a person.
"""


def wrap_note(text: str, width: int = 72) -> list[str]:
    """A NOTE plus CONT lines. GEDCOM 5.5.1 has no continuation of unlimited
    length, and Geni's importer is happier with short lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    out = [f"1 NOTE {lines[0]}"] if lines else ["1 NOTE"]
    out += [f"2 CONT {line}" for line in lines[1:]]
    return out


def build(people: list[tuple[int, dict]]) -> str:
    lines = [HEAD.rstrip("\n")]
    fams = []

    for i, (gen, rec) in enumerate(people, start=1):
        lines.append(f"0 @I{i}@ INDI")
        if is_placeholder(rec):
            lines.append(f"1 NAME {generation_label(gen)} //")
        else:
            lines.append(f"1 NAME {rec['name']}")
        lines.append(f"1 SEX {rec['sex'] or 'M'}")
        if rec["titl"]:
            lines.append(f"1 TITL {rec['titl']}")
        if rec["occu"]:
            lines.append(f"1 OCCU {rec['occu']}")

        if is_placeholder(rec):
            note = (
                f"Generation {gen} of the Itamar line, counting Aaron ben Amram "
                f"as 1. NO SOURCE NAMES THIS PERSON - the record asserts a "
                f"position in the descent and nothing else. The LENGTH of the "
                f"unnamed stretch is borrowed from the parallel Phinhas line, "
                f"which the source gives as 112 generations father-to-son from "
                f"Aaron to 1624. Nobody counted this line. Do not read the "
                f"number as measured, and do not give this person a name that "
                f"does not come from a source."
            )
            if rec["note"] and "may be zero" in " ".join(rec["note"]):
                note = (
                    f"Generation {gen} of the Itamar line, counting Aaron ben "
                    f"Amram as 1. NO SOURCE NAMES THIS PERSON. This one carries "
                    f"the distance between 'Abed Ela ben Shalma and Yusef, which "
                    f"the source does not state and WHICH MAY BE ZERO: 'Abed Ela "
                    f"may simply be Yusef's father. Do not treat this generation "
                    f"as attested."
                )
            lines += wrap_note(note)
        else:
            note = " ".join(" ".join(rec["note"]).split())
            if display(rec["name"]) == "Itamar ben Aaron":
                note = note.rstrip(".") + (
                         ". His father Aaron ben Amram is generation 1 and is NOT "
                         "in this file: he is already on Geni, and emitting him "
                         "here would invite a duplicate. Attach Itamar to the "
                         "existing Aaron.")
            # The named records already carry their own "Source: ..." sentence,
            # copied from samaritan-sources.ged.
            lines += wrap_note(f"Generation {gen}. {note}")

        if i < len(people):
            lines.append(f"1 FAMS @F{i}@")
        if i > 1:
            lines.append(f"1 FAMC @F{i - 1}@")

        # Each FAM goes immediately after the father it belongs to, rather than
        # in a block at the end. That is what keeps Tabia the LAST record in the
        # file and Itamar the first, which is the ordering Emma asked for.
        if i < len(people):
            lines.append(f"0 @F{i}@ FAM")
            lines.append(f"1 HUSB @I{i}@")
            lines.append(f"1 CHIL @I{i + 1}@")
            fams.append(i)

    lines.append("0 TRLR")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="gedcom/samaritan-itamar-spine.ged")
    args = ap.parse_args()

    people = spine()
    out = REPO / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(people), encoding="utf-8")

    named = sum(1 for _, r in people if not is_placeholder(r))
    first, last = people[0], people[-1]
    print(f"{len(people)} records, generations {first[0]}-{last[0]} "
          f"({display(first[1]['name'])} -> {display(last[1]['name'])}), "
          f"{named} named, {len(people) - named} numbered generations -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
