"""Part 3 of the Geni-drift item: each of the 58 items' live revision history, read from Wikidata.

For each item in `reports/geni-drift-versions-2026-10-08.csv`: creation time, then every later edit (time, user,
the edit summary Wikibase writes, e.g. "wbsetclaim-create ... [[Property:P22]]: [[Q...]]"), with item ids in the
summaries resolved to labels. Writes `reports/geni-drift-history-2026-10-08.csv`. Read-only.

    python scripts/session-2026-10-08/drift-history.py
"""
import csv, json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "genealogy-review/1.0 (emma)"}
OUT = ROOT / "reports" / "geni-drift-history-2026-10-08.csv"


def api(params):
    u = "https://www.wikidata.org/w/api.php?format=json&" + urllib.parse.urlencode(params)
    for i in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))
        except Exception:
            time.sleep(10 * (i + 1))
    raise SystemExit("API failed")


def main():
    rows = list(csv.DictReader(open(ROOT / "reports" / "geni-drift-versions-2026-10-08.csv", encoding="utf-8")))
    hist = {}
    for r in rows:
        d = api({"action": "query", "prop": "revisions", "titles": r["qid"], "rvlimit": 500, "rvdir": "newer",
                 "rvprop": "timestamp|user|comment"})
        hist[r["qid"]] = next(iter(d["query"]["pages"].values())).get("revisions", [])
        time.sleep(0.5)
    qs = sorted({q for revs in hist.values() for v in revs for q in re.findall(r"\[\[(Q\d+)\]\]", v.get("comment", ""))})
    lab = {}
    for i in range(0, len(qs), 50):
        d = api({"action": "wbgetentities", "ids": "|".join(qs[i:i + 50]), "props": "labels", "languages": "mul|en"})
        for k, e in d.get("entities", {}).items():
            l = e.get("labels") or {}
            lab[k] = (l.get("mul") or l.get("en") or {}).get("value", k)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["qid", "timestamp", "user", "edit"])
        for r in rows:
            for v in hist[r["qid"]]:
                c = re.sub(r"\[\[(Q\d+)\]\]", lambda m: f"{m.group(1)} {lab.get(m.group(1), '')}", v.get("comment", ""))
                c = re.sub(r"\[\[Property:(P\d+)\]\]", r"\1", c).replace(", #quickstatements", "")
                c = re.sub(r"; #temporary_batch_\d+", "", c)
                w.writerow([r["qid"], v["timestamp"], v["user"], c[:300]])
    print("wrote", OUT.name, sum(len(v) for v in hist.values()), "revisions")


if __name__ == "__main__":
    main()
