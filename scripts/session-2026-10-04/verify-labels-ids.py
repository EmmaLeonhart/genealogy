"""Check a batch of id and label lines (Q P "v" / Q Lxx "v") against live Wikidata."""
import json, sys, time, urllib.error, urllib.parse, urllib.request
UA = {"User-Agent": "genealogy-batch-verify/1.0 (emma@topazcomputing.com)"}
rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
ids = sorted({r[0] for r in rows})
E = {}
for i in range(0, len(ids), 50):
    for t in range(8):
        try:
            u = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(dict(action="wbgetentities", ids="|".join(ids[i:i+50]), props="labels|claims", format="json"))
            E.update(json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))["entities"]); break
        except urllib.error.HTTPError as x:
            if x.code != 429: raise
            time.sleep(30)
    time.sleep(1)
bad = []
for q, p, v in (r[:3] for r in rows):
    v = json.loads(v)
    if p.startswith("L"):
        ok = E[q].get("labels", {}).get(p[1:], {}).get("value") == v
    else:
        ok = any(c["mainsnak"].get("datavalue", {}).get("value") == v for c in E[q].get("claims", {}).get(p, []))
    if not ok: bad.append((q, p, v))
print(f"{len(rows)-len(bad)} ok, {len(bad)} not as intended")
for b in bad: print("  ", *b)
