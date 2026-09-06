"""Take a collector family scrape off stdin as JSON and write it into the repo.

**Emma, 2026-09-06:** *"Only the exports need downloading because you write stuff into files in
the repo you dummy."* This is the "write it into files in the repo" half. The collector returns
the scrape on a data attribute; this puts it where it belongs and updates the isolate ledger in
the same pass, so the two cannot drift.

It writes two things per person:

  `geni-families/<geni id>-family.tsv`   step 1 of `docs/per-individual-loop.md`
  a row in `reports/isolates.csv`        her instruction, 2026-09-03: *"you store these numbers
                                         even before a path is found or not, but you always stay
                                         on the page and request the path"*

**`path_found` is THREE-VALUED and the blank is load-bearing.** `yes` / `no` / empty-while-running.
A pending search folded into the miss column is the failure `geni-paths/README.md` § *THE SEARCH
IS ASYNCHRONOUS* records: nine targets read as *"0 steps"* when they had simply not finished.

**A MISSING STATISTICS ROW IS ZERO** -- Emma, 2026-09-03 on Dorothy Jeakins: *"geni is weird and
gives zero as not an option there"*. The collector already reads it that way; nothing here turns
a zero back into a blank.
"""

from __future__ import annotations

import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAMILIES = ROOT / "geni-families"
ISOLATES = ROOT / "reports" / "isolates.csv"

FIELDS = ["family_tree", "blood_relatives", "ancestors", "descendants", "followers"]

#: What the profile's own banner says, mapped onto the three states. Order matters: the
#: in-progress sentence is checked first because a page can carry both while it settles.
def path_state(banner: str) -> str:
    b = (banner or "").lower()
    if "path search in progress" in b or "relative?" in b:
        return ""          # pending -- come back, never a miss
    if "no path found" in b or "could not be found" in b:
        return "no"
    return "yes" if b else ""


def main() -> int:
    blob = json.load(sys.stdin)
    ext, relatives = blob["ext"], blob["relatives"]
    gid, name = ext["geni_id"], ext.get("name", "")
    stats = ext.get("stats", {})

    head = [
        "# Immediate family scraped from the Geni profile page. Step 1 of the per-individual loop.",
        "# subject\t%s\t%s" % (gid, name),
        "# prose\t%s" % blob.get("prose", "")[:400],
        "# statistics\t" + "\t".join(
            "%s=%s" % (f, "" if stats.get(f) is None else stats[f]) for f in FIELDS)
        + "\tread=%s" % ("1" if stats.get("read") else "0"),
        "\t".join(["subject_geni_id", "relation", "phrase", "relative_geni_id", "relative_name"]),
    ]
    for r in relatives:
        head.append("\t".join([gid, r["relation"], r["phrase"], r["geni_id"], r["name"]]))
    FAMILIES.mkdir(exist_ok=True)
    (FAMILIES / ("%s-family.tsv" % gid)).write_text("\n".join(head) + "\n", encoding="utf-8")

    rows = list(csv.reader(ISOLATES.open(encoding="utf-8")))
    header, body = rows[0], [r for r in rows[1:] if r and r[0] != gid]
    body.append([gid, name] + [str(stats.get(f, 0) or 0) for f in FIELDS]
                + ["2026-09-06", path_state(blob.get("banner", ""))])
    body.sort(key=lambda r: r[0])
    with ISOLATES.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(body)

    sys.path.insert(0, str(ROOT / "scripts"))
    from export_gate import decide
    d = decide(stats)
    print("%s  %s | %d relatives | path=%r | %s" % (
        gid, name, len(relatives), path_state(blob.get("banner", "")) or "pending",
        ("EXPORT if it misses: " + d["why"]) if d["export"] else ("NO EXPORT: " + d["why"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
