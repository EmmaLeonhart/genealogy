"""Save every Wikidata item that is `instance of` patronymic (Q110874).

Emma, 2026-08-15: *"for the 119 patronymic items, please save them. Save the
patronymic items and also the items above, first names and stuff like that, so
that we can be a bit clear about this stuff. Because I don't want us to be
creating duplicates of things."*

Given-name and family-name items our people reference are already saved, in
`reports/name-items.csv` (132,569 rows). **Patronymic items were the gap** — the
local store is a Geni-shaped slice of people and holds none of them.

One aggregate SPARQL query, under the same authorisation as the property survey.
Writes `reports/patronymic-items.csv`.
"""
import csv, json, urllib.parse, urllib.request
from collections import defaultdict
from pathlib import Path

Q = """
SELECT ?item ?itemLabel ?itemDescription ?native ?lang ?langLabel
       ?based ?basedLabel ?other ?otherLabel WHERE {
  ?item wdt:P31 wd:Q110874 .
  OPTIONAL { ?item wdt:P1705 ?native }
  OPTIONAL { ?item wdt:P407  ?lang }
  OPTIONAL { ?item wdt:P144  ?based }
  OPTIONAL { ?item wdt:P5278 ?other }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
"""
url = "https://query.wikidata.org/sparql"
data = urllib.parse.urlencode({"query": Q, "format": "json"}).encode()
req = urllib.request.Request(url, data=data, headers={
    "User-Agent": "geni-genealogy-research/1.0 (emma@topazcomputing.com)",
    "Accept": "application/sparql-results+json"})
with urllib.request.urlopen(req, timeout=180) as r:
    res = json.load(r)

def v(b, k):
    x = b.get(k, {}).get("value", "")
    return x.rsplit("/", 1)[-1] if x.startswith("http://www.wikidata.org/entity/") else x

merged = {}
multi = defaultdict(lambda: defaultdict(set))
for b in res["results"]["bindings"]:
    qid = v(b, "item")
    merged.setdefault(qid, {
        "qid": qid,
        "label": v(b, "itemLabel"),
        "description": v(b, "itemDescription"),
        "native_label": v(b, "native"),
        "language": v(b, "langLabel"),
        "language_qid": v(b, "lang"),
    })
    if v(b, "based"):
        multi[qid]["based_on"].add(f"{v(b,'based')} ({v(b,'basedLabel')})")
    if v(b, "other"):
        multi[qid]["other_gender"].add(f"{v(b,'other')} ({v(b,'otherLabel')})")

rows = []
for qid, row in merged.items():
    row["based_on"] = " | ".join(sorted(multi[qid]["based_on"]))
    row["other_gender_form"] = " | ".join(sorted(multi[qid]["other_gender"]))
    rows.append(row)
rows.sort(key=lambda r: (not r["based_on"], r["label"]))

out = Path(__file__).resolve().parents[0]
dest = Path(r"C:\Users\Emma\Documents\GitHub\geni\reports\patronymic-items.csv")
with dest.open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["qid", "label", "description",
                                       "native_label", "language",
                                       "language_qid", "based_on",
                                       "other_gender_form"])
    w.writeheader(); w.writerows(rows)
print(f"{len(rows)} patronymic items -> {dest}")
print(f"  {sum(1 for r in rows if r['based_on'])} carry P144 based on")
print(f"  {sum(1 for r in rows if r['other_gender_form'])} carry P5278 other-gender form")
for r in rows[:6]:
    print(f"    {r['qid']:<10} {r['label']:<22} based on: {r['based_on'] or '-'}")
