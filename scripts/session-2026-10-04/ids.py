# Read-only: every P2600/P2889 claim the account added (wbcreateclaim) since a date. Decides nothing.
import json, re, sys, csv, time, urllib.request, urllib.parse
UA = "genealogy-session/1.0 (emma@topazcomputing.com)"
p = {"action": "query", "list": "usercontribs", "ucuser": "日巫女", "uclimit": 500, "ucstart": sys.argv[1],
     "ucdir": "newer", "format": "json", "ucprop": "title|timestamp|comment|ids"}
w = csv.writer(open(sys.argv[2], "w", newline="", encoding="utf-8"), delimiter="\t")
w.writerow(["timestamp", "item", "property", "value", "revid", "batch"])
cont, n, k = {}, 0, 0
while True:
    for i in range(6):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({**p, **cont}), headers={"User-Agent": UA}), timeout=90)); break
        except Exception: time.sleep(15 * (i + 1))
    for c in d["query"]["usercontribs"]:
        n += 1
        m = re.search(r"wbcreateclaim-create.*?\[\[Property:(P2600|P2889)\]\]: (\S+?)(?:,|$)", c["comment"])
        if m:
            b = re.search(r"batch/(\d+)|temporary_batch_(\d+)", c["comment"])
            w.writerow([c["timestamp"], c["title"], m.group(1), m.group(2), c["revid"], b.group(0) if b else ""]); k += 1
    if "continue" not in d: break
    cont = d["continue"]
print("done", n, "edits;", k, "id claims", flush=True)
