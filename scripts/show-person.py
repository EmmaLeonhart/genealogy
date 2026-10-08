"""Print a person item live: labels, aliases, description, family and name statements (with labels),
ids, and the account's label edits and creation from its history.
Usage: python scripts/show-person.py Q1 [Q2 ...]"""
import json, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "genealogy-check/1.0 (emma@topazcomputing.com)"}
g = lambda u: json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))
API = "https://www.wikidata.org/w/api.php?format=json&"
REL = ("P22", "P25", "P26", "P40", "P3373", "P735", "P734", "P5056")
IDS = ("P2600", "P2889", "P569", "P570")
for q in sys.argv[1:]:
    e = g(API + "action=wbgetentities&props=labels|aliases|descriptions|claims&languages=mul|en|ja&ids=" + q)["entities"][q]
    c = e.get("claims", {})
    vals = {s["mainsnak"]["datavalue"]["value"]["id"] for p in REL for s in c.get(p, [])
            if "datavalue" in s["mainsnak"]}
    names = {}
    vl = list(vals)
    for i in range(0, len(vl), 50):
        for k, v in g(API + "action=wbgetentities&props=labels&languages=mul|en&ids=" + "|".join(vl[i:i + 50]))["entities"].items():
            names[k] = (v.get("labels", {}).get("mul") or v.get("labels", {}).get("en") or {}).get("value", "")
    print(f"== {q}", {k: v["value"] for k, v in e.get("labels", {}).items()},
          {k: [a["value"] for a in v] for k, v in e.get("aliases", {}).items()},
          (e.get("descriptions", {}).get("en") or {}).get("value", ""))
    for p in REL:
        if p in c:
            print(f"   {p}", [f'{s["mainsnak"]["datavalue"]["value"]["id"]} {names.get(s["mainsnak"]["datavalue"]["value"]["id"], "")}'
                              for s in c[p] if "datavalue" in s["mainsnak"]])
    for p in IDS:
        if p in c:
            print(f"   {p}", [str(s["mainsnak"].get("datavalue", {}).get("value", {}).get("time")
                                  if p in ("P569", "P570") else s["mainsnak"].get("datavalue", {}).get("value"))
                              for s in c[p]])
    h = g(API + "action=query&prop=revisions&rvlimit=200&rvdir=newer&rvprop=timestamp|user|comment&titles=" + q)
    for r in list(h["query"]["pages"].values())[0].get("revisions", []):
        cm = r.get("comment", "")
        if "label" in cm or "create-item" in cm or ("P22]" in cm) or r["user"] != "日巫女":
            print("     ", r["timestamp"], r["user"], cm[:110])
