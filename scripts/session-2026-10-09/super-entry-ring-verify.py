"""Check the super entry ring live: each created id on exactly one item, each super entry point's family links.

    python scripts/session-2026-10-09/super-entry-ring-verify.py
"""
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "genealogy-review/1.0 (emma)"}


def api(params):
    url = "https://www.wikidata.org/w/api.php?format=json&" + urllib.parse.urlencode(params)
    for i in range(8):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception:
            time.sleep(5 * (i + 1))
    raise SystemExit("API failed: " + url)


text = (ROOT / "reports" / "super-entry-ring-held.txt").read_text(encoding="utf-8")
ids = re.findall(r'^LAST\t(P2889|P2600)\t"([^"]+)"', text, re.M)
bad = 0
for prop, v in ids:
    hits = [h["title"] for h in api({"action": "query", "list": "search",
                                     "srsearch": f"haswbstatement:{prop}={v}"})["query"]["search"]]
    time.sleep(0.5)
    if len(hits) != 1:
        bad += 1
    print(f"{prop}={v}\t{len(hits)}\t{' '.join(hits)}")
print(f"{len(ids) - bad} of {len(ids)} on exactly one item")
rows = list(csv.DictReader(open(ROOT / "reports" / "super-entry-points.tsv", encoding="utf-8"), delimiter="\t"))
ents = api({"action": "wbgetentities", "ids": "|".join(r["qid"] for r in rows), "props": "claims"})["entities"]
for r in rows:
    c = ents[r["qid"]].get("claims", {})
    print(r["qid"], r["label"], {p: len(c.get(p, [])) for p in ("P22", "P25", "P26", "P40", "P3373")})
