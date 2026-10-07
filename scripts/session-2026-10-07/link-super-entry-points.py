"""Family links for the super entry points, which are still isolates (queue item: 2026-10-06 audit, part 2).

All 11 rows of `reports/super-entry-points.tsv` have items and none has a P22/P25/P26/P40/P3373 (checked live
2026-10-07). Each is linked to every relative our tree gives it whose own Geni or FamilySearch id is already on an
item, both directions, as a creation would have been (CLAUDE.md: a created person gets every relationship at
creation). Relatives are read from `derived-family.csv` (Geni keys) or the FamilySearch corpus (`FS` keys).

Writes `reports/super-entry-points-links-2026-10-07.qs`. Sends nothing.

    python scripts/session-2026-10-07/link-super-entry-points.py
"""
import csv
import importlib.util
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))
UA = {"User-Agent": "genealogy-review/1.0 (emma)"}
OUT = ROOT / "reports" / "super-entry-points-links-2026-10-07.qs"


def api(params):
    url = "https://www.wikidata.org/w/api.php?format=json&" + urllib.parse.urlencode(params)
    for i in range(8):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception:
            time.sleep(10 * (i + 1))
    raise SystemExit("API failed: " + url)


def holder(prop, value):
    hits = api({"action": "query", "list": "search", "srsearch": f"haswbstatement:{prop}={value}"})
    return [h["title"] for h in hits["query"]["search"]]


def main():
    rows = list(csv.DictReader(open(ROOT / "reports" / "super-entry-points.tsv", encoding="utf-8"), delimiter="\t"))
    geni = {r["key"]: r for r in rows if not r["key"].startswith("FS")}
    fs = {r["key"][2:6] + "-" + r["key"][6:]: r for r in rows if r["key"].startswith("FS")}
    rel = {}   # key -> [(role, relative id, prop kind)]
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["geni_id"] in geni:
                out = []
                for col, prop in (("father", "P22"), ("mother", "P25"), ("spouses", "P26"), ("children", "P40")):
                    out += [(prop, x.strip(), "P2600") for x in (r.get(col) or "").split("|") if x.strip()]
                rel[r["geni_id"]] = out
    spec = importlib.util.spec_from_file_location("fsday", ROOT / "scripts" / "build-familysearch-day.py")
    fsday = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fsday)
    people, father, mother, spouses, children = fsday.read_corpus(sorted(fsday.CORPUS.rglob("*.ged")))
    for key, rec in people.items():
        fid = rec["fs_id"]
        if fid in fs and fid not in rel:
            out = []
            for prop, others in (("P22", [father.get(key)]), ("P25", [mother.get(key)]),
                                 ("P26", sorted(spouses.get(key, ()))), ("P40", sorted(children.get(key, ())))):
                out += [(prop, people[o]["fs_id"], "P2889") for o in others if o and people.get(o, {}).get("fs_id")]
            rel[fid] = out
    sex = {}
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["geni_id"] in geni:
                sex[r["geni_id"]] = (r.get("sex") or "").upper()
    for key, rec in people.items():
        if rec["fs_id"] in fs:
            sex.setdefault(rec["fs_id"], (rec.get("sex") or "").upper())
    lines = ["# Family links for the super entry points (isolates on Wikidata, checked 2026-10-07): each relative our",
             "# tree gives them whose own id is on an item, both directions. Run with Run."]
    for k, links in rel.items():
        row = geni.get(k) or fs.get(k)
        q = row["qid"]
        ref = f'\tS2600\t"{k}"' if k in geni else f'\tS2889\t"{k}"'
        lines.append(f"# {q} {row['label']}: {len(links)} relative(s) in the tree")
        for prop, other, idprop in links:
            hits = holder(idprop, other)
            time.sleep(1)
            if len(hits) != 1:
                lines.append(f"#   {prop} {idprop}={other}: {len(hits)} item(s), not linked")
                continue
            o = hits[0]
            lines.append(f"{q}\t{prop}\t{o}{ref}")
            back = {"P22": "P40", "P25": "P40", "P26": "P26"}.get(prop)
            if prop == "P40":
                back = {"M": "P22", "F": "P25"}.get(sex.get(k, ""))
            if back:
                lines.append(f"{o}\t{back}\t{q}{ref}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
