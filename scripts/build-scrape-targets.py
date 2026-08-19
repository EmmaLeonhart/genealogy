"""Who needs their Geni page saved, for the paths too short to be worth an export.

**Emma, 2026-08-18:** *"It is not worth six minutes to fill in something on the flat
tail that is just covering one or two individuals."* So a path with **<=3 missing
people** is not an export. Instead each of its members gets their profile page saved
into `geni-scraping/`, and the relatives section expanded before saving.

**Every path member needs their OWN saved page.** Emma was emphatic, correcting the
opposite claim: *"A mention on the saved page is not legitimate enough for a path
member. It's just enough for making a non-path individual."* So this lists every step
of every such path, not only the missing ones --- *"If there's a two-person path, yes,
you save the page of every single individual there."*

What a saved page yields per person: the Geni ID (-> `P2600` Geni.com profile ID), the
display name (-> label, via `scripts/labels.py`), and each relationship word, which
gives both a link property and the sex.

Rate: one page a minute, no concurrency, bail immediately on anything suspicious.

**DO NOT RE-RUN THIS WHILE THE SAVING IS IN PROGRESS.** Emma, 2026-08-19:
*"the target list is just a set amount of individuals that we are determined to
download. Me mass downloading the descendants of people should not [change it].
Just ignore these exports honestly... Just focus on getting all the pages
saved."*

The roster is **not** a fixed set of people — it is re-derived from whichever
paths currently have 1-3 missing. So any new export moves it: a path at 4
missing falls to 3 and its whole membership joins the list. Re-running it after
her thirteen `8-19 exports` took it 1,824 -> 1,869, which is the script working
and the wrong thing to do mid-run. `reports/scrape-targets.csv` was restored to
the 1,824 and is **frozen** until the saving finishes.

Her Descendants exports are filed in `exports/8-19 exports/` and are corpus like
any other; they are simply not allowed to redefine this list while it is being
worked. She keeps her own copies separately and the two will be joined later.

    PYTHONPATH=src python scripts/build-scrape-targets.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import sources

REPO = sources.REPO_ROOT
OUT = REPO / "reports" / "scrape-targets.csv"
INDI_XREF = re.compile(rb"^0 @I(\d+)@ INDI", re.M)


def main() -> int:
    present: set[str] = set()
    for path in sources.find_exports(REPO / "exports"):
        present.update(m.group(1).decode()
                       for m in INDI_XREF.finditer(path.read_bytes()))

    saved = {p.name for p in (REPO / "geni-scraping").glob("*.html")} \
        if (REPO / "geni-scraping").exists() else set()

    rows = []
    for path in sorted((REPO / "paths").glob("*.tsv")):
        steps = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#") or line.startswith("step"):
                continue
            c = line.split("\t")
            if len(c) < 2:
                continue
            gid = ""
            for tok in c[-1].split():
                if tok.startswith("geni:"):
                    gid = tok[5:]
            if gid:
                steps.append((c[0], c[1], c[2] if len(c) > 2 else "", gid))
        if not steps:
            continue
        missing = [s for s in steps if s[3] not in present]
        if not (1 <= len(missing) <= 3):
            continue
        for st, nm, rel, gid in steps:
            rows.append({
                "path": path.name,
                "path_missing": len(missing),
                "step": st,
                "name": nm,
                "relation_to_previous": rel,
                "geni_id": gid,
                "in_corpus": int(gid in present),
                "url": f"https://www.geni.com/people/x/{gid}",
            })

    # one row per person; a person on several short paths is saved once
    seen, uniq = set(), []
    for r in rows:
        if r["geni_id"] in seen:
            continue
        seen.add(r["geni_id"])
        uniq.append(r)

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(uniq[0].keys()))
        w.writeheader()
        w.writerows(uniq)

    paths = {r["path"] for r in rows}
    absent = sum(1 for r in uniq if not r["in_corpus"])
    print(f"{len(paths)} paths with 1-3 missing people")
    print(f"{len(rows):,} path memberships -> {len(uniq):,} distinct people to save")
    print(f"  {absent:,} of them are not in the corpus at all")
    print(f"  {len(uniq)-absent:,} are held but still need their own page")
    print(f"\nat one a minute that is {len(uniq)/60:.1f} hours")
    print(f"wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
