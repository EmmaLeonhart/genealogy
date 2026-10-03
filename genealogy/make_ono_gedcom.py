"""Build genealogy/ono_inbe_honkeicho.ged from genealogy/ono_inbe_honkeicho.csv.

The Ono family's 斎部宿禰本系帳 (1870; NDL pid 2538213, images 50-56), judged a
Suzuki Masatoshi forgery by Kosugi Sugimura in 1876. Parent links follow the
transcription order: each numbered row is the child of the previous numbered
row, a "b" row is a sibling of the same-numbered row, and H rows are the
second (Ame no Hiwashi) line. Run: python genealogy/make_ono_gedcom.py
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "ono_inbe_honkeicho.csv"
OUT = HERE / "ono_inbe_honkeicho.ged"

rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
by_seq = {r["seq"]: r for r in rows}

# Extra people named in the pedigree but not rows of their own.
EXTRA = {
    "W2": {"name": "天比理乃咩命", "note": "Wife of 天太玉命 (Ame no Hiritome)."},
}

people = {}  # key -> dict(name, note, sex)
for r in rows:
    note = "; ".join(x for x in [
        r["alias_or_note"] and f"Alias/note: {r['alias_or_note']}",
        r["reign_or_date_given"] and f"Reign/date given: {r['reign_or_date_given']}",
        r["matches_chronicle_person"] and f"Matches chronicle person: {r['matches_chronicle_person']}",
        r["notes"],
        f"NDL pid 2538213 image {r['ndl_image']}",
    ] if x)
    people[r["seq"]] = {"name": r["name"].split(" / ")[0], "note": note}
people.update(EXTRA)

FEMALE = {"5", "W2"}


def parent_of(seq):
    """Previous generation's key for a row, per the transcription order."""
    m = re.fullmatch(r"(H?)(\d+)(b?)", seq)
    prefix, n = m.group(1), int(m.group(2))
    if n == 1:
        return None
    prev = f"{prefix}{n - 1}"
    return prev if prev in by_seq else None


# Families: (father, mother) -> children
families = {}


def add_child(father, mother, child):
    families.setdefault((father, mother), []).append(child)


for seq in by_seq:
    if seq == "H11":
        # Text: 訶多々主命 is the son of 由布津主命 (H10) and 飯長媛命 (5).
        add_child("H10", "5", seq)
        continue
    if seq == "6":
        # The Futodama line continues through 飯長媛命 and her husband H10.
        add_child("H10", "5", seq)
        continue
    p = parent_of(seq)
    if p is None:
        continue
    if p == "2":
        add_child("2", "W2", seq)
    elif p == "5":
        continue  # handled above
    else:
        add_child(p, None, seq)
families.setdefault(("2", "W2"), [])

ids = {k: f"@I{i}@" for i, k in enumerate(people, 1)}
fam_ids = {k: f"@F{i}@" for i, k in enumerate(families, 1)}

L = ["0 HEAD", "1 SOUR INBE-research", "2 NAME make_ono_gedcom.py",
     "1 GEDC", "2 VERS 5.5.1", "2 FORM LINEAGE-LINKED", "1 CHAR UTF-8",
     "1 NOTE 斎部宿禰本系帳 (Ono family Inbe pedigree, 1870). Judged forged by Kosugi "
     "Sugimura (1876); not evidence of real descent. Parent links follow transcription "
     "order; see genealogy/ono_inbe_honkeicho.csv and research/notes/inbe-pedigrees.md.",
     "0 @S1@ SOUR", "1 TITL 斎部宿禰本系帳 (in 安房国忌部家系 volume), NDL Digital Collections",
     "1 PUBL National Diet Library, pid 2538213, doi 10.11501/2538213",
     "1 NOTE Kosugi Sugimura's 1876 headnote attributes it to Suzuki Masatoshi."]

for key, p in people.items():
    L += [f"0 {ids[key]} INDI", f"1 NAME {p['name']}",
          f"1 SEX {'F' if key in FEMALE else 'M' if key not in ('W2',) else 'F'}"]
    for fk, kids in families.items():
        if key in kids:
            L.append(f"1 FAMC {fam_ids[fk]}")
        if key in fk:
            L.append(f"1 FAMS {fam_ids[fk]}")
    L += [f"1 NOTE {p['note']}", "1 SOUR @S1@", "2 QUAY 0"]

for fk, kids in families.items():
    father, mother = fk
    L.append(f"0 {fam_ids[fk]} FAM")
    if father:
        L.append(f"1 HUSB {ids[father]}")
    if mother:
        L.append(f"1 WIFE {ids[mother]}")
    L += [f"1 CHIL {ids[c]}" for c in kids]
    L += ["1 SOUR @S1@", "2 QUAY 0"]

L.append("0 TRLR")
OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"wrote {OUT} ({len(people)} people, {len(families)} families)")
