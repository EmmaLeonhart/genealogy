"""Hold out of a batch every CREATE block whose entity is already live on Wikidata: a person by P2600/P2889
(haswbstatement), a name item by its mul label plus one of its P31 classes. Only the creation block goes: from
its comment line (if any) through the blank line that ends it. Writes <batch>-held.txt and
<batch>-held-out.tsv next to the input.
Usage: python scripts/session-2026-10-06/hold-live-creations.py reports/wikidata-garborg-day-manual.txt"""
import json, re, sys, time, urllib.parse, urllib.request
UA = {"User-Agent": "genealogy-batch-precheck/1.0 (emma@topazcomputing.com)"}
src = sys.argv[1]
lines = open(src, encoding="utf-8").read().split("\n")

def api(params):
    u = "https://www.wikidata.org/w/api.php?format=json&" + urllib.parse.urlencode(params)
    for i in range(8):  # the search API rate-limits bursts: back off up to ~4 minutes in all
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA)))
        except Exception:
            time.sleep(5 * (i + 1))
    raise SystemExit("API failed: " + u)

def live_by_id(prop, value):
    d = api({"action": "query", "list": "search", "srsearch": f"haswbstatement:{prop}={value}"})
    return [h["title"] for h in d["query"]["search"]]

def live_name_item(label, classes):
    # The search API's `inlabel:` instead of SPARQL: on 2026-10-06 WDQS was held to 1 request a minute during an
    # outage. `inlabel` matches words, so each hit is checked for the exact `mul` label.
    hits = set()
    for c in classes:
        d = api({"action": "query", "list": "search", "srsearch": f'inlabel:"{label}@mul" haswbstatement:P31={c}'})
        hits |= {h["title"] for h in d["query"]["search"]}
    if not hits:
        return []
    ents = api({"action": "wbgetentities", "ids": "|".join(sorted(hits)[:50]), "props": "labels",
                "languages": "mul"})["entities"]
    return sorted(q for q, e in ents.items() if e.get("labels", {}).get("mul", {}).get("value") == label)


i, keep, held = 0, [], []
while i < len(lines):
    if lines[i] == "CREATE":
        start = i - 1 if i > 0 and lines[i - 1].startswith("#") and keep and keep[-1] == lines[i - 1] else i
        j = i
        while j < len(lines) and lines[j] != "":
            j += 1
        block = "\n".join(lines[i:j])
        found, why = [], ""
        for prop in ("P2600", "P2889"):
            m = re.search(rf'^LAST\t{prop}\t"([^"]+)"', block, re.M)
            if m:
                found, why = live_by_id(prop, m.group(1)), f"{prop} {m.group(1)}"
                break
        else:
            lab = re.search(r'^LAST\tLmul\t"([^"]+)"', block, re.M)
            classes = re.findall(r"^LAST\tP31\t(Q\d+)", block, re.M)
            if lab and "Q5" not in classes:
                found, why = live_name_item(lab.group(1), classes), f"name item {lab.group(1)}"
        time.sleep(0.3)
        if found:
            if start != i:
                keep.pop()
            label = (re.search(r'^LAST\tL(?:en|mul)\t"([^"]+)"', block, re.M) or [None, ""])[1]
            held.append((label, why, " ".join(found)))
            i = j + 1  # the blank line after the block goes with it
            continue
    keep.append(lines[i])
    i += 1
base = src.rsplit(".", 1)[0]
open(base + "-held.txt", "w", encoding="utf-8", newline="\n").write("\n".join(keep))
with open(base + "-held-out.tsv", "w", encoding="utf-8", newline="\n") as f:
    f.write("label\tkey\tlive_items\n")
    for h in held:
        f.write("\t".join(h) + "\n")
print(f"held out {len(held)} creation blocks; {sum(l == 'CREATE' for l in keep)} creations left")
