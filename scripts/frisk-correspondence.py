"""Pair the Cameron Frisk Geni ancestors with the FamilySearch-sourced tree, by POSITION.

The two trees are near-structurally identical, so the correspondence is a walk up the pedigree
from Cameron on both sides at once: father against father, mother against mother, ahnentafel
number for ahnentafel number. Names and years do not choose a pair -- position does -- they are
carried beside it so a disagreement is visible.

    frisk_geni/Cameron Frisk geni ancestors.ged   Geni export, keyed on the Geni profile id
    frisk_geni/Cameron Frisk.ged                  MyHeritage export of the FamilySearch-sourced tree
    -> reports/frisk-geni-familysearch.tsv
"""
import csv
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from genimerge.gedcom import parse_file  # noqa: E402
from genimerge.dates import parse_date  # noqa: E402

GENI = ROOT / "frisk_geni" / "Cameron Frisk geni ancestors.ged"
MH = ROOT / "frisk_geni" / "Cameron Frisk.ged"
OUT = ROOT / "reports" / "frisk-geni-familysearch.tsv"


def index(path):
    doc = parse_file(path)
    recs = doc.by_xref()
    people = {x: r for x, r in recs.items() if r.tag == "INDI"}
    return people, recs


def name(rec):
    return (rec.value_of("NAME") or "").replace("/", "").strip() if rec else ""


def year(rec, tag):
    node = rec.path(tag, "DATE") if rec else None
    return parse_date(node.value).year if node is not None else None


def parents(rec, recs):
    """Father and mother from the first family the person is a child in."""
    for c in rec.children:
        if c.tag == "FAMC" and c.value in recs:
            fam = recs[c.value]
            return fam.value_of("HUSB"), fam.value_of("WIFE")
    return None, None


def fold(s):
    s = unicodedata.normalize("NFKD", s.casefold())
    return "".join(ch for ch in s if ch.isalnum() or ch == " ").split()


def agree(a, b):
    """Shared words between the two names -- a reading beside the position, never a choice."""
    return len(set(fold(a)) & set(fold(b)))


def root(people, first, last):
    for x, r in people.items():
        if fold(name(r)) == [first, last]:
            return x
    sys.exit("no %s %s in the file" % (first, last))


def main():
    g_people, g_recs = index(GENI)
    m_people, m_recs = index(MH)
    queue = [(1, root(g_people, "cameron", "frisk"), root(m_people, "cameron", "frisk"))]
    rows = []
    while queue:
        n, gx, mx = queue.pop(0)
        g, m = g_people[gx], m_people[mx]
        gb, mb = year(g, "BIRT"), year(m, "BIRT")
        rows.append({
            "ahnentafel": n, "generation": n.bit_length() - 1,
            "geni_id": gx.strip("@").lstrip("I"), "geni_name": name(g),
            "geni_birth": gb or "", "geni_death": year(g, "DEAT") or "",
            "mh_uid": m.value_of("_UID"), "mh_name": name(m),
            "mh_birth": mb or "", "mh_death": year(m, "DEAT") or "",
            "shared_words": agree(name(g), name(m)),
            "birth_gap": abs(gb - mb) if gb and mb else "",
        })
        gf, gm = parents(g, g_recs)
        mf, mm = parents(m, m_recs)
        if gf in g_people and mf in m_people:
            queue.append((2 * n, gf, mf))
        if gm in g_people and mm in m_people:
            queue.append((2 * n + 1, gm, mm))
    rows.sort(key=lambda r: r["ahnentafel"])
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    named = sum(1 for r in rows if r["shared_words"])
    print("%d positional pairs, %d sharing a name word, %d sharing none -> %s"
          % (len(rows), named, len(rows) - named, OUT.relative_to(ROOT)))


if __name__ == "__main__":
    main()
