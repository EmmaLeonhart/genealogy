"""Which remaining paths are worth an export, and which get page-saving instead.

**Emma, 2026-08-18**, after the destination-seeded exports turned out to halve gaps
rather than clear them: *"the person has to be either really weird and far out there,
like [Ludovico Buglio] or something, or popes or something like that. They have to be
weird and far out there, or they need to be popes, or they need to be Scandinavian, for
us to do a series of them. Otherwise, they'll just be in the same page thing."*

So three qualifying categories, and everything else goes to `geni-scraping/`:

* **Scandinavian / Nordic** --- *"if there's particularly very large paths that are
  specifically related to Scandinavian people, like the Norwegian, Swedish academics we
  were doing for the Rogaland people, these ones are pretty valuable."* This is the same
  reasoning as CLAUDE.md § *The practical goal is EMMA densely linked*: Norway and Sweden
  are where she is linked, so the paths are short and the links land near her.
* **Popes** --- named explicitly, twice.
* **Weird and far out there** --- her phrase, and she confirmed the three groups I put to
  her: religious founders and missionaries, people who named or founded something
  load-bearing, and non-European scholars.

**The place comes from the path FILENAME, not from the path text.** Every path starts at
Emma and runs up through her Norwegian ancestors, so scanning the file body for Nordic
place names fires on the path's own members and says nothing about the destination --- it
ranked Nelly Sachs and Burton Watson as strongly Scandinavian. The isolate slug carries
the destination's own recorded place (`...-1879-1964-oslo`), which is the right signal.

    PYTHONPATH=src python scripts/classify-export-worth.py
"""

from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import sources

REPO = sources.REPO_ROOT
SRC = REPO / "reports" / "destination-targets.csv"
OUT = REPO / "reports" / "export-worth.csv"
MD = REPO / "reports" / "export-worth.md"

NORDIC = re.compile(
    r"(stavanger|oslo|bergen|trondheim|kristiania|troms|drammen|kristiansand|"
    r"stockholm|uppsala|lund|goteborg|g-teborg|malmo|malm-|"
    r"helsinki|helsingfors|turku|espoo|tampere|"
    r"copenhagen|benhavn|frederiksberg|aarhus|odense|reykjav)", re.I)

POPE = re.compile(r"\bpope\b", re.I)

#: **"I'm going to leave it up to you to determine what a long path is."** — Emma,
#: 2026-08-18, and she was explicit that she is handing over an unusually large amount of
#: discretion because she is trying to close this work off.
#:
#: Sixteen. The median incomplete path carries 8 missing people, so 16 is double the
#: median and is a defensible reading of "particularly long". It is also where the
#: two-export bound pays: 16 halved twice is 4, which is page-saving territory anyway,
#: whereas a 10-missing path reaches 5 after ONE export and would be page-saved either
#: way — so an export below this buys nothing that page-saving does not.
LONG = 16

#: Popes and the weird tier qualify at ANY length: there are about 25 of them and the
#: person is the prize rather than the neighbourhood. Nordic paths need 12, because there
#: are 126 of them and without a floor they swamp the list.
NORDIC_FLOOR = 12

#: Her three confirmed "weird and far out there" groups, by destination name. This list
#: is deliberately explicit rather than heuristic --- weirdness is a judgement she made,
#: and a regex guessing at it would be the fuzzy matching this repo refuses everywhere.
WEIRD = {
    # religious founders and missionaries
    "Bahá'u'lláh Mirza Husayn Ali Nuri": "religious founder",
    "Ludovico Paolo Francesco Buglio": "Jesuit missionary to China",
    # named or founded something load-bearing
    "Dr. Raphael Lemkin": "coined 'genocide'",
    "Kristen Nygaard": "invented object-oriented programming",
    "Friedlieb Ferdinand Runge": "isolated caffeine",
    # non-European scholars
    "Fu Ssu-nien 傅斯年": "president of Academia Sinica",
    "Akeo Watanabe": "Japanese conductor",
}


def main() -> int:
    rows = [r for r in csv.DictReader(io.open(SRC, encoding="utf-8"))
            if r["action"] == "export"]

    for r in rows:
        m = int(r["missing"])
        pope = bool(POPE.search(r["destination"]))
        weird = r["destination"] in WEIRD
        nordic = bool(NORDIC.search(r["path"]))
        if m >= LONG:
            r["worth"], r["why"] = "export", "long path"
        elif pope:
            r["worth"], r["why"] = "export", "pope"
        elif weird:
            r["worth"], r["why"] = "export", f"weird: {WEIRD[r['destination']]}"
        elif nordic and m >= NORDIC_FLOOR:
            r["worth"], r["why"] = "export", "nordic"
        else:
            r["worth"], r["why"] = "save-pages", "short, and not significant"

    rows.sort(key=lambda r: (r["worth"] != "export", -int(r["missing"])))
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    keep = [r for r in rows if r["worth"] == "export"]
    drop = [r for r in rows if r["worth"] != "export"]
    by = {}
    for r in keep:
        by[r["why"].split(":")[0]] = by.get(r["why"].split(":")[0], 0) + 1

    L = ["# Which paths are worth an export", "",
         "Emma's rule, 2026-08-18: a path earns a series of exports only if the "
         "destination is **Scandinavian**, a **pope**, or **weird and far out there**. "
         "Everything else goes to page-saving in `geni-scraping/`.", "",
         f"Of the **{len(rows)}** paths still in the export band (4+ missing):", "",
         "| | paths |", "| --- | ---: |"]
    for k in sorted(by):
        L.append(f"| {k} | {by[k]} |")
    L += [f"| **export total** | **{len(keep)}** |",
          f"| page-saving instead | {len(drop)} |", "",
          "## The export list, longest gap first", "",
          "| missing | steps | destination | why |", "| ---: | ---: | --- | --- |"]
    for r in keep:
        L.append(f"| {r['missing']} | {r['steps']} | {r['destination']} | {r['why']} |")
    L.append("")
    io.open(MD, "w", encoding="utf-8").write("\n".join(L))

    print(f"{len(rows)} paths in the export band\n")
    for k in sorted(by):
        print(f"  {k:<10} {by[k]:>4}")
    print(f"  {'EXPORT':<10} {len(keep):>4}")
    print(f"  {'save-pages':<10} {len(drop):>4}")
    print(f"\nwrote {OUT.relative_to(REPO)} and {MD.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
