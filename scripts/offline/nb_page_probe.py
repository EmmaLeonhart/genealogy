import json, sys, urllib.request, urllib.parse
ID = '1d0d79060c1eb690db15c5dbb0708dc3'
def pages(q):
    url = f'https://api.nb.no/catalog/v1/items/{ID}/contentfragments?' + urllib.parse.urlencode({'q': q, 'fragments': 50})
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'genealogy-offline-analysis/1.0 (read-only)'}), timeout=60))
    return sorted({f.get('pageid', '')[-4:] for f in d.get('contentFragments', [])})
for q in sys.argv[1:]:
    p = pages(q); print(f'{q!r}: {"ON PAGE 64" if "0064" in p else "-"}  {p[:12]}')
