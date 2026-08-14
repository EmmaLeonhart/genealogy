"""Shared reading of `gedcom/samaritan-sources.ged` for the Itamar-line spine.

Both `build-samaritan-spine-gedcom.py` and `build-samaritan-spine-page.py` walk
the same descent and number the same generations, so the walk lives here rather
than in each of them.

**Generation 1 is Aaron ben Amram.** Itamar is 2, Tabia ha'Abta'i is 112. The
numbering counts from Aaron even though the spine file starts at Itamar, because
Aaron is where the count means something — the source's own claim is "112
generations father-to-son from Aaron" for the parallel Phinhas line.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GED = REPO / "gedcom" / "samaritan-sources.ged"

#: Aaron ben Amram — generation 1, and the head of both priestly lines.
ROOT = "@I1@"

#: Tabia ha'Abta'i, the bottom of the spine: the person the Geni component of 33
#: hangs from (profile 6000000220294810877). Everything above him is missing
#: from Geni, which is what the spine file exists to supply.
BOTTOM_NAME = "Tabia /ha'Abta'i/"

#: The spine file starts here, not at Aaron. Aaron is already on Geni; emitting
#: him would invite a duplicate.
SPINE_TOP_NAME = "Itamar /ben Aaron/"


def parse(path: Path = GED):
    """The subset of GEDCOM this file uses: INDI/FAM with NAME, SEX, TITL,
    OCCU, NOTE/CONT, FAMC/FAMS, HUSB/WIFE/CHIL."""
    indi: dict[str, dict] = {}
    fam: dict[str, dict] = {}
    cur = None
    kind = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\d+) (?:(@[^@]+@) )?(\w+)(?: (.*))?$", raw)
        if not m:
            continue
        level, xref, tag, val = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        if level == "0":
            if tag == "INDI":
                cur = indi.setdefault(xref, {"id": xref, "famc": None, "fams": [],
                                             "name": "", "sex": "", "titl": "",
                                             "occu": "", "note": []})
                kind = "indi"
            elif tag == "FAM":
                cur = fam.setdefault(xref, {"id": xref, "husb": None, "wife": None,
                                            "chil": []})
                kind = "fam"
            else:
                cur, kind = None, None
            continue
        if cur is None:
            continue
        if kind == "indi":
            if tag in ("NAME", "SEX", "TITL", "OCCU"):
                cur[tag.lower()] = val
            elif tag == "NOTE":
                cur["note"] = [val]
            elif tag == "CONT" and cur["note"]:
                cur["note"].append(val)
            elif tag == "FAMC":
                cur["famc"] = val
            elif tag == "FAMS":
                cur["fams"].append(val)
        else:
            if tag in ("HUSB", "WIFE"):
                cur[tag.lower()] = val
            elif tag == "CHIL":
                cur["chil"].append(val)
    return indi, fam


def descent(indi, fam, root: str = ROOT, target_name: str = BOTTOM_NAME) -> list[str]:
    """Xrefs from `root` down to the person whose NAME is `target_name`.

    Depth-first. The file is a spine with branches only below Tabia, so the
    first path found is the only path; a missing target is an error rather than
    a shrug, because a silent short walk would publish a truncated lineage.
    """
    stack = [(root, [root])]
    seen: set[str] = set()
    while stack:
        person, path = stack.pop()
        if person in seen:
            continue
        seen.add(person)
        if indi[person]["name"] == target_name:
            return path
        for f in indi[person]["fams"]:
            for child in fam.get(f, {}).get("chil", []):
                if child in indi:
                    stack.append((child, path + [child]))
    raise SystemExit(f"no descent from {root} to {target_name!r}")


def spine(indi=None, fam=None) -> list[tuple[int, dict]]:
    """`(generation, record)` from Itamar (generation 2) to Tabia (112).

    Aaron is walked but not returned: the count starts at him, the file does not.
    """
    if indi is None or fam is None:
        indi, fam = parse()
    path = descent(indi, fam)
    numbered = list(enumerate(path, start=1))
    top = next(n for n, x in numbered if indi[x]["name"] == SPINE_TOP_NAME)
    return [(n, indi[x]) for n, x in numbered if n >= top]


def display(name: str) -> str:
    """`Itamar /ben Aaron/` -> `Itamar ben Aaron`; `//` -> `''`."""
    return " ".join(name.replace("/", " ").split())


def is_placeholder(record: dict) -> bool:
    return not display(record["name"])


def ordinal(n: int) -> str:
    """1 -> 1st, 112 -> 112th. The teens are all `th`, including 111th."""
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


#: The descriptive name a placeholder generation carries instead of a personal
#: name. Emma's instruction, 2026-08-14: they are not "unnamed placeholders",
#: they are a numbered generation of a named line, and the label has to say so.
def generation_label(n: int) -> str:
    return f"{ordinal(n)} generation Samaritan Itamar line"
