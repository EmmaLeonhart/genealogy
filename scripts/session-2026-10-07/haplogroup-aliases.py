"""Every live item carrying a haplogroup as a label or alias, from the Geni name fields that hold one.
Audit 2026-10-06 defect (4): Alba Autun Q141653950 carries Amul "mtH1".
Writes reports/haplogroup-aliases-2026-10-07.csv. Usage: python scripts/session-2026-10-07/haplogroup-aliases.py"""
import csv, json, sys, time, urllib.parse, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from namemodel import HAPLOGROUP  # noqa: E402
csv.field_size_limit(10 ** 8)
UA = {"User-Agent": "genealogy-haplogroup-check/1.0 (emma@topazcomputing.com)"}
ids = set()
for r in csv.DictReader(open(ROOT / "reports" / "display-names.csv", encoding="utf-8")):
    if any(HAPLOGROUP.search(r.get(f) or "") for f in ("givn", "surn", "nick", "nsfx", "marnm")):
        ids.add(r["geni_id"])
qid_of = {}
for g in sorted(ids):
    if not g.isdigit():
        continue
    u = ("https://www.wikidata.org/w/api.php?action=query&format=json&list=search&srsearch="
         + urllib.parse.quote(f"haswbstatement:P2600={g}"))
    for h in json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))["query"]["search"]:
        qid_of.setdefault(g, h["title"])
    time.sleep(0.5)
rows = []
qids = sorted(set(qid_of.values()))
for i in range(0, len(qids), 50):
    u = ("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=labels|aliases&ids="
         + "|".join(qids[i:i + 50]))
    ents = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))["entities"]
    for q, e in ents.items():
        for kind, vals in (("label", [v for v in e.get("labels", {}).values()]),
                           ("alias", [a for vs in e.get("aliases", {}).values() for a in vs])):
            for v in vals:
                if HAPLOGROUP.search(v["value"]):
                    rows.append({"qid": q, "kind": kind, "lang": v["language"], "value": v["value"],
                                 "geni_id": next(g for g, x in qid_of.items() if x == q)})
    time.sleep(0.5)
out = ROOT / "reports" / "haplogroup-aliases-2026-10-07.csv"
with out.open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["qid", "geni_id", "kind", "lang", "value"])
    w.writeheader(); w.writerows(sorted(rows, key=lambda r: (r["qid"], r["kind"], r["lang"], r["value"])))
print(f"{len(ids)} Geni ids with a haplogroup in a name field, {len(qids)} with an item, {len(rows)} live strings")
