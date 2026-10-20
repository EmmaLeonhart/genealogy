"""The Japanese emperors in Emma's FamilySearch descendants file of Izanagi (`PF5Q-L8W`), against our roster.

Queue item (Emma, 2026-10-08): is `PF5Q-L8W` Izanagi, and how does the imperial line it heads line up with Geni
(`reports/japanese-emperors.tsv`, which carries the Geni ids) and with the Wikidata items. Read-only, from the
archived copy of the RootsMagic file; the roster's `ja` labels are read live from Wikidata (no edits).

    python scripts/izanagi-emperors.py [rmtree]   ->  reports/izanagi-emperors.tsv
"""
import collections
import csv
import json
import sqlite3
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RM = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"C:\Users\Emma\Documents\rootsmagic-archive\2026-10-19\PF5Q-L8W Izanagi descendants.rmtree")
UA = {"User-Agent": "genealogy-izanagi-emperors/1.0 (emma@topazcomputing.com)"}

db = sqlite3.connect(f"file:{urllib.parse.quote(RM.as_posix())}?mode=ro&immutable=1", uri=True)
db.create_collation("RMNOCASE", lambda a, b: (a.lower() > b.lower()) - (a.lower() < b.lower()))
names = collections.defaultdict(list)
fs = dict(db.execute("SELECT rmID, fsID FROM FamilySearchTable WHERE LinkType=0"))
for pid, g, s in db.execute("SELECT OwnerID, Given, Surname FROM NameTable WHERE IsPrimary=1"):
    names[" ".join(x for x in ((g or "").strip(), (s or "").strip()) if x)].append(pid)

roster = list(csv.DictReader(open(ROOT / "reports" / "japanese-emperors.tsv", encoding="utf-8"), delimiter="\t"))
ja = {}
qids = [r["qid"] for r in roster]
for i in range(0, len(qids), 50):
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "wbgetentities", "ids": "|".join(qids[i:i + 50]), "props": "labels", "languages": "ja",
         "format": "json"})
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        for q, e in json.load(r)["entities"].items():
            ja[q] = e.get("labels", {}).get("ja", {}).get("value", "")

out = ROOT / "reports" / "izanagi-emperors.tsv"
found = 0
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write("qid\tlabel\tja\tgeni_ids\tfamilysearch_ids\tfamilysearch_records\n")
    for r in roster:
        label = ja.get(r["qid"], "")
        # A FamilySearch name matches when it carries the emperor's name with 天皇 (`嵯峨天皇`, `顕仁 崇徳天皇`),
        # not preceded by 後: `冷泉天皇` is not `後冷泉天皇`.
        hits = [p for n, ps in names.items() for p in ps
                if label and label in n.replace(" ", "") and "後" + label not in n.replace(" ", "")]
        found += bool(hits)
        f.write(f"{r['qid']}\t{r['label']}\t{label}\t{r['geni_ids']}\t"
                f"{';'.join(fs.get(p, '') for p in hits)}\t{len(hits)}\n")
print(f"{found} of {len(roster)} roster emperors in {RM.name}; wrote {out}")
