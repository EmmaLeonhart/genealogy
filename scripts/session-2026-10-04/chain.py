# For the account's contribs in a window: after each item creation, look at the back-reference claims
# (claims on OTHER items made in the same batch right after) and see whether their value is the new item.
import json, re, sys, urllib.request, urllib.parse, collections
UA = "genealogy-session/1.0 (emma@topazcomputing.com)"
start, end = sys.argv[1], sys.argv[2]
cs, cont = [], {}
while True:
    p = {"action": "query", "list": "usercontribs", "ucuser": "日巫女", "uclimit": 500, "ucstart": start,
         "ucend": end, "format": "json", "ucprop": "title|timestamp|comment", "ucdir": "newer"}
    pass
    p.update(cont)
    d = json.load(urllib.request.urlopen(urllib.request.Request(
        "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(p), headers={"User-Agent": UA})))
    cs += d["query"]["usercontribs"]
    if "continue" not in d or len(cs) > 6000: break
    cont = d["continue"]
stat = collections.Counter(); bad = []
cur = None
for c in cs:
    b = re.search(r"batch/(\d+)|temporary_batch_(\d+)", c["comment"]); b = b.group(0) if b else None
    if "wbeditentity-create" in c["comment"]:
        cur = (c["title"], b); continue
    m = re.search(r"wbcreateclaim-create.*?\[\[Property:(P\d+)\]\]: \[\[(Q\d+)\]\]", c["comment"])
    if cur and m and b == cur[1] and c["title"] != cur[0] and m.group(1) in ("P22", "P25", "P26", "P40", "P3373"):
        ok = m.group(2) == cur[0]
        stat[(b.split('/')[0][:9], ok)] += 1
        if not ok: bad.append((c["timestamp"], c["title"], m.group(1), m.group(2), "new=" + cur[0], b))
print(len(cs), "contribs", sum("wbeditentity-create" in c["comment"] for c in cs), "creates"); print(stat)
for x in bad[:15]: print(*x)
print("bad total", len(bad))
