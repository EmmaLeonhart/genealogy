"""For each wrong-script name item in `reports/name-links-wrong-script-2026-10-06.tsv`, count the items live
that carry it as `P735`/`P734`/`P5056`, how many of them are ours (`reports/garborg-qids.tsv`), and who added
it to ours: the account (a `#quickstatements` edit) or somebody else. Writes
`reports/name-links-wrong-script-live-2026-10-06.tsv` (one row per our item and link).

    python scripts/session-2026-10-06/name-links-live-count.py
"""
import csv, json, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "genealogy-audit (https://github.com/EmmaLeonhart/genealogy)",
      "Accept": "application/sparql-results+json"}
PROP = {"given": "P735", "family": "P734", "patronymic": "P5056"}

ours = {r["qid"] for r in csv.DictReader(open(ROOT / "reports/garborg-qids.tsv", encoding="utf-8"), delimiter="\t")}
wrong = list(csv.DictReader(open(ROOT / "reports/name-links-wrong-script-2026-10-06.tsv", encoding="utf-8"), delimiter="\t"))
pairs = sorted({(PROP[r["usage"]], r["linked_qid"], r["token"]) for r in wrong})


def get(url, headers=UA):
    for _ in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120))
        except Exception:                                            # noqa: BLE001
            time.sleep(10)
    return {}


summary, detail = [], []
for prop, qid, token in pairs:
    q = f"SELECT ?item WHERE {{ ?item wdt:{prop} wd:{qid} }}"
    data = get("https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q}))
    items = [b["item"]["value"].rsplit("/", 1)[1] for b in data.get("results", {}).get("bindings", [])]
    mine = [i for i in items if i in ours]
    summary.append((token, prop, qid, len(items), len(mine)))
    for item in mine:
        revs = get("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
            {"action": "query", "prop": "revisions", "titles": item, "rvlimit": "500",
             "rvprop": "timestamp|user|comment", "format": "json"}))
        added_by, when = "", ""
        for page in revs.get("query", {}).get("pages", {}).values():
            for r in page.get("revisions", []):
                c = r.get("comment", "")
                if f"[[Property:{prop}]]: [[{qid}]]" in c and ("create" in c or "wbsetclaim" in c):
                    added_by, when = r.get("user", ""), r["timestamp"]   # oldest wins: revisions are newest first
        detail.append((item, token, prop, qid, added_by, when))
        time.sleep(0.3)
    time.sleep(1)

with open(ROOT / "reports/name-links-wrong-script-live-2026-10-06.tsv", "w", encoding="utf-8", newline="") as f:
    f.write("item\ttoken\tproperty\tlinked_qid\tadded_by\tadded_at\n")
    for d in sorted(detail, key=lambda d: (d[1], int(d[0][1:]))):
        f.write("\t".join(d) + "\n")
summary.sort(key=lambda s: -s[4])
print(f"{len(pairs)} wrong-script links; live on {sum(s[3] for s in summary)} items, "
      f"{sum(s[4] for s in summary)} of them ours")
for s in summary[:30]:
    print(*s, sep="\t")
