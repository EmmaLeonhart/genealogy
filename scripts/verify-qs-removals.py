"""Check a QuickStatements v1 file (adds and `-` removals of item- or string-valued statements) against live Wikidata.
Usage: python scripts/verify-qs-removals.py <file.qs> [--wait MINUTES]
Prints the lines not landed; exits 0 when all have, 1 otherwise. With --wait, re-checks every 30 s until done."""
import json, sys, time, urllib.request
UA = {"User-Agent": "genealogy-check/1.0 (emma@topazcomputing.com)"}
lines = [l.split("\t") for l in open(sys.argv[1], encoding="utf-8").read().split("\n") if l.strip()]
wait = float(sys.argv[sys.argv.index("--wait") + 1]) if "--wait" in sys.argv else 0
deadline = time.time() + wait * 60
while True:
    qs = sorted({l[0].lstrip("-") for l in lines})
    ents = {}
    for i in range(0, len(qs), 50):
        u = ("https://www.wikidata.org/w/api.php?action=wbgetentities&props=claims&format=json&ids="
             + "|".join(qs[i:i + 50]))
        ents.update(json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))["entities"])
    missing = []
    for q, p, v in (l[:3] for l in lines):
        rm, q = q.startswith("-"), q.lstrip("-")
        have = set()
        for s in ents[q].get("claims", {}).get(p, []):
            val = s["mainsnak"].get("datavalue", {}).get("value")
            have.add(val.get("id") if isinstance(val, dict) else f'"{val}"')
        if (v in have) == rm:
            missing.append(("-" if rm else "") + f"{q}\t{p}\t{v}")
    if not missing or time.time() >= deadline:
        break
    time.sleep(30)
print(f"{len(lines) - len(missing)} of {len(lines)} landed")
for m in missing:
    print("NOT LANDED", m)
sys.exit(1 if missing else 0)
