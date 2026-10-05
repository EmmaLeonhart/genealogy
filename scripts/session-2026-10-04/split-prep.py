"""For zipper pairs judged SPLIT, print each wrong link with its live state, every relative's label and
claims, our ledger item for the Geni person, and Wikidata search hits for the Geni name, so a split
batch can be written by hand from live data.  Usage: split-prep.py <n> [<n> ...]"""
import csv, json, sys, time, urllib.parse, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
UA = "genealogy-session/1.0 (emma@topazcomputing.com)"
def api(**p):
    u = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({**p, "format": "json"})
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=90))
o = json.load(open(ROOT / "reports/session-2026-10-04/zipper-pairs-behind-wikidata-links.json", encoding="utf-8"))
led = {}
for r in csv.DictReader(open(ROOT / "reports/garborg-qids.tsv", encoding="utf-8"), delimiter="\t"):
    led.setdefault(r["geni_id"], []).append(r["qid"])
ns = [int(a) for a in sys.argv[1:]]
ids = set()
for n in ns:
    ids.add(o[n]["qid"]); ids |= {t for l in o[n]["links"] for t in l.split() if t.startswith("Q")}
ent = {}
def fetch(qs):
    qs = sorted(set(qs) - set(ent))
    for k in range(0, len(qs), 50):
        ent.update(api(action="wbgetentities", ids="|".join(qs[k:k+50]), props="claims|labels|descriptions", languages="en|mul|ja")["entities"]); time.sleep(.3)
fetch(ids)
def vals(q, p):
    out = []
    for s in ent.get(q, {}).get("claims", {}).get(p, []):
        v = s["mainsnak"].get("datavalue", {}).get("value")
        out.append(v.get("id") if isinstance(v, dict) else v)
    return out
fetch({v for q in list(ent) for p in ("P22","P25","P26","P40","P3373") for v in vals(q, p) if v})
def lab(q):
    l = ent.get(q, {}).get("labels", {}); return (l.get("en") or l.get("mul") or l.get("ja") or {}).get("value", "?")
def show(q):
    d = ent.get(q, {}).get("descriptions", {}).get("en", {}).get("value", "")
    rel = " ".join(f"{p}:{v}({lab(v)[:24]})" for p in ("P22","P25","P26","P40","P3373") for v in vals(q, p))
    return f"{q} {lab(q)} [{d[:50]}] P2600={vals(q,'P2600')} | {rel}"
for n in ns:
    r = o[n]
    print(f"\n#{n} Geni {r['geni']} {r['G']['name']} b{r['G']['b']} d{r['G']['d']} sex {r['G'].get('sex')}  ledger={led.get(r['geni'])}")
    print("   G f", r["G"]["f"], "m", r["G"]["m"], "s", r["G"]["s"], "c", r["G"]["c"][:5])
    print("   WD", show(r["qid"]))
    for l in r["links"]:
        t = l.split()
        if len(t) == 3:
            print(f"   link {l}: {'LIVE' if t[2] in vals(t[0], t[1]) else 'gone'}")
    for q in sorted({t for l in r["links"] for t in l.split() if t.startswith("Q")} - {r["qid"]}):
        print("     ", show(q))
    try:
        hits = api(action="wbsearchentities", search=r["G"]["name"], language="en", limit=5)["search"]
        print("   search:", [(h["id"], h.get("label"), h.get("description", "")[:40]) for h in hits])
    except Exception as e:
        print("   search failed", e)
