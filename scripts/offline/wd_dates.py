"""Read birth/death years from Wikidata (read only) for every person in a wikidata_to_gedcom
export, and write them back into a copy of the GEDCOM. No login, no edits.
Usage: python wd_dates.py IN.ged OUT.ged CACHE.json"""
import sys, re, json, os, time, urllib.request, urllib.parse
UA = 'genealogy-offline-analysis/1.0 (read-only; https://github.com/EmmaLeonhart/genealogy)'
src, out, cache_path = sys.argv[1:4]
lines = open(src, encoding='utf-8').read().splitlines()
qids = sorted(set(re.findall(r'wikidata\.org/wiki/(Q\d+)', '\n'.join(lines))))
cache = json.load(open(cache_path, encoding='utf-8')) if os.path.exists(cache_path) else {}
todo = [q for q in qids if q not in cache]
print(len(qids), 'qids;', len(todo), 'to fetch', file=sys.stderr)
def year(claims, prop):
    for c in claims.get(prop, []):
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value', {})
        m = re.match(r'([+-])(\d+)-', v.get('time', ''))
        if m:
            y = int(m.group(2)); return -y if m.group(1) == '-' else y
    return None
for i in range(0, len(todo), 50):
    batch = todo[i:i + 50]
    url = 'https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbgetentities', 'ids': '|'.join(batch), 'props': 'claims', 'format': 'json'})
    for attempt in range(5):
        try:
            data = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60)); break
        except Exception as e:
            print('retry', e, file=sys.stderr); time.sleep(5 * (attempt + 1))
    for q, ent in data.get('entities', {}).items():
        cl = ent.get('claims', {})
        cache[q] = [year(cl, 'P569'), year(cl, 'P570')]
    json.dump(cache, open(cache_path, 'w', encoding='utf-8'))
    time.sleep(0.5)
# write dates into the GEDCOM: insert BIRT/DEAT after each person's NOTE line
res = []
for l in lines:
    res.append(l)
    m = re.match(r'1 NOTE https://www\.wikidata\.org/wiki/(Q\d+)', l)
    if m and m.group(1) in cache:
        b, d = cache[m.group(1)]
        if b is not None: res += ['1 BIRT', f'2 DATE {abs(b)}{" BC" if b < 0 else ""}']
        if d is not None: res += ['1 DEAT', f'2 DATE {abs(d)}{" BC" if d < 0 else ""}']
open(out, 'w', encoding='utf-8').write('\n'.join(res) + '\n')
n = sum(1 for q in qids if cache.get(q, [None, None]) != [None, None])
print('with a date:', n, 'of', len(qids), file=sys.stderr)
