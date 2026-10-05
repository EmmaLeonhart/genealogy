import csv, json, time, urllib.request, urllib.parse, sys
UA = "genealogy-session/1.0 (emma@topazcomputing.com)"
ACC = "日巫女"
rows = [(r['x'].rsplit('/',1)[1], r['m'].rsplit('/',1)[1]) for r in csv.DictReader(open(sys.argv[1], encoding='utf-8'))]
def get(params):
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(params)
    for i in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60))
        except Exception as e:
            time.sleep(10 * (i + 1))
    raise SystemExit("failed " + url)
out = csv.writer(open(sys.argv[2], 'w', newline='', encoding='utf-8'), delimiter='\t')
out.writerow(['item', 'male_mother', 'how', 'timestamp', 'comment'])
for x, m in rows:
    d = get({"action": "query", "prop": "revisions", "titles": x, "rvprop": "user|timestamp|comment",
             "rvlimit": 500, "format": "json"})
    revs = next(iter(d['query']['pages'].values())).get('revisions', [])
    hit = None
    for r in revs:
        if r.get('user') == ACC and 'P25' in r.get('comment', '') and m in r.get('comment', ''):
            hit = ('claim', r['timestamp'], r['comment'])
    if not hit and revs and revs[-1].get('user') == ACC and len(revs) < 500:
        hit = ('created-by-account', revs[-1]['timestamp'], revs[-1].get('comment', ''))
    if hit:
        out.writerow([x, m, *hit]); print(x, m, hit[0], hit[1], flush=True)
    time.sleep(0.3)
