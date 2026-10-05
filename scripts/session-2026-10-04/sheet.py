# Lists the 1,261 zipper pairs behind live statements and fetches both sides. It decides nothing.
import csv, json, time, urllib.request, urllib.parse, sys
csv.field_size_limit(10**9)
SP = "reports/session-2026-10-04"
UA = "genealogy-session/1.0 (emma@topazcomputing.com)"
pairs = {}
for r in csv.DictReader(open('reports/zipper-only-links-on-wikidata.csv', encoding='utf-8')):
    pairs.setdefault((r['relative_geni'], r['relative_qid']), set()).add(f"{r['created_qid']} {r['property']}")
for r in csv.DictReader(open('reports/zipper-driven-links.csv', encoding='utf-8')):
    pairs.setdefault((r['zipper_geni'], r['zipper_qid']), set()).add(f"{r['subject']} {r['property']} {r['value']}")
G = {g for g, _ in pairs}
fam, fac, lab = {}, {}, {}
for r in csv.DictReader(open('reports/derived-family.csv', encoding='utf-8')):
    if r['geni_id'] in G: fam[r['geni_id']] = r
need = set(G)
for r in fam.values():
    for k in ('fathers', 'mothers', 'spouses', 'children'):
        need |= {x.strip() for x in r[k].split('|') if x.strip()}
for r in csv.DictReader(open('reports/derived-labels.csv', encoding='utf-8')):
    if r['geni_id'] in need: lab[r['geni_id']] = r.get('label_en') or r.get('label_mul') or ''
for r in csv.DictReader(open('reports/derived-facts.csv', encoding='utf-8')):
    if r['geni_id'] in G: fac[r['geni_id']] = r
Q = sorted({q for _, q in pairs})
ent = {}
def get(ids, props):
    u = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({"action": "wbgetentities", "ids": "|".join(ids), "props": props, "languages": "en|mul|ja|zh|ko", "format": "json"})
    for i in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=90))["entities"]
        except Exception: time.sleep(10 * (i + 1))
    return {}
for i in range(0, len(Q), 50):
    ent.update(get(Q[i:i + 50], "labels|descriptions|claims")); time.sleep(0.3)
rel = set()
for e in ent.values():
    for p in ('P22', 'P25', 'P26', 'P40'):
        for s in e.get('claims', {}).get(p, []):
            v = s['mainsnak'].get('datavalue', {}).get('value')
            if isinstance(v, dict): rel.add(v['id'])
rl = {}
rel = sorted(rel - set(ent))
for i in range(0, len(rel), 50):
    for q, e in get(rel[i:i + 50], "labels").items():
        l = e.get('labels', {}); rl[q] = (l.get('en') or l.get('mul') or next(iter(l.values()), {})).get('value', '')
    time.sleep(0.3)
def L(e):
    l = e.get('labels', {}); return (l.get('en') or l.get('mul') or next(iter(l.values()), {}) or {}).get('value', '')
def T(e, p):
    out = []
    for s in e.get('claims', {}).get(p, []):
        v = s['mainsnak'].get('datavalue', {}).get('value')
        if isinstance(v, dict) and 'time' in v: out.append(v['time'][1:5] if v['time'][0] == '+' else v['time'][:5])
    return '/'.join(out)
def R(e, p):
    out = []
    for s in e.get('claims', {}).get(p, []):
        v = s['mainsnak'].get('datavalue', {}).get('value')
        if isinstance(v, dict) and 'id' in v:
            q = v['id']; out.append(rl.get(q) or (L(ent[q]) if q in ent else q))
    return out
def N(ids): return [lab.get(x.strip(), x.strip()) for x in ids.split('|') if x.strip()]
rows = []
for n, ((g, q), links) in enumerate(sorted(pairs.items())):
    f, fa, e = fam.get(g, {}), fac.get(g, {}), ent.get(q, {})
    rows.append({"n": n, "geni": g, "qid": q, "links": sorted(links),
        "G": {"name": lab.get(g, ''), "b": fa.get('birth_date_raw', ''), "d": fa.get('death_date_raw', ''), "sex": fa.get('sex', ''),
              "f": N(f.get('fathers', '')), "m": N(f.get('mothers', '')), "s": N(f.get('spouses', '')), "c": N(f.get('children', ''))},
        "W": {"name": L(e), "desc": (e.get('descriptions', {}).get('en') or {}).get('value', ''), "b": T(e, 'P569'), "d": T(e, 'P570'),
              "geni": [s['mainsnak'].get('datavalue', {}).get('value') for s in e.get('claims', {}).get('P2600', [])],
              "f": R(e, 'P22'), "m": R(e, 'P25'), "s": R(e, 'P26'), "c": R(e, 'P40'), "missing": 'missing' in e}})
json.dump(rows, open(SP + "/zipper-pairs-behind-wikidata-links.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(rows), "pairs written")
