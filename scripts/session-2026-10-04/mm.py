import csv, json, time, urllib.request, urllib.parse, sys
UA = "genealogy-session/1.0 (emma@topazcomputing.com)"
rows = [r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter="\t") if r["how"] == "created-by-account"]
ids = sorted({r[k] for r in rows for k in ("item", "male_mother")})
ent = {}
for i in range(0, len(ids), 50):
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({"action": "wbgetentities", "ids": "|".join(ids[i:i+50]), "props": "claims|labels", "languages": "en|mul", "format": "json"})
    ent.update(json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90))["entities"]); time.sleep(0.5)
def vals(q, p):
    return [s["mainsnak"].get("datavalue", {}).get("value") for s in ent[q].get("claims", {}).get(p, [])]
def ids_(q, p): return [v["id"] for v in vals(q, p) if isinstance(v, dict)]
def lab(q):
    l = ent[q].get("labels", {}); return (l.get("en") or l.get("mul") or {}).get("value", "")
w = csv.writer(open(sys.argv[2], "w", newline="", encoding="utf-8"), delimiter="\t")
w.writerow(["item", "item_label", "male_mother", "male_mother_label", "his_P40_lists_item", "item_P22", "action", "created"])
qs = []; n = {"move": 0, "remove": 0, "gone": 0}
for r in rows:
    it, m = r["item"], r["male_mother"]
    if m not in ids_(it, "P25"): n["gone"] += 1; continue
    child = it in ids_(m, "P40"); p22 = ids_(it, "P22"); g = vals(it, "P2600")
    act = "move to P22" if child and m not in p22 else ("remove (already P22)" if m in p22 else "remove")
    w.writerow([it, lab(it), m, lab(m), child, "|".join(p22), act, r["timestamp"]])
    qs.append(f"# {it} {lab(it)}: P25 mother = {m} {lab(m)}, a man; {act}")
    qs.append(f"-{it}\tP25\t{m}")
    if act == "move to P22":
        qs.append(f"{it}\tP22\t{m}" + (f"\tS2600\t\"{g[0]}\"" if g else "")); n["move"] += 1
    else: n["remove"] += 1
open(sys.argv[3], "a", encoding="utf-8").write("\n".join(qs) + "\n")
print(n)
