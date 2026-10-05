# Every relationship claim the account created in a NUMBERED QuickStatements batch whose value is the item
# edited just before it in that batch (the LAST-resolves-to-last-edited signature), after a creation.
import json, re, sys, csv, time, urllib.request, urllib.parse, collections
UA = "genealogy-session/1.0 (emma@topazcomputing.com)"
def get(p):
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(p)
    for i in range(6):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90))
        except Exception: time.sleep(15 * (i + 1))
    raise SystemExit("failed")
p = {"action": "query", "list": "usercontribs", "ucuser": "日巫女", "uclimit": 500, "ucstart": sys.argv[1],
     "ucdir": "newer", "format": "json", "ucprop": "title|timestamp|comment|ids"}
w = csv.writer(open(sys.argv[2], "w", newline="", encoding="utf-8"), delimiter="\t")
w.writerow(["timestamp", "item", "property", "wrong_value", "created_item", "batch", "revid"])
state = {}  # batch -> (created item, previous title)
n = 0; stat = collections.Counter(); batches = collections.Counter()
cont = {}
while True:
    d = get({**p, **cont})
    for c in d["query"]["usercontribs"]:
        n += 1
        b = re.search(r"quickstatements/#/batch/(\d+)", c["comment"])
        if not b: continue
        b = b.group(1); batches[b] += 1
        cur, prev = state.get(b, (None, None))
        if "wbeditentity-create" in c["comment"]:
            state[b] = (c["title"], c["title"]); continue
        m = re.search(r"wbcreateclaim-create.*?\[\[Property:(P\d+)\]\]: \[\[(Q\d+)\]\]", c["comment"])
        if cur and m and c["title"] != cur and m.group(1) in ("P22", "P25", "P26", "P40", "P3373"):
            if m.group(2) == prev and m.group(2) != cur:
                w.writerow([c["timestamp"], c["title"], m.group(1), m.group(2), cur, b, c["revid"]]); stat["wrong"] += 1
            elif m.group(2) == cur: stat["right"] += 1
        state[b] = (cur, c["title"])
    if "continue" not in d: break
    cont = d["continue"]
    if n % 20000 < 500: print(n, c["timestamp"], dict(stat), flush=True)
print("done", n, dict(stat), dict(batches), flush=True)
