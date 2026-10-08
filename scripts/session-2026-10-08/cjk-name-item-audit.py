"""Every name item the account created, and which carry Han, kana or Hangul in `en` or `mul` (Emma, 2026-10-08).

Reads the account's page creations (all of them), keeps items whose P31 is a name class, and writes
reports/cjk-name-item-audit-2026-10-08.tsv: qid, created, kind, en, mul, leak (yes/no), redirect target if merged.
    python scripts/session-2026-10-08/cjk-name-item-audit.py
"""
import collections, csv, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "cjk-name-item-audit-2026-10-08.tsv"
UA = {"User-Agent": "genealogy-check/1.0 (emma@topazcomputing.com)"}
USER = "日巫女"
KIND = {"Q101352": "family", "Q202444": "given", "Q12308941": "given", "Q11879590": "given", "Q3409032": "given",
        "Q110874": "patronymic", "Q130444148": "patronymic", "Q130444179": "patronymic",
        "Q10673705": "patronymic", "Q10476255": "patronymic"}
CJK = re.compile(r"[぀-ヿ㐀-鿿가-힯豈-﫿]")


def get(url):
    for i in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120))
        except Exception:
            time.sleep(10 * (i + 1))
    raise SystemExit("API failed: " + url[:120])


pages, cont = [], None
while True:
    u = ("https://www.wikidata.org/w/api.php?action=query&format=json&list=usercontribs&ucshow=new&uclimit=500"
         "&ucnamespace=0&ucprop=title|timestamp&ucuser=" + urllib.parse.quote(USER))
    d = get(u + ("&uccontinue=" + urllib.parse.quote(cont) if cont else ""))
    pages += [(c["title"], c["timestamp"][:10]) for c in d["query"]["usercontribs"]]
    cont = d.get("continue", {}).get("uccontinue")
    if not cont:
        break
when = dict(pages)
ids = [q for q, _ in pages]
rows = []
for i in range(0, len(ids), 50):
    d = get("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&redirects=yes&props=labels|claims"
            "&languages=en|mul&ids=" + "|".join(ids[i:i + 50]))
    for asked, e in d.get("entities", {}).items():
        if "missing" in e:
            continue
        kinds = sorted({KIND[s["mainsnak"].get("datavalue", {}).get("value", {}).get("id")]
                        for s in e.get("claims", {}).get("P31", [])
                        if s["mainsnak"].get("datavalue", {}).get("value", {}).get("id") in KIND})
        if not kinds:
            continue
        en = e.get("labels", {}).get("en", {}).get("value", "")
        mul = e.get("labels", {}).get("mul", {}).get("value", "")
        rows.append((asked, when.get(asked, ""), ",".join(kinds), en, mul,
                     "yes" if CJK.search(en + mul) else "no", e.get("id") if e.get("id") != asked else ""))
    time.sleep(0.3)
with open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["qid", "created", "kind", "en", "mul", "cjk_leak", "merged_into"])
    w.writerows(rows)
leaks = [r for r in rows if r[5] == "yes"]
print(f"{len(ids)} creations; {len(rows)} name items; {len(leaks)} with CJK in en or mul "
      f"({sum(1 for r in leaks if r[6])} of them already merged away)")
print("by date:", sorted(collections.Counter(r[1] for r in leaks).items()))
print("by kind:", collections.Counter(r[2] for r in leaks).most_common())
for r in leaks:
    print(*r)
