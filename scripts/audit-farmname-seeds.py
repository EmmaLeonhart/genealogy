"""Placeholder seeds that should have taken the child's surname and did not.

**Emma, 2026-08-18:** *"uhh farm names are surnames here lol"* --- and, on the two
already created: *"add a task in the queue to fix the surnames of these people before
the synoptic tree is built. I will do the editing on geni for this."*

A tier-1 seed gives the created father **the child's surname**, with the patronymic
stripped out of it. A tier-2 seed has no surname to give and uses `father of <child>`.
The farm-name correction moves a whole class of Nordic people from tier 2 to tier 1, so
some existing placeholders carry `father of X` where they should carry a real surname.

**The screen has to exclude the patronymic case or it is useless.** Most `father of X`
placeholders have a child whose surname *is* the patronymic --- `Barbro /Endresdatter/`,
`Sigrid /Larsdotter/` --- and there tier 2 was correct all along, because tier 1 is
explicit that the patronymic must not survive into the father's surname. Only a child
whose surname is something OTHER than a patronymic is a miss.

    PYTHONPATH=src python scripts/audit-farmname-seeds.py
"""

from __future__ import annotations

import collections
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import sources

OUT = sources.REPO_ROOT / "reports" / "farmname-seed-fixes.md"

#: A surname in this shape is the child's patronymic, not a family name, so the father
#: must NOT inherit it. Anchored at the end so `Tjaland` and `Gilja` pass through.
PATRONYMIC = re.compile(r"(sen|son|sson|sdatter|sdotter|sdtr|datter|dotter|dttr)$", re.I)

#: Not surnames: regnal epithets and descriptors that happen to sit in the surname slot.
NOT_A_SURNAME = re.compile(r"\b(king|kings|r\.\d|usurper|sassanian|sasanian|"
                           r"emperor|khan|dynasty|\d{3,})\b", re.I)


def main() -> int:
    name: dict[str, str] = {}
    fam_child = collections.defaultdict(set)
    fam_parent = collections.defaultdict(set)

    for path in sources.find_exports(sources.REPO_ROOT / "exports"):
        cur = curf = None
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("0 @I"):
                cur, curf = line[4:].split("@")[0], None
            elif line.startswith("0 @F"):
                curf, cur = line[4:].split("@")[0], None
            elif line.startswith("0 "):
                cur = curf = None
            elif cur and line.startswith("1 NAME "):
                name.setdefault(cur, line[7:].strip())
            elif curf:
                if line.startswith("1 CHIL @I"):
                    fam_child[curf].add(line.split("@I")[1].split("@")[0])
                elif line.startswith(("1 HUSB @I", "1 WIFE @I")):
                    fam_parent[curf].add(line.split("@I")[1].split("@")[0])

    hits, skipped = [], 0
    for gid, nm in name.items():
        if "/father of " not in nm and "/mother of " not in nm:
            continue
        kids = set()
        for f, ps in fam_parent.items():
            if gid in ps:
                kids |= fam_child[f]
        for k in sorted(kids):
            kn = name.get(k, "")
            surn = kn.split("/")[1].strip() if "/" in kn else ""
            if not surn or surn in (".", "?"):
                continue
            if PATRONYMIC.search(surn) or NOT_A_SURNAME.search(surn):
                skipped += 1
                continue
            hits.append((gid, nm, k, kn, surn))
            break

    hits.sort(key=lambda r: r[1])
    lines = [
        "# Placeholder seeds that need a surname, not `father of X`",
        "",
        "Emma, 2026-08-18: *\"uhh farm names are surnames here lol\"* --- and *\"add a "
        "task in the queue to fix the surnames of these people before the synoptic tree "
        "is built. I will do the editing on geni for this.\"*",
        "",
        "**She does the Geni edits.** This file is the worklist, not an instruction to "
        "touch anything.",
        "",
        f"**{len(hits)} placeholders** carry `father of <child>` where the child has a "
        f"real surname the father should have taken. A further **{skipped}** were "
        "checked and left alone because the child's surname *is* their patronymic "
        "(`Barbro /Endresdatter/`, `Sigrid /Larsdotter/`), where tier 2 was correct --- "
        "tier 1 is explicit that the patronymic must not survive into the father's "
        "surname.",
        "",
        "| Geni ID | placeholder now | should be | child |",
        "| --- | --- | --- | --- |",
    ]
    for gid, nm, k, kn, surn in hits:
        given = nm.split("/")[0].strip()
        lines.append(f"| [{gid}](https://www.geni.com/people/x/{gid}) | `{nm}` | "
                     f"`{given} /{surn}/` | {kn} |")
    lines.append("")
    io.open(OUT, "w", encoding="utf-8").write("\n".join(lines))

    print(f"{len(hits)} to fix, {skipped} correctly left as tier 2\n")
    for gid, nm, k, kn, surn in hits:
        given = nm.split("/")[0].strip()
        print(f"  {gid}  {nm}")
        print(f"  {'':>19}  -> {given} /{surn}/   (child {kn})")
    print(f"\nwrote {OUT.relative_to(sources.REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
