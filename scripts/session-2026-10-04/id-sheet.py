# Fetches both sides of each id statement on reports/id-claims-added-since-2026-09-28.tsv for review.
# It decides nothing: every verdict is read by the session from this sheet.
import csv, json, sys, time, urllib.request, urllib.parse
csv.field_size_limit(10**9)
UA = "genealogy-session/1.0 (emma@topazcomputing.com)"
prop = sys.argv[1]                      # P2600 or P2889
rows = [r for r in csv.DictReader(open("reports/id-claims-added-since-2026-09-28.tsv", encoding="utf-8"), delimiter="\t")
        if r["property"] == prop]
seen, claims = set(), []
for r in rows:
    k = (r["item"], r["value"].strip('"'))
    if k not in seen: seen.add(k); claims.append((k, r["timestamp"]))
def get(ids, props):
    u = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({"action": "wbgetentities", "ids": "|".join(ids), "props": props, "languages": "en|mul|sv|nb|de|fr|zh|ja|ko", "format": "json"})
    for i in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=90)).get("entities", {})
        except Exception: time.sleep(10 * (i + 1))
    return {}
Q = sorted({q for (q, _), _ in claims}); ent = {}
for i in range(0, len(Q), 50): ent.update(get(Q[i:i + 50], "labels|descriptions|claims")); time.sleep(0.3)
rel = sorted({s["mainsnak"]["datavalue"]["value"]["id"] for e in ent.values() for p in ("P22", "P25", "P26", "P40")
              for s in e.get("claims", {}).get(p, []) if s["mainsnak"].get("datavalue")} - set(ent))
rl = {}
for i in range(0, len(rel), 50):
    for q, e in get(rel[i:i + 50], "labels").items():
        l = e.get("labels", {}); rl[q] = (l.get("en") or l.get("mul") or next(iter(l.values()), {}) or {}).get("value", "")
    time.sleep(0.3)
def L(e): l = e.get("labels", {}); return (l.get("en") or l.get("mul") or next(iter(l.values()), {}) or {}).get("value", "")
def T(e, p): return "/".join(s["mainsnak"]["datavalue"]["value"]["time"][1:5] for s in e.get("claims", {}).get(p, []) if s["mainsnak"].get("datavalue"))
def R(e, p): return [rl.get(v, L(ent[v]) if v in ent else v) for v in (s["mainsnak"]["datavalue"]["value"]["id"] for s in e.get("claims", {}).get(p, []) if s["mainsnak"].get("datavalue"))]
def V(e, p): return [s["mainsnak"]["datavalue"]["value"] for s in e.get("claims", {}).get(p, []) if s["mainsnak"].get("datavalue")]
G = {v for (_, v), _ in claims} if prop == "P2600" else set()
fam, lab, fac = {}, {}, {}
if G:
    for r in csv.DictReader(open("reports/derived-family.csv", encoding="utf-8")):
        if r["geni_id"] in G: fam[r["geni_id"]] = r
    need = set(G) | {x.strip() for r in fam.values() for k in ("fathers", "mothers", "spouses", "children") for x in r[k].split("|") if x.strip()}
    for r in csv.DictReader(open("reports/derived-labels.csv", encoding="utf-8")):
        if r["geni_id"] in need: lab[r["geni_id"]] = r.get("label_en") or r.get("label_mul") or (r.get("cjk_names") or "").split("|")[0].strip() or (r.get("other_script_names") or "").split("|")[0].strip()
    for r in csv.DictReader(open("reports/derived-facts.csv", encoding="utf-8")):
        if r["geni_id"] in G: fac[r["geni_id"]] = r
def N(s): return [lab.get(x.strip(), x.strip()) for x in s.split("|") if x.strip()]
out = []
for n, ((q, v), ts) in enumerate(claims):
    e = ent.get(q, {}); f = fam.get(v, {}); fa = fac.get(v, {})
    out.append({"n": n, "qid": q, "value": v, "added": ts, "live": v in [str(x) for x in V(e, prop)],
                "W": {"name": L(e), "desc": (e.get("descriptions", {}).get("en") or {}).get("value", ""), "b": T(e, "P569"), "d": T(e, "P570"),
                      "f": R(e, "P22"), "m": R(e, "P25"), "s": R(e, "P26"), "c": R(e, "P40")[:6], "geni": V(e, "P2600"), "fs": V(e, "P2889")},
                "S": {"name": lab.get(v, ""), "b": fa.get("birth_date_raw", ""), "d": fa.get("death_date_raw", ""),
                      "f": N(f.get("fathers", "")), "m": N(f.get("mothers", "")), "s": N(f.get("spouses", "")), "c": N(f.get("children", ""))[:6]}})
json.dump(out, open(f"reports/session-2026-10-04/id-review-{prop}.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(out), prop, "statements;", sum(o["live"] for o in out), "still live")
