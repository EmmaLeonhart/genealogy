"""Check a run QuickStatements batch against live Wikidata, line by line.

Removals must be gone, additions on existing items present. A CREATE block is found by the
P2600 it carries and every statement of the block is checked on the new item, LAST resolved.
Usage: python verify-qs.py reports/<batch>.qs
"""
import json, sys, time, urllib.parse, urllib.request

UA = {"User-Agent": "genealogy-batch-verify/1.0 (emma@topazcomputing.com)"}


def api(**p):
    p["format"] = "json"
    req = urllib.request.Request("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(p), headers=UA)
    r = json.load(urllib.request.urlopen(req))
    time.sleep(0.2)
    return r


def values(q, prop):
    e = api(action="wbgetentities", ids=q, props="claims")["entities"][q]
    out = []
    for c in e.get("claims", {}).get(prop, []):
        v = (c["mainsnak"].get("datavalue") or {}).get("value")
        out.append(v["id"] if isinstance(v, dict) and "id" in v else v)
    return out


lines = [l.rstrip("\n").split("\t") for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
blocks, cur = [], None
for f in lines:
    if f == ["CREATE"]:
        cur = []; blocks.append(("create", cur))
    elif f[0] == "LAST" and cur is not None:
        cur.append(f)
    else:
        cur = None; blocks.append(("line", f))
last, ok, bad = None, 0, []
for kind, b in blocks:
    if kind == "create":
        geni = next(f[2].strip('"') for f in b if f[1] == "P2600")
        hits = api(action="query", list="search", srsearch=f"haswbstatement:P2600={geni}")["query"]["search"]
        last = hits[0]["title"] if hits else None
        if not last:
            bad.append(f"CREATE {geni}: no item"); continue
        for f in b:
            if f[1].startswith("P") and f[1] not in ("P2600",):
                v = f[2].strip('"')
                (ok := ok + 1) if v in values(last, f[1]) else bad.append(f"{last} {f[1]} {v} missing")
        print(f"created {last} for Geni {geni}")
        continue
    s, p, o = b[0], b[1], b[2]
    rm = s.startswith("-")
    s = s.lstrip("-")
    s = last if s == "LAST" else s
    o = last if o == "LAST" else o.strip('"')
    present = o in values(s, p)
    if present != rm:
        ok += 1
    else:
        bad.append(f"{'-' if rm else ''}{s} {p} {o}: {'still there' if rm else 'missing'}")
print(f"{ok} ok, {len(bad)} not as intended")
for x in bad:
    print("  ", x)
