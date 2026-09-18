"""MyHeritage Family Tree Builder `.ftb` databases, rendered as GEDCOM.

    python scripts/ftb-to-gedcom.py

**Queue item 2, 2026-09-17:** *"figure out how to deal with the git ignored files often by
converting to gedcoms"*.

The three MyHeritage *Descent from Antiquity archive* backups are 220 MB each and GitHub refuses
anything over 100 MB, so they are gitignored. **Almost all of that is photographs.** Each zip
holds ~3,870 images and one database:

    13.1 MB  Database/Descent from Antiquity archive.ftb
     9.5 MB  Photos/P469_1280_15000.png
     ...     ~3,870 more

So the genealogy is 13 MB inside a 220 MB archive, and it is a **SQLite database** — 39 tables,
`individual_main_data`, `family_main_data`, `family_individual_connection`. Nothing needs
MyHeritage installed to read it.

## What the archive actually is

Three snapshots of one growing tree, taken minutes apart on 2024-09-15:

    16-11-51   1,550 individuals   1,043 families
    16-27-05   4,033 individuals   2,689 families
    16-36-40   4,093 individuals   2,740 families   <- the fullest

The names are late-antique — `Licinia Eudoxia Augusta`, `Afranius Hanniballianus`, `Olybrius` —
which is what the archive's own title says it is.

## The schema, decoded rather than assumed

`individual_role_type` in `family_individual_connection` is an integer with no lookup table in the
file. It was decoded by joining role against gender, which is unambiguous:

    role 2   2,720 people, ALL male      husband
    role 3   1,473 people, ALL female    wife
    role 5   2,975 people, mixed         child
    role 6      14 people, all male      a second husband slot; written as a spouse

Names live one join away: `individual_data_set` maps an individual to its `individual_lang_data`
rows, and a person may have SEVERAL — `Licinia Eudoxia`/`Augusta` and `Roman Empress`/`Aelia` are
the same woman. The first row is the name; the rest are written as `2 _AKA` rather than dropped,
because a discarded alias is exactly what makes a later name search miss.

⛔ **THIS IS NOT CORPUS AND ITS IDS ARE NOT GENI IDS.** `CLAUDE.md` § *The Geni profile ID is the
primary key* governs `exports/`, where every xref is a real Geni profile. These are MyHeritage row
ids, so the output goes to `preservation/` and **must never be merged into the synoptic tree as
though its xrefs were Geni ids**. It is written to be readable and searchable, not joinable.
"""

from __future__ import annotations

import pathlib
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "preservation" / "extracted-databases"
OUT = ROOT / "preservation" / "converted-gedcoms"

#: Decoded above by joining role against gender. 6 is a second husband slot.
HUSBAND, WIFE, CHILD, HUSBAND2 = 2, 3, 5, 6


def names(conn):
    """`{individual_id: [(first, last), ...]}` — every name row, first one wins as the name."""
    out: dict[int, list[tuple[str, str]]] = {}
    q = """select d.individual_id, l.first_name, l.last_name
           from individual_data_set d
           join individual_lang_data l
             on l.individual_data_set_id = d.individual_data_set_id
           order by d.individual_id, l.individual_lang_data_id"""
    for iid, first, last in conn.execute(q):
        out.setdefault(iid, []).append(((first or "").strip(), (last or "").strip()))
    return out


def convert(path: pathlib.Path) -> tuple[str, int, int]:
    conn = sqlite3.connect(path)
    nm = names(conn)
    lines = [
        "0 HEAD",
        "1 SOUR genimerge",
        "2 NAME scripts/ftb-to-gedcom.py",
        "1 NOTE Converted from a MyHeritage Family Tree Builder .ftb SQLite database.",
        "2 CONT Source: %s" % path.name,
        "2 CONT The xrefs are MyHeritage row ids and are NOT Geni profile ids. Do not merge",
        "2 CONT this into the synoptic tree on the assumption that they are.",
        "1 GEDC",
        "2 VERS 5.5.1",
        "2 FORM LINEAGE-LINKED",
        "1 CHAR UTF-8",
    ]
    people = 0
    for iid, gender in conn.execute(
            "select individual_id, gender from individual_main_data "
            "where coalesce(delete_flag,0)=0 order by individual_id"):
        rows = nm.get(iid) or [("", "")]
        first, last = rows[0]
        lines.append("0 @I%d@ INDI" % iid)
        lines.append("1 NAME %s /%s/" % (first, last))
        if first:
            lines.append("2 GIVN %s" % first)
        if last:
            lines.append("2 SURN %s" % last)
        # Every further name row is an alias. Dropping them is what makes a later search miss.
        for f2, l2 in rows[1:]:
            if (f2, l2) != (first, last) and (f2 or l2):
                lines.append("2 _AKA %s %s" % (f2, l2))
        if gender in ("M", "F"):
            lines.append("1 SEX %s" % gender)
        people += 1

    fams = 0
    members: dict[int, dict[str, list[int]]] = {}
    q = """select family_id, individual_id, individual_role_type
           from family_individual_connection
           where coalesce(delete_flag,0)=0"""
    for fid, iid, role in conn.execute(q):
        slot = members.setdefault(fid, {"HUSB": [], "WIFE": [], "CHIL": []})
        if role in (HUSBAND, HUSBAND2):
            slot["HUSB"].append(iid)
        elif role == WIFE:
            slot["WIFE"].append(iid)
        elif role == CHILD:
            slot["CHIL"].append(iid)
    for fid in sorted(members):
        slot = members[fid]
        if not any(slot.values()):
            continue
        lines.append("0 @F%d@ FAM" % fid)
        for tag in ("HUSB", "WIFE", "CHIL"):
            for iid in slot[tag]:
                lines.append("1 %s @I%d@" % (tag, iid))
        fams += 1
    lines.append("0 TRLR")
    return "\n".join(lines) + "\n", people, fams


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not SRC.is_dir():
        raise SystemExit("%s missing" % SRC)
    OUT.mkdir(parents=True, exist_ok=True)
    for db in sorted(SRC.glob("*.ftb")):
        text, people, fams = convert(db)
        dest = OUT / (db.stem + ".ged")
        dest.write_text(text, encoding="utf-8")
        print("%-46s %5d people %5d families -> %s"
              % (db.name, people, fams, dest.relative_to(ROOT).as_posix()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
