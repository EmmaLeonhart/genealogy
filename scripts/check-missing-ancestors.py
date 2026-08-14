"""Check the saved "missing ancestors" pages against the synoptic tree.

Emma saves a Geni *ancestor list* page for a root person; Geni enumerates every
ancestor it knows, including the ones an export (capped ~4100) never reached.
This script reads those pages, pulls each enumerated ancestor by its Geni
profile id, and asks one question per person: is that id present as an INDI in
the merged corpus, or absent?

Matching is an exact join on the Geni profile id -- the repo's primary key --
never a substring and never a name. `data-profile-id` on the page equals the
INDI xref in the export for the same person (verified on Coenwalh King of
Wessex, 6000000000437546093). A short legacy id like 45855 substring-matches 59
files and none of them are that person, which is exactly why substrings are out.

Writes reports/missing-ancestors-check.csv -- one row per (page person), every
instance -- and prints a present/absent summary.
"""

from __future__ import annotations

import csv
import html
import re
import sys
from collections import Counter
from pathlib import Path

from genimerge import sources

# Windows consoles default to cp1252; ancestor names are full of runic-era and
# accented characters. Never let a print crash after the CSV is already written.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
PAGES_DIR = REPO / "missing ancestors"
OUT_CSV = REPO / "reports" / "missing-ancestors-check.csv"

# **Scope to the row, never to the anchors.** Matching `people/<slug>/<id>`
# anchors anywhere on the page silently pulls in the *profile managers* -- the
# Geni users who curate each ancestor -- because their links sit in a
# `managed_by-area` cell of the same row and carry the same `?through=` seed.
# That is not a near-miss: it put Sally Cole, Margaret C and Bernard Assaf into
# a list of Clara's Norwegian ancestors, and inflated the absent count with
# living account holders no export will ever contain. It is the same trap
# CLAUDE.md documents for relationship paths, where only anchors inside
# `span.segment > span.name` are on the path.
#
# Geni gives one `<tr>` per enumerated ancestor and stamps the id on the row
# itself, so the row is the record and everything nested in it is decoration.
ROW = re.compile(
    r'<tr id="list_row_(\d+)"[^>]*data-profile-id="\1"(.*?)</tr>', re.S
)
# ...and within a row, the ancestor's own name lives in the name-area cell.
NAME_CELL = re.compile(r'<td class="name-area[^"]*"[^>]*>(.*?)</td>', re.S)
NAME_LINK = re.compile(r'<a [^>]*data-profile-id="(\d+)"[^>]*>([^<]*)</a>')
SEED = re.compile(r"\?through=(\d+)")
RELATION = re.compile(
    r'<td class="relationship-area[^"]*"[^>]*>.*?</div>\s*([^<]*)</td>', re.S
)
INDI_XREF = re.compile(r"^0 @I(\d+)@ INDI", re.MULTILINE)


def build_present_counts() -> Counter:
    """id -> number of distinct exports holding it as an INDI."""
    counts: Counter = Counter()
    exports = sources.find_exports()
    for i, path in enumerate(exports, 1):
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        for gid in set(INDI_XREF.findall(text)):
            counts[gid] += 1
    print(f"corpus: {len(exports)} exports, {len(counts)} distinct people")
    return counts


def root_name(page: Path) -> str:
    # "Randolph Paulus Borsheim's Ancestors207.html" -> "Randolph Paulus Borsheim"
    stem = page.stem
    return re.sub(r"'s Ancestors.*$", "", stem)


def read_pages():
    """Yield (geni_id, name, relationship, root, seed, page) per enumerated ancestor.

    One record per `<tr>`. The name is taken from the row's own name-area cell
    and only when the anchor's `data-profile-id` equals the row's, so a manager
    link cannot supply it either.
    """
    for page in sorted(PAGES_DIR.glob("*.html")):
        text = page.read_text(encoding="utf-8", errors="replace")
        for gid, body in ROW.findall(text):
            name = ""
            cell = NAME_CELL.search(body)
            if cell:
                for anchor_id, anchor_text in NAME_LINK.findall(cell.group(1)):
                    if anchor_id == gid and anchor_text.strip():
                        name = html.unescape(anchor_text).strip()
                        break
            rel = RELATION.search(body)
            seed = SEED.search(body)
            yield (gid, name, html.unescape(rel.group(1)).strip() if rel else "",
                   root_name(page), seed.group(1) if seed else "", page.name)


def main() -> None:
    counts = build_present_counts()

    # Collapse to one record per (id, root): a person is listed once per page but
    # appears twice in the markup (avatar + name link); keep the best name seen.
    people: dict[tuple[str, str], dict] = {}
    for gid, name, rel, root, seed, pagename in read_pages():
        key = (gid, root)
        rec = people.setdefault(
            key,
            {"geni_id": gid, "name": name, "relationship": rel, "root": root,
             "seed": seed, "pages": set()},
        )
        rec["pages"].add(pagename)
        if len(name) > len(rec["name"]):
            rec["name"] = name
        if rel and not rec["relationship"]:
            rec["relationship"] = rel

    rows = []
    for rec in people.values():
        n = counts.get(rec["geni_id"], 0)
        rows.append(
            {
                "geni_id": rec["geni_id"],
                "name": rec["name"],
                "relationship": rec["relationship"],
                "root": rec["root"],
                "seed": rec["seed"],
                "present": "yes" if n else "no",
                "n_exports": n,
                "source_pages": ";".join(sorted(rec["pages"])),
            }
        )

    rows.sort(key=lambda r: (r["root"], r["present"], r["name"]))

    OUT_CSV.parent.mkdir(exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=[
                "geni_id",
                "name",
                "relationship",
                "root",
                "seed",
                "present",
                "n_exports",
                "source_pages",
            ],
        )
        w.writeheader()
        w.writerows(rows)

    total = len(rows)
    absent = [r for r in rows if r["present"] == "no"]
    print(f"\nwrote {OUT_CSV.relative_to(REPO)}  ({total} enumerated ancestors)")
    print(f"present: {total - len(absent)}   absent: {len(absent)}")
    by_root: Counter = Counter()
    absent_by_root: Counter = Counter()
    for r in rows:
        by_root[r["root"]] += 1
        if r["present"] == "no":
            absent_by_root[r["root"]] += 1
    print("\nper root person  (absent / total):")
    for root in sorted(by_root):
        print(f"  {root:<28} {absent_by_root[root]:>3} / {by_root[root]}")
    print("\nabsent people (id  name  root):")
    for r in absent:
        print(f"  {r['geni_id']:<20} {r['name']:<45} {r['root']}")


if __name__ == "__main__":
    main()
