import csv, json, time, urllib.request, urllib.parse, collections, sys
UA = "genealogy-session/1.0 (emma@topazcomputing.com)"
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter="\t"))
ids = sorted({r[k] for r in rows for k in ("item", "wrong_value", "created_item")})
ent = {}
for i in range(0, len(ids), 50):
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({"action": "wbgetentities", "ids": "|".join(ids[i:i+50]), "props": "claims|labels", "languages": "en|mul", "format": "json"})
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90))
    ent.update(d["entities"]); time.sleep(0.5)
def vals(q, p):
    e = ent.get(q, {}); out = []
    for s in e.get("claims", {}).get(p, []):
        v = s["mainsnak"].get("datavalue", {}).get("value")
        if isinstance(v, dict): out.append(v.get("id"))
        elif v: out.append(v)
    return out
def lab(q):
    l = ent.get(q, {}).get("labels", {}); return (l.get("en") or l.get("mul") or {}).get("value", "")
REL = ("P22", "P25", "P26", "P40", "P3373")
out = csv.writer(open(sys.argv[2], "w", newline="", encoding="utf-8"), delimiter="\t")
out.writerow(["item", "item_label", "property", "wrong_value", "wrong_value_label", "created_item", "created_label", "prev_property", "verdict", "wrong_live", "right_live", "batch", "timestamp"])
qs = []; stat = collections.Counter()
byitem = {(r["item"], r["created_item"]): r["property"] for r in rows}
for r in rows:
    it, p, wv, new = r["item"], r["property"], r["wrong_value"], r["created_item"]
    prevp = [byitem[(wv, new)]] if (wv, new) in byitem else [pp for pp in REL if new in vals(wv, pp)]
    plausible = p == "P3373" and prevp == ["P3373"]
    wlive = wv in vals(it, p); rlive = new in vals(it, p)
    verdict = "keep: siblings of one person" if plausible else "false"
    stat[(verdict, wlive, rlive)] += 1
    out.writerow([it, lab(it), p, wv, lab(wv), new, lab(new), "|".join(prevp), verdict, wlive, rlive, r["batch"], r["timestamp"]])
    if verdict == "false" and wlive:
        qs.append(f"# {it} {lab(it)}: {p} {wv} {lab(wv)} is the chained LAST of batch #{r['batch']}; meant {new} {lab(new)}")
        qs.append(f"-{it}\t{p}\t{wv}")
    if not rlive:
        g = vals(new, "P2600")
        if g:
            qs.append(f"# {it}: {p} = {new} {lab(new)}, the link the batch meant")
            qs.append(f"{it}\t{p}\t{new}\tS2600\t\"{g[0]}\"")
        else:
            stat["no-geni-on-created"] += 1
open(sys.argv[3], "w", encoding="utf-8").write("\n".join(qs) + "\n")
for k, v in sorted(stat.items(), key=str): print(k, v)
print("qs commands", sum(1 for l in qs if not l.startswith("#")))
