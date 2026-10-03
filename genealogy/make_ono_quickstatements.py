"""Draft QuickStatements (v1) for putting the Ono Inbe pedigree on Wikidata.
REVIEW ONLY: nothing here is run against Wikidata. See
research/notes/wikidata-import-plan.md. Writes
genealogy/ono_quickstatements_phase1.txt (create items) and
genealogy/ono_quickstatements_phase2.txt (family statements, with {ono:<id>}
placeholders for the QIDs phase 1 creates; {honkeicho} for the document item).
Run: python genealogy/make_ono_quickstatements.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import make_ono_gedcom as g  # noqa: E402

# Kobito and Shikobuchi are real people: no parent statements (plan, option 1).
REAL = {"21", "21b"}
GODS_NEW = {"5", "H2", "H3", "H4", "H5", "H6", "H7", "H10"}
NDL_URL = "https://dl.ndl.go.jp/pid/2538213"


def ref(key):
    img = g.by_seq.get(key, {}).get("ndl_image", "")
    return f'\tS248\t{{honkeicho}}' + (f'\tS304\t"image {img}"' if img else "") + f'\tS854\t"{NDL_URL}"'


def item(key):
    return g.WIKIDATA.get(key) or f"{{ono:{key}}}"


p1 = ["/* Phase 1: the document item. Note its new QID as {honkeicho}. */",
      "CREATE",
      'LAST\tLen\t"Inbe no Sukune honkeichō"',
      'LAST\tLja\t"斎部宿禰本系帳"',
      'LAST\tDen\t"1870 genealogy of the Ono family, claimed descendants of the Inbe clan"',
      "LAST\tP31\tQ87167",
      'LAST\tP9836\t"2538213"',
      "LAST\tP50\tQ6536470\tP1480\tQ32188232\tP1310\tQ6536257",
      "",
      "/* Phase 1: people not yet on Wikidata. Note each new QID as {ono:<id>}. */"]
for key, p in g.people.items():
    if key in g.WIKIDATA:
        continue
    en = g.EN[key]
    p1 += [f"/* {key} */", "CREATE", f'LAST\tLja\t"{p["name"]}"']
    if en.endswith("?"):
        p1.append(f'LAST\tAen\t"{en.rstrip("?")}"')  # uncertain reading: alias only
    else:
        p1.append(f'LAST\tLen\t"{en}"')
    p1 += ['LAST\tDen\t"figure in the 1870 Ono family Inbe pedigree"',
           f"LAST\tP31\t{'Q524158' if key in GODS_NEW else 'Q13002315'}",
           f"LAST\tP1343\t{{honkeicho}}" + ref(key).replace("\tS248\t{honkeicho}", "", 1)]

p2 = ["/* Phase 2: family statements, all marked disputed and referenced. */",
      "/* CHECK BY HAND: lines where both items already exist may duplicate existing claims. */"]
fem = g.FEMALE
for (father, mother), kids in g.families.items():
    for kid in kids:
        if kid in REAL:
            p2.append(f"/* skipped: parents of real person {g.EN[kid]} (plan option 1) */")
            continue
        for par, prop in ((father, "P22"), (mother, "P25")):
            if par:
                p2.append(f"{item(kid)}\t{prop}\t{item(par)}\tP1480\tQ18912752" + ref(kid))
                p2.append(f"{item(par)}\tP40\t{item(kid)}\tP1480\tQ18912752" + ref(kid))
    if father and mother:
        p2.append(f"{item(father)}\tP26\t{item(mother)}\tP1480\tQ18912752" + ref(mother))
        p2.append(f"{item(mother)}\tP26\t{item(father)}\tP1480\tQ18912752" + ref(mother))

(HERE / "ono_quickstatements_phase1.txt").write_text("\n".join(p1) + "\n", encoding="utf-8")
(HERE / "ono_quickstatements_phase2.txt").write_text("\n".join(p2) + "\n", encoding="utf-8")
print(f"phase 1: {sum(l == 'CREATE' for l in p1)} items; phase 2: "
      f"{sum(1 for l in p2 if not l.startswith('/*'))} statements")
