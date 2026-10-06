"""Before a batch runs: every creation's Geni id (P2600) and every name-item creation's label, checked live on
Wikidata, so nothing created since the batch's snapshot is created twice.
Usage: python scripts/session-2026-10-06/batch-precheck.py reports/wikidata-garborg-day-manual.txt"""
import json, re, sys, time, urllib.parse, urllib.request
UA = {"User-Agent": "genealogy-batch-precheck/1.0 (emma@topazcomputing.com)"}
text = open(sys.argv[1], encoding="utf-8").read()
blocks = re.split(r"(?m)^CREATE\s*$", text)[1:]
genis, names = [], []
for b in blocks:
    m = re.search(r'LAST\tP2600\t"(\d+)"', b)
    if m:
        genis.append(m.group(1))
    elif re.search(r"LAST\tP31\tQ(110874|202444|101352)\b", b):
        lab = re.search(r'LAST\tLmul\t"([^"]+)"', b)
        p31 = re.findall(r"LAST\tP31\t(Q\d+)", b)
        if lab:
            names.append((lab.group(1), p31))
def sparql(q):
    u = "https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(q)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))["results"]["bindings"]
hits = []
for i in range(0, len(genis), 200):
    vals = " ".join(f'"{g}"' for g in genis[i:i + 200])
    for r in sparql(f"SELECT ?item ?g WHERE {{ VALUES ?g {{ {vals} }} ?item wdt:P2600 ?g }}"):
        hits.append((r["g"]["value"], r["item"]["value"].rsplit("/", 1)[1]))
    time.sleep(1)
print(f"{len(blocks)} creations, {len(genis)} with a Geni id, {len(names)} name items")
print("Geni ids already on Wikidata:", hits or "none")
for lab, p31 in names:
    q = (f'SELECT ?item WHERE {{ ?item rdfs:label "{lab}"@mul . VALUES ?c {{ {" ".join("wd:"+c for c in p31)} }} '
         f'?item wdt:P31 ?c }} LIMIT 3')
    r = sparql(q)
    if r:
        print("name item exists:", lab, [x["item"]["value"].rsplit("/", 1)[1] for x in r])
    time.sleep(0.5)
