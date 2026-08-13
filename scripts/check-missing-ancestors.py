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

# href is the first attribute on the anchor, so its value ends at the closing
# quote before the other attributes; capture id, the through= seed, then the
# visible name in the anchor body (empty for the avatar-image copy of the link).
ANCHOR = re.compile(
    r'<a href="[^"]*?people/[^"/]+/(\d+)\?through=(\d+)"[^>]*>([^<]*)</a>'
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
    """Yield (geni_id, name, root, seed, page) for every enumerated ancestor."""
    for page in sorted(PAGES_DIR.glob("*.html")):
        text = page.read_text(encoding="utf-8", errors="replace")
        for gid, seed, name in ANCHOR.findall(text):
            yield gid, html.unescape(name).strip(), root_name(page), seed, page.name


def main() -> None:
    counts = build_present_counts()

    # Collapse to one record per (id, root): a person is listed once per page but
    # appears twice in the markup (avatar + name link); keep the best name seen.
    people: dict[tuple[str, str], dict] = {}
    for gid, name, root, seed, pagename in read_pages():
        key = (gid, root)
        rec = people.setdefault(
            key,
            {"geni_id": gid, "name": name, "root": root, "seed": seed, "pages": set()},
        )
        rec["pages"].add(pagename)
        if len(name) > len(rec["name"]):
            rec["name"] = name

    rows = []
    for rec in people.values():
        n = counts.get(rec["geni_id"], 0)
        rows.append(
            {
                "geni_id": rec["geni_id"],
                "name": rec["name"],
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
